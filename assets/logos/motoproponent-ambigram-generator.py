# -*- coding: utf-8 -*-
"""
MOTOPROPONENT - 180 degree rotational ambigram.

Built to Jeffrey's brief (see original/brief.md), which changes the target:
the mark is NOT meant to be legible cold.  It is a glyph that resolves into
the word once you already know what it says.  Three of the six letter pairs
are structurally obstructed (see README section 4) and under this brief that
is texture rather than failure, so nothing here fights it.

THE THREE DEVICES FROM THE ORIGINAL
-----------------------------------
(a) The last T's crossbar - which is also part of the first M - runs the full
    width as an underline and a top border.  One authored stroke does both:
    a full-width rule on the baseline whose rotation is a full-width rule on
    the cap line.

(b) A colour centre line through the mark.  Two readings of Jeffrey's
    description are geometrically possible and they are mutually exclusive;
    both are built here.  See LINE_STRAIGHT / LINE_ZIGZAG below.

(c) Rounder bowls and more air than the recreation sketch, which Jeffrey
    calls "more squished in than it needs to be" with circles "a little too
    oblong".

ARCHITECTURE
------------
The artwork is authored ONCE, for the left half plus the pivot letter, in
one word-space coordinate system.  The right half is never drawn - it is the
authored half rotated 180 degrees about the pivot:

    <use href="#half"/>
    <use href="#half" transform="rotate(180, CX, CY)"/>

So the mark is rotationally symmetric by construction, which is the whole
point: painted down the crown of a helmet it reads the same from either side.

WHAT THE BORDER RULES BUY
-------------------------
With a rule on both the cap line and the baseline, every letter is bracketed
top and bottom, and several letters stop needing strokes of their own:

    T at p3, p13   crossbar comes from the cap rule
    E at p11       top AND bottom arms come from the rules
    M at p1        sits on the baseline rule

which leaves the E needing only a spine and a middle arm.  The spine is the
T's stem (centred, so it maps onto itself), and the middle arm is the colour
line.  That is why device (b) is structural rather than decorative, and it
is the strongest argument that the line runs at mid-height.
"""

import os
import re
import sys

# ---------------------------------------------------------------- metrics
CAP, BASE, MID = 6, 134, 70
W_MAIN, W_SEC, W_RULE, W_LINE = 16, 11, 12, 14

BG     = "#FAF8F5"
INK    = "#14110E"
SEC    = "#7A736B"
ACCENT = "#C8452F"
LABEL  = "#8E8880"
HAIR   = "#DCD7CF"
SHELL  = "#1B1B1D"      # helmet shell
PAINT  = "#F2EDE6"      # helmet paint, light

# Left half + pivot.  Roomier than the sketch, per device (c).
LEFT = [               # (letter, width, gap after)
    ("M", 130, 30),
    ("O", 118, 30),
    ("T",  90, 30),
    ("O", 118, 30),
    ("P",  96, 30),
    ("R", 112, 30),
]
PIVOT_W = 118

_x, X0 = 0, []
for _l, _w, _g in LEFT:
    X0.append(_x)
    _x += _w + _g
X0.append(_x)
LW = 2 * (_x + PIVOT_W / 2.0)
CX, CY = LW / 2.0, MID

HALF = []


def S(d, role="main"):
    HALF.append((d, role))


# ---------------------------------------------------------------- letters

def draw_M(x, w):
    """Stems + V as one mitred polyline, plus a tail from the apex down to
    the baseline rule.  Rotated, that tail is the final T's stem and the cap
    rule is its crossbar - device (a) in Jeffrey's brief, and the reason the
    rule has to run the full width rather than stopping at the letter."""
    l, r, m = x + 8, x + w - 8, x + w / 2.0
    S(f"M{l},134 V6 L{m},84 L{r},6 V134")
    S(f"M{m},84 V134")


def draw_O(x, w):
    """Near-circular, per device (c) - the sketch's O's are too oblong.  The
    diagonal is the N's, sitting at 45 degrees inside the bowl so it reads as
    an interior detail rather than slashing out to the corners."""
    cx, rx, ry = x + w / 2.0, w / 2.0 - 8, 64
    S(f"M{cx - rx},70 A{rx},{ry} 0 0 1 {cx + rx},70 "
      f"A{rx},{ry} 0 0 1 {cx - rx},70")
    S(f"M{cx - 36},34 L{cx + 36},106")


def draw_T(x, w):
    """Just a centred stem.  The crossbar is the cap rule, and because the
    stem is centred it maps onto itself under rotation, so it is also the E's
    spine at p11.  The E's middle arm is the colour line."""
    S(f"M{x + w / 2.0},6 V134")


def draw_P(x, w):
    """Rotated, the bowl becomes a lowercase o sitting on the baseline and
    the stem becomes a post to its right."""
    l, ry = x + 8, 42
    S(f"M{l},6 V134")
    S(f"M{l},14 A{w - 40},{ry} 0 0 1 {l},{14 + 2 * ry}")


