#!/usr/bin/env python3
"""Generate the HelloVoice site.

A structural clone of the Ariyana Studio reference — same ten-section order,
same pinned tracks, same interaction grammar — carrying HelloVoice content
pulled from capture/content.json and build/content.py.

See docs/REFERENCE-TEARDOWN.md for the section-by-section contract and
docs/INVENTED-CONTENT.md for everything written rather than captured.
"""

import html as _html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CAP = json.loads((ROOT / "capture" / "content.json").read_text())
AR = json.loads((ROOT / "build" / "assets-report.json").read_text())

S = C.SITE

# ---------------------------------------------------------------- utilities

def esc(t):
    return _html.escape(_html.unescape(str(t)), quote=False)


def attr(t):
    return _html.escape(_html.unescape(str(t)), quote=True)


def mmss(sec):
    if not sec:
        return ""
    sec = int(sec)
    return "%d:%02d" % (sec // 60, sec % 60)


def swap(label, cls=""):
    """The reference renders every interactive label twice and swaps on hover."""
    e = esc(label)
    return ('<span class="swap' + ((" " + cls) if cls else "") + '">'
            "<span>" + e + "</span><span aria-hidden=\"true\">" + e +
            "</span></span>")


ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h12M9 3l5 5-5 5" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

STAR = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.3 5.9 20.6l1.4-6.8'
        'L2.2 9.1l6.9-.8L12 2z"/></svg>')


# The reference's pill: three white masks break the border, and a short bar
# beside the label stretches on hover.
MASKS = ('<span class="mask m1"></span><span class="mask m2"></span>'
         '<span class="mask m3"></span>')


def btn(label, href, cls="", icon=True):
    return ('<a class="btn ' + cls + '" href="' + attr(href) + '">' + MASKS +
            swap(label) + ('<span class="line"></span>' if icon else "") + "</a>")


# ------------------------------------------------------------------ content

NAV = [("Work", "work/"), ("Services", "services/"),
       ("About", "about/"), ("Contact", "contact/")]

# The reference's 2020–2025 year track. HelloVoice milestones.
YEARS = [
    ("2019", "The studio opens",
     "HelloVoice starts in Riyadh as a small crew making corporate film for Saudi "
     "brands, with one edit suite and a habit of saying yes to difficult briefs."),
    ("2021", "Healthcare takes over",
     "The first pharmaceutical accounts arrive and change how the studio works. "
     "Scripts start being written for medical review, not just for the screen."),
    ("2022", "Arabic and English together",
     "Bilingual delivery becomes the default rather than a post-production step, "
     "which changes timing, on-screen text and how voice is directed."),
    ("2023", "Congress speed",
     "An editor starts travelling to events so recap films cut and deliver while "
     "the congress is still running."),
    ("2024", "Animation and CGI",
     "Medical and scientific animation grows into its own department, alongside "
     "anamorphic DOOH and 3D work for retail and exhibition."),
    ("2025", "627 films",
     "The busiest year on record. Fifty-plus clients across eight industries, and "
     "the studio's first mixed-reality and VR builds."),
]

STEPS = [
    ("Brief", "We start with what the film has to achieve, who signs it off, and "
              "what it cannot say. On healthcare work the constraints shape the "
              "idea, so we surface them before anyone writes a word."),
    ("Script &amp; storyboard", "Scripts and boards go to medical, legal and "
              "regulatory before a camera is booked. The expensive mistake at this "
              "stage is a re-shoot; the cheap one is a re-write."),
    ("Production", "Crew, cast, location and kit, in Riyadh or wherever the brief "
              "goes. Bilingual direction on the day, so the Arabic and the English "
              "are performed rather than dubbed."),
    ("Delivery", "Grade, online, versioning and localisation. Every cut-down, "
              "aspect ratio and language sized for the platform it actually runs on."),
]

SERVICE_TAGS = {
    "Brand &amp; Campaign Films":
        ["Concept", "Direction", "Casting", "Locations", "Grade", "Versioning"],
    "Patient Awareness &amp; Education":
        ["Scripting", "Medical review", "Bilingual VO", "Subtitling", "Animation"],
    "Medical &amp; Scientific Animation":
        ["Mechanism of action", "3D", "Motion graphics", "Device visualisation"],
    "Congress &amp; Event Films":
        ["On-site edit", "Same-day recap", "Multi-camera", "Interviews", "Highlights"],
    "KOL &amp; Testimonial Films":
        ["Interview direction", "Multi-camera", "Bilingual", "Cut-downs"],
    "CGI, 3D &amp; Anamorphic DOOH":
        ["Anamorphic", "Product CGI", "Simulation", "Compositing", "Retail"],
    "Influencer &amp; UGC Campaigns":
        ["Talent", "Briefing", "UGC direction", "Volume delivery", "Reporting"],
    "Technology &amp; Immersive":
        ["Mixed reality", "VR", "Interactive", "Exhibition", "Booth activation"],
    "AI Production":
        ["Generative video", "Versioning at volume", "Localisation", "Rapid concepts"],
    "Post Production":
        ["Offline", "Online", "Grade", "Sound", "Localisation", "Mastering"],
}

