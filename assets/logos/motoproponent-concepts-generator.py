# -*- coding: utf-8 -*-
"""
MOTOPROPONENT — multi-direction concept studies.

Companion to motoproponent-ambigram-generator.py. That script solves the problem
at the letterform level (and pays for it in compromised glyphs). These four
concepts solve it at the *arrangement* level instead, so nothing is distorted:

  wheel   — rotational symmetry of the whole mark; one copy is always upright
  column  — MOTO stacked vertically is a true mirror ambigram, no cheating
  card    — the word plus its own 180° twin; legible either way by construction
  hidden  — MOTO · PRO · ONE already sit inside the name, in order

Letterforms here are placeholder system type: every character is positioned
individually on a fixed advance, so the LAYOUT is font-independent even though
the shapes are not. Swap FONT for the real brand face.

Usage
  python3 motoproponent-concepts-generator.py            # all four, sequential
  python3 motoproponent-concepts-generator.py wheel      # just one
  python3 motoproponent-concepts-generator.py card 12    # force study-012
"""

import math
import os
import re
import sys

WORD = "MOTOPROPONENT"

INK   = "#14110E"
GHOST = "#C8452F"
LABEL = "#8E8880"
RULE  = "#D8D3CB"
FAINT = "#DDD8D0"
BG    = "#FAF8F5"

FONT = "Futura, Century Gothic, Avenir Next, Poppins, Helvetica Neue, Arial, sans-serif"
UI   = "Helvetica Neue, Helvetica, Arial, sans-serif"

SW = 1560
STEM = "motoproponent-ambigram-study-"
HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ helpers
def label(x, y, s, size=12, col=LABEL, weight="400", anchor="start", ls="0.14em"):
    return (f'<text x="{x}" y="{y}" font-family="{UI}" font-size="{size}" fill="{col}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def chars(s, x0, y, size, adv, fill=INK, weight="500", opacity=1.0):
    """Lay out a string on a fixed advance. Returns (svg, total_width)."""
    out = []
    for i, c in enumerate(s):
        cx = x0 + adv * (i + 0.5)
        out.append(f'<text x="{cx:.1f}" y="{y}" font-family="{FONT}" font-size="{size}" '
                   f'fill="{fill}" font-weight="{weight}" text-anchor="middle" '
                   f'opacity="{opacity}">{c}</text>')
    return "\n".join(out), adv * len(s)


def ring(s, cx, cy, r, size, start_deg=0.0, fill=INK, weight="500"):
    """Set a string around a circle, each glyph rotated tangentially."""
    out, n = [], len(s)
    for i, c in enumerate(s):
        th = start_deg + i * 360.0 / n
        rad = math.radians(th)
        x = cx + r * math.sin(rad)
        y = cy - r * math.cos(rad)
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
                   f'fill="{fill}" font-weight="{weight}" text-anchor="middle" '
                   f'dominant-baseline="central" '
                   f'transform="rotate({th:.2f},{x:.2f},{y:.2f})">{c}</text>')
    return "\n".join(out)


def sheet(n, title, blurb, body, height):
    head = [
        label(40, 58, f"STUDY {n:03d} &#183; {title}", 26, INK, "700", ls="0.22em"),
        label(40, 84, blurb, 12),
        f'<line x1="40" y1="104" x2="{SW-40}" y2="104" stroke="{RULE}"/>',
    ]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{SW}" height="{height}" viewBox="0 0 {SW} {height}">'
            f'<rect width="{SW}" height="{height}" fill="{BG}"/>'
            + "\n".join(head) + "\n".join(body) + '</svg>')


