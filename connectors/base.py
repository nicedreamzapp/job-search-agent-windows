"""Shared types and helpers for all ATS connectors.

Every connector returns a list of `Job` dataclasses with a consistent shape so
the filter and scorer layers can be ATS-agnostic. New connectors should import
from this module rather than inventing their own job representation — that
keeps the rest of the pipeline pluggable.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from typing import Any


# A 10-second connect/read timeout strikes the right balance: most ATS APIs
# respond in well under a second, but we don't want a single slow company to
# stall the whole daily run. The connector layer catches the timeout and moves
# on to the next company.
HTTP_TIMEOUT_SECONDS = 10

# Identify ourselves so ATS operators can see who is hitting their public
# endpoints. Using a real URL here is good neighborliness — it lets them reach
# out if our crawl pattern ever causes them trouble.
USER_AGENT = "job-search-agent/0.1 (+https://github.com/your-org/job-search-agent)"


@dataclass
class Job:
    """A normalized job posting from any ATS.

    Connectors are responsible for translating their provider-specific JSON
    into this shape. Downstream code (filters, scorer, output) only ever
    touches `Job` — it never reads raw ATS responses.

    Attributes:
        id: Stable identifier within the source ATS. Combined with `source`
            and `company_slug` to form the global dedup key.
        source: Lowercase ATS name, e.g. "ashby", "greenhouse", "lever".
        company_slug: The slug used to query this company on the ATS, e.g.
            "anthropic" for boards-api.greenhouse.io/v1/boards/anthropic.
            Useful when the same company is later requested again.
        company_name: Human-readable company name as the ATS reports it.
        title: Job title exactly as posted.
        location: Free-form location string. ATSes are wildly inconsistent
            here ("Remote", "San Francisco, CA", "US-Remote / NY"); the
            filter layer does the messy normalization, not the connector.
        url: Canonical apply URL the user would visit.
        description: Plain-text job description. Connectors should strip
            HTML before storing here — the scorer works much better on text.
        department: Optional department/team name when the ATS exposes one.
        employment_type: Optional "Full time" / "Contract" etc. when known.
        raw: The original ATS response payload for this posting, kept for
            debugging and for future fields we haven't normalized yet.
    """

    id: str
    source: str
    company_slug: str
    company_name: str
    title: str
    location: str
    url: str
    description: str = ""
    department: str | None = None
    employment_type: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def global_id(self) -> str:
        """Stable cross-ATS identifier used for deduplication in state."""
        return f"{self.source}:{self.company_slug}:{self.id}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize for JSON output. Drops `raw` to keep files small."""
        d = asdict(self)
        d.pop("raw", None)
        return d


def http_get_json(url: str, timeout: int = HTTP_TIMEOUT_SECONDS) -> Any:
    """GET a URL and parse the response as JSON.

    Raises:
        urllib.error.URLError: on network / DNS failures.
        urllib.error.HTTPError: on non-2xx responses.
        json.JSONDecodeError: if the body isn't valid JSON.

    We deliberately surface exceptions to the connector layer so each
    connector can decide how to handle partial failure (most just log and
    return an empty list — one bad company shouldn't kill the run).
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_html(html: str) -> str:
    """Crude HTML-to-text conversion using stdlib only.

    We tag-strip, decode entities, and collapse whitespace. This is sufficient
    for LLM scoring — we don't need perfect fidelity, we need readable text
    without markup noise inflating the token count.
    """
    if not html:
        return ""
    import html as html_module
    import re

    # Drop script/style blocks wholesale before tag-stripping so their contents
    # don't end up in the output text.
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    # Replace block-level closing tags with newlines so paragraph structure
    # survives — the LLM scorer benefits from seeing list items as lines.
    html = re.sub(r"</(p|div|li|h[1-6]|br|tr)>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    # Strip all remaining tags.
    html = re.sub(r"<[^>]+>", " ", html)
    # Decode HTML entities (&amp;, &#39;, &nbsp; etc.).
    html = html_module.unescape(html)
    # Collapse runs of whitespace, but keep newlines.
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n[ \t]*", "\n", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()
