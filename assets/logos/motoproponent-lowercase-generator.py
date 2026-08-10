# -*- coding: utf-8 -*-
"""
motoproponent - 180 degree rotational ambigram, LOWERCASE.

WHY LOWERCASE
-------------
Every one of the makeambigrams samples that worked was lowercase or mixed
case, and that is not a style coincidence.  All-caps forces two pairs that
are structurally impossible (see README section 4): M/T both need full-height
edge stems that fight each other, and O and N are each already 180-degree
symmetric, so the pair collapses to one glyph and reads as a slashed zero.

Lowercase dissolves most of that, because it has three things caps do not:
ascenders, descenders, and open counters.

THE METRIC SYSTEM IS THE WHOLE TRICK
------------------------------------
    ASC   0      ascender top
    XH   30      x-height top
    MID  85      rotation centre
    BASE 140     baseline
    DESC 170     descender bottom

Rotation about MID maps y -> 170 - y.  The bands are set up so that XH and
BASE are equidistant from MID, and ASC and DESC likewise:

    XH  30  <->  140 BASE      the x-band maps ONTO ITSELF
    ASC  0  <->  170 DESC      ascender space maps to descender space

So an ascender is a descender seen upside down, which is exactly what the
hard pairs need.  Caps have no such spare vertical real estate, which is why
the caps version spent its whole budget fighting.

50/50 - THE CHANGE THAT MATTERS MOST IN THIS PASS
-------------------------------------------------
Studies 000-002 authored the left half to read correctly and let the right
half be whatever fell out.  That yields a crisp "motopro" followed by mush.
For a poster that might be defensible; for a helmet stripe read from either
side it is backwards, because it means there is a good side of his head and
a bad side.

Every glyph is ONE picture serving TWO readings, and where it sits on that
spectrum is a free choice.  This pass pushes each glyph toward the middle:
the whole word is evenly semi-legible instead of half-perfect and half-
broken.  That reads as deliberate texture - which is the "glyph that resolves
once you know the word" effect Jeffrey described - rather than as a wordmark
that gave up partway through.

Concretely, 50/50 means:
  * a glyph's vertical extent is symmetric about MID wherever the pair does
    not forbid it, so neither orientation collects stray ink outside the band
  * shape cues are chosen for the reading that needs them MORE, not for the
    upright one (the o's straight sides below are the clearest case)

THE RULES
---------
Jeffrey never asked for borders.  He described one stroke - the final t's
crossbar, which is also part of the first m - run out to full width, and
noticed it happened to frame the mark.  The frame was the side effect he
liked, not the request.

In studies 000-002 the rules were free-standing horizontals belonging to no
letter, which is exactly why they caged the mark and destroyed the small
sizes.  Here the m owns a foot bar, and that bar is what extends.  Rotated,
the m's foot IS the final t's crossbar, landing exactly where a lowercase t
wants one - which is Jeffrey's construction, transposed.

The rules also stop short of full width.  They run from the outer edge to
somewhat past the pivot, so bottom and top overlap through the centre rather
than closing a box.  The mark stays open at two corners.

WHAT LOWERCASE FIXES ABOUT THE COLOUR LINE
------------------------------------------
Jeffrey asked for one line that is both the e's MIDDLE bar and the t's TOP
bar.  In caps that is geometrically impossible: positions 3 and 11 are a
rotation pair, so height y at one forces 170-y at the other - cap height maps
to baseline, and only mid-height maps to itself.  The caps study had to ship
two mutually exclusive variants, neither matching the description.

A lowercase t's crossbar sits at mid-height naturally.  So a single straight
line at the rotation centre is the t's crossbar AND the e's middle bar,
honestly and simultaneously.  Two of Jeffrey's three devices fall out of
lowercase for free.

PAIR BY PAIR (left half authored, right half is its rotation)
-------------------------------------------------------------
  m <-> t   The m's last leg drops to DESC; rotated it is the final t's
            ascender.  The m's foot bar, rotated, is that t's crossbar.  Both
            of the t's defining strokes are m parts - no residue invented.

  o <-> n   IMPROVED, NOT SOLVED, and an earlier draft of this file claimed
            otherwise, which was wrong.  One picture: a bowl with a gap at
            top centre.  Upright that is an o with a notch; rotated the gap
            is at the bottom, which is an n.  The notch width is a tug-of-war
            with no winning value - narrow enough for a convincing o is too
            narrow for a convincing n (study 000), and wide enough for the n
            turns the o into a u (study 001, where the half read "mutupru").

            The 50/50 move that actually helps: give the bowl STRAIGHT
            VERTICAL SIDES.  Flat sides plus a top arch plus an open bottom
            is emphatically an n, and it costs the o almost nothing, because
            a squared-off o is ordinary.  This buys the n reading without
            spending any of the notch budget.

  t <-> e   CLEAN, and inherently 50/50 - the centred stem and the centred
            mid bar both map onto themselves, so one stroke is the t's stem
            and the e's spine, one bar is both crossbars.  Only the tail is
            asymmetric: it sweeps right off the baseline for the t, and
            rotated it is the e's upper bowl, leaving the e correctly open at
            bottom right.

  p <-> o   The p's descender is deliberately stubby.  The bowl does the work
            of identifying a p, so shortening the descender costs that
            reading little, while every pixel below the baseline becomes a
            tick above the x-height rule on the o at position 9.

  r <-> p   STILL IMPOSSIBLE - r's arm and p's bowl both point right, and 180
            degrees flips handedness.  That is invariant and no amount of
            drawing fixes it.  Balanced as far as it will go: the stem spans
            symmetrically about MID, so the r gets a slight ascender and the
            p gets a real descender out of the same stroke, and the arm is
            drawn as a full open bowl so the p side has something to read.

  o pivot   Authored once and drawn again by the rotation, so the notch at
            top and the notch at bottom fill each other in.  The centre o is
            the only fully closed, fully resolved letter in the mark - which
            is precisely why it makes the small-size sibling.

TIER TWO
--------
Thirteen rotationally symmetric letters is roughly 13:1.  Ideal for a helmet
stripe, useless as an avatar, favicon, corner bug, sticker or embroidery -
all of which the channel needs.  The small-size sibling is a crop of the
pivot o with the colour line through it: legible at 16px, rotationally
symmetric by definition, and visibly a detail lifted from the big mark rather
than a second unrelated logo.
"""

