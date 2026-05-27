# Contributing to job-search-agent

Thanks for considering a contribution. This project is small on purpose
and aims to stay that way. The bar is: does the change keep the tool
**stdlib-only, local-first, and easy to read in an evening**? If yes,
we'd love to see it.

## What we'd especially love

1. **New ATS connectors.** Workday, SmartRecruiters, Recruitee, Personio,
   Greenhouse Job Boards API variants, etc. See
   [`docs/ADD_A_CONNECTOR.md`](docs/ADD_A_CONNECTOR.md) for the pattern.
2. **Tuned prompts.** If you've improved `prompts/scoring.md` or
   `prompts/pitch.md` in a way that surfaces better signal, send a PR
   with a one-paragraph note on what you changed and why.
3. **More local-LLM backends.** Anything that speaks OpenAI-compatible
   chat-completions works out of the box; bug reports and tested setup
   notes for vLLM, llama.cpp, LM Studio, etc. are welcome.
4. **Real-world `credentials.md` templates.** The example in
   `examples/credentials.example.md` is a generic engineer. Variants for
   designers, GTM, applied research, comms, ops, etc. would help a lot
   of people.
5. **Bug fixes** in the connectors when an ATS subtly changes its
   response shape.

## Ground rules

- **Stdlib only in the runtime path.** No `pip install` dependency for
  end users. The optional `dev` extra in `pyproject.toml` is for linting
  and similar dev-time conveniences only.
- **Connectors must not raise.** One bad company should never kill the
  daily run. Log and return an empty list on failure.
- **Tests are required for new logic.** Tests use stdlib `unittest` and
  mock the HTTP layer by monkey-patching `connectors.base.http_get_json`.
  See `tests/test_ashby.py` for a template.
- **Keep the README claims true.** If you change behavior that the README
  describes, update the README in the same PR.

## Getting started

```bash
git clone https://github.com/USER/job-search-agent.git
cd job-search-agent
python3 -m unittest discover tests
```

If the test suite passes, you have a working dev setup. There is no
build step.

## Running the tool against a real config

```bash
mkdir -p ~/.config/jobscout
cp examples/companies.example.json   ~/.config/jobscout/companies.json
cp examples/credentials.example.md   ~/.config/jobscout/credentials.md
cp examples/filters.example.yml      ~/.config/jobscout/filters.yml
python3 jobscout.py --dry-run
```

`--dry-run` skips the LLM scoring step, so you can verify the connector
and filter layers without a model running.

## Submitting a PR

1. **One change per PR.** A new connector and a prompt tweak should be
   two PRs.
2. **Run the tests.** `python3 -m unittest discover tests` must pass.
3. **If you added a connector**, register it in `CONNECTORS` in
   `jobscout.py` and add a test file under `tests/`.
4. **Update docs** if your change is user-visible. The README, the
   `docs/` files, and the `examples/` are all fair game.

## Questions

Open an issue. We'd rather have a 30-second back-and-forth before you
spend an hour on a change than have you guess at the right approach.
