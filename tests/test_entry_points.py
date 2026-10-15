"""The set of skills a user can invoke changes only on purpose.

Users reach new capabilities through figure-out, define, do and auto; other skills are steps
those four call, or optional extras. A new user-invocable skill is a new name to remember, so
adding one has to be a deliberate edit here rather than a side effect of a new SKILL.md. See
docs/adr/20261013-new-capabilities-live-inside-the-four-workflow-entry-points.md.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS = REPO_ROOT / "claude-plugins"

USER_INVOCABLE = {
    "manifest-dev": {
        "auto",
        "check-pr",
        "define",
        "design",
        "do",
        "figure-out",
        "figure-out-team",
        "help",
        "next-ticket",
        "review-code",
        "review-design",
        "review-writing",
        "run-ticket",
        "setup-project",
        "sweep-tickets",
        "ticket-up",
    },
    "manifest-dev-tools": {
        "babysit-pr",
        "eli5",
        "handoff",
        "manifest-to-goal",
        "prompt-engineering",
        "review-pr",
        "review-prompt",
        "teach-me",
        "walk-pr",
    },
}

INVOCABLE_FALSE = re.compile(r"^user-invocable:\s*false\s*$", re.MULTILINE)


def user_invocable(plugin: str) -> set[str]:
    found = set()
    for skill in sorted((PLUGINS / plugin / "skills").glob("*/SKILL.md")):
        frontmatter = skill.read_text(encoding="utf-8").split("---", 2)[1]
        if not INVOCABLE_FALSE.search(frontmatter):
            found.add(skill.parent.name)
    return found


# Holds the decision in docs/adr/20261013-new-capabilities-live-inside-the-four-workflow-entry-points.md.
# Holds the decision in docs/adr/20260809-init-context-skill-lives-in-core.md.
# Holds the decision in docs/adr/20260901-design-skill-pair-distills-research-eval-deferred.md.
# Holds the decision in docs/adr/20261015-a-help-skill-explains-manifest-dev-in-simplified-technical-english.md.
def test_user_invocable_skills_are_the_declared_set() -> None:
    for plugin, expected in USER_INVOCABLE.items():
        actual = user_invocable(plugin)
        assert actual == expected, (
            f"{plugin}: user-invocable skills changed. Added: {sorted(actual - expected)}; "
            f"removed: {sorted(expected - actual)}. A new skill users must remember needs a "
            f"decision; otherwise mark it `user-invocable: false` and reach it from figure-out, "
            f"define, do or auto."
        )
