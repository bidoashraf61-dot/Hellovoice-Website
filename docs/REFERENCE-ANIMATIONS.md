# Reference animations — Ariyana Studio

Every value below was read off the live site, not estimated. Two sources:

**IX2** — the older Webflow interaction engine, which drives all the hovers and
the showreel. Read directly from its config:

```js
const d = Webflow.require('ix2').store.getState().ixData;
d.actionLists[id].actionItemGroups[].actionItems[]              // hover
d.actionLists[id].continuousParameterGroups[]
  .continuousActionGroups[].actionItems[]                       // scroll
```

**IX3** — Webflow's newer GSAP-backed scroll animations. These are *not*
introspectable: the timelines are rebuilt per frame and `getChildren()` comes
back empty. They were characterised instead by sampling computed transforms
against scroll progress at 1/16 resolution.

The element list is not guesswork either. The reference's own stylesheet holds
a pre-paint hide rule that enumerates every animated hook:

```css
html.w-mod-js:not(.w-mod-ix3) :is([data-button-text], [data-stroke="no"],
  [data-stroke="yes"], [data-slide-card], .canvas_menu_active_bg,
  [data-menu-text]:nth-of-type(1), [data-menu-text]:nth-of-type(2),
  .canvas_menu, .brands_ticker_row, [data-title-anim], [data-floating-badge],
  [data-text-anim], [data-work-item]:nth-child(2), [data-work-item]:nth-child(3),
  [data-work-item]:nth-child(4), .year_wrapper, [data-text-reveal],
  [data-preloader-logo], .preloader, .hero_image, [data-hero-title],
  [data-hero-subtitle], [data-hero-text], .hero_social_links, .hero_stat,
  .step_item_info_wrap) { visibility: hidden !important; }
```

The build reproduces both halves: `w-mod-js` is stamped on `<html>` at build
time, and `assets/js/motion.js` adds `w-mod-ix3` once initial states are set,
with a 2s failsafe so a script error can never strand the page.

---

## Breakpoints

IX2 registers each event against Webflow's own media queries. Anything marked
**main only** must not run below 992px — the stylesheet lays those elements out
differently there, and applying the desktop initial state breaks the mobile
layout. In the build these sit inside `gsap.matchMedia()` with cleanup.

| key | range |
|---|---|
| `main` | ≥ 992px |
| `medium` | 768–991px |
| `small` | 480–767px |
| `tiny` | ≤ 479px |

---

## Scroll tracks

### The year track — `.about_track` → `.year_wrapper`

ScrollTrigger read live off the reference: `start: clamp(top top)`,
`end: clamp(bottom 130%)`, `scrub: 0.8`. Measured at 1440×900, the wrapper's
`x` runs **+640 → −2716**, dead linear:

| progress | 0 | .125 | .25 | .375 | .5 | .625 | .75 | .875 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| x | 640 | 220 | −199 | −619 | −1038 | −1458 | −1877 | −2297 | −2716 |

Written against the viewport so it holds at any width: opens with the first
year at `44.44vw`, closes with the last year's right edge at `80.83vw`.

### The work stack — `.work_items_track` → `[data-work-item]` ×4

`start: clamp(top top)`, `end: clamp(bottom bottom)`, `scrub: 0.8`, under the
`perspective: 1500px` the stylesheet puts on `.work_items_wrapper`.

Resting state: `y = 40i`, `scale = 1 − 0.06i`.

The timeline holds for **1/16**, then runs **three equal linear steps of 5/16**.
Sampled at 1/16 the steps land on 0.0625 → 0.375 → 0.6875 → 1.0. Per step:

| target | from | to |
|---|---|---|
| the front card | `rotateX 0`, `y 0` | `rotateX 45deg`, `y −792px` |
| the next card | its resting slot | `y 0`, `scale 1` |
| every card behind | — | `y −= 20`, `scale += 0.06` |

Ease is `none` throughout. Verified against the live values at p = 0.5:
reference `45/−792, 18/−316.8, 0.964/36, 0.904/92`; build
`45/−792, 17.4/−307, 0.963/37, 0.903/92`.

### The showreel — `.showreel_track` (IX2 `a-17`, main only)

