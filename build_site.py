#!/usr/bin/env python3
"""Build the static portfolio site for raoshahzaib.site (root domain).
Generates ~/workspace/root-portfolio/build/ : pages as pagename.html AND
pagename/index.html (clean trailing-slash URLs), plus robots/sitemap/ads.txt.
Facts are grounded ONLY in the brief + the live CV (cv.raoshahzaib.site).
"""
import pathlib, shutil, re

OUT = pathlib.Path(__file__).resolve().parent / "build"  # repo-relative: works locally and in CI
SITE = "https://raoshahzaib.site"

CSS = """/* Rao Shahzaib — raoshahzaib.site. System fonts only, no external assets. */
:root{--ink:#1a1a1a;--muted:#555;--accent:#0b5fff;--line:#e5e5e5;--bg:#fff;--soft:#f7f9ff}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;font-size:17px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:760px;margin:0 auto;padding:0 24px}
header.site{border-bottom:1px solid var(--line);padding:18px 0}
header.site .wrap{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.brand{font-size:1.15rem;font-weight:700;color:var(--ink)}
.brand small{display:block;font-size:.8rem;font-weight:400;color:var(--muted)}
nav.main a{margin-left:18px;font-size:.95rem}
nav.main a:first-child{margin-left:0}
main{padding:36px 0 56px}
h1{font-size:2rem;line-height:1.25;letter-spacing:-.5px;margin-bottom:14px}
h2{font-size:1.3rem;margin:32px 0 10px}
h3{font-size:1.1rem;margin:24px 0 8px}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px 22px}
li{margin-bottom:6px}
.lede{font-size:1.12rem;color:#333}
.muted{color:var(--muted)}
.hero{padding:28px 0 8px}
.hero .tagline{font-size:1.15rem;color:var(--muted);margin-top:4px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
.card{border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.card h3{margin:0 0 6px;font-size:1.05rem}
.card p{font-size:.95rem;margin:0 0 8px}
.card .tech{font-size:.85rem;color:var(--muted)}
.skills{display:grid;grid-template-columns:1fr 1fr;gap:8px 24px;margin:12px 0 20px;font-size:.95rem}
.skills b{display:block;font-size:.85rem;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}
.cta{background:var(--soft);border:1px solid #dbe6ff;border-radius:10px;padding:20px 22px;margin:28px 0}
.timeline{list-style:none;margin:0 0 14px}
.timeline li{margin-bottom:14px;padding-left:0}
.timeline .when{font-weight:700}
article.post p{margin-bottom:16px}
article.post .meta{color:var(--muted);font-size:.9rem;margin-bottom:20px}
footer.site{border-top:1px solid var(--line);padding:22px 0 34px;font-size:.9rem;color:var(--muted)}
footer.site nav a{margin-right:14px}
footer.site p{margin:6px 0}
@media (max-width:640px){.cards,.skills{grid-template-columns:1fr}h1{font-size:1.6rem}body{font-size:16px}}
"""

NAV = ('<a href="/">Home</a><a href="/about/">About</a><a href="/projects/">Projects</a>'
       '<a href="/blog/">Blog</a><a href="/contact/">Contact</a>')

FOOTER = ('<footer class="site"><div class="wrap"><nav>' + NAV +
          '<a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></nav>'
          '<p>Copyright &copy; 2023-2026 Rao Shahzaib &middot; '
          '<a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a></p>'
          '<p>DevOps Engineer &middot; Rahim Yar Khan, Pakistan &middot; Working remotely</p>'
          '</div></footer>')

HEADER = ('<header class="site"><div class="wrap">'
          '<a class="brand" href="/">Rao Shahzaib<small>DevOps Engineer</small></a>'
          '<nav class="main">' + NAV + '</nav></div></header>')

WEBSITE_LD = ('{"@context":"https://schema.org","@type":"WebSite",'
              '"url":"https://raoshahzaib.site/","name":"Rao Shahzaib",'
              '"description":"Rao Shahzaib — DevOps Engineer. Kubernetes, Docker, CI/CD, GitOps.",'
              '"inLanguage":"en"}')

