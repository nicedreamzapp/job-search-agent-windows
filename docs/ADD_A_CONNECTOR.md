# Adding a new ATS connector

Adding support for a new ATS (Workday, Smartrecruiters, Recruitee, etc.)
is one Python file plus one dispatch-table entry. Here's the recipe.

## 1. Find the public API

Most ATSes expose a JSON endpoint for their job boards. Look at:

- A company's careers page on that ATS.
- Network tab in DevTools when the page loads.
- The ATS's own developer docs (search for "job board API" or
  "postings API").

You want an endpoint that:

- Returns JSON.
- Doesn't require an auth token (we want zero-config for users).
- Returns *all* open postings for a company in one call (paginate only
  if absolutely necessary).

If the endpoint requires an API key, document that requirement in the
connector and read the key from an env var like
`JOBSCOUT_<ATS>_API_KEY`.

## 2. Create the connector file

Copy `connectors/lever.py` as a template — it's the simplest of the
three. Then:

1. Update the docstring with the endpoint URL and an example response
   shape. Future you (and other contributors) will thank you.
2. Set the `SOURCE` constant to the lowercase ATS name.
3. Set `API_URL` with a `{slug}` placeholder.
4. Implement `fetch(slug)` — call the endpoint, catch all exceptions
   (return `[]` on failure), and map each posting through a `_normalize`
   helper.
5. Implement `_normalize(slug, raw)` to translate one provider posting
   into a `Job`. The required fields are `id`, `source`, `company_slug`,
   `company_name`, `title`, `location`, and `url`. Everything else is
   optional but useful.

Example skeleton:

```python
"""Workday connector.

Workday's public board endpoint is:

    https://{slug}.wd1.myworkdayjobs.com/wday/cxs/...

(Replace with the actual URL pattern you've validated.)
"""

from __future__ import annotations

import logging

from connectors.base import Job, http_get_json, strip_html

log = logging.getLogger(__name__)

SOURCE = "workday"
API_URL = "https://..."


def fetch(slug: str) -> list[Job]:
    try:
        payload = http_get_json(API_URL.format(slug=slug))
    except Exception as exc:  # noqa: BLE001
        log.warning("workday fetch failed for %s: %s", slug, exc)
        return []
    return [_normalize(slug, raw) for raw in payload.get("jobPostings", [])]


def _normalize(slug: str, raw: dict) -> Job:
    return Job(
        id=str(raw.get("bulletFields", [""])[0]),
        source=SOURCE,
        company_slug=slug,
        company_name=slug.title(),
        title=raw.get("title", ""),
        location=raw.get("locationsText", ""),
        url=f"https://{slug}.wd1.myworkdayjobs.com{raw.get('externalPath', '')}",
        description=strip_html(raw.get("description", "")),
        raw=raw,
    )
```

## 3. Register it

In `connectors/__init__.py`, expose `fetch`:

```python
from connectors.workday import fetch as fetch_workday

__all__ = [..., "fetch_workday"]
```

In `jobscout.py`, add an entry to the `CONNECTORS` dispatch table:

```python
CONNECTORS = {
    "ashby": fetch_ashby,
    "greenhouse": fetch_greenhouse,
    "lever": fetch_lever,
    "workday": fetch_workday,   # <-- new
}
```

## 4. Write a test

Drop `tests/test_workday.py` mirroring `tests/test_lever.py`. Mock the
HTTP layer by patching `connectors.base.http_get_json` so the test runs
offline:

```python
import unittest
from unittest.mock import patch

from connectors import workday


class TestWorkday(unittest.TestCase):
    def test_normalize_basic(self):
        sample = {"jobPostings": [{"title": "SWE", "locationsText": "Remote"}]}
        with patch("connectors.workday.http_get_json", return_value=sample):
            jobs = workday.fetch("acme")
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "SWE")
        self.assertEqual(jobs[0].source, "workday")
```

Optionally add a live smoke test gated on `JOBSCOUT_LIVE_TESTS=1`.

## 5. Add an example company

Add at least one company using the new ATS to
`examples/companies.example.json` so users can verify it works without
having to find a slug themselves.

## 6. Update docs

- Mention the new ATS in the README's "supported ATSes" list.
- If the new connector requires an env var or special config, document
  it in `examples/README.md`.

That's it. The pipeline is genuinely pluggable — every other layer
(filters, scorer, output) is ATS-agnostic and works on `Job` objects.
