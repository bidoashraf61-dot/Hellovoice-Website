# Hello Voice — Technology Activations Brochure

**Date:** 2026-08-12 · last revised 2026-08-12 after first build and audit
**Status:** **Built and audited — not launch-ready.** See §11 for what blocks launch.

| | |
|---|---|
| Build | `User Assets/Tech Prochuere/HelloVoice-Technology-Catalogue.html` |
| Preview | `https://claude.ai/code/artifact/e6d3fd20-6b1d-4c26-8f90-35c90d7669f4` |
| Source | `src2.html` + `data.js` + `build2.py` (scratchpad — see §12) |
| Supersedes | the invented-content placeholder at `artifact/3bc6495e…` |

> The preview link cannot play video: that host blocks all third-party embeds. Open the
> HTML file locally or self-host it to see the players work.

---

## 1. What this is

A standalone, self-hosted brochure page presenting Hello Voice's technology activations —
one card per application, each opening a real video. It ships ahead of the website rebuild
and is built so it can be absorbed into the new site later without a redesign.

**Audience:** prospective clients and agencies. The sales team sends one link.

**Not in scope:** pricing, client names, case studies, the corporate site's navigation.

## 2. Decisions taken

| Decision | Outcome |
|---|---|
| Format | Interactive web page, self-hosted on a Hello Voice subdomain |
| Language | English only |
| Visual design | Keep v1 exactly as published — dark control-room, Hello Voice red, monitor cards, tally lights, modal |
| Content source | HyperX company-profile deck + applications supplied directly by Mohamed |
| Client naming | **None.** Cards focus on the application only. No logos, no client names, no sector labels |
| Card model | One card per application; multiple films nested inside it |
| Video host | Vimeo for everything except the El-Sewedy 360° film (YouTube, for sphere playback) |
| Card behaviour | Still frame on the card; the player loads in the modal on click |
| Lab section | Removed — those six ideas were invented and are not Hello Voice offerings |

**Why v1's design is kept:** it was reviewed and approved as published. This work replaces
its content, not its design system. The typefaces (Montserrat, Roboto) are already subset
and embedded, the layout is verified responsive down to 390px, and the tally-light system
already models exactly the state this project needs — which applications have footage and
which do not.

**Why the HyperX deck is content only:** the deck's own identity is yellow `#FFCD00` with
Barlow Italic. This is a Hello Voice brochure, so it carries Hello Voice's identity. The
deck supplies the application list, descriptions and video links.

## 3. The catalogue — 23 applications in 3 banks

*(20 agreed, plus the three provisional entries from the client's own `Screens/` folder.
Resolving the naming overlaps below may reduce this number.)*

**Naming convention: applications are named for the technology, not the campaign.**
"Who Art You?" is a campaign built for one client; the thing Hello Voice sells is an
Interactive Art Wall. The campaign name survives as the *film label* inside the card, which
also resolves input 4 — the films now have meaningful names without naming any client.

| Bank | Application (technical) | Was called | Films |
|---|---|---|---|
| INT | Interactive Art Wall | Who Art You? | 1 |
| INT | Interactive Game Wall | Tic Tac Toe Goal | 1 |
| INT | Motion Reactive Wall | Flower Wall | 1 |
| INT | Multi-Screen Installation | What Would It Feel? | 1 |
| INT | Interactive Music Wall | Music Wall | 1 |
| INT | Interactive Light & Sound Tunnel | Music Tunnel | 1 |
| INT | Interactive Touch Catalogue | Catalogue Display | 1 |
| INT | Smart Cube | — | 3 + 2 on Vimeo |
| IMM | Interactive Hologram (Holobox) | HoloBox | 4 on Vimeo |
| IMM | VR Experience | VR Immersive | 1 on Vimeo |
| IMM | Laser Cube | — | 1 on Vimeo |
| IMM | Hologram Fan | — | **none** |
| IMM | UV Camera | UV Cam | **none** |
| MMC | 3D Naked Eye | 3D Naked Eye Show | 1 |
| MMC | 3D Anamorphic Content | Anamorphic Illusion | 8 + 2 on Vimeo |
| MMC | 3D Projection Mapping | — | 1 |
| MMC | Laser Mapping | Laser Mapping Show | 1 |
| MMC | Stage Show Media | Pharaonic Show | 1 |
| MMC | CGI Production | CGI | 4 + 1 on Vimeo |
| MMC | 360° Video | 360 Video Onboarding | 1 on YouTube |

### Three unplaced applications
`Touch Interactive Screen`, `Motion Gesture Interactive Screen` and
`Interactive Product Detailing` come from the client's own `Screens/` folder names and have
footage, but were not in the agreed 20. They are either separate applications or footage
belonging to existing ones — awaiting the client's call.

