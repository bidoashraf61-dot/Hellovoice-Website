#!/usr/bin/env python3
"""HelloVoice's content, and the transforms that put it into the clone.

Everything here is either captured from hellovoice.co.uk (`capture/content.json`)
or written. Written copy is marked WRITTEN in the comment above it so the
content report can list it — nothing invented should reach a client unflagged.

The clone's markup is regenerated from the reference on every build, so content
cannot live in the HTML. It lives here and is substituted by class name.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = json.loads((ROOT / "content" / "projects.json").read_text(encoding="utf-8"))

# Spelling corrections applied to the captured film titles (client checklist
# rows 1-6, 17 Sep 2026). Client names and common words only, never a change of
# meaning. The table is ordered: longer keys first where one contains another,
# because these are plain replacements.
#
# Applied here, at load, rather than at each render — the titles feed cards,
# section headings, alt text, lightbox captions and the filter tags, and a fix
# applied in one of those places but not the others is how "Molyncke" and
# "Molnlycke" came to sit on the same page. `slug` is a stored field, so
# correcting a title never moves an image or breaks the AI-video matching.
TITLE_FIXES = [
    ("Medical_Skintellectual", "Medical \u2013 Skintellectual"),
    ("Suliman Al Habib patient", "Sulaiman Al Habib \u2013 Patient"),
    ("Qasser El saraya", "Qasser Al-Saraya"),
    ("LA Roche- Posay", "La Roche-Posay"),
    ("Molyncke", "M\u00f6lnlycke"), ("Molynlcke", "M\u00f6lnlycke"),
    ("Molnlycke", "M\u00f6lnlycke"),
    ("Spc-", "SPC \u2013"),
    ("Awarness", "Awareness"), ("Kwait", "Kuwait"), ("kwait", "Kuwait"),
    ("Zoiets", "Zoetis"),
    ("L'Oreal", "L\u2019Or\u00e9al"), ("Neweast", "NewEast"),
    ("CGi", "CGI"), ("Grand opening", "Grand Opening"),
    # Not on the client's list, but the same class of defect: the rule is that
    # a correction applies everywhere the pattern appears, and these would
    # otherwise come back as a second round of the same comment.
    ("Medugate- ", "Medugate \u2014 "), ("FGM- ", "FGM \u2014 "),
    ("Dermactive - ", "Dermactive \u2014 "), ("Orchidia - ", "Orchidia \u2014 "),
    ("Ad - ", "Ad \u2014 "), ("Portal - ", "Portal \u2014 "),
    ("Solo fresh", "Solo Fresh"), ("On Boarding", "Onboarding"),
    ("Cycle meeting", "Cycle Meeting"),
    ("Anamorphic illusion", "Anamorphic Illusion"),
    # "X" between two client names is the house pattern (Abbott X Kuwait,
    # QV X Elnahdi, Sudair X KSMC); one film used a lowercase x.
    ("NewEast x Isuzu", "NewEast X Isuzu"),
]


def clean_title(t: str) -> str:
    # A stray Arabic kasra sits before the A of "Abbott" in the capture. It is
    # invisible in most editors, which is why it survived this long.
    t = t.replace("\u0650", "").strip()
    for a, b in TITLE_FIXES:
        t = t.replace(a, b)
    return t[:1].upper() + t[1:]


for _p in PROJECTS:
    _p["title"] = clean_title(_p["title"])

# ----------------------------------------------------------------- captured

SITE = {
    "name": "HelloVoice",
    "tagline": "Your Innovative Media Solution Partner",
    "proof": "Trusted by Leading Multinational Brands",
    "email": "info@hellovoice.co.uk",
    "phone": "+966 11 463 4518",
    "mobile": "+966 50 744 8866",
    "address": "Al-Olaya 12222, Riyadh, Saudi Arabia",
    "hours": "Sunday – Thursday, 9am to 5pm",
}

# CLIENT FIGURES.
STATS = [("1000+", "Minutes of Content"), ("98%", "Client Retention Rate"),
         ("100+", "Clients"), ("10+", "Industries Covered")]

TESTIMONIALS = [
    ("Hello Voice translated our vision into a cinematic campaign that increased "
     "engagement and drove measurable results on time and above expectations.",
     "Leila Mansour", "Head of Marketing"),
    ("Dependable, creative, and strategic — their team handled a complex launch "
     "with precision and gave us a creative partner we can truly trust.",
     "Omar Haddad", "Regional Brand Manager"),
    ("Hello Voice managed our brand video from concept to final edit, and the "
     "result was outstanding. Cinematic visuals, perfect lighting, and a smooth, "
     "professional experience.",
     "Faisal Al-Qahtani", "Marketing Manager"),
]

# Mariam Samir, Muhammed Saeed and Mahmoud Farag have left; Mirna Edwar,
# Mariam Hani and
# Muhammed Khalid join, and Amr Khashab's title is the client's own wording
# rather than the "Senior" the reference capture had.
# Portraits the client has pulled, pending replacements they are sending.
# The person stays on the roster — only the photograph goes. Leaving them in
# with no handling would be worse than removing them: the card is cloned from
# a template that already carries a face, so a skipped portrait shows somebody
# else's.
#
# Muhammed Khalid's replacement has arrived (Team/khaled_3.jpg) and is off the
# list. It came already matched to the set — same dark navy ground, comparable
# saturation — so it needed resizing to the team's 760x1013 and nothing else.
#
# Mariam Hani is off the list too: the client has asked for her original
# photograph back rather than waiting for a replacement. It was never deleted —
# the processed 760x1013 and its -sm pair have been in assets/team all along —
# so restoring her is removing the name, not reprocessing anything.
#
# The set is now complete. Empty rather than deleted, because the monogram
# handling below is what stops a pulled portrait showing somebody else's face:
# the card is cloned from a template that already carries one.
NO_PORTRAIT = set()

TEAM = [("Abdelrahman Ashraf", "Media Production Manager"),
        ("Omnia Hegazi", "Video Editor"),
        ("Amr Khashab", "Motion Graphic Artist"),
        ("Mirna Edwar", "Project Manager"),
        ("Mariam Hani", "Video Editor"),
        ("Muhammed Khalid", "Video Editor")]

# the portfolio's own six sections — the works filter uses these verbatim
# One ground per work group. The site's own accents at low alpha: enough to
# separate the bands so the eye has somewhere to stop, not enough to compete
# with the film stills standing on them — the stills are the point of the page.
# Cycled by index, so adding a seventh section cannot land without a colour.
# ---------------------------------------------------------------- INDUSTRY
# A second facet across the catalogue, cutting the other way from the format
# categories: what the film was for, rather than what kind of film it is.
#
# Every tag below is derived from titles actually in projects.json and matched
# by keyword, so a filter can never come up empty. That constraint is the point.
# The client asked for pharma genre tags — Mechanism of Action, Medical Trials,
# Patient Testimonials — and none of the fifty films is one: no title, section
# or description in the capture describes an MoA animation or a trial film.
# Adding them would ship three filters that match nothing, which reads as a
# broken page rather than as an empty category. They belong here the day that
# work exists, and the table is written so adding one is a single line.
INDUSTRY_TAGS = [
    ("Pharma & Healthcare", (
        "dermactive", "abbott", "sanofi", "molnlycke", "molyncke", "molynlcke",
        "roche- posay", "roche-posay", "spimaco", "vichy", "filorga", "seroflo", "menarini",
        "medugate", "gilead", "kite", "orchidia", "bionnex", "svr", "qv ",
        "habib", "ksmc", "hospital", "blood bank", "derma", "skintellectual",
        "oncology", "inhaler", "pharmalys", "nahdi", "elnahdi", "medical")),
    ("Automotive", (
        "isuzu", "aisin", "neweast", "automechanika")),
    ("Cycle Meetings & Congress", (
        "cycle meeting", "cycle meetings", "congress", "gallery", "derm 2024",
        "derma 2024")),
    ("Patient & HCP Education", (
        "awareness", "awarness", "patient", "hcp", "on boarding", "whiteboard",
        "fgm", "female genital")),
    ("Events & Openings", (
        "grand opening", "gala", "recap", "closing video", "national day",
        "founding day", "take off")),
]


# The films made with AI, named by the client 17 Sep 2026. They keep their own
# category as well — a film is an awareness film and an AI film at once, which
# is why the bar carries two rows rather than one.
AI_FILMS = {
    "suliman-al-habib-patient-awarness-video",
    "svr-sun-secure-spf50",
    "neweast-isuzu-riyadh-grand-opening-video",
}

# The video-type row, in the order the page's own bands run.
TYPE_TAGS = ["Commercial Ads", "Corporate Videos", "Awareness Videos",
             "CGI & Anamorphic Illusion", "Events & Live Production",
             "Interviews & Testimonials", "AI Videos"]


def industry_tags(project) -> list:
    """Which industry facets a project carries.

    Matched against the title, lowercased. A project can hold several — an
    Isuzu grand-opening recap is both automotive and an event — which is the
    point of a second facet rather than a second category.
    """
    hay = (project.get("title", "") + " " + (project.get("section") or "")).lower()
    return [name for name, keys in INDUSTRY_TAGS if any(k in hay for k in keys)]


# Two grounds, alternating — the theme's own neutrals rather than a new palette:
# white, and the linen the technology and video sections already stand on.
#
# Six accents at low alpha were the previous answer, and each band read as its
# own little world — a page of fifty films felt like six unrelated pages. Two
# grounds do the one job a band colour has here, which is to say where a section
# starts.
GROUP_TONES = ["#FFFFFF", "#E9DCD2"]

SECTIONS = ["Commercial Ads", "Awareness Videos", "Corporate Videos",
            "Events & Live Production", "CGI & Anamorphic Illusion",
            "Interviews & Testimonials"]

# ------------------------------------------------------------------ WRITTEN

# WRITTEN — the eight services the client confirmed. Tags drawn from the
# client-to-service mapping in build/content.py; needs review.
# Each discipline's loop and where its work lives.
#
# The loops are the client's GIFs, converted to H.264 by build/gifs (see
# site/assets/loops) — 1.9GB of source became 7.5MB, so a card can actually
# carry moving work without costing the page its load time. Never reference
# GIFS/ directly: those are the 100MB+ masters.
#
# The portfolio link points at the works page section that holds that
# discipline's films, so a visitor reading about a service is one click from
# seeing it. Two disciplines have no section of their own yet and go to their
# own detail page instead.
SERVICE_MEDIA = {
    "Video Production":              ("commircal-ads",       "/projects/#commercial-ads"),
    "Post Production":               ("recaps1",             "/projects/#corporate-videos"),
    "CGI & 3D Production":           ("cgi",                 "/projects/#cgi-anamorphic-illusion"),
    "AI Video Production":           ("ai",                  "/projects/#commercial-ads"),
    "AVL & Live Production":         ("event-srreming",      "/projects/#events-live-production"),
    "Animation & Motion Production": ("animation",           "/projects/#awarness-videos"),
    # the multi-campaign montage rather than a single how-to: the card is
    # selling range, and one creator in one kitchen does not read as range
    "Influencer Campaigns":          ("influencer-multi",    "/service/influencer-campaigns/"),
    "Technology Activations":        ("inteactive1",         "/service/technology-activations/"),
}

SERVICES = [
    ("Video Production", ["Campaign Films", "Brand Films", "Patient Awareness",
                          "Product Launch", "Documentary", "Direction"]),
    ("Post Production", ["Offline Edit", "Online & Grade", "Sound Design",
                         "Versioning", "Localisation", "Subtitling"]),
    ("CGI & 3D Production", ["Anamorphic DOOH", "Product CGI", "3D Environments",
                             "Medical Visualisation", "Simulation", "Compositing"]),
    ("AI Video Production", ["AI Generation", "Digital Doubles", "Voice Synthesis",
                             "Scale Versioning", "Rapid Concepting", "Upscaling"]),
    ("AVL & Live Production", ["Congress Coverage", "Multi-Camera", "Live Streaming",
                               "Stage & Screens", "Same-Day Edit", "Event Recap"]),
    ("Animation & Motion Production", ["2D Animation", "Motion Graphics",
                                       "Explainer Films", "Mechanism of Action",
                                       "Infographics", "Titles"]),
    ("Influencer Campaigns", ["Creator Casting", "UGC Production", "Briefing",
                              "Delivery Tracking", "Usage Rights", "Reporting"]),
    ("Technology Activations", ["Mixed Reality", "VR Experiences", "Hologram Box",
                                "Interactive Screens", "Smart Cube", "Laser & Projection"]),
]

# WRITTEN — the production pipeline, replacing the reference's design pipeline.
STEPS = [
    ("Step 01", "BRIEF & STRATEGY",
     "We take the objective, the audience and the medical or brand constraints, and agree the story before anything is shot."),
    ("Step 02", "PRE-PRODUCTION",
     "Script, storyboard, casting, locations and permits — with review and compliance built into the schedule, not bolted on."),
    ("Step 03", "PRODUCTION",
     "Crews, studios and live capture across the Gulf, from a single interview to a multi-camera congress floor."),
    ("Step 04", "POST & DELIVERY",
     "Edit, grade, sound, animation and every language version, delivered to each platform's specification."),
]

# WRITTEN — the About statement. Grounded in facts on file (the service list,
# the client roster) but not the client's own words.
#
# Deliberately not "a studio in Riyadh": the client's correction is that
# HelloVoice is not a Riyadh brand. It runs a UK office and works across
# markets, so the statement leads with reach rather than an address.
ABOUT_STATEMENT = ("HELLOVOICE IS A 360 MEDIA PRODUCTION HOUSE MAKING FILM, "
                   "ANIMATION AND IMMERSIVE WORK FOR HEALTHCARE AND GLOBAL BRANDS")

# WRITTEN — hero supporting copy.
HERO_INFO = ("A 360 media production house working with multinational brands — "
             "film, animation, CGI, live production and immersive technology, "
             "handled end to end under one roof.")

# the site's own showreel, 72s — capture/vimeo.json calls it "Website Showreel"
VIMEO_SHOWREEL = "1129859185"

# PLAY / REEL runs the behind-the-scenes cut rather than the showreel: the
# film section directly above it already carries the showreel, and running the
# same 72s twice on one page read as a duplicate. vimeo.com/1129831285, 55s.
VIMEO_BTS = "1129831285"
BTS_TITLE = "Hello Voice Behind the Scene"


# ---------------------------------------------------------------- utilities

def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fill(html, cls, values, limit=None):
    """Replace the inner text of every element carrying `cls`, in order.

    The reference prints many labels twice (the hover swap), so a value is
    consumed only when the text actually changes — repeated identical
    neighbours take the same value.
    """
    vals = list(values)
    state = {"i": 0, "last": None}

    def sub(m):
        head, inner, tail = m.group(1), m.group(2), m.group(3)
        if state["last"] is not None and inner.strip() == state["last"]:
            v = vals[state["i"] - 1] if state["i"] else inner
            return head + esc(v) + tail
        if state["i"] >= len(vals):
            return m.group(0)
        state["last"] = inner.strip()
        v = vals[state["i"]]
        state["i"] += 1
        return head + esc(v) + tail

    pat = re.compile(r'(<(?:p|h1|h2|h3|h4|div|span|a|button)[^>]*class="[^"]*\b'
                     + re.escape(cls) + r'\b[^"]*"[^>]*>)([^<]*)(</)')
    return pat.sub(sub, html, count=limit or 0)


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def work_card(p, offset=False):
    """One card on the works listing.

    The thumbnail keeps the film's own shape — 16:9 or 9:16, taken from the
    poster's real dimensions — rather than being cropped square. Clicking opens
    the film in a player on this page; it does not leave for vimeo.com. The
    href stays as the no-JS and middle-click fallback.
    """
    href = f"https://vimeo.com/{p['vimeo']}" if p["vimeo"] else "#"
    hook = (f' data-vimeo="{p["vimeo"]}" data-ratio="{p["ratio"]}" '
           f' data-vimeo-h="{p.get("vimeo_h","")}" '
            f'data-title="{esc(p["title"])}"' if p["vimeo"] else "")
    # Both facets in one attribute: the format category and every industry the
    # film belongs to. The filter matches on membership, so a card can answer to
    # "Corporate Videos" and to "Automotive" without either filter knowing the
    # other exists. Built here rather than inline because a nested join inside
    # an f-string is not valid on the Python this builds with.
    tagstr = " ".join([slug(p["section"])] + [slug(t) for t in industry_tags(p)]
                      + (["ai-videos"] if p.get("slug") in AI_FILMS else []))
    cls = "is-" + p["ratio"].replace(":", "-")
    img = (f'<img src="/assets/work/{p["img"]}-700.webp" '
           f'srcset="/assets/work/{p["img"]}-700.webp 700w, /assets/work/{p["img"]}-1400.webp 1400w" '
           f'sizes="(max-width: 991px) 100vw, 620px" loading="lazy" '
           f'width="{p["w"]}" height="{p["h"]}" '
           f'alt="{esc(p["title"])}" class="image-cover"/>')
    return (
        f'<div role="listitem" class="project_item w-dyn-item" '
        f'data-tags="{tagstr}" data-ratio="{p["ratio"]}">'
        f'<a aria-label="Watch {esc(p["title"])}" href="{href}"{hook} '
        f'class="project_image w-inline-block {cls}">{img}'
        '<span class="work_play" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor">'
        '<path d="M8 5v14l11-7z"/></svg></span></a>'
        '<div class="project_content_wrapper"><div class="project_content_left">'
        f'<a aria-label="Watch {esc(p["title"])}" href="{href}"{hook} class="link-secondary w-inline-block">'
        f'<h3 class="text-3xl color-inherit">{esc(p["title"])}</h3></a>'
        '<div class="w-dyn-list"><div role="list" class="project_tag_wrapper w-dyn-items">'
        f'<div role="listitem" class="w-dyn-item"><button type="button" class="project_tag" '
        f'data-filter-to="{slug(p["section"])}">{esc(p["section"])}</button></div>'
        '</div></div></div></div></div>')


def extract_element(html, open_pattern):
    """Return one <div> and its whole subtree, matched by depth.

    The companion to replace_element. Capturing a template block with a
    lookahead — `<div class="x">.*?(?=<div class="x"|</div></div>)` — is what
    keeps going wrong: for the LAST match the lookahead lands before that
    element's own closing tag, so the captured span is short one </div> and the
    surplus survives into whatever follows. Counting depth removes the whole
    class of error.
    """
    m = re.search(open_pattern, html)
    if not m:
        return None, None, None
    depth = 0
    for t in re.finditer(r'<(/?)div\b[^>]*>', html[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            return html[m.start():end], m.start(), end
    return None, None, None


def replace_element(html, open_pattern, new_html, count=1):
    """Replace a <div> and its whole subtree, matched by depth rather than regex.

    `<div class="x">.*?</div>` cannot do this: it stops at the first closing tag
    inside the subtree. Here the works listing sits inside a
    .project_collection_list wrapper, and a hand-written tail of "</div></div>
    </div></section>" consumed one closing tag more than it opened — leaving
    .padding_global unclosed for the whole page.
    """
    done = 0
    while done < count:
        m = re.search(open_pattern, html)
        if not m:
            break
        depth, end = 0, None
        for t in re.finditer(r'<(/?)div\b[^>]*>', html[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        if end is None:
            break
        html = html[:m.start()] + new_html + html[end:]
        done += 1
    return html


def works_page(html):
    """The whole portfolio, grouped into its own six sections.

    The reference lists cards in one flat grid. hellovoice.co.uk's portfolio is
    organised by type — "Commercial Ads", "Corporate Videos" and so on are
    headings on the live site, captured in capture/content.json — so the
    listing is grouped the same way and each group gets its heading.

    The tag filter still works across the whole page: filtering hides the cards
    that do not match *and* any section left with nothing in it, so a filtered
    view never shows an empty heading.
    """
    groups = []
    for name in SECTIONS:
        items = [p for p in PROJECTS if p.get("section") == name]
        if not items:
            continue
        cards = "".join(work_card(p) for p in items)
        # Each group takes its own ground. The client's note is that the page
        # read as one undifferentiated column; a band per discipline gives the
        # eye somewhere to stop and makes the headings do their job.
        #
        # The colours are the site's own accents at low alpha rather than new
        # hues — saturated grounds behind a grid of film stills would fight the
        # stills, which are the point of the page. Cycled by index so adding a
        # seventh section cannot land without one.
        tone = GROUP_TONES[len(groups) % len(GROUP_TONES)]
        groups.append(
            f'<section class="work_group" data-group="{slug(name)}" '
            f'style="background-color:{tone}">'
            f'<div class="work_group_head">'
            f'<h2 data-title-anim="" class="work_group_title">{esc(name)}</h2>'
            '</div>'
            f'<div role="list" class="project_listing w-dyn-items">{cards}</div>'
            f'</section>')

    # anything whose section is not one of the six still has to appear
    known = {p for name in SECTIONS for p in
             [q.get("slug") for q in PROJECTS if q.get("section") == name]}
    rest = [p for p in PROJECTS if p.get("slug") not in known]
    if rest:
        groups.append(
            '<section class="work_group" data-group="other">'
            '<div class="work_group_head">'
            '<h2 data-title-anim="" class="work_group_title">More work</h2>'
            '</div>'
            '<div role="list" class="project_listing w-dyn-items">'
            + "".join(work_card(p) for p in rest) + '</div></section>')

    # replace the whole collection wrapper, not just the inner list — matching
    # by depth so the surrounding .project_listing_content / .container /
    # .padding_global closers are left exactly as the template has them
    html = replace_element(
        html, r'<div class="project_collection_list[^"]*"[^>]*>', "".join(groups))

    # Two rows, each labelled, rather than one long run of chips.
    #
    # Eleven filters in a single row is a wall the eye has to read end to end
    # before it can choose. Split by facet — what kind of film, then who it was
    # for — each row is short enough to scan and the labels say what the choice
    # means. Both rows wrap rather than clipping or scrolling: a hidden chip is
    # a filter nobody knows exists.
    #
    # Exclusive sits with the format categories rather than apart from them:
    # the client's pick is a way of looking at the work the same as a category
    # is, and a bar that omits one of the page's own sections leaves a band
    # nothing can isolate.
    def chip(label, value, active=False):
        return (f'<button type="button" class="works_filter_button'
                f'{" is-active" if active else ""}" data-filter="{value}" '
                f'aria-pressed="{"true" if active else "false"}">{esc(label)}</button>')

    # One row, Sector, multi-select.
    #
    # The type row is gone from the bar. It was the weaker cut — by sector the
    # thinnest slice is eight films and the largest twenty-nine, where two type
    # slices are under six — and the coloured bands below already group the work
    # by type, so scrolling does that job without thirteen controls standing
    # between the visitor and the films.
    #
    # Multi-select because a visitor's real question is often two sectors wide:
    # an agency that does pharma and automotive wants to see both, and picking
    # one used to wipe the other.
    def chip(label, value, active=False):
        return (f'<button type="button" class="works_filter_button'
                f'{" is-active" if active else ""}" data-filter="{value}" '
                f'aria-pressed="{"true" if active else "false"}">'
                f'<span class="works_filter_label">{esc(label)}</span></button>')

    row_sector = "".join(chip(name, slug(name)) for name, _keys in INDUSTRY_TAGS)
    # A second row, by what kind of film it is — the client's ask, 17 Sep 2026.
    # The two rows narrow together: a sector and a type give the films that are
    # both, while two chips in the same row give either.
    row_type = "".join(chip(name, slug(name)) for name in TYPE_TAGS)

    buttons = (
        '<div class="works_filter_head">'
        '<span class="works_filter_kicker">Filter</span>'
        '<h3 class="works_filter_lead">What are you looking for?</h3>'
        '</div>'
        '<p class="works_filter_row_label" id="filter-type-label">Video type</p>'
        '<div class="works_filter_chips" data-facet="type" role="group" '
        'aria-labelledby="filter-type-label">'
        f'{chip("All types", "all-type", True)}{row_type}</div>'
        '<p class="works_filter_row_label" id="filter-sector-label">Sector</p>'
        '<div class="works_filter_chips" data-facet="sector" role="group" '
        'aria-labelledby="filter-sector-label">'
        f'{chip("All work", "all", True)}{row_sector}</div>'
        '<div class="works_result_bar" data-result-bar hidden>'
        '<p class="works_result_count" role="status" aria-live="polite"></p>'
        '<div class="works_result_chips" data-active-chips></div>'
        '<button type="button" class="works_clear" data-clear-filters>Clear all</button>'
        '</div>')

    html = re.sub(r'<div class="works_filter" role="group"[^>]*>.*?</div>',
                  '<div class="works_filter" role="group" aria-label="Filter work by type">'
                  + buttons + '</div>', html, flags=re.S, count=1)
    return html


# ---------------------------------------------------------------- EXCLUSIVE
# The films that open the portfolio, above the grouped listing.
#
# CLIENT PICK PENDING. These four are a placeholder chosen so the section can
# be built, reviewed and signed off before the real selection arrives — they
# are simply the four already featured on the home page. Replace the ids with
# whichever films the client wants and the section follows; nothing else needs
# touching.
#
# An id here that has no entry in content/projects.json fails the build rather
# than silently shrinking the row.
EXCLUSIVE = ["1096246650", "1096217860", "1087486372", "1087490128"]

# The four films on the home page, chosen by the client rather than taken as
# whichever four happen to sort first.
FEATURED = ["1096246650", "1096217860", "1087486372", "1087490128"]


def featured_work(html):
    """The home page's four stacked cards — the client's own selection."""
    by_id = {p["vimeo"]: p for p in PROJECTS if p.get("vimeo")}
    picks = [by_id[v] for v in FEATURED if v in by_id]
    if len(picks) != len(FEATURED):
        missing = [v for v in FEATURED if v not in by_id]
        raise SystemExit(f"featured_work: no PROJECTS entry for {missing}")
    titles = [p["title"] for p in picks]
    html = fill(html, "work_title", titles)
    html = fill(html, "work_description_text",
                [f"{p['section']} — watch the film on Vimeo." for p in picks])
    # each card carries its still plus a play control, and opens the film in
    # the page player — the card is not a static picture
    for p in picks:
        # The still takes the FILM's orientation, not a blanket 16:9. A vertical
        # film cropped into a landscape box shows a slice of its middle and
        # reads as the wrong thumbnail — which is exactly what happened to the
        # Dermactive card. The ratio class is the same one the works listing
        # uses, so both pages describe shape the same way.
        ratio_cls = "is-" + p["ratio"].replace(":", "-")
        html = re.sub(
            r'<div class="work_image_visual(?: is-\d+-\d+)?">\s*<img[^>]*>',
            lambda m, p=p, rc=ratio_cls: f'<div class="work_image_visual {rc}">' 
            + f'<a class="work_visual_link" href="https://vimeo.com/{p["vimeo"]}" '
              f'data-vimeo="{p["vimeo"]}" data-ratio="{p["ratio"]}" '
           f' data-vimeo-h="{p.get("vimeo_h","")}" '
              f'data-title="{esc(p["title"])}" aria-label="Watch {esc(p["title"])}">'
              f'<img src="/assets/work/{p["img"]}-1400.webp" loading="lazy" '
              f'alt="{esc(p["title"])}" class="image-cover"/>'
              '<span class="work_play" aria-hidden="true">'
              '<svg viewBox="0 0 24 24" width="30" height="30" fill="currentColor">'
              '<path d="M8 5v14l11-7z"/></svg></span></a>',
            html, count=1)
    for p in picks:
        html = re.sub(
            r'href="/projects/[a-z0-9-]+/"',
            f'href="https://vimeo.com/{p["vimeo"]}" data-vimeo="{p["vimeo"]}" '
            f'data-ratio="{p["ratio"]}" data-title="{esc(p["title"])}"',
            html, count=2)
    return html


def home(html):
    html = fill(html, "hero_sub_title", [SITE["tagline"]])
    html = fill(html, "hero_info", [HERO_INFO])
    html = fill(html, "hero_stat_title", [STATS[0][0]])
    html = fill(html, "hero_stat_info", [STATS[0][1]])
    html = fill(html, "about_section_title", [ABOUT_STATEMENT])
    html = fill(html, "step_count", [s[0] for s in STEPS])
    html = fill(html, "step_title", [s[1] for s in STEPS])
    html = fill(html, "step_info", [s[2] for s in STEPS])
    html = fill(html, "step_section_title", ["BRIEF, BUILD, AND DELIVER"])
    html = fill(html, "step_section_info",
                ["We are with you from the first brief to the final language version."])
    html = featured_work(html)
    html = services(html)
    html = testimonials(html)
    return html


def services(html):
    """All eight disciplines, generated rather than filled.

    Two problems made fill() the wrong tool here. The reference ships only four
    service_item blocks, so half the list was silently dropped while the badge
    above still claimed eight. And fill() deliberately reuses a value when it
    meets the same text twice in a row — that is what makes the template's
    hover-swap labels work — so cloning the block four more times gave four
    copies carrying the *same* title.

    Building the run directly sidesteps both: one block is taken as the
    template, and one is emitted per service with its own title and tags.
    """
    m = re.search(r'<div class="service_item">.*?(?=<div class="service_item">)',
                  html, re.S)
    if not m:
        return html
    tpl = m.group(0)

    # Drop the reference's own background video from the template.
    #
    # Every card now carries the discipline's loop in .service_item_media, so
    # the reference's player was a second, competing video on the same card —
    # a small box on the left with its own pause control, next to our loop on
    # the right. It was already stripped on /service/ by service_page, but the
    # home page builds its cards through this same function and never saw that
    # pass, so home shipped both. Removing it from the template fixes every
    # page that clones it, which is the only place it can be fixed once.
    #
    # Depth-counted: the wrap holds nested divs and a `.*?</div>` cut leaves
    # the surplus closers behind — the mistake that has bitten this file three
    # times already.
    tpl_found = tpl          # the untouched text, for locating the run below
    tpl = replace_element(tpl, r'<div class="service_item_video_wrap">', "")

    def block(name, tags, idx=0):
        b = tpl
        # Stack order, written per card rather than selected by position.
        #
        # These were assigned with `.service_item:nth-child(N)` for N in 1..8.
        # The container's first child is the .section_header, so the cards are
        # actually children 2..9 — every card took the z-index of the one
        # before it, and the eighth matched no rule at all and fell back to the
        # base z-index:1. Technology Activations therefore painted *underneath*
        # Influencer Campaigns instead of sliding over it.
        #
        # The builder knows each card's real index, so it writes the value
        # directly. No selector to drift when the markup around it changes.
        b = b.replace('<div class="service_item">',
                      f'<div class="service_item" style="z-index:{idx + 1}">', 1)
        b = b.replace('<div class="service_item _',
                      f'<div style="z-index:{idx + 1}" class="service_item _', 1)
        # every copy of the title (the template prints it twice for the swap)
        b = re.sub(r'(<h3[^>]*class="[^"]*service_item_title[^"]*"[^>]*>)[^<]*(</h3>)',
                   lambda mm: mm.group(1) + esc(name) + mm.group(2), b)
        # the six tags, in order
        it = iter(tags)
        def tag(mm):
            try:
                return mm.group(1) + esc(next(it)) + mm.group(2)
            except StopIteration:
                return mm.group(0)
        b = re.sub(r'(<p[^>]*class="[^"]*service_item_tag_text[^"]*"[^>]*>)[^<]*(</p>)',
                   tag, b)

        loop, href = SERVICE_MEDIA.get(name, (None, None))

        # The loop fills the card's media slot. It is decoration, so it is
        # muted, inert to the pointer and lazy — and it carries its poster, so
        # a card that has not reached the viewport still shows a frame rather
        # than a hole.
        if loop and (ROOT / "site" / "assets" / "loops" / f"{loop}.mp4").exists():
            b = b.replace('<div class="service_item_content">',
                '<div class="service_item_media">'
                f'<video class="service_loop" autoplay muted loop playsinline '
                f'preload="none" poster="/assets/loops/{loop}.webp" aria-hidden="true">'
                f'<source src="/assets/loops/{loop}.mp4" type="video/mp4"/>'
                '</video></div>'
                '<div class="service_item_content">', 1)

        # and a way through to the work itself, on its own line under the tags
        if href:
            # The label is printed twice inside a clipping wrapper, which is
            # exactly how every other button on the site is built - "Learn
            # More" and the CTA both do it. Hovering rolls the pair up by one
            # line so the second copy takes the first's place. Written into the
            # markup here rather than injected by script so the button reads
            # correctly with no JS and the roll is a pure enhancement.
            # The second copy is aria-hidden, or the label is announced twice.
            link = (f'<a class="service_item_link" href="{href}">'
                    '<span class="button_text_wrapper service_item_link_label">'
                    '<span class="button_text">See the work</span>'
                    '<span class="button_text second_text" aria-hidden="true">'
                    'See the work</span></span>'
                    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" '
                    'stroke="currentColor" stroke-width="2" aria-hidden="true">'
                    '<path d="M5 12h14M13 6l6 6-6 6"/></svg></a>')

            # Placed after the tag wrapper closes, by counting depth rather than
            # matching `</div></div></div>`. That literal matched the *tag's*
            # closing div first, which dropped the link inside the wrapper — so
            # it flowed as one more tag and sat on the same row as the last one
            # whenever that row had space left. Which row it landed on then
            # depended on how the tags happened to wrap.
            m = re.search(r'<div class="service_item_tags_wrapper">', b)
            if m:
                depth, at = 0, None
                for t in re.finditer(r"<(/?)div\b[^>]*>", b[m.start():]):
                    depth += -1 if t.group(1) else 1
                    if depth == 0:
                        at = m.start() + t.end()
                        break
                if at is not None:
                    b = b[:at] + link + b[at:]
        return b

    # The home page shows the three services the Services page leads with —
    # the client's call, 17 Sep 2026. The full list still drives the ticker and
    # the Services page's own sections.
    home_names = {"Video Production", "Influencer Campaigns", "Technology Activations"}
    shown = [sv for sv in SERVICES if sv[0] in home_names]
    run = "".join(block(name, tags, i)
                  for i, (name, tags) in enumerate(shown))

    # replace every existing block in one go
    first = html.index(tpl_found)
    last_m = None
    for last_m in re.finditer(r'<div class="service_item">.*?(?=<div class="service_item">|</div></div></section>)',
                              html, re.S):
        pass
    end_at = last_m.end() if last_m else first + len(tpl)
    html = html[:first] + run + html[end_at:]

    html = fill(html, "service_section_title", ["What we make"])
    return html


def testimonials(html):
    """Three real quotes. The pile is built for four, so the fourth card is
    removed rather than filled with a person who did not say anything."""
    html = fill(html, "testimonial_text", [t[0] for t in TESTIMONIALS])
    html = fill(html, "testimonial_author_name", [t[1] for t in TESTIMONIALS])
    html = fill(html, "testimonial_author_profession", [t[2] for t in TESTIMONIALS])
    html = re.sub(r'<div[^>]*class="testimonial_card card_four"[^>]*>.*?(?=<div class="testimonial_card|</div></div></div></section>)',
                  "", html, flags=re.S, count=1)
    return html


def team_slots(html):
    """Build one card per person, rather than filling a fixed set of slots.

    Two problems made fill() the wrong tool here, and they are the same two
    that made it wrong for the services list.

    The reference ships four cards, so a roster longer than four silently lost
    everyone past the fourth — the names were in TEAM, the cards were not in
    the page. And fill() deliberately reuses a value when it meets the same
    text twice in a row, which is what makes the template's hover-swap labels
    work; cloning a card to make more slots gives every clone the *same*
    placeholder text, so all of them came back with the fourth person's name.

    Generating each card from the template sidesteps both. The numbered
    modifier the reference uses for its stagger is continued, so a fifth card
    is `._5` and picks up whatever offset the stylesheet has for it.
    """
    tpl, _s, _e = extract_element(html, r'<div class="team_card(?: _\d+)?">')
    if not tpl:
        return html

    def slug_of(name):
        return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")

    def card(i, person, role):
        c = re.sub(r'<div class="team_card(?: _\d+)?">',
                   '<div class="team_card">' if i == 0 else f'<div class="team_card _{i+1}">',
                   tpl, count=1)
        c = re.sub(r'(<h3[^>]*class="[^"]*text-xxl[^"]*"[^>]*>)[^<]*(</h3>)',
                   lambda m: m.group(1) + esc(person) + m.group(2), c)
        c = re.sub(r'(<p[^>]*class="[^"]*text-md[^"]*"[^>]*>)[^<]*(</p>)',
                   lambda m: m.group(1) + esc(role) + m.group(2), c)

        # The portrait is written here, not left to the generic still swap.
        # That swap runs earlier in the pipeline, so by the time this clones a
        # card the template already carries the *first* person's face — and
        # every clone inherited it. Setting it per person removes the ordering
        # dependency entirely: the card cannot show anyone but its own subject.
        slug = slug_of(person)
        if person in NO_PORTRAIT:
            # A monogram, not a stock silhouette. It reads as deliberate rather
            # than as a broken image, and it cannot be mistaken for a likeness
            # of someone who has not agreed to one.
            initials = "".join(w[0] for w in person.split()[:2]).upper()
            c = re.sub(
                r'<img[^>]*class="image-cover"[^>]*>',
                f'<div class="team_monogram image-cover" role="img" '
                f'aria-label="{esc(person)}"><span aria-hidden="true">'
                f'{esc(initials)}</span></div>',
                c, count=1)
        elif (ROOT / "site" / "assets" / "team" / f"{slug}.webp").exists():
            c = re.sub(
                r'<img[^>]*class="image-cover"[^>]*>',
                f'<img src="/assets/team/{slug}-sm.webp" '
                f'srcset="/assets/team/{slug}-sm.webp 380w, '
                f'/assets/team/{slug}.webp 760w" '
                f'sizes="(max-width: 767px) 80vw, 260px" '
                f'alt="{esc(person)}" loading="lazy" decoding="async" '
                f'class="image-cover"/>',
                c, count=1)
        return c

    # One row, one staircase, however many people there are.
    #
    # A two-group version was tried, each group sharing the pinned frame and
    # cross-fading. The client's call is that nothing fades — cards only slide
    # up — and without opacity two groups in one frame simply overlap. So the
    # whole roster goes in a single row and the step is sized to fit the frame
    # rather than the roster being split to fit the step.
    run = "".join(card(i, n, r) for i, (n, r) in enumerate(TEAM))
    # Replace the whole .team_cards container rather than a span between the
    # first and last card. The span version left the final card's own </div>
    # behind, which closed <section class="team_section"> early and put every
    # later element outside it.
    return replace_element(html, r'<div class="team_cards">',
                           '<div class="team_cards">' + run + '</div>')


def about(html):
    html = team_slots(html)          # grow the carousel before anything fills it
    html = fill(html, "about_hero_title", [ABOUT_STATEMENT])
    html = fill(html, "about_stats_item_text", [s[1] for s in STATS])
    html = about_stat_numbers(html)   # the figures, not just the labels
    return html


def footer(html):
    html = fill(html, "footer_address_text", [SITE["address"]])
    html = html.replace("hello@hellovoice.com", SITE["email"])
    html = re.sub(r'mailto:[^"?]*', "mailto:" + SITE["email"], html)
    html = re.sub(r'>\s*hello@[^<]*<', f'>{SITE["email"]}<', html)
    html = re.sub(r'tel:\+?[0-9]+', "tel:+966114634518", html)
    html = re.sub(r'>\s*\+91[^<]*<', f'>{SITE["phone"]}<', html)
    return html


def hero_lockup(html):
    """Split the wordmark so VOICE can carry the accent skew, the way the logo
    itself splits Hello from Voice."""
    return html.replace(
        '<h1 data-hero-title="">HELLOVOICE</h1>',
        '<h1 data-hero-title="">HELLO<span class="hv-accent">VOICE</span></h1>')


def apply(html, page):
    html = footer(html)
    html = media(html, page)
    html = loose_ends(html)
    html = floating_labels(html)
    html = brands_wall(html)
    if page == "home":
        html = home(html)
        html = hero_lockup(html)
        html = milestones(html)   # the year track's copy, not the reference's
    elif page == "about-us":
        html = about(html)
        html = life_strip(html)
    elif page == "service":
        html = services(html)
        html = testimonials(html)
    elif page == "projects":
        html = works_page(html)
        html = works_ticker(html)
    elif page == "contact-us":
        html = contact_page(html)
    return html


# ------------------------------------------------------------------- media

WORK = [p for p in PROJECTS if p["img"]]


def media(html, page):
    """Point every remaining reference image and video at HelloVoice's own.

    The service rows, the showreel and the full-bleed film all take footage cut
    from HelloVoice's reel (build note: `site/assets/video/loop-*.mp4`, eight
    four-second segments). Stills come from the 84 work frames on file.
    """
    # --- the looping service rows
    seq = iter(range(1, 9))

    def swap_video(m):
        block = m.group(0)
        # Leave alone anything already pointing at a real HelloVoice file.
        # This pass exists to fill the reference's placeholder <video> tags, and
        # it used to rewrite every video on the page — including the ones the
        # site's own builders had just installed. The full-bleed film and the
        # PLAY / REEL cut were both silently swapped back to four-second reel
        # segments after being set to the real 1080p encodes.
        if re.search(r'src="/assets/(?:video|loops)/(?!loop-)', block):
            return block
        try:
            n = next(seq)
        except StopIteration:
            return block
        block = re.sub(r'<source[^>]*>', "", block)
        block = re.sub(r'(<video\b[^>]*?)\sposter="[^"]*"', r"\1", block)
        block = block.replace("<video", f'<video poster="/assets/video/loop-{n}.jpg"', 1)
        block = block.replace("</video>",
                              f'<source src="/assets/video/loop-{n}.mp4" type="video/mp4"/></video>')
        block = re.sub(r'background-image:url\([^)]*\)',
                       f'background-image:url("/assets/video/loop-{n}.jpg")', block)
        return block

    html = re.sub(r'<video\b.*?</video>', swap_video, html, flags=re.S)

    # --- the showreel and the full-bleed film take the reel itself
    html = re.sub(r'/assets/ref/68f529d8f44ff8a8473854d5[^"\']*\.(?:mp4|webm)',
                  "/assets/video/reel.mp4", html)
    html = re.sub(r'/assets/ref/68f529d8f44ff8a8473854d5[^"\']*\.jpg',
                  "/assets/video/reel-poster.jpg", html)
    html = re.sub(r'/assets/ref/691ddb73f3a125d59699dbf5[^"\']*\.(?:mp4|webm)',
                  "/assets/video/reel.mp4", html)
    html = re.sub(r'/assets/ref/691ddb73f3a125d59699dbf5[^"\']*\.jpg',
                  "/assets/video/reel-poster.jpg", html)

    # --- stills: year cards, project cards, life images, about visuals
    still = iter(WORK)

    def swap_img(m):
        src = m.group(0)
        try:
            p = next(still)
        except StopIteration:
            return src
        out = re.sub(r'src="/assets/ref/[^"]*"', f'src="/assets/work/{p["img"]}-1400.webp"', src)
        out = re.sub(r'\ssrcset="[^"]*"', "", out)
        out = re.sub(r'\ssizes="[^"]*"', "", out)
        out = re.sub(r'alt="[^"]*"', f'alt="{esc(p["title"])}"', out)
        return out

    html = re.sub(
        r'<img[^>]*/assets/ref/(?:68f3377a|6910d8|6910da|6910db|695a0|6958ad|6948117|694812b|69180fa)[^>]*>',
        swap_img, html)

    # --- team portraits
    # The real staff portraits, keyed to the person rather than to a slot.
    #
    # These were numbered files (fy25-team-1..6) handed out in DOM order, which
    # only worked as long as nobody was added, removed or reordered — and the
    # names come from the same TEAM list, so a single edit there would have put
    # the wrong face on every card silently. Deriving the filename from the
    # name means the pairing cannot drift: if a portrait is missing the card
    # keeps the reference image rather than borrowing a colleague's face.
    def person_slug(name):
        return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")

    tseq = iter([(person_slug(n), n) for n, _role in TEAM])

    def swap_team(m):
        try:
            slug, person = next(tseq)
        except StopIteration:
            return m.group(0)
        p = ROOT / "site" / "assets" / "team" / f"{slug}.webp"
        if not p.exists():
            return m.group(0)
        out = re.sub(r'src="[^"]*"', f'src="/assets/team/{slug}.webp"', m.group(0))
        out = re.sub(r'\ssrcset="[^"]*"',
                     f' srcset="/assets/team/{slug}-sm.webp 380w, '
                     f'/assets/team/{slug}.webp 760w"', out)
        out = re.sub(r'alt="[^"]*"', f'alt="{esc(person)}"', out)
        return out

    html = re.sub(r'<img[^>]*/assets/ref/(?:6918bdae|69464c2)[^>]*>', swap_team, html)

    # --- testimonial avatars
    # The block used to be deleted outright because there were no headshots on
    # file. The client has since pointed at the portraits on hellovoice.co.uk,
    # so each card carries its author's face, keyed by name rather than by
    # position — the quotes are filled by fill() in list order and a card that
    # lost its photo should show none rather than a colleague's.
    def author_slug(name):
        return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")

    faces = iter([author_slug(n) for _q, n, _r in TESTIMONIALS])

    def avatar(m):
        try:
            slug = next(faces)
        except StopIteration:
            return ""
        if not (ROOT / "site" / "assets" / "testimonials" / f"{slug}.webp").exists():
            return ""
        return ('<div class="testimonial_author_image">'
                f'<img src="/assets/testimonials/{slug}-sm.webp" '
                f'srcset="/assets/testimonials/{slug}-sm.webp 160w, '
                f'/assets/testimonials/{slug}.webp 320w" sizes="64px" '
                f'alt="" loading="lazy" decoding="async" '
                f'width="160" height="160"/></div>')

    html = re.sub(r'<div class="testimonial_author_image">.*?</div>',
                  avatar, html, flags=re.S)
    return html


PLAY_SVG = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" '
            'aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>')
PAUSE_SVG = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" '
             'aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>')
STARS_SVG = ('<svg viewBox="0 0 120 20" width="120" height="20" fill="#ff691e" '
             'aria-hidden="true">' + "".join(
    f'<path transform="translate({i*24},0)" d="M10 0l2.9 6.2 6.6.9-4.8 4.7 1.2 6.7L10 15.3'
    f' 4.1 18.5l1.2-6.7L.5 7.1l6.6-.9z"/>' for i in range(5)) + '</svg>')


def loose_ends(html):
    """The last reference assets: its play glyphs, its poster frames left in
    background-image and noscript, and the about page's rating block."""
    # poster frames still sitting in inline styles and noscript fallbacks
    html = re.sub(r'/assets/ref/690ee[a-z0-9]*_service-video-\d-poster-00001\.jpg',
                  "/assets/video/loop-1.jpg", html)
    html = re.sub(r'<noscript>\s*<img[^>]*/assets/ref/[^>]*>\s*</noscript>', "", html)

    # its play / pause glyphs become inline marks
    html = re.sub(r'<img[^>]*690ed6eb94e729b06fd5b156_play-icon\.svg[^>]*>', PLAY_SVG, html)
    html = re.sub(r'<img[^>]*69102b3e0b0940fe98f3251f_video-play-button\.svg[^>]*>', PAUSE_SVG, html)

    # the about page's "4.9 from clients" strip
    html = re.sub(r'<img[^>]*6915f47de77cf49ae58c208b_users-avatar\.avif[^>]*>',
                  '<img src="/assets/helv/team-avatars.webp" alt="The HelloVoice team" '
                  'width="292" height="120" class="image-contain"/>', html)
    html = re.sub(r'<img[^>]*star-icon-group[^>]*>', STARS_SVG, html)

    # Webflow's background-video wrappers carry the source list twice, once in
    # the <video> and once in data- attributes its runtime read. The runtime is
    # gone, so the attributes are inert — and they were the last thing still
    # pointing at the reference's CDN files.
    html = re.sub(r'\sdata-video-urls="[^"]*"', "", html)
    html = re.sub(r'\sdata-poster-url="[^"]*"', "", html)

    # two decorative plates beside the section headers
    if WORK:
        html = re.sub(r'<img[^>]*(?:about-section-pattern|design-shape)[^>]*>',
                      f'<img src="/assets/work/{WORK[6]["img"]}-1400.webp" loading="lazy" '
                      f'alt="{esc(WORK[6]["title"])}" class="image-cover"/>', html)
    return html


