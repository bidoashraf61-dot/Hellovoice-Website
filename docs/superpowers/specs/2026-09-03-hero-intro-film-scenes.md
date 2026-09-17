# Hero intro film — Phase 1: scene list and frame chain

Planning output only. Generation runs in Higgsfield (Seedance 2.5), not the local
ComfyUI pipeline, so this carries the scene breakdown and the character-anchoring
strategy rather than a Qwen edit chain.

## Deviations from the director default, and why

| Default | Here | Reason |
|---|---|---|
| 2–6 scenes | 10 | The loop sells sector range; fewer reads as a narrow shop. |
| Portrait 832x1472 | Landscape 16:9 | The hero section is 16:9. |
| Scene N end frame = Scene N+1 start frame | Every scene has its own start and end | That rule exists to hide jumps between continuous scenes. This film is deliberately hard-cut between unrelated sets; inheriting frames would fight the design. |
| Qwen edit chain from a hero frame | One reference still, reused as the character reference on every generation | Seedance takes a reference image directly. The anchoring intent is identical. |

## The anchor

Character identity is the single largest risk across ten generations. One canonical
still anchors all of them, supplied as the character reference on every scene.

**Anchor still**: `character/1080-1920/character with camera.png` (1536x2752, full
figure, camera in hand, neutral pose). Already on file.

**Identity block** — carried verbatim in every prompt:

> a stylised three-dimensional matte-vinyl character with an oversized rounded
> scarlet cube head, no nose, small closed mouth, oversized black rectangular
> sunglasses, dark burgundy ribbed knit beanie folded at the brim, deep maroon
> high-pile sherpa fleece jacket worn open, cream white hoodie beneath with
> neon-yellow drawstrings, black cargo trousers, pale cream hands

**Scale block** — also verbatim, because it is the joke and the thing most likely
to drift:

> he is knee-high beside the adults, roughly 60cm tall, and none of the people
> react to him or look at him

## Structure: a day cycle

Prep, then the work, then wrap. An arc has a beginning, which a loop entered at a
random moment normally discards — but prep to work to wrap to prep is a *cycle*,
and a cycle reads correctly from any entry point. A viewer joining at the pharma
beat feels they have joined mid-shift, not that they missed an opening.

Two beats were cut to hold 30 seconds: a corporate interview (visually the dullest
— a talking head under lights) and a skincare macro (it repeated beauty's
territory).

## One rule bends, on purpose

The spine says nobody reacts to him. The closing beat is people crowding to
photograph him, which is a reaction.

That is deliberate. **On set** nobody reacts, because there he is simply the
director and his size is beside the point. **Off** set, at wrap, everyone wants the
photo. The rule holding for nine beats is what makes the tenth land.

## The ten beats

Each carries its sector's own visual language. Start frame, end frame, motion.

### 1 — Prep (3.0s)
- **Start**: Dark stage, a single practical glowing behind. He holds a lens in both hands against a camera body larger than himself.
- **End**: Lens seated, and a large fresnel blazing behind him, throwing his small silhouette long across the floor.
- **Motion**: He twists the lens onto the body; it clicks home; on the click a fresnel kicks on behind him and the stage floods with light.

### 2 — Beauty (3.0s)
- **Start**: White cyc, two models in soft high-key light, him on an apple box holding a camera larger than himself, arm half-raised.
- **End**: Arm fully raised, both chins lifted, strobe mid-pop.
- **Motion**: He raises one arm; both models lift their chins in response; the strobe fires once.

### 3 — Automotive (3.5s)
- **Start**: Low three-quarter on a car mid-track on desert asphalt, him strapped to the hood-mounted rig, jacket beginning to flatten.
- **End**: Car further along, jacket fully flattened, dust trail long behind.
- **Motion**: The car drives toward camera at speed; he braces one arm on the rig, entirely calm; heat shimmer and dust rise behind. **Speed ramp.**

### 4 — Pharma (2.5s)
- **Start**: Clean white lab bench, a clinician holding a pipette mid-air, him on the bench edge framing her with thumb and forefinger.
- **End**: Head tilted mid-nod, her hand lowering toward the tray.
- **Motion**: He tilts his head and nods once; she resumes on the nod.

