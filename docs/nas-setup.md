# One-time NAS bringup for motoproponent.com

Do these once, in order, before the first `./utils/deploy/prod.sh`. After that, redeploys are just that one command from your Mac.

## How this site is served

The NAS runs a single **remotely-managed** Cloudflare Tunnel. Its on-disk config at `/volume1/@appdata/cloudflared/config.yml` contains only a connector token plus a few connector flags — there is **no `ingress:` block**. That means every public hostname and its routing rule lives in the Cloudflare Zero Trust dashboard, not on the NAS. Editing files on the NAS will not add a route.

The site itself follows the house pattern for static sites here: a small `nginx:alpine` container publishing a host port, with the tunnel pointing at that port. Direct analogues already running are `fuckpicrights` (4317), `ziad-af` (47489) and `cats-web` (54999).

| Fact | Value |
| --- | --- |
| NAS host | `nas.feralcreative.co` |
| SSH port | `33725` |
| SSH user | `ziad` (keys in the 1Password agent — expect a Touch ID prompt) |
| Deploy path | `/volume1/web/motoproponent.com` |
| Container | `motoproponent` |
| Host port | `1480` |
| Tunnel | remotely managed; routes edited in the Zero Trust dashboard |

## 1. Confirm the zone is in the Cloudflare account

The tunnel can only create a route for `motoproponent.com` if that zone lives in the **same Cloudflare account** as the tunnel. Check `dash.cloudflare.com` for the zone. If it is not there, add the domain to that account and move its nameservers before going further — nothing below will work otherwise.

## 2. First deploy

From the project root on your Mac:

```bash
./utils/deploy/prod.sh
```

The script creates `/volume1/web/motoproponent.com`, builds for `linux/amd64`, pipes the image over SSH, loads it, brings the container up, and then verifies the origin answers `200` on `127.0.0.1:1480`. It refuses to run on a dirty tree or off `main` unless you pass `--force`, and it always asks for a typed `yes`. Use `--dry-run` to preview.

At this point the site is live **on the NAS only**. It is not yet reachable from the internet.

## 3. Add the tunnel route

In the Cloudflare Zero Trust dashboard: **Networks → Tunnels →** the NAS tunnel **→ Public Hostnames → Add a public hostname**.

| Field | Value |
| --- | --- |
| Subdomain | *(leave blank for the apex)* |
| Domain | `motoproponent.com` |
| Path | *(leave blank)* |
| Service type | `HTTP` |
| URL | `127.0.0.1:1480` |

Use the literal `127.0.0.1`, **not** `localhost`. `cloudflared` resolves `localhost` to IPv6 `::1` first, which is what caused the `home.ezzat.com` 400 outage when Home Assistant rejected `::1` as an untrusted proxy. It does not matter to this nginx container, but the habit is worth keeping.

Saving the hostname auto-creates the proxied DNS record pointing at `<tunnel-id>.cfargotunnel.com`. Repeat with subdomain `www` if you want `www.motoproponent.com` to resolve — `tankbag.app` currently 404s on `www` precisely because that step was skipped.

## 4. Verify

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://motoproponent.com/
```

Expect `200`. A Cloudflare `1033` or a bare 404 means the tunnel route is missing or the hostname is misspelled. A `502` means the route exists but the container is not answering — check it on the NAS:

```bash
ssh -p 33725 ziad@nas.feralcreative.co \
  "/usr/local/bin/docker ps --filter name=motoproponent; \
   curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:1480/"
```

## Notes

- **The page is `noindex`.** Both `robots.txt` and a `robots` meta tag block indexing, deliberately, so a placeholder does not get cemented in search results for an undecided domain. Flip both when the real site ships.
- **No Cloudflare Access.** This is a public holding page. If it ever needs gating, the origin is tunnel-backed, so the origin-lockdown step in `~/.claude/docs/cloudflare-access.md` does not apply.
- **Port block.** `1480` is this project's baseline; `1481` and `1482` are the natural next ports if a stage or sidecar ever appears.
