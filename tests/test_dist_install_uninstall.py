from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
TOOLS_SKILLS = (
    "adr",
    "babysit-pr",
    "handoff",
    "prompt-engineering",
    "review-pr",
    "teach-me",
    "walk-pr",
)

# Codex is distributed as native plugins (no installer). Only OpenCode still
# ships an install.sh; its install/uninstall behavior is exercised below.


def run_opencode_installer(
    env: dict[str, str], *args: str
) -> subprocess.CompletedProcess[str]:
    cmd = ["bash", str(DIST / "opencode" / "install.sh"), *args]
    return subprocess.run(
        cmd, cwd=ROOT, env=env, capture_output=True, text=True, check=True
    )


def _opencode_env(tmp_path: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env["OPENCODE_TARGET"] = str(Path(env["HOME"]) / ".config" / "opencode")
    return env


# --------------------------------------------------------------------------
# Codex: plugin-native distribution (no installer)
# --------------------------------------------------------------------------

CODEX_PLUGINS = ("manifest-dev", "manifest-dev-tools")


def test_codex_ships_no_installer_artifacts() -> None:
    """The legacy Codex installer is retired; none of its files may remain."""
    codex = DIST / "codex"
    for retired in (
        "install.sh",
        "install_helpers.py",
        "config.toml",
        "rules",
        "agents",
        "AGENTS.md",
        "component-namespaces.json",
        "skills",
    ):
        assert not (
            codex / retired
        ).exists(), f"retired Codex artifact present: {retired}"


def test_codex_marketplace_registers_both_plugins() -> None:
    marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )
    names = {entry["name"] for entry in marketplace["plugins"]}
    assert names == set(CODEX_PLUGINS)
    for entry in marketplace["plugins"]:
        # Required marketplace fields.
        assert entry["policy"]["installation"]
        assert entry["policy"]["authentication"]
        assert entry["category"]
        # source.path points at a real plugin directory, relative to repo root.
        rel = entry["source"]["path"]
        assert rel.startswith("./")
        plugin_dir = ROOT / rel
        assert (plugin_dir / ".codex-plugin" / "plugin.json").is_file(), rel


def test_codex_marketplace_only_file_under_agents_plugins() -> None:
    """`.agents/plugins/` holds only the registry — no SKILL.md may leak there."""
    agents_plugins = ROOT / ".agents" / "plugins"
    files = {p.name for p in agents_plugins.iterdir()}
    assert files == {"marketplace.json"}
    assert list(agents_plugins.rglob("SKILL.md")) == []