import os
import re
import sys

# ---------------------------------------------------------------- metrics
ASC, XH, MID, BASE, DESC = 0, 30, 85, 140, 170

# Heavier than 000-002.  Helmet paint, vinyl, embroidery and a 32px favicon
# all want mass, and a fat monoline is also the cleanest way to stay a long
# way from blackletter.
W_MAIN, W_RULE, W_LINE = 22, 14, 16

# Bowls are held clear of the rules by INSET, and that is load-bearing rather
# than cosmetic.  In study 000 the bowls were tangent to the rules, which put
# the o's notch exactly on the baseline - so the baseline rule filled the gap
# and every n read back as an o.
INSET = 16
TOP, BOT = XH + INSET, BASE - INSET

BG     = "#FAF8F5"
INK    = "#14110E"
ACCENT = "#C8452F"
LABEL  = "#8E8880"
HAIR   = "#DCD7CF"
SHELL  = "#1B1B1D"
PAINT  = "#F2EDE6"

GAP = 38
LEFT = [                # (letter, width)
    ("m", 172),
    ("o", 118),
    ("t",  98),
    ("o", 118),
    ("p", 116),
    ("r",  98),
]
PIVOT_W = 118

_x, X0 = 0, []
for _l, _w in LEFT:
    X0.append(_x)
    _x += _w + GAP
X0.append(_x)                              # pivot slot
LW = 2 * (_x + PIVOT_W / 2.0)
CX, CY = LW / 2.0, MID

HALF, ROUND = [], []
_TARGET = HALF


def S(d, role="main"):
    _TARGET.append((d, role))


def bowl(cx, sx, top, bot, gap, rr=30):
    """A rounded rectangle open at top centre by 2*gap.

    Straight vertical sides are the point.  A pure ellipse with a gap reads
    as a broken o in both orientations; flat sides plus an arch plus an open
    bottom reads as an n, which is the reading that needs the help."""
    rr = min(rr, sx, (bot - top) / 2.0)
    return (f"M{cx - gap},{top} H{cx - sx + rr} Q{cx - sx},{top} {cx - sx},{top + rr} "
            f"V{bot - rr} Q{cx - sx},{bot} {cx - sx + rr},{bot} "
            f"H{cx + sx - rr} Q{cx + sx},{bot} {cx + sx},{bot - rr} "
            f"V{top + rr} Q{cx + sx},{top} {cx + sx - rr},{top} H{cx + gap}")