# ------------------------------------------------------------------ 1. wheel
def study_wheel(n):
    b = []
    b.append(label(40, 150, "Rotational symmetry of the MARK, not the letterforms. Repeat the word N times around", 13))
    b.append(label(40, 172, "the circle and the whole thing is N-fold symmetric — turned any way, a copy is upright.", 13))

    def wheel(cx, cy, r, copies, size, cap):
        g = []
        # one diamond separator per copy keeps the slot count an exact multiple
        seq = (WORD + "◆") * copies
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r+34}" fill="none" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r-30}" fill="none" stroke="{INK}" stroke-width="3"/>')
        g.append(ring(seq, cx, cy, r, size))
        # hub + spokes
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r-92}" fill="none" stroke="{RULE}" stroke-width="2"/>')
        for k in range(copies * 2):
            a = math.radians(k * 360.0 / (copies * 2) + 180.0 / (copies * 2))
            x1, y1 = cx + (r - 92) * math.sin(a), cy - (r - 92) * math.cos(a)
            x2, y2 = cx + (r - 34) * math.sin(a), cy - (r - 34) * math.cos(a)
            g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{RULE}" stroke-width="2"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r-150}" fill="{INK}"/>')
        g.append(f'<text x="{cx}" y="{cy}" font-family="{FONT}" font-size="{r*0.30:.0f}" fill="{BG}" '
                 f'font-weight="600" text-anchor="middle" dominant-baseline="central" '
                 f'letter-spacing="0.08em">MP</text>')
        g.append(label(cx, cy + r + 96, cap, 11, LABEL, anchor="middle"))
        return "\n".join(g)

    b.append(wheel(430, 500, 250, 2, 40, "TWO COPIES &#183; 180&#176; SYMMETRY &#183; ONE COPY ALWAYS WITHIN 90&#176; OF UPRIGHT"))
    b.append(wheel(1130, 500, 250, 3, 30, "THREE COPIES &#183; 120&#176; SYMMETRY &#183; TIGHTER, READS AS A ROUNDEL"))

    y = 900
    b.append(f'<line x1="40" y1="{y}" x2="{SW-40}" y2="{y}" stroke="{RULE}"/>')
    b.append(label(40, y + 28, "WHY IT WORKS", 11, INK, "700"))
    b.append(label(40, y + 52, "13 letters + 1 separator = 14 slots per copy. Two copies fill 28 slots, and slot j always "
                               "matches slot j+14 — so a half turn maps the mark onto itself exactly.", 12))
    b.append(label(40, y + 74, "Nothing is distorted: this is ordinary type on a circle. The wheel reading is free, and the "
                               "hub is available for a monogram, a year, or a rider number.", 12))
    return sheet(n, "WHEEL / RING", "Rotational symmetry by repetition — the whole mark turns, the letterforms stay honest.", b, y + 110)


# ------------------------------------------------------------------ 2. column
def study_column(n):
    b = []
    b.append(label(40, 150, "M, O, T and O are each symmetric about a vertical axis, and stacking preserves their order", 13))
    b.append(label(40, 172, "under reflection — so the column is a TRUE mirror ambigram, with zero stylisation.", 13))

    size, lh = 124, 120
    top = 320
    bot = top + 3*lh

    # fill=currentColor so the same <use> can be tinted without redrawing it
    d = ['<defs><g id="motocol">']
    for i, c in enumerate("MOTO"):
        d.append(f'<text x="0" y="{i*lh}" font-family="{FONT}" font-size="{size}" fill="currentColor" '
                 f'font-weight="600" text-anchor="middle">{c}</text>')
    d.append('</g></defs>')
    b.append("".join(d))

    def axis(cx):
        return (f'<line x1="{cx}" y1="{top-70}" x2="{cx}" y2="{bot+70}" stroke="{RULE}" '
                f'stroke-width="1.5" stroke-dasharray="6 7"/>')

    def cap(cx, s):
        return label(cx, bot + 108, s, 11, INK, "700", anchor="middle")

    # translate(X) puts the group's local x=0 at X; scale(-1,1) then reflects about X.
    for cx, note, tint in ((300, "AS DRAWN", None),
                           (780, "MIRRORED &#8212; SAME DATA, FLIPPED", "mirror"),
                           (1260, "SUPERIMPOSED &#8212; REGISTERS EXACTLY", "both")):
        b.append(axis(cx))
        if tint != "mirror":
            b.append(f'<g color="{INK}"><use xlink:href="#motocol" transform="translate({cx},{top})"/></g>')
        if tint in ("mirror", "both"):
            op = ' opacity="0.6"' if tint == "both" else ''
            col = GHOST if tint == "both" else INK
            b.append(f'<g color="{col}"{op}><use xlink:href="#motocol" '
                     f'transform="translate({cx},{top}) scale(-1,1)"/></g>')
        b.append(cap(cx, note))

    y = bot + 160
    b.append(f'<line x1="40" y1="{y}" x2="{SW-40}" y2="{y}" stroke="{RULE}"/>')
    b.append(label(40, y + 30, "SUGGESTED LOCKUP", 11, INK, "700"))
    b.append(label(40, y + 52, "PROPONENT breaks mirror symmetry (P, R, N and E all fail), so it plays support at small size "
                               "and sits centred on the same axis.", 12))

    s, lx, ly = 0.58, 780, y + 130
    b.append(axis(lx) if False else
             f'<line x1="{lx}" y1="{ly-50}" x2="{lx}" y2="{ly+3*lh*s+90}" stroke="{RULE}" '
             f'stroke-width="1.5" stroke-dasharray="6 7"/>')
    b.append(f'<g color="{INK}" transform="translate({lx},{ly}) scale({s})"><use xlink:href="#motocol"/></g>')
    adv = 34
    sub, _ = chars("PROPONENT", lx - adv*9/2, ly + 3*lh*s + 52, 28, adv, LABEL, "500")
    b.append(sub)
    b.append(label(lx, ly + 3*lh*s + 92, "READS THE SAME ON GLASS, IN A MIRROR, OR REVERSED", 11, LABEL, anchor="middle"))

    return sheet(n, "VERTICAL COLUMN", "MOTO stacked vertically is a flawless mirror ambigram — the one free win in the name.",
                 b, int(ly + 3*lh*s + 140))


