# Hacker News — Show HN Post

**Posting notes:** Submit Tuesday 9am PT (12pm ET). Title matters more than body for HN ranking. Don't edit the post after submission — title edits are penalized. First comment from your account within 5 min, dropping a "how it works under the hood" technical note to anchor the conversation. Then walk away for 90 minutes — HN dislikes authors who reply too aggressively in the first hour.

---

## Title

`Show HN: Job-search-agent – Local-first daily job scorer using your full portfolio`

## URL field

`https://github.com/USER/job-search-agent`

## Text field (leave blank)

(HN convention: if you have a repo, the URL goes in the URL field and the text field stays empty. Your top-level comment is where the body lives.)

---

## First comment (post immediately after submission)

I built this after burning a Friday night writing four cover letters by hand and realizing the actual bottleneck wasn't writing — it was deciding which roles deserved the effort. Existing job boards optimize for application volume, not signal.

The architecture is intentionally boring:

1. You maintain one `credentials.md` file — your real portfolio, projects, salary expectations, hard constraints. This is the source of truth, not LinkedIn's structured fields.
2. Connectors poll public job APIs (Greenhouse, Lever, Ashby boards, a few RSS feeds) on a cron. Easy to extend — each connector is ~40 lines.
3. A local LLM scores each job 0–100 against the credentials file. Default is a 7B MLX model on Apple Silicon; llama.cpp fallback for Linux/CUDA.
4. Daily digest of roles scoring above your threshold. That's it.

What it explicitly does NOT do: auto-apply. Auto-submitted applications are noise on both sides of the market. The agent stops at "these three are worth your Friday night."

Anticipating the obvious objection — "isn't this what LinkedIn / Wellfound / Indeed already do?" Sort of, but their ranking is optimized for THEIR engagement metric (you click, you apply, they monetize). The fit signal is one input among many, and it's based on whatever keywords you stuffed into your profile. Here the ranking IS the fit signal, computed from a free-form portfolio file that's allowed to be 2,000 tokens of nuance.

Local-only because the credentials file contains things you wouldn't paste into a SaaS "AI job matcher" — current salary, the industries you refuse to work in, the founder you don't want to work for again. Stays on disk.

MIT licensed. Currently single-user. Repo: github.com/USER/job-search-agent. Happy to answer questions about the connector pattern or the scoring rubric.

---

## Comment-ready FAQ (paste replies as questions come in)

### Objection 1: "Why a local LLM? Just use GPT-4 / Claude API"

Three reasons:

1. The credentials file is the most sensitive thing in this system. Current comp, family situation, industries you've burned bridges in. None of that should hit a SaaS log.
2. The task — score a job posting 0–100 against a portfolio — is well within a 7B model's capability. Spent a weekend evaluating Llama-3.1-8B-Instruct vs Claude Sonnet on 200 manually-labeled jobs. Spearman correlation was 0.83. Good enough.
3. Cost. Running this on ~500 jobs/week against an API would be $15-30/month per user. On-device is free after the model download.

That said, the scorer is pluggable. If you want to pipe it to Claude/GPT, swap the `Scorer` class. Roughly 30 lines.

### Objection 2: "How does this scale past your curated allow-list of job boards?"

Honestly, it doesn't, and that's the point. Greenhouse + Lever + Ashby cover the vast majority of well-run tech companies' postings. Indeed/LinkedIn aggregator scraping is a different problem (ToS, rate limits, low signal-to-noise). The deliberate stance is: a curated set of high-signal sources beats a firehose. If you want firehose, the existing job boards have it.

Connector pattern is documented — adding a new source is ~40 lines. Pull requests welcome.

### Objection 3: "Privacy — what actually leaves my machine?"

Inbound only. The job boards' public APIs return listing JSON. That's the only network traffic from the agent. No telemetry, no analytics, no account creation, no auth server. `lsof -i` is your friend if you want to verify.

The credentials file, scoring prompts, model weights, and digest output all stay local. The daily digest is rendered as static HTML in `~/.job-search-agent/digest/` and opens in your browser. No third-party rendering.
