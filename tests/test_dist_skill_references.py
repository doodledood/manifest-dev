"""
Verify each CLI distribution carries the full skill set with correct namespacing.

The dist payload ships core manifest-dev skills with the `-manifest-dev` suffix
and manifest-dev-tools skills with the `-manifest-dev-tools` suffix.

Also confirms the removed plugin components stay removed:
  - no `verify` skill in any dist
  - no `manifest-verifier` agent in any dist
  - no `pretool_verify_hook.py` or `prompt_submit_hook.py` in the gemini hooks dir
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"

CORE_SKILLS = (
    "auto",
    "define",
    "do",
    "done",
    "escalate",
    "figure-out",
    "figure-out-team",
)
TOOLS_SKILLS = ("adr", "handoff", "prompt-engineering", "walk-pr")

REMOVED_SKILLS = ("verify",)
REMOVED_AGENTS = ("manifest-verifier",)
REMOVED_GEMINI_HOOKS = ("pretool_verify_hook.py", "prompt_submit_hook.py")


def namespace_dist(tmp_path: Path, cli: str) -> Path:
    """Mirror dist/{cli} into tmp_path and run that CLI's install_helpers.

    Per-CLI argv conventions differ — codex uses ``namespace <dir> <cli>``
    in place while gemini and opencode copy from ``<src>`` into ``<dst>``.
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


def load_helper(cli: str):
    helper_path = DIST / cli / "install_helpers.py"
    spec = importlib.util.spec_from_file_location(f"{cli}_install_helpers", helper_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_dist_namespaces_the_surviving_skill_set(tmp_path: Path) -> None:
    for cli in ("codex", "opencode", "gemini"):
        dist_dir = namespace_dist(tmp_path / cli, cli)
        for skill, suffix in component_namespaces(cli)["skills"].items():
            skill_dir = dist_dir / "skills" / f"{skill}{suffix}"
            assert skill_dir.is_dir(), f"{cli}: {skill}-manifest-dev missing"
            assert (
                skill_dir / "SKILL.md"
            ).is_file(), f"{cli}: {skill}{suffix}/SKILL.md missing"


def test_every_dist_namespaces_every_distributed_component(tmp_path: Path) -> None:
    """Installer helpers must discover components from dist/, not static name lists."""
    for cli in ("codex", "opencode", "gemini"):
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

    gemini = load_helper("gemini")
    assert gemini.patch_cross_references(source, skills, agents) == (
        "Invoke manifest-dev:figure-out-team-manifest-dev, then "
        "manifest-dev:figure-out-manifest-dev. "
        "Invoke manifest-dev-tools:adr-manifest-dev-tools."
    )

    opencode = load_helper("opencode")
    assert opencode._patch_cross_references(source, skills, agents) == (
        "Invoke manifest-dev:figure-out-team-manifest-dev, then "
        "manifest-dev:figure-out-manifest-dev. "
        "Invoke manifest-dev-tools:adr-manifest-dev-tools."
    )


def test_component_namespace_metadata_matches_dist() -> None:
    for cli in ("codex", "opencode", "gemini"):
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
    for cli in ("codex", "opencode", "gemini"):
        for skill in REMOVED_SKILLS:
            assert not (
                DIST / cli / "skills" / skill
            ).exists(), f"{cli}: removed skill {skill!r} still in dist"
        for agent in REMOVED_AGENTS:
            for ext in (".md", ".toml"):
                assert not (
                    DIST / cli / "agents" / f"{agent}{ext}"
                ).exists(), f"{cli}: removed agent {agent}{ext} still in dist"

    for hook in REMOVED_GEMINI_HOOKS:
        assert not (
            DIST / "gemini" / "hooks" / hook
        ).exists(), f"removed gemini hook {hook} still in dist"


def test_figure_out_team_command_exists_for_opencode() -> None:
    """OpenCode exposes user-invocable skills as slash commands; figure-out-team must be one."""
    command_file = DIST / "opencode" / "commands" / "figure-out-team.md"
    assert command_file.is_file(), "opencode/commands/figure-out-team.md missing"


def test_slack_poller_agent_exists_in_every_dist() -> None:
    """The slack-poller subagent is new in this release; every dist must carry it."""
    assert (DIST / "gemini" / "agents" / "slack-poller.md").is_file()
    assert (DIST / "opencode" / "agents" / "slack-poller.md").is_file()
    assert (DIST / "codex" / "agents" / "slack-poller.toml").is_file()