PERSON_LD = ('{"@context":"https://schema.org","@type":"Person",'
             '"name":"Rao Shahzaib","jobTitle":"DevOps Engineer",'
             '"url":"https://raoshahzaib.site/",'
             '"email":"contact@raoshahzaib.site",'
             '"address":{"@type":"PostalAddress","addressLocality":"Rahim Yar Khan",'
             '"addressCountry":"PK"},'
             '"sameAs":["https://www.linkedin.com/in/rao-shahzaib/",'
             '"https://github.com/ShahzaibRao",'
             '"https://blog.raoshahzaib.site","https://docker.raoshahzaib.site",'
             '"https://cv.raoshahzaib.site"]}')

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__CANON__">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__CANON__">
<meta property="og:site_name" content="Rao Shahzaib">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESC__">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">__JSONLD__</script>
</head>
<body>
__HEADER__
<main><div class="wrap">
__BODY__
</div></main>
__FOOTER__
</body>
</html>
"""

def page(title, desc, canon, body, extra_ld=""):
    ld = WEBSITE_LD + ("," + extra_ld if extra_ld else "")
    # JSON-LD: WebSite on every page; Person added on homepage via extra_ld
    html = (TEMPLATE
            .replace("__TITLE__", title)
            .replace("__DESC__", desc)
            .replace("__CANON__", canon)
            .replace("__JSONLD__", "[" + ld + "]")
            .replace("__HEADER__", HEADER)
            .replace("__BODY__", body)
            .replace("__FOOTER__", FOOTER))
    assert html.count("<h1") == 1, f"h1 count != 1 on {canon}"
    assert "lorem" not in html.lower() and "TODO" not in html
    return html

def write(rel, html):
    """Write pagename.html AND pagename/index.html (clean trailing-slash URLs)."""
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    if rel.endswith(".html") and rel != "index.html" and rel != "404.html":
        d = OUT / rel[:-5] / "index.html"
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(html, encoding="utf-8")

# ---------------------------------------------------------------- pages ----

HOME_BODY = """<section class="hero">
<h1>Rao Shahzaib</h1>
<p class="tagline">DevOps Engineer &mdash; I build reliable infrastructure: Kubernetes platforms, GitOps pipelines, and systems that recover when things break.</p>
<p class="lede">I am a DevOps engineer based in Rahim Yar Khan, Pakistan, working remotely. I have spent the last three years building and operating real systems &mdash; a production-style Kubernetes platform on Oracle Cloud, a license-key SaaS, a social fitness app, and a permanent email service &mdash; and I write about what I learn along the way.</p>
<p><a href="/about/">More about me &rarr;</a> &nbsp; <a href="/contact/">Get in touch &rarr;</a></p>
</section>

<h2>What I do</h2>
<div class="skills">
<div><b>Containers &amp; Orchestration</b>Docker, Kubernetes (k3s)</div>
<div><b>CI/CD &amp; GitOps</b>Jenkins, GitHub Actions, ArgoCD</div>
<div><b>Infrastructure as Code</b>Terraform, Ansible</div>
<div><b>Cloud</b>AWS, Oracle Cloud (OCI), DigitalOcean</div>
<div><b>Secrets, TLS &amp; DNS</b>External Secrets Operator, OCI Vault, cert-manager, Cloudflare</div>
<div><b>Monitoring &amp; Backup</b>Prometheus, Grafana, Alertmanager, Velero</div>
<div><b>Linux &amp; Networking</b>Administration, iptables, NAT, NFS, RAID, Traefik</div>
<div><b>Virtualization &amp; Web</b>Proxmox (2-node cluster), Nginx, Apache</div>
</div>

<h2>Featured projects</h2>
<div class="cards">
<div class="card"><h3>Production Kubernetes Platform</h3><p>A 2-node k3s cluster on OCI Always Free with ArgoCD GitOps, Velero disaster recovery, and Prometheus/Grafana monitoring. A full restore drill passed: a deleted namespace came back with pods Running.</p><p class="tech">k3s &middot; Terraform &middot; ArgoCD &middot; Velero &middot; OCI</p></div>
<div class="card"><h3>LifeQuest</h3><p>A social health and fitness app with a GPS territory-capture game: walk, capture hexes on a map, challenge friends, climb the leaderboard.</p><p class="tech">React Native &middot; Expo &middot; FastAPI &middot; PostgreSQL + PostGIS</p><p><a href="https://github.com/ShahzaibRao/lifequest">github.com/ShahzaibRao/lifequest &rarr;</a></p></div>
<div class="card"><h3>DownPilot</h3><p>An Electron desktop downloader with a Go sidecar: paste a link, pick a quality, and download videos, playlists, and creator content.</p><p class="tech">Electron &middot; Go &middot; yt-dlp</p><p><a href="https://github.com/ShahzaibRao/downpilot">github.com/ShahzaibRao/downpilot &rarr;</a></p></div>
<div class="card"><h3>CreatorWatch</h3><p>A license-key SaaS: accounts, encrypted license keys, and a validation API that desktop apps call to check a license. Deployed on the OCI platform over HTTPS.</p><p class="tech">FastAPI &middot; PostgreSQL &middot; Fernet &middot; Docker</p></div>
<div class="card"><h3>Rao Shahzaib Mail</h3><p>A free permanent email service. One account creates up to 100 email addresses on @raoshahzaib.site &mdash; addresses that never expire. Receive-only, running on Cloudflare for three years.</p><p class="tech">Cloudflare Workers &middot; Pages &middot; D1</p><p><a href="https://webmail.raoshahzaib.site">webmail.raoshahzaib.site &rarr;</a></p></div>
<div class="card"><h3>Video Ad Editor</h3><p>An offline-first desktop app that inserts ad videos mid-roll into a primary video and renders one finished MP4.</p><p class="tech">Rust &middot; Slint &middot; FFmpeg</p></div>
</div>
<p><a href="/projects/">All projects &rarr;</a></p>

