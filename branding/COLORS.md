# Colors

The `job-search-agent` palette. Confident, technical, builder-first — think Linear / Vercel / Modal, not Notion or Slack. Mostly neutral, with a single decisive accent. Tailwind-style naming so it drops straight into Tailwind / shadcn / any design-token system.

## Brand

| Token | Hex | Use |
|---|---|---|
| `brand.primary` | `#0B0F14` | Default ink on light backgrounds. The wordmark, body copy on white, primary buttons on light theme. |
| `brand.accent` | `#10B981` | The one decisive accent. Score badges, success indicators, the radar pulse in the logo, primary CTA on dark. **Use sparingly** — one or two hits per screen. |
| `brand.accent.deep` | `#059669` | Hover/pressed state for the accent. Also the accent on light backgrounds where `#10B981` would feel too candy. |

> One accent. Resist the urge to add a second. If you find yourself reaching for a second color, you probably want a different shade of gray.

## Neutrals (the workhorse)

Tailwind's `slate` scale, used wholesale — neutral but with the slightest cool cast, which reads as "engineering" rather than "warm marketing."

| Token | Hex | Use |
|---|---|---|
| `neutral.50` | `#F8FAFC` | Page background, light theme. |
| `neutral.100` | `#F1F5F9` | Card background, light theme. Subtle dividers. |
| `neutral.200` | `#E2E8F0` | Borders on light theme. Disabled fills. |
| `neutral.300` | `#CBD5E1` | Muted icons on light theme. |
| `neutral.400` | `#94A3B8` | Placeholder text. Tertiary copy. |
| `neutral.500` | `#64748B` | Secondary body copy. Captions. |
| `neutral.600` | `#475569` | Body copy on light theme (if `neutral.900` feels too heavy). |
| `neutral.700` | `#334155` | Card background on dark theme. |
| `neutral.800` | `#1E293B` | Surface elevated on dark theme. Borders on dark. |
| `neutral.900` | `#0F172A` | Page background, dark theme. |
| `neutral.950` | `#020617` | Deepest ink. Use rarely — usually `neutral.900` is dark enough. |

## Status

| Token | Hex | Use |
|---|---|---|
| `success` | `#10B981` | Same as the accent — match-found, score-high, applied. No second green. |
| `warning` | `#F59E0B` | Score-medium, stale listing, deferred application. |
| `error` | `#EF4444` | Failed scrape, rejected, blocking validation. Use sparingly. |
| `info` | `#3B82F6` | Informational toast/banner. Borrowed for links inside long-form docs. |

## Usage rules

1. **80/15/5 rule.** ~80% of any screen is neutrals, ~15% is ink (`brand.primary` or white), ~5% is the accent. If accent climbs above 10%, the design starts to feel hype-y instead of confident.
2. **Never gradient the accent.** Flat fills only. Gradients read as "AI demo," not "shippable product."
3. **One status color per row.** A row that's both warning *and* error is a UX failure — pick whichever is most actionable for the user and surface only that.
4. **Pair the accent with neutral, not with itself.** Green-on-green = dashboard noise. Green on `neutral.900` = a clear signal.
5. **Borders are `neutral.200` (light) or `neutral.800` (dark).** Not gray-300, not white-with-opacity. Pick one and hold it across the whole app.

## CSS variables (drop-in)

```css
:root {
  --brand-primary: #0B0F14;
  --brand-accent: #10B981;
  --brand-accent-deep: #059669;

  --neutral-50:  #F8FAFC;
  --neutral-100: #F1F5F9;
  --neutral-200: #E2E8F0;
  --neutral-300: #CBD5E1;
  --neutral-400: #94A3B8;
  --neutral-500: #64748B;
  --neutral-600: #475569;
  --neutral-700: #334155;
  --neutral-800: #1E293B;
  --neutral-900: #0F172A;
  --neutral-950: #020617;

  --success: #10B981;
  --warning: #F59E0B;
  --error:   #EF4444;
  --info:    #3B82F6;
}
```
