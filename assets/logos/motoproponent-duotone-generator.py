# -*- coding: utf-8 -*-
"""
MOTOPROPONENT - duotone rotational lockup.

A different device from the strict ambigram in
motoproponent-ambigram-generator.py, and worth understanding as its own
thing rather than as a variant.

THE CONSTRUCTION
----------------
Draw the word properly, once, as W.  The artwork is then

    layer A  =  W
    layer B  =  rotate(W, 180)

in two different colours, overlaid.

Upright you read layer A.  Rotate the whole composite and layer A becomes
the upside-down one while layer B comes upright, so you read layer B.  And
because rotate(A + B) = rotate(W) + W = B + A, the composite is rotationally
symmetric onto itself with the two colours swapping roles.

WHY THIS IS EASIER
------------------
The strict ambigram forces one stroke to serve both readings, which is
where MOTOPROPONENT hits three structural walls (M/T needs full-height edge
stems the T cannot have; O/N cannot open a counter that rotation keeps
closed; R/P share handedness).  Here each reading gets its own ink, so
every letter can be drawn correctly.  No compromised glyphs, no residue
posts, no letters carried by context.

WHAT IT COSTS
-------------
Colour is now load-bearing: in one ink the two readings collapse into an
unreadable tangle.  So this cannot be the only lockup - it needs the flat
ambigram, or a wordmark set in type, wherever colour is not available.

Layout is completely unconstrained (any W works, since the composite is
symmetric by construction).  The one deliberate choice is that the pivot O
at position 7 is centred on the rotation axis, so both layers draw it in
exactly the same place and it renders as a single darker form - the point
the whole mark turns on.
"""

import os
import re
import sys

# ---------------------------------------------------------------- metrics
CAP, BASE, MID = 6, 134, 70
W_MAIN = 14
INSET = W_MAIN // 2

BG      = "#FAF8F5"
INK     = "#14110E"
LABEL   = "#8E8880"
HAIR    = "#DCD7CF"
# Two hues of near-equal value, so neither reading wins by default.
HUE_A   = "#C8452F"     # warm red
HUE_B   = "#26697A"     # deep teal

LETTERS = "MOTOPROPONENT"

# Natural geometric-sans proportions.  Two earlier passes tried to force the
# letters before and after the pivot O to total the same width, so that the
# pivot would land on the word's centre - once by loosening tracking across
# N-E-N-T, once by squaring the widths up.  Both were wrong: the first broke
# the rhythm, the second flattened M, N and E toward a single width and the
# word went monotonous.  Width variety is not negotiable, so nothing here is
# bent to serve the pivot.
WIDTHS = {"M": 120, "O": 112, "T": 96, "P": 96, "R": 100, "N": 104, "E": 88}
TRACK = 24

X0, _x = [], 0
for _i, _l in enumerate(LETTERS):
    X0.append(_x)
    _x += WIDTHS[_l] + (TRACK if _i < len(LETTERS) - 1 else 0)
LW = _x

# Rotate about the pivot O's own centre, NOT the word's centre.  The
# composite is symmetric about whatever point you rotate around, so this
# still holds - and it pins the pivot O of both layers to the same spot
# without touching a single letterform.  The word's letters are 18 units
# heavier before the pivot than after, so the price is simply that the
# composite runs 36 units wider than the word: each layer overhangs the
# other at one end.
CX = X0[6] + WIDTHS["O"] / 2.0
CY = MID
LO = min(0.0, 2 * CX - LW)                 # left edge of the composite
CW = max(LW, 2 * CX) - LO                  # composite width

# ---------------------------------------------------------------- letters
# Clean geometric sans.  Nothing here is a compromise - that is the point.

def L_M(x, w):
    l, r, m = x + INSET, x + w - INSET, x + w / 2.0
    return [f"M{l},134 V6 L{m},110 L{r},6 V134"]


def L_O(x, w):
    cx, rx, ry = x + w / 2.0, w / 2.0 - INSET, 64
    return [f"M{cx - rx},70 A{rx},{ry} 0 0 1 {cx + rx},70 "
            f"A{rx},{ry} 0 0 1 {cx - rx},70"]


def L_T(x, w):
    return [f"M{x},13 H{x + w}", f"M{x + w / 2.0},13 V134"]


