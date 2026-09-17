# HelloVoice — website

The HelloVoice studio website: a static site, no framework and no server-side code.

| Folder | What it is |
|---|---|
| `site/` | **The website.** Deploy this folder as-is. |
| `build/` | Python scripts that regenerate `site/` (`python3 build/clone.py`). |
| `content/` | Client data the build reads (projects, clients, technology, influencer posts). |
| `docs/` | Design notes and the client review lists. |

## Preview locally

```bash
python3 build/serve.py 8811
```

Then open http://localhost:8811/.

## Deploy

The site uses root-relative paths (`/assets/...`), so host it at the root of a domain.

- **Netlify:** import the repo; `netlify.toml` already sets the publish folder to `site`.
- **Vercel:** import the repo; `vercel.json` already sets the output folder to `site` with no build step.
- **Any static host / nginx:** upload the contents of `site/`. `404.html` is the not-found page.

Nothing needs to be built on the host — `site/` is committed ready to serve.

## Notes

- The **creator catalogue** is a separate app at https://influencer-catalogue.hellovoice.co.uk (it needs its own API); the site links to it.
- The home hero plays `site/assets/video/hero-loop.mp4` (phones: `hero-loop-m.mp4`). Replace those files to change the hero film.
- The private creator roster (`content/catalogue_private.json`) is not in this repository.
- `site/assets/ref/` holds the Webflow template's own assets the design is built on; check its licence before a public launch.