<h2>From the blog</h2>
<ul>
<li><a href="/blog/gitops-with-argocd/">GitOps with ArgoCD: why Git is the source of truth</a></li>
<li><a href="/blog/docker-multi-stage-builds/">Smaller Docker images with multi-stage builds</a></li>
<li><a href="/blog/cicd-pipeline-design/">Designing a CI/CD pipeline that fails safe</a></li>
<li><a href="/blog/kubernetes-backup-disaster-recovery/">Kubernetes backups and disaster recovery: what actually restores</a></li>
<li><a href="/blog/running-your-own-email/">Running your own email service: what three years taught me</a></li>
</ul>
<p>I also write longer technical pieces at <a href="https://blog.raoshahzaib.site">blog.raoshahzaib.site</a> and <a href="https://docker.raoshahzaib.site">docker.raoshahzaib.site</a>.</p>

<div class="cta">
<h2 style="margin-top:0">Open to remote DevOps roles</h2>
<p>I am looking for a remote DevOps role in a strong engineering team. If you are hiring, or you want to talk about Kubernetes, CI/CD, or GitOps, write to me.</p>
<p><a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a> &nbsp;&middot;&nbsp; <a href="https://cv.raoshahzaib.site">View my CV</a></p>
</div>
"""

ABOUT_BODY = """<h1>About</h1>
<p class="lede">I am Rao Shahzaib, a DevOps engineer from Rahim Yar Khan, Pakistan. I learn by building: my Kubernetes platform, my SaaS projects, and my content all come from systems I actually run.</p>
<p>I did not come to DevOps through a single job title. I started with Linux administration, ran my own business for two years, then worked as a freelance DevOps engineer from January 2023 to September 2025. Along the way I kept a habit that still defines how I work: if I cannot explain a system, I have not understood it yet. That is why I write &mdash; long technical articles on networking, Docker, and Kubernetes, on my blogs and on LinkedIn.</p>

<h2>Experience</h2>
<ul class="timeline">
<li><span class="when">2017&ndash;2019 &mdash; MCS, NCBA&amp;E, Rahim Yar Khan.</span> Master&rsquo;s in Computer Science at the National College of Business Administration &amp; Economics.</li>
<li><span class="when">Linux Administrator.</span> Worked as a Linux administrator at a local software house, running Linux servers and networking day to day.</li>
<li><span class="when">Own business, 2 years.</span> Ran my own business for two years, which taught me the other side of technology: customers, costs, and keeping a service up.</li>
<li><span class="when">Jan 2023 &ndash; Sep 2025 &mdash; Freelance DevOps Engineer (remote).</span> Built CI/CD automation with Jenkins and GitHub Actions, containerized apps with Docker on Kubernetes, automated provisioning with Ansible, and deployed Nginx and Apache on Linux and DigitalOcean. Diagnosed infrastructure problems across Linux, NFS, RAID, and thin provisioning.</li>
<li><span class="when">2023 &ndash; present &mdash; Content creation.</span> In-depth technical write-ups on DevOps and infrastructure, including a long-running series on networking internals: iptables, NAT, and Docker/Kubernetes networking.</li>
<li><span class="when">Sep 2026 &ndash; present &mdash; Production Kubernetes platform.</span> A 2-node k3s cluster on OCI Always Free, run as a production-style platform with ArgoCD GitOps, Velero disaster recovery, and Prometheus/Grafana monitoring.</li>
<li><span class="when">Oct 2026 &ndash; present &mdash; CreatorWatch Cloud.</span> A license-key SaaS backend with a web UI and admin panel, deployed on the OCI platform.</li>
</ul>

<h2>How I work</h2>
<ul>
<li><strong>Official tooling first.</strong> I learn a tool the way its makers intend, and only customize after I understand it.</li>
<li><strong>Security shift-left.</strong> Secrets never live in code or in cluster manifests. They live in a vault and are delivered by External Secrets. Security is part of the design, not a step at the end.</li>
<li><strong>Git is the source of truth.</strong> If a change is not in Git, it does not exist. Deploys happen from Git, rollbacks are a revert, and drift gets detected and fixed.</li>
<li><strong>Verify everything.</strong> A backup is only real after a restore drill. A pipeline is only green after a real run. I test what I build and measure what I claim.</li>
</ul>
<p>I am currently open to remote DevOps roles. My CV is at <a href="https://cv.raoshahzaib.site">cv.raoshahzaib.site</a>, and you can reach me at <a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a>.</p>
"""

PROJECTS_BODY = """<h1>Projects</h1>
<p class="lede">Systems I built and operate. Each one taught me something I now use on the next one.</p>

<h2>Production Kubernetes Platform &mdash; OCI Always Free</h2>
<p>A production-style platform on two OCI Always Free ARM VMs: a 2-node k3s cluster provisioned with modular Terraform, with state in Cloudflare R2. ArgoCD runs app-of-apps GitOps through an ApplicationSet that manages cert-manager, External Secrets, monitoring, Velero, and the app workloads. Daily GitHub Actions drift detection keeps the cluster honest. Disaster recovery is Velero daily backups to R2 with a 30-day retention, and it is proven, not assumed: a full restore drill deleted a namespace and brought it back with pods Running. Secrets moved from Sealed Secrets to External Secrets Operator plus OCI Vault, TLS is a wildcard certificate from cert-manager with Cloudflare DNS-01, and traffic enters through an OCI load balancer with health checks.</p>
<p class="muted">k3s &middot; Terraform &middot; ArgoCD &middot; Velero &middot; Prometheus &middot; Grafana &middot; OCI &middot; Cloudflare R2</p>

