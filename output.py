"""Output and state handling.

Three responsibilities:

1. **State** — `seen.json` in `JOBSCOUT_STATE_DIR` records every job we've
   already scored, keyed by `Job.global_id`. Re-runs same day skip already-
   seen jobs so we don't burn LLM tokens twice.

2. **Local result file** — every run writes `results/<YYYY-MM-DD>.json` with
   the full list of scored jobs. This is the human-readable output the
   user reviews each morning.

3. **Optional webhook** — if `JOBSCOUT_HQ_URL` is set, we POST the daily
   summary there too. Useful for piping results into a personal dashboard.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

from connectors.base import Job
from scorer import Score

log = logging.getLogger(__name__)


def state_dir() -> Path:
    """Resolve and create the state directory.

    Defaults to `$XDG_STATE_HOME/jobscout` (or `~/.local/state/jobscout` if
    XDG isn't set), per the XDG Base Directory spec. Override with the
    `JOBSCOUT_STATE_DIR` env var.
    """
    override = os.environ.get("JOBSCOUT_STATE_DIR")
    if override:
        path = Path(override).expanduser()
    else:
        xdg = os.environ.get("XDG_STATE_HOME")
        base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "state"
        path = base / "jobscout"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_seen() -> set[str]:
    """Load the set of global_ids we've already scored.

    Returns an empty set if the state file doesn't exist yet (first run)
    or if it's corrupt — we'd rather re-score than crash the daily job.
    """
    path = state_dir() / "seen.json"
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return set(data.get("seen", []))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("could not read state file %s: %s — starting fresh", path, exc)
        return set()


def save_seen(seen: set[str]) -> None:
    """Persist the set of already-scored global_ids."""
    path = state_dir() / "seen.json"
    tmp = path.with_suffix(".json.tmp")
    # Atomic write: write to tmp file, then rename. Avoids leaving a
    # half-written state file if the process dies mid-write.
    tmp.write_text(json.dumps({"seen": sorted(seen)}, indent=2), encoding="utf-8")
    tmp.replace(path)


def write_results(scored: list[tuple[Job, Score]], run_date: date | None = None) -> Path:
    """Write today's scored jobs to `results/<YYYY-MM-DD>.json`.

    Returns the path of the written file so the CLI can print it.
    """
    run_date = run_date or date.today()
    results_dir = state_dir() / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / f"{run_date.isoformat()}.json"

    payload = {
        "date": run_date.isoformat(),
        "count": len(scored),
        "jobs": [
            {
                **job.to_dict(),
                "score": score.score,
                "rationale": score.rationale,
                "pitch": score.pitch,
                "scoring_error": score.error,
            }
            for job, score in scored
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def post_to_webhook(payload: dict[str, Any]) -> bool:
    """POST the daily summary to a webhook if configured.

    The webhook URL comes from `JOBSCOUT_HQ_URL`. An optional bearer token
    can be set via `JOBSCOUT_HQ_TOKEN`. Returns True on 2xx, False otherwise.
    Never raises — webhook failures shouldn't break the daily run.
    """
    url = os.environ.get("JOBSCOUT_HQ_URL", "").strip()
    if not url:
        return False
    token = os.environ.get("JOBSCOUT_HQ_TOKEN", "").strip()

    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as exc:
        log.warning("webhook %s returned %s", url, exc.code)
        return False
    except Exception as exc:  # noqa: BLE001
        log.warning("webhook %s failed: %s", url, exc)
        return False