def test_codex_plugins_bundle_skills() -> None:
    for plugin in CODEX_PLUGINS:
        plugin_dir = DIST / "codex" / "plugins" / plugin
        manifest = json.loads(
            (plugin_dir / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        assert manifest["name"] == plugin
        assert manifest["version"]
        assert manifest["skills"] == "./skills/"
        skills_dir = plugin_dir / "skills"
        assert skills_dir.is_dir()
        skills = [p.name for p in skills_dir.iterdir() if p.is_dir()]
        assert skills, f"{plugin}: no bundled skills"
        for skill in skills:
            assert (skills_dir / skill / "SKILL.md").is_file()


def test_codex_core_plugin_bundles_code_review_with_all_dimensions() -> None:
    refs = (
        DIST
        / "codex"
        / "plugins"
        / "manifest-dev"
        / "skills"
        / "code-review"
        / "references"
    )
    dimensions = {p.stem for p in refs.glob("*.md")}
    assert dimensions == {
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


# --------------------------------------------------------------------------
# OpenCode: installer-based distribution (retained)
# --------------------------------------------------------------------------


def test_opencode_installer_installs_tools_skills(tmp_path: Path) -> None:
    env = _opencode_env(tmp_path)
    run_opencode_installer(env)

    target = Path(env["OPENCODE_TARGET"])
    for skill in TOOLS_SKILLS:
        skill_dir = target / "skills" / f"{skill}-manifest-dev-tools"
        assert skill_dir.is_dir(), f"missing {skill_dir}"
        assert (skill_dir / "SKILL.md").is_file()
        command = target / "commands" / f"{skill}-manifest-dev-tools.md"
        assert command.is_file(), f"missing {command}"

    assert (target / "skills" / "define-manifest-dev").is_dir()
    assert (target / "skills" / "code-review-manifest-dev").is_dir()


def test_opencode_installer_defaults_to_global_config_dir(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env.pop("OPENCODE_TARGET", None)

    result = run_opencode_installer(env)

    target = Path(env["HOME"]) / ".config" / "opencode"
    assert f"Target:  {target}" in result.stdout
    assert (target / "skills" / "define-manifest-dev").is_dir()
    # criteria-checker is a skill now, not an agent.
    assert (target / "skills" / "criteria-checker-manifest-dev").is_dir()
    assert not (target / "agents").exists()
    assert (target / "commands" / "define-manifest-dev.md").is_file()


def test_opencode_installer_local_scope_is_explicit(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env.pop("OPENCODE_TARGET", None)
    project = tmp_path / "project"
    project.mkdir()

    subprocess.run(
        ["bash", str(DIST / "opencode" / "install.sh"), "--local"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    target = project / ".opencode"
    assert (target / "skills" / "define-manifest-dev").is_dir()
    assert not (Path(env["HOME"]) / ".config" / "opencode").exists()


def test_opencode_reinstall_syncs_state_without_touching_user_files(
    tmp_path: Path,
) -> None:
    env = _opencode_env(tmp_path)
    run_opencode_installer(env)

    target = Path(env["OPENCODE_TARGET"])
    managed_skill = target / "skills" / "adr-manifest-dev-tools" / "SKILL.md"
    managed_skill.write_text("stale managed content\n", encoding="utf-8")

    stale_skill = target / "skills" / "retired-manifest-dev-tools"
    stale_skill.mkdir(parents=True)
    (stale_skill / "SKILL.md").write_text("retired\n", encoding="utf-8")

    custom_skill = target / "skills" / "custom-skill"
    custom_skill.mkdir(parents=True)
    (custom_skill / "SKILL.md").write_text("custom\n", encoding="utf-8")

    managed_command = target / "commands" / "adr-manifest-dev-tools.md"
    managed_command.write_text("stale command\n", encoding="utf-8")
    stale_command = target / "commands" / "retired-manifest-dev-tools.md"
    stale_command.write_text("retired command\n", encoding="utf-8")
    custom_command = target / "commands" / "custom-command.md"
    custom_command.write_text("custom command\n", encoding="utf-8")

    run_opencode_installer(env)

    refreshed_skill = managed_skill.read_text(encoding="utf-8")
    assert "name: adr-manifest-dev-tools" in refreshed_skill
    assert "stale managed content" not in refreshed_skill
    assert not stale_skill.exists()
    assert (custom_skill / "SKILL.md").read_text(encoding="utf-8") == "custom\n"

    refreshed_command = managed_command.read_text(encoding="utf-8")
    assert "manifest-dev-tools:adr-manifest-dev-tools" in refreshed_command
    assert "stale command" not in refreshed_command
    assert not stale_command.exists()
    assert custom_command.read_text(encoding="utf-8") == "custom command\n"


def test_opencode_uninstall_removes_only_manifest_dev_files(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    opencode_dir = Path(env["HOME"]) / ".config" / "opencode"
    env["OPENCODE_TARGET"] = str(opencode_dir)
    custom_skill = opencode_dir / "skills" / "custom-skill"
    custom_skill.mkdir(parents=True, exist_ok=True)
    (custom_skill / "SKILL.md").write_text("custom\n", encoding="utf-8")

    plugins_dir = opencode_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    root_plugin = plugins_dir / "index.ts"
    root_plugin.write_text("// user-managed root plugin\n", encoding="utf-8")

    opencode_config = opencode_dir / "opencode.json"
    opencode_config.write_text(
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "plugin": ["./plugins/index.ts"],
                "mcp": {"custom": {"type": "local", "command": ["echo", "hi"]}},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    run_opencode_installer(env)
    assert (opencode_dir / "skills" / "define-manifest-dev").is_dir()

    run_opencode_installer(env, "uninstall")

    assert custom_skill.is_dir()
    assert root_plugin.read_text(encoding="utf-8") == "// user-managed root plugin\n"
    assert json.loads(opencode_config.read_text(encoding="utf-8")) == {
        "$schema": "https://opencode.ai/config.json",
        "plugin": ["./plugins/index.ts"],
        "mcp": {"custom": {"type": "local", "command": ["echo", "hi"]}},
    }
    assert not (opencode_dir / "skills" / "define-manifest-dev").exists()
    assert not (opencode_dir / "skills" / "adr-manifest-dev-tools").exists()
    assert not (opencode_dir / "agents" / "criteria-checker-manifest-dev.md").exists()
    assert not (opencode_dir / "commands" / "define-manifest-dev.md").exists()


def test_opencode_install_leaves_user_root_plugin_and_config_untouched(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    opencode_dir = Path(env["HOME"]) / ".config" / "opencode"
    env["OPENCODE_TARGET"] = str(opencode_dir)
    plugins_dir = opencode_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    root_plugin = plugins_dir / "index.ts"
    root_plugin.write_text("// user-managed root plugin\n", encoding="utf-8")
    opencode_config = opencode_dir / "opencode.json"
    opencode_config.write_text(
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "plugin": ["./plugins/index.ts"],
                "default_agent": "build",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    run_opencode_installer(env)

    assert root_plugin.read_text(encoding="utf-8") == "// user-managed root plugin\n"
    assert json.loads(opencode_config.read_text(encoding="utf-8")) == {
        "$schema": "https://opencode.ai/config.json",
        "plugin": ["./plugins/index.ts"],
        "default_agent": "build",
    }
