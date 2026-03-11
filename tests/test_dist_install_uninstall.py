from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"


def run_installer(cli: str, env: dict[str, str], action: str = "install") -> subprocess.CompletedProcess[str]:
    cmd = ["bash", str(DIST / cli / "install.sh")]
    if action != "install":
        cmd.append(action)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )


def test_codex_uninstall_removes_only_manifest_dev_and_reverts_added_config(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    config_path = codex_dir / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        (
            'preferred_auth_method = "chatgpt"\n\n'
            "[features]\n"
            "preview_feature = true\n\n"
            "[agents]\n"
            'project_doc_fallback_filenames = ["AGENTS.md"]\n\n'
            "[mcp_servers.custom]\n"
            'command = ["echo", "hi"]\n'
        ),
        encoding="utf-8",
    )

    custom_skill = codex_dir / "skills" / "custom-skill"
    custom_skill.mkdir(parents=True, exist_ok=True)
    (custom_skill / "SKILL.md").write_text("custom\n", encoding="utf-8")
    custom_agent = codex_dir / "agents" / "custom-agent.toml"
    custom_agent.parent.mkdir(parents=True, exist_ok=True)
    custom_agent.write_text("model = 'inherit'\n", encoding="utf-8")
    custom_rule = codex_dir / "rules" / "custom.rules"
    custom_rule.parent.mkdir(parents=True, exist_ok=True)
    custom_rule.write_text("# custom\n", encoding="utf-8")

    install_result = run_installer("codex", env)

    installed_config = config_path.read_text(encoding="utf-8")
    assert "preview_feature = true" in installed_config
    assert 'project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]' in installed_config
    assert "multi_agent = true" in installed_config
    assert "max_threads = 6" in installed_config
    assert "max_depth = 1" in installed_config
    assert "# >>> manifest-dev managed config >>>" in installed_config
    assert (codex_dir / "manifest-dev-install-state.json").is_file()
    assert (codex_dir / "rules" / "manifest-dev.rules").is_file()
    assert "config.toml merged" in install_result.stdout

    uninstall_result = run_installer("codex", env, "uninstall")

    final_config = config_path.read_text(encoding="utf-8")
    assert 'preferred_auth_method = "chatgpt"' in final_config
    assert "preview_feature = true" in final_config
    assert 'project_doc_fallback_filenames = ["AGENTS.md"]' in final_config
    assert "multi_agent = true" not in final_config
    assert "max_threads = 6" not in final_config
    assert "max_depth = 1" not in final_config
    assert "# >>> manifest-dev managed config >>>" not in final_config
    assert "[agents.criteria-checker-manifest-dev]" not in final_config
    assert "[mcp_servers.custom]" in final_config

    assert custom_skill.is_dir()
    assert custom_agent.is_file()
    assert custom_rule.is_file()
    assert not (codex_dir / "skills" / "define-manifest-dev").exists()
    assert not (codex_dir / "agents" / "criteria-checker-manifest-dev.toml").exists()
    assert not (codex_dir / "rules" / "manifest-dev.rules").exists()
    assert not (codex_dir / "manifest-dev-install-state.json").exists()
    assert (codex_dir / "config.toml.pre-manifest-dev-uninstall.bak").is_file()
    assert "Removed manifest-dev-managed Codex files only." in uninstall_result.stdout


