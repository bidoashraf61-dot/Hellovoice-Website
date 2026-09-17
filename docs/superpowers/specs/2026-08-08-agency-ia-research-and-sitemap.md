# Agency IA Research → The New HelloVoice Sitemap

**Date:** 8 August 2026
**Method:** pulled and parsed the live sitemaps of 20 leading production, post, creative
and healthcare-communications companies, then drilled into the section structure of the
eight most relevant. Real URL data, not opinion.

---

## 1. What was studied

| Reachable | URLs | Category |
|---|---|---|
| Framestore | 2,309 | VFX / post |
| Monks | 5,859 | Global production network |
| Prettybird | 1,530 | Production |
| Biscuit Filmworks | 782 | Production |
| Territory Studio | 754 | Design / motion |
| Real Chemistry | 529 | Healthcare comms |
| Hungry Man | 503 | Production |
| BUCK | 339 | Design / motion |
| Pulse Films | 331 | Production |
| Havas Health | 161 | Healthcare comms |
| 21GRAMS | 119 | Healthcare comms |
| The Mill | 114 | Post |
| AREA 23 | 26 | Healthcare creative |
| Klick Health | 14 | Healthcare |

Somesuch, Iconoclast, Stink Studios, Riff Raff, ManvsMachine and Tag publish no sitemap —
itself a signal about how lightly the fashion end of the industry treats search.

**Sections shared across the set:** `/contact` (9 sites), `/about` (7), `/news` (7),
`/work` (6), `/careers` (5), `/privacy-policy` (5).

---

## 2. The four models that actually exist

**Talent-led.** Pulse Films, Hungry Man, Prettybird, Biscuit. The spine is `/directors`
— the roster *is* the product, and work hangs off each name. Almost no service pages.
*Not applicable to HelloVoice:* you don't sell signed directors, you sell a studio.

**Sector-led.** Framestore. The spine is the market, with capabilities nested inside it:

```
/advertising              /film
/advertising/animation    /film/animation
/advertising/characters   /film/characters
/advertising/creatures    /film/creatures
/advertising/environments /film/environments
/advertising/services     /film/fps
```

The *same* capabilities repeat under each sector, because a film buyer and an advertising
buyer want to hear about animation differently. **This is the model closest to what
HelloVoice needs** — it is the "who it's for" axis made structural.

**Case-study-led.** Monks: **451 case studies** at `/case-studies/<keyword-rich-slug>`
(`bmw-i4-edge-electrified-social-first-campaign`), against a single `/what-we-do` page.
The case studies *are* the SEO surface. Everything else is thin.

**Radically lean.** Klick Health runs a **14-URL site**. AREA 23 runs **26**. Two of the
most decorated healthcare agencies on earth have almost no website. Their model is pure
credibility — you arrive already knowing the name. *This is the trap HelloVoice must
avoid,* because you chose inbound as well as credibility, and a 14-URL site cannot rank.

---

## 3. Findings worth stealing

**Results go at the top of a case study, not the bottom.** Monks' Bayer study runs:
client & solutions overview → **results** → challenge → solution → press quote →
implementation → results summary → related work. The numbers are stated before the story:
*"$10 million in cost savings within the first six weeks"*, *"35% ongoing efficiency
improvement in media cost"*.

**Sector reels are first-class work items.** The Mill publishes `/work/automotive-reel-2026`,
`/work/fashion-and-beauty-reel-2026`, `/work/environment-reel-2026`,
`/work/brand-and-content-reel-2026`, `/work/film-and-series-reel-2026` — one reel per
market, each its own URL. HelloVoice already owns six showreels sitting unnamed inside the
portfolio. They should be pages.

**Accessibility can be a positioning signal.** AREA 23 publishes audio-described versions
of its work at `/work/<project>/audio-description`. For a healthcare audience — where
accessibility is a professional value, not a compliance chore — this reads as competence.
Cheap to do, and nobody in the Gulf market does it.

**Case-study slugs are keyword real estate.** Monks writes
`boAt-Enigma-x-series-CGI-Animation`, not `case-study-12`. Your current media library is
full of `12345_00000-1.png`.

**Scale calibration.** The Mill at 114 URLs and Havas Health at 161 are the right size
reference for HelloVoice. Monks' 5,859 is a different business. Klick's 14 is a different
strategy.

---

## 4. The recommended sitemap

Framestore's sector spine, Monks' case-study discipline, The Mill's scale — flattened so
it doesn't combinatorially explode at your size.

