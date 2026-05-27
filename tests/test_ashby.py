"""Unit tests for the Ashby connector.

The unit tests monkey-patch `http_get_json` so they run offline. A live
smoke test runs only when `JOBSCOUT_LIVE_TESTS=1` is set in the environment
so CI doesn't hammer real ATSes.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Allow `python3 -m unittest discover tests` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from connectors import ashby  # noqa: E402


SAMPLE_RESPONSE = {
    "apiVersion": "1",
    "jobs": [
        {
            "id": "abc-123",
            "title": "Senior Software Engineer",
            "department": "Engineering",
            "team": "Platform",
            "location": "San Francisco",
            "employmentType": "FullTime",
            "isListed": True,
            "isRemote": False,
            "descriptionPlain": "Build cool stuff.",
            "jobUrl": "https://jobs.ashbyhq.com/acme/abc-123",
        },
        {
            "id": "def-456",
            "title": "Unlisted Posting",
            "isListed": False,  # should be filtered out
            "descriptionPlain": "Hidden.",
            "jobUrl": "https://jobs.ashbyhq.com/acme/def-456",
        },
        {
            "id": "ghi-789",
            "title": "Remote ML Engineer",
            "location": "",
            "isListed": True,
            "isRemote": True,
            "descriptionPlain": "Remote-first role.",
            "jobUrl": "https://jobs.ashbyhq.com/acme/ghi-789",
        },
    ],
}


class TestAshbyNormalize(unittest.TestCase):
    def test_skips_unlisted_postings(self) -> None:
        with patch.object(ashby, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = ashby.fetch("acme")
        self.assertEqual(len(jobs), 2)
        ids = {j.id for j in jobs}
        self.assertIn("abc-123", ids)
        self.assertNotIn("def-456", ids)

    def test_normalize_basic_fields(self) -> None:
        with patch.object(ashby, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = ashby.fetch("acme")
        job = next(j for j in jobs if j.id == "abc-123")
        self.assertEqual(job.source, "ashby")
        self.assertEqual(job.company_slug, "acme")
        self.assertEqual(job.title, "Senior Software Engineer")
        self.assertEqual(job.location, "San Francisco")
        self.assertEqual(job.url, "https://jobs.ashbyhq.com/acme/abc-123")
        self.assertEqual(job.description, "Build cool stuff.")
        self.assertEqual(job.department, "Engineering")
        self.assertEqual(job.employment_type, "FullTime")

    def test_remote_flag_adjusts_location(self) -> None:
        with patch.object(ashby, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = ashby.fetch("acme")
        job = next(j for j in jobs if j.id == "ghi-789")
        # An empty location plus isRemote=True should produce "Remote".
        self.assertEqual(job.location, "Remote")

    def test_global_id_is_stable(self) -> None:
        with patch.object(ashby, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = ashby.fetch("acme")
        job = next(j for j in jobs if j.id == "abc-123")
        self.assertEqual(job.global_id, "ashby:acme:abc-123")

    def test_network_failure_returns_empty(self) -> None:
        def boom(_url: str) -> None:
            raise ConnectionError("network is down")

        with patch.object(ashby, "http_get_json", side_effect=boom):
            jobs = ashby.fetch("acme")
        self.assertEqual(jobs, [])

    def test_malformed_response_returns_empty_safely(self) -> None:
        # A response with no "jobs" key should produce an empty list, not raise.
        with patch.object(ashby, "http_get_json", return_value={}):
            jobs = ashby.fetch("acme")
        self.assertEqual(jobs, [])


@unittest.skipUnless(
    os.environ.get("JOBSCOUT_LIVE_TESTS") == "1",
    "set JOBSCOUT_LIVE_TESTS=1 to enable live ATS smoke tests",
)
class TestAshbyLive(unittest.TestCase):
    """Hit the real Ashby API. Skipped by default."""

    def test_openai_board_is_reachable(self) -> None:
        # OpenAI uses Ashby and reliably has many open roles. (Slugs change
        # over time as companies switch ATSes; if this starts failing,
        # swap in another known-Ashby customer.)
        jobs = ashby.fetch("openai")
        self.assertGreater(len(jobs), 0)
        for job in jobs:
            self.assertTrue(job.id)
            self.assertTrue(job.title)
            self.assertEqual(job.source, "ashby")


if __name__ == "__main__":
    unittest.main()