def test_codex_uninstall_keeps_user_modified_shared_settings(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    run_installer("codex", env)

    config_path = codex_dir / "config.toml"
    installed_config = config_path.read_text(encoding="utf-8")
    installed_config = installed_config.replace("max_threads = 6", "max_threads = 8")
    config_path.write_text(installed_config, encoding="utf-8")

    run_installer("codex", env, "uninstall")

    final_config = config_path.read_text(encoding="utf-8")
    assert "max_threads = 8" in final_config
    assert "max_depth = 1" not in final_config
    assert "multi_agent = true" not in final_config
    assert "# >>> manifest-dev managed config >>>" not in final_config


def test_codex_uninstall_removes_generated_config_when_install_created_it(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    run_installer("codex", env)

    assert (codex_dir / "config.toml").is_file()

    run_installer("codex", env, "uninstall")

    assert not (codex_dir / "config.toml").exists()
    assert not (codex_dir / "manifest-dev-install-state.json").exists()


def test_codex_uninstall_uses_embedded_state_when_state_file_is_missing(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    run_installer("codex", env)

    state_path = codex_dir / "manifest-dev-install-state.json"
    assert state_path.is_file()
    state_path.unlink()

    run_installer("codex", env, "uninstall")

    assert not (codex_dir / "config.toml").exists()


def test_codex_uninstall_preserves_user_kept_fallback_list_changes(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    run_installer("codex", env)

    config_path = codex_dir / "config.toml"
    config_text = config_path.read_text(encoding="utf-8")
    config_text = config_text.replace(
        'project_doc_fallback_filenames = ["CLAUDE.md"]',
        'project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]',
    )
    config_path.write_text(config_text, encoding="utf-8")

    run_installer("codex", env, "uninstall")

    final_config = config_path.read_text(encoding="utf-8")
    assert 'project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]' in final_config


def test_codex_upgrade_from_v1_state_preserves_preexisting_shared_settings(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    config_path = codex_dir / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        (
            'preferred_auth_method = "apikey"\n\n'
            "[features]\n"
            "multi_agent = true\n\n"
            "[agents]\n"
            "max_threads = 6\n"
            "max_depth = 1\n"
            'project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]\n'
        ),
        encoding="utf-8",
    )

    run_installer("codex", env)

    state_path = codex_dir / "manifest-dev-install-state.json"
    state_path.write_text(
        json.dumps(
            {
                "version": 1,
                "config_existed": True,
                "added_keys": {
                    "features.multi_agent": False,
                    "agents.max_threads": False,
                    "agents.max_depth": False,
                },
                "added_list_values": {
                    "agents.project_doc_fallback_filenames": [],
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    config_path.write_text(
        "\n".join(
            line
            for line in config_path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("# manifest-dev-shared-state: ")
        )
        + "\n",
        encoding="utf-8",
    )

    run_installer("codex", env)
    state_path.unlink()
    run_installer("codex", env, "uninstall")

    final_config = config_path.read_text(encoding="utf-8")
    assert 'preferred_auth_method = "apikey"' in final_config
    assert "multi_agent = true" in final_config
    assert "max_threads = 6" in final_config
    assert "max_depth = 1" in final_config
    assert 'project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]' in final_config
    assert "# >>> manifest-dev managed config >>>" not in final_config
    assert "[agents.criteria-checker-manifest-dev]" not in final_config


def test_codex_upgrade_from_v1_state_removes_manifest_added_shared_settings(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    codex_dir = Path(env["HOME"]) / ".codex"
    config_path = codex_dir / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text('preferred_auth_method = "apikey"\n', encoding="utf-8")

    run_installer("codex", env)

    state_path = codex_dir / "manifest-dev-install-state.json"
    state_path.write_text(
        json.dumps(
            {
                "version": 1,
                "config_existed": True,
                "added_keys": {
                    "features.multi_agent": True,
                    "agents.max_threads": True,
                    "agents.max_depth": True,
                },
                "added_list_values": {
                    "agents.project_doc_fallback_filenames": ["CLAUDE.md"],
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    config_path.write_text(
        "\n".join(
            line
            for line in config_path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("# manifest-dev-shared-state: ")
        )
        + "\n",
        encoding="utf-8",
    )

    run_installer("codex", env)
    state_path.unlink()
    run_installer("codex", env, "uninstall")

    final_config = config_path.read_text(encoding="utf-8")
    assert 'preferred_auth_method = "apikey"' in final_config
    assert "multi_agent = true" not in final_config
    assert "max_threads = 6" not in final_config
    assert "max_depth = 1" not in final_config
    assert "CLAUDE.md" not in final_config
    assert "# >>> manifest-dev managed config >>>" not in final_config


def test_opencode_uninstall_removes_only_manifest_dev_files(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    opencode_dir = Path(env["HOME"]) / ".config" / "opencode"
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

    run_installer("opencode", env)
    run_installer("opencode", env, "uninstall")

    assert custom_skill.is_dir()
    assert root_plugin.read_text(encoding="utf-8") == "// user-managed root plugin\n"
    assert json.loads(opencode_config.read_text(encoding="utf-8")) == {
        "$schema": "https://opencode.ai/config.json",
        "plugin": ["./plugins/index.ts"],
        "mcp": {"custom": {"type": "local", "command": ["echo", "hi"]}},
    }
    assert not (plugins_dir / "manifest-dev.ts").exists()
    assert not (plugins_dir / "manifest-dev.HOOK_SPEC.md").exists()
    assert not (opencode_dir / "skills" / "define-manifest-dev").exists()
    assert not (opencode_dir / "agents" / "criteria-checker-manifest-dev.md").exists()
    assert not (opencode_dir / "commands" / "define-manifest-dev.md").exists()


def test_opencode_uninstall_removes_legacy_manifest_dev_root_plugin(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    opencode_dir = Path(env["HOME"]) / ".config" / "opencode"
    plugins_dir = opencode_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    root_plugin = plugins_dir / "index.ts"
    root_plugin.write_text(
        "/** manifest-dev plugin for OpenCode CLI */\nexport default {}\n",
        encoding="utf-8",
    )

    run_installer("opencode", env)
    assert (plugins_dir / "index.ts.manifest-dev-legacy.bak").is_file()

    run_installer("opencode", env, "uninstall")

    assert not root_plugin.exists()
    assert (plugins_dir / "index.ts.manifest-dev-legacy.bak").is_file()
    assert not (plugins_dir / "manifest-dev.ts").exists()


def test_gemini_uninstall_removes_extension_and_manifest_hooks_only(
    tmp_path: Path,
) -> None:
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

    install_dir = gemini_dir / "extensions" / "manifest-dev"
    run_installer("gemini", env)
    assert install_dir.is_dir()
    assert (install_dir / "install-state.json").is_file()

    run_installer("gemini", env, "uninstall")

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged["selectedAuthType"] == "gemini-api-key"
    assert merged["experimental"] == {"otherFlag": True}
    assert merged["hooks"] == {
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
    }
    assert not install_dir.exists()
    assert (gemini_dir / "settings.json.pre-manifest-dev-uninstall.bak").is_file()


def test_gemini_uninstall_preserves_preexisting_enable_agents(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    settings_path = gemini_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "experimental": {
                    "enableAgents": True,
                    "otherFlag": True,
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    run_installer("gemini", env)
    run_installer("gemini", env, "uninstall")

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged["experimental"]["enableAgents"] is True
    assert merged["experimental"]["otherFlag"] is True


def test_gemini_uninstall_removes_settings_file_created_by_install(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    settings_path = gemini_dir / "settings.json"

    run_installer("gemini", env)
    assert settings_path.is_file()

    run_installer("gemini", env, "uninstall")

    assert not settings_path.exists()
    assert not (gemini_dir / "extensions" / "manifest-dev").exists()


def test_gemini_uninstall_uses_global_state_when_extension_state_is_missing(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    settings_path = gemini_dir / "settings.json"

    run_installer("gemini", env)

    local_state = gemini_dir / "extensions" / "manifest-dev" / "install-state.json"
    global_state = gemini_dir / "manifest-dev-install-state.json"
    assert local_state.is_file()
    assert global_state.is_file()
    local_state.unlink()

    run_installer("gemini", env, "uninstall")

    assert not settings_path.exists()
    assert not global_state.exists()


def test_gemini_uninstall_preserves_enable_agents_after_user_expands_experimental_settings(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    run_installer("gemini", env)

    settings_path = gemini_dir / "settings.json"
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    data.setdefault("experimental", {})["otherFeature"] = True
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    run_installer("gemini", env, "uninstall")

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged["experimental"]["enableAgents"] is True
    assert merged["experimental"]["otherFeature"] is True


def test_gemini_upgrade_from_v1_state_removes_manifest_added_enable_agents(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    settings_path = gemini_dir / "settings.json"
    settings_path.write_text(
        json.dumps({"selectedAuthType": "gemini-api-key"}, indent=2) + "\n",
        encoding="utf-8",
    )

    run_installer("gemini", env)

    local_state = gemini_dir / "extensions" / "manifest-dev" / "install-state.json"
    hooks_added = json.loads(local_state.read_text(encoding="utf-8"))["hooks_added"]
    local_state.write_text(
        json.dumps(
            {
                "version": 1,
                "settings_existed": True,
                "experimental": {
                    "enableAgents": {
                        "present": False,
                        "value": None,
                    }
                },
                "hooks_added": hooks_added,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    global_state = gemini_dir / "manifest-dev-install-state.json"
    if global_state.exists():
        global_state.unlink()

    run_installer("gemini", env)
    local_state.unlink()
    run_installer("gemini", env, "uninstall")

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged == {"selectedAuthType": "gemini-api-key"}


def test_gemini_upgrade_from_v1_state_preserves_preexisting_enable_agents(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")

    gemini_dir = Path(env["HOME"]) / ".gemini"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    settings_path = gemini_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "selectedAuthType": "gemini-api-key",
                "experimental": {"enableAgents": True},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    run_installer("gemini", env)

    local_state = gemini_dir / "extensions" / "manifest-dev" / "install-state.json"
    hooks_added = json.loads(local_state.read_text(encoding="utf-8"))["hooks_added"]
    local_state.write_text(
        json.dumps(
            {
                "version": 1,
                "settings_existed": True,
                "experimental": {
                    "enableAgents": {
                        "present": True,
                        "value": True,
                    }
                },
                "hooks_added": hooks_added,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    global_state = gemini_dir / "manifest-dev-install-state.json"
    if global_state.exists():
        global_state.unlink()

    run_installer("gemini", env)
    local_state.unlink()
    run_installer("gemini", env, "uninstall")

    merged = json.loads(settings_path.read_text(encoding="utf-8"))
    assert merged == {
        "selectedAuthType": "gemini-api-key",
        "experimental": {"enableAgents": True},
    }
