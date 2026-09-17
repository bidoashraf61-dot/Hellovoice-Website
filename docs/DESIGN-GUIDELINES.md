# HelloVoice — Website Design Guidelines

**Direction:** Oxblood Editorial. A light page broken by full-bleed oxblood panels, with
one hot red accent and an acid lime reserved for live states. Derived from the Silva
reference for structure and the KAWS reference for the lime.

This documents what the site actually ships, not what was intended.

---

## 0. Quick reference

```css
/* paste this to start anything new */
--paper:#F4F1EE;  --card:#FFFFFF;  --panel:#5E1512;  --studio:#0B0A0A;
--ink:#14100F;    --ink-2:#5A5150; --ink-3:#8B807D;  --line:#E2DAD4;
--red:#F42010;    --red-deep:#C71200;                --lime:#C8F000;

--d:"Montserrat";  /* display — 800/900, uppercase, negative tracking */
--t:"Roboto";      /* text    — 400/500/700 */
--ui:"Manrope";    /* buttons, nav, labels — 600/700 */
--m: monospace;    /* eyebrow labels ONLY */

--gut:clamp(18px,4vw,44px);  --max:1320px;
--ease:cubic-bezier(.22,.8,.3,1);
```

| Decision | Answer |
|---|---|
| Ground | Warm off-white `#F4F1EE` |
| Sections that break it | Oxblood `#5E1512`, full-bleed |
| Accent | `#F42010` — the only one |
| Lime | Live states only |
| Headline case | UPPERCASE, tracking `-.035em` |
| Button | Manrope 700, 15px, sentence case |
| Corners | Square |
| Media | No borders, no cards, no shadows |
| Motion | Scroll-triggered, `.85s`, one easing curve |

---

## 1. Colour

```css
--paper:#F4F1EE;   /* page ground — warm off-white */
--card:#FFFFFF;    /* white cards, used on oxblood panels */
--panel:#5E1512;   /* oxblood — full-bleed section surface */
--panel-2:#4A100E; /* deeper oxblood, for the second panel in a row */
--studio:#0B0A0A;  /* hero and footer ground */

--ink:#14100F;     /* primary text — warm near-black */
--ink-2:#5A5150;   /* body */
--ink-3:#8B807D;   /* meta and captions */
--line:#E2DAD4;    /* hairline */

--red:#F42010;     /* the accent. Sampled from the logo */
--red-deep:#C71200;/* hover */
--lime:#C8F000;    /* live states only — never decorative */
```

**Rules**

- **Red is the only accent.** It marks action, the current page, and the one word in a
  headline that carries the meaning.
- **Lime has exactly one job:** something is live or tracking. The lens caption, panel
  eyebrows, one dot in three on the white cards. Using it decoratively breaks the signal.
- **Neutrals are warm-biased.** Every grey carries a trace of red. Never substitute a
  neutral grey — it flattens the whole thing.
- **Oxblood panels are the rhythm.** A light page with no dark sections reads as a
  document. The panels are what stop that.

---

## 2. Typography

| Role | Family | Weights | Used for |
|---|---|---|---|
| Display | **Montserrat** | 800, 900 | h1, h2, h3, card and project titles |
| Text | **Roboto** | 400, 500, 700 | body copy, ledes, descriptions |
| **UI** | **Manrope** | **600, 700** | **buttons, navigation, form labels, filters, captions** |
| Meta | system mono | — | eyebrow labels and bracket tags only |

All three self-hosted as woff2. No CDN.

### The button font — changed

The first build set buttons in **10px monospace, uppercase, `.16em` tracking**. It looked
technical and was genuinely hard to read. **Replaced with Manrope 700 at 15px, near-normal
tracking, sentence case.**

```css
.btn{
  font-family:"HV UI";          /* Manrope */
  font-weight:700;
  font-size:15px;
  letter-spacing:.01em;
  padding:17px 26px;
}
```

Manrope was chosen over Sora, Archivo and Montserrat because it is the most legible of the
four at small sizes while staying geometric enough to sit beside Montserrat. **Swapping it
is a one-line change** — replace `assets/fonts/manrope.woff2` and the `HV UI` `@font-face`
src.

**Monospace is now restricted to eyebrow labels only** — `— RIYADH · HEALTHCARE FILM` and
`[ our services ]`. Never buttons, never navigation, never form labels.

### Scale

