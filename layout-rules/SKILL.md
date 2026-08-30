---
name: layout-rules
description: >-
  The load-bearing foundations of a web layout — an explicit column grid
  and shared alignment axes instead of invented offsets, one spacing scale,
  a type scale that stays readable, content that never escapes its
  container, components that survive real variable text, and a layout
  checked across the whole width range rather than at two mockup widths.
  Project-agnostic; carries no palette, fonts or class names of its own.
  Load before composing the first screen of an interface and before
  shipping one. Triggers on layout, composition, alignment, grid and
  columns, gutters and page padding, responsive design, mobile layout,
  breakpoints, media queries, container and max-width, flexbox, overflow,
  horizontal scrollbar, text wrapping and truncation, long URLs, font
  sizes, line-height, line length, fluid type and clamp(), spacing scale,
  whitespace, touch targets, empty and error states, and on any report
  that a page "breaks", "overflows", "looks cramped", "feels misaligned"
  or "is broken on mobile".
---

# Layout rules

The foundations under any screen: the grid elements are placed on, the
scales their sizes come from, and what keeps content inside the boxes
drawn for it.

Rules, not suggestions. Each says what to do and how to check it.

Most of this is correctness rather than taste. A layout that overflows at
320px is broken the same way a crash is broken — it is simply broken
somewhere nobody looked. The specific numbers below are starting
conventions to design against, not constants to obey: adapt them to the
project's content and to a design system that already exists. What is not
adaptable is having a system at all. Inventing a fresh width, offset,
gap or font-size per component is the failure these rules exist to
prevent.

## 1. Use a real layout grid

Before composing or substantially changing an interface, establish an
explicit layout grid. Do not place major elements by independently
inventing widths, margins and horizontal offsets.

Define the grid for at least one representative narrow frame and one
representative wide frame before placing major components.

**Narrow / phone frame**, at a representative width such as 390px:

- 4 columns
- 16px outer gutters
- 16px column gutters
- base spacing unit of 4px or 8px

**Wide / desktop frame**, at a representative width such as 1440px:

- 12 columns
- a bounded content container rather than full-width content
- consistent column gutters
- intentional outer margins
- the same base spacing system used everywhere else

### Place elements on shared grid lines

Major sections should share a small number of alignment axes. Related
elements reuse the same left and right alignment lines, the same
container boundaries, the same column widths, the same gutter logic.

Do not build a page where the hero starts at one arbitrary x-position,
the next section at another, the cards at a third and the footer at a
fourth. Nothing about that is visible in the code — it only appears in
the render, as a page that feels subtly wrong without an obvious cause.

If an element breaks the grid, the break is deliberate and visually
meaningful. Accidental misalignment is a bug.

### Use the grid as a constraint system

Elements span whole columns or align to established grid lines. A grid is
not decoration and not a set of guides to be ignored the moment it is
defined.

Do not hard-code each component's width independently when that width can
be expressed through the shared container and grid. Prefer a small number
of reusable layout primitives over many unrelated values.

### The mobile and desktop grids are related, not identical

Do not scale the desktop grid down. A 12-column desktop composition may
become a 4-column mobile composition, and components may change span,
order or arrangement as space decreases.

For each major component, decide how it maps between the narrow and the
wide grid — then verify the behaviour continuously between them. The two
representative frames are design anchors, not the only widths that must
work (rule 6).

### The container the grid lives in

- **A content container has a `max-width`, not a `width`.** A fixed width
  is a promise the viewport will not keep.
- **Gutters always** — side padding so text never touches the screen
  edge. Text against the bezel reads as broken.
- **Below the max-width the container is fluid:** full width minus its
  padding. `width: min(70rem, 100% - 2rem)` with `margin-inline: auto`
  does the whole job in one line, gutters included.
- **Do not nest gutters.** A padded container inside a padded container
  doubles the inset and the content drifts inward for no reason anyone
  chose. One element owns the page gutter; everything inside goes edge to
  edge of that.
