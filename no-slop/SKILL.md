---
name: no-slop
description: >-
  Catch and strip the tell-tale signs of AI-generated UI — rainbow or gradient
  headings, fake live/status chrome, ∴ decoration, empty eyebrow kickers,
  monospace body copy, half-painted card edges, hand-drawn SVG artwork — and
  hold the correctness invariants a machine-written page usually misses,
  namely WCAG contrast and
  chrome that never takes a text selection. Project-agnostic; carries no
  palette, fonts or class names of its own. Load before shipping any interface,
  and whenever asked whether a design looks AI-made or "sloppy". Triggers on
  UI review, visual polish, pre-ship review, design cleanup, accessibility
  review, AI-generated look, slop, neuroslop, vibe-coded UI, and on
  establishing an initial design system, visual language, component library
  or interface direction for a new project — as well as on the concrete
  work, headings, status bars, badges, eyebrows, icons, contrast, animation,
  motion, transitions and CSS.
---

# No slop

The tells that make an interface read as machine-written, and the
correctness invariants machine-written interfaces usually miss.

Rules, not suggestions. Each says what to do and how to check it.

**No rule here has an exception you may grant yourself.** Slop stays out
even when it looks justified by the interface — that feeling is the tell,
not a reason, and it will feel justified every time. Only the person you
are working for can waive a rule, and only by asking for the thing
directly. When unsure whether something reads as slop, leave it out or
ask.

## When establishing a design system

Apply these rules before choosing decorative conventions. Do not introduce
AI-default motifs into the design language in the first place — gradient
headings, fake status chrome, decorative eyebrows, arbitrary monospace,
faux telemetry and ornamental tech glyphs should not become reusable system
primitives unless explicitly requested.

A token or a component variant is where this bites hardest: one bad
instance is one fix, but a `--status-live` colour or an `.eyebrow` class
is an invitation, and everything built on it inherits the motif without
anyone choosing it again.

The goal is prevention, not cleanup. A design system should make slop
difficult to produce downstream.

## 1. A title is one flat colour

A heading whose words are different colours ("THINGS" cyan + "DRAW"
lavender) reads as instant slop. So does a gradient fill across the text.
One heading, one flat colour.

No exceptions. If a two-tone split or a gradient feels justified by the
interface, it is not — that feeling is the tell itself.

**Check:** every heading resolves to a single computed `color`, with no
`background-clip: text`.

## 2. No fake system chrome

Nothing may imply a running system that isn't there:

- no pulsing status dots
- no `SYS:ONLINE`, `● Live`, `online` badges
- no invented telemetry, uptime, latency or "system" readouts

A status bar carries a title and, if useful, a clock.

**Check:** every number and state on screen traces to real data. If you
cannot name where a value comes from, delete it.

## 3. `∴` is banned as decoration

The "therefore" symbol is a heavy slop tell. Never use it in eyebrows,
tickers, status bars, dividers or credits rows. Use a plain word, an
em-dash, or nothing. The same goes for emoji used as bullets or section
markers. Only if explicitly asked for.

## 4. Eyebrows need permission

