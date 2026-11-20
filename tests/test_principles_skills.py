"""Principles skills follow one shipped method, and this repository's own follow its shape.

The method — what a line must be, the skill's shape, the pointer line, which areas are worth a
skill, and how lines are written and pruned — lives in setup-project's PRINCIPLES_SKILLS.md
alone. Every other shipped file that works with a principles skill points there, so the copies
cannot drift. create-principles-skill stays a thin wrapper over figure-out that points there too.
The one exception is the review rule: review-code runs alone, so its PROJECT_PRINCIPLES.md carries
the method's review paragraph word for word, and a test below keeps the two equal.

Holds docs/adr/20261109-area-principles-live-in-project-skills.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from tests.prose import flat

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
    for path in (
        METHOD,
        SKILLS / "figure-out" / "SKILL.md",
        SKILLS / "define" / "SKILL.md",
    ):
        text = flat(path.read_text(encoding="utf-8"))
        where = path.relative_to(ROOT)
        assert "the principle holds unless the" in text, where
        assert "chose the departure" in text, where
        assert "the one change that restores what was asked" in text, where
        assert "whether the principle has moved or this is an exception" in text, where


REVIEW_CODE = SKILLS / "review-code" / "SKILL.md"
REVIEW_CODE_RULE = SKILLS / "review-code" / "references" / "PROJECT_PRINCIPLES.md"
# Every dimension in review-code's table still reports a principle departure that bears on its own
# calls, except these, each for its reason.
NOT_OWNING = {
    "context-file-adherence": "it is the backstop that covers every principle",
    "defect-class": "it reviews a fix against a supplied defect and routes no project rules away",
    "operational-readiness": "its out-of-scope list routes no project rules away",
}
OWNING_DIMENSIONS = sorted(
    set(
        re.findall(
            r"^\| `([a-z-]+)` \| `references/",
            REVIEW_CODE.read_text(encoding="utf-8"),
            re.M,
        )
    )
    - set(NOT_OWNING)
)
# The shared review paragraph opens and closes on these; everything between them must match word for
# word. review-code's copy opens with two sentences of its own (which dimension reports a departure;
# its grade), which this pattern leaves out; the test asserts both separately.
REVIEW_RULE = re.compile(
    r"A\s+project's\s+principles\s+skills\s+are\s+project\s+skills\s+named\s.*?"
    r"naming\s+the\s+principle\s+that\s+produced\s+it\.",
    re.S,
)


def review_rule(path: Path) -> str:
    match = REVIEW_RULE.search(path.read_text(encoding="utf-8"))
    assert match, f"{path.relative_to(ROOT)} lost the review rule for principles skills"
    return flat(match.group(0))


def test_review_code_carries_the_review_rule_word_for_word() -> None:
    """A review holds work to the project's principles unless a person with authority over the
    principle chose the departure, and a record the change adds is its case, not that choice.
    review-code runs alone, so it carries the rule in a reference its body loads only where the
    project points to principles skills; the method states it too. The two copies must not drift
    apart, and review-code's own leading sentence keeps one grade across dimensions.

    Holds docs/adr/20261117-a-review-holds-work-to-the-projects-principles-unless-a-person-chose-the-departure.md.
    """
    method = review_rule(METHOD)
    for marker in (
        "A principle holds unless its yield is shown or a person with authority over it chose the departure.",
        "authoring the change gives none",
        "it is not chosen",
        "is its case, not a person's choice",
        "never grade it Low",
        "count it against acceptance",
        "outrank the review's general standards in both directions",
        "whatever the skill holding it is called",
        "the work's own assertion that it holds does not",
        "anything the run that produced the change wrote",
        "until then the work departs, unless such a person chose the departure",
        "a condition the evidence leaves open or arguable is not shown",
        "for a line the work under review cannot show either way",
    ):
        assert marker in method, f"the review rule lost {marker!r}"
    assert (
        review_rule(REVIEW_CODE_RULE) == method
    ), "review-code carries a review rule that differs from the method's"
    own = flat(REVIEW_CODE_RULE.read_text(encoding="utf-8"))
    assert (
        "the dimension that owns a principle's call reports a departure from it, and "
        "`context-file-adherence` covers every principle" in own
    ), "review-code no longer says which dimension reports a departure"
    pointer = (
        "Where `PROJECT_PRINCIPLES.md` is loaded, a departure from one of its principles that "
        "bears on this dimension's own calls is reported here as well."
    )
    assert len(OWNING_DIMENSIONS) == 11, "review-code's dimension table was not read"
    for name in OWNING_DIMENSIONS:
        reference = SKILLS / "review-code" / "references" / f"{name}.md"
        assert pointer in flat(
            reference.read_text(encoding="utf-8")
        ), f"{name} no longer reports a departure from a principle bearing on its own calls"
    assert (
        "Whichever dimension reports an unchosen departure, it is a broken binding requirement: High"
        in own
    ), "review-code no longer grades an unchosen departure the same in every dimension"
    body = flat(REVIEW_CODE.read_text(encoding="utf-8"))
    assert (
        "also load `references/PROJECT_PRINCIPLES.md` and follow it" in body
    ), "review-code's body no longer loads its review rule for principles skills"


def test_no_review_skill_picks_principles_by_area_name() -> None:
    """Projects name their areas freely, so a review finds principles skills by their pointers and
    stated use. No file in a review skill's own directory may name a concrete principles skill: the
    only form allowed is the placeholder `<area>-principles`.

    Holds docs/adr/20261117-a-review-holds-work-to-the-projects-principles-unless-a-person-chose-the-departure.md.
    """
    named = re.compile(r"(?<![\w<>-])[a-z][a-z-]*-principles\b(?!-)")
    review_files = sorted(ROOT.glob("claude-plugins/*/skills/review-*/**/*.md"))
    skills = {p.relative_to(ROOT).parts[3] for p in review_files}
    assert {
        "review-code",
        "review-design",
        "review-writing",
        "review-prompt",
        "review-pr",
    } <= skills
    hits = [
        f"{p.relative_to(ROOT)}: {m.group(0)}"
        for p in review_files
        for m in named.finditer(p.read_text(encoding="utf-8"))
    ]
    assert not hits, f"these review files name a principles skill: {hits}"
