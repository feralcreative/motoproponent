# \_AI_AGENT_PRIMER — motoproponent.com

Audience: AI coding agents. Read this before touching anything.

**Current status, open threads, and what to do next: [docs/STATUS.md](docs/STATUS.md).** Read it second. This file is stable reference; that file changes every session.

## 0. What this is in one paragraph

A static holding page for `motoproponent.com`, plus an in-progress logo (a 180° rotational ambigram) that is **not** used on the site. Client is Jeffrey, a motorcycle YouTuber; the real product is his YouTube channel and the goal is subscribers. There is no framework, no build step for the site, no database, no backend, no tests, no CI. The site is one hand-written HTML file served by nginx in a container on a Synology NAS behind a Cloudflare Tunnel. The logo work is Python scripts that emit SVG.

## 1. Secrets reference guide

Nothing in this repo is a secret, and no `.env` file exists. Listed so you do not go looking.

| Item | Value / location | Notes |
| --- | --- | --- |
| GA4 Measurement ID | `G-3YRC...L242` — [public/index.html:46](public/index.html#L46), [:51](public/index.html#L51) | **Not a secret.** Public by design; it ships in client HTML. Do not obfuscate it in code. |
| NAS SSH port | `337**` — [utils/deploy/prod.sh:14](utils/deploy/prod.sh#L14) | Committed deliberately; not a credential. |
| NAS host / user | `nas.feralcreative.co` / `ziad` — [utils/deploy/prod.sh:12-13](utils/deploy/prod.sh#L12-L13) | |
| SSH private key | 1Password SSH agent | Never on disk. `prod.sh` falls through to the agent ([prod.sh:71-77](utils/deploy/prod.sh#L71-L77)). Expect a Touch ID prompt mid-deploy. |
| Cloudflare API token | 1Password, item UUID `jjnr7y3j4qzxx4du6j2lk4xyqq` | Read with `op read "op://Private/jjnr7y3j4qzxx4du6j2lk4xyqq/Token"`. Reference by **UUID, not item name** — the name has been changed once and broke the lookup. |
| `.env` | Does not exist | `prod.sh:64-66` sources it if present. Ignored via `.gitignore:204-209`. |

Git-ignored paths that matter: `.private` ([.gitignore:241](.gitignore#L241)) hides `docs/.private/`; `site/` ([.gitignore:170](.gitignore#L170)) is a live trap — see §9.

## 2. Stack

| Layer | Choice | Version |
| --- | --- | --- |
| Web server | `nginx:1.27-alpine` | pinned, [Dockerfile:4](Dockerfile#L4) |
| Container | single-stage Docker, no build step | Docker 29.5.3 local |
| Orchestration | `docker-compose` on the NAS | [docker-compose.yml](docker-compose.yml) |
| Edge | Cloudflare (DNS, proxy, Tunnel, Redirect Rules) | dashboard state, not in git |
| Logo tooling | Python 3 stdlib only — no deps, no venv | 3.14.5 local |
| Rasteriser | headless Google Chrome | no `rsvg-convert`/`magick`/`inkscape` on this machine |
| Analytics | GA4 + Cloudflare Web Analytics | |

No `package.json`, no `requirements.txt`, no lockfiles. Nothing to install.

## 3. Directory tree

```text
.
├── _AI_AGENT_PRIMER.md      this file
├── README.md                human-facing overview
├── Dockerfile               single-stage nginx; COPY public/ (see §9)
├── docker-compose.yml       host 1480 → container 80
├── nginx.conf               baked into the image at /etc/nginx/conf.d/default.conf
├── .dockerignore            excludes assets/ docs/ utils/ *.md — see §9
├── public/                  THE WEBROOT. Everything public. Copied wholesale.
│   ├── index.html           the entire site: one file, inline CSS, inline SVG
│   ├── robots.txt           Allow: / on purpose; carries the launch checklist
│   └── static/              og.png (1200×630), apple-touch-icon.png (180×180)
├── utils/deploy/prod.sh     build → save → pipe over SSH → load → compose up → verify
├── docs/
│   ├── STATUS.md            ← current state and next actions. Read this.
│   ├── nas-setup.md         one-time bringup + ALL Cloudflare dashboard state
│   └── .private/            GIT-IGNORED. Client answers and open questions.
└── assets/                  NOT shipped in the image, excluded by .dockerignore
    └── logos/
        ├── README.md        ambigram theory, impossibility proofs (partly STALE, §10)
        ├── original/        Jeffrey's brief.md + his sketch 1000016578.jpg
        ├── makeambigrams/   7 reference PNGs from a free generator site
        ├── motoproponent-ambigram-generator.py     UPPERCASE — abandoned
        ├── motoproponent-duotone-generator.py      abandoned mid-edit, DO NOT RUN (§10)
        ├── motoproponent-lowercase-generator.py    ← THE LIVE ONE
        ├── build-presentation.py                   builds the client page
        ├── presentation.html                       generated, 333KB, published artifact
        └── *-study-NNN.svg                         construction sheets, all kept
```

## 4. Data flow

```text
DEPLOY
  Mac: docker build --platform linux/amd64
    → docker save | gzip → /tmp/motoproponent-<epoch>.tar.gz
    → cat | ssh -p 337** → /volume1/web/motoproponent.com/image.tar.gz
    → remote: docker load; docker-compose down; docker-compose up -d; rm tarball
    → remote: curl 127.0.0.1:1480 must return 200 or the script exits 1

REQUEST
  browser → Cloudflare edge (Always Use HTTPS, HSTS, www→apex 301 Redirect Rule)
          → Cloudflare Tunnel (remotely managed; route lives in the dashboard)
          → NAS 127.0.0.1:1480 → container :80 → nginx → /usr/share/nginx/html

LOGO
  *-generator.py → *-study-NNN.svg → headless Chrome → PNG → look at it
  build-presentation.py reads the study SVGs → presentation.html → Artifact
```

## 5. Commands

```bash
# Deploy. Refuses on a dirty tree or off main without --force. Always prompts for
# a typed "yes". Expect a Touch ID prompt for the 1Password SSH agent.
./utils/deploy/prod.sh
./utils/deploy/prod.sh --dry-run     # previews every step, touches nothing

# Local container test
docker build -t motoproponent:test .
docker run --rm motoproponent:test ls -R /usr/share/nginx/html   # did everything ship?
docker run --rm -p 8080:80 motoproponent:test

curl -sI localhost:8080/            | grep -iE 'x-content-type|x-frame|referrer|robots-tag'
curl -sI localhost:8080/index.html  | grep -iE 'x-content-type|x-frame|referrer|robots-tag'
curl -sI localhost:8080/subscribe   | grep -iE 'HTTP/|location'   # expect 302 to YouTube

# Production checks
curl -sI https://motoproponent.com/          | grep -iE 'HTTP/|referrer|robots-tag'
curl -sI https://www.motoproponent.com/      | grep -iE 'HTTP/|location'   # expect 301
ssh -p 337** ziad@nas.feralcreative.co \
  "/usr/local/bin/docker ps --filter name=motoproponent; \
   curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:1480/"

# Logo: next numbered study, or overwrite the last one
cd assets/logos
python3 motoproponent-lowercase-generator.py
python3 motoproponent-lowercase-generator.py --replace
python3 motoproponent-lowercase-generator.py 007      # explicit number

# Look at the SVG. This step is not optional — every real defect in this
# project was found by rendering and looking, never by reading the path data.
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --hide-scrollbars --window-size=<W>,<H> --screenshot=/tmp/out.png \
  "file://$PWD/motoproponent-lowercase-study-003.svg"

# Client presentation page
python3 build-presentation.py     # then republish presentation.html as an Artifact
```

`--window-size` must match the SVG's own `width`/`height`, which the generator prints. Chrome silently falls back to 756×468 otherwise.

## 6. The site

One file, [public/index.html](public/index.html). No JS beyond the GA4 snippet. Palette `#FAF8F5` / `#14110E` / `#C8452F`, with a dark-mode block at [:63-71](public/index.html#L63-L71).

The wordmark is SVG `<text>` with `textLength="1000" lengthAdjust="spacing"` ([:226-229](public/index.html#L226-L229)) so a 13-character word fits any viewport by absorbing the difference into tracking rather than overflowing or distorting the glyphs.

### Load-bearing details — do not "clean these up"

| Thing | Where | Why it must stay |
| --- | --- | --- |
| `Referrer-Policy: strict-origin-when-cross-origin` | [nginx.conf:48](nginx.conf#L48) | YouTube Studio attributes external traffic by the `Referer` header, **not** by URL parameters. Tighten this to `no-referrer` and the only measurement of whether the site sends anyone to the channel silently disappears. |
| `rel="noopener"` with **no** `noreferrer` | [public/index.html:244](public/index.html#L244) | Same reason. `noreferrer` strips the header. It is the kind of thing someone adds by reflex. |
| `expires 5m;` and nothing else | [nginx.conf:16-18](nginx.conf#L16-L18) | An `add_header` in a `location` suppresses inheritance of all server-level `add_header` directives. Because `index index.html` makes `/` re-match this block, adding one strips the three security headers from the only page on the site. `expires` is not an `add_header`, so inheritance survives. Same rule for `/static/` at [:21-23](nginx.conf#L21-L23). |
| `Allow: /` with `noindex` | [public/robots.txt](public/robots.txt), [index.html:17](public/index.html#L17) | Blocking the crawl stops Google ever *reading* the `noindex`, which is how a bare snippet-less URL gets stuck in the index. Crawlable + noindex is what actually keeps a page out. |
| `Sitemap:` line commented out | [public/robots.txt](public/robots.txt) | A `Sitemap:` pointing at a 404 generates persistent Search Console errors. |

### Launch day — all four in ONE deploy

1. Remove `<meta name="robots">` from [public/index.html:17](public/index.html#L17)
2. Remove `add_header X-Robots-Tag` from [nginx.conf:53](nginx.conf#L53)
3. Ship `public/sitemap.xml`
4. Uncomment the `Sitemap:` line in `public/robots.txt`

To de-index later, never add `Disallow:` first — add `noindex`, wait for the recrawl, confirm in GSC, and only then block. Disallowing first freezes the URL in the index permanently.

## 7. Deployment

[utils/deploy/prod.sh](utils/deploy/prod.sh), 193 lines, `set -euo pipefail`.

| Stage | Lines | Note |
| --- | --- | --- |
| Flags `--dry-run` / `--force` / `--help` | [46-55](utils/deploy/prod.sh#L46-L55) | |
| SSH key detection | [71-77](utils/deploy/prod.sh#L71-L77) | `SSH_KEY_PATH` → `id_ed25519` → `id_rsa` → agent. Agent tier normally wins. |
| Safety gates | [93-102](utils/deploy/prod.sh#L93-L102) | Clean tree **and** branch `main`, unless `--force` |
| Typed confirmation | [104-111](utils/deploy/prod.sh#L104-L111) | Must type `yes`; skipped on `--dry-run` |
| Build / save / transfer | [113-150](utils/deploy/prod.sh#L113-L150) | `--platform linux/amd64`; piped over SSH, not `scp` |
| Remote load + restart | [152-166](utils/deploy/prod.sh#L152-L166) | Absolute paths `/usr/local/bin/docker*` — Synology's PATH is not the login PATH |
| Health check | [168-178](utils/deploy/prod.sh#L168-L178) | Exits 1 unless `127.0.0.1:1480` returns 200 |

**Deploying only puts files on the NAS.** Public reachability additionally needs the Cloudflare Tunnel route, which is a dashboard action. All dashboard state — tunnel route, `www`→apex redirect, HSTS, Always Online, Rocket Loader off, Web Analytics — is in [docs/nas-setup.md](docs/nas-setup.md). None of it is in git and `prod.sh` does not touch it.

## 8. The logo

Not used on the site. Live generator: `assets/logos/motoproponent-lowercase-generator.py`. Latest output: `motoproponent-lowercase-study-003.svg`.

**Architecture.** Only the left half plus the pivot letter is ever authored. The right half is that artwork rotated:

```html
<use href="#half"/>
<use href="#half" transform="rotate(180, CX, CY)"/>
```

Symmetry is therefore true by construction, not by eye. Never hand-author the right half.

**Metric system — this is the whole design.**

```text
ASC 0 · XH 30 · MID 85 · BASE 140 · DESC 170     rotation maps y → 170 − y
XH 30 ↔ 140 BASE     the x-height band maps onto itself
ASC  0 ↔ 170 DESC    an ascender is a descender upside down
```

That spare vertical real estate is what lowercase has and capitals do not, and it is why the uppercase direction was abandoned.

**Pair status** (letter *i* must be the rotation of letter *14 − i*):

| Pair | Status |
| --- | --- |
| m ↔ t | works — m's dropped last leg becomes the t's ascender; m's foot bar becomes its crossbar |
| o ↔ n | compromise — notch width has no winning value; straight sides on the bowl sell the n |
| t ↔ e | clean — centred stem and centred mid bar both map onto themselves |
| p ↔ o | works — stubby descender becomes a small tick above the rule |
| r ↔ p | **impossible** — r's arm and p's bowl both point right; rotation flips handedness. Invariant. |
| o (pivot) | drawn twice, so its notch fills itself in; the only fully closed letter |

## 9. Traps that have already cost time

1. **`.gitignore:170` ignores `site/`.** It means MkDocs output. A webroot named `site/` is silently untracked — `git mv` force-adds files so it *looks* fine, but anything added later is invisible. The build reads the filesystem, so it succeeds locally, deploys, passes its health check, and 404s from a fresh clone with no error anywhere. The webroot is `public/` for this reason. Run `git check-ignore -v <path>` before assuming any new top-level directory is tracked.
2. **`.dockerignore` excludes `assets/`, `docs/`, `utils/`, `*.md`.** A `COPY` from any of them hard-fails the build — the path is excluded from the build context before `COPY` runs.
3. **Never enumerate filenames in `COPY`.** [Dockerfile:16](Dockerfile#L16) copies the whole directory. Listing files ships builds that succeed and then 404 on the asset you just added.
4. **SVG ids are document-global.** `<svg>` does **not** scope them. Every study sheet names its groups `half-final` / `line-straight`, so inlining two marks in one HTML page collides and the second `<use>` silently renders the *first* mark's artwork. This bit twice while building the presentation page — once across different studies, once across three copies of the same mark. `build-presentation.py` namespaces every instance ([instance()](assets/logos/build-presentation.py)).
5. **CSS cannot restyle content rendered through `<use>`.** A rule written against the original element in `<defs>` does not reliably reach the shadow-tree clone. Symptom: the mark stayed black on a black plate despite a more-specific override. Fix in use: `strip_stroke()` removes the baked `stroke` attributes and the colour is set on the `<use>` elements, which are ordinary DOM, and inherits inward.
6. **Chrome's `--force-dark-mode` invalidates dark-theme testing.** It inverts the whole page, so a broken theme looks fine. Test by stamping `<html data-theme="dark">` instead.
7. **`--window-size` must match the SVG's declared size** or Chrome renders at 756×468 and you screenshot the top-left corner.
8. **Verify a channel's videos via the RSS feed**, `https://www.youtube.com/feeds/videos.xml?channel_id=<ID>`. Scraping the HTML for `videoRenderer` returns nothing because the channel grid uses `richItemRenderer` — that produced a confidently wrong "this channel has 0 videos".
9. **Cloudflare has no write permission group for Web Analytics (RUM).** `Account Analytics` is read-only. Creating a site is dashboard-only; the API returns `Authentication error` regardless of token scope.
10. **Cloudflare account-level token permissions** must sit in the policy whose resource is the *account* (`"...account.<id>": "*"`), not the zone-scoped policy.

## 10. Known-bad / stale in-repo

| Item | State |
| --- | --- |
| `assets/logos/motoproponent-duotone-generator.py` | Abandoned mid-edit. Last edits were applied but **never re-run or verified**, and its NOTES text still argues for a width-balance rationale that was reverted. Do not run or cite it without regenerating first. |
| `assets/logos/README.md` | Written for the **uppercase** direction. §5/§6 describe the old T/E construction and a partial-overlap rule motif that no longer exist; the whole document predates the lowercase turn. The impossibility proofs in §4 are still correct. |
| `assets/logos/motoproponent-ambigram-generator.py` | Uppercase, superseded. Kept because study-004 is cited by the presentation page. Do not delete. |
| `motoproponent-lowercase-study-{000,001,002}.svg` | Deliberately kept as the record of what failed. `build-presentation.py` reads them. **Deleting them breaks the build.** |
| `README.md` §"The ambigram" | Still describes the uppercase mark as the current state. |

## 11. Conventions

- Utility scripts go in `utils/`, never `scripts/`. Cross-repo utilities go in `~/www/_code/utils` instead of this repo.
- Docs go in `docs/`, except `README.md` and `_AI_AGENT_PRIMER.md`, which stay in the root.
- Em dashes are tight: `word—word`. Use a spaced en dash if the line needs air.
- Never hard-wrap prose in markdown. One line per paragraph.
- Every fenced code block gets a language; use `text` if nothing fits.
- Port baseline for this project is `1480`; `1481`/`1482` are next if a stage or sidecar appears.
- **Never commit or deploy without explicit permission.** Hand over a single chained one-liner (`git add -A && git commit -m "type(scope): subject"`) and let the user run it.
- Never add AI attribution to commit messages or PR bodies.
- Fix lint errors in code, never by running a linter in the terminal.

## 12. Not present

No tests, no CI/CD, no GitHub Actions, no database, no backend, no API of our own, no auth, no session management, no background jobs, no webhooks, no SSL certificates we manage (Cloudflare terminates), no migrations, no state management, no routing beyond nginx `try_files`, no `sitemap.xml` yet, no JSON-LD yet (deliberately deferred pending client answers).