INDUSTRIES = ["Healthcare", "Pharma", "Dermatology", "Medical devices",
              "FMCG", "Retail", "Technology", "Furniture"]

# One line per captured category. The old site shipped no per-film copy, so these
# describe the category of work rather than inventing detail about each film.
CATEGORY_LINE = {
    "Commercial Ads":
        "A commercial for {c} — concept, shoot and finish handled in-house.",
    "Corporate Videos":
        "A corporate film for {c}, built around what the business actually needed "
        "to say.",
    "Awareness Videos":
        "Patient awareness for {c}, scripted for medical review and delivered in "
        "Arabic and English.",
    "Events & Live Production":
        "Live coverage for {c}, cut on site so the film landed while the event was "
        "still running.",
    "CGI & Anamorphic Illusion":
        "CGI and anamorphic work for {c}, built for a screen people walk past rather "
        "than sit in front of.",
    "Interviews & Testimonials":
        "Interview films for {c}, directed so the speaker sounds like themselves.",
}

# ------------------------------------------------------------------- assets

DIMS = {r["slug"]: (r.get("w"), r.get("h"), r.get("portrait", False)) for r in AR["work"]}
IMGS = {r["slug"]: r["img"] for r in AR["work"]}
CLIENT_LOGOS = sorted(p.stem for p in (SITE / "assets" / "clients").glob("*.webp"))


# Film titles carry no consistent delimiter, so the client is resolved by
# matching the title against the real client roster on file. Anything that
# matches nothing is a showreel or an internal piece and gets no client.
CLIENT_NAMES = {
    "dermactive": "Dermactive", "qasser": "Qasser Al-Saraya", "neweast": "NewEast",
    "isuzu": "NewEast", "aisin": "NewEast", "automechanika": "NewEast",
    "suliman al habib": "Dr. Suliman Al Habib", "molyncke": "Mölnlycke",
    "molynlcke": "Mölnlycke", "molnlycke": "Mölnlycke",
    "abbott": "Abbott", "sanofi": "Sanofi", "sudair": "SPC Sudair Pharma",
    "spc": "SPC Sudair Pharma", "seroflo": "SPC Sudair Pharma",
    "al naghi": "Al Naghi", "elnahdi": "Nahdi", "el nahdi": "Nahdi",
    "nahdi": "Nahdi", "roche- posay": "La Roche-Posay",
    "roche-posay": "La Roche-Posay", "l'oreal": "L’Oréal",
    "loreal": "L’Oréal", "filorga": "Filorga", "spimaco": "Spimaco",
    "vichy": "Vichy", "qv": "QV", "jeddah derm": "Jeddah Derm",
    "ksmc": "KSMC", "whites": "Whites", "skintellectual": "Skintellectual",
    "kwait blood bank": "Kuwait Blood Bank", "zoiets": "Zoetis",
    "menarini": "Menarini", "medugate": "Menarini", "orchidia": "Orchidia",
    "bionnex": "Bionnex",
}


def client_for(title):
    low = title.lower()
    hits = [(len(k), v) for k, v in CLIENT_NAMES.items() if k in low]
    return max(hits)[1] if hits else ""


# Spelling corrections applied to captured film titles. Every one of these is a
# misspelling on the current site — client names and common words only, never a
# change of meaning. Listed in docs/INVENTED-CONTENT.md for sign-off.
TITLE_FIXES = [
    ("Awarness", "Awareness"), ("Molyncke", "Mölnlycke"),
    ("Molynlcke", "Mölnlycke"), ("Molnlycke", "Mölnlycke"),
    ("Kwait", "Kuwait"), ("Zoiets", "Zoetis"), ("Qasser El saraya", "Qasser Al-Saraya"),
    ("LA Roche- Posay", "La Roche-Posay"), ("L'Oreal", "L’Oréal"),
    ("Neweast", "NewEast"), ("Spc-", "SPC"), ("sudair", "Sudair"),
    ("Medical_Skintellectual", "Skintellectual"), ("CGi", "CGI"),
    ("Solo fresh", "Solo Fresh"), ("Medugate-", "Medugate —"),
    ("Orchidia -", "Orchidia —"), ("Dermactive -", "Dermactive —"),
    ("Ad - ", "Ad — "), ("FGM-", "FGM —"),
]


def clean_title(t):
    t = t.replace("ِ", "").strip()
    for a, b in TITLE_FIXES:
        t = t.replace(a, b)
    return t[:1].upper() + t[1:]


