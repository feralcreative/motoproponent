#!/usr/bin/env bash
# Checks that the page still carries everything the site depends on: analytics,
# search and social tags, icons, and the correct outbound links. Run before
# every PR or zip.
#
#   ./utils/check-page.sh                     check public/index.html
#   ./utils/check-page.sh path/to/index.html  check another copy
#   ./utils/check-page.sh --update            maintainer only: accept the
#                                             current <head> as the new reference
#
# The <head>, minus the contents of its <style> element, is locked by a
# checksum in utils/head.sha256. Any edit there fails the check; only the
# maintainer changes the head, and re-runs with --update in the same commit.
#
# Exits 0 when everything is in order, 1 with a plain-English list otherwise.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REF="$HERE/head.sha256"
UPDATE=0
if [ "${1:-}" = "--update" ]; then
  UPDATE=1
  shift
fi
FILE="${1:-$HERE/../public/index.html}"
if [ ! -f "$FILE" ]; then
  echo "Cannot find $FILE"
  exit 1
fi

sha() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 | cut -d' ' -f1
  else sha256sum | cut -d' ' -f1
  fi
}

# Everything from <head> to </head>, skipping the <style> element.
head_hash() {
  awk '
    /<head>/ { inhead = 1 }
    inhead && /<style>/ && !instyle { line = $0; sub(/<style>.*/, "<style>", line); print line; instyle = 1 }
    inhead && instyle && /<\/style>/ { line = $0; sub(/.*<\/style>/, "</style>", line); print line; instyle = 0; next }
    inhead && !instyle { print }
    /<\/head>/ { inhead = 0 }
  ' "$FILE" | sha
}

if [ "$UPDATE" -eq 1 ]; then
  head_hash > "$REF"
  echo "Updated $REF"
  exit 0
fi

fail=0
BODY="$(awk '/<body/ { on = 1 } on { print }' "$FILE")"

if [ ! -f "$REF" ]; then
  echo "MISSING: utils/head.sha256 reference file"
  fail=1
elif [ "$(head_hash)" != "$(cat "$REF")" ]; then
  echo "CHANGED: the <head> section (analytics, search and preview tags, icons, structured data). Only the CSS inside <style> may change. Restore the original <head>."
  fail=1
fi

body_has() {
  if ! printf '%s\n' "$BODY" | grep -qE -- "$1"; then
    echo "MISSING: $2"
    fail=1
  fi
}
page_forbids() {
  if grep -qE -- "$1" "$FILE"; then
    echo "NOT ALLOWED: $2"
    fail=1
  fi
}

body_has "href=[\"']https://www\.youtube\.com/@motoproponent[\"']"   'YouTube link in the page body (https://www.youtube.com/@motoproponent)'
body_has "href=[\"']https://www\.instagram\.com/m0t0pr0p0nent/[\"']" 'Instagram link in the page body (https://www.instagram.com/m0t0pr0p0nent/, with zeros)'

# Every YouTube or Instagram link in the body must be one of the two above.
BAD_LINKS="$(printf '%s\n' "$BODY" | grep -oE "href=[\"'][^\"']*(youtube\.com|youtu\.be|instagram\.com)[^\"']*[\"']" \
  | grep -vE "^href=[\"'](https://www\.youtube\.com/@motoproponent|https://www\.instagram\.com/m0t0pr0p0nent/)[\"']$")"
if [ -n "$BAD_LINKS" ]; then
  echo "NOT ALLOWED: these links must be exactly https://www.youtube.com/@motoproponent or https://www.instagram.com/m0t0pr0p0nent/:"
  printf '  %s\n' $BAD_LINKS
  fail=1
fi
page_forbids "rel=[\"'][^\"']*noreferrer"  'rel="noreferrer" breaks YouTube Studio traffic attribution; use rel="noopener"'
page_forbids 'M0t0pt0p0nent'               'wrong Instagram handle M0t0pt0p0nent'
page_forbids '[?&](si|srtk|igsh)='         'share-tracking token (?si=, ?srtk=, ?igsh=) in a link'

if [ "$fail" -eq 0 ]; then
  echo "OK: $FILE has every required tag and link."
fi
exit "$fail"