### Naming overlaps to resolve
Renaming to technical names exposed three pairs that may describe the same technology:
- **Motion Reactive Wall** vs **Motion Gesture Interactive Screen**
- **Interactive Touch Catalogue** vs **Touch Interactive Screen**
- **3D Naked Eye** vs **3D Anamorphic Content** — the deck lists these separately, but
  anamorphic content *is* the naked-eye technique

Each pair is either one application with more films, or two genuinely different products.
Resolving them may reduce the catalogue below 20.

### Two deliberate merges
- **Smart Cube** — the deck's *Smart Cube Interaction* and Mohamed's *Smart Cube Technology*
  are one application. Three films.
- **Anamorphic Illusion** — the deck's *3D Naked Eye Content* is the same technique.
  Three films.

Listing either pair separately would advertise the same capability twice.

### Bank 02 placement is provisional
Laser Cube may belong in Real-time Interactive, and UV Cam is arguably a capture tool
rather than an immersive one. Both move once their content arrives.

## 4. Data model

An application is not a video. It is a capability with one or more films:

Shape only — the `label` values below are placeholders, pending input 4:

```js
{
  code:  "HV-INT-08",
  bank:  "INT",
  name:  "Smart Cube",
  head:  "<one-line headline>",
  desc:  "<40-60 word description>",
  tags:  ["Touchless", "Multi-language", "Data out"],
  films: [
    { label: "<awaiting label>", host: "vimeo", id: "1146927623", hash: "",           poster: "…" },
    { label: "<awaiting label>", host: "vimeo", id: "1184612647", hash: "27d6bfd696", poster: "…" },
    { label: "<awaiting label>", host: "vimeo", id: "<migrated>",  hash: "",           poster: "…" }
  ]
}
```

- `films: []` renders the existing standby tally and "feed pending" slate. This is how
  Hologram Fan and UV Cam ship before their content exists.
- `hash` is mandatory for unlisted Vimeo videos. `vimeo.com/1184612647/27d6bfd696` embeds as
  `player.vimeo.com/video/1184612647?h=27d6bfd696`. Dropping the hash returns a private-video
  error.
- `host: "youtube"` is used only for the 360° film, whose sphere needs YouTube's player.
- The modal shows a film switcher when `films.length > 1`; otherwise it loads the single film.

**Player loading:** no iframe is created until the modal opens, and it is destroyed on close.
Twenty embedded players on one page is the failure mode this avoids.

## 5. Copy

Every description is rewritten from the deck's rough text into the v1 voice — headline plus
40-60 words — preserving all facts and inventing none. No specification numbers (footprint,
crew, build hours) are published unless supplied; tags stay qualitative, as in v1.

**HoloBox is the exception.** Its proposal deck carries enough real substance for a detailed
card: 75″ life-size holographic display with real optical depth, self-supporting movable
metal-frame unit, plug-and-play on power and network, four ways in (presence sensor,
microphone, touch screen, button), on-board Windows PC driving display and avatar locally,
and a bilingual Arabic/English AI avatar trained on the brand's own knowledge base.

> **Confidentiality.** `HoloBox_Proposal_Bioderma V2.pptx` is marked *CLIENT PROPOSAL ·
> CONFIDENTIAL*, prepared for NAOS · Bioderma. Only client-neutral capability content may be
> published. All Bioderma naming, the pharmacy narrative written for them, and every
> commercial term must be stripped. The associated quotation file must never be published.

## 6. Assets

Still frames come from the film masters, with the deck as fallback — it holds 135 embedded
images, 46 of them 1200px or larger, including full 1080×1920 verticals. Client photography
is not required.

Typefaces are unchanged from v1: Montserrat 800/900 and Roboto 400/500/700, subset to Latin
and embedded as woff2 (~84KB total). Both are open-licensed. System monospace is used for
codes and status.

## 7. Required inputs

Ordered by what each blocks. Item 1 is the long pole — 13 of 20 applications currently have
video only on HyperX's gumlet.tv account.

### Blocks the build
1. ~~13 master video files from HyperX~~ — **done.** Retrieved from gumlet and placed in
   `User Assets/Tech Prochuere/HyperX Videos/`. Awaiting upload to Hello Voice's Vimeo.
   *(Optional follow-up: ask HyperX for true masters — see the note in §8.)*
2. **Vimeo IDs for all 20 applications**, with the privacy hash retained on unlisted videos.
3. **A line or two each on Hologram Fan and UV Cam** — what the hardware is and what it does.
   Polishing is mine; the facts are not inventable.
4. **A neutral label per film** for the multi-film applications — Smart Cube (3),
   Anamorphic (3), HoloBox (4) — e.g. "pharmacy activation", "congress stand". Without client
   names, nothing else distinguishes them.
5. **A nominated frame per film** (timecode), or masters so frames can be chosen.

