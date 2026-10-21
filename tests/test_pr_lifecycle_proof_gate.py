"""define's pull-request task file carries the gate that a pull request shows the change working.

Holds the decision in docs/adr/20261018-every-pull-request-shows-the-change-working.md: the
proof gate's templated Acceptance Criterion keeps the one-minute top of the description, the rule
that proof never comes from production, media attached with `--attach`, media that still reaches
the pull request through a kept `pr-media/<number>` branch where the upload is unavailable, and
text alone only when neither works — and a rule that drops the `check-pr` lifecycle gate does not
drop it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

TASK_FILE = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md"
)
TITLE = "#### AC-N.M — The pull request shows the change working"
RECORD = "docs/adr/20261018-every-pull-request-shows-the-change-working.md"


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def proof_gate() -> str:
    """The templated proof AC: from its title to the fence that closes the template."""
    text = TASK_FILE.read_text(encoding="utf-8")
    assert (
        TITLE in text
    ), f"{TASK_FILE.name} has no templated proof AC titled {TITLE!r}; see {RECORD}"
    return _flat(text.split(TITLE, 1)[1].split("````", 1)[0])


# Each clause the record decides, as the gate text carries it.
CLAUSES = {
    "one-minute top": (
        "Its top reads in about a minute: what changed and why, how the change was shown "
        "working, the decisions made with the user's calls first, and the debt left."
    ),
    "long lists fold": "Long lists fold",
    "never production": "never on production",
    "proof from the touched checks": "runs of the checks the change touches",
    "screenshots and motion": "screenshots, and motion as a short GIF or video",
    "attached with --attach": (
        "attached to the pull request with `--attach` on `gh pr create`, `gh pr edit` or "
        "`gh pr comment` (`gh` 2.99 or later)"
    ),
    "media reaches the pull request without the upload": (
        "Where that upload is unavailable — `gh` older than 2.99, GitHub Enterprise Server, a "
        "token the upload refuses, or a network that blocks it — the media still reaches the "
        "pull request. It is committed to a branch named `pr-media/<pull request number>` that "
        "shares no history with the code and is never merged, and each file is linked by that "
        "commit"
    ),
    "media branch kept": "The branch stays after the pull request closes",
    "text alone only as a last resort": (
        "Only when neither way works is the proof command output alone, and the description "
        "names what was tried."
    ),
    "judged on the live pull request": "read fresh from GitHub on every evaluation",
    "declared kind": "Judgment gate.",
}


@pytest.mark.parametrize("clause", CLAUSES)
def test_proof_gate_keeps_each_recorded_clause(clause: str) -> None:
    assert (
        CLAUSES[clause] in proof_gate()
    ), f"{TASK_FILE.name}'s proof gate lost its {clause} clause; see {RECORD}"


def test_dropping_the_lifecycle_gate_leaves_the_proof_gate() -> None:
    text = TASK_FILE.read_text(encoding="utf-8")
    quality_gates = _flat(text.split("## Quality Gates", 1)[1].split("###", 1)[0])
    assert (
        "A rule or Taste entry about the lifecycle gate — CI, review feedback, mergeability — "
        "does not bear on the proof gate" in quality_gates
    ), f"{TASK_FILE.name} no longer keeps the proof gate apart from the lifecycle gate; see {RECORD}"
