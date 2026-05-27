#!/usr/bin/env python3
"""Setup wizard for job-search-agent.

A friendly, plain-English Q&A flow that produces a polished `credentials.md`
file for the scorer — no markdown knowledge or terminal experience required.

Two entry points:

  * CLI mode    — `python jobscout.py setup`
                  Asks one question at a time on the terminal.
  * Web mode    — `python jobscout.py setup --web`
                  Serves `wizard/index.html` on http://localhost:8765 and
                  accepts a POST from the browser to save the result.

Progress is autosaved to `~/.config/jobscout/wizard_progress.json` after
every answer so quitting halfway never loses work. Resume by re-running.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import socketserver
import sys
import textwrap
import threading
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Pretty terminal helpers — safe on Windows / old terminals (auto-degrade to
# plain ASCII if NO_COLOR is set or the terminal isn't a TTY).
# ---------------------------------------------------------------------------


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


_COLOR = _supports_color()


def _c(code: str, text: str) -> str:
    """Wrap `text` in an ANSI color sequence if the terminal supports it."""
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


def bold(text: str) -> str:
    return _c("1", text)


def dim(text: str) -> str:
    return _c("2", text)


def green(text: str) -> str:
    return _c("32", text)


def cyan(text: str) -> str:
    return _c("36", text)


def yellow(text: str) -> str:
    return _c("33", text)


# ---------------------------------------------------------------------------
# Wizard data model
# ---------------------------------------------------------------------------


@dataclass
class WizardState:
    """Every answer the wizard collects. Stored as JSON for resume."""

    # Step 1 — Basics
    name: str = ""
    city: str = ""
    relocate: str = ""  # "yes" | "no" | "maybe: cities..."
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    web: str = ""

    # Step 2 — Coffee-shop paragraph
    story: str = ""

    # Step 3 — Work history (multiple entries)
    work_entries: list[str] = field(default_factory=list)
    shipped_entries: list[str] = field(default_factory=list)
    numbers: str = ""

    # Step 4 — Skills
    skills: str = ""
    tools: str = ""
    superpowers: str = ""

    # Step 5 — What you're looking for
    excited_by: str = ""
    hard_no: str = ""
    pay: str = ""
    things_to_know: str = ""

    # Bookkeeping
    last_step: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "city": self.city,
            "relocate": self.relocate,
            "email": self.email,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "web": self.web,
            "story": self.story,
            "work_entries": self.work_entries,
            "shipped_entries": self.shipped_entries,
            "numbers": self.numbers,
            "skills": self.skills,
            "tools": self.tools,
            "superpowers": self.superpowers,
            "excited_by": self.excited_by,
            "hard_no": self.hard_no,
            "pay": self.pay,
            "things_to_know": self.things_to_know,
            "last_step": self.last_step,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "WizardState":
        state = cls()
        for key, value in d.items():
            if hasattr(state, key):
                setattr(state, key, value)
        return state


# ---------------------------------------------------------------------------
# Config / progress paths
# ---------------------------------------------------------------------------


def config_dir() -> Path:
    """Resolve the config dir. Mirrors `jobscout.config_dir`."""
    override = os.environ.get("JOBSCOUT_CONFIG_DIR")
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / "jobscout"


def progress_path() -> Path:
    return config_dir() / "wizard_progress.json"


def credentials_path() -> Path:
    return config_dir() / "credentials.md"


def save_progress(state: WizardState) -> None:
    """Persist the wizard state so it survives a Ctrl-C."""
    config_dir().mkdir(parents=True, exist_ok=True)
    progress_path().write_text(
        json.dumps(state.to_dict(), indent=2),
        encoding="utf-8",
    )


def load_progress() -> WizardState | None:
    """Load saved progress if any. Returns None if nothing's there."""
    path = progress_path()
    if not path.exists():
        return None
    try:
        return WizardState.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return None


def clear_progress() -> None:
    """Delete the resume file after a successful save."""
    path = progress_path()
    if path.exists():
        path.unlink()


# ---------------------------------------------------------------------------
# Question helpers — every prompt goes through these so the look is uniform.
# ---------------------------------------------------------------------------


def _print_question(
    label: str,
    example: str | None = None,
    note: str | None = None,
    multiline: bool = False,
) -> None:
    """Print a friendly question block with optional example + note."""
    print()
    print(cyan(label))
    if note:
        print(dim(note))
    if example:
        print(dim(f"  example: {example}"))
    if multiline:
        print(dim("  (paste or type multiple lines — finish with an empty line)"))


