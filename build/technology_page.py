"""The Technology Catalogue, built from the client's handover.

Source: User Assets/Tech Prochuere/HANDOVER — catalogue.json (23 applications
in 3 banks), 21 posters, and a README that specifies the content model.

Two things from that README are followed literally because the handover says
so in as many words:

  * **Status is derived, never authored.** It is recomputed from each
    application's films on every build:
        no films            -> no-material
        any film with an id -> live
        otherwise           -> awaiting-upload
    The JSON carries a `status` field; it is ignored. The README's reasoning is
    that a hand-set field drifts out of sync within a week — an editor adds a
    Vimeo id and the card should promote itself.

  * **The tally system stays.** Every card shows its state. A catalogue that
    admits what is unfinished reads as more credible than one pretending to be
    complete, and it doubles as the production tracker.

What is *not* carried over is the reference build's own styling. The handover
ships a single-theme dark "broadcast rack" stylesheet; this has to live inside
the HelloVoice site, so the structure, components and copy are the handover's
and the surface is the site's — the same linen ground, type scale and red as
every other page. The tally keeps its own semantic colours because those encode
state, not decoration.
"""
import html as _html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "content" / "technology.json"

# The handover's own words, kept verbatim.
LEDE = ("Applications Hello Voice builds and operates — interactive walls, "
        "holograms, projection mapping and CGI. Each one is the technology "
        "itself, not the campaign it was built for.")

STATUS_LABEL = {
    "live": "Live",
    "awaiting-upload": "Awaiting upload",
    "no-material": "No material",
}


def esc(s):
    return _html.escape(str(s), quote=True)


def derive_status(app):
    """Recomputed from the films every build — see the module docstring."""
    films = app.get("films") or []
    if not films:
        return "no-material"
    return "live" if any(f.get("id") for f in films) else "awaiting-upload"


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def _embed(f):
    """A player URL with the lightbox's parameters appended, not glued on.

    An unlisted film's `embed` already carries its privacy hash as `?h=...`,
    so joining with a second `?` produced `?h=27d6bfd696?autoplay=1` — one
    parameter whose value is the hash plus a query string. Vimeo then reads a
    hash that does not match and refuses the film as private, and autoplay,
    title, byline and dnt are all silently dropped with it.
    """
    src = f.get("embed") or f"https://player.vimeo.com/video/{f['id']}"
    if f.get("host") == "local":
        return src          # served from this site; no player parameters apply
    h = f.get("hash")
    if h and "h=" not in src:
        src += ("&" if "?" in src else "?") + f"h={h}"
    sep = "&" if "?" in src else "?"
    return f"{src}{sep}autoplay=1&title=0&byline=0&portrait=0&dnt=1"


def _card(app):
    """The still is the control.

    The handover listed each film as its own chip — "Film 01", "Film 02" —
    under a poster that did nothing when you clicked it. Those labels name
    nothing a visitor is looking for, and the obvious target was inert. So the
    still plays, and an application with more than one film gets a pager on the
    still to move between them rather than a row of numbered tags.

    The status lights are gone at the client's request: live / awaiting upload
    / no material described how complete this document was, not what HelloVoice
    can build, and a visitor has no use for the distinction.
    """
    status = derive_status(app)
    poster = app.get("poster")
    stem = pathlib.Path(poster).stem if poster else None
    films = [f for f in (app.get("films") or []) if f.get("id")]

    if stem:
        visual = (f'<img class="tech_poster" src="/assets/tech/{esc(stem)}.webp" '
                  f'alt="" loading="lazy" decoding="async" width="720" height="405"/>')
    else:
        # the handover's empty-state slate: visibly a placeholder, impossible
        # to mistake for content
        visual = ('<div class="tech_slate" aria-hidden="true">'
                  + "".join('<span></span>' for _ in range(9)) + '</div>')

    # The "provisional" badge described the state of the handover document,
    # not the offer, and read to a visitor as unfinished work (audit P1-12,
    # removed with the client's approval 12 Sep 2026).
    prov = ""

    if films:
        srcs = "|".join(_embed(f) for f in films)
        pager = ""
        if len(films) > 1:
            pager = (
                '<div class="tech_pager">'
                '<button type="button" class="tech_pager_btn" data-tech-prev '
                f'aria-label="Previous film for {esc(app["name"])}">'
                '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" '
                'aria-hidden="true"><path d="M15 5l-7 7 7 7z"/></svg></button>'
                f'<span class="tech_pager_count" data-tech-count>1 / {len(films)}</span>'
                '<button type="button" class="tech_pager_btn" data-tech-next '
                f'aria-label="Next film for {esc(app["name"])}">'
                '<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" '
                'aria-hidden="true"><path d="M9 5l7 7-7 7z"/></svg></button>'
                '</div>')
        still = (
            f'<div class="tech_still has-film" data-tech-films="{esc(srcs)}" '
            f'data-tech-index="0">{visual}'
            # data-ig-embed is what the existing lightbox reads, and it is
            # collected once at init — so the first film has to be on the
            # button at load. The pager rewrites it in place.
            f'<button type="button" class="tech_play" data-tech-play '
            f'data-ig-embed="{esc(_embed(films[0]))}" '
            # stated, not inferred — see the lightbox note in motion.js
            f'data-ratio="{esc(films[0].get("ratio") or "16:9")}" '
            f'data-title="{esc(app["name"])}" '
            f'aria-label="Play film for {esc(app["name"])}">'
            '<span class="tech_play_glyph" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">'
            '<path d="M8 5v14l11-7z"/></svg></span></button>'
            f'{pager}</div>')
    else:
        still = f'<div class="tech_still">{visual}</div>'

    return (
        f'<article class="tech_card is-{status}" id="{esc(app["code"])}">'
        f'{still}'
        f'<div class="tech_body">'
        f'<p class="tech_code">{esc(app["code"])}{prov}</p>'
        f'<h3 class="tech_name">{esc(app["name"])}</h3>'
        f'<p class="tech_headline">{esc(app.get("headline") or "")}</p>'
        f'<p class="tech_desc">{esc(app.get("description") or "")}</p>'
        + ('<ul class="tech_tags">'
           + "".join(f'<li>{esc(t)}</li>' for t in (app.get("tags") or []))
           + '</ul>' if app.get("tags") else "")
        + '</div></article>')


