# MOTOPROPONENT — 180° Rotational Ambigram

Design notes, construction logic, and build instructions for the MOTOPROPONENT ambigram lockup.

**TL;DR** — MOTOPROPONENT looks like an unusually good ambigram candidate: odd letter count, a rotationally symmetric `O` sitting exactly in the middle, heavy letter reuse. It is not. Three of its six letter pairs are structurally obstructed rather than merely hard, and the obstructions are proved below rather than asserted. What that buys you is a known ceiling: the strict one-ink mark will always be a "you have to be told what it says" wordmark. See [Where it breaks](#4-where-it-breaks).

There are therefore **two marks in this folder**, built by two generators. The **flat ambigram** is one artwork read two ways, and it lives with that ceiling. The **duotone lockup** spends colour instead of legibility: it overlays the word with its own rotation in a second ink, so every letter in both readings is drawn correctly and nothing is carried by context. See [The duotone route](#10-the-duotone-route).

## 1. What kind of ambigram this is

An **ambigram** is a piece of lettering that stays readable under some transformation. The main families:

| Type | Transformation | Notes |
| --- | --- | --- |
| **Rotational (180°)** | Turn the artwork upside-down | The classic. What we're building. |
| Mirror | Reflect across a vertical axis | Needs letters that survive reflection; `N E P R` all fight you here. |
| Lake / reflection | Reflect across a horizontal axis | Usually rendered with a "water" gutter. |
| Chain / tessellation | Repeats infinitely | Different problem entirely. |
| Figure-ground | Reads in the negative space | Not applicable to a 13-letter word. |

We chose **180° rotational** because the word's structure appears to hand it to you. A mirror ambigram of the same word would be substantially harder: mirroring flips `N → И`, `E → Ǝ`, `P → ꟼ`, `R → Я`, and unlike rotation there's no centre-letter trick to exploit.

## 2. The pairing rule

In a 180° rotational ambigram, turning the artwork over lands the **first** letter where the **last** letter was. So for an `n`-letter word, letter `i` must be the 180° rotation of letter `n + 1 − i`.

```text
position:   1  2  3  4  5  6  7  8  9 10 11 12 13
letter:     M  O  T  O  P  R  O  P  O  N  E  N  T
            └──────────────────┐│┌──────────────────┘
                          pairs across the centre
```

Which gives six pairs plus a free centre:

| Positions | Pair | Status |
| --- | --- | --- |
| 1 ↔ 13 | **M / T** | Obstructed – see §4 |
| 2 ↔ 12 | **O / N** | Obstructed – see §4 |
| 3 ↔ 11 | **T / E** | Solved |
| 4 ↔ 10 | **O / N** | *(same problem as 2 ↔ 12)* |
| 5 ↔ 9 | **P / O** | Solved, with a residue stroke |
| 6 ↔ 8 | **R / P** | Obstructed – see §4 |
| 7 | **O** (its own partner) | Free |

Position 7 has no partner, so it must rotate onto *itself*. That is fatal for most letters, but position 7 is `O`, which is already rotationally symmetric. It is the one piece of genuine luck in the word, and it is the pivot the whole mark turns on.

## 3. The method

### Author one half, generate the other

The artwork is authored **once**, for the left half of the word plus the pivot letter, in a single word-space coordinate system. The right half is never drawn. It is the authored half rotated 180° about the lockup centre:

```xml
<use xlink:href="#half"/>
<use xlink:href="#half" transform="rotate(180, CX, CY)"/>
```

The mark is therefore rotationally symmetric **by construction**. There is no second copy of anything to quietly fix up, and the "rotated" row on the study sheet is pixel-identical to the upright one, which is precisely what a 180° ambigram is.

This replaces the earlier approach (studies 000 and before) of drawing five self-contained glyphs and placing them on a palindromic width grid. What the change buys:

- **No palindromic width grid.** Advances and tracking are declared once in a table; the mirror side inherits them automatically. Widths are free.
- **No self-contained glyphs.** A stroke may begin inside one letter and end inside the next, so ligatures and connective strokes cost nothing.
- **Symmetry cannot drift.** Previously the two halves were separate artwork that happened to agree. Now disagreement is not representable.

### Skeleton-first, not outline-first

Glyphs are **centreline strokes** (SVG `<path>` with `stroke-width`), not filled outlines. A clean geometric sans is structurally uniform-weight strokes made of straight lines and arcs, so skeletons model it directly, and editing two numbers in a `d` attribute beats pushing bezier handles when you are iterating. When the geometry settles, outline the strokes in Illustrator (`Object → Path → Outline Stroke`) and take over by hand.

### The rotation maths

Everything lives on a 140-unit metric with cap height running `y = 6` (cap line) to `y = 134` (baseline). Rotation happens about the lockup centre `(LW/2, 70)`:

```text
(x, y)  →  (LW − x, 140 − y)
```

Four consequences drive every decision in this project:

1. **Horizontals swap top for bottom.** A bar at the cap line becomes a bar at the baseline. This is what the rule motif exploits.
2. **Verticals swap left for right,** *unless* they sit on the centre line, in which case they map onto themselves.
3. **Handedness flips.** Anything on the left ends up on the right. This is why `R/P` is obstructed.
4. **Diagonals keep their angle** but swap quadrants, so a `\` stays a `\`.

### What weight can and cannot do

**Weight is orientation-invariant.** A heavy stroke is heavy in both readings. You therefore *cannot* use weight to make a stroke dominate upright and recede when rotated — it only sorts strokes into primary, secondary and rule globally.

This corrects the earlier design note claiming the `M`'s residue was "drawn lighter so the `T`'s silhouette dominates". Those strokes are also the `M`'s defining strokes, so lightening them for the `T`'s benefit is exactly why the `M` stopped reading. The levers that genuinely differ between orientations are position relative to the cap and base lines, immediate context, and whether a stroke connects into its neighbour.

<!--| PAGE-BREAK -->

## 4. Where it breaks

Three of the six pairs are obstructed by the geometry of rotation, not by lack of skill. Knowing *why* is what stops you burning passes on them.

### `M / T` — full-height edge stems

An `M` requires two full-height stems at its outer edges; without them `\/\/` is a `W` and `\/` is a `V`. A full-height vertical at `x` rotates to a full-height vertical at `LW − x`, so the `T` reading inherits two full-height verticals flanking its stem. A `T` is defined by having nothing beside its stem. The conflict is unavoidable at 1:1.

### `O / N` — closure is rotation-invariant

Reading `O` requires a closed counter. Rotation maps closed loops to closed loops, so whatever closes the `O` is still closing it in the `N` reading. You cannot make the closure subordinate in one orientation only, because weight is orientation-invariant (above). Worse, `O` and `N` are *both* intrinsically 180°-symmetric, so there is no asymmetry to exploit either: the pair genuinely wants to be one picture read two ways.

This one is worth stating carefully, because the obvious diagnosis — "study 000 forced this glyph to be self-rotational and that was a self-imposed extra constraint" — is wrong. The constraint is essentially forced by the symmetry of both letters. Study 000's error was execution (a 40-unit corner radius left almost no straight side, so it read `Ø`), not architecture.

### `R / P` — same handedness

`R` and `P` both have the stem on the left and the bowl in the upper right. Rotation flips left for right *and* top for bottom. So:

> A left-stemmed, top-bowled letter always rotates into a right-stemmed, bottom-bowled shape. No single-bowl glyph can rotate from `R` into `P` while keeping both bowls in the upper half and both stems on the left.

Give the `P` its left stem and the bowl lands in the bottom half; put the bowl in the top half and the stem lands on the right.

### What we do about it

All three are handled the same way, which is how most published ambigrams handle same-handed pairs: **let context carry the weaker reading**. `MOTOP?OPONENT` and `MOTOPRO?ONENT` each admit essentially one answer. The residue strokes are then absorbed by the rule motif (§5) so they read as deliberate rather than as leftovers.

The one avenue not yet explored inside the strict ambigram is **letting the two readings divide the artwork differently**. The authored half spans seven letters upright (`MOTOPRO`) and six rotated (`PONENT`), so the rotated side has ~17% more width per letter and its letter boundaries need not fall where the upright ones do. Exploiting that means drawing a continuous stroke field rather than a row of letters, which is hand-drawing work rather than parametric work. It is the most promising remaining idea inside this constraint, and it is not cheap.

The cheaper escape is to stop insisting on one ink. See §10.

## 5. The rule motif

One authored stroke — a rule sitting on the baseline under the left half — becomes, under rotation, a rule sitting on the cap line over the right half. They overlap across the pivot `O`.

It does three jobs at once:

- gives the final `T` its crossbar
- gives the `E` its top arm
- establishes rules-and-verticals as a deliberate visual language, so the leftover posts from the obstructed pairs read as intentional structure rather than as residue

That third job is the important one. It is a systemic answer to the residue problem instead of fighting it glyph by glyph, and it is why the `R`'s right-hand post (which exists only to give the `P` a stem) does not look like a mistake.

## 6. Letter-by-letter state

| Letter | Upright | Rotated | Notes |
| --- | --- | --- | --- |
| `M` | Reads | Weak `T` | Edge stems become flanking verticals; the V's tail becomes the `T`'s stem, the rule its crossbar. |
| `O` | Reads | Weak `N` | Stadium at uniform weight, straight sides 62% of cap height, plus a diagonal. Leans `Ø`; that is the compromise. |
| `T` | Reads | Reads `E` | The best solve. Stem right of centre so the `E`'s bottom arm reaches further right than left; top arm is the rule; only the middle arm is smuggled in, as a short left tick. |
| `P` | Reads | Reads `o` | Bowl becomes a lowercase `o` on the baseline; the stem becomes a post to its right, kerned tight so it ligatures into `p10`'s stem. Mixed case is legitimate in ambigrams. |
| `R` | Reads | Weak `P` | Leg terminates on a full-height rule at the right edge; that rule gives the `P` its stem. The bowl still lands in the wrong half. |

Uniform stroke weight inside the bowls matters more than it sounds. Mixing weights left visible notches where light curves met heavy stems, which read as drawing errors at any size above about 100px.

## 7. The two-tier lockup

A 13-letter ambigram will never survive a favicon, and this one has a legibility ceiling even at full width. So the mark is two things:

- **Wordmark** — the full lockup, for hero and large-format use, where the reader has time and context.
- **Roundel** — a circle with the rule motif running tangent below it on the left and above it on the right, cropped square. Self-rotational, so it is its own ambigram, and it holds together at 32px. It is a crop of the wordmark's pivot, so the two are visibly of a piece.

The two rails overlap across the middle rather than butting end-to-end at the centre; butted, they read as one zigzag instead of two offset rules.

<!--| PAGE-BREAK -->

## 8. Reading the study sheet

| Row | What it shows |
| --- | --- |
| **The mark** | Monotone, as it would actually be used. This is the honest view — everything else is diagnostic. |
| **Rotated 180°** | Identical to the row above, pixel for pixel. That identity *is* the ambigram. |
| **Stroke roles** | Black = primary letterform, grey = secondary, red = rule motif. Letters are labelled above (upright reading) and below (rotated reading) each position. |
| **Size test** | The lockup at 820px, 430px and 240px. An ambigram that only works at full width is not finished. |
| **Small-size sibling** | The roundel at 168px down to 32px. |

## 9. Files

Two generators, two independent series of studies. They share no code and are not variants of each other — they are different marks.

```text
assets/logos/
├── README.md                                 ← this document
│
├── motoproponent-ambigram-generator.py       ← flat ambigram, one ink (§3–§7)
├── motoproponent-ambigram-study-000.svg      ← five-glyph architecture (superseded)
├── motoproponent-ambigram-study-001.svg      ← half + rotation architecture
├── motoproponent-ambigram-study-002.svg      ← uniform-weight bowls, computed layout
├── motoproponent-ambigram-study-003.svg      ← shorter T spur, legible roundel
│
├── motoproponent-duotone-generator.py        ← duotone lockup, two inks (§10)
├── motoproponent-duotone-study-000.svg       ← the device, three treatments
├── motoproponent-duotone-study-001.svg       ← tint + dark-ground treatments added
└── motoproponent-duotone-study-002.svg       ← widths rebalanced, tracking uniform
```

### Dependencies

None. Plain Python 3, standard library only. Output is SVG — vector all the way down, no raster export step.

### Regenerating

Both generators take the same arguments, and each numbers its own series independently. Every run writes a **new numbered study** rather than overwriting the last one, so the folder and the git history show the mark evolving:

```bash
python3 motoproponent-ambigram-generator.py             # -> next free number
python3 motoproponent-ambigram-generator.py --replace   # -> overwrite the latest study
python3 motoproponent-ambigram-generator.py 7           # -> force study-007

python3 motoproponent-duotone-generator.py              # same three forms
```

Numbering scans the folder for existing studies and takes the highest + 1, so it survives deletions and manual renames. Use `--replace` while iterating on one idea; let it increment when a pass is worth keeping.

### Reviewing a study

There is no raster step, so to actually look at a study at a given size, render it with headless Chrome:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars \
  --screenshot=study.png --window-size=1828,1593 \
  "file://$PWD/motoproponent-ambigram-study-003.svg"
```

Judging an ambigram from its path data does not work. Look at the picture.

### Editing the letterforms

Two places, and only two.

**Layout** lives in the `LEFT` table near the top of the generator. Widths and gaps are free; the lockup width and the mirror side are derived from them:

```python
LEFT = [               # (letter, width, gap after)
    ("M", 126, 40),
    ("O", 104, 30),
    ...
]
```

**Letterforms** live in one `draw_*` function each, taking the letter's left edge and width:

```python
def draw_O(x, w):
    l, r = x + 8, x + w - 8
    S(f"M{l},30 V110 C{l},142 {r},142 {r},110 V30 C{r},-2 {l},-2 {l},30 Z")
    S(f"M{l},30 L{r},110")
```

**The one invariant to preserve:** never author anything in the right half of the word. It does not exist as artwork. Everything from the lockup centre rightward is generated, so a change to a left-half letter necessarily changes the letter it rotates into. That coupling is the whole discipline of ambigram design; the tool makes it impossible to forget.

The duotone generator is laid out the same way — a `WIDTHS` table and one `L_*` function per letter — but with none of that coupling, since each letter is only ever itself. The only thing to preserve there is the width balance across the pivot described in §10; change a letter's width and re-check that the two halves still total the same, or the pivot drifts off the axis.

## 10. The duotone route

Every wall in §4 comes from one requirement: a single stroke has to serve both readings. Drop that and they all fall over at once.

### The construction

Draw the word properly, once, as `W`. The artwork is then two layers in two colours:

```text
layer A  =  W
layer B  =  rotate(W, 180°)
```

Upright you read layer A. Rotate the composite and layer A goes upside-down while layer B comes upright, so you read layer B. And since `rotate(A + B) = rotate(W) + W = B + A`, the composite is rotationally symmetric onto itself with the two hues swapping roles. The rotated row on the study sheet is the same geometry with the colours exchanged.

### What it buys

Every letter in both readings is a correct letterform. No compromised glyphs, no residue posts, no letters carried by context — `M`, `O`, `N`, `T`, `E`, `P` and `R` are simply drawn as themselves. The alphabet is seven letters and none of them fight.

Layout is also completely unconstrained, because the composite is symmetric for *any* `W`. Widths and tracking are free to be purely optical.

The one deliberate layout choice is that the letters before the pivot `O` total exactly the same width as the letters after it (624 units each), so uniform tracking puts the pivot on the rotation axis. Both layers then draw that `O` in the same place and it resolves to a single darker form — a useful anchor at the point the mark turns on. Only `M`, `R`, `N` and `E` were free to be adjusted to hit that total; every other letter appears on both sides of the pivot and has to keep one width. An earlier pass bought the same centring with looser tracking across `NENT`, and the uneven rhythm was obvious the moment you looked at a single reading on its own.

### What it costs

**Colour becomes load-bearing.** Flattened to one ink the two layers tangle into noise. So this cannot be the only lockup — it needs a monochrome fallback, which is what the flat ambigram or plain type is for.

It is also twice the ink, so it gives out at small sizes sooner than a normal wordmark. The size test puts the floor around 500–550px wide for the equal-value treatment.

### Treatments

How hard the second reading pushes is a dial:

| Treatment | Behaviour |
| --- | --- |
| Equal value, two hues | Neither reading wins; the eye chooses which hue to follow. Densest option. |
| Ink primary, accent secondary | Upright dominates, second reading is discoverable. |
| One hue, tint secondary | Same as above but needs no second brand colour — useful while the palette is unsettled. |
| Ink primary, hairline secondary | Second reading is a watermark. Cleanest read, least drama. |

Overlaps blend rather than one layer simply hiding the other: **multiply** on a light ground, **screen** on a dark one. Note that `mix-blend-mode` may not survive an Illustrator round-trip; reapply Multiply to the second layer there, or set it as a transparency-group blend on export.

<!--| PAGE-BREAK -->

## 11. Suggested next steps

1. Decide whether the legibility ceiling in §4 is acceptable. If it is not, the realistic alternatives are a different typographic vernacular (blackletter or vintage brush script — both far more forgiving vehicles, and both more idiomatic to motorcycle culture than a geometric sans) or a shorter ambigram with `MOTOPROPONENT` set as ordinary type.
2. Attempt the different-boundaries idea at the end of §4 on the `M/T` pair specifically, since the final `T` is the weakest reading in the mark.
3. Tighten kerning at positions 4–5 further so the `P`'s residue post fully ligatures into `p10`'s stem rather than sitting near it.
4. Relieve the congestion around positions 6–8, where the `R`'s post, the pivot `O` and the rotated `R`'s bowl currently crowd into one mass.
5. Outline the strokes and take it into Illustrator for optical correction — overshoot on the round forms, thin the diagonal joins, balance the apparent weight of diagonals against stems.
6. Test at low contrast and on a dark ground, not just at small size.
