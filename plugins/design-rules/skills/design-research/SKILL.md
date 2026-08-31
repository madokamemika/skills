---
name: design-research
description: >-
  Find how a design has actually been built before inventing an answer, by
  running the pipeline that works for an agent: a gallery or competition
  gives you the NAME of a site, GitHub gives you somebody's open rebuild of
  it, the live site's own markup gives you its stack, and GitHub code search
  gives you the mechanic as real code. Carries the verified query syntax for
  each step and a catalogue of sources in `references/sources.md`. Load
  before building any non-trivial interaction, motion or layout mechanic;
  when picking a pattern with obvious prior art; when establishing a visual
  direction; and whenever someone says a design looks generic, cheap or
  AI-made. Triggers on design research, references, prior art, inspiration,
  awwwards, FWA, CSS Design Awards, competition winners, case study,
  teardown, breakdown, "how is this done", "how did they build that", "find
  a repo that does this", clone or rebuild of a site, experimental web
  design, scroll-driven and WebGL effects, GSAP, Lenis, three.js,
  interaction and motion patterns, UI pattern libraries, type pairing
  references, and on "make it look less generic".
---

# Design research

Recall returns the average of everything seen, and the average is the
definition of generic. So for anything with real prior art, look it up.

The whole method is one pipeline, and each step is a different kind of
source. **A gallery gives you a name. GitHub gives you the code. The live
site gives you the numbers.** Run it in that order.

**Ask before a deep search** — it costs time and the person may already know
what they want. Except after a complaint: when they have just said the work
looks generic, guessing again from memory is the mistake.

## Step 1 — get a name

An inspiration gallery is a wall of images. Fetched as text it is nearly
empty, measured on the homepages themselves:

| Source | Words returned |
|---|---|
| designspells.com | 62 |
| godly.website | 133 |
| cosmos.so | 143 |
| awwwards.com/websites | ~1,400 — almost all names and studios |

So do not try to *look* at a gallery. Harvest **names** — of sites and of
the studios that built them. That is the only thing it is for, and the name
is the query for every step after this.

Two sources return names as plain text, which the galleries do not:

- **The awwwards listing pages** — the names and studios are in the markup
  even though the images are not.
- **Curated lists on GitHub**, which are Markdown and read perfectly:
  `Evavic44/portfolio-ideas` (~6.3k stars), `Arif-un/awesome-portfolio-websites`,
  `mejed-alkoutaini/designer-portfolios`.

## Step 2 — find somebody's rebuild

Award winners ship no source. People who rebuild them to learn do, and they
say so in the repository description. This is the highest-value step in the
pipeline, and most of it is query craft.

**Search one name at a time**, quoted:

```
"dennis snellenberg" in:name,description,readme
```

That returns `AliBagheri2079/dennis-snellenberg-portfolio` (185 stars),
whose description names the entire stack: Next.js, GSAP, Lenis, Framer
Motion, Styled Components. That is the mechanism, the libraries and the
source, from one query.

Four rules, each learned the hard way:

- **One name per query.** OR-ing five site names together collapses the
  results onto whichever org is strongest — a five-name query came back as
  fifteen repositories from Cuberto and nothing else.
- **Never search the bare word `clone`.** It returns four thousand
  voice-cloning repositories. The site's own name is a distinctive token;
  `clone` is not.
- **`topic:awwwards` is for browsing, not for finding.** The whole topic
  holds about sixteen repositories above twenty stars. Useful to see what
  people rebuild; useless for a specific site.
- **Sort by stars, and filter `pushed:>2025-01-01`.** A rebuild abandoned
  in 2021 is written against an API that has since changed.

Naming conventions to try when the plain name misses: `<name>-clone`,
`<name>-replica`, `<name>-portfolio`, and the topics `awwwards-inspired`
and `awwwards-replica`.

**Also search the studio as an org.** Studios that win awards open-source
the mechanics they built to win them — `Cuberto/mouse-follower` (821 stars)
is the cursor effect itself, from the studio whose sites you were admiring.
That is better than any rebuild: it is the original, maintained, and
licensed for use.

