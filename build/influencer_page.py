"""The Influencer Campaigns page, built on the service page's shell.

There is no reference capture for this page — it is HelloVoice's own. Rather
than author a new document (and drift from the template's header, footer,
preloader, type and spacing), it reuses the captured service page and swaps
everything between the hero and the CTA for its own sections.

The content is the 86 reposts captured from instagram.com/helv.studio/reposts.
Two deliberate constraints shape how they are shown:

  * Thumbnails are Instagram's public Open Graph poster for each post, fetched
    once and stored under site/assets/ig. Storing the *URL* would have rotted
    within days (they are signed and expire); storing the bytes does not.
  * Campaigns come from the @mentions, hashtags and links in each caption.
    "Other campaigns" is the honest residual where no brand is named — it is
    not a guess.
  * No third-party frame until a click. Instagram's /embed/ page is loaded into
    the existing lightbox on demand, so nothing from Instagram is fetched when
    the page loads.

Copy marked WRITTEN below is mine, not the client's, and needs their sign-off.
"""
import html as _html
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "content" / "influencer.json"

# The first screenful of tiles; the rest arrive on request. 24 is two full
# rows at the widest breakpoint and keeps the initial DOM small.
FIRST_BATCH = 24

# WRITTEN — needs client sign-off.
LEDE = ("We cast, brief and run creator campaigns end to end — from shortlisting "
        "talent against the brief to delivering the cutdowns the brand actually "
        "ships. Every film below was produced and published through HelloVoice.")

# WRITTEN — needs client sign-off.
STEPS = [
    ("Casting", "Shortlisted against the brief — audience, category fit and "
                "past brand work, not follower count alone."),
    ("Brief & script", "A per-creator brief that protects the claim set and "
                       "still sounds like them."),
    ("Production", "Shot by the creator or by our crew, to the same spec "
                   "either way."),
    ("Compliance", "Every claim checked before it posts — the pharma work "
                   "leaves no room for a re-cut after the fact."),
    ("Delivery & reporting", "Master files, cutdowns and a post-by-post "
                             "performance read."),
]


def esc(s: str) -> str:
    return _html.escape(str(s), quote=True)


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def _hue(handle: str) -> int:
    """A stable hue per creator, so the grid reads as many hands rather than
    one repeated tile. Deterministic from the handle, kept inside a red-to-
    amber arc (-18..+42 degrees off the brand red) so nothing lands on a colour
    the palette does not own."""
    h = 0
    for ch in handle:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return -18 + (h % 61)


# Engagement read from Instagram, keyed by shortcode. Likes and comments only:
# views and shares live in Insights, which is visible to the account that owns
# a post, and these posts belong to the creators rather than to HelloVoice.
# Fourteen of the eighty-six publish no counts at all — those creators have
# hidden them — and those tiles carry no bar rather than a zero, because a zero
# is a claim and an absence is the truth.
def _kpis():
    f = ROOT / "content" / "influencer-kpis.csv"
    if not f.exists():
        return {}
    out = {}
    with f.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            likes = row.get("likes", "")
            comments = row.get("comments", "")
            reposts = row.get("reposts", "")
            # A post qualifies on any real metric, not on likes alone. Fourteen
            # of these hide their like count — the Like icon carries no number
            # at all — but publish comments and reposts, and a tile with two
            # real figures on it should not be blank because the third is
            # private. Each value is None when absent rather than zero: zero is
            # a claim, absent is the truth.
            row_vals = (
                int(likes) if likes.isdigit() else None,
                int(comments) if comments.isdigit() else None,
                int(reposts) if reposts.isdigit() else None,
            )
            if any(v is not None for v in row_vals):
                out[row["shortcode"]] = row_vals
    return out


KPIS = _kpis()


def _compact(n):
    """1200 -> 1.2k. A four-figure count in a 20px bar wraps the row."""
    if n >= 1000:
        s = f"{n/1000:.1f}".rstrip("0").rstrip(".")
        return s + "k"
    return str(n)


HEART = ('<svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor" '
         'aria-hidden="true"><path d="M12 21s-7.5-4.9-9.6-9A5.4 5.4 0 0 1 12 '
         '6.2 5.4 5.4 0 0 1 21.6 12c-2.1 4.1-9.6 9-9.6 9z"/></svg>')
REPOST = ('<svg viewBox="0 0 24 24" width="13" height="13" fill="none" '
          'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
          'stroke-linejoin="round" aria-hidden="true">'
          '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/>'
          '<path d="M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>')
SPEECH = ('<svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor" '
          'aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 '
          '8 0 1 1 21 12z"/></svg>')


