# HelloVoice — Website Rebuild Design

**Date:** 8 August 2026
**Supersedes:** the scroll-world approach in `docs/roadmap.html` (2 August 2026)
**Status:** awaiting review

---

## 1. What changed since the 2 August roadmap

That roadmap proposed rebuilding the homepage as a scroll-scrubbed cinematic camera
flight, gated behind seven decisions. Three things have since been decided that
retire most of it:

1. **No scroll-animated landing page.** Gates 1, 2, 3, 4 and 7 are void. Phases 3 and 4
   — previz and render, roughly nine days and $66 of render spend — are removed.
2. **No patching of the live site.** The old Phase 0 is folded into the new build.
3. **A new site from scratch**, which settles Gate 5.

Gate 6 (Arabic) survived and has been answered: **bilingual at launch**.

One item from the old Phase 0 is still worth doing in isolation. The header
**Free Consultation** button links to `#hellovoice.co.uk/contact` — a malformed anchor,
so the site's only primary call-to-action does nothing. It is a one-line change and the
current site stays live for the whole build. This has been flagged; it remains the
client's call.

---

## 2. The finding that shapes everything

The live site publishes two taxonomies that do not agree with each other:

| Services (homepage) | Categories (portfolio) |
|---|---|
| Video Production | Commercial Ads |
| Post Production | Corporate Videos |
| CGI & 3D Production | CGI & Anamorphic |
| AI Production | Event Coverage |
| AVL & Live Production | Awareness Videos |
| Animation & Motion Production | Interviews |

The left column describes *how the work is made*. The right describes *what it is*.
Neither describes *who it is for*, which is how buyers search and filter.

Reading all 42 portfolio projects, **roughly 28 are healthcare, pharma or derma**:
Pfizer, Abbott, Molnlycke, Sanofi, Nahdi, La Roche-Posay, Vichy, Filorga, Dermactive,
Spimaco, Menarini, Orchidia, Bionnex, QV, Seroflo/SPC, Suliman Al Habib, KSMC Hospital,
Kuwait Blood Bank, Jeddah Derm, Derma 2024. Automotive (Neweast / Isuzu / Aisin) is
second. Industrial (Sudair, Al Naghi, Sweedy) is a distant third.

**HelloVoice is a pharma and healthcare film specialist presenting itself as a
generalist video company.** The new site leads with the specialism. Automotive and
corporate work stays visible as proof of range, not as the headline.

---

## 3. What the site is for

Two jobs, chosen deliberately:

**Credibility for outbound and referrals.** Most work arrives by pitch, relationship or
RFP invitation. A visitor who already has the name opens the site to answer one question
in about ninety seconds: *are these people real, and are they at my level?* The site must
survive that check.

**Inbound lead generation.** Strangers should find HelloVoice through search — including
AI answer engines — and be able to qualify themselves before making contact.

Two audiences were considered and **deliberately excluded**: procurement/compliance
(no dedicated credentials page) and recruitment (no careers section). Both can be added
later; neither earns its build cost now.

---

## 4. Services — named from what is actually sold

Five of the eight below are things HelloVoice already delivers and has never named.
Each has proof already sitting in the portfolio.

| Service page | Replaces / draws from | Proof in the portfolio |
|---|---|---|
| Brand & Campaign Films | Video Production | Dermactive, La Roche-Posay, Qasser El Saraya |
| **Patient Awareness & Education** | *(unnamed)* | 10 projects — the largest single category |
| **Medical & Scientific Animation** | Animation & Motion | Seroflo whiteboard, Ciphaler, Menarini HCP portal, Skintellectual |
| **Congress & Event Films** | AVL & Live Production | Molnlycke, Spimaco, Vichy, Jeddah Derm, Filorga, L'Oréal Derma — 10+ |
| **KOL & Testimonial Films** | *(unnamed)* | Abbott × Kuwait Blood Bank, Vichy, Bionnex |
| CGI, 3D & Anamorphic DOOH | CGI & 3D Production | Mela B3, Automechanika, Isuzu screens |
| Post Production | Post Production | (existing) |
| AI Production | AI Production | Neweast × Isuzu AI film + BTS documentary |

Each service page carries: what is delivered, the process, the kit, a typical timeline,
a **budget band**, two or three proof films, and the named lead. Budget bands qualify
inbound traffic and prevent unpayable pitches.

