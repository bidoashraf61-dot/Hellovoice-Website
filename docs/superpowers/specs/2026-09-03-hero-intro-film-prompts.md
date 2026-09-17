# Hero intro film — Step 3: Seedance 2.5 generation prompts

Ten prompts, one per beat. Paste each into Higgsfield with the anchor still
attached as the single image reference.

## Verified parameters

Read from `specs/model-specs.yaml`, snapshot 2026-08-07 (27 days old, inside the
30-day freshness window).

| Setting | Value | Note |
|---|---|---|
| Model | `seedance_2_5` | |
| Mode | `omni_reference` | one image reference is supplied per generation |
| Aspect ratio | `16:9` | in the model's enum |
| Duration | **4s** | 4 is the floor — see below |
| Resolution | **720p** | 720p is the ceiling on 2.5 — see below |
| `generate_audio` | `false` | the film is silent under the wordmark |
| `extension_mode` | not set | only allowed on `video_extension` |

## Two constraints the plan collides with

**1. The duration floor is 4 seconds.** Seven of the ten beats are planned
shorter (2.5s and 3.0s). Seedance 2.5 cannot render below 4s. Render every beat
at 4s and trim to the planned length in the edit — the extra second is a handle,
which the match-cuts in beats 2, 4, 6, 8 and 9 need anyway.

**2. Seedance 2.5 has no lane above 720p.** The hero currently ships 4K. Two
routes, both verified in the catalog:

- **Seedance 2.0** (`mode=std`) does native **4K**, 16:9, duration 4–15s. Every
  beat here is 4s, so 2.0 renders each one at 4K natively. It has no 30-second
  lane, but this film is never generated as one 30-second take.
- **Topaz** (`topaz_video`) upscales to 1080p or 2160p after the fact.

Seedance 2.0 is the better route for this job and the prompt bodies below carry
over unchanged — only the parameter header differs (`mode: std`,
`resolution: 4k`, no `mode: omni_reference`; the anchor attaches under
`image_references` there too). The prompts are written for 2.5 as asked; fire
them on 2.0 if the 4K matters more than the 2.5 dialect.

## The anchor

`character/1080-1920/character with camera.png` attaches as `@Image1` on all ten.

Per the reference-role law, the prompt does **not** re-describe what the image
already carries — long appearance text fights the reference and degrades it.
What stays in words is only what the image cannot carry: the colours the model
drops, the scale relationship (the anchor has no human beside him), and the
locks.

## Shot grammar across the ten

Every cut changes both shot size and camera character, and the loop closes
correctly from 10 back to 1.

| # | Beat | Size | FOV | Camera character | Kelvin |
|---|---|---|---|---|---|
| 1 | Prep | MCU | 29° | static locked-off | 3200K → 5600K |
| 2 | Beauty | wide | 84° | stabilized push in | 5600K |
| 3 | Automotive | medium | 47° | stabilized tracking | 4000K |
| 4 | Pharma | close-up | 18° | static locked-off | 5600K |
| 5 | FMCG | MCU | 29° | slow orbit | 5600K |
| 6 | CGI | extreme wide | 107° | crane up | 8500K |
| 7 | Events | medium | 47° | handheld | 5600K |
| 8 | Influencer | close-up | 18° | static, then whip | 5600K |
| 9 | Industrial | wide | 84° | jib | 4000K |
| 10 | Fans | medium wide | 63° | handheld | 3200K |

Beats 3 and 5 render entirely in slow motion — one speed start to finish — and
are ramped in the edit. Mixing speed modes inside one generation breaks.

---

## SHOT 1 — PREP

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: The opening shot of a silent title film — the director figure builds his camera on a dark stage and the lights hit.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a blacked-out sound stage at night. An empty deck, flight cases at the edge of the light, cable runs underfoot. A camera body sits on a low stand taller than he is.

CAMERA: Locked-off static, 29° FOV, medium close-up at his height, ending on his long lit silhouette across the deck. One continuous shot; the camera does not cut on its own.

