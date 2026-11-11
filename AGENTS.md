# AGENTS.md — motoproponent.com

Static one-page site for Motoproponent, a San Francisco motorcycle YouTuber (client: Jeffrey). The channel is the product; the site is the address. One HTML file served by nginx in a Docker container on a Synology NAS behind a Cloudflare Tunnel. Separately, `assets/logos/` holds logo exploration that is not used on the site.

Current state and open threads: [docs/STATUS.md](docs/STATUS.md). Read it before starting work.

> When a change makes anything in this file inaccurate—a command, a path, a convention, a prohibition—update this file in the same change.

## Who you are working for — read first

Run `git config user.name`. If it is `Ziad Ezzat`, you are working for the **maintainer**: skip this section and follow the rest of this file. Anyone else—most likely Jeffrey—is a **contributor**: follow this section, and where it conflicts with anything below, this section wins. If `git` is not installed or the folder is not a git checkout, the user is a contributor.

Jeffrey is the client, not a developer. Do all the technical work yourself, explain what you are doing in plain language, and never ask him to type commands, read diffs, or resolve git problems. If something technical goes wrong that you cannot fix, stop and tell him to ask Ziad.

### What a contributor may change

- Anything under `public/`: edit pages, add new pages, styles, scripts, and images.
- Nothing outside `public/`. `nginx.conf`, `Dockerfile`, `docker-compose.yml`, `utils/`, `docs/`, `assets/`, and this file belong to Ziad. If a request needs one of them (a server redirect, a form that sends email, a build step), say so and leave it for Ziad.
- `public/robots.txt` and the `noindex` tags stay as they are until Ziad switches the site to "launched".

### Rules for every change

