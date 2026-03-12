from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parent.parent


def test_do_skill_documents_execution_policy_contract() -> None:
    skill_text = (
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "do" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert (
        'If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path] [--policy=<name>]"'
        in skill_text
    )
    assert "Accepted execution policies for v1: `economy`, `balanced`, `max-quality`." in skill_text
    assert "Fresh run with explicit CLI policy: use it and record `policy_source: cli`." in skill_text
    assert "If policy is omitted, default to backward-compatible current behavior and record `policy_source: default`." in skill_text
    assert "If an unknown policy is supplied, warn and fall back to backward-compatible current behavior." in skill_text
    assert "If resuming with an existing execution log, treat the log as the source of truth for active policy." in skill_text
    assert "If CLI policy conflicts with the log policy on resume, keep the log value, warn, and do not switch policy mid-run." in skill_text
    assert "Execution log entries must record both `active_policy` and `policy_source`." in skill_text
    assert "Checkpoint guidance about model choice must remain recommendation-only." in skill_text
    assert "Do not claim automatic model switching or automatic effort changes." in skill_text
