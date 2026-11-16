# Rao Shahzaib — raoshahzaib.site

Personal portfolio and blog hub for the root domain **raoshahzaib.site**.
Rao Shahzaib, DevOps Engineer (Kubernetes, Docker, CI/CD, AWS, Ansible).

Static site, system fonts only, no frameworks, no external assets.

## Structure

- `build_site.py` — the whole site lives here. It generates `build/`
  (pages as `pagename.html` AND `pagename/index.html` for clean
  trailing-slash URLs, plus `robots.txt`, `sitemap.xml`, `ads.txt`).
  Edit the content in this file, never in `build/` — it is wiped and
  regenerated on every build.
- `.github/workflows/deploy.yml` — CI/CD: push to `main` builds the
  site and deploys it to Cloudflare Pages.

## Build locally

```bash
python3 build_site.py
python3 -m http.server 8000 --directory build
```

## Deploy

Push to `main` and GitHub Actions deploys to Cloudflare Pages
(project `raoshahzaib-site`). The first run creates the Pages project.
Hosting is **Cloudflare Pages, not GitHub Pages**.

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

## AdSense

After the root site is live, add the bare domain `raoshahzaib.site`
in Google AdSense (subdomains cannot be added on their own; an
approved root domain covers its subdomains). When AdSense gives the
verification code / publisher ID, put the publisher line in `ads.txt`
in `build_site.py` and push — the next deploy publishes it.