1. **Build on what is there; never start the site over.** Edit `public/index.html` rather than replacing it. For a new page, copy `public/index.html`, keep its `<head>`, and change only what is page-specific: `<title>`, the description, the canonical and `og:url` (the page's own `https://motoproponent.com/...` address), and the `og:`/`twitter:` title and description.
2. **Every page keeps the shared head tags:** the Google Analytics snippet, canonical link, `noindex` robots tag, Open Graph and Twitter tags, favicon, and Apple touch icon. The home page also keeps the JSON-LD Person block. You may add to `<head>`; do not remove these.
3. Run `./utils/check-page.sh` after every edit. Every page must print `OK`. Fix what it reports; never edit the script to make it pass.
4. Open each changed page in a browser and look at it at phone and desktop widths before calling the work done. Show Jeffrey a screenshot. Save screenshots outside the repo folder; never commit them.
5. **The site must stay plain static files.** The server copies `public/` as-is; there is no build step. Hand-written HTML, CSS, and JavaScript are fine, and so are small libraries loaded from a CDN. A framework, package manager, or build tool (React, Next.js, npm, Tailwind CLI, a site generator) changes how the site is deployed, so propose it to Ziad first rather than adding it.
6. Never embed YouTube videos as the main way to watch them, and never host video files; link to YouTube so views count on the channel. Recent-video lists should update automatically, not by hand.
7. Images: JPEG or WebP whose file extension matches the real format, under 300 KB each, and no wider than 2000px. Do not show readable licence plates or bystanders' faces unless Jeffrey says so.
8. Links out use `rel="noopener"`, never `noreferrer`. The channel is `https://www.youtube.com/@motoproponent`; Instagram is `https://www.instagram.com/m0t0pr0p0nent/` (zeros, not letters). Strip share tokens like `?si=` from pasted links.
9. Never deploy, touch the server, or change Cloudflare or DNS. Ziad publishes the site.

### Sending the change to Ziad: pull request (preferred)

The repo is public, so Jeffrey needs only a free GitHub account; he does not need access to Ziad's copy. Install the GitHub CLI (`gh`) if it is missing, then run `gh auth login` and let Jeffrey finish the sign-in in his browser. After that:

```bash
gh repo fork feralcreative/motoproponent --clone
cd motoproponent
git switch -c fix/short-description
```

If you are already inside a git checkout of this repo, do not clone again inside it. Run `gh repo fork feralcreative/motoproponent --remote` there instead, which adds `upstream` and points `origin` at the fork, then `git fetch upstream && git switch -c fix/short-description upstream/main`. If the folder is an unzipped download (no `.git`), it cannot become a PR: run the fork-and-clone commands in a different folder, then copy the finished `public/` changes across.

Use `feat/…` for something new and `fix/…` for a correction. Before each new piece of work, start a fresh branch from the latest `main` (`git switch main && git pull upstream main`). Commit with a plain-English message, then:

```bash
git push -u origin HEAD
gh pr create --repo feralcreative/motoproponent --base main --attach '/path/outside/repo/screenshot.png#How the page looks now'
```

The PR description says, in plain language, what changed and why, and confirms `check-page.sh` printed `OK`. The screenshot goes in with `--attach`, not as a committed file. One change per PR. Never push to `main`, never merge your own PR, and never force-push.

### Sending the change to Ziad: zip (fallback)

If GitHub sign-in is too much, get the latest `main` without an account: `git clone https://github.com/feralcreative/motoproponent.git` (or `git pull` in an existing clone), or download <https://github.com/feralcreative/motoproponent/archive/refs/heads/main.zip>. Always start from the latest `main`, never from an older copy. Work only in `public/` under the rules above, run the check, then zip the whole `public/` folder and have Jeffrey email it to Ziad with a sentence on what changed.

## Commands

No package manager, no install step, no tests, no linter, no CI.

| Task | Command |
| --- | --- |
| Build image | `docker build -t motoproponent:test .` |
| List what ships | `docker run --rm motoproponent:test ls -R /usr/share/nginx/html` |
| Start a test container (no host port) | `cid=$(docker run -d motoproponent:test)` |
| Check a path and its headers | `docker exec $cid wget -S -q -O /dev/null http://127.0.0.1/index.html 2>&1` (repeat for `/`, `/subscribe`, each asset) |
| Stop the test container | `docker rm -f $cid` |
| Preview page without Docker | open `public/index.html` in a browser (relative asset paths work over `file://`) |
| Screenshot page | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 --screenshot=out.png "file://$PWD/public/index.html"` |
| Check required tags and links | `./utils/check-page.sh` (every page in `public/`, or pass specific files) |
| Deploy dry run | `./utils/deploy/prod.sh --dry-run` |
| Deploy | `./utils/deploy/prod.sh` (user runs it; see Prohibitions) |
| Public checks | `curl -sI https://motoproponent.com/` and `curl -sI https://www.motoproponent.com/` (expect 200 and 301) |
| Logo study (lowercase) | `cd assets/logos && python3 motoproponent-lowercase-generator.py` (`--replace` overwrites latest; a number forces it) |
| Logo study (uppercase / duotone) | same arguments on `motoproponent-ambigram-generator.py`, `motoproponent-duotone-generator.py` |
| Concept studies | `python3 motoproponent-concepts-generator.py` (all four), `… wheel` (one), `… card 12` (force number); no `--replace` |
| Render an SVG | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=<W>,<H> --screenshot=out.png "file://$PWD/<study>.svg"` |
| Client presentation page | `cd assets/logos && python3 build-presentation.py` |

Logo generators are Python 3 stdlib only. `--window-size` must equal the SVG's declared `width`/`height`; the lowercase generator prints it, otherwise read it from the SVG root.

## Definition of done

Maintainer checklist; contributors follow "Rules for every change" above.

1. `./utils/check-page.sh` prints `OK`.
2. `docker build` succeeds and the `ls -R` check lists every file you added under `public/`.
3. `/`, every new asset, and `/subscribe` (302 to YouTube) answer correctly inside the container, with the right `Content-Type`.
4. Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `X-Robots-Tag`) are present on `/` and `/index.html`.
5. For page or logo changes: render it and look at the screenshot. Do not judge visuals from source.
6. Codex has reviewed the diff (`codex exec -s read-only -m gpt-5.6-sol "<prompt>" < /dev/null`).
7. `docs/STATUS.md` reflects what changed.

No test suite exists; do not invent one.

## Prohibitions

- Never deploy. `prod.sh` is run by the user; the auto-mode classifier blocks it anyway. Hand over the command.
- Never pass `--force` to `prod.sh` to get past the dirty-tree or off-`main` gate. Deploy from a clean checkout of `main` (a `git worktree` works).
- Maintainer: never push or open PRs without being asked. Contributor PRs follow the section at the top.
- Never change Cloudflare DNS, Tunnel routes, or Redirect Rules without the user's written permission for that specific change.
- Never add `rel="noreferrer"` to outbound links or tighten `Referrer-Policy` in `nginx.conf`. See [docs/decisions.md](docs/decisions.md).
- Never add an `add_header` to the `/index.html` or `/static/` locations in `nginx.conf`; use `expires` only. It silently strips the server-level security headers. (`/subscribe` has its own `add_header` on purpose; it returns before serving content.)
- Never add `Disallow:` to `robots.txt` while the page is `noindex`, and never uncomment the `Sitemap:` line before `public/sitemap.xml` exists.
- Never enumerate files in a Dockerfile `COPY`; copy `public/` whole.
- Never normalise the Instagram handle. It is `m0t0pr0p0nent` with literal zeros (verified live 2026-11-11).
- Never hand-author the right half of an ambigram; it is generated by rotation.
- Never delete `motoproponent-lowercase-study-000`–`003.svg` or `motoproponent-ambigram-study-004.svg`; `build-presentation.py` reads them.
- Never run `motoproponent-duotone-generator.py` and cite its output without regenerating and checking it; its last edit was never verified.
- Never commit anything under `docs/.private/` (git-ignored client data), `.env`, or deploy tarballs.

## Architecture

Request path:

1. Browser → Cloudflare edge (Always Use HTTPS, HSTS, `www` → apex 301 Redirect Rule).
2. Cloudflare Tunnel, remotely managed; the route lives in the Zero Trust dashboard, not on the NAS.
3. NAS `127.0.0.1:1480` → container port 80 → nginx (`nginx.conf`) → `/usr/share/nginx/html`, which is `public/`.

Deploy path (`utils/deploy/prod.sh`): build `linux/amd64` → `docker save | gzip` → piped over SSH to the NAS → `docker load` → `docker-compose up -d` → health check on `127.0.0.1:1480`. It verifies the NAS origin only, not the public URL.

Site: `public/index.html` is the whole page. The `<head>` (canonical, `noindex`, OG/Twitter, GA4, Person JSON-LD, icons) is ours; the `<style>` and `<body>` are Jeffrey's design as he delivered it (archived in `assets/from-client/`). Photos are in `public/assets/`; long-cache files are in `public/static/`.

nginx routes worth knowing: `/index.html` cached 5 minutes, `/static/` cached one year, `/subscribe` is a 302 to the channel with `sub_confirmation=1`.

Depth: [docs/architecture.md](docs/architecture.md), [docs/deployment.md](docs/deployment.md).

## Conventions

- Copy says `Motoproponent`: one initial cap, never `MotoProponent` in new copy. Jeffrey's own body copy and his all-caps heading are kept as he wrote them.
- Description copy is Jeffrey's approved wording from his channel description. Do not rewrite it for keywords.
- Files in `public/static/` are cached for a year: give a changed file a new name (e.g. `og-20261111.png`) and update every reference.
- Utility scripts go in `utils/`, never `scripts/`. Cross-repo utilities go in `~/www/_code/utils`.
- Docs go in `docs/`; only `README.md`, `AGENTS.md`, and the one-line `CLAUDE.md` live at the root. Plans go in `_PLANS/` (git-ignored).
- Markdown: never hard-wrap prose; tight em dashes (`word—word`); every fenced block has a language; Oxford comma.
- Dev port baseline for this project is `1480` (taken by production on the NAS); `1481`/`1482` are next if a stage or sidecar appears. Check `~/www/_code/port-roulette-config.json` before using one.

## Gotchas

1. **`.gitignore` ignores `site/`** (MkDocs output). A new top-level directory may be silently untracked; run `git check-ignore -v <path>` first. The webroot is `public/` for this reason.
2. **`.gitignore` ignores `*.zip`**, so `assets/from-client/motoproponent_placeholder_website.zip` is local only. The extracted folder is the tracked copy.
3. **`.dockerignore` excludes `assets/`, `docs/`, `utils/`, and `*.md`.** A `COPY` from any of them fails the build. Anything public must be in `public/`.
4. **Deploying does not make the site reachable.** The Tunnel route and all Cloudflare settings are dashboard state, recorded in [docs/nas-setup.md](docs/nas-setup.md).
5. **The user's main checkout often has uncommitted logo work.** `prod.sh` refuses a dirty tree. Deploy from a separate clean worktree of `main`.
6. **File extensions lie.** Jeffrey's `instagram-photo.webp` was JPEG bytes; it ships as `.jpg`. Check with `file` before adding images.
7. **SVG ids are document-global.** Inlining two study sheets in one HTML page makes the second `<use>` render the first mark. `build-presentation.py` namespaces each instance (`instance()`).
8. **CSS does not reliably restyle `<use>` shadow content.** Strip baked `stroke` attributes (`strip_stroke()`) and colour the `<use>` element instead.
9. **Chrome `--force-dark-mode` inverts the page** and hides a broken dark theme. Test dark mode another way.
10. **Headless Chrome falls back to 756×468** if `--window-size` does not match the SVG's size.
11. **Verify a channel's videos via RSS** (`https://www.youtube.com/feeds/videos.xml?channel_id=<ID>`). Scraping the channel HTML returns nothing.
12. **Cloudflare Web Analytics sites cannot be created by API**; it is dashboard-only regardless of token scope.
13. **Cloudflare account-level token permissions** must sit in the policy whose resource is the account, not a zone.
14. **Synology's non-login PATH lacks Docker.** Remote commands use `/usr/local/bin/docker` and `/usr/local/bin/docker-compose`.
15. **`assets/logos/README.md` mixes eras**: it documents the uppercase, duotone, and concepts directions; lowercase is documented in [docs/architecture.md](docs/architecture.md). Which logo direction is current: TBD—ask.

## Credentials

Maintainer only. A contributor has no credentials and needs none.

Nothing in the repo is a secret and no `.env` exists (`prod.sh` sources one if present).

| Item | Source | Notes |
| --- | --- | --- |
| NAS SSH key | 1Password SSH agent | Never on disk; expect Touch ID mid-deploy |
| NAS host, user, and SSH port | `utils/deploy/prod.sh`, `docs/nas-setup.md` | Committed deliberately; not credentials |
| Cloudflare API token | 1Password item "Cloudflare Feral Admin API" (`jjnr7y3j4qzxx4du6j2lk4xyqq`), field `credential`, account `ziadezzat.1password.com` | Reference by UUID. Never echo it |
| GA4 Measurement ID | `public/index.html` | Public by design; not a secret |

Git-ignored and never to be read into a commit, log, or chat: `.env`, `docs/.private/`, `*.tar.gz`.

## Commit and PR conventions

- Maintainer, personal repo: commit on the user's behalf in logical blocks, without being asked. Pushing, PRs, and deploys need explicit permission.
- Conventional Commits: `type(scope): subject`, imperative. Types in use: `feat`, `fix`, `docs`, `chore`, `refactor`.
- Branches: `type/kebab-subject` (e.g. `feat/client-placeholder`). PRs target `main`.
- No AI attribution in commits or PR bodies, ever.

## Deep-dive index

- [docs/STATUS.md](docs/STATUS.md)—current state, open decisions, what is waiting on Jeffrey. Read at session start.
- [docs/architecture.md](docs/architecture.md)—site structure and the lowercase ambigram construction. Read before touching the page or the logo.
- [docs/deployment.md](docs/deployment.md)—`prod.sh` stages, launch-day checklist, post-deploy checks. Read before any deploy.
- [docs/decisions.md](docs/decisions.md)—why the load-bearing details are the way they are. Read before "cleaning up" headers, robots, links, or caching.
- [docs/nas-setup.md](docs/nas-setup.md)—one-time NAS bringup and all Cloudflare dashboard state.
- [docs/website-scope.md](docs/website-scope.md)—what the site is for, agreed with the client.
- [assets/logos/README.md](assets/logos/README.md)—ambigram theory, impossibility proofs, uppercase, duotone, and concepts directions.