**Two cautions.** A rebuild is someone's practice project: it can be
partial, or wrong, and it is evidence of *an* approach, not of the one the
studio took — check it against the live site. And a repository with no
LICENSE file is all rights reserved by default, whatever "clone" in the
title implies. Read it to understand the mechanism; do not paste it.

## Step 3 — read the live site

When no rebuild exists, the site itself is the primary source, and unlike
its screenshot it is machine-readable. Its markup names the stack:

```bash
curl -sL -A "Mozilla/5.0" "$URL" | grep -oiE \
 '(gsap|scrolltrigger|lenis|locomotive[.-]?scroll|three(\.min)?\.js|barba|swiper|splitting|matter\.js|pixi|curtains|tailwind|next/static|nuxt|_astro|sveltekit|webflow|framer)' \
 | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
```

**A hit is strong evidence; a miss proves nothing** — a bundler renames
everything. Verified on three studio sites: locomotive.ca reports
`locomotive-scroll`, basement.studio reports `next` and `gsap`, and
lusion.co reports only `_astro` despite being WebGL throughout.

Once you know the library, its own docs and showcase are the mechanism in
words, and they are far easier to read than minified source.

With a browser, go further: read the computed type scale, spacing steps,
colour tokens and breakpoints off the real page. That is a design system
handed over in numbers, and no screenshot carries it.

## Step 4 — find the mechanic as code

When you know the technique but not the site, search the code instead of
the name — the API call is the distinctive token:

```
ScrollTrigger.create pin scrub language:javascript path:src
```

That returns 137 real implementations of a pinned, scrubbed scroll
sequence. The same shape works for any library: search the function that
only that effect calls, narrowed with `language:` and `path:src`.

## What to take and what to leave

**Take the mechanism.** What moves, triggered by what, over what distance,
for how long, on what easing; what the container does meanwhile; what
happens on touch and under `prefers-reduced-motion`. Write it down in
words — if you cannot describe it without the source open, you have not
understood it.

**Leave the implementation.** An award site runs on a stack this project
probably does not have. Do not add GSAP, Lenis, three.js or a framework to
reproduce one effect without asking: a dependency is the person's call.

**Never lift** copy, photography, illustration, icons, fonts or brand —
and never paste code from an unlicensed repository.

Leave the habits that come attached, too: scroll-jacking, a loader that
exists to delay, motion on every element. Award portfolios are showreels; a
page built to be read is not one.

## Judge the source before you trust it

| Kind | What it is worth |
|---|---|
| **Juried award** (Awwwards SOTD, FWA, CSSDA, D&AD) | A real shipped site a jury argued about. Strongest signal. |
| **Studio's own repository** | The original mechanic, maintained and licensed. Best possible outcome. |
| **A rebuild repository** | Someone's reading of the mechanic. Verify against the live site. |
| **Curated gallery** (Godly, SiteInspire, Minimal Gallery) | One editor's taste, but real sites. |
| **Product pattern library** (Mobbin, Refero) | Real flows from shipped products. Best for conventions, worst for originality. |
| **Research** (NN/g, Baymard, GOV.UK) | Evidence with numbers. Outranks taste when they disagree. |
| **Mood boards** (Are.na, Cosmos, Savee, Pinterest) | Deep and strange, and stripped of provenance. A starting point, never proof. |
| **Dribbble / Behance shots** | A drawing of an interface: no real content, no empty state, often never built. Take colour and mood; never layout, density or feasibility. |

Before adopting a pattern that merely looks current, search its name with
`usability` or `problems`. The failure modes are usually documented.

## Report back with three, not one

A finding is **the link, one line on what to take, and the cost** — the
dependency, the work, the thing it breaks. Give three, ranked, and say
which you would pick and why. One reference is a decision made on the
person's behalf without telling them there were alternatives.

Then say what you searched and what you did not find. An empty search is a
result: say so and ask, rather than quietly falling back on memory.

## Etiquette

Fetch pages, do not crawl. Several sources answer an automated request with
403 (Land-book, Lapa Ninja, CodePen, Behance, Webby, Screenlane) or
rate-limit it (SiteInspire) — that is their answer, so reach the specific
page through a search engine instead of retrying harder.

## The catalogue

`references/sources.md` — around eighty sources grouped by what each is
for, each tagged with what an automated fetch actually returns. Read it
when you need a source; do not paste it into an answer.
