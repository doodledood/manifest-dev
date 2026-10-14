"""A change to what setup-project writes into projects must ship as a new surfaces version.

setup-project copies or emits a few files into every project it sets up. A project records
the surfaces version it carries in its context file, and a later update offers only the
changes listed in `CHANGES.md` after that version. So an edit to an emitted file that does
not add a version leaves every installed project unable to learn about it.

This test pins a digest of the emitted text to the latest version in `CHANGES.md`. HTML
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
    HARNESS / "harness.md",
    *sorted((HARNESS / "recipes").glob("*.md")),
)

HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
VERSION_HEADING = re.compile(r"^## v(\d+)\s*$", re.MULTILINE)
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
    """Each `CHANGES.md` entry as (version, body, digest), in file order."""
    text = CHANGES.read_text(encoding="utf-8")
    headings = list(VERSION_HEADING.finditer(text))
    assert headings, f"{CHANGES} lists no `## vN` entries"
    entries = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[heading.end() : end]
        digest = DIGEST_LINE.search(body)
        assert digest, f"{CHANGES} entry v{heading.group(1)} has no `Digest:` line"
        entries.append((int(heading.group(1)), body, digest.group(1)))
    return entries


def test_versions_count_up_from_one() -> None:
    numbers = [number for number, _, _ in versions()]
    assert numbers == list(
        range(1, len(numbers) + 1)
    ), f"{CHANGES} versions must run 1, 2, 3, … in order; found {numbers}"


# Holds the decision in docs/adr/20261013-set-up-projects-receive-updates-through-a-version-marker.md.
def test_every_version_says_what_projects_gain() -> None:
    for number, body, _ in versions():
        assert re.search(
            r"^- \S", body, re.MULTILINE
        ), f"{CHANGES} entry v{number} lists nothing an installed project gains"


# Holds the decision in docs/adr/20261013-runs-build-and-maintain-a-project-verification-surface.md.
# Holds the decision in docs/adr/20261013-set-up-projects-receive-updates-through-a-version-marker.md.
# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_latest_version_matches_what_setup_project_emits() -> None:
    latest_number, _, latest_digest = versions()[-1]
    current = emitted_digest()
    assert latest_digest == current, (
        f"A file setup-project emits into projects changed since surfaces v{latest_number}. "
        f"Add `## v{latest_number + 1}` to {CHANGES.relative_to(REPO_ROOT)} listing what an "
        f"installed project gains, with `Digest: {current}`, and set the version comment "
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


NEWEST_VERSION_CASE = "45-current-setup-offers-nothing"


# Holds the decision in docs/adr/20261014-setup-project-audits-the-whole-setup-when-run.md.
def test_eval_cases_track_the_newest_version() -> None:
    # The newest-version case is graded on no offer, so it records the newest version. From
    # v2 on, another case records the version before it, the only way to exercise the update
    # for a project recording an older version.
    newest = versions()[-1][0]
    recorded = {
        p.parent.name: {
            int(v) for v in TEMPLATE_VERSION.findall(p.read_text(encoding="utf-8"))
        }
        for p in EVALS.glob("*/scaffold.sh")
    }
    assert newest in recorded.get(
        NEWEST_VERSION_CASE, set()
    ), f"{NEWEST_VERSION_CASE} must record the newest version, v{newest}"
    if newest >= 2:
        assert any(
            newest - 1 in found for found in recorded.values()
        ), f"no eval case records v{newest - 1}, one behind"


GUIDE = re.compile(r"^v(\d+)-to-current\.md$")


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_one_upgrade_guide_per_older_version_each_to_the_newest() -> None:
    # Each guide takes a project straight to the newest version, so a new version updates
    # every guide: a guide still naming an older target would walk a project to a replaced shape.
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
        targets = set(re.findall(r"\bto v(\d+)\b", path.read_text(encoding="utf-8")))
        assert targets == {str(newest)}, (
            f"{path.relative_to(REPO_ROOT)} must upgrade v{number} to v{newest}, the newest; "
            f"it names {sorted(targets)}"
        )