# ---------------------------------------------------------------- letters

# Half-width of the o's notch.  Round caps eat W_MAIN/2 at each end, so this
# has to scale with the stroke weight or the gap closes optically.
NOTCH = 26


def draw_m(x, w):
    """Three stems, two round shoulders, a final leg to DESC, and a foot bar.

    Rotated, the leg is the final t's ascender and the foot bar is that t's
    crossbar - so both of the t's defining strokes are parts of the m, which
    is Jeffrey's original device transposed to lowercase."""
    l, mid, r = x + 11, x + w / 2.0, x + w - 11
    sh = TOP + 30                                  # where the shoulder starts
    S(f"M{l},{BASE} V{sh} Q{l},{TOP} {(l + mid) / 2.0},{TOP} "
      f"Q{mid},{TOP} {mid},{sh} V{BASE}")
    S(f"M{mid},{sh} Q{mid},{TOP} {(mid + r) / 2.0},{TOP} "
      f"Q{r},{TOP} {r},{sh} V{DESC}")


def draw_o(x, w):
    """Bowl with straight sides and a notch at top centre.  Upright a squared
    o; rotated, arch over two legs, which is an n."""
    S(bowl(x + w / 2.0, w / 2.0 - 11, TOP, BOT, NOTCH))


def draw_t(x, w):
    """Centred stem and centred mid bar both map onto themselves, so they
    serve the t and the e at once.  The tail off the baseline is, rotated,
    the e's upper bowl - which is why it is a generous sweep, not a flick."""
    cx = x + w / 2.0
    S(f"M{cx},{TOP - 12} V{BASE}")
    S(f"M{cx - 27},{MID} H{cx + 27}")
    S(f"M{cx},{BASE} Q{cx + 42},{BASE} {cx + 42},{BASE - 58}")


def draw_p(x, w):
    """Stubby descender on purpose.  The bowl identifies the p, so cutting
    the descender costs that reading little - and every pixel below the
    baseline is a tick above the x-height rule on the o at position 9."""
    l, r = x + 11, x + w - 11
    S(f"M{l},{TOP - 12} V{BASE + 16}")
    # Bowl squared off to match the o, so the rotated reading at position 9
    # is the same letter the o's at 2 and 4 are, not a rounder cousin.
    S(f"M{l},{TOP} H{r - 23} Q{r},{TOP} {r},{TOP + 26} "
      f"V{BOT - 26} Q{r},{BOT} {r - 23},{BOT} H{l}")


def draw_r(x, w):
    """The sacrificial pair, balanced as far as it will go.  The stem spans
    symmetrically about MID, so the same stroke gives the r a slight ascender
    and the p a real descender.  The arm is a full open bowl rather than a
    flick, so the p side has something to read - but handedness is invariant
    and this pair never fully resolves."""
    l = x + 11
    S(f"M{l},{XH - 14} V{BASE + 14}")
    S(f"M{l},{TOP + 34} Q{l},{TOP} {x + w - 30},{TOP} "
      f"Q{x + w - 11},{TOP} {x + w - 11},{TOP + 30} V{MID + 6}")


DRAW = {"m": draw_m, "o": draw_o, "t": draw_t, "p": draw_p, "r": draw_r}

# The m's foot bar, extended.  Authored on the baseline; its rotation is the
# x-height rule.  It stops past the pivot rather than at the far edge, so the
# two rules overlap through the centre instead of closing a box.
RULE_END = X0[6] + PIVOT_W + 76
S(f"M-16,{BASE} H{RULE_END}", "rule")

for (ltr, w), x in zip(LEFT, X0):
    DRAW[ltr](x, w)
draw_o(X0[6], PIVOT_W)                     # pivot; its own rotation closes it

# The colour centre line.  At MID it maps onto itself, and it is already the
# t's crossbar and the e's crossbar - structural, not decoration.
LINE_STRAIGHT = [f"M0,{MID} H{CX}"]

