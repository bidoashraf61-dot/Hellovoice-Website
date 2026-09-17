# HelloVoice hero intro film — design

A ~30-second looping film for the home hero, made in Seedance 2.5, replacing the
cursor-tracking character. Ten fast-cut vignettes placing the 3D character inside
ten different sectors of commercial work.

## Why it replaces what is there

The hero currently seeks a 4K render frame-by-frame against cursor position. That
was pushed as far as a clip can go: a pre-rendered film only contains the gaze
directions rendered into it, so it can glance toward a cursor but never track it.
The feature is retired rather than improved further.

## The job

- Runs silent and looping behind the wordmark, intro line and slate.
- Sells range: this company shoots beauty, pharma, automotive, FMCG, industrial,
  events and CGI — evidenced by the real roster in `content/projects.json`.
- Survives being entered at any moment. A viewer arrives mid-loop, reads the type,
  and leaves. Nothing may depend on having seen a beginning.

## Structure

Ten self-contained vignettes of roughly three seconds, in no required order.

Chosen over a compressed single shoot and over an escalating build, both of which
carry an implied beginning that a loop discards. Ten independent beats also mean a
failed generation costs one re-roll rather than breaking a sequence.

## The spine

Rules that make ten separate generations read as one film.

- He is knee-high among adult crew, and **nobody reacts to it**. A surprised
  bystander turns the joke into a cartoon.
- He is **the only stylised thing in frame**. Sets, crew, gear and light are
  photoreal. Drift toward CG environments is a defect, not a style.
- He is always mid-command or mid-act, never watching. Authority is shown by what
  others do in response.
- The **bottom fifth of every frame stays quiet** — no faces, no action. The
  wordmark and slate sit there.
- Identity, unchanged in every beat: scarlet cube head, dark burgundy ribbed
  beanie, black-framed sunglasses, maroon sherpa jacket over a cream hoodie with
  yellow drawstrings, black cargo trousers.

## The beats

Each carries its sector's own visual language; the variety of looks is what sells
"many ads, different styles".

| # | Sector | Style signature | Action |
|---|---|---|---|
| 1 | Beauty | High-key, soft white, glossy skin, 85mm | Two models on a cyc. He is on an apple box with a camera bigger than he is, waving one arm — chin up, more. They adjust. He fires; the flash pops. |
| 2 | Automotive | Hard sun, chrome, low angle, motion blur | A car mid-track on a desert road. He is strapped to the hood rig, jacket flattened by wind, one arm braced on the camera, calm at speed. |
| 3 | Pharma | Clean white, cool daylight, shallow | Lab bench. A clinician frozen mid-pipette. He is on the bench edge framing her with thumb and forefinger, tilts his head, nods once. She resumes. |
| 4 | FMCG | Saturated, hard specular, high-speed | A splash rig. He stands inside the frame beside the product as liquid crowns in slow motion around him, untouched, arms folded, mid-nod. |
| 5 | CGI / anamorphic | Night, LED spill, city ambience | A giant anamorphic billboard at dusk. He is on the roof ledge opposite, arms wide like a conductor; the illusion on the screen moves with his arms. |
| 6 | Events / live | Stage wash, haze, long lens, crowd bokeh | Concert stage from the pit. He is on the barrier rail, back to the crowd, calling a camera move with a raised fist. A real multi-cam crew swings together behind him. |
| 7 | Skincare macro | Black sweep, single hard key, macro | Extreme macro on a serum drop hitting glass. He walks in at the right scale, both hands on the bottle, rotates it a few degrees, nods, walks out. |
| 8 | Corporate | Warm office, soft key, 50mm | An executive mid-interview under lights. He is perched on a C-stand arm, finger raised — hold — the crew still. He drops it; she continues. |
| 9 | Industrial | Steel, cold blue, wide, atmospheric | A factory floor, sparks, operators in PPE. He walks the gantry in a hard hat sized for him, pointing a crane camera down the line. |
| 10 | Wrap / reset | Beat 1's cyc, half-struck | The empty white cyc. He walks away into the light and gives a small backward wave without turning. Cuts to beat 1. |

Beat 10 into beat 1 is the loop point: the same cyc, empty then full, so the join
reads as the next job rather than a rewind.

## Cutting

Fast cutting alone is only fast. These make the cuts appear motivated:

- **Match-on-action** — his hand drops in one beat, the next begins on a matching
  movement.
- **Match-on-shape** — the serum bottle in 7 against the product in 4; the
  billboard in 5 against the monitor wall in 6.
- **Two speed ramps only** — beat 2's road and beat 4's splash. Used twice they
  are punctuation; used throughout they are a screensaver.
- **Uneven rhythm** — beats run roughly 2s / 4s / 2s / 3s. Ten equal cuts read as
  a slideshow.

## Excluded deliberately

- **No real brand names, logos or recognisable packaging.** Placing the character
  inside what reads as a specific client's advertisement implies that client
  endorsed this film. Sectors read clearly without them.
- **No spoken dialogue or on-screen text.** The film runs silent behind type.
- **No story arc.** Anything depending on order is spent on a viewer who will not
  see it.

## Known risks

- **Character identity drift** across ten generations is the main risk: beanie
  shape, jacket colour, head proportion. Every prompt carries the identity block
  verbatim, and drift is grounds to re-roll.
- **Scale reads as error.** A knee-high figure among adults can look like a
  compositing mistake rather than a choice. The fix is that crew must be lit and
  shadowed consistently with him, and must never look at him.
- **Beat 5 is the most likely to fail.** An illusion on a screen responding to his
  arms is the exact thing these models fudge. Fallback: the billboard plays its
  illusion regardless and only he reacts to it.

## Delivery

- 16:9, silent, seamless loop, roughly 30 seconds.
- Encoded as the hero film currently is: retina width, keyframe-dense, faststart.
- The hero layout is unchanged — film leads, type in a band along the foot.
