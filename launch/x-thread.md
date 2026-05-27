# X Thread — Launch Day

**Posting notes:** Post as a native thread (not a long-form). Reply to your own tweet each time, no quote-tweets. Drop the demo screenshot on tweet 3. First tweet must be ≤280 chars.

---

## Tweet 1 (hook — 268 chars)

I got tired of spraying resumes into LinkedIn's keyword roulette.

So I built an agent that reads my credentials, scores every new job posting against them locally on my laptop, and only surfaces the ones that actually fit.

It's open source. MIT. No SaaS. 🧵

---

## Tweet 2 (the problem)

LinkedIn / Wellfound / Indeed all optimize for THEIR funnel — more applications = more revenue.

Job-seeker side, the math is brutal: ~2% reply rate on cold applies, ~6 hours per serious cover letter.

The bottleneck isn't volume. It's signal. So I built for signal.

---

## Tweet 3 (architecture — drop screenshot here)

How it works:

1. You write ONE `credentials.md` — your real portfolio, in your words
2. Connectors pull job listings (Greenhouse, Lever, Ashby, RSS — extend as you like)
3. A local MLX model scores each role 0–100 against your file
4. You see only the >70s

[📸 attach a screenshot of the daily scored-jobs report here]

---

## Tweet 4 (the local-first part)

The scorer runs on-device via MLX (Apple Silicon) or llama.cpp.

Your resume, your salary expectations, your "I won't work for X industry" preferences — none of it leaves your machine.

Compare that to uploading your resume to an "AI job matcher" SaaS. Yeah.

---

## Tweet 5 (vs LinkedIn / Wellfound)

LinkedIn shows you what THEIR algorithm thinks you should see.
Wellfound shows you what startups paid to put in front of you.

This shows you what YOUR credentials file says fits.

Source-of-truth flips from the platform → to you.

---

## Tweet 6 (no auto-submit, intentionally)

What it does NOT do: auto-apply.

Auto-submitted applications are noise. Hiring managers can smell them.

This stops at "here are the 3 roles worth your Friday night." You still write the cover letter. The agent just makes sure it's worth writing.

---

## Tweet 7 (extensibility)

Everything is a plugin:

- New job board? Write a 40-line connector
- Different scoring rubric? Swap the prompt template
- Want Slack/Discord alerts instead of daily digest? One YAML edit

Built it for myself. Shipping it because friends kept asking for the binary.

---

## Tweet 8 (the ask)

If you're job-hunting in 2026 and the funnel is breaking you, give it a try:

→ github.com/USER/job-search-agent

MIT licensed. Runs entirely on your machine. No account required.

A ⭐ on the repo helps surface it to other tired job-seekers. 🙏

---

**Reply-guy ammo (use if a tweet blows up):**

- "Why not GPT-4 for scoring?" → Cost + privacy. A 7B local model is plenty accurate for a binary fit/no-fit decision. Save the cloud spend for cover letter drafting.
- "Doesn't this just reinvent LinkedIn alerts?" → LinkedIn alerts run on keywords + their ranking. This runs on a 2K-token portrait of YOU.
- "Can I use it for hiring (other side)?" → Not yet. Roadmap.
