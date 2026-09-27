<p align="center">
  <img src="branding/logo.svg" width="160" alt="job-search-agent logo">
</p>

<p align="center">
  <h1 align="center">🎯⚡ job-search-agent</h1>
  <p align="center">
    <strong>Wake up to a hand-curated, AI-scored list of job openings — ranked against <em>you</em>, not against a keyword bag.<br>Local-first. No spray-apply. No SaaS fees.</strong>
  </p>
  <p align="center">
    <a href="../../stargazers"><img src="https://img.shields.io/github/stars/nicedreamzapp/job-search-agent-windows?style=for-the-badge&logo=github&color=f5c542&labelColor=1f2328" alt="GitHub stars"></a>
    <a href="../../network/members"><img src="https://img.shields.io/github/forks/nicedreamzapp/job-search-agent-windows?style=for-the-badge&logo=github&color=4c9a2a&labelColor=1f2328" alt="GitHub forks"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/📜_License-MIT-yellow?style=for-the-badge" alt="MIT"></a>
    <a href="#-quick-start-3-minutes"><img src="https://img.shields.io/badge/🐍_Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+"></a>
    <a href="#-privacy--local-first"><img src="https://img.shields.io/badge/🔒_Privacy-100%25_Local--First-success?style=for-the-badge" alt="100% Local-First"></a>
    <a href="#-how-it-works-architecture-diagram"><img src="https://img.shields.io/badge/🧠_LLM-MLX_·_Ollama_·_Claude_API-purple?style=for-the-badge" alt="LLM backends"></a>
    <a href="#-what-makes-this-different"><img src="https://img.shields.io/badge/🚫_Spray--Apply-Zero-red?style=for-the-badge" alt="No spray-apply"></a>
    <a href="#-adding-a-new-ats"><img src="https://img.shields.io/badge/🧩_ATS-Ashby_·_Greenhouse_·_Lever-ff69b4?style=for-the-badge" alt="ATS connectors"></a>
    <a href="#-schedule-daily-runs"><img src="https://img.shields.io/badge/📅_Daily-Task_Scheduler_·_cron_·_systemd-orange?style=for-the-badge" alt="Schedule"></a>
    <a href="#-the-big-claim"><img src="https://img.shields.io/badge/🪴_Ambient-Computing-9cf?style=for-the-badge" alt="Ambient Computing"></a>
  </p>
  <p align="center">
    <a href="#-tldr">✨ TL;DR</a> ·
    <a href="#-the-big-claim">💥 Claim</a> ·
    <a href="#-30-second-demo">🎬 Demo</a> ·
    <a href="#-quick-start-3-minutes">🚀 Quick Start</a> ·
    <a href="#-how-it-works-architecture-diagram">🧠 Architecture</a> ·
    <a href="#-what-makes-this-different">🎯 Why</a> ·
    <a href="#-privacy--local-first">🔒 Privacy</a> ·
    <a href="#-customizing-the-scoring-rubric">🛠️ Customize</a> ·
    <a href="#-adding-a-new-ats">🧩 Connectors</a> ·
    <a href="#-schedule-daily-runs">📅 Schedule</a> ·
    <a href="#%EF%B8%8F-known-limits">⚠️ Limits</a> ·
    <a href="#-roadmap">🛣️ Roadmap</a> ·
    <a href="#-contributing">🤝 Contribute</a>
  </p>
</p>

---

**What it does:** every run, it pulls open roles from the public Ashby, Greenhouse and Lever job boards of the companies you list, drops the ones that break your rules, and has an LLM score each remaining role 0 to 100 against a profile you wrote, drafting a short pitch for the strong matches.

**Proof it runs:** a 60-second video walkthrough (below), 30 unit tests for the connectors and filters (`python -m unittest discover -s tests`: 27 run offline and pass, 3 live-network smoke tests are skipped unless `JOBSCOUT_LIVE_TESTS=1`), and zero third-party dependencies (see [`pyproject.toml`](pyproject.toml)).

---

## 👷 What I built

Written by **Matt Macosko**. This repo is the Windows-ready fork of job-search-agent.

