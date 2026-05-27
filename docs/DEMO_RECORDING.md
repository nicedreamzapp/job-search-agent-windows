# 🎥 Record Your Own Demo (on your own machine)

A step-by-step guide for recording a polished, README-embeddable demo of `job-search-agent` using **free Mac tools** (built-in Screen Recording, QuickTime) — with optional upgrade paths if you want to spend a little.

This guide tracks the shot list in [`VIDEO_PLAN.md`](VIDEO_PLAN.md). If you want the full production plan, read that first. This document is the **"open it and do it"** version.

---

## 1. Tools You'll Use (Free First)

### Built-in (free, no installs)

| Tool | What it does | How to launch |
|---|---|---|
| **macOS Screen Recording** | Captures the whole screen, a window, or a region. Best for short, simple captures. | `Cmd + Shift + 5` |
| **QuickTime Player** | Same capture engine, but also records your iPhone if you plug it in. Useful for mobile-perspective shots. | Applications → QuickTime Player → File → New Screen Recording |
| **Photo Booth** | Quick & dirty for talking-head intro/outro if you change your mind and want to be on camera. | Applications → Photo Booth |
| **iMovie** | Free non-linear editor. Enough for cuts, captions, music, and a single export. | Applications → iMovie |

### Optional (paid, much faster workflow)

| Tool | Cost | Why you'd pay |
|---|---|---|
| **Descript** | $15/mo | Auto-captions, word-by-word transcript editing, AI voice cleanup, B-roll cut suggestions |
| **Submagic** | $16/mo | Best-in-class word-by-word highlight captions, fastest social-cut workflow |
| **CapCut Pro** | $10/mo | Free tier is generous; Pro unlocks longer exports + better LUTs |
| **DaVinci Resolve** | Free (Studio $295 one-time) | Hollywood-grade color + audio; overkill for a 60-second demo but worth the install |

**Recommendation for a first-time recording:** start with Screen Recording + iMovie. If you finish the cut and the captions feel like the weak link, upgrade to Descript or Submagic for the next take.

---

## 2. Pre-Flight Setup

Do all of this **before you press record**. Re-shoots cost more than setup.

### 2.1 Clean your desktop

```bash
# Hide all desktop icons
defaults write com.apple.finder CreateDesktop -bool false && killall Finder

# (When you're done recording, turn icons back on:)
# defaults write com.apple.finder CreateDesktop -bool true && killall Finder
```

### 2.2 Set up a clean terminal

- **Font:** Menlo or JetBrains Mono, **size 18+ pt minimum** (24 pt looks better for 1080p screen recording).
- **Color scheme:** Solarized Dark, Dracula, or pure black background. Avoid light themes — they wash out in re-encoding.
- **Window size:** Full-screen, or at least 1600×900. Smaller windows look cramped at 1080p.
- **Prompt:** Strip your prompt down. A noisy `oh-my-zsh` prompt with git status + virtualenv + emoji eats screen real estate. Just `$ ` is fine for the demo.

```bash
# Temporary minimal prompt for recording
export PS1='$ '
```

### 2.3 Set up a clean browser

- **Use Brave or Chrome in Guest Mode** — no extensions, no bookmark bar, no tab history bleed-through.
- **One tab only.** Open it to the dashboard / briefing page you'll be demoing.
- **Zoom level:** `Cmd + 0` (reset) then `Cmd + +` two or three times. Bigger text reads better at 1080p.
- **Hide the bookmarks bar:** `Cmd + Shift + B`.

### 2.4 Notifications off

```bash
# Enable Do Not Disturb
# System Settings → Focus → Do Not Disturb → Turn On
```

Slack, iMessage, Mail, calendar reminders — all of them will pop into your screen recording if you don't kill them now.

### 2.5 Pre-populate the state directory

You do not want to wait on a real LLM run mid-take. Run the agent once **before** you start recording, so `state/briefing.md` and `state/pitches/` are already populated with real, recent output.

```bash
python3 jobscout.py --verbose
```

Then, when you record shot 4 (the terminal command), you can run it again — but the dashboard in shot 3 already shows real data.

### 2.6 Resolution

Run your display at 1920×1080 **scaled to look like 1440×900** (System Settings → Displays → Scaled → "Larger Text"). This gives the recording crisp 1080p output without the text being microscopic.

---

