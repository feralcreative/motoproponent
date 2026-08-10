# -*- coding: utf-8 -*-
"""
Build the client-facing presentation page for the ambigram work.

Everything visual on the page is lifted straight out of the construction
sheets rather than redrawn, so the page cannot drift from the studies.  Each
sheet already carries its artwork once in <defs>, as an authored half plus
the rotation that completes it; this pulls those groups out and re-emits the
same two <use> elements the sheet itself uses.

Two traps worth knowing about if you edit this:

1.  An <svg> does NOT scope element ids.  Every sheet names its groups the
    same things ("half-final", "line-straight"), so inlining several marks in
    one page collides - the first "half-final" in the document wins and every
    later mark silently renders the first one's artwork.  Hit exactly that:
    three different studies all drew the uppercase one.  Hence the ns prefix.

2.  Stroke colours are baked into the sheets as presentation attributes,
    which would leave black-on-black in dark mode.  Presentation attributes
    lose to any CSS rule, so the stylesheet restyles them by class - the ink
    strokes and the colour line are separate groups, which is what makes that
    possible.

Run it, then publish presentation.html as an Artifact.
"""

import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "presentation.html")

MARKS = {                       # name -> (sheet, glyph-box height)
    "caps": ("motoproponent-ambigram-study-004.svg", 140),
    "s000": ("motoproponent-lowercase-study-000.svg", 170),
    "s001": ("motoproponent-lowercase-study-001.svg", 170),
    "s002": ("motoproponent-lowercase-study-002.svg", 170),
    "s003": ("motoproponent-lowercase-study-003.svg", 170),
}
KEEP = ["half-final", "line-straight"]
ROLE = {"half-final": "ink", "line-straight": "accent"}


def strip_stroke(s):
    """Drop the baked-in stroke colours so the marks can follow the theme.

    Colour cannot be restyled where it sits. The artwork is rendered through
    <use>, which clones the <defs> content into a shadow tree, and a CSS rule
    written against the original elements does not reliably reach the clone -
    that is why an .on-shell override left the mark black on a black plate.

    stroke IS an inherited property, though, and the <use> elements are
    ordinary DOM. So: remove the attribute here, set the colour on the <use>,
    and let it inherit inward. stroke-width stays - it varies per path and is
    not a theming concern."""
    return re.sub(r'\s+stroke="#[0-9A-Fa-f]{3,8}"', "", s)


def groups(svg):
    """Every top-level <g id="..."> inside <defs>, by id."""
    defs = re.search(r"<defs>(.*)</defs>", svg, re.S).group(1)
    out, i = {}, 0
    while True:
        m = re.compile(r'<g id="([^"]+)">').search(defs, i)
        if not m:
            return out
        depth, j = 1, m.end()
        while depth:
            nxt = re.compile(r"<g\b|</g>").search(defs, j)
            depth += 1 if nxt.group(0) != "</g>" else -1
            j = nxt.end()
        out[m.group(1)] = defs[m.start():j]
        i = j


def mark(ns, src, gh, pad=26):
    svg = open(os.path.join(HERE, src)).read()
    g = groups(svg)
    cx, cy = (float(v) for v in
              re.search(r"rotate\(180,([\d.]+),([\d.]+)\)", svg).groups())
    defs = strip_stroke("".join(g[k] for k in KEEP if k in g))
    for k in KEEP:
        defs = defs.replace(f'<g id="{k}">', f'<g id="{ns}-{k}">')
    uses = "".join(
        f'<use class="{ROLE[k]}" href="#{ns}-{k}"/>'
        f'<use class="{ROLE[k]}" href="#{ns}-{k}" transform="rotate(180,{cx},{cy})"/>'
        for k in KEEP if k in g)
    return (f'<svg class="mk" xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="{-pad} {-pad} {2 * cx + 2 * pad} {gh + 2 * pad}" '
            f'role="img" aria-label="the motoproponent ambigram">'
            f'<defs>{defs}</defs>{uses}</svg>')