ACTION: The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, turns a lens onto the mount with both hands. The lens seats, and on the seat a fresnel kicks on behind him and floods the deck.

LIGHTING: One warm 3200K practical burning behind him, then a hard 5600K fresnel. Deep contrast, cool sheen on the deck.

POSITIVE LOCKS: He is 110 cm tall, waist-high to an adult; the camera stand is taller than he is. He holds that scale throughout, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. Bottom fifth of frame: deck only, faces and action above it. No on-screen text, no branding.
```

---

## SHOT 2 — BEAUTY

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A beauty-campaign shot — the director figure calls a pose on a studio cyc and the strobe answers.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a photographic studio, daytime. A white cyclorama, seamless floor, a low wooden riser in the light.

CAMERA: Stabilized slow push in, 84° FOV, wide, ending with the three of them centred and the strobe bloom clearing. One continuous shot; the camera does not cut on its own.

ACTION: Two models in editorial makeup stand in the light. The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, stands on the riser holding a full-size cinema camera. He raises one arm; both models lift their chins on the movement; a strobe pops once and the frame blooms white.

LIGHTING: Soft even 5600K beauty light, high-key, pale even complexions, faint warm bounce off the floor, no shadow on the wall.

POSITIVE LOCKS: He is 110 cm tall, the models 165–180 cm; his head reaches their waists in every frame, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses; neither model looks at him. Distinct body separation between all three. Bottom fifth of frame: cyc floor only, faces and action above it. No on-screen text, no branding.
```

---

## SHOT 3 — AUTOMOTIVE

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: An automotive shot — the director figure rides the hood rig on a moving car and does not blink.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Exterior, a desert highway at low sun. Open asphalt, dust on the shoulder, heat shimmer at 30 metres. A matte dark sedan with no badges carries a hood-mounted camera rig.

CAMERA: Stabilized tracking alongside at low three-quarter, 47° FOV, medium, ending with the car filling the right two thirds and the dust trail still lengthening. One continuous shot; the camera does not cut on its own.

ACTION: The sedan tracks toward camera at 60 km/h. The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, is strapped to the rig, one arm braced, body steady, as the pile of his jacket flattens in the airflow and a dust trail lengthens behind. The whole shot renders in slow motion, one speed start to finish.

LIGHTING: Hard 4000K low sun, long shadows, amber dust, deep blue shade under the car.

POSITIVE LOCKS: He is 110 cm tall and reads waist-high against the car's bodywork, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. Bottom fifth of frame: asphalt only, faces and action above it. No on-screen text, no badges, no branding.
```

---

## SHOT 4 — PHARMA

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A pharmaceutical shot — the director figure gives a clinician her cue from the bench edge.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a hospital laboratory, daytime. A clean white bench, sterile stainless and matte white surfaces, a sample tray and a rack of tubes.

CAMERA: Locked-off static on the bench line, 18° FOV, close-up, ending with her hand settled at the tray and his framing hands still up. One continuous shot; the camera does not cut on its own.

ACTION: A clinician in a lab coat holds a pipette above the tray, hand paused. The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, sits on the bench edge and frames her with thumb and forefinger. He tilts his head and nods once; on the nod her hand lowers and she resumes the transfer.

LIGHTING: Soft 5600K top light, clinical and even. Subject in sharp focus, background falling into soft bokeh.

POSITIVE LOCKS: He is 110 cm tall, the clinician 165–180 cm; his head reaches her waist when they are both standing, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses; she does not look at him. Distinct body separation between them. Bottom fifth of frame: bench surface only, faces and action above it. No on-screen text, no labels, no branding.
```

---

## SHOT 5 — FMCG

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A packaged-goods shot — a liquid crown rises around the director figure and he holds his ground.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a product studio. A matte black sweep, non-reflective ground, an unbranded matte hero bottle standing upright, chest-high to him.

CAMERA: Slow orbit around the bottle, 29° FOV, medium close-up, ending with the crown at full height and him inside it, untouched. One continuous shot; the camera does not cut on its own.

