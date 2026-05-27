#!/usr/bin/env python3
"""Job Search Agent — daily curated job search across multiple ATS providers.

Run once a day (manually or via a LaunchAgent / cron):

    python jobscout.py [--dry-run] [--companies-only=slug1,slug2] [--verbose] [--no-llm]

What it does:

1. Reads the user's company allow-list from `$JOBSCOUT_CONFIG_DIR/companies.json`.
2. Fetches all open jobs from each company's ATS (Ashby / Greenhouse / Lever).
3. Drops obvious mismatches using filters from `filters.yml`.
4. Skips jobs we've already scored (state in `$JOBSCOUT_STATE_DIR/seen.json`).
5. Scores remaining jobs with a local MLX server (or Anthropic API if
   `ANTHROPIC_API_KEY` is set) using `credentials.md` as the profile.
6. Writes results to `$JOBSCOUT_STATE_DIR/results/<date>.json` and
   optionally POSTs to a webhook.

Privacy by default: nothing leaves your machine unless you explicitly
configure a webhook or the Anthropic fallback.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from connectors import fetch_ashby, fetch_greenhouse, fetch_lever
from connectors.base import Job
from filters import FilterConfig, apply as apply_filters
from output import load_seen, post_to_webhook, save_seen, state_dir, write_results
from scorer import Score, score_job

log = logging.getLogger("jobscout")


# Dispatch table from ATS name (as it appears in companies.json) to the
# connector function. To support a new ATS, add a module under
# `connectors/` and register it here. That's the entire integration step.
CONNECTORS = {
    "ashby": fetch_ashby,
    "greenhouse": fetch_greenhouse,
    "lever": fetch_lever,
}


@dataclass
class CompanyEntry:
    """One row from companies.json.

    Attributes:
        slug: The company's slug on its ATS.
        ats: Lowercase ATS name — must be a key in `CONNECTORS`.
        name: Optional human-readable name (overrides the slug-derived default).
    """

    slug: str
    ats: str
    name: str | None = None


def config_dir() -> Path:
    """Resolve the config directory.

    Defaults to `$XDG_CONFIG_HOME/jobscout` (or `~/.config/jobscout`).
    Override with `JOBSCOUT_CONFIG_DIR`.
    """
    override = os.environ.get("JOBSCOUT_CONFIG_DIR")
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / "jobscout"


def load_companies(path: Path) -> list[CompanyEntry]:
    """Read companies.json. Each entry must have `slug` and `ats` keys.

    A `name` key is optional. Unknown ATS values are dropped with a
    warning so a typo in one entry doesn't kill the run.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    out: list[CompanyEntry] = []
    for i, entry in enumerate(data):
        if not isinstance(entry, dict) or "slug" not in entry or "ats" not in entry:
            log.warning("companies.json entry %d missing slug/ats — skipping", i)
            continue
        ats = entry["ats"].lower()
        if ats not in CONNECTORS:
            log.warning("companies.json entry %d uses unknown ats %r — skipping", i, ats)
            continue
        out.append(CompanyEntry(slug=entry["slug"], ats=ats, name=entry.get("name")))
    return out


def load_credentials(path: Path) -> str:
    """Read the credentials markdown profile.

    Returns an empty string if missing — the scorer will still run but
    will produce noise. Tests use this path to exercise the no-LLM path.
    """
    if not path.exists():
        log.warning("credentials.md not found at %s — scoring will be weak", path)
        return ""
    return path.read_text(encoding="utf-8")


