# Reference audit — `ref-parity`

Verification of `site/` against `https://ariyana-studio.webflow.io`.

**Verdict: layout parity is exact.** Every section on every page matches the
reference's top offset and height to the pixel, at both 1440×900 and 375×812,
with the document heights equal. The one divergence is the hero, and it is
deliberate.

Parity is exact by construction rather than by eye: the build transforms the
reference's own served HTML and serves its own stylesheet, only rewriting asset
URLs. Nothing about the palette, type scale, spacing or grounds is re-authored,
so there is nothing there to drift. What *was* rebuilt is the behaviour layer —
Webflow's IX2 and IX3 runtimes are not portable — and that is where the audit
below concentrates.

---

## Method

Both pages opened at the same viewport and probed with the same script:
section offsets and heights, computed styles, and for the scroll tracks the
transform sampled against scroll progress. Screenshots were used only to
sanity-check; the numbers are the audit.

---

## Layout — 1440 × 900

| section | reference top/height | build | |
|---|---|---|---|
| `hero_section` | 0 / 1266 | 0 / 1266 | ✓ |
| `about_section` | 1266 / 3530 | 1266 / 3530 | ✓ |
| `step_section` | 4796 / 741 | 4796 / 741 | ✓ |
| `work_section` | 5537 / 3319 | 5537 / 3319 | ✓ |
| `brands_section` | 8857 / 720 | 8857 / 720 | ✓ |
| `service_section` | 9577 / 2897 | 9577 / 2897 | ✓ |
| `showreel_section` | 12528 / 2250 | 12528 / 2250 | ✓ |
| `leader_section` | 14778 / 1350 | 14778 / 1350 | ✓ |
| `testimonial_section` | 16128 / 1162 | 16128 / 1162 | ✓ |
| `cta_section` | 17290 / 306 | 17290 / 306 | ✓ |
| `footer` | 17686 / 804 | 17686 / 804 | ✓ |
| **document** | **18490** | **18490** | ✓ |

Spot-checked deeper on the year track: `.year_item` `[-795, 59, 480, 782]`,
`.year_text` `[-788, 59, 363, 245]`, `.year_image` `[-795, 541, 480, 300]`,
`.about_sticky` `[0, 0, 1440, 900]` — identical on both.

## Layout — 375 × 812

| section | reference | build | |
|---|---|---|---|
| `hero_section` | 0 / 640 | 0 / 640 | ✓ |
| `about_section` | 640 / 2856 | 640 / 2856 | ✓ |
| `step_section` | 3496 / 1222 | 3496 / 1222 | ✓ |
| `work_section` | 4718 / 1888 | 4718 / 1888 | ✓ |
| `brands_section` | 6606 / 713 | 6606 / 713 | ✓ |
| `service_section` | 7319 / 2392 | 7319 / 2392 | ✓ |
| `showreel_section` | 9745 / 353 | 9745 / 353 | ✓ |
| `leader_section` | 10098 / 568 | 10098 / 568 | ✓ |
| `testimonial_section` | 10666 / 1343 | 10666 / 1343 | ✓ |
| `cta_section` | 12010 / 108 | 12010 / 108 | ✓ |
| `footer` | 12169 / 1113 | 12169 / 1113 | ✓ |
| **document** | **13281** | **13281** | ✓ |

Two defects were found and fixed here, both the same mistake: applying a
desktop-only initial state at every width.

- **`step_section` was 889 instead of 1222.** `motion.js` collapsed
  `.step_item_info_wrap` to `height: 0` unconditionally. The reference only
  does that on desktop, where the panel opens on hover; below 992px it stands
  open. Four steps × ~83px = the missing 333px.
- **`showreel_section` was 453 instead of 353.** The mask was being given
  `50vw × 40vh` inline at every width, overriding the stylesheet's
  `width: 100%; height: auto` below 991px.

Both now sit inside `gsap.matchMedia()` with cleanup, along with the
testimonial pile's rest rotations and the leader copy's `opacity: .5` — all
four are `main`-only in IX2 and all four are neutralised by the reference's own
stylesheet below 991px.

## The other pages

| page | document height | h1 | broken images | hidden elements | overflow-x |
|---|---|---|---|---|---|
| `/` | 18490 ✓ | 1 | 0 | 0 | none |
| `/about-us/` | 13685 ✓ | 1 | 0 | 0 | none |
| `/service/` | 6659 ✓ | 1 | 0 | 0 | none |
| `/projects/` | 5286 | 1 | 0 | 0 | none |
| `/blogs/` | 6690 | 1 | 0 | 0 | none |
| `/contact-us/` | 2603 | 1 | 0 | 0 | none |
| `/404.html` | 2100 | 0 | 0 | 0 | none |

