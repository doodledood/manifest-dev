from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"


def skill_text(root: Path, name: str) -> str:
    return (root / name / "SKILL.md").read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Collapse whitespace so a phrase assertion survives prose re-wrapping."""
    return " ".join(text.split())


def convention_text(root: Path) -> str:
    return (root / "ticket-up" / "references" / "TICKET_CONVENTION.md").read_text(
        encoding="utf-8"
    )


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
    assert "Escalation ends this attempt, not the work" in flat(text)
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
    assert "match every configured effort or type filter" in flat(text)
    assert "whose dependencies are all closed" in text
    assert (
        "dependency-blocked, policy-filtered, and human-assigned items untouched"
        in flat(text)
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
    assert "Never mutate any claim during selection" in flat(text)
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


def test_convention_escalation_releases_the_claim_and_marks_the_ticket() -> None:
    text = convention_text(SOURCE_SKILLS)

    assert "a handoff record carrying a mark automation can recognize" in flat(text)
    assert "retain Auto when present, and release the claim" in flat(text)
    assert "unattended dispatch skips a marked Ticket" in flat(text)
    assert "records the continuation context and clears the mark" in flat(text)
    assert "A venue reference maps how the mark renders" in flat(text)
    assert "Neither path touches a Ticket carrying the escalation mark" in flat(text)
    # The superseded disposition: the claim must not be reused as the pause.
    assert "transfer or preserve its claim" not in flat(text)


def test_run_ticket_escalation_releases_the_claim_and_marks_the_ticket() -> None:
    text = skill_text(SOURCE_SKILLS, "run-ticket")

    assert "<!-- manifest-dev-run-ticket-escalated -->" in text
    assert "apply the venue's escalation mark" in flat(text)
    assert (
        "retain its Auto grant when it is still present, and release the claim"
        in flat(text)
    )
    assert "clears the mark, which makes the Ticket eligible" in flat(text)
    # Ordering is load-bearing: releasing the claim is itself a dispatch event.
    assert "release the claim — in that order, mark first" in flat(text)
    # An escalation mark is a dispatch rule, enforced by dispatchers rather than here.
    assert "never stops a person who invokes this skill on it deliberately" in flat(
        text
    )
    assert "otherwise preserve a claim" not in flat(text)
    assert "Transfer its claim to the identified person" not in flat(text)


def test_sweep_excludes_escalated_tickets_from_the_eligible_set() -> None:
    text = skill_text(SOURCE_SKILLS, "sweep-tickets")

    assert "open Auto Tickets that carry no escalation mark" in flat(text)
    assert "Leave closed, ungranted, escalated," in flat(text)
    assert "remove Auto, clear an escalation mark" in flat(text)
    # Escalated is excluded by the eligible set, not by the recovery branch.
    assert "An escalated Ticket is not one either" in flat(text)


def test_event_eligibility_excludes_escalated_tickets() -> None:
    text = (
        SOURCE_SKILLS / "ticket-up" / "references" / "AUTOMATED_EXECUTION.md"
    ).read_text(encoding="utf-8")

    assert "carries Auto, carries no escalation mark" in flat(text)
    # Why the adapter check is load-bearing rather than a duplicate of the sweep's.
    assert "that release is itself an unassignment event" in flat(text)
    assert "The escalation mark expresses a handoff awaiting a person" in flat(text)
    assert "infrastructure exhaustion assigns a person" in flat(text)


def test_github_venue_renders_the_escalation_mark_as_a_label() -> None:
    text = (SOURCE_SKILLS / "ticket-up" / "references" / "GITHUB_STORE.md").read_text(
        encoding="utf-8"
    )

    assert "| Escalation mark | An `escalated` label on the ticket" in text
    assert (
        "apply the `escalated` label, leave `auto` unchanged, and clear the assignee"
        in flat(text)
    )
    assert "removes the `escalated` label" in flat(text)
    assert (
        "it also requires the `auto` label and the absence of the `escalated` label"
        in flat(text)
    )
    assert "assign the person needed next" not in flat(text)
    # Tidying surfaces a stale escalation; only the continuation step clears the mark.
    assert "clearing that label belongs to the continuation step" in flat(text)


def test_picker_reads_a_ticket_whole_not_just_its_body() -> None:
    text = skill_text(SOURCE_SKILLS, "next-ticket")
    github = (SOURCE_SKILLS / "ticket-up" / "references" / "GITHUB_STORE.md").read_text(
        encoding="utf-8"
    )

    # The rule reaches both points the picker touches a Ticket.
    assert (
        "A Ticket is everything its venue holds for it, not the item body alone"
        in flat(text)
    )
    assert "Present the complete Ticket, its attached context included" in flat(text)
    # Every evaluated candidate is read whole — a subset would let the ranking
    # decide what informs the ranking.
    assert (
        "Read every candidate whole, not just the ones already looking strong"
        in flat(text)
    )
    assert "candidates that actually compete" not in flat(text)
    # The venue reference owns which surfaces those are; the skill stays venue-neutral.
    assert "the venue reference names those surfaces" in flat(text)
    assert "| Ticket context | Everything the issue carries beyond its body" in github


def test_human_picker_needs_no_escalation_special_case() -> None:
    """Releasing the claim is what lets the selector rank escalated work unchanged."""
    text = skill_text(SOURCE_SKILLS, "next-ticket")

    assert "keep only ready Tickets: open, unclaimed, all dependencies done" in flat(
        text
    )
    assert "escalat" not in text.lower()


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

        convention = convention_text(skills_root)
        assert "expected project value lost while work waits" in convention
        assert "urgent → unblocking → impact → cheap" not in convention
        assert "retain Auto when present, and release the claim" in flat(convention)
        assert "transfer or preserve its claim" not in flat(convention)
        assert "<!-- manifest-dev-run-ticket-escalated -->" in text
        assert "open Auto Tickets that carry no escalation mark" in flat(sweep)

        automation = (
            skills_root / "ticket-up" / "references" / "AUTOMATED_EXECUTION.md"
        ).read_text(encoding="utf-8")
        assert "carries Auto, carries no escalation mark" in flat(automation)

        github = (
            skills_root / "ticket-up" / "references" / "GITHUB_STORE.md"
        ).read_text(encoding="utf-8")
        assert "| Escalation mark | An `escalated` label on the ticket" in github