## 3. The 6-Shot Recording Script

This matches the storyboard in [`VIDEO_PLAN.md`](VIDEO_PLAN.md). Run through the list in order. Each shot has the exact command/action to perform.

---

### 🎬 Shot 1 — Cold Open (4 seconds)

**What's on screen:** A closed/sleeping laptop on a desk. Sunrise light if you can get it.

**How to record:** You'll shoot this with your **iPhone**, not screen recording. Set the phone on a tripod or prop it against a coffee mug. Frame: laptop in lower third, window/sunrise in upper two-thirds. Record 8–10 seconds (you'll trim to 4 in the edit).

**Tip:** If you don't have real sunrise, a desk lamp with a warm bulb (2700K) angled across the laptop lid fakes it well enough at 1080p.

---

### 🎬 Shot 2 — Wake the Laptop (5 seconds)

**What's on screen:** Hand enters frame, opens the laptop, dashboard is already open and rendered.

**How to record:** Continuation of shot 1, iPhone still rolling. Open the laptop with one hand. The dashboard must already be the foreground window — open it *before* you close the lid for the cold open shot.

**Tip:** This shot benefits from **two takes pieced together**: (a) iPhone shot of the hand opening the laptop, (b) screen recording of the dashboard rendering. Cut between them at the moment the screen lights up. Editors call this a "match cut."

---

### 🎬 Shot 3 — Click Into Top Role (13 seconds)

**What's on screen:** Browser at the dashboard. Cursor moves smoothly to the top role, clicks it, the auto-drafted pitch fills the screen with a slow scroll.

**How to record:**

```
1. Cmd + Shift + 5
2. Choose "Record Selected Portion"
3. Drag the selection to cover just the browser window (not the menu bar, not the dock)
4. Click "Record"
5. Move the cursor deliberately (slow is faster — fast cursor movement looks panicked on recording)
6. Click the top role
7. Slow-scroll through the pitch markdown (use trackpad two-finger scroll, never page-down — page-down jumps are jarring)
8. Cmd + Shift + 5 → Stop, or hit the stop button in the menu bar
```

**Tip:** Move the cursor like you're showing a grandparent. 30% of "normal" speed. It reads as confident, not slow.

---

### 🎬 Shot 4 — Terminal Run (16 seconds)

**What's on screen:** Full-screen terminal. Command `python3 jobscout.py --verbose` runs, output streams.

**How to record:**

```
1. Switch to your terminal window
2. Clear the screen: clear
3. Cmd + Shift + 5 → Record Selected Portion → drag selection over the terminal
4. Click Record
5. Type the command at a deliberate (not blazing) pace:
     python3 jobscout.py --verbose
6. Press Enter
7. Let the real output stream — Scanning Anthropic... 14 roles, Scanning Modal... 6 roles, filter line, scoring line, "🟢 92/100 — Anthropic"
8. Stop recording 1 second after the last line lands
```

**Tip:** If your real run takes longer than 16 seconds, speed up the middle of the clip 2x in your editor. Keep the first 3 seconds (command typing) and the last 3 seconds (final score line) at real speed — those are the moments the viewer reads.

---

### 🎬 Shot 5 — Architecture Diagram (10 seconds)

**What's on screen:** The ASCII architecture diagram from the README, animated in piece by piece.

**How to record:** This is **not** a screen recording — build it in your editor.

**Option A (free, iMovie):** Screenshot each stage of the diagram (connectors only, then connectors + filter, then connectors + filter + scorer, then full diagram). Drop the 4 screenshots into iMovie with 2.5-second durations and a crossfade between each. Done.

**Option B (paid, Descript):** Build the diagram as a single PNG. Drop it in. Use Descript's "draw on" animation to reveal each block in sequence. Polish.

**Option C (Hollywood, After Effects):** Build each block as a separate layer. Slide each one in from its respective direction (connectors from left, filter from center, scorer from right, briefing from bottom). 1-second slide-in per block. 10 seconds total.

---

### 🎬 Shot 6 — Title Cards + Call To Action (12 seconds)

**What's on screen:** Black screen. Three lines appear one at a time. Then the GitHub URL.

**How to record:** Same as shot 5 — build in your editor, don't screen-record.

