# Hello Voice — Technology Catalogue Design System

Self-contained brief. Everything needed to rebuild, extend or restyle the technology
catalogue without the originating conversation. Written 2026-08-12.

**Reference build:** `User Assets/Tech Prochuere/HelloVoice-Technology-Catalogue.html`

---

## 1. The direction, in one line

A **broadcast equipment rack**. Applications are channel strips in banks; each has a monitor
and a tally light. Chosen because the client sells screens, projection and live installations
— the vocabulary of a control room is the subject's own world, not decoration borrowed from
elsewhere.

Deliberately **single-theme dark**. This is a screening surface for video, so it commits to
one world rather than supporting a light mode. Every colour is painted explicitly so the page
holds on any host background — nothing inherits.

**Avoid:** rounded cards with a coloured accent rail, centred everything, emoji section
markers, gradient hero on white, Inter/Space Grotesk. The rack reads as considered precisely
because it uses square corners, hairline rules and a real metaphor.

---

## 2. Colour

Sampled from the Hello Voice logo: the bubble red measures ~`#F81800` at its brightest,
falling to ~`#C81E00`. Everything else is built around it.

Neutrals are **warm — biased toward the red**, never pure grey. A pure `#808080` reads as
unconsidered next to this accent.

```css
:root{
  /* grounds — darkest to lightest */
  --ink:#0B0A0B;        /* page background */
  --panel:#131113;      /* card / channel surface */
  --panel-2:#1A171A;    /* hover, raised surface */
  --rail:#221E21;       /* the 1px grid the cards sit on */

  /* lines */
  --line:#332C30;       /* visible hairline, borders */
  --line-soft:#231F22;  /* internal divider */

  /* text */
  --text:#F4F0F1;       /* headings, primary */
  --text-2:#B2A8AC;     /* body copy */
  --text-3:#7B7175;     /* labels, meta, tags */

  /* brand */
  --red:#F42010;        /* tally, accent, primary CTA */
  --red-hot:#FF5236;    /* headline accent, hover */
  --red-deep:#8C1607;   /* dim/inactive tally */

  /* semantic — one job only */
  --amber:#E9A93C;      /* "no material" / provisional. Never decorative. */
}
```

### Rules

- **Red is the tally light.** It signals live state and one primary action. It is not a
  general-purpose highlight — if red appears in three places on one card, two are wrong.
- **Amber is semantic, not a second accent.** It means exactly one thing: this item is
  incomplete. Using it decoratively destroys the signal.
- Spend boldness in one place — the hero accent word — and keep everything else quiet.

### Contrast — known defect

| Pair | Ratio | Verdict |
|---|---|---|
| `--text` on `--panel` | 16.9:1 | ✅ |
| `--text-2` on `--panel` | 8.2:1 | ✅ AAA |
| `--text-3` on `--panel` | **4.03:1** | ❌ **fails AA** (needs 4.5) |

`--text-3` is used for tags and meta labels at **9.4px–11px**, which compounds it.
**Fix before launch:** lift to `#8C8286` (≈5.0:1) and raise the tag size from `.5875rem`
to `.6875rem`.

---

## 3. Typography

Three roles. Two self-hosted faces plus a system stack.

| Role | Family | Weights | Licence | Used for |
|---|---|---|---|---|
| Display | **Montserrat** | 800, 900 | SIL OFL 1.1 — embeddable | Hero, bank titles, card names |
| Body | **Roboto** | 400, 500, 700 | Apache 2.0 — embeddable | Descriptions, running text |
| Utility | system mono | — | n/a | Codes, tallies, labels, filenames |

```css
--display:"HV Display","Helvetica Neue",Arial,sans-serif;   /* Montserrat */
--text-face:"HV Text","Helvetica Neue",Arial,sans-serif;    /* Roboto */
--mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
```

**Why Montserrat:** the Hello Voice wordmark is an oblique geometric grotesque. Montserrat's
geometry rhymes with it — this is a brand-derived choice, not a default reach. It must be set
**tight and uppercase** to work; at default tracking it looks generic.

**Never link a webfont CDN.** Inline as `@font-face` with a base64 `data:` URI. Subset first:

```bash
pyftsubset Montserrat-900.ttf \
  --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122,U+2190-2193,U+2022,U+00D7,U+00B0" \
  --layout-features='kern,liga,tnum,onum' --flavor=woff2 --output-file=mont900.woff2
```

Five faces subset this way total ~84KB (~113KB as base64).

### Scale and treatment

| Element | Size | Treatment |
|---|---|---|
| Hero h1 | `clamp(2.5rem, 7.6vw, 6rem)` | 900, uppercase, `letter-spacing:-.035em`, `line-height:.92` |
| Hero accent | inline span | `--red-hot` + `transform:skewX(-7deg)` — the one flourish |
| Bank title h2 | `clamp(1.65rem, 4.2vw, 3rem)` | 900, uppercase, `-.03em` |
| Card name h3 | `1.2rem` | 800, uppercase, `-.015em` |
| Card headline | `.9375rem` | 500, `--red-hot` |
| Body | `.875rem` / `1rem` | 400, `line-height:1.6–1.62` |
| Meta / mono | `.6875rem` | uppercase, `letter-spacing:.14em`, `tabular-nums` |

