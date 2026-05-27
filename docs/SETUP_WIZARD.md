# Setup Wizard — full guide

This wizard is the friendly front door for everyone who doesn't want to
hand-edit a markdown file. It asks plain-English questions about your work
history, projects, skills, and what you're looking for next — then writes
a clean `credentials.md` to `~/.config/jobscout/credentials.md` for the
scorer to read every morning.

You never have to type a command flag, learn markdown, or open a text
editor. The whole flow is point-and-answer.

---

## Two ways to run it

### 1. Terminal Q&A (CLI mode)

```
python3 jobscout.py setup
```

Asks one question at a time. Auto-saves after every answer so quitting
half-way is fine. Re-run the same command to resume where you left off.

```
  Welcome to job-search-agent.

  I'll ask you a handful of plain-English questions about your work, your
  story, and what kind of job you'd actually want. At the end I'll write
  the answers into a file the agent uses to score real openings every
  morning.

  This usually takes 5-10 minutes. You can quit any time — your
  answers save as you go, so you can resume right where you left off.

  Step 1 of 6 — the basics
  [█░░░░░]

What's your full name?
  example: Alex Rivera
> Alex Rivera

What city are you in?
We'll highlight roles in the same city. Free text — neighborhoods are fine too.
  example: Boise, Idaho
> Boise, Idaho

Are you open to moving for the right job?
If 'maybe', we'll ask which cities are on the table.
  type: yes  /  no  /  maybe
> maybe

Which cities are on the table?
  example: San Francisco, Boston, NYC
> San Francisco, Boston, NYC
```

…and so on. After Step 6 the wizard prints the rendered markdown for
review and asks for confirmation before saving.

### 2. Browser form (web mode)

```
python3 jobscout.py setup --web
```

Opens `http://127.0.0.1:8765/` and serves the wizard as a single HTML
page. Same questions, multi-step form with a progress bar, download
button at the end. Everything runs locally — the Python server only
listens on `127.0.0.1` and never makes outbound calls.

```
  ┌──────────────────────────────────────────────────────────────┐
  │  Set up your job-search-agent                                │
  │  Plain-English questions about your work and what you want.  │
  │                                                              │
  │  [██████░░░░░░░░░░░░░░░░░░░░░░░░░░]   Step 2 of 6            │
  │                                                              │
  │  Your story in one paragraph                                 │
  │                                                              │
  │  Imagine you're meeting a hiring manager at a coffee shop.   │
  │  They ask "so what do you do?" What's your answer? Don't     │
  │  think too hard — write it like you'd actually say it.       │
  │                                                              │
  │  ┌────────────────────────────────────────────────────────┐  │
  │  │                                                        │  │
  │  │                                                        │  │
  │  └────────────────────────────────────────────────────────┘  │
  │                                                              │
  │  [ Back ]                                       [ Next → ]   │
  └──────────────────────────────────────────────────────────────┘
```

Or, if you don't want a Python server running at all, just open
`wizard/index.html` straight in your browser (double-click it from
Finder / Explorer). The wizard works fully offline as a static page —
the only difference is that you'll Download / Copy the file at the end
instead of getting a "save to ~/.config/jobscout/credentials.md" button.

---

## What the wizard asks

Six short steps:

1. **The basics** — name, city, are-you-open-to-moving, email, phone, LinkedIn, website.
2. **Your story in one paragraph** — the "what do you do?" coffee-shop answer.
3. **Your work** — jobs, side projects, volunteer things, classes you taught, anything. You can add as many as you want. Plus: anything you've shipped or made, plus any numbers worth knowing.
4. **Skills** — what you know how to do (in plain English, no jargon), what tools/software you've used, and underrated superpowers that wouldn't make a normal resume.
5. **What you're looking for** — what kind of role excites you, hard nos, money range, anything a hiring manager should know up front.
6. **Review and save** — see the rendered markdown, confirm save.

Every question has an example in gray underneath so you know what kind
of answer fits. No question is jargon-y. The wizard never asks for
"credentials" or "profile" — it asks about "your story" and "your work."

---

## Where things get saved

| File | What it is |
|---|---|
| `~/.config/jobscout/credentials.md` | The final output. The scorer reads this. |
| `~/.config/jobscout/wizard_progress.json` | Auto-save of every answer so you can resume. Deleted automatically on successful save. |

Override the config directory with `JOBSCOUT_CONFIG_DIR=/some/path` if
you want to keep multiple profiles (e.g. one for "IC track me" and one
for "founder track me").

---

## Resuming a half-finished wizard

The CLI wizard saves after every answer. Re-run `python3 jobscout.py setup`
and you'll see:

```
  Found saved progress — picking up where we stopped.
  (delete ~/.config/jobscout/wizard_progress.json if you want a fresh start)
```

The web wizard stores progress in two places: `localStorage` in your
browser (always) and the on-disk `wizard_progress.json` file (only when
you launched with `--web`, i.e. the Python server is running).

---

## Editing afterwards

`credentials.md` is just a markdown file. Open it in any editor and
change whatever you want. The scorer doesn't care about the exact
section names — it reads the whole file as your profile every time it
scores a role. Keep it under ~1500 words so it fits comfortably in the
LLM context window without crowding out the job description.

Want to start over? Delete the file and run `python3 jobscout.py setup`
again.

---

## Privacy

Everything happens locally:

- The CLI wizard is pure Python stdlib. No network calls of any kind.
- The web wizard is a single HTML file. No CDNs, no fonts, no
  analytics, no telemetry. The page only talks to its own bundled
  Python server (when launched with `--web`) or runs as a static page
  with no server at all.
- Your answers and the rendered `credentials.md` never leave your
  machine.

This is the same privacy posture as the rest of the agent — see the
[Privacy / Local-First](../README.md#-privacy--local-first) section of
the main README.

---

## Screenshots

Real screenshots will live in `docs/assets/wizard-*.png`. For now,
here's the text-art mockup of step 6 (review and save) so you know what
to expect:

```
  Step 6 of 6 — review and save
  [██████]

  ──────────────────────────────────────────────────────────
  # Alex Rivera

  **Where:** Boise, Idaho (open to relocating to SF, NYC)
  **Contact:** alex@example.com | https://linkedin.com/in/alex

  ## Who I Am
  I've spent 12 years running a small bakery...

  ## What I've Done
  - Ran the front of house at Romano's Italian for 6 years...
  ...
  ──────────────────────────────────────────────────────────

  Save this to ~/.config/jobscout/credentials.md?
    type: yes  to save  /  no  to bail (we'll keep your progress)
    type: edit to jump back to a step and change something
  > yes

  Saved! Your file is at /Users/alex/.config/jobscout/credentials.md
  You can now run `python3 jobscout.py` to score real jobs against it.
```
