# Architecture

## Site

| Path | Role |
| --- | --- |
| `public/index.html` | The whole page. Our `<head>`, Jeffrey's `<style>` and `<body>` |
| `public/assets/` | Jeffrey's photos: background, YouTube card, Instagram card. Default caching |
| `public/static/` | Social card and touch icon. Cached for one year; rename on change |
| `public/robots.txt` | `Allow: /`, launch checklist in comments |
| `nginx.conf` | Caching, `/subscribe` redirect, security and referrer headers, `X-Robots-Tag` |
| `Dockerfile` | `nginx:1.27-alpine`, copies `nginx.conf` and `public/` whole |
| `docker-compose.yml` | Host `1480` → container `80` on the NAS |

There is no JavaScript beyond the GA4 snippet, no build step, and no backend.

## Lowercase ambigram

Generator: `assets/logos/motoproponent-lowercase-generator.py`. Latest study: `motoproponent-lowercase-study-003.svg`. Not used on the site.

Only the left half and the pivot letter are authored. The right half is the same artwork rotated:

```html
<use href="#half"/>
<use href="#half" transform="rotate(180, CX, CY)"/>
```

Symmetry is therefore true by construction.

Metrics, where rotation maps `y` to `170 − y`:

```text
ASC 0 · XH 30 · MID 85 · BASE 140 · DESC 170
XH 30 ↔ 140 BASE     the x-height band maps onto itself
ASC 0 ↔ 170 DESC     an ascender is a descender upside down
```

Pairs (letter *i* is the rotation of letter *14 − i*):

| Pair | Status |
| --- | --- |
| m ↔ t | Works: the `m`'s dropped last leg becomes the `t`'s ascender; its foot bar becomes the crossbar |
| o ↔ n | Compromise: no notch width wins; straight bowl sides sell the `n` |
| t ↔ e | Clean: centred stem and centred bar map onto themselves |
| p ↔ o | Works: the stubby descender becomes a small tick above the rule |
| r ↔ p | Impossible: both point right, and rotation flips handedness |
| o (pivot) | Drawn twice, so its notch fills itself in |

`build-presentation.py` lifts artwork out of the study sheets into `presentation.html` (the client page), namespacing every SVG id per instance. Re-run it after any study change.