ACTION: The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, stands beside the bottle with arms folded. Liquid rises around them both in a slow crown, droplets climbing and hanging at the crown's lip; he holds his stance and nods once as the crown reaches full height. The whole shot renders in slow motion, one speed start to finish.

LIGHTING: One cool 5600K key from the left, a hard rim along the liquid edge, specular highlights on the droplets.

POSITIVE LOCKS: He is 110 cm tall, waist-high to an adult, and the hero bottle stands chest-high to him. He holds that scale throughout, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. Bottom fifth of frame: black sweep only, faces and action above it. No on-screen text, no labels, no branding.
```

---

## SHOT 6 — CGI BILLBOARD

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A CGI shot — the director figure conducts a dimensional illusion on a billboard across the street.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Exterior, a city rooftop at dusk. Gravel roof, a parapet ledge, and a vast curved LED billboard on the opposite building carrying an abstract illusion of folding geometry. Haze visible at 40 metres.

CAMERA: Slow crane up, 107° FOV, extreme wide, ending with the billboard filling the upper half and him small and readable on the ledge below it. One continuous shot; the camera does not cut on its own.

ACTION: The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, stands on the parapet ledge in the lower left third. He opens both arms like a conductor; the folding geometry expands outward in time with them; coloured spill spreads across the gravel toward camera.

LIGHTING: 8500K dusk ambient with magenta and cyan spill from the billboard washing the roof gravel.

POSITIVE LOCKS: He is 110 cm tall and stays a readable waist-high figure on the ledge, never enlarged toward adult height and never lost as a distant dot. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. The billboard carries geometry only. Bottom fifth of frame: roof gravel only, faces and action above it. No on-screen text, no logos, no branding.
```

---

## SHOT 7 — EVENTS

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A live-events shot — the director figure calls a camera move from the barrier and the crew answers together.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a concert arena at night, shot from the photo pit. A barrier rail, a working deck behind it, and a crowd beyond reading as one dark mass. Haze density 60%.

CAMERA: Handheld from the pit, low angle, 47° FOV, medium, ending with the fist at full height and the three rigs settled on the new angle. One continuous shot; the camera does not cut on its own.

ACTION: The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, stands on the barrier rail with his back to the crowd. Three camera operators work the deck behind him. He raises a fist to call the move; all three swing their rigs to a new angle together; haze drifts through the beams.

LIGHTING: Saturated magenta and white 5600K stage beams through the haze. Subject in sharp focus, the crowd falling into soft bokeh.

POSITIVE LOCKS: He is 110 cm tall, the operators 165–180 cm; standing on the rail he reads waist-high beside them, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses; no operator looks at him. The crowd reads as one mass with collective motion, never individuals. Bottom fifth of frame: barrier and deck only, faces and action above it. No on-screen text, no branding.
```

---

## SHOT 8 — INFLUENCER

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: A creator shot — the director figure poses for a selfie and the camera whips to the phone.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a plain room, daytime. Clean white walls, a window out of frame, an uncarpeted floor.

CAMERA: Static, 18° FOV, close-up, then a 0.8-second whip-pan, ending settled and square on the phone screen. One continuous shot — the whip-pan is a camera move, not a cut; the camera does not cut on its own.

ACTION: A content creator crouches down beside the orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, who holds a phone up at arm's length. Both face the phone; he gives a small thumbs-up; the camera whips to the screen over 0.8 seconds of blur travel and settles on a plain photo frame with a small row of blank icons beneath it.

LIGHTING: Soft 5600K window light, warm neutral complexions. Subject in sharp focus, background falling into soft bokeh.

POSITIVE LOCKS: He is 110 cm tall, the creator 165–180 cm and crouched to his level; he holds that scale, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. Distinct body separation between them. The screen carries a photo and blank icons only. Bottom fifth of frame: floor only, faces and action above it. No on-screen text, no numerals, no app interface, no logos, no branding.
```

---