```
/                                        Home — healthcare-led
│
├── /work/                               Index. Filter: service · industry · format · client
│   └── /work/<project>/                 42 projects, one per film
│
├── /reels/                              Index
│   ├── /reels/healthcare/               ← the flagship
│   ├── /reels/congress-events/
│   ├── /reels/cgi-anamorphic/
│   ├── /reels/medical-animation/
│   ├── /reels/interviews-kol/
│   └── /reels/automotive/
│
├── /case-studies/                       Index
│   └── /case-studies/<keyword-slug>/    3–5 deep. Results stated first.
│
├── /services/                           Index
│   ├── /services/brand-campaign-films/
│   ├── /services/patient-awareness-education/
│   ├── /services/medical-scientific-animation/
│   ├── /services/congress-event-films/
│   ├── /services/kol-testimonial-films/
│   ├── /services/cgi-3d-anamorphic-dooh/
│   ├── /services/post-production/
│   └── /services/ai-production/
│
├── /industries/                         Index — the credibility axis
│   ├── /industries/pharma-healthcare/   ← two-thirds of your work
│   ├── /industries/automotive/
│   └── /industries/corporate-industrial/
│
├── /how-we-work/                        MLR-aware process, bilingual delivery, confidentiality
├── /guides/                             Index — 4 evergreen pages, no dates, no feed
│   ├── /guides/mlr-review-for-video/
│   ├── /guides/hcp-vs-patient-content/
│   ├── /guides/congress-film-planning/
│   └── /guides/arabic-localisation-for-pharma/
│
├── /about/                              Company, values, the six named people
├── /contact/                            Qualifying form + WhatsApp
│
├── /privacy/  /terms/  /accessibility/
│
└── /ar/…                                Full Arabic mirror of everything above
```

**Roughly 81 URLs in English, ~162 bilingual** — between The Mill and Havas Health.
Correct scale for the business.

### Why services *and* industries, both flat

Framestore nests capabilities inside sectors, which at their scale produces a rich matrix.
At your scale it would produce 24 thin pages that cannibalise each other. Flat and
cross-linked instead:

- **`/services/*` is the search surface.** Someone types "medical animation Saudi Arabia".
- **`/industries/*` is the credibility surface.** A pharma brand manager arriving from a
  referral wants one page that proves you understand their world — MLR, HCP vs patient,
  congress calendars, Arabic.
- **`/work/` is filterable by both**, so the two axes meet without extra pages.

### What each page type must carry

**Service page:** what you deliver · process · kit · typical timeline · **budget band** ·
2–3 proof films · named lead · FAQ block (`FAQPage` schema).

**Industry page:** why this sector is different · the constraints you work inside ·
client logos · 4–6 proof films · the relevant case study · a sector reel.

**Case study:** **results first**, then brief → constraint → what we did → the film →
credits → related work.

**Project page:** the film behind a poster facade · client · services · industry · year ·
description · `VideoObject` schema · related projects.

### Deliberately excluded

`/careers` — you chose credibility and inbound, not recruitment. `/news` or a blog —
nobody will maintain it; `/guides/` gives the SEO benefit with four evergreen pages
instead of an empty feed. `/directors` — wrong model for a studio. A procurement
credentials page — no longer in scope.

---

## 5. Migration mapping

| Today | Becomes |
|---|---|
| `/portfolio/` — 6 format categories, 42 projects, all posters broken | `/work/` with four filter axes and 42 real project pages |
| 6 service labels linking to `#` | 8 service pages that exist |
| Showreels buried inside the portfolio | 6 `/reels/*` pages |
| "Case Studies" section — 2 items, no copy | `/case-studies/` with results-first structure |
| No industry axis anywhere | `/industries/*`, led by pharma |
| No process page | `/how-we-work/` — the page that wins pharma work |
| English only | Full `/ar/` mirror |
| 6 junk posts | `410 Gone` |

---

## 6. Sources

- Sitemaps parsed directly from each domain, 8 August 2026
- [Monks — Bayer Consumer Health case study](https://www.monks.com/case-studies/bayer-consumer-health)
- [The Mill — work index](https://www.themill.com/work)
- [Framestore](https://www.framestore.com)
- [BUCK](https://www.buck.co)
- [Klick Health](https://www.klick.com)
- [AREA 23](https://www.area23hc.com)
- [Elsewedy Electric](https://www.elsewedyelectric.com/about-us) — client name verification
