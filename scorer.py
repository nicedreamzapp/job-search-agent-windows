"""LLM-based job scorer and pitch drafter.

Given a `credentials.md` profile and a `Job`, the scorer asks an LLM to
return a fit score (0-100) plus a one-paragraph rationale. For roles
above `pitch_threshold` (default 80), it follows up with a second call
that drafts a ~200-word custom pitch. Two backends are supported:

1. **Local OpenAI-compatible server** (default) — anything speaking
   `/v1/chat/completions` on `JOBSCOUT_LLM_ENDPOINT` (default
   `http://localhost:8000`): `mlx_lm.server`, `llama.cpp`'s server
   mode, Ollama's OpenAI compat layer, vLLM, etc. This is the
   privacy-first path; your credentials never leave the machine.

2. **Anthropic API fallback** — if `ANTHROPIC_API_KEY` is set in the
   environment, we use the Anthropic Messages API instead. Useful when
   you don't have a local model handy.

The scoring and pitch prompts live in `prompts/scoring.md` and
`prompts/pitch.md` so users can tune them without editing Python. If
either file is missing, we fall back to a baked-in default — the tool
still runs on a fresh clone.

The scorer is deliberately small and dependency-free. It speaks raw
HTTP to both backends so you don't need to install the `anthropic`
package just to try the cloud path.
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from connectors.base import Job

log = logging.getLogger(__name__)


# Sensible defaults: local MLX servers (mlx_lm.server, llama.cpp, etc.) all
# expose OpenAI-compatible `/v1/chat/completions`. We POST there.
DEFAULT_LOCAL_ENDPOINT = "http://localhost:8000"
DEFAULT_LOCAL_MODEL = "mlx-community/Llama-3.1-8B-Instruct-4bit"
DEFAULT_ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"

# We trim descriptions before scoring. ~6000 chars is roughly 1500 tokens —
# enough to capture the meat of a posting while keeping each scoring call
# cheap. Most JDs are well under this; long ones get truncated at a
# paragraph boundary so we don't slice mid-sentence.
MAX_DESCRIPTION_CHARS = 6000

# Roles at or above this score get a custom pitch drafted in a second LLM
# call. The threshold is conservative on purpose — pitches are token-heavy
# and only worth drafting for roles the candidate would actually pursue.
DEFAULT_PITCH_THRESHOLD = 80

# Where externalized prompt templates live. Resolved relative to this file
# so the tool still works when run from any cwd.
_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Inlined fallbacks — used when the corresponding file in `prompts/` is
# missing. Keeps the tool runnable on a clone where someone has deleted
# the prompts directory; also keeps the tests offline-friendly.
_DEFAULT_SCORING_PROMPT = """You are a job-fit scorer. Read the candidate profile and the job posting below, then return a JSON object with two fields:

  - "score": an integer 0-100 representing how strong a fit this role is for this candidate (100 = ideal, 0 = mismatch).
  - "rationale": a single short paragraph (2-3 sentences max) explaining the score.

Be honest. A score of 70+ should mean you would actually recommend this person apply.

=== CANDIDATE PROFILE ===
{credentials_text}

=== JOB POSTING ===
Company: {company_name}
Title: {title}
Location: {location}
Department: {department}
URL: {url}

{description}

=== RESPOND WITH JSON ONLY ===
{{"score": <int 0-100>, "rationale": "<one short paragraph>"}}
"""

_DEFAULT_PITCH_PROMPT = """You are drafting a ~200-word custom pitch — the paragraph the candidate would paste into a cover letter or a recruiter DM to make the case for this specific role at this specific company.

Write in the candidate's voice — first person, plainspoken, specific. Pull at least two concrete facts from the profile and tie each one to something in the job posting. End with a one-line ask. Hard cap 250 words.

Return JSON only:

{{"pitch": "<the pitch as a single string>"}}

=== CANDIDATE PROFILE ===
{credentials_text}

=== JOB POSTING ===
Company: {company_name}
Title: {title}
Location: {location}
Department: {department}
URL: {url}

