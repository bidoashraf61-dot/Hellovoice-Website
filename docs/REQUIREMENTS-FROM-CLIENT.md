# What I need from HelloVoice to rebuild the site

Everything required from your side, in the order it blocks work. Nothing here is
optional — each item stops something specific.

**Legend:** 🔴 blocks work starting · 🟠 blocks design · 🟡 blocks build · ⚪ blocks launch

---

## A. Start this week — time-sensitive

These lose value or become impossible if delayed. They are not blocked by anything else.

### A1. 🔴 Export the contact form submissions
**From:** WordPress admin → your form plugin → Export
**Why:** every enquiry you have ever received. It exists nowhere else and **cannot be
reconstructed**. The moment the old site is decommissioned it is gone.
**Format:** CSV
**Bonus:** it is also the only evidence of what your real inbound mix looks like, which
sharpens the service pages.

### A2. 🔴 Verify the domain in Google Search Console
**Why:** Search Console data accrues **only from the day you verify** — never
retroactively. Every day you wait is a day of query data you will never have.
**Time:** 10 minutes. Do it before anything else on this list.
**Then:** add me as a user, or send screenshots of Queries + Pages after 30 days.

### A3. 🔴 Start case-study clearance
**Why:** **This is the longest lead time in the entire project — 4 to 8 weeks with pharma
clients, longer than the whole build.** If it starts late, the site launches without named
case studies, which removes the most persuasive thing on it.
**Action:** pick 5 candidates, send clearance requests now. Ship with whatever clears.
**My recommendation for the 5:** a Dermactive campaign, the Abbott × Kuwait Blood Bank
work, a Mölnlycke cycle meeting, the Neweast × Isuzu AI film, and one animation piece
(Seroflo or Menarini).

---

## B. Brand and design

### B1. 🟠 Logo in vector
**Format:** SVG preferred; AI or EPS accepted
**Why:** what is on your site today is a **350 × 100 PNG** — below 1× for modern displays.
It renders soft on every retina screen and cannot be scaled for a hero, print, or a
favicon without resampling.
**Also needed:**
- A **mono / knockout variant** for light backgrounds. The current logo's "Voice" half is
  white and disappears on anything pale.
- The **favicon** as vector or at 512 × 512 minimum.

### B2. 🟠 Design direction
Tell me which applies:
- You have **brand guidelines** (colours, typefaces, tone) → send them
- You have a **theme or reference site** you want followed → send it
- You have **nothing formal** → I propose a direction for approval

**What exists today is not a design system.** Your only distinctive value is `#d8613c`
(the CTA orange). Everything else is untouched WordPress and Twenty Twenty-Three defaults,
and six typefaces load for no reason. There is nothing to preserve, so this is a genuine
choice rather than a constraint.

### B3. 🟠 Typeface licences
If you own brand fonts, send the licences and web-font files. If not, I will select from
open-source families — no cost, no licensing risk.

### B4. 🟡 Team photographs
Six people, consistent treatment, on a plain or controlled background.
**Why:** production is bought from people. Named leads on service pages materially raise
enquiry quality.
**Current state:** no usable team photography was found in the media library.

---

## C. Access and credentials

### C1. 🔴 Vimeo account
**Why:** three things depend on it.
1. **Films not on the website.** Your library almost certainly holds work the site never
   published — the portfolio shows visible gaps, including a furniture/interior vertical
   that appears in reels but in none of the six categories.
2. **Player configuration.** Whether the account is Pro/Business decides if we can remove
   Vimeo branding, set a custom player colour, and kill the "watch on Vimeo" overlay. All
   three matter for a premium presentation.
3. **Domain privacy settings**, which decide whether embeds will play on the new domain.

### C2. 🟡 Social account URLs
**Why:** your site has a "Follow us" block, but the Facebook link has a **completely empty
`href`** and no Instagram, LinkedIn, X, YouTube or TikTok link exists anywhere in the
markup.
**Needed:** real URLs for every account you want linked, and which are actually active.
**LinkedIn matters most** — it is where B2B pharma buyers verify a vendor is real.

### C3. ⚪ Hosting and DNS
**When:** launch only, not before.
**Needed:** registrar login or someone who can change DNS, plus confirmation of the
current email setup so the cutover does not break `info@hellovoice.co.uk`.

### C4. ⚪ Analytics accounts
A Google account to own the GA4 property, plus Meta and LinkedIn ad-account access if you
want those pixels. **You currently have zero analytics of any kind**, so there is no
history to migrate — we start clean.

---

## D. Company and legal details

None of this is on your site, and all of it is needed for schema markup, the footer, and
basic credibility.