def _kpi_bar(shortcode):
    """A band of real engagement under a tile, or nothing.

    Nothing is deliberate for a post whose counts are hidden: rendering "0
    likes" there would state something false about work that may have done
    perfectly well.
    """
    hit = KPIS.get(shortcode)
    if not hit:
        return ""
    likes, comments, reposts = hit
    parts = []
    for value, glyph, unit in ((likes, HEART, "likes"),
                               (comments, SPEECH, "comments"),
                               (reposts, REPOST, "reposts")):
        if value is None:
            continue          # hidden by the creator; the gap is the honest answer
        parts.append(
            f'<span class="ig_kpi" title="{value:,} {unit}">{glyph}'
            f'<span>{_compact(value)}</span>'
            f'<span class="u-sr-only"> {unit}</span></span>')
    if not parts:
        return ""
    return '<div class="ig_card_kpis">' + "".join(parts) + '</div>'


# The influencer page shows the same roster as the landing page's banner, at
# the client's instruction — one client list, stated once, rather than a
# separate shortlist per page that has to be kept in step by hand.
#
# Imported rather than copied: clone.BANNER_CLIENTS is built from the 63
# artboards the client supplied, so adding a logo there adds it here.


def brand_band() -> str:
    """A row of the brands behind the campaigns on this page.

    A static row rather than the home page's marquee. Nine marks do not need to
    scroll, and a row that holds still can be read — the marquee exists on the
    home page because the full roster is fifty-seven and could not fit.

    Each logo is a 1x/2x pair authored at 64px optical height, so they sit at a
    consistent weight beside each other rather than at whatever size their
    source happened to be.
    """
    import clone as _clone           # imported here: clone imports this module
    have = [(slug, name) for slug, name in _clone.BANNER_CLIENTS
            if (ROOT / "site" / "assets" / "clients" / f"{slug}.webp").exists()]
    if not have:
        return ""
    marks = "".join(
        f'<li class="ig_brand"><img src="/assets/clients/{slug}.webp" '
        f'srcset="/assets/clients/{slug}.webp 1x, /assets/clients/{slug}@2x.webp 2x" '
        f'alt="{esc(name)}" loading="lazy" decoding="async" height="32"/></li>'
        for slug, name in have)
    # Fifty-seven marks cannot wrap into a static block without becoming a wall,
    # so this is the home page's marquee treatment: one row, scrolling, the set
    # printed twice so the loop has somewhere to go.
    return (
        '<section class="ig_brands_section">'
        '<div class="padding_global"><div class="container">'
        '<p class="ig_brands_heading">'
        '<span class="ig_brands_dot" aria-hidden="true"></span>'
        'Trusted by leading multinational brands</p>'
        '</div></div>'
        '<div class="ig_brands_track" data-ig-brands>'
        f'<ul class="ig_brands_row">{marks}</ul>'
        f'<ul class="ig_brands_row" aria-hidden="true">{marks}</ul>'
        '</div></section>')


def _tile(p, i):
    """One tile: the post's own poster, with the handle and campaign over it.

    The play control is a button and the permalink is a separate link beneath,
    so "watch here" and "open on Instagram" stay distinguishable to a screen
    reader instead of collapsing into one ambiguous target.
    """
    handle = esc(p["handle"])
    camp = esc(p.get("campaign", "Other campaigns"))
    return (
        f'<article class="ig_card" data-campaign="{camp}"'
        f'{"" if i < FIRST_BATCH else " hidden"}>'
        f'<button type="button" class="ig_card_play"'
        f' data-ig-embed="{esc(p["embed"])}"'
        f' data-title="@{handle} — {camp}"'
        f' aria-label="Play the reel by @{handle} for {camp}">'
        f'<img class="ig_card_img" src="{esc(p["thumb"])}" alt="" loading="lazy"'
        f' decoding="async" width="480" height="854"/>'
        f'<span class="ig_card_glyph" aria-hidden="true">'
        f'<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor">'
        f'<path d="M8 5v14l11-7z"/></svg></span>'
        # The creator's handle is deliberately not shown. The client's call is
        # that the page sells the campaign, not the roster — and a wall of
        # third-party handles reads as their credits, not HelloVoice's. The
        # handle stays in the accessible name and the outbound link so the work
        # is still attributable, just not shouted.
        f'<span class="ig_card_meta">'
        f'<span class="ig_card_campaign">{camp}</span></span>'
        f'</button>'
        + _kpi_bar(pathlib.Path(p["thumb"]).stem) +
        f'<a class="ig_card_link" href="{esc(p["permalink"])}"'
        f' target="_blank" rel="noopener noreferrer">'
        f'View on Instagram<span class="u-sr-only"> — @{handle}</span></a>'
        f'</article>')


