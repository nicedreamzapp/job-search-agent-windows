# 🎬 Video Production Plan — `job-search-agent` README Demo

This is the full production brief for the 58-second README embed video. The animated `demo.svg` (a self-contained SMIL loop) is the primary deliverable; the narration script is timed beat-for-beat to its SMIL events (see `SYNC_TABLE.md`). The video is intentionally short, factual, and built for retention: README-embedded videos only get watched in full if they finish before the viewer's "is this worth it?" instinct kicks in (~75 seconds in our testing).

---

## 1. Video Concept

**"The 58-second job-hunt walkthrough."**

Open on a fresh terminal prompt. The user runs `python3 jobscout.py --verbose`. Connectors fetch from five public ATS boards. Filter culls 46 misses. Local LLM scores the 47 survivors. Screen clears. Summary, top three matches, deep links, report-written. Idle cursor blinks. End.

The whole video answers exactly one question: **"What does it feel like to use this every morning?"**

No feature tour. No code walkthrough. No founder talking head. The terminal does the demoing — and the terminal *is* the deliverable, since `demo.svg` ships in the README.

---

## 2. Length Target

**58 seconds** for the README embed (matches the `demo.svg` loop exactly). Hard cap at 90 for any long-cut version.

Rationale: README embeds compete with the reader's "scroll to install instructions" instinct. Published data on GitHub README video retention shows >70% drop-off past 90 seconds. We optimize for full-watch, not for runtime. The 58-second figure is set by the SVG's SMIL loop — narration was tuned to that, not the other way around (see `SYNC_TABLE.md`).

---

## 3. Production Budget Tier

**Flagship-OSS tier — "no expenses spared" within the bounds of a one-person production.**

