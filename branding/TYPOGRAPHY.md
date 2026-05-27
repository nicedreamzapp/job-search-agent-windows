# Typography

One sans for UI/body, one mono for code and the wordmark. Both open-source, both shipped through Google Fonts and self-hostable.

## The pair

| Role | Font | License | Why |
|---|---|---|---|
| **UI + body** | [Inter](https://rsms.me/inter/) | SIL OFL 1.1 | Tuned for screen rendering at small sizes. Variable axis covers 100–900 in one file. Wide x-height keeps dense dashboards legible. Default voice of "modern engineering product." |
| **Code + wordmark** | [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | SIL OFL 1.1 | Designed for IDEs, so the operator audience already reads it eight hours a day. Distinct `0/O`, `1/l/I`, `()` and `{}` glyphs. Ligatures available but off by default — turn them on only inside actual code blocks. |

## Why this pair (not Plex, not Geist, not custom)

- **Familiar to the audience.** OSS contributors run Inter in their browser DevTools and JetBrains Mono in their editor. They'll recognize "their" type, which makes the project feel native to their world before they read a word.
- **Free and self-hostable.** No CDN dependency, no licensing fee, no surprise rebrand if a vendor changes terms.
- **Variable fonts.** One file per family, every weight and width — small footprint, no FOUT swap.
- **Mono in the wordmark.** Reinforces "this is a tool, not a brand consultancy." Aligns with the GitHub-CLI / Vercel / Modal pattern.

## Where each is used

| Surface | Font | Weight | Size |
|---|---|---|---|
| Wordmark | JetBrains Mono | 600 | 22–72px depending on context |
| Page title (H1) | Inter | 600 | 32–48px |
| Section heading (H2) | Inter | 600 | 22–28px |
| Sub-heading (H3) | Inter | 500 | 18–20px |
| Body | Inter | 400 | 15–16px |
| Caption / meta | Inter | 400 | 12–13px |
| Buttons / labels | Inter | 500 | 14px |
| Inline code | JetBrains Mono | 500 | 0.92em (matches surrounding body) |
| Code blocks | JetBrains Mono | 400 | 13–14px |
| Numeric/score badges | JetBrains Mono | 600 | 14px — tabular nums on |

## Rules

1. **Two families, no exceptions.** Inter and JetBrains Mono only. If you find yourself wanting a third (display, serif, handwriting), use a heavier Inter weight instead.
2. **Letter-spacing**: tight headlines (`-0.02em`), normal body (`0`), open captions/uppercase tags (`+0.06em`).
3. **Tabular numerals on for any table or score**: `font-variant-numeric: tabular-nums;`. Otherwise columns wobble.
4. **Never use a system font as a "lightweight fallback."** The stack falls back to `ui-sans-serif`/`ui-monospace` for the SVG marks only — in the app, ship the font.
5. **No italics in UI.** Italics belong in long-form prose, never in dashboards.

## CSS

```css
@import url('https://rsms.me/inter/inter.css');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  --font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

body { font-family: var(--font-sans); }
code, pre, kbd, samp { font-family: var(--font-mono); }
```

## Acceptable swaps

If Inter / JetBrains Mono can't ship for some reason (corp policy, weight budget), the only acceptable substitutions are:

- **Sans**: IBM Plex Sans (same neutral-but-warm voice, slightly more character)
- **Mono**: IBM Plex Mono (pairs natively with Plex Sans), or Fira Code

Never substitute toward: Roboto (too generic), Poppins (too rounded/cute), system-ui alone (no shared identity across platforms).