# ------------------------------------------------------------------ 3. card
def study_card(n):
    b = []
    b.append(label(40, 150, "Print both orientations. Legibility is guaranteed by construction rather than by "
                            "letterform trickery — the deck-of-cards solution.", 13))

    size, adv = 54, 44
    w = adv * len(WORD)
    defs = ['<defs><g id="cardblock">']
    up, _ = chars(WORD, 0, 0, size, adv, INK, "600")
    defs.append(up)
    defs.append(f'<line x1="-30" y1="26" x2="{w+30}" y2="26" stroke="{INK}" stroke-width="3"/>')
    dn, _ = chars(WORD, 0, 0, size, adv, INK, "600")
    defs.append(f'<g transform="translate({w},{52}) rotate(180)">{dn}</g>')
    defs.append('</g></defs>')
    b.append("".join(defs))

    cx = (SW - w) / 2
    b.append(f'<rect x="{cx-70}" y="230" width="{w+140}" height="260" fill="none" stroke="{RULE}" stroke-width="2" rx="14"/>')
    b.append(f'<g transform="translate({cx},334)"><use xlink:href="#cardblock"/></g>')
    b.append(label(SW/2, 540, "AS DRAWN", 11, INK, "700", anchor="middle"))

    b.append(f'<rect x="{cx-70}" y="610" width="{w+140}" height="260" fill="none" stroke="{RULE}" stroke-width="2" rx="14"/>')
    b.append(f'<g transform="translate({cx+w},{714+52}) rotate(180)"><use xlink:href="#cardblock"/></g>')
    b.append(label(SW/2, 920, "THE WHOLE BLOCK ROTATED 180&#176; &#8212; INDISTINGUISHABLE", 11, INK, "700", anchor="middle"))

    y = 970
    b.append(f'<line x1="40" y1="{y}" x2="{SW-40}" y2="{y}" stroke="{RULE}"/>')
    b.append(label(40, y + 28, "NOTES", 11, INK, "700"))
    b.append(label(40, y + 52, "The centre rule is the hinge — it reads as a design element upright and does the same job inverted.", 12))
    b.append(label(40, y + 74, "Best on objects that get handed across a counter or sit between two people: cards, patches, "
                               "tank-top graphics, service-counter signage.", 12))
    return sheet(n, "PLAYING-CARD LOCKUP", "The word plus its own 180° twin, hinged on a centre rule.", b, y + 110)