`/`, `/about-us/` and `/service/` were compared section-by-section against the
live reference and match exactly. The rest were verified for structural health
only; they share the same stylesheet and transform, and nothing on them is
page-specific beyond content.

## Motion

| | verified against |
|---|---|
| year track | reference x curve, +640 → −2716, 9 sample points |
| work stack | reference transforms at 1/16 resolution; build within 1 unit at p = 0.5 |
| showreel | reference mask/text curve at 7 scroll offsets; build within 2–3px throughout |
| logo fan rotation | reference 243.5deg at scroll 15400; build −116.5deg ≡ 243.5deg |
| CTA marquees | reference ∓180.1 px/s; build ∓180.0 |
| brands marquee | reference +81.7 px/s; build +81.5 |
| hovers | IX2 config values, transcribed |

Full values in [`REFERENCE-ANIMATIONS.md`](REFERENCE-ANIMATIONS.md).

---

## Divergences

Everything below is deliberate. Anything not in this table is a defect.

### Asked for by the client

| # | divergence | note |
|---|---|---|
| C1 | **Titles fade up from opacity 0** as they drop | The reference holds opacity at 1 through the whole drop. The fade runs over the first ~55% of the fall so the `back.inOut` overshoot still reads. Toggle with `FADE_IN` in `motion.js`. **This makes an un-run reveal invisible rather than merely unanimated**, so every reveal now registers with a 4s failsafe that force-completes anything on screen and still untouched. |
| C2 | **A client logo marquee is section two**, between the hero and About | Built from the reference's own brand marks, which ship as white knockouts for its black brands grid and are laid to the page's ink with `filter: brightness(0)`. Runs at the brands ticker's speed so the page keeps one marquee tempo; pauses on hover. |
| C3 | **The About section carries a film** above the year track | 16:9, the reference's own People/Person footage as placeholder. Plays muted on entry, pauses off screen, and the corner button toggles it. |
| C4 | **The works listing filters by category** | Six controls built from the tags already in the markup. Cards leave the grid so it reflows, and the reference's every-other-card offset is re-applied to whatever stays visible. |
| C5 | **The blog is removed** | `/blogs` is not built, and every link to it or to a post is stripped from the nav, canvas menu and footer. |
| C6 | **The hero is white and carries the 3D character** | The client's standing decision. Built from the reference's own light-surface variant — the `is-secondary` / `is-dark` nav classes it already uses on `/about-us` and `/service` — so it introduces no colour, size or spacing the design system does not contain. Isolated to `assets/css/hero-exception.css` and one function in `build/clone.py`; `HERO_EXCEPTION = False` reverts it exactly. |

### Structural

| # | divergence | reason |
|---|---|---|
| S1 | No Webflow runtime, jQuery, IX2 or IX3 | Static build. Behaviour is hand-written against the same GSAP + Lenis stack the reference loads, using the reference's own measured values. |
| S2 | Cloudflare Turnstile removed from the newsletter form | Third-party widget keyed to the reference's own site. Forms show their success block and stop the navigation. |
| S3 | The preloader is removed from the tree after 3.2s | The reference parks it at `translateY(-120%)` and never plays it back in, but its own copy hangs in headless contexts. Not visible on either site. |
| S4 | Assets are self-hosted under `/assets/ref/` | Mirrored from `cdn.prod.website-files.com`, including both webfonts. See the licensing note below. |
| S5 | The footer's `/utilities/*` links are removed | Style guide, licences and changelog are the template's own scaffolding, not in the agreed page set, and would 404 here. |
| S6 | Card tags are buttons, not links to tag archives | `/project-tags/*` pages are not in this build. Now that the listing filters in place, the tag drives that filter — a better answer than an archive page. |
| S7 | The step cards' collapsed info panel is CSS, not a GSAP set | A `matchMedia` context can be reverted out from under an inline style, which silently springs the panel open and adds 125px to the section. The initial state is now a plain desktop media query. |

## Defects found and fixed after the client changes