---

## 5. Information architecture

```
/                       Home — healthcare-led
/work/                  All 51 films, filterable by service · industry · format · client
/work/<project>/        Individual project
/case-studies/<slug>/   3–5 deep studies
/services/              Index
/services/<slug>/       The eight above
/how-we-work/           Process, MLR awareness, bilingual delivery, confidentiality
/about/                 Company + the six named team members
/contact/               Qualifying form + WhatsApp
/ar/…                   Full Arabic mirror of the above
```

**`/how-we-work/` is the page that wins pharma work.** MLR review cycles, medical
accuracy, bilingual delivery, congress turnaround, confidentiality. No competitor in
this market publishes one. It is the cheapest differentiator available.

**Case studies use a fixed spine:** brief → constraint → what we did → the film →
results. Results are what separates a partner from a vendor and what almost no agency
site carries. Soft numbers count: reach, delivery in eleven days across four languages,
awards, repeat commissions.

---

## 6. Architecture

| Layer | Choice | Reasoning |
|---|---|---|
| Front end | **Astro 5** | Ships zero JavaScript by default. The current site loads 19.2 MB across 93 requests with 27 stylesheets and 23 scripts; Astro's defaults are the direct correction. Filters, form and video facades become islands. |
| CMS | **Sanity** | Hosted, no devops. Non-technical staff publish often — that was the deciding requirement. Its localisation plugin holds EN and AR as parallel documents. |
| Images | **Sanity image pipeline** | On-the-fly WebP/AVIF, responsive sizes, art-directed crops. Retires the "295 assets, 243 MB, no WebP, zero alt text" problem structurally rather than by hand. |
| Video | **Vimeo + poster facade** | All 51 films stay on Vimeo. A Vimeo iframe costs roughly 500 KB of JavaScript; on a 40-item work index that is fatal. The facade shows a poster and loads the player only on click. |
| Hosting | **Vercel** | Edge CDN, preview deploys for client review, zero-config with Astro. |
| Forms | Astro API route | Qualifying fields → email + webhook, firing a conversion event to GA4, Meta and LinkedIn on submit. |

### Content model

Six document types, each localised EN/AR:

- **Project** — title, Vimeo ID, poster, client ref, service refs, industry, format, year, description, alt text
- **CaseStudy** — brief, constraint, approach, films, results, client ref
- **Service** — the eight, with deliverables, process, timeline, budget band, lead
- **Client** — name, logo, industry
- **TeamMember** — name, role, portrait, own work
- **Page** — home, about, how-we-work, contact

`Project` is the migration target for everything currently trapped inside Elementor.

---

## 7. Budgets

**Performance** — measured on throttled mobile, not desktop:

| Metric | Target | Today |
|---|---|---|
| First paint weight | < 400 KB | ~19.2 MB total transfer |
| LCP | < 2.5 s | 6.3 s load, desktop broadband |
| CLS | < 0.1 | unmeasured |
| INP | < 200 ms | unmeasured |
| Lighthouse performance (mobile) | ≥ 95 | unmeasured |

**SEO and machine readability:**

- Exactly one H1 per page. Today: `/` has one; `/about/`, `/portfolio/` and
  `/contact-us/` have none, and `/portfolio/` carries 56 headings without one.
- Meta title and description on every page, in both languages.
- `hreflang` for `en` and `ar`, plus `x-default` → English.
- Schema.org: `Organization`, `LocalBusiness`, `VideoObject` per film, `CreativeWork`,
  `BreadcrumbList`, `FAQPage` on service pages.
- XML sitemap covering both languages, submitted to Search Console. Both current
  sitemap URLs return 404.
- Alt text on every image. Today **0 of 295**.

**Analytics:** GA4, Meta pixel, LinkedIn insight tag, and a form-submit conversion
event wired end to end. The current site has none of these on any page.

---

## 8. Migration

Everything on the live site was captured on 8 August 2026 into `capture/`:

| File | Contents |
|---|---|
| `capture/content.json` | **The migration base.** All 42 projects with category, title, Vimeo id, runtime and corrected poster URL; plus links, headings, copy, images, contact, tech |
| `capture/CONTENT-INVENTORY.md` | Human-readable summary of everything below |
| `capture/vimeo.json` | All 51 films — titles, durations, thumbnails |
| `capture/videos.json` | Vimeo IDs mapped to the pages they appear on |
| `capture/structure.json` | Heading trees, link maps, per-page image references |
| `capture/media-summary.json` | Media library breakdown |
| `capture/raw/pages.json` | All 4 pages via the WordPress REST API |
| `capture/raw/posts.json` | The 6 junk posts |
| `capture/raw/media.json` | All 295 media items with metadata |
| `capture/raw/page-*.html` | Rendered HTML of each live page (git-ignored) |
| `capture/text/*.txt` | Extracted plain-text copy per page |
| `capture/media/` | The full media library, downloaded (git-ignored) |
| `capture/*.py` | The capture scripts — re-runnable against the live site |

**Redirects at launch:**

| Old | New | Type |
|---|---|---|
| `/` | `/` | — |
| `/about/` | `/about/` | — |
| `/portfolio/` | `/work/` | 301 |
| `/contact-us/` | `/contact/` | 301 |
| `/2025/10/19/hello-world/` | — | **410 Gone** |
| `/2020/01/01/x/` … `/x-5/` | — | **410 Gone** |

The six junk posts get `410 Gone` rather than a redirect. There is nothing to redirect
them to, and 410 tells search engines to drop them immediately.

**Filenames:** a large share of the media library carries machine-generated names
(`ezgif.com-optimize`, `WhatsApp Image …`, `IMG_1234`, `12345_00000-1.png`). All assets
are renamed on migration.

**Not migrated — must be written from scratch, because it does not exist:** service page
copy, case study copy, alt text, meta titles and descriptions, all Arabic content, and
any client result or metric.

### Technical defects found during capture

Eight issues beyond the 2 August audit. All are resolved by the rebuild, but two
should be understood now because they change what the audit concluded.

**1. Every Portfolio poster image is broken.** 48 assets are served from
`http://52.211.223.138:1005` — a raw IP on port 1005 over plain HTTP. That host is
completely unreachable. The identical files serve fine from `hellovoice.co.uk`. Forty-two
of these are Portfolio poster images and seven are on the homepage.

This is almost certainly the true cause of the audit's *"sections render as empty space —
2,163 px blank block, six empty 701 px cells."* A staging server's address was baked into
the content and never rewritten at go-live. The capture rewrites every one of these URLs
onto the live domain in `content.json`.

**2. 117 broken links.**

| Count | Problem |
|---|---|
| 86 | placeholder `#` anchors that go nowhere |
| 15 | anchors with no `href` attribute at all |
| 8 | empty `href` |
| 4 | insecure `http://` links |
| 4 | malformed anchors that look like URLs |

The 86 placeholders include **all six homepage service areas** — *Video Production*,
*Post Production* and the rest each link to `#`. The malformed set includes the header
**Free Consultation** button on every page.

**3. `robots.txt` publishes the secret admin URL** — `Disallow:
/hellovoiceadminsecuredlogin/`. The login path was renamed for security, then advertised
publicly. The new site must not repeat this.

**4. Six junk posts are live and indexable** — WordPress's default `Hello world!`, never
deleted, plus five posts titled `x` dated 2020-01-01. All need `410 Gone` at launch, not
redirects; there is nothing to redirect them to.

**5. The sitemap is a redirect into a dead end.** `sitemap.xml` returns 301 →
`/wp-sitemap.xml`, which 404s. Worse than a plain 404 — it burns crawl budget first.

**6. Six typefaces are loaded.** DM Sans, Inter Tight, Manrope and Nunito Sans each at
every weight 100–900 plus italics, alongside Cardo and Inter. The new site uses two.

**7. `Qasser El saraya Ad` has no video.** Configured as a Vimeo item with a poster and a
lightbox, but no URL. Clicking it opens nothing.

**8. Only the homepage has an H1.** Portfolio carries 56 headings and not one is an H1.

### Design tokens on the live site

The only distinctive brand value is **`#d8613c`**, the CTA orange. Everything else in the
palette is untouched WordPress core and Twenty Twenty-Three defaults. There is no type
system to preserve. This supports treating the visual identity as new work built from the
logo and theme the client supplies.

### Content problems found during capture

Resolving all 51 Vimeo films against the live pages surfaced four issues that the
rebuild must fix rather than carry over.

