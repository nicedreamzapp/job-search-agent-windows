# Customizing the scoring rubric

The scorer is small on purpose: one prompt, one model call, one
0–100 number plus a rationale. Most of the "personality" of the
search comes from your `credentials.md`, not from the scorer code.

This doc covers what to tune, in order of leverage.

## 1. Tune `credentials.md` (highest leverage)

The single biggest determinant of score quality is how well your
profile describes what you actually want. The LLM is doing
straightforward "does this profile fit this JD?" reasoning — give it
specifics and you get specific scores.

**Good profile sections:**

- A "what I want next" list with 5–8 concrete signals. Tells the LLM
  exactly what a 90+ looks like.
- A "what I'm *not* looking for" list with hard exclusions. Tells the
  LLM what a 20 looks like.
- 3–5 specific shipped projects with quantified outcomes. Lets the
  LLM verify alignment with the role's stated impact areas.

**Bad profile sections:**

- "Looking for impactful work at a mission-driven company." This
  scores everything 60 because it matches everything.
- Bullet lists of every framework you've touched. The LLM doesn't
  care; recruiters' resume parsers do, and that's not who's reading
  this.
- More than ~1500 words. Crowds out the JD in the model's context.

A useful test: have a friend read your `credentials.md` and predict
how you'd score a sample JD. If they can't, the LLM can't either.

## 2. Tune `filters.yml` (second-highest leverage)

Anything you can disqualify with a regex shouldn't reach the LLM. Filters
are free; LLM calls are not. Common additions:

```yaml
drop_titles_matching:
  # Don't waste a score on roles you'd never take
  - "Manager"               # if you want IC only
  - "Director"
  - "Vice President"
  - "Sales\\b"
  - "Account Executive"

drop_descriptions_matching:
  - "in-office 5 days"      # if you want remote-friendly
  - "must be located in"    # often a hard location lock
  - "secret clearance"      # if you can't get one
```

Watch for over-filtering. Run `python3 jobscout.py --verbose` to see
*why* each posting was dropped — if you're losing roles you'd
actually consider, soften the regex.

## 3. Tune the prompt (lowest leverage but possible)

If you want to change *how* the LLM scores — e.g. ask it to weight
team size heavily, or to penalize ambiguous compensation — edit
[`prompts/scoring.md`](../prompts/scoring.md). For top-scoring roles
the scorer also drafts a ~200-word custom pitch using
[`prompts/pitch.md`](../prompts/pitch.md); edit that file to change
the voice, length, or structure of the auto-drafted pitch.

Both prompt files use `{name}` placeholders that get filled in at
runtime (`{credentials_text}`, `{title}`, `{company_name}`,
`{location}`, `{department}`, `{url}`, `{description}`). The default
scoring prompt asks for honesty and defines 70+ as "would actually
recommend you apply"; that anchor sets the scale.

If you change the prompts:

- Keep the JSON output shape — scoring returns
  `{"score": int, "rationale": str}` and pitch returns
  `{"pitch": str}`. If you change either, also update
  `_parse_json_response` in `scorer.py`.
- Test on 10–20 known roles before trusting the new scoring. A small
  prompt change can shift scores by 15 points.
- Consider adding a `prompt_version` field to the output JSON so you
  can diff scoring runs across prompt revisions.

## 4. Pick a better model

The default local model (`mlx-community/Llama-3.1-8B-Instruct-4bit`)
is fast and free but only "good enough." For more reliable scoring:

- **Local upgrade:** swap in a 70B-class model if your hardware allows.
  Set `JOBSCOUT_LLM_MODEL` to the model name your server exposes.
- **Cloud upgrade:** set `ANTHROPIC_API_KEY`. Set
  `JOBSCOUT_ANTHROPIC_MODEL` to pick a specific Claude model. A daily
  scoring run across 50 jobs costs cents on Sonnet.

The privacy/cost tradeoff is yours. The default optimizes for "never
leaves the machine"; the Anthropic path optimizes for score quality.

## 5. Two-pass scoring (advanced)

For high-volume runs, consider a two-pass setup:

1. Cheap pass: score with the local 8B model. Drop anything under 60.
2. Expensive pass: re-score the survivors with a stronger model.

You'd implement this by running `jobscout.py` twice — first with the
local model, then again with `ANTHROPIC_API_KEY` set, reading the
first pass's results and only re-scoring the top N. The current
codebase doesn't ship this out of the box because most users find a
single pass with a decent model is plenty.

## A debugging checklist

If scores look wrong, walk through these in order:

- [ ] Is `credentials.md` specific enough? (paste it into ChatGPT and
      ask it what kind of roles you'd recommend you for — if the
      answer is vague, your file is vague)
- [ ] Are filters too lenient? (lots of junk reaching the scorer means
      lots of false 60s)
- [ ] Is the model too small? (8B models can be fooled by buzzword
      density; try the Anthropic path on a problem case)
- [ ] Is the JD description being truncated? (long JDs get cut at
      6000 chars; check the `raw` field of the offending job)
- [ ] Is the LLM returning malformed JSON? (look for `scoring_error`
      in the results file)