| what was wrong | cause | fix |
|---|---|---|
| Section headlines on the landing page appeared with no animation | The reveal failsafe force-completed anything within 1.5 viewports at the 4s mark. A visitor who scrolled during those first seconds arrived at sections already revealed — the animation was skipped, not lost. | The rescue now only fires for a reveal whose **trigger has already passed its start** while its timeline is still at zero, i.e. one that genuinely failed. It re-checks at 4s, 8s and 14s. The hero, which plays on load and has no trigger, is snapped on the plain timer. |
| `ARIYANA STUDIO` broke mid-word, dropping the `O` to a second line | SplitText was called with `type: "chars"`. Each character becomes an `inline-block`, so with no word wrappers the browser may break a line between any two letters. | Split as `"words,chars"`, which is what the reference does — its four-word heading reports 28 nodes, 4 words + 24 characters. Words stay atomic; the heading holds one line. |
| The About page's "Respond within / Make an offer in / Close the deal in" cards showed only the first, and its corner graphic read as oversized | `.why_choose_track` is a 300vh pinned horizontal track — `.why_choose_item` is `width:100%` in a nowrap flex row, so three cards span ~3920px — and **that track was never implemented**. The section pinned for 2700px showing card one, frozen, with its 224px graphic the only other thing on screen. | Implemented with the reference's own trigger values, read live: `start: clamp(top top)`, `end: clamp(bottom 130%)`, `scrub: 0.8` — the year track's configuration, and the same 2212→3742 range. Each card now lands flush at the container's left edge at each third. |

## Second review round

| what was wrong | cause | fix |
|---|---|---|
| `ARIYANA STUDIO` wrapped to two lines and sat on top of the character | The h1 is `19vw`, and `vw` counts the scrollbar while the content box does not — so the wordmark is a few pixels wider than the space it has. It measured 1440px in a 1425px box. | `white-space: nowrap` on the hero h1. The `vw` sizing already scales it. |
| The primary button's label vanished on hover | Every button prints its label twice inside a clipping `.button_text_wrapper`: the first copy in place, the second at `top: 100%` and coloured **white**. Hover is meant to slide the pair up so the white copy takes over. That slide was never implemented, so the ground went black under a black label. | Implemented the swap. Verified: on hover the ground is `rgb(0,0,0)` and the white copy lands exactly at the wrapper top. |
| The CTA button also went black | It should not: nothing in IX2 darkens it, its ground is pale lime and **both** copies of its label are black. It had been lumped in with `.button_primary`. | Separated. Its hover is the label swap plus the arrow rolling over inside its clipped disc. |
| The team section scrolled 2700px with nothing happening | Another 300vh pinned track with no animation attached. | Each card rises from `yPercent: 100` to 0, staggered, scrubbed across the track — which is what the reference's static residual implies: `y = [0, 296, 196, 96]` against heights `[396, 296, 196, 96]`, i.e. every card offset by exactly one of itself. |
| Rebuilds appeared to do nothing | `clone.css` and `motion.js` were linked without a version, so browsers served stale copies. This cost real debugging time twice. | Both are stamped `?v=<content hash>` at build time. |

## Added sections (beyond the reference)

The home page now runs **hero → client logos → film → About → …**. Neither of
the first two additions exists on the reference.

| section | what it is |
|---|---|
| `.client_banner_section` | Two-copy marquee of client marks on a dark ground, −81.7 px/s, pausing on hover. |
| `.film_section` | Full-bleed film: `100vw × 100vh`, `object-fit: cover`, muted, looping, autoplaying. Pauses off screen; a corner control stops it, and a manual pause is not overridden by scrolling. `100dvh` under 768px so collapsing mobile browser chrome does not resize it. |

The film's play is attempted on every ScrollTrigger update rather than once on
entry. A one-shot `onEnter` is not enough — a browser can reject autoplay while
the tab is backgrounded, a restored scroll position starts the page already
past the trigger, and a fast scroll can skip the callback. Any of those left it
sitting on its poster.

### Deviations added on request

| # | deviation | note |
|---|---|---|
| 6 | The client logo banner sits on a **dark** ground, marks at full colour and opacity | Asked for the marks "coloured and normal". The placeholder marks are white knockouts, so a dark ground is the only way to show them in their own colour rather than recolouring them with a filter — and it is how the reference presents this same set in its brands grid. Hover lifts and scales the mark instead of fading it, and the marquee pauses. When real full-colour logos replace these, the ground can go back to white. |
| 7 | `.why_choose_item` background-size pinned to `148px` on desktop | The reference leaves it at `auto`, painting the corner graphic at its intrinsic 186–213 × 224 — about a third of the 680px card. Verified identical in both builds before changing it. Pinned smaller on request; delete the block in `clone.css` to restore `auto`. |

### Known gap

`.team_section .track` carries a ScrollTrigger on the reference with the same
`scrub: 0.8` configuration, and the build does not implement it. The cards'
staggered layout is CSS (`margin-top: 100 / 200 / 300px` on cards 2–4) and
renders correctly, so the section is not broken — but whatever that scrub adds
is missing. It could not be measured this session: the browser pane was hidden,
which throttles `requestAnimationFrame`, so Lenis stops driving ScrollTrigger
and every scroll-sampled value reads as its resting state. Re-measure with the
pane visible.