| Item | Why |
|---|---|
| Registered legal entity name | `Organization` schema, footer |
| Commercial Registration (CR) number | Credibility, enterprise buyers |
| VAT number | Invoicing, credibility |
| Registered address | `LocalBusiness` schema |
| **Correct phone numbers** | `+966 50 74488665` currently has **one digit too many** for a Saudi mobile. `+966 11 463 4518` appears on Contact but not the footer. |
| Is there a UK entity? | You use a `.co.uk` domain from a Riyadh office. If there is no UK entity, that is worth knowing before we write `hreflang` and schema. |

---

## E. Decisions only you can make

### E1. 🔴 Confirm the eight service names
I derived these from your actual work, not from your current labels:

1. Brand & Campaign Films
2. Patient Awareness & Education
3. Medical & Scientific Animation
4. Congress & Event Films
5. KOL & Testimonial Films
6. CGI, 3D & Anamorphic DOOH
7. Post Production
8. AI Production

**Approve, rename, or cut.** Everything downstream is built on this list.

### E2. 🔴 Confirm the three industries
Pharma & Healthcare · Automotive · Corporate & Industrial.
**Also decide:** the furniture / interior work — name it as a fourth, or retire it?

### E3. 🔴 Is Mondelēz International a client?
Its logo is on your homepage — misfiled as `nahdi_00000.png` — and the company is
**named nowhere on your site**. Oreo, Cadbury, Toblerone. If it is real, it belongs in the
client strip properly.

### E4. 🔴 Are the three testimonial authors real people?
Leila Mansour, Omar Haddad, Faisal Al-Qahtani — none carries a company attribution. On the
same site, `Alex Turner` (a theme demo name) renders six times on the About page.
**Those two facts together mean these quotes cannot be carried over unverified.** To a
pharma buyer, an unattributed quote on a site with visible placeholder content reads as
invented.
**Needed:** real name, real title, real company, and permission — or we cut them.

### E5. 🔴 Are the About statistics accurate?
Configured values: **1000+ minutes of content · 98% client retention · 100+ clients ·
15+ industries.** They render as `0` until JavaScript animates them, so nobody has ever
seen them to check. Confirm or correct each.

### E6. 🟠 Do you want to publish budget bands?
**My recommendation: yes.** A "from SAR X" band on each service page filters out enquiries
you cannot serve and raises the quality of the ones you get. It is the single most
effective qualifier on a B2B site.
**Your call** — some agencies refuse on principle.

### E7. 🟡 Who publishes after launch?
- **Nobody / rarely** → static site, fastest and cheapest, I hand you a simple process
- **Someone weekly** → a lightweight CMS, adds ~4 days to the build

This changes the architecture, so I need it before the build starts.

### E8. 🟠 Arabic — who writes it?
Full RTL is committed. The question is the copy.
- You write / translate in-house
- You commission a translator
- I draft it for your review

**Do not use machine translation.** In a market where Arabic is a credibility signal, bad
Arabic is worse than no Arabic.

---

## F. Content you need to supply or approve

| Content | Who | Notes |
|---|---|---|
| **Results / metrics** for each case study | You | The single most persuasive thing on the site, and the thing 95% of agency sites omit. Soft numbers work: reach, delivery in X days, Y languages, awards, repeat commissions. |
| Case study narratives | I draft, you approve | Brief → constraint → what we did → results |
| Service page copy | I draft, you approve | 8 pages × 2 languages |
| Industry page copy | I draft, you approve | 3 pages × 2 languages |
| "How We Work" — your real process | You describe, I write | MLR handling, revision rounds, turnaround, confidentiality. **This is the page that wins pharma work** and nobody else in your market has it. |
| Team bios | You | One or two lines each |
| Correct film titles | You | ~12 films are currently called `CGI`, `Video Animation`, `Bts -3`, `thumb-1` |
| Alt text | I draft | 295 images currently have **zero** |

---

## G. Commercial

| Item | Why |
|---|---|
| **Build budget** | Determines scope of custom work vs. sensible defaults |
| **Target launch date** | Working estimate is 6–8 weeks from unblock, sequential from clearance |
| **Who signs off** | One named decision-maker. Design by committee doubles the timeline. |
| **Hosting budget** | Static hosting is roughly free–$20/mo; a CMS raises it |

---

## The short version

If you only do four things this week:

1. **Export the form submissions** — irreplaceable, lost on decommission
2. **Verify Search Console** — 10 minutes, and the clock only starts when you do
3. **Send the clearance requests** — the longest pole in the project by weeks
4. **Send the logo in vector** — nothing visual starts without it

Then answer **E1–E5**, and the build is unblocked.