# WRITTEN — the rotated annotation labels. Each replaces an Ariyana one.

# WRITTEN — the milestone track's copy. Needs client sign-off, and the YEARS
# need confirming before this ships: they are the reference's own 2020-2025 and
# nobody has told me HelloVoice's real dates.
#
# The badges were swapped to HelloVoice milestones some time ago; the paragraphs
# under them were not, so the track shipped a web agency's boilerplate — "a
# strong and reliable team of designers, developers and digital specialists",
# "performance-driven channels", "future-ready digital solutions" — directly
# beneath badges reading PHARMA ACCOUNTS and CGI & ANIMATION. Each paragraph
# now says what its own badge says, in the studio's terms.
# HelloVoice's own six values, lifted verbatim from hellovoice.co.uk/about —
# the titles and the sentences under them are the client's own words, so
# nothing here needs sign-off. Six values and six slots in the track is a
# straight fit.
#
# This replaces a set of invented company milestones. The track's year slot was
# showing 2020-2025 with dates nobody had confirmed; values carry no dates at
# all, so the problem goes away rather than being papered over.
MILESTONES = [
    ("INNOVATION",
     "We embrace creativity and technology to craft fresh, forward-thinking "
     "media solutions."),
    ("QUALITY",
     "We strive for excellence in every frame, ensuring our work meets the "
     "highest standards."),
    ("PEOPLE",
     "We value our team and clients, believing that great work starts with "
     "genuine collaboration."),
    ("ETHICS",
     "We act with honesty, integrity, and respect in everything we do."),
    ("SERVICE",
     "We go beyond expectations to deliver a seamless, client-focused "
     "experience every time."),
    ("TEAM SPIRIT",
     "We succeed together, combining diverse talents to bring every vision "
     "to life."),
]


