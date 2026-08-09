# MOTOPROPONENT — 180° Rotational Ambigram

Design notes, construction logic, and build instructions for the MOTOPROPONENT
ambigram lockup.

**TL;DR** — MOTOPROPONENT is an unusually good ambigram candidate: it has an odd
letter count with a rotationally symmetric letter (`O`) sitting exactly in the
middle, and its letter pairs collapse down to **five unique glyphs** for thirteen
letters. Three of those five are clean. Two (`M/T` and `R/P`) are compromises,
and one of them (`R/P`) is provably not solvable by naive means — see
[The handedness problem](#the-handedness-problem).

---

## 1. What kind of ambigram this is

An **ambigram** is a piece of lettering that stays readable under some
transformation. The main families:

| Type | Transformation | Notes |
| --- | --- | --- |
| **Rotational (180°)** | Turn the artwork upside-down | The classic. What we're building. |
| Mirror | Reflect across a vertical axis | Needs letters that survive reflection; `N E P R` all fight you here. |
| Lake / reflection | Reflect across a horizontal axis | Usually rendered with a "water" gutter. |
| Chain / tessellation | Repeats infinitely | Different problem entirely. |
| Figure-ground | Reads in the negative space | Not applicable to a 13-letter word. |

We chose **180° rotational** because the word's structure hands it to you (see
next section). A mirror ambigram of the same word would be substantially harder:
mirroring flips `N → И`, `E → Ǝ`, `P → ꟼ`, `R → Я`, and unlike rotation there's no
"centre letter" trick to exploit.

---

## 2. Why this word works

### The pairing rule

In a 180° rotational ambigram, when you turn the artwork over, the **first**
letter lands where the **last** letter was. So for an `n`-letter word, letter `i`
must be the 180° rotation of letter `n + 1 − i`.

MOTOPROPONENT is 13 letters:

```
position:   1  2  3  4  5  6  7  8  9 10 11 12 13
letter:     M  O  T  O  P  R  O  P  O  N  E  N  T
            └──────────────────┐│┌──────────────────┘
                          pairs across the centre
```

Which gives:

| Positions | Pair | Difficulty |
| --- | --- | --- |
| 1 ↔ 13 | **M / T** | Hard |
| 2 ↔ 12 | **O / N** | Easy |
| 3 ↔ 11 | **T / E** | Moderate |
| 4 ↔ 10 | **O / N** | *(same glyph as 2↔12)* |
| 5 ↔ 9 | **P / O** | Moderate |
| 6 ↔ 8 | **R / P** | Hardest |
| 7 | **O** (its own partner) | Free |

### Two pieces of luck

1. **Odd letter count.** Position 7 has no partner — it must rotate onto
   *itself*. That's fatal for most letters, but position 7 is **O**, which is
   already rotationally symmetric. Free win. (Had the centre letter been, say,
   `R`, the whole approach would need rethinking.)

2. **Massive glyph reuse.** `O/N` appears twice, and the centre `O` can reuse the
   same glyph a third time (in two orientations, so five instances total). Net
   result: **13 letters, 5 drawings.**

   ```
   G_MT   used at positions  1, 13
   G_ON   used at positions  2,  4,  7, 10, 12
   G_TE   used at positions  3, 11
   G_PO   used at positions  5,  9
   G_RP   used at positions  6,  8
   ```

---

## 3. The method

### Skeleton-first, not outline-first

The glyphs are built as **centreline strokes** (SVG `<path>` with `stroke-width`),
not as filled outlines. Reasons:

- A clean geometric sans is, structurally, uniform-weight strokes made of straight
  lines and circular arcs. Skeletons model that directly.
- Ambigram work is iterative — you nudge a vertex, check the rotation, nudge
  again. Editing two numbers in a `d` attribute is much faster than pushing
  bezier handles on an outlined form.
- Stroke weight becomes a *tunable*, which turns out to be the main lever for
  making the compromised pairs read (see §5).

When the geometry is settled, outline the strokes in Illustrator
(`Object → Path → Outline Stroke`) and take over by hand from there.

### The rotation maths

Every glyph lives in a box `0..w` wide by `0..140` tall, with cap height running
`y = 6` (top) to `y = 134` (baseline). Rotation happens about the box centre
`(w/2, 70)`:

```
(x, y)  →  (w − x, 140 − y)
```

Four consequences drive every decision in this project:

1. **Horizontals swap top for bottom.** A bar at the cap line becomes a bar at the
   baseline. *This is what makes `M/T` possible* — the rule under the M becomes
   the crossbar over the T.
2. **Verticals swap left for right,** *unless* they sit at `x = w/2`, in which case
   they map onto themselves. A centred stem is therefore the most valuable stroke
   in an ambigram: it costs you nothing in either orientation. Both `M/T` and
   `T/E` are built around one.
