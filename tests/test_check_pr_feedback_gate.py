"""check-pr's third gate inspects the whole review-feedback inbox.

Holds the decision in docs/adr/20261021-check-pr-review-feedback-is-one-inbox.md:
gate 3 covers open review threads, non-empty latest CHANGES_REQUESTED/COMMENTED review
bodies, and inbound human top-level comments (including review-pr-marked ones); it does
not treat APPROVED bodies or unthreaded GitHub-App comments as outstanding; a follow-up
commit does not address a body or comment; unthreaded FAILs are prose, not a new token.
"""

from __future__ import annotations

import re
from pathlib import Path

CHECK_PR = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins/manifest-dev/skills/check-pr/SKILL.md"
)
TASK_FILE = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md"
)
RECORD = "docs/adr/20261021-check-pr-review-feedback-is-one-inbox.md"
REPLY_TOKENS = ("`reply <thread-id>`", "`reply-and-resolve <thread-id>`")
FORBIDDEN_TOKENS = ("`comment <", "`reply-comment", "`reply <comment", "`reply <review")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def skill() -> str:
    return CHECK_PR.read_text(encoding="utf-8")


def canonical_gates() -> str:
    text = skill()
    match = re.search(r"## Canonical gates.*?\n(.*?)(?=\n## )", text, re.DOTALL)
    assert match, f"{CHECK_PR.name} has no Canonical gates section; see {RECORD}"
    return _flat(match.group(1))


def gate_three() -> tuple[str, str]:
    gates = canonical_gates()
    match = re.search(r"3\. \*\*(.+?)\*\* — (.+?)(?=4\. \*\*|$)", gates)
    assert match, f"{CHECK_PR.name} has no numbered gate 3; see {RECORD}"
    return match.group(1), match.group(2)


def test_gate_three_is_the_review_feedback_inbox() -> None:
    title, body = gate_three()
    assert (
        title == "Review feedback addressed"
    ), f"{CHECK_PR.name} gate 3 is {title!r}, not Review feedback addressed; see {RECORD}"
    for needle in (
        "review bodies",
        "CHANGES_REQUESTED",
        "COMMENTED",
        "top-level",
        "manifest-dev:review-pr",
    ):
        assert needle in body, (
            f"{CHECK_PR.name} gate 3 lost {needle!r}; a reviewer can hide asks there; "
            f"see {RECORD}"
        )


def test_gate_three_skips_approved_bodies_and_app_issue_comments() -> None:
    _title, body = gate_three()
    assert "APPROVED" in body, (
        f"{CHECK_PR.name} gate 3 does not name APPROVED bodies, so it cannot skip them; "
        f"see {RECORD}"
    )
    assert re.search(
        r"not |skip|out|except", body, re.I
    ), f"{CHECK_PR.name} gate 3 names APPROVED without excluding it; see {RECORD}"
    assert re.search(
        r"GitHub App|GitHub-App|unthreaded.*[Aa]pp", body
    ), f"{CHECK_PR.name} gate 3 does not exclude unthreaded GitHub-App comments; see {RECORD}"


def test_a_follow_up_commit_does_not_address_a_body_or_comment() -> None:
    _title, body = gate_three()
    assert (
        "follow-up commit" in body
    ), f"{CHECK_PR.name} gate 3 dropped the follow-up-commit addressing rule; see {RECORD}"
    assert re.search(
        r"follow-up commit does not address a (?:body|review body|comment)",
        body,
    ), (
        f"{CHECK_PR.name} gate 3 still lets a follow-up commit address a body or comment; "
        f"see {RECORD}"
    )


def test_reply_tokens_still_require_a_review_thread_id() -> None:
    text = skill()
    for token in REPLY_TOKENS:
        assert token in text, f"{CHECK_PR.name} lost {token}; see {RECORD}"
    assert "review-thread GraphQL ID" in text, (
        f"{CHECK_PR.name} reply tokens no longer require a review-thread GraphQL ID; "
        f"see {RECORD}"
    )
    for bad in FORBIDDEN_TOKENS:
        assert bad not in text, (
            f"{CHECK_PR.name} grew vocabulary token {bad!r}; unthreaded items use prose; "
            f"see {RECORD}"
        )


def test_fail_schema_and_description_use_the_inbox_name() -> None:
    text = skill()
    assert "- Review feedback addressed: PASS | FAIL" in text, (
        f"{CHECK_PR.name} FAIL breakdown still does not report Review feedback addressed; "
        f"see {RECORD}"
    )
    assert (
        "- Threads addressed:" not in text
    ), f"{CHECK_PR.name} FAIL schema still speaks only of threads; see {RECORD}"
    description = text.split("description:", 1)[1].split("\n", 1)[0]
    assert (
        "review bodies" in description or "top-level" in description
    ), f"{CHECK_PR.name} frontmatter still describes only review threads; see {RECORD}"


def test_review_pr_marker_is_inbox_not_skip() -> None:
    gotchas = skill().split("## Gotchas", 1)[1]
    assert (
        "manifest-dev:review-pr" in gotchas
    ), f"{CHECK_PR.name} Gotchas dropped the review-pr marker; see {RECORD}"
    assert re.search(r"inbox|outstanding|this gate", gotchas, re.I), (
        f"{CHECK_PR.name} Gotchas no longer treat the review-pr marker as an inbox signal; "
        f"see {RECORD}"
    )


def test_lifecycle_subject_names_bodies_and_top_level_comments() -> None:
    text = TASK_FILE.read_text(encoding="utf-8")
    subject = text.split("### The lifecycle gate", 1)[1].split("### The proof gate", 1)[
        0
    ]
    flat = _flat(subject)
    assert "review bodies" in flat and "top-level comments" in flat, (
        f"{TASK_FILE.name} lifecycle Subject lost review bodies or top-level comments; "
        f"see {RECORD}"
    )
