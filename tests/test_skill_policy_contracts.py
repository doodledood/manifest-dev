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
    assert (
        "When the same criterion fails repeatedly, stop repeating cheap retries and emit a checkpoint recommending a stronger model or stronger review path."
        in skill_text
    )


def test_verify_skill_documents_economy_staged_fanout_contract() -> None:
    skill_text = (
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "verify" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert (
        "| **Maximize parallelism** | Launch all verifiers in a SINGLE message with multiple Task tool calls. Never launch one at a time. |"
        not in skill_text
    )
    assert "Read the execution log as the source of truth for active policy context." in skill_text
    assert (
        "Under `economy`, first pass always runs `criteria-checker` for automated `bash`, `codebase`, and `research` criteria."
        in skill_text
    )
    assert (
        "Under `economy`, first pass also runs any named `subagent` verifier explicitly required by a criterion."
        in skill_text
    )
    assert (
        "This deferral never overrides criteria that explicitly require one of those named agents."
        in skill_text
    )
    assert (
        "- `code-design-reviewer`\n- `code-maintainability-reviewer`\n- `code-simplicity-reviewer`\n- `code-testability-reviewer`\n- `docs-reviewer`\n- `context-file-adherence-reviewer`\n- `type-safety-reviewer`\n- `code-coverage-reviewer`"
        in skill_text
    )
    assert (
        "Under `economy`, if the same criterion fails twice, reintroduce the deferred broad-reviewer set."
        in skill_text
    )
    assert (
        "Under `economy`, repeated failure of the same criterion is a trigger to reintroduce deferred reviewers."
        not in skill_text
    )
    assert "Reintroduce deferred reviewers when the same criterion fails twice." not in skill_text
    assert "Reintroduce deferred reviewers when multiple unrelated criteria fail." in skill_text
    assert "Reintroduce deferred reviewers when a failure suggests design-level ambiguity." in skill_text
    assert "Policy may change orchestration, never completion semantics: every criterion still needs verification." in skill_text
    assert "If no policy context is available, use the baseline/default broad parallel behavior." in skill_text
    assert (
        "Baseline/default behavior: launch broad parallel verification coverage in a single message, consistent with the existing max-parallelism workflow."
        in skill_text
    )


def test_repeat_failure_guidance_stays_explicit_and_recommendation_only() -> None:
    do_skill_text = (
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "do" / "SKILL.md"
    ).read_text(encoding="utf-8")
    verify_skill_text = (
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "verify" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert (
        "When the same criterion fails repeatedly, stop repeating cheap retries and emit a checkpoint recommending a stronger model or stronger review path."
        in do_skill_text
    )
    assert "recommendation-only" in do_skill_text
    assert "automatic model switching" in do_skill_text
    assert (
        "Under `economy`, if the same criterion fails twice, reintroduce the deferred broad-reviewer set."
        in verify_skill_text
    )
    assert (
        "Under `economy`, repeated failure of the same criterion is a trigger to reintroduce deferred reviewers."
        not in verify_skill_text
    )


def test_verify_skill_routes_failures_by_verification_method() -> None:
    skill_text = (
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "verify" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert (
        "For `subagent` failures under `economy`, if the failing criterion explicitly named that verifier, rerun that criterion's named-agent path first instead of immediately adding unrelated broad reviewers."
        in skill_text
    )
    assert (
        "If that `subagent` criterion fails again, treat it as the same-criterion-failed-twice case: reintroduce the deferred broad-reviewer set."
        in skill_text
    )
    assert (
        "If that `subagent` criterion fails again, reintroduce the deferred reviewer set or emit stronger-model guidance when the failure suggests the named path is no longer sufficient."
        not in skill_text
    )
    assert (
        "For `research` failures under `economy`, treat them as potentially high-ambiguity rather than purely mechanical retries."
        in skill_text
    )
    assert (
        "Retry a `research` criterion once with tighter scope or better source targeting; if it still cannot be resolved confidently, report it as a failed automated criterion."
        in skill_text
    )
    assert (
        "If unresolved `research` work reveals a genuinely manual follow-up criterion from the manifest, surface that separate manual handoff for `/escalate`; do not treat unresolved research as a passing result."
        in skill_text
    )
    assert (
        "For `manual` criteria, do not invent retry or downgrade heuristics: keep surfacing them for `/escalate` exactly as manual handoff work."
        in skill_text
    )
    assert (
        "Manual verification never becomes automated just because policy routing is active."
        in skill_text
    )
    assert "emit stronger-model guidance or escalate." not in skill_text