Body measure stays near 65 characters. Headings get `text-wrap:balance`.

---

## 4. Layout

- Container `--max:1320px`; gutter `clamp(1.15rem, 4vw, 2.75rem)`.
- **The rack:** `grid-template-columns:repeat(auto-fill,minmax(300px,1fr))` with **`gap:1px`
  over a `--rail` background**. The hairlines *are* the rack frame — not borders on cards.
- Square corners throughout. Max radius anywhere: 2px.
- Section rhythm `clamp(3.5rem, 7vw, 6rem)`.
- Sibling spacing via flex/grid `gap`, never per-element margins.
- Verified clean at **390px** — single column, no horizontal overflow.

---

## 5. The tally system — the load-bearing idea

Every card carries a status light. **It is derived from data, never authored**, and it
encodes something true: whether that application actually has a film.

| Status | Light | Label | Meaning |
|---|---|---|---|
| `live` | `--red`, glowing | "Live" / "N films" | ≥1 film has a playable ID |
| `standby` | `--red-deep`, 55% | "Awaiting upload" | footage exists, no ID yet |
| `dev` | `--amber` | "No material" | nothing supplied — placeholder |

```js
function statusOf(item){
  if(!item.films || !item.films.length) return "dev";
  return item.films.some(f => f.id) ? "live" : "standby";
}
```

**Do not remove or fake this.** A catalogue that admits what is unfinished is more persuasive
than one pretending to be complete, and it doubles as the production tracker. Cards with no
material show an animated waveform slate instead of a poster — visibly a placeholder, never
mistakable for content.

---

## 6. Components

**Channel card** — 16:9 monitor (poster `object-fit:cover`, scanline + vignette overlay via
`::after`, `pointer-events:none`), spec code top-left, tally top-right, play mark centred when
live. Below: name, headline, description, tags pinned to the bottom with `margin-top:auto`.

**Bank header** — mono code in `--red-hot` preceded by a 22px rule, then the uppercase title,
then one line of plain-English framing.

**Modal player** — third-party iframe (Vimeo/YouTube) mounted **on click only**, destroyed on
close. Never render 20 players on one page. Poster sits behind as `background-image` so the
frame is never a black void. Film tabs appear only when an application has more than one film.

> **Sizing trap:** do not put `max-height` on the 16:9 monitor — the player letterboxes inside
> it. Constrain the *card width* instead:
> `width:min(920px, 100%, calc((100svh - 250px) * 16 / 9))`.

**Waveform slate** — canvas oscilloscope, seeded per card, drawn in red with glow. Echoes the
sound arcs in the logo. One shared `requestAnimationFrame` loop; `IntersectionObserver` so only
visible canvases draw; static frame under `prefers-reduced-motion`.

---

## 7. Motion

Restrained. Hover lifts and brightens; the tally glows; the waveform gains amplitude. The
ticker scrolls and pauses on hover. Everything collapses under `prefers-reduced-motion:reduce`.
More animation would read as AI-generated rather than designed.

---

## 8. Assets

| Asset | Location |
|---|---|
| Logo (all formats) | `User Assets/HelloVoice/` — AI, EPS, PDF, PNG, transparent PNG |
| Dark-ready logo | Wordmark is black; invert low-saturation pixels to light grey for dark grounds |
| Client logos | `assets/clients-fy26/` (22), `assets/clients-fy25/` |
| Brand red | `#F42010` (sampled `#F81800`→`#C81E00`) |

Logo recolour, for dark backgrounds:

```python
if max(r,g,b) - min(r,g,b) < 42:      # low saturation = the black wordmark
    px[x,y] = (255-int(r*0.42),)*3 + (a,)   # leave the red bubble untouched
```

---

## 9. Build pipeline

`src2.html` (markup + CSS + logic, with `__TOKEN__` placeholders) + `data.js` (content)
→ `build2.py` inlines fonts, logo and posters as data URIs → single self-contained HTML.

**Known defect:** the built file has **no `<!doctype html>`, `<html>`, `<head>` or `<body>`** —
it was authored to be wrapped by a host that supplies them. Standalone it renders in **quirks
mode** (`document.compatMode === "BackCompat"`). Any self-hosted build must add a proper
document wrapper with `<html lang="en">`, `<meta charset>`, viewport, description and Open
Graph tags.

---

## 10. Carry-over fixes

1. Wrap in a real HTML document — kills quirks mode, adds `lang`.
2. Lift `--text-3` to `#8C8286`; raise tag size to `.6875rem`.
3. Add `<meta name="description">` and OG tags — the page shares as a bare URL today.
4. Focus-trap the modal; 25 elements remain tabbable behind it.
5. Deep links (`#hv-int-06`) so one application can be sent on its own.
6. Externalise posters and lazy-load them when self-hosting (currently 1.17MB inline).