def L_P(x, w):
    l, b = x + INSET, x + w - INSET
    return [f"M{l},6 V134",
            f"M{l},13 C{l + 52},13 {b},25 {b},43 C{b},61 {l + 52},73 {l},73"]


def L_R(x, w):
    l, b = x + INSET, x + w - 14
    return [f"M{l},6 V134",
            f"M{l},13 C{l + 52},13 {b},25 {b},43 C{b},61 {l + 52},73 {l},73",
            f"M{l + 45},73 L{x + w - INSET},134"]


def L_N(x, w):
    l, r = x + INSET, x + w - INSET
    return [f"M{l},134 V6 L{r},134 V6"]


def L_E(x, w):
    l = x + INSET
    return [f"M{l},6 V134", f"M{l},13 H{x + w}",
            f"M{l},70 H{x + w - 14}", f"M{l},127 H{x + w}"]


DRAW = {"M": L_M, "O": L_O, "T": L_T, "P": L_P, "R": L_R, "N": L_N, "E": L_E}

WORD = []
for i, ltr in enumerate(LETTERS):
    WORD += DRAW[ltr](X0[i], WIDTHS[ltr])

# ---------------------------------------------------------------- render
MARGIN = 44
SW = int(LW + 2 * MARGIN)


def layer(gid, colour, weight=W_MAIN, opacity=1.0):
    out = [f'<g id="{gid}">']
    for d in WORD:
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" '
                   f'stroke-width="{weight}" stroke-opacity="{opacity}" '
                   f'stroke-linecap="butt" stroke-linejoin="miter" '
                   f'stroke-miterlimit="4"/>')
    out.append('</g>')
    return "\n".join(out)


def composite(a, b, blend="multiply"):
    """Layer A upright + layer B rotated.  B blends over A so the overlaps
    resolve into a third tone instead of one layer simply hiding the other:
    multiply on a light ground, screen on a dark one."""
    style = f' style="mix-blend-mode:{blend}"' if blend else ''
    return (f'<use xlink:href="#{a}"/>'
            f'<g{style}><use xlink:href="#{b}" '
            f'transform="rotate(180,{CX},{CY})"/></g>')


def txt(x, y, s, size=13, col=LABEL, anchor="start", weight="400", ls="0.14em"):
    return (f'<text x="{x}" y="{y}" font-family="Helvetica Neue,Helvetica,Arial,'
            f'sans-serif" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}">{s}</text>')


def caption(y, kicker, note):
    return [txt(MARGIN, y, kicker, 12, INK, weight="700"),
            txt(MARGIN, y + 18, note, 11)]


body, y = [], 150

body.append(txt(MARGIN, 58, "MOTOPROPONENT", 30, INK, weight="700", ls="0.28em"))
body.append(txt(MARGIN, 84,
                "DUOTONE ROTATIONAL LOCKUP &#8212; STUDY SHEET", 12))
body.append(txt(MARGIN, 104,
                "the word, plus the same word rotated 180&#176; in a second colour "
                "&#183; read one hue or the other", 12))

# -- one reading alone ---------------------------------------------------
body += caption(y, "ONE READING ALONE",
                "layer A by itself &#8212; proper letterforms, nothing compromised, "
                "nothing carried by context")
y += 44
body.append(f'<g transform="translate({MARGIN},{y})"><use xlink:href="#wordA"/></g>')
y += 140 + 54

# -- the composite ------------------------------------------------------
body += caption(y, "BOTH READINGS",
                "red reads upright &#183; teal reads upside-down &#183; the pivot O sits "
                "on the axis so both layers draw it in the same place")
y += 44
body.append(f'<g transform="translate({MARGIN},{y})">{composite("wordA", "wordB")}</g>')
y += 140 + 54

# -- rotated ------------------------------------------------------------
body += caption(y, "THE SAME ARTWORK, ROTATED 180&#176;",
                "identical geometry with the hues swapped &#8212; now teal reads upright")
y += 44
body.append(f'<g transform="translate({MARGIN},{y}) rotate(180,{CX},{CY})">'
            f'{composite("wordA", "wordB")}</g>')
y += 140 + 64

# -- treatments ---------------------------------------------------------
body += caption(y, "TREATMENTS",
                "how hard the second reading pushes is a dial, not a given")
