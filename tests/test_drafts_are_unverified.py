"""A disposable draft is never verified, and is shown in minutes.

Holds the decisions in
docs/adr/20261031-figure-out-drafts-are-unverified-and-shown-in-minutes.md and
docs/adr/20261031-autonomous-figure-out-shows-a-draft-to-an-owner-it-can-reach.md, and
docs/adr/20261031-do-takes-a-reaction-to-a-draft-as-direction-not-a-lock.md for /do and the
Taste paths.

A draft exists so the user can judge what they cannot put into words. The rule that kept it
cheap once lived in the design skill and was lost when that mode was retired; a draft was then
pulled into review rounds and planted-break checks that took hours. Each assertion below pins one
line that keeps a draft out of a check, or keeps a reaction to a draft from becoming a permanent
rule, so dropping it fails here before it ships.
"""

from __future__ import annotations

import re
from pathlib import Path

SKILLS = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins"
    / "manifest-dev"
    / "skills"
)
FIGURE_OUT = SKILLS / "figure-out" / "SKILL.md"
AUTONOMOUS = SKILLS / "figure-out" / "references" / "autonomous.md"
DEFINE = SKILLS / "define" / "SKILL.md"
TASTE = SKILLS / "figure-out" / "references" / "TASTE.md"
DO = SKILLS / "do" / "SKILL.md"
HARVEST = SKILLS / "do" / "references" / "HARVEST.md"