- **`100vw` is not "the width of the page".** With a classic desktop
  scrollbar it is wider than the viewport, so `width: 100vw` inside a
  padded body produces a horizontal scrollbar — the most common single
  cause of that bug. Use `100%`, or `100dvw` where a full-bleed break-out
  is genuinely wanted.

## 2. Use a spacing system

Do not invent spacing values independently for every component. Choose a
small scale, normally built on a 4px or 8px unit, and reuse it for gaps,
padding, margins, section spacing and control spacing.

Not every distance must be identical or mechanically divisible by one
number, but repeated relationships use repeated values. A `margin-top:
37px` anywhere means the scale has been abandoned.

Prefer intentional hierarchy: tight spacing within a component, moderate
spacing between related components, larger spacing between major
sections.

- **Do not use large empty areas to make an interface feel "premium".**
  And do not compensate for weak hierarchy by adding whitespace — a
  `margin-top: 140px` that came from nudging something into place reads
  as a broken section on a laptop screen.
- **Container padding scales with the viewport** — tighter on a phone,
  generous on a desktop, via a step at a breakpoint or a `clamp()`.
  Desktop padding on a 320px screen eats the content column.
- **Touch targets:** 44×44px is the target, 24×24px the floor, and small
  targets need space around them so a thumb cannot hit two at once. A
  control may *look* small and still be big enough — pad it or give it a
  larger hit area — but it must not be small.
- **Vertical rhythm is consistent.** The gap between a heading and its
  text, and between one block and the next, is the same everywhere.
  Uneven vertical spacing is what makes a page feel assembled rather than
  designed.

**Check** — pressable things too small to press:

```js
[...document.querySelectorAll('a, button, [role="button"], input, select, textarea, [onclick]')]
  .map(el => ({ el, r: el.getBoundingClientRect(), cs: getComputedStyle(el) }))
  .filter(({ el, r, cs }) => cs.display !== 'none' && r.width > 0 &&
    (r.width < 24 || r.height < 24) && el.offsetParent !== null)
  .map(({ el, r }) => el.tagName + '.' + el.className +
    ` ${Math.round(r.width)}×${Math.round(r.height)}`)
```

Inline links inside a paragraph are exempt; standalone controls are not.

## 3. Typography has a scale

Do not choose every font size independently. Establish a small scale —
body, secondary, labels, section headings, page headings — and take every
size from it.

|  | Sensible minimum | Good default |
|---|---|---|
| Body text, mobile | 16px | 16–18px |
| Body text, desktop | 16px | 16–18px |
| Secondary text, captions | 12–14px | 14px |
| Buttons, controls | 14–16px | 16px |
| Form inputs on iOS | **16px** | 16px+ |

- **Body text starts at 16px.** Below that, reading is work.
- **Secondary text may be smaller when it is genuinely secondary** —
  12–14px, and nothing under 12px without a reason you can say out loud.
- **Never shrink text to make something fit.** A size is a decision about
  readability, not a lever for fitting a layout. If the text does not fit,
  the container, the wrap or the copy is wrong. This is the most common
  way a machine-written page goes unreadable: `font-size` is the one knob
  that always works, so it is the one that gets reached for.
- **Hierarchy without inflation.** Headings establish order by scale,
  weight and spacing together; not every heading needs to be enormous.
- **Line-height:** ~1.5 for body copy, 1.2–1.3 for headings, looser for
  long prose rather than tighter. Unitless (`line-height: 1.5`), so it
  scales with the element's own size instead of inheriting a fixed px.
- **Measure: 45–75ch for prose.** `max-width: 65ch` is the whole fix.
  Long-form text should not stretch across a wide container merely
  because the screen space is there — a full-width paragraph on a 1440px
  screen loses the reader on every return sweep.

