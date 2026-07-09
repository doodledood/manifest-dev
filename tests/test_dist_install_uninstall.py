from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"
TOOLS_SKILLS = (
    "babysit-pr",
    "handoff",
    "prompt-engineering",
    "review-prompt",
    "review-pr",
    "teach-me",
    "walk-pr",
)

# Codex and OpenCode are distributed as native plugins (no installer anywhere).
# OpenCode's plugin entry is exercised below by invoking its config hook in node.


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
        / "review-code"
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
# OpenCode: plugin-native distribution (no installer)
# --------------------------------------------------------------------------

OPENCODE = DIST / "opencode"


def test_opencode_ships_no_installer_artifacts() -> None:
    """The OpenCode installer is retired; none of its files may remain."""
    for retired in (
        "install.sh",
        "install_helpers.py",
        "component-namespaces.json",
        "commands",
    ):
        assert not (
            OPENCODE / retired
        ).exists(), f"retired OpenCode artifact present: {retired}"


def test_opencode_plugin_entry_shape() -> None:
    """Dependency-free ESM plugin whose version mirrors the core plugin."""
    manifest = json.loads(
        (OPENCODE / "plugin" / "package.json").read_text(encoding="utf-8")
    )
    assert manifest["name"] == "@doodledood/manifest-dev-opencode"
    assert manifest["type"] == "module"
    assert manifest["main"] == "index.js"
    assert not manifest.get("dependencies")
    assert not manifest.get("devDependencies")

    core = json.loads(
        (
            ROOT / "claude-plugins" / "manifest-dev" / ".claude-plugin" / "plugin.json"
        ).read_text(encoding="utf-8")
    )
    assert manifest["version"] == core["version"]

    assert (OPENCODE / "plugin" / "index.js").is_file()


def test_opencode_plugin_config_hook_registers_payload(tmp_path: Path) -> None:
    """The config hook appends package-local skills.paths, command wrappers, and instructions."""
    script = tmp_path / "smoke.mjs"
    script.write_text(
        f"""
import {{ ManifestDevPlugin }} from {json.dumps((OPENCODE / "plugin" / "index.js").as_posix())}
const hooks = await ManifestDevPlugin({{}})
const cfg = {{
  skills: {{ paths: ["/user/existing"] }},
  instructions: ["USER.md"],
  command: {{ define: {{ description: "User override", template: "Keep me" }} }},
}}
await hooks.config(cfg)
console.log(JSON.stringify(cfg))
""",
        encoding="utf-8",
    )
    result = subprocess.run(
        ["node", str(script)], capture_output=True, text=True, check=True
    )
    cfg = json.loads(result.stdout)
    assert cfg["skills"]["paths"] == [
        "/user/existing",
        (OPENCODE / "skills").as_posix(),
    ]
    assert cfg["instructions"] == ["USER.md", (OPENCODE / "AGENTS.md").as_posix()]

    commands = cfg["command"]
    assert commands["define"] == {"description": "User override", "template": "Keep me"}
    assert (
        commands["figure-out"]["template"]
        == "Use the figure-out skill with: $ARGUMENTS"
    )
    assert commands["prompt-engineering"]["template"] == (
        "Use the prompt-engineering skill with: $ARGUMENTS"
    )
    assert (
        commands["babysit-pr"]["template"]
        == "Use the babysit-pr skill with: $ARGUMENTS"
    )
    assert "done" not in commands
    assert "escalate" not in commands
    # 17 OpenCode skills minus the two internal user-invocable:false helpers;
    # the user-provided define override replaces, rather than adds to, that set.
    assert len(commands) == 15


def test_opencode_plugin_config_hook_never_throws_without_assets(
    tmp_path: Path,
) -> None:
    """Missing sibling assets degrade to warnings — startup must survive."""
    bare = tmp_path / "bare" / "plugin"
    bare.mkdir(parents=True)
    for name in ("package.json", "index.js"):
        (bare / name).write_bytes((OPENCODE / "plugin" / name).read_bytes())
    script = tmp_path / "smoke.mjs"
    script.write_text(
        f"""
import {{ ManifestDevPlugin }} from {json.dumps((bare / "index.js").as_posix())}
const hooks = await ManifestDevPlugin({{}})
const cfg = {{}}
await hooks.config(cfg)
console.log(JSON.stringify(cfg))
""",
        encoding="utf-8",
    )
    result = subprocess.run(
        ["node", str(script)], capture_output=True, text=True, check=True
    )
    assert json.loads(result.stdout) == {}


def test_opencode_bundles_all_skills_under_original_names() -> None:
    skills_dir = OPENCODE / "skills"
    skills = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    assert {"define", "do", "auto", "review-code", "check-pr"} <= skills
    assert set(TOOLS_SKILLS) <= skills
    for skill in skills:
        skill_md = skills_dir / skill / "SKILL.md"
        assert skill_md.is_file()
        # Native discovery requires frontmatter name == directory name.
        frontmatter = skill_md.read_text(encoding="utf-8").split("---", 2)[1]
        assert f"name: {skill}" in frontmatter, f"{skill}: frontmatter name mismatch"
