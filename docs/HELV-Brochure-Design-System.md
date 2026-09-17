# Hello Voice — Brochure Design System

Extracted from the built Technology Activations brochure so it can be reused on other
projects. Everything here is what the page actually ships, not an intention.

**Direction in one line:** a dark broadcast control room. Equipment-rack layout, square
corners, hairline separators, one red accent used as a tally light. Deliberately
single-theme — it does not switch to light mode.

---

## 1. Colour

The red is sampled from the Hello Voice logo itself. The neutrals are **warm-biased**, not
pure grey — each one carries a trace of red so the palette reads as chosen rather than
defaulted. Never substitute a neutral grey; it flattens the whole thing.

```css
--ink:       #0B0A0B;  /* page ground — near-black, faint warm bias */
--panel:     #131113;  /* card and section surface */
--panel-2:   #1A171A;  /* card surface on hover */
--rail:      #221E21;  /* grid rail behind 1px card gaps */
--line:      #332C30;  /* visible hairline */
--line-soft: #231F22;  /* subtle hairline */

--text:      #F4F0F1;  /* primary */
--text-2:    #B2A8AC;  /* body / secondary */
--text-3:    #7B7175;  /* meta, codes, captions */

--red:       #F42010;  /* brand accent, tally light */
--red-hot:   #FF5236;  /* hover, headline accent, glow */
--red-deep:  #8C1607;  /* dim/inactive tally */

--amber:     #E9A93C;  /* semantic only — "in development". Never decorative */
```

**Rules**
- Red is the only accent. Spend it on one thing per screen and keep everything else quiet.
- Amber is reserved for a single meaning (in-development state). Using it decoratively
  breaks the signal.
- `body` must set `background: var(--ink)` explicitly — a transparent body borrows whatever
  ground the host paints.

---

## 2. Typography

Three roles. Two embedded families plus the system monospace stack.

| Role | Family | Weights | Used for |
|---|---|---|---|
| Display | **Montserrat** | 800, 900 | h1, h2, card names, step numbers |
| Text | **Roboto** | 400, 500, 700 | body copy, descriptions |
| Utility | system mono | — | codes, status, tags, captions |

```css
--display:   "HV Display", "Helvetica Neue", Arial, sans-serif;   /* Montserrat */
--text-face: "HV Text", "Helvetica Neue", Arial, sans-serif;      /* Roboto */
--mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
```

**Why Montserrat:** it is a geometric grotesque, the same species as the Hello Voice
wordmark, so the display type and the logo agree instead of competing. This is the reason
for the choice — do not swap it for Inter or Space Grotesk.

Both families are open-licensed (Montserrat OFL, Roboto Apache 2.0) and are **subset to
Latin and embedded as woff2 data URIs**, about 84KB for all five faces. No CDN, no font
requests, no silent fallback.

### Scale

```css
h1        { font: 900 clamp(2.5rem, 7.6vw, 6rem)/0.92 var(--display);
            letter-spacing: -0.035em; text-transform: uppercase; }
h2        { font: 900 clamp(1.65rem, 4.2vw, 3rem)/0.98 var(--display);
            letter-spacing: -0.03em;  text-transform: uppercase; }
.card-name{ font: 800 1.2rem/1.1 var(--display);
            letter-spacing: -0.015em; text-transform: uppercase; }
body      { font: 400 1rem/1.62 var(--text-face); }
.desc     { font-size: 0.875rem; line-height: 1.6; color: var(--text-2); }
.meta     { font: 0.6875rem var(--mono); letter-spacing: 0.14em;
            text-transform: uppercase; color: var(--text-3); }
```

**Details that carry the look**
- Display type is uppercase with **negative** tracking. Tight, not airy.
- Mono/meta type is uppercase with **wide** tracking (`0.14em`). The contrast between the
  two is most of the personality.
- Headings get `text-wrap: balance`; body copy stays near 60–65 characters.
- Use `font-variant-numeric: tabular-nums` anywhere digits align.

### The one flourish
The hero accent word is skewed to echo the logo's oblique wordmark. Used **once** on the page:

```css
.accent { display:inline-block; color:var(--red); transform:skewX(-7deg);
          transform-origin:left bottom; }
```

---

## 3. Layout

```css
--gut: clamp(1.15rem, 4vw, 2.75rem);   /* page gutter */
--max: 1320px;                          /* container */
```

**The rack grid** — the signature device. Cards sit on a rail-coloured background with 1px
gaps, so separators are the background showing through rather than borders. This is what
makes it read as equipment rather than as cards.

