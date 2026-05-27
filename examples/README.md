# Examples — copy these into your config dir

`job-search-agent` looks for its config in `$JOBSCOUT_CONFIG_DIR`
(default `~/.config/jobscout`). Bootstrap your local setup by copying the
files in this folder there, then editing them:

```bash
mkdir -p ~/.config/jobscout
cp examples/companies.example.json     ~/.config/jobscout/companies.json
cp examples/filters.example.yml        ~/.config/jobscout/filters.yml
cp examples/credentials.example.md     ~/.config/jobscout/credentials.md
```

Then edit each file for your situation:

| File | What to change |
|---|---|
| `companies.json` | Add/remove companies. Each entry needs `slug` and `ats` (one of `ashby`, `greenhouse`, `lever`). To find a company's slug, look at its careers page URL — most ATSes put the slug in the path. |
| `filters.yml` | Tune the disqualifier rules. The example assumes a senior IC who doesn't want internships, junior roles, degree-gated postings, or regulated-finance work. Adjust for your situation. |
| `credentials.md` | **Rewrite this entirely as you.** It's the candidate profile the LLM scores every role against. Be specific about what you've shipped and what you want next — vague aspirations score poorly. |

## What's in each example

### `companies.example.json`

Thirteen well-known AI / dev-tools companies with their real ATS slugs.
Running `python3 jobscout.py --dry-run` with this file as-is should fetch
several hundred jobs across the list, so you can verify everything wires
up before you customize.

> ⚠️ Slugs change over time as companies migrate between ATSes. If a
> connector returns 0 jobs for a company you know is hiring, check whether
> they've moved to a different ATS recently.

### `filters.example.yml`

A starter set of disqualifier patterns plus a remote-or-US location
allow-list. The format is documented inline. Note that we use a tiny
hand-rolled YAML parser (stdlib-only goal), so syntax is restricted to
top-level keys mapping to lists of strings — if you need richer config,
rename to `filters.json` and use JSON.

### `credentials.example.md`

A fictional senior backend engineer named Jane Doe. About 800 words. Use
it as a template — the structure (snapshot, what you've shipped, what
you want next, tools, fit signals) is what makes the LLM score reliably.
A one-line profile will give you noisy scores; a war-and-peace résumé
will crowd out the job description in the model's context.