def ask(
    label: str,
    *,
    example: str | None = None,
    note: str | None = None,
    default: str = "",
    required: bool = False,
    validate: Callable[[str], str | None] | None = None,
) -> str:
    """Ask a single-line question. Returns the trimmed answer.

    Pressing Enter on a required question keeps re-prompting. `validate`
    can return None (ok) or a string error message.
    """
    _print_question(label, example=example, note=note)
    while True:
        prompt = f"> "
        if default:
            prompt = f"> [{default}] "
        try:
            answer = input(prompt).strip()
        except EOFError:
            return default
        if not answer and default:
            answer = default
        if not answer and required:
            print(yellow("  (this one's required — give it a try)"))
            continue
        if validate:
            err = validate(answer)
            if err:
                print(yellow(f"  {err}"))
                continue
        return answer


def ask_multiline(
    label: str,
    *,
    example: str | None = None,
    note: str | None = None,
    required: bool = False,
) -> str:
    """Ask a multi-line question. Finish with an empty line."""
    _print_question(label, example=example, note=note, multiline=True)
    lines: list[str] = []
    while True:
        try:
            line = input("  ")
        except EOFError:
            break
        if line.strip() == "":
            if lines:
                break
            if not required:
                break
            print(yellow("  (this one's required — type something then press Enter twice)"))
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def ask_yes_no_maybe(
    label: str,
    *,
    note: str | None = None,
    follow_up_if_maybe: str | None = None,
) -> str:
    """Friendly tri-state: 'yes' / 'no' / 'maybe — <follow-up>'."""
    _print_question(label, note=note)
    print(dim("  type: yes  /  no  /  maybe"))
    while True:
        try:
            ans = input("> ").strip().lower()
        except EOFError:
            return ""
        if ans in ("y", "yes"):
            return "yes"
        if ans in ("n", "no"):
            return "no"
        if ans in ("m", "maybe"):
            if follow_up_if_maybe:
                follow = ask(follow_up_if_maybe, example="San Francisco, Boston, NYC")
                return f"maybe: {follow}" if follow else "maybe"
            return "maybe"
        print(yellow("  (please type yes, no, or maybe)"))


def ask_repeating(
    label: str,
    *,
    example: str | None = None,
    note: str | None = None,
    min_items: int = 1,
) -> list[str]:
    """Ask the same multi-line question repeatedly until the user says 'done'."""
    answers: list[str] = []
    first = True
    while True:
        if first:
            print()
            print(cyan(label))
            if note:
                print(dim(note))
            if example:
                print(dim(f"  example: {example}"))
            print(dim("  (type your answer, then an empty line. Add more or type 'done' to finish.)"))
            first = False
        else:
            print()
            print(cyan("  Add another? Type it below, or type 'done' to move on."))
            print(dim("  (you can keep adding as many as you want)"))

        lines: list[str] = []
        eof_hit = False
        while True:
            try:
                line = input("  ")
            except EOFError:
                # No more stdin — bail out gracefully rather than spinning.
                eof_hit = True
                line = ""
            stripped = line.strip().lower()
            if stripped == "done":
                # "done" terminates the question. If the user has typed part
                # of a new entry, commit it first so we don't drop their work.
                if lines:
                    answers.append("\n".join(lines).strip())
                if len(answers) >= min_items:
                    return answers
                print(yellow(f"  (please add at least {min_items} before typing done)"))
                first = True
                break
            if line.strip() == "":
                if lines:
                    answers.append("\n".join(lines).strip())
                    break
                # Empty enter with nothing typed — treat as 'next prompt' once
                # we have enough answers, or surrender on EOF.
                if len(answers) >= min_items or eof_hit:
                    return answers
                print(yellow(f"  (please add at least {min_items} before moving on)"))
                if eof_hit:
                    return answers
                continue
            lines.append(line)
            if eof_hit:
                # EOF arrived mid-entry — commit what we have and exit.
                answers.append("\n".join(lines).strip())
                return answers


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def _validate_email(value: str) -> str | None:
    if not value:
        return None
    if "@" not in value or "." not in value.split("@")[-1]:
        return "that doesn't look like an email — try again (e.g. you@example.com)"
    return None


