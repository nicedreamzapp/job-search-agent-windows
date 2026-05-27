# Architecture

A 10,000-foot view of how `job-search-agent` works internally.

```
                ┌──────────────────────────────────────────┐
                │            jobscout.py (CLI)             │
                │  argparse → orchestrate → write results  │
                └──────────────────────────────────────────┘
                  │                │             │
                  ▼                ▼             ▼
       ┌────────────────┐  ┌─────────────┐  ┌──────────────┐
       │  connectors/   │  │ filters.py  │  │  scorer.py   │
       │  ─────────     │  │  rules from │  │  local MLX   │
       │  ashby.py      │  │  YAML/JSON  │  │     or       │
       │  greenhouse.py │  │             │  │  Anthropic   │
       │  lever.py      │  │             │  │              │
       └────────────────┘  └─────────────┘  └──────────────┘
                  │                │             │
                  └────────────────┼─────────────┘
                                   ▼
                          ┌──────────────────┐
                          │   output.py      │
                          │  state + write   │
                          │  + webhook       │
                          └──────────────────┘
```

## The five pillars

### 1. Multi-ATS connector layer

Each ATS (Applicant Tracking System) lives in its own file under
`connectors/`. The pattern is identical for all three:

```python
def fetch(slug: str) -> list[Job]:
    """Return all open postings for a company's board on this ATS."""
```

Every connector:

- Calls one public, documented API endpoint.
- Never raises — failures are logged and return an empty list. One bad
  company doesn't kill the daily run.
- Normalizes the provider-specific JSON into the shared `Job` dataclass
  defined in `connectors/base.py`.

To add a new ATS, drop a new file in `connectors/`, register it in the
`CONNECTORS` dispatch table in `jobscout.py`, and you're done. See
`docs/ADD_A_CONNECTOR.md` for the step-by-step.

### 2. Local-first LLM

The scorer prefers a local MLX server on `localhost:8000`. Anything that
speaks the OpenAI chat-completions API works:

- [`mlx_lm.server`](https://github.com/ml-explore/mlx-lm) on Apple Silicon
- [`llama.cpp`'s server mode](https://github.com/ggerganov/llama.cpp)
- [Ollama](https://ollama.com/) with its OpenAI compatibility layer
- Any cloud-hosted Anthropic-API-compatible endpoint you control

If `ANTHROPIC_API_KEY` is set in the environment, the scorer falls back
to the Anthropic Messages API. This is the **only** path that sends data
off your machine, and it's opt-in.

The scorer talks raw HTTP via `urllib`. No `pip install anthropic`
required — that's deliberate. Keeping the dep surface at zero means new
users can run the tool on a fresh macOS install without setting up a
virtualenv.

### 3. Curated allow-list

We do **not** crawl the open job market. The user provides a list of
companies they'd actually consider in `companies.json`. The scorer only
sees postings from that list.

Why: quality over volume. A daily list of 8 hand-picked roles you'd
seriously interview at beats a feed of 800 roles you'd never touch.
This is also why we use ATS APIs (which are stable, free, and respectful)
rather than scraping LinkedIn (which is none of those things).

### 4. `credentials.md` is the single source of truth

The candidate profile is one markdown file. The scorer reads it as
context for every role. You write it once. You don't need to:

- Tune the prompt per application.
- Maintain separate "version" résumés.
- Re-explain your background each time.

When your story changes (new job, new focus area, new constraint),
edit the file. Every subsequent score uses the updated profile.

### 5. Surface-only by default

`jobscout.py` outputs a JSON file. It does **not**:

- Auto-submit applications.
- Send emails on your behalf.
- POST to any external service unless you explicitly configure
  `JOBSCOUT_HQ_URL`.

The reason is honest: auto-submitting is high-stakes and hard to recover
from. Surfacing a daily list lets a human make the final call cheaply.
If you want to layer auto-submission on top, you're welcome to — but
that's a deliberate user choice, not the default.

## Data flow per run

1. **Load config.** `companies.json`, `filters.yml`, and `credentials.md`
   from `$JOBSCOUT_CONFIG_DIR`.
2. **Fetch.** For each company, dispatch to the right connector. Returned
   `Job` objects accumulate in one list.
3. **Filter.** Drop obvious-no jobs (title regex, description regex,
   location allow-list). Verbose mode prints why each was dropped.
4. **Dedup.** Skip anything in `seen.json` from a previous run. Re-runs
   the same day are cheap.
5. **Score.** For each remaining job, ask the LLM for a 0–100 fit score
   plus a one-sentence rationale.
6. **Output.** Sort by score descending, write to
   `$JOBSCOUT_STATE_DIR/results/<date>.json`, optionally POST to webhook,
   update `seen.json`.

The whole pipeline is plain functions composing plain dataclasses. There
is no global state, no async machinery, no plugin loader — just files
calling files.

## Why stdlib-only

The default install path is `git clone` + `python3 jobscout.py`. No
`pip`, no virtualenv, no compiled extensions. This matters because:

- The friction to try it is near zero.
- It works on managed laptops where you can't `pip install`.
- It survives Python upgrades that break third-party deps.
- The whole codebase is auditable in an evening.

The cost is hand-rolling small things (a tiny YAML subset parser, a
crude HTML-to-text converter). All of that lives in `connectors/base.py`
and `filters.py` — under 100 lines of glue total.

## State directory layout

```
$JOBSCOUT_STATE_DIR/        # ~/.local/state/jobscout by default
├── seen.json               # {"seen": ["ashby:anthropic:abc123", ...]}
└── results/
    ├── 2026-05-21.json     # full scored output for each run
    ├── 2026-05-22.json
    └── ...
```

`seen.json` is the only thing that needs to persist between runs. The
results files are intentionally per-day so you can diff "today's list
vs. yesterday's list" if you want.

## Testing

Tests live in `tests/` and use stdlib `unittest`. The connector tests
mock the HTTP layer by monkey-patching `connectors.base.http_get_json`,
so the unit suite runs offline.

A live-endpoint smoke test runs when the env flag `JOBSCOUT_LIVE_TESTS=1`
is set. CI keeps this off by default to avoid hammering real ATSes.