def _flat(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def _bullet(text: str, opening: str) -> str:
    """The figure-out spine bullet that opens with `opening`, up to the next bullet."""
    start = text.index(f"- {opening}")
    end = text.find(" - ", start + 2)
    return text[start:] if end == -1 else text[start:end]


def test_the_draft_bullet_states_its_purpose_and_that_nothing_checks_it() -> None:
    draft = _bullet(
        _flat(FIGURE_OUT), "When the read implies making something, also offer"
    )
    assert "a way for the user to judge what they cannot put into words" in draft
    assert (
        "draws out criteria they cannot state and agrees a general direction" in draft
    )
    assert "rough, not sloppy — and never perfect it" in draft
    assert "A draft is never verified, tested, reviewed or gated" in draft
    assert "no harness or recipe run, no scratch break" in draft
    assert (
        "no review skill, and no design measuring or checking tool run on it" in draft
    )
    # The terms these words replace were never defined where a reader meets them.
    assert "design instrument" not in draft
    assert "design-check round" not in draft
    assert "The user's reaction is its only check." in draft


def test_the_draft_bullet_bounds_the_time_and_says_what_to_cut() -> None:
    draft = _bullet(
        _flat(FIGURE_OUT), "When the read implies making something, also offer"
    )
    assert "within about 15 minutes of agent working time" in draft
    assert "keep each iteration to minutes" in draft
    assert "cut it down to the question being judged rather than show it late" in draft
    assert "one standalone throwaway file with fake data" in draft
    assert "the draft is done" in draft
    assert "changes again only when the user asks" in draft
    # Choosing a variant is choosing the direction, so no line may read as refining it after.
    assert "the variant the user chooses is the direction, so drop the rest" in draft
    assert "continue with one" not in draft


def test_the_design_step_runs_no_review_loop_on_a_draft() -> None:
    draft = _bullet(
        _flat(FIGURE_OUT), "When the read implies making something, also offer"
    )
    assert (
        "that it is a draft no review loop runs on — no review skill, none of the design "
        "skill's optional measuring instruments, no second pass" in draft
    )
    assert "no review skill, no instrument, no second pass" not in draft


def test_the_verification_bullet_excludes_a_draft() -> None:
    check = _bullet(
        _flat(FIGURE_OUT), "When the read implies making something, state exactly"
    )
    assert "repaired as part of the work" in check
    assert (
        "None of this applies to a disposable draft (next bullet), which nothing checks."
        in check
    )


def test_autonomous_mode_shows_a_draft_to_an_owner_it_can_reach() -> None:
    text = _flat(AUTONOMOUS)
    assert (
        "a channel that can show the owner an artifact and return their reaction"
        in text
    )
    assert "accept the offer: produce the draft under `SKILL.md`'s draft rules" in text
    assert "keep working independent branches while it is out" in text
    assert (
        "Only where no reaction can reach the owner does the draft offer take the second branch"
        in text
    )
    assert "The draft offer always takes the second branch" not in text


def test_define_loads_no_task_file_for_a_draft() -> None:
    text = _flat(DEFINE)
    assert (
        "A disposable draft made only to get a person's reaction loads no task file — no "
        "Quality Gate and no Default — because that reaction is its check." in text
    )
    assert "nothing reviews, tests or checks the draft's quality" in text
    assert "keep the draft's Deliverable outside their gates" in text


def _section(text: str, heading: str) -> str:
    """The `## heading` section of a flattened file, up to the next `## ` heading."""
    start = text.index(f"## {heading}")
    end = text.find(" ## ", start + 3)
    return text[start:] if end == -1 else text[start:end]


def test_do_keeps_the_draft_throwaway_and_makes_the_decision_durable() -> None:
    text = _flat(DO)
    assert "A disposable draft is the exception: a throwaway rendering" in text
    assert (
        "made only so a person can react to what they cannot yet put into words" in text
    )
    assert (
        "never perfected or verified beyond reaching that person with the question it poses"
        in text
    )
    assert (
        "What the run makes durable is the decision and the criteria their reaction draws out, "
        "never the draft." in text
    )
    # The draft exists to pose a choice; an unattended run does not guess it.
    assert (
        "The choice it poses waits for that person's reaction, and work that depends on the "
        "choice holds until it arrives." in text
    )


def test_do_reads_the_draft_rule_when_a_reaction_arrives() -> None:
    text = _flat(DO)
    assert "receives a correction or a reaction to a disposable draft" in text
    assert (
        "a reaction to a draft steers the work's direction and locks only what reaches past it"
        in text
    )
    # Taste on reversal points to the rule rather than restating it, and its own trigger (a call
    # this run made) does not refuse what the rule routes there.
    assert (
        "A reaction to a disposable draft (defined below) drafts an entry exactly when "
        "`references/HARVEST.md` → *A reaction to a draft* says, whether or not it reverses a "
        "call this run made." in text
    )


def test_harvest_takes_a_reaction_to_a_draft_as_direction_and_captures_it() -> None:
    rule = _section(_flat(HARVEST), "A reaction to a draft")
    assert "A reaction to it is not a correction" in rule
    assert (
        "By default the reaction steers the direction the draft was made to settle, and the "
        "design behind it, and installs no lock and drafts no Taste entry." in rule
    )
    assert "Capture every reaction, whatever else it does." in rule
    assert "They never go back into the draft" in rule
    assert "Lock only what the reaction shows reaches past the draft" in rule
    assert "**A requirement or constraint on the real work**" in rule
    assert (
        "**A personal lean the person states as reaching beyond this artifact, with a reason**"
        in rule
    )
    assert "whether or not it reverses a call this run made" in rule
    assert "A lean with no stated reason is captured only." in rule
    assert (
        "When it is unclear whether a reaction reaches past the draft, capture it and do not "
        "lock it or draft a Taste entry" in rule
    )


def test_harvest_gives_an_example_of_each_case() -> None:
    rule = _section(_flat(HARVEST), "A reaction to a draft")
    assert '"Go with B, but less dense." Direction only' in rule
    assert "A requirement on the real work" in rule
    assert "A personal lean with a reason, reaching past this draft" in rule


def test_figure_out_and_define_do_not_take_a_draft_reaction_as_taste() -> None:
    assert (
        "A reaction to a disposable draft is about that draft's direction, and is not taste "
        "unless the user states it as reaching beyond that artifact." in _flat(TASTE)
    )
    assert (
        "is about that draft's direction, not such a reversal, unless the user states it as "
        "reaching beyond that artifact." in _flat(DEFINE)
    )
