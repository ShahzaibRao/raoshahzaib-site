# Rao Shahzaib — raoshahzaib.site

Personal portfolio and blog hub for the root domain **raoshahzaib.site**.
Rao Shahzaib, DevOps Engineer (Kubernetes, Docker, CI/CD, AWS, Ansible).

Built with [Astro](https://astro.build) (static site, no frameworks in the
browser) and hosted on **Cloudflare Pages** — chosen for its caching, CDN
and features. (GitHub Pages was considered and dropped.) The old Python
generator (`build_site.py`) and the old Cloudflare workflow are gone; the
Astro project in this repo is the only source of truth.

## Structure

- `src/pages/` — Home, About, Projects, Blog hub, Contact, Privacy,
  Terms, 404 (`src/pages/404.astro`).
- `src/pages/blog/[slug].astro` — template for the blog articles.
- `src/content/blog/*.md` — the 5 original DevOps articles (content
  collection; each file's frontmatter holds its `title`, `description`
  and `slug`).
- `src/layouts/BaseLayout.astro` — header nav, footer, SEO meta,
  canonical, Open Graph / Twitter tags, JSON-LD (WebSite everywhere,
  Person on the homepage).
- `src/styles/global.css` — the whole stylesheet (system fonts only).
- `public/` — `robots.txt` and `ads.txt`. Astro copies these into the
  build output untouched. There is no `CNAME` file: on Cloudflare Pages
  the custom domain is set in the dashboard, not via a file.
- `astro.config.mjs` — `site: https://raoshahzaib.site` + sitemap
  integration (generates `sitemap-index.xml`).

## Develop locally

```bash
npm install
npm run dev
```

## Deploy

Push to `main` and GitHub Actions builds the site and deploys it to
Cloudflare Pages (project `raoshahzaib-site`). The first run creates the
Pages project. No zip upload, no manual step.

### One-time setup (owner does this once)

1. Cloudflare API token: dashboard → My Profile → API Tokens →
   Create Token → custom token with **Account → Cloudflare Pages → Edit**
   (plus Account → Account → Read if shown). Copy the token.
2. Cloudflare Account ID: dashboard home, right sidebar (or the ID in
   the dashboard URL).
3. GitHub repo → Settings → Secrets and variables → Actions → New
   repository secret, add both:
   - `CLOUDFLARE_API_TOKEN` = the token from step 1
   - `CLOUDFLARE_ACCOUNT_ID` = the ID from step 2
4. Custom domain: Cloudflare dashboard → Workers & Pages →
   `raoshahzaib-site` → Custom domains → Set up a custom domain →
   `raoshahzaib.site`. This replaces the root domain's current DNS
   record (it points at a Cloudflare Tunnel today, which is why the
   root returns 530). Subdomains (`webmail`, `blog`, `docker`, `cv`)
   are separate records and are not affected.
5. Push any commit to `main` (or run the workflow manually) and check
   https://raoshahzaib.site/ loads.

Until the two secrets are added, the workflow fails at the deploy step.
Add the secrets, then re-run it from the Actions tab.

## AdSense

After the root site is live, add the bare domain `raoshahzaib.site`
in Google AdSense (subdomains cannot be added on their own; an
approved root domain covers its subdomains). When AdSense gives the
publisher ID, put the publisher line in `public/ads.txt` and push —
the next deploy publishes it.