- 🧠 **Orchestrator and CLI** ([`jobscout.py`](jobscout.py)): loads config, runs the connectors, filters, dedups against past runs, scores, writes results.
- 🔌 **Three ATS connectors** ([`connectors/ashby.py`](connectors/ashby.py), [`connectors/greenhouse.py`](connectors/greenhouse.py), [`connectors/lever.py`](connectors/lever.py)) on a shared `Job` model in [`connectors/base.py`](connectors/base.py).
- 🪓 **Rule filter** ([`filters.py`](filters.py)) with a small hand-rolled YAML parser so there is nothing to `pip install`.
- 🎯 **LLM scorer and pitch drafter** ([`scorer.py`](scorer.py)) speaking raw HTTP to a local OpenAI-compatible server or the Anthropic Messages API, with editable prompts in [`prompts/`](prompts/).
- 📬 **Output and state** ([`output.py`](output.py)): daily JSON results, seen-job dedup, optional webhook.
- ✨ **Setup wizard** in the terminal ([`setup.py`](setup.py)) and in the browser ([`wizard/index.html`](wizard/index.html)).
- ✅ **Tests** ([`tests/`](tests/)) and the demo animation ([`docs/demo.svg`](docs/demo.svg), [`render/demo.html`](render/demo.html)).

Upstream, not mine: the LLMs themselves (default local model `mlx-community/Llama-3.1-8B-Instruct-4bit`, or Claude via the Anthropic API), the servers that run them (Apple's [mlx-examples](https://github.com/ml-explore/mlx-examples) / `mlx_lm.server`, Ollama, llama.cpp, vLLM), and the public Ashby, Greenhouse and Lever job board APIs. See [`CREDITS.md`](CREDITS.md).

---

<p align="center">
  <h2 align="center">🎬 WATCH THE 60-SECOND DEMO</h2>
  <p align="center">
    <strong>A scripted walkthrough with a fictional candidate. 47 roles scored across 12 companies. 3 custom pitches drafted. 60 seconds, end to end, on a laptop.<br>
    No cloud LLM. No SaaS. No "AI resume optimizer" hype.</strong>
  </p>
  <p align="center">
    <a href="https://youtu.be/qlgvh2N8HJ4">
      <img src="https://img.youtube.com/vi/qlgvh2N8HJ4/maxresdefault.jpg" width="820" alt="job-search-agent — 60-second walkthrough on YouTube">
    </a>
  </p>
  <p align="center">
    <a href="https://youtu.be/qlgvh2N8HJ4">
      <img src="https://img.shields.io/badge/▶_Watch_on_YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
    </a>
    &nbsp;
    <a href="https://www.youtube.com/@nicedreamzapps">
      <img src="https://img.shields.io/badge/Subscribe-@nicedreamzapps-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Subscribe">
    </a>
  </p>
  <p align="center">
    <em>Built for anyone who's tired of LinkedIn's "200 applicants in 12 hours" job-board roulette.</em>
  </p>
</p>

---

## ✨ TL;DR

**Wake up to a daily list of AI-scored job matches across every company on your allow-list** (the example list ships with a starter set of AI and dev-tools companies). Local-first. Your data stays on your machine if you use a local model. The agent reads **your** portfolio, as you describe it in `credentials.md` — GitHub stars, shipped products, published research, community size, the work you'd actually point a hiring manager at — and scores every open role against you, not against a generic resume-keyword match. Every role that scores 80 or higher comes with a ~200-word, role-specific pitch already drafted. You stay in the loop on every send.

---

## 💥 The Big Claim

Most job seekers do one of two things: **spray-apply** through a Workday queue and never hear back, or **hand-curate** roles from LinkedIn one tab at a time and burn an hour a day on it. Both lose.

This repo flips it. **You write your credentials once** — your real story, your real ships, your real numbers — into a single markdown file. Every morning, the agent fetches fresh openings from every company in your allow-list (Ashby, Greenhouse, Lever, more on the way), filters them through your hard constraints (title, description, company and location patterns), and **scores each surviving role against your actual portfolio using a local LLM**. The top hits (score 80+) get a ~200-word custom pitch drafted on the spot — the kind of paragraph you'd normally take 20 minutes to write, ready to paste into a cover letter or a recruiter DM.

**No auto-submit.** You stay in the loop. No data leaves your machine if you pick the MLX or Ollama backend — the Anthropic API is an explicit, opt-in fallback for users who don't have a beefy local box. Built for the ambient-computing era of job hunting: the agent does the boring grind at 6 AM so you spend your morning coffee reading three roles that actually fit, not 200 that don't.

---

## 🎬 30-Second Demo

<p align="center">
  <img src="docs/demo.svg" width="720" alt="Animated loop of the agent scoring roles">
</p>

<p align="center">
  <em>Animated mock-up with simulated output (fictional candidate Jane Doe): the agent scores 47 roles across Anthropic / Modal / Replit / Cohere / Cursor, then writes a custom pitch for the top 3.</em>
</p>

---

## ✨ First-time setup (no terminal experience needed)

**Never used the terminal before?** Run

```bash
python jobscout.py setup
```

and answer the questions in plain English. The wizard asks who you are,
what you've done, and what kind of role you'd actually want — then writes
a polished `credentials.md` file to the right place for you. Takes about
5–10 minutes. Your answers save as you go, so you can quit and resume
later. The wizard only writes `credentials.md`. You still need a
`companies.json` (see Quick Start step 3).

Prefer a webpage to the terminal? Run

```bash
python jobscout.py setup --web
```

and the wizard opens in your browser. Same questions, multi-step form,
"Download credentials.md" button at the end. Or — if you'd rather not run
any command at all — just open `wizard/index.html` straight in your
browser (double-click it). Works fully offline, no internet needed.

Full wizard guide: [`docs/SETUP_WIZARD.md`](docs/SETUP_WIZARD.md)

---

## 🚀 Quick Start (3 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/nicedreamzapp/job-search-agent-windows.git
cd job-search-agent-windows

# 2. No deps to install — pure stdlib. Python 3.11+ is the only requirement.
#    Download Python from https://python.org if you don't have it.

# 3. Copy the example company list (required) and filters (optional).
#    Windows commands shown; on macOS/Linux use ~/.config/jobscout and cp.
mkdir %USERPROFILE%\.config\jobscout
copy examples\companies.example.json  %USERPROFILE%\.config\jobscout\companies.json
copy examples\filters.example.yml     %USERPROFILE%\.config\jobscout\filters.yml

# 4. Write your profile: run the setup wizard (plain-English Q&A, ~5 minutes)...
python jobscout.py setup
# ...or copy the example and edit it by hand:
copy examples\credentials.example.md  %USERPROFILE%\.config\jobscout\credentials.md
notepad %USERPROFILE%\.config\jobscout\credentials.md

# 5. Optional: check the connectors work (fetch + filter, no LLM needed).
#    A dry run marks the jobs as seen, so delete seen.json afterwards (see Known limits).
python jobscout.py --dry-run --companies-only=anthropic

# 6. Start a local LLM server on http://localhost:8000 (or set ANTHROPIC_API_KEY), then:
python jobscout.py
```

**Scoring needs an LLM.** Without a server at `JOBSCOUT_LLM_ENDPOINT` (default `http://localhost:8000`) and without `ANTHROPIC_API_KEY`, every role is saved with score 0 and an "unreachable" error in the log. `--dry-run` works with no LLM at all.

What a good run looks like (illustrative mock-up; the real CLI prints plain progress lines and writes JSON, see below):

```
╭─────────────────────────────────────────────────────────────╮
│  job-search-agent — daily briefing · 2026-05-21 06:14       │
│  ─────────────────────────────────────────────────────────  │
│  Scanned : 12 companies · 312 roles                         │
│  Filtered: 47 roles passed your hard constraints            │
│  Scored  : top 3 below · full list in state/briefing.md     │
╰─────────────────────────────────────────────────────────────╯

🟢 92/100 — Anthropic · Member of Technical Staff, Agents
   why: ships agent frameworks, you've shipped 4 OSS agent repos,
        128k+ combined stars, exactly the cohort they describe.
   pitch drafted → state/pitches/anthropic-mts-agents.md

🟢 88/100 — Modal Labs · Founding DevRel
   why: your blog ships weekly, your community is 3k+ Discord,
        Modal explicitly wants someone who can write & ship demos.
   pitch drafted → state/pitches/modal-devrel.md

🟡 79/100 — Replit · Applied AI Engineer
   ...
```

**Where results actually go today:** the ranked list, rationales and drafted pitches are written to one JSON file per day at `results/<YYYY-MM-DD>.json` inside the state directory (`$JOBSCOUT_STATE_DIR`, default `~/.local/state/jobscout`, which on Windows is `%USERPROFILE%\.local\state\jobscout`). The `briefing.md` and `pitches/` folder shown in the mock-up above are **not implemented yet**. If you set `JOBSCOUT_HQ_URL`, the top 10 are also POSTed to that webhook.

---

## 🧠 How It Works (architecture diagram)

```
   ┌─────────────────────────────────────────────────────────────────┐
   │                       YOUR MACHINE                              │
   │                                                                 │
   │  📋 companies.json     ┌─────────────────────────────────────┐  │
   │      (allow-list)      │                                     │  │
   │           │            │   🧠 jobscout.py orchestrator       │  │
   │           ▼            │                                     │  │
   │  ┌──────────────────┐  │   ┌─────────────────────────────┐   │  │
   │  │  🔌 connectors   │──┼──▶│  raw_roles[]                │   │  │
   │  │                  │  │   └──────────────┬──────────────┘   │  │
   │  │  · Ashby         │  │                  ▼                  │  │
   │  │  · Greenhouse    │  │   ┌─────────────────────────────┐   │  │
   │  │  · Lever         │  │   │  🪓 hard-constraint filter  │   │  │
   │  │  · (your own)    │  │   │  (location · comp · family) │   │  │
   │  └──────────────────┘  │   └──────────────┬──────────────┘   │  │
   │                        │                  ▼                  │  │
   │  📝 credentials.md ───▶│   ┌─────────────────────────────┐   │  │
   │      (your story)      │   │  🎯 LLM scorer + pitcher    │   │  │
   │                        │   │  (MLX · Ollama · Anthropic) │   │  │
   │                        │   └──────────────┬──────────────┘   │  │
   │                        │                  ▼                  │  │
   │                        │   📬 results/<date>.json            │  │
   │                        │      (scores · rationale · pitch)   │  │
   │                        └─────────────────────────────────────┘  │
   │                                                                 │
   │              🚫 ZERO outbound calls with local backend          │
   └─────────────────────────────────────────────────────────────────┘
```

**1 — Connectors** hit each company's public ATS endpoint (Ashby, Greenhouse, Lever) and return a normalized `Job` object. No login. No scraping headless Chrome. Public job-board APIs only.

**2 — The hard-constraint filter** drops anything that fails your non-negotiables (regex rules on title, description, company and location, from `filters.yml`) before any LLM tokens get spent.

**3 — The scorer** prompts the LLM with your full `credentials.md` and the surviving role, asks for a 0–100 fit score with a one-sentence justification, and — for any role scoring at or above `pitch_threshold` (80, set in `scorer.py`) — drafts a 200-word custom pitch.

---

## 🎯 What Makes This Different

|                                              | This agent | LinkedIn Jobs | Wellfound | Spray-applying |
|----------------------------------------------|:----------:|:-------------:|:---------:|:--------------:|
| Reads YOUR full credentials                  |     ✅     |       ❌      |     ❌    |        ❌       |
| Scores roles against your actual portfolio   |     ✅     |       ❌      |     ❌    |        ❌       |
| Drafts custom pitches per role               |     ✅     |       ❌      |     ❌    |        ❌       |
| Runs locally / private                       |     ✅     |       ❌      |     ❌    |       N/A       |
| Costs $0/mo (local LLM)                      |     ✅     |       ❌      |     ❌    |       N/A       |
| Doesn't spam recruiters                      |     ✅     |       ✅      |     ✅    |        ❌       |
| Surfaces roles you'd never have searched for |     ✅     |       ❌      |     ❌    |        ❌       |
| You stay in the loop on every send           |     ✅     |       ✅      |     ✅    |       N/A       |

The core unlock: **the LLM has read your real story before it ever sees a role.** That's a different question than "does this resume contain the word `kubernetes`."

---

## 🔒 Privacy / Local-First

Your `credentials.md` is the most sensitive file in your job search. It has your real numbers, your real ships, the unvarnished version of your story. It should never leak.

- **Default backend: local.** Point `JOBSCOUT_LLM_ENDPOINT` at any OpenAI-compatible chat-completions server — an [MLX server](https://github.com/ml-explore/mlx-examples), a local [Ollama](https://ollama.com) instance, `llama.cpp` server mode, vLLM, anything that speaks `/v1/chat/completions`. The default is `http://localhost:8000`. Nothing about your credentials or the roles you're scoring ever touches the public internet.
- **Optional cloud fallback.** If you don't have a beefy enough local box, set `ANTHROPIC_API_KEY` in your environment. The scorer detects the key and switches to the Anthropic Messages API automatically. This is explicitly opt-in — the env var has to be present. There is no "anonymous telemetry," no "share your usage to improve the model" toggle. Off means off.
- **Optional webhook.** Only if you set `JOBSCOUT_HQ_URL` does a summary of the top 10 get POSTed anywhere.
- **The connectors are read-only.** They hit public ATS endpoints. They never log in as you, never submit anything on your behalf, never even know your name.

```
   ┌─────────────────────────────────────────────────────────┐
   │                    YOUR MACHINE                         │
   │                                                         │
   │   credentials.md  ──▶  scorer  ──▶  LLM (local)         │
   │                                       │                 │
   │                                       └─▶ results/*.json│
   │                                                         │
   │   🚫 nothing crosses this boundary with local backend   │
   └─────────────────────────────────────────────────────────┘
                              ↕
                  (only the connectors talk out,
                   and only to public ATS endpoints)
```

---

## 🛠️ Customizing the Scoring Rubric

The default scoring prompt asks the LLM to weigh shipped artifacts, demonstrated impact, role-family fit, and timing signals. You can replace it wholesale.

- Edit [`prompts/scoring.md`](prompts/scoring.md) to change how the LLM weighs your portfolio against a role.
- Edit [`prompts/pitch.md`](prompts/pitch.md) to change the voice and length of the auto-drafted pitch.
- Full rubric reference + examples → [`docs/CUSTOMIZE_SCORING.md`](docs/CUSTOMIZE_SCORING.md)

---

## 🧩 Adding a New ATS

Connectors live in `connectors/`. Each one is a single Python file that exposes a `fetch_<ats>(slug) -> list[Job]` function, registered in the `CONNECTORS` table in `jobscout.py`. Each of the three existing connectors is **about 100 lines of code**.

Already supported:

| ATS | Module | Auth | Public endpoint |
|---|---|---|---|
| 🟢 **Ashby** | `connectors/ashby.py` | None | `api.ashbyhq.com/posting-api/job-board/{slug}` |
| 🟢 **Greenhouse** | `connectors/greenhouse.py` | None | `boards-api.greenhouse.io/v1/boards/{slug}/jobs` |
| 🟢 **Lever** | `connectors/lever.py` | None | `api.lever.co/v0/postings/{slug}` |

Adding Workday, SmartRecruiters, or your own — see [`docs/ADD_A_CONNECTOR.md`](docs/ADD_A_CONNECTOR.md).

---

## 📅 Schedule Daily Runs

The whole point is that you wake up to the briefing, not that you remember to type `python jobscout.py`. Pick your platform:

- **Windows** → Task Scheduler (see below)
- **macOS** → launchd plist in [`docs/LAUNCHAGENT_MACOS.md`](docs/LAUNCHAGENT_MACOS.md)
- **Linux** → systemd timer in [`docs/SYSTEMD_LINUX.md`](docs/SYSTEMD_LINUX.md)

### Windows Task Scheduler Setup

1. Open **Task Scheduler** (search for it in the Start menu)
2. Click **Create Basic Task**
3. Name it `JobScout Daily` and click Next
4. Choose **Daily**, set it to 6:00 AM, click Next
5. Choose **Start a program**, click Next
6. Set:
   - **Program:** `python`
   - **Arguments:** `C:\path\to\job-search-agent-windows\jobscout.py`
   - **Start in:** `C:\path\to\job-search-agent-windows`
7. Check **Open the Properties dialog** and click Finish
8. In Properties, under **Conditions**, uncheck "Start the task only if the computer is on AC power"
9. Under **Settings**, check "Run task as soon as possible after a scheduled start is missed"

Done. Briefing waits for you with your first coffee.

You can also run it from the command line to test:

```bash
python jobscout.py --dry-run
```

---

## ⚠️ Known limits

- **Results are JSON only.** No `briefing.md` or `pitches/` files yet; read `results/<date>.json`.
- **Dry runs and failed scores still count as "seen."** Every fetched job is added to `seen.json` in the state directory, even on `--dry-run` or when the LLM was unreachable, so the next run skips it. Delete `seen.json` to re-score.
- **Filters are regex only.** There is no salary or comp filter; you can only match on title, description, company and location text.
- **The pitch threshold (80) is fixed in `scorer.py`**, not a config option.
- **No LLM, no scores.** A local OpenAI-compatible server or `ANTHROPIC_API_KEY` is required for anything beyond `--dry-run`.

---

## 🛣️ Roadmap

- [ ] **LinkedIn Jobs connector** — once the public API stabilizes (currently rate-limited into uselessness for OSS tools)
- [ ] **Workday connector** — the white whale; non-trivial because every Workday instance is its own snowflake
- [ ] **SmartRecruiters + Recruitee + Personio** connectors
- [ ] **More LLM endpoints** — any local OpenAI-compatible server already works (MLX, Ollama, llama.cpp, vLLM); hosted ones like Together and OpenRouter need API-key support
- [ ] **Markdown briefing + per-role pitch files**: today results are one JSON file per day
- [ ] **Email-driven results delivery** — agent emails you the briefing instead of dropping it to disk
- [ ] **Browser-extension submit-on-your-behalf** — explicit per-role consent toggle, never silent
- [ ] **`.ics` calendar feed** — top roles drop on your calendar at apply-deadline
- [ ] **Multi-credential profiles** — score the same role against "founder-track me" and "IC-track me"
- [ ] **Negative-example training** — let the LLM learn from roles you marked `not_interested` last week

---

## 🤝 Contributing

Issues and PRs welcome. Especially:

1. **New ATS connectors** — bring your favorite company's job board into the allow-list.
2. **Better scoring prompts** — if you've tuned `prompts/scoring.md` to surface better signal, send a PR.
3. **More local-LLM backends** — keep us off the cloud.
4. **Real-world `credentials.md` templates** — the example in `examples/` is a generic engineer; we'd love variants for designers, GTM, applied research, comms, ops.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guide.

---

## 📜 License

MIT. Use it, fork it, ship it. Credit appreciated but not required.

---

<p align="center">
  <a href="../../stargazers"><img src="https://img.shields.io/github/stars/nicedreamzapp/job-search-agent-windows?style=for-the-badge&logo=github&color=f5c542&labelColor=1f2328" alt="GitHub stars"></a>
  <a href="../../network/members"><img src="https://img.shields.io/github/forks/nicedreamzapp/job-search-agent-windows?style=for-the-badge&logo=github&color=4c9a2a&labelColor=1f2328" alt="GitHub forks"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/📜_License-MIT-yellow?style=for-the-badge" alt="MIT"></a>
  <a href="#-privacy--local-first"><img src="https://img.shields.io/badge/🔒_Privacy-100%25_Local--First-success?style=for-the-badge" alt="100% Local-First"></a>
</p>

<p align="center">
  <a href="https://star-history.com/#nicedreamzapp/job-search-agent-windows&Date">
    <img src="https://api.star-history.com/svg?repos=nicedreamzapp/job-search-agent-windows&type=Date" width="540" alt="Star history">
  </a>
</p>

<p align="center">
  <strong>If this saved you 10 hours of job hunting, please ⭐ the repo.</strong>
</p>
