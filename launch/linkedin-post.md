# LinkedIn Post — Launch Day

**Posting notes:** Post Tuesday ~11am PT (2pm ET). LinkedIn's algorithm rewards posts that hold attention in the first 90 minutes — reply to every comment in that window. Keep emojis to 1-2 max. No links in the post body itself (LinkedIn deboosts external links); drop the repo link in the FIRST COMMENT, not the post.

---

## Post body (1,772 chars)

I spent six hours one Friday night writing four cover letters and submitting four job applications.

By 2am I realized something embarrassing: the actual hard part wasn't writing. It was deciding which four roles deserved the effort in the first place.

Every job board — LinkedIn included — is optimized for the platform's funnel, not the applicant's signal. The result is the same loop every job-seeker knows: scroll, doubt, apply anyway, get ghosted.

So I built an agent to flip the source of truth.

→ You write ONE credentials file: real portfolio, real constraints, real comp expectations.
→ The agent pulls listings from public ATS APIs (Greenhouse, Lever, Ashby).
→ A local LLM — running on your laptop, nothing uploaded — scores each role 0-100 against your file.
→ You get a daily digest of just the roles that fit.

Three deliberate design calls:

1. NO auto-apply. Auto-submitted applications are noise. The agent stops at "this one is worth your Friday night."

2. Local-only inference. Your credentials file probably contains current salary, industries you won't work in, and other things you'd never paste into a SaaS "AI job matcher." It stays on disk.

3. The credentials file is your portfolio in YOUR words. Not LinkedIn's structured fields. Not a parsed PDF. A free-form document the model can actually understand.

It's open-source, MIT licensed, single binary, runs on Apple Silicon out of the box.

If you're job-hunting in 2026 and tired of LinkedIn's keyword roulette, try running it on your own machine. It's local, it's free, and the only person who sees your credentials is you.

Repo link in the first comment.

#OpenSource #JobSearch #AIAgents #LocalLLM #BuildInPublic

---

## First comment (post immediately after)

Repo here: github.com/USER/job-search-agent

PRs welcome — especially for new ATS connectors. The pattern is ~40 lines per source.

---

## Reply templates (queue these for the first 90 min of comment activity)

**For "how does the local LLM work?":**
> Default is a 7B Llama variant via MLX on Apple Silicon. ~4GB RAM footprint, ~2 seconds per job. The scorer is a clean interface though — you can swap to llama.cpp, Ollama, or pipe to Claude/GPT if you'd rather pay for cloud inference. Repo has a swap example in /docs.

**For "isn't this just LinkedIn alerts?":**
> LinkedIn alerts run on keyword match against your profile fields. This runs an actual fit-evaluation over a 2K-token portrait of your career, projects, and constraints. Very different signal.

**For "can I use this for hiring (other side)?":**
> Not yet — currently single-user job-seeker tooling. The scoring rubric flips naturally for the other side though, so it's on the roadmap. Open an issue if you'd use it.

**For recruiters trying to DM you about a role:**
> Polite redirect: "Appreciate it — currently focused on shipping the tool. If your role is on a Greenhouse/Lever/Ashby board, the agent will surface it. ;)"
