# Regenerating `demo.svg`

`docs/demo.svg` is the animated terminal recording embedded in the README. It is
**handcrafted SMIL**, not a recording — every line, color, and timing lives in
the SVG itself. This keeps it small (~16 KB), deterministic, and dependency-
free.

This guide covers two ways to regenerate or modify it:

1. **The handcrafted route** (what's currently in tree) — edit the SVG directly.
2. **The asciinema route** — record a real terminal session and convert it to
   SVG. Useful if you'd rather capture a live `jobscout` run than maintain
   handcrafted SMIL.

`docs/demo-script.md` holds the canonical narration and timing — both routes
treat it as the source of truth for *what the demo says*.

---

## Route 1 — Edit the handcrafted SVG (recommended)

This is the default. The SVG is structured so common edits are mechanical.

### Change the company list, scores, or copy

1. Open `docs/demo-script.md` and edit the text you want to change. Keep the
   timing column accurate so other contributors know when each line appears.
2. Open `docs/demo.svg` and locate the matching `<g opacity="0"> ... </g>` block
   (one per line of terminal output).
3. Edit the `<tspan>` text inside that group. Color classes (`green`, `peach`,
   `blue`, `mauve`, etc.) are defined in the `<style>` block at the top of the
   file — re-use those rather than inlining `fill="..."`.

### Change the timing

Each output line has a `<animate>` element like:

```xml
<animate attributeName="opacity" to="1" begin="15.3s;loop.end+15.3s" dur="0.01s" fill="freeze"/>
```

The two values in `begin="..."` are:

- `15.3s` — first-pass start time (seconds from page load)
- `loop.end+15.3s` — every subsequent loop start time, anchored to the master
  loop driver at the bottom of the file

When you adjust a line's timing, change **both** numbers and keep them in sync.

### Change the total loop length

There's a single master loop driver near the bottom of the SVG:

```xml
<animate id="loop" attributeName="x" from="-10" to="-10" dur="58s"
         begin="0s;loop.end" repeatCount="indefinite"/>
```

Change `dur="58s"` to the new loop duration. All `loop.end+Xs` references will
re-anchor automatically.

### Re-render check

The SVG is its own renderable artifact — there's no build step. Verify it works:

```bash
open docs/demo.svg                    # macOS — opens in default browser
xdg-open docs/demo.svg                # Linux
```

You should see the animation play through one full cycle (~58s) and loop
cleanly.

Sanity checks before committing:

```bash
# 1. XML well-formedness
python3 -c "import xml.etree.ElementTree as ET; ET.parse('docs/demo.svg'); print('ok')"

# 2. File size (target: < 200 KB)
du -h docs/demo.svg

# 3. No external resource fetches (only the SVG namespace and the URLs shown
#    inside the terminal as visible text should match)
grep -E "http(s)?://" docs/demo.svg
```

### Localize for a different audience

Common forks people may want:

- **Different allow-list** — swap the five fetch lines and update the company
  names in the scoring + top-3 blocks.
- **Different role profile** — swap titles + score numbers to reflect a
  designer, PM, etc.
- **Different theme** — change the palette in the `<style>` block. The Catppuccin
  Mocha hex values are listed in `demo-script.md` for reference. Solarized Dark,
  Dracula, and Tokyo Night also work well and slot in via the same class names.

---

## Route 2 — Record a real terminal run with asciinema

If you'd rather record an actual `jobscout` run than maintain handcrafted SMIL:

### One-time setup

```bash
# macOS
brew install asciinema
npm install -g svg-term-cli       # or: cargo install --git https://github.com/asciinema/agg
```

### Record + render

```bash
# 1. Record (Ctrl-D when done)
asciinema rec docs/demo.cast \
  --title "jobscout --verbose" \
  --idle-time-limit 2 \
  --command "python3 jobscout.py --verbose"

# 2. Convert to SVG
svg-term --in docs/demo.cast --out docs/demo.svg \
         --window --width 102 --height 30 \
         --term iterm2 --profile "Catppuccin Mocha"

# Alternative renderer (Rust, smaller output, GIF/SVG capable):
# agg docs/demo.cast docs/demo.svg --theme monokai
```

### Trade-offs vs. handcrafted

| Concern              | Handcrafted SMIL                  | asciinema + svg-term            |
| -------------------- | --------------------------------- | ------------------------------- |
| File size            | ~16 KB                            | typically 60–150 KB             |
| Deterministic output | Yes — every char is in the SVG    | No — depends on live timings    |
| Personal data risk   | Zero — no real fetches            | Need a sanitized config first   |
| Edit-friendliness    | Edit XML, see change immediately  | Re-record from scratch          |
| Looks like a real CLI| Mimics it — close enough          | Yes — it *is* a real CLI        |

For the public OSS demo we prefer the handcrafted route because it can never
accidentally leak environment data and survives `jobscout` internals changing.

---

## Route 3 — Last resort: terminalizer

If neither asciinema nor agg is available, [`terminalizer`](https://github.com/faressoft/terminalizer)
records to a YAML file and renders to GIF. Output GIFs are typically 1–3 MB —
too big for a clean GitHub README — so only use this if you genuinely can't get
SVG output.

```bash
npm install -g terminalizer
terminalizer record docs/demo
terminalizer render docs/demo -o docs/demo.gif
```

If you go this route, also write a `docs/demo.gif`-sized warning in the PR so
the maintainer can decide whether to accept the size bump.

---

## Constraints any regenerated demo must satisfy

These come from the original spec — please don't regress them:

- **File size** < 200 KB (the current SVG is ~16 KB; lots of headroom).
- **No external assets** — no `<image href="https://...">`, no `@font-face` with
  a CDN URL, no `<link>` tags. The only URLs allowed in the file are: (a) the
  SVG namespace declaration, and (b) URLs shown as visible terminal text.
- **Self-contained looping** — must loop seamlessly via SMIL (or, if rendered
  via asciinema, embed `repeatCount="indefinite"` in the output SVG).
- **Accessibility** — keep the `<title>` and `<desc>` tags at the top of the
  SVG and update them if the content changes meaningfully.
- **Open-licensed fonts only** — the current SVG declares a fallback chain
  ending in `monospace`, which is always safe. Avoid embedding a font face
  unless it's a permissively-licensed one (JetBrains Mono, Fira Code, IBM Plex
  Mono) and even then check that the file stays under 200 KB.
- **No personal data** — the demo user is "Jane Doe" and the company allow-list
  is five public AI companies. Do not substitute real candidate info.

---

## Quick reference — where things live

| File                                | Purpose                                       |
| ----------------------------------- | --------------------------------------------- |
| `docs/demo.svg`                     | The animated SVG embedded in the README       |
| `docs/demo-script.md`               | Storyboard, copy, timing, color palette       |
| `docs/HOW_TO_REGENERATE_DEMO.md`    | This file                                     |

To embed in the README:

```markdown
<p align="center">
  <img src="docs/demo.svg" alt="jobscout demo" width="820"/>
</p>
```
