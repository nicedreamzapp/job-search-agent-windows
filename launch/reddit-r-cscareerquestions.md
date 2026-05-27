# Reddit — r/cscareerquestions Self-Post

**Posting notes:** r/cscareerquestions is allergic to anything that smells like self-promotion. Lead with the job-seeker problem, not the tool. Don't link the repo in the title. Mention it once in the body and once in a comment. Be ready to defend "why not just use LinkedIn" three different ways.

---

## Title

`Stop spray-applying. Score your fit BEFORE writing the cover letter. (Open-source tool I built after burning a Friday night writing four cover letters.)`

## Flair

`Tools / Resources`

---

## Body

The math that broke me:

- ~2% reply rate on cold applications (your mileage varies; this is roughly the consensus on this sub)
- ~3-6 hours per genuinely-tailored cover letter
- Implied effort to one offer: dozens of cover letters, hundreds of hours

So the obvious move is to spray-apply with a generic letter and hope volume saves you. Except spray-applies get ghosted at an even higher rate, and recruiters are getting very good at spotting AI-generated boilerplate. The volume strategy is breaking.

The actual leverage point is filtering BEFORE you write the cover letter. If you can reliably identify the 3 roles in this week's pile that genuinely fit you, you can spend 6 hours on each, send three excellent applications, and beat the spray-and-pray crowd's reply rate by a wide margin.

That filtering step is what I automated. I'll describe the approach in case it's useful, then drop the repo at the bottom.

**The approach:**

1. Write ONE credentials file. Not a resume — a free-form 2,000-word document describing your real projects, the things you're actually good at, the things you'd refuse to work on, your comp floor, your geo constraints. The honest version. The version you'd never put on LinkedIn.

2. Set up connectors to the public ATS APIs — Greenhouse, Lever, Ashby. These cover most well-run tech companies. Indeed/LinkedIn aggregators are intentionally out of scope because the signal-to-noise is awful.

3. A local LLM (runs on your laptop, nothing uploaded) scores each new posting 0-100 against your credentials file. Daily digest of the >70s lands in your inbox or browser.

4. You write cover letters only for the daily-digest survivors. Because they actually fit, your letters are genuinely good and your reply rate climbs.

**What it deliberately doesn't do:**

- No auto-apply. Auto-submitted apps are noise. Recruiters can tell.
- No cloud inference. Your credentials file has stuff in it you wouldn't paste into a SaaS.
- No account creation. No data leaves your machine.

**Honest about limits:**

- It won't surface jobs that aren't on Greenhouse/Lever/Ashby. If you're hunting for FAANG-only or banking, this won't help — those have proprietary systems.
- It can't fix a weak credentials file. Garbage in, garbage out. The first 30 minutes of writing yours is the most leveraged time you'll spend.
- It's single-user. No team / partner / "spouse is also job-hunting" support yet.

**The repo:**

github.com/USER/job-search-agent — MIT licensed, runs on Apple Silicon out of the box. llama.cpp fallback for Linux/CUDA.

Built this for myself, shipping because friends kept asking for the binary. If you try it, an issue with feedback (especially "the connector for X is missing") is genuinely useful.

Stop spray-applying. The funnel is broken on the applicant side too — you just have to flip the source of truth from LinkedIn's algorithm to your own credentials file.

---

## Pre-drafted reply: "Why not just use LinkedIn alerts?"

> LinkedIn alerts run on keyword match against your structured profile. So if your profile says "Senior Software Engineer" and the job says "Staff Engineer," the keyword miss filters you out even when the role would be a perfect fit. The scoring model here reads a 2,000-word free-form portrait of you and reasons about fit — completely different signal. Same input data on LinkedIn's side, but their alert system isn't using it that way because their incentive is to keep you scrolling, not to give you the three best jobs and let you log off.

## Pre-drafted reply: "Sounds like overengineering for a problem I don't have"

> Probably! If you're in a hot market and getting recruiter DMs you don't need this. It's for the case where you're sending applications outbound and the funnel feels broken. If that's not you right now, save it for the next downturn.

## Pre-drafted reply: "Won't recruiters smell that this is AI-assisted?"

> The agent doesn't write the cover letter. It just decides which jobs deserve a hand-written cover letter from you. Output of the agent is a ranked list, not a generated artifact. You still write every word recruiters see.
