"""Unit tests for the Greenhouse connector."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from connectors import greenhouse  # noqa: E402


SAMPLE_RESPONSE = {
    "jobs": [
        {
            "id": 1001,
            "title": "Engineering Manager",
            "updated_at": "2026-01-15T10:00:00-08:00",
            "location": {"name": "San Francisco, CA"},
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/1001",
            "content": "<p>Lead a team of engineers.</p><p>Requirements: <ul><li>5+ years</li></ul></p>",
            "departments": [{"id": 1, "name": "Engineering"}],
            "offices": [{"id": 1, "name": "San Francisco"}],
        },
        {
            "id": 1002,
            "title": "Backend Engineer",
            "location": "Remote",  # some boards return a string, not a dict
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/1002",
            "content": "&lt;p&gt;Build the backend.&lt;/p&gt;",  # html-encoded HTML
            "departments": [],
        },
    ],
    "meta": {"total": 2},
}


class TestGreenhouseNormalize(unittest.TestCase):
    def test_dict_location(self) -> None:
        with patch.object(greenhouse, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = greenhouse.fetch("acme")
        job = next(j for j in jobs if j.id == "1001")
        self.assertEqual(job.location, "San Francisco, CA")

    def test_string_location(self) -> None:
        with patch.object(greenhouse, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = greenhouse.fetch("acme")
        job = next(j for j in jobs if j.id == "1002")
        self.assertEqual(job.location, "Remote")

    def test_html_decoded_and_stripped(self) -> None:
        with patch.object(greenhouse, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = greenhouse.fetch("acme")
        job1001 = next(j for j in jobs if j.id == "1001")
        # Tags should be gone but the text should survive.
        self.assertIn("Lead a team of engineers", job1001.description)
        self.assertNotIn("<p>", job1001.description)
        self.assertNotIn("<ul>", job1001.description)

        job1002 = next(j for j in jobs if j.id == "1002")
        # Double-encoded HTML should still produce clean text.
        self.assertIn("Build the backend", job1002.description)
        self.assertNotIn("&lt;", job1002.description)

    def test_department_extracted(self) -> None:
        with patch.object(greenhouse, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = greenhouse.fetch("acme")
        job1001 = next(j for j in jobs if j.id == "1001")
        self.assertEqual(job1001.department, "Engineering")
        job1002 = next(j for j in jobs if j.id == "1002")
        self.assertIsNone(job1002.department)

    def test_network_failure_returns_empty(self) -> None:
        with patch.object(greenhouse, "http_get_json", side_effect=ConnectionError("boom")):
            self.assertEqual(greenhouse.fetch("acme"), [])

    def test_source_is_greenhouse(self) -> None:
        with patch.object(greenhouse, "http_get_json", return_value=SAMPLE_RESPONSE):
            jobs = greenhouse.fetch("acme")
        for job in jobs:
            self.assertEqual(job.source, "greenhouse")


@unittest.skipUnless(
    os.environ.get("JOBSCOUT_LIVE_TESTS") == "1",
    "set JOBSCOUT_LIVE_TESTS=1 to enable live ATS smoke tests",
)
class TestGreenhouseLive(unittest.TestCase):
    def test_stripe_board_is_reachable(self) -> None:
        # Stripe is a stable Greenhouse customer.
        jobs = greenhouse.fetch("stripe")
        self.assertGreater(len(jobs), 0)


if __name__ == "__main__":
    unittest.main()