# ---------------------------------------------------------------- tier two
# The pivot o, cropped out, with the colour line through it.  Drawn twice
# (once rotated) exactly as it is in the wordmark, so the notch closes and
# the roundel is a true detail crop rather than a redrawn lookalike.
_TARGET = ROUND
draw_o(0, PIVOT_W)
_TARGET = HALF
R_CX = PIVOT_W / 2.0
ROUND_LINE = [f"M{-14},{MID} H{PIVOT_W + 14}"]
R_BOX = (-26, XH - 4, PIVOT_W + 52, (BASE + 4) - (XH - 4))   # x, y, w, h

# ---------------------------------------------------------------- render
MARGIN = 44
SW = int(LW + 2 * MARGIN)
GH = DESC

WEIGHT = {"main": W_MAIN, "rule": W_RULE}
C_FINAL = {"main": INK, "rule": INK}
C_DIAG  = {"main": INK, "rule": ACCENT}
C_PAINT = {"main": PAINT, "rule": PAINT}


def strokes_group(gid, strokes, colours):
    out = [f'<g id="{gid}">']
    for d, role in strokes:
        out.append(f'<path d="{d}" fill="none" stroke="{colours[role]}" '
                   f'stroke-width="{WEIGHT[role]}" stroke-linecap="round" '
                   f'stroke-linejoin="round"/>')
    out.append('</g>')
    return "\n".join(out)


def line_group(gid, paths, colour, w=None):
    out = [f'<g id="{gid}">']
    for d in paths:
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" '
                   f'stroke-width="{w or W_LINE}" stroke-linecap="butt"/>')
    out.append('</g>')
    return "\n".join(out)


def mark(gid, line=None):
    out = f'<use xlink:href="#{gid}"/>' \
          f'<use xlink:href="#{gid}" transform="rotate(180,{CX},{CY})"/>'
    if line:
        out += f'<use xlink:href="#{line}"/>' \
               f'<use xlink:href="#{line}" transform="rotate(180,{CX},{CY})"/>'
    return out


def roundel(gid="round-final", line=True):
    out = f'<use xlink:href="#{gid}"/>' \
          f'<use xlink:href="#{gid}" transform="rotate(180,{R_CX},{MID})"/>'
    if line:
        out += '<use xlink:href="#round-line"/>'
    return out


def txt(x, y, s, size=13, col=LABEL, anchor="start", weight="400", ls="0.14em"):
    return (f'<text x="{x}" y="{y}" font-family="Helvetica Neue,Helvetica,Arial,'
            f'sans-serif" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}">{s}</text>')


def caption(y, kicker, note):
    return [txt(MARGIN, y, kicker, 12, INK, weight="700"),
            txt(MARGIN, y + 18, note, 11)]


body, y = [], 150

body.append(txt(MARGIN, 58, "motoproponent", 30, INK, weight="700", ls="0.28em"))
body.append(txt(MARGIN, 84,
                "180&#176; ROTATIONAL AMBIGRAM &#8212; LOWERCASE, STUDY 003", 12))
body.append(txt(MARGIN, 104,
                "50/50 glyphs &#183; heavier monoline &#183; rules owned by the m "
                "&#183; pivot-o roundel as tier two", 12))

# -- structure ----------------------------------------------------------
body += caption(y, "THE MARK &#8212; STRUCTURE ONLY",
                "the m's foot bar, extended &#8212; rotated it is the final t's "
                "crossbar. the rules stop past the pivot, so they overlap through "
                "the centre instead of closing a box")
y += 50
body.append(f'<g transform="translate({MARGIN},{y})">{mark("half-final")}</g>')
y += GH + 60

# -- with colour line ---------------------------------------------------
body += caption(y, "WITH THE COLOUR CENTRE LINE",
                "at mid-height it maps onto itself and is simultaneously the t's "
                "crossbar and the e's middle bar &#8212; the thing caps could not do")
y += 50
body.append(f'<g transform="translate({MARGIN},{y})">'
            f'{mark("half-final", "line-straight")}</g>')
y += GH + 60

# -- rotated proof ------------------------------------------------------
body += caption(y, "ROTATED 180&#176; &#8212; THE 50/50 TEST",
                "identical to the row above, pixel for pixel. the point of this pass: "
                "neither orientation should look like the wrong side")
y += 50
body.append(f'<g transform="translate({MARGIN},{y}) rotate(180,{CX},{CY})">'
            f'{mark("half-final", "line-straight")}</g>')
