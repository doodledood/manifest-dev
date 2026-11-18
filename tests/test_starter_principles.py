"""The starter principles setup-project offers keep the shape setup reads.

Setup shows each starter line word for word and writes the accepted ones into a project's
principles skill, so a line without its reason or yield, a conditional line without its
condition, or a choice without its sides would be offered and written broken. The method in
`PRINCIPLES_SKILLS.md` names the sets in a table; a set on disk the table does not name is never
offered, and a row with no set points setup at nothing. A change to a set's text reaches installed
projects only through a new surfaces version, which `test_setup_project_versions.py` holds by
digesting these files with the rest of what setup emits.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SETUP = REPO_ROOT / "claude-plugins" / "manifest-dev" / "skills" / "setup-project" / "references"
SETS = SETUP / "starter-principles"
METHOD = SETUP / "PRINCIPLES_SKILLS.md"

TITLE = re.compile(r"^# Starter principles: (?P<area>.+)$")
SKILL = re.compile(r"^- Skill: `(?P<name>[a-z]+(?:-[a-z]+)*-principles)`$")
OFFERED = re.compile(r"^- Offered when: \S")
CONDITION = re.compile(r"^Only where (?P<cond>[^:]+): (?P<line>.+)$")
CHOICE = re.compile(
    r"^Choice — (?P<what>[^.]+)\. Default side, unless (?P<signal>.+); then the other side\.$"
)
SIDE = re.compile(r"^  - (?P<side>Default side|Other side): (?P<line>.+)$")
TABLE_ROW = re.compile(r"^\| (?P<area>[^|]+?) \| `starter-principles/(?P<file>[a-z-]+\.md)` \|$")


def principle_errors(text: str) -> list[str]:
    """What a written principle lacks: its reason after a dash, and its yield statement."""
    errors = []
    if " — " not in text:
        errors.append("no reason after ' — '")
    if not re.search(r"(Yields (when|for|where|while|to|inside|once)|Holds without a yield)", text):
        errors.append("no 'Yields ...' or 'Holds without a yield'")
    return errors


def set_errors(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or not TITLE.match(lines[0]):
        errors.append("first line is not '# Starter principles: <Area>'")
    if not any(SKILL.match(l) for l in lines):
        errors.append("no '- Skill: `<area>-principles`' line")
    if not any(OFFERED.match(l) for l in lines):
        errors.append("no '- Offered when:' line")
    if "## Lines" not in lines:
        errors.append("no '## Lines' section")
        return errors
    body = lines[lines.index("## Lines") + 1 :]
    entries = [l for l in body if l.strip()]
    if not any(l.startswith("- ") for l in entries):
        errors.append("no lines under '## Lines'")
    i = 0
    while i < len(entries):
        entry = entries[i]
        if not entry.startswith("- "):
            errors.append(f"stray text: {entry[:60]!r}")
            i += 1
            continue
        text = entry[2:]
        conditional = CONDITION.match(text)
        if text.startswith("Only where") and not conditional:
            errors.append(f"conditional line without 'Only where <condition>: ': {text[:60]!r}")
        if conditional:
            text = conditional["line"]
        if text.startswith("Choice"):
            if not CHOICE.match(text):
                errors.append(f"choice without its default rule: {text[:60]!r}")
            sides = []
            while i + 1 < len(entries) and entries[i + 1].startswith("  - "):
                i += 1
                side = SIDE.match(entries[i])
                if not side:
                    errors.append(f"choice side not named: {entries[i][:60]!r}")
                    continue
                sides.append(side["side"])
                errors += [f"{side['side']}: {e}" for e in principle_errors(side["line"])]
            if sides != ["Default side", "Other side"]:
                errors.append(f"choice sides are {sides}, not a default then an other side")
        else:
            errors += [f"{text[:50]!r}: {e}" for e in principle_errors(text)]
        i += 1
    return errors


def method_table() -> dict[str, str]:
    rows = {}
    for line in METHOD.read_text(encoding="utf-8").splitlines():
        row = TABLE_ROW.match(line)
        if row:
            rows[row["file"]] = row["area"]
    return rows


def test_every_starter_set_keeps_the_shape_setup_reads() -> None:
    failures = {p.name: set_errors(p) for p in sorted(SETS.glob("*.md"))}
    failures = {name: errs for name, errs in failures.items() if errs}
    assert not failures, f"starter sets out of shape: {failures}"


def test_the_method_names_exactly_the_sets_on_disk() -> None:
    on_disk = {p.name for p in SETS.glob("*.md")}
    named = method_table()
    assert on_disk and set(named) == on_disk, (
        f"PRINCIPLES_SKILLS.md names {sorted(named)}; on disk: {sorted(on_disk)}"
    )
    for name, area in named.items():
        title = TITLE.match((SETS / name).read_text(encoding="utf-8").splitlines()[0])
        assert title and area.split(" (")[0] == title["area"], f"{name}: the table calls it {area!r}"


def test_each_set_names_a_skill_of_its_own() -> None:
    names = []
    for path in SETS.glob("*.md"):
        names += [m["name"] for m in map(SKILL.match, path.read_text().splitlines()) if m]
    assert len(names) == len(set(names)), f"two sets name the same skill: {sorted(names)}"


def test_set_errors_catches_each_broken_shape() -> None:
    good = (
        "# Starter principles: X\n\n- Skill: `x-principles`\n- Offered when: always.\n\n## Lines\n\n"
        "- A rule — a reason. Yields when a case.\n"
    )
    assert not set_errors_text(good)
    broken = {
        "no reason": good.replace(" — a reason", ""),
        "no yield": good.replace(" Yields when a case.", ""),
        "condition": good.replace("- A rule", "- Only where a thing holds A rule"),
        "choice rule": good + "- Choice — a call.\n  - Default side: a — b. Yields when c.\n"
        "  - Other side: d — e. Yields when f.\n",
        "choice side": good + "- Choice — a call. Default side, unless s; then the other side.\n"
        "  - Default side: a — b. Yields when c.\n",
    }
    for what, text in broken.items():
        assert set_errors_text(text), f"a set with a broken {what} passed"


def set_errors_text(text: str) -> list[str]:
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.md"
        p.write_text(text, encoding="utf-8")
        return set_errors(p)