<h2>LifeQuest</h2>
<p>A social health and fitness app: meals and calories, steps and distance, sleep, exercise, and water, plus a GPS territory-capture game. Walk a hex on the map and capture it; friends can challenge your territory; a weekly leaderboard ranks everyone. The app is one React Native and Expo codebase for iPhone and Android, with MapLibre and OpenStreetMap, H3 hexes, and a FastAPI backend on PostgreSQL with PostGIS. It is offline-first: sessions are saved on the device and synced when the connection returns.</p>
<p><a href="https://github.com/ShahzaibRao/lifequest">github.com/ShahzaibRao/lifequest &rarr;</a></p>
<p class="muted">React Native &middot; Expo &middot; FastAPI &middot; PostgreSQL + PostGIS &middot; H3 &middot; Docker</p>

<h2>DownPilot</h2>
<p>An Electron desktop app for downloading videos, with a Go sidecar doing the heavy work. Paste a link and it detects whether it is a single video, a playlist, or a channel; pick a quality, queue up to four downloads at once, and keep a history. A prospect mode watches creators and downloads new content automatically. Free for local use; cloud features are the paid tier.</p>
<p><a href="https://github.com/ShahzaibRao/downpilot">github.com/ShahzaibRao/downpilot &rarr;</a></p>
<p class="muted">Electron &middot; Go &middot; yt-dlp &middot; Windows-first</p>

<h2>CreatorWatch</h2>
<p>A license-key SaaS. The desktop product stays local; the cloud side is accounts, licenses, and a validation API. Keys are Fernet-encrypted, the web UI and admin panel manage users, licenses, devices, and revenue, and the backend runs on PostgreSQL (SQLite as a fallback). Multi-architecture CI builds versioned images to Docker Hub, and the service is deployed through ArgoCD on the OCI platform over HTTPS. The repository is open source.</p>
<p class="muted">FastAPI &middot; PostgreSQL &middot; Fernet &middot; Docker &middot; ArgoCD</p>

<h2>Rao Shahzaib Mail &mdash; permanent email</h2>
<p>A free permanent email service, running for three years. One account creates up to 100 email addresses on @raoshahzaib.site, and none of them expire &mdash; the opposite of a throwaway inbox. It is receive-only by design, hosted on Cloudflare Workers, Pages, and D1. There is a second instance at <a href="https://inbox.crackone.org">inbox.crackone.org</a> that works the same way.</p>
<p><a href="https://webmail.raoshahzaib.site">webmail.raoshahzaib.site &rarr;</a></p>
<p class="muted">Cloudflare Workers &middot; Pages &middot; D1</p>

<h2>Video Ad Editor</h2>
<p>An offline-first desktop app that inserts ad videos mid-roll into a primary video and renders one finished MP4. Built for the machine it runs on: no cloud, no upload, just the file and the result.</p>
<p class="muted">Rust &middot; Slint &middot; FFmpeg</p>