def interleave(posts):
    """Mix the campaigns so the wall does not run in brand blocks.

    Capturing the reposts in feed order grouped them by campaign, so the grid
    opened with twenty-six Alpha Plus tiles then thirteen SVR — which reads as
    two clients rather than a body of work.

    This is a round-robin across the campaign buckets rather than a shuffle.
    A shuffle only makes long runs *unlikely*; dealing one from each bucket in
    turn makes them impossible while the buckets last, and it is deterministic,
    so the order does not churn on every rebuild. The larger campaigns
    inevitably tail out on their own at the end, once the small ones are spent.
    """
    buckets = {}
    for post in posts:
        buckets.setdefault(post.get("campaign") or "Other campaigns", []).append(post)
    # biggest bucket first so the tail is one campaign rather than an abrupt stop
    order = sorted(buckets, key=lambda k: -len(buckets[k]))
    out = []
    while any(buckets[k] for k in order):
        for k in order:
            if buckets[k]:
                out.append(buckets[k].pop(0))
    return out


# Posts the client has pulled from the grid, keyed by the Instagram shortcode
# that names their thumbnail. Held here rather than deleted from
# content/influencer.json so the capture stays a faithful record of what was
# collected — the site filters, the data does not lose anything.
PULLED = {
    "DbA_ZjID1VC",   # SVR, four-panel grid
    "Da2qmYYiqpt",   # SVR, dresser
    "DZCQ2HasrF4",   # Other campaigns, TV segment
}


def _pulled(post):
    stem = (post.get("thumb") or "").rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return stem in PULLED


# ------------------------------------------------ the creator catalogue CTA
# Client comment #14 (16 Sep 2026): a section that sells the catalogue, and the
# same button in several places on the page. WRITTEN — the benefit lines are
# drawn from what /catalogue/ actually does; they need client sign-off.
# The catalogue runs on its own host with its own API (deploy/README.md); a
# static copy of the site cannot unlock it, so every button goes there.
CATALOGUE_URL = "https://influencer-catalogue.hellovoice.co.uk/"
CATALOGUE_BENEFITS = [
    ("Browse the roster", "Creators sorted by tier — nano to macro — and by "
                          "category: beauty, skincare, hair care, fragrance, "
                          "make-up and lifestyle."),
    ("Build a shortlist", "Pick the creators that fit the brief and review the "
                          "selection as one list."),
    ("One quote for the set", "Costs are quoted for the shortlist as a whole, "
                              "not creator by creator."),
    ("Share it privately", "Send the selection to your team with a link; access "
                           "stays behind your code."),
]


def catalogue_button(extra: str = "") -> str:
    return (f'<a class="ig_cat_button {extra}" href="{CATALOGUE_URL}">'
            '<span>Open the creator catalogue</span>'
            '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>')


def catalogue_section() -> str:
    items = "".join(
        f'<li class="ig_cat_benefit"><span class="ig_cat_n">{i + 1:02d}</span>'
        f'<h3 class="ig_cat_title">{esc(t)}</h3><p class="ig_cat_text">{esc(b)}</p></li>'
        for i, (t, b) in enumerate(CATALOGUE_BENEFITS))
    return (
        '<section class="ig_cat_section" aria-labelledby="ig-cat-title">'
        '<div class="padding_global"><div class="container">'
        '<div class="ig_cat_top">'
        '<div class="ig_cat_head">'
        '<p class="ig_cat_kicker">Creator catalogue</p>'
        '<h2 class="ig_cat_heading" id="ig-cat-title">Find the right creators '
        'before the first call</h2>'
        '<p class="ig_cat_lede">Our private roster of vetted creators, ready to '
        'filter, shortlist and quote — open it with the access code we sent you.</p>'
        '</div>'
        f'<a class="ig_cat_cover" href="{CATALOGUE_URL}" tabindex="-1" aria-hidden="true">'
        '<img src="/assets/catalogue-cover/catalogue-cover-1600.webp" '
        'srcset="/assets/catalogue-cover/catalogue-cover-800.webp 800w, '
        '/assets/catalogue-cover/catalogue-cover-1600.webp 1600w" '
        'sizes="(max-width: 991px) 92vw, 46vw" width="1600" height="900" '
        'alt="" loading="lazy" decoding="async"/></a>'
        '</div>'
        f'<ol class="ig_cat_benefits">{items}</ol>'
        '<div class="ig_cat_actions">' + catalogue_button("is-primary") +
        '<p class="ig_cat_note">No code yet? <a href="/contact-us/">Ask us for access</a>.</p>'
        '</div></div></div></section>')