A tiny uppercase letter-spaced kicker above a heading ("INKWASH · HOW IT
WORKS", "OVERVIEW", "INTRODUCING") is a dead giveaway. It fills the slot
above the title with something magazine-shaped and carries no
information.

Do not add one unless the user asked, or you asked and they said yes.
The heading stands on its own.

## 5. Monospace is for code

Use a mono face inside code blocks, or when the user asks for it. Not for
body copy, headings, labels, captions, buttons or nav — mono as a general
UI face is a tell.

A project may override this deliberately, in which case its own design
rules say so.

## 6. Card edges are never half-painted

A card with one or two edges in a coloured tint — a left rib, a right rib,
a top stripe, a bottom band — while the rest of the border is hairline or
a different colour. Never, and never because the interface seems to call
for it. Only if the person asks for it directly.

Do one of these instead:

- **No tint** — uniform hairline border on all four sides; the category
  colour lives inside the card, in the tag text, badge or accent glyph
- **Paint the whole card** — solid colour-fill background, all four edges
  matching, one hard border around the lot

Applies to every card-like surface: grid tiles, list rows drawn as cards,
specimen and artifact tiles, and any new card-like surface added later.

**Check:** for every card, the four border colours are equal.

## 7. Contrast

Every text element against its effective background:

| | |
|---|---|
| Normal text | **4.5:1** minimum |
| Large text (≥24px, or ≥18.7px at weight 700+) | **3:1** minimum |
| Icons, borders and controls carrying meaning | **3:1** minimum |

Effective background is the first opaque ancestor — a transparent
element has none of its own.

**Every state counts, not only the resting one.** Selected, current,
hover, focus, active, visited and disabled each carry their own pair of
colours. A selected row that flips to a tinted fill is where this fails
most often, and it is the easiest failure to miss: those colours exist
only while the state is set, so a page that looks fine at rest can be
unreadable the moment something is chosen.

**Check.** When you can drive a browser, run a real accessibility audit
first — axe, Lighthouse, or the DevTools accessibility inspector. Those
render the page, so they see compositing, images and overlays that no
script reading computed styles can reach.

The script below is the fallback for when you cannot, and it adds the
state sweep those tools do not do. It normalises colour through a canvas,
so `oklch()` / `lab()` / `color()` resolve instead of being read as three
unrelated numbers, and it composites semi-transparent layers instead of
taking any tint for an opaque background.

Treat `fails` as things to fix or account for — not as a complete list.
Anything it cannot resolve (text over a gradient or image, opacity on an
ancestor, a filter, a blend mode) comes back under `couldNotJudge` rather
than quietly passing, and those need eyes or real tooling. A page can be
clean here and still be unreadable where the script had to abstain.

`:hover` and `:focus` cannot be forced from a script either, so a rule
setting only one of the two colours stays out of reach — use the
browser's force-element-state panel for those.

```js
(() => {
  // getComputedStyle returns oklch() / lab() / color() verbatim, so colours are
  // normalised by painting them — canvas resolves any syntax to sRGB bytes. An
  // invalid value leaves fillStyle untouched, which is how it is detected.
  const cx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  const rgba = css => {
    if (!css) return null;
    cx.fillStyle = '#000'; cx.fillStyle = css; const a = cx.fillStyle;
    cx.fillStyle = '#fff'; cx.fillStyle = css; const b = cx.fillStyle;
    if (a !== b) return null;
    cx.clearRect(0, 0, 1, 1); cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  };
  const over = (f, b) => [0, 1, 2].map(i => f[i] * f[3] + b[i] * (1 - f[3])).concat(1);
  const lin = c => (c /= 255) <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4;
  const lum = c => .2126 * lin(c[0]) + .7152 * lin(c[1]) + .0722 * lin(c[2]);
  const ratio = (f, b) => {
    const [x, y] = [lum(f), lum(b)].sort((m, n) => n - m);
    return (x + .05) / (y + .05);
  };

  // What this cannot compute, named instead of guessed at. Stops at the first
  // fully opaque layer, since nothing above it can affect the result.
  const unknown = el => {
    // Opacity, filters and blending anywhere above repaint the whole subtree,
    // so the walk cannot stop early for these the way it can for backgrounds.
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (n !== el && +cs.opacity < 1) return 'opacity on an ancestor';
      if (cs.filter !== 'none') return 'filter';
      if (cs.mixBlendMode !== 'normal') return 'blend mode';
    }
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== 'none') return 'background image or gradient';
      const c = rgba(cs.backgroundColor);
      if (c && c[3] === 1) return null;
    }
    return null;
  };
  // Semi-transparent layers are composited, not treated as opaque.
  const bgOf = el => {
    let acc = null;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const c = rgba(getComputedStyle(n).backgroundColor);
      if (!c || c[3] === 0) continue;
      acc = acc ? over(acc, c) : c;
      if (acc[3] === 1) return acc;
    }
    return over(acc || [0, 0, 0, 0], [255, 255, 255, 1]);
  };
  const own = el => [...el.childNodes].filter(n => n.nodeType === 3)
    .map(n => n.textContent.trim()).join('');

  const fails = [], skipped = {}, seen = new Set();
  const sweep = state => {
    for (const el of document.querySelectorAll('*')) {
      const txt = own(el);
      if (!txt) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      const note = why => {
        if (state === 'resting') (skipped[why] = skipped[why] || []).push(txt.slice(0, 30));
      };
      const why = unknown(el);
      if (why) { note(why); continue; }
      const fg = rgba(cs.color);
      if (!fg) { note('unreadable colour'); continue; }
      const bg = bgOf(el);
      const size = parseFloat(cs.fontSize);
      const need = (size >= 24 || (+cs.fontWeight >= 700 && size >= 18.66)) ? 3 : 4.5;
      const r = ratio(over(fg, bg), bg);
      if (r < need && !seen.has(el)) {
        if (state === 'resting') seen.add(el);
        fails.push({ state, el: el.tagName + '.' + (el.className || ''),
                     ratio: +r.toFixed(2), need, text: txt.slice(0, 40) });
      }
    }
  };

  sweep('resting');

  // A state's colours exist only while the state is set, so set it. Collect the
  // state classes this page's own CSS defines, apply each, sweep, put it back.
  const classes = new Set();
  const sheets = [...document.styleSheets];
  for (const sh of sheets) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const r of rules || []) {
      const m = (r.selectorText || '').match(/\.[\w-]*(active|selected|current|open|checked)[\w-]*/gi);
      if (m) m.forEach(c => classes.add(c.slice(1)));
    }
  }
  const targets = [...document.querySelectorAll('*')].filter(own);
  for (const cls of classes) {
    const added = targets.filter(e => !e.classList.contains(cls));
    added.forEach(e => e.classList.add(cls));
    sweep('.' + cls);
    added.forEach(e => e.classList.remove(cls));
  }

  // :hover / :focus cannot be forced from script. Where such a rule sets both
  // colours itself, check that pair directly.
  for (const sh of sheets) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const r of rules || []) {
      const sel = r.selectorText || '';
      if (!/:(hover|focus|focus-visible|active|visited)/.test(sel)) continue;
      const fg = rgba(r.style.color), bg = rgba(r.style.backgroundColor);
      if (!fg || !bg || bg[3] < 1) continue;
      const rr = ratio(over(fg, bg), bg);
      if (rr < 4.5) fails.push({ state: 'css rule', el: sel, ratio: +rr.toFixed(2), need: 4.5, text: '' });
    }
  }

  return { fails, couldNotJudge: Object.fromEntries(
    Object.entries(skipped).map(([k, v]) => [k, { count: v.length, examples: v.slice(0, 3) }])) };
})()
```

## 8. Chrome is not text

Anything you press or glance at must never take a text selection:
buttons, close crosses (`×`), tabs, tool glyphs, hover labels, viewer
tips, counters, frame numbers, drag handles, navigation tiles,
decorative glyphs. A selection smear over a `×` is always a mis-drag, and
it instantly reads as a broken page.

```css
button, [role="button"] {
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;   /* no long-press save/copy sheet on iOS */
}
```

Every stylesheet that does not `@import` one already carrying that block
needs its own copy. Pressable chrome that isn't a `<button>` (tips,
counters, chips, drag bars) goes in that page's own selector list.

