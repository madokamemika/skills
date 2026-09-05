# skills

Skills for Claude — review rules for building and shipping interfaces.

The skills are project-agnostic: they carry no palette, fonts or class
names of their own, and they say what to do *and* how to check it. The two
review skills ship eight runnable browser checks between them, and the
colour skill ships a generator that verifies its own output, so a review
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

Researches a design in stages instead of inventing one, because recall
returns the average of everything seen, and the average is the definition of
generic.

**Find a site → find its rebuild → read how it works → build the smallest
version → name what you took.**

1. **Find a site** on Awwwards, the FWA, Godly, SiteInspire, Hoverstat.es
   for the experimental end, Codrops when you want the effect with its
   source. A gallery is a name index, not a picture book — measured,
   `godly.website` returns 133 words of text — so it is mined for the names
   of sites and studios, which are the query for everything after.
2. **Find somebody's rebuild.** Award winners ship no source; people who
   rebuild them to learn do. `"dennis snellenberg" in:name,description,readme`
   returns a 185-star rebuild naming its whole stack. The skill carries the
   query rules that make this work, each from a failed search: one name per
   query, never the bare word `clone`, `topic:awwwards` browses rather than
   finds. Studios also publish the mechanics they won with —
   `Cuberto/mouse-follower` is the cursor effect from their award sites,
   original and licensed.
3. **Read how it works.** The live site's markup names its stack; its
   computed styles hand over the type scale, spacing steps and durations.
4. **Build the smallest version** — one card, one reveal, one pin — then put
   it beside the original. What is still wrong is almost always the timing.

Then the part that decides whether the research was worth anything: **take
the shapes, not the palette.** The palette is the first thing anyone
extracts and the last thing that transfers — those colours were chosen
against someone else's photography and density. What travels is the
composition, the shape language, the rhythm down the page, the motion *with
its numbers*, type as material, and the register — said out loud and then
traced back to which of the others produce it. Name those and you can build
in the same spirit while sharing no pixels; bring back hex codes and you
have a costume.

### `randomcolors`

Builds a colour system from a seed instead of emitting remembered hex codes.
Left alone a model writes the same palette every time — indigo `#6366f1`,
violet `#8b5cf6`, slate `#0f172a` — which is not a taste but Tailwind's
default, the most probable string of characters rather than a choice.

So the hues come from outside (four hexes pasted from Colorhunt or a brand,
the keyless Colormind API with its `ui` and `fauvism`-style models, or a hue
geometry rolled locally), and everything else is rebuilt here: a lightness
ladder, twenty-odd roles — surfaces, text, borders, accent with its states,
focus ring, semantics — and neutrals carrying a trace of the seed hue rather
than being grey.

Every foreground is binary-searched against its actual backgrounds until it
reaches its target, because **OKLCH lightness is not luminance** — yellow and
blue at the same lightness differ by more than 2:1 against white, so
generators that *assign* lightnesses fail on some hues and not others. Muted
text lands at exactly 4.50:1, since overshooting means it is not muted any
more. Out-of-gamut colours lose chroma rather than being clipped, which would
shift the hue.

```
scripts/palette.py --colormind ui
scripts/palette.py --seed "#c93e5a,#27273c,#699198,#c1bda7"
```

Out comes a 54-pair contrast report and CSS custom properties for both
themes; the script exits non-zero if anything fails, so it can gate a commit.
Two hundred random seeds all passed, with accent hues spread across the whole
circle — the indigo band took twenty of them, not all two hundred.

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
      design-research/SKILL.md
      randomcolors/
        SKILL.md
        scripts/palette.py
```

A skill lives at `skills/<name>/SKILL.md` inside a plugin — that is where
Claude Code looks, so the path is structure, not preference. Unrelated
skills added later get their own directory under `plugins/` and their own
entry in `marketplace.json`, rather than being bolted onto this plugin.

## Licence

MIT — see [LICENSE](LICENSE).