def roundel(ns):
    svg = open(os.path.join(HERE, "motoproponent-lowercase-study-003.svg")).read()
    g = groups(svg)
    d = strip_stroke(
        g["round-final"].replace('<g id="round-final">', f'<g id="{ns}-final">')
        + g["round-line"].replace('<g id="round-line">', f'<g id="{ns}-line">'))
    return ('<svg class="mk" xmlns="http://www.w3.org/2000/svg" '
            'viewBox="-30 4 178 156" role="img" '
            'aria-label="the motoproponent roundel">'
            f'<defs>{d}</defs>'
            f'<use class="ink" href="#{ns}-final"/>'
            f'<use class="ink" href="#{ns}-final" transform="rotate(180,59,85)"/>'
            f'<use class="accent" href="#{ns}-line"/></svg>')


M = {k: mark(k, *v) for k, v in MARKS.items()}
RD = roundel("rd")


def instance(key):
    """A fresh copy of a mark with its own id namespace.

    Ids are document-global even inside <svg>, so emitting the same mark
    string twice means the second <use> silently resolves to the FIRST copy's
    artwork. That is invisible until the two copies are styled differently -
    it showed up here as the mark on the dark helmet shell rendering black,
    because its <use> was pointing at the hero's defs."""
    instance.n += 1
    if key == "rd":
        return roundel(f"rd{instance.n}")
    return mark(f"{key}x{instance.n}", *MARKS[key])


instance.n = 0
SKETCH = base64.b64encode(
    open(os.path.join(HERE, "original", "1000016578.jpg"), "rb").read()).decode()

STUDIES = [
    ("s000", "01", "First try",
     "Two lines running right across the top and bottom, the way you "
     "described them.",
     "They backfired. Each <em>n</em> is really an <em>o</em> with a small "
     "bite taken out of the bottom, and that bite is the only thing telling "
     "your eye it is an <em>n</em>. The bottom line ran straight through the "
     "bite and filled it in, so every <em>n</em> turned back into an "
     "<em>o</em>."),
    ("s001", "02", "Opened the bite right up",
     "If a small bite disappears, take a bigger one.",
     "Too far the other way. Once the bite gets big, the <em>o</em> stops "
     "being a closed ring and starts looking like a <em>u</em>. The first "
     "half went from reading <em>motopro</em> to reading <em>mutupru</em>."),
    ("s002", "03", "Split the difference",
     "Bite size settled between the two, and the round letters pulled inside "
     "the lines so nothing gets filled in again.",
     "This one works. The first half reads <em>motopro</em> straight off. But "
     "the line is thin, and the second half is rougher than the first &mdash; "
     "which turned out to be the real problem."),
    ("s003", "04", "Where it stands now",
     "Three changes: even quality in both directions, a much heavier line, "
     "and the top and bottom lines rebuilt so they belong to a letter.",
     "This is the one I would put forward. The three changes are spelled out "
     "below."),
]

studies_html = "\n".join(
    f'''    <article class="study" data-step="{i}"{"" if i == 0 else " hidden"}>
      <div class="study-head"><span class="step">{n}</span><h3>{title}</h3></div>
      <div class="plate">{M[key]}</div>
      <dl class="ledger">
        <dt>What I tried</dt><dd>{tried}</dd>
        <dt>What happened</dt><dd>{got}</dd>
      </dl>
    </article>'''
    for i, (key, n, title, tried, got) in enumerate(STUDIES))

dots_html = "\n".join(
    f'        <button type="button" class="dot{" is-on" if i == 0 else ""}" '
    f'data-goto="{i}" aria-label="Attempt {n}, {title}">{n}</button>'
    for i, (key, n, title, _t, _g) in enumerate(STUDIES))