def _counter(value: str) -> str:
    """Build one odometer from a value like "1000+" or "98%".

    The reference's markup is a row of digit reels: each .stats_column holds
    ten .stats_counter_number divs, and the one shown through the clipping
    window is the first — the rest are what the column rolls past on the way.
    A final .stats_column.is-suffix carries the +, % or M+.

    Only the labels beside these were ever replaced, so the site was showing
    the reference's own figures — 20+, 90M+, 100+, 4.9 — under HelloVoice's
    headings. The number of columns is decided by the value, because the
    reference's counts are wired to its numbers: 1000+ needs four reels where
    20+ needs two.
    """
    digits = "".join(ch for ch in value if ch.isdigit())
    suffix = value[len(digits):] if value[:len(digits)] == digits else \
             "".join(ch for ch in value if not ch.isdigit())

    # Which end of the reel is showing depends on the alignment class, and the
    # two are opposite: is-align-top rests on its first child, is-align-bottom
    # on its last. The reference's own markup says so — its second column runs
    # 0,1..8,0 and displays the trailing 0, while its first runs 2,1..9 and
    # displays the leading 2.
    #
    # Putting the target first in every column, which is the obvious reading,
    # left the bottom-aligned reels resting on a 9: 1000+ came out as 1999.
    cols = []
    for n, d in enumerate(digits):
        roll = "".join(f'<div class="stats_counter_number">{i}</div>'
                       for i in range(10))
        if n == 0:
            cols.append('<div class="stats_column is-align-top">'
                        f'<div class="stats_counter_number">{d}</div>{roll}</div>')
        else:
            cols.append('<div class="stats_column is-align-bottom">'
                        f'{roll}<div class="stats_counter_number">{d}</div></div>')
    if suffix:
        cols.append('<div class="stats_column is-suffix">'
                    f'<div class="stats_counter_number_suffix">{esc(suffix)}</div>'
                    '</div>')
    return "".join(cols)


