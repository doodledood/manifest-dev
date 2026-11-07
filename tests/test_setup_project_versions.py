"""A change to what setup-project writes into projects must ship as a new surfaces version.

setup-project copies or emits a few files into every project it sets up. A project records
the surfaces version it carries in its context file, and a later update offers only the
changes listed for the versions after it: `CHANGES.md` holds one line per version, and each
version's items live in its own file under `changes/`, so an update reads only what it offers. So an edit to an emitted file that does
not add a version leaves every installed project unable to learn about it.

This test pins a digest of the emitted text to the latest version's file. HTML
comments are left out of the digest: they are maintainer notes the copy drops, and the
template's own version comment would otherwise make the digest depend on itself.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "claude-plugins" / "manifest-dev" / "skills"
SETUP = SKILLS / "setup-project" / "references"
CHANGES = SETUP / "CHANGES.md"
CHANGES_DIR = SETUP / "changes"
NORTH_STAR_FORMAT = SETUP / "NORTH_STAR_FORMAT.md"
EVALS = REPO_ROOT / "claude-plugins" / "manifest-dev" / "evals"
UPGRADES = SETUP / "upgrades"
HARNESS = SETUP / "harness"

# Every file whose text setup-project copies or emits into a project: the conventions, the
# surfaces template, and the verification harness it copies (the tool and its example data).
EMITTED = (
    SKILLS / "figure-out" / "references" / "ADR_FORMAT.md",
    NORTH_STAR_FORMAT,
    HARNESS / "verify",
    HARNESS / "verify.mts",
    HARNESS / "harness.md",
    *sorted((HARNESS / "recipes").glob("*.md")),
)

HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
INDEX_LINE = re.compile(r"^- v(\d+) — `changes/v\1\.md`: \S", re.MULTILINE)
VERSION_FILE = re.compile(r"^v(\d+)\.md$")
DIGEST_LINE = re.compile(r"^Digest: ([0-9a-f]{64})\s*$", re.MULTILINE)
TEMPLATE_VERSION = re.compile(r"<!-- setup-project surfaces v(\d+) -->")


def emitted_digest() -> str:
    digest = hashlib.sha256()
    for path in EMITTED:
        text = HTML_COMMENT.sub("", path.read_text(encoding="utf-8"))
        digest.update(
            path.relative_to(SETUP.parent.parent).as_posix().encode("utf-8") + b"\n"
        )
        digest.update(re.sub(r"\s+", " ", text).strip().encode("utf-8") + b"\n")
    return digest.hexdigest()


def versions() -> list[tuple[int, str, str]]:
    """Each version as (version, body, digest), in the order `CHANGES.md` lists them."""
    listed = [int(m.group(1)) for m in INDEX_LINE.finditer(CHANGES.read_text("utf-8"))]
    assert listed, f"{CHANGES} lists no `- vN — `changes/vN.md`: …` lines"
    entries = []
    for number in listed:
        path = CHANGES_DIR / f"v{number}.md"
        assert path.is_file(), f"{CHANGES} lists v{number}, but {path} does not exist"
        body = path.read_text(encoding="utf-8")
        digest = DIGEST_LINE.search(body)
        assert digest, f"{path} has no `Digest:` line"
        entries.append((number, body, digest.group(1)))
    return entries


def test_every_version_file_is_listed_and_every_listed_version_has_a_file() -> None:
    # The index and the files are one list read two ways; a reader finds the newest version in
    # the index, so a file it does not list would never be offered.
    files = sorted(
        int(m.group(1))
        for p in CHANGES_DIR.iterdir()
        if (m := VERSION_FILE.match(p.name))
    )
    listed = sorted(number for number, _, _ in versions())
    assert files == listed, (
        f"{CHANGES_DIR.relative_to(REPO_ROOT)} holds versions {files}, but "
        f"{CHANGES.relative_to(REPO_ROOT)} lists {listed}: add the missing line or file"
    )
    stray = sorted(
        p.name for p in CHANGES_DIR.iterdir() if not VERSION_FILE.match(p.name)
    )
    assert (
        not stray
    ), f"{CHANGES_DIR.relative_to(REPO_ROOT)} holds non-version files: {stray}"


def test_versions_count_up_from_one() -> None:
    numbers = [number for number, _, _ in versions()]
    assert numbers == list(
        range(1, len(numbers) + 1)
    ), f"{CHANGES} must list versions 1, 2, 3, … in order; found {numbers}"


# Holds the decision in docs/adr/20261013-set-up-projects-receive-updates-through-a-version-marker.md.
def test_every_version_says_what_projects_gain() -> None:
    for number, body, _ in versions():
        assert re.search(
            r"^- \S", body, re.MULTILINE
        ), f"{CHANGES_DIR}/v{number}.md lists nothing an installed project gains"


# Holds the decision in docs/adr/20261013-runs-build-and-maintain-a-project-verification-surface.md.
# Holds the decision in docs/adr/20261013-set-up-projects-receive-updates-through-a-version-marker.md.
# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_latest_version_matches_what_setup_project_emits() -> None:
    latest_number, _, latest_digest = versions()[-1]
    current = emitted_digest()
    assert latest_digest == current, (
        f"A file setup-project emits into projects changed since surfaces v{latest_number}. "
        f"Add {CHANGES_DIR.relative_to(REPO_ROOT)}/v{latest_number + 1}.md listing what an "
        f"installed project gains, with `Digest: {current}`, its line in "
        f"{CHANGES.relative_to(REPO_ROOT)}, and set the version comment "
        f"in {NORTH_STAR_FORMAT.relative_to(REPO_ROOT)}'s surfaces template to "
        f"v{latest_number + 1}."
    )


# Holds the decision in docs/adr/20261013-set-up-projects-receive-updates-through-a-version-marker.md.
def test_surfaces_template_carries_the_latest_version() -> None:
    latest_number = versions()[-1][0]
    found = TEMPLATE_VERSION.findall(NORTH_STAR_FORMAT.read_text(encoding="utf-8"))
    assert found == [str(latest_number)], (
        f"the project-surfaces template in {NORTH_STAR_FORMAT.relative_to(REPO_ROOT)} must "
        f"carry exactly one `<!-- setup-project surfaces v{latest_number} -->`; found {found}"
    )


DECLINE_LINE = "`<!-- setup-project update declined through vN -->`"
WITH_DOCS = SKILLS / "figure-out" / "references" / "WITH_DOCS.md"


# Holds the decision in docs/adr/20261107-only-setup-project-writes-the-surfaces-version.md. The
# version line says which surfaces a project carries, and setup-project attributes every
# difference by it. figure-out once wrote it on a declined offer, appending a section holding
# only that line, so a project never set up claimed the newest version and setup-project never
# offered its wiring or seeded it. No shipped skill but setup-project may emit the version line
# or the section, and figure-out records its decline in the one form setup-project reads.
def test_only_setup_project_writes_the_surfaces_version() -> None:
    writers = sorted(
        str(path.relative_to(REPO_ROOT))
        for path in (REPO_ROOT / "claude-plugins").glob("*/skills/**/*.md")
        if SKILLS / "setup-project" not in path.parents
        and re.search(
            r"setup-project surfaces v|^## Project surfaces|into the surfaces version line",
            path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    )
    assert not writers, (
        f"{writers} write the surfaces version line or the project-surfaces section; only "
        "setup-project writes them, and figure-out records a declined offer on its own line"
    )
    for path in (WITH_DOCS, SKILLS / "setup-project" / "SKILL.md"):
        assert DECLINE_LINE in path.read_text(encoding="utf-8"), (
            f"{path.relative_to(REPO_ROOT)} must name the decline line as {DECLINE_LINE}, the "
            "form figure-out writes and setup-project reads"
        )


# Holds the same record's repair of a legacy section. figure-out writes its decline line directly
# after the version line, so a legacy section holding only a version line and then declined again
# holds both. Recognizing only a lone version line read that legacy number as a real version: the
# run skipped seeding and attributed every older gap to the project.
def test_a_declined_legacy_section_is_still_read_as_no_version() -> None:
    text = (SKILLS / "setup-project" / "SKILL.md").read_text(encoding="utf-8")
    assert re.search(
        r"section holding nothing but a version line, with or without decline lines",
        text,
    ), (
        "setup-project must read a project-surfaces section holding only a version line and "
        "decline lines as left by a figure-out decline, since figure-out writes its decline line "
        "beside the version line"
    )


NEWEST_VERSION_CASE = "45-current-setup-offers-nothing"


def recorded_versions() -> dict[str, set[int]]:
    """The surfaces versions each eval case's scaffold records, by case, across both suites."""
    return {
        p.parent.name: {
            int(v) for v in TEMPLATE_VERSION.findall(p.read_text(encoding="utf-8"))
        }
        for p in EVALS.rglob("scaffold.sh")
    }