def projects():
    out = []
    for p in CAP["portfolio_projects"]:
        slug = re.sub(r"[^a-z0-9]+", "-", p["title"].lower()).strip("-")
        if slug not in IMGS:
            continue
        title = clean_title(_html.unescape(p["title"]))
        client = client_for(title)
        out.append({
            "slug": slug, "title": title, "client": client,
            "vimeo": p.get("vimeo_id"), "dur": p.get("duration_sec"),
            "img": IMGS[slug], "dims": DIMS.get(slug, (None, None, False)),
            "section": p.get("section") or "",
        })
    return out


PROJECTS = projects()
LANDSCAPE = [p for p in PROJECTS if not p["dims"][2]]


def featured(n=4):
    """Four films, one per client — the reference shows four distinct brands and
    repeating one here would read as a thin portfolio."""
    seen, out = set(), []
    for p in LANDSCAPE:
        key = p["client"].lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(p)
        if len(out) == n:
            break
    return out


FEATURED = featured()


# Display labels for the captured categories. The stored keys keep the original
# spelling so filtering still matches; only what the visitor reads is corrected.
SECTION_LABEL = {
    "Awareness Videos": "Awareness Films",
    "Commercial Ads": "Commercials",
    "Corporate Videos": "Corporate Films",
    "Events & Live Production": "Events &amp; Live",
    "CGI & Anamorphic Illusion": "CGI &amp; Anamorphic",
    "Interviews & Testimonials": "Interviews &amp; Testimonials",
}


def label(section):
    return SECTION_LABEL.get(section, section)


NO_CLIENT_LINE = {
    "Commercial Ads": "A commercial, taken from concept through to final delivery.",
    "Corporate Videos": "A corporate film, written, shot and finished in-house.",
    "Awareness Videos": "Patient awareness, scripted for medical review and "
                       "delivered in Arabic and English.",
    "Events & Live Production": "Live coverage, cut on site while the event was "
                                "still running.",
    "CGI & Anamorphic Illusion": "CGI and anamorphic work, built for a screen "
                                 "people walk past rather than sit in front of.",
    "Interviews & Testimonials": "Interview film, directed so the speaker sounds "
                                 "like themselves.",
}


def describe(p):
    if p["client"]:
        return CATEGORY_LINE.get(
            p["section"], "Made for {c} — concept through to final delivery."
        ).format(c=p["client"])
    return NO_CLIENT_LINE.get(p["section"],
                              "Made by HelloVoice, concept through to delivery.")


def media(kind, label, cls="", w=1280, h=720):
    """A placeholder plate the client swaps later. Keep the wrapper, change the src."""
    return ('<div class="media ' + cls + '" data-placeholder="' + attr(label) + '">'
            '<img src="/assets/placeholder/' + kind + '.webp" alt="" '
            'width="' + str(w) + '" height="' + str(h) + '" loading="lazy" '
            'decoding="async"></div>')


def shot(p, w="1400", cls="shot"):
    pw, ph, _ = p["dims"]
    ratio = str(pw) + "/" + str(ph) if pw and ph else "16/9"
    iw = int(w)
    ih = round(iw * ph / pw) if pw and ph else round(iw * 9 / 16)
    dur = mmss(p["dur"])
    runtime = '<span class="runtime">' + dur + "</span>" if dur else ""
    vim = p["vimeo"] or ""
    return (
        '<div class="' + cls + '" style="aspect-ratio:' + ratio + '"'
        + (' data-vimeo="' + attr(vim) + '" data-title="' + attr(p["title"]) +
           '" role="button" tabindex="0" aria-label="Play ' + attr(p["title"]) + '"'
           if vim else "") + ">"
        '<img src="/' + p["img"] + "-" + w + '.webp" alt="' + attr(p["title"]) +
        '" width="' + str(iw) + '" height="' + str(ih) + '" loading="lazy" decoding="async">'
        + ('<span class="play">Play</span>' if vim else "") + runtime + "</div>")


# -------------------------------------------------------------------- shell

def head(title, desc, path):
    url = S["origin"] + "/" + (path if path != "index.html" else "")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>" + esc(title) + "</title>\n"
        '<meta name="description" content="' + attr(desc) + '">\n'
        '<link rel="canonical" href="' + attr(url) + '">\n'
        '<meta property="og:title" content="' + attr(title) + '">\n'
        '<meta property="og:description" content="' + attr(desc) + '">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:url" content="' + attr(url) + '">\n'
        '<meta property="og:image" content="' + S["origin"] + '/assets/brand/logo@2x.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="theme-color" content="#F4F1EE">\n'
        '<link rel="icon" href="/assets/brand/icon-32.png" sizes="32x32">\n'
        '<link rel="apple-touch-icon" href="/assets/brand/icon-180.png">\n'
        '<link rel="preload" as="font" type="font/woff2" '
        'href="/assets/fonts/bebas-neue.woff2" crossorigin>\n'
        '<link rel="preload" as="font" type="font/woff2" '
        'href="/assets/fonts/dm-sans.woff2" crossorigin>\n'
        '<link rel="stylesheet" href="/assets/theme.css">\n'
        '<script>document.documentElement.classList.add("js")</script>\n'
        "</head>\n<body>\n")


