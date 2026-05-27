# Demo Script — `jobscout.py --verbose`

This is the storyboard for `demo.svg`. The animated SVG renders this sequence
frame-by-frame using SMIL `<animate>` elements. Edit this file to change the
copy, then re-render the SVG following `HOW_TO_REGENERATE_DEMO.md`.

The simulated user is **Jane Doe**. The demo allow-list uses five real, public
AI companies that all run public Ashby/Greenhouse boards:

- Anthropic (ashby)
- Modal (greenhouse)
- Replit (greenhouse)
- Cohere (greenhouse)
- Cursor (ashby)

**No real candidate data appears anywhere in the demo.**

---

## Timing budget

| Phase                    | Start (s) | End (s) | Duration |
| ------------------------ | --------: | ------: | -------: |
| Prompt + typed command   |       0.0 |     2.5 |     2.5s |
| Header + config loaded   |       2.8 |     4.5 |     1.7s |
| Fetching 5 connectors    |       4.8 |    13.0 |     8.2s |
| Filter pass              |      13.3 |    15.0 |     1.7s |
| Scoring progress         |      15.3 |    32.0 |    16.7s |
| Summary block            |      32.3 |    36.0 |     3.7s |
| Top 3 high-fit roles     |      36.3 |    48.0 |    11.7s |
| Closing line             |      48.3 |    50.0 |     1.7s |
| Hold / pause             |      50.0 |    58.0 |     8.0s |
| **Loop**                 |      58.0 |       — |        — |

Total loop duration: **58 seconds**.

---

## Frame-by-frame copy

The terminal prompt is rendered as:

```
jane@laptop ~/job-search-agent $
```

### t = 0.0 — empty prompt visible
```
jane@laptop ~/job-search-agent $ █
```
(cursor blinks)

### t = 0.4 to 2.4 — command types character-by-character
End state:
```
jane@laptop ~/job-search-agent $ python3 jobscout.py --verbose
```

### t = 2.5 — newline, command runs

### t = 2.8 — banner
```
jobscout v0.4.0  ·  searching 5 companies for Jane Doe
loaded config: profile.yaml  ·  allow_list: 5  ·  filters: 3 active
```

### t = 4.8 to 13.0 — fetching (one line per company, ~1.5s apart)
```
[fetch][ashby:anthropic     ] 23 roles
[fetch][greenhouse:modal    ] 12 roles
[fetch][greenhouse:replit   ] 18 roles
[fetch][greenhouse:cohere   ] 31 roles
[fetch][ashby:cursor        ]  9 roles
```
After all five appear, a summary line:
```
[fetch] done · 93 roles total · 5/5 boards ok
```

### t = 13.3 to 15.0 — filter pass
```
[filter] excluding 46 roles (location, level, role-family)
[filter] 47 roles remain for scoring
```

### t = 15.3 to 32.0 — scoring (8 visible lines, the rest abbreviated by a "..." line)
```
[score]  1/47  Forward Deployed Engineer    @ Modal Labs          9.2
[score]  4/47  Research Engineer, Alignment @ Anthropic           8.9
[score]  7/47  AI Agent Engineer            @ Replit              8.6
[score] 11/47  Solutions Architect          @ Cohere              7.8
[score] 18/47  Developer Experience Eng     @ Cursor              8.3
[score] 24/47  Product Engineer             @ Modal Labs          7.4
[score] 31/47  Member of Technical Staff    @ Anthropic           8.1
[score] 39/47  Open Source Engineer         @ Replit              6.9
[score] ...
[score] 47/47  complete
```

### t = 32.3 to 36.0 — summary block
Drawn as a boxed panel:
```
─────────────────────────────────────────────────────────────
  47 roles scored   ·   5 high-fit (≥8.0)   ·   12 worth-considering
─────────────────────────────────────────────────────────────
```

### t = 36.3 to 48.0 — top 3 high-fit roles printed
```
top 3 matches:

  1. Forward Deployed Engineer            @ Modal Labs   (9.2)
     remote · senior · ships customer integrations
     → https://jobs.ashbyhq.com/modal/...

  2. Research Engineer, Alignment         @ Anthropic    (8.9)
     SF / hybrid · senior IC · interpretability team
     → https://jobs.ashbyhq.com/anthropic/...

  3. AI Agent Engineer                    @ Replit       (8.6)
     remote · staff · agent runtime / sandboxing
     → https://job-boards.greenhouse.io/replit/...
```

### t = 48.3 — closing line
```
report written: out/2026-05-21-jobscout.md
```

### t = 50.0 — return to prompt
```
jane@laptop ~/job-search-agent $ █
```
(holds for 8 seconds, then loops)

---

## Color palette (Catppuccin Mocha)

| Token            | Hex       | Used for                                   |
| ---------------- | --------- | ------------------------------------------ |
| `base`           | `#1e1e2e` | terminal background                        |
| `surface0`       | `#313244` | window chrome / divider lines              |
| `text`           | `#cdd6f4` | default text                               |
| `subtext0`       | `#a6adc8` | dimmed text (timestamps, paths)            |
| `green`          | `#a6e3a1` | success markers, "ok", high score          |
| `yellow`         | `#f9e2af` | mid-score, warnings                        |
| `peach`          | `#fab387` | section headers (`[fetch]`, `[score]`)     |
| `blue`           | `#89b4fa` | URLs, company names                        |
| `mauve`          | `#cba6f7` | the user's typed command                   |
| `red`            | `#f38ba8` | (reserved — not used in the happy-path demo) |
| `red-traffic`    | `#ff5f57` | macOS close button                         |
| `yellow-traffic` | `#febc2e` | macOS minimize button                      |
| `green-traffic`  | `#28c840` | macOS maximize button                      |

---

## Rendering notes

- Each text element is hidden by default (`opacity: 0`) and animated to
  `opacity: 1` via SMIL at its scheduled `begin` time.
- The cursor is a separate `<rect>` that blinks with a 1-second `repeatCount`
  animation while not typing, then is hidden during the long pauses where
  output is streaming.
- The whole animation uses one master `<animate>` on a top-level group with
  `repeatCount="indefinite"` and a `dur` matching the loop duration, so
  re-timing the loop only requires changing one value.
