# Ariyana Studio — reference clone

> **Branch `ref-parity`.** This branch is a clone of
> `https://ariyana-studio.webflow.io` carrying **the reference's own content,
> images and video**. It is a build target for verifying parity, not a
> deliverable. The HelloVoice site lives on `ariyana-clone`.
>
> Every borrowed asset is tagged `data-placeholder`. See
> [`docs/REFERENCE-AUDIT.md`](docs/REFERENCE-AUDIT.md#licensing).

A static site. No framework, no CMS, no build step at runtime.

---

## Run it

```bash
python3 build/serve.py 8811   # no-store on documents; http.server caches them
```

## Rebuild it

```bash
python3 build/clone.py
```

---

## How it is built

The reference's own served HTML is the source. Rather than re-authoring the
markup, `build/clone.py` transforms each captured page in place:

| | |
|---|---|
| `cdn.prod.website-files.com/*` | → `/assets/ref/<file>` (113 files mirrored) |
| the Webflow shared stylesheet | → `/assets/css/main.css`, its `url()`s rewritten and nothing else |
| jQuery, the Webflow runtime, IX2, IX3, Turnstile | removed |
| GSAP, ScrollTrigger, SplitText, Lenis | vendored under `/assets/vendor` |
| the site's inline Lenis snippet | → `/assets/js/motion.js` |

That makes structure, palette, type scale and spacing identical **by
construction** — there is no re-authored design system to drift. Only the
behaviour layer is rewritten, and it is written against values measured off the
live site rather than estimated.

## What is where

| path | |
|---|---|
| `site/` | **The website.** Deploy this folder and nothing else |
| `build/clone.py` | The transform. `HERO_EXCEPTION` at the top toggles the one divergence |
| `site/assets/js/motion.js` | The behaviour layer — every interaction, with its source value in a comment |
| `site/assets/css/main.css` | The reference's stylesheet, `url()`s localised |
| `site/assets/css/clone.css` | Only what Webflow's runtime used to supply. No colours, sizes or spacing |
| `site/assets/css/hero-exception.css` | The one sanctioned divergence |
| `scratchpad/ariyana/` | The captured reference: `main.css` and all seven pages |
| `capture/reference-assets/` | The 113 mirrored CDN files |
| `capture/fetch_all.py` | Re-mirrors them from `reference-assets-all.json` |
| `docs/REFERENCE-ANIMATIONS.md` | Every animation value and where it was read from |
| `docs/REFERENCE-AUDIT.md` | Section-by-section parity, and the divergence table |

## The pages

`/` · `/about-us/` · `/projects/` · `/service/` · `/contact-us/` · `/blogs/` ·
`404.html`

---

## Parity

Verified at 1440×900 and 375×812. Every section on every page matches the
reference's top offset and height to the pixel; the document heights are equal
(18490 home, 13685 about, 6659 service, 13281 home at 375). Motion was measured
against the live site rather than eyeballed — the work stack lands within one
unit, the showreel within 2–3px across its whole curve, the marquees within
0.2 px/s. Full tables in the audit.

## Notes

**The one divergence is the hero** — white, carrying the approved 3D character
instead of the reference's dark photograph. It is built from the reference's own
light-surface nav variant, isolated to one stylesheet and one function, and
reverts with `HERO_EXCEPTION = False`.

**Webflow hides animated elements before first paint.** Its stylesheet holds a
rule keyed on `html.w-mod-js:not(.w-mod-ix3)`, and that rule is what enumerates
every animated hook. `clone.py` stamps `w-mod-js` at build time; `motion.js`
adds `w-mod-ix3` once initial states are set, with a 2s failsafe. **Do not
remove either** — without the failsafe a script error leaves the page blank.

**Desktop-only interactions must be gated.** IX2 registers most hovers, the
showreel and the step panel for `main` (≥992px) only, and the reference's
stylesheet lays those elements out differently below it. Applying a desktop
initial state at every width is what broke the mobile layout twice; they now
sit in `gsap.matchMedia()` with cleanup.

**Fonts are the reference's own TTFs**, mirrored from its CDN — which avoids the
Google `css2` trap where the latin subset is last and taking the first silently
gives you Cyrillic. Verified: Bebas measures 0.577× Arial. ~0.99× means it is
falling back.

**Console errors are inherited, not introduced.** 20 inline SVGs carry
`width="auto"`, verbatim from the reference. Same count on both sites.
