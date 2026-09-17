#!/usr/bin/env python3
"""Build a static clone of ariyana-studio.webflow.io into site/.

The reference's own served HTML is the source. Rather than re-authoring the
markup, each page is transformed in place:

  * every cdn.prod.website-files.com asset  ->  /assets/ref/<file>
  * the Webflow shared stylesheet           ->  /assets/css/main.css
  * jQuery, the Webflow runtime and IX2     ->  removed
  * GSAP / ScrollTrigger / SplitText / Lenis -> vendored under /assets/vendor
  * the site's inline Lenis snippet          -> /assets/js/motion.js

That keeps structure, palette, type scale and spacing identical by
construction; only the behaviour layer is rewritten, against the interaction
values measured off the live site (docs/REFERENCE-ANIMATIONS.md).

Every borrowed asset keeps a data-placeholder attribute so it stays greppable.
"""

import hashlib
import json
import itertools
import re
import shutil

from PIL import Image
import sys
import urllib.parse
from pathlib import Path
import pathlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helv_content as HC
import influencer_page as IP  # noqa: E402
import service_page as SP  # noqa: E402
import technology_page as TP  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scratchpad" / "ariyana"
PAGES = SRC / "pages"
SITE = ROOT / "site"
REF_ASSETS = ROOT / "capture" / "reference-assets"

CDN = "https://cdn.prod.website-files.com"

# The one sanctioned divergence: the home hero is white and carries the
# approved 3D character rather than the reference's dark VR photograph.
# Set to False for a hero that matches the reference exactly.
HERO_EXCEPTION = True
# The home hero film (client, 17 Sep 2026) and Vimeo's own 1280x720 still of it,
# shown until the player's first frame and whenever the film cannot play.
HERO_VIMEO = "1227814361"
HERO_POSTER = ("https://i.vimeocdn.com/video/2202126783-9d94dc1b8e8e84d09aa22d7d6bdb47d94"
               "a9bd744966854b7e9efc4e63f1dcd57-d_1280?region=us")

# The WebGL character is ON, at the client's request.
#
# It was off because the mesh comes from single-image reconstruction, which can
# only invent everything the source photograph does not show — the back of the
# head, the depth of the face. It holds inside about 20 degrees and falls apart
# past 45.
#
# That limit has not gone away; it is contained instead. hero3d.js caps yaw at
# 20 degrees and pitch at 7 for exactly this reason, so the character turns
# toward the cursor without ever reaching the angle where the reconstruction
# shows. A properly modelled and rigged character would let those caps rise —
# until then the cap is the quality control.
#
# Everything about it is still a progressive upgrade: no WebGL, a slow link, a
# decode error, reduced-motion, touch or data-saver all leave the flat cutout
# in place, which is the real artwork at full quality.
HERO_3D = False   # retired: the hero character is a film now

# page slug -> output directory (None = site root)
# The blog is pulled for now, so /blogs is not built and every link to it or to
# a post is stripped below.
ROUTES = {
    "home": "",
    "about-us": "about-us",
    "projects": "projects",
    "service": "service",
    "contact-us": "contact-us",
    "404": None,          # written as site/404.html
}


# ------------------------------------------------------------------ assets

def check_css(path) -> None:
    """Fail the build on unbalanced braces in a stylesheet.

    A single stray `}` does not throw anything — the browser silently stops
    applying rules from that point and every declaration after it vanishes.
    That is how the header lockup ended up ignoring a rule that was plainly
    present in the file, and it cost a long detour to find. Cheap to check,
    expensive to miss.
    """
    css = path.read_text(encoding="utf-8")
    stripped = re.sub(r"/\*[\s\S]*?\*/", "", css)
    depth = stripped.count("{") - stripped.count("}")
    if depth:
        raise SystemExit(
            "%s: unbalanced braces (%+d). A stray closer silently disables every "
            "rule after it." % (path.name, depth))
    if css.count("/*") != css.count("*/"):
        raise SystemExit("%s: unterminated comment" % path.name)


def asset_name(url: str) -> str:
    """Local filename for a CDN url. Decode first — some encode / as %2F."""
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    return path.split("/")[-1].replace(" ", "-")