def _validate_url(value: str) -> str | None:
    if not value:
        return None
    if not (value.startswith("http://") or value.startswith("https://") or value.startswith("www.")):
        return "URLs should start with http:// or https:// (or just press Enter to skip)"
    return None


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _join_contact(state: WizardState) -> str:
    """Build the `**Contact:** ...` line from whatever the user provided."""
    parts: list[str] = []
    if state.email:
        parts.append(state.email)
    if state.phone:
        parts.append(state.phone)
    if state.linkedin:
        parts.append(state.linkedin)
    if state.web:
        parts.append(state.web)
    return " | ".join(parts) if parts else "(not provided)"


def _format_where(state: WizardState) -> str:
    """Build the location line, accounting for relocation preferences."""
    where = state.city or "(not provided)"
    relocate = (state.relocate or "").strip()
    if relocate.startswith("yes"):
        where += " (open to relocating)"
    elif relocate.startswith("maybe"):
        rest = relocate[len("maybe"):].lstrip(": ").strip()
        if rest:
            where += f" (open to relocating to {rest})"
        else:
            where += " (open to relocating for the right role)"
    elif relocate.startswith("no"):
        where += " (not relocating)"
    return where


def _bulletize(entries: list[str]) -> str:
    """Turn a list of free-text entries into clean markdown bullets."""
    bullets: list[str] = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        # If the entry has multiple lines, indent the continuation lines so
        # they stay inside the same bullet.
        lines = entry.splitlines()
        first = lines[0]
        rest = "\n  ".join(line.strip() for line in lines[1:] if line.strip())
        bullets.append(f"- {first}" + (f"\n  {rest}" if rest else ""))
    return "\n".join(bullets)


def render_markdown(state: WizardState) -> str:
    """Turn the wizard state into a clean credentials.md document."""
    where_line = _format_where(state)
    contact_line = _join_contact(state)

    parts: list[str] = []
    parts.append(f"# {state.name or '(your name)'}")
    parts.append("")
    parts.append(f"**Where:** {where_line}")
    parts.append(f"**Contact:** {contact_line}")
    parts.append("")
    parts.append("## Who I Am")
    parts.append("")
    parts.append(state.story.strip() or "(coffee-shop paragraph goes here)")
    parts.append("")
    parts.append("## What I've Done")
    parts.append("")

    work_block = _bulletize(state.work_entries)
    shipped_block = _bulletize(state.shipped_entries)
    if work_block:
        parts.append(work_block)
    if shipped_block:
        if work_block:
            parts.append("")
        parts.append("**Things I've shipped or made:**")
        parts.append("")
        parts.append(shipped_block)
    if state.numbers.strip():
        parts.append("")
        parts.append("**Numbers worth knowing:**")
        parts.append("")
        parts.append(state.numbers.strip())

    parts.append("")
    parts.append("## Skills")
    parts.append("")
    parts.append(state.skills.strip() or "(skills paragraph)")
    if state.tools.strip():
        parts.append("")
        parts.append(f"**Tools / software I actually use:** {state.tools.strip()}")
    if state.superpowers.strip():
        parts.append("")
        parts.append(f"**Underrated strengths:** {state.superpowers.strip()}")

    parts.append("")
    parts.append("## What I'm Looking For")
    parts.append("")
    parts.append(state.excited_by.strip() or "(what kind of role excites you)")
    if state.hard_no.strip():
        parts.append("")
        parts.append(f"**Not interested in:** {state.hard_no.strip()}")
    if state.pay.strip():
        parts.append("")
        parts.append(f"**Pay:** {state.pay.strip()}")

    if state.things_to_know.strip():
        parts.append("")
        parts.append("## Things to Know Up Front")
        parts.append("")
        parts.append(state.things_to_know.strip())

    parts.append("")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI wizard steps
# ---------------------------------------------------------------------------


def _header(title: str, current: int, total: int = 6) -> None:
    print()
    bar = "█" * current + "░" * (total - current)
    print(bold(f"  Step {current} of {total} — {title}"))
    print(dim(f"  [{bar}]"))


