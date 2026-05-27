"""ATS connectors.

Each connector module exposes a `fetch(slug: str) -> list[Job]` function that
returns all currently-open postings for a company's board on that ATS.

Adding a new ATS is one file in this package plus an entry in the dispatch
table in `jobscout.py`. See `docs/ADD_A_CONNECTOR.md` for the recipe.
"""

from connectors.ashby import fetch as fetch_ashby
from connectors.base import Job
from connectors.greenhouse import fetch as fetch_greenhouse
from connectors.lever import fetch as fetch_lever

__all__ = ["Job", "fetch_ashby", "fetch_greenhouse", "fetch_lever"]
