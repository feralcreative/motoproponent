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

Saving the hostname auto-creates the proxied DNS record pointing at `<tunnel-id>.cfargotunnel.com`.

**Do not add a `www` tunnel hostname.** `www` is handled entirely at the edge — see the next section — so the request never reaches the origin and a second tunnel route would be dead weight. (`tankbag.app` 404s on `www` because neither was done there.)

## 3a. Canonical host — `www` → apex

Already applied, documented here so it is not undone by accident. The apex is canonical; `www` exists only to redirect to it.

| What | Where | Value |
| --- | --- | --- |
| DNS | Cloudflare DNS | `CNAME www → motoproponent.com`, **proxied** |
| Redirect | Rules → Redirect Rules | if `http.host eq "www.motoproponent.com"` → `concat("https://motoproponent.com", http.request.uri.path)`, **301**, preserve query string |

Because the rule fires at the edge, `www` never touches the tunnel or the container. Verify with:

```bash
curl -sI https://www.motoproponent.com/some/path?x=1 | grep -iE '^HTTP/|^location'
```

Expect `301` and `location: https://motoproponent.com/some/path?x=1`. Note that rules take a few seconds to propagate — an initial 404 immediately after saving is propagation lag, not a broken rule.

## 3b. Zone settings

Also already applied. All of these are dashboard state, invisible to `git` and untouched by `prod.sh`.

| Setting | Value | Why |
| --- | --- | --- |
| Always Use HTTPS | on | edge-level http → https 301 |
| HSTS | on, `max-age` 6 months, no preload, no subdomains | preload is effectively irreversible; skip it |
| Always Online | on | the origin is a home NAS on a residential line |
| Early Hints | on | free |
| Rocket Loader | **off** | reorders scripts, hurts INP |
| Minimum TLS | 1.2 | was 1.0 |
| Web Analytics | on, automatic | edge-injected beacon, no repo change |

Web Analytics has to be enabled by hand in **Analytics & Logs → Web Analytics**. There is no API route: Cloudflare ships no write permission group for RUM, so a scoped token can read the site list but never create one.

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

- **The page is `noindex`, but crawling is ALLOWED.** That combination is deliberate and the ordering matters: `robots.txt` controls crawling, the meta tag controls indexing, and blocking the crawl stops Google from ever reading the `noindex` — which is how a bare, snippet-less URL gets stuck in the index. `site/robots.txt` carries the full explanation and the launch-day checklist.
- **Webroot is `site/`.** Everything public lives there and the Dockerfile copies the whole directory. Do not go back to listing filenames in `COPY` — that ships builds which succeed, deploy, pass the health check, and 404 on the new asset. Note also that `.dockerignore` excludes `assets/` and `docs/`, so a `COPY` from either hard-fails.
- **`Referrer-Policy` in `nginx.conf` is load-bearing.** YouTube Studio attributes external traffic by the `Referer` header, so tightening it to `no-referrer` would silently destroy the only measurement of whether the site sends anyone to the channel. Same reason links to YouTube must not carry `rel="noreferrer"`.
- **`/subscribe`** 302s to the channel with `?sub_confirmation=1`. Printable on stickers and end-cards, countable in the access log, one line to change if the handle moves.
- **Search Console / Bing.** Verify GSC as a **Domain** property via a Cloudflare DNS `TXT` record, not a URL-prefix property — Domain covers apex, `www`, both protocols and any future subdomain, and DNS verification survives deploys and webroot moves. Leave that TXT record in place forever; deleting it un-verifies the property. Then import into Bing Webmaster Tools in one click.
- **No Cloudflare Access.** This is a public holding page. If it ever needs gating, the origin is tunnel-backed, so the origin-lockdown step in `~/.claude/docs/cloudflare-access.md` does not apply.
- **Port block.** `1480` is this project's baseline; `1481` and `1482` are the natural next ports if a stage or sidecar ever appears.
