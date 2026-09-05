"""Plugin skills load only through plugins; local maintenance links stay valid."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent.parent
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
AGENTS_SKILLS = ROOT / ".agents" / "skills"
TEMPLATE_PLUGIN = "PLUGIN_TEMPLATE"


def plugin_skill_dirs() -> list[Path]:
    """Every skill directory shipped by a real plugin, template plugin excluded."""
    return sorted(
        skill_md.parent
        for skill_md in (ROOT / "claude-plugins").glob("*/skills/*/SKILL.md")
        if TEMPLATE_PLUGIN not in skill_md.parts
    )


def local_skill_entries(parent: Path) -> list[Path]:
    """Every entry under a local skills directory, dangling links included."""
    return sorted(entry for entry in parent.iterdir() if not entry.name.startswith("."))


def links_to(link: Path, target: Path) -> bool:
    return link.is_symlink() and link.resolve() == target.resolve()


def test_plugin_skills_are_not_exposed_as_local_skills() -> None:
    names = {skill.name for skill in plugin_skill_dirs()}
    duplicates = [
        str(entry.relative_to(ROOT))
        for parent in (CLAUDE_SKILLS, AGENTS_SKILLS)
        for entry in local_skill_entries(parent)
        if entry.name in names or (ROOT / "claude-plugins") in entry.resolve().parents
    ]
    assert not duplicates, f"plugin skills duplicated in local discovery: {duplicates}"


def test_every_claude_skill_is_linked_from_agents() -> None:
    broken = [
        entry.name
        for entry in local_skill_entries(CLAUDE_SKILLS)
        if (entry.is_dir() or entry.is_symlink())
        and not links_to(AGENTS_SKILLS / entry.name, entry)
    ]
    assert not broken, (
        f"skills missing an .agents/skills symlink: {broken}; create with "
        "ln -sfn ../../.claude/skills/<name> .agents/skills/<name>"
    )


def test_no_agents_skill_outlives_its_claude_counterpart() -> None:
    """A rename leaves the old name behind as a real directory, which no link check sees."""
    orphans = [
        entry.name
        for entry in local_skill_entries(AGENTS_SKILLS)
        if not (CLAUDE_SKILLS / entry.name).exists()
    ]
    assert not orphans, (
        f"entries under .agents/skills with no .claude/skills counterpart: {orphans}; "
        "a renamed or deleted skill leaves these behind and sessions still load them"
    )


def test_no_local_skill_link_dangles() -> None:
    dangling = [
        str(entry.relative_to(ROOT))
        for parent in (CLAUDE_SKILLS, AGENTS_SKILLS)
        for entry in local_skill_entries(parent)
        if entry.is_symlink() and not entry.resolve().exists()
    ]
    assert not dangling, (
        f"symlinks pointing at nothing: {dangling}; a renamed or deleted skill "
        "leaves these behind, and the skill loader reports an entry it cannot read"
    )