Two traps:

- **`all: unset` wipes it.** A reset like `.hotspot { all: unset }` puts
  `user-select` back to `auto`. Any rule using `all: unset` / `all: initial`
  must re-declare `user-select: none` right after it.
- **Images drag away.** `<img>` inside anything clickable needs
  `draggable="false"`, or a drag starts a native image-drag instead of
  your gesture.

Real content stays selectable: prose, blurbs, descriptions, titles, list
rows, credit and article links. People copy those on purpose.

**Check** — anything returned that isn't a prose/content link is a bug:

```js
[...document.querySelectorAll('*')].filter(el => {
  const cs = getComputedStyle(el);
  const clickable = el.tagName === 'BUTTON' ||
    el.getAttribute('role') === 'button' || cs.cursor === 'pointer';
  const txt = (el.textContent || '').trim();
  return clickable && txt && txt.length < 60 && cs.userSelect !== 'none';
}).map(el => el.tagName + '.' + el.className);
```

## 9. Do not hand-draw artwork

Do not author complex icons, mascots, illustrations or figures as SVG
path data. Multi-path artwork written by hand comes out misshapen, and
the failure is invisible in the code — it only appears in the render.

Use an icon set with a clear licence (Lucide, Heroicons, Phosphor and
Tabler are MIT) or an asset the user supplies. Record source and licence
beside the asset, and check the licence before use — marketplace assets
vary per item and many forbid redistribution.

