# Deployment

`utils/deploy/prod.sh` deploys production. The user runs it; agents hand it over. One-time NAS and Cloudflare setup is in [nas-setup.md](nas-setup.md).

## Running it

```bash
cd /path/to/clean/checkout/of/main
./utils/deploy/prod.sh --dry-run
./utils/deploy/prod.sh
```

Type `yes` at the prompt and approve Touch ID for the 1Password SSH agent. If the main checkout is dirty, deploy from a worktree: `git worktree add ../motoproponent-deploy main`.

## Stages

| Stage | Behaviour |
| --- | --- |
| Flags | `--dry-run` previews every step and touches nothing; `--force` skips the safety gates (do not use); `--help` |
| `.env` | Sourced if present; none exists |
| SSH key | `SSH_KEY_PATH`, then `id_ed25519`, then `id_rsa`, then the agent; the agent normally wins |
| Safety gates | Clean working tree and branch `main`, unless `--force` |
| Confirmation | Typed `yes`, skipped on `--dry-run` |
| Build | `docker build --platform linux/amd64` |
| Transfer | `docker save \| gzip` to a local tarball, piped over SSH to the deploy path (not `scp`) |
| Restart | Remote `docker load`, `docker-compose down`, `docker-compose up -d`, tarball removed; absolute `/usr/local/bin/` paths |
| Health check | Exits 1 unless `http://127.0.0.1:1480/` on the NAS returns 200 |

## After deploying

The script checks the NAS origin only. Also check:

```bash
curl -sI https://motoproponent.com/ | grep -iE 'HTTP/|referrer|robots-tag'
curl -sI https://www.motoproponent.com/ | grep -iE 'HTTP/|location'
curl -sI https://motoproponent.com/subscribe | grep -iE 'HTTP/|location'
```

Then confirm a hit in GA4 Realtime, and that both social cards land on the right accounts.

## Launch day

The page is `noindex` until there is something worth indexing. On launch, do all four in one deploy:

1. Remove `<meta name="robots">` from `public/index.html`.
2. Remove the server-level `add_header X-Robots-Tag` from `nginx.conf` (keep the one in `/subscribe`).
3. Ship `public/sitemap.xml`.
4. Uncomment the `Sitemap:` line in `public/robots.txt`.
