# Character gaze + expression sheet — generation prompts

Source character: `User Assets/Char PNG copy.tiff` (also `Char PNG.webp`, 4800×6424).

## What to generate, and why

For a cursor-driven character the browser swaps between **discrete stills**. It does
not play a video. So the asset is a **locked-off grid**: same camera, same light,
same body, same scale — only the head, eyes and mouth change between cells.

That constraint is the whole job. If framing, lighting or body position drifts even
slightly between cells, the swap reads as a jump cut rather than the character
looking at you. Every prompt below therefore says "locked off", "identical", and
"only the head moves" explicitly — that is not padding, it is the requirement.

**Background:** flat chroma. His palette is red, maroon, cream and black, so a blue
screen shares no hue with him and cuts cleanly. Use a single flat value, unlit and
even — a gradient or a lit backdrop makes the matte inconsistent cell to cell.

---

## Prompt 1 — the 3×3 gaze grid (the one you need first)

> Reference sheet of the same 3D character in a 3×3 grid, nine cells, identical in
> every cell except the direction of his gaze. The character: a stylised Pixar-style
> young man with a smooth matte-red rounded head, oversized black rectangular
> sunglasses, a dark maroon knitted beanie, a maroon sherpa fleece jacket over a
> cream hoodie with yellow drawstrings, black cargo trousers, holding a black cinema
> camera in his right hand. Framed from the waist up, centred, filling the same area
> of every cell at exactly the same scale.
>
> The camera is locked off — a static three-quarter front view at eye level, 50mm
> equivalent, no perspective change, no dolly, no zoom between cells. The body,
> shoulders, arms, jacket folds and camera in hand are identical in all nine cells.
> Only the head rotation and eye direction change.
>
> Cell order, left to right, top to bottom: up-left, up-centre, up-right;
> centre-left, straight at the viewer, centre-right; down-left, down-centre,
> down-right. Head turn is subtle — no more than 25 degrees from centre — with the
> eyes leading the movement further than the head.
>
> Lighting: flat, even, soft frontal key with a gentle top fill, no hard shadows on
> the face, no rim light, identical intensity and direction in every cell. Palette:
> maroon, cream and matte red against a flat chroma-blue background, pure and unlit
> and completely even.
>
> Clean studio product-shot mood, neutral and friendly. No cast shadow on the
> backdrop, no floor, no props, no set, no logos, no watermarks, no on-screen text,
> no labels, no grid lines or borders between cells, no colour variation in the
> background, no motion blur, no depth of field.

---

## Prompt 2 — the expression row (run after the gaze grid is approved)

> Reference sheet of the same 3D character in a single horizontal row of five cells,
> identical in every cell except his facial expression. The character: stylised
> Pixar-style young man, smooth matte-red rounded head, oversized black rectangular
> sunglasses, dark maroon knitted beanie, maroon sherpa fleece jacket over a cream
> hoodie with yellow drawstrings, black cinema camera in his right hand. Waist up,
> centred, facing the viewer straight on, same scale in every cell.
>
> Camera locked off, static, eye level, 50mm equivalent, no movement between cells.
> Body, shoulders, arms and jacket identical throughout. Only the mouth, cheeks,
> brow and the visible eyes behind the sunglass lenses change.
>
> Left to right: neutral and calm; a small closed-mouth smile; eyebrows raised in
> curiosity with a slight head tilt; a wide open delighted grin; a wry one-sided
> smirk. Keep every expression readable at small size — clear mouth shapes and brow
> positions rather than subtle micro-expression.
>
> Lighting: flat even soft frontal key, gentle top fill, no hard shadows, no rim
> light, identical in every cell. Palette: maroon, cream and matte red on a flat
> chroma-blue background, pure, unlit and completely even. Friendly, warm,
> approachable mood.
>
> No cast shadow on the backdrop, no floor, no props, no logos, no watermarks, no
> text, no captions, no borders between cells, no background gradient, no motion
> blur, no depth of field.

---

## Prompt 3 — single-cell top-up (for any pose that comes back wrong)

Use this to regenerate one cell rather than the whole sheet, so the rest stays
consistent.

> The same 3D character — stylised Pixar-style young man, matte-red rounded head,
> oversized black rectangular sunglasses, dark maroon beanie, maroon sherpa fleece
> over a cream hoodie with yellow drawstrings, black cinema camera in his right
> hand — waist up, centred, on a flat chroma-blue background.
>
> He is looking **[DIRECTION: up and to his left / straight at the viewer / down and
> to his right / …]** with **[EXPRESSION: a neutral calm face / a small closed-mouth
> smile / raised curious eyebrows / a wide delighted grin / a wry smirk]**.
>
> Static locked-off camera, eye level, 50mm equivalent, no movement. Flat even soft
> frontal key with gentle top fill, no hard shadows, no rim light. Palette maroon,
> cream and matte red on pure flat unlit chroma blue. Head turned no more than 25
> degrees from centre, eyes leading the head. Warm, friendly, approachable.
>
> No cast shadow on the backdrop, no floor, no props, no logos, no watermarks, no
> text, no motion blur, no depth of field.

---

## Settings

- **Model:** an image model with strong character consistency. Feed
  `Char PNG copy.tiff` as the reference image on every run.
- **Aspect:** 1:1 for the 3×3 grid; 16:9 or wider for the five-cell expression row.
- **Resolution:** the highest available — each cell gets cropped out, so a 3×3 at
  2K yields roughly 680px cells, which is the practical minimum for a hero.
- **Reference strength:** high. Identity drift between cells is the failure mode
  that makes the whole sheet unusable.

## After generation

1. Check identity first — same beanie, same jacket, same sunglasses in every cell.
   One drifted cell ruins the illusion more than a slightly wrong gaze angle.
2. Cut each cell out on the chroma and export as transparent PNG/WebP at matched
   dimensions.
3. Drop them in `site/assets/character/gaze/` named by direction:
   `up-left.webp`, `centre.webp`, `down-right.webp`, and
   `expr-neutral.webp`, `expr-smile.webp` and so on.
4. The hero then swaps the nearest cell to the cursor's angle and cross-fades
   expressions on scroll.

## If the grid comes back inconsistent

Generate the **centre cell alone first**, approve it, then use that as the
reference image for all eight remaining directions via Prompt 3. Slower, but it
holds identity far better than asking for nine cells in one pass.
