# motoproponent.com

A static holding page for `motoproponent.com`, served from the Synology NAS behind the existing Cloudflare Tunnel while the domain's long-term purpose is still undecided.

## What's here

| Path                   | What it is                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `AGENTS.md`            | Operating manual for AI agents (`CLAUDE.md` imports it)                                  |
| `docs/STATUS.md`       | Where the work actually stands and what to do next                                       |
| `public/`              | **The webroot.** Everything public lives here; the Dockerfile copies the whole directory |
| `public/index.html`    | The entire site — one self-contained file, inline CSS                                    |
| `public/assets/`       | Jeffrey's photos for the background and social cards                                     |
| `public/robots.txt`    | Allows crawling, explains why, and carries the launch-day checklist                      |
| `public/static/`       | Social card and `apple-touch-icon.png`, cached for a year                                |
| `nginx.conf`           | Server config baked into the image                                                       |
| `Dockerfile`           | Single-stage `nginx:1.27-alpine`; no build step                                          |
| `docker-compose.yml`   | Publishes host port `1480` → container `80`                                              |
| `utils/deploy/prod.sh` | Build, ship, and restart on the NAS                                                      |
| `docs/nas-setup.md`    | One-time bringup, the Cloudflare Tunnel route, and all dashboard state                   |
| `docs/.private/`       | Untracked — brand answers and open questions for Jeffrey                                 |
| `assets/logos/`        | Ambigram studies and their generators (not part of the site)                             |

The webroot is `public/`, not `site/`, because the boilerplate `.gitignore` ignores `site/` as MkDocs build output — which silently kept the static assets out of the repo.

The page is `noindex` but **crawlable** — see `public/robots.txt` for why that combination is deliberate and what to change on launch day.

## Deploy

```bash
./utils/deploy/prod.sh
```

Refuses to run on a dirty tree or off `main` without `--force`, and always requires a typed `yes`. `--dry-run` previews every step. Expect a Touch ID prompt — the SSH key lives in the 1Password agent.

Deploying only puts files on the NAS. Making the site publicly reachable also requires a tunnel route, which is a Cloudflare dashboard action — see [docs/nas-setup.md](docs/nas-setup.md).

## Design

The page is Jeffrey's own design, adopted as he delivered it on 2026-11-11 (original archived in `assets/from-client/`). Our `<head>` carries the canonical tag, `noindex`, social tags, GA4, and Person JSON-LD. See [docs/decisions.md](docs/decisions.md).

## The logo

Logo exploration lives in `assets/logos/` and is not used on the site. See [docs/architecture.md](docs/architecture.md) for the lowercase ambigram and [assets/logos/README.md](assets/logos/README.md) for the other directions.