def copy_assets() -> int:
    out = SITE / "assets" / "ref"
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(REF_ASSETS.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            shutil.copy2(f, out / f.name)
            n += 1
    return n


def check_spacing_tokens() -> int:
    """Fail the build on a spacing token the reference never defines.

    The scale runs 4px..80px in fours, then 100 and 120 — there is no 96px.
    A `var()` naming a property that does not exist is invalid at
    computed-value time, so the whole declaration is dropped and the property
    falls back to its inherited or initial value. Silently: no console warning,
    no visible error, just a padding that is zero.

    Two rules had been sitting dead because of exactly that — the technology
    page's bank padding and the clearance under a film hero — and neither
    announced itself. So the build checks now.
    """
    ref = (SITE / "assets" / "css" / "main.css").read_text(encoding="utf-8")
    defined = set(re.findall(r"(--_spacing---spacing-primitives--\d+px)\s*:", ref))
    mine_path = SITE / "assets" / "css" / "clone.css"
    bad = []
    for n, line in enumerate(mine_path.read_text(encoding="utf-8").splitlines(), 1):
        for tok in re.findall(r"var\((--_spacing---spacing-primitives--\d+px)\)", line):
            if tok not in defined:
                bad.append((n, tok))
    for n, tok in bad:
        print(f"  ! clone.css:{n} uses undefined {tok}")
    if bad:
        sizes = sorted(int(re.search(r"(\d+)px", d).group(1)) for d in defined)
        raise SystemExit("css: %d undefined spacing token(s) — defined sizes are %s"
                         % (len(bad), sizes))
    return len(defined)


def build_css() -> int:
    """Localise the reference stylesheet: rewrite every url() to /assets/ref."""
    css = (SRC / "main.css").read_text(encoding="utf-8")

    def sub(m):
        quote, url = m.group(1), m.group(2)
        if url.startswith("data:"):
            return m.group(0)
        if url.startswith("http"):
            return f"url({quote}/assets/ref/{asset_name(url)}{quote})"
        return m.group(0)

    css = re.sub(r'url\((["\']?)([^)"\']+)\1\)', sub, css)

    # The two brand faces as WOFF2 rather than the reference's TTFs: DM Sans
    # variable 233KB -> ~60KB, Bebas Neue 56KB -> ~10KB. Cut from the same
    # files by build/site_fonts.py (all axes kept, subset to every character
    # the site uses), so nothing renders differently. Falls back to the TTF if
    # the WOFF2 has not been generated.
    for ttf, woff in (("68f262b1b60fe57e398c9c09_DMSans-VariableFont_opsz,wght.ttf", "dm-sans-site.woff2"),
                      ("68efdbc172d0ac625d40c65f_BebasNeue-Regular.ttf", "bebas-neue-site.woff2")):
        if (SITE / "assets" / "fonts" / woff).exists():
            old = f'url(/assets/ref/{ttf})format("truetype")'
            if old not in css:
                raise SystemExit(f"build_css: font url not found for {ttf}")
            css = css.replace(old, f'url(/assets/fonts/{woff})format("woff2")')

    # Webflow ships this variable name with an escaped "<deleted|…>" suffix that
    # some parsers choke on. It resolves fine in browsers; left as-is.
    out = SITE / "assets" / "css"
    out.mkdir(parents=True, exist_ok=True)
    (out / "main.css").write_text(css, encoding="utf-8")
    return len(css)


# ------------------------------------------------------------------- html

# scripts to strip entirely
DROP_SRC = (
    "jquery",
    "webflow.schunk",
    "webflow.24c5dbb3",
    "/js/webflow",
    "challenges.cloudflare.com",
    "google-analytics", "googletagmanager",
)

VENDOR = [
    "/assets/vendor/gsap.min.js",
    "/assets/vendor/ScrollTrigger.min.js",
    "/assets/vendor/SplitText.min.js",
    "/assets/vendor/lenis.min.js",
]

# internal Webflow routes -> our directory layout
LINKS = {
    "/": "/",
    "/about-us": "/about-us/",
    "/projects": "/projects/",
    "/service": "/service/",
    "/contact-us": "/contact-us/",
    "/404": "/404.html",
}


HELV = "/assets/helv"
CLIENTS_DIR = "/assets/clients"
CHAR_BTS = "/assets/character-bts"
CARD_CLIENTS = json.loads((ROOT / "content" / "logocards.json").read_text(encoding="utf-8"))

# The client roster is the 63 artboards the client supplied, processed by
# build/client_logos.py. Everything that used to be hand-listed here now comes
# from that one source, so there is a single place a logo can be wrong.
_ROSTER = json.loads((ROOT / "content" / "clients.json").read_text(encoding="utf-8"))
ALL_CLIENTS = [(c["slug"], c["name"]) for c in _ROSTER]

# The marquee runs the whole roster — it is a scroll, so length is a feature.
BANNER_CLIENTS = ALL_CLIENTS

# The black wall and the fan hold the marks a visitor will actually recognise,
# because those two are static: six and ten slots that have to earn their space.
_MAJORS = ["pfizer", "l-oreal-dermatological-beauty", "nahdi", "astrazeneca",
           "bayer", "sanofi", "abbott", "merck", "msd", "molnlycke", "zoetis",
           "vichy", "la-roche-posay", "cerave", "hikma", "menarini-group",
           "isuzu", "mondelez-international"]
_BY_SLUG = dict(ALL_CLIENTS)
_MAJOR_PAIRS = [(sl, _BY_SLUG[sl]) for sl in _MAJORS if sl in _BY_SLUG]

WALL_CLIENTS = _MAJOR_PAIRS[:6]
FAN_CLIENTS = _MAJOR_PAIRS[:10]


def helv_logos(html: str, page: str = "") -> str:
    """Swap every Ariyana mark for HelloVoice's.

    Covers the nav brand, the preloader, the fullscreen menu, the footer
    wordmark, the client marquee, the knocked-out wall on black, the
    Trusted-by-Leaders fan and the favicons.
    """
    wordmark = (f'<img src="{HELV}/logo.webp" srcset="{HELV}/logo@2x.webp 2x" '
                'alt="HelloVoice" class="helv_wordmark" width="760" height="166"/>')
    knockout = (f'<img src="{HELV}/logo-knockout.webp" '
                f'srcset="{HELV}/logo-knockout@2x.webp 2x" alt="HelloVoice" '
                'class="helv_wordmark is-knockout" width="760" height="166"/>')

    # The home hero is a dark red ground, so its nav takes the knockout; every
    # other page uses the reference's own light nav and takes the colour mark.
    # the home hero and the works hero are both dark grounds now
    nav_mark = knockout if page in ("home", "projects") else wordmark
    html = re.sub(r'<p class="logo_text[^"]*">\s*//\s*ARIYANA\s*</p>', nav_mark, html)
    # preloader sits on near-black
    html = re.sub(r'(<div data-preloader-logo="" class="logo_text">)\s*//ARIYANA\s*(</div>)',
                  r'\1' + knockout + r'\2', html)
    # The fullscreen menu's mark is a watermark, not a logo: 19vw type at
    # opacity .3 sitting behind the links. An image at that scale would fight
    # them, so like the footer it stays as type.
    html = re.sub(r'<p class="canvas_logo">\s*ARiyana STUDIO\s*</p>',
                  '<p class="canvas_logo">HELLOVOICE</p>', html)
    # the giant footer wordmark is a type treatment, clipped to a gradient —
    # keep it as text so the clip survives
    html = html.replace('<p class="logo_big_text">// ARIYANA</p>',
                        '<p class="logo_big_text">// HELLOVOICE</p>')

    # the six marks on the black wall, knocked out to white by CSS
    wall = iter(WALL_CLIENTS)
    def wall_sub(m):
        try:
            slug, name = next(wall)
        except StopIteration:
            return m.group(0)
        return (f'<img src="{CLIENTS_DIR}/{slug}.webp" '
                f'srcset="{CLIENTS_DIR}/{slug}@2x.webp 2x" alt="{name}" '
                'loading="lazy" class="brand_logo is-helv"/>')
    html = re.sub(r'<img[^>]*class="brand_logo"[^>]*/?>', wall_sub, html)

    # ---- TEST: the client's three supplied logo cards -------------------
    # These are full-bleed brand cards — a coloured ground with the mark
    # knocked out — which is exactly what the reference's own tiles are. That
    # is why they can rotate with the ring and still look designed, and why
    # they need no disc, no counter-rotation and no white padding.
    #
    # Ten slots, and the client has now supplied exactly ten cards — so the
    # ring shows ten different brands instead of cycling three of them across
    # the wheel, which was visibly the same logo three times over.
    fan = iter([(c["slug"], c["name"]) for c in CARD_CLIENTS][:10])

    def fan_sub(m):
        try:
            slug, name = next(fan)
        except StopIteration:
            return m.group(0)
        return (f'<img src="{CLIENTS_DIR}/logocards/{slug}-sm.webp" '
                f'srcset="{CLIENTS_DIR}/logocards/{slug}.webp 2x" alt="{name}" '
                'loading="lazy" decoding="async" '
                'class="leader_circle_image is-card"/>')

    html = re.sub(r'<img[^>]*class="leader_circle_image"[^>]*/?>', fan_sub, html)

    # favicons
    html = re.sub(r'<link[^>]*rel="shortcut icon"[^>]*/?>',
                  f'<link href="/assets/icons/icon-32.png" rel="shortcut icon" type="image/png"/>', html)
    html = re.sub(r'<link[^>]*rel="apple-touch-icon"[^>]*/?>',
                  f'<link href="/assets/icons/icon-180.png" rel="apple-touch-icon"/>', html)
    return html


def brand_name(html: str) -> str:
    """Carry the name through the places a logo cannot reach.

    The giant hero wordmark, the page titles, the social meta and the legal
    line are all brand marks set as type. Only the *name* is substituted —
    the sentences around it are still Ariyana's and are listed as needing a
    rewrite in the content report.
    """
    html = html.replace(">ARIYANA STUDIO<", ">HELLOVOICE<")
    for a, b in (("ARIYANA", "HELLOVOICE"), ("Ariyana Studio", "HelloVoice"),
                 ("ARiyana STUDIO", "HelloVoice"), ("Ariyana", "HelloVoice"),
                 ("ariyana", "hellovoice")):
        html = html.replace(a, b)

    html = html.replace("© 2025 HELLOVOICE. ALL RIGHTS RESERVED.",
                        "© 2026 HELLOVOICE. ALL RIGHTS RESERVED.")
    # the site is no longer a Webflow export, so the credit is simply untrue
    html = re.sub(r'<p class="footer_legal_text">\s*POWERED BY.*?</p>', "", html, flags=re.S)

    # the reference's template suffix, and its social card
    html = html.replace(" - Webflow HTML website template", "")
    html = re.sub(r'(<meta[^>]*(?:og:image|twitter:image)[^>]*content=")[^"]*(")',
                  r'\1' + HELV + r'/og-image.jpg\2', html)
    html = re.sub(r'(content=")[^"]*(694830f92d32cafbb0ba9b4d_open-graph-image\.jpg")',
                  HELV + '/og-image.jpg"', html)
    html = html.replace("/assets/ref/694830f92d32cafbb0ba9b4d_open-graph-image.jpg",
                        HELV + "/og-image.jpg")
    return html


def strip_blog(html: str) -> str:
    """Remove the blog from every menu, footer column and link list."""
    for pat in (r'<a\b[^>]*href="/blogs"[^>]*>.*?</a>',
                r'<a\b[^>]*href="/post/[^"]*"[^>]*>.*?</a>'):
        html = re.sub(pat, "", html, flags=re.S)
    return html


def error_plate(html: str) -> str:
    """The 404's number plate is the reference's own artwork."""
    return re.sub(r'<img[^>]*error[- ]number[- ]logo[^>]*>',
                  f'<img src="{HELV}/icon-512.png" alt="HelloVoice" width="180" '
                  'height="180" class="image-contain"/>', html)


def strip_dead_links(html: str) -> str:
    """Drop links to pages this build does not carry.

    The reference's footer points at its own template utility pages — style
    guide, licences, changelog — which are not part of the agreed page set and
    would 404 here. Their wrapper is removed with them so the column does not
    keep an empty row.
    """
    html = re.sub(
        r'<a\b[^>]*href="/utilities/[^"]*"[^>]*>.*?</a>', "", html, flags=re.S)
    # the column that held them is now empty of links; drop the whole column
    html = re.sub(
        r'<div class="footer_link_col"[^>]*>(?:(?!</div></div>).)*?'
        r'utilities</p><div class="footer_link_wrapper"></div></div>',
        "", html, flags=re.S)
    return html


def tags_drive_filter(html: str) -> str:
    """Turn each card's tag links into filter controls.

    On the reference every tag is a link to its own archive page. Those pages
    are not in this build, and now that the listing filters in place they
    would be a worse answer anyway — so the tags become buttons that drive the
    filter they already describe.
    """
    def sub(m):
        label = m.group(2).strip()
        return (f'<button type="button" class="project_tag" '
                f'data-filter-to="{slug(label)}">{m.group(2)}</button>')

    return re.sub(r'<a\b[^>]*href="/project-tags/([^"]*)"[^>]*class="project_tag">(.*?)</a>',
                  sub, html, flags=re.S)


def tags_to_listing(html: str) -> str:
    """On a detail page a tag has no local grid to filter, so send it to the
    listing pre-filtered. `worksFilter` reads ?filter= on load."""
    return re.sub(
        r'<a\b([^>]*)href="/project-tags/([^"]*)"([^>]*)class="project_tag">',
        lambda m: f'<a{m.group(1)}href="/projects/?filter={m.group(2)}"{m.group(3)}class="project_tag">',
        html)


# --------------------------------------------------------- inserted sections

def client_banner() -> str:
    """A marquee of client logos, sitting directly under the hero.

    Built from the reference's own brand marks. They ship as white knockouts
    for its black brands grid, so the banner uses a dark ground too and shows
    them in their own colour — see clone.css.
    """
    def box(path, h=64):
        """Width the mark occupies at the banner's row height.

        Declared per logo from its own pixels: the marquee measures one copy's
        width to set its loop distance, and if the images have not sized yet
        that measurement is wrong and the loop jumps.
        """
        from struct import unpack
        try:
            with Image.open(path) as im:
                w0, h0 = im.size
        except Exception:
            return h, h
        return round(h * w0 / h0), h

    # Plain marks only in the marquee — the client's call.
    #
    # The ten coloured cards were shown here for a while. They still exist and
    # are still used on the About page's fan ring, where a card is the right
    # object; in a single scrolling row they read as ten tiles among fifty-odd
    # wordmarks, which is two treatments doing one job.
    row = ""
    for slug, name in BANNER_CLIENTS:
        p = SITE / "assets" / "helv" / f"{slug}.webp"
        w, h = box(p)
        row += (f'<div class="client_logo">'
                f'<img src="{CLIENTS_DIR}/{slug}.webp" '
                f'srcset="{CLIENTS_DIR}/{slug}@2x.webp 2x" alt="{name}" '
                f'width="{w}" height="{h}"/></div>')

    # two identical copies: the marquee loops on one copy's width
    return (
        '<section class="client_banner_section" aria-label="Clients">'
        '<div class="client_banner_head"><div class="section_caption">'
        '<div class="section_caption_circle"></div>'
        '<p class="section_caption_text">Trusted <span class="text-italic">(by)</span> Leading Multinational Brands</p>'
        '</div></div>'
        '<div class="client_banner_track">'
        f'<div class="client_banner_row">{row}</div>'
        f'<div class="client_banner_row" aria-hidden="true">{row}</div>'
        '</div></section>')


def film_section() -> str:
    """The showreel, full bleed, between the client logos and About.

    Self-hosted rather than a Vimeo background player. Three reasons, in order
    of how often they bite:

      * Vimeo's background player picks its own rendition and was serving well
        below the source's 1080p on a full-bleed frame. A local file plays at
        the resolution it was encoded at.
      * `player.vimeo.com` is on the default block list of uBlock Origin and
        Brave, and on plenty of corporate networks. A blocked iframe leaves a
        flat empty box — there is no fallback inside an iframe to reach for.
      * It is a third party in the critical path of the page's first screen.
        Vimeo returned 503s during this build.

    The button still opens the Vimeo player for sound, which is a click the
    visitor chooses to make: if that is blocked they have already seen the film.

    preload="none" plus the poster means the file costs nothing until the
    visitor is near it, and the frame is never blank while it arrives.
    """
    return (
        '<section class="film_section" aria-label="HelloVoice showreel">'
        '<div class="about_video_wrap is-local">'
        '<video class="film_video" autoplay muted loop playsinline '
        'preload="none" poster="/assets/video/film-reel-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/film-reel.mp4" type="video/mp4"/>'
        '</video>'
        '<button type="button" class="about_video_button" data-open-reel '
        f'data-vimeo="{HC.VIMEO_SHOWREEL}" data-ratio="16:9" '
        'aria-label="Watch the showreel with sound">'
        '<span class="about_video_icon">'
        '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" '
        'aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button>'
        '</div></section>')


def knockout_nav(html: str) -> str:
    """Re-key the header lockup to its white pair.

    `nav_mark` picks the wordmark from the page name, which cannot know about
    pages built after the fact. Services, Influencer Campaigns and Technology
    Activations all open on a full-bleed film, so the colour lockup sat in brand
    blue and red over moving footage. Swapped here, after those pages exist.

    Both marks move together — brand_lockup reads the HelloVoice variant to
    choose the parent's, so leaving one behind would put a blue Blue Holding
    beside a white HelloVoice.
    """
    m = re.search(r'<a[^>]*\bclass="brand[^"]*\bw-nav-brand[^"]*"[^>]*>[\s\S]{0,1200}?</a>', html)
    if not m:
        raise SystemExit("knockout_nav: no nav brand link")
    nav = m.group(0)
    # the srcset's 240px cut too — it is the file a phone actually loads, and
    # leaving it blue kept Blue Holding brand-blue over the Influencer film
    swapped = (nav.replace("/assets/brand/blueholding.webp",
                           "/assets/brand/blueholding-white.webp")
                  .replace("/assets/brand/blueholding-240.webp",
                           "/assets/brand/blueholding-white-240.webp")
                  .replace("/assets/helv/logo.webp", "/assets/helv/logo-knockout.webp")
                  .replace("/assets/helv/logo@2x.webp", "/assets/helv/logo-knockout@2x.webp"))
    return html[:m.start()] + swapped + html[m.end():]


def about_media(html: str) -> str:
    """The About page's two picture slots become film.

    The stats block's left panel and the "Life at HelloVoice" card fan were both
    stills. The client's call is that each carries a film instead — the vertical
    studio clip beside the numbers, and the behind-the-scenes cut in place of
    the four-card fan.

    The fan's four cards go rather than being filled with the same frame four
    times: the effect is a stack of overlapping photographs, and four copies of
    one video reads as a bug. One frame, at the fan's own width.
    """
    # --- the panel beside the stats
    html = re.sub(
        r'<img[^>]*character-with-camera-540\.webp[^>]*>',
        '<video class="about_stats_video" autoplay muted loop playsinline '
        'preload="none" poster="/assets/video/about-left-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/about-left.mp4" type="video/mp4"/></video>',
        html, count=1)

    # --- the card fan
    # matched on the class, not on an exact tag: Webflow emits
    # `data-slide-cards` before it, so `<div class="life_images">` never appears
    m = re.search(r'<div[^>]*\bclass="life_images"[^>]*>', html)
    if m:
        depth, end = 0, None
        for t in re.finditer(r"<(/?)div\b[^>]*>", html[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        if end is not None:
            html = (html[:m.start()]
                    + '<div class="life_images is-film">'
                      '<video class="life_video" autoplay muted loop playsinline '
                      'preload="none" poster="/assets/video/bts-reel-poster.jpg" '
                      'aria-hidden="true">'
                      '<source src="/assets/video/bts-reel.mp4" type="video/mp4"/>'
                      '</video></div>'
                    + html[end:])
    return html


def about_clients(html: str) -> str:
    """Carry the home page's client band onto About.

    Built from the same client_logos data the home page uses rather than copied
    out of the built markup, so the two cannot drift apart when the roster
    changes. Seated above the team, where "who we work for" reads before "who
    we are".
    """
    band = client_banner()
    m = re.search(r'<section[^>]*\bclass="[^"]*team_section', html)
    if not m:
        return html
    return html[:m.start()] + band + html[m.start():]


def value_numbers(html: str) -> str:
    """The track's big numeral is a sequence, not a year.

    The reference ships 2020..2025 in these slots and the section used to carry
    invented company milestones to match. It now carries HelloVoice's own six
    values, which have no dates attached — so a year beside each one is a claim
    about when the studio started believing something, which is both untrue and
    slightly absurd.

    Numbered 01..06 instead. The slot keeps the display numeral the layout is
    built around, and asserts nothing.
    """
    seq = iter(f"{i:02d}" for i in range(1, 7))

    def one(m):
        try:
            return f'<h2 class="year_text">{next(seq)}</h2>'
        except StopIteration:
            return m.group(0)

    return re.sub(r'<h2 class="year_text">\s*\d{4}\s*</h2>', one, html)


def hero_no_info(html: str) -> str:
    """Drop the hero's supporting paragraph.

    The hero already carries the wordmark, the headline and the stat. The
    paragraph under them repeated what the headline says at greater length, in
    all-caps at a size that competed with the headline rather than supporting
    it. The client's call is that it goes; the space it frees is what lets the
    character below it read.

    Removed with its own wrapper so the column does not keep the paragraph's
    slot as a gap, and its reveal is dropped from the intro timeline with it.
    """
    m = re.search(r'<p[^>]*\bclass="[^"]*hero_info[^"]*"[^>]*>', html)
    if not m:
        return html
    end = html.find("</p>", m.end())
    if end == -1:
        return html
    return html[:m.start()] + html[end + 4:]


def exclusive_section(html: str) -> str:
    """The client's own pick, as a two-up carousel above the listing.

    Two films in view with an arrow either side rather than a static row of
    four: a shortlist should read as picked over rather than laid out, and two
    at a time gives each film enough width to carry at this scale.

    Built from HC.EXCLUSIVE, which names films by Vimeo id — a list the client
    edits rather than a rule they have to express. An id with no projects.json
    entry fails the build rather than silently shrinking the row.

    The pager is markup here and motion.js drives it. With no JS the track stays
    a horizontally scrollable row, so every film is still reachable.
    """
    by_id = {p["vimeo"]: p for p in HC.PROJECTS if p.get("vimeo")}
    picks = [by_id[v] for v in HC.EXCLUSIVE if v in by_id]
    missing = [v for v in HC.EXCLUSIVE if v not in by_id]
    if missing:
        raise SystemExit(f"exclusive: no projects.json entry for {missing}")
    if not picks:
        return html

    def tile(p):
        return (
            f'<a aria-label="Watch {HC.esc(p["title"])}" '
            f'href="https://vimeo.com/{p["vimeo"]}" data-vimeo="{p["vimeo"]}" '
            f'data-ratio="{p["ratio"]}" data-title="{HC.esc(p["title"])}" '
            f'class="project_image exclusive_item">'
            f'<img src="/assets/work/{p["img"]}-700.webp" '
            f'srcset="/assets/work/{p["img"]}-700.webp 700w, '
            f'/assets/work/{p["img"]}-1400.webp 1400w" '
            f'sizes="(max-width: 991px) 92vw, 46vw" loading="lazy" '
            f'alt="{HC.esc(p["title"])}" class="image-cover"/>'
            '<span class="work_play" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor">'
            '<path d="M8 5v14l11-7z"/></svg></span>'
            f'<span class="exclusive_label">{HC.esc(p["title"])}</span></a>')

    arrow = ('<button type="button" class="exclusive_arrow is-{d}" '
             'aria-label="{lab} projects">'
             '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" '
             'stroke="currentColor" stroke-width="2" aria-hidden="true">'
             '<path d="{path}"/></svg></button>')

    section = (
        '<section class="work_group exclusive_section" data-group="exclusive" '
        'data-exclusive-group '
        'style="background-color:rgba(18,18,18,.05)">'
        '<div class="work_group_head">'
        '<h2 data-title-anim="" class="work_group_title is-exclusive">'
        'Exclusive Projects</h2>'
        '</div>'
        '<div class="exclusive_carousel" data-exclusive>'
        + arrow.format(d="prev", lab="Previous", path="M15 5l-7 7 7 7")
        + '<div class="exclusive_track" data-exclusive-track>'
        + "".join(tile(p) for p in picks)
        + '</div>'
        + arrow.format(d="next", lab="Next", path="M9 5l7 7-7 7")
        + '</div></section>')

    # Below the filter bar: the page title and the controls come first, then
    # the client's pick, then the listing. The client's order — a visitor should
    # meet the page and the way through it before a curated row.
    m = re.search(r'</div>\s*(?=<section class="work_group")', html)
    if m:
        return html[:m.end()] + section + html[m.end():]
    m = re.search(r'<section class="work_group"', html)
    if m:
        return html[:m.start()] + section + html[m.start():]
    return html


def nav_rework(html: str) -> str:
    """Header, menu and footer: Work links the film archive, Services is Services.

    It used to drop /projects/ from every nav and relabel /service/ as
    "Portfolio", on the reasoning that visitors should reach the work through
    each discipline. The mobile audit (10 Sep 2026) found what that cost: the
    42-film archive — the evidence a referred visitor comes to check — had no
    link anywhere global, and "Portfolio" opened a services overview. The
    client approved the change on 12 Sep 2026.

    So the reference's own /projects/ anchors stay (header "Works", menu and
    footer "Projects") and all read "Work"; /service/ keeps "Services".

    Labels are printed twice per link for the hover roll, so every copy inside
    the anchor changes, case-preserving (the inner pages ship lowercase and
    uppercase it in CSS).
    """
    def _work(m):
        return re.sub(r'>(\s*)(Works|Projects|works|projects)(\s*)<',
                      lambda t: ">" + t.group(1)
                      + ("Work" if t.group(2)[0].isupper() else "work")
                      + t.group(3) + "<", m.group(0))

    return re.sub(
        r'<a\b[^>]*href="/projects/"[^>]*class="[^"]*'
        r'(?:nav_link|canvas_menu_link|footer_link_widget)[^"]*"[^>]*>.*?</a>',
        _work, html, flags=re.S)


# Only the accounts the client actually runs. Instagram is confirmed —
# it is the account the influencer grid was captured from. The other two carry
# the reference's bare domains and are flagged rather than shipped as if real.
SOCIALS = [
    ("Instagram", "https://instagram.com/helv.studio",
     "M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9"
     ".42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 "
     "3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82"
     ".68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85"
     "-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82"
     "-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58"
     ".07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38"
     "-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33"
     ".01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.31-1.46.72-2.12 1.38C1.35 2.67.94"
     " 3.34.63 4.13.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95"
     "c.06 1.27.26 2.15.56 2.91.31.79.72 1.46 1.38 2.12.66.66 1.33 1.07 2.12 "
     "1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27"
     "-.06 2.15-.26 2.91-.56.79-.31 1.46-.72 2.12-1.38.66-.66 1.07-1.33 1.38"
     "-2.12.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c"
     "-.06-1.27-.26-2.15-.56-2.91-.31-.79-.72-1.46-1.38-2.12C21.33 1.35 20.66"
     ".94 19.87.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84a6.16 "
     "6.16 0 100 12.32 6.16 6.16 0 000-12.32zM12 16a4 4 0 110-8 4 4 0 010 8zm"
     "7.85-10.4a1.44 1.44 0 11-2.88 0 1.44 1.44 0 012.88 0z"),
    ("Facebook", "https://facebook.com",
     "M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v"
     "-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 "
     "2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24"
     "C19.61 23.1 24 18.1 24 12.07z"),
    ("TikTok", "https://tiktok.com",
     "M16.6 5.82A4.28 4.28 0 0115.54 3h-3.09v12.4a2.59 2.59 0 01-2.59 2.5 2.59 "
     "2.59 0 01-2.59-2.59 2.59 2.59 0 013.36-2.47V9.7a5.68 5.68 0 00-.77-.05A5.7"
     " 5.7 0 004.17 15.3 5.7 5.7 0 009.87 21a5.7 5.7 0 005.7-5.7V9.01a7.35 7.35"
     " 0 004.29 1.37V7.3a4.28 4.28 0 01-3.26-1.48z"),
]


def footer_socials(html: str) -> str:
    """The footer's newsletter form becomes a row of social links.

    The client has no newsletter to send, so a subscribe field collected
    addresses nobody was going to use — and the form posted to Webflow's own
    endpoint, which would have quietly failed or, worse, quietly worked and put
    their visitors' addresses somewhere they do not control.

    Icons are inline SVG rather than an icon font or sprite, so they inherit
    currentColor, need no extra request, and cannot arrive after the footer has
    painted.

    Facebook and TikTok carry bare domains here because that is all the
    reference had — they are the client's own placeholder to replace, and are
    marked as such in SOCIALS rather than being dressed up as real profiles.
    """
    m = re.search(r'<div class="footer_cta">', html)
    if not m:
        return html
    depth, end = 0, None
    for t in re.finditer(r'<(/?)div\b[^>]*>', html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        return html

    links = "".join(
        f'<a class="footer_social_link" href="{HC.esc(url)}" '
        f'target="_blank" rel="noopener noreferrer" aria-label="{HC.esc(name)}">'
        f'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" '
        f'aria-hidden="true"><path d="{path}"/></svg>'
        f'<span class="footer_social_name">{HC.esc(name)}</span></a>'
        for name, url, path in SOCIALS if name == "Instagram")

    block = ('<div class="footer_cta">'
             '<p class="footer_link_col_heading">Follow us on social media</p>'
             f'<div class="footer_socials">{links}</div>'
             '</div>')
    return html[:m.start()] + block + html[end:]


def work_card_buttons(html: str) -> str:
    """Featured work cards: Learn More becomes Watch Now.

    The button opens the film in the lightbox, so "Learn More" described
    something the card does not do. Both label copies change — the template
    rolls one up and the other down on hover, and changing one leaves the old
    word showing underneath as soon as the pointer arrives.

    Scoped to the work cards. The About and service buttons still say Learn
    More, and still should: those go to a page rather than to a film.
    """
    m = re.search(r'<div class="work_items_track">', html)
    if not m:
        return html
    depth, end = 0, None
    for t in re.finditer(r'<(/?)div\b[^>]*>', html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        return html
    # The work cards ship the v2 button — data-button-text-v2 / button_text_v2 —
    # not the button_text the rest of the site uses. Matching the plain form
    # found the block, replaced nothing, and reported success.
    block = re.sub(r'(<p data-button-text(?:-v2)?="" '
                   r'class="button_text(?:_v2)?(?: second_text)?">)Learn More(</p>)',
                   r"\1Watch Now\2", html[m.start():end])
    return html[:m.start()] + block + html[end:]


def home_order(html: str) -> str:
    """Reorder the home page to the sequence the client asked for.

    Hero, clients, film, values, services, featured work, then everything else
    in the order it already had.

    Sections are moved whole — matched from their opening <section> to the tag
    that closes it, counting depth, so a nested <section> cannot cut one short.
    Anything not named is left where it is and follows the named block, which
    means adding a section to the page later does not silently reshuffle it.

    about_section is the values track: the six values live inside it, and it is
    the section the client means by "values" rather than the About page.
    """
    def take(name):
        m = re.search(r'<section[^>]*\bclass="[^"]*' + name + r'[^"]*"', html)
        if not m:
            return None, None
        depth, end = 0, None
        for t in re.finditer(r"<(/?)section\b[^>]*>", html[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        return (m.start(), end) if end else (None, None)

    WANTED = ["hero_section", "client_banner_section", "film_section",
              "about_section", "service_section", "work_section"]

    spans = {}
    for name in WANTED:
        a, b = take(name)
        if a is None:
            raise SystemExit(f"home_order: {name} not found")
        spans[name] = (a, b)

    # everything else, in the order it already appears
    ordered = sorted(spans.values())
    first, last = ordered[0][0], ordered[-1][1]
    between = []
    cursor = first
    for a, b in ordered:
        if a > cursor:
            between.append(html[cursor:a])
        cursor = max(cursor, b)

    rebuilt = "".join(html[spans[n][0]:spans[n][1]] for n in WANTED) + "".join(between)
    return html[:first] + rebuilt + html[last:]


# The finished home page, stashed so about-us can lift its values section
# rather than rebuild one. Set when home is built; ROUTES is ordered so that
# happens first, and about_values no-ops rather than guesses if it is empty.
_HOME_HTML = ""
_HOME_VALUES_SRC = ""   # the home values before Ethics is dropped (About keeps six)


def about_values(html: str, home_html: str) -> str:
    """Put the values track on the About page too.

    The client wants the six values on the page about the company as well as on
    the home page. The section is copied from the built home page rather than
    rebuilt from HC.MILESTONES, so the two can never drift: one of them would
    otherwise be a second implementation quietly diverging from the first the
    next time a value is reworded.

    Seated above the team, which is the natural reading order — what the studio
    believes, then who does it.

    Its id and any anchor-bearing attributes are left alone: the section
    carries none, and the numerals are plain text rather than link targets.
    """
    m = re.search(r'<section[^>]*\bclass="[^"]*about_section', home_html)
    if not m:
        return html
    depth, end = 0, None
    for t in re.finditer(r"<(/?)section\b[^>]*>", home_html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        return html
    block = home_html[m.start():end]

    seat = re.search(r'<section[^>]*\bclass="[^"]*team_section', html)
    if not seat:
        return html
    return html[:seat.start()] + block + html[seat.start():]


def works_heading(html: str) -> str:
    """"Our New Works" becomes "Our Work".

    The reference's wording, kept through the clone. "New" dates the section
    the moment anything is added below it, and the page is the whole portfolio
    rather than a recent-additions feed.
    """
    return html.replace("<h2>Our New Works</h2>", "<h2>Our Work</h2>", 1)


def check_posters() -> None:
    """Refuse to build if a work poster is missing either of its two sizes.

    Cards ship src="-700" with a srcset naming both, so a film with only the
    1400 present renders on a page that happens to request the large one and
    404s on a page that requests the small — which is exactly what the
    exclusive carousel hit, while the same film worked on the home page. The
    browser shows nothing and says nothing; only the network log knows.

    Three files were missing their 700 when this was added.
    """
    d = SITE / "assets" / "work"
    if not d.exists():
        return
    big = {f.name[:-len("-1400.webp")] for f in d.glob("*-1400.webp")}
    small = {f.name[:-len("-700.webp")] for f in d.glob("*-700.webp")}
    gaps = sorted((big - small) | (small - big))
    if gaps:
        raise SystemExit(
            "work posters missing a size (each needs -700 and -1400):\n  "
            + "\n  ".join(gaps))


def mark_hero_tone(html: str) -> str:
    """Tell the stylesheet whether this page opens on a dark hero.

    The header sits over the hero before it scrolls, and the two kinds of hero
    need opposite ink: three pages open on film and one on a photograph, where
    the nav has to be white to be read at all; the rest open on linen, where
    white is invisible. Guessing from the page name would break the moment a
    hero changes, so the class is derived from the hero's own markup.

    Set on <html> rather than on the header, because the header is fixed and
    the hero is not — a rule scoped to the header alone cannot see what it is
    sitting on.
    """
    # Runs last on purpose. has-photo is added by works_hero and is-reel-hero
    # by the service builder, both of which come after the shared passes — a
    # stamp taken earlier reads a hero that has not been rebuilt yet and marks
    # every page light, which is precisely what it did the first time.
    m = re.search(r'<section[^>]*\bclass="([^"]*hero[^"]*)"', html)
    hero = m.group(1) if m else ""
    # is-light names the reference's pale hero, but this build puts the warm
    # brand band behind the home header — white reads on it and ink does not,
    # which is why home is on this list despite the class it carries.
    dark = any(k in hero for k in ("has-photo", "is-reel-hero", "is-dark",
                                   "hero_section is-light"))
    if not dark:
        return html
    return html.replace("<html", '<html data-hero-tone="dark"', 1)


def work_header_badge(html: str) -> str:
    """Lift FILM & IMMERSIVE above "Our Work" instead of across it.

    The badge ships after the heading and is absolutely positioned, so it sat
    over the words — which is the treatment the section headings use elsewhere,
    but this is the page's own title and the tag was landing on the O of Our.

    Moved before the heading in the DOM and set static in this one place, so it
    reads as a label introducing the title rather than a sticker across it.
    Every other badge on the site keeps the overlay treatment.
    """
    m = re.search(
        r'(<div class="section_header is_project">)(<h2>.*?</h2>)'
        r'(<div class="floating_text is-work">.*?</div>)',
        html, flags=re.S)
    if not m:
        return html
    return html[:m.start()] + m.group(1) + m.group(3) + m.group(2) + html[m.end():]


def work_separators(html: str) -> str:
    """Put the ticker band between the work groups.

    The page already carries one below the hero; the client wants the same rule
    between sections. It is reused rather than rebuilt so the two cannot drift,
    and the copies are aria-hidden — the band is decorative, and a screen
    reader meeting "Video Production, CGI & 3D Production" six more times is
    being read a decoration as content.

    Not placed before the first group: the filter bar sits directly above it,
    and a band between a control and the thing it controls separates two things
    that belong together.
    """
    m = re.search(r'<section class="project_ticker">.*?</section>', html, flags=re.S)
    if not m:
        return html
    band = m.group(0).replace(
        '<section class="project_ticker">',
        '<section class="project_ticker is-separator" aria-hidden="true">', 1)

    parts = html.split('<section class="work_group"')
    if len(parts) < 3:
        return html
    out = [parts[0]]
    for i, chunk in enumerate(parts[1:]):
        # a band before every group except the first
        out.append(("" if i == 0 else band) + '<section class="work_group"' + chunk)
    return "".join(out)


def menu_button_semantics(html: str) -> str:
    """Make the hamburger a real control.

    The reference ships it as a bare <div> with a click handler: no role, no
    accessible name, and nothing in the tab order. On a phone it is the only
    way into the navigation, so a keyboard or screen-reader visitor had no way
    to open the menu at all.

    role and tabindex rather than swapping the tag for a <button>: the element
    carries Webflow's own interaction classes and variant attributes, and a
    <button> would also bring a user-agent border and background that the
    styling here does not expect.
    """
    # Matched by class, not by a literal opening tag: the element ships with
    # data-menu-icon and Webflow's variant attribute before its class, so a
    # literal "<div class=..." matched nothing and added nothing — silently,
    # which is the third time that shape of mistake has cost time here.
    return re.sub(
        r'<div\b(?![^>]*\brole=)([^>]*\bclass="[^"]*hamburger_menu_icon)',
        r'<div role="button" tabindex="0" aria-label="Open menu" '
        r'aria-expanded="false"\1',
        html, count=1)


def works_filter(html: str) -> str:
    """A filter bar above the project grid, built from the tags in the markup."""
    tags = []
    for t in re.findall(r'class="project_tag">(.*?)</a>', html):
        t = t.strip()
        if t not in tags:
            tags.append(t)
    if not tags:
        return html

    buttons = ('<button type="button" class="works_filter_button is-active" '
               'data-filter="all" aria-pressed="true">All</button>')
    buttons += "".join(
        f'<button type="button" class="works_filter_button" data-filter="{slug(t)}" '
        f'aria-pressed="false">{t}</button>' for t in tags)

    bar = ('<div class="works_filter" role="group" aria-label="Filter works by type">'
           + buttons +
           '</div><p class="works_filter_count" role="status" aria-live="polite"></p>')

    html = html.replace('<div class="project_collection_list w-dyn-list">',
                        bar + '<div class="project_collection_list w-dyn-list">', 1)

    # stamp each card with its own tags so the filter has something to match
    def stamp(m):
        block = m.group(0)
        found = [slug(x) for x in re.findall(r'class="project_tag">(.*?)</a>', block)]
        return block.replace('class="project_item w-dyn-item"',
                             'class="project_item w-dyn-item" data-tags="'
                             + " ".join(found) + '"', 1)

    return re.sub(r'<div role="listitem" class="project_item w-dyn-item">.*?(?=<div role="listitem" class="project_item|</div></div></div>)',
                  stamp, html, flags=re.S)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def rewrite_assets(html: str) -> str:
    """Point every CDN reference at the local mirror."""
    def sub(m):
        url = m.group(0)
        base = url.split("?")[0]
        if "/css/" in base or base.endswith(".js"):
            return url          # handled separately
        return f"/assets/ref/{asset_name(base)}"

    return re.sub(re.escape(CDN) + r'/[^\s"\'\)>,]+', sub, html)


def strip_scripts(html: str) -> str:
    # remove <script src="…"> for anything we do not ship
    def drop(m):
        tag = m.group(0)
        return "" if any(d in tag for d in DROP_SRC) else tag

    html = re.sub(r'<script\b[^>]*\bsrc="[^"]*"[^>]*>\s*</script>', drop, html)
    # the reference's gsap/lenis script tags — replaced by our vendored set
    html = re.sub(
        r'<script\b[^>]*\bsrc="[^"]*(?:gsap|ScrollTrigger|SplitText|lenis)[^"]*"[^>]*>\s*</script>',
        "", html)
    html = re.sub(
        r'<link\b[^>]*href="[^"]*lenis[^"]*"[^>]*/?>', "", html)
    # Webflow's touch-detect shim, plugin registration and Lenis init
    html = re.sub(
        r'<script\b(?![^>]*\bsrc=)[^>]*>\s*(?:!function\(o,c\)|gsap\.registerPlugin|// Initialize Lenis).*?</script>',
        "", html, flags=re.S)
    return html


def rewrite_links(html: str) -> str:
    def sub(m):
        href = m.group(1)
        if href in LINKS:
            return f'href="{LINKS[href]}"'
        # project detail pages are written as directories too
        if href.startswith("/projects/") and not href.endswith("/"):
            return f'href="{href}/"'
        return f'href="{href}"'
    return re.sub(r'href="(/[^"#?]*)"', sub, html)


def mark_placeholders(html: str) -> str:
    """Tag whatever is still borrowed, so `grep data-placeholder` finds it.

    Runs last, after the content pass, and is scoped to /assets/ref/. Once a
    slot carries a HelloVoice file it is no longer a placeholder — leaving the
    tag on would make the tripwire lie about what still needs replacing.
    """
    html = re.sub(r'\sdata-placeholder="[^"]*"', "", html)

    def tag(m):
        el = m.group(0)
        return el[:-1].rstrip("/") + ' data-placeholder="ariyana-reference"' + el[-1:]

    return re.sub(r'<(?:img|source)\b[^>]*/assets/ref/[^>]*>', tag, html)


def stamp(rel: str) -> str:
    """`?v=<short hash>` for a file we author, so a rebuild is never cached.

    Without this a browser holds the previous clone.css and motion.js and the
    build looks unchanged — which has cost real debugging time.
    """
    p = SITE / rel.lstrip("/")
    if not p.exists():
        return rel
    h = hashlib.sha1(p.read_bytes()).hexdigest()[:8]
    return f"{rel}?v={h}"


MINIFY = [("assets/css/clone.css", "assets/css/clone.min.css"),
          ("assets/css/hero-exception.css", "assets/css/hero-exception.min.css"),
          ("assets/js/motion.js", "assets/js/motion.min.js")]


def minify_assets() -> int:
    """Minified copies of the three files we author, when esbuild is at hand.

    The sources stay commented and readable; pages link the .min twin. If no
    esbuild is found the twins are deleted rather than left behind — a stale
    minified file would silently serve yesterday's code, which is worse than
    serving today's code uncompressed.
    """
    import shutil, subprocess, os
    exe = os.environ.get("HELV_ESBUILD") or shutil.which("esbuild") or \
        "/Users/bido/Bido Visuals/Stock Footage Portal/node_modules/.bin/esbuild"
    made = 0
    for src, dst in MINIFY:
        out = SITE / dst
        if not pathlib.Path(exe).exists():
            out.unlink(missing_ok=True)
            continue
        r = subprocess.run([exe, str(SITE / src), "--minify", "--log-level=error",
                            f"--outfile={out}"], capture_output=True, text=True)
        if r.returncode:
            out.unlink(missing_ok=True)
            print(f"  ! minify failed for {src}: {r.stderr.strip()[:200]}")
        else:
            made += 1
    return made


def asset(rel: str) -> str:
    """The minified twin if the build made one, else the source — stamped."""
    for src, dst in MINIFY:
        if rel.lstrip("/") == src and (SITE / dst).exists():
            return stamp("/" + dst)
    return stamp(rel)


def head_inject() -> str:
    return (
        '<link rel="stylesheet" href="/assets/vendor/lenis.css"/>\n'
        f'<link rel="stylesheet" href="{stamp("/assets/css/main.css")}"/>\n'
        f'<link rel="stylesheet" href="{asset("/assets/css/clone.css")}"/>\n'
    )


def hero_css() -> str:
    return f'<link rel="stylesheet" href="{asset("/assets/css/hero-exception.css")}"/>\n'


def apply_hero_exception(html: str) -> str:
    """The home hero: a red radial ground carrying the approved character.

    The ground is dark, so the reference's default light-on-dark nav and hero
    type are already correct — nothing is inverted here. Only the section class
    and the stylesheet are added.
    """
    html = html.replace('<section class="hero_section">',
                        '<section class="hero_section is-light">', 1)

    # The reference stacks its name over STUDIO on a second line. Both lines
    # live inside the one h1 so SplitText treats them as a single run and the
    # character drop staggers straight through — a second h1 would restart the
    # stagger and read as two separate animations.
    # The wordmark stacks over the intro line, both held in the left half of the
    # frame. It reads as one lockup rather than as a title and a caption.
    html = html.replace(
        '<h1 data-hero-title="">HELLO<span class="hv-accent">VOICE</span></h1>',
        '<h1 data-hero-title="" aria-label="HelloVoice Studio">'
        'HELLO<span class="hv-accent">VOICE</span>'
        '<span class="hv-line2">Studio</span></h1>', 1)
    # The character is now a film with its own ground baked in, so the cutout
    # and the WebGL mesh both retire — three characters competing for the same
    # space was the mess. .hero_image already fills the section absolutely and
    # .hero_heading already carries z-index 1, so the film needs no new
    # stacking context: it sits in the existing hole and the type is above it.
    #
    # Not autoplaying. Scroll position drives currentTime (see heroFilm in
    # motion.js), so the film is paused and seeked. It still needs muted and
    # playsinline: without them iOS refuses to decode a video it considers
    # uninitiated, and seeking a never-decoded video yields a blank frame.
    html = html.replace(
        '<div data-hero-image="" class="hero_image"></div>',
        '<div data-hero-image="" class="hero_image">'
        # 17 Sep 2026: the client's hero film, played by Vimeo's background
        # player (muted, looping, no controls). It is 16:9 — the desktop hero is
        # 16:9 too, and phones show it as a full-width band (hero-exception.css)
        # so nothing is cropped on either.
        f'<iframe class="hero_film hero_vimeo" data-hero-vimeo '
        f'src="https://player.vimeo.com/video/{HERO_VIMEO}?background=1&amp;autoplay=1'
        f'&amp;loop=1&amp;muted=1&amp;dnt=1&amp;quality=1080p" '
        'title="HelloVoice showreel" allow="autoplay; fullscreen; picture-in-picture" '
        'referrerpolicy="strict-origin-when-cross-origin" tabindex="-1" aria-hidden="true" '
        'frameborder="0"></iframe>'
        '</div>', 1)
    # No poster attribute. The still is the hero's own CSS background (see
    # hero-exception.css), so it shows whether or not the film ever decodes —
    # a poster on the video is hidden along with the video until its first
    # frame, which on iPhone meant an empty box. The phone gets its own
    # portrait cut of the film and of the still; mobile_media() adds the
    # <source media> for it at write time.
    #
    # A returning visitor has already sat through the intro this session, so
    # the loading panel must not flash before motion.js can hide it.
    html = html.replace("<head>", '<head><script>try{if(sessionStorage.getItem('
                        '"hv-intro"))document.documentElement.classList.add("intro-seen")'
                        '}catch(e){}</script>', 1)
    html = html.replace("</head>", hero_css() + "</head>", 1)
    # The still is the largest thing in the first screen, so it is fetched at
    # once rather than when the stylesheet gets round to it — the portrait cut
    # on an upright phone, the 16:9 frame everywhere else.
    html = html.replace("</head>", (
        f'<link rel="preload" as="image" href="{HERO_POSTER}" fetchpriority="high"/>'
        '<link rel="preconnect" href="https://player.vimeo.com"/>'
        '<link rel="preconnect" href="https://i.vimeocdn.com"/>'
        '<link rel="preconnect" href="https://vod-adaptive-ak.vimeocdn.com"/>') + "</head>", 1)

    if not HERO_3D:
        return html

    # The WebGL character is a progressive upgrade over that cutout, so it
    # loads as a module (deferred by definition) and only on this page. If it
    # fails for any reason the cutout is what the visitor keeps.
    return html.replace("</body>", (
        '<script type="importmap">'
        '{"imports":{"three":"/assets/vendor/three.module.min.js"}}</script>\n'
        f'<script type="module" src="{stamp("/assets/js/hero3d.js")}"></script>\n'
        "</body>"), 1)

def showreel_video(html: str) -> str:
    """PLAY / REEL: the reference's stock loop becomes the behind-the-scenes cut.

    Self-hosted at 1080p for the same reasons as the film section above — the
    background player was serving a lower rendition than the source, and a
    blocked iframe has nothing to fall back to. The button still opens Vimeo
    with sound.

    The whole video atom is swapped rather than just its <source>: Webflow's
    background-video widget ships a poster, a noscript fallback and its own
    play/pause control, none of which apply here.
    """
    return re.sub(
        r'(<div class="showreel_video_mask">)[\s\S]*?(?=</div>\s*</div>\s*</div>\s*</section>)',
        lambda m: m.group(1)
        + '<div class="showreel_video_wrapper">'
        '<div class="showreel_video is-local">'
        '<video class="showreel_video_el" autoplay muted loop playsinline '
        'preload="none" poster="/assets/video/bts-reel-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/bts-reel.mp4" type="video/mp4"/>'
        '</video>'
        '<button type="button" class="showreel_video_button" data-open-reel '
        f'data-vimeo="{HC.VIMEO_BTS}" data-ratio="16:9" '
        f'aria-label="Watch {HC.BTS_TITLE} with sound">'
        '<span class="showreel_video_icon_wrapper">'
        '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" '
        'aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button>'
        '</div></div>',
        html, flags=re.S, count=1)


def showreel_words(html: str) -> str:
    """Take the two display words off the reel frame.

    The reference flanks its frame with "Play" and "Reel" — four letters each,
    sitting either side of a small centred video. Once the frame opens to full
    bleed those words are over the film, not beside it, and with a title as long
    as this one they covered the middle of the picture. The client's call is
    that the film carries the section on its own.

    Removed rather than hidden, so nothing is left for the timeline to animate
    or for a screen reader to announce.
    """
    for cls in ("showreel_text _1", "showreel_text _2"):
        s_open = f'<h3 class="{cls}">'
        i = html.find(s_open)
        if i == -1:
            continue
        j = html.find("</h3>", i)
        if j == -1:
            continue
        html = html[:i] + html[j + len("</h3>"):]
    return html


def error_page_heading(html: str) -> str:
    """The 404 has no h1 — its only heading-shaped text is a <p> caption.

    Promoted to <h1> so the page has a document outline (and something for a
    search engine or screen reader to announce) rather than opening on a
    paragraph. The class carries all the styling, so the element swap is
    visually inert; the explicit font reset guards against the browser's own
    h1 defaults leaking in.
    """
    return html.replace(
        '<p class="section_caption_text">Page <span class="text-italic">(not)</span> Found</p>',
        '<h1 class="section_caption_text is-error-title">Page '
        '<span class="text-italic">(not)</span> Found</h1>', 1)


INSTAGRAM_SVG = (
    # Drawn as a badge, not as the brand's outline mark.
    #
    # TikTok and Facebook beside it are solid rounded squares with the glyph
    # cut out of them. Instagram's own logo is an outline design, so dropping it
    # in unchanged put a wiry camera next to two solid tiles — the row read as
    # two icons and a sketch.
    #
    # One path, evenodd. A ray crossing an odd number of subpaths is inside, so
    # nesting them alternates fill and hole: badge fills, the camera's outer
    # edge opens a hole, its inner edge fills again — which leaves the outline
    # as a cut-out ring — and the lens and the dot repeat the trick.
    '<svg width="20" height="20" viewBox="0 0 20 20" fill="white" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path fill-rule="evenodd" clip-rule="evenodd" d="'
    # the badge
    'M5 0h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H5a5 5 0 0 1-5-5V5a5 5 0 0 1 5-5z'
    # camera body, outer edge -> hole
    'M7.4 4h5.2A3.4 3.4 0 0 1 16 7.4v5.2a3.4 3.4 0 0 1-3.4 3.4H7.4A3.4 3.4 0 0 '
    '1 4 12.6V7.4A3.4 3.4 0 0 1 7.4 4z'
    # camera body, inner edge -> filled again, so the wall between them is the
    # visible outline
    'M7.9 5.5h4.2a2.4 2.4 0 0 1 2.4 2.4v4.2a2.4 2.4 0 0 1-2.4 2.4H7.9a2.4 2.4 0 '
    '0 1-2.4-2.4V7.9a2.4 2.4 0 0 1 2.4-2.4z'
    # the lens, as a ring
    'M6.9 10a3.1 3.1 0 1 0 6.2 0 3.1 3.1 0 1 0-6.2 0z'
    'M8.1 10a1.9 1.9 0 1 0 3.8 0 1.9 1.9 0 1 0-3.8 0z'
    # and the dot
    'M12.75 6.4a.85.85 0 1 0 1.7 0 .85.85 0 1 0-1.7 0z'
    '"/></svg>')


def works_hero(html: str) -> str:
    """A photograph behind the works hero, with the copy sitting over it.

    The reference's works hero is type on flat linen. HelloVoice's portfolio
    page is the one that has to look like a production company's, so a still
    from the client's own work goes behind it and the caption, headline and
    button sit on top. A scrim carries the type: white on an unknown frame is
    not legible by luck, and the scrim is what makes it legible by design.
    """
    return html.replace(
        '<section class="project_hero_section">',
        '<section class="project_hero_section has-photo">'
        '<div class="project_hero_media" aria-hidden="true">'
        '<img src="/assets/work/works-hero-2000.webp" '
        'srcset="/assets/work/works-hero-1200.webp 1200w, '
        '/assets/work/works-hero-2000.webp 2000w" sizes="100vw" '
        'alt="" loading="eager" decoding="async"/></div>', 1)


def footer_pages(html: str) -> str:
    """Footer link columns: drop Utilities, list the service pages properly.

    The reference ships a "utilities" column whose only entry is a link to its
    own 404 — a template artefact, not navigation. It goes.

    The second Pages column becomes the services index: Influencer Campaigns
    was already there, Technology Activations joins it, and the heading says
    what the column is rather than repeating "Pages" a second time.
    """
    # 1. remove the utilities column outright
    html = re.sub(
        r'<div[^>]*class="footer_link_col"[^>]*>\s*<p class="footer_link_col_heading">'
        r'\s*utilities\s*</p>.*?</div>\s*</div>',
        "", html, count=1, flags=re.S | re.I)

    # 2. name the services column and add Technology Activations beside
    #    Influencer Campaigns
    tech = ('<a data-link="" href="/service/technology-activations/" '
            'class="footer_link_widget w-inline-block">'
            '<p data-link-text="" class="footer_link_text">Technology Activations</p>'
            '<p data-link-text="" class="footer_link_text secondary-text">'
            'Technology Activations</p></a>')
    # Video Production leads the column: it is the studio's core service and
    # the only one of the three without a page of its own, so without a link
    # here it was the one discipline the footer did not mention. It points at
    # its section on the services page — the other two entries name a service
    # and land on that service, and sending this one straight to the film grid
    # would make it the odd link out. The section carries its own button
    # through to the work.
    #
    # Added here rather than in a pass of its own: this column is assembled at
    # this point in the pipeline, and an earlier pass has nothing to attach to.
    video = ('<a data-link="" href="/service/#video-production" '
             'class="footer_link_widget w-inline-block">'
             '<p data-link-text="" class="footer_link_text">Video Production</p>'
             '<p data-link-text="" class="footer_link_text secondary-text">'
             'Video Production</p></a>')
    html = re.sub(
        r'(<a\b[^>]*href="/service/influencer-campaigns/"[^>]*'
        r'class="footer_link_widget[^"]*"[^>]*>)',
        lambda m: video + m.group(1), html, count=1)

    html = html.replace(
        '<p data-link-text="" class="footer_link_text secondary-text">'
        'Influencer Campaigns</p></a>',
        '<p data-link-text="" class="footer_link_text secondary-text">'
        'Influencer Campaigns</p></a>' + tech, 1)

    # the column that now holds the service pages is headed as such
    parts = html.split('<p class="footer_link_col_heading">Pages</p>')
    if len(parts) == 3:
        html = (parts[0] + '<p class="footer_link_col_heading">Pages</p>'
                + parts[1] + '<p class="footer_link_col_heading">Services</p>'
                + parts[2])
    return html


def remove_why_choose(html: str) -> str:
    """Drop the "why choose us" section from About.

    Nothing replaces it — the client's call. The page already earns the point
    with the stats panel and the timeline, and a list of reasons to pick the
    studio, written by the studio, was the weakest thing on it.
    """
    return re.sub(r'<section[^>]*\bclass="[^"]*why_choose_us_section[^"]*"[\s\S]*?</section>',
                  "", html, count=1)


def remove_awards(html: str) -> str:
    """Drop the Awards & Trophy section from About.

    The reference fills it with its own award marks; HelloVoice has none on
    file, so it was standing empty of anything true.
    """
    return re.sub(r'<section[^>]*\bclass="[^"]*awards_section[^"]*"[\s\S]*?</section>',
                  "", html, count=1)


def dedupe_ids(html: str) -> str:
    """Make repeated element ids unique.

    Several blocks on this site are generated by cloning one of the reference's
    template blocks — the service cards, the team cards, the work groups. The
    template carries Webflow's own `id` attributes, so every clone inherited
    the same id: the home page shipped eight elements all called
    `...-fef38d752545-video`.

    Duplicate ids are invalid HTML, and they break the things that rely on them
    being unique — `getElementById` returns only the first, in-page anchors
    jump to the wrong element, and `aria-labelledby`/`aria-describedby` resolve
    to whichever came first regardless of which control the user is on.

    The first occurrence keeps the original id so any existing reference still
    resolves; later ones are suffixed.
    """
    seen: dict[str, int] = {}

    def one(m):
        whole, val = m.group(0), m.group(1)
        if not val:
            return whole
        n = seen.get(val, 0)
        seen[val] = n + 1
        if n == 0:
            return whole
        return whole.replace(f'id="{val}"', f'id="{val}-{n + 1}"', 1)

    return re.sub(r'\sid="([^"]*)"', one, html)


def no_cache(html: str) -> str:
    """Stop review copies going stale.

    CSS and JS are cache-busted by content hash, but the HTML documents are not
    — nothing can version the page's own URL. So a browser holding an old
    /projects/ document keeps requesting the old stylesheet hash with it, and
    the reviewer sees a build from an hour ago while being told it is fixed.
    That has now cost a round trip over card aspect ratios that were already
    correct on disk.
    """
    tag = ('<meta http-equiv="Cache-Control" '
           'content="no-cache, no-store, must-revalidate"/>')
    return html.replace("<head>", "<head>" + tag, 1)


def rating_cluster(html: str) -> str:
    """The three faces beside "4.9 Rating From Clients".

    It was a flat composite of three team members, which put staff where the
    line claims clients. It now shows the three people actually quoted in the
    testimonials below, built as one overlapping cluster so the row keeps the
    reference's stacked-disc look without three separately-positioned images.
    """
    return re.sub(
        r'<img[^>]*src="/assets/helv/team-avatars\.webp"[^>]*>',
        '<img src="/assets/testimonials/cluster.webp" '
        'alt="Three clients who reviewed HelloVoice" '
        'width="324" height="132" loading="lazy" decoding="async" '
        'class="image-contain"/>',
        html, count=1)


def brand_lockup(html: str) -> str:
    """Blue Holding leads the header lockup, beside the HelloVoice mark.

    HelloVoice is a Blue Holding brand and the client's call is that the parent
    reads first in the navigation rather than as a footnote at the bottom of the
    page — so the footer endorsement is gone and this replaces it.

    "Like hello voice" is taken literally: the parent mark mirrors whichever
    treatment the HelloVoice wordmark itself has on that page, read straight out
    of the markup rather than inferred. An earlier version keyed off the nav's
    `is-dark` class, which turns out not to track the wordmark — the works page
    carries is-dark *and* the knockout wordmark, over a dark photographic hero,
    so the parent mark came out brand-blue against a dark picture while
    HelloVoice beside it was white.

    Anchored on the nav brand link specifically: the preloader carries its own
    copy of the wordmark, and matching the first occurrence in the document puts
    the parent mark inside the loading animation instead of the header.
    """
    pattern = (r'(<a[^>]*\bclass="brand[^"]*\bw-nav-brand[^"]*"[^>]*>)'
               r'([\s\S]{0,800}?)'
               r'(<img[^>]*src="/assets/helv/(logo(?:-knockout)?)\.webp")')

    def _lockup(m):
        open_tag, between, helv_img, variant = m.groups()
        white = variant.endswith("knockout")
        src = "blueholding-white.webp" if white else "blueholding.webp"
        # 640px wide for a slot 59-72px wide: seven times the pixels a phone
        # needs. The 240px cut covers a 72px slot at 3x; the original stays in
        # the srcset for anything denser.
        small = src.replace(".webp", "-240.webp")
        srcset = (f' srcset="/assets/brand/{small} 240w, /assets/brand/{src} 640w" sizes="72px"'
                  if (SITE / "assets" / "brand" / small).exists() else "")
        mark = (f'<img src="/assets/brand/{src}"{srcset} alt="Blue Holding" '
                'class="bh_mark" width="640" height="305" loading="eager" '
                'decoding="async"/>'
                '<span class="bh_rule" aria-hidden="true"></span>')
        return open_tag + mark + between + helv_img

    out, n = re.subn(pattern, _lockup, html, count=1)
    if not n:
        raise SystemExit("brand_lockup: nav brand link + wordmark not found")
    return out


def footer_endorsement(html: str) -> str:
    """Blue Holding, once, in the footer.

    The loading screen is seen once per visit; a visitor arriving on an inner
    page from search never sees it. The footer is the other place a parent
    brand belongs, and it is the only other place it appears — an endorsement
    repeated on every section stops reading as an endorsement.
    """
    mark = ('<p class="footer_endorse"><span>part of</span>'
            '<img src="/assets/brand/blueholding.webp" alt="Blue Holding" '
            'width="320" height="153" loading="lazy"/></p>')
    return re.sub(r'(<p class="footer_legal_text">)', mark + r'\1', html, count=1)


def fix_svg_dimensions(html: str) -> str:
    """Drop width/height="auto" from inline SVGs.

    `auto` is not a valid <length> for an SVG's width/height attribute, so the
    browser rejects it and logs an error for each one — 30 on the service page
    alone. The attribute is doing nothing useful either: these icons are sized
    by CSS. Removing it silences the console without changing a pixel.
    """
    return re.sub(r'\s(?:width|height)="auto"', "", html)


# The character on real HelloVoice sets. Ordered so the biggest crew shot leads
# the section and the timeline reads as the studio growing into its own rooms:
# a rig in the office, a venue, a full studio floor, an interview set, the grade.
CHARACTER_BTS = [
    ("studio-crew",       "The HelloVoice crew on a studio shoot"),
    ("brand-stage",       "A brand stage activation on camera"),
    ("venue-shoot",       "Shooting a live venue"),
    ("rooftop-interview", "A rooftop interview setup"),
    ("cafe-shoot",        "Filming on location in a cafe"),
    ("grading-suite",     "Grading in the edit suite"),
]


def character_bts(html: str) -> str:
    """Put the character's behind-the-scenes stills through the home timeline.

    The generic still swap fills every year card, life image and about visual
    from the WORK list in document order, which left "Inside (the) HelloVoice"
    illustrated with the same delivered films shown three sections further down.
    The section is about the studio, not the slate, so it takes the character
    set instead: the same figure the hero uses, on real sets with real crew.

    Every slot in the section takes a character shot, cycling the set when it
    runs out. Leaving the later milestones on work stills read as an accident
    rather than a decision — the section is about the studio, so it should be
    the studio all the way down. The client will replace the repeats with more
    BTS frames later.
    """
    block = re.search(r'<section class="about_section">[\s\S]*?(?=<section)', html)
    if not block:
        return html
    src = block.group(0)
    shots = itertools.cycle(CHARACTER_BTS)
    slot = iter(range(999))

    def swap(m):
        stem, alt = next(shots)
        # measured at 1440: the lead visual renders at 24vw, each milestone
        # card at 33vw. Declaring one figure for both makes half of them
        # fetch a size they never use.
        sizes = "26vw" if next(slot) == 0 else "34vw"
        return (f'<img src="{CHAR_BTS}/{stem}-700.webp" '
                f'srcset="{CHAR_BTS}/{stem}-700.webp 700w, '
                f'{CHAR_BTS}/{stem}.webp 1400w" '
                f'sizes="(max-width: 767px) 92vw, {sizes}" '
                f'loading="lazy" decoding="async" width="1400" height="781" '
                f'alt="{alt}" class="image-cover"/>')

    out = re.sub(r'<img[^>]*class="image-cover"[^>]*>', swap, src)
    return html.replace(src, out, 1)


def about_life_photos(html: str) -> str:
    """The About page's "life at the studio" grid takes the character set too.

    Same reasoning as the home timeline: the generic still swap filled these
    four cards from the WORK list, so a section about what it is like inside
    HelloVoice was illustrated with four client deliverables. The character BTS
    frames are the studio's own images and are literally on location, which is
    what the section is claiming.

    Cycles the set, so a fifth or sixth card would repeat rather than fall back
    to a client film — the client will swap the repeats for more BTS later.
    """
    block = re.search(r'<section[^>]*\bclass="[^"]*life_section[^"]*"[\s\S]*?</section>', html)
    if not block:
        return html
    src = block.group(0)
    shots = itertools.cycle(CHARACTER_BTS)

    def swap(m):
        stem, alt = next(shots)
        return (f'<img src="{CHAR_BTS}/{stem}-700.webp" '
                f'srcset="{CHAR_BTS}/{stem}-700.webp 700w, '
                f'{CHAR_BTS}/{stem}.webp 1400w" '
                f'sizes="(max-width: 767px) 92vw, 44vw" '
                f'loading="lazy" decoding="async" width="1400" height="781" '
                f'alt="{alt}" class="image-cover"/>')

    return html.replace(src, re.sub(r'<img[^>]*class="image-cover"[^>]*>', swap, src), 1)


def about_character(html: str) -> str:
    """The About stats panel is illustrated by the character, not a client film.

    The generic still swap put a Dermactive campaign frame here, which sells a
    client's product on a page about HelloVoice. The character-with-camera shot
    is the studio's own image, and it is a portrait frame that actually fits the
    tall slot the layout gives it — the landscape stills were being cropped hard
    to fill it.
    """
    return re.sub(
        r'(<div[^>]*class="about_stats_image"[^>]*>)<img[^>]*>',
        lambda m: m.group(1)
        + f'<img src="{CHAR_BTS}/character-with-camera-540.webp" '
          f'srcset="{CHAR_BTS}/character-with-camera-540.webp 540w, '
          f'{CHAR_BTS}/character-with-camera.webp 1080w" '
          f'sizes="(max-width: 767px) 92vw, 50vw" '
          f'loading="lazy" decoding="async" width="1080" height="1935" '
          f'alt="A HelloVoice shoot in progress" class="image-cover"/>',
        html, count=1)


def showreel_no_button(html: str) -> str:
    """The showreel under the client logos loses its play badge.

    The client's call: the film should be its own control. A circular icon
    parked over a full-bleed reel reads as a video-player chrome rather than as
    part of the page, and the reel is already playing — the badge only ever
    meant "open it larger", which the click does anyway.

    The <button> goes and the wrap itself becomes the control. It keeps a real
    role and keyboard handling rather than a bare click handler, so the reel is
    still reachable without a mouse — an invisible affordance is a design
    choice, an unreachable one is a defect.
    """
    def wire(m):
        block = m.group(0)
        btn = re.search(r'<button[^>]*about_video_button[\s\S]*?</button>', block)
        if not btn:
            return block
        vimeo = re.search(r'data-vimeo="(\d+)"', btn.group(0))
        ratio = re.search(r'data-ratio="([^"]*)"', btn.group(0))
        block = block.replace(btn.group(0), "")
        return block.replace(
            '<div class="about_video_wrap is-embed">',
            '<div class="about_video_wrap is-embed is-bare" role="button" tabindex="0"'
            f'{" data-open-reel data-vimeo=" + chr(34) + vimeo.group(1) + chr(34) if vimeo else ""}'
            f'{" data-ratio=" + chr(34) + ratio.group(1) + chr(34) if ratio else ""}'
            ' aria-label="Watch the showreel with sound">', 1)

    return re.sub(r'<section class="film_section"[\s\S]*?</section>', wire, html, count=1)


def preloader_animation(html: str) -> str:
    """The loading screen plays the HelloVoice logo animation, on nothing.

    The client's Main_Animation_logo is delivered over a flat white ground. That
    ground is keyed out by build/alpha_logo.py, which floods inward from the
    frame edges rather than keying on colour — "Hello" is knocked out *white*
    inside the red bubble, so a colour key punches holes through the logotype.

    It ships as an **animated WebP** at 24fps, and both halves of that matter. The first cut was VP9-with-alpha in a WebM: correct in Chrome and
    Firefox, but Safari supports VP9 while ignoring its alpha channel, so it
    played the film perfectly and painted the transparent ground solid white —
    a white rectangle sitting on the linen panel. There is no reliable fallback
    path for that, because Safari does not *fail*; it succeeds opaquely. An
    <img> sidesteps the whole problem: animated WebP carries real alpha in every
    modern browser, loops on its own with no script, and needs no autoplay
    permission. It costs about 700KB against the WebM's 200KB, which is the
    honest price of the thing actually working.

    The frame rate was briefly halved to 15fps to claw back file size, and that
    read exactly as dropped frames on a mark that builds this quickly. 24fps at
    a slightly smaller frame costs the same bytes and looks continuous. Going
    the other way to a full 30 is a false economy here: Safari decodes animated
    WebP on the main thread, so every extra frame is main-thread work during
    the one moment the page has none to spare.

    The <link rel=preload> matters as much as the encode — an animated WebP that
    is still downloading animates in fits, which looks identical to a bad frame
    rate and is a completely different bug.

    Only the HelloVoice mark plays here. The Blue Holding endorsement that used
    to sit beneath it has moved into the header lockup, where the parent brand
    reads on every page rather than only during a load nobody waits through.
    """
    # Preloaded only on the page that has the loading screen. It was injected
    # into every <head>, so each inner page fetched 693KB at high priority for
    # an animation it never shows — about 3.5s of a Slow 4G connection.
    if 'class="preloader"' in html:
        html = html.replace(
            "<head>",
            '<head><link rel="preload" as="image" '
            'href="/assets/brand/helv-logo-alpha-anim.webp"/>', 1)
    art = (
        '<div class="preloader_anim">'
        '<img class="preloader_video" src="/assets/brand/helv-logo-alpha-anim.webp" '
        'alt="HelloVoice" width="640" height="360" '
        'decoding="sync" fetchpriority="high"/>'
        '</div>')
    return re.sub(
        r'(<div data-preloader-logo="" class="logo_text">).*?(</div>)',
        lambda m: m.group(1) + art + m.group(2), html, count=1, flags=re.S)


def add_instagram(html: str) -> str:
    """A third social icon beside TikTok and Facebook.

    Cloned from the Facebook link so it inherits the row's markup, hover and
    the 44px target added in clone.css — rather than hand-rolling an anchor
    that would drift from the other two.
    """
    def one(m):
        tag = m.group(0)
        # The footer builds its own complete set in footer_socials, Instagram
        # included. Cloning its Facebook link too produced a fourth anchor that
        # said "Facebook" and pointed at Instagram — the label came along with
        # the copy. Leave those alone; this pass exists only for the hero row,
        # which the reference shipped with TikTok and Facebook and nothing else.
        if "footer_social_link" in tag:
            return tag
        clone = re.sub(r'href="[^"]*"', 'href="https://instagram.com/helv.studio"', tag, count=1)
        clone = re.sub(r'aria-label="[^"]*"', 'aria-label="HelloVoice on Instagram"', clone, count=1)
        clone = re.sub(r'<svg[\s\S]*?</svg>', INSTAGRAM_SVG, clone, count=1)
        return tag + clone

    return re.sub(
        r'<a[^>]*href="https://facebook\.com"[^>]*>[\s\S]*?</a>',
        one, html, count=0)


def a11y_fixes(html: str) -> str:
    """Accessibility corrections the reference template ships broken.

    Found by auditing every built page:

      * The social icon links carry no accessible name at all in the hero, and
        a generic "social link" in the footer. A screen reader announces four
        identical "social link" targets. Named from the href instead.
      * The footer newsletter field is labelled by its placeholder only, which
        disappears as soon as the visitor types.

    The 20x20 tap targets these links present are widened in CSS, not here.
    """
    def name_for(href: str) -> str:
        for key, label in (("tiktok", "TikTok"), ("facebook", "Facebook"),
                           ("instagram", "Instagram"), ("linkedin", "LinkedIn"),
                           ("youtube", "YouTube"), ("twitter", "X"), ("x.com", "X")):
            if key in href.lower():
                return label
        return "Social profile"

    def sub(m):
        tag = m.group(0)
        href = re.search(r'href="([^"]*)"', tag)
        if not href:
            return tag
        label = f'HelloVoice on {name_for(href.group(1))}'
        if 'aria-label="' in tag:
            return re.sub(r'aria-label="[^"]*"', f'aria-label="{label}"', tag, count=1)
        return tag.replace("<a ", f'<a aria-label="{label}" ', 1)

    html = re.sub(r'<a[^>]*class="[^"]*(?:hero_social_icon_link|footer_social)[^"]*"[^>]*>',
                  sub, html)

    # The newsletter field is labelled by its placeholder alone. Matched on the
    # class, not on attribute order: Webflow emits name= before type= here, so
    # a pattern expecting type first silently matched nothing.
    html = re.sub(
        r'(<input(?![^>]*aria-label)[^>]*\bclass="[^"]*footer_cta_input[^"]*"[^>]*?)(\s*/?>)',
        r'\1 aria-label="Your email address"\2', html)
    return html


def footer_dead_link(html: str) -> str:
    """The footer's "Project Details" slot pointed at a reference project page.

    Those detail pages are no longer built — the work cards open Vimeo instead —
    so the link 404'd on every page of the site. The slot is reused for the
    Influencer Campaigns page rather than deleted, which keeps the footer's
    column grid intact and turns a dead link into a real one.
    """
    html = re.sub(
        r'href="/projects/[a-z0-9-]+/"(\s+class="footer_link_widget)',
        r'href="/service/influencer-campaigns/"\1', html)
    return html.replace(
        '<p data-link-text="" class="footer_link_text">Project Details</p>'
        '<p data-link-text="" class="footer_link_text secondary-text">Project Details</p>',
        '<p data-link-text="" class="footer_link_text">Influencer Campaigns</p>'
        '<p data-link-text="" class="footer_link_text secondary-text">Influencer Campaigns</p>')


def influencer_nav(html: str) -> str:
    """Deliberately a no-op — kept so the intent is on the record.

    Influencer Campaigns used to be cloned into both the header and the
    fullscreen menu. The client's call is that it belongs to Services and is
    reached from that page alone, so neither nav carries it now.

    It also had a bug worth remembering: the header clone kept the label
    "Services", because the reference prints every nav label twice for its
    hover swap and only the first copy was being replaced — so the row read
    SERVICES / SERVICES. Removing the clone removes that too.
    """
    return html


def hero_spacer(html: str) -> str:
    """Wrap the home hero in the element ScrollTrigger will use as its pin spacer.

    ScrollTrigger normally creates that spacer itself, when motion.js runs —
    which on a slow connection is after the page has painted, so everything
    below the hero jumped down 1.5 screens at once: CLS 0.35 on Slow 4G. With
    the spacer in the markup, hero-exception.css reserves the same 150vh from
    first paint and motion.js hands this element to the pin as `pinSpacer`.
    """
    m = re.search(r'<section[^>]*\bclass="hero_section is-light"', html)
    if not m:
        raise SystemExit("hero_spacer: hero section not found")
    depth = 0
    for t in re.finditer(r"<(/?)section\b[^>]*>", html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            return (html[:m.start()] + '<div class="hero_spacer">'
                    + html[m.start():end] + "</div>" + html[end:])
    raise SystemExit("hero_spacer: hero section never closes")


def contact_direct(html: str) -> str:
    """Contact: a direct line above the form, and fields a phone can autofill.

    The form composes an email in the visitor's own mail app. On a phone with
    no mail app set up that goes nowhere, so the call and email lines sit above
    the form rather than only in the footer. The reply-time and NDA line is the
    client's promise, approved 12 Sep 2026. Number and address as everywhere
    else on the site (helv_content.py).
    """
    block = (
        '<div class="contact_direct">'
        '<p class="contact_direct_note">Reply within one working day · NDA on request</p>'
        '<div class="contact_direct_links">'
        '<a class="contact_direct_link" href="tel:+966114634518">Call +966 11 463 4518</a>'
        '<a class="contact_direct_link" href="mailto:info@hellovoice.co.uk">'
        'info@hellovoice.co.uk</a></div></div>')
    anchor = '<div data-current="Tab 1"'
    if anchor not in html:
        raise SystemExit("contact_direct: contact tabs not found")
    html = html.replace(anchor, block + anchor, 1)

    tokens = {"name": "name", "Email": "email", "Phone": "tel", "Company-name": "organization"}

    def ac(m):
        tag = m.group(0)
        nm = re.search(r'\bname="([^"]+)"', tag)
        if "autocomplete=" in tag or not nm or nm.group(1) not in tokens:
            return tag
        return tag.replace("<input ", f'<input autocomplete="{tokens[nm.group(1)]}" ', 1)
    return re.sub(r"<input\b[^>]*>", ac, html)


VIDEO_DIR = SITE / "assets" / "video"


def mobile_media(html: str) -> str:
    """Video that downloads when it is wanted, at a size a phone can use.

    Every background film carried `autoplay`, and a browser starts fetching an
    autoplay video while it parses the HTML — before motion.js can set
    preload="none". On a phone that was 33.8MB on the home page before the
    first scroll. Here the attribute goes; motion.js plays each film when it
    nears the viewport (and not at all under reduced motion).

    Where a phone rendition exists (<name>-m.mp4, 540-960px, a fifth to a half
    of the size — or for the hero, a portrait cut) it is offered first with
    media="(max-width: 767px)", so phones never touch the full file.
    """
    def vid(m):
        tag = m.group(0)
        if "data-hero-film" in tag:
            return tag
        tag = re.sub(r'\s+autoplay(?:="[^"]*")?(?=[\s>/])', "", tag)   # bare or autoplay=""
        if "preload=" in tag:
            return re.sub(r'preload="[^"]*"', 'preload="none"', tag)
        return tag.replace("<video", '<video preload="none"', 1)
    html = re.sub(r"<video\b[^>]*>", vid, html)

    def src(m):
        folder, base = m.group(1), m.group(2)
        if not (SITE / "assets" / folder / f"{base}-m.mp4").exists():
            return m.group(0)
        # The hero's phone cut is portrait; a phone on its side keeps the 16:9 film.
        media = ("(max-width: 767px) and (orientation: portrait)" if base in ("hero-char", "hero-loop")
                 else "(max-width: 767px)")
        return (f'<source src="/assets/{folder}/{base}-m.mp4" type="video/mp4" '
                f'media="{media}"/>' + m.group(0))
    return re.sub(r'<source src="/assets/(video|film)/([a-z0-9-]+)\.mp4" type="video/mp4"/>', src, html)


def lean_images(html: str) -> str:
    """Lazy-load everything but the header marks, and give lone 1400px posters a srcset.

    The home page loaded 115 below-the-fold images eagerly (mostly client
    logos). A browser still loads a lazy image that is on screen, so marking
    all but the nav and loading marks costs the first screen nothing.
    """
    def one(m):
        tag = m.group(0)
        if re.search(r'class="[^"]*\b(bh_mark|helv_wordmark|preloader_video)\b', tag):
            return tag
        if "loading=" not in tag:
            tag = tag.replace("<img ", '<img loading="lazy" ', 1)
        if "decoding=" not in tag:
            tag = tag.replace("<img ", '<img decoding="async" ', 1)
        big = re.search(r'src="(/assets/[a-z0-9/_-]+)-1400\.webp"', tag)
        if big and "srcset=" not in tag and (SITE / (big.group(1).lstrip("/") + "-700.webp")).exists():
            b = big.group(1)
            tag = tag.replace("<img ", f'<img srcset="{b}-700.webp 700w, {b}-1400.webp 1400w" '
                              'sizes="(max-width: 767px) 92vw, 45vw" ', 1)
        return tag
    return re.sub(r"<img\b[^>]*>", one, html)


def landmarks(html: str) -> str:
    """A skip link, a <main>, and the hover-roll duplicates hidden from screen readers.

    Every footer link, header link and primary button prints its label twice
    for a hover roll; screen readers read both ("Video Production Video
    Production"). The second copy is presentation only. The 01-06 numerals are
    decoration on the values track, not six headings.

    Webflow's IX2 leaves initial states inline (data-w-id + opacity:0) for
    animations its runtime would play. That runtime is not on this site, so the
    About hero's eyebrow sat invisible forever — the state is stripped.
    """
    def second(m):
        return m.group(1) + ' aria-hidden="true"' + m.group(2)
    html = re.sub(r'(<p data-link-text="" class="(?:footer_link_text secondary-text|nav_link_text[^"]*)")(>)(?=[^<]*</p>\s*</a>)',
                  second, html)
    html = re.sub(r'(<p data-button-text="" class="button_text second_text")(>)', second, html)
    html = html.replace('<h2 class="year_text">', '<h2 class="year_text" aria-hidden="true">')
    html = re.sub(r'(<[^>]*data-w-id="[^"]*"[^>]*style="[^"]*?)opacity:\s*0;?\s*', r"\1", html)

    if 'id="main"' not in html:
        nav = html.find('class="navigation')
        first = min([i for i in (html.find("<section", nav), html.find('<div class="hero_spacer"', nav)) if i != -1])
        foot = html.find("<footer", first)
        if nav != -1 and first != -1 and foot != -1:
            html = html[:first] + '<main id="main">' + html[first:foot] + "</main>" + html[foot:]
    html = re.sub(r"(<body\b[^>]*>)", r'\1<a class="skip_link" href="#main">Skip to content</a>', html, count=1)
    return html


def _css_blocks(css: str):
    """(prelude, body, start, end) for each rule at this nesting level; strings and comments respected."""
    i, n = 0, len(css)
    while i < n:
        j, depth, pre = i, 0, None
        while j < n:
            c = css[j]
            if c in "\"'":
                q = c; j += 1
                while j < n and css[j] != q:
                    j += 2 if css[j] == "\\" else 1
            elif css.startswith("/*", j):
                j = css.find("*/", j) + 1
                if j == 0: j = n
            elif c == "{":
                if depth == 0: pre = j
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    yield css[i:pre], css[pre + 1:j], i, j + 1
                    break
            elif c == ";" and depth == 0:          # @charset / @import
                break
            j += 1
        i = j + 1


def _split_selectors(sel: str):
    out, depth, cur = [], 0, ""
    for ch in sel:
        if ch in "([": depth += 1
        elif ch in ")]": depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def purge_css(css: str, tokens: set):
    """Drop selectors that name a class nothing on the site can ever carry.

    A selector survives unless one of its classes appears nowhere in the built
    HTML or in any script (so classes added at runtime — w--current, is-open,
    pin-spacer, the SplitText classes — are kept). Rules without classes, and
    @font-face / @keyframes, are always kept. This removes only CSS that cannot
    match; it does not guess about state.
    """
    out, dropped = [], 0
    for pre, body, a, b in _css_blocks(css):
        head = re.sub(r"/\*.*?\*/", "", pre, flags=re.S).strip()
        if head.startswith(("@media", "@supports", "@container", "@layer")):
            inner, d = purge_css(body, tokens)
            dropped += d
            if inner.strip():
                out.append(pre + "{" + inner + "}")
            continue
        if head.startswith("@"):
            out.append(css[a:b]); continue
        keep = []
        for sel in _split_selectors(pre):
            classes = re.findall(r"\.(-?[_a-zA-Z][_a-zA-Z0-9-]*)", re.sub(r"\[[^\]]*\]", "", sel))
            if all(c in tokens for c in classes):
                keep.append(sel)
            else:
                dropped += 1
        if keep:
            out.append(",".join(keep) + "{" + body + "}")
    return "".join(out), dropped


def purge_main_css() -> tuple:
    """main.css is the reference's whole Webflow sheet; a phone used 25-46% of it."""
    tokens = set()
    for f in list(SITE.rglob("*.html")) + list((SITE / "assets" / "js").glob("*.js")) \
            + list((SITE / "assets" / "vendor").glob("*.js")):
        if "-test" in str(f):
            continue
        tokens |= set(re.findall(r"[A-Za-z0-9_-]+", f.read_text(encoding="utf-8", errors="ignore")))
    path = SITE / "assets" / "css" / "main.css"
    css = path.read_text(encoding="utf-8")
    purged, dropped = purge_css(css, tokens)
    path.write_text(purged, encoding="utf-8")
    return len(css), len(purged), dropped


def finalize(html: str) -> str:
    """Last passes on every written page, including the two built on the service shell."""
    return landmarks(lean_images(mobile_media(html)))


# --------------------------------------------- client comments, 16 Sep 2026
# docs/client-comments-2026-09-16.md. One pass per comment; each applies to
# every page this build writes, desktop and phone alike.

def instagram_only(html: str) -> str:
    """#1 — Instagram is the one social account the client keeps.

    TikTok and Facebook only ever pointed at the bare domains the reference
    shipped with. The hero row, the menu row and the footer lose both.
    """
    return re.sub(
        r'<a\b(?=[^>]*hero_social_icon_link)'
        r'(?=[^>]*href="https://(?:www\.)?(?:tiktok|facebook)\.com)[^>]*>[\s\S]*?</a>',
        "", html)


def footer_services_0916(html: str) -> str:
    """#17, #18 — the footer's Services column and its closing wordmark.

    "Work" is not a service, so it leaves the column, and "Video Production"
    becomes the way in to the film archive. The faded HELLOVOICE type at the
    foot of every page goes.
    """
    html = re.sub(
        r'<a data-link="" href="/projects/"[^>]*class="footer_link_widget[^"]*">'
        r'<p data-link-text="" class="footer_link_text">Work</p>.*?</a>',
        "", html, flags=re.S)
    html = html.replace(
        '<a data-link="" href="/service/#video-production" class="footer_link_widget w-inline-block">',
        '<a data-link="" href="/projects/" class="footer_link_widget w-inline-block">')
    return re.sub(r'<p class="logo_big_text">[^<]*</p>', "", html)


def leader_marquee(html: str) -> str:
    """#6 — Trusted by Leaders on a phone: two rows of the same logo cards,
    drifting in opposite directions, instead of the scroll-turned ring.

    The ring needs a screen and a half of height to turn and it stood its lower
    cards on their heads; at phone width it left a screen of empty page and
    crowded the heading. The rows use the ring's own cards, so the two can
    never list different brands. Shown below 768px only (clone.css).
    """
    i = html.find('<div class="leader_circle_wrapper">')
    if i < 0:
        return html
    j = html.find('</section>', i)
    imgs = re.findall(r'<img[^>]*class="leader_circle_image is-card"[^>]*/?>', html[i:j])
    if not imgs:
        return html
    cards = [re.sub(r'class="leader_circle_image is-card"', 'class="leader_marquee_card"', t)
             for t in imgs]
    def row(seq, cls):
        cells = "".join(f'<li>{c}</li>' for c in seq)
        return (f'<div class="leader_marquee_track {cls}">'
                f'<ul class="leader_marquee_row">{cells}</ul>'
                f'<ul class="leader_marquee_row" aria-hidden="true">{cells}</ul></div>')
    half = len(cards) // 2
    block = ('<div class="leader_marquee" data-leader-marquee>'
             + row(cards[:half] + cards[half:], "is-left")
             + row(cards[half:][::-1] + cards[:half][::-1], "is-right")
             + '</div>')
    return html[:i] + block + html[i:]


def service_tag_marquee(html: str) -> str:
    """#8, #9 — each services section's tag list becomes an auto-playing tag
    marquee under the section's pictures, instead of a long ruled list.

    The first copy of the row stays readable to assistive technology; the
    second exists only to close the loop and is hidden from it.
    """
    def one(sec):
        m = re.search(r'<ul class="svc_camp_list">.*?</ul>', sec, flags=re.S)
        if not m:
            return sec
        names = re.findall(r'<span class="svc_camp_name">(.*?)</span>', m.group(0), flags=re.S)
        sec = sec[:m.start()] + sec[m.end():]
        cells = "".join(f'<li class="svc_tag">{n}</li>' for n in names)
        block = ('<div class="svc_tag_marquee">'
                 '<div class="svc_tag_track">'
                 f'<ul class="svc_tag_row" aria-label="What this covers">{cells}</ul>'
                 f'<ul class="svc_tag_row" aria-hidden="true">{cells}</ul>'
                 '</div></div>')
        # under the pictures: straight after the catalogue grid closes
        c = re.search(r'<div class="svc_catalogue[^"]*">', sec)
        if not c:
            return sec
        depth = 0
        for t in re.finditer(r'<(/?)div\b[^>]*>', sec[c.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                at = c.start() + t.end()
                return sec[:at] + block + sec[at:]
        return sec
    return re.sub(r'<section class="svc_feature_section.*?</section>',
                  lambda m: one(m.group(0)), html, flags=re.S)


# ------------------------------------------- the short film, 17 Sep 2026
# HelloVoice's entry in the Higgsfield Global Film Festival. Details and the
# synopsis are the film's own page:
# https://higgsfield.ai/@hellovoice/projects/@id__0d8cb1f9-8534-4ad3-91d6-4def0a9b7549
FILM = {
    "title": "The Four Coats",
    "tagline": "Every house keeps its own rules",
    "synopsis": ("Four thieves enter an abandoned house expecting an easy score, "
                 "only to discover that the house has its own plans for them."),
    "runtime": "11 min",
    "url": ("https://higgsfield.ai/@hellovoice/projects/@id__0d8cb1f9-8534-4ad3-"
            "91d6-4def0a9b7549?from=%2Fcontests%2Fhiggsfield-global-film-festival"),
}


def film_feature(where: str = "") -> str:
    """Split screen: the vertical reel on one side, the billing on the other.

    The client's structure, 18 Sep 2026 — the wide cut of the film is gone and
    the reel carries the section alone. The poster is the ground only: blurred,
    and cropped past its printed title so nothing on it competes with the
    heading beside it.
    """
    return (
        f'<section class="film_feature{where}" id="the-four-coats" '
        'aria-labelledby="four-coats-title">'
        '<div class="film_feature_bg" aria-hidden="true"></div>'
        '<div class="padding_global"><div class="container">'
        '<div class="film_feature_inner">'
        '<div class="film_feature_head">'
        '<img class="film_feature_lockup" src="/assets/film/festival-lockup.png" '
        'width="1230" height="256" alt="Higgsfield Global Film Festival" '
        'loading="lazy" decoding="async"/>'
        '<p class="film_feature_kicker">'
        '<img src="/assets/film/higgsfield-mark.webp" width="128" height="128" '
        'alt="Higgsfield" loading="lazy" decoding="async"/>'
        '<span class="film_feature_brand">Higgsfield</span>'
        '<span class="film_feature_kicker_note">Our entry · 2026</span></p>'
        '</div>'
        '<figure class="film_feature_reel">'
        '<video class="film_feature_video" muted loop playsinline preload="none" '
        'poster="/assets/film/four-coats-reel-poster.webp" aria-hidden="true" tabindex="-1">'
        '<source src="/assets/film/four-coats-reel.mp4" type="video/mp4"/>'
        '</video>'
        '<figcaption class="film_feature_cap">Every asset, every prompt</figcaption>'
        '</figure>'
        '<div class="film_feature_body">'
        f'<h2 class="film_feature_title" id="four-coats-title">{HC.esc(FILM["title"])}</h2>'
        f'<p class="film_feature_tagline">{HC.esc(FILM["tagline"])}</p>'
        f'<p class="film_feature_synopsis">{HC.esc(FILM["synopsis"])}</p>'
        '</div>'
        '<ul class="film_feature_meta">'
        '<li>AI short film</li>'
        f'<li>{HC.esc(FILM["runtime"])}</li>'
        '<li>Written, directed and produced by HelloVoice</li>'
        '</ul>'
        '<div class="film_feature_actions">'
        f'<a class="film_feature_play" href="{FILM["url"]}" target="_blank" '
        'rel="noopener noreferrer">'
        '<span class="film_feature_play_glyph" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">'
        '<path d="M8 5v14l11-7z"/></svg></span>Watch the film</a>'
        '<span class="film_feature_note">Plays on Higgsfield</span>'
        '</div>'
        '</div></div></div></section>')


def film_on_home(html: str) -> str:
    """The short film takes Featured Works' place on the home page (17 Sep 2026).

    The four client cards go; every one of those films is still on the Work page.
    """
    m = re.search(r'<section class="work_section">', html)
    if not m:
        return html
    depth = 0
    for t in re.finditer(r"<(/?)section\b[^>]*>", html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            return html[:m.start()] + film_feature(" is-home") + html[end:]
    return html


def film_on_work(html: str) -> str:
    """The same section leads the Work page, above the filter."""
    m = re.search(r'<div class="works_filter"', html)
    if not m:
        return html
    return html[:m.start()] + film_feature(" is-work") + html[m.start():]


def drop_values_track(html: str) -> str:
    """The 01..06 values leave the home page (client, 17 Sep 2026); About keeps
    them. The statement above the track stays where it is."""
    m = re.search(r'<div class="about_track">', html)
    if not m:
        return html
    depth = 0
    for t in re.finditer(r"<(/?)div\b[^>]*>", html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html[:m.start()] + html[m.start() + t.end():]
    return html


def nav_without_work(html: str) -> str:
    """17 Sep 2026 — Work leaves the header bar and the full-screen menu; the
    client wants it reached from Services (Video Production -> /projects/)."""
    html = re.sub(r'<a data-link="" href="/projects/"[^>]*class="nav_link[^"]*">.*?</a>',
                  "", html, flags=re.S)
    return re.sub(r'<a href="/projects/"[^>]*class="canvas_menu_link[^"]*">.*?</div></div></a>',
                  "", html, flags=re.S)


def client_comments_0916(html: str) -> str:
    html = nav_without_work(html)
    html = leader_marquee(footer_services_0916(instagram_only(html)))
    return service_tag_marquee(html)


def body_inject() -> str:
    return ("".join(f'<script src="{v}"></script>\n' for v in VENDOR)
            + f'<script src="{asset("/assets/js/motion.js")}"></script>\n')


def transform(name: str, html: str, drop_hero: bool = True) -> str:
    html = strip_scripts(html)
    html = rewrite_assets(html)

    # Webflow's runtime stamps .w-mod-js on <html> before first paint; the
    # reference's stylesheet then hides every animated element until the IX3
    # runtime adds .w-mod-ix3. Reproduce the first half here — motion.js adds
    # the second once it has set initial states, with its own failsafe.
    html = re.sub(r'<html\b', '<html class="w-mod-js"', html, count=1)

    # stylesheet: the Webflow shared sheet becomes our localised copy
    html = re.sub(
        r'<link\b[^>]*href="[^"]*ariyana-studio\.webflow\.shared[^"]*"[^>]*/?>',
        head_inject().strip(), html, count=1)
    if "/assets/css/main.css" not in html:
        html = html.replace("</head>", head_inject() + "</head>", 1)

    # drop subresource-integrity: the files are now local and unhashed
    html = re.sub(r'\s+integrity="[^"]*"', "", html)
    html = re.sub(r'\s+crossorigin="anonymous"', "", html)
    html = re.sub(r'<link\b[^>]*rel="preconnect"[^>]*/?>', "", html)

    html = helv_logos(html, name)
    html = brand_name(html)
    html = error_plate(html)
    html = rewrite_links(html)
    html = strip_blog(html)
    html = nav_rework(html)
    html = menu_button_semantics(html)
    html = footer_socials(html)
    html = strip_dead_links(html)

    if name == "home":
        # sections two and three, between the hero and About: the client
        # marquee, then the full-bleed film
        html = html.replace(
            '<section class="about_section">',
            client_banner() + film_section() + '<section class="about_section">', 1)
        html = showreel_video(html)      # PLAY / REEL carries the BTS cut
        html = showreel_words(html)      # ...and the two words say which film

    if name == "projects":
        html = works_heading(html)
        html = work_header_badge(html)
        html = works_hero(html)
        html = works_filter(html)        # reads the tag links, so run it first
        html = tags_drive_filter(html)   # then turn them into filter controls
    elif name == "project-detail":
        html = tags_to_listing(html)

    html = HC.apply(html, name)          # HelloVoice's own words and work

    if name == "projects":
        # Both of these run after HC.apply, which is what generates the work
        # groups and the filter bar. Run earlier, exclusive_section found no
        # groups to sit above and fell back to inserting ahead of the whole
        # listing — which put the client's pick above their own page title.
        html = exclusive_section(html)
        html = work_separators(html)
        html = film_on_work(html)

    if name == "service":                # runs after HC: it adds the testimonials
        html = SP.apply(html, drop_hero=drop_hero)  # no videos; influencer + technology
        if drop_hero:
            # drop_hero is also what swaps this page's opening still for a film,
            # and a film hero needs the white lockup like the other two. The
            # Influencer page derives from this output with drop_hero False and
            # re-keys its own nav afterwards.
            html = knockout_nav(html)
    html = mark_placeholders(html)       # then tag whatever is still borrowed

    if HERO_EXCEPTION and name == "home":
        html = apply_hero_exception(html)

    if name == "home":
        html = work_card_buttons(html)
        html = hero_no_info(html)   # the hero loses its paragraph
        html = character_bts(html)
        html = value_numbers(html)   # the track carries values, not years
        # About lifts its values from the home page, and it keeps all six — so
        # the six-card copy is kept aside before Ethics is dropped here.
        global _HOME_VALUES_SRC
        _HOME_VALUES_SRC = html
        html = drop_values_track(html)   # the values live on About only
        html = home_order(html)      # hero, clients, film, values, services, work
        html = film_on_home(html)    # the short film stands where Featured Works did
    if name == "about-us":
        html = about_values(html, _HOME_VALUES_SRC or _HOME_HTML)   # all six values
        html = remove_awards(html)
        html = remove_why_choose(html)
        html = about_character(html)
        html = about_life_photos(html)
        html = about_media(html)      # the two picture slots become film
        html = about_clients(html)    # the home page's client band, shared
        html = rating_cluster(html)
    if name == "404":
        html = error_page_heading(html)
    if name == "contact-us":
        html = contact_direct(html)
    html = showreel_no_button(html)
    html = fix_svg_dimensions(html)
    html = preloader_animation(html)
    html = add_instagram(html)
    html = a11y_fixes(html)
    html = footer_dead_link(html)     # repoints the dead slot -> Influencer
    html = footer_pages(html)         # then reads that link to seat Technology
    html = brand_lockup(html)         # Blue Holding leads the header lockup
    html = dedupe_ids(html)
    html = no_cache(html)
    html = influencer_nav(html)
    html = client_comments_0916(html)
    html = html.replace("</body>", body_inject() + "</body>", 1)
    html = mark_hero_tone(html)   # last: the hero is final by now
    return html


def project_pages():
    """Every captured project detail page, keyed by its slug."""
    d = PAGES / "projects"
    return sorted(d.glob("*.html")) if d.exists() else []


def main():
    if not PAGES.exists():
        raise SystemExit(f"missing {PAGES} — capture the reference pages first")

    # wipe the previous build's pages, keep assets we are about to rewrite.
    # KEEP holds hand-authored pages that the build does not generate — the
    # sweep would otherwise delete them every run and they would 404.
    # "catalogue" is built by build/influencer_catalogue.py, not by this
    # script. Without it here the sweep deletes the client-facing roster on
    # every site build and the link 404s — which happened twice before anyone
    # noticed, because the page only disappears once you rebuild.
    KEEP = {"char-test", "eye-test", "spline-test", "scroll-test", "catalogue"}
    stale = set(SITE.glob("*.html")) | set(SITE.glob("**/index.html"))
    for p in stale:
        if "assets" not in p.parts and not (KEEP & set(p.parts)):
            p.unlink()
    for d in sorted(SITE.rglob("*"), key=lambda p: -len(p.parts)):
        if (d.is_dir() and "assets" not in d.parts
                and not (KEEP & set(d.parts)) and not any(d.iterdir())):
            d.rmdir()

    for _css in sorted((SITE / "assets" / "css").glob("*.css")):
        check_css(_css)
    check_spacing_tokens()

    n_assets = copy_assets()
    n_css = build_css()
    n_min = minify_assets()

    written = []
    check_posters()   # both sizes present, or stop

    for slug, route in ROUTES.items():
        src = PAGES / f"{slug}.html"
        if not src.exists():
            print(f"  ! missing page capture: {slug}")
            continue
        html = transform(slug, src.read_text(encoding="utf-8"))
        if slug == "home":
            # about-us lifts its values section from the finished home page, so
            # the two cannot drift. ROUTES is ordered with home first; if that
            # ever changes, about_values no-ops rather than emitting a broken
            # section, and this assert says why.
            global _HOME_HTML
            _HOME_HTML = html
        if route is None:
            dest = SITE / "404.html"
        elif route == "":
            dest = SITE / "index.html"
        else:
            dest = SITE / route / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = finalize(html)
        dest.write_text(html, encoding="utf-8")
        written.append((str(dest.relative_to(SITE)), len(html)))

    # Influencer Campaigns is HelloVoice's own page and has no reference
    # capture, so it is built on the service page's shell — same header,
    # footer, preloader and type, its own body.
    src = PAGES / "service.html"
    if src.exists():
        html = IP.build(transform("service", src.read_text(encoding="utf-8"),
                                  drop_hero=False))
        html = knockout_nav(html)   # its hero is a full-bleed film
        # Re-stamp: these two pages run transform() first and swap the hero in
        # afterwards, so the tone taken at the end of transform saw the shell's
        # hero rather than the film that replaced it.
        html = mark_hero_tone(html)
        dest = SITE / "service" / "influencer-campaigns" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = finalize(html)
        dest.write_text(html, encoding="utf-8")
        written.append((str(dest.relative_to(SITE)), len(html)))

    if src.exists():
        html = TP.build(transform("service-detail", src.read_text(encoding="utf-8")))
        html = knockout_nav(html)   # its hero is a full-bleed film too
        html = mark_hero_tone(html)
        dest = SITE / "service" / "technology-activations" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = finalize(html)
        dest.write_text(html, encoding="utf-8")
        written.append((str(dest.relative_to(SITE)), len(html)))

    # The work cards open Vimeo now, so the reference's own detail pages are
    # orphaned — and they carried the last of its project copy.
    for src in []:
        html = transform("project-detail", src.read_text(encoding="utf-8"))
        dest = SITE / "projects" / src.stem / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = finalize(html)
        dest.write_text(html, encoding="utf-8")
        written.append((str(dest.relative_to(SITE)), len(html)))

    # Purge last: it reads every page just written. The pages carry main.css's
    # stamp from before the purge, so it is swapped for the new one after.
    import os
    if os.environ.get("HELV_NO_PURGE") != "1":
        old = stamp("/assets/css/main.css")
        size0, size1, dropped = purge_main_css()
        new = stamp("/assets/css/main.css")
        for rel, _ in written:
            f = SITE / rel
            f.write_text(f.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
        print(f"purge   main.css {size0:,} -> {size1:,} bytes, {dropped} selectors dropped")

    print(f"assets  {n_assets} files -> site/assets/ref")
    print(f"css     {n_css:,} bytes -> site/assets/css/main.css")
    print(f"minify  {n_min} files")
    for path, size in written:
        print(f"page    {path:<44} {size:,} bytes")


if __name__ == "__main__":
    main()