def fetch_all(companies: list[CompanyEntry]) -> tuple[list[Job], dict[str, int]]:
    """Fetch jobs from every configured company.

    Returns:
        `(jobs, counts)` where `counts` maps "<ats>:<slug>" to the number
        of jobs fetched. Used by the CLI to print a per-company summary.
    """
    all_jobs: list[Job] = []
    counts: dict[str, int] = {}
    for company in companies:
        fetcher = CONNECTORS[company.ats]
        try:
            jobs = fetcher(company.slug)
        except Exception as exc:  # noqa: BLE001 — defensive: one bad company shouldn't kill the run
            log.warning("connector %s/%s raised unexpectedly: %s", company.ats, company.slug, exc)
            jobs = []
        # Apply the human-readable override if provided.
        if company.name:
            for job in jobs:
                job.company_name = company.name
        counts[f"{company.ats}:{company.slug}"] = len(jobs)
        all_jobs.extend(jobs)
        log.info("fetched %d jobs from %s/%s", len(jobs), company.ats, company.slug)
    return all_jobs, counts


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a Unix exit code.

    Special-case the `setup` subcommand before argparse runs: it has its
    own arg parser and entirely separate question-driven flow, and we
    don't want to muddy the main daily-run flags with wizard-specific
    options. Users invoke it as `python jobscout.py setup [--web]`.
    """
    raw_args = sys.argv[1:] if argv is None else argv
    if raw_args and raw_args[0] == "setup":
        # Defer the import so a bad/missing setup.py never breaks daily runs.
        from setup import main as setup_main

        return setup_main(raw_args[1:])

    parser = argparse.ArgumentParser(
        description="Daily job-search agent. Fetches openings from configured companies, filters them, and scores fit with an LLM.",
        epilog=(
            "First-time setup? Run `python jobscout.py setup` for a friendly Q&A "
            "wizard that writes your credentials.md for you. Add --web to do it "
            "in a browser instead."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and filter but skip the LLM scoring step. Useful for testing connectors.",
    )
    parser.add_argument(
        "--companies-only",
        metavar="SLUG1,SLUG2",
        default="",
        help="Comma-separated list of company slugs to fetch (default: all configured).",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Alias for --dry-run. Skip scoring.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose logging including filter drop reasons.",
    )
    parser.add_argument(
        "--config-dir",
        metavar="DIR",
        default=None,
        help="Override the config directory (default: $JOBSCOUT_CONFIG_DIR or ~/.config/jobscout).",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    if args.config_dir:
        os.environ["JOBSCOUT_CONFIG_DIR"] = args.config_dir
    cfg_dir = config_dir()
    companies_path = cfg_dir / "companies.json"
    filters_path_yml = cfg_dir / "filters.yml"
    filters_path_json = cfg_dir / "filters.json"
    credentials_path = cfg_dir / "credentials.md"

    if not companies_path.exists():
        print(
            f"ERROR: no companies.json found at {companies_path}.\n"
            f"Copy examples/companies.example.json into {cfg_dir} to get started.",
            file=sys.stderr,
        )
        return 2

    companies = load_companies(companies_path)
    if args.companies_only:
        wanted = {s.strip() for s in args.companies_only.split(",") if s.strip()}
        companies = [c for c in companies if c.slug in wanted]
        log.info("filtered to %d companies via --companies-only", len(companies))

    if filters_path_yml.exists():
        filters = FilterConfig.from_file(filters_path_yml)
    elif filters_path_json.exists():
        filters = FilterConfig.from_file(filters_path_json)
    else:
        log.info("no filters.yml or filters.json found — running with no filters")
        filters = FilterConfig.empty()

    jobs, counts = fetch_all(companies)
    print(f"Fetched {len(jobs)} jobs across {len(companies)} companies.", file=sys.stderr)
    for key, count in counts.items():
        print(f"  {key}: {count}", file=sys.stderr)

    kept, dropped = apply_filters(jobs, filters)
    print(f"After filters: {len(kept)} kept, {len(dropped)} dropped.", file=sys.stderr)
    if args.verbose:
        for job, reason in dropped:
            log.debug("dropped %s (%s) — %s", job.title, job.company_name, reason)

    # Dedup against state — skip anything we've already scored.
    seen = load_seen()
    fresh = [j for j in kept if j.global_id not in seen]
    print(f"After dedup: {len(fresh)} new jobs to score ({len(kept) - len(fresh)} already seen).", file=sys.stderr)

    if args.dry_run or args.no_llm:
        print("--dry-run / --no-llm: skipping scoring.", file=sys.stderr)
        # Still write a results file so the user can see what would have been scored.
        scored = [(j, Score(score=0, rationale="(dry run — not scored)")) for j in fresh]
    else:
        credentials_text = load_credentials(credentials_path)
        scored = []
        for i, job in enumerate(fresh, start=1):
            log.info("scoring %d/%d: %s — %s", i, len(fresh), job.company_name, job.title)
            result = score_job(job, credentials_text)
            scored.append((job, result))
            if result.error:
                log.warning("scoring error for %s: %s", job.global_id, result.error)

    # Sort by score descending so the user sees the best fits first.
    scored.sort(key=lambda pair: pair[1].score, reverse=True)

    # Persist state and write results.
    seen.update(j.global_id for j in fresh)
    save_seen(seen)
    results_path = write_results(scored)
    print(f"Wrote {len(scored)} scored jobs to {results_path}", file=sys.stderr)

    # Optional webhook.
    webhook_payload = {
        "date": results_path.stem,
        "count": len(scored),
        "top": [
            {
                **job.to_dict(),
                "score": score.score,
                "rationale": score.rationale,
                "pitch": score.pitch,
            }
            for job, score in scored[:10]
        ],
    }
    if post_to_webhook(webhook_payload):
        print("Posted summary to webhook.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
