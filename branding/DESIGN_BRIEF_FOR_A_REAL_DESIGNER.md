# Design Brief — for a real designer

**Read this first.** The SVGs in this folder are placeholders, hand-coded by an AI as a starting point. They are intentional and shippable as a v0 — they will look reasonable in a GitHub README, in a browser tab, and on an OG card. But they are not a *crafted* identity. If `job-search-agent` grows beyond the first few hundred stars, hire a real designer and hand them this brief.

---

## The project, in 90 seconds

`job-search-agent` is an open-source local-first agent. Every morning it scrapes job boards, scores each new listing against the operator's full credentials (resume + writing samples + GitHub + side projects), and surfaces a ranked shortlist. The audience is the technical operator — staff/principal engineers, founders between gigs, indie builders who are quietly looking. They live in the terminal and on GitHub.

Adjacent reference points: Linear, Vercel, Modal, Resend, the GitHub CLI. Not adjacent: LinkedIn, Indeed, ZipRecruiter, Notion's marketing pages.

## The concept the placeholder uses

A **radar sweep** (three arcs ascending from a single origin pin) with a **chevron arrow** pointing up and to the right out of the largest arc. The radar represents continuous scanning; the chevron represents scoring and prioritizing. The wordmark sits to the right, set in JetBrains Mono 600 with tight letter-spacing, reinforcing "this is a developer tool, not a brand."

You don't have to keep this concept. Other concepts that fit the brief equally well:

- A magnifying glass over a sparkline / chart line (literal but clean if executed well).
- An upward arrow growing out of a search box / `find` input.
- A stylized agent loop — a circular arrow with a single marked node, suggesting "scans, scores, repeats."
- A minimal terminal cursor next to a tally or score badge.

Whatever the concept, it should be readable at 16px (favicon), at 32px (browser tab), and at 1000px (social card), without modification.

## Must-haves

1. **Works in monochrome.** The primary mark must read clearly as a single-color shape on white *and* on a near-black background, no gradients, no drop shadows.
2. **Square icon + horizontal lockup from one mark.** The same shape powers the favicon, the GitHub avatar, and the wordmark lockup. No separate "icon-only" redesign — just a clean crop.
3. **Geometric, hand-buildable in SVG.** A junior contributor should be able to open the SVG, change a stroke width, and not destroy the design.
4. **Pairs with JetBrains Mono.** The wordmark is set in mono. The mark should not fight against that — i.e. no overly organic curves, no whimsical mascot.
5. **Two-color variant exists.** Mostly neutral with one decisive accent hit, currently `#10B981`. The designer can re-propose the accent if they have a stronger argument.

## Must-avoids

- Anything that looks like a generic "AI" logo (gradient blob, abstract orb, particle swarm, neural-network-style nodes). Reads as 2023 AI startup, ages badly.
- Mascots. No owl, no robot, no fox, no chameleon. Operator audience does not want a friend; they want a tool.
- Custom hand-drawn type. The wordmark should remain typesettable so it survives README updates and translation.
- More than one decisive color. The brand is neutral + one accent, full stop.
- Trendy gimmicks: chromatic aberration, "memphis style," brutalist mismatched typefaces, low-poly 3D renders.

## Deliverables to ask for

1. Primary mark in monochrome (SVG, single color via `currentColor`).
2. Wordmark lockup, horizontal (SVG).
3. Wordmark lockup, stacked / vertical (SVG) — currently missing from this kit; ask for it.
4. Favicon at 16x16, 32x32, 48x48 (SVG + ICO).
5. Social card template at 1200x630 (SVG with editable text layer, plus an exported PNG).
6. README banner at ~1280x320 (SVG + PNG).
7. Animated logo (Lottie or short MP4 ≤ 2 sec) — radar sweep loops once on hover. Optional but nice.
8. Updated `COLORS.md` if they want to revise the accent or add tints/shades.
9. Updated `TYPOGRAPHY.md` if they recommend a different open-source pair (must remain open-source and self-hostable).
10. A `brand-source.fig` Figma file with everything organized, so the next designer doesn't have to start over.

## Budget guidance

Match the budget to how seriously the project takes itself. Honest ranges:

| Tier | Where | What you'll get | When it fits |
|---|---|---|---|
| **$50 – $300** | Fiverr / Upwork | One pass at the mark. Iteration is paid extra. Quality varies wildly — vet portfolios hard. | Hobby project, weekend repo, never going to leave GitHub. |
| **$500 – $2,000** | Dribbble / Twitter freelancers | A capable solo designer who'll deliver the full deliverable list above. Two or three rounds of revision. Decent thinking, but won't push back on the brief. | Repo with traction, planning to launch on HN, sub-1K stars. |
| **$3,000 – $8,000** | Established freelance designer with a verifiable book | Strategic input, real concept exploration, motion, a Figma source file you can hand to the next designer in two years. Will push back on the brief where it's wrong. | Repo with thousands of stars, paid hosted version on the roadmap, going to outlast you. |
| **$15,000+** | Branding agency / studio (Pentagram-lite tier) | Full identity system: marks, motion, typography licensing, voice doc, illustration library, swag-ready files, brand-applied screenshots. Months of work, sometimes a research phase. | This is now a funded company and the OSS repo is the marketing surface. |

For most OSS projects, **$500–$2,000** is the right number. Below that, you're rolling dice; above that, you're paying for strategy you can't yet use.

## How to give the designer this brief

Send them, in order:
1. This file (`DESIGN_BRIEF_FOR_A_REAL_DESIGNER.md`).
2. `BRAND_GUIDE.md` — for voice, since the visual identity should reinforce it.
3. `COLORS.md` and `TYPOGRAPHY.md` — as starting points to push back on, not gospel.
4. The current placeholder SVGs in this folder — so they understand the v0 they're replacing.
5. A link to the live repo and a paragraph about who the audience is.

Then get out of their way.