{description}
"""


@dataclass
class Score:
    """A scoring result for one job.

    `score` is 0-100. `rationale` is a single short paragraph the LLM
    wrote explaining the score. `pitch` is the optional ~200-word custom
    pitch — populated only for roles that cleared `pitch_threshold`; an
    empty string otherwise. If `error` is non-None, scoring failed and
    the other fields are best-effort defaults.
    """

    score: int
    rationale: str
    pitch: str = ""
    error: str | None = None


def score_job(
    job: Job,
    credentials_text: str,
    pitch_threshold: int = DEFAULT_PITCH_THRESHOLD,
) -> Score:
    """Score one job against the user's credentials.

    Picks the backend based on env vars:
      - If `ANTHROPIC_API_KEY` is set, use Anthropic.
      - Else, use the local OpenAI-compatible server at
        `JOBSCOUT_LLM_ENDPOINT`.

    For roles scoring at or above `pitch_threshold`, follows up with a
    second LLM call to draft a ~200-word custom pitch.

    Args:
        job: The normalized job posting.
        credentials_text: The full markdown body of credentials.md.
        pitch_threshold: Minimum score that triggers a pitch draft.

    Returns:
        A `Score` — never raises. Errors are returned in `Score.error`.
    """
    scoring_prompt = _build_prompt(job, credentials_text, _load_template("scoring.md", _DEFAULT_SCORING_PROMPT))
    result = _call_llm(scoring_prompt)
    if result.error or result.score < pitch_threshold:
        return result

    # Score cleared the threshold — draft a custom pitch in a second
    # call. We treat pitch failures as non-fatal: a missing pitch is
    # strictly less useful than a present one, but the score itself is
    # still good signal.
    pitch_prompt = _build_prompt(job, credentials_text, _load_template("pitch.md", _DEFAULT_PITCH_PROMPT))
    pitch_result = _call_llm(pitch_prompt, expect_field="pitch")
    if pitch_result.error:
        log.warning("pitch draft failed for %s: %s — keeping score, skipping pitch", job.global_id, pitch_result.error)
        return result
    result.pitch = pitch_result.pitch or pitch_result.rationale
    return result


def _load_template(filename: str, fallback: str) -> str:
    """Read a prompt template from `prompts/` with an inlined fallback.

    Users can edit `prompts/scoring.md` or `prompts/pitch.md` to retune
    the LLM without touching Python code. The fallback exists so a clone
    with the directory missing still runs.
    """
    path = _PROMPTS_DIR / filename
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            log.warning("could not read prompt template %s: %s — using inlined fallback", path, exc)
    return fallback


def _build_prompt(job: Job, credentials_text: str, template: str) -> str:
    """Fill a prompt template with the candidate profile + job posting.

    Templates use `{name}` placeholders. We use `str.replace` rather
    than `str.format` so curly braces in the template's expected
    JSON-response example (e.g. `{{"score": ..., "rationale": ...}}`)
    don't confuse the formatter.
    """
    description = job.description.strip()
    if len(description) > MAX_DESCRIPTION_CHARS:
        # Truncate at the last paragraph break before the limit so we
        # don't cut mid-sentence.
        cutoff = description.rfind("\n\n", 0, MAX_DESCRIPTION_CHARS)
        if cutoff == -1:
            cutoff = MAX_DESCRIPTION_CHARS
        description = description[:cutoff] + "\n\n[... description truncated ...]"

    fields = {
        "credentials_text": credentials_text.strip(),
        "company_name": job.company_name,
        "title": job.title,
        "location": job.location,
        "department": job.department or "n/a",
        "url": job.url,
        "description": description,
    }
    out = template
    for key, value in fields.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def _call_llm(prompt: str, expect_field: str | None = None) -> Score:
    """Dispatch one LLM call to whichever backend is configured.

    `expect_field` is the JSON key the parser should look for ("score"
    by default, "pitch" for pitch drafts). The returned `Score` has the
    requested field populated; the other field is whatever the model
    happened to include.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if api_key:
        return _score_via_anthropic(prompt, api_key, expect_field)
    return _score_via_local(prompt, expect_field)


def _score_via_local(prompt: str, expect_field: str | None = None) -> Score:
    """Call the local OpenAI-compatible chat-completions endpoint."""
    endpoint = os.environ.get("JOBSCOUT_LLM_ENDPOINT", DEFAULT_LOCAL_ENDPOINT).rstrip("/")
    model = os.environ.get("JOBSCOUT_LLM_MODEL", DEFAULT_LOCAL_MODEL)
    url = f"{endpoint}/v1/chat/completions"

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 600,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return Score(score=0, rationale="", error=f"local LLM unreachable at {url}: {exc}")
    except Exception as exc:  # noqa: BLE001
        return Score(score=0, rationale="", error=f"local LLM call failed: {exc}")

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        return Score(score=0, rationale="", error=f"unexpected local LLM response: {exc}")

    return _parse_json_response(content, expect_field)


def _score_via_anthropic(prompt: str, api_key: str, expect_field: str | None = None) -> Score:
    """Call the Anthropic Messages API."""
    model = os.environ.get("JOBSCOUT_ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
    url = "https://api.anthropic.com/v1/messages"

    body = json.dumps({
        "model": model,
        "max_tokens": 600,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Read the body so we can surface API errors (rate-limit, auth, etc.).
        try:
            err_body = exc.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            err_body = ""
        return Score(score=0, rationale="", error=f"anthropic API {exc.code}: {err_body[:200]}")
    except urllib.error.URLError as exc:
        return Score(score=0, rationale="", error=f"anthropic API unreachable: {exc}")

    try:
        # Anthropic returns `content` as a list of blocks; we want the first
        # text block.
        content = next(block["text"] for block in payload["content"] if block.get("type") == "text")
    except (StopIteration, KeyError, TypeError) as exc:
        return Score(score=0, rationale="", error=f"unexpected anthropic response: {exc}")

    return _parse_json_response(content, expect_field)


def _parse_json_response(content: str, expect_field: str | None = None) -> Score:
    """Extract a JSON object from an LLM response and map it to a Score.

    Models sometimes wrap their JSON in prose ("Here's the result: {...}")
    or in a markdown code fence. We pluck out the first balanced JSON
    object we can find — robust to either.

    `expect_field`:
        - "pitch" — pull `pitch` into `Score.pitch`. `score`/`rationale`
          come from whatever the model included (often nothing on a
          pitch call) and default to 0/"".
        - anything else / None — pull `score` + `rationale` (the normal
          scoring path). `pitch` stays empty.
    """
    # Try the fast path first: the whole content is valid JSON.
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Look for a fenced code block.
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError:
                data = None
        else:
            data = None

        if data is None:
            # Last resort: find the first top-level `{...}` and try that.
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                except json.JSONDecodeError:
                    return Score(score=0, rationale=content.strip()[:300], error="could not parse score JSON")
            else:
                return Score(score=0, rationale=content.strip()[:300], error="no JSON in response")

    if expect_field == "pitch":
        pitch = str(data.get("pitch", "")).strip()
        if not pitch:
            return Score(score=0, rationale="", error="no pitch field in response")
        return Score(score=0, rationale="", pitch=pitch)

    try:
        score = int(data.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    score = max(0, min(100, score))  # Clamp to [0, 100].
    rationale = str(data.get("rationale", "")).strip()
    return Score(score=score, rationale=rationale)