In iMovie:
1. Add a "Background" clip (the default black one)
2. Add a "Title" overlay → choose the simplest text-only template
3. Type each line ("Local-first.", "No spray-apply.", "No SaaS fees.") as a separate title clip
4. Each clip: 2 seconds, fade in on the first frame
5. Add a final title for the URL: `github.com/USER/job-search-agent` — hold for 6 seconds

---

## 4. Edit It Together

### Free path (iMovie)

1. **Drop everything in order.** Shot 1 → Shot 2 → Shot 3 → Shot 4 → Shot 5 → Shot 6.
2. **Trim each clip** to the durations in the shot list (4s / 5s / 13s / 16s / 10s / 12s = 60s total).
3. **Add a music track.** Pick something ambient and quiet from iMovie's built-in library, or import an Epidemic Sound / Artlist track.
4. **Add the voice-over.** Record with QuickTime (File → New Audio Recording), import the .m4a into iMovie, lay it under the picture. Auto-duck the music in iMovie: select the music clip → click the music icon → enable "Reduce volume of other clips."
5. **Add captions.** iMovie's titles work but are clunky. For better captions, export the cut without captions, then run it through CapCut (free) or Submagic to auto-caption, then re-export.
6. **Export.** File → Share → File → 1080p, High quality.

### Paid path (Descript)

1. **Import all clips** into a single Descript composition.
2. **Record VO directly in Descript** (it has a built-in recorder).
3. **Auto-caption** the whole timeline with one click. Hand-correct every word.
4. **Music**: drop in the track, Descript auto-ducks under VO by default.
5. **Export.** Publish → Video → 1080p, MP4.

---

## 5. Output Specs

Match what's in [`VIDEO_PLAN.md`](VIDEO_PLAN.md) §10:

| Spec | Value |
|---|---|
| **Resolution** | 1920×1080 |
| **Codec** | H.264 |
| **Bitrate** | 8–12 Mbps |
| **Audio** | AAC stereo, 192 kbps |
| **Frame rate** | 30 fps |
| **Format** | `.mp4` |
| **File size** | **<50 MB** if you want to inline-embed in the GitHub README; unlimited if you're hosting on YouTube |

To check your export against the file-size cap:

```bash
ls -lh /path/to/your/export.mp4
# Want to see "M" not "G", and ideally under 50M
```

If your export is too big, drop the bitrate to 6–8 Mbps or shorten the runtime.

---

## 6. Quality Checklist Before You Publish

- [ ] No notification banners visible in any frame
- [ ] No personal data on screen (real names in `credentials.md`, real comp numbers, real GitHub handles you don't want public) — **redact before recording**
- [ ] Captions are hand-corrected (no "Ashbee" instead of "Ashby")
- [ ] Audio levels are consistent — no clipping VO, no music drowning the VO
- [ ] Cursor movements are deliberate, not panicked
- [ ] The final frame (the GitHub URL) holds for at least 5 full seconds
- [ ] You can watch the whole thing back without cringing once

If you cringe at one part — re-cut that part. The viewer will too.

---

## 7. Where to Host

| Host | Pros | Cons |
|---|---|---|
| **YouTube** | Free, great analytics, embeds in README via thumbnail-click pattern | Requires a YouTube channel; you can't autoplay it on the README page |
| **GitHub inline** (commit the .mp4) | Plays inline on the README; no third-party dependency | 100 MB file-size limit; no analytics; no captions baked in unless you encode them |
| **Vimeo** | Cleaner player, no ads | Free tier has upload limits |
| **Self-host on your domain** | Full control | Need to handle CDN, bandwidth, encoding |

**Recommended:** Upload to YouTube for the public version, then *also* commit a compressed `<10 MB` version to `docs/assets/demo.mp4` so the README has a fallback inline player.

---

## 8. After You Publish

1. Update the README's video-link placeholder with the real YouTube ID.
2. Update the thumbnail at `docs/assets/demo-thumbnail.png` with a clean still from shot 3.
3. Tweet/post a 9:16 cut on social — pull shots 3, 4, 6, 7 only, captioned in Submagic.
4. Submit the repo to Hacker News, r/MachineLearning, and r/cscareerquestions **after** the video is up, not before. The video does 80% of the conversion lift.
5. Track the success metrics in [`VIDEO_PLAN.md`](VIDEO_PLAN.md) §13 for the first week. Iterate the cold open if average-view-duration is under 30 seconds.

---

**You're done.** Coffee, push, ship.
