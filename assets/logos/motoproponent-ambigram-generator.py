# -*- coding: utf-8 -*-
"""
MOTOPROPONENT — 180 degree rotational ambigram construction sheet.
Every 'rotated' view is the IDENTICAL path data with transform=rotate(180),
so nothing on the sheet can cheat.
"""

import os
import re
import sys

H_TOP, H_BOT = 6, 134          # cap height band
CY = 70                        # vertical rotation centre

INK   = "#14110E"
GHOST = "#C8452F"
LABEL = "#8E8880"
RULE  = "#D8D3CB"
BG    = "#FAF8F5"

# ---------------------------------------------------------------- glyphs
# each glyph: (width, [(d, stroke-width, colour), ...])
# glyph box is 0..w  x  0..140 ; rotation centre (w/2, 70)

G = {}

# ---- O / N  (self-rotational: same glyph reads O or N) -----------------
w = 112
G["ON"] = (w, [
    # squircle O: straight sides give the N its stems
    ("M52,6 H60 A40,40 0 0 1 100,46 V94 A40,40 0 0 1 60,134 H52 "
     "A40,40 0 0 1 12,94 V46 A40,40 0 0 1 52,6 Z", 20, INK),
    # diagonal: decorative in the O reading, structural in the N reading
    ("M18,42 L94,98", 20, INK),
])

# ---- T / E -------------------------------------------------------------
w = 104
G["TE"] = (w, [
    ("M0,16 H104", 20, INK),      # T crossbar  <->  E bottom arm
    ("M52,16 V124", 20, INK),     # T stem      <->  E spine (self-mapping)
    ("M20,70 H52", 14, GHOST),    # spur        <->  E middle arm
    ("M20,124 H52", 14, GHOST),   # spur        <->  E top arm
])

# ---- P / O -------------------------------------------------------------
w = 118
G["PO"] = (w, [
    ("M18,6 V134", 20, GHOST),    # P stem -> becomes a ligature stroke into the N
    ("M18,16 C72,16 106,30 106,56 C106,84 72,100 18,100", 20, INK),  # bowl = P upright, o rotated
])

# ---- R / P -------------------------------------------------------------
w = 124
G["RP"] = (w, [
    ("M18,6 V134", 20, INK),      # R stem
    ("M18,16 C72,16 102,30 102,54 C102,78 72,94 18,94", 20, INK),   # bowl
    ("M60,94 L102,134", 20, INK), # R leg
    ("M104,6 V134", 16, GHOST),   # ghost post -> becomes the P's stem after rotation
])

# ---- M / T -------------------------------------------------------------
w = 140
G["MT"] = (w, [
    ("M0,124 H140", 22, INK),     # base rule  <->  T crossbar
    ("M70,16 V124", 24, INK),     # M centre spine <-> T stem (self-mapping)
    ("M20,16 L70,124", 17, INK),
    ("M120,16 L70,124", 17, INK),
    ("M20,16 V124", 11, GHOST),
    ("M120,16 V124", 11, GHOST),
])

# ---------------------------------------------------------------- word
# position : (glyph key, rotated?)
WORD = [
    ("MT", 0), ("ON", 0), ("TE", 0), ("ON", 0), ("PO", 0), ("RP", 0),
    ("ON", 0),
    ("RP", 1), ("PO", 1), ("ON", 1), ("TE", 1), ("ON", 1), ("MT", 1),
]
LETTERS = list("MOTOPROPONENT")
TRACK = 10

def defs():
    out = ['<defs>']
    for k, (w, strokes) in G.items():
        out.append(f'<g id="g{k}">')
        for d, sw, col in strokes:
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" '
                       f'stroke-linecap="butt" stroke-linejoin="round"/>')
        out.append('</g>')
    out.append('</defs>')
    return "\n".join(out)

def place(key, rot, x):
    w = G[key][0]
    t = f'translate({x},0)'
    if rot:
        t += f' rotate(180,{w/2},70)'
    return f'<use xlink:href="#g{key}" transform="{t}"/>', w

def lockup():
    parts, x = [], 0
    for key, rot in WORD:
        s, w = place(key, rot, x)
        parts.append(s)
        x += w + TRACK
    return "\n".join(parts), x - TRACK

body = []
SW = 1560

def txt(x, y, s, size=13, col=LABEL, anchor="start", weight="400", ls="0.14em"):
    return (f'<text x="{x}" y="{y}" font-family="Helvetica Neue,Helvetica,Arial,sans-serif" '
            f'font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" '
            f'letter-spacing="{ls}">{s}</text>')