Simple geometry you may write directly: rules, arrows, chevrons, carets,
single-shape marks.

If nothing suitable exists, say so and ask. Do not improvise a drawing.

## 10. Research a mechanic before you invent one

Before building anything with non-trivial motion or interaction — a
scroll-driven sequence, a drag or gesture, a page transition, 3D, physics,
elaborate hover choreography, anything on a canvas — stop and ask the
person whether to research how it is actually done first.

Ask rather than assume: research costs time, and they may already know
exactly what they want. But do not reconstruct a mechanic from memory
unasked. Memory returns the average of everything seen, and the average is
the definition of generic — the same reason the tells above exist.

When the answer is yes, look at real work: awwwards and Godly for what is
current, Codrops for the same effects with source you can read, and the
`awwwards` / `awwwards-inspired` GitHub topics, which collect rebuilds of
sites that ship no source of their own.

Take the **mechanism**: what moves, triggered by what, over what duration,
with what easing, and what the container does while it happens. Do not
take the implementation — award-winning sites are usually built on a stack
this project does not use, so the code will not port even though the idea
will.

Leave behind: scroll-jacking, which fights any page meant to be read, and
any animation library the project does not already have. Adding a heavy
dependency is the person's call, not yours.

Whatever you build, honour `prefers-reduced-motion` — a reduced-motion
user gets the state change without the travel. It is the most commonly
skipped part of machine-written animation.

## 11. When they are unhappy, search — do not remember

When the person says a design is wrong, off, cheap, generic, or looks
AI-made, do not fix it from memory and do not simply guess again. Run a
real web search.

The reason is exact: the output that just disappointed them came out of
the same memory you would otherwise consult. Recall returns the average,
and the average is what went wrong. A second guess from that source is
usually the first mistake in a different colour.

Search for the specific thing being criticised together with the
complaint, for how the pattern is done well by people who do it for a
living, and for the known failure modes of machine-written interfaces in
that particular context — they are well documented and specific, not
folklore.

Read the results before changing anything. Then say what you found and
what you are changing because of it, so the person can tell whether you
understood the complaint or just moved things around. If the search turns
up nothing useful, say so and ask — that is worth more than another guess.

## 12. The general rule

If an element exists only to look techy or AI-made and carries no real
meaning, it is slop. Leave it out. Fewer fake-system flourishes, not more.

## Before calling a UI done

1. Run the accessibility audit, or the scripts. Fix what they return, and
   look with your own eyes at whatever the contrast one could not judge.
2. Every heading: one flat colour.
3. Every number on screen: traceable to real data.
4. Every eyebrow: asked for, or removed.
5. Every card: four edges the same, or the whole card filled.