def step_1_basics(state: WizardState) -> None:
    _header("the basics", 1)
    state.name = ask(
        "What's your full name?",
        example="Alex Rivera",
        default=state.name,
        required=True,
    )
    save_progress(state)
    state.city = ask(
        "What city are you in?",
        note="We'll highlight roles in the same city. Free text — neighborhoods are fine too.",
        example="Boise, Idaho",
        default=state.city,
        required=True,
    )
    save_progress(state)
    state.relocate = ask_yes_no_maybe(
        "Are you open to moving for the right job?",
        note="If 'maybe', we'll ask which cities are on the table.",
        follow_up_if_maybe="Which cities are on the table?",
    )
    if not state.relocate and state.relocate != "":
        # ask_yes_no_maybe always returns a string
        pass
    save_progress(state)
    state.email = ask(
        "What email do you want recruiters to contact you at?",
        example="alex.rivera@gmail.com",
        default=state.email,
        required=True,
        validate=_validate_email,
    )
    save_progress(state)
    state.phone = ask(
        "Phone number? (optional — press Enter to skip)",
        example="(208) 555-0134",
        default=state.phone,
    )
    save_progress(state)
    state.linkedin = ask(
        "LinkedIn URL? (optional)",
        example="https://www.linkedin.com/in/alexrivera",
        default=state.linkedin,
        validate=_validate_url,
    )
    save_progress(state)
    state.web = ask(
        "GitHub URL or personal website? (optional)",
        example="https://alexrivera.com",
        default=state.web,
        validate=_validate_url,
    )
    state.last_step = 2
    save_progress(state)


def step_2_story(state: WizardState) -> None:
    _header("your story in one paragraph", 2)
    print()
    print(textwrap.fill(
        "Imagine you're meeting a hiring manager at a coffee shop. They ask "
        "'so what do you do?' What's your answer? Don't think too hard — "
        "write it like you'd actually say it.",
        width=78,
    ))
    print(dim("\n  Aim for 3-5 sentences. Done? Press Enter on an empty line."))
    print(dim("  example: \"I've spent 12 years running a small bakery — I do everything from"))
    print(dim("           sourcing flour to training new hires. Lately I've been teaching "))
    print(dim("           myself bookkeeping software because my accountant keeps fixing my mess."))
    print(dim("           I'm looking for something that lets me use the people-skills and"))
    print(dim("           the spreadsheet-skills at the same time.\""))
    state.story = ask_multiline("", required=True) or state.story
    state.last_step = 3
    save_progress(state)


def step_3_work(state: WizardState) -> None:
    _header("your work", 3)
    print()
    print(textwrap.fill(
        "Tell me about things you've worked on or built. Each entry can be a "
        "job, a side project, a volunteer thing, a class you taught — "
        "anything. You can add as many as you want.",
        width=78,
    ))
    print(dim("\n  After each one, press Enter on an empty line to add it. Type 'done' to move on."))

    if not state.work_entries:
        state.work_entries = ask_repeating(
            "What have you worked on? Tell me what it was and what you actually did.",
            example=(
                "Ran the front of house at Romano's Italian for 6 years. "
                "Managed 12 servers, did weekly schedules, trained every new hire."
            ),
            min_items=1,
        )
    save_progress(state)

    if not state.shipped_entries:
        print()
        print(textwrap.fill(
            "Now anything you've shipped or made? Apps, websites, products, "
            "photos, articles, art, classes you taught, problems you fixed. "
            "(Skip if nothing comes to mind — type 'done' on the first one.)",
            width=78,
        ))
        state.shipped_entries = ask_repeating(
            "Anything you've shipped or made?",
            example="Built and ran a small Etsy shop selling hand-poured candles — 240 orders in year one.",
            min_items=0,
        )
    save_progress(state)

    state.numbers = ask_multiline(
        "Numbers help. Did anything you did have a number attached?",
        note="(customers served, hours saved, money saved, kids tutored, plates served, anything)",
        example="Trained 40+ new hires over 6 years. Cut weekly inventory time from 6 hours to 90 minutes.",
    ) or state.numbers
    state.last_step = 4
    save_progress(state)