<h2>Writing &amp; study</h2>
<p>Alongside the code, I keep two long-running study threads: a system-design series covering indexing, replication, sharding, and Kafka, and coding lessons built around a small FastAPI link shortener. The notes from both land on <a href="https://blog.raoshahzaib.site">blog.raoshahzaib.site</a> and <a href="https://docker.raoshahzaib.site">docker.raoshahzaib.site</a>.</p>
"""

CONTACT_BODY = """<h1>Contact</h1>
<p class="lede">The fastest way to reach me is email. I read everything and reply to anything about DevOps work, remote roles, or my projects.</p>
<p><strong>Email:</strong> <a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a></p>
<p><strong>CV:</strong> <a href="https://cv.raoshahzaib.site">cv.raoshahzaib.site</a></p>
<p><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/rao-shahzaib/">linkedin.com/in/rao-shahzaib</a></p>
<p><strong>GitHub:</strong> <a href="https://github.com/ShahzaibRao">github.com/ShahzaibRao</a></p>
<p><strong>Blogs:</strong> <a href="https://blog.raoshahzaib.site">blog.raoshahzaib.site</a> &middot; <a href="https://docker.raoshahzaib.site">docker.raoshahzaib.site</a></p>
<p><strong>Location:</strong> Rahim Yar Khan, Pakistan &mdash; working remotely (Asia/Karachi).</p>
<div class="cta">
<h2 style="margin-top:0">Open to remote DevOps roles</h2>
<p>I am looking for a remote DevOps role in a strong engineering team &mdash; junior roles included. My experience is freelance DevOps from January 2023 to September 2025, plus the platforms on my <a href="/projects/">projects page</a>, which I build and operate myself. If you are hiring, send me the role and I will tell you honestly whether I fit it.</p>
</div>
"""

PRIVACY_BODY = """<h1>Privacy Policy</h1>
<p class="muted">Last updated: 16 November 2026</p>
<p>This is a personal portfolio website. It is a static site: there are no user accounts, no logins, and no forms that collect your data.</p>
<h2>What I collect</h2>
<p>I do not collect personal data through this site. There is no analytics, no tracking code, and no advertising on this site yet. If this site is later approved for Google AdSense, that section will be updated and the ads.txt file will carry the publisher line.</p>
<h2>Hosting</h2>
<p>This site is served by Cloudflare Pages. Cloudflare may keep standard server logs (such as your IP address and the pages you request) as part of serving the site, under Cloudflare&rsquo;s own privacy policy. I do not see or use those logs to identify you.</p>
<h2>Links to other sites</h2>
<p>This site links to my other properties (my blogs, my CV, my GitHub and LinkedIn profiles, and my email service). Those sites have their own privacy practices; this policy covers only raoshahzaib.site.</p>
<h2>Contact</h2>
<p>If you email me, I use your email address only to reply to you. I do not share it, sell it, or add it to any list. Questions about this policy: <a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a>.</p>
"""

TERMS_BODY = """<h1>Terms of Service</h1>
<p class="muted">Last updated: 16 November 2026</p>
<p>This website is the personal portfolio of Rao Shahzaib. It describes my work, my projects, and what I have learned building them.</p>
<h2>Content</h2>
<p>Everything on this site is my own work, written from my own experience, unless a page says otherwise. The articles are educational: they describe what worked for me on my own systems. They are not a guarantee that the same approach will work for yours. Test changes on your own systems before you apply them to anything that matters.</p>
<h2>Use of this site</h2>
<p>You may read, link to, and share pages from this site. Do not copy whole articles and republish them as your own. If you quote a short passage, credit the source.</p>
<h2>No warranties</h2>
<p>This site is provided as-is, without warranties of any kind. I do my best to keep it accurate, but I may update or correct pages at any time without notice.</p>
<h2>Links</h2>
<p>This site links to third-party sites (GitHub, LinkedIn, my blogs, and my other services). I am not responsible for their content or their availability.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:contact@raoshahzaib.site">contact@raoshahzaib.site</a>.</p>
"""

NOTFOUND_BODY = """<h1>Page not found</h1>
<p class="lede">The page you are looking for does not exist, or it has moved.</p>
<p>Try one of these instead:</p>
<ul>
<li><a href="/">Home</a></li>
<li><a href="/about/">About</a></li>
<li><a href="/projects/">Projects</a></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/contact/">Contact</a></li>
</ul>
"""

# --------------------------------------------------------------- articles ----

ARTICLES = [
{
 "slug": "gitops-with-argocd",
 "title": "GitOps with ArgoCD: why Git is the source of truth",
 "desc": "GitOps means the cluster follows Git, not the other way round. How ArgoCD, drift detection, and pull-request reviews keep a real Kubernetes platform honest.",
 "body": """
<p class="meta">By Rao Shahzaib &middot; DevOps</p>
<p>GitOps is a simple idea with a strict rule: the desired state of your cluster lives in Git, and nothing else is allowed to change it. If a change is not in Git, it does not exist. I run a two-node k3s cluster on Oracle Cloud this way. Without it, a cluster becomes a pile of commands somebody once typed into a terminal.</p>
<p>The problem GitOps solves is drift. A cluster changes all the time: someone scales a deployment by hand during an incident, a dashboard edit tweaks a resource, a Helm upgrade leaves a value behind. None of those changes are recorded anywhere. Six months later, nobody can say why the cluster looks the way it does, and rebuilding it is impossible because the real configuration only exists inside the cluster. GitOps turns that around. ArgoCD watches a Git repository and continuously compares it with the live cluster. When they differ, ArgoCD shows the drift and, depending on how you configure it, syncs it back. The repository becomes the one place you can read to know what should be running.</p>
<p>The workflow is ordinary Git workflow, and that is the point. A change is a pull request. Somebody reviews it. It merges, ArgoCD notices, and the cluster moves to the new state. A bad change is a revert, and the revert is itself a reviewed change. There is no separate deployment step to forget, and no one needs cluster credentials to ship a change &mdash; they need repository access and a review. That separation matters for security too: the cluster only ever pulls from Git, so a compromised laptop cannot push straight into production.</p>
<p>On my own platform I use the app-of-apps pattern. One root ArgoCD application points at a repository folder, and it creates the child applications: cert-manager for TLS, External Secrets for secrets, the monitoring stack, Velero for backups, and the application workloads. Adding a new component is adding a file to Git, not running a command. A daily GitHub Actions job checks for drift, so even a change that ArgoCD would sync away gets noticed and recorded.</p>
<p>Secrets deserve a special note, because they are the one thing that must never go into Git. I keep them in OCI Vault and deliver them into the cluster with the External Secrets Operator. Git holds the reference &mdash; which secret, from where &mdash; and the value never appears in a repository. If you put a password in Git, assume it is public forever.</p>
<p>GitOps is not magic. It will not fix a bad application, and it will not stop you from merging a bad manifest. What it gives you is a record: every change has an author, a review, and a time. When something breaks at 2 a.m., you do not guess what changed. You read the log, find the commit, and revert it. That is the whole argument. The cluster is a machine; Git is its memory.</p>
""",
},
{
 "slug": "docker-multi-stage-builds",
 "title": "Smaller Docker images with multi-stage builds",
 "desc": "A Dockerfile that ships its compiler, its cache, and its history is slow to pull and easy to attack. Multi-stage builds keep the build tools out of the final image.",
 "body": """
