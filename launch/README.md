# Launch Content Pack — job-search-agent

This folder is everything you need to launch the `job-search-agent` repo on a single day. Eight files, ready to copy-paste.

## ⚠️ Before posting ANYTHING

Every file in this folder uses the placeholder `github.com/USER/job-search-agent` for the repo URL. **You must do a global find-and-replace on `USER` with your actual GitHub username (or org) before posting any of this.**

Also replace these other placeholders that appear in specific files:

- `INVITE-PLACEHOLDER` in `discord-announcement.md` — your Discord invite code
- `[REPORTER FIRST NAME]`, `[YOUR NAME]`, `[YOUR EMAIL]`, `[YOUR PORTFOLIO LINK]`, `[DAY]`, `[N]` in `email-to-tech-press.md`

A quick sanity check:

```bash
grep -rn "USER/job-search-agent\|PLACEHOLDER\|\[YOUR\|\[REPORTER\|\[N\]\|\[DAY\]" .
```

Should return zero hits before you send anything.

---

## The files

| File | Channel | One-line description |
|------|---------|---------------------|
| `hacker-news.md` | Hacker News | "Show HN" submission with first-comment body + 3 pre-drafted FAQ replies for predictable objections |
| `x-thread.md` | X (Twitter) | 8-tweet launch thread with hook tweet, architecture explainer, demo screenshot slot, and a star CTA |
| `linkedin-post.md` | LinkedIn | 1,772-char post with story-led lead, first-comment repo link, and reply templates for the first 90 min |
| `discord-announcement.md` | Discord | Two versions (short for #announcements, longer for #show-and-tell) ready to drop in existing communities |
| `reddit-r-machinelearning.md` | r/MachineLearning | `[P]` self-post with eval methodology + Spearman correlation numbers, mod-friendly framing |
| `reddit-r-cscareerquestions.md` | r/cscareerquestions | Job-seeker-framed self-post with 3 pre-drafted objection replies |
| `email-to-tech-press.md` | Tech reporters | 193-word cold email with subject-line options + a 4-day follow-up template |
| `README.md` | (this file) | Index, posting order, and sanity checklist |

---

## Recommended launch sequence

Optimal day is **Tuesday** (highest HN front-page conversion historically; Mon is too noisy, Fri reads as desperate).

| Time | Action | Why this slot |
|------|--------|---------------|
| **T+0** — Tue 9:00am PT | Submit Show HN post | Hits HN as US East Coast comes back from lunch and EU is winding down — peak voting window for the "new" page |
| **T+5min** | Post first comment on your HN submission | Anchors the conversation before randos do. Then walk away — HN hates authors who reply too aggressively early. |
| **T+30min** — 9:30am PT | Post X thread | Drives traffic to the repo during the HN climb window; ⭐ momentum reinforces the HN ranking |
| **T+2h** — 11:00am PT | Post LinkedIn (repo link in FIRST COMMENT, not the post) | Different audience from HN/X; LinkedIn's algorithm rewards comment engagement so reply to everything in the first 90 min |
| **T+4h** — 1:00pm PT | Discord announcement(s) | Your existing communities. Don't spam every Discord you've ever joined — 2-3 relevant servers max. |
| **T+24h** — Wed 9am PT | r/MachineLearning + r/cscareerquestions | Wait a day so the HN traction provides social proof in the Reddit post. Post in r/ML's monthly `[P]` thread, not standalone. |
| **T+72h** — Fri 9am PT | Email to tech press | Reporters want a number ("1.2k stars in 72 hours") more than a pitch. Wait until you have one. |

---

## Day-of operational checklist

Before T+0 on launch morning:

- [ ] Repo is public on GitHub
- [ ] README.md in the repo is final (sibling agent's deliverable)
- [ ] Code is final and `git clone && make install` actually works on a fresh machine
- [ ] A demo screenshot exists at a stable URL (for the X thread's tweet 3)
- [ ] All `USER` placeholders replaced in this folder
- [ ] Discord invite code ready
- [ ] First 5 ⭐ already on the repo (ask 5 friends the night before — this is not gaming, it's making sure HN visitors don't see a 0-star repo and bounce)
- [ ] You have 4 uninterrupted hours blocked for HN comment replies
- [ ] You have a clean screenshot/demo ready for the X thread

During T+0 to T+4h:

- [ ] Reply to every HN comment within ~30 min (but not in the first 5 min after each — let conversation develop)
- [ ] Reply to every LinkedIn comment in the first 90 min after posting
- [ ] Pin your X thread to your profile
- [ ] Don't pivot the messaging based on early hot takes — wait until at least T+4h before changing your story

---

## Style guardrails (applied across all files)

- No emojis in HN body (HN audience dislikes)
- Emojis OK in X thread and Discord; sparing in LinkedIn (1-2 max)
- Tone is confident, technical, builder-first — show, don't sell
- All copy generic enough to be posted as-is by the project maintainer (no personal narrative details that pin it to a specific human)
- Repo URL is the single source of truth; everything points there

---

## After-launch debrief checklist (T+1 week)

- [ ] GitHub stars count vs goal
- [ ] HN front-page peak position + duration
- [ ] X thread impressions / engagement
- [ ] LinkedIn post impressions
- [ ] Inbound issues + PRs (quality, not just count)
- [ ] Press replies (any reporter even acknowledging counts as a hit)
- [ ] Most common objection across all channels — feeds back into README + FAQ