def step_4_skills(state: WizardState) -> None:
    _header("skills", 4)
    state.skills = ask_multiline(
        "What do you know how to do?",
        note="Don't list tech stacks unless you actually use them. Write it like a friend asked.",
        example=(
            "I'm good with people — calming an upset customer is my native skill. "
            "I can read a P&L. I'm a fast learner on any software you put in front of me."
        ),
        required=True,
    ) or state.skills
    save_progress(state)

    state.tools = ask_multiline(
        "What software, tools, or equipment have you actually used at work?",
        note="(Examples: Excel, Photoshop, Shopify, Square POS, restaurant POS, woodshop tools, a Mac.)",
        example="Excel, QuickBooks, Square POS, Canva, Mailchimp, a Mac.",
    ) or state.tools
    save_progress(state)

    state.superpowers = ask_multiline(
        "Anything you wouldn't list on a resume but is actually a superpower of yours?",
        note="(Working at 4am, never missing a deadline, picking up new tools fast, fluent in customer-talk.)",
        example=(
            "I never miss a deadline. I can read a room before I say anything. "
            "I genuinely like writing — internal memos at my last job got passed around the office."
        ),
    ) or state.superpowers
    state.last_step = 5
    save_progress(state)


def step_5_looking_for(state: WizardState) -> None:
    _header("what you're looking for", 5)
    state.excited_by = ask_multiline(
        "What kind of job feels exciting right now?",
        example="Something operations-y at a small business that's growing. Bonus if I can be the person who builds the systems from scratch.",
        required=True,
    ) or state.excited_by
    save_progress(state)

    state.hard_no = ask_multiline(
        "What kind of job is a HARD NO?",
        note="(e.g. 'no nights/weekends', 'no commission-only', 'no banks', 'no startups under 10 people')",
        example="No commission-only roles. No restaurants. No 5am starts.",
    ) or state.hard_no
    save_progress(state)

    state.pay = ask(
        "Money range you're willing to take?",
        note="You can say 'whatever's fair' if you don't know — we'll skip salary filtering.",
        example="$65k-$85k base, open to a little lower for the right team",
        default=state.pay,
    )
    save_progress(state)

    state.things_to_know = ask_multiline(
        "Anything else a hiring manager should know about you?",
        note="(Health stuff, family stuff, schedule stuff, anything that should be on the table early. Optional.)",
        example="I'm caring for my dad two afternoons a week — totally workable, just need a heads-up if a meeting moves into that window.",
    ) or state.things_to_know
    state.last_step = 6
    save_progress(state)


def step_6_review(state: WizardState) -> bool:
    """Show the rendered markdown and ask the user to confirm save.

    Returns True if the user saved, False if they bailed.
    """
    _header("review and save", 6)
    md = render_markdown(state)
    print()
    print(dim("─" * 78))
    print(md)
    print(dim("─" * 78))
    print()
    print(cyan("Save this to ~/.config/jobscout/credentials.md?"))
    print(dim("  type: yes  to save  /  no  to bail (we'll keep your progress)"))
    print(dim("  type: edit to jump back to a step and change something"))
    while True:
        try:
            answer = input("> ").strip().lower()
        except EOFError:
            return False
        if answer in ("y", "yes"):
            path = credentials_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(md, encoding="utf-8")
            clear_progress()
            print()
            print(green(f"Saved! Your file is at {path}"))
            print(green("You can now run `python jobscout.py` to score real jobs against it."))
            return True
        if answer in ("n", "no"):
            print(yellow("Bailed. Your answers are saved — run setup again to pick up where you left off."))
            return False
        if answer.startswith("edit"):
            print(dim("  Which step do you want to redo? 1 (basics) / 2 (story) / 3 (work) / 4 (skills) / 5 (looking for)"))
            try:
                which = input("> ").strip()
            except EOFError:
                continue
            if which in ("1", "2", "3", "4", "5"):
                state.last_step = int(which)
                save_progress(state)
                run_cli_from_step(state, int(which))
                return step_6_review(state)
            print(yellow("  (please type 1, 2, 3, 4, or 5)"))
            continue
        print(yellow("  (please type yes, no, or edit)"))


# ---------------------------------------------------------------------------
# Wizard orchestrator
# ---------------------------------------------------------------------------


STEP_FUNCS = [
    step_1_basics,
    step_2_story,
    step_3_work,
    step_4_skills,
    step_5_looking_for,
]


def run_cli_from_step(state: WizardState, start: int) -> None:
    """Run the CLI wizard starting at `start` (1-indexed)."""
    for i, fn in enumerate(STEP_FUNCS, start=1):
        if i < start:
            continue
        # On 'edit' jumps we want to redo just the requested step — but if the
        # user is moving forward through the wizard, run all later steps too.
        if state.last_step > i and start != i:
            continue
        fn(state)


