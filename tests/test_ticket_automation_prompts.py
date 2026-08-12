from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"


def skill_text(root: Path, name: str) -> str:
    return (root / name / "SKILL.md").read_text(encoding="utf-8")


def test_run_ticket_has_exact_input_and_dispatch_boundaries() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")

    assert "identifies exactly one Ticket" in text
    assert "Never scan the store, rank work, or invoke `next-ticket`" in text
    assert "Do not check for the Auto grant" in text
    assert "a person may invoke `run-ticket` on an ungranted Ticket" in text
    assert "Invoke `manifest-dev:auto`" in text
    assert "a conflicting claim stops the attempt" in text


def test_run_ticket_preserves_ticket_identity_and_routes_follow_ups() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")

    assert "Then close the same Ticket as done" in text
    assert "Leave the Ticket open" in text
    assert "Escalation ends this attempt, not the work" in text
    assert "Never close the source or create a replacement Ticket" in text
    assert "invoke `manifest-dev:ticket-up`" in text
    assert "Never write a follow-up directly to the venue" in text


def test_ticket_up_defaults_to_coherent_units_and_conjunctive_auto() -> None:
    text = skill_text(SOURCE_SKILLS, "ticket-up")

    assert "Manifest input defaults to one Shaped Ticket for the whole Manifest" in text
    assert (
        "only when the caller explicitly asks for delegation or parallel pickup" in text
    )
    assert "Question Ticket only when the question needs its own lifecycle" in text
    assert "source Ticket must carry Auto" in text
    assert "follow-up must independently pass the same grant criterion" in text
    assert "An ungranted source can create only ungranted follow-ups" in text


def test_selector_presents_without_executing() -> None:
    text = skill_text(SOURCE_SKILLS, "next-ticket")

    assert "Claim it, then present it" in text
    assert "Do not execute it, invoke `run-ticket`" in text
    assert "selection and execution are separate actions" in text


@pytest.mark.parametrize(
    "skills_root",
    [
        ROOT / "dist" / "codex" / "plugins" / "manifest-dev" / "skills",
        ROOT / "dist" / "opencode" / "skills",
        ROOT / "dist" / "pi" / "skills",
    ],
)
def test_run_ticket_ships_on_every_distribution(skills_root: Path) -> None:
    text = skill_text(skills_root, "run-ticket")

    assert "name: run-ticket" in text
    assert "one exact Ticket" in text
    assert "DONE" in text
    assert "ESCALATED" in text
