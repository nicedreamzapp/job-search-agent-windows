"""Greenhouse connector.

Greenhouse exposes a public job-board API at:

    https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true

`content=true` includes the HTML description in the same response — without
it you'd have to make a second call per job, which gets rude at scale.

Response shape:

    {
      "jobs": [
        {
          "id": 123,
          "internal_job_id": 456,
          "title": "Engineering Manager",
          "updated_at": "2026-01-15T10:00:00-08:00",
          "location": {"name": "San Francisco, CA"},
          "absolute_url": "https://boards.greenhouse.io/<slug>/jobs/123",
          "content": "<p>...</p>",
          "departments": [{"id": 1, "name": "Engineering"}],
          "offices": [{"id": 1, "name": "San Francisco"}],
          "metadata": [...]
        }
      ],
      "meta": {"total": 50}
    }
"""

from __future__ import annotations

import logging

from connectors.base import Job, http_get_json, strip_html

log = logging.getLogger(__name__)

SOURCE = "greenhouse"
API_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"


def fetch(slug: str) -> list[Job]:
    """Fetch all open jobs for a Greenhouse board.

    Args:
        slug: The board token, e.g. "anthropic" for
            boards.greenhouse.io/anthropic. Note Greenhouse calls this the
            "board token" — most companies use their company name, but a
            few have custom tokens (e.g. "stripe" not "stripeinc").

    Returns:
        Empty list on any failure — we never raise.
    """
    url = API_URL.format(slug=slug)
    try:
        payload = http_get_json(url)
    except Exception as exc:  # noqa: BLE001
        log.warning("greenhouse fetch failed for %s: %s", slug, exc)
        return []

    raw_jobs = payload.get("jobs", []) or []
    return [_normalize(slug, raw) for raw in raw_jobs]


def _normalize(slug: str, raw: dict) -> Job:
    """Translate one Greenhouse job blob into our `Job` shape."""
    location = ""
    loc = raw.get("location")
    if isinstance(loc, dict):
        location = loc.get("name", "") or ""
    elif isinstance(loc, str):
        location = loc

    departments = raw.get("departments") or []
    department = departments[0].get("name") if departments and isinstance(departments[0], dict) else None

    # Greenhouse's `content` is HTML-encoded HTML (e.g. &lt;p&gt;...) in some
    # boards and plain HTML in others. `strip_html` handles both: it decodes
    # entities first, then strips tags.
    description = strip_html(raw.get("content", "") or "")

    return Job(
        id=str(raw.get("id", "")),
        source=SOURCE,
        company_slug=slug,
        company_name=slug.replace("-", " ").title(),
        title=raw.get("title", "") or "",
        location=location,
        url=raw.get("absolute_url", "") or "",
        description=description,
        department=department,
        employment_type=None,  # Greenhouse doesn't expose this in the public API.
        raw=raw,
    )
