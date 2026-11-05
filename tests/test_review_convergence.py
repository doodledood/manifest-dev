"""Hold the impact-based review boundary and its repair-history handoffs.

Behavior drives exercise decisions; these locks prevent contradictory prompt owners.
ADR: 20261105-review-severity-follows-consequence
Also holds 20261105-repairs-track-the-accepted-promise.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(params=[ROOT / "claude-plugins", ROOT / "dist/codex/plugins"])
def plugins(request: pytest.FixtureRequest) -> Path:
    return Path(request.param)


def skill(plugins: Path, name: str, file: str = "SKILL.md") -> str:
    return (plugins / "manifest-dev/skills" / name / file).read_text()


def test_severity_cannot_make_rarity_a_license_to_drop_wrong_behavior(
    plugins: Path,
) -> None:
    review = skill(plugins, "review-code")
    assert "no LOW" not in review
    assert (
        "polish or a nit of any kind: style, naming, structure, or otherwise" in review
    )
    assert "optional polish" not in review.lower()
    assert (
        "correctness or safety failure or broken binding promise received as Low"
        in review
    )
    assert "All Critical, High and Medium findings block" not in review
    assert "**Threshold**: no MEDIUM+" not in review
    assert "caller chooses the acceptance threshold and handling policy" in review
    for reference in (plugins / "manifest-dev/skills/review-code/references").glob(
        "*.md"
    ):
        text = reference.read_text()
        assert "Low for unusual" not in text, reference
        assert "**Low**: Rare scenarios" not in text, reference
        assert "**Low**: Type holes with a narrow trigger" not in text, reference
        assert "Documentation issues are capped" not in text, reference
        assert "presentation-only" not in text.lower(), reference


def test_task_files_cannot_recreate_the_retired_low_threshold(plugins: Path) -> None:
    for name in ("CODING", "BUG", "PROMPTING"):
        text = skill(plugins, "define", f"tasks/{name}.md")
        assert "no LOW+" not in text
        assert "no MEDIUM+" in text


def test_repair_history_survives_finding_and_commit_identity_changes(
    plugins: Path,
) -> None:
    executor = skill(plugins, "do")
    assert "underlying promise" in executor
    assert "across finding IDs and commits" in executor
    assert "two repairs on that promise have failed" in executor
    assert "before a third" in executor
    assert "contract, Appetite and scope" in executor
    assert "commit wording does not strengthen acceptance" in executor
    recovery = skill(plugins, "do", "references/LOG.md")
    assert "underlying promise and its accepted source" in recovery
    intent = skill(plugins, "review-code", "references/change-intent.md")
    assert "cannot strengthen that contract" in intent


def test_pr_consolidation_filters_consequences_before_severity_labels(
    plugins: Path,
) -> None:
    for name in ("review-pr", "review-pr-holistic", "review-pr-judgment"):
        text = (plugins / "manifest-dev-tools/skills" / name / "SKILL.md").read_text()
        assert "caller" in text.lower() and "policy" in text.lower()
        assert "optional polish" not in text.lower()
        assert (
            "correctness or safety failures and broken binding promises" in text.lower()
        )
        assert "regrad" in text.lower()
        assert "presentation-only" not in text
        assert "except defect-class" not in text
        assert "drop-Low" not in text
        assert "other than defect-class" not in text


def test_nit_classification_does_not_encode_caller_optionality(
    plugins: Path,
) -> None:
    for name, reference in [
        ("define", "references/DOCS-STYLE-REFERENCE.md"),
        ("define", "references/WRITING-REFERENCE.md"),
        ("review-writing", "SKILL.md"),
        ("review-design", "SKILL.md"),
    ]:
        text = skill(plugins, name, reference)
        normalized = " ".join(text.lower().split())
        assert "polish or a nit of any kind" in normalized
        assert "optional polish" not in normalized
        assert "style, naming, structure, or otherwise" in normalized
        assert "presentation-only" not in normalized
        assert "without cost to comprehension" not in text
    docs = skill(plugins, "define", "references/DOCS-STYLE-REFERENCE.md")
    low_row = next(line for line in docs.splitlines() if line.startswith("| **LOW**"))
    assert "serial commas" in low_row
    executor = skill(plugins, "do")
    assert "Manifest's chosen severities, categories and acceptance" in executor
    assert "before applying that policy" in executor
    assert "Shared review gates pass" not in executor
    assert "optional polish" not in executor
    assert "presentation-only" not in executor
    prompt_review = (
        plugins / "manifest-dev-tools/skills/review-prompt/SKILL.md"
    ).read_text()
    assert "polish or a nit of any kind" in prompt_review
    assert "optional polish" not in prompt_review


def test_mechanical_failure_cannot_disappear_as_an_intent_mismatch(
    plugins: Path,
) -> None:
    bugs = skill(plugins, "review-code", "references/code-bugs.md")
    assert "broken bounds that omit data" in bugs
    assert "stays here even when it also violates" in bugs
    assert "implementation choice cannot waive the accepted contract" in bugs
    assert "logic errors, behavioral mismatches" not in bugs
    intent = skill(plugins, "review-code", "references/change-intent.md")
    assert "cannot waive that promise" in intent


def test_caller_owns_gate_and_handling_without_changing_severity(plugins: Path) -> None:
    reviewer = " ".join(skill(plugins, "review-code").split())
    assert "Choosing to address a Low does not raise its severity" in reviewer
    assert (
        "Report classifications without a verdict when no gate is requested" in reviewer
    )
    assert "If a verdict is requested without an acceptance policy" in reviewer
    assert "Every dimension uses the same threshold" not in reviewer
    builder = skill(plugins, "define")
    assert (
        "The skill owns classification; the Manifest owns what fails the gate"
        in builder
    )
    coding = skill(plugins, "define", "tasks/CODING.md")
    assert "the gate states the chosen threshold explicitly" in coding
    assert "thresholds in the table above orient the author, not the gate" not in coding
    holistic = (
        plugins / "manifest-dev-tools/skills/review-pr-holistic/SKILL.md"
    ).read_text()
    assert "Preserve Low findings retained by the caller's chosen policy" in holistic
    assert "consolidation does not impose its own severity cutoff" in holistic