## Inherited defects — reproduced, not fixed

| | |
|---|---|
| 20 inline SVGs carry `width="auto" height="auto"`, which the console rejects | Verbatim from the reference's markup — identical count in both. Correcting it would be a divergence. |
| The testimonial pile overlaps by `−10vw`, so a quote cannot be read in full without hovering | The reference's own composition. |
| `.year_wrapper` is 3880px wide inside a clipped track | The reference's own; the horizontal scrub is what makes it legible. |

---

## Licensing

Every borrowed asset carries `data-placeholder="ariyana-reference"` — **134
across the seven pages** (61 home, 35 service, 27 about, 6 projects, 4 blogs,
1 on 404). All 113 mirrored files under `site/assets/ref/` are the template's
licensed assets, as is the copy, which is Ariyana Studio's own.

This build is a review target. Nothing ships until

```bash
grep -rc 'data-placeholder' site --include='*.html'
```

returns zero.

## Fonts

Bebas Neue and DM Sans are the reference's own TTFs, mirrored from its CDN —
which sidesteps the Google `css2` subset trap entirely. Verified live: Bebas
measures **0.577×** Arial for the same string. A fallback would measure ~0.99×.

## Hero character — 3D (divergence, home only)

The home hero's character is the client's own asset, not the reference's VR
photograph. It now ships in two layers:

1. **`site/assets/character/character-red.webp`** — the flat cutout from
   `User Assets/Char PNG.webp`, tilted toward the cursor by motion.js. This is
   what every visitor gets, and the only layer on touch, on narrow viewports,
   under `prefers-reduced-motion`, and under `navigator.connection.saveData`.
2. **`site/assets/character/character.glb`** — a textured mesh, rendered with
   three.js by `assets/js/hero3d.js`, which cross-fades over the cutout once
   loaded. Every failure path (no WebGL, network, decode) simply leaves layer 1
   in place, so the upgrade can never regress the page.

The mesh came from single-image reconstruction, so it is accurate from the
front and invented behind. **Yaw is capped at 20°** for that reason — past
roughly 45° the head reads as a flat slab. That cap is a quality limit, not a
stylistic one.

Measured on the built page at 1440×900: the mesh occupies **72.03%** of the
section height against the cutout's 72%, its feet land **0.2px** off the
baseline, and it is centred to **0px**. Those are solved by a four-pass
calibration in `fit()` rather than a closed form, because under perspective the
parts of him nearest the camera project larger than his bounding box.

Added weight, gzipped: three.js 163 KB + GLTFLoader 23 KB +
BufferGeometryUtils 7 KB + mesh 903 KB. All of it loads after
DOMContentLoaded (measured: document ready at 114 ms, GLB requested at 113 ms),
so none of it blocks first paint. The mesh's texture was downsampled 2048→1024,
which took the GLB from 4.23 MB to 1.24 MB with no visible difference.

Three.js is MIT; it carries no `data-placeholder` because it is not borrowed
from the reference.

## Animations matched to the reference (read, not estimated)

Both were extracted from the reference's own IX3 config in
`webflow.24c5dbb3.*.js` rather than sampled, because sampling cannot see a
timeline that has not fired. Ease indices resolve against Webflow's ordered
ease table, found in `webflow.schunk.aa86840d07d01efd.js`.

**Testimonials** — timeline `t-f0abf957`, trigger `wf:scroll`,
`start "top center"`, `end "bottom top"`, `scrub: null` (so it *plays once*,
it is not scrubbed), and `conditionalPlayback: dont-animate` on
medium/small/tiny. Each `[data-slide-card]` runs from
`x: 100vw, rotation: 40deg, transformOrigin: 100% 100%` to its natural state,
`duration 1`, `stagger {amount: .4}`, ease 14 = `back.out`. The cards deal in
from the **right**, pivoting on their bottom-right corner. Their resting tilt
(-3deg, +5deg) is the reference stylesheet's own, which is why the timeline
animates *to null* and still lands tilted — `REST_ROT` is therefore read off
the elements at runtime rather than hard-coded.

**Preloader into hero** — timeline `t-45657481`, fired by interaction
`i-99a118f3` on `wf:load`, home page only. One 5.55s timeline:

| at | target | move |
|----|--------|------|
| 0.05 | `[data-preloader-logo]` | chars, masked, y −100% → 0, dur 1, stagger .4, back.inOut |
| 1.44 | `.preloader` | y 0% → −120%, dur 1, power2.inOut |
| 1.60 | `.hero_image` | scaleX .3 / scaleY .2 → natural, dur 1.5, power1.inOut |
| 2.57 | `[data-hero-title]` | chars, masked, y −100% → natural, dur 1, stagger .5, back.inOut |
| 3.46 | `[data-hero-subtitle]` | as above |
| 4.06 | `[data-hero-text]` | dur .8, stagger .4, power3.out |
| 4.89 | `.hero_social_links` | opacity 0, y 30 → natural |
| 5.05 | `.hero_stat` | opacity 0, y 30 → natural |

One adaptation: the reference's mark is the word ARIYANA set in type, so it
splits into characters. HelloVoice's is a logo image, so the same move is
applied to the mark as a whole — the stagger is the only part that cannot
carry over.

## Influencer Campaigns (HelloVoice's own page)

`/service/influencer-campaigns/`, built by `build/influencer_page.py` on the
service page's shell so header, footer, preloader, type and spacing are the
template's. Content is `content/influencer.json` — **86 reposts across 46
creators**, captured read-only from `instagram.com/helv.studio/reposts` on
2026-08-17.

Two constraints shape it:

* **No stored posters.** Instagram's CDN URLs are signed and expire within
  days, so a grid of saved thumbnails would be broken inside a week. The tiles
  are typographic — handle, index, play affordance — and never rot.
* **No third-party frame until a click.** Instagram's `/embed/` page loads into
  the existing lightbox on demand. Verified: zero Instagram iframes on load.

The grid ships all 86 tiles but reveals 24 at a time. Copy marked WRITTEN in
`build/influencer_page.py` (the lede and the five campaign stages) is mine and
still needs the client's sign-off.

## Full site audit — 2026-08-18

Eight pages at 1440 / 768 / 500, plus a static scan of the build.

### Method, and what it can and cannot see

Automated overlap detection does not work on this site, and it is worth saying
why rather than reporting its output as fact. The layout genuinely depends on
transforms — the work stack, the year track, the marquees — so:

* forcing every timeline to `progress(1)` parks the year track at x −2716 and
  slides the work cards into their final overlap;
* stripping every transform collapses the stack into a pile.

Both then report "overlap" faults that do not exist. Two passes were spent
chasing them. The audit was narrowed to what holds regardless of animation
state, in the page's natural condition; overlap and stacking are left to visual
review. One earlier finding — the step-card copy apparently covered by its own
icon — was a false positive of the same kind: that copy is clipped to `height:0`
until hover, exactly as the reference does it, but still reports a full
bounding rect.

### Fixed

| Severity | Finding | Fix |
|---|---|---|
| HIGH | **Three of the reference's photographs were still shipping** — `about-text-image.avif`, `service-text-Image.avif`, `hero-image.webp` — pulled in as CSS backgrounds by the reference stylesheet | The two heading "pills" now carry HelloVoice's own work; the VR portrait is cleared site-wide, not just on the home hero |
| HIGH | The service page still played the reference's stock loop in its hero | `.service_video` removed; the page opens on the capability list |
| MED | Newsletter field labelled by placeholder only | `aria-label` added. The earlier fix had silently matched nothing — it expected `type=` before `name=`, and Webflow emits them the other way |
| MED | 404 page had no `<h1>` | Its caption is promoted to `h1`, with a font reset so it is visually identical |
| MED | Select chevron was a reference file | Inlined as a data URI. Needed the reference's own two-class specificity (`.contact_form_input.is-select`) to win |

### Known and deliberately not changed

* **Seven decorative SVG watermarks** from the reference remain on About
  (`about-stats-item-visual-1..4`, `why-choose-image-1..3`). They are abstract
  shapes at 5–10% opacity. Replacing them is a design decision, not a bug fix,
  so they are flagged rather than silently redrawn.
* **`/assets/video/loop-*.mp4`** (the service-card films on the home page) do
  **not** match any reference CDN file byte-for-byte, so they are not the
  reference's footage — but their provenance is unconfirmed and needs the
  client to say where they came from.
* Bebas Neue and DM Sans are the reference's own TTFs, as recorded above.

**The licensing gate was wrong.** `grep data-placeholder` returning zero was
treated as proof nothing borrowed remained. That attribute only ever tagged
assets embedded in HTML — it never saw CSS backgrounds, which is exactly where
the three photographs above were hiding. The check to trust is a rendered one:
load each page and look for `/assets/ref/` in computed styles.

### Clean

Zero horizontal overflow, zero broken images, zero duplicate ids, zero 404s
(every request 200/206/304), zero console errors, no missing alt text, no
unlabelled fields, no undersized tap targets, and no missing local assets —
across all eight pages at all three widths.