<p class="meta">By Rao Shahzaib &middot; DevOps</p>
<p>Most Docker images are bigger than they need to be. The usual reason is simple: the Dockerfile installs the compiler, the test tools, and the package cache, builds the application, and then ships all of it. The final image carries the entire workshop that built it. That costs time on every pull, disk on every node, and attack surface on every container.</p>
<p>A multi-stage build fixes this by splitting the Dockerfile into stages. The first stage is the workshop: it has the compiler and the dependencies, and it produces the application binary. The second stage is the shipping box: it starts from a small base image and copies only the finished binary into it. Nothing else travels. A Go service that needed a full Go toolchain to build can ship in a minimal image with one binary. A Python application can build its wheels in one stage and install only the wheels in the next, leaving pip and the build headers behind.</p>
<p>The pattern looks like this in practice. Stage one is named <code>build</code>, and it runs the compile step. Stage two starts from a slim base, copies the artifact out of stage one with <code>COPY --from=build</code>, and sets the entrypoint. The two stages share nothing except the artifact you choose to copy. If you need a shell for debugging, use a debug variant of the base image rather than stuffing tools into production. On my own services I build both: a slim image for production and a debug image with a shell for the staging environment, from the same Dockerfile.</p>
<p>Order matters for speed as much as size. Docker caches each layer, and a cache miss rebuilds everything below it. So copy the dependency files first and install dependencies before copying the source code. That way a one-line code change reuses the cached dependency layer instead of reinstalling the world. A <code>.dockerignore</code> file helps too: keep <code>.git</code>, test data, and local configuration out of the build context entirely, so the daemon never sends them in the first place.</p>
<p>Pin your base images. <code>python:3.13-slim</code> today is not the same image it was last month, and an unpinned tag can change under you without a word. A digest pin makes the build reproducible: the same input gives the same image, and an upgrade is a deliberate commit, not an accident. The same goes for the packages you install inside the image. Reproducible builds are what let you answer the question &ldquo;what changed?&rdquo; with a commit hash instead of a shrug.</p>
<p>Finally, measure. Run <code>docker images</code> before and after, and look at the number. A service that went from hundreds of megabytes to tens of megabytes pulls faster on every node, starts faster on every restart, and presents a smaller target. Small images are not a vanity metric. They are what makes the rest of the pipeline &mdash; the registry, the pull, the rollout &mdash; cheap enough to do often.</p>
""",
},
{
 "slug": "cicd-pipeline-design",
 "title": "Designing a CI/CD pipeline that fails safe",
 "desc": "A good pipeline is not the fastest one. It is the one that refuses to ship a broken build, keeps its secrets out of reach, and can always roll back.",
 "body": """
<p class="meta">By Rao Shahzaib &middot; DevOps</p>
<p>A CI/CD pipeline has one job that matters more than speed: it must refuse to ship a broken build. Everything else &mdash; the caching, the parallel jobs, the dashboard &mdash; is secondary. If a pipeline can deploy a failing build, it will, at the worst possible moment. So I design pipelines around that one rule, and every other choice follows from it.</p>
<p>The first decision is to separate building from deploying. The CI job builds the code, runs the tests, scans the image, and pushes it to the registry with a digest pin &mdash; a unique hash, not a moving tag like <code>latest</code>. Nothing in that job touches the cluster. Deployment is a second, separate act: a change to a Git repository that says &ldquo;run this digest.&rdquo; The cluster, or the GitOps controller watching the repository, picks it up from there. If the build fails, there is no new digest and nothing to deploy. If the deploy fails, the build is untouched and the previous digest is still right there in Git.</p>
<p>The second decision is that every gate is a real gate. Tests run on every pull request, and a red build blocks the merge &mdash; no overrides, no &ldquo;merge it and fix it later.&rdquo; A static analysis scan runs on the code, and an image scan runs on the built image, and both must pass before the image is pushed. These gates feel slow the first week, then disappear into the background. What they replace is the 2 a.m. page that says a bad image is in production.</p>
<p>The third decision is about secrets. A pipeline needs credentials: registry logins, cloud keys, deployment tokens. Those belong in the CI system&rsquo;s secret store, injected at run time, and nowhere else. They never appear in a log, never sit in a repository, and never get baked into an image. If a secret leaks into a log, rotate it and fix the logging. On my own projects the rule is absolute: no hardcoded passwords anywhere, in any file, for any reason.</p>
<p>The fourth decision is the rollback plan, written before the deploy, not after the incident. A deploy that cannot be undone is a gamble. With digest pins and Git as the source of truth, a rollback is a revert: the previous known-good digest goes back into the repository and the cluster returns to it. I also keep deployments small and frequent. A small change that breaks something is easy to find; a week of changes shipped at once is a mystery.</p>
<p>Finally, the pipeline should tell you when it fails, loudly. A failed job that nobody notices is worse than no pipeline at all, because it creates the illusion of safety. Failures go to a channel somebody reads, and a failed deploy blocks the next one. A pipeline that fails safe is a pipeline you can trust &mdash; and trust is the only reason to automate deployments at all.</p>
""",
},
{
 "slug": "kubernetes-backup-disaster-recovery",
 "title": "Kubernetes backups and disaster recovery: what actually restores",
 "desc": "A backup you have never restored is a hope, not a plan. Velero, a real restore drill, and the gaps most people only find during an incident.",
 "body": """