def draw_R(x, w):
    """The leg lands on a full-height post at the right edge; rotated, that
    post is the P's left stem at p8.  With rules top and bottom the post
    reads as part of the framing rather than as residue."""
    l, ry, post = x + 8, 38, x + w - 8
    S(f"M{l},6 V134")
    S(f"M{l},14 A{w - 48},{ry} 0 0 1 {l},{14 + 2 * ry}")
    S(f"M{l + 46},{14 + 2 * ry} L{post},134")
    S(f"M{post},6 V134", "sec")


DRAW = {"M": draw_M, "O": draw_O, "T": draw_T, "P": draw_P, "R": draw_R}

# Device (a): one authored baseline rule; its rotation is the cap rule.
# Laid down first so it sits behind the letters.
S(f"M0,134 H{LW}", "rule")

for (ltr, w, _g), x in zip(LEFT, X0):
    DRAW[ltr](x, w)
draw_O(X0[6], PIVOT_W)                     # pivot, self-rotational

# ---------------------------------------------------------------- device (b)
# Two readings of "from the center of the first O ... to become the middle
# bar of the E ... as it passes through it becomes the top bar of the T".
#
# Positions 3 and 11 are a rotation pair, so the line's height at one forces
# its height at the other: y maps to 140 - y.  Cap height maps to baseline;
# only mid-height maps to itself.  So the line cannot be both the T's top bar
# and the E's MIDDLE bar.  Each variant keeps one half of the description.
#
# Both are authored as a left half and completed by the same rotation as the
# letters, so either way the line is self-rotational.

O1_CX = X0[1] + LEFT[1][1] / 2.0           # centre of the first O (p2)
T1_CX = X0[2] + LEFT[2][1] / 2.0           # centre of the T (p3)

# Straight: mid-height throughout.  Passes through the first O's centre, the
# pivot O and the E's middle arm; crosses the T at mid-stem rather than at
# its top.  Reads literally as a helmet centre stripe.
LINE_STRAIGHT = [f"M0,70 H{CX}"]

# Zigzag: rises from the first O's centre to cap height at the T, so it IS
# the T's top bar - and therefore, rotated, the E's BOTTOM arm.
LINE_ZIGZAG = [f"M0,70 L{O1_CX},70 L{T1_CX},14 L{CX},70"]

# ---------------------------------------------------------------- roundel
ROUNDEL = []


def R_(d, role="main"):
    ROUNDEL.append((d, role))


R_("M0,120 H130", "rule")
R_("M50,70 A50,50 0 1 1 150,70 A50,50 0 1 1 50,70")

# ---------------------------------------------------------------- geometry
LETTERS = "MOTOPROPONENT"
BOX_L = [(x, x + w) for (_l, w, _g), x in zip(LEFT, X0)]
BOX_L.append((X0[6], X0[6] + PIVOT_W))
BOXES = BOX_L + [(LW - b, LW - a) for (a, b) in reversed(BOX_L[:-1])]

# ---------------------------------------------------------------- render
MARGIN = 44
SW = int(LW + 2 * MARGIN)


def strokes_group(gid, strokes, colours):
    out = [f'<g id="{gid}">']
    for d, role in strokes:
        out.append(f'<path d="{d}" fill="none" stroke="{colours[role]}" '
                   f'stroke-width="{WEIGHT[role]}" stroke-linecap="butt" '
                   f'stroke-linejoin="miter" stroke-miterlimit="4"/>')
    out.append('</g>')
    return "\n".join(out)


def line_group(gid, paths, colour):
    out = [f'<g id="{gid}">']
    for d in paths:
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" '
                   f'stroke-width="{W_LINE}" stroke-linecap="butt" '
                   f'stroke-linejoin="miter"/>')
    out.append('</g>')
    return "\n".join(out)


WEIGHT = {"main": W_MAIN, "sec": W_SEC, "rule": W_RULE}
C_FINAL = {"main": INK, "sec": INK, "rule": INK}
C_DIAG  = {"main": INK, "sec": SEC, "rule": ACCENT}
C_PAINT = {"main": PAINT, "sec": PAINT, "rule": PAINT}


def mark(gid, line=None):
    out = f'<use xlink:href="#{gid}"/>' \
          f'<use xlink:href="#{gid}" transform="rotate(180,{CX},{CY})"/>'
    if line:
        out += f'<use xlink:href="#{line}"/>' \
               f'<use xlink:href="#{line}" transform="rotate(180,{CX},{CY})"/>'
    return out


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
                "180&#176; ROTATIONAL AMBIGRAM &#8212; BUILT TO THE ORIGINAL BRIEF", 12))
body.append(txt(MARGIN, 104,
                "full-width rules top and bottom &#183; rounder bowls &#183; more air "
                "&#183; two readings of the colour centre line", 12))