def nav(active):
    links = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += ('<a class="nav_link" href="/' + href + '"' + cur +
                  '><i class="dot" aria-hidden="true"></i>' + swap(label) + "</a>")
    canvas = ""
    for label, href in [("Home", "")] + NAV:
        canvas += '<a href="/' + href + '">' + esc(label) + "</a>"
    return (
        '<div class="preloader"><p class="mark">HelloVoice</p>'
        '<div class="preloader_border" aria-hidden="true">'
        "<i></i><i></i><i></i><i></i><i></i></div></div>\n"
        '<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="nav">'
        '<a class="brand" href="/" aria-label="HelloVoice home">HelloVoice</a>'
        '<nav class="nav_menu" aria-label="Primary">' + links + "</nav>"
        '<button class="burger" type="button" aria-expanded="false" '
        'aria-controls="canvas" aria-label="Menu">'
        "<i></i><i></i><i></i></button></header>\n"
        '<div class="canvas" id="canvas">' + canvas +
        '<div class="meta"><a href="mailto:' + S["email"] + '">' + S["email"] + "</a>"
        '<a href="tel:' + S["office"].replace(" ", "") + '">' + S["office"] + "</a>"
        '<a href="' + S["instagram"] + '" rel="noopener">Instagram</a></div></div>\n')


def foot():
    pages = "".join('<li><a href="/' + h + '">' + swap(l) + "</a></li>"
                    for l, h in [("Home", "")] + NAV)
    svc = "".join('<li><a href="/services/">' + swap(_html.unescape(n)) + "</a></li>"
                  for n, _ in C.SERVICES[:5])
    return (
        '<footer class="foot"><div class="padding_global"><div class="container">'
        '<div class="foot_top">'
        "<div><h4>Studio</h4><address>" + esc(S["address"]) +
        "<br>" + esc(S["hours"]) + "</address>"
        '<p style="margin-top:16px"><a href="mailto:' + S["email"] + '">' +
        S["email"] + '</a><br><a href="tel:' +
        S["office"].replace(" ", "") + '">' + S["office"] + "</a></p></div>"
        "<div><h4>Pages</h4><ul>" + pages + "</ul></div>"
        "<div><h4>Services</h4><ul>" + svc + "</ul></div>"
        '<div><h4>Newsletter</h4>'
        '<p class="muted" style="font-size:15px">Occasional notes on what the studio '
        "is making. No more than a few a year.</p>"
        '<form class="foot_form" method="post" action="#" '
        'aria-label="Newsletter signup">'
        '<label class="skip" for="nl">Email address</label>'
        '<input id="nl" name="email" type="email" placeholder="Email address" required>'
        '<button type="submit">Join</button></form></div>'
        "</div>"
        '<p class="foot_big" aria-hidden="true">HELLOVOICE</p>'
        '<div class="foot_legal"><span>&copy; 2026 HelloVoice. All rights reserved.</span>'
        "<span>" + esc(S["tagline"]) + "</span>"
        '<a href="' + S["instagram"] + '" rel="noopener">Instagram</a></div>'
        "</div></div></footer>\n"
        '<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Video player">'
        '<div class="box"><button class="x" type="button">Close</button></div></div>\n'
        '<script src="/assets/vendor/lenis.min.js" defer></script>\n'
        '<script src="/assets/vendor/gsap.min.js" defer></script>\n'
        '<script src="/assets/vendor/ScrollTrigger.min.js" defer></script>\n'
        '<script src="/assets/site.js" defer></script>\n'
        "</body>\n</html>\n")


def page(path, title, desc, body, active=""):
    out = SITE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, path) + nav(active) +
                   '<main id="main">' + body + "</main>" + foot())
    return out


# ------------------------------------------------------------------ sections

def cta_section():
    line = "Let’s make something worth watching"
    row = "".join("<span>" + esc(line) + "</span>" for _ in range(4))
    return (
        '<section class="cta">'
        '<div class="ticker" aria-hidden="true">' + row + "</div>"
        '<div class="ticker is_stroke" aria-hidden="true">' + row + "</div>"
        + btn("Start a project", "/contact/", "cta_button") +
        "</section>")


def brands_section():
    """The reference's bordered box grid on black — 22 columns, two rows."""
    boxes = ""
    for i in range(44):
        slug = CLIENT_LOGOS[i % len(CLIENT_LOGOS)]
        boxes += ('<div class="box"><img src="/assets/clients/' + slug +
                  '.webp" alt="' + attr(slug.replace("-", " ").title()) +
                  '" loading="lazy" decoding="async" width="90" height="90"></div>')
    return ('<section class="brands" aria-label="Clients">'
            '<div class="brands_grid">' + boxes + "</div></section>")


