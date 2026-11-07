"""Every hand-kept list of a plugin's skills names exactly the skills that plugin ships.

The distribution READMEs and OpenCode's AGENTS.md list skills by hand, so a new skill leaves them
behind unless something fails; two of them had drifted before this check existed.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ("manifest-dev", "manifest-dev-tools")
DIST_READMES = [
    ROOT / "dist" / cli / "README.md" for cli in ("codex", "cursor", "opencode", "pi")
]


def shipped(plugin: str) -> set[str]:
    skills = ROOT / "claude-plugins" / plugin / "skills"
    return {p.name for p in skills.iterdir() if (p / "SKILL.md").is_file()}


def user_invocable(plugin: str) -> set[str]:
    return {
        name
        for name in shipped(plugin)
        if "user-invocable: false"
        not in (
            ROOT / "claude-plugins" / plugin / "skills" / name / "SKILL.md"
        ).read_text(encoding="utf-8")
    }


@pytest.mark.parametrize("readme", DIST_READMES, ids=lambda p: p.parent.name)
@pytest.mark.parametrize("plugin", PLUGINS)
def test_dist_readme_table_lists_every_skill(readme: Path, plugin: str) -> None:
    text = readme.read_text(encoding="utf-8")
    row = re.search(rf"^\| `{re.escape(plugin)}` \|(.*)\|\s*$", text, re.M)
    assert row, f"{readme.relative_to(ROOT)} has no skill row for {plugin}"
    listed = set(re.findall(r"`([a-z0-9-]+)`", row.group(1)))
    assert listed == shipped(plugin), (
        f"{readme.relative_to(ROOT)} row for {plugin}: missing {sorted(shipped(plugin) - listed)},"
        f" extra {sorted(listed - shipped(plugin))}"
    )


def test_opencode_agents_names_every_user_invocable_skill() -> None:
    text = (ROOT / "dist" / "opencode" / "AGENTS.md").read_text(encoding="utf-8")
    names = set(re.findall(r"/([a-z0-9-]+)", text))
    missing = sorted(
        name
        for plugin in PLUGINS
        for name in user_invocable(plugin)
        if name not in names
    )
    assert not missing, f"dist/opencode/AGENTS.md names no /{missing}"
