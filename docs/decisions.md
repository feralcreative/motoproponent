# Decisions

Why deliberate choices are the way they are, so they are not "fixed". Newest at the bottom.

## Referrer is preserved on purpose

`nginx.conf` sends `Referrer-Policy: strict-origin-when-cross-origin`, and outbound links use `rel="noopener"` without `noreferrer`. YouTube Studio attributes external traffic by the `Referer` header, not by URL parameters, so this is the only way visits from the site show up as "External → motoproponent.com". Rejected: `no-referrer` and `noreferrer`, which silently delete that measurement.

## `expires` only inside nginx `location` blocks

Any `add_header` in a `location` suppresses inheritance of every server-level `add_header`. Because `index index.html` makes `/` re-match `location = /index.html`, one `add_header` there strips the security headers from the only page. `expires` is not an `add_header`, so inheritance survives.

## Crawlable plus `noindex`

`robots.txt` allows everything while the page carries `noindex` (meta tag and `X-Robots-Tag`). Blocking the crawl would stop Google from ever reading the `noindex`, and a single inbound link would then list the bare URL. To de-index later: add `noindex`, wait for the recrawl in Search Console, and only then `Disallow`.

## Webroot is `public/`, not `site/`

The boilerplate `.gitignore` ignores `site/` as MkDocs output, which silently kept static assets untracked. Builds read the filesystem, so the failure only shows from a fresh clone.

## Dockerfile copies the whole webroot

Enumerating files in `COPY` produces builds that succeed, deploy, pass the health check, and 404 on the asset just added.

## Person, not Organization, in JSON-LD

Motoproponent is one person under a name. Switching to `Organization` later would break the entity rather than upgrade it. `sameAs` ties the domain to the channel and Instagram; both URLs must resolve.

## `/subscribe` is a 302

A vanity redirect for stickers and end cards, countable in the access log. 302 so the target stays changeable; `noindex` so it never becomes a URL in its own right.

## Jeffrey's design adopted as delivered (2026-11-11)

Jeffrey vibe-coded a placeholder with two equal YouTube and Instagram cards. The user chose to ship it as he designed it, overriding `docs/website-scope.md`'s "one door" guidance and Codex's recommendation to demote Instagram. Only technical fixes were applied: our `<head>` kept, `noreferrer` and share tokens removed, the mislabelled `.webp` renamed `.jpg`.

## Instagram handle is `m0t0pr0p0nent`

The repo previously recorded `M0t0pt0p0nent`, which is not a live account. Verified 2026-11-11 that `instagram.com/m0t0pr0p0nent` is Jeffrey's. `@motoproponent` was already taken.

## Social card is a screenshot of the page

`public/static/og-20261111.png` is a 1200×630 screenshot of the live design. Dated filename because `/static/` is cached for a year at the edge.

## Logo: lowercase over uppercase

Lowercase has spare vertical space capitals lack: ascenders rotate into descenders and the x-height band maps onto itself, which makes several pairs workable that are obstructed in caps. The `r`/`p` pair stays impossible in either case, because 180° rotation does not preserve handedness. Lowercase was presented to the client in August 2026; concept studies followed in November 2026 (`motoproponent-ambigram-study-005`–`008`, from `motoproponent-concepts-generator.py`). Which direction is current is not recorded.

## Logo study 003 choices

Glyphs drawn to read about equally either way up, rather than a crisp first half and mush after it, because the mark is read from both sides of a helmet. Heavier stroke (`W_MAIN` 22) for paint, vinyl, and favicon use. Rules are owned by the `m`'s foot bar, which rotates into the final `t`'s crossbar. A pivot-`o` roundel exists as the small-size tier. The `o`/`n` pair is a compromise, not solved: no notch width reads well both ways.
