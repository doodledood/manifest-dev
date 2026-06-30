"""
Verify each CLI distribution carries the surviving skill set in the right shape.

- Codex ships native plugins (two plugins under dist/codex/plugins/, registered by
  the repo-root .agents/plugins/marketplace.json). No installer, no agents, no
  namespacing suffixes.
- OpenCode ships a plugin (dist/opencode/plugin/) that registers the skills payload
  via skills.paths and slash-command wrappers via cfg.command. No installer,
  no command files, no namespacing suffixes; qualified skill ids are stripped to
  bare names like Pi.
- Pi ships the full compatible skill set plus prompt-template aliases for the main
  entrypoints; no TypeScript runtime extension.

Reviewers are dimensions of the review-code skill, not standalone agents.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
SYNC_TOOLS = ROOT / ".claude" / "skills" / "sync-tools"

CORE_SKILLS = (
    "auto",
    "review-code",
    "define",
    "do",
    "done",
    "escalate",
    "figure-out",
    "figure-out-team",
    "check-pr",
    "poll-slack",
)
TOOLS_SKILLS = (
    "adr",
    "babysit-pr",
    "handoff",
    "prompt-engineering",
    "review-prompt",
    "review-pr",
    "teach-me",
    "walk-pr",
)
PI_SKILLS = CORE_SKILLS + TOOLS_SKILLS
PI_PROMPTS = ("do", "auto", "babysit-pr")

CODE_REVIEW_DIMENSIONS = {
    "change-intent",
    "code-bugs",
    "code-design",
    "code-maintainability",
    "code-simplicity",
    "code-testability",
    "context-file-adherence",
    "contracts",
    "docs",
    "operational-readiness",
    "prose-value",
    "test-quality",
    "type-safety",
}
RETIRED_REVIEWER_AGENTS = {f"{d}-reviewer" for d in CODE_REVIEW_DIMENSIONS}
REMOVED_SKILLS = ("verify",)


# --------------------------------------------------------------------------
# Codex: plugin-native distribution
# --------------------------------------------------------------------------


def codex_plugin_skills(plugin: str) -> set[str]:
    skills_dir = DIST / "codex" / "plugins" / plugin / "skills"
    return {p.name for p in skills_dir.iterdir() if p.is_dir()}


def test_codex_plugins_carry_their_skill_split() -> None:
    assert codex_plugin_skills("manifest-dev") == set(CORE_SKILLS)
    assert codex_plugin_skills("manifest-dev-tools") == set(TOOLS_SKILLS)
    for plugin in ("manifest-dev", "manifest-dev-tools"):
        for skill in codex_plugin_skills(plugin):
            assert (
                DIST / "codex" / "plugins" / plugin / "skills" / skill / "SKILL.md"
            ).is_file()


def test_codex_code_review_skill_carries_every_dimension() -> None:
    refs = (
        DIST
        / "codex"
        / "plugins"
        / "manifest-dev"
        / "skills"
        / "review-code"
        / "references"
    )
    assert {p.stem for p in refs.glob("*.md")} == CODE_REVIEW_DIMENSIONS


def test_codex_does_not_ship_reviewer_agents_or_removed_skills() -> None:
    # No agents directory at all in the plugin-native distribution.
    assert not (DIST / "codex" / "agents").exists()
    for plugin in ("manifest-dev", "manifest-dev-tools"):
        skills = codex_plugin_skills(plugin)
        for removed in REMOVED_SKILLS:
            assert removed not in skills
        # Retired reviewer agents must not have reappeared as skills.
        assert not (RETIRED_REVIEWER_AGENTS & skills)


def test_codex_marketplace_points_at_existing_plugins() -> None:
    marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )
    for entry in marketplace["plugins"]:
        plugin_dir = ROOT / entry["source"]["path"]
        manifest = json.loads(
            (plugin_dir / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert manifest["name"] == entry["name"]


# --------------------------------------------------------------------------
# OpenCode: plugin-native distribution
# --------------------------------------------------------------------------


def test_opencode_carries_full_skill_split() -> None:
    skills = {
        path.name for path in (DIST / "opencode" / "skills").iterdir() if path.is_dir()
    }
    assert skills == set(CORE_SKILLS) | set(TOOLS_SKILLS)
    for skill in skills:
        assert (DIST / "opencode" / "skills" / skill / "SKILL.md").is_file()


def test_opencode_ships_no_agents() -> None:
    # manifest-dev ships zero agents on every target; OpenCode drops its agents/ dir.
    assert not (DIST / "opencode" / "agents").exists()


def test_former_functional_agents_are_skills_in_every_dist() -> None:
    """The four converted agents now ship as skills, not agents."""
    assert {
        "check-pr",
        "poll-slack",
    } <= codex_plugin_skills("manifest-dev")
    assert "review-prompt" in codex_plugin_skills("manifest-dev-tools")
    for name in (
        "check-pr",
        "poll-slack",
        "review-prompt",
    ):
        assert (DIST / "opencode" / "skills" / name / "SKILL.md").is_file()
        assert (DIST / "pi" / "skills" / name / "SKILL.md").is_file()


# --------------------------------------------------------------------------
# sync-tools references
# --------------------------------------------------------------------------


def test_sync_tools_declares_pi_as_first_class_target() -> None:
    skill = (SYNC_TOOLS / "SKILL.md").read_text(encoding="utf-8")
    assert "`opencode`, `codex`, `pi`" in skill
    assert "dist/{opencode,codex,pi}/" in skill
    assert ".claude/skills/sync-tools/references/{cli}-cli.md" in skill
    assert (SYNC_TOOLS / "references" / "pi-cli.md").is_file()


def test_codex_reference_is_plugin_native() -> None:
    reference = (SYNC_TOOLS / "references" / "codex-cli.md").read_text(encoding="utf-8")
    assert ".codex-plugin/plugin.json" in reference
    assert ".agents/plugins/marketplace.json" in reference
    assert "~/.codex/plugins/cache/" in reference
    # The legacy installer approach is retired.
    assert "TOML config stubs" not in reference
    # manifest-dev ships no agents — all former agents are skills.
    assert "all former agents are skills" in reference


def test_goal_setting_backstop_is_universal_across_source_and_dist() -> None:
    """Unattended-run backstops are a portable capability, not a literal /goal rule.

    Source skills should tell the model to set a harness-native durable goal when the
    host exposes one, and to print a copy-pasteable completion contract only as the
    fallback. Pi must preserve that backstop instead of dropping it for lack of a
    `/goal` command; OpenCode/Codex must not regress to target-only `/goal` prose.
    """
    source_skill_files = [
        ROOT / "claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        ROOT / "claude-plugins/manifest-dev/skills/define/SKILL.md",
        ROOT / "claude-plugins/manifest-dev/skills/auto/SKILL.md",
        ROOT / "claude-plugins/manifest-dev/skills/do/SKILL.md",
    ]
    for path in source_skill_files:
        text = path.read_text(encoding="utf-8")
        assert "goal-setting" in text, path
        assert "completion contract" in text, path
        assert "/goal" not in text, path

    source_docs = [
        ROOT / "README.md",
        ROOT / "claude-plugins/README.md",
        ROOT / "claude-plugins/manifest-dev/README.md",
        ROOT / "claude-plugins/manifest-dev/.claude-plugin/plugin.json",
    ]
    for path in source_docs:
        assert "goal-setting" in path.read_text(encoding="utf-8"), path

    pi_ref = (SYNC_TOOLS / "references" / "pi-cli.md").read_text(encoding="utf-8")
    assert "universal goal-setting backstop guidance" in pi_ref
    assert "Pi has no `/goal` command, so drop" not in pi_ref
    assert "drop the `/goal` unattended-execution backstop" not in pi_ref

    opencode_ref = (SYNC_TOOLS / "references" / "opencode-cli.md").read_text(
        encoding="utf-8"
    )
    assert "universal goal-setting backstop guidance" in opencode_ref
    assert "keep the `/goal` blocks" not in opencode_ref

    pi_skill_files = [
        DIST / "pi/skills/figure-out/references/autonomous.md",
        DIST / "pi/skills/define/SKILL.md",
    ]
    for path in pi_skill_files:
        text = path.read_text(encoding="utf-8")
        assert "goal-setting" in text, path
        assert "completion contract" in text, path
        assert "/goal" not in text, path

    dist_skill_files = [
        DIST / "codex/plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        DIST / "codex/plugins/manifest-dev/skills/define/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/do/SKILL.md",
        DIST / "opencode/skills/figure-out/references/autonomous.md",
        DIST / "opencode/skills/define/SKILL.md",
        DIST / "opencode/skills/auto/SKILL.md",
        DIST / "opencode/skills/do/SKILL.md",
    ]
    stale_phrases = (
        "print the copy-pasteable full-chain backstop below so the user can relaunch under it",
        "launch `/do` under a `/goal`",
        "launch under a self-contained `/goal`",
        "print a copy-pasteable backstop for the run: a `/goal`",
    )
    for path in dist_skill_files:
        text = path.read_text(encoding="utf-8")
        assert "goal-setting" in text, path
        for stale in stale_phrases:
            assert stale not in text, f"{path}: stale goal wording {stale!r}"


def test_do_completion_contract_requires_auditable_gate_ledger() -> None:
    """The continuation backstop must make incomplete verification non-terminal."""
    do_files = [
        ROOT / "claude-plugins/manifest-dev/skills/do/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/do/SKILL.md",
        DIST / "opencode/skills/do/SKILL.md",
        DIST / "pi/skills/do/SKILL.md",
    ]
    required_do_phrases = (
        "gate ledger covering every Acceptance Criterion and Global Invariant",
        "latest independent verifier verdict",
        "freshness relative to the last relevant implementation change",
        "Completion requires every listed gate to have fresh PASS evidence",
        "Do not accept self-attestation",
    )
    for path in do_files:
        text = path.read_text(encoding="utf-8")
        for phrase in required_do_phrases:
            assert phrase in text, f"{path}: missing {phrase!r}"

    parent_goal_files = [
        ROOT / "claude-plugins/manifest-dev/skills/auto/SKILL.md",
        ROOT / "claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "codex/plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md",
        DIST / "opencode/skills/auto/SKILL.md",
        DIST / "opencode/skills/babysit-pr/SKILL.md",
        DIST / "pi/skills/auto/SKILL.md",
        DIST / "pi/skills/babysit-pr/SKILL.md",
    ]
    for path in parent_goal_files:
        text = path.read_text(encoding="utf-8")
        assert "manifest gate ledger" in text, path
        assert "fresh independent verifier" in text, path
        assert "self-attestation" in text, path


def test_auto_parent_goal_carries_autonomous_read_checkpoint() -> None:
    """The /auto parent backstop carries Read rigor as a phase checkpoint."""
    auto_files = [
        ROOT / "claude-plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "opencode/skills/auto/SKILL.md",
        DIST / "pi/skills/auto/SKILL.md",
    ]
    required_phrases = (
        "The terminal success condition is outcome-gated",
        "phase checkpoint before `/define`",
        "full-anatomy Read checkpoint before /define",
        "every load-bearing branch pressed",
        "Evidence Ledger explicit",
        "assumptions separated from verified and inferred claims",
        "independent re-derivation run or explicitly unavailable",
        "rival set no longer moving",
        "the Read checkpoint is not complete if it only localizes where the symptom concentrates",
        "name the concrete mechanism",
        "naming the surviving explanations",
        "feasible probes that could distinguish them were run",
        "Treat a missing or weak Read checkpoint as a phase defect",
        "manifest gate ledger",
    )
    forbidden_phrases = (
        "contract must carry both child completion bars",
        "until figure-out names a Read",
    )
    for path in auto_files:
        text = path.read_text(encoding="utf-8")
        for phrase in required_phrases:
            assert phrase in text, f"{path}: missing {phrase!r}"
        for phrase in forbidden_phrases:
            assert phrase not in text, f"{path}: forbidden {phrase!r}"


def test_autonomous_figure_out_supplements_weak_parent_backstops() -> None:
    """A weak parent is supplemented without replacing it with a Read-only goal."""
    files = [
        ROOT / "claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        DIST / "codex/plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        DIST / "opencode/skills/figure-out/references/autonomous.md",
        DIST / "pi/skills/figure-out/references/autonomous.md",
    ]
    required_phrases = (
        "Suppress it only when",
        "carries this Read-completion contract",
        "If the visible parent is weak",
        'only says "Read named"',
        "do not replace or narrow that parent into a Read-only goal",
        "Augment the parent only when the harness can do so without narrowing it",
        "print or carry this Read-level contract as a local checkpoint",
        "preserve the broader parent",
    )
    forbidden_phrases = (
        "supplement it by setting or printing this Read-level contract",
    )
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in required_phrases:
            assert phrase in text, f"{path}: missing {phrase!r}"
        for phrase in forbidden_phrases:
            assert phrase not in text, f"{path}: forbidden {phrase!r}"


def test_autonomous_diagnosis_goal_requires_mechanism_or_earned_underdetermination() -> (
    None
):
    expected = (
        "For diagnosis-shaped work, finding where the symptom concentrates is only "
        "localization, not a complete Read: name the concrete mechanism — the "
        "variable, difference, or sequence that produces the symptom, including "
        "why this case differs when the question is comparative — or earn an "
        "underdetermined Read by naming the surviving explanations and showing "
        "which feasible probes that could distinguish them were run, what they "
        "showed, or why they were blocked."
    )
    files = [
        ROOT / "claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        DIST / "codex/plugins/manifest-dev/skills/figure-out/references/autonomous.md",
        DIST / "opencode/skills/figure-out/references/autonomous.md",
        DIST / "pi/skills/figure-out/references/autonomous.md",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert expected in text, path


def test_continuation_backstop_is_owned_by_top_level_entrypoint() -> None:
    """Nested workflow skills should not set competing narrower goals."""
    define_files = [
        ROOT / "claude-plugins/manifest-dev/skills/define/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/define/SKILL.md",
        DIST / "opencode/skills/define/SKILL.md",
        DIST / "pi/skills/define/SKILL.md",
    ]
    for path in define_files:
        text = path.read_text(encoding="utf-8")
        assert "Deliver <deliverables>" not in text, path
        assert "/define does not set a separate /do goal" in text, path
        assert (
            "/do reads the manifest and owns the manifest-completion contract" in text
        ), path

    do_files = [
        ROOT / "claude-plugins/manifest-dev/skills/do/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/do/SKILL.md",
        DIST / "opencode/skills/do/SKILL.md",
        DIST / "pi/skills/do/SKILL.md",
    ]
    for path in do_files:
        text = path.read_text(encoding="utf-8")
        assert "When /do is the top-level execution entrypoint" in text, path
        assert "broader parent workflow backstop" in text, path
        assert "do not set or print a second narrower goal" in text, path

    auto_files = [
        ROOT / "claude-plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "codex/plugins/manifest-dev/skills/auto/SKILL.md",
        DIST / "opencode/skills/auto/SKILL.md",
        DIST / "pi/skills/auto/SKILL.md",
    ]
    for path in auto_files:
        text = path.read_text(encoding="utf-8")
        assert "/auto` owns this backstop as the chain entrypoint" in text, path
        assert "`figure-out --autonomous` suppresses" in text, path
        assert "/do` operates under the existing full-chain contract" in text, path

    babysit_files = [
        ROOT / "claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md",
        DIST / "codex/plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md",
        DIST / "opencode/skills/babysit-pr/SKILL.md",
        DIST / "pi/skills/babysit-pr/SKILL.md",
    ]
    for path in babysit_files:
        text = path.read_text(encoding="utf-8")
        assert (
            "including the `--manifest` path where `/define` is skipped" in text
        ), path
        assert "outer backstop for the tend" in text, path
        assert "should not set or print competing narrower goals" in text, path


# --------------------------------------------------------------------------
# Pi: skill-only package + prompt aliases
# --------------------------------------------------------------------------


def test_pi_package_metadata_points_to_generated_skills_and_prompts() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    assert package["name"] == "@doodledood/manifest-dev-pi"
    assert package["version"] == "1.0.2"
    assert "pi-package" in package["keywords"]
    assert package["pi"] == {
        "skills": ["./dist/pi/skills"],
        "prompts": ["./dist/pi/prompts"],
    }
    assert "extensions" not in package["pi"]
    assert "workspaces" not in package
    assert "exports" not in package
    assert not (ROOT / "pi" / "extensions").exists()
    assert not (ROOT / "packages" / "manifest-dev-pi-tools").exists()


def test_pi_dist_contains_full_skill_set_and_prompt_aliases() -> None:
    skill_dirs = {
        path.name for path in (DIST / "pi" / "skills").iterdir() if path.is_dir()
    }
    prompt_files = {path.stem for path in (DIST / "pi" / "prompts").glob("*.md")}
    metadata = json.loads(
        (DIST / "pi" / "component-namespaces.json").read_text(encoding="utf-8")
    )

    assert skill_dirs == set(PI_SKILLS)
    assert prompt_files == set(PI_PROMPTS)
    assert set(metadata["skills"]) == set(PI_SKILLS)
    assert set(metadata["prompts"]) == set(PI_PROMPTS)
    assert metadata.get("agents", {}) == {}
    assert metadata.get("commands", {}) == {}
    assert metadata.get("tools", {}) == {}
    assert metadata.get("runtime_dependencies", {}) == {}


def test_pi_prompt_aliases_expand_to_matching_skills() -> None:
    expected = {
        "do.md": "Use the do skill with: $ARGUMENTS",
        "auto.md": "Use the auto skill with: $ARGUMENTS",
        "babysit-pr.md": "Use the babysit-pr skill with: $ARGUMENTS",
    }
    for filename, body in expected.items():
        text = (DIST / "pi" / "prompts" / filename).read_text(encoding="utf-8")
        assert body in text
        assert "description:" in text


def test_pi_live_docs_do_not_claim_runtime_verifier_fanout() -> None:
    live_paths = [
        ROOT / "README.md",
        DIST / "pi" / "README.md",
        DIST / "pi" / ".sync-meta.json",
        DIST / "pi" / "component-namespaces.json",
        SYNC_TOOLS / "references" / "pi-cli.md",
    ]
    stale = (
        "manifest-verifier-max-concurrent",
        "MANIFEST_DEV_VERIFIER_MAX_CONCURRENT",
        "manifest_dev_request_verification",
        "manifest_dev_report_outcome",
        "WAIT-PENDING",
        "JSON subprocess verifier fanout",
        "runtime-owned verification",
        "done outcome",
    )
    for path in live_paths:
        text = path.read_text(encoding="utf-8")
        for phrase in stale:
            assert phrase not in text, f"{path}: stale Pi runtime claim {phrase!r}"


def _without_cross_host_review_pr_markers(text: str) -> str:
    """Remove review-pr's literal hidden GitHub marker before skill-id scans.

    The marker is cross-host comment metadata (`<!-- manifest-dev:review-pr ... -->`),
    not a skill activation id; the review-pr skill explicitly says not to namespace-
    rewrite it or comments posted by one host stop matching another's.
    """
    return re.sub(r"<!-- manifest-dev:review-pr[^>]*-->", "", text)


def test_skill_activation_names_are_per_target() -> None:
    """Verifier-activation / chain prose must name skills in each target's own form:
    source + Codex use the canonical plugin-qualified colon form (Claude native;
    Codex plugins keep it), while Pi and OpenCode strip the qualifier to bare skill
    names (no plugin namespace exists to resolve qualified ids there)."""
    qualified = re.compile(r"manifest-dev(?:-tools)?:[a-z]")

    # Source canonical form: colon-qualified, never the unrewritable space form.
    for rel in (
        "claude-plugins/manifest-dev/skills/define/SKILL.md",
        "claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "manifest-dev check-pr skill" not in text
        assert "manifest-dev:check-pr" in text
    review_pr = (
        ROOT / "claude-plugins/manifest-dev-tools/skills/review-pr/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "manifest-dev-tools:review-prompt" in review_pr

    # Cross-plugin verifier activations in task files must also be qualified at the
    # source, or a sync would copy the stale bare id back into the dists.
    prompting = (
        ROOT / "claude-plugins/manifest-dev/skills/define/tasks/PROMPTING.md"
    ).read_text(encoding="utf-8")
    assert "manifest-dev-tools:review-prompt" in prompting
    assert "activates the `review-prompt` skill" not in prompting

    # Pi and OpenCode dists: no plugin-qualified skill ids survive (both invoke
    # skills by bare name).
    for dist_skills in (DIST / "pi" / "skills", DIST / "opencode" / "skills"):
        for path in dist_skills.rglob("*.md"):
            text = _without_cross_host_review_pr_markers(
                path.read_text(encoding="utf-8")
            )
            assert not qualified.search(text), path

    # Codex dist keeps the colon form (plugins are real namespaces there).
    codex_pr = (
        DIST
        / "codex"
        / "plugins"
        / "manifest-dev"
        / "skills"
        / "define"
        / "tasks"
        / "PR_LIFECYCLE.md"
    ).read_text(encoding="utf-8")
    assert "manifest-dev:check-pr" in codex_pr


# --- Durable source<->dist drift guards -----------------------------------------
# These sweep EVERY skill markdown on each surface so a future /sync-tools that
# regenerates dist (it force-full-regenerates when the reference files change)
# cannot silently reintroduce the drift classes this PR fixed. They assert the
# per-target invariant holds everywhere, not just on the files edited by hand.

SOURCE_SKILL_ROOTS = (
    ROOT / "claude-plugins" / "manifest-dev" / "skills",
    ROOT / "claude-plugins" / "manifest-dev-tools" / "skills",
)
DIST_QUALIFIER_KEEPING_ROOTS = (
    DIST / "codex" / "plugins" / "manifest-dev" / "skills",
    DIST / "codex" / "plugins" / "manifest-dev-tools" / "skills",
)
# Non-canonical activation forms — they must never appear in source or in the
# qualifier-keeping Codex dist (the strip substitution for Pi/OpenCode only handles
# the canonical colon form, so anything else would survive a sync in a stale shape).
_UNREWRITABLE_FORMS = (
    "manifest-dev check-pr skill",  # space form instead of colon
    "activates the `review-prompt` skill",  # bare cross-plugin activation
)


def _skill_markdowns(*roots: Path) -> list[Path]:
    return [p for root in roots for p in root.rglob("*.md")]


def test_no_unrewritable_activation_forms_in_source_or_qualifier_dists() -> None:
    """Source and the colon-keeping Codex dist must use the canonical plugin-qualified
    activation form everywhere — never the space form or a bare cross-plugin id the
    qualifier-strip substitution can't recognize."""
    for path in _skill_markdowns(*SOURCE_SKILL_ROOTS, *DIST_QUALIFIER_KEEPING_ROOTS):
        text = path.read_text(encoding="utf-8")
        for bad in _UNREWRITABLE_FORMS:
            assert bad not in text, f"{path}: stale activation form {bad!r}"


