# Reddit — r/MachineLearning Self-Post

**Posting notes:** r/MachineLearning is strict about flair and self-promotion. Post in the monthly `[P]` Project showcase thread (pinned at the top of the sub) rather than as a standalone — standalone project posts get nuked. If posting standalone, use the `[P]` flair and acknowledge the limitations up front (no novel research, no benchmarks paper). Mods care more about honesty than novelty.

---

## Title

`[P] job-search-agent — local-LLM-based job-role scorer trained on a free-form credentials file`

## Flair

`Project`

---

## Body

Up front: this is not research. There is no novel architecture, no SOTA benchmark, no ablation table. If you came for a paper, this is not it — sorry for the noise, the self-deprecating disclaimer is mandatory.

What it is: a small, opinionated, open-source tool that uses a local LLM as the scoring component in a personal job-search pipeline. Sharing because the engineering shape might be interesting to people building practical local-LLM apps, and because I think the eval methodology is mildly defensible.

**The setup:**

- Input A: a free-form Markdown file describing the user's full portfolio, constraints, and preferences (~2K tokens).
- Input B: a structured job listing pulled from a public ATS API (Greenhouse, Lever, Ashby).
- Task: produce a 0–100 fit score plus a one-paragraph rationale.

**The model:**

Default is Llama-3.1-8B-Instruct served via MLX on Apple Silicon (llama.cpp fallback for CUDA). The prompt is a chain-of-thought rubric that decomposes the score into five sub-scores (technical fit, seniority fit, comp fit, hard-constraint check, stage/culture fit) and aggregates. Greedy decoding, temperature 0.

**The "eval":**

Hand-labeled 200 job postings against a single credentials file with a 1–5 fit score, then computed Spearman ρ between human label and model score (rescaled to 1–5).

- Llama-3.1-8B-Instruct (local): ρ = 0.83
- Claude Sonnet 3.5 (API): ρ = 0.88
- GPT-4o (API): ρ = 0.86
- Bag-of-words logistic regression baseline (trained on the same 200): ρ = 0.61

The cloud models do better, but the gap is small enough that the privacy + cost wins (the credentials file stays on disk, $0/month) feel like the right tradeoff for this use case. The BoW baseline shows it's not a trivial keyword-match problem — the model is doing something useful with the free-form input.

**Honest limitations:**

- N=200 is tiny. Labels are from one annotator (me) with all the bias that implies.
- The credentials file is the most important input by far; quality is bounded by user effort there.
- No public eval set yet because the labels are tied to one person's career. Working on a synthetic eval but it's not great.

**What might be reusable:**

- The connector pattern for ATS APIs (~40 lines per source)
- The chain-of-thought scoring rubric (in `/docs/scoring-prompt.md`)
- The labeling + eval scripts (in `/eval/`)

Repo: github.com/USER/job-search-agent — MIT licensed.

Happy to discuss the eval methodology, the prompt design, or take pointers on how to make the eval less embarrassing.