# ---- header
body.append(txt(40, 58, "MOTOPROPONENT", 30, INK, weight="700", ls="0.28em"))
body.append(txt(40, 84, "180° ROTATIONAL AMBIGRAM — CONSTRUCTION SHEET / GEOMETRIC SANS", 12))
body.append(txt(40, 104, "13 letters · centre letter O is rotationally symmetric · only 5 unique glyphs to draw", 12))

# ---- pair cards
pairs = [("MT","M","T","hard — base rule becomes the crossbar, spine becomes the stem"),
         ("ON","O","N","easy — one self-rotational glyph, used 5×"),
         ("TE","T","E","good — spurs point left as T, right as E"),
         ("PO","P","O","fair — bowl reads P; rotated it reads as a lowercase o"),
         ("RP","R","P","hardest — same handedness; ghost post carries the P stem")]

CARD_W, CARD_H = 500, 300
ox, oy = 40, 150
for i,(key,a,b,note) in enumerate(pairs):
    cx = ox + (i % 3) * CARD_W
    cy = oy + (i // 3) * CARD_H
    w = G[key][0]
    body.append(f'<rect x="{cx}" y="{cy}" width="{CARD_W-30}" height="{CARD_H-30}" fill="none" stroke="{RULE}"/>')
    body.append(txt(cx+18, cy+30, f"{a} &#8596; {b}", 15, INK, weight="700"))
    body.append(txt(cx+18, cy+50, note, 11))
    s = 1.05
    gx = cx + 40
    gy = cy + 70
    body.append(f'<g transform="translate({gx},{gy}) scale({s})"><use xlink:href="#g{key}"/></g>')
    body.append(txt(gx + w*s/2, gy + 140*s + 26, f"reads {a}", 11, INK, anchor="middle"))
    gx2 = cx + 40 + w*s + 110
    body.append(f'<g transform="translate({gx2},{gy}) scale({s})">'
                f'<use xlink:href="#g{key}" transform="rotate(180,{w/2},70)"/></g>')
    body.append(txt(gx2 + w*s/2, gy + 140*s + 26, f"reads {b}", 11, INK, anchor="middle"))
    body.append(f'<text x="{gx + w*s + 55}" y="{gy+82}" font-family="Helvetica,Arial" font-size="22" '
                f'fill="{LABEL}" text-anchor="middle">&#8635;</text>')

# ---- lockups
lk, lw = lockup()
scale = 1480.0 / lw
y1 = oy + 2*CARD_H + 40
body.append(txt(40, y1, "THE LOCKUP", 12, INK, weight="700"))
body.append(f'<g transform="translate(40,{y1+30}) scale({scale})">{lk}</g>')
body.append(txt(40, y1 + 30 + 140*scale + 32, "read upright", 11))

y2 = y1 + 30 + 140*scale + 80
body.append(txt(40, y2, "THE SAME ARTWORK, ROTATED 180°", 12, INK, weight="700"))
body.append(f'<g transform="translate(40,{y2+30}) scale({scale}) rotate(180,{lw/2},70)">{lk}</g>')
body.append(txt(40, y2 + 30 + 140*scale + 32, "read upside-down — identical path data, nothing redrawn", 11))

# ---- legend
y3 = y2 + 30 + 140*scale + 70
body.append(f'<line x1="40" y1="{y3}" x2="{SW-40}" y2="{y3}" stroke="{RULE}"/>')
body.append(f'<line x1="40" y1="{y3+24}" x2="80" y2="{y3+24}" stroke="{INK}" stroke-width="12"/>')
body.append(txt(92, y3+29, "LOAD-BEARING — reads as a real stroke in both orientations", 11))
body.append(f'<line x1="640" y1="{y3+24}" x2="680" y2="{y3+24}" stroke="{GHOST}" stroke-width="12"/>')
body.append(txt(692, y3+29, "COMPROMISED — decorative one way, structural the other; tune weight by eye", 11))

SH = int(y3 + 70)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{SW}" height="{SH}" '
       f'viewBox="0 0 {SW} {SH}">'
       f'<rect width="{SW}" height="{SH}" fill="{BG}"/>'
       + defs() + "\n".join(body) + '</svg>')

# ---------------------------------------------------------------- output
# Each run drops a new numbered study alongside the previous ones, so the
# evolution of the mark stays visible in the folder (and in the git history).
#   python3 motoproponent-ambigram-generator.py            -> next free number
#   python3 motoproponent-ambigram-generator.py --replace  -> overwrite the latest
#   python3 motoproponent-ambigram-generator.py 7          -> force study-007

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
print(f"wrote {os.path.basename(OUT)}  ({SW}×{SH}, lockup width {lw})")