def about_stat_numbers(html: str) -> str:
    """Put HelloVoice's figures into the About counters.

    Replaces the contents of each .stats_counter_visible_height in order, so
    the numbers stay attached to the labels the fill above them already set.
    Fails loudly if the count of counters and the count of stats disagree —
    silently filling three of four is how a figure ends up under the wrong
    heading.
    """
    # Matched by depth, not by a non-greedy run to the next </div>. The
    # counter holds nested divs, so a lazy match closes on the first inner one
    # and leaves the remaining original columns standing — which showed up as
    # 10000+ where 1000+ was meant, the new reels prepended to a survivor.
    opens = [m for m in re.finditer(
        r'<div[^>]*class="stats_counter_visible_height"[^>]*>', html)]
    blocks = []
    for m in opens:
        depth, end = 0, None
        for t in re.finditer(r"<(/?)div\b[^>]*>", html[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        if end:
            blocks.append((m.start(), m.end(), end))
    if not blocks:
        return html
    if len(blocks) != len(STATS):
        raise SystemExit(
            f"about stats: {len(blocks)} counters but {len(STATS)} figures")

    out, last = [], 0
    for (start, open_end, end), (value, _label) in zip(blocks, STATS):
        out.append(html[last:start])
        out.append(html[start:open_end] + _counter(value) + "</div>")
        last = end
    out.append(html[last:])
    return "".join(out)


def milestones(html):
    """Give the year track copy that matches the badge above it."""
    return fill(html, "year_info_text", [c for _b, c in MILESTONES])


FLOATING = {
    "Design First Digital Agency": SITE["tagline"],
    "DIGITAL SCREENS": "FILM & IMMERSIVE",
    "5 STAR SERVICES": "EIGHT SERVICES",
    "5 Star Services": "In their words",
    "20 team Member": "20+ team members",
    # the value track's badges, taken from MILESTONES so the label above each
    # entry and the sentence inside it cannot drift apart
    "uk office": MILESTONES[0][0],
    "NEW TEAM": MILESTONES[1][0],
    "GLOBAL CLIENTS": MILESTONES[2][0],
    "ONLINE GROWTH": MILESTONES[3][0],
    "CREATIVE HUB": MILESTONES[4][0],
    "NEW VISION": MILESTONES[5][0],
}


def floating_labels(html):
    """Swap the rotated annotation labels beside each section title."""
    def sub(m):
        head, inner, tail = m.group(1), m.group(2), m.group(3)
        key = " ".join(inner.split())
        return head + esc(FLOATING.get(key, inner)) + tail

    return re.sub(r'(<div[^>]*class="floating_text[^"]*"[^>]*>)([^<]*)(</div>)',
                  sub, html)


# WRITTEN — the black brands wall's ticker and its pull-quote.
# The company is not a Riyadh brand — Riyadh is the head office, and that is
# said once, in the footer address. The ticker carries the positioning only.
BRANDS_TICKER = ["Trusted by leading multinational brands",
                 "360 media production", "Trusted by leading multinational brands",
                 "360 media production"]

# the wall quote is one of the three real testimonials
BRANDS_QUOTE = (TESTIMONIALS[2][0], TESTIMONIALS[2][1], TESTIMONIALS[2][2])

# WRITTEN — the works page's rotating banner. The eight service names.
TICKER_SERVICES = [s[0] for s in SERVICES]

# captured from the contact form's own field, plus the service list
PROJECT_TYPES = [s[0] for s in SERVICES]
BUDGETS = ["Under SAR 50k", "SAR 50k – 150k", "SAR 150k – 400k", "SAR 400k+"]

# WRITTEN — the About page's culture strip.
LIFE_LEDE = ("A production team of twenty across direction, camera, edit, "
             "animation, live and immersive technology — under one roof.")


def brands_wall(html):
    html = fill(html, "brands_ticker_text", BRANDS_TICKER * 2)
    html = fill(html, "brands_testimony_text", [BRANDS_QUOTE[0]])
    html = fill(html, "brands_testimony_author_name", [BRANDS_QUOTE[1]])
    html = fill(html, "brands_testimony_author_designation", [BRANDS_QUOTE[2]])
    return html


def works_ticker(html):
    """The banner above the listing: HelloVoice's services, not Ariyana's.

    The reference prints one row and slides it. The second copy the marquee
    needs to loop against goes *inside* that row, not below it — emitting two
    sibling rows stacked them vertically and read as the banner being printed
    twice, which is exactly what it looked like.
    """
    items = re.findall(r'<div class="project_ticker_item">.*?</div></div>', html, re.S)
    if not items:
        return html
    icon = re.search(r'<div class="project_ticker_icon w-embed">.*?</div>', items[0], re.S)
    icon = icon.group(0) if icon else ""
    cell = ('<div class="project_ticker_item">'
            '<h2 class="project_ticker_title">{}</h2>' + icon + '</div>')
    row = "".join(cell.format(esc(s)) for s in TICKER_SERVICES)
    return re.sub(r'(<section class="project_ticker">).*?(</section>)',
                  lambda m: m.group(1)
                  + '<div class="project_ticker_row">'
                  + row
                  + f'<span class="project_ticker_dup" aria-hidden="true">{row}</span>'
                  + '</div>'
                  + m.group(2), html, flags=re.S, count=1)


def contact_page(html):
    """The two selects still offered a web agency's options."""
    def sub(m):
        name, body = m.group(1), m.group(2)
        opts = PROJECT_TYPES if "Project" in name else BUDGETS
        first = re.search(r'<option[^>]*value=""[^>]*>[^<]*</option>', body)
        head = first.group(0) if first else ""
        return (m.group(0)[:m.group(0).index(">") + 1] + head
                + "".join(f'<option value="{esc(o)}">{esc(o)}</option>' for o in opts)
                + "</select>")
    return re.sub(r'<select[^>]*name="([^"]*)"[^>]*>(.*?)</select>', sub, html, flags=re.S)


def life_strip(html):
    """The culture strip's lede. Matched on the reference's own sentence rather
    than by class — `text-case-normal` also sits on the why-choose copy."""
    return html.replace(
        "We’re with you all the way from the pilot to beyond. A great Team",
        LIFE_LEDE)