def testimonials_section():
    cards = ""
    for q, name, role in C.TESTIMONIALS:
        initial = esc(name.strip()[:1].upper())
        cards += (
            '<figure class="tcard">'
            '<div class="stars" aria-label="Five out of five">' + STAR * 5 + "</div>"
            '<blockquote class="tquote">' + esc(q) + "</blockquote>"
            '<figcaption class="tauthor"><span class="tavatar" aria-hidden="true">' +
            initial + "</span><span><b>" + esc(name) + "</b><span>" + esc(role) +
            "</span></span></figcaption></figure>")
    return (
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">What clients say</h2>'
        '<p class="floating_text">In their words</p></div>'
        '<div class="testimonials">' + cards + "</div></div></section>")


# --------------------------------------------------------------------- home

def home():
    stat = C.METRICS[1]
    hero = (
        '<section class="hero">'
        '<div class="hero_image" aria-hidden="true">'
        '<img src="/assets/character/character.webp" alt="" width="1055" '
        'height="1701" fetchpriority="high" decoding="async">'
        "</div>"
        '<div class="hero_heading"><h1>HELLOVOICE</h1></div>'
        '<div class="hero_wrapper"><div class="hero_content">'
        '<h2 class="hero_sub">Healthcare-first film studio</h2>'
        '<p class="hero_info">' + esc(_html.unescape(C.HERO["lede"])) + "</p></div>"
        '<div class="hero_proof">'
        '<div class="hero_social"><span>Follow us</span><span class="rule"></span>'
        '<a href="' + S["instagram"] + '" rel="noopener">Instagram</a></div>'
        '<div class="hero_stat"><div><b>' + esc(stat[0]) + "</b><span>" +
        esc(stat[1]) + "</span></div></div>"
        "</div></div></section>")

    years = ""
    for y, tag, info in YEARS:
        years += ('<article class="year_item">'
                  '<p class="year_tag">' + esc(_html.unescape(tag)) + "</p>"
                  '<h3 class="year_text">' + y + "</h3>"
                  '<div class="year_text_line" aria-hidden="true"></div>'
                  '<div class="year_divider"></div>'
                  '<p class="year_info">' + esc(info) + "</p>"
                  + media("image-4x3", "Year image", "year_media", 1000, 750) +
                  "</article>")

    about = (
        '<section class="section padding_global"><div class="container">'
        '<div class="about_header">'
        '<div><h2 class="about_statement h4">HelloVoice is a Riyadh film studio. '
        "Two thirds of what we make is <span class=\"grad\">healthcare and "
        "pharma</span> — work that "
        "has to clear review and still be worth watching.</h2>"
        '<div class="about_actions">' + btn("More about the studio", "/about/") +
        "</div></div>"
        '<div class="about_pattern"><img src="/' + FEATURED[0]["img"] + '-1400.webp" '
        'alt="A still from ' + attr(FEATURED[0]["title"]) + '" width="1400" '
        'height="788" loading="lazy" decoding="async"></div>'
        "</div></div></section>"
        '<section class="about_track"><div class="about_sticky">'
        '<div class="year_rail">' + years + "</div></div></section>")

    steps = ""
    for i, (title, info) in enumerate(STEPS, 1):
        t = esc(_html.unescape(title))
        steps += ('<article class="step_item">'
                  '<span class="step_dot" aria-hidden="true"></span>'
                  '<p class="step_count">Step ' + ("%02d" % i) + "</p>"
                  '<div class="step_title_wrap"><h3 class="step_title">' + t + "</h3>"
                  '<h3 class="step_title is_gradiant" aria-hidden="true">' + t +
                  "</h3></div>"
                  '<p class="step_info">' + esc(_html.unescape(info)) + "</p>"
                  + media("image-1x1", "Step icon", "step_media", 800, 800) +
                  "</article>")

    step_section = (
        '<section class="section padding_global step_section">'
        '<div class="container">'
        '<div class="section_header"><h2 class="h3">How the work gets made</h2>'
        '<p class="floating_text">Brief to delivery</p></div>'
        '<div class="steps_wrapper">'
        '<div class="steps_line" aria-hidden="true"></div>' + steps +
        "</div></div></section>")

    items = ""
    for i, p in enumerate(FEATURED, 1):
        tags = "".join('<span class="tag">' + esc(t) + "</span>"
                       for t in [_html.unescape(label(p["section"])) or "Film",
                                 mmss(p["dur"]) or "Film"]
                       if t)
        items += (
            '<article class="work_item">'
            '<div class="work_left">'
            '<p class="work_index">' + ("%02d" % i) + " / " +
            ("%02d" % len(FEATURED)) + "</p>"
            '<h3 class="work_title">' + esc(p["title"]) + "</h3>"
            '<p class="work_desc">' + esc(describe(p)) + "</p>"
            '<div class="work_meta">' + tags + "</div>"
            + btn("Watch the film", "/work/", "", False) +
            "</div>"
            '<div class="work_right">'
            '<div class="work_visual" data-vimeo="' + attr(p["vimeo"] or "") +
            '" data-title="' + attr(p["title"]) + '" role="button" tabindex="0" '
            'aria-label="Play ' + attr(p["title"]) + '" '
            'style="aspect-ratio:' + str(p["dims"][0] or 16) + "/" +
            str(p["dims"][1] or 9) + '">'
            '<img src="/' + p["img"] + '-1400.webp" alt="' + attr(p["title"]) +
            '" width="1400" height="' +
            str(round(1400 * (p["dims"][1] or 9) / (p["dims"][0] or 16))) +
            '" loading="lazy" decoding="async">'
            '<span class="play">Play</span>'
            + ('<span class="runtime">' + mmss(p["dur"]) + "</span>" if p["dur"] else "")
            + "</div></div></article>")

    work = (
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">Featured work</h2>'
        '<p class="floating_text">' + str(len(PROJECTS)) + " films</p></div>"
        '<div class="work_track"><div class="work_items_wrapper">' + items +
        "</div></div>"
        '<div style="margin-top:64px;display:flex;justify-content:center">' +
        btn("All " + str(len(PROJECTS)) + " films", "/work/") + "</div>"
        "</div></section>")

    svc = ""
    for name, clients in C.SERVICES[:5]:
        tags = "".join('<span class="tag">' + esc(t) + "</span>"
                       for t in SERVICE_TAGS.get(name, []))
        svc += ('<article class="service_item"><div class="padding_global">'
                '<div class="container"><div class="service_inner">'
                '<h3 class="service_title">' + esc(_html.unescape(name)) + "</h3>"
                '<div class="service_side">'
                '<p class="service_tags_sub">Included</p>'
                '<div class="service_tags">' + tags + "</div>"
                '<p class="muted" style="margin-top:16px;font-size:15px">' +
                esc(_html.unescape(clients)) + "</p></div>"
                + media("video-16x9", "Service video", "service_media") +
                "</div></div></div></article>")

    services = (
        '<section class="service_section">'
        '<div class="section padding_global" style="padding-bottom:0">'
        '<div class="container">'
        '<div class="section_header"><h2 class="h3">What we make</h2>'
        '<p class="floating_text">Ten services</p></div></div></div>'
        + svc +
        '<div class="padding_global" style="padding-block:var(--sec)">'
        '<div class="container" style="display:flex;justify-content:center">' +
        btn("Every service", "/services/", "on-linen") +
        "</div></div></section>")

    showreel = (
        '<section class="showreel_track on-dark"><div class="showreel_sticky">'
        '<span class="showreel_word _1" aria-hidden="true">Play</span>'
        '<span class="showreel_word _2" aria-hidden="true">Reel</span>'
        '<div class="showreel_mask" data-vimeo="1129859185" data-title="HelloVoice showreel" '
        'role="button" tabindex="0" aria-label="Play the HelloVoice showreel">'
        '<iframe src="https://player.vimeo.com/video/1129859185?background=1&amp;autoplay=1'
        '&amp;loop=1&amp;muted=1&amp;dnt=1" allow="autoplay; fullscreen" '
        'title="HelloVoice showreel" loading="lazy" tabindex="-1"></iframe>'
        "</div></div></section>")

    # the reference fans ten logos in a radial arc from the bottom centre,
    # each rotated a further 36 degrees around a shared origin
    ring = ""
    for i in range(10):
        slug = CLIENT_LOGOS[i % len(CLIENT_LOGOS)]
        deg = -162 + i * 36
        ring += ('<span style="transform:translateX(-50%) rotate(' + str(deg) +
                 'deg)"><i><img src="/assets/clients/' + slug + '.webp" alt="" '
                 'loading="lazy" decoding="async" width="80" height="80"></i></span>')

    leaders = (
        '<section class="leader_section">'
        '<div class="leader_ring" aria-hidden="true">' + ring + "</div>"
        '<div class="leader_content">'
        '<p class="leader_badge">' + str(len(CLIENT_LOGOS)) + " brands on file</p>"
        '<h2>Trusted by <span class="grad">leaders</span></h2>'
        + btn("See the work", "/work/") +
        "</div></section>")

    body = (hero + brands_section() + about + step_section + work + services +
            showreel + leaders + testimonials_section() + cta_section())
    return page("index.html", "HelloVoice — Riyadh film and media production",
                "A Riyadh film studio. Two thirds of what we make is healthcare and "
                "pharma — campaign films, patient education, medical animation and "
                "immersive technology.", body, "")