**The iOS trap.** Safari on iPhone zooms the whole page when a focused
`<input>`, `<textarea>` or `<select>` has a font-size under 16px — and it
does not zoom back out. 15px inputs are why a form "jumps" on iPhone.
16px on every form control, `<select>` included.

**The zoom trap.** Text must survive being scaled to 200%. Size it in
`rem`, not `px`, so the user's own font-size setting moves it — and never
size text with viewport units alone, because `vw` does not change when
you zoom:

```css
/* breaks zoom */     font-size: clamp(1rem, 4vw, 1.25rem);
/* scales properly */ font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
```

**Check** — every distinct text size on the page, smallest first, plus any
form control that will zoom on iOS:

```js
(() => {
  const sizes = new Map(), inputs = [];
  for (const el of document.querySelectorAll('*')) {
    if (/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|TITLE)$/.test(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) && parseFloat(cs.fontSize) < 16)
      inputs.push(el.tagName + '.' + el.className + ' @ ' + cs.fontSize);
    const own = [...el.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent.trim()).join('');
    if (!own) continue;
    const px = Math.round(parseFloat(cs.fontSize) * 10) / 10;
    if (!sizes.has(px)) sizes.set(px, { count: 0, lineHeight: cs.lineHeight, sample: '' });
    const rec = sizes.get(px);
    rec.count++;
    if (!rec.sample) rec.sample = own.slice(0, 40);
  }
  return {
    sizes: [...sizes].sort((a, b) => a[0] - b[0]).map(([px, r]) => ({ px, ...r })),
    zoomsOnIOS: inputs,
  };
})()
```

Read the top of that list. Every size under 14px needs a reason, and a
list with eleven distinct sizes in it is not a scale.

## 4. Content must stay inside its layout

Text and intrinsic content must not enlarge a component past its intended
container unless overflow is explicitly part of the design. This one is
not negotiable: text escaping its box, or a stray horizontal scrollbar, is
the most visible way a layout is wrong.

- **Flex and grid children that may shrink need `min-width: 0`.** Their
  automatic minimum size is `auto` — "never smaller than my content" — so
  one long word, URL or hash pushes the whole row wider than the parent
  instead of wrapping. `min-width: 0` (or a non-visible `overflow`)
  restores shrinking. In a column, the same trap is `min-height: 0`.
- **Grid tracks holding arbitrary content:** `minmax(0, 1fr)`, not bare
  `1fr`. `1fr` means `minmax(auto, 1fr)`, and that `auto` floor is the
  same rule — one long string and the column wins the argument with the
  grid.
- **Unbreakable strings need a wrapping strategy** — URLs, hashes,
  tokens, filenames, long IDs:

  ```css
  overflow-wrap: anywhere;   /* also shrinks the box's min-content width */
  ```

  `overflow-wrap: break-word` breaks the *visible* line but does not
  affect intrinsic sizing, so inside a grid or flex track it can still
  blow out the column — `anywhere` fixes both. Avoid `word-break:
  break-all`, which chops ordinary words mid-letter too.
- **Responsive media:** `max-width: 100%; height: auto;` — every time.
  Give images their `width`/`height` attributes or an `aspect-ratio` too,
  so the page does not jump as they load.
- **No fixed `height` on a container holding dynamic text.** Copy grows,
  translations grow more, and a user's font-size setting grows
  everything. Use `min-height` when a floor is needed and let the box
  grow.
- **`white-space: nowrap` only where wrapping would be wrong** — a
  numeric cell, a date, a keyboard shortcut. As a layout crutch on
  variable-length content it guarantees overflow at some width.
- **Clip on purpose or not at all.** Truncation is a decision: it needs a
  visible affordance and the full text still reachable (a `title`, a
  tooltip, an expand). Both forms need `overflow: hidden`:

  ```css
  /* one line */  white-space: nowrap; text-overflow: ellipsis; overflow: hidden;
  /* n lines */   display: -webkit-box; -webkit-box-orient: vertical;
                  -webkit-line-clamp: 3; overflow: hidden;
  ```

  Text that simply disappears under a clipped edge is a bug, not
  truncation. And never reach for `overflow: hidden` on an ancestor to
  make a spill go away — that hides the symptom and takes the sticky and
  focus behaviour of everything inside it with it.
