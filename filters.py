"""Hard-disqualifier filters.

Filters run *before* the LLM scorer. The whole point is to throw out
obvious-no jobs cheaply so we don't spend a model call on them. A filter
returns True to *keep* a job and False to drop it.

Rules are loaded from a YAML or JSON config; the example file at
`examples/filters.example.yml` documents every supported key. The config
schema is intentionally tiny — if you need more expressive filtering,
write a Python predicate in `custom_filter()` below and call it from
`apply()`.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from connectors.base import Job

log = logging.getLogger(__name__)


@dataclass
class FilterConfig:
    """Parsed filter rules.

    Every list is a list of *regex patterns* (case-insensitive). Empty lists
    mean "no rule of this kind" — i.e. don't drop anything for that reason.
    `require_locations_in` is the only allow-list rule: if non-empty, a job's
    location must match at least one pattern, or it's dropped.
    """

    drop_titles_matching: list[str] = field(default_factory=list)
    drop_descriptions_matching: list[str] = field(default_factory=list)
    drop_companies_matching: list[str] = field(default_factory=list)
    require_locations_in: list[str] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: Path) -> "FilterConfig":
        """Load rules from a YAML or JSON file.

        We prefer the stdlib, so YAML is parsed via a tiny hand-rolled
        loader that handles only the subset we use (top-level keys, lists
        of strings, and `#` comments). For anything fancier, use JSON —
        which the stdlib supports natively.
        """
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() in (".json",):
            data = json.loads(text)
        else:
            data = _parse_simple_yaml(text)
        return cls(
            drop_titles_matching=list(data.get("drop_titles_matching") or []),
            drop_descriptions_matching=list(data.get("drop_descriptions_matching") or []),
            drop_companies_matching=list(data.get("drop_companies_matching") or []),
            require_locations_in=list(data.get("require_locations_in") or []),
        )

    @classmethod
    def empty(cls) -> "FilterConfig":
        """A config that drops nothing. Useful for tests and `--no-filter` runs."""
        return cls()


def apply(jobs: list[Job], config: FilterConfig) -> tuple[list[Job], list[tuple[Job, str]]]:
    """Run the filter rules against a job list.

    Returns:
        A tuple `(kept, dropped)` where `dropped` is a list of
        `(job, reason)` so callers can log *why* something was thrown out.
        Verbose mode in the CLI prints these — invaluable for tuning
        filters that are too aggressive.
    """
    kept: list[Job] = []
    dropped: list[tuple[Job, str]] = []

    title_regexes = [re.compile(p, re.IGNORECASE) for p in config.drop_titles_matching]
    desc_regexes = [re.compile(p, re.IGNORECASE) for p in config.drop_descriptions_matching]
    company_regexes = [re.compile(p, re.IGNORECASE) for p in config.drop_companies_matching]
    location_regexes = [re.compile(p, re.IGNORECASE) for p in config.require_locations_in]

    for job in jobs:
        reason = _disqualify(job, title_regexes, desc_regexes, company_regexes, location_regexes)
        if reason:
            dropped.append((job, reason))
        else:
            kept.append(job)

    return kept, dropped


def _disqualify(
    job: Job,
    title_regexes: list[re.Pattern],
    desc_regexes: list[re.Pattern],
    company_regexes: list[re.Pattern],
    location_regexes: list[re.Pattern],
) -> str | None:
    """Return a reason string if the job should be dropped, else None.

    Order matters only for which reason gets reported first; a job that hits
    multiple rules is still dropped exactly once.
    """
    for pattern in title_regexes:
        if pattern.search(job.title):
            return f"title matches /{pattern.pattern}/"

    for pattern in company_regexes:
        if pattern.search(job.company_name) or pattern.search(job.company_slug):
            return f"company matches /{pattern.pattern}/"

    for pattern in desc_regexes:
        if pattern.search(job.description):
            return f"description matches /{pattern.pattern}/"

    if location_regexes:
        # Allow-list: at least one pattern must match.
        if not any(p.search(job.location) for p in location_regexes):
            return f"location {job.location!r} not in allowed set"

    return None


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """A 30-line YAML subset parser — top-level keys mapping to lists of strings.

    Why hand-roll this instead of `pip install pyyaml`? Keeping the dep
    surface at zero means `python3 jobscout.py` works on a fresh macOS
    install without `pip install` — which is the whole point of "anyone
    can run it." If you need real YAML, swap this for `yaml.safe_load`.

    Supported syntax:

        # comments
        key_name:
          - "item"
          - 'item'
          - item

    Anything else (nested maps, anchors, multi-line strings) is not
    supported. Use JSON for those cases.
    """
    result: dict[str, list[str]] = {}
    current_key: str | None = None

    for raw_line in text.splitlines():
        # Strip comments — but only outside quoted strings. Our subset
        # doesn't allow `#` inside list items, so this is safe.
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if not line.startswith(" ") and line.endswith(":"):
            current_key = line[:-1].strip()
            result[current_key] = []
            continue

        stripped = line.strip()
        if stripped.startswith("- ") and current_key is not None:
            item = stripped[2:].strip()
            # Strip surrounding quotes if present.
            if len(item) >= 2 and item[0] == item[-1] and item[0] in ("'", '"'):
                item = item[1:-1]
            result[current_key].append(item)

    return result