3. **Handedness flips.** Anything on the left ends up on the right. This is the
   whole reason `R/P` is hard.
4. **Diagonals stay diagonal at the same angle** but swap quadrants, so a `\`
   stays a `\`. This is why the `O/N` diagonal maps onto itself perfectly.

### Proving it, rather than eyeballing it

The bottom two rows of the construction sheet are the honesty check. The upright
lockup is a group of `<use>` references. The "rotated" lockup is **the identical
group** with `rotate(180)` applied:

```xml
<g transform="translate(40,Y) scale(S) rotate(180, LW/2, 70)"> …same content… </g>
```

Nothing is redrawn, re-kerned, or quietly fixed up. If the artwork reads upside
down on that sheet, it will read upside down on a t-shirt.

This also constrains the layout: for the lockup as a whole to be rotationally
symmetric, the glyph widths must be palindromic (`w₁ = w₁₃`, `w₂ = w₁₂`, …) and
the tracking must be uniform (or itself palindromic). Both hold here because
positions `i` and `14 − i` literally share a glyph definition.

---

## 4. Glyph-by-glyph rationale

### `G_ON` — O ↔ N *(easy, and it does the most work)*

A **squircle** — a rounded rectangle with a 40-unit corner radius — plus a single
diagonal from upper-left to lower-right.

- **Read as O:** the closed squircle is the letter; the diagonal reads as a slash
  detail (think a slashed zero, or `Ø`).
- **Read as N:** the squircle's straight left and right sides become the N's two
  stems; the diagonal becomes the N's diagonal; the top and bottom curves read as
  connecting flourishes.

The diagonal runs `(18,42) → (94,98)`, whose two endpoints are each other's
rotation about `(56,70)` — so the diagonal maps exactly onto itself. Combined with
the symmetric squircle, **the entire glyph is self-rotational**, which is why one
drawing serves all five `O`/`N` positions.

*Refinement note:* it currently leans `Ø`. Narrowing the box and lengthening the
straight sides pushes the reading toward `N` without hurting the `O`.

### `G_TE` — T ↔ E *(the neatest solve)*

Four strokes:

| Stroke | Reads as T | Reads as E |
| --- | --- | --- |
| Full-width bar at cap line | crossbar | bottom arm *(after rotation)* |
| Centred stem, cap to baseline | stem | spine *(maps onto itself)* |
| Short spur at mid-height | decorative | middle arm |
| Short spur at baseline | decorative | top arm *(after rotation)* |

The trick: **the spurs point left in the T reading and right in the E reading.**
Arms on the left of a spine don't say "E" to anyone, so upright the eye discards
them as ornament and reads the dominant T. Rotate, and they land on the correct
side and switch from noise to structure.

The centred stem doing double duty as spine *and* stem is the free lunch from
rotation rule #2 above.

### `G_PO` — P ↔ O *(fair)*

A full-height stem plus a bowl closing at `y = 100`.

- **Upright:** stem + bowl in the upper two-thirds = `P`.
- **Rotated:** the bowl becomes a closed round counter sitting on the baseline —
  reading as a **lowercase `o`** — with the ex-stem now rising on its right.

Mixed case is entirely legitimate in ambigrams, so the small `o` is a feature, not
a bug. The leftover stem is the honest compromise: it's marked as a ghost stroke
and is intended to be **kerned into the neighbouring `N`'s left stem** so it reads
as a ligature rather than a stray.

Because kerning must stay palindromic, tightening the gap between positions 9–10
(`O N`) automatically tightens 4–5 (`O P`) by the same amount — which is exactly
where you want it. Free.

### `G_MT` — M ↔ T *(hard, but landed)*

This one only works because of rotation rule #1.

| Stroke | Reads as M | Reads as T |
| --- | --- | --- |
| Full-width rule at the baseline | a base rule / underline | **the crossbar** |
| Heavy centred spine | the M's middle | **the stem** (maps onto itself) |
| Two diagonals, top corners → bottom centre | the M's V | an A-frame ghost |
| Two thin outer verticals | the M's shoulders | ghost brackets |

The base rule is the key move. `M` has no horizontal anywhere, and `T` is 50%
horizontal — so the horizontal has to be smuggled in as a design element (an
underline under the word's opening) that the rotation promotes into the T's
crossbar. Because the rule sits at the baseline it reads as deliberate styling
upright, and as pure letterform rotated.

The residue is the M's V and shoulders, which hang under the rotated crossbar as a
faint A-frame. They're drawn lighter so the T's silhouette dominates. **Weight
contrast is the load-bearing device here** — this pair will not read at uniform
stroke weight.

*Refinement note:* consider extending the rule across the first six letters as a
continuous underline. Under rotation it becomes a continuous overline across the
last six, which reads as intentional in both orientations and lets the M's
shoulders curl into it instead of dangling.

### `G_RP` — R ↔ P *(the unsolved one)*

Stem + bowl + diagonal leg for the `R`, plus a ghost post on the right that
becomes the `P`'s stem after rotation. Upright it reads `R` cleanly. Rotated it
reads as a mirrored `R` — which is to say, it doesn't read as `P` on its own
merits yet.

Why, and what to do about it, is its own section.

---

## 5. The handedness problem

`R` and `P` have the **same handedness**: stem on the left, bowl on the upper
right. Rotation rule #3 says a 180° turn flips left and right. So:

> A left-stemmed letter always rotates into a right-stemmed shape. Therefore no
> single-bowl glyph can rotate from `R` into `P` while keeping both bowls in the
> upper half and both stems on the left.

This isn't a lack of skill — it's geometry. Every attempt runs into the same wall:
give the P its left stem and the bowl lands in the bottom half; put the bowl in
the top half and the stem lands on the right.

Three real escapes, in rough order of how well they tend to work:

1. **Let context carry it.** Draw one glyph that reads `R` strongly and `P`
   acceptably, and rely on the reader. Both slots have overwhelming context:
   `MOTOP?OPONENT` and `MOTOPRO?ONENT` admit essentially one answer each. This is
   how most published ambigrams handle same-handed pairs, and it's the
   recommended path here.
2. **Equalise the handedness.** Redraw the `R` with a straight *vertical* leg
   instead of a diagonal one, giving the glyph a full-height post on both left and
   right. The two posts then swap roles under rotation, and letter identity is
   carried by the bowl and by weight contrast rather than by silhouette. Costs you
   a slightly techno-looking `R`.
3. **Restructure the pairing.** Break the strict one-glyph-per-letter mapping and
   let a block of letters rotate into a *different-length* block (e.g. `M ↔ NT`).
   This buys new pairings but requires reworking the whole lockup, and the
   alternatives explored (`O/E`, `T/N`, `P/P`) were not obviously easier.

---

## 6. Reading the construction sheet

| | Meaning |
| --- | --- |
| **Black strokes** | Load-bearing — the stroke does real letterform work in *both* orientations. |
| **Red strokes** | Compromised — decorative in one orientation, structural in the other. These are the strokes to tune by eye, and the ones to lighten, curl, or kern away. |

The `O/N` glyph is entirely black. `T/E` is mostly black. `M/T` and `R/P` carry
the most red — which is a fair visual summary of where the remaining work is.

---

## 7. Files

```
assets/logos/
├── README.md                                 ← this document
├── motoproponent-ambigram-generator.py       ← generates the sheet from glyph definitions
└── motoproponent-ambigram-study-000.svg      ← study 000; each pass adds the next number
```

### Dependencies

None. Plain Python 3, standard library only. Output is SVG — vector all the way
down, no raster export step.

### Regenerating

Every run writes a **new numbered study** rather than overwriting the last one, so
the folder (and the git history) shows the mark evolving:

```bash
python3 motoproponent-ambigram-generator.py             # -> next free number
python3 motoproponent-ambigram-generator.py --replace   # -> overwrite the latest study
python3 motoproponent-ambigram-generator.py 7           # -> force study-007
```

Files land next to the script as `motoproponent-ambigram-study-NNN.svg`. The
numbering is derived by scanning the folder for existing studies and taking the
highest + 1, so it survives deletions and manual renames. Use `--replace` while
you're iterating on a single idea, and let it increment when a pass is worth
keeping.

### Editing the letterforms

All geometry lives in the `G` dictionary near the top of the generator:

```python
G["ON"] = (112, [                       # (advance width, [strokes])
    ("M52,6 H60 A40,40 0 0 1 …", 20, INK),   # (path data, stroke width, colour)
    ("M18,42 L94,98",            20, INK),
])
```

Change a coordinate, re-run, and the rotated views on the sheet update
automatically and *honestly* — they're references to the same paths, so you can't
accidentally flatter yourself.

**The one invariant to preserve:** every glyph's rotation partner is generated
from the same definition, so a change to a glyph changes *both* letters it
represents. Adjusting the `O` necessarily adjusts the `N`. That coupling is the
whole discipline of ambigram design; the tool just makes it impossible to forget.

---

## 8. Suggested next steps

1. Narrow `G_ON` so it leans less `Ø` and more `O`/`N`.
2. Run the `M/T` base rule out into a continuous underline across the first half
   of the word (it becomes an overline across the second half).
3. Pick an escape route for `R/P` — recommendation is option 1, context.
4. Tighten kerning at positions 4–5 and 9–10 so the `P` stem ligatures into its
   neighbour.
5. Outline the strokes and take it into Illustrator for optical correction —
   overshoot on the round forms, thin the diagonal joins, and balance the
   apparent weight of the diagonals against the stems.
6. Test at small size and at low contrast. An ambigram that only works at 400px
   isn't finished.