# -- structure, no colour line ------------------------------------------
body += caption(y, "THE MARK &#8212; STRUCTURE ONLY",
                "device (a): one authored baseline rule, whose rotation is the top border")
y += 44
body.append(f'<g transform="translate({MARGIN},{y})">{mark("half-final")}</g>')
y += 140 + 60

# -- variant A ----------------------------------------------------------
body += caption(y, "COLOUR LINE &#8212; STRAIGHT",
                "mid-height throughout: first O's centre, pivot O, and the E's MIDDLE "
                "arm &#183; crosses the T at mid-stem")
y += 44
body.append(f'<g transform="translate({MARGIN},{y})">'
            f'{mark("half-final", "line-straight")}</g>')
y += 140 + 60

# -- variant B ----------------------------------------------------------
body += caption(y, "COLOUR LINE &#8212; ZIGZAG",
                "rises to cap height at the T so it IS the T's top bar &#8212; which "
                "forces it to be the E's BOTTOM arm, not the middle")
y += 44
body.append(f'<g transform="translate({MARGIN},{y})">'
            f'{mark("half-final", "line-zigzag")}</g>')
y += 140 + 60

# -- rotated proof ------------------------------------------------------
body += caption(y, "ROTATED 180&#176;",
                "the straight variant, actually rotated &#8212; identical to its row "
                "above, pixel for pixel")
y += 44
body.append(f'<g transform="translate({MARGIN},{y}) rotate(180,{CX},{CY})">'
            f'{mark("half-final", "line-straight")}</g>')
y += 140 + 64

# -- helmet stripe ------------------------------------------------------
body += caption(y, "HELMET STRIPE",
                "the actual brief: painted down the crown, it has to read the same from "
                "either side &#8212; second band is the first one rotated")
y += 40
hs = 0.46
band_h = 140 * hs + 56
for label in ("left side", "right side &#8212; same artwork, rotated"):
    body.append(f'<rect x="{MARGIN}" y="{y}" width="{LW * hs}" height="{band_h}" '
                f'fill="{SHELL}"/>')
    rot = "" if "left" in label else f" rotate(180,{CX},{CY})"
    body.append(f'<g transform="translate({MARGIN},{y + 28}) scale({hs})'
                f'{rot}">{mark("half-paint", "line-straight")}</g>')
    body.append(txt(MARGIN, y + band_h + 18, label, 10))
    y += band_h + 40
y += 24

# -- size test ----------------------------------------------------------
body += caption(y, "SIZE TEST", "the border rules are what survive longest")
y += 40
for target in (860, 460, 260):
    sc = target / float(LW)
    body.append(f'<g transform="translate({MARGIN},{y}) scale({sc})">'
                f'{mark("half-final", "line-straight")}</g>')
    body.append(txt(MARGIN + target + 24, y + 140 * sc * 0.62, f"{target}px wide", 10))
    y += 140 * sc + 26
y += 30

# -- notes --------------------------------------------------------------
body.append(f'<line x1="{MARGIN}" y1="{y}" x2="{SW - MARGIN}" y2="{y}" stroke="{HAIR}"/>')
y += 28
body.append(txt(MARGIN, y, "NOTES", 12, INK, weight="700"))
y += 22
for n in [
    "The two colour-line variants are mutually exclusive. Positions 3 and 11 are a "
    "rotation pair, so height y at one is height 140-y at the other: cap maps to "
    "baseline, and only mid-height maps to itself.",
    "The straight variant is the one the structure wants. With rules top and bottom the "
    "E already has its top and bottom arms, so the only thing missing is a middle arm - "
    "which is exactly what a mid-height line supplies.",
    "It is also the one a helmet wants: a centre stripe is a straight line front to back.",
    "Not legible cold, by design. Per the brief this is a glyph that resolves once you "
    "know the word, not a wordmark.",
]:
    body.append(txt(MARGIN, y, "&#8226; " + n, 11))
    y += 20

SH = int(y + 40)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">'
       f'<rect width="{SW}" height="{SH}" fill="{BG}"/>'
       f'<defs>'
       + strokes_group("half-final", HALF, C_FINAL)
       + strokes_group("half-diag", HALF, C_DIAG)
       + strokes_group("half-paint", HALF, C_PAINT)
       + line_group("line-straight", LINE_STRAIGHT, ACCENT)
       + line_group("line-zigzag", LINE_ZIGZAG, ACCENT)
       + strokes_group("roundel", ROUNDEL, C_FINAL)
       + '</defs>'
       + "\n".join(body) + '</svg>')

# ---------------------------------------------------------------- output
STEM = "motoproponent-ambigram-study-"
HERE = os.path.dirname(os.path.abspath(__file__))


def existing():
    ns = []
    for f in os.listdir(HERE):
        m = re.fullmatch(re.escape(STEM) + r"(\d+)\.svg", f)
        if m:
            ns.append(int(m.group(1)))
    return sorted(ns)


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
