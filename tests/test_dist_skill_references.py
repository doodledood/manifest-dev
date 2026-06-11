"""
Verify each CLI distribution carries the surviving skill set in the right shape.

- Codex ships native plugins (two plugins under dist/codex/plugins/, registered by
  the repo-root .agents/plugins/marketplace.json). No installer, no agents, no
  namespacing suffixes.
- OpenCode ships a plugin (dist/opencode/plugin/) that registers the skills payload
  via skills.paths. No installer, no commands, no namespacing suffixes; qualified
  skill ids are stripped to bare names like Pi.
- Pi ships compatible shared skills (incl. review-code) plus a two-package runtime
  (core @doodledood/manifest-dev-pi, tools @doodledood/manifest-dev-pi-tools).

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
PI_SKILLS = (
    "adr",
    "review-code",
    "define",
    "figure-out",
    "figure-out-team",
    "check-pr",
    "handoff",
    "prompt-engineering",
    "review-prompt",
    "review-pr",
    "poll-slack",
    "teach-me",
    "walk-pr",
)
PI_EXCLUDED_RUNTIME_SKILLS = ("do", "done", "escalate")
PI_EXTENSION_WRAPPER_SKILLS = ("auto", "babysit-pr")
PI_CORE_COMMANDS = ("do", "auto")
PI_TOOLS_COMMANDS = ("babysit-pr",)
PI_EXTENSION = ROOT / "pi" / "extensions" / "manifest-dev.ts"
PI_EXTENSION_RUNTIME = ROOT / "pi" / "extensions" / "manifest-dev-runtime.ts"
PI_TOOLS_EXTENSION = (
    ROOT
    / "packages"
    / "manifest-dev-pi-tools"
    / "pi"
    / "extensions"
    / "manifest-dev-tools.ts"
)

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


# --------------------------------------------------------------------------
# Pi: two-package runtime + compatible skills
# --------------------------------------------------------------------------


def test_pi_package_metadata_points_to_generated_skills_and_extension() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    assert "pi-package" in package["keywords"]
    # The repo-root Pi package loads BOTH extensions so a single
    # `pi install git:...@main` registers /do, /auto (core) and /babysit-pr (tools).
    assert package["pi"]["extensions"] == [
        "./pi/extensions/manifest-dev.ts",
        "./packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts",
    ]
    assert package["pi"]["skills"] == ["./dist/pi/skills"]
    assert package["peerDependencies"] == {
        "@earendil-works/pi-coding-agent": "*",
    }
    assert PI_EXTENSION.is_file()
    assert PI_EXTENSION_RUNTIME.is_file()
    assert PI_TOOLS_EXTENSION.is_file()


def test_pi_split_into_core_and_tools_packages() -> None:
    core = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    tools = json.loads(
        (ROOT / "packages" / "manifest-dev-pi-tools" / "package.json").read_text(
            encoding="utf-8"
        )
    )

    assert core["name"] == "@doodledood/manifest-dev-pi"
    assert tools["name"] == "@doodledood/manifest-dev-pi-tools"
    # Tools depends on core via a local file path so git installs resolve the
    # private repo-root package instead of hitting the public registry (E404).
    assert tools["dependencies"]["@doodledood/manifest-dev-pi"] == "file:../.."
    assert tools["version"] == core["version"]
    assert tools["peerDependencies"] == {
        "@earendil-works/pi-coding-agent": "*",
    }
    # Tools is repo-root-only: it has NO standalone `pi.extensions`, so it is never
    # installed as its own Pi package (which couldn't resolve the relatively-imported
    # core runtime from its own tarball). It loads solely from the repo-root
    # pi.extensions, which lists the tools extension file directly.
    assert "pi" not in tools
    assert core["pi"]["extensions"][1] == (
        "./packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts"
    )
    assert PI_TOOLS_EXTENSION.is_file()


def test_pi_dist_contains_only_compatible_skill_set() -> None:
    skill_dirs = {
        path.name for path in (DIST / "pi" / "skills").iterdir() if path.is_dir()
    }
    metadata = json.loads(
        (DIST / "pi" / "component-namespaces.json").read_text(encoding="utf-8")
    )

    assert skill_dirs == set(PI_SKILLS)
    assert set(metadata["skills"]) == set(PI_SKILLS)
    assert metadata.get("agents", {}) == {}
    assert metadata.get("runtime_dependencies", {}) == {}


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
            assert not qualified.search(path.read_text(encoding="utf-8")), path

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
        assert not qualified.search(path.read_text(encoding="utf-8")), path


def test_check_pr_stays_workflow_neutral_on_every_surface() -> None:
    """check-pr is a workflow-neutral reporter: the caller-side WAIT-PENDING token
    must never leak into it (source or any dist copy). The wait-pending decision is a
    verifier->runtime concern; check-pr only emits its fixed-vocabulary directives."""
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
        assert "WAIT-PENDING" not in path.read_text(encoding="utf-8"), path


def test_wait_pending_contract_lives_in_runtime_and_pi_reference() -> None:
    """The wait-pending contract must live where check-pr is not: the runtime module
    (marker + the verifier-prompt rule the runtime injects when ciOneShot), the routing
    in the extension, and the Pi runtime reference. Guards against the contract being
    dropped (which would silently route wait-only PRs back into repair). The rule MUST be
    in the verifier-prompt builder, not only the executor prompt, or the verifier that has
    to emit the marker never receives it."""
    runtime_mod = PI_EXTENSION_RUNTIME.read_text(encoding="utf-8")
    assert 'WAIT_PENDING_MARKER = "WAIT-PENDING"' in runtime_mod
    # The derivation rule is injected into the gate verifier prompt (reaches the verifier
    # verifier for synthesized AND --manifest runs), gated on ciOneShot.
    assert "CI_WAIT_PENDING_VERIFIER_RULE" in runtime_mod
    assert "buildGateVerifierPrompt" in runtime_mod
    assert "ciOneShot" in runtime_mod
    ext = PI_EXTENSION.read_text(encoding="utf-8")
    assert "isWaitPendingVerification" in ext
    assert (
        "ciOneShot: run.ciOneShot" in ext
    )  # threaded into the verifier prompt at spawn
    pi_ref = (SYNC_TOOLS / "references" / "pi-cli.md").read_text(encoding="utf-8")
    assert "WAIT-PENDING" in pi_ref
    assert "workflow-neutral" in pi_ref


def test_pi_core_extension_registers_do_and_auto_only() -> None:
    content = PI_EXTENSION.read_text(encoding="utf-8")
    for command in PI_CORE_COMMANDS:
        assert f'pi.registerCommand("{command}"' in content
    # babysit-pr lives in the tools package now.
    assert 'pi.registerCommand("babysit-pr"' not in content

    # Runtime orchestration stays in core and is reusable by tools.
    for symbol in (
        "runHarnessVerification",
        "maybeRunHarnessVerification",
        "shouldTriggerHarnessVerification",
        "createRuntimeState",
        "wireRuntimeHooks",
        "registerVerifierFlags",
        "export async function startWrapper",
    ):
        assert symbol in content
    for tool in ("manifest_dev_request_verification", "manifest_dev_report_outcome"):
        assert f'name: "{tool}"' not in content


def test_pi_tools_extension_registers_babysit_pr_over_core_runtime() -> None:
    content = PI_TOOLS_EXTENSION.read_text(encoding="utf-8")
    assert 'pi.registerCommand("babysit-pr"' in content
    assert 'pi.registerCommand("do"' not in content
    assert 'pi.registerCommand("auto"' not in content
    # Reuses the core runtime wiring rather than forking it.
    assert "wireRuntimeHooks" in content
    assert "startWrapper" in content


def test_pi_readmes_document_install_update_and_runtime_boundary() -> None:
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pi_readme = (DIST / "pi" / "README.md").read_text(encoding="utf-8")
    pi_sync_meta = (DIST / "pi" / ".sync-meta.json").read_text(encoding="utf-8")

    for content in (root_readme, pi_readme, pi_sync_meta):
        assert "pi install git:github.com/doodledood/manifest-dev@main" in content
        assert "Harness-level Do" in content or "Harness-level Do runtime" in content
        assert "JSON subprocess" in content
        assert "pi install npm:@gotgenes/pi-subagents" not in content

    assert "/do <manifest-path>" in pi_readme
    assert "/auto <task>" in pi_readme
    assert "/babysit-pr <github-pr-url>" in pi_readme
    pi_markdown = "\n".join(
        path.read_text(encoding="utf-8") for path in (DIST / "pi").rglob("*.md")
    )
    assert "manifest_dev_request_verification" not in pi_markdown
    assert "manifest_dev_report_outcome" not in pi_markdown
