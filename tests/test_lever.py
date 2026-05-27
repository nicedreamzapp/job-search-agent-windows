"""Unit tests for the Lever connector."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from connectors import lever  # noqa: E402


SAMPLE_RESPONSE = [
    {
        "id": "uuid-1",
        "text": "Staff Software Engineer",
        "categories": {
            "team": "Platform",
            "department": "Engineering",
            "commitment": "Full-time",
            "location": "New York",
        },
        "descriptionPlain": "Help us scale the platform.",
        "additionalPlain": "We are an equal opportunity employer.",
        "hostedUrl": "https://jobs.lever.co/acme/uuid-1",
        "workplaceType": "on-site",
    },
    {
        "id": "uuid-2",
        "text": "Remote ML Engineer",
        "categories": {
            "location": "Boston",
        },
        "descriptionPlain": "Build models.",
        "hostedUrl": "https://jobs.lever.co/acme/uuid-2",
        "workplaceType": "remote",
    },
]


class TestLeverNormalize(unittest.TestCase):
    def test_categories_extracted(self) -> None:
        with patch.object(lever, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = lever.fetch("acme")
        job = next(j for j in jobs if j.id == "uuid-1")
        self.assertEqual(job.location, "New York")
        self.assertEqual(job.department, "Engineering")
        self.assertEqual(job.employment_type, "Full-time")

    def test_remote_workplace_appends_remote(self) -> None:
        with patch.object(lever, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = lever.fetch("acme")
        job = next(j for j in jobs if j.id == "uuid-2")
        # Lever's workplaceType=remote should tag the location.
        self.assertIn("Remote", job.location)

    def test_description_combines_main_and_additional(self) -> None:
        with patch.object(lever, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = lever.fetch("acme")
        job = next(j for j in jobs if j.id == "uuid-1")
        self.assertIn("Help us scale", job.description)
        self.assertIn("equal opportunity", job.description)

    def test_non_list_response_returns_empty(self) -> None:
        # If the API returns an error object instead of a list, don't crash.
        with patch.object(lever, "http_get_json", return_value={"error": "not found"}):
            self.assertEqual(lever.fetch("acme"), [])

    def test_network_failure_returns_empty(self) -> None:
        with patch.object(lever, "http_get_json", side_effect=ConnectionError("boom")):
            self.assertEqual(lever.fetch("acme"), [])


@unittest.skipUnless(
    os.environ.get("JOBSCOUT_LIVE_TESTS") == "1",
    "set JOBSCOUT_LIVE_TESTS=1 to enable live ATS smoke tests",
)
class TestLeverLive(unittest.TestCase):
    def test_leverdemo_board_is_reachable(self) -> None:
        # `leverdemo` is Lever's own public demo board — stable, always
        # populated, perfect for a smoke test that won't flake when a real
        # company happens to have zero open roles.
        jobs = lever.fetch("leverdemo")
        self.assertGreater(len(jobs), 0)


if __name__ == "__main__":
    unittest.main()
