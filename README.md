# motoproponent.com

A static holding page for `motoproponent.com`, served from the Synology NAS behind the existing Cloudflare Tunnel while the domain's long-term purpose is still undecided.

## What's here

| Path                   | What it is                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `_AI_AGENT_PRIMER.md`  | Full briefing for AI agents — stack, traps, load-bearing details                         |
| `docs/STATUS.md`       | Where the work actually stands and what to do next                                       |
| `public/`              | **The webroot.** Everything public lives here; the Dockerfile copies the whole directory |
| `public/index.html`    | The entire site — one self-contained file, inline CSS                                    |
| `public/robots.txt`    | Allows crawling, explains why, and carries the launch-day checklist                      |
| `public/static/`       | `og.png`, `apple-touch-icon.png`                                                         |
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

## Design notes

The page deliberately claims nothing about what Motoproponent is, because that is still being worked out. It carries the palette from the ambigram construction sheet (`#14110E` ink, `#C8452F` accent, `#FAF8F5` ground) so it does not conflict with the brand work in progress, and it is laid out with 180°-rotational symmetry — matched rules above and below, and a centred diagonal that maps onto itself when rotated — as a quiet nod to the ambigram without leaning on the unfinished mark.

The wordmark is SVG text pinned with `textLength` and `lengthAdjust="spacing"`, so a 13-character word fits any viewport exactly by absorbing the difference into tracking rather than overflowing or distorting.

## The ambigram

`assets/logos/motoproponent-ambigram-generator.py` emits the construction sheet. The pairing scheme is sound — M↔T, O↔N, T↔E, P↔O, R↔P, with a self-symmetric centre O, and palindromic glyph widths that make the whole lockup genuinely self-inverse. The letterforms are not there yet: the O/N glyph reads as a slashed zero, and the M/T, R/P and P/O pairs each still show the other letter's structure. It is not used on the site for that reason.

Note that the script writes to a hardcoded sandbox path and will not run as-is.
