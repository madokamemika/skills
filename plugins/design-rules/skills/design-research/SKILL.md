---
name: design-research
description: >-
  Research a design in stages instead of inventing one: find a site that
  already solved it on Awwwards, Godly, Codrops or Hoverstat.es; find
  somebody's open rebuild of it on GitHub; read how it is actually built;
  build the smallest version yourself to check you understood it. Carries
  the query syntax for each stage, and the part that decides whether the
  research was worth anything — what to take from a reference, which is the
  composition, the shape language, the rhythm and the motion, never the
  palette. Load before building any non-trivial interaction, motion or
  layout mechanic; when picking a pattern with obvious prior art; when
  establishing a visual direction; and whenever someone says a design looks
  generic, cheap or AI-made. Triggers on design research, references, prior
  art, inspiration, awwwards, FWA, competition winners, case study,
  teardown, breakdown, "how is this done", "how did they build that", "find
  a repo that does this", clone or rebuild of a site, experimental web
  design, scroll-driven and WebGL effects, GSAP, Lenis, three.js, motion
  and interaction patterns, visual direction, moodboard, and on "make it
  look less generic".
---

# Design research

Recall returns the average of everything seen, and the average is the
definition of generic. So for anything with real prior art, look it up —
in stages, because each stage answers a question the previous one cannot.

**Find a site → find its rebuild → read how it works → build the smallest
version → name what you took.**

**Ask before a deep search** — it costs time, and the person may already
know what they want. Except after a complaint: when they have just said the
work looks generic, guessing again from memory is the mistake.

## Stage 1 — find a site that already solved it

Where to look, by what you are after:

- **Awwwards** (awwwards.com) — Site of the Day, and collections by
  category. The default starting point: every entry names the studio, and
  the studio name is the query for everything after this.
- **The FWA** (thefwa.com) — the heaviest interactive and WebGL work.
- **Godly** (godly.website) — tighter curation than the awards, filterable
  by the kind of motion.
- **SiteInspire** (siteinspire.com) — filters by style, type and subject,
  which is the fastest route from a brief to a shortlist.
- **Minimal Gallery** (minimal.gallery) — hierarchy and whitespace rather
  than effects.
- **Hoverstat.es** — experimental, essayistic, non-commercial. Go here when
  the brief is "unusual" and the awards all look alike.
- **Codrops** (tympanus.net/codrops) — the exception to everything below:
  the effect *and* its source, explained. Often ends the research at
  stage 1.
- **Mobbin, Refero** — real flows from shipped products. For conventions,
  not for originality.
- **Typewolf, Fonts In Use** — what typeface that is, and what it has been
  used for.
- **Are.na** — user-built channels; the least algorithmic source there is.

**A gallery is a name index, not a picture book.** Fetched as text these
sites are nearly empty — measured on their own homepages, godly.website
returns 133 words, cosmos.so 143, designspells.com 62. So do not try to
*look* at one. Harvest names of sites and studios; that is what it is for.
Curated lists on GitHub (`Evavic44/portfolio-ideas`,
`Arif-un/awesome-portfolio-websites`) are Markdown and read perfectly,
which makes them a better index than the galleries themselves.

## Stage 2 — find somebody's rebuild

Award winners ship no source. People who rebuild them to learn do, and they
say so in the repository description. Search **one name at a time**, quoted:

```
"dennis snellenberg" in:name,description,readme
```

which returns `AliBagheri2079/dennis-snellenberg-portfolio` (185 stars),
whose description names the whole stack: Next.js, GSAP, Lenis, Framer
Motion. Mechanism, libraries and source from one query.

Four rules, each learned from a failed search:

- **One name per query.** OR-ing five site names collapsed the results onto
  fifteen repositories from a single studio and nothing else.
- **Never search the bare word `clone`** — four thousand voice-cloning
  projects. The site's name is a distinctive token; `clone` is not.
- **`topic:awwwards` is for browsing, not finding** — about sixteen repos
  above twenty stars in the whole topic.
- **Sort by stars, filter `pushed:>2025-01-01`.** A rebuild abandoned in
  2021 targets an API that has changed since.

If the plain name misses, try `<name>-clone`, `<name>-replica`,
`<name>-portfolio`, and the topics `awwwards-inspired` / `awwwards-replica`.

**Search the studio as an organisation too.** Studios open-source the
mechanics they won with: `Cuberto/mouse-follower` (821 stars) is the cursor
effect from their own award sites — the original, maintained and licensed,
which no rebuild is.

When the technique is known but the site is not, search the code instead of
the name, because an API call is a distinctive token:

```
ScrollTrigger.create pin scrub language:javascript path:src
```

— 137 real implementations of a pinned, scrubbed scroll sequence.

**Two cautions.** A rebuild is someone's practice project: evidence of *an*
approach, not necessarily the studio's, so check it against the live site.
And a repository with no LICENSE file is all rights reserved by default,
whatever "clone" in the title implies — read it to understand, do not paste
it.

## Stage 3 — read how it actually works

When no rebuild exists, the live site is the primary source, and unlike a
screenshot it is machine-readable. Its markup names the stack:

```bash
curl -sL -A "Mozilla/5.0" "$URL" | grep -oiE \
 '(gsap|scrolltrigger|lenis|locomotive[.-]?scroll|three(\.min)?\.js|barba|swiper|splitting|matter\.js|pixi|curtains|tailwind|next/static|nuxt|_astro|sveltekit|webflow|framer)' \
 | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
```