### 5 — FMCG (3.0s)
- **Start**: Black sweep, a product upright, liquid beginning to crown around its base, him beside it arms folded.
- **End**: Crown at full height around him, droplets suspended, he is untouched, mid-nod.
- **Motion**: Liquid rises in a slow crown around him; he does not flinch; one nod as it peaks. **Speed ramp.**

### 6 — CGI / anamorphic (3.5s)
- **Start**: Dusk rooftop, a vast curved LED billboard opposite showing a dimensional illusion, him on the ledge with arms starting to open.
- **End**: Arms wide, the illusion at full extension, LED spill across the roof.
- **Motion**: He opens both arms like a conductor; the illusion expands in time with them; city light shifts across the roof.

### 7 — Events / live (2.5s)
- **Start**: From the pit, stage wash and haze, crowd bokeh, him on the barrier rail with his back to the crowd, fist starting to rise.
- **End**: Fist at full height, a multi-camera crew behind him swung to a new angle in unison.
- **Motion**: He raises a fist to call a camera move; three operators swing their rigs together; haze drifts through the beams.

### 8 — Influencer (3.5s)
- **Start**: A real creator crouched beside him, both framed in a phone's front camera, him holding a phone nearly his own size at arm's length.
- **End**: Whip to the phone screen: the posted frame, and a like counter running up fast.
- **Motion**: They both look into the phone; he gives a small thumbs-up; whip-pan to the screen where the counter climbs.
- **Constraint**: A generic counter and a generic post frame. **No Instagram or TikTok interface, no platform logos** — a recognisable UI in a company's own film implies a partnership that does not exist.

### 9 — Industrial (2.5s)
- **Start**: Wide factory floor, cold blue steel, sparks at depth, operators in PPE, him on the gantry in a correctly-sized hard hat, arm starting to extend.
- **End**: Arm fully extended down the line, a crane camera swung to follow it.
- **Motion**: He points down the production line; a crane camera swings to follow; sparks fall behind.

### 10 — Fans / wrap (3.0s)
- **Start**: The stage of beat 1, now half-struck and warm-lit. Real crew and visitors begin crouching down around him.
- **End**: Six people crouched low in a loose arc around a knee-high figure, phones up, him mid-thumbs-up, flashes firing.
- **Motion**: People crouch to get down to his height, phones raised; he holds a thumbs-up; several flashes fire. Cuts to beat 1.

## The loop

Beat 10 (wrap, warm light, people leaving) cuts to beat 1 (the same stage, dark
again, lens going on). It reads as the next morning. Beats 1 and 10 share a set
and nothing else does, which is what makes the join legible as a day rather than
a rewind.

## Cut plan — 30.0s total

| # | Beat | Length | Into the next |
|---|---|---|---|
| 1 | Prep | 3.0s | Hard cut on the lens click and the light kicking on |
| 2 | Beauty | 3.0s | Match-on-action: his rising arm into the rising hood rig |
| 3 | Automotive | 3.5s | Hard cut at the speed-ramp peak |
| 4 | Pharma | 2.5s | Match-on-shape: pipette into the falling liquid |
| 5 | FMCG | 3.0s | Hard cut at the crown's peak |
| 6 | CGI | 3.5s | Match-on-shape: LED wall into the stage wash |
| 7 | Events | 2.5s | Hard cut on the fist |
| 8 | Influencer | 3.5s | Match-on-shape: phone screen into the factory monitor |
| 9 | Industrial | 2.5s | Match-on-action: his point into the crowd crouching |
| 10 | Fans | 3.0s | Loop cut back to 1 |

Two speed ramps only, in beats 3 and 5. Used twice they are punctuation; used
throughout they are a screensaver.

## Frame-safe zone

The bottom fifth of every frame stays free of faces and action — that band carries
the wordmark, intro line and slate. Every prompt states it.

## Next

Step 3: each beat through the higgsfield skill for a model-specific Seedance 2.5
prompt carrying the identity block, the scale block, the safe-zone constraint, and
the per-sector visual language.