# --------------------------------------------------------------------- work

def work_page():
    svcs = sorted({p["section"] for p in PROJECTS if p["section"]})
    fbtn = '<button type="button" data-f="all" aria-pressed="true">All</button>'
    for s in svcs:
        fbtn += ('<button type="button" data-f="' + attr(s) + '">' +
                 esc(_html.unescape(label(s))) + "</button>")

    cards = ""
    for p in PROJECTS:
        who = p["client"] or _html.unescape(label(p["section"])) or "HelloVoice"
        cards += ('<article class="wcard" data-svc="' + attr(p["section"]) + '">'
                  + shot(p, "700") +
                  '<div><p class="who">' + esc(who) + "</p>"
                  "<h3>" + esc(p["title"]) + "</h3></div></article>")

    body = (
        '<section class="pagehead padding_global"><div class="container">'
        "<h1>The <em>work</em></h1>"
        '<p class="lede">' + str(len(PROJECTS)) + " films made and delivered by "
        "HelloVoice. Every one plays through Vimeo — press any frame.</p>"
        "</div></section>"
        '<section class="padding_global" style="padding-bottom:var(--sec)">'
        '<div class="container">'
        '<div class="filters" id="filters" role="group" aria-label="Filter films">' +
        fbtn + "</div>"
        '<p class="count" id="count">' + str(len(PROJECTS)) + " films</p>"
        '<div class="work_grid" id="workgrid" data-stagger>' + cards + "</div>"
        "</div></section>" + cta_section())
    return page("work/index.html", "Work — HelloVoice",
                str(len(PROJECTS)) + " films made by HelloVoice for healthcare, "
                "pharma and consumer brands across the Gulf.", body, "work/")