def _placeholder(app):
    """A card with nothing to show yet: no poster and no film, or copy that says so.

    Those cards printed the handover's internal note to the public — "this card
    is a placeholder and will not go live until Hello Voice sends both". They
    are left out of the build until their content exists; adding the poster,
    films and copy to technology.json brings them back on the next build.
    """
    if not app.get("poster") and not (app.get("films") or []):
        return True
    words = f'{app.get("headline") or ""} {app.get("description") or ""}'.lower()
    return "awaiting content" in words or "placeholder" in words


def _bank(bank, idx=0):
    return (
        f'<section class="tech_bank is-alt-{idx % 2}" id="{esc(bank["id"])}">'
        '<div class="padding_global"><div class="container">'
        '<div class="tech_bank_head">'
        f'<p class="tech_bank_code">{esc(bank["code"])}</p>'
        f'<h2 data-title-anim="" class="service_section_title">{esc(bank["title"])}</h2>'
        f'<p class="tech_bank_note">{esc(bank.get("note") or "")}</p>'
        '</div>'
        '<div class="tech_grid">'
        + "".join(_card(a) for a in bank["applications"] if not _placeholder(a))
        + '</div></div></div></section>')


def build(html: str) -> str:
    banks = load()
    apps = [a for b in banks for a in b["applications"]]
    counts = {"live": 0, "awaiting-upload": 0, "no-material": 0}
    for a in apps:
        counts[derive_status(a)] += 1
    n_films = sum(len(a.get("films") or []) for a in apps)

    # CLIENT FIGURE. The catalogue documents 23 applications; HelloVoice's own
    # count of what they build and operate is higher, and that is the number
    # they want stated. Banks and the film tally are gone at their request —
    # both described the state of this document rather than the offer.
    stats = [("+50", "Applications")]

    # The hero opens on a technology showreel cut for the job.
    #
    # It stood on the anamorphic film for a while — the only thing in the
    # catalogue that was already an edited reel — but that is one discipline
    # standing in for eleven, and it carries HelloVoice's own logo burned into
    # the top-left corner, which landed on the navigation.
    #
    # This is assembled from eleven of the catalogue's own installations, four
    # seconds each: things people touch, then things that surround them, then
    # work at architectural scale. The logo measures x 0.026-0.117, y
    # 0.061-0.206 across these files, so every clip is cropped 21% off the top,
    # full width kept — which clears the badge outright instead of slicing it
    # in half and leaving a fragment welded to the frame edge. Two clips start
    # later than the rest to get past burned-in subtitles.
    #
    # A local file, not a Vimeo player: it is decoration behind a headline, and
    # 6.3MB served from our own origin beats a third-party player process.
    hero = (
        '<section class="service_hero_section is-tech is-reel-hero">'
        '<div class="ig_hero_media" data-reel-slot>'
        '<video class="ig_hero_video" autoplay muted loop playsinline '
        'preload="metadata" poster="/assets/video/tech-reel-poster.jpg" '
        'aria-hidden="true">'
        '<source src="/assets/video/tech-reel.mp4" type="video/mp4"/>'
        '</video></div>'
        '<div class="ig_hero_scrim" aria-hidden="true"></div>'
        '<div class="padding_global"><div class="container">'
        '<div class="ig_hero_copy">'
        '<h1 class="service_hero_title">Technology Activations</h1>'
        f'<p class="ig_lede">{esc(LEDE)}</p>'
        '<div class="ig_stats">'
        + "".join(f'<div class="ig_stat"><p class="ig_stat_num">{esc(n)}</p>'
                  f'<p class="ig_stat_label">{esc(l)}</p></div>' for n, l in stats)
        + '</div></div></div></div></section>')

    body = hero + "".join(_bank(b, i) for i, b in enumerate(banks))

    out, n = re.subn(
        r'<section class="service_hero_section".*?(?=<section class="cta_section")',
        lambda _m: body, html, count=1, flags=re.S)
    if not n:
        raise SystemExit("technology: could not find the service hero -> cta span")
    return out.replace("<title>", "<title>Technology Activations — ", 1)