| Line item | Recommended pick | Why |
|---|---|---|
| **Editor** | [Descript](https://descript.com) **or** [Submagic](https://submagic.co) | Auto-captions + B-roll cuts; both ship word-by-word highlight captions out of the box |
| **Motion graphics** | Light only — title cards, lower-thirds, one architecture animation | Heavy motion graphics make OSS demos feel like SaaS landing pages |
| **Music** | [Epidemic Sound](https://epidemicsound.com) **or** [Artlist](https://artlist.io) — single ambient electronic track | Sub-license clean, won't trip YouTube ContentID |
| **Voice-over** | Real human, recorded on a decent USB condenser (Shure MV7, RØDE NT-USB, or similar) | Synth VO reads as "AI slop" in 2026; defeats the purpose |
| **Color** | Light LUT pass in DaVinci Resolve (free) or Descript's built-in | Pulls cohesion across the screen-recording / camera B-roll seams |
| **Captions** | Auto-generate → hand-correct every word | Watch-time-multiplier; ~85% of LinkedIn/X views are sound-off |
| **Thumbnail** | One static frame, white text on dark, no clickbait arrows | OSS audience punishes clickbait |

Estimated total: **$30–60 in stock-music subs + 4–6 hours of editing time.** No agency, no studio, no actors.

---

## 4. Shot List (in order)

There are **two deliverables** that share one narration:

- **(A) The README-embedded `demo.svg`** — a self-contained 58-second SMIL loop of the terminal session. This is the primary deliverable and the file every visitor will see first. The shot breakdown for the SVG itself is in `demo-script.md`; the narration is timed to the SVG's SMIL events in `SYNC_TABLE.md`.
- **(B) An optional 58-second long-cut for YouTube / X / LinkedIn** — wraps the SVG with a real cold-open + CTA card. Shot list below describes this version. If you only ship (A), skip the table and use the narration as captions over the SVG.

| # | Shot | Duration | What's on screen | Notes |
|---|---|---|---|---|
| **1** | Cold open | 0:00 – 0:02.5 | Title card fades in over a dark frame: **"Wake up to a hand-curated list of jobs."** Then the terminal window appears with the prompt visible and the cursor blinking. | Match the SVG's first 2.5 s — let the command type itself in. No VO yet. |
| **2** | Terminal: fetch | 0:02.8 – 0:13.0 | Full-screen terminal (the `demo.svg` view at 1× zoom). Banner draws, then the five `[fetch][…]` lines stream in 1.5 s apart, ending with "93 roles total · 5/5 boards ok." | Use the SVG directly — re-encoding the SMIL frames to mp4 with `rsvg-convert` + `ffmpeg` keeps the typography pixel-perfect. |
| **3** | Terminal: filter + score | 0:13.3 – 0:31.0 | Filter lines, then the score stream (8 visible role lines + a `...` + `47/47 complete`). | This is the longest sustained beat — the VO carries it. Don't cut away. |
| **4** | Terminal: summary + top 3 | 0:32.0 – 0:48.0 | Screen clears, summary box draws ("47 roles scored · 5 high-fit · 12 worth-considering"), then `top 3 matches:` and the three roles unspool one at a time. | The clear at 0:32 is the only hard visual transition in the loop. Mix the music so a soft cymbal swell sits underneath it. |
| **5** | Terminal: report + idle prompt | 0:48.3 – 0:58.0 | `report written: out/2026-05-21-jobscout.md` appears, then a fresh prompt + blinking cursor holds while the closing VO lands. | This is also the CTA hold — overlay the GitHub URL as a lower-third for the long-cut version. SVG version stays clean. |

**Total: 58 seconds — matches the `demo.svg` loop exactly.** If you need a hard cap at 60 s for a platform that requires it, add a 2-second outro card after the loop ends. Do **not** stretch the SVG — its SMIL timing is the single source of truth.

---

## 5. Narration Script (word-for-word)

**Target: 128 words at ~145 wpm = 53 s of speech + ~5 s of inter-line breaths = 58 s, matching the `demo.svg` loop exactly.** Read warm, factual, slightly under-energy. Do NOT read it like a SaaS ad.

Every line below is timed to coincide with a specific visual event in `demo.svg`. The sync map is in `SYNC_TABLE.md`.

> *(0:00 – music in, no VO yet — cursor blinks, command types in over 2.5 s)*
>
> *(0:02.8, as the banner appears and the first fetch line lands at 0:04.8)*
> **"Every morning the agent wakes up and scans every ATS on your allow-list."**
>
> *(0:06.3, as Modal / Replit / Cohere / Cursor fetch lines stream)*
> **"Ashby, Greenhouse, Lever — no logins, no scraping, just the public boards."**
>
> *(0:13.3, as the filter lines land)*
> **"It filters out the obvious misses — wrong level, wrong location, wrong family."**
>
> *(0:15.3, as the score stream starts)*
> **"Then it scores every survivor against your portfolio, using a local LLM."**
>
> *(0:22.0, scoring continues through line 8/10)*
> **"Your real ships, your real numbers, the version of your story you'd actually tell a hiring manager."**
>
> *(0:32.0, screen clears and the summary box draws)*
> **"Forty-seven roles scored. Five high-fit. Twelve worth a second look."**
>
> *(0:36.3, as "top 3 matches:" prints and matches 1 & 2 unspool)*
> **"Top three matches, ranked, with a one-line why-this-fit and a deep link to the application."**
>
> *(0:43.5, as the third match lands)*
> **"Every hit ships with a custom pitch already drafted, saved as portable markdown."**
>
> *(0:48.3, on the `report written:` line)*
> **"Report written. You stay in the loop on every send."**
>
> *(0:50.0, on the return-to-prompt with blinking cursor; CTA hold)*
> **"Clone it. Edit your credentials. Wake up tomorrow to a better list."**

**Word count: 128. Total VO wall-clock: ~55 s. The remaining ~3 s of cursor-blink hold lets the loop seam breathe. Read once at full pace; the SVG loop is the metronome — VO conforms to it, not the other way around.**

---

## 6. Music Direction

- **Genre:** Ambient electronic. Think early Tycho, Bonobo's quieter cuts, Floating Points' meditative work. **Not** EDM, not corporate-uplift, not LoFi.
- **Energy curve:** Starts quiet. Builds *slightly* through the scoring section (0:15 – 0:31). A soft cymbal swell under the 0:32 screen clear. Plateaus through the top-3 matches. **Never peaks.** This is background score, not foreground.
- **Tempo:** 90–105 BPM. Faster reads as "tech ad," slower reads as "meditation app."
- **License:** Pull from Epidemic Sound or Artlist. Avoid YouTube Audio Library — too many other OSS demos use the same five tracks and it homogenizes the brand.
- **Mix:** -18 LUFS for the music bed, VO sits at -14 LUFS, +4 dB of headroom. Auto-duck the music under the VO if your editor supports it (Descript does this natively).

---

## 7. Captions

- **Auto-generate** with the editor's built-in (Descript / Submagic / CapCut all reliable).
- **Hand-correct** every word. Especially: ATS names (Ashby is often heard as "Ashbee"), "MLX," "Ollama," "Anthropic." A wrong-word caption on a tech demo kills credibility.
- **Style:** Word-by-word highlight (Submagic's default). Active word in accent color, rest in white. Bottom-third placement, never top.
- **Font:** Inter Bold or SF Pro Display Bold. 48-56 pt at 1080p. White with a thin dark drop shadow for legibility on any background.
- **Punctuation:** Drop periods at the ends of lines (cleaner). Keep commas. Question marks if they're rhetorical.

---

## 8. Title Card Font

- **Primary:** **Inter** (free, open-source, neutral, reads as "tech-adjacent" without screaming "I downloaded Helvetica off Dafont").
- **Fallback:** **SF Pro Display** if you're on macOS and want the native feel.
- **Weight:** 600 (Semibold) for the body, 700 (Bold) for emphasis lines.
- **Color:** Pure white (#FFFFFF) on pure black (#000000). No drop shadows on title cards (clean modernist look — drop shadows are for captions on noisy backgrounds, not title cards on clean ones).
- **Kerning:** -2% tracking on body text, -4% on the bold emphasis lines. Slight tightening looks more designed.

---

## 9. B-Roll Suggestions

In rough priority order — pull these if you have extra runtime or a shot doesn't land:

1. **Terminal recordings.** `htop` showing the LLM eating GPU. `tree` of the repo layout. `git log --oneline` showing real commit cadence.
2. **Dashboard close-ups.** Cursor hovering over scores, the tooltip showing the why-this-fit one-liner.
3. **Real ATS pages being scrolled.** Ashby, Greenhouse, Lever — film yourself opening a real job posting on each. Adds credibility that these are real public endpoints, not invented ones.
4. **The credentials.md file open in an editor.** Showing a redacted snippet of "GitHub: 4 OSS repos, 128k+ combined stars" — proves the agent is reading something real.
5. **A `state/pitches/anthropic-mts-agents.md` rendered in Marked or Obsidian.** Shows the output isn't terminal-only; it's portable markdown.
6. **Sunrise time-lapse.** Cuts back to the cold-open mood if you need a breath between shots.

**Don't use:** stock footage of people typing, stock footage of LinkedIn on a phone, stock footage of "happy diverse team in office." Kills the indie-OSS authenticity that's the whole vibe.

---

## 10. Delivery Specs

| Spec | Value |
|---|---|
| **Resolution** | 1920×1080 (1080p) |
| **Codec** | H.264, High profile |
| **Bitrate** | 8–12 Mbps (sweet spot for GitHub README embed file-size limits if you choose to inline it) |
| **Audio** | AAC, stereo, 192 kbps |
| **Frame rate** | 30 fps (or 24 fps if you want a slightly more cinematic feel — pick one and stay consistent) |
| **File size target** | <50 MB for GitHub inline; unlimited for YouTube embed |
| **Format** | `.mp4` |
| **Thumbnail** | 1280×720 PNG, single-frame export from shot 3 (the dashboard close-up) |

---

## 11. Recording Order (production sequence)

You will not shoot this in script order. Shoot in this order to minimize setup re-do:

1. **All terminal shots in one sitting.** Same window, same font, same prompt. Shoot multiple takes of each command for editor flexibility.
2. **All dashboard shots in one sitting.** Same browser window, same zoom level. Pre-populate `state/briefing.md` so you're not waiting on a real morning run mid-take.
3. **Cold open and hand-on-laptop.** Real sunrise if possible, or a tunable LED panel with a 2700K + slight orange gel.
4. **All title cards.** Build them as a single comp in your editor, export as a sequence.
5. **VO last.** Once the picture is locked, you know exactly how long each VO segment can be. Recording VO before picture-lock is the #1 cause of "the VO feels rushed in the final edit."

---

## 12. Post-Production Checklist

- [ ] Picture lock with placeholder VO
- [ ] Record real VO against locked picture
- [ ] Drop in music; auto-duck under VO
- [ ] Generate auto-captions; hand-correct every word
- [ ] Color pass (single LUT, consistent across cuts)
- [ ] Loudness normalize to -14 LUFS integrated
- [ ] Export master (.mp4, 1080p, 12 Mbps)
- [ ] Export 720p compressed version for the README inline
- [ ] Export a 9:16 cut for social (use shots 3, 4, 6, 7 only)
- [ ] Upload to YouTube, set thumbnail, write description with the repo URL in the first line
- [ ] Update the README's `REPLACE_WITH_VIDEO_ID` placeholder with the real ID

---

## 13. Success Metrics (what to watch after launch)

| Metric | Target | Where to check |
|---|---|---|
| README → video click-through rate | >12% | YouTube Studio "Traffic source: External" |
| Average view duration | >45 seconds (75%+) | YouTube Studio Analytics |
| Star velocity in week 1 | >100 stars | GitHub repo insights |
| Like-to-view ratio | >4% | YouTube Studio |
| HN front page | bonus | submit only after the video is up |

If average view duration drops below 30 seconds, the cold open isn't earning the next 55. Re-cut shot 1 and shot 2 — that's almost always where retention dies.

---

**This plan is opinionated on purpose.** Every recommendation here is overridable — but the override should be a deliberate "I disagree because X," not a default-skip. The 60-second video is the highest-leverage marketing asset this project will ever ship. Treat it accordingly.
