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
    assert text.index(
        "After that coherent result is committed and pushed"
    ) > text.index("create or refresh its one pull request")
    assert text.index(
        "update the marked\nattempt comment with the verified head commit"
    ) < text.index("Immediately before any irreversible landing")
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


def test_ticket_up_preserves_auto_authority_boundary() -> None:
    text = skill_text(SOURCE_SKILLS, "ticket-up")

    assert "Manifest input defaults to one Shaped Ticket for the whole Manifest" in text
    assert (
        "only when the caller explicitly asks for delegation or parallel pickup" in text
    )
    assert "Question Ticket only when the question needs its own lifecycle" in text
    assert "fresh human grant for Auto" in text
    assert "person directly authoring here" in text
    assert "source Ticket must carry Auto **and**" in text
    assert "Merely invoking `run-ticket` manually" in text
    assert "Shaped never implies Auto" in text


def test_ticket_priority_uses_delay_loss_and_executor_time() -> None:
    convention = (
        SOURCE_SKILLS / "ticket-up" / "references" / "TICKET_CONVENTION.md"
    ).read_text(encoding="utf-8")
    selector = skill_text(SOURCE_SKILLS, "next-ticket")
    sweep = skill_text(SOURCE_SKILLS, "sweep-tickets")

    assert "expected project value lost while work waits" in convention
    assert "urgent → unblocking → impact → cheap" not in convention
    assert "executor-native serial time" in convention
    assert "compare their ready Tickets together" in selector
    assert "human-plus-AI session" in selector
    assert "Auto alone proves authority, not that a runner exists" in selector
    assert "Do not infer days from traditional feature size" in selector
    assert "**Recover first.**" in sweep
    assert "expected-delay-loss rule" in sweep
    assert "traditional feature size" in sweep


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
    assert "run for that same canonical Ticket" in text
    assert "run with the same identity" not in text
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
    assert "The sweep can operate alone" in text
    assert (
        "without the sweep, missed\ndeliveries and dependency closes are not recovered reliably"
        in text
    )
    assert "Either route can operate alone" not in text


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
        assert "expected-delay-loss rule" in sweep

        ticket_up = skill_text(skills_root, "ticket-up")
        assert "fresh human grant for Auto" in ticket_up
        assert "Shaped never implies Auto" in ticket_up

        selector = skill_text(skills_root, "next-ticket")
        assert "human-plus-AI session" in selector
        assert "Auto alone proves authority, not that a runner exists" in selector

        convention = (
            skills_root / "ticket-up" / "references" / "TICKET_CONVENTION.md"
        ).read_text(encoding="utf-8")
        assert "expected project value lost while work waits" in convention
        assert "urgent → unblocking → impact → cheap" not in convention