- **Prefer intrinsic sizing to magic numbers** where it says what you
  mean: `min-content`, `max-content`, `fit-content()`, `min()`, `max()`,
  `clamp()`. `width: min(60ch, 100%)` states the intent; `width: 720px`
  states a coincidence.

Do not solve overflow by shrinking the font until the content fits. Fix
the layout constraint.

Ordinary page content stays usable at **320px** CSS width with no
unintended page-level horizontal scrolling. Local horizontal scrolling is
fine only where the component genuinely needs to preserve horizontal
structure — some tables, some timelines.

**Check** — run it at 320px, then again at full width:

```js
(() => {
  const de = document.documentElement, vw = de.clientWidth, out = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const scrolls = /^(auto|scroll)$/.test(cs.overflowX);   // meant to scroll
    const clipped = /^(hidden|clip)$/.test(cs.overflowX);
    const r = el.getBoundingClientRect();
    if (!r.width) continue;
    const spills = el.scrollWidth > el.clientWidth + 1 && !scrolls && !clipped;
    const past = cs.position !== 'fixed' && (r.right > vw + 1 || r.left < -1);
    if (spills || past) out.push({
      el: el.tagName + '.' + (el.className || ''),
      why: spills ? 'content wider than box' : 'extends past viewport',
      overhang: Math.round(spills ? el.scrollWidth - el.clientWidth : r.right - vw),
      text: (el.textContent || '').trim().slice(0, 40),
    });
  }
  return { pageScrollsSideways: de.scrollWidth > vw + 1, offenders: out.slice(0, 40) };
})()
```

`pageScrollsSideways: true` is always a bug. Among the offenders, fix the
outermost one first — a single overflowing child reports its whole
ancestor chain.

## 5. Design for variable content

Do not validate a component only against the exact example text currently
on screen. A reusable or dynamic component stays structurally correct
with:

- short text and long text
- multi-line headings
- long names
- large numbers
- missing optional content
- empty states
- validation and error text
- localized text, where localization is relevant

Do not assume a heading, label, button, metadata row or name stays on one
line. **Text wrapping is part of layout, not an edge case.**

So test with real content, not lorem: the longest name in the data, a
150-character URL, an empty list, and a number with five more digits than
you expect.

## 6. Check the whole width range

A layout is not responsive because it looks correct at one phone width
and one desktop width. Use the two frames to establish the system, then
resize continuously between them and watch. Bugs live between the
breakpoints, which is exactly where mockup-width testing never looks.

Check especially:

- just below each layout transition
- at the transition
- just above it
- 320px, as a narrow-width smoke test
- the representative phone frame
- the representative desktop frame

**Add a breakpoint where the composition actually stops working** — where
the cards get too narrow to read, where the nav stops fitting. Not
because a common device width exists; "iPhone width" is not a property of
your layout, and the device it was named after is discontinued.

Prefer fluid to stepped where it fits: `clamp()` for type and spacing,
`repeat(auto-fit, minmax(16rem, 1fr))` for card grids. A grid that
reflows on its own needs no breakpoint at all.

If the same failure shows up at several widths, fix the underlying grid,
sizing or content constraint. Do not paper over it with a media query per
screenshot.

## Before calling a layout done

1. The grid is written down, and every major element sits on one of its
   axes.
2. Drag the window from 320px to full width. Nothing overflows, nothing
   clips, nothing collapses.
3. Run the overflow check at 320px. `pageScrollsSideways` is `false`.
4. Every form input is 16px or more.
5. The longest real string in the data — URL, name, number — is in the
   layout, and it wraps.
6. Prose sits in a 45–75ch column.
7. Every gap on the page is a step on the scale.
