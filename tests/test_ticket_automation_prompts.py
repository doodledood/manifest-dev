from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"


def skill_text(root: Path, name: str) -> str:
    return (root / name / "SKILL.md").read_text(encoding="utf-8")


def test_run_ticket_has_exact_input_and_dispatch_boundaries() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")

    assert "identifies exactly one Ticket" in text
    assert "Never scan the store, rank work, or invoke `next-ticket`" in text
    assert "Do not check for the Auto grant to decide whether to begin" in text
    assert "a person may invoke\n`run-ticket` on an ungranted Ticket" in text
    assert "Invoke `manifest-dev:auto`" in text
    assert "A conflicting human claim stops the attempt" in text


def test_run_ticket_recovers_and_lands_before_done() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")
    convention = (
        SOURCE_SKILLS / "ticket-up" / "references" / "TICKET_CONVENTION.md"
    ).read_text(encoding="utf-8")

    assert "<!-- manifest-dev-run-ticket-attempt -->" in text
    assert "one stable branch for the life of the Ticket" in text
    assert "Discover and reuse the pull request" in text
    assert "Push coherent checkpoints" in text
    assert "Activate the\n`manifest-dev:check-pr` skill" in text
    assert "Immediately before any irreversible landing" in text
    assert "requires Auto still to\nbe present" in text
    assert "merge through the venue's\nnormal protected mechanism" in text
    assert "After the required landing is observed" in text
    assert (
        "Ordinary landing through the repository's declared protections is within Auto"
        in convention
    )
    assert (
        "irreversible act that requires separate human authority beyond the Auto grant"
        in convention
    )


def test_run_ticket_preserves_ticket_identity_and_routes_follow_ups() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")

    assert "Then close the same Ticket as done" in text
    assert "Leave the Ticket open" in text
    assert "Escalation ends this attempt, not the work" in text
    assert "Never close the source or\ncreate a replacement Ticket" in text
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


def test_sweep_tickets_recovers_first_and_runs_at_most_one() -> None:
    text = skill_text(SOURCE_SKILLS, "sweep-tickets")

    assert "Advance unattended Ticket work by at most one Ticket" in text
    assert "Build the eligible set before choosing a branch" in text
    assert "match every configured\neffort or type filter" in text
    assert "whose dependencies are all closed" in text
    assert (
        "dependency-blocked, policy-filtered, and\nhuman-assigned items untouched"
        in text
    )
    assert "**Recover first.**" in text
    assert (
        "From the eligible set, find Tickets claimed by this automation identity"
        in text
    )
    assert "**Otherwise start ready work.**" in text
    assert "Human-assigned Tickets are paused" in text
    assert "Never mutate any claim during\nselection" in text
    assert "Invoke the `manifest-dev:run-ticket` skill" in text
    assert "Do not invoke `next-ticket`" in text
    assert "Do not select a second Ticket" in text


def test_trigger_adapter_contract_stays_thin_and_recoverable() -> None:
    text = (
        SOURCE_SKILLS / "ticket-up" / "references" / "AUTOMATED_EXECUTION.md"
    ).read_text(encoding="utf-8")

    assert "Invoke the manifest-dev:run-ticket skill" in text
    assert "Invoke the manifest-dev:sweep-tickets skill" in text
    assert "**Per-Ticket single-flight.**" in text
    assert "**Finite runner retries.**" in text
    assert "**Terminal runner-failure handoff.**" in text
    assert "stable hidden marker" in text
    assert "does not remove and re-add `auto`" in text
    assert "Set cron to `*/10 * * * *`" in text
    assert "issue `opened`, `reopened`, and `unassigned` events" in text
    assert "`labeled` when the applied\n  label is `auto`" in text
    assert "Schedule only is correct but starts at most one Ticket per tick" in text
    assert "Event plus schedule adds the fast\npath and parallelism" in text
    assert "A person may also run the exact-Ticket prompt manually" in text


def test_ticket_execution_skills_ship_on_every_distribution() -> None:
    for skills_root in [
        ROOT / "dist" / "codex" / "plugins" / "manifest-dev" / "skills",
        ROOT / "dist" / "opencode" / "skills",
        ROOT / "dist" / "pi" / "skills",
    ]:
        text = skill_text(skills_root, "run-ticket")

        assert "name: run-ticket" in text
        assert "one exact Ticket" in text
        assert "DONE" in text
        assert "ESCALATED" in text

        sweep = skill_text(skills_root, "sweep-tickets")
        assert "name: sweep-tickets" in sweep
        assert "at most one Ticket" in sweep
        assert "Recover first" in sweep
