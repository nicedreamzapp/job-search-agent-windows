# SYNC_TABLE — demo.svg ↔ VIDEO_PLAN.md narration

Beat-by-beat alignment between the **60-second**, **7-scene** SMIL animation in `demo.svg`
and the narration in `VIDEO_PLAN.md` §5.

**Loop length:** 60.0 s (SVG master loop, `<animate id="loop" ... dur="60s">`).
**Narration target:** ~140 words at 145 wpm ≈ 58 s of speech + ~2 s of inter-scene breaths = 60 s.

---

## Scene map (timestamps drive the SMIL `begin=` attributes)

| #  | Scene                | t (s)        | Visual summary                                                                                  |
| -- | -------------------- | ------------ | ----------------------------------------------------------------------------------------------- |
| 1  | Cold open            | 0.0 – 3.0    | Wordmark `job-search-agent` letter-stagger fade-in, accent underline sweeps, tagline pulses, fades. |
| 2  | Terminal kickoff     | 3.0 – 12.0   | Terminal window with traffic-light buttons. Prompt + `$ python3 jobscout.py --verbose` types in. Five `[boot]` lines slide in from below. Progress bar fills to "connecting to market…". |
| 3  | Fetch dashboard      | 12.0 – 22.0  | Diagonal wipe. 2×3 grid of company cards (ANTHROPIC 390, MODAL 31, REPLIT 80, COHERE 131, CURSOR 89, STRIPE 479). Counters tick to target. Progress bars fill staggered. Footer total: 1,200 across 6 boards in 2.4s. |
| 4  | Filter pipeline      | 22.0 – 30.0  | Vertical wipe. Three pipeline stages — "Drop junior/intern" 6,006 → 5,820, "Drop already-applied" 5,820 → 312, "Score ≥ 7" 312 → 47. Rejection labels fly off-screen left. Footer: "5,959 dropped · 47 remain". |
| 5  | Scoring engine       | 30.0 – 42.0  | Radial wipe. Three emerald score bars fill staggered with ticking numbers: Modal Labs FDE-ML → **9.2**, Anthropic Solutions Architect → **8.9**, Replit Senior PM → **8.6**. Pulsing "scoring…" indicator. Distribution footer: 5 high-fit · 12 worth-considering · 30 below. |
| 6  | Card reveal          | 42.0 – 52.0  | Slide-up wipe. Polished card for Modal Labs FDE-ML — company, location, $180K–$250K comp band, stack tags, deep link, AI pitch typewrites first two lines then fades in bullets. **MATCH SCORE 9.2** badge bounces in top-right. |
| 7  | Call to action       | 52.0 – 60.0  | Fade to near-black. Logo glyph ("j" in rounded square) scales in. Wordmark + tagline "Wake up to the right roles." Repo URL pill `github.com/USER/job-search-agent` with soft pulse. Footer hint: "MIT licensed · runs locally · no cloud dependencies". Holds until loop reseats at 60.0s. |

---

## Narration-to-scene sync

| Beat | t (s)       | Narration line (suggested)                                                                                  | Lands on                                            |
| ---- | ----------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 0    | 0.0 – 2.6   | *(music in, no VO — wordmark assembles)*                                                                    | Scene 1 letter-stagger                              |
| 1    | 3.5 – 7.5   | "Every morning the agent wakes up — no logins, no scraping, just the public boards."                        | Scene 2 `$ python3 jobscout.py --verbose` + first `[boot]` lines |
| 2    | 8.0 – 11.5  | "Credentials load. Connectors open. The market scan starts."                                                | Scene 2 progress-bar fill                           |
| 3    | 12.5 – 17.5 | "Twelve hundred open roles across six public AI companies — in two and a half seconds."                     | Scene 3 cards lighting up + counters ticking        |
| 4    | 18.0 – 21.5 | "Ashby, Greenhouse, Lever. All six boards, one pipeline."                                                   | Scene 3 footer total                                |
| 5    | 22.5 – 26.5 | "Then the filter pipeline kills the obvious misses — wrong level, already applied, score below seven."      | Scene 4 stages 1 → 2 → 3 + rejection icons flying off |
| 6    | 27.0 – 29.5 | "Six thousand candidates become forty-seven."                                                               | Scene 4 footer "47 remain"                          |
| 7    | 30.5 – 35.5 | "A local LLM scores every survivor against your portfolio — your real ships, your real numbers."           | Scene 5 bars 1, 2, 3 filling                        |
| 8    | 36.0 – 41.0 | "Five high-fit. Twelve worth a second look. Top three sorted and ready."                                    | Scene 5 distribution tally                          |
| 9    | 42.5 – 47.5 | "The number-one match: a Forward Deployed ML role at Modal. Comp, stack, deep link, and a 200-word pitch — pre-written." | Scene 6 card materializes, badge bounces in       |
| 10   | 48.0 – 51.5 | "Saved to portable markdown. Two more matches already in your inbox."                                       | Scene 6 footer "Report saved…"                      |
| 11   | 52.5 – 57.5 | "Clone it. Edit your credentials. Wake up to the right roles."                                              | Scene 7 logo + tagline + repo URL                   |
| 12   | 57.5 – 60.0 | *(hold on CTA pill, soft pulse — viewer reads the URL — loop reseats)*                                      | Scene 7 hold                                        |

---

## Production technique reference (which SMIL primitive does what)

| Effect                         | SMIL primitive                                                                                                                    |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Letter-by-letter fade-in       | Per-`<tspan>` `<animate attributeName="opacity" to="1" begin="<offset>" dur="0.3s" fill="freeze"/>`                               |
| Counter ticker (0 → N)         | Sequence of `<tspan>` elements with `<animate to="1"/>` then `<animate to="0"/>` 50-100ms apart                                   |
| Progress bar / score bar fill  | `<animate attributeName="width" from="0" to="<target>" calcMode="spline" keySplines="0.2 0.8 0.2 1">`                             |
| Slide-in-from-below            | `<animateTransform type="translate" from="0 16" to="0 0">` with matching opacity 0→1                                              |
| Wipe transitions               | `<rect>` overlay + `<animateTransform type="translate">` from full-cover to off-screen                                            |
| Radial wipe                    | `<circle>` with `<animate attributeName="r" from="0" to="1100">` + fade to 0 at end                                               |
| Badge "pop" entry              | `<animateTransform type="scale" from="0.6" to="1" keySplines="0.2 1.6 0.4 1">` (overshoot easing)                                 |
| Soft pulse on CTA              | `<animate attributeName="opacity" values="0.08;0.2;0.08" dur="2.2s" repeatCount="indefinite"/>`                                   |
| Master loop driver             | Invisible `<rect>` with `<animate id="loop" dur="60s" begin="0s;loop.end" repeatCount="indefinite"/>` — every other scene references `loop.end+<offset>` to restart cleanly. |

---

## Drift remediation log

- **2026-05-21:** Rewritten from 58-second single-scene terminal loop to 60-second, 7-scene multi-act animation. ViewBox upgraded from 820×540 to 1280×720. New scenes: cold open, terminal kickoff, fetch dashboard, filter pipeline, scoring engine, card reveal, CTA. SMIL timings serve as the source of truth; narration in `VIDEO_PLAN.md` §5 must be re-recorded to match the table above (the old terminal-only narration no longer fits the visual arc).
- **Prior (2026-04):** Original 58 s narration was tuned to the single-terminal-scene SVG. That table is preserved in git history for reference but is no longer accurate.
