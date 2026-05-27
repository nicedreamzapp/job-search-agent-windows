"""Unit tests for the filter layer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from connectors.base import Job  # noqa: E402
from filters import FilterConfig, apply, _parse_simple_yaml  # noqa: E402


def make_job(**overrides) -> Job:
    """Build a Job with sensible defaults for testing."""
    defaults = dict(
        id="x",
        source="ashby",
        company_slug="acme",
        company_name="Acme",
        title="Senior Backend Engineer",
        location="Remote",
        url="https://example.com/x",
        description="Build and operate a backend service. 5+ years experience required.",
    )
    defaults.update(overrides)
    return Job(**defaults)


class TestFilters(unittest.TestCase):
    def test_empty_config_keeps_everything(self) -> None:
        jobs = [make_job(), make_job(id="y", title="Junior Dev")]
        kept, dropped = apply(jobs, FilterConfig.empty())
        self.assertEqual(len(kept), 2)
        self.assertEqual(len(dropped), 0)

    def test_drop_title_regex(self) -> None:
        jobs = [
            make_job(id="a", title="Senior Backend Engineer"),
            make_job(id="b", title="Junior Backend Engineer"),
            make_job(id="c", title="Engineering Intern"),
        ]
        cfg = FilterConfig(drop_titles_matching=["Junior", "Intern\\b"])
        kept, dropped = apply(jobs, cfg)
        self.assertEqual({j.id for j in kept}, {"a"})
        self.assertEqual(len(dropped), 2)
        # Reasons should mention the matching pattern.
        for _job, reason in dropped:
            self.assertIn("title matches", reason)

    def test_drop_description_regex(self) -> None:
        jobs = [
            make_job(id="a", description="Build a backend. No degree required."),
            make_job(id="b", description="Build a backend. Bachelor's degree required."),
        ]
        cfg = FilterConfig(drop_descriptions_matching=["Bachelor[’']s degree required"])
        kept, dropped = apply(jobs, cfg)
        self.assertEqual({j.id for j in kept}, {"a"})
        self.assertEqual(len(dropped), 1)

    def test_drop_company_matches_name_or_slug(self) -> None:
        jobs = [
            make_job(id="a", company_name="Acme", company_slug="acme"),
            make_job(id="b", company_name="Big Bank Corp", company_slug="bigbank"),
            make_job(id="c", company_name="Innocent Inc", company_slug="totally-a-bank"),
        ]
        cfg = FilterConfig(drop_companies_matching=["bank"])
        kept, dropped = apply(jobs, cfg)
        self.assertEqual({j.id for j in kept}, {"a"})
        # Both b and c should be dropped — one by name, one by slug.
        self.assertEqual(len(dropped), 2)

    def test_require_locations_allowlist(self) -> None:
        jobs = [
            make_job(id="a", location="Remote"),
            make_job(id="b", location="United States"),
            make_job(id="c", location="Berlin, Germany"),
            make_job(id="d", location="Tokyo"),
        ]
        cfg = FilterConfig(require_locations_in=["Remote", "United States"])
        kept, dropped = apply(jobs, cfg)
        self.assertEqual({j.id for j in kept}, {"a", "b"})
        self.assertEqual(len(dropped), 2)

    def test_empty_location_allowlist_means_no_filtering(self) -> None:
        jobs = [make_job(location="Mars")]
        cfg = FilterConfig(require_locations_in=[])
        kept, dropped = apply(jobs, cfg)
        self.assertEqual(len(kept), 1)
        self.assertEqual(len(dropped), 0)


class TestYamlParser(unittest.TestCase):
    def test_basic_parse(self) -> None:
        text = """
# Top comment
drop_titles_matching:
  - "Junior"
  - Intern
  - 'Entry Level'

drop_companies_matching:
  - bank
"""
        out = _parse_simple_yaml(text)
        self.assertEqual(out["drop_titles_matching"], ["Junior", "Intern", "Entry Level"])
        self.assertEqual(out["drop_companies_matching"], ["bank"])

    def test_empty_keys(self) -> None:
        text = """
drop_titles_matching:
drop_companies_matching:
  - foo
"""
        out = _parse_simple_yaml(text)
        self.assertEqual(out["drop_titles_matching"], [])
        self.assertEqual(out["drop_companies_matching"], ["foo"])

    def test_loads_from_file(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write("drop_titles_matching:\n  - Junior\n")
            path = Path(f.name)
        try:
            cfg = FilterConfig.from_file(path)
            self.assertEqual(cfg.drop_titles_matching, ["Junior"])
        finally:
            path.unlink()

    def test_loads_from_json_file(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write('{"drop_titles_matching": ["Junior", "Intern"]}')
            path = Path(f.name)
        try:
            cfg = FilterConfig.from_file(path)
            self.assertEqual(cfg.drop_titles_matching, ["Junior", "Intern"])
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