```css
h1  { font:900 clamp(2.5rem,7.4vw,6.2rem)/0.9 Montserrat; letter-spacing:-.04em;
      text-transform:uppercase }
h2  { font:900 clamp(1.8rem,4.6vw,3.4rem)/0.96;           letter-spacing:-.034em;
      text-transform:uppercase }
h3  { font:800 clamp(1.1rem,2vw,1.5rem)/1.1;              letter-spacing:-.02em }
body{ font:400 16px/1.62 Roboto }
.lbl{ font:600 11px mono; letter-spacing:.18em; text-transform:uppercase }
```

**Display is uppercase with negative tracking. Meta is uppercase with wide tracking.** The
contrast between those two is most of the personality. Body copy is never uppercase.

### The one flourish

The accent phrase in a headline is red and skewed −7°, echoing the logo's oblique wordmark.
**Once per page, never twice.**

```css
.skew{ display:inline-block; transform:skewX(-7deg); transform-origin:left bottom }
```

---

## 3. Layout

```css
--gut: clamp(18px,4vw,44px);
--max: 1320px;
```

- Sections: `padding-block: clamp(56px,9vw,120px)`.
- **Media is large and unbordered.** Films run at full container width or in a 2–3 column
  grid, sitting directly on the page. No cards around images, no shadows, no rounded
  corners on media.
- Service and value lists are **rows with hairline separators**, not boxes. Rows indent
  14px on hover.
- White cards appear **only on oxblood panels** — that contrast is the point.
- Prose caps at 64ch, ledes at 56ch, section intros at 46ch.

---

## 4. Components

**Hero** — full-screen video, `autoplay muted loop playsinline`, with a five-stop scrim so
copy reads over any frame. On the live site the source is the Vimeo showreel with
`background=1`, which strips player chrome and loops natively.

**Header** — transparent over the hero with a knockout logo, solid off-white elsewhere.
Pages without a hero are solid at all times. Hides on scroll down, returns on scroll up.

**Marquee** — client logos, greyscale at 42% opacity, full colour on hover, paused on
hover. Duplicated track, 46s linear loop.

**Film card** — 16:9 frame, play badge fading in on hover, image scaling to 1.035 over
0.9s. Below it: industry in red, title in Montserrat, service and runtime in `--ink-3`.

**Lightbox** — Vimeo iframe injected only on click. Nothing loads a player until the
visitor asks for one. Escape and backdrop both close.

**Buttons** — square, Manrope 700, 15px. Primary is solid red; ghost is a 1.5px border
that inverts on hover.

**Form** — underline-only fields, no boxes. Focus turns the underline red. Every field has
a real `<label>`.

---

## 5. Motion

Scroll-driven, never automatic.

- **Reveals:** `translateY(26px)` + fade over 0.85s, triggered by IntersectionObserver at
  8% visibility with a −12% bottom margin.
- **Kinetic type:** headline lines sit in `overflow:hidden` and slide up from 102% over
  0.9s.
- **Stagger:** grouped children get a 70ms cascade.
- **Easing:** `cubic-bezier(.22,.8,.3,1)` everywhere.
- **The lens:** canvas, watches the pointer, blinks on its own, lime tally. Pauses when
  off-screen.

### Reveals use animations, not transitions — and this matters

```css
.js [data-rise]      { opacity:0; transform:translateY(26px) }
.js [data-rise].in   { animation:riseIn .85s var(--ease) forwards }
@keyframes riseIn    { to { opacity:1; transform:none } }
```

A class-triggered **transition** only runs if the browser has already painted the start
value. Adding the class in the same frame the element first paints leaves it stuck at
`translateY(102%)` — a headline that is permanently invisible. This happened, and it was
reproducible on the About page.

Three defences, all required:

1. **Animations with `forwards`**, not transitions.
2. The observer defers the class by **two animation frames**, so the start value paints.
3. A **2.6s failsafe** measures every reveal target and, if it is still hidden, forces
   `opacity:1; transform:none` inline. This also covers browsers that throttle animations
   entirely.

**Critical:** reveal states are gated behind a `.js` class set on `<html>` before first
paint. If the script never loads, everything is visible. **Never ship a hidden-by-default
headline that only JavaScript can reveal.**

---

## 6. Breakpoints

Four, and no others. Everything else is fluid via `clamp()`.

