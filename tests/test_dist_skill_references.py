"""
Verify each CLI distribution carries the full surviving skill set with correct namespacing.

The post-promotion plugin ships seven skills: auto, define, do, done, escalate,
figure-out, figure-out-team. After install_helpers.py namespaces them with the
`-manifest-dev` suffix, every skill directory should resolve in every dist.

Also confirms the removed plugin components stay removed:
  - no `verify` skill in any dist
  - no `manifest-verifier` agent in any dist
  - no `pretool_verify_hook.py` or `prompt_submit_hook.py` in the gemini hooks dir
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist"

SURVIVING_SKILLS = (
    "auto",
    "define",
    "do",
    "done",
    "escalate",
    "figure-out",
    "figure-out-team",
)

REMOVED_SKILLS = ("verify",)
REMOVED_AGENTS = ("manifest-verifier",)
REMOVED_GEMINI_HOOKS = ("pretool_verify_hook.py", "prompt_submit_hook.py")


def namespace_dist(tmp_path: Path, cli: str) -> Path:
    """Mirror dist/{cli} into tmp_path and run that CLI's install_helpers to
    namespace components in place. Per-CLI argv conventions differ — codex
    uses ``namespace <dir> <cli>`` while gemini and opencode take ``<src> <dst>``.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    src = DIST / cli
    dest = tmp_path / cli
    shutil.copytree(src, dest)

    if cli == "codex":
        argv = [sys.executable, str(dest / "install_helpers.py"), "namespace", str(dest), cli]
    else:
        argv = [sys.executable, str(dest / "install_helpers.py"), str(dest), str(dest)]

    subprocess.run(argv, check=True, cwd=dest)
    return dest


def test_every_dist_namespaces_the_surviving_skill_set(tmp_path: Path) -> None:
    for cli in ("codex", "opencode", "gemini"):
        dist_dir = namespace_dist(tmp_path / cli, cli)
        for skill in SURVIVING_SKILLS:
            skill_dir = dist_dir / "skills" / f"{skill}-manifest-dev"
            assert skill_dir.is_dir(), f"{cli}: {skill}-manifest-dev missing"
            assert (skill_dir / "SKILL.md").is_file(), (
                f"{cli}: {skill}-manifest-dev/SKILL.md missing"
            )


def test_removed_components_are_not_distributed() -> None:
    for cli in ("codex", "opencode", "gemini"):
        for skill in REMOVED_SKILLS:
            assert not (DIST / cli / "skills" / skill).exists(), (
                f"{cli}: removed skill {skill!r} still in dist"
            )
        for agent in REMOVED_AGENTS:
            for ext in (".md", ".toml"):
                assert not (DIST / cli / "agents" / f"{agent}{ext}").exists(), (
                    f"{cli}: removed agent {agent}{ext} still in dist"
                )

    for hook in REMOVED_GEMINI_HOOKS:
        assert not (DIST / "gemini" / "hooks" / hook).exists(), (
            f"removed gemini hook {hook} still in dist"
        )


def test_figure_out_team_command_exists_for_opencode() -> None:
    """OpenCode exposes user-invocable skills as slash commands; figure-out-team must be one."""
    command_file = DIST / "opencode" / "commands" / "figure-out-team.md"
    assert command_file.is_file(), "opencode/commands/figure-out-team.md missing"


def test_slack_poller_agent_exists_in_every_dist() -> None:
    """The slack-poller subagent is new in this release; every dist must carry it."""
    assert (DIST / "gemini" / "agents" / "slack-poller.md").is_file()
    assert (DIST / "opencode" / "agents" / "slack-poller.md").is_file()
    assert (DIST / "codex" / "agents" / "slack-poller.toml").is_file()