def test_bare_name_dists_have_no_qualified_skill_ids_anywhere() -> None:
    """Pi invokes /skill:<name> and OpenCode discovers bare skill names, so no
    manifest-dev(-tools): qualified id may survive in ANY of their skill markdowns
    (sweep, not just sampled files)."""
    qualified = re.compile(r"manifest-dev(?:-tools)?:[a-z]")
    for path in _skill_markdowns(DIST / "pi" / "skills", DIST / "opencode" / "skills"):
        text = _without_cross_host_review_pr_markers(path.read_text(encoding="utf-8"))
        assert not qualified.search(text), path


def test_check_pr_stays_workflow_neutral_on_every_surface() -> None:
    """check-pr is a workflow-neutral reporter and should not grow caller-specific
    pending tokens or workflow routing state in source or dist copies."""
    check_pr_copies = [
        ROOT / "claude-plugins/manifest-dev/skills/check-pr/SKILL.md",
        DIST / "pi" / "skills" / "check-pr" / "SKILL.md",
        DIST / "opencode" / "skills" / "check-pr" / "SKILL.md",
        DIST
        / "codex"
        / "plugins"
        / "manifest-dev"
        / "skills"
        / "check-pr"
        / "SKILL.md",
    ]
    for path in check_pr_copies:
        assert path.exists(), path
        forbidden = "WAIT" + "-PENDING"
        assert forbidden not in path.read_text(encoding="utf-8"), path
