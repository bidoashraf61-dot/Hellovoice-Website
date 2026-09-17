# Handoff — next session

Branch: **`ref-parity`**. The HelloVoice build is on **`ariyana-clone`**.

Read [`../README.md`](../README.md) first, then
[`REFERENCE-AUDIT.md`](REFERENCE-AUDIT.md) and
[`REFERENCE-ANIMATIONS.md`](REFERENCE-ANIMATIONS.md).

---

## The goal, and where it stands

Make `site/` identical to `https://ariyana-studio.webflow.io` using the
reference's own content, images and video — so that any remaining difference is
unambiguously a build error rather than HelloVoice's copy reflowing. Then swap
HelloVoice's content back in.

**Stage one is done.** Seven pages. Layout parity is exact at 1440×900 and
375×812: every section's top offset and height matches the reference to the
pixel, and the document heights are equal. All 113 CDN assets mirrored. Motion
rebuilt against measured values, not estimates. No broken assets, no hidden
elements, no horizontal overflow, one `h1` per page.

```bash
python3 build/serve.py 8811   # no-store on documents; http.server caches them
python3 build/clone.py     # regenerate all seven pages
```

**Stage two — swapping HelloVoice's content in — has not started**, and should
be a separate session. Do not start it inside a parity session; that is the
ambiguity this branch exists to remove.

---

## What changed in approach, and why it matters

The previous build hand-authored markup in `build/site.py` against a re-written
design system. That is what made parity a moving target. This branch
**transforms the reference's own served HTML and serves its own stylesheet**,
rewriting only asset URLs. Palette, type scale, spacing and grounds cannot
drift, because they were never re-authored.

`build/site.py` and `build/theme.css` are the old path and are unused here.
They still drive the HelloVoice build on `ariyana-clone`. Leave them alone.

This does mean stage two is a different shape than previously assumed: content
gets swapped **into the reference's own markup**, node by node, rather than
regenerated from a Python model. That is the point — the markup is the contract.

## Three findings worth keeping

**1. The reference's stylesheet enumerates every animated element.** A
pre-paint hide rule keyed on `html.w-mod-js:not(.w-mod-ix3)` lists all 24 hooks.
That is where the `data-*` attribute map came from — no guessing. Quoted in
full in `REFERENCE-ANIMATIONS.md`.

**2. Webflow now runs two engines.** IX2 still drives the hovers and is fully
introspectable via `Webflow.require('ix2')`. The scroll work is IX3, which is
GSAP-backed and *not* introspectable — `getChildren()` returns empty. Those had
to be characterised by sampling computed transforms against scroll progress at
1/16 resolution. Do not waste time trying to read IX3 config; sample it.

**3. `SCROLL_PROGRESS` maps to the whole traversal**, not the pinned range: 0%
when the element's top is at the viewport bottom, 100% when its bottom is at the
viewport top. Getting this wrong put the showreel ~30% out of phase.

## The trap that cost time twice

Applying a desktop-only initial state at every width. IX2 registers most
hovers, the showreel and the step panel for `main` (≥992px) only, and the
reference's stylesheet lays those elements out differently below it. Both
mobile defects in the audit were this. Everything desktop-only now sits in
`gsap.matchMedia()` **with a cleanup function** — the cleanup is what makes a
resize back to mobile correct.

## Other working notes

- The browser pane's screenshots are unreliable with two tabs open and one
  remote. Close the spare tab. **Trust measurement over screenshots**: two
  "obvious" visual differences this session turned out to be capture artifacts
  over geometry that was already identical to the pixel.
- Fonts are the reference's own TTFs from its CDN, so the Google `css2` trap
  does not arise here. If that changes, verify by measurement: Bebas is
  ~0.577× Arial for the same string; ~0.99× means it is falling back.
- Assets: `capture/reference-assets-all.json` is the manifest,
  `capture/fetch_all.py` re-mirrors it. Extract HTML urls with a catch-all
  pattern but CSS urls with a `url()` pattern — a catch-all over minified CSS
  swallows the rest of the rule.
- Do not patch `build/clone.py` by index-slicing. Use `Edit` with unique
  anchors.

---

## Open

**Nothing blocking.** These are decisions, not defects.

1. **Licensing.** 134 `data-placeholder` tags across seven pages; all 113
   mirrored files and all copy are the template's. Nothing ships until
   `grep -rc 'data-placeholder' site --include='*.html'` returns zero. Stated
   once in the audit; it does not need repeating to the client.

2. **The hero exception.** Built as asked — white ground, the approved
   character, using the reference's own `is-secondary` / `is-dark` light nav
   variant. It is isolated to `assets/css/hero-exception.css` plus one function
   in `build/clone.py`, so `HERO_EXCEPTION = False` reverts it exactly. Worth a
   sentence to the client: on *this* branch the page is otherwise wholly
   Ariyana, so the HelloVoice character sits oddly in it. It will read correctly
   once stage two lands. If they want a clean parity screenshot in the
   meantime, flip the flag.

3. **Nothing is estimated any more.** The text entrances were the last gap and
   are now measured: the reference splits to words *and* chars and drops the
   **chars** in from one line-height above, no fade and no clipping mask, with
   a `back.inOut` on headings and a `power2.out` on body copy. The build tracks
   it within 1–5px at every 70ms sample and is exact at 420ms. Table in
   `REFERENCE-ANIMATIONS.md`.

   The trick, if any of these need re-measuring: they are `once: true`, so a
   warm page shows nothing. Hard-reload with a cache-busting query, park just
   short of the `clamp(top 90%)` crossing, then sample while crossing it.
