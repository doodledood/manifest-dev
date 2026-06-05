"""
Verify each CLI distribution carries the full skill set with correct namespacing.

The dist payload ships core manifest-dev skills with the `-manifest-dev` suffix
and manifest-dev-tools skills with the `-manifest-dev-tools` suffix.

Also confirms the removed plugin components stay removed:
  - no `verify` skill in any dist
  - no `manifest-verifier` agent in any dist
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
SYNC_TOOLS = ROOT / ".claude" / "skills" / "sync-tools"

CORE_SKILLS = (
    "auto",
    "define",
    "do",
    "done",
    "escalate",
    "figure-out",
    "figure-out-team",
)
TOOLS_SKILLS = (
    "adr",
    "babysit-pr",
    "handoff",
    "prompt-engineering",
    "review-pr",
    "walk-pr",
)
PI_SKILLS = (
    "adr",
    "define",
    "figure-out",
    "figure-out-team",
    "handoff",
    "prompt-engineering",
    "review-pr",
    "walk-pr",
)
PI_EXCLUDED_RUNTIME_SKILLS = ("do", "done", "escalate")
PI_EXTENSION_WRAPPER_SKILLS = ("auto", "babysit-pr")
PI_EXTENSION_COMMANDS = ("manifest-do", "manifest-auto", "manifest-babysit-pr")
PI_EXTENSION_TOOLS: tuple[str, ...] = ()
PI_EXTENSION = ROOT / "pi" / "extensions" / "manifest-dev.ts"
PI_EXTENSION_RUNTIME = ROOT / "pi" / "extensions" / "manifest-dev-runtime.ts"

REMOVED_SKILLS = ("verify",)
REMOVED_AGENTS = ("manifest-verifier",)


def namespace_dist(tmp_path: Path, cli: str) -> Path:
    """Mirror dist/{cli} into tmp_path and run that CLI's install_helpers.

    Per-CLI argv conventions differ — codex uses ``namespace <dir> <cli>``
    in place while opencode copies from ``<src>`` into ``<dst>``.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    src = DIST / cli
    source_copy = tmp_path / "source"
    shutil.copytree(src, source_copy)

    if cli == "codex":
        argv = [
            sys.executable,
            str(source_copy / "install_helpers.py"),
            "namespace",
            str(source_copy),
            cli,
        ]
        subprocess.run(argv, check=True, cwd=source_copy)
        return source_copy

    dest = tmp_path / "installed"
    argv = [
        sys.executable,
        str(source_copy / "install_helpers.py"),
        str(source_copy),
        str(dest),
    ]
    subprocess.run(argv, check=True, cwd=source_copy)
    return dest


def component_namespaces(cli: str) -> dict[str, dict[str, str]]:
    metadata = json.loads(
        (DIST / cli / "component-namespaces.json").read_text(encoding="utf-8")
    )
    return {
        "skills": metadata["skills"],
        "agents": metadata["agents"],
        "commands": metadata["commands"],
    }


