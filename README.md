# skills

Skills for Claude — review rules for building and shipping interfaces.

The skills are project-agnostic: they carry no palette, fonts or class
names of their own, and they say what to do *and* how to check it. The two
review skills ship eight runnable browser checks between them, so a review
ends in a list of offending elements rather than an opinion.

## Skills

### `no-slop`

Strips the tells that make an interface read as machine-written, and holds
the correctness invariants a generated page usually misses.

Twelve rules, among them: a heading is one flat colour, never a gradient or
a word-split; no fake `● Live` / `SYS:ONLINE` chrome or invented telemetry;
`∴` is not decoration; an eyebrow kicker needs permission; monospace is for
code; a card's four edges match or the whole card is filled; WCAG contrast
in *every* state, not just at rest; nothing pressable takes a text
selection; do not hand-write SVG artwork; research a motion mechanic before
inventing one; and when someone says a design looks AI-made, search — do
not guess again from the same memory that produced it.

Two checks: a contrast audit that composites transparent layers, resolves
`oklch()`/`lab()` through a canvas and sweeps selected/active states, and a
sweep for clickable elements that still take a selection.

Load it before shipping any interface, when establishing a design system,
or when asked whether something looks AI-made.

### `layout-rules`

The foundations under any screen — the grid elements are placed on, the
order the eye reads them in, the scales and components their look comes
from, and what keeps content inside the boxes drawn for it.

Nine rules:

1. **Use a real layout grid** — a narrow and a wide frame defined before
   composing, shared alignment axes, the grid as a constraint system rather
   than guides that get ignored; container with `max-width`, gutters that
   never nest.
2. **Establish a visual hierarchy** — primary content, support, metadata
   and chrome must not read at comparable size, contrast, weight and
   spacing. Demote rather than promote.
3. **Use a spacing system** — one 4/8px scale for every gap, padding and
   margin; touch targets of 44px, floor of 24px.
4. **Typography has a scale** — 16px body, 12–14px secondary, 16px form
   inputs (below that iOS zooms and does not zoom back), 45–75ch measure.
   Never shrink text to make something fit.
5. **Reuse before you invent** — reuse the buttons, cards, radii and
   shadows a project already has; no near-duplicates that differ only in a
   couple of pixels or a slightly different muted colour.
6. **Prefer flow over coordinate placement** — absolute positioning is for
   genuinely overlaid relationships, and an overlay must escape the
   ancestors that clip it (including the `transform` / `filter` / `contain`
   that trap even `position: fixed`).
7. **Content must stay inside its layout** — `min-width: 0`,
   `minmax(0, 1fr)`, `overflow-wrap: anywhere`, no fixed heights on dynamic
   text, deliberate truncation, 320px with no page-level sideways scroll.
8. **Design for variable content** — long names, empty states, error text,
   multi-line headings. Wrapping is part of layout, not an edge case.
9. **Check the whole width range** — resize continuously; a breakpoint goes
   where the composition breaks, not where a device is named.

Six checks: text ranked by visual weight, a census of radii / shadows /
colours flagging near-duplicates, the type scale plus inputs that zoom on
iOS, undersized touch targets, what is trapping an overlay, and an overflow
sweep for 320px.

### `design-research`

Finds out how a design has actually been built before inventing an answer —
because recall returns the average of everything seen, and the average is
the definition of generic.

The skill is one pipeline, and each step is a different kind of source: **a
gallery gives you a name, GitHub gives you the code, the live site gives you
the numbers.**

1. **Get a name.** A gallery is a wall of images — measured,
   `godly.website` returns 133 words of text and `cosmos.so` 143 — so it is
   a name index, nothing more. Curated lists on GitHub are Markdown and read
   perfectly, which the galleries do not.
2. **Find somebody's rebuild.** Award winners ship no source; people who
   rebuild them to learn do. `"dennis snellenberg" in:name,description,readme`
   returns a 185-star rebuild whose description names the whole stack. The
   skill carries the query rules that make this work — one name per query,
   never the bare word `clone`, and why `topic:awwwards` is for browsing
   rather than finding. Studios also publish their own mechanics:
   `Cuberto/mouse-follower` is the cursor effect from their award sites,
   original and licensed.
3. **Read the live site.** Its markup names the stack, so a screenshot is
   never the best available evidence; with a browser, its computed styles
   hand over the type scale, spacing steps and breakpoints.
4. **Find the mechanic as code.** When you know the technique but not the
   site, search the API call instead of the name.

Plus: take the mechanism and leave the implementation, check the licence
before copying anything, rate a source before trusting it (a Dribbble shot
is a drawing of an interface), and report three references with costs rather
than one.

The catalogue of about eighty checked sources lives in
[`references/sources.md`](plugins/design-rules/skills/design-research/references/sources.md),
each tagged with what an automated fetch actually gets back.

## Install

As a plugin, from this repository:

```
/plugin marketplace add madokamemika/skills
/plugin install design-rules@madokamemika
```

Or copy a single skill into a project or your home directory — a skill is
one self-contained `SKILL.md`, with no scripts or assets beside it:

```
cp -r plugins/design-rules/skills/no-slop ~/.claude/skills/
```

## Layout

```
.claude-plugin/marketplace.json     the marketplace this repo publishes
plugins/
  design-rules/
    .claude-plugin/plugin.json      the plugin manifest
    skills/
      no-slop/SKILL.md
      layout-rules/SKILL.md
      design-research/
        SKILL.md
        references/sources.md
```

A skill lives at `skills/<name>/SKILL.md` inside a plugin — that is where
Claude Code looks, so the path is structure, not preference. Unrelated
skills added later get their own directory under `plugins/` and their own
entry in `marketplace.json`, rather than being bolted onto this plugin.

## Licence

MIT — see [LICENSE](LICENSE).
