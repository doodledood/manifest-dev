from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"


def namespace_dist(tmp_path: Path, cli: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    src = DIST / cli
    dest = tmp_path / cli
    shutil.copytree(src, dest)

    subprocess.run(
        [sys.executable, str(dest / "install_helpers.py"), "namespace", str(dest), cli],
        check=True,
        cwd=dest,
    )

    return dest


def test_namespaced_skill_handoffs_are_installed_safely(tmp_path: Path) -> None:
    for cli in ("codex", "opencode", "gemini"):
        dist_dir = namespace_dist(tmp_path / cli, cli)

        define_text = (
            dist_dir / "skills" / "define-manifest-dev" / "SKILL.md"
        ).read_text()
        do_text = (dist_dir / "skills" / "do-manifest-dev" / "SKILL.md").read_text()
        verify_text = (
            dist_dir / "skills" / "verify-manifest-dev" / "SKILL.md"
        ).read_text()
        escalate_text = (
            dist_dir / "skills" / "escalate-manifest-dev" / "SKILL.md"
        ).read_text()

        assert "`do-manifest-dev` skill" in define_text
        assert "verify-manifest-dev" in do_text
        assert "done-manifest-dev" in do_text
        assert "escalate-manifest-dev" in do_text
        assert "done-manifest-dev" in verify_text
        assert "escalate-manifest-dev" in verify_text
        assert "`do-manifest-dev` skill" in escalate_text

        assert "Explicit /do invocation" not in define_text
        assert "To execute: /do " not in define_text
        assert "/define ends here." not in define_text

        assert "Usage: /do <manifest-file-path> [log-file-path]" not in do_text
        assert "**Must call /verify**" not in do_text
        assert "**Stop requires /escalate**" not in do_text
        assert "calling /verify" not in do_text

        assert (
            'Return error "Usage: /verify <manifest-path> <log-path>"'
            not in verify_text
        )
        assert (
            "| `manual` | Set aside for human verification | /escalate |"
            not in verify_text
        )
        assert "| All pass | Call /done |" not in verify_text
        assert "suggest /escalate." not in verify_text
        assert "**On full success** - Call /done." not in verify_text

        assert 'e.g., "/do <manifest> <log>"' not in escalate_text

        if cli == "opencode":
            plugin_text = (dist_dir / "plugins" / "index.ts").read_text()
            assert 'isSkillCall(tool, args, "do-manifest-dev")' in plugin_text
            assert 'isSkillCall(tool, args, "done-manifest-dev")' in plugin_text
            assert 'isSkillCall(tool, args, "escalate-manifest-dev")' in plugin_text
            assert 'isSkillCall(tool, args, "verify-manifest-dev")' in plugin_text
            assert 'isSkillCall(tool, args, "do")' not in plugin_text

        if cli == "gemini":
            pretool_text = (dist_dir / "hooks" / "pretool_verify_hook.py").read_text()
            hook_utils_text = (dist_dir / "hooks" / "hook_utils.py").read_text()
            hooks_json = (dist_dir / "hooks" / "hooks.json").read_text()

            assert 'skill != "verify-manifest-dev"' in pretool_text
            assert 'skill.endswith(":verify-manifest-dev")' in pretool_text
            assert 'was_skill_invoked(data, "do-manifest-dev")' in hook_utils_text
            assert 'was_skill_invoked(data, "verify-manifest-dev")' in hook_utils_text
            assert "/verify-manifest-dev" in hooks_json
            assert "/do-manifest-dev" in hooks_json


def test_codex_reference_guide_uses_namespaced_dollar_invocations(
    tmp_path: Path,
) -> None:
    codex_dir = namespace_dist(tmp_path, "codex")
    agents_text = (codex_dir / "AGENTS.md").read_text()

    assert "$define-manifest-dev" in agents_text
    assert "$do-manifest-dev" in agents_text
    assert "$verify-manifest-dev" in agents_text
    assert "$done-manifest-dev" in agents_text
    assert "$escalate-manifest-dev" in agents_text
    assert "$learn-define-patterns-manifest-dev" in agents_text
    assert "code-bugs-reviewer-manifest-dev" in agents_text


def test_opencode_readme_distinguishes_commands_from_internal_skills(
    tmp_path: Path,
) -> None:
    opencode_dir = namespace_dist(tmp_path, "opencode")
    readme_text = (opencode_dir / "README.md").read_text()

    assert "/define-manifest-dev" in readme_text
    assert "/do-manifest-dev" in readme_text
    assert "/learn-define-patterns-manifest-dev" in readme_text
    assert (
        "The `verify-manifest-dev`, `done-manifest-dev`, and "
        "`escalate-manifest-dev` skills remain internal workflow steps."
    ) in readme_text


def test_gemini_docs_describe_extension_skills_not_slash_commands(
    tmp_path: Path,
) -> None:
    gemini_dir = namespace_dist(tmp_path, "gemini")
    gemini_md = (gemini_dir / "GEMINI.md").read_text()
    readme_text = (gemini_dir / "README.md").read_text()

    assert "Gemini activates them via `activate_skill`" in gemini_md
    assert "`define-manifest-dev` -- Interview-driven task specification" in gemini_md
    assert "/define-manifest-dev" not in gemini_md
    assert "/do-manifest-dev" not in gemini_md
    assert "/verify-manifest-dev" not in gemini_md

    assert "extension-managed skills via `activate_skill`" in readme_text
    assert "`verify-manifest-dev` -> parallel verification" in readme_text
    assert "/verify-manifest-dev ->" not in readme_text


def test_gemini_installer_outputs_skill_usage_guidance(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    result = subprocess.run(
        ["bash", str(DIST / "gemini" / "install.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "gemini> /define-manifest-dev my task" not in result.stdout
    assert "ask it to use the define-manifest-dev skill" in result.stdout
    assert "Enable agents in settings.json" not in result.stdout
    assert "Merge hooks into your settings.json" not in result.stdout
    assert "No manual settings changes are required." in result.stdout


def test_sync_tools_docs_require_complete_additive_installs() -> None:
    sync_text = (ROOT / ".claude" / "skills" / "sync-tools" / "SKILL.md").read_text()
    opencode_ref = (
        ROOT / ".claude" / "skills" / "sync-tools" / "references" / "opencode-cli.md"
    ).read_text()
    gemini_ref = (
        ROOT / ".claude" / "skills" / "sync-tools" / "references" / "gemini-cli.md"
    ).read_text()

    assert "do not ship stubs or require manual post-install wiring" in sync_text
    assert (
        "Generate complete plugin module placed in the local plugin directory"
        in opencode_ref
    )
    assert "install.sh` must merge" in gemini_ref


def test_verification_model_defaults_to_inherit_across_source_and_dist() -> None:
    define_paths = [
        ROOT / "claude-plugins" / "manifest-dev" / "skills" / "define" / "SKILL.md",
        ROOT / "dist" / "codex" / "skills" / "define" / "SKILL.md",
        ROOT / "dist" / "gemini" / "skills" / "define" / "SKILL.md",
        ROOT / "dist" / "opencode" / "skills" / "define" / "SKILL.md",
    ]
    verifier_paths = [
        ROOT / "claude-plugins" / "manifest-dev" / "agents" / "manifest-verifier.md",
        ROOT / "dist" / "codex" / "agents" / "manifest-verifier.toml",
        ROOT / "dist" / "gemini" / "agents" / "manifest-verifier.md",
        ROOT / "dist" / "opencode" / "agents" / "manifest-verifier.md",
    ]

    for path in define_paths:
        text = path.read_text()
        assert "default to `inherit`." in text
        assert 'model: "[if subagent, default inherit]"' in text
        assert "default opus for general-purpose" not in text

    for path in verifier_paths:
        text = path.read_text()
        assert (
            "doesn't specify `model: inherit` for general-purpose judgment tasks"
            in text
        )
        assert "opus model for general-purpose judgment tasks" not in text


def test_opencode_installer_preserves_root_plugin_and_config(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    opencode_dir = Path(env["HOME"]) / ".config" / "opencode"
    plugins_dir = opencode_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    root_plugin = plugins_dir / "index.ts"
    root_plugin.write_text("// user-managed root plugin\n", encoding="utf-8")
    opencode_config = opencode_dir / "opencode.json"
    opencode_config.write_text(
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "default_agent": "build",
                "plugin": ["./plugins/index.ts"],
                "mcp": {"custom": {"type": "local", "command": ["echo", "hi"]}},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(DIST / "opencode" / "install.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    merged = json.loads(opencode_config.read_text(encoding="utf-8"))
    assert merged["default_agent"] == "build"
    assert merged["mcp"]["custom"]["command"] == ["echo", "hi"]
    assert merged["plugin"].count("./plugins/index.ts") == 1
    assert root_plugin.read_text(encoding="utf-8") == "// user-managed root plugin\n"
    assert (plugins_dir / "manifest-dev.ts").is_file()
    assert (plugins_dir / "manifest-dev.HOOK_SPEC.md").is_file()
    assert not (plugins_dir / "index.ts.manifest-dev-legacy.bak").exists()
    assert not (opencode_dir / "opencode.json.bak").exists()
    assert "No manual plugin wiring is required." in result.stdout

    subprocess.run(
        ["bash", str(DIST / "opencode" / "install.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    merged_again = json.loads(opencode_config.read_text(encoding="utf-8"))
    assert merged_again == merged


def test_gemini_installer_merges_settings_additively(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    settings_path = gemini_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "selectedAuthType": "gemini-api-key",
                "experimental": {"otherFlag": True},
                "hooks": {
                    "BeforeTool": [
                        {
                            "matcher": "write_file",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "python3 /custom/hook.py",
                                    "name": "custom-before-tool",
                                }
                            ],
                        }
                    ]
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(DIST / "gemini" / "install.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged["selectedAuthType"] == "gemini-api-key"
    assert merged["experimental"]["otherFlag"] is True
    assert merged["experimental"]["enableAgents"] is True
    before_tool = merged["hooks"]["BeforeTool"]
    assert any(hook["hooks"][0]["name"] == "custom-before-tool" for hook in before_tool)
    assert any(
        hook["hooks"][0]["name"] == "pretool-verify"
        and hook["hooks"][0]["command"].endswith("gemini_adapter.py BeforeTool")
        for hook in before_tool
    )
    assert (gemini_dir / "settings.json.bak").is_file()
    assert "No manual settings changes are required." in result.stdout

    subprocess.run(
        ["bash", str(DIST / "gemini" / "install.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    merged_again = json.loads(settings_path.read_text(encoding="utf-8"))
    before_tool_again = merged_again["hooks"]["BeforeTool"]
    assert (
        sum(
            1
            for hook in before_tool_again
            if hook["hooks"][0]["name"] == "pretool-verify"
        )
        == 1
    )