## SHOT 9 — INDUSTRIAL

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: An industrial shot — the director figure points down a production line and a crane camera follows him.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, a factory floor, daytime. Cold blue steel, a running line below, operators in protective gear, sparks falling at depth, a gantry rail above.

CAMERA: Slow jib move following his arm, 84° FOV, wide, ending with the crane camera settled on the far end of the line and him small and readable on the gantry. One continuous shot; the camera does not cut on its own.

ACTION: The orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses, stands at the gantry rail in a hard hat sized to him. He extends one arm and points down the line; a crane-mounted camera swings across to follow the point; sparks keep falling behind.

LIGHTING: 4000K overhead work lights with an 8500K cold fill, orange spark accents. Sharp focus throughout, deep depth of field.

POSITIVE LOCKS: He is 110 cm tall, the operators 165–180 cm; he stays a readable waist-high figure, never enlarged toward adult height and never lost as a distant dot. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses; no operator looks at him. Bottom fifth of frame: factory floor only, faces and action above it. No on-screen text, no signage, no branding.
```

---

## SHOT 10 — FANS (loop tail)

**Model:** Seedance 2.5 · **Mode:** omni_reference · **Aspect ratio:** 16:9 · **Duration:** 4s · **Resolution:** 720p · **Audio:** off

```
SCENE CONTEXT: The wrap shot that loops back to the opening — the crew crouch down to photograph the director figure.

ACTIVE REFERENCES:
@director: the character, exactly as in the element — speech-bubble head shape and gradient, clear-lensed glasses, proportions, materials, clothing, white sneakers with neon-yellow laces. Do not take the element's backdrop, its film set, its crew, its pose or its camera.

LOCATION MAP: Interior, the same sound stage as the opening, night, half-struck. Flight cases open, dust in the air, deep shadow at the stage edges.

CAMERA: Handheld at his height, 63° FOV, medium wide, ending with the arc closed around him and the last flash clearing. One continuous shot; the camera does not cut on its own.

ACTION: A loose arc of crew and visitors crouches down together as one group to reach the height of the orange-red speech-bubble-headed figure in the maroon sherpa fleece and burgundy beanie, brown eyes visible behind thick brown-rimmed clear-lensed glasses. Phones come up around him; he holds a thumbs-up; several phone flashes pop in quick succession across the arc.

LIGHTING: Warm 3200K work lights, dust catching the beams, deep shadow beyond.

POSITIVE LOCKS: He is 110 cm tall and the crouched adults come down to roughly his height; he holds that scale, never enlarged toward adult height. A moulded vinyl figure, not a person. His brown eyes stay visible and alive behind clear lenses, never hidden by dark or opaque lenses. The group reads as one mass with collective motion, never tracked individuals. Distinct body separation between the crouched figures. Bottom fifth of frame: deck only, faces and action above it. No on-screen text, no branding.
```

---

## Notes carried into the edit

**The like counter is not generated.** Glyph fidelity is unreliable and
re-rolls every generation, so shot 8 renders a clean screen with blank icons
and no numerals. The counter is a post overlay, which also keeps it on-brand
and legible at hero scale.

**Trim from 4s.** Planned lengths: 3.0 / 3.0 / 3.5 / 2.5 / 3.0 / 3.5 / 2.5 /
3.5 / 2.5 / 3.0 = 30.0s. Each render gives 4s; trim to the plan, keeping the
handles at the ends the match-cuts need.

**Speed ramps.** Beats 3 and 5 arrive as full slow-motion clips. Ramp them in
the edit — the model renders clean physics in slow motion and breaks when asked
to change speed mid-shot.

**If a beat fails instantly (under 10 seconds)**, that is the content filter,
not the GPU. Do not regenerate unchanged. The likeliest trigger here is the
scale language reading as a person of small stature; the mitigation already in
every prompt is "a moulded vinyl figure, not a person" — strengthen it before
re-firing rather than changing a word elsewhere.

**Batch, don't iterate, on identity misses.** If the character comes back wrong
in varied ways across rolls, that is variance — roll the same locked prompt
again and cull. Only iterate the prompt if he fails the *same* way every time.