**Client names are misspelled on the live site.** For an agency selling to pharma
multinationals, a misspelled client name is a direct credibility cost — it is the first
thing a brand manager notices.

| On the site | Should be | Where |
|---|---|---|
| `Zoiets` / `Zoites` | **Zoetis** — confirmed by the film's own Vimeo title | Portfolio, homepage client list |
| `Molynlcke` | **Mölnlycke** — letters transposed | Homepage client list, portfolio |
| `L'Oreal` | **L'Oréal** | Portfolio |
| `Kwait` | **Kuwait** | Portfolio |
| `Sweedy Electric` | Verify — likely **Elsewedy Electric** | Homepage client list |
| `Qasser Elsaraya` / `Qasser El saraya` | Pick one spelling | Homepage vs portfolio disagree |

One portfolio entry also begins with a stray Arabic diacritic character:
`ِAbbott X Kwait Blood Bank Interviews`.

**A whole vertical is invisible.** Three films — `Furniture Industry showreel`,
`Furniture Showreel / Bed Room Video 02`, `Isuzu - Neweast- Showroom Branding
Presentation` — cover furniture and interior/retail environment work. None of the six
portfolio categories admits this exists. Either it becomes a named capability or it is
deliberately retired; it should not stay hidden.

**Arabic deliverables already exist.** `MK_Molnlycke_Habib Patient awareness (Teaser
Video) - Arabic` and `Neweast X Isuzu Social Media English` (implying an Arabic
counterpart) confirm bilingual production is already routine. This is evidence for the
bilingual launch decision, and it is a selling point the current site never makes.

**Roughly a dozen films carry unusable titles** — `Video Animation`, `CGI`,
`Website Showreel`, `Bts -3`, `Teaser 1 Reduced Size`, `Screen 3d Showreel`,
`Neweast Social Media Reel Without The Main V`. Each needs a real title, client
attribution and description written during Phase 1. These are also the `VideoObject`
schema titles, so they affect search directly.

---

## 9. Phases

| Phase | Work | Days |
|---|---|---|
| **0** | Content capture | done |
| **1** | Content architecture: sitemap, eight service pages, copy deck EN + AR, alt text, meta, case-study selection | 5 |
| **2** | Design system and key page designs: type, colour, motion, home / service / case study / work index | 5 |
| **3** | Build: all pages, Sanity schema, Vimeo facades, image pipeline, qualifying form, analytics, schema.org, RTL | 12–14 |
| **4** | QA and launch: performance budget, accessibility, redirects, tracking, sitemap, Search Console | 4 |

**Roughly 6–7 weeks**, assuming inputs below arrive without delay.

### Starts immediately, in parallel

**Client clearance for case studies.** Pharma legal and brand approval routinely runs
4–8 weeks — longer than the build. Requests go out in week 1 or the site ships without
named case studies. Candidates, chosen because each shows something technically
distinctive:

1. **La Roche-Posay Mela B3** — CGI
2. **Neweast × Isuzu AI film + BTS documentary** — the documentary is rare and unusually persuasive
3. **Molnlycke Cycle Meeting** — a full congress package: teaser, 3D screen, recap
4. **Abbott × Kuwait Blood Bank** — campaign, interviews and awareness across one client

---

## 10. Inputs needed from HelloVoice

| Input | Blocks | Status |
|---|---|---|
| Logo in vector (SVG/AI/EPS) | Phase 2 | requested |
| Theme — colours, fonts, or a reference | Phase 2 | client to provide |
| Decision on fixing the live CTA | — | flagged, client's call |
| Case-study clearance requests sent | Phase 1 | to start week 1 |
| Arabic copy source — in-house or commissioned | Phase 1 | open |
| Correct phone numbers | Phase 3 | `+966 50 74488665` has one digit too many for a Saudi mobile; `+966 11 463 4518` appears on Contact but not the footer |
| Where enquiries should route — inbox, CRM, WhatsApp | Phase 3 | open |

---

## 11. Explicitly out of scope

Removed on purpose, to be re-argued later if they earn it:

- The scroll-scrubbed camera flight
- A blog
- A procurement / compliance credentials page
- A careers section
- A client login portal
- Awards tickers, "years of experience" counters, stock team photography
- Preloader animations that gate content