| Width | What changes |
|---|---|
| `≤ 1080px` | Three-column grids drop to two. Metrics go 4 → 2. Footer goes 4 → 2 columns |
| `≤ 900px` | Hero splits to one column |
| `≤ 820px` | The lens section stacks; lens centres |
| `≤ 720px` | Burger menu appears, nav becomes a panel. Everything goes single column. Service rows drop their third column. The header CTA hides |

The site is designed mobile-up in behaviour but authored desktop-first in CSS, because the
grid collapses are simpler expressed as overrides.

---

## 7. Assets

**Images**

| Use | Format | Widths | Quality |
|---|---|---|---|
| Film stills | WebP | 1400 and 700 | 74 / 72 |
| Client logos | WebP + alpha | 400 | 88 |
| Team portraits | WebP + alpha | 360 | 84 |
| Logo (display) | WebP | 760, 1520 | 90 |
| Logo (OG + schema) | **PNG** | 1520 | — |
| Favicons | PNG | 32, 180, 512 | — |

**The OG image must stay PNG or JPEG.** WhatsApp and LinkedIn do not reliably render WebP
in link previews. Display logos are WebP; the social and schema references are not.

**Every `<img>` carries `alt`, `width` and `height`.** The dimensions are not optional —
they reserve space and prevent layout shift. Decorative images get `alt=""`.

Everything below the fold gets `loading="lazy"`. Nothing in the first viewport does.

**Film stills** come from Vimeo's own thumbnails at 1920×1080, pulled by rewriting the
`-d_295x166` suffix on the thumbnail URL. They are real frames, not title cards — the old
site's posters were client logo plates, which is why the work looked like a logo grid.

**Fonts** are self-hosted woff2 in `assets/fonts/`. Montserrat and Manrope are preloaded;
Roboto is not, because body copy tolerates a swap.

---

## 8. Accessibility

Non-negotiable, and all of it verified at build:

- Exactly **one `<h1>` per page**, and heading order never skips a level.
- **Skip link** to `#main` as the first focusable element.
- **Every form field has a real `<label for>`.** No placeholder-as-label.
- Visible focus: `2px solid var(--red)` with `3px` offset. Never removed.
- The burger reports `aria-expanded`; the current nav item carries `aria-current="page"`.
- The lightbox is `role="dialog" aria-modal="true"`, closes on Escape and on backdrop.
- Decorative canvas gets `aria-hidden="true"`.
- `prefers-reduced-motion` disables all animation, the marquee and the lens.
- Contrast: `--ink` on `--paper` is well past AA. `--red` on white passes for large text and
  UI; **use `--red-deep` for small red text.**

---

## 9. Performance budget

Measured, not aspirational:

| | Budget | Actual |
|---|---|---|
| First paint, home | < 250 KB | **~168 KB** |
| First paint, inner pages | < 250 KB | ~198 KB |
| Whole site on disk | < 8 MB | **5.0 MB** |
| Fonts | < 120 KB | 90 KB (3 families) |
| CSS | < 30 KB | 18 KB |
| JS | < 20 KB | 9 KB, no dependencies |

Rules that keep it there:

- The hero video is `preload="metadata"`, so it streams rather than blocking first paint.
- No video player JavaScript loads until a visitor presses play.
- No framework, no jQuery, no analytics loaded synchronously.
- Every image is WebP and sized to its slot.

For context, the site this replaced shipped a **19.2 MB homepage** with 31.6 MB of animated
GIFs in the media library.

---

## 10. Non-negotiables

1. Warm-biased neutrals, never pure grey.
2. Red is the only accent; lime means *live* and nothing else.
3. Display uppercase with negative tracking, against wide-tracked mono meta.
4. **Monospace never appears on a button, a nav item or a form label.**
5. Media sits directly on the page — no cards, no borders, no shadows around film.
6. Oxblood panels break the light page. A page with none of them reads as a document.
7. Self-hosted fonts. Never a CDN.
8. No video player loads until the visitor presses play.
9. Reveal animations gated behind `.js`.
10. Verify `scrollWidth === clientWidth` at 375px before shipping.

---

## 11. What is deliberately not here

No 3D hero, no LED volume, no mascot. Tried and rejected — the work is the personality.
The lens survives in one section because it earns its place next to copy about review.

Arabic is out of scope for this build. The site is English only; Arabic delivery remains a
service described in the copy, not a feature of the site.