# ------------------------------------------------------------------ 4. hidden
def study_hidden(n):
    b = []
    b.append(label(40, 150, "Not a direction trick — a reading trick. Four brand-positive words already sit inside the "
                            "name, in order, needing nothing but a change of weight or colour.", 13))

    size, adv = 86, 72
    w = adv * len(WORD)
    x0 = (SW - w) / 2
    base_y = 330

    found = [("MOTO", 0, 3), ("TOP", 2, 4), ("PRO", 4, 6), ("OPO", 6, 8),
             ("PROP", 4, 7), ("ONE", 8, 10), ("PROPONENT", 4, 12)]
    trio = [(0, 3), (4, 6), (8, 10)]

    faint, _ = chars(WORD, x0, base_y, size, adv, FAINT, "500")
    b.append(faint)
    for k, (a, z) in enumerate(trio):
        col = GHOST if k == 1 else INK          # MOTO / PRO / ONE — PRO tinted so the
        seg, _ = chars(WORD[a:z+1], x0 + adv*a, base_y, size, adv, col, "700")
        b.append(seg)                           # first two don't read as one run
    b.append(label(SW/2, base_y + 60, "MOTO &#183; PRO &#183; ONE &#8212; THE THREE THAT DO NOT OVERLAP", 11, INK, "700", anchor="middle"))

    # bracket diagram
    by = base_y + 130
    for i, (wd, a, z) in enumerate(found):
        yy = by + i * 40
        xa, xz = x0 + adv*a + 6, x0 + adv*(z+1) - 6
        col = INK if (a, z) in trio else LABEL
        b.append(f'<line x1="{xa:.1f}" y1="{yy}" x2="{xz:.1f}" y2="{yy}" stroke="{col}" stroke-width="3"/>')
        b.append(f'<line x1="{xa:.1f}" y1="{yy-6}" x2="{xa:.1f}" y2="{yy+6}" stroke="{col}" stroke-width="3"/>')
        b.append(f'<line x1="{xz:.1f}" y1="{yy-6}" x2="{xz:.1f}" y2="{yy+6}" stroke="{col}" stroke-width="3"/>')
        b.append(label(xz + 18, yy + 5, wd, 13, col, "700" if col == INK else "400"))
        note = {"OPO": "palindrome, and the rotational centre of the word",
                "PROPONENT": "the name splits exactly MOTO + PROPONENT"}.get(wd, "")
        if note:
            b.append(label(xa - 18, yy + 5, note, 11, LABEL, anchor="end"))

    y = by + len(found) * 40 + 40
    b.append(f'<line x1="40" y1="{y}" x2="{SW-40}" y2="{y}" stroke="{RULE}"/>')
    b.append(label(40, y + 28, "HOW TO USE IT", 11, INK, "700"))
    b.append(label(40, y + 52, "Static: set MOTO / PRO / ONE at full weight and the connective letters lighter — the second "
                               "reading surfaces without a second mark.", 12))
    b.append(label(40, y + 74, "Motion: reveal them in sequence. The name literally spells out the positioning.", 12))
    b.append(label(40, y + 96, "Careful: TOP, PROP and PRO overlap one another, so only one of that cluster can be lit at a time.", 12))
    return sheet(n, "HIDDEN WORDS", "MOTO · PRO · ONE — already in the name, in order, without overlap.", b, y + 130)


# ------------------------------------------------------------------ output
BUILDERS = {"wheel": study_wheel, "column": study_column,
            "card": study_card, "hidden": study_hidden}


def next_index():
    ns = [int(m.group(1)) for f in os.listdir(HERE)
          if (m := re.fullmatch(re.escape(STEM) + r"(\d+)\.svg", f))]
    return max(ns) + 1 if ns else 0


def main():
    args = sys.argv[1:]
    forced = next((int(a) for a in args if a.isdigit()), None)
    names = [a for a in args if a in BUILDERS] or list(BUILDERS)

    n = forced if forced is not None else next_index()
    for name in names:
        svg = BUILDERS[name](n)
        out = os.path.join(HERE, f"{STEM}{n:03d}.svg")
        with open(out, "w") as f:
            f.write(svg)
        print(f"wrote {os.path.basename(out)}  ({name})")
        n += 1


if __name__ == "__main__":
    main()
