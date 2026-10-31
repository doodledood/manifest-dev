"""The setup update from surfaces v11 leaves no time line in a project's harness.

Holds the decision in docs/adr/20261031-time-lines-are-removed-and-run-time-is-only-reported.md:
an existing project strips its time lines through the v12 update. The update itself is a model
following `upgrades/v11-to-current.md`, so this test checks the two things a deterministic test
can: that the removals the guide names leave nothing behind in a real v11 harness carrying plain,
raised and frozen lines, and that the shipped tool fails `verify check` on any field the removals
miss. The project is the one-behind eval case's own scaffold, so the fixture and the behavior case
share one source.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCES = REPO_ROOT / "claude-plugins/manifest-dev/skills/setup-project/references"
SHIPPED_HARNESS = REFERENCES / "harness"
GUIDE = REFERENCES / "upgrades" / "v11-to-current.md"
SCAFFOLD = (
    REPO_ROOT / "claude-plugins/manifest-dev/evals/53-update-offer-from-v11/scaffold.sh"
)
TOOL_FILES = ("verify", "verify.mts")

if shutil.which("node") is None:
    pytest.fail("node is not on PATH; the verification tool needs Node 22.18 or newer")


def _guide_fields(part: str) -> list[str]:
    """The backticked `name:` fields one bullet of the guide's removal item names."""
    text = GUIDE.read_text(encoding="utf-8")
    bullet = re.search(rf"\*\*{part}:\*\*(.*?)(?=\n\s*- \*\*|\n\n)", text, re.S)
    assert bullet, f"{GUIDE.name} has no **{part}:** bullet in its removal item"
    return re.findall(r"`(\w[\w-]*):`", bullet.group(1))


def _verify(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(project / "scripts" / "verify"), *args],
        cwd=project,
        capture_output=True,
        text=True,
        env={k: v for k, v in os.environ.items() if not k.startswith("VERIFY_")},
    )


def _recipes_and_settings(project: Path) -> str:
    data = project / "verification"
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in [data / "harness.md", *sorted((data / "recipes").glob("*.md"))]
    )


@pytest.fixture
def project(tmp_path: Path) -> Path:
    subprocess.run(["bash", str(SCAFFOLD)], cwd=tmp_path, check=True)
    return tmp_path


def test_the_v11_project_starts_with_lines_of_every_kind(project: Path) -> None:
    before = _recipes_and_settings(project)
    assert re.search(r"^Line: [\d.]+ s on \S+$", before, re.M), "no plain line"
    assert re.search(r"^Line: .*; raised: ", before, re.M), "no raised line"
    assert re.search(
        r"^Line: .*; frozen at [\d.]+ s by ", before, re.M
    ), "no frozen line"
    assert re.search(r"^Workload: varies$", before, re.M), "no Workload field"
    assert re.search(r"^headroom: ", before, re.M) and re.search(
        r"^raise: ", before, re.M
    )
    tool = (project / "scripts" / "verify.mts").read_text(encoding="utf-8")
    assert "EXIT_OVER_LINE" in tool and 'case "freeze":' in tool, "not the v11 tool"


def test_the_guide_names_every_removed_field() -> None:
    assert set(_guide_fields("Recipe fields")) == {"Line", "Workload"}
    assert set(_guide_fields("Settings")) == {"headroom", "raise"}


def test_the_updated_tool_refuses_every_field_the_update_has_not_removed_yet(
    project: Path,
) -> None:
    for name in TOOL_FILES:
        shutil.copy2(SHIPPED_HARNESS / name, project / "scripts" / name)
    result = _verify(project, "check")
    assert result.returncode == 1, result.stdout + result.stderr
    for named in (
        "carries `Line: 0.4 s on linux-x64-4cpu`",
        "carries `Line: 0.6 s on linux-x64-4cpu; frozen at 0.9 s by #41`",
        "carries `Line: 3.1 s on linux-x64-4cpu; raised: tests for the CSV export`",
        "carries `Workload: varies`",
        "verification/harness.md: carries `headroom: 30%`",
    ):
        assert named in result.stdout, (named, result.stdout)


def test_the_removals_the_guide_names_leave_no_time_line(project: Path) -> None:
    # The tool update: the shipped tool over the project's own copy.
    for name in TOOL_FILES:
        shutil.copy2(SHIPPED_HARNESS / name, project / "scripts" / name)
    # Recipe fields and settings: each line the guide names, deleted, whatever follows it.
    scenario_fields = "|".join(_guide_fields("Recipe fields"))
    for recipe in (project / "verification" / "recipes").glob("*.md"):
        text = recipe.read_text(encoding="utf-8")
        recipe.write_text(
            re.sub(rf"^(?:{scenario_fields}):.*\n", "", text, flags=re.M), "utf-8"
        )
    settings = project / "verification" / "harness.md"
    keys = "|".join(_guide_fields("Settings"))
    settings.write_text(
        re.sub(rf"^(?:{keys}):.*\n", "", settings.read_text("utf-8"), flags=re.M),
        "utf-8",
    )

    checked = _verify(project, "check")
    assert checked.returncode == 0, checked.stdout + checked.stderr
    after = _recipes_and_settings(project)
    for left in (r"^Line:", r"^Workload:", r"^headroom:", r"^raise:", r"frozen at"):
        assert not re.search(left, after, re.M), left
    tool = (project / "scripts" / "verify.mts").read_text(encoding="utf-8")
    assert "EXIT_OVER_LINE" not in tool
    shown = _verify(project, "--help").stdout
    codes = shown[shown.index("Exit codes:") :].split("\n\n")[0]
    assert not re.search(r"\b5\b", codes), codes
    for command in ("line", "raise", "freeze"):
        gone = _verify(project, command, "project-checks", "tests", "why")
        assert gone.returncode == 2 and f"unknown command '{command}'" in gone.stderr