<p class="meta">By Rao Shahzaib &middot; DevOps</p>
<p>Everyone has backups. Far fewer people have restores. A backup job that runs every night and reports success tells you almost nothing, because the only question that matters is whether the backup can bring the system back. I learned this by testing it: on my own two-node Kubernetes cluster I run Velero backups every day, and I proved they work by deleting a namespace and restoring it. The pods came back Running. Until that drill, the backups were a hope, not a plan.</p>
<p>The first thing to understand is what a Kubernetes backup actually has to capture. A cluster is not a single database. It is etcd state, application manifests, secrets, persistent volume data, and the custom resources that operators create. Backing up etcd alone gives you the state but not the data on disk. Snapshotting volumes alone gives you the data but not the objects that point at it. Velero covers the middle ground: it backs up the Kubernetes objects and, with the right configuration, the persistent volumes behind them. My backups go to Cloudflare R2, off the cluster and off the cloud account that runs it, with a 30-day retention. A backup that lives on the same infrastructure it protects is not a backup.</p>
<p>The second thing is the restore drill, and it has to be a real one. A drill is not reading the Velero logs. It is picking a namespace, deleting it, restoring it from the backup, and checking that the application actually works &mdash; not just that the pods exist, but that they serve traffic and read their data. I run this kind of check because the gaps only show up during a restore. The common ones are secrets that were never in the backup because they were created by hand, custom resources that the backup skipped, and volume snapshots that were never taken because the storage class was not configured for them. Every one of those is a five-minute fix before an incident and a multi-hour problem during one.</p>
<p>Retention and schedule deserve the same honesty. Daily backups with a 30-day window mean I can lose a day of work at most, and I can go back a month. That is a deliberate trade: more frequent backups cost more storage and more time, and the right answer depends on how much data you can afford to lose. Whatever you choose, write it down. A recovery plan that only exists in someone&rsquo;s head is not a plan.</p>
<p>The last piece is the runbook. When the cluster is down, nobody should be improvising. The runbook says where the backups live, which command restores them, in what order the namespaces come back, and how you verify each one. It is short, it is tested, and it is boring. Boring is the goal. Disaster recovery is not a heroic act. It is a checklist you have already run, on a calm afternoon, when nothing was on fire.</p>
""",
},
{
 "slug": "running-your-own-email",
 "title": "Running your own email service: what three years taught me",
 "desc": "Three years of operating a permanent email service on Cloudflare: why it is receive-only, why the addresses never expire, and what the real work turns out to be.",
 "body": """