`SCROLL_PROGRESS`, which Webflow measures across the element's **whole
traversal** — 0% when its top is at the viewport bottom, 100% when its bottom
is at the viewport top — not across the pinned range. Confirmed: the mask
starts growing at scroll 12643 and finishes at 13519, which is exactly 32% and
60% of that traversal.

| keyframe | `.showreel_video_mask` | `.showreel_text` |
|---|---|---|
| 32% | `50vw × 40vh`, radius `40px` | `x 0`, `y −50%`, opacity 0 |
| 42% | — | opacity 1 |
| 60% | `100vw × 100vh`, radius `0` | `._1 x +34vw`, `._2 x −34vw` |

The split distance is a breakpoint value (34vw at main, then 25 / 22 / 15), so
the build reads it off the computed transform rather than hard-coding it.

Measured against the build:

| scroll | reference | build |
|---|---|---|
| 12300 | 720×360 r40 x0 op0 | 720×360 r40 x0 op0 |
| 12800 | 849×457 r32.8 x87.9 op0.50 | 854×460 r33 x91.0 op0.52 |
| 13000 | 1015×581 r23.6 x200.7 op1 | 1017×583 r23 x202.1 op1 |
| 13400 | 1342×826 r5.4 x422.9 op1 | 1344×828 r5 x424.1 op1 |
| 13700 | 1440×900 r0 x489.6 op1 | 1440×900 r0 x489.6 op1 |

### The logo fan — `.leader_section` (IX2 `a-3`)

`SCROLL_PROGRESS` 0 → 100 rotates `.leader_circle_wrapper` **0 → 360deg**,
linear, across the same full-traversal mapping. Verified: at scroll 15400 the
build reports −116.5deg, i.e. 243.5deg — the reference's exact value.

---

## Entrances

### The text grammar — measured, not estimated

`[data-title-anim]` and `[data-text-anim]` share one grammar. The reference
splits each element into **words *and* characters** and animates the
**characters**, dropping them in from exactly one line-height above. No fade —
opacity stays 1 throughout — and **no clipping mask**: the split wrappers
compute `overflow: visible`, so characters visibly cross the line above on the
way down.

The node counts give the split away: 28 for the four-word heading
`ASSESS, DEPLOY, AND OPERATE` (4 words + 24 characters), 53 for the eleven-word
paragraph beneath it.

Sampled at 70ms across the trigger crossing, from a cold load, first three
characters — reference against build:

| t | reference | build |
|---|---|---|
| 0ms | −69 −68 −68 | −69 −68 −68 |
| 140ms | −71 −71 −71 | −70 −70 −70 |
| 280ms | −63 −66 −67 | −60 −62 −65 |
| 420ms | −29 −36 −42 | −29 −36 −42 |
| 560ms | −3 −6 −9 | −3 −5 −7 |
| 700ms | +3 +3 +3 | +2 +2 +2 |
| 910ms | 0 0 0 | 0 0 0 |

The dip to −71 before travelling, and the +3 overshoot after, are symmetric at
±4.4% of the 68px line — a `back.inOut`. Adjacent characters lag ~7px
mid-flight, which is a ~0.02s stagger. Settled by 910ms.

The paragraph runs the same drop with no overshoot: −28 → 0 by ~630ms, fitting
`power2.out` over ~0.53s with a tighter stagger.

| element | from | duration | ease | stagger |
|---|---|---|---|---|
| `[data-title-anim]` chars | `yPercent: -100` | 0.97 | `back.inOut(1.4)` | 0.022 |
| `[data-text-anim]` chars | `yPercent: -100` | 0.55 | `power2.out` | 0.008 |

### Everything else

