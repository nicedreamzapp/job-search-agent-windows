# Discord Announcement

**Posting notes:** Drop in the #announcements or #show-and-tell channel of an existing community (your own server, a builder/AI Discord you're a member of). Don't cross-post to every Discord you've ever joined — that reads as spam. Two or three relevant servers is the right number.

---

## Short version (for #announcements channels)

🚀 **Shipped a thing today: job-search-agent**

A local-first daily job scorer. You write one credentials file describing your real portfolio, and a local LLM scores every new job posting against it — only surfaces the roles that actually fit.

No SaaS. No auto-apply. No account. Runs on your laptop.

→ Repo: <https://github.com/USER/job-search-agent>
→ Server / chat about it: <https://discord.gg/INVITE-PLACEHOLDER>

If you know anyone job-hunting right now, throw them the link 🙏 — they're probably tired of LinkedIn's keyword roulette and this might save them a Friday night.

⭐ on the repo helps it find other tired job-seekers. MIT licensed, PRs welcome.

---

## Longer version (for #show-and-tell channels that allow more context)

Hey everyone — shipping something open-source today and wanted to share with this crowd first since y'all get it.

**job-search-agent** — a local-first daily job scorer.

The pitch: every job board is optimized for THEIR funnel, not yours. The result is the keyword-roulette experience we all know. So I built an agent that flips the source of truth:

→ You maintain ONE credentials file (your real portfolio, in your own words)
→ Connectors pull listings from public ATS APIs — Greenhouse, Lever, Ashby
→ A local LLM scores each role 0–100 against your file
→ Daily digest of just the roles worth your time

Three things it deliberately doesn't do:
- No auto-apply (auto-submitted apps are noise)
- No cloud inference (your credentials file stays on disk)
- No account / no telemetry / no SaaS

Single binary, runs on Apple Silicon out of the box, llama.cpp fallback for Linux.

Repo: <https://github.com/USER/job-search-agent>
MIT licensed. PRs especially welcome for new ATS connectors — the pattern is ~40 lines per source.

If you've got friends job-hunting, share it with them. The point is for tired job-seekers to find it.

Server invite for ongoing discussion: <https://discord.gg/INVITE-PLACEHOLDER>

⭐ on the repo would help a lot today — first 24 hours of a launch matter for surface area. Thanks 🙏