<p class="meta">By Rao Shahzaib &middot; DevOps</p>
<p>Three years ago I started running my own email service. It is a permanent email service, not a throwaway one: one account creates up to 100 email addresses on my own domain, and none of them expire. The idea was simple. Most of us hand the same address to every website we sign up for, and then wonder why the spam never stops. A different address for every site means you always know which site shared it, and you can stop using that address without changing your real email anywhere else.</p>
<p>The first decision was receive-only. The service receives mail; it does not send it. That sounds like a limitation, and it is, but it is a deliberate one. Sending email is a different job from receiving it. A sending service has to fight spam filters, manage reputation, and deal with abuse, and one bad actor can get the whole domain blocked for everyone. Receiving is a smaller, cleaner problem: accept the message, store it, show it to the right account. Keeping the scope small is what has let one person operate the service for three years without it becoming a second job.</p>
<p>The second decision was the platform. The whole service runs on Cloudflare: Workers for the API, Pages for the frontend, and D1 for the database. There is no server to patch and no database to babysit. That matters more than it sounds, because the service has to be up when people check their mail, and a one-person operation cannot afford a 3 a.m. pager for a server it owns. The trade is that the service lives and dies by the platform&rsquo;s rules &mdash; rate limits, request sizes, and the occasional breaking change &mdash; and I have had to learn those rules the way I would learn any vendor.</p>
<p>The third lesson is that the hard part is not the code. The hard part is everything around it: people who forget their credentials, addresses that need to be recovered, signups that need to be real humans and not bots. I use a challenge on registration, and I keep the login and the admin console as separate things, because mixing them is how accounts get compromised. Support is the real work of running a service, and it never shows up in the architecture diagram.</p>
<p>If I started again, I would change two things. First, I would write the policy pages on day one &mdash; what the service is, what it is not, and what happens to an account &mdash; instead of adding them three years later when a reviewer asks for them. Second, I would decide the limits earlier and say them plainly: 100 addresses, receive-only, permanent while the account is active. Clear limits are a feature. They tell people exactly what they are getting, and they protect the service from being used as something it was never meant to be.</p>
""",
},
]

BLOG_BODY = """<h1>Blog</h1>
<p class="lede">Short, practical articles about DevOps, Kubernetes, and running real systems. Everything here is written from systems I actually operate.</p>
<ul>
<li><a href="/blog/gitops-with-argocd/">GitOps with ArgoCD: why Git is the source of truth</a> &mdash; The cluster follows Git, not the other way round. How ArgoCD, drift detection, and pull-request reviews keep a real Kubernetes platform honest.</li>
<li><a href="/blog/docker-multi-stage-builds/">Smaller Docker images with multi-stage builds</a> &mdash; A Dockerfile that ships its compiler is slow to pull and easy to attack. Multi-stage builds keep the build tools out of the final image.</li>
<li><a href="/blog/cicd-pipeline-design/">Designing a CI/CD pipeline that fails safe</a> &mdash; A good pipeline is not the fastest one. It is the one that refuses to ship a broken build and can always roll back.</li>
<li><a href="/blog/kubernetes-backup-disaster-recovery/">Kubernetes backups and disaster recovery: what actually restores</a> &mdash; A backup you have never restored is a hope, not a plan. Velero, a real restore drill, and the gaps most people only find during an incident.</li>
<li><a href="/blog/running-your-own-email/">Running your own email service: what three years taught me</a> &mdash; Why the service is receive-only, why the addresses never expire, and what the real work turns out to be.</li>
</ul>
<h2>Elsewhere</h2>
<p>I publish longer technical pieces &mdash; including a long-running series on networking internals (iptables, NAT, and Docker/Kubernetes networking) &mdash; at <a href="https://blog.raoshahzaib.site">blog.raoshahzaib.site</a> and <a href="https://docker.raoshahzaib.site">docker.raoshahzaib.site</a>. My older blog is at <a href="https://shahzaibraocloud.blogspot.com">shahzaibraocloud.blogspot.com</a>.</p>
"""

# ---------------------------------------------------------------- build ----

PAGES = [
    ("index.html", "Rao Shahzaib — DevOps Engineer",
     "Rao Shahzaib — DevOps Engineer. Kubernetes, Docker, CI/CD, GitOps, Terraform, Ansible. Projects, writing, and contact.",
     SITE + "/", HOME_BODY, PERSON_LD),
    ("about.html", "About — Rao Shahzaib",
     "About Rao Shahzaib: DevOps engineer, freelance DevOps 2023–2025, MCS 2017–2019, and how he works — Git as source of truth, security shift-left.",
     SITE + "/about/", ABOUT_BODY, ""),
    ("projects.html", "Projects — Rao Shahzaib",
     "Projects by Rao Shahzaib: a production Kubernetes platform on OCI, LifeQuest, DownPilot, CreatorWatch, a permanent email service, and a video ad editor.",
     SITE + "/projects/", PROJECTS_BODY, ""),
    ("blog.html", "Blog — Rao Shahzaib",
     "DevOps articles by Rao Shahzaib: GitOps with ArgoCD, Docker multi-stage builds, CI/CD pipeline design, Kubernetes disaster recovery, running an email service.",
     SITE + "/blog/", BLOG_BODY, ""),
    ("contact.html", "Contact — Rao Shahzaib",
     "Contact Rao Shahzaib: email, CV, LinkedIn, and GitHub. Open to remote DevOps roles.",
     SITE + "/contact/", CONTACT_BODY, ""),
    ("privacy.html", "Privacy Policy — Rao Shahzaib",
     "Privacy policy for raoshahzaib.site: a static portfolio site with no accounts, no tracking, and no data collection.",
     SITE + "/privacy/", PRIVACY_BODY, ""),
    ("terms.html", "Terms of Service — Rao Shahzaib",
     "Terms of service for raoshahzaib.site: content is educational, provided as-is, and written from the author's own experience.",
     SITE + "/terms/", TERMS_BODY, ""),
]

def word_count(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    for rel, title, desc, canon, body, extra_ld in PAGES:
        write(rel, page(title, desc, canon, body, extra_ld))

    for a in ARTICLES:
        wc = word_count(a["body"])
        print(f"article {a['slug']}: {wc} words")
        assert 400 <= wc <= 500, f"{a['slug']} word count {wc} outside 400-500"
        body = f"<article class=\"post\"><h1>{a['title']}</h1>\n{a['body']}\n<p><a href=\"/blog/\">&larr; All articles</a></p></article>"
        write(f"blog/{a['slug']}.html",
              page(f"{a['title']} — Rao Shahzaib", a["desc"],
                   f"{SITE}/blog/{a['slug']}/", body))

    # 404 (top-level only — this is a static site, SPA fallback does not apply)
    (OUT / "404.html").write_text(
        page("Page not found — Rao Shahzaib",
             "The page you are looking for does not exist on raoshahzaib.site.",
             SITE + "/404.html", NOTFOUND_BODY), encoding="utf-8")

    # robots.txt, ads.txt
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://raoshahzaib.site/sitemap.xml\n",
        encoding="utf-8")
    (OUT / "ads.txt").write_text(
        "# AdSense publisher line goes here after approval (format: google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0).\n",
        encoding="utf-8")

    # sitemap.xml — every page, trailing-slash URLs
    urls = ["/", "/about/", "/projects/", "/blog/", "/contact/",
            "/privacy/", "/terms/"]
    urls += [f"/blog/{a['slug']}/" for a in ARTICLES]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        sm += f"  <url><loc>{SITE}{u}</loc></url>\n"
    sm += "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    print(f"sitemap: {len(urls)} URLs")

    total = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"build complete: {total} files in {OUT}")

if __name__ == "__main__":
    main()