HTML = f"""<title>Motoproponent &mdash; the ambigram, so far</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --paper:     #FAF8F5;
  --sunk:      #F1EDE5;
  --ink:       #14110E;
  --ink-soft:  #57504A;
  --ink-faint: #8E8880;
  --hair:      #DDD7CE;
  --accent:    #C8452F;
  --shell:     #1B1B1D;

  --display: "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;
  --mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
  --rail: 9rem;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper:     #16151A;
    --sunk:      #1E1D23;
    --ink:       #F2EDE6;
    --ink-soft:  #B3ABA2;
    --ink-faint: #8A837B;
    --hair:      #33313A;
    --accent:    #E8654C;
    --shell:     #0C0C0E;
  }}
}}
:root[data-theme="dark"] {{
  --paper:     #16151A;
  --sunk:      #1E1D23;
  --ink:       #F2EDE6;
  --ink-soft:  #B3ABA2;
  --ink-faint: #8A837B;
  --hair:      #33313A;
  --accent:    #E8654C;
  --shell:     #0C0C0E;
}}

* {{ box-sizing: border-box; }}

body {{
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--display);
  font-size: 17px;
  line-height: 1.62;
  -webkit-font-smoothing: antialiased;
}}

/* ---------------------------------------------------------- the artwork */
/* Stroke colours are baked into the sheets as presentation attributes,
   which lose to any CSS rule - so the marks follow the theme. */
.mk {{ display: block; width: 100%; height: auto; }}
.mk .ink {{ stroke: var(--ink); }}
.mk .accent {{ stroke: var(--accent); }}
.on-shell .mk .ink {{ stroke: #F2EDE6; }}

/* ---------------------------------------------------------- scaffolding */
.wrap {{
  max-width: 78rem;
  margin: 0 auto;
  padding: 0 clamp(1.25rem, 4vw, 3.5rem);
}}
section {{ padding-block: clamp(3rem, 7vw, 5.5rem); border-top: 1px solid var(--hair); }}
section:first-of-type {{ border-top: 0; }}

.cols {{ display: grid; gap: clamp(1.5rem, 4vw, 3rem); grid-template-columns: 1fr; }}
@media (min-width: 60rem) {{
  .cols {{ grid-template-columns: var(--rail) minmax(0, 1fr); }}
}}

.rail {{
  font-family: var(--mono);
  font-size: 0.7rem;
  line-height: 1.5;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-faint);
  display: flex; flex-direction: column; gap: 0.4rem;
}}
.rail b {{ color: var(--accent); font-weight: 400; }}

.body {{ display: flex; flex-direction: column; gap: 1.15rem; }}
.body > * {{ margin: 0; }}
.body p, .body li {{ max-width: 36rem; color: var(--ink-soft); }}
.body ul {{ padding-left: 1.1rem; display: flex; flex-direction: column; gap: 0.6rem; }}

h1, h2, h3 {{ margin: 0; color: var(--ink); text-wrap: balance; font-weight: 700; }}
h1 {{ font-size: clamp(2.1rem, 6vw, 3.4rem); line-height: 1.04; letter-spacing: -0.035em; }}
h2 {{ font-size: clamp(1.4rem, 3vw, 1.9rem); line-height: 1.14; letter-spacing: -0.02em; }}
h3 {{ font-size: 1.12rem; letter-spacing: -0.01em; }}
strong {{ color: var(--ink); font-weight: 700; }}
em {{ font-style: normal; font-family: var(--mono); font-size: 0.92em; color: var(--ink); }}

/* ---------------------------------------------------------------- hero */
.hero {{ padding-block: clamp(2.5rem, 6vw, 4.5rem) clamp(2rem, 5vw, 3.5rem); }}
.eyebrow {{
  font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--ink-faint); margin: 0 0 1.1rem;
}}
.lede {{ font-size: clamp(1.05rem, 2vw, 1.25rem); color: var(--ink-soft); max-width: 40rem; margin: 1.1rem 0 0; }}

.stage {{ margin-top: clamp(2rem, 5vw, 3.25rem); }}
.stage .mk {{ transition: transform 900ms cubic-bezier(.7,0,.2,1); transform-origin: 50% 50%; }}
.stage.flipped .mk {{ transform: rotate(180deg); }}
@media (prefers-reduced-motion: reduce) {{
  .stage .mk {{ transition: none; }}
}}

.controls {{ display: flex; flex-wrap: wrap; gap: 0.7rem; align-items: center; margin-top: 1.5rem; }}
button {{
  font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--ink); background: transparent;
  border: 1px solid var(--hair); border-radius: 999px;
  padding: 0.6rem 1.15rem; cursor: pointer;
  transition: border-color 150ms, color 150ms, background 150ms;
}}
button:hover {{ border-color: var(--accent); color: var(--accent); }}
button:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; }}
.hint {{ font-family: var(--mono); font-size: 0.72rem; color: var(--ink-faint); }}

/* --------------------------------------------------------------- quote */
blockquote {{
  margin: 0; padding-left: 1.2rem; border-left: 2px solid var(--accent);
  color: var(--ink); max-width: 36rem;
}}
blockquote p {{ margin: 0 0 0.8rem; color: var(--ink); }}
blockquote p:last-child {{ margin-bottom: 0; }}
figure {{ margin: 0; }}
figure img {{ display: block; width: 100%; height: auto; border: 1px solid var(--hair); }}
figcaption {{
  font-family: var(--mono); font-size: 0.7rem; color: var(--ink-faint);
  margin-top: 0.6rem; letter-spacing: 0.04em;
}}

/* --------------------------------------------------------------- pairs */
.pairs {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.4rem 0 0; padding: 0; list-style: none; }}
.pairs li {{
  font-family: var(--mono); font-size: 0.8rem; color: var(--ink);
  border: 1px solid var(--hair); border-radius: 3px; padding: 0.35rem 0.7rem;
  display: flex; gap: 0.5rem; align-items: baseline; max-width: none;
}}
.pairs .verdict {{ font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; }}
.ok   {{ color: var(--ink-faint); }}
.bad  {{ color: var(--accent); }}

/* --------------------------------------------------------------- plate */
.plate {{
  background: var(--sunk); border: 1px solid var(--hair);
  padding: clamp(1rem, 3vw, 2rem); overflow-x: auto;
}}
/* Wordmarks are 13:1 and need a floor before they turn to mush; the plate
   scrolls rather than letting them shrink. The roundel is square and must be
   exempt, or it blows straight out of its column. */
.plate .mk {{ min-width: 30rem; }}
.plate.tile .mk {{ min-width: 0; }}
.on-shell {{ background: var(--shell); border-color: var(--shell); }}

/* ------------------------------------------------------------ flipbook */
.flip-head {{ display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; justify-content: space-between; margin-bottom: 1.4rem; }}
.dots {{ display: flex; gap: 0.4rem; }}
.dot {{ padding: 0.5rem 0.85rem; }}
.dot.is-on {{ background: var(--ink); color: var(--paper); border-color: var(--ink); }}
.dot.is-on:hover {{ background: var(--accent); border-color: var(--accent); color: var(--paper); }}

.study-head {{ display: flex; gap: 0.85rem; align-items: baseline; margin-bottom: 1rem; }}
.step {{ font-family: var(--mono); font-size: 0.78rem; color: var(--accent); }}

.ledger {{ margin: 1.25rem 0 0; display: grid; gap: 0.35rem 1.4rem; grid-template-columns: 1fr; }}
@media (min-width: 46rem) {{ .ledger {{ grid-template-columns: 9rem minmax(0, 1fr); }} }}
.ledger dt {{
  font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--ink-faint); padding-top: 0.25rem;
}}
.ledger dd {{ margin: 0 0 0.7rem; color: var(--ink-soft); max-width: 36rem; }}
.ledger dd:last-child {{ margin-bottom: 0; }}

/* ----------------------------------------------------------- two tiers */
.tiers {{ display: grid; gap: 1.5rem; grid-template-columns: 1fr; align-items: start; }}
@media (min-width: 46rem) {{ .tiers {{ grid-template-columns: minmax(0,1fr) 12rem; }} }}
.sizes {{ display: flex; gap: 1.4rem; align-items: flex-end; flex-wrap: wrap; margin-top: 1.2rem; }}
.sizes figure {{ display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }}


/* --------------------------------------------------------------- notes */
.callout {{
  border: 1px solid var(--hair); border-left: 2px solid var(--accent);
  padding: 1.1rem 1.3rem; background: var(--sunk);
}}
.callout p {{ margin: 0; max-width: 36rem; color: var(--ink-soft); }}
.callout p + p {{ margin-top: 0.7rem; }}

ol.asks {{ counter-reset: ask; list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem; }}
ol.asks li {{ counter-increment: ask; display: grid; grid-template-columns: 1.9rem minmax(0,1fr); gap: 0.6rem; max-width: 38rem; color: var(--ink-soft); }}
ol.asks li::before {{
  content: counter(ask, decimal-leading-zero);
  font-family: var(--mono); font-size: 0.72rem; color: var(--accent); padding-top: 0.35rem;
}}

footer {{ padding-block: 3rem 4rem; border-top: 1px solid var(--hair); }}
footer p {{ font-family: var(--mono); font-size: 0.72rem; color: var(--ink-faint); margin: 0; letter-spacing: 0.04em; }}
</style>

<div class="wrap">

  <section class="hero">
    <p class="eyebrow">Motoproponent &middot; identity &middot; work in progress</p>
    <h1>It reads the same upside&nbsp;down.</h1>
    <p class="lede">This is where the ambigram has got to. Below is how it got
      here, what I changed from your sketch and why, and the two bits that
      honestly do not work yet.</p>

    <div class="stage" id="stage">{instance("s003")}</div>

    <div class="controls">
      <button type="button" id="flip">Turn it upside down</button>
      <span class="hint" id="hint">Nothing moves but the page &mdash; it is the same artwork.</span>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>The brief</span><span><b>your words</b></span></div>
      <div class="body">
        <h2>What you asked for</h2>
        <blockquote>
          <p>The basic idea is that this will be able to rotate 180&deg; around
            the center &ldquo;O&rdquo;. Its not something you&rsquo;ll look at
            cold and recognize it as the word &ldquo;Motoproponent&rdquo;.</p>
          <p>The main motivation for the ambigram is to be able to paint it on
            a helmet as the center stripe and it be the same from either side
            of my helmet.</p>
        </blockquote>
        <p>Two other things you flagged: the circles were a bit squashed, and
          the whole thing was more crammed together than it needed to be. Both
          are fixed. You also wanted a coloured line down the middle, and a
          line running across the top and bottom &mdash; more on those.</p>
        <figure>
          <img src="data:image/jpeg;base64,{SKETCH}"
               alt="The original pencil recreation of the ambigram, drawn on an iPad">
          <figcaption>Your recreation, redrawn by Devynn</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>The problem</span><span><b>13 letters</b></span></div>
      <div class="body">
        <h2>Why this is hard</h2>
        <p>Motoproponent has thirteen letters. Spin it round and the first
          letter lands where the last one was, the second lands where the
          twelfth was, and so on. So each letter has to be a single shape that
          your eye accepts as two different letters depending on which way up
          it is. The middle <em>o</em> is the only one that stays put &mdash;
          that is the pivot.</p>
        <p>Some of those pairings are friendly. Some are genuinely impossible,
          and no amount of drawing fixes them:</p>
        <ul class="pairs">
          <li><span>m &harr; t</span><span class="verdict ok">works</span></li>
          <li><span>o &harr; n</span><span class="verdict bad">a compromise</span></li>
          <li><span>t &harr; e</span><span class="verdict ok">works well</span></li>
          <li><span>o &harr; n</span><span class="verdict bad">a compromise</span></li>
          <li><span>p &harr; o</span><span class="verdict ok">works</span></li>
          <li><span>r &harr; p</span><span class="verdict bad">impossible</span></li>
          <li><span>o</span><span class="verdict ok">the pivot</span></li>
        </ul>
        <p>That is the honest picture: four of the six pairings behave, and two
          fight back. Which is fine, because you already said it is not meant
          to be readable cold.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>Wrong turn</span><span><b>capitals</b></span></div>
      <div class="body">
        <h2>Capital letters were a dead end</h2>
        <div class="plate">{M["caps"]}</div>
        <p>This was the first direction, and it is worth showing because the
          reason it failed is the reason the current one works.</p>
        <p>Capitals are all one height &mdash; nothing sticks up, nothing hangs
          down. That leaves nowhere to hide the differences between two letters
          that have to share a shape. <strong>M</strong> and <strong>T</strong>
          both need a tall straight edge in the same spot and end up fighting
          over it. Worse, a capital <strong>O</strong> already looks identical
          upside down, so it can never turn into an <strong>N</strong> &mdash;
          the pair collapses into one shape that reads as a zero with a line
          through it.</p>
        <p>You can also see what the top and bottom lines do here: they close
          the whole thing into a box.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>The fix</span><span><b>small letters</b></span></div>
      <div class="body">
        <h2>Small letters solved most of it</h2>
        <p>Small letters have tall bits and low bits &mdash; the stalk on a
          <em>t</em>, the tail hanging off a <em>p</em>. Turn the word upside
          down and a tall bit becomes a low bit. That is exactly the trade the
          difficult pairs needed, and capitals simply do not have it.</p>
        <p>It sorted out your coloured line too. You asked for one line that is
          both the middle bar of the <em>e</em> and the top bar of the
          <em>t</em>. In capitals that is impossible &mdash; those two letters
          swap places when you spin it, so a line at the top of one is at the
          bottom of the other. A small <em>t</em> has its crossbar halfway up
          anyway, so one straight line through the middle is now both bars at
          once, exactly as you described it.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>The attempts</span><span><b>four passes</b></span></div>
      <div class="body">
        <h2>Four goes at it</h2>
        <div class="flip-head">
          <span class="hint">Click through them</span>
          <div class="dots" id="dots">
{dots_html}
          </div>
        </div>
{studies_html}
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>Latest</span><span><b>what changed</b></span></div>
      <div class="body">
        <h2>The three changes in the current one</h2>
        <p><strong>It is now equally good both ways up.</strong> Every earlier
          attempt was drawn to look its best the right way up, so the first
          half read beautifully and the second half was a mess. On a helmet
          that means one side of your head looks right and the other looks
          wrong. Each letter has been pulled back toward the middle so the
          whole word is evenly half-readable instead. It reads as a pattern
          that resolves once you know the word &mdash; which is what you
          described wanting.</p>
        <p><strong>Much heavier line.</strong> Paint, vinyl, stitching and a
          tiny profile picture all need weight behind them. The thin version
          disappeared.</p>
        <p><strong>The top and bottom lines belong to a letter now.</strong>
          You described the last <em>t</em>&rsquo;s bar, which is also part of
          the first <em>m</em>, stretched right across. In the earlier attempts
          I had just drawn two loose lines, which is why they caged the thing
          in. Now the <em>m</em> has a foot, and that foot is what extends
          &mdash; turn it upside down and it lands exactly where the final
          <em>t</em> needs its crossbar. They also stop a bit past the middle
          instead of running the full width, so the mark is open at two corners
          rather than boxed.</p>
        <div class="plate on-shell">{instance("s003")}</div>
        <p class="hint">On a dark helmet shell.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>Second mark</span><span><b>small sizes</b></span></div>
      <div class="body">
        <h2>You need a small version too</h2>
        <p>Thirteen letters in a row is long and thin. Perfect down the middle
          of a helmet &mdash; useless as a YouTube profile picture, a favicon,
          a sticker or a stitched patch, which the channel will need. Shrink
          the full wordmark and it turns into a smudge.</p>
        <p>So the middle <em>o</em> does double duty. It is the point the whole
          thing spins around, it is the only letter that comes out completely
          clean, and with the red line through it, it still reads at the size
          of a browser tab. It is not a second logo &mdash; it is a close-up of
          the one you already have.</p>
        <div class="tiers">
          <div class="plate">{instance("s003")}</div>
          <div class="plate tile">{instance("rd")}</div>
        </div>
        <div class="sizes">
          <figure><div class="tile" style="width:64px">{instance("rd")}</div><figcaption>64px</figcaption></figure>
          <figure><div class="tile" style="width:32px">{instance("rd")}</div><figcaption>32px</figcaption></figure>
          <figure><div class="tile" style="width:16px">{instance("rd")}</div><figcaption>16px</figcaption></figure>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>Straight up</span><span><b>what is broken</b></span></div>
      <div class="body">
        <h2>What still does not work</h2>
        <div class="callout">
          <p><strong>The <em>r</em> and the <em>p</em> will never both be
            right.</strong> The arm of an <em>r</em> sticks out to the right.
            The belly of a <em>p</em> also sticks out to the right. Spin the
            word and right becomes left, so one of them is always facing the
            wrong way. There is no clever drawing that gets round this &mdash;
            it is the geometry. I have drawn it to favour the <em>r</em>,
            because your eye fills in the <em>p</em> from the rest of the word
            more easily than the other way round.</p>
          <p><strong>The <em>o</em> and the <em>n</em> are a compromise, not a
            solution.</strong> The bite that turns an <em>o</em> into an
            <em>n</em> has no right size: small enough to keep a convincing
            <em>o</em> is too small to make a convincing <em>n</em>, and big
            enough for the <em>n</em> turns the <em>o</em> into a <em>u</em>.
            It sits between the two. Giving the letters flat sides rather than
            round ones helped more than fiddling with the bite did.</p>
        </div>
        <p>Neither of these stops the mark working the way you described it.
          They just mean it will never be a thing someone reads cold, and I
          would rather you heard that from me now than noticed it later.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="cols">
      <div class="rail"><span>Over to you</span><span><b>4 questions</b></span></div>
      <div class="body">
        <h2>What I need from you</h2>
        <ol class="asks">
          <li>Is this the right feel? It is deliberately clean and modern to
            keep it miles away from the Old English thing you did not want. Say
            if you want it rougher, or more aggressive.</li>
          <li>Is the red right? It can be anything. If the helmet is already a
            colour, tell me which and I will work to it.</li>
          <li>How do you write the name day to day &mdash; Motoproponent,
            MotoProponent, or all lowercase? It affects everything else that
            gets set alongside the mark.</li>
          <li>Do you want to see it mocked up on an actual helmet before we go
            further, or are you happy judging it flat?</li>
        </ol>
      </div>
    </div>
  </section>

  <footer>
    <p>Motoproponent &middot; ambigram studies &middot; attempt 04</p>
  </footer>

</div>

<script>
(function () {{
  var stage = document.getElementById('stage');
  var flip = document.getElementById('flip');
  var hint = document.getElementById('hint');
  var flipped = false;

  flip.addEventListener('click', function () {{
    flipped = !flipped;
    stage.classList.toggle('flipped', flipped);
    flip.textContent = flipped ? 'Turn it back' : 'Turn it upside down';
    // textContent does not decode entities, so this needs a real character.
    hint.textContent = flipped
      ? 'Same artwork, same pixels\\u2014just rotated.'
      : 'Nothing changes but the angle.';
  }});

  var studies = Array.prototype.slice.call(document.querySelectorAll('.study'));
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dot'));

  function show(n) {{
    studies.forEach(function (s, i) {{ s.hidden = (i !== n); }});
    dots.forEach(function (d, i) {{ d.classList.toggle('is-on', i === n); }});
  }}
  dots.forEach(function (d, i) {{
    d.addEventListener('click', function () {{ show(i); }});
  }});
}})();
</script>
"""

# House style: em dashes are tight, everywhere.  Easier to write the copy
# with spaces around them and close them up once than to hand-set every one.
HTML = HTML.replace(" &mdash; ", "&mdash;").replace(" &mdash;", "&mdash;")

with open(OUT, "w") as f:
    f.write(HTML)
print(f"wrote {os.path.basename(OUT)}  ({len(HTML):,} bytes)")
