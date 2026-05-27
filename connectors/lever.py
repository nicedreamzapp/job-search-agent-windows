"""Lever connector.

Lever exposes a public postings API at:

    https://api.lever.co/v0/postings/{slug}?mode=json

Response is a flat JSON array of postings:

    [
      {
        "id": "uuid",
        "text": "Senior Software Engineer",
        "categories": {
          "team": "Engineering",
          "department": "Product",
          "commitment": "Full-time",
          "location": "San Francisco"
        },
        "description": "<p>...</p>",
        "descriptionPlain": "...",
        "additional": "<p>...</p>",
        "additionalPlain": "...",
        "lists": [{"text": "...", "content": "<li>...</li>"}],
        "hostedUrl": "https://jobs.lever.co/<slug>/<uuid>",
        "applyUrl": "https://jobs.lever.co/<slug>/<uuid>/apply",
        "workplaceType": "remote" | "on-site" | "hybrid",
        ...
      }
    ]
"""

from __future__ import annotations

import logging

from connectors.base import Job, http_get_json

log = logging.getLogger(__name__)

SOURCE = "lever"
API_URL = "https://api.lever.co/v0/postings/{slug}?mode=json"


def fetch(slug: str) -> list[Job]:
    """Fetch all open postings for a Lever company.

    Args:
        slug: The Lever site slug, e.g. "netflix" for jobs.lever.co/netflix.

    Returns:
        Empty list on any failure — we never raise.
    """
    url = API_URL.format(slug=slug)
    try:
        payload = http_get_json(url)
    except Exception as exc:  # noqa: BLE001
        log.warning("lever fetch failed for %s: %s", slug, exc)
        return []

    # Lever's response is a top-level array, not an object.
    if not isinstance(payload, list):
        log.warning("lever fetch for %s returned unexpected shape: %s", slug, type(payload).__name__)
        return []

    return [_normalize(slug, raw) for raw in payload]


def _normalize(slug: str, raw: dict) -> Job:
    """Translate one Lever posting into our `Job` shape."""
    categories = raw.get("categories") or {}
    location = categories.get("location", "") or ""
    if raw.get("workplaceType") == "remote" and "remote" not in location.lower():
        location = f"{location} (Remote)" if location else "Remote"

    # Lever helpfully provides `descriptionPlain` and `additionalPlain`
    # alongside their HTML twins. We concatenate them: `description` is the
    # role overview and `additional` is the "About us" / EEO boilerplate.
    # The scorer benefits from having both since salary bands and visa
    # policy often live in the `additional` section.
    parts = []
    if raw.get("descriptionPlain"):
        parts.append(raw["descriptionPlain"])
    if raw.get("additionalPlain"):
        parts.append(raw["additionalPlain"])
    description = "\n\n".join(parts)

    return Job(
        id=str(raw.get("id", "")),
        source=SOURCE,
        company_slug=slug,
        company_name=slug.replace("-", " ").title(),
        title=raw.get("text", "") or "",
        location=location,
        url=raw.get("hostedUrl") or raw.get("applyUrl") or "",
        description=description,
        department=categories.get("department") or categories.get("team"),
        employment_type=categories.get("commitment"),
        raw=raw,
    )