# Holds the decision in docs/adr/20261014-setup-project-audits-the-whole-setup-when-run.md.
def test_eval_cases_track_the_newest_version() -> None:
    # The newest-version case is graded on no offer, so it records the newest version. From
    # v2 on, another case records the version before it, the only way to exercise the update
    # for a project recording an older version.
    newest = versions()[-1][0]
    recorded = recorded_versions()
    assert newest in recorded.get(
        NEWEST_VERSION_CASE, set()
    ), f"{NEWEST_VERSION_CASE} must record the newest version, v{newest}"
    if newest >= 2:
        assert any(
            newest - 1 in found for found in recorded.values()
        ), f"no eval case records v{newest - 1}, one behind"


def test_a_new_version_replaces_the_one_behind_case_instead_of_adding_one() -> None:
    # Each version used to add a case beside the last, so the suite grew by one paid case per
    # version while every one of them tested the same offer. One case stays one behind; a new
    # version moves it (or replaces it) rather than leaving the old one in place.
    newest = versions()[-1][0]
    behind = {
        case: sorted(v for v in found if v < newest)
        for case, found in recorded_versions().items()
        if any(v < newest for v in found)
    }
    assert all(found == [newest - 1] for found in behind.values()), (
        f"eval cases behind the newest version, v{newest}: {behind}. Only one may stay, at "
        f"v{newest - 1}: move the one-behind case there and retire the others"
    )
    assert len(behind) <= 1, (
        f"more than one eval case records v{newest - 1}: {sorted(behind)}. A new version "
        "replaces the one-behind case rather than adding one"
    )