**A hit is strong evidence; a miss proves nothing** — bundlers rename
everything. Verified: locomotive.ca reports `locomotive-scroll`,
basement.studio reports `next` and `gsap`, lusion.co reports only `_astro`
despite being WebGL throughout.

Once the library is known, its own docs and showcase describe the mechanism
in words — far better reading than minified source.

With a browser, take the numbers: computed type scale, spacing steps,
colour tokens, breakpoints, animation durations. That is a design system
handed over in figures, and no screenshot carries it.

## Stage 4 — build the smallest version

Reading is not understanding. Strip the mechanic to one element on a blank
page and get it moving right — one card that lifts, one line that reveals,
one panel that pins. Then put it beside the original and look at what is
still wrong. It is almost always the timing.

**If you cannot describe it in words without the source open, you have not
got it yet.** Which brings us to the part that decides whether any of this
was worth doing.

## Take the shapes, not the palette

The palette is the first thing anyone extracts and the last thing that
transfers. An eyedropper gets it in seconds — which is exactly why it is
the wrong souvenir. Those colours were chosen against their photography,
their logo, their density and their amount of empty space. On different
material they read as a costume, and everyone can tell, because the
original is one search away.

What actually makes the reference good is harder to see and travels
intact:

- **Composition** — where things sit and what they align to. How much of
  the screen is empty, and *where* the emptiness is. Centred and calm, or
  off-axis and tense. How many things are on screen at once. The size ratio
  between the biggest and smallest element: scale contrast is usually where
  "expensive" comes from.
- **Shape language** — the vocabulary of forms the page repeats. Hard
  corners or soft. Rectangles, circles, or type as the only shape. Images
  cropped into shapes or bled to the edge. Edges drawn with a hairline, or
  not drawn at all. A page reads as designed when its shapes agree with
  each other, not when they are unusual.
- **Rhythm** — the pacing down the page. How far you scroll between events,
  whether density alternates, where it lets you breathe. A screenshot
  cannot show this at all, which is why it is the most commonly missed
  thing in the room.
- **Motion** — what moves, triggered by what, over what distance, for how
  long, on what easing, staggered by how much; what the rest of the page
  does meanwhile; and how it ends, settling or snapping. **Take the
  numbers.** The same animation at 200ms and at 600ms is two different
  products.
- **Type as material** — whether type is the content or the artwork; the
  ratio between display and body size; set tight and heavy, or wide and
  quiet.
- **The register** — say out loud how it feels: quiet, loud, expensive,
  cheap, playful, severe, clinical. Then name which of the five things
  above produce that feeling. "It feels premium" is not a finding. "The
  display type is eight times the body size, everything hangs off one
  axis, and nothing animates faster than 600ms" is a finding, and it can
  be built.

Name those six and you can build something in the same spirit that shares
no pixels with the reference. Bring back only hex codes and you have a
costume.

One nuance on colour: the *structure* travels even though the hues do not.
How many colours there are, how they are distributed — one accent on five
percent of the page — and how far apart they are in value. Take that. Leave
the hues with the brand they belong to.

## What never travels

Their copy, photography, illustration, icons and fonts — licensed work, and
usually the brand itself. Code from a repository with no licence. And the
habits that come attached to award sites: scroll-jacking, a loader that
exists to delay, motion on every element. Those are showreel conventions,
and a page built to be read is not a showreel.

Also leave the stack. An award site runs on something this project probably
does not have — do not add GSAP, Lenis, three.js or a framework to
reproduce one effect without asking. A dependency is the person's call.

## Judge the source before you trust it

| Kind | What it is worth |
|---|---|
| **Juried award** (Awwwards, FWA, CSSDA, D&AD) | A real shipped site a jury argued about. Strongest signal. |
| **Studio's own repository** | The original mechanic, maintained and licensed. Best possible outcome. |
| **A rebuild repository** | Someone's reading of the mechanic. Verify against the live site. |
| **Curated gallery** (Godly, SiteInspire) | One editor's taste, but real sites. |
| **Product pattern library** (Mobbin, Refero) | Real flows from shipped products. Best for conventions, worst for originality. |
| **Research** (NN/g, Baymard, GOV.UK Design System) | Evidence with numbers. Outranks taste when they disagree. |
| **Mood boards** (Are.na, Cosmos, Savee, Pinterest) | Deep and strange, stripped of provenance. A start, never proof. |
| **Dribbble / Behance shots** | A drawing of an interface: no real content, no empty state, often never built. Take mood; never layout, density or feasibility. |

Before adopting a pattern that merely looks current, search its name with
`usability` or `problems` — the failure modes are usually documented.

## Report back with three, not one

A finding is **the link, what to take from it in the terms above, and the
cost** — the dependency, the work, the thing it breaks. Give three, ranked,
and say which you would pick and why. One reference is a decision made on
the person's behalf without telling them there were alternatives.

Then say what you searched and did not find. An empty search is a result:
say so and ask, rather than quietly falling back on memory.

## Etiquette

Fetch pages, do not crawl. Land-book, Lapa Ninja, CodePen, Behance and
Screenlane answer an automated request with 403, and SiteInspire
rate-limits — that is their answer, so reach the specific page through a
search engine rather than retrying harder.
