"""Service page restructure, and the Technology Activations detail page.

The reference's service page opens with four autoplaying loops inside the
service cards. They are the reference's own stock footage, they push "What we
make" below the fold, and four simultaneous videos is a real cost on a page
whose job is to list capabilities. They come out; the page now opens on the
list itself.

Two disciplines then get their own section below it, because they are the two
that need more than a tag list to explain — influencer work has a catalogue
behind it, and technology activations are physical installations people have to
picture. Each section ends in a button through to its own page.

Copy marked WRITTEN is mine and needs the client's sign-off.
"""
import html as _html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "content" / "influencer.json"
TECH_DATA = ROOT / "content" / "technology.json"
PROJECTS_DATA = ROOT / "content" / "projects.json"

# WRITTEN — needs client sign-off. The services page's own opening line.
# Summarised at the client's request (16 Sep 2026) so the film behind it shows.
SERVICES_LEDE = ("Film, CGI, live production and immersive technology — "
                 "from brief to final cut, under one roof.")

# WRITTEN — needs client sign-off.
INFLUENCER_LEDE = (
    "Creator campaigns run end to end — casting against the brief, per-creator "
    "scripts that protect the claim set, compliance before anything posts, and "
    "a post-by-post read afterwards.")

# WRITTEN — needs client sign-off.
TECH_LEDE = (
    "Installations people walk up to and use: mixed reality, holographic "
    "display, interactive screens and projection, built for congresses, "
    "launches and retail floors across the Gulf.")

TECH = [
    ("Mixed Reality", "Presenters and product sharing one stage, composited live."),
    ("VR Experiences", "Headset journeys for mechanism-of-action and facility tours."),
    ("Hologram Box", "Free-standing holographic display for product and data."),
    ("Interactive Screens", "Touch and gesture walls for congress stands."),
    ("Smart Cube", "A four-face volumetric unit for launches."),
    ("Laser & Projection", "Projection mapping and laser for stage moments."),
]


def esc(s):
    return _html.escape(str(s), quote=True)


def _anchor_button(href, label):
    """A hero button that scrolls to a section on this same page.

    Same component as _button so the hover mask and the label roll match every
    other button on the site — only the destination differs. Lenis owns the
    scroll, so a bare hash jump would fight it; motion.js intercepts
    [data-scroll-to] and hands the target to Lenis instead.
    """
    return (
        f'<a href="{esc(href)}" data-scroll-to="{esc(href)}" data-button-primary="" '
        f'class="button_primary w-inline-block is-hero">'
        '<div class="button_line_mask_wrapper">'
        '<div data-button-line-mask="" class="button_line_mask"></div>'
        '<div data-button-line-mask="" class="button_line_mask _2"></div>'
        '<div data-button-line-mask="" class="button_line_mask _3"></div></div>'
        '<div data-button-line="" class="button_line"></div>'
        '<div class="button_text_wrapper">'
        f'<p data-button-text="" class="button_text">{esc(label)}</p>'
        f'<p data-button-text="" class="button_text second_text">{esc(label)}</p>'
        '</div></a>')


def _button(href, label):
    """The template's own primary button, so it inherits the hover mask."""
    return (
        f'<a href="{esc(href)}" data-button-primary="" '
        f'class="button_primary w-inline-block">'
        '<div class="button_line_mask_wrapper">'
        '<div data-button-line-mask="" class="button_line_mask"></div>'
        '<div data-button-line-mask="" class="button_line_mask _2"></div>'
        '<div data-button-line-mask="" class="button_line_mask _3"></div></div>'
        '<div data-button-line="" class="button_line"></div>'
        '<div class="button_text_wrapper">'
        f'<p data-button-text="" class="button_text">{esc(label)}</p>'
        # `second_text`, not `is_2`: the template prints every button label twice
        # for its hover swap, and it is the .second_text rule that parks the
        # second copy one line below and lets the wrapper's overflow clip it.
        # Under any other class name both copies sit in flow, the wrapper grows
        # to fit them, and the label reads twice over.
        f'<p data-button-text="" class="button_text second_text">{esc(label)}</p>'
        '</div></a>')


