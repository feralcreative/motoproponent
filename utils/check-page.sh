#!/usr/bin/env bash
# Checks that every page carries what the site depends on: analytics, search
# and link-preview tags, icons, and correct outbound links. Run before every
# PR or zip.
#
#   ./utils/check-page.sh               check every .html file under public/
#   ./utils/check-page.sh a.html b.html check specific files
#
# Exits 0 when every page passes, 1 with a plain-English list otherwise.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PUBLIC="$HERE/../public"

if [ "$#" -gt 0 ]; then
  FILES=("$@")
else
  FILES=()
  while IFS= read -r f; do FILES+=("$f"); done < <(find "$PUBLIC" -name '*.html' ! -name '50x.html' | sort)
fi

fail=0
for FILE in "${FILES[@]}"; do
  if [ ! -f "$FILE" ]; then
    echo "Cannot find $FILE"
    fail=1
    continue
  fi
  name="$(basename "$FILE")"
  problems=()

  need() { grep -qE -- "$1" "$FILE" || problems+=("MISSING: $2"); }
  forbid() { grep -qE -- "$1" "$FILE" && problems+=("NOT ALLOWED: $2"); }

  need '<title>[^<]+</title>'                                   'a non-empty <title>'
  need '<meta name="description" content="[^"]+"'              'meta description'
  need "gtag\\('config', 'G-3YRCXQL242'\\)"                     'Google Analytics (GA4) snippet, copied from public/index.html'
  need 'googletagmanager\.com/gtag/js\?id=G-3YRCXQL242'         'Google Analytics (GA4) loader script'
  need '<link rel="canonical" href="https://motoproponent\.com/' 'canonical link to this page'"'"'s own https://motoproponent.com/ URL'
  need '<meta name="robots" content="noindex, nofollow"'        'robots noindex tag (Ziad removes it on launch day)'
  need 'property="og:title" content="[^"]+"'                    'Open Graph title (link previews)'
  need 'property="og:description" content="[^"]+"'              'Open Graph description (link previews)'
  need 'property="og:image" content="https://motoproponent\.com/' 'Open Graph image (absolute https://motoproponent.com/ URL)'
  need 'property="og:url" content="https://motoproponent\.com/' 'Open Graph URL'
  need 'name="twitter:card"'                                    'Twitter/X card tag'
  need 'rel="icon"'                                             'favicon'
  need 'rel="apple-touch-icon"'                                 'Apple touch icon'

  if [ "$name" = "index.html" ] && [ "$(dirname "$FILE")" -ef "$PUBLIC" ]; then
    need '"@type": "Person"'                                    'structured data (JSON-LD Person block) on the home page'
    need "href=[\"']https://www\\.youtube\\.com/@motoproponent[\"']"    'YouTube link on the home page'
    need "href=[\"']https://www\\.instagram\\.com/m0t0pr0p0nent/[\"']"  'Instagram link on the home page'
  fi

  bad="$(grep -oE "href=[\"'][^\"']*(youtube\\.com/@|youtube\\.com/c/|youtube\\.com/channel|instagram\\.com)[^\"']*[\"']" "$FILE" \
    | grep -vE "^href=[\"'](https://www\\.youtube\\.com/@motoproponent|https://www\\.instagram\\.com/m0t0pr0p0nent/)[\"']$")"
  [ -n "$bad" ] && problems+=("NOT ALLOWED: channel/profile links must be exactly https://www.youtube.com/@motoproponent or https://www.instagram.com/m0t0pr0p0nent/ (found: $(echo $bad))")
  forbid "rel=[\"'][^\"']*noreferrer"  'rel="noreferrer" breaks YouTube Studio traffic attribution; use rel="noopener"'
  forbid 'M0t0pt0p0nent'               'wrong Instagram handle M0t0pt0p0nent'
  forbid '[?&](si|srtk|igsh)='         'share-tracking token (?si=, ?srtk=, ?igsh=) in a link'

  if [ "${#problems[@]}" -eq 0 ]; then
    echo "OK: $FILE"
  else
    echo "FAIL: $FILE"
    printf '  %s\n' "${problems[@]}"
    fail=1
  fi
done

exit "$fail"
