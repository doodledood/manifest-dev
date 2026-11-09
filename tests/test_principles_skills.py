"""Principles skills follow one shipped method, and this repository's own follow its shape.

The method — what a line must be, the skill's shape, the pointer line, which areas are worth a
skill, and how lines are written and pruned — lives in setup-project's PRINCIPLES_SKILLS.md
alone. Every other shipped file that works with a principles skill points there, so the copies
cannot drift. create-principles-skill stays a thin wrapper over figure-out that points there too.

Holds docs/adr/20261109-area-principles-live-in-project-skills.md.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"
METHOD = SKILLS / "setup-project" / "references" / "PRINCIPLES_SKILLS.md"
WRAPPER = SKILLS / "create-principles-skill" / "SKILL.md"
METHOD_NAME = "PRINCIPLES_SKILLS.md"
# Wording only the method states; a second shipped file carrying it is a restated method.
METHOD_MARKERS = (
    "One stray comment in an area is not signal",
    "A call a run made on its own | nowhere",
    "Sharpen before adding:",
    "A principle steered against:",
    "Gather what the session showed:",
)
LOCAL_SKILLS = ROOT / ".claude" / "skills"
CONTEXT_FILE = ROOT / "CLAUDE.md"


def shipped_markdown() -> list[Path]:
    return sorted((ROOT / "claude-plugins").rglob("*.md"))


def instructing_markdown() -> list[Path]:
    """Shipped skill files a run acts on; version notes and the help glossary only describe."""
    notes = SKILLS / "setup-project" / "references"
    describing = (notes / "changes", SKILLS / "manifest-dev-help")
    return [
        p
        for p in sorted(SKILLS.rglob("*.md"))
        if p != notes / "CHANGES.md" and not any(d in p.parents for d in describing)
    ]


def test_wrapper_invokes_figure_out_and_points_to_the_method() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    invoke = re.search(r"Invoke the figure-out skill\b[^.]*\.", text)
    assert invoke, "the wrapper must invoke figure-out"
    assert "when given" in invoke.group(
        0
    ), "the wrapper forwards --autonomous only when given, so it runs attended by default"
    assert (
        "Run it attended unless `--autonomous` was given" in text
    ), "the wrapper must run attended by default, so only a person's yes writes a line"
    assert (
        f"`../setup-project/references/{METHOD_NAME}`" in text
    ), "the wrapper must point to the method"


def test_the_method_lives_in_one_file() -> None:
    method = METHOD.read_text(encoding="utf-8")
    for marker in METHOD_MARKERS:
        assert marker in method, f"the method lost its marker {marker!r}"
        holders = [
            p.relative_to(ROOT)
            for p in shipped_markdown()
            if marker in p.read_text(encoding="utf-8")
        ]
        assert holders == [
            METHOD.relative_to(ROOT)
        ], f"{marker!r} must live in the method alone: {holders}"


def test_every_shipped_file_naming_a_principles_skill_points_to_the_method() -> None:
    missing = [
        str(p.relative_to(ROOT))
        for p in instructing_markdown()
        if p != METHOD
        and re.search(r"principles skill", p.read_text(encoding="utf-8"), re.I)
        and METHOD_NAME not in p.read_text(encoding="utf-8")
    ]
    assert (
        not missing
    ), f"these files work with principles skills without the method: {missing}"


METHOD_PATH = re.compile(r"`([^`\s]*/" + re.escape(METHOD_NAME) + r")`")


def test_every_path_to_the_method_resolves() -> None:
    broken = [
        f"{p.relative_to(ROOT)}: {target}"
        for p in instructing_markdown()
        for target in METHOD_PATH.findall(p.read_text(encoding="utf-8"))
        if (p.parent / target).resolve() != METHOD
    ]
    assert not broken, f"these paths to the method do not reach it: {broken}"


def local_principles_skills() -> list[Path]:
    return sorted(LOCAL_SKILLS.glob("*-principles/SKILL.md"))


def pointer_line(name: str, path: str) -> re.Pattern[str]:
    """The method's pointer line: `- **<Area> work** — load the `<name>` skill (`<path>`) before ...`."""
    return re.compile(
        rf"^- \*\*[^*\n]+ work\*\* — load the `{re.escape(name)}` skill"
        rf" \(`{re.escape(path)}`\) before ",
        re.MULTILINE,
    )


def test_this_repositorys_principles_skills_keep_the_shape() -> None:
    context = CONTEXT_FILE.read_text(encoding="utf-8")
    skills = local_principles_skills()
    assert skills, f"no principles skills under {LOCAL_SKILLS.relative_to(ROOT)}"
    for skill in skills:
        name = skill.parent.name
        body = skill.read_text(encoding="utf-8").split("---", 2)[2].strip()
        assert body.startswith("Edit rule:"), f"{name} must open with the edit rule"
        assert (
            "fresh start" in body.split("\n\n")[-1]
        ), f"{name} must end with the self-check"
        assert pointer_line(name, str(skill.relative_to(ROOT))).search(
            context
        ), f"CLAUDE.md must carry the method's pointer line for {name} and its path"


def test_a_principle_holds_unless_the_person_chose_the_departure() -> None:
    """The method, figure-out and define each say what happens when a request conflicts with a
    principle: figure-out and define run without the method loaded, so each carries the rule.

    Holds docs/adr/20261109-an-unattended-run-keeps-to-a-principle-over-a-conflicting-request.md.
    """
    for path in (METHOD, SKILLS / "figure-out" / "SKILL.md", SKILLS / "define" / "SKILL.md"):
        text = " ".join(path.read_text(encoding="utf-8").split())
        where = path.relative_to(ROOT)
        assert "the principle holds unless the" in text, where
        assert "chose the departure" in text, where
        assert "the one change that restores what was asked" in text, where
        assert "whether the principle has moved or this is an exception" in text, where
