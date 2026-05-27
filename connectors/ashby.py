"""Ashby connector.

Ashby exposes a public posting API at:

    https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true

The response shape is:

    {
      "apiVersion": "1",
      "jobs": [
        {
          "id": "uuid",
          "title": "Software Engineer",
          "department": "Engineering",
          "team": "Platform",
          "location": "San Francisco",
          "employmentType": "FullTime",
          "publishedAt": "2026-01-15T12:00:00.000Z",
          "isListed": true,
          "isRemote": false,
          "descriptionPlain": "...",
          "descriptionHtml": "<p>...</p>",
          "jobUrl": "https://jobs.ashbyhq.com/<slug>/<uuid>",
          ...
        },
        ...
      ]
    }

Notable: `descriptionPlain` is already stripped of HTML, so we use that
directly. The `jobUrl` field is the canonical apply link.
"""

from __future__ import annotations

import logging

from connectors.base import Job, http_get_json

log = logging.getLogger(__name__)

SOURCE = "ashby"
API_URL = "https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"


def fetch(slug: str) -> list[Job]:
    """Fetch all listed jobs for an Ashby company board.

    Args:
        slug: The company's Ashby slug, e.g. "anthropic" for
            https://jobs.ashbyhq.com/anthropic.

    Returns:
        A list of normalized `Job` objects, or an empty list if the board
        is empty / private / unreachable. We never raise — the caller
        treats this as "best-effort fetch, move on if it fails."
    """
    url = API_URL.format(slug=slug)
    try:
        payload = http_get_json(url)
    except Exception as exc:  # noqa: BLE001 — see base.http_get_json docstring
        log.warning("ashby fetch failed for %s: %s", slug, exc)
        return []

    raw_jobs = payload.get("jobs", []) or []
    jobs: list[Job] = []
    for raw in raw_jobs:
        # Skip postings the company has unlisted but not yet deleted —
        # they're not actually open for application.
        if raw.get("isListed") is False:
            continue
        jobs.append(_normalize(slug, raw))
    return jobs


def _normalize(slug: str, raw: dict) -> Job:
    """Translate one Ashby job blob into our `Job` shape."""
    # Ashby gives us a plain-text description for free — prefer it over the
    # HTML variant since we'd just strip the HTML anyway.
    description = raw.get("descriptionPlain") or ""
    location = raw.get("location") or ""
    # Some Ashby boards include `secondaryLocations` for hybrid postings; we
    # append them so the filter layer's location-matching catches "Remote"
    # boards that primary on a city.
    secondary = raw.get("secondaryLocations") or []
    if secondary:
        extra = ", ".join(s.get("location", "") for s in secondary if s.get("location"))
        if extra:
            location = f"{location} / {extra}" if location else extra
    if raw.get("isRemote") and "remote" not in location.lower():
        location = f"{location} (Remote)" if location else "Remote"

    return Job(
        id=str(raw.get("id", "")),
        source=SOURCE,
        company_slug=slug,
        company_name=slug.replace("-", " ").title(),
        title=raw.get("title", "") or "",
        location=location,
        url=raw.get("jobUrl") or raw.get("applyUrl") or "",
        description=description,
        department=raw.get("department"),
        employment_type=raw.get("employmentType"),
        raw=raw,
    )
