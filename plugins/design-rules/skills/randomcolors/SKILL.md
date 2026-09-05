---
name: randomcolors
description: >-
  Build a project's colour system from a seed palette instead of emitting
  remembered hex codes, so it does not come out the same indigo-and-slate
  every time. Takes a seed — four swatches pasted from Colorhunt or Coolors,
  a brand colour, a palette fetched from the Colormind API, or a hue geometry
  rolled locally — keeps its hues, and rebuilds the lightness and chroma into
  a full role system (surfaces, text, borders, accent with its states,
  focus ring, semantic colours) whose every rendered pair is solved and
  verified against WCAG in both light and dark. Emits CSS custom properties
  ready to paste. Load whenever colours are being chosen: a new project's
  palette, a redesign, a theme, dark mode, "pick some colours", "these
  colours look generic or AI-made", brand colour needs a system around it,
  or an existing palette fails contrast. Triggers on colour palette, colour
  scheme, theme, design tokens, brand colour, accent colour, dark mode,
  OKLCH, contrast failure, WCAG, Colorhunt, Coolors, Colormind.
---

# Random colours

Left to itself a model writes the same palette every time: indigo `#6366f1`,
violet `#8b5cf6`, slate `#0f172a`, and off-white `#f8fafc`. That is not a
taste — it is Tailwind's default, which is the most common palette in the
training data, so it is the most probable string of characters. Hex makes it
worse: nothing in `#6366f1` says how light it is, so the colours cannot be
reasoned about, only recalled.

The fix is not to remember better palettes. It is to stop recalling and
start constructing: **take the hues from outside, rebuild the lightness
ladder here, solve every pair for contrast.**

```
scripts/palette.py --seed "#c93e5a,#27273c,#699198,#c1bda7"
scripts/palette.py --colormind ui
scripts/palette.py --colormind fauvism --lock "#c93e5a"
scripts/palette.py --random --rng-seed 42
```

Output is a contrast report and a block of CSS custom properties for both
themes. **The script exits non-zero if any pair fails**, so it can gate a
commit; if it prints `FAIL`, the palette is not finished.

## Where the seed comes from

The seed exists to supply hues that did not come out of the model's memory.
Any of these do that:

- **The person pastes one.** Four hexes from Colorhunt, Coolors, a photo,
  their brand — `--seed "#a,#b,#c,#d"`. Prefer this when they have any
  opinion at all. Note that **Colorhunt cannot be fetched**: its palettes
  are served from `/tab.php`, which its `robots.txt` disallows, and its
  crawlable pages contain no colour data. Ask for the hexes; do not scrape.
- **Colormind** — `--colormind <model>`, a keyless public API. Models:
  `ui` (trained on interfaces, the safe default), `default`, and the
  character ones — `fauvism`, `akira_film`, `contempt_1963`,
  `game_of_thrones`. Passing `--lock "#hex"` keeps a brand colour and lets
  the model complete the rest around it.
- **A local roll** — `--random` picks a base hue and one of four geometries
  (analogous, complement, split-complement, triad). No network. Also the
  automatic fallback when Colormind is unreachable, announced on stderr.

Two colours are enough; four or five give the system spare accents for
charts and tags.

## What the script keeps and what it rebuilds

**Kept: the hues, and their relationships.** Those are what a person chose
when they made the palette, and they are the part worth having.

**Rebuilt: lightness and chroma.** A four-swatch aesthetic palette is a
mood, not an interface. It has no page background, no card, no muted text,
no disabled state, no dark mode, and no guarantee that any two of its
colours can legally be put on top of each other. That gap is the actual
work, and it is why "just use the palette from the gallery" produces a page
that looks nice in a screenshot and fails the moment it has real content.

The roles it produces: `bg`, `surface`, `surface-sunken`, `border`,
`border-strong`, `text`, `text-muted`, `accent` with `accent-hover`,
`accent-active`, `accent-subtle`, `on-accent`, `on-accent-subtle`, `focus`,
`success` / `warning` / `danger` each with an `on-` fill pair and a `-text`
variant, plus `accent-2…4` from the seed's remaining hues.

Neutrals are not grey: they carry a trace of the seed's hue at chroma
~0.012. That single decision is most of what separates a palette that
reads as designed from one that reads as a default.

## Why it is solved rather than assigned

**OKLCH lightness is not luminance.** Yellow at `L=0.75` and blue at
`L=0.75` differ by more than two to one in WCAG contrast against white. So
a palette built by handing each role a lightness — which is how almost
every OKLCH generator works — passes on some hues and quietly fails on
others.

Here every foreground is binary-searched against its *actual* backgrounds
until it reaches its target, and then re-measured. Two consequences worth
knowing:

- **Minimal overshoot is deliberate.** `text-muted` lands at 4.50:1, not
  9:1. Muted text that overshoots is not muted any more, it is just text,
  and the hierarchy it was supposed to create is gone.
- **Chroma is reduced, never clipped.** Out-of-gamut colours are brought in
  by lowering chroma at constant hue, because clipping RGB channels shifts
  the hue — which is why a naive picker hands back a colour that does not
  match the number you asked for. Every reduction is reported as a note.

The check that earns the tool its place caught a bug in its own first
draft: deriving `accent-hover` by stepping lightness in a fixed direction
walks the fill *towards* the text sitting on it whenever that text is dark,
and `on-accent` fell to 3.68:1. States now step away from their own
foreground, and shrink the step rather than break the 3:1 against the page.

## Verification

Every run measures 27 pairs per theme, 54 in all: text on each of the three
surfaces, muted text on each, borders, the accent on the page and on a
card, the label on the accent in all three of its states, the chip, the
focus ring, each semantic fill with its label and its text variant, and the
spare accents.

Two hundred random seeds were generated and every one passed in both
themes, with accent hues spread across the whole circle — the indigo band
that a model reaches for unprompted took twenty of the two hundred rather
than all of them. Eight live Colormind palettes passed as well.

One honest artifact: blues and cyans turn up as the accent slightly less
often under `--random`, because sRGB allows less chroma there at mid
lightness, so those hues less often win the most-chromatic slot. Pass
`--seed` with a blue if you want one.

## Using the result

Paste the CSS as-is. It emits `:root` for light, the same tokens under
`prefers-color-scheme: dark` guarded by `:root:not([data-theme="light"])`,
and again under `:root[data-theme="dark"]` so an explicit toggle wins in
both directions.

Then check the page, because the script only knows the pairs it was told
about. Text over an image or a gradient, anything behind a `backdrop-filter`
and any colour a component invents locally are outside its reach — those
are for the contrast audit in the `no-slop` skill, which reads the rendered
page instead of the token list.

And a palette does not make a design. What colour is doing here is
carrying meaning and hierarchy; the composition, rhythm and motion sit in
`layout-rules` and `design-research`.