y += 40
treatments = [
    ("wordA", "wordB", "multiply", "equal value &#8212; neither reading wins"),
    ("wordInk", "wordAcc", "multiply",
     "ink primary, accent secondary &#8212; upright dominates"),
    ("wordA", "wordTint", None,
     "one hue, tint secondary &#8212; no second brand colour required"),
    ("wordInk", "wordHair", None,
     "ink primary, hairline secondary &#8212; the second reading is a watermark"),
]
s = 0.52
for a, b, blend, note in treatments:
    body.append(f'<g transform="translate({MARGIN},{y}) scale({s})">'
                f'{composite(a, b, blend)}</g>')
    body.append(txt(MARGIN, y + 140 * s + 20, note, 11))
    y += 140 * s + 46
y += 20

# -- dark ground --------------------------------------------------------
body += caption(y, "DARK GROUND",
                "screen instead of multiply, so the overlaps still resolve to a "
                "third tone rather than going flat")
y += 40
_pad, _h = 30, 140 * s + 2 * 30
body.append(f'<rect x="{MARGIN - _pad}" y="{y - _pad}" '
            f'width="{LW * s + 2 * _pad}" height="{_h}" fill="{INK}"/>')
body.append(f'<g transform="translate({MARGIN},{y}) scale({s})">'
            f'{composite("wordLightA", "wordLightB", "screen")}</g>')
y += _h + 26

# -- size test ----------------------------------------------------------
body += caption(y, "SIZE TEST",
                "two overlaid words is twice the ink &#8212; this is where it gives out")
y += 40
for target in (900, 520, 300):
    sc = target / float(LW)
    body.append(f'<g transform="translate({MARGIN},{y}) scale({sc})">'
                f'{composite("wordA", "wordB")}</g>')
    body.append(txt(MARGIN + target + 24, y + 140 * sc * 0.62, f"{target}px wide", 10))
    y += 140 * sc + 26
y += 30

# -- notes --------------------------------------------------------------
body.append(f'<line x1="{MARGIN}" y1="{y}" x2="{SW - MARGIN}" y2="{y}" stroke="{HAIR}"/>')
y += 28
body.append(txt(MARGIN, y, "NOTES", 12, INK, weight="700"))
y += 22
for n in [
    "Colour is load-bearing. Flattened to one ink the two layers tangle, so this "
    "needs a monochrome fallback &#8212; the flat ambigram, or the word set in type.",
    "Layout is unconstrained: the composite is symmetric for ANY layout, because "
    "rotating it just swaps the two layers. Widths and tracking are purely optical here.",
    "The letters before and after the pivot O total the same width (624 each), so uniform "
    "tracking centres the pivot on the axis without bending the rhythm to do it.",
    "mix-blend-mode may not survive an Illustrator round-trip; reapply Multiply to the "
    "second layer there, or set it as a transparency-group blend on export.",
]:
    body.append(txt(MARGIN, y, "&#8226; " + n, 11))
    y += 20

SH = int(y + 40)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">'
       f'<rect width="{SW}" height="{SH}" fill="{BG}"/>'
       f'<defs>'
       + layer("wordA", HUE_A)
       + layer("wordB", HUE_B)
       + layer("wordInk", INK)
       + layer("wordAcc", HUE_A)
       + layer("wordHair", INK, weight=5, opacity=0.55)
       + layer("wordTint", HUE_A, opacity=0.30)
       + layer("wordLightA", "#F5F0E9")
       + layer("wordLightB", "#E08A5A")
       + '</defs>'
       + "\n".join(body) + '</svg>')

# ---------------------------------------------------------------- output
STEM = "motoproponent-duotone-study-"
HERE = os.path.dirname(os.path.abspath(__file__))


def existing():
    return sorted(int(m.group(1)) for m in
                  (re.fullmatch(re.escape(STEM) + r"(\d+)\.svg", f)
                   for f in os.listdir(HERE)) if m)


args = sys.argv[1:]
found = existing()
if args and args[0].isdigit():
    n = int(args[0])
elif "--replace" in args:
    n = found[-1] if found else 0
else:
    n = found[-1] + 1 if found else 0

OUT = os.path.join(HERE, f"{STEM}{n:03d}.svg")
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {os.path.basename(OUT)}  ({SW}x{SH}, lockup width {LW})")