y += GH + 60

# -- authored half ------------------------------------------------------
body += caption(y, "WHAT IS ACTUALLY DRAWN",
                "only the left half and the pivot o are authored; the right half is "
                "this, rotated. symmetry is by construction, not by eye")
y += 50
body.append(f'<g transform="translate({MARGIN},{y})">'
            f'<use xlink:href="#half-diag"/></g>')
y += GH + 60

# -- tier two -----------------------------------------------------------
body += caption(y, "TIER TWO &#8212; THE ROUNDEL",
                "the pivot o, cropped, with the colour line through it. the only "
                "fully closed letter in the mark, and the axis it rotates around")
y += 46
rx = MARGIN
for px in (168, 96, 56, 32, 16):
    sc = px / float(R_BOX[3])
    body.append(f'<g transform="translate({rx},{y}) scale({sc}) '
                f'translate({-R_BOX[0]},{-R_BOX[1]})">{roundel()}</g>')
    body.append(txt(rx, y + 168 + 20, f"{px}px", 10))
    rx += R_BOX[2] * sc + 40
# same again, knocked out of the shell colour
rx += 40
body.append(f'<rect x="{rx - 20}" y="{y - 16}" width="{168 * (R_BOX[2] / R_BOX[3]) + 40}" '
            f'height="{168 + 32}" fill="{SHELL}"/>')
sc = 168 / float(R_BOX[3])
body.append(f'<g transform="translate({rx},{y}) scale({sc}) '
            f'translate({-R_BOX[0]},{-R_BOX[1]})">{roundel("round-paint")}</g>')
body.append(txt(rx - 20, y + 168 + 36, "reversed", 10))
y += 168 + 76

# -- helmet stripe ------------------------------------------------------
body += caption(y, "HELMET STRIPE",
                "the actual brief: painted down the crown it has to read the same "
                "from either side &#8212; second band is the first one rotated")
y += 44
hs = 0.46
band_h = GH * hs + 56
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
body += caption(y, "SIZE TEST",
                "the wordmark is a stripe, not a logo &#8212; below about 400px it "
                "is texture, which is what tier two is for")
y += 44
for target in (860, 460, 260):
    sc = target / float(LW)
    body.append(f'<g transform="translate({MARGIN},{y}) scale({sc})">'
                f'{mark("half-final", "line-straight")}</g>')
    body.append(txt(MARGIN + target + 24, y + GH * sc * 0.62, f"{target}px wide", 10))
    y += GH * sc + 26
y += 30

# -- notes --------------------------------------------------------------
body.append(f'<line x1="{MARGIN}" y1="{y}" x2="{SW - MARGIN}" y2="{y}" stroke="{HAIR}"/>')
y += 28
body.append(txt(MARGIN, y, "NOTES", 12, INK, weight="700"))
y += 22
for n in [
    "50/50 is the change that matters. Studies 000-002 optimised every glyph for its "
    "upright reading, which gave a crisp \"motopro\" and then mush. For an object read "
    "from both sides that means a good side and a bad side.",
    "The metric system is the design. XH and BASE are equidistant from MID, so the "
    "x-band maps onto itself; ASC and DESC likewise, so an ascender is a descender "
    "upside down. Caps have no spare vertical real estate and that is why they lost.",
    "The rules are no longer free-standing. The m owns a foot bar and that bar is what "
    "extends - rotated, it is the final t's crossbar. They also stop past the pivot, so "
    "top and bottom overlap through the centre rather than boxing the mark in.",
    "o/n is improved, not solved. The notch width has no winning value; what helps is "
    "giving the bowl straight sides, which sells the n and costs the o nothing.",
    "r/p is still impossible. r's arm and p's bowl both point right and rotation flips "
    "handedness. Balanced as far as it goes, but this pair does not resolve.",
    "Tier two exists because 13 symmetric letters is 13:1 - a stripe, not an avatar.",
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
       + strokes_group("round-final", ROUND, C_FINAL)
       + strokes_group("round-paint", ROUND, C_PAINT)
       + line_group("line-straight", LINE_STRAIGHT, ACCENT)
       + line_group("round-line", ROUND_LINE, ACCENT)
       + '</defs>'
       + "\n".join(body) + '</svg>')

# ---------------------------------------------------------------- output
STEM = "motoproponent-lowercase-study-"
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
