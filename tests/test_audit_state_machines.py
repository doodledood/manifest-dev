"""audit-state-machines stays a thin wrapper over autonomous figure-out, pointing at one check.

The audit and review share one statement of the state-machine method, in code-bugs, so the two
cannot drift; the wrapper runs figure-out unattended and with its project-document writes off, so
an audit writes nothing in the audited project.

Holds docs/adr/20261107-a-figure-out-wrapper-sweeps-existing-code-for-state-machines.md and
docs/adr/20261107-review-checks-the-whole-state-machine-a-change-touches.md.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"
WRAPPER = SKILLS / "audit-state-machines" / "SKILL.md"
CODE_BUGS = SKILLS / "review-code" / "references" / "code-bugs.md"
POINTER = "`../review-code/references/code-bugs.md` → *State machines*"
METHOD_STEPS = (
    "Rebuild the whole machine",
    "Confirm every counterexample on the real code",
)


# Holds docs/adr/20261107-a-figure-out-wrapper-sweeps-existing-code-for-state-machines.md.
def test_wrapper_runs_autonomous_figure_out_with_docs_off() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    invoke = re.search(r"Invoke the figure-out skill\b[^.]*\.", text)
    assert invoke, "the wrapper must invoke figure-out"
    for flag in ("`--autonomous`", "`--no-docs`"):
        assert flag in invoke.group(
            0
        ), f"the wrapper's invoke sentence must pass {flag}"


# Holds docs/adr/20261107-review-checks-the-whole-state-machine-a-change-touches.md.
def test_one_statement_of_the_method_shared_by_audit_and_review() -> None:
    wrapper = WRAPPER.read_text(encoding="utf-8")
    assert (
        POINTER in wrapper
    ), "the wrapper must point at code-bugs' State machines section"
    assert re.search(
        r"^## State machines\s*$", CODE_BUGS.read_text(encoding="utf-8"), re.M
    )
    holders = [
        p.relative_to(ROOT)
        for p in (ROOT / "claude-plugins").rglob("*.md")
        if all(step in p.read_text(encoding="utf-8") for step in METHOD_STEPS)
    ]
    assert holders == [
        CODE_BUGS.relative_to(ROOT)
    ], f"the method must live in code-bugs alone: {holders}"