def print_welcome(resuming: bool) -> None:
    print()
    print(bold("  Welcome to job-search-agent."))
    print()
    print(textwrap.fill(
        "I'll ask you a handful of plain-English questions about your work, "
        "your story, and what kind of job you'd actually want. At the end "
        "I'll write the answers into a file the agent uses to score real "
        "openings every morning.",
        width=78,
        initial_indent="  ",
        subsequent_indent="  ",
    ))
    print()
    print(dim("  This usually takes 5-10 minutes. You can quit any time — your"))
    print(dim("  answers save as you go, so you can resume right where you left off."))
    if resuming:
        print()
        print(green("  Found saved progress — picking up where we stopped."))
        print(dim("  (delete ~/.config/jobscout/wizard_progress.json if you want a fresh start)"))


def run_cli() -> int:
    """Top-level entry point for the CLI wizard."""
    resume = load_progress()
    state = resume or WizardState()
    print_welcome(resuming=resume is not None)
    start_at = state.last_step if resume else 1
    try:
        run_cli_from_step(state, start_at)
        step_6_review(state)
    except KeyboardInterrupt:
        print()
        print(yellow("\n  Caught Ctrl-C. Your answers are saved — run setup again to pick up where you left off."))
        return 130
    return 0


# ---------------------------------------------------------------------------
# Web wizard server — same questions, served as a single HTML page
# ---------------------------------------------------------------------------


WIZARD_HTML_PATH = Path(__file__).parent / "wizard" / "index.html"


def _make_handler() -> type[http.server.BaseHTTPRequestHandler]:
    """Build the request handler class for the local web wizard."""

    class WizardHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:  # noqa: ARG002 — silence default access log
            return

        def _serve_html(self) -> None:
            try:
                html = WIZARD_HTML_PATH.read_text(encoding="utf-8")
            except FileNotFoundError:
                self.send_error(500, "wizard/index.html not found")
                return
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _serve_json(self, payload: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 — http.server API
            if self.path in ("/", "/index.html"):
                self._serve_html()
            elif self.path == "/api/progress":
                state = load_progress() or WizardState()
                self._serve_json({"state": state.to_dict()})
            else:
                self.send_error(404)

        def do_POST(self) -> None:  # noqa: N802 — http.server API
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._serve_json({"ok": False, "error": "bad json"}, status=400)
                return

            if self.path == "/api/save-progress":
                state = WizardState.from_dict(payload.get("state", {}))
                save_progress(state)
                self._serve_json({"ok": True})
                return

            if self.path == "/api/save-credentials":
                state = WizardState.from_dict(payload.get("state", {}))
                md = payload.get("markdown") or render_markdown(state)
                path = credentials_path()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(md, encoding="utf-8")
                clear_progress()
                self._serve_json({"ok": True, "path": str(path)})
                return

            self.send_error(404)

    return WizardHandler


def run_web(port: int = 8765, open_browser: bool = True) -> int:
    """Serve the wizard on http://localhost:<port> and block until Ctrl-C."""
    if not WIZARD_HTML_PATH.exists():
        print(f"ERROR: wizard HTML missing at {WIZARD_HTML_PATH}", file=sys.stderr)
        return 1
    handler = _make_handler()
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/"
        print()
        print(bold(f"  Web wizard running at {url}"))
        print(dim("  (your answers save locally — nothing leaves your machine)"))
        print(dim("  Press Ctrl-C to stop."))
        print()
        if open_browser:
            # Open after a tiny delay so the listen socket is definitely ready.
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print(yellow("  Stopping web wizard."))
            return 0
    return 0


# ---------------------------------------------------------------------------
# Public entry point used by jobscout.py
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a Unix exit code."""
    parser = argparse.ArgumentParser(
        description=(
            "Friendly setup wizard for job-search-agent. "
            "Run with no args for the terminal Q&A, or --web for a browser form."
        )
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Open the wizard in your browser instead of running it in the terminal.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port for the web wizard (default: 8765). Only used with --web.",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Don't try to auto-open a browser window for --web. (You'll have to click the URL yourself.)",
    )
    args = parser.parse_args(argv)
    if args.web:
        return run_web(port=args.port, open_browser=not args.no_open)
    return run_cli()


if __name__ == "__main__":
    sys.exit(main())
