# Reference teardown — Ariyana Studio

Source: `https://ariyana-studio.webflow.io`, captured to `scratchpad/ariyana/` (`index.html` 106 KB,
`main.css` 162 KB). This is the structural contract the HelloVoice build clones.

---

## System

| | Reference | HelloVoice |
|---|---|---|
| Container | `1680px` | same |
| Display face | Bebas Neue | same |
| Body face | DM Sans | same |
| H1 | `19vw` | same |
| H2 | `clamp(3.75rem, -0.19rem + 16.83vw, 20rem)` | same |
| H3 | `clamp(2.75rem, 1.48rem + 5.44vw, 8rem)` | same |
| Year text | `clamp(5rem, 1.36rem + 15.53vw, 20rem)` | same |
| Footer logo | `24vw` → `28vw` | same |
| Radii | sm 12/16/20 · md 16/20/30 · lg 16/20/24/40 · xl 32/40/60/100 · pill 999 | same |
| Motion | GSAP 3.15 + ScrollTrigger + SplitText + Lenis 1.3.4 | same |
| Palette | near-monochrome — `#fff` `#000` `#222` `#333` `#ddd` `#fafafa` | mapped to HelloVoice tokens |

The reference is deliberately colourless; its accent is *scale*, not hue. HelloVoice keeps the
structure and substitutes the Oxblood Editorial palette, with red reserved as the single accent
and lime for live states only.

---

## Section order — ten blocks, fixed

| # | Reference class | Reference content | HelloVoice content |
|---|---|---|---|
| 1 | `hero_section` | H1 wordmark, subtitle, info, social + stat, full-bleed `hero_image` | H1 `HELLOVOICE`, positioning line, **character slot replaces `hero_image`** |
| 2 | `about_section` | caption, big statement, button, then 300vh pinned year track 2020–2025 | studio statement + HelloVoice milestone years |
| 3 | `step_section` | `ASSESS, DEPLOY, AND OPERATE` + 4 numbered steps | the production process, 4 steps |
| 4 | `work_section` | `FEATURED WORKS`, 300vh track, 4 stacked project items | 4 featured films from `content.json` |
| 5 | `service_section` | `Expert SOLUTIONS`, service items with tag lists + looping video | HelloVoice services with tag lists |
| 6 | `showreel_section` | 250vh pinned track, video mask scales up, `Play` / `Reel` split heading | the Vimeo showreel |
| 7 | `leader_section` | `Trusted by Leaders`, badge, 10 orbiting client circles | client logos on file |
| 8 | `testimonial_section` | `Clients Feedback`, 4 alternating cards | captured testimonials |
| 9 | `cta_section` | 2 marquee rows — one solid, one stroked — plus pill button | same |
| 10 | `footer` | 4 link columns, newsletter form, giant `logo_big_text` | same |

Plus a `brands_section` grid between work and services, a `preloader`, and a `canvas_menu`
fullscreen overlay.

---

## The mechanics that carry the design

**Pinned scroll tracks.** Three sections are tall parents with a `position: sticky; top: 0;
height: 100vh` child. Scroll distance inside the parent drives a GSAP timeline.

| Track | Height | What moves |
|---|---|---|
| `about_track` | `300vh` | years translate horizontally across the pinned viewport |
| `work_items_track` | `300vh` | project items stack and swap |
| `showreel_track` | `250vh` | the video mask scales from a small rounded rect to full bleed |

**Duplicated text nodes.** Nav links, buttons and step titles each render their label twice
(`nav_link_text` + `nav_link_text._2`, `button_text` + `button_text.second_text`,
`step_title` + `step_title.is_gradiant`). The second copy is offset and revealed on hover — a
vertical text swap. Every interactive label in the build follows this pattern.

**Masked line buttons.** `button_primary` carries three stacked `button_line_mask` elements that
sweep on hover behind the label.

**Floating text.** Small rotated labels (`floating_text.is-about`, `.is-work`, `.is_service`)
sit beside section titles as a secondary annotation layer.

**Marquee.** `cta_ticker_row` duplicates its `h2` and translates continuously; the second row
uses `is_stroke` — transparent fill with a text outline.

**Hero image is a full-bleed absolute layer.** `.hero_image { position: absolute; inset: 0 }`
sitting behind the hero content. This is where the HelloVoice character video mounts, which is
why the clone needs no structural change to accommodate it.

---

## Deliberate divergences

Recorded here so the audit can distinguish a defect from a decision.

| Divergence | Reason |
|---|---|
| Palette is HelloVoice, not monochrome | The brief pins the structure, not the colour. Oxblood Editorial is the committed identity. |
| No Webflow runtime, jQuery, or CMS | Static build. Behaviour is hand-written against the same GSAP/Lenis stack. |
| Blog and utility pages dropped | Not in the agreed page set. |
| Work section carries 42 films, not 4 | Real inventory from `capture/content.json`. |
| Vimeo facade instead of background video | Films must open in the real Vimeo player, per the brief. |