```css
.rack   { display:grid; grid-template-columns:repeat(auto-fill, minmax(300px,1fr));
          gap:1px; background:var(--rail); border:1px solid var(--rail); }
.card   { background:var(--panel); display:flex; flex-direction:column; }
.card:hover { background:var(--panel-2); }
```

**Rules**
- Square corners. Radius `0`, or `2px` at most. No rounded cards, no accent rails.
- Space with flex/grid `gap`, never per-element margins.
- Sections: `padding-block: clamp(3.5rem, 7vw, 6rem)`.
- Section heading blocks cap at `60ch`; body notes at `52ch`.
- Wide content gets its own `overflow-x:auto` container; the body never scrolls sideways.

---

## 4. Components

**Monitor** — 16:9 surface, near-black `#0A090A`, with a scanline and vignette overlay:

```css
.monitor::after {
  content:""; position:absolute; inset:0; pointer-events:none;
  background:
    repeating-linear-gradient(180deg, rgba(255,255,255,.03) 0 1px, transparent 1px 3px),
    radial-gradient(ellipse at 50% 55%, transparent 45%, rgba(0,0,0,.55) 100%);
}
```

**Tally light** — an 8px **square** (broadcast tallies are square, not round). It encodes
real state, which is the point: solid red = live, dim = standby, amber = in development.

```css
.tally { width:8px; height:8px; background:var(--red-deep); opacity:.55; }
[data-status="live"] .tally { background:var(--red); opacity:1;
                              box-shadow:0 0 9px var(--red); }
[data-status="dev"]  .tally { background:var(--amber); opacity:.9; }
```

**Tag** — mono micro-label, hairline box, no fill:
`font-size:.5875rem; letter-spacing:.1em; text-transform:uppercase; border:1px solid var(--line-soft); padding:.28rem .5rem;`

**Buttons** — square, mono, wide-tracked. Primary is solid `--red`; secondary is
`--panel` with a `--line` border.

**Section eyebrow** — a mono label in `--red-hot` preceded by a 22px red rule:
`.eyebrow::before { content:""; width:22px; height:1px; background:var(--red); }`

**Hero glow** — a single red radial behind the headline:
`radial-gradient(ellipse at center, rgba(244,32,16,.20), rgba(244,32,16,0) 68%)`

**Modal** — `display:flex` with `margin:auto` on the card. Do **not** use
`place-items:center`; it clips tall content. Media capped at `max-height:52vh`.

---

## 5. Motion

Restrained. Ambient motion is limited to two things: a slow pulse on the live indicator and
a continuous ticker.

- Transitions: `.18s`–`.2s` on colour, background and border only.
- Tally pulse: `2.4s ease-in-out infinite`, opacity 1 → .35.
- Ticker: `58s linear infinite`, `translateX(0 → -50%)` over a duplicated track, paused on
  hover.
- Canvas waveforms run on a single `requestAnimationFrame` loop, drawing only the canvases
  an `IntersectionObserver` reports as visible.

Always guard:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration:.001ms !important; animation-iteration-count:1 !important;
    transition-duration:.001ms !important;
  }
}
```

---

## 6. Voice

Short declaratives. Concrete over clever. A headline states the benefit in plain words
("Your product, floating in mid-air"), the description gives 40–60 words of substance, and
tags stay qualitative — never publish invented specifications.

---

## 7. Non-negotiables

Six things that carry the identity. Change any of them and it stops looking like this:

1. Warm-biased neutrals, never pure grey.
2. Square corners and hairline separators — no rounded cards with accent rails.
3. Uppercase display with negative tracking against wide-tracked mono.
4. One accent colour, plus amber for one semantic job only.
5. Structural markers must encode something true. The tally means footage status; if a
   marker means nothing, remove it.
6. Self-hosted subset fonts. Never link a font CDN.

---

## 8. Reuse checklist

- [ ] Copy the token block from §1 verbatim
- [ ] Embed Montserrat 800/900 and Roboto 400/500/700 as subset woff2 data URIs
- [ ] Set `body { background: var(--ink); color: var(--text); }` explicitly
- [ ] Build lists on the rack grid, not on bordered cards
- [ ] Give every status indicator a real meaning before adding it
- [ ] Add the `prefers-reduced-motion` guard
- [ ] Verify no horizontal overflow at 390px (`scrollWidth === clientWidth`)

**Reference build:** `HelloVoice-Tech-Activations.html`
· spec: `docs/superpowers/specs/2026-08-12-tech-activations-brochure-design.md`