def load_helper(cli: str) -> ModuleType:
    helper_path = DIST / cli / "install_helpers.py"
    spec = importlib.util.spec_from_file_location(f"{cli}_install_helpers", helper_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_dist_namespaces_the_surviving_skill_set(tmp_path: Path) -> None:
    for cli in ("codex", "opencode"):
        dist_dir = namespace_dist(tmp_path / cli, cli)
        for skill, suffix in component_namespaces(cli)["skills"].items():
            skill_dir = dist_dir / "skills" / f"{skill}{suffix}"
            assert skill_dir.is_dir(), f"{cli}: {skill}-manifest-dev missing"
            assert (
                skill_dir / "SKILL.md"
            ).is_file(), f"{cli}: {skill}{suffix}/SKILL.md missing"


def test_every_dist_namespaces_every_distributed_component(tmp_path: Path) -> None:
    """Installer helpers must discover components from dist/, not static name lists."""
    for cli in ("codex", "opencode"):
        agent_ext = ".toml" if cli == "codex" else ".md"
        metadata = component_namespaces(cli)
        source_skills = sorted(
            path.name for path in (DIST / cli / "skills").iterdir() if path.is_dir()
        )
        source_agents = sorted(
            path.stem for path in (DIST / cli / "agents").glob(f"*{agent_ext}")
        )

        dist_dir = namespace_dist(tmp_path / f"{cli}-all-components", cli)

        assert sorted(
            path.name for path in (dist_dir / "skills").iterdir() if path.is_dir()
        ) == [
            f"{skill}{metadata['skills'][skill]}" for skill in source_skills
        ], f"{cli}: installed skill set diverged from dist/{cli}/skills"

        assert sorted(
            path.name for path in (dist_dir / "agents").glob(f"*{agent_ext}")
        ) == [
            f"{agent}{metadata['agents'][agent]}{agent_ext}" for agent in source_agents
        ], f"{cli}: installed agent set diverged from dist/{cli}/agents"

        if cli == "opencode":
            source_commands = sorted(
                path.stem for path in (DIST / cli / "commands").glob("*.md")
            )
            assert sorted(
                path.name for path in (dist_dir / "commands").glob("*.md")
            ) == [
                f"{command}{metadata['commands'][command]}.md"
                for command in source_commands
            ], "opencode: installed command set diverged from dist/opencode/commands"


def test_opencode_namespaced_commands_invoke_existing_namespaced_skills(
    tmp_path: Path,
) -> None:
    dist_dir = namespace_dist(tmp_path / "opencode-command-targets", "opencode")
    metadata = component_namespaces("opencode")

    for command, command_suffix in metadata["commands"].items():
        skill_suffix = metadata["skills"][command]
        command_file = dist_dir / "commands" / f"{command}{command_suffix}.md"
        content = command_file.read_text(encoding="utf-8")
        plugin_name = (
            "manifest-dev-tools"
            if command_suffix == "-manifest-dev-tools"
            else "manifest-dev"
        )

        assert (
            f"Invoke the {plugin_name}:{command}{skill_suffix} skill" in content
        ), f"opencode: {command_file.name} does not target its installed skill"

    figure_out_team = (
        dist_dir / "commands" / "figure-out-team-manifest-dev.md"
    ).read_text(encoding="utf-8")
    assert "figure-out-manifest-dev-team" not in figure_out_team


def test_namespacing_helpers_preserve_overlapping_skill_names() -> None:
    skills = {
        "figure-out": "-manifest-dev",
        "figure-out-team": "-manifest-dev",
        "adr": "-manifest-dev-tools",
    }
    agents: dict[str, str] = {}
    source = (
        "Invoke manifest-dev:figure-out-team, then manifest-dev:figure-out. "
        "Invoke manifest-dev-tools:adr."
    )

    opencode = load_helper("opencode")
    assert opencode._patch_cross_references(source, skills, agents) == (
        "Invoke manifest-dev:figure-out-team-manifest-dev, then "
        "manifest-dev:figure-out-manifest-dev. "
        "Invoke manifest-dev-tools:adr-manifest-dev-tools."
    )


def test_component_namespace_metadata_matches_dist() -> None:
    for cli in ("codex", "opencode"):
        metadata = component_namespaces(cli)
        agent_ext = ".toml" if cli == "codex" else ".md"

        assert set(metadata["skills"]) == {
            path.name for path in (DIST / cli / "skills").iterdir() if path.is_dir()
        }, f"{cli}: skills metadata drifted from dist"
        assert set(metadata["agents"]) == {
            path.stem for path in (DIST / cli / "agents").glob(f"*{agent_ext}")
        }, f"{cli}: agents metadata drifted from dist"

        if cli == "opencode":
            assert set(metadata["commands"]) == {
                path.stem for path in (DIST / cli / "commands").glob("*.md")
            }, "opencode: commands metadata drifted from dist"
        else:
            assert metadata["commands"] == {}

        for skill in CORE_SKILLS:
            assert metadata["skills"][skill] == "-manifest-dev"
        for skill in TOOLS_SKILLS:
            assert metadata["skills"][skill] == "-manifest-dev-tools"


def test_removed_components_are_not_distributed() -> None:
    for cli in ("codex", "opencode"):
        for skill in REMOVED_SKILLS:
            assert not (
                DIST / cli / "skills" / skill
            ).exists(), f"{cli}: removed skill {skill!r} still in dist"
        for agent in REMOVED_AGENTS:
            for ext in (".md", ".toml"):
                assert not (
                    DIST / cli / "agents" / f"{agent}{ext}"
                ).exists(), f"{cli}: removed agent {agent}{ext} still in dist"


def test_figure_out_team_command_exists_for_opencode() -> None:
    """OpenCode exposes user-invocable skills as slash commands; figure-out-team must be one."""
    command_file = DIST / "opencode" / "commands" / "figure-out-team.md"
    assert command_file.is_file(), "opencode/commands/figure-out-team.md missing"


def test_slack_poller_agent_exists_in_every_dist() -> None:
    """The slack-poller subagent is new in this release; every dist must carry it."""
    assert (DIST / "opencode" / "agents" / "slack-poller.md").is_file()
    assert (DIST / "codex" / "agents" / "slack-poller.toml").is_file()


def test_sync_tools_declares_pi_as_first_class_target() -> None:
    skill = (SYNC_TOOLS / "SKILL.md").read_text(encoding="utf-8")

    assert "`opencode`, `codex`, `pi`" in skill
    assert "dist/{opencode,codex,pi}/" in skill
    assert ".claude/skills/sync-tools/references/{cli}-cli.md" in skill
    assert (
        "| Pi | N compatible | N runtime prompt assets | source-owned runtime extension | extension commands | Complete |"
        in skill
    )
    assert (SYNC_TOOLS / "references" / "pi-cli.md").is_file()


def test_pi_sync_reference_keeps_harness_do_out_of_generated_skills() -> None:
    reference = (SYNC_TOOLS / "references" / "pi-cli.md").read_text(encoding="utf-8")

    assert "| Harness-level Do | Do not copy as a normal skill |" in reference
    assert "- `do`: exclude from `dist/pi/skills/`" in reference
    assert "- `done`: exclude from `dist/pi/skills/`" in reference
    assert "- `escalate`: exclude from `dist/pi/skills/`" in reference
    assert (
        "- `auto`: exclude from `dist/pi/skills/`; expose as `/manifest-auto`"
        in reference
    )
    assert (
        "- `babysit-pr`: exclude from `dist/pi/skills/`; expose as `/manifest-babysit-pr`"
        in reference
    )
    assert "/manifest-do <manifest-path>" in reference
    assert "/manifest-auto <task>" in reference
    assert "/manifest-babysit-pr <github-pr-url>" in reference
    assert "runtime-owned verification/outcome orchestration" in reference
    assert "Do not generate `install.sh` for Pi." in reference
    assert (
        "Do not silently generate or overwrite a repo-root package manifest"
        in reference
    )


def test_pi_sync_reference_models_pi_capabilities() -> None:
    reference = (SYNC_TOOLS / "references" / "pi-cli.md").read_text(encoding="utf-8")

    for required in (
        "## Capability Model",
        "## Claude Code Component Mapping",
        "repo-root package install",
        "registerCommand",
        "resources_discover",
        "sendUserMessage",
        "appendEntry",
        "@gotgenes/pi-subagents",
        "Session files and `--fork`",
        "SDK / JSON-mode subprocesses",
        "Prompt resources",
        "runtime-owned verification/outcome orchestration",
        "Executor Session prompt",
        "## Known Uncertainties",
    ):
        assert required in reference


def test_pi_package_metadata_points_to_generated_skills_and_extension() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    assert "pi-package" in package["keywords"]
    assert package["pi"] == {
        "extensions": ["./pi/extensions/manifest-dev.ts"],
        "skills": ["./dist/pi/skills"],
    }
    assert package["peerDependencies"] == {
        "@earendil-works/pi-coding-agent": "*",
        "@gotgenes/pi-subagents": "*",
    }
    assert PI_EXTENSION.is_file()
    assert PI_EXTENSION_RUNTIME.is_file()


def test_pi_dist_contains_only_compatible_skill_set() -> None:
    skill_dirs = {
        path.name for path in (DIST / "pi" / "skills").iterdir() if path.is_dir()
    }
    metadata = json.loads(
        (DIST / "pi" / "component-namespaces.json").read_text(encoding="utf-8")
    )

    assert skill_dirs == set(PI_SKILLS)
    assert set(metadata["skills"]) == set(PI_SKILLS)
    assert set(metadata["runtime_owned_skills"]) == set(PI_EXCLUDED_RUNTIME_SKILLS)
    assert set(metadata["extension_wrappers"]) == set(PI_EXTENSION_WRAPPER_SKILLS)
    assert set(metadata["commands"]) == set(PI_EXTENSION_COMMANDS)
    assert metadata["tools"] == {}
    assert metadata["runtime_internal"] == {
        "verification": (
            "Runtime-owned verifier fanout over manifest Acceptance Criteria and "
            "Global Invariants; not exposed as an executor-callable tool."
        ),
        "outcome": (
            "Runtime-owned done and blocker outcomes after verifier fanout; not "
            "exposed as an executor-callable tool."
        ),
    }
    assert metadata["runtime_dependencies"] == {
        "@gotgenes/pi-subagents": "Required for clean verifier subagent sessions."
    }
    assert metadata["agents"] == {}


def test_pi_extension_registers_harness_commands_and_runtime_internals() -> None:
    content = PI_EXTENSION.read_text(encoding="utf-8")
    runtime = PI_EXTENSION_RUNTIME.read_text(encoding="utf-8")

    for command in PI_EXTENSION_COMMANDS:
        assert f'pi.registerCommand("{command}"' in content

    for tool in ("manifest_dev_request_verification", "manifest_dev_report_outcome"):
        assert f'name: "{tool}"' not in content

    assert "runHarnessVerification" in content
    assert "maybeRunHarnessVerification" in content
    assert "shouldTriggerHarnessVerification" in content
    assert "formatRepairFollowUpMessage" in content
    assert "createVerificationOrchestratorSession" in content
    assert "verificationSessionDir" in content
    assert "resolveManifestPath" in content
    assert "@gotgenes/pi-subagents" in content
    assert "subagents.spawn" in content
    assert "inheritContext: false" in content
    assert "VERDICT: PASS|FAIL|BLOCKED" in runtime
    assert "extractManifestGates" in runtime
    assert "aggregateVerificationStatus" in runtime
    assert "pi.appendEntry(RUN_ENTRY" in content
    assert "pi.appendEntry(VERIFICATION_ENTRY" in content
    assert "pi.appendEntry(OUTCOME_ENTRY" in content
    assert "pi.sendUserMessage(formatRepairFollowUpMessage" in content
    assert "runtime owns authoritative verification" in content
    assert "Do not use /done or /escalate" in content
    # Durable + freshness-bound done gate, phase-aware fanout, session inheritance, resumable blocker.
    assert "evaluateDoneReadiness(" in content
    assert "writeRunStateFile(" in content
    assert "rehydrateRuntimeState" in content
    assert "planVerifierBatches(" in content
    assert "chunkManifestGates(" in content
    assert "bypassQueue: true" in content
    assert "resolveVerifierModel(gate.model, ctx.model)" in content
    assert "pi.registerFlag(FLAG_MAX_TURNS" in content
    assert "pi.registerFlag(FLAG_MAX_CONCURRENT" in content
    assert "shouldTerminateOutcome(outcome)" in content


def test_pi_readmes_document_install_update_and_runtime_boundary() -> None:
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pi_readme = (DIST / "pi" / "README.md").read_text(encoding="utf-8")

    for content in (root_readme, pi_readme):
        assert "pi install git:github.com/doodledood/manifest-dev@main" in content
        assert "pi update" in content
        assert "pi remove git:github.com/doodledood/manifest-dev" in content
        assert "Harness-level Do" in content

    assert "/manifest-do <manifest-path>" in pi_readme
    assert "/manifest-auto <task>" in pi_readme
    assert "/manifest-babysit-pr <github-pr-url>" in pi_readme
    assert "not exposed as normal skills or executor-callable tools" in pi_readme
    assert "The executor is not asked to call verification or outcome tools" in pi_readme
    pi_markdown = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (DIST / "pi").rglob("*.md")
    )
    assert "manifest_dev_request_verification" not in pi_markdown
    assert "manifest_dev_report_outcome" not in pi_markdown
    assert "`/do`, `/done`, and `/escalate` remain intentionally absent" in pi_readme
    assert "pi install npm:@gotgenes/pi-subagents" in root_readme
    assert "pi install npm:@gotgenes/pi-subagents" in pi_readme
    assert "clean verifier subagent sessions" in root_readme
    assert "--manifest-verifier-max-concurrent" in root_readme
    assert "--manifest-verifier-max-concurrent" in pi_readme
    assert "bypassQueue: true" in pi_readme
    assert "inheritContext: false" in pi_readme
    assert (
        "Full independent verifier-session fanout remains future Pi runtime work"
        not in root_readme
    )