# ----------------------------------------------------------------- services

def services_page():
    svc = ""
    for i, (name, clients) in enumerate(C.SERVICES, 1):
        tags = "".join('<span class="tag">' + esc(t) + "</span>"
                       for t in SERVICE_TAGS.get(name, []))
        svc += ('<article class="service_item" data-rise>'
                '<div class="service_inner">'
                '<div><h3 class="service_title">' + esc(_html.unescape(name)) + "</h3>"
                '<p class="service_tags_sub">Included</p>'
                '<div class="service_tags">' + tags + "</div></div>"
                "<div>"
                '<p class="muted">Recent: ' + esc(_html.unescape(clients)) + "</p>"
                '<p style="margin-top:20px">' +
                btn("Talk about this", "/contact/?service=" +
                    re.sub(r"[^a-z0-9]+", "-", _html.unescape(name).lower()).strip("-"),
                    "", False) + "</p>"
                "</div></div></article>")

    inds = "".join('<span class="tag">' + esc(i) + "</span>" for i in INDUSTRIES)
    body = (
        '<section class="pagehead padding_global"><div class="container">'
        "<h1>What we <em>make</em></h1>"
        '<p class="lede">Ten services, run by one team in Riyadh. A brand that needs '
        "a congress recap on Thursday and a mixed-reality build the same quarter "
        "should not need two suppliers.</p>"
        "</div></section>"
        '<section class="padding_global"><div class="container">' + svc +
        "</div></section>"
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">Industries</h2>'
        '<p class="floating_text">Where the work lands</p></div>'
        '<div class="service_tags">' + inds + "</div></div></section>"
        + testimonials_section() + cta_section())
    return page("services/index.html", "Services — HelloVoice",
                "Campaign films, patient education, medical animation, congress "
                "films, CGI, influencer campaigns, immersive technology and post "
                "production.", body, "services/")


# -------------------------------------------------------------------- about

def about_page():
    body_copy = "".join('<p class="muted" style="margin-bottom:20px">' + esc(b) + "</p>"
                        for b in C.ABOUT["body"])
    metrics = "".join('<div class="metric"><b>' + esc(v) + "</b><span>" + esc(l) +
                      "</span></div>" for v, l in C.METRICS)
    pillars = ""
    for title, info in C.PILLARS:
        pillars += ('<article class="step_item">'
                    '<p class="step_count">' + esc(title) + "</p>"
                    '<h3 class="step_title">' + esc(title) + "</h3>"
                    '<p class="step_info">' + esc(info) + "</p></article>")

    team = ""
    for name, role, img in C.TEAM:
        if img:
            fig = ('<img src="/assets/team/' + img + '.webp" alt="' + attr(name) +
                   '" width="460" height="575" loading="lazy" decoding="async">')
        else:
            initials = "".join(w[0] for w in name.split()[:2]).upper()
            fig = '<div class="init" aria-hidden="true">' + initials + "</div>"
        team += ('<article class="member"><figure>' + fig + "</figure>"
                 "<h3>" + esc(name) + "</h3><span>" + esc(role) + "</span></article>")

    years = ""
    for y, tag, info in YEARS:
        years += ('<article class="step_item">'
                  '<p class="step_count">' + y + "</p>"
                  '<h3 class="step_title">' + esc(_html.unescape(tag)) + "</h3>"
                  '<p class="step_info">' + esc(info) + "</p></article>")

    body = (
        '<section class="pagehead padding_global"><div class="container">'
        "<h1>The <em>studio</em></h1>"
        '<p class="lede">' + esc(C.ABOUT["lede"]) + "</p>"
        "</div></section>"
        '<section class="padding_global"><div class="container">'
        '<div class="metrics">' + metrics + "</div></div></section>"
        '<section class="section padding_global"><div class="container">'
        '<div style="max-width:74ch">' + body_copy + "</div></div></section>"
        + brands_section() +
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">How we work</h2>'
        '<p class="floating_text">Three commitments</p></div>'
        '<div class="steps">' + pillars + "</div></div></section>"
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">The story so far</h2>'
        '<p class="floating_text">2019 to now</p></div>'
        '<div class="steps">' + years + "</div></div></section>"
        '<section class="section padding_global"><div class="container">'
        '<div class="section_header"><h2 class="h3">The team</h2>'
        '<p class="floating_text">Riyadh</p></div>'
        '<div class="team" data-stagger>' + team + "</div></div></section>"
        + testimonials_section() + cta_section())
    return page("about/index.html", "About — HelloVoice",
                "A media production studio in Riyadh working with multinational "
                "healthcare and consumer brands across the Gulf.", body, "about/")