GUIDE = re.compile(r"^v(\d+)-to-current\.md$")
VERSION_NAMED = re.compile(r"\bv(\d+)\b")


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_one_upgrade_guide_per_older_version_each_covering_only_the_next() -> None:
    # A project follows its own version's guide and then every later one, and setup-project
    # adds up what they offer (SKILL.md -> *The update pass*). So a guide says only what the next
    # version gives a project at its own version: one naming a later version, or recording one,
    # restates a step another guide owns, and a new version would have to edit it.
    newest = versions()[-1][0]
    guides = {
        int(m.group(1)): p for p in UPGRADES.glob("*.md") if (m := GUIDE.match(p.name))
    }
    assert sorted(guides) == list(range(1, newest)), (
        f"{UPGRADES.relative_to(REPO_ROOT)} must hold v1-to-current.md … "
        f"v{newest - 1}-to-current.md and none for v{newest}; found "
        f"{sorted(p.name for p in guides.values())}"
    )
    for number, path in guides.items():
        text = path.read_text(encoding="utf-8")
        later = sorted(
            {int(v) for v in VERSION_NAMED.findall(text) if int(v) > number + 1}
        )
        assert not later, (
            f"{path.relative_to(REPO_ROOT)} must say only what v{number + 1} gives a project "
            f"at v{number}; it names v{later}. Later versions belong to their own guides"
        )
        assert not re.search(r"\brecord v\d+", text), (
            f"{path.relative_to(REPO_ROOT)} records a version; setup-project records the "
            "newest once every guide on the path has an answer"
        )


def test_shape_guides_load_whatever_version_is_recorded() -> None:
    # MOVE_TO_HARNESS.md and RESHAPE_NORTH_STAR.md repair a project's shape, so its shape loads
    # them. The move once loaded only with no version recorded or through v3-to-current.md, so a
    # pre-v4 project whose line had been advanced past v3 — a figure-out decline used to do it —
    # kept its feature map and surface README on every later run.
    skill = re.sub(
        r"\s+", " ", (SKILLS / "setup-project" / "SKILL.md").read_text("utf-8")
    )
    rows = re.findall(r"\| (none|the newest|vN[^|]*) \| ([^|]*) \|", skill)
    assert rows, "setup-project/SKILL.md lost the table of guides by recorded version"
    for version, loads in rows:
        for guide in ("MOVE_TO_HARNESS.md", "RESHAPE_NORTH_STAR.md"):
            assert guide not in loads, (
                f"the `{version}` row loads {guide}; a shape guide loads whatever version is "
                "recorded, from the sentence below the table"
            )
    sentence = re.search(
        r"Whatever version is recorded, the newest included, [^:]*", skill
    )
    assert sentence and "MOVE_TO_HARNESS.md" in sentence.group(
        0
    ), "MOVE_TO_HARNESS.md must load on the project's shape, whatever version is recorded"
    assert "RESHAPE_NORTH_STAR.md" in skill
    # The trigger lives in the loading layer: a deferred guide is read only after the load its
    # own trigger would gate (docs/adr/20260703-progressive-disclosure-triggers-live-in-loading-layer.md).
    move = (SKILLS / "setup-project/references/upgrades/MOVE_TO_HARNESS.md").read_text(
        "utf-8"
    )
    assert (
        "whatever version the project records" not in move
    ), "MOVE_TO_HARNESS.md restates its own load trigger; setup-project/SKILL.md owns it"


def test_setup_project_follows_every_guide_from_the_recorded_version_on() -> None:
    # The other half of the rule above: the loading layer walks the whole path and adds the
    # guides up, so no single guide has to take a project to the newest version.
    skill = re.sub(
        r"\s+", " ", (SKILLS / "setup-project" / "SKILL.md").read_text("utf-8")
    )
    assert (
        "`references/upgrades/vN-to-current.md`, then each later `vM-to-current.md`"
        in skill
    )
    assert "an item a later version replaces is not offered" in skill