| hook | what | trigger |
|---|---|---|
| `[data-hero-title]` | same character drop, wider stagger | on load |
| `[data-hero-subtitle]`, `[data-hero-text]`, `.hero_social_links`, `.hero_stat` | rise + fade | on load, staggered |
| `[data-hero-image]` | scale 1.12 → 1, fade in | on load |
| `[data-text-reveal]` | **word opacity scrub**, stagger 0.4, `scrub: 1.2`, `start: clamp(top bottom)`, `end: clamp(bottom center)` | scroll |
| `[data-floating-badge]` | scale 0.6 → 1, `outBack` | scroll |
| `[data-counter]` | column rolls up, 1900ms, `cubic-bezier(.784,.325,.222,.98)` (IX2 `a-32`) | scroll |
| `[data-slide-card]` | the pile drops in, staggered | scroll |
| `.leader_circle_item` | each swings to `−36deg × index`, 1000ms `inOutCubic` (IX2 `a-7`) | scroll into view |

`[data-text-reveal]` is the only scrubbed entrance; everything else fires once.
The reference's ScrollTriggers confirm the split: eight non-scrub triggers on
the home page at `clamp(top 90%)`, one scrubbed at 1.2 on the statement.

To re-measure any of these: hard-reload with a cache-busting query, park the
scroll just short of the element's `clamp(top 90%)` crossing, then sample
transforms at 70ms while crossing it. They are `once: true`, so a warm page
will show you nothing.

---

## Marquees

Measured by sampling `x` over 2s on the live site.

| row | speed | loop distance |
|---|---|---|
| `[data-stroke="no"]` (solid) | **−180.1 px/s** | one headline copy |
| `[data-stroke="yes"]` (outlined) | **+180.1 px/s** | one headline copy |
| `.brands_ticker_row` | **+81.7 px/s** | one full row (818px) |

The brands ticker repeats at *row* level: two identical `.brands_ticker_row`
siblings sit end to end in a clipped box and carry the same `x`, so one row's
width is the loop distance — not half its children. Build measures +81.5 px/s.

---

## Hovers

All values from IX2. **main only** unless noted.

| # | target | over | out |
|---|---|---|---|
| `a`/`a-2` | `.brands_grid .box` | background → `rgba(255,255,255,.8)`, 500ms | → black, 500ms |
| `a-20`/`a-21` | `.step_icon` | scale 1.05, 500ms `ease`; the info panel opens from `height: 0` | scale 1, 500ms |
| `a-9`…`a-16` | `.testimonial_card` ×4 | scale 1.1, rotate 0, 800ms `outBack`; neighbours shoulder aside | scale 1 / rest rotate, 600ms |
| `a-73`…`a-80` | `.life_image_item` ×4 | same pile, about page | same |
| `a-5`/`a-6` | `.leader_section_content` | opacity .5 → 1; fan scales to 0.8, 500ms `inOutQuart` | reverse |
| `a-34`/`a-35` | `.button_primary`, `.cta_button` | ground → black 350ms `ease`; `.button_line` → white, `scaleX 1.3` 500ms `inOutCubic` | **delay 500ms**, then reverse |
| `a-22`/`a-23` | `.hero_social_icon_link` | scale 0.9, 350ms `ease` (all breakpoints) | scale 1, 350ms |
| `a-71`/`a-72` | `.project_item` → `.image-cover` | scale 1.15, 500ms `outQuad` (all breakpoints) | scale 1, 350ms `outQuad` |
| `a-36`/`a-37` | `.award_item` | ground wipes up `scaleY 0→1`, 750ms `outCubic`; text inverts 250ms | 600ms |
| `a-27`/`a-28` | burger | crosses to an X, 300ms `outSine`, ±8px / ±45deg | 300ms |

The testimonial pile's neighbour offsets, in px, indexed `[hovered][other]`:

```
[ —,   7,   5,   5]
[-10,  —,   8,   8]
[-15, -8,   —,  10]
[-10, -8, -10,   —]
```

Resting rotations alternate `−3deg, +5deg, −3deg, −3deg`. Below 992px the
stylesheet flattens the pile (`transform: none`), so these are desktop-only.

## Webflow easings → GSAP

| Webflow | GSAP |
|---|---|
| *(blank)* | `none` |
| `ease` | `power1.inOut` |
| `outSine` / `outQuad` / `outCubic` / `outQuart` | `sine.out` / `power1.out` / `power2.out` / `power3.out` |
| `outBack` | `back.out(1.7)` |
| `inOutCubic` / `inOutQuart` | `power2.inOut` / `power3.inOut` |