def film_hero(html: str) -> str:
    """Replace the reference's still hero with the studio showreel and a title.

    The reference opens this page on one photograph with a scroll cue over it —
    a screen of nothing before the answer on a page whose job is to say what
    HelloVoice makes. It was taken out entirely for a while; the client's call
    now is a film with a heading over it, and "What we make" directly after.

    The showreel rather than a discipline reel: this page is the whole offer,
    and the film that stands for all of it is the one the studio already cuts.
    Checked for the burned-in logo the technology films carry — it has none, so
    it plays uncropped.
    """
    m = re.search(r'<section[^>]*\bclass="[^"]*service_hero_section', html)
    if not m:
        raise SystemExit("service: hero section not found")
    depth, end = 0, None
    for t in re.finditer(r"<(/?)section\b[^>]*>", html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        raise SystemExit("service: hero section never closes")

    # Built like the Technology Activations hero: the film behind, a display
    # title, a line saying what the studio actually offers, and a way into each
    # of the two disciplines that have their own page. The two buttons are
    # in-page anchors rather than links away — both sections are further down
    # this page, and sending a visitor to another URL to reach something they
    # can already scroll to is the wrong move.
    hero = (
        '<section class="service_hero_section is-services is-reel-hero">'
        '<div class="ig_hero_media" data-reel-slot>'
        '<video class="ig_hero_video" autoplay muted loop playsinline '
        'preload="metadata" poster="/assets/video/service-reel-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/service-reel.mp4" type="video/mp4"/>'
        '</video></div>'
        '<div class="ig_hero_scrim" aria-hidden="true"></div>'
        '<div class="padding_global"><div class="container">'
        '<div class="ig_hero_copy">'
        '<h1 class="service_hero_title">Hello Voice Services</h1>'
        f'<p class="ig_lede">{esc(SERVICES_LEDE)}</p>'
        '<div class="svc_hero_actions">'
        + _anchor_button("#video-production", "Video production")
        + _anchor_button("#influencer-campaigns", "Influencer campaigns")
        + _anchor_button("#technology-activations", "Technology activations")
        + '</div>'
        '</div></div></div></section>')
    return html[:m.start()] + hero + html[end:]


def remove_testimonials(html: str) -> str:
    """Drop the testimonial pile from the service page.

    The client's call: nothing replaces it. The quotes still run on the home
    page, which is where a visitor meets the studio; repeating them here pushed
    the disciplines further from the CTA without adding anything new.
    """
    return re.sub(r'<section[^>]*\bclass="[^"]*testimonial_section[^"]*"[\s\S]*?</section>',
                  "", html, count=1)


def cut_element(html: str, open_pattern: str) -> str:
    """Remove every <div> matching open_pattern, including its whole subtree.

    A regex cannot do this. `<div class="x">.*?</div>` stops at the first
    closing tag inside the subtree, not the one that matches — so it removes an
    unbalanced fragment and leaves the surplus </div>s behind. On this page that
    silently closed .container, .padding_global and the <section> early, and the
    browser hoisted the remaining service cards out to <body>, where they lost
    the layout's side padding and stacked on top of each other.

    So walk the tags and track depth instead.
    """
    out, pos = [], 0
    for m in re.finditer(open_pattern, html):
        if m.start() < pos:
            continue
        depth, i = 0, m.start()
        for t in re.finditer(r'<(/?)div\b[^>]*>', html[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                i = m.start() + t.end()
                break
        else:
            continue                       # unterminated: leave it alone
        out.append(html[pos:m.start()])
        pos = i
    out.append(html[pos:])
    return "".join(out)


def strip_service_videos(html: str) -> str:
    """Drop the looping film from each service card.

    The whole wrap goes, not just the <video> — an empty 16:9 box would leave a
    hole in the card's grid and read as a failed image.
    """
    return cut_element(html, r'<div class="service_item_video_wrap">')


def influencer_section() -> str:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    posts, camps = d["posts"], d["campaigns"]
    # a strip of the catalogue, one film per campaign so the row shows range
    seen, strip = set(), []
    for p in posts:
        c = p.get("campaign")
        if c in seen:
            continue
        seen.add(c)
        strip.append(p)
        if len(strip) == 6:
            break

    return (
        '<section class="svc_feature_section is-influencer" id="influencer-campaigns">'
        '<div class="padding_global"><div class="container">'
        '<div class="section_header">'
        '<h2 data-title-anim="" class="service_section_title">Influencer campaigns</h2>'
        # The figure the destination page states, not a count of this strip.
        # A visitor who reads "86 FILMS" here and "1500 Films published" one
        # click later has been told two different things about the same body of
        # work. CLIENT FIGURE — see the influencer page's own stats block.
        f'<div data-floating-badge="" class="floating_text">'
        f'1500 FILMS</div></div>'
        f'<p class="svc_feature_lede">{esc(INFLUENCER_LEDE)}</p>'
        '<div class="svc_catalogue">'
        + "".join(
            f'<a class="svc_cat_item" href="/service/influencer-campaigns/" '
            f'aria-label="{esc(p.get("campaign","Campaign"))} — see the catalogue">'
            f'<img src="{esc(p["thumb"])}" alt="" loading="lazy" decoding="async" '
            f'width="480" height="854"/>'
            f'<span class="svc_cat_label">{esc(p.get("campaign",""))}</span></a>'
            for p in strip)
        + '</div>'
        # The per-brand tally is gone at the client's request. It read as an
        # internal report — a client list with counts beside it — on a page
        # whose job is to show the work, and it contradicted the badge above it.
        + _button("/service/influencer-campaigns/", "See the catalogue")
        + '</div></div></section>')


# WRITTEN — needs client sign-off.
VIDEO_LEDE = (
    "Commercials, corporate films, live production, CGI and interviews — the "
    "core of the studio. Scripted, shot, cut and delivered in as many language "
    "versions as the campaign needs.")


# WRITTEN — needs client sign-off. Taken from the portfolio's own six sections
# plus the two the catalogue shows but does not name as categories.
VIDEO_SERVICES = [
    "Commercials", "Corporate films", "Event & live production",
    "CGI & anamorphic", "Awareness & patient education",
    "Interviews & testimonials", "Animation", "Localisation",
]


def video_section() -> str:
    """The Video Production teaser, first of the three disciplines.

    Built exactly like the influencer and technology blocks below it so the
    three read as one family rather than as one section plus two variations:
    heading, badge, lede, a strip of real stills, one button.

    The strip takes one film per section of the portfolio, so a visitor sees
    the range of work rather than five angles on the same shoot. Films are
    chosen from projects.json — the same source the works page is built from —
    so a still here can never advertise something the destination does not hold.

    The button goes to the works page, which is now reached from here rather
    than from the header.
    """
    projects = json.loads(PROJECTS_DATA.read_text(encoding="utf-8"))

    # Landscape only. The strip is a row of equal boxes, so a 9:16 film in it
    # either crops to nothing or forces the whole row to its height — which is
    # what made this section look broken next to the other two. Every section
    # of the portfolio has at least one 16:9 film, so filtering costs no range.
    seen, strip = set(), []
    for pr in projects:
        sec = pr.get("section")
        if not sec or sec in seen or not pr.get("img"):
            continue
        if pr.get("ratio") != "16:9":
            continue
        seen.add(sec)
        strip.append(pr)
        # Three, not five. The row is three across, so five left a second row
        # holding two tiles and a gap where the third should be — which reads
        # as something failing to load rather than as a deliberate short row.
        if len(strip) == 3:
            break
    if not strip:
        raise SystemExit("video_section: no projects with a still")

    return (
        '<section class="svc_feature_section is-video" id="video-production">'
        '<div class="padding_global"><div class="container">'
        '<div class="section_header">'
        '<h2 data-title-anim="" class="service_section_title">Video production</h2>'
        f'<div data-floating-badge="" class="floating_text">'
        f'{len(projects)} FILMS</div></div>'
        f'<p class="svc_feature_lede">{esc(VIDEO_LEDE)}</p>'
        # What the discipline actually covers, named. The other two sections
        # carry the same row, so the three read as one family.
        '<ul class="svc_camp_list">'
        + "".join(f'<li><span class="svc_camp_name">{esc(t)}</span></li>'
                  for t in VIDEO_SERVICES)
        + '</ul>'
        '<div class="svc_catalogue">'
        + "".join(
            f'<a class="svc_cat_item" href="/projects/" '
            f'aria-label="{esc(pr.get("section","Film"))} — see the work">'
            f'<img src="/assets/work/{esc(pr["img"])}-700.webp" '
            f'srcset="/assets/work/{esc(pr["img"])}-700.webp 700w, '
            f'/assets/work/{esc(pr["img"])}-1400.webp 1400w" '
            f'sizes="(max-width: 991px) 45vw, 260px" '
            f'alt="" loading="lazy" decoding="async"/>'
            f'<span class="svc_cat_label">{esc(pr.get("section",""))}</span></a>'
            for pr in strip)
        + '</div>'
        + _button("/projects/", "See the work")
        + '</div></div></section>')


def technology_section() -> str:
    """The Technology teaser, built like the influencer one — real films, not a
    list of format names.

    It used to be six cards of text. The influencer block beside it opens with
    six stills you can click, and next to that a text grid read as the poor
    relation of the two disciplines — which is the opposite of true: the
    technology work is the more visual of the pair.

    So it leads with posters from the catalogue's own live films, one per
    application so the row shows range rather than four angles on the same
    installation. Only applications that actually have a film with an id are
    eligible — the catalogue derives its status the same way, so a card here can
    never advertise something the detail page then admits has no material.
    """
    banks = json.loads(TECH_DATA.read_text(encoding="utf-8"))

    strip, n_films = [], 0
    for bank in banks:
        for app in bank["applications"]:
            films = [f for f in (app.get("films") or []) if f.get("id")]
            n_films += len(films)
            if not films or not app.get("poster"):
                continue
            if len(strip) < 4:
                stem = pathlib.Path(app["poster"]).stem
                strip.append((app["name"], stem, films[0]))

    n_apps = sum(len(b["applications"]) for b in banks)

    tiles = "".join(
        f'<a class="svc_cat_item is-wide" href="/service/technology-activations/#{esc(name).replace(" ", "-")}" '
        f'aria-label="{esc(name)} — explore the formats">'
        f'<img src="/assets/tech/{esc(stem)}.webp" alt="" loading="lazy" '
        f'decoding="async" width="720" height="405"/>'
        f'<span class="svc_cat_label">{esc(name)}</span></a>'
        for name, stem, _film in strip)

    return (
        '<section class="svc_feature_section is-tech" id="technology-activations">'
        '<div class="padding_global"><div class="container">'
        '<div class="section_header">'
        '<h2 data-title-anim="" class="service_section_title">Technology activations</h2>'
        # Same reasoning: the technology page counts what it can build, not
        # how many films this document happens to hold. CLIENT FIGURE.
        f'<div data-floating-badge="" class="floating_text">'
        f'+50 APPLICATIONS</div></div>'
        f'<p class="svc_feature_lede">{esc(TECH_LEDE)}</p>'
        f'<div class="svc_catalogue is-tech">{tiles}</div>'
        '<ul class="svc_camp_list">'
        + "".join(
            f'<li><span class="svc_camp_name">{esc(t)}</span></li>' for t, _b in TECH)
        + '</ul>'
        + _button("/service/technology-activations/", "Explore activations")
        + '</div></div></section>')


def remove_what_we_make(html: str) -> str:
    """Drop the What We Make carousel.

    It listed the same disciplines the three feature sections below it now
    cover, as a row of cards that scrolled past without linking anywhere. Two
    statements of the same list on one page, one of which was a dead end.

    Removed whole rather than hidden in CSS: a display:none carousel still
    ships its markup, still loads its images and still has its ScrollTrigger
    computed against a zero-height element.
    """
    m = re.search(r'<section[^>]*\bclass="[^"]*service_section', html)
    if not m:
        return html
    depth, end = 0, None
    for t in re.finditer(r"<(/?)section\b[^>]*>", html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    if end is None:
        return html
    return html[:m.start()] + html[end:]


def apply(html: str, drop_hero: bool = True) -> str:
    """Rebuild the service page: no videos, then the three feature sections."""
    html = strip_service_videos(html)
    html = remove_what_we_make(html)   # the three sections below cover it
    # The three sections sit between the capability list and the testimonials,
    # in the client's order: video production, influencer, technology.
    # Matched by regex, not a literal: Webflow emits its variant data-attribute
    # before class on this element, so `<section class="testimonial_section`
    # never appears in the markup.
    m = re.search(r'<section[^>]*\bclass="[^"]*testimonial_section', html)
    if not m:
        raise SystemExit("service: testimonial section not found")
    at = m.start()
    html = (html[:at] + video_section() + influencer_section()
            + technology_section() + html[at:])
    # only now: the testimonial section is the anchor the two feature sections
    # are seated against, so it has to survive until they are in place
    html = remove_testimonials(html)
    # The Influencer Campaigns page is grown from this same output and seats
    # its own body against the reference's hero, so it asks for that one
    # untouched rather than this page's film.
    return film_hero(html) if drop_hero else html


def tech_page(html: str) -> str:
    """The Technology Activations detail page, on the service page's shell."""
    body = (
        '<section class="service_hero_section is-tech">'
        '<div class="padding_global"><div class="container">'
        '<h1 data-title-anim="" class="service_hero_title">Technology Activations</h1>'
        f'<p class="ig_lede">{esc(TECH_LEDE)}</p>'
        '</div></div></section>'
        '<section class="ig_steps_section"><div class="padding_global">'
        '<div class="container">'
        '<div class="section_header">'
        '<h2 data-title-anim="" class="service_section_title">The formats</h2>'
        f'<div data-floating-badge="" class="floating_text">{len(TECH)} FORMATS</div>'
        '</div><ol class="ig_steps">'
        + "".join(
            f'<li class="ig_step"><span class="ig_step_num">{i + 1:02d}</span>'
            f'<h3 class="ig_step_title">{esc(t)}</h3>'
            f'<p class="ig_step_info">{esc(b)}</p></li>'
            for i, (t, b) in enumerate(TECH))
        + '</ol>'
        # Said plainly rather than padded with invented case studies.
        '<p class="svc_pending">Installation photography and per-format case '
        'studies are still to come from the client.</p>'
        '</div></div></section>')

    out, n = re.subn(
        r'<section class="service_hero_section".*?(?=<section class="cta_section")',
        lambda _m: body, html, count=1, flags=re.S)
    if not n:
        raise SystemExit("tech page: could not find the service hero -> cta span")
    return out.replace("<title>", "<title>Technology Activations — ", 1)
