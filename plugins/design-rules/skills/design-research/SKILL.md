---
name: design-research
description: >-
  Find out how a design problem has already been solved before inventing an
  answer to it — in juried competitions, curated galleries, product pattern
  libraries, technique write-ups that ship source, and evidence-based UX
  research. Carries a vetted catalogue of where to look
  (`references/sources.md`) and the methods that work for an agent rather
  than a human eye: galleries are name indexes, the awarded site itself is
  the primary source and is machine-readable, and rebuild repositories are
  where the source lives. Load before building any non-trivial interaction,
  motion or layout mechanic; when picking a pattern with obvious prior art;
  when establishing a visual direction; and whenever someone says a design
  looks generic, cheap or AI-made. Triggers on design research, references,
  prior art, inspiration, awwwards, FWA, CSS Design Awards, competition
  winners, case study, "how is this done", "how do other people solve
  this", making-of and teardown, experimental or unusual web design,
  scroll-driven and WebGL effects, interaction and motion patterns, UI
  pattern libraries, type pairing references, and on "make it look less
  generic".
---

# Design research

Recall returns the average of everything seen, and the average is the
definition of generic. So for anything with real prior art, look it up
before inventing it. This skill is the method and the catalogue; the
catalogue is `references/sources.md`, read it when you need a source rather
than up front.

**Ask before running a deep search.** Research costs time, and the person
may already know exactly what they want. What does not need asking: a quick
look when they have just said the work looks generic — that is the one case
where guessing again from memory is the mistake.

## What research is for

- **A mechanic you are about to invent** — a scroll-driven sequence, a drag
  or gesture, a page transition, 3D, physics, hover choreography, anything
  on a canvas.
- **A pattern with heavy prior art** — pricing tables, onboarding, empty
  states, data tables, filtering, multi-step forms. These have been solved,
  measured and written up. Do not re-derive them.
- **A visual direction** at the start of a project, before conventions
  harden into a design system.
- **A complaint.** "Generic", "cheap", "AI-made", "off" — search the
  specific thing being criticised, not the whole category.

## Galleries are name indexes, not sources

This is the part that differs from how a human uses these sites. An
inspiration gallery is a wall of images: fetched as text it is nearly
empty. Measured on the homepages themselves:

| Source | Words of text returned |
|---|---|
| designspells.com | 62 |
| godly.website | 133 |
| cosmos.so | 143 |
| gsap.com/showcase | 354 |
| awwwards.com/websites | ~1,400 — almost all names and authors |
| baymard.com/blog | 1,203 |
| component.gallery/components | 1,729 |
| nngroup.com/articles | 1,838 |

So a gallery gives you **names**, and names are the query for the next
step. Three moves follow, in this order.

### Move 1 — harvest names, then search the name

Pull the site and studio names out of the gallery, then search each with
`case study`, `making of`, `teardown`, `behind the scenes`, or the studio
name plus `process`. The write-up has the text the gallery does not.

### Move 2 — read the awarded site itself

The live site is the primary source, and unlike its screenshot it is
machine-readable. Fetch it and read the stack off the markup:

```bash
curl -sL -A "Mozilla/5.0" "$URL" | grep -oiE \
 '(gsap|scrolltrigger|lenis|locomotive[.-]?scroll|three(\.min)?\.js|barba|swiper|splitting|matter\.js|pixi|curtains|tailwind|next/static|nuxt|_astro|sveltekit|webflow|framer)' \
 | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
```

**A hit is strong evidence; a miss proves nothing** — a bundler renames
everything. Verified on three studio sites: locomotive.ca reports
`locomotive-scroll`, basement.studio reports `next` and `gsap`, and
lusion.co reports only `_astro` despite the work being WebGL throughout.

When you can drive a browser, go further: read the computed type scale,
the spacing steps, the colour tokens and the breakpoints off the real
page. That is a design system handed to you in numbers, and no screenshot
carries it.

### Move 3 — find source you can read

Award winners almost never ship source. These do:

- **Codrops** — every demo is downloadable and the tutorial explains it.
- **The `awwwards` and `awwwards-inspired` GitHub topics** — rebuilds of
  sites that publish nothing, written specifically to reverse-engineer
  them.
- **CodePen** — search the technique, not the site.
- **Library showcases** (GSAP, Motion) — the effect plus the API that made
  it.

## What to take and what to leave

**Take the mechanism.** What moves, triggered by what, over what distance,
for how long, on what easing; what the container does meanwhile; what
happens on touch, and under `prefers-reduced-motion`. Write that down in
words — if you cannot describe it without the source, you have not
understood it yet.

**Leave the implementation.** An award-winning site usually runs on a
stack the project does not have. Do not import GSAP, Lenis, three.js or a
framework to reproduce one effect without asking — a dependency is the
person's call, not yours.

**Never lift** their copy, photography, illustration, icons, fonts or
brand. The mechanism is an idea and ideas travel; the assets are someone's
licensed work.

And leave the habits that come attached: scroll-jacking, a loader that
exists to delay, and motion that fires on every element. Most award
portfolios are showreels, and a page built to be read is not a showreel.

## Judge the source before you trust it

| Kind | What it is worth |
|---|---|
| **Juried award** (Awwwards SOTD, FWA, CSS Design Awards, D&AD) | A real, shipped, working site that a jury argued about. The strongest signal. |
| **Curated gallery** (Godly, SiteInspire, Minimal Gallery) | One editor's taste, but real sites that exist. |
| **Product pattern library** (Mobbin, Refero, Page Flows) | Real flows from shipped products — the best source for conventions, the worst for originality. |
| **Research** (NN/g, Baymard, GOV.UK) | Evidence with numbers behind it. Outranks taste when they disagree. |
| **Mood boards** (Are.na, Cosmos, Savee, Pinterest) | Deep, strange, genuinely useful — and stripped of provenance. Treat an image with no source as a starting point, never as proof something works. |
| **Dribbble / Behance shots** | A drawing of an interface, usually never built, with no real content, no empty state and no error state. Take colour and mood; never take layout, density or feasibility. |

Cross the taste sources with the evidence sources. A pattern that looks
current and tests badly is documented — search the pattern's name together
with `usability` or `problems` before adopting it.

## Report back with three, not one

A finding is: **the link, one line on what to take from it, and the cost.**
Give three, ranked, and say which you would pick and why. One reference is
not research — it is a decision made on the person's behalf without
telling them there were alternatives.

Then say what you searched and what you did not find. If the search turned
up nothing useful, that is a result: say so and ask, rather than quietly
falling back on memory.

## Etiquette

Fetch pages, do not crawl sites — a handful of requests, not a sweep.
Several of these sites answer an automated request with 403 (Land-book,
Lapa Ninja, CodePen, Behance, Webby, Screenlane) or rate-limit it
(SiteInspire); that is their answer, so use a search engine to reach the
specific page instead of retrying harder.

## The catalogue

`references/sources.md` — around sixty sources grouped by what they are
for, each with what it holds and whether it returns anything readable to
an agent. Read it when you need a source; do not paste it into an answer.