# ------------------------------------------------------------------ contact

def contact_page():
    opts = "".join('<option value="' +
                   re.sub(r"[^a-z0-9]+", "-", _html.unescape(n).lower()).strip("-") +
                   '">' + esc(_html.unescape(n)) + "</option>" for n, _ in C.SERVICES)
    body = (
        '<section class="pagehead padding_global"><div class="container">'
        "<h1>Start a <em>project</em></h1>"
        '<p class="lede">Tell us what the film has to achieve and who has to sign it '
        "off. We will come back within one working day.</p>"
        "</div></section>"
        '<section class="padding_global" style="padding-bottom:var(--sec)">'
        '<div class="container">'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));'
        'gap:var(--gut);align-items:start">'
        '<form class="form" method="post" action="#">'
        '<div class="field"><label for="name">Your name</label>'
        '<input id="name" name="name" type="text" autocomplete="name" required></div>'
        '<div class="field"><label for="email">Email</label>'
        '<input id="email" name="email" type="email" autocomplete="email" required></div>'
        '<div class="field"><label for="company">Company</label>'
        '<input id="company" name="company" type="text" autocomplete="organization"></div>'
        '<div class="field"><label for="service">What do you need</label>'
        '<select id="service" name="service"><option value="">Select a service</option>' +
        opts + "</select></div>"
        '<div class="field"><label for="message">About the project</label>'
        '<textarea id="message" name="message" '
        'placeholder="Audience, deadline, who signs it off"></textarea></div>'
        '<button class="btn is-red" type="submit">' + swap("Send enquiry") + ARROW +
        "</button></form>"
        "<div>"
        "<h2 class=\"h4\" style=\"margin-bottom:24px\">Studio</h2>"
        "<address style=\"font-style:normal;line-height:1.8\" class=\"muted\">" +
        esc(S["address"]) + "<br>" + esc(S["hours"]) + "</address>"
        '<p style="margin-top:22px;line-height:1.9">'
        '<a href="mailto:' + S["email"] + '">' + S["email"] + "</a><br>"
        '<a href="tel:' + S["office"].replace(" ", "") + '">' + S["office"] +
        "</a> &middot; office<br>"
        '<a href="tel:' + S["mobile"].replace(" ", "") + '">' + S["mobile"] +
        "</a> &middot; mobile</p>"
        '<p style="margin-top:22px">'
        '<a class="btn" href="https://wa.me/' + S["wa"] + '" rel="noopener">' +
        swap("WhatsApp") + ARROW + "</a></p>"
        "</div></div></div></section>" + cta_section())
    return page("contact/index.html", "Contact — HelloVoice",
                "Start a project with HelloVoice. Al-Olaya, Riyadh. "
                "info@hellovoice.co.uk", body, "contact/")


def notfound():
    body = ('<section class="pagehead padding_global"><div class="container">'
            "<h1>Page <em>not found</em></h1>"
            '<p class="lede">That page has moved or never existed.</p>'
            '<p style="margin-top:32px">' + btn("Back to the work", "/work/") +
            "</p></div></section>" + cta_section())
    return page("404.html", "Not found — HelloVoice", "Page not found.", body)


def extras():
    urls = ["", "work/", "services/", "about/", "contact/"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("<url><loc>" + S["origin"] + "/" + u + "</loc><changefreq>monthly"
                  "</changefreq></url>")
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm))
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + S["origin"] + "/sitemap.xml\n")


def main():
    (SITE / "assets" / "theme.css").write_text((ROOT / "build" / "theme.css").read_text())
    (SITE / "assets" / "site.js").write_text((ROOT / "build" / "site.js").read_text())
    built = [home(), work_page(), services_page(), about_page(),
             contact_page(), notfound()]
    extras()
    total = 0
    for p in built:
        kb = p.stat().st_size / 1024
        total += kb
        print("  %-28s %6.1f KB" % (str(p.relative_to(SITE)), kb))
    print("  %-28s %6.1f KB" % ("total html", total))
    print("  %d films · %d client logos" % (len(PROJECTS), len(CLIENT_LOGOS)))


if __name__ == "__main__":
    main()