def build(html: str) -> str:
    d = load()
    posts = interleave([p for p in d["posts"] if not _pulled(p)])
    creators = d["creators"]
    n_posts = len(posts)
    n_creators = len(creators)

    # CLIENT FIGURES — the agency's totals, supplied by HelloVoice, not counted
    # from this dataset. They deliberately outrun the grid below, which shows
    # the 86 films we actually hold; see the note on the work section's badge.
    stats = [("1500", "Films published"),
             ("1800", "Creators"),
             ("UAE · KSA · Egypt", "Markets covered")]

    # A full-height hero built ON the showreel rather than above it: the film
    # is the background, the copy sits over it behind a scrim. The stats come
    # along so the first screen carries the whole claim — who we are, what we
    # do, and the scale of it — without the visitor scrolling.
    #
    # The film itself is still the client's to supply. Until it lands the media
    # layer renders as a labelled placeholder, which is why the scrim and the
    # copy are styled against a dark ground rather than against the film: the
    # type has to stay readable whichever arrives.
    hero = (
        '<section class="service_hero_section is-influencer is-reel-hero">'
        # The client's UGC reel. Muted + playsinline + autoplay is the only
        # combination a browser will start unprompted, and the poster covers
        # the first frames so the hero is never a black rectangle while the
        # file arrives. 66MB of master at 1920x1080 became 10.1MB — kept at
        # full height rather than the 1280 the earlier montage used, since the
        # client asked for 1080p on the films that carry a page.
        '<div class="ig_hero_media" data-reel-slot>'
        '<video class="ig_hero_video" autoplay muted loop playsinline '
        'preload="metadata" poster="/assets/video/hero-reel-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/hero-reel.mp4" type="video/mp4"/>'
        '</video></div>'
        '<div class="ig_hero_scrim" aria-hidden="true"></div>'
        '<div class="padding_global"><div class="container">'
        '<div class="ig_hero_copy">'
        # No data-title-anim and no lede: the client's call. The film behind
        # it is the introduction, and a headline that assembles itself over a
        # moving background was competing with it rather than landing on it.
        '<h1 class="service_hero_title">Influencer Campaigns</h1>'
        '<div class="ig_stats">'
        + "".join(
            f'<div class="ig_stat"><p class="ig_stat_num">{esc(n)}</p>'
            f'<p class="ig_stat_label">{esc(l)}</p></div>' for n, l in stats)
        + '</div>' + catalogue_button("is-hero") + '</div></div></div></section>')

    steps = (
        '<section class="ig_steps_section" data-hv-slider="How a campaign runs">'
        '<div class="padding_global"><div class="container">'
        '<div class="section_header"><h2 data-title-anim="" class="service_section_title">'
        'How a campaign runs</h2>'
        '<div data-floating-badge="" class="floating_text">FIVE STAGES</div></div>'
        '<ol class="ig_steps" data-hv-slider-track>'
        + "".join(
            f'<li class="ig_step"><span class="ig_step_num">Step {i + 1:02d}</span>'
            f'<h3 class="ig_step_title">{esc(t)}</h3>'
            f'<p class="ig_step_info">{esc(b)}</p></li>'
            for i, (t, b) in enumerate(STEPS))
        + '</ol>' + catalogue_button("is-after-steps") + '</div></div></section>')

    # Filter chips. Real buttons carrying aria-pressed, not clickable divs, and
    # the collection wraps rather than clipping — both per the UX guidance for
    # compact interactive controls.
    # The brand chips are gone at the client's request. Every tile still names
    # its campaign, so the information is not lost — it just no longer invites
    # the visitor to slice a 47-creator body of work into a client list.
    chips = ""

    grid = (
        brand_band() +
        '<section class="ig_work_section"><div class="padding_global">'
        '<div class="container">'
        '<div class="section_header"><h2 data-title-anim="" class="service_section_title">'
        'The work</h2>'
        f'<div data-floating-badge="" class="floating_text">{n_posts} SELECTED</div></div>'
        + chips +
        '<div class="ig_grid" id="ig-grid">'
        + "".join(_tile(p, i) for i, p in enumerate(posts))
        + '</div>'
        f'<button type="button" class="ig_more" data-ig-more'
        f' data-step="{FIRST_BATCH}">'
        f'Show more <span class="ig_more_count">'
        f'({n_posts - FIRST_BATCH} left)</span></button>'
        '</div></div></section>')

    # The catalogue section follows the portfolio (client, 16 Sep 2026): the
    # visitor has seen the work before being offered the roster.
    body = hero + steps + grid + catalogue_section()

    # Swap everything from the service hero up to the CTA, keeping the shell's
    # header, CTA and footer exactly as the template has them.
    out, n = re.subn(
        r'<section class="service_hero_section".*?(?=<section class="cta_section")',
        lambda _m: body, html, count=1, flags=re.S)
    if not n:
        raise SystemExit("influencer: could not find the service hero -> cta span")

    out = out.replace("<title>", "<title>Influencer Campaigns — ", 1)
    return out