### Blocks polish
6. **Hello Voice logo in vector** (SVG, AI or EPS). Currently a recoloured PNG. Already
   flagged as item B1 in `docs/REQUIREMENTS-FROM-CLIENT.md`.

### Blocks launch
7. **Contact details** — email, phone, website. Three empty slots in the CTA today.
8. **Hosting target** — subdomain and DNS access.

### Not required
Photography, brand fonts, client logos, clearance.

## 8. Content inventory

### From `HyperX_CP_2026.pdf` — videos on gumlet.tv, to be migrated
| Application | Current video |
|---|---|
| Who Art You? | gumlet.tv/watch/6a4e8de11c338f62ccc2afed |
| Tic Tac Toe Goal | gumlet.tv/watch/6a4e8f281c338f62ccc2cfbc |
| Flower Wall | gumlet.tv/watch/6a4e8c913c3a5e1dbd911082 |
| What Would It Feel? | gumlet.tv/watch/6a4e8c22e68bdcaeb978fb9b |
| Music Wall | gumlet.tv/watch/6a4e883c3c3a5e1dbd90a3e6 |
| Smart Cube | gumlet.tv/watch/6a4e86d53c3a5e1dbd90810b |
| Music Tunnel | gumlet.tv/watch/6a4e8c511c338f62ccc2878f |
| Catalogue Display | gumlet.tv/watch/6a4e85d21c338f62ccc1e74d |
| 3D Naked Eye Show | gumlet.tv/watch/6a4e8fd23c3a5e1dbd9161c5 |
| Laser Mapping | gumlet.tv/watch/6a4e91403c3a5e1dbd918361 |
| Pharaonic Show | gumlet.tv/watch/6a4e817b1c338f62ccc1700c |
| 3D Projection Mapping | gumlet.tv/watch/6a4e8216e68bdcaeb977f95d |
| Anamorphic Illusion | gumlet.tv/watch/6a4e89b01c338f62ccc243e8 |

### Supplied directly — already on Vimeo/YouTube
| Application | Film | Link |
|---|---|---|
| Smart Cube | film 2 | vimeo.com/1146927623 |
| Smart Cube | film 3 | vimeo.com/1184612647/27d6bfd696 *(unlisted)* |
| Anamorphic Illusion | film 2 | vimeo.com/1137468181/33cf76b38d *(unlisted)* |
| Anamorphic Illusion | showreel | vimeo.com/1046771415 |
| CGI | — | vimeo.com/1046702532 |
| 360 Video Onboarding | — | youtu.be/PMcCcWbHy04 *(360° sphere)* |
| VR Immersive | — | vimeo.com/1217635643 |
| Laser Cube | — | vimeo.com/1217640072/7f3574479b *(unlisted)* |
| HoloBox | 1 of 4 | vimeo.com/1217631831 |
| HoloBox | 2 of 4 | vimeo.com/1217631828 |
| HoloBox | 3 of 4 | vimeo.com/1217631830 |
| HoloBox | 4 of 4 | vimeo.com/1217631829 |

HoloBox masters also exist locally at
`User Assets/Tech Prochuere/Holo Box Samples/1–4.MP4`.

### Awaiting content
Hologram Fan · UV Cam (positioned for pharmacy activations)

### The 13 HyperX films, retrieved
All 13 have been pulled from gumlet and placed in
`User Assets/Tech Prochuere/HyperX Videos/`, numbered to match the table above, with
gumlet's own thumbnails in a `posters/` subfolder. Ready to upload to Hello Voice's Vimeo.

> ⚠️ **These are delivery renditions, not masters.** gumlet's highest rendition is
> 1080 × 1920 at roughly 3 Mbps, already compressed for streaming. Re-uploading them to Vimeo
> puts a second generation of compression on top, which shows most on the projection-mapping
> and laser films where fine detail sits against black. They are good enough to launch with.
> If HyperX can supply the true masters, swapping them in later costs nothing but the upload,
> since the Vimeo IDs stay the same.

## 9. Build sequence

1. Replace the v1 data array with the 20 real applications and 3 banks; delete the Lab section.
2. Rewrite the deck's rough copy into headline + description per application.
3. Add the film model, the modal switcher, and lazy player mounting.
4. Wire the films that already have Vimeo IDs; leave the rest on standby tallies.
5. Extract and set still frames.
6. Fill contact details, swap in the vector logo, deploy to the subdomain.

Steps 1–3 can proceed immediately. Step 4 completes as inputs arrive.

## 10. Open questions

- Final bank for Laser Cube and UV Cam, once their content arrives.
- Whether the 360° film keeps YouTube long-term or moves to Vimeo — Vimeo supports 360°,
  so consolidating to one host is possible if the master is re-uploaded there.
