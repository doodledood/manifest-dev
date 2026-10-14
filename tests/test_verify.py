"""This repository's verification harness stays sound.

`scripts/verify` reads one recipe per thing a user reaches or a reader relies on, from
`verification/recipes/`. A recipe that no longer parses, or names a path that moved, sends the
next run to nothing; a skill with no recipe cannot place a report about it; a walk pointing at a
renamed section cannot run. The tool itself is the one setup-project ships, so the two must not
drift apart.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFY = REPO_ROOT / "scripts" / "verify"
SHIPPED_HARNESS = (
    (REPO_ROOT / "claude-plugins" / "manifest-dev" / "skills" / "setup-project")
    / "references"
    / "harness"
)
# The tool is TypeScript that Node runs directly; `verify` is the shell entry that starts it.
TOOL_FILES = ("verify", "verify.mts")
NODE = shutil.which("node")
RECIPES = REPO_ROOT / "verification" / "recipes"
DRIVE = REPO_ROOT / "scripts" / "drive-skill.sh"
WALK = REPO_ROOT / "scripts" / "walk.sh"

INVOCABLE_FALSE = re.compile(r"^user-invocable:\s*false\s*$", re.MULTILINE)
SECTION = r"\*([^*\n]+)\*"
POINTER = re.compile(rf"`([\w./-]+\.(?:md|html))` → ({SECTION}(?: and {SECTION})*)")


def run_verify(
    *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    if NODE is None:
        pytest.fail(
            "node is not on PATH; the verification tool needs Node 22.18 or newer"
        )
    return subprocess.run(
        [str(VERIFY), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


def front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    block = text.split("---\n", 2)[1]
    return {
        key.strip(): value.strip()
        for key, _, value in (line.partition(":") for line in block.splitlines())
        if key.strip()
    }


def recipes_of_kind(kind: str) -> list[Path]:
    return [p for p in sorted(RECIPES.glob("*.md")) if front_matter(p)["kind"] == kind]


def user_invocable_skills() -> set[str]:
    marketplace = json.loads(
        (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    found = set()
    for plugin in marketplace["plugins"]:
        for skill in (REPO_ROOT / plugin["source"] / "skills").glob("*/SKILL.md"):
            frontmatter = skill.read_text(encoding="utf-8").split("---", 2)[1]
            if not INVOCABLE_FALSE.search(frontmatter):
                found.add(skill.parent.name)
    return found


# Holds the decision in docs/adr/20261013-runs-build-and-maintain-a-project-verification-surface.md.
def test_every_recipe_parses_and_names_only_existing_paths() -> None:
    result = run_verify("check")
    assert result.returncode == 0, result.stdout + result.stderr


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_every_user_invocable_skill_has_a_recipe() -> None:
    recipes = {p.stem for p in recipes_of_kind("skill")}
    skills = user_invocable_skills()
    assert not skills - recipes, (
        f"{sorted(skills - recipes)} can be invoked but have no `kind: skill` recipe in "
        f"{RECIPES.relative_to(REPO_ROOT)}"
    )
    assert (
        not recipes - skills
    ), f"{sorted(recipes - skills)} are `kind: skill` recipes naming no user-invocable skill"


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
@pytest.mark.parametrize("name", TOOL_FILES)
def test_this_repositorys_tool_is_the_shipped_one(name: str) -> None:
    assert (REPO_ROOT / "scripts" / name).read_bytes() == (
        SHIPPED_HARNESS / name
    ).read_bytes(), (
        f"scripts/{name} differs from the tool setup-project ships; change the shipped copy "
        "(with a new surfaces version) and copy it here"
    )


EVALS = REPO_ROOT / "claude-plugins" / "manifest-dev" / "evals"
EMBEDDED = re.compile(
    r"cat > scripts/(verify(?:\.mts)?) <<'VERIFY_TOOL_EOF'\n(.*?\n)VERIFY_TOOL_EOF\n",
    re.S,
)


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md: an eval case
# that seeds a harness seeds the tool a project would get, so a grade measures the shipped one.
@pytest.mark.parametrize(
    "scaffold",
    sorted(
        p
        for p in EVALS.rglob("scaffold.sh")
        if "VERIFY_TOOL_EOF" in p.read_text(encoding="utf-8")
    ),
    ids=lambda p: str(p.parent.relative_to(EVALS)),
)
def test_eval_scaffolds_seed_the_shipped_tool(scaffold: Path) -> None:
    embedded = dict(EMBEDDED.findall(scaffold.read_text(encoding="utf-8")))
    assert set(embedded) == set(TOOL_FILES), f"{scaffold} must write {TOOL_FILES}"
    for name, text in embedded.items():
        assert text == (SHIPPED_HARNESS / name).read_text(
            encoding="utf-8"
        ), f"{scaffold.relative_to(REPO_ROOT)} writes a {name} that differs from the shipped one"


def _path_with_node_version(tmp_path: Path, version: str | None) -> str:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    if version:
        stub = bin_dir / "node"
        stub.write_text(f"#!/bin/sh\necho {version}\n")
        stub.chmod(0o755)
    return str(bin_dir)


@pytest.mark.parametrize("version", ["v22.18.0", "v23.6.0", "v24.0.0"])
def test_the_entry_starts_the_tool_on_a_node_that_runs_it(
    tmp_path: Path, version: str
) -> None:
    # The stub reports the version, then hands the tool to it, standing in for that Node.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "node"
    stub.write_text(
        f'#!/bin/sh\n[ "$1" = --version ] && {{ echo {version}; exit 0; }}\necho "started $*"\n'
    )
    stub.chmod(0o755)
    result = subprocess.run(
        ["sh", str(VERIFY), "list"],
        capture_output=True,
        text=True,
        env={"PATH": f"{bin_dir}:/usr/bin:/bin"},
    )
    assert result.returncode == 0 and result.stdout.startswith(
        "started "
    ), result.stderr


@pytest.mark.parametrize("version", [None, "v20.11.0", "v22.17.1", "v23.5.0"])
def test_the_entry_names_the_node_it_needs(tmp_path: Path, version: str | None) -> None:
    # Without a Node that runs TypeScript, the entry stops as unreachable and says what to
    # install, rather than failing on the first line of TypeScript.
    result = subprocess.run(
        [str(VERIFY), "list"],
        capture_output=True,
        text=True,
        env={"PATH": _path_with_node_version(tmp_path, version)},
    )
    assert result.returncode == 3, result.stderr
    assert "Node 22.18 or newer" in result.stderr


def _has_section(path: Path, title: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        return f'data-name="{title}"' in text
    return bool(re.search(rf"^#+ {re.escape(title)}\s*$", text, re.MULTILINE))


# Holds the decision in docs/adr/20261013-runs-build-and-maintain-a-project-verification-surface.md.
@pytest.mark.parametrize("recipe", recipes_of_kind("walk"), ids=lambda p: p.stem)
def test_walk_points_at_sections_that_exist(recipe: Path) -> None:
    # A walk's *How a user reaches it* names its documents as `FILE` → *Section*, joined by
    # "; ", with further sections of one file as *A* and *B*; a site section is a `data-name`.
    text = recipe.read_text(encoding="utf-8")
    where = text.split("## How a user reaches it", 1)[1].split("\n## ", 1)[0].strip()
    broken = []
    for part in where.split("; "):
        pointer = POINTER.fullmatch(part)
        if not pointer:
            broken.append(f"not written `FILE` → *Section*: {part}")
            continue
        path = REPO_ROOT / pointer.group(1)
        if not path.is_file():
            broken.append(f"{pointer.group(1)} does not exist")
            continue
        for name in re.findall(SECTION, pointer.group(2)):
            if not _has_section(path, name):
                broken.append(f"{pointer.group(1)} has no section *{name}*")
    assert not broken, "\n".join(broken)


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_ask_first_recipe_is_refused_without_yes() -> None:
    marked = [
        p for p in sorted(RECIPES.glob("*.md")) if front_matter(p).get("ask-first")
    ]
    assert marked, "no ask-first recipe to test against"
    result = run_verify("drive", marked[0].stem)
    assert result.returncode == 4 and "ask-first" in result.stderr, result.stderr


def _harness(
    tmp_path: Path,
    history: str,
    scenarios: str = "### once\nRun: `true`\nProves: it runs.\n",
) -> dict[str, str]:
    data = tmp_path / "verification"
    (data / "recipes").mkdir(parents=True)
    (data / "recipes" / "thing.md").write_text(
        "---\nkind: feature\n---\n# Thing\n\nDoes a thing.\n\n## Scenarios\n\n"
        + scenarios,
        encoding="utf-8",
    )
    if history:
        _evidence(tmp_path, "20260101T000000Z", history)
    return {**os.environ, "VERIFY_ROOT": str(tmp_path), "VERIFY_DATA": str(data)}


def _evidence(tmp_path: Path, stamp: str, text: str) -> Path:
    folder = tmp_path / "verification" / "evidence" / "thing"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stamp}.md"
    path.write_text(text, encoding="utf-8")
    return path


TWO_SCENARIOS = "### one\nRun: `true`\n\n### two\nRun: `true`\n"


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_runs_from_one_second_keep_the_order_they_were_written_in(
    tmp_path: Path,
) -> None:
    # One drive writes STAMP.md, STAMP-2.md, … ; a directory listing orders -10 before -2 and
    # may order them any way at all.
    env = _harness(tmp_path, "", TWO_SCENARIOS)
    for n in range(1, 11):
        _evidence(
            tmp_path,
            "20260101T000000Z" if n == 1 else f"20260101T000000Z-{n}",
            "- **Scenario:** one\n- **Outcome:** "
            + ("failed" if n == 10 else "verified")
            + "\n",
        )
    _evidence(
        tmp_path,
        "20260101T000000Z-11",
        "- **Scenario:** two\n- **Outcome:** verified\n",
    )
    listed = run_verify("list", env=env)
    assert "failed (2026-01-01)" in listed.stdout, listed.stdout + listed.stderr


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_a_recipe_shows_the_worst_of_its_scenarios_latest_runs(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", TWO_SCENARIOS)
    _evidence(
        tmp_path, "20260101T000000Z", "- **Scenario:** one\n- **Outcome:** failed\n"
    )
    _evidence(
        tmp_path, "20260102T000000Z", "- **Scenario:** two\n- **Outcome:** verified\n"
    )
    assert "failed (2026-01-01)" in run_verify("list", env=env).stdout
    _evidence(
        tmp_path, "20260103T000000Z", "- **Scenario:** one\n- **Outcome:** verified\n"
    )
    # Every scenario passed; the date is the weakest proof's.
    assert "verified (2026-01-02)" in run_verify("list", env=env).stdout


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
@pytest.mark.parametrize(
    ("history", "expected"),
    [
        ("", "unverified"),
        ("- **Outcome:** verified\n", "verified (2026-01-01)"),
        ("- **Outcome:** failed\n", "failed (2026-01-01)"),
        ("# no outcome line\n", "unjudged (2026-01-01)"),
    ],
)
def test_status_follows_evidence(tmp_path: Path, history: str, expected: str) -> None:
    result = run_verify("list", env=_harness(tmp_path, history))
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout, result.stdout


def _git(repo: Path, *args: str, when: str = "2026-01-02T00:00:00Z") -> None:
    # Commit times have one-second resolution; pinning them keeps two commits in one test
    # from sharing a second.
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t", *args],
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when},
    )


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_status_goes_stale_when_covered_files_change_after_the_evidence(
    tmp_path: Path,
) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ncovers: src.txt\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "src.txt").write_text("one\n", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "change and its evidence")
    fresh = run_verify("list", env=env)
    assert "verified (2026-01-01)" in fresh.stdout, fresh.stdout + fresh.stderr

    (tmp_path / "src.txt").write_text("two\n", encoding="utf-8")
    edited = run_verify("list", env=env)
    assert "stale (" in edited.stdout, edited.stdout

    # Evidence newer than an uncommitted edit is fresh: the edit counts from its own time.
    os.utime(tmp_path / "src.txt", (1767225600, 1767225600))  # 2026-01-01T00:00:00Z
    _evidence(tmp_path, "20260101T000001Z", "- **Outcome:** verified\n")
    rerun = run_verify("list", env=env)
    assert "verified (2026-01-01)" in rerun.stdout, rerun.stdout

    _git(tmp_path, "commit", "-qam", "a later change", when="2026-01-03T00:00:00Z")
    committed = run_verify("list", env=env)
    assert "stale (" in committed.stdout, committed.stdout


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_a_drift_line_marks_the_recipe_stale(tmp_path: Path) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8")
        + "\nDrift (2099-01-01): the command takes a flag now.\n",
        encoding="utf-8",
    )
    shown = run_verify("help", "thing", env=env)
    assert "stale (2099-01-01): the command takes a flag now." in shown.stdout
    listed = run_verify("list", env=env)
    assert "stale (2099-01-01)" in listed.stdout and "flag" not in listed.stdout


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
@pytest.mark.parametrize(
    ("scenario", "outcome", "code"),
    [
        ("Run: `true`\n", "verified", 0),
        ("Run: `exit 1`\n", "failed", 1),
        ("Run: `exit 3`\n", "unreachable", 1),
        ("Run: `true`\nCheck: read\n", "unjudged", 0),
    ],
)
def test_a_drive_keeps_evidence_that_reads_back_as_its_outcome(
    tmp_path: Path, scenario: str, outcome: str, code: int
) -> None:
    env = {
        **_harness(tmp_path, "", f"### once\n{scenario}"),
        "VERIFY_STAMP": "20260101T000000Z",
    }
    result = run_verify("drive", "thing", env=env)
    assert result.returncode == code, result.stdout + result.stderr
    kept = (
        tmp_path / "verification" / "evidence" / "thing" / "20260101T000000Z.md"
    ).read_text(encoding="utf-8")
    assert f"- **Outcome:** {outcome}\n" in kept and "- **Scenario:** once\n" in kept
    assert f"{outcome} (2026-01-01)" in run_verify("list", env=env).stdout


def test_kept_output_carries_no_local_paths(tmp_path: Path) -> None:
    env = _harness(
        tmp_path, "", "### once\nRun: `echo /Users/someone/secret ~/x /tmp/y`\n"
    )
    assert run_verify("drive", "thing", env=env).returncode == 0
    (kept,) = (tmp_path / "verification" / "evidence" / "thing").iterdir()
    text = kept.read_text(encoding="utf-8").split("## Output", 1)[1]
    assert "/Users" not in text and "~/x" not in text and "/tmp/y" not in text, text
    assert text.count("[local path]") == 3


def test_a_scenario_that_never_ran_leaves_the_recipe_unverified(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### one\nRun: `true`\n\n### two\nRun: `false`\n")
    assert run_verify("drive", "thing", "one", env=env).returncode == 0
    assert "unverified (" in run_verify("list", env=env).stdout
    shown = run_verify("help", "thing", env=env).stdout
    assert "no run yet for two" in shown, shown


def test_runs_in_one_second_get_their_own_evidence(tmp_path: Path) -> None:
    env = {
        **_harness(tmp_path, "", "### once\nRun: `true`\n"),
        "VERIFY_STAMP": "20260101T000000Z",
    }
    for _ in range(2):
        assert run_verify("drive", "thing", env=env).returncode == 0
    made = sorted(
        p.name for p in (tmp_path / "verification" / "evidence" / "thing").iterdir()
    )
    assert made == ["20260101T000000Z-2.md", "20260101T000000Z.md"], made


@pytest.mark.parametrize("has_outcome", [True, False])
def test_judge_records_one_verdict(tmp_path: Path, has_outcome: bool) -> None:
    env = _harness(tmp_path, "")
    lines = "- **Scenario:** once\n" + (
        "- **Outcome:** unjudged\n" if has_outcome else ""
    )
    path = _evidence(
        tmp_path, "20260101T000000Z", f"# thing / once\n\n{lines}\n## Output\n\nok\n"
    )
    result = run_verify(
        "judge", "thing", "20260101T000000Z", "verified", "read", "it", env=env
    )
    assert result.returncode == 0, result.stderr
    text = path.read_text(encoding="utf-8")
    assert text.count("- **Outcome:**") == 1 and "- **Outcome:** verified" in text
    assert text.endswith("## Verdict\n\nverified: read it\n")
    assert "verified (2026-01-01)" in run_verify("list", env=env).stdout


@pytest.mark.parametrize(
    ("recipe", "evidence", "problem"),
    [
        (
            "---\nkind: feature\ncovers: missing.txt\n---\n# T\n",
            "",
            "covers missing.txt",
        ),
        (
            "---\nkind: feature\n---\n# T\n\n## Scenarios\n\n### a\nRun: `src/nope.sh`\n",
            "",
            "names src/nope.sh",
        ),
        (
            "---\nkind: feature\n---\n# T\n\n## Scenarios\n\n### a\nRun: `true`\n",
            "- **Scenario:** ghost\n",
            "'ghost' is not in",
        ),
        ("---\ncovers: src\n---\n# T\n", "", "no `kind:`"),
    ],
)
def test_check_reports_what_would_send_a_run_to_nothing(
    tmp_path: Path, recipe: str, evidence: str, problem: str
) -> None:
    env = _harness(tmp_path, "")
    (tmp_path / "src").mkdir()
    (tmp_path / "verification" / "recipes" / "thing.md").write_text(
        recipe, encoding="utf-8"
    )
    if evidence:
        _evidence(tmp_path, "20260101T000000Z", evidence)
    result = run_verify("check", env=env)
    assert result.returncode == 1 and problem in result.stdout, result.stdout


def test_detail_beside_the_summaries_is_kept_and_a_misnamed_summary_reported(
    tmp_path: Path,
) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n")
    folder = tmp_path / "verification" / "evidence" / "thing"
    (folder / "transcript.md").write_text("what the session said\n", encoding="utf-8")
    assert "verified (2026-01-01)" in run_verify("list", env=env).stdout
    assert run_verify("check", env=env).returncode == 0
    (folder / "browser-run.md").write_text("- **Outcome:** failed\n", encoding="utf-8")
    assert "verified (2026-01-01)" in run_verify("list", env=env).stdout
    result = run_verify("check", env=env)
    assert (
        result.returncode == 1
        and "browser-run.md: reads as a run summary" in result.stdout
    )


def test_check_leaves_a_directory_a_run_creates_alone(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### a\nRun: `mkdir -p out && touch out/new.txt`\n")
    result = run_verify("check", env=env)
    assert result.returncode == 0, result.stdout


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_evidence_after_a_drift_line_clears_it(tmp_path: Path) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8")
        + "\nDrift (2025-11-30): older.\nDrift (2025-12-31): newer.\n",
        encoding="utf-8",
    )
    assert "verified (2026-01-01)" in run_verify("list", env=env).stdout
    _evidence(tmp_path, "20251201T000000Z", "- **Outcome:** verified\n")
    (tmp_path / "verification" / "evidence" / "thing" / "20260101T000000Z.md").unlink()
    shown = run_verify("help", "thing", env=env).stdout
    assert "stale (2025-12-31): newer." in shown, shown


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_an_edit_after_the_run_stays_stale_however_it_is_committed(
    tmp_path: Path,
) -> None:
    env = _harness(tmp_path, "", "### once\nRun: `true`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ncovers: src.txt\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "src.txt").write_text("one\n", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    assert run_verify("drive", "thing", env=env).returncode == 0
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "change and its evidence")
    assert "verified (" in run_verify("list", env=env).stdout

    assert run_verify("drive", "thing", env=env).returncode == 0
    (tmp_path / "src.txt").write_text("two\n", encoding="utf-8")
    _git(
        tmp_path, "add", "-A"
    )  # the edit and the evidence of the run before it, together
    _git(
        tmp_path,
        "commit",
        "-qm",
        "edit committed with older evidence",
        when="2099-01-01T00:00:00Z",
    )
    listed = run_verify("list", env=env).stdout
    assert "stale (" in listed, listed


def test_an_interrupted_run_keeps_no_evidence(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### slow\nRun: `sleep 5`\n")
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    folder = tmp_path / "verification" / "evidence" / "thing"
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith(
        "running [slow]"
    )  # the command has started
    os.killpg(drive.pid, signal.SIGINT)  # Ctrl-C reaches the whole foreground group
    _, err = drive.communicate(timeout=10)
    assert drive.returncode == 130, err
    assert not list(folder.iterdir()), "an interrupted run left evidence behind"


@pytest.mark.parametrize("when", ["before the command", "while it runs"])
def test_a_signal_at_any_point_keeps_no_evidence(tmp_path: Path, when: str) -> None:
    # A large covered tree keeps the run busy hashing before the command starts.
    env = _harness(tmp_path, "", "### slow\nRun: `sleep 5`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ncovers: big\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "big").mkdir()
    for i in range(400):
        (tmp_path / "big" / f"{i}.txt").write_bytes(b"x" * 50_000)
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    folder = tmp_path / "verification" / "evidence" / "thing"
    if when == "before the command":
        deadline = time.monotonic() + 10
        while (
            not (folder.is_dir() and any(folder.iterdir()))
            and time.monotonic() < deadline
        ):
            time.sleep(0.005)
    else:
        assert drive.stdout is not None and drive.stdout.readline().startswith(
            b"running"
        )
    drive.send_signal(signal.SIGTERM)  # to the tool alone, as a process manager would
    started = time.monotonic()
    drive.communicate(timeout=10)
    assert drive.returncode == 130
    assert time.monotonic() - started < 4, "the signal did not reach the command"
    assert not list(folder.iterdir()), "an interrupted run left evidence behind"


def test_a_second_signal_stops_what_the_command_started(tmp_path: Path) -> None:
    env = _harness(
        tmp_path, "", "### stubborn\nRun: `trap '' INT TERM; sleep 8; echo finished`\n"
    )
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert drive.stdout is not None and drive.stdout.readline().startswith(b"running")
    time.sleep(0.3)
    drive.send_signal(signal.SIGINT)
    time.sleep(0.3)
    drive.send_signal(signal.SIGINT)
    started = time.monotonic()
    out, _ = drive.communicate(timeout=10)
    assert drive.returncode == 130 and b"finished" not in out
    assert time.monotonic() - started < 4


def test_a_command_that_dies_by_its_own_signal_failed(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### crash\nRun: `kill -ABRT $$`\n")
    result = run_verify("drive", "thing", env=env)
    assert result.returncode == 1, result.stdout + result.stderr
    (kept,) = (tmp_path / "verification" / "evidence" / "thing").iterdir()
    text = kept.read_text(encoding="utf-8")
    assert "- **Outcome:** failed\n" in text and "- **Exit code:** 134\n" in text, text


def test_a_reader_that_goes_away_still_leaves_whole_evidence(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### loud\nRun: `seq 1 20000`\n")
    piped = subprocess.run(
        f"'{VERIFY}' drive thing | head -n1",
        shell=True,
        env=env,
        capture_output=True,
        text=True,
    )
    assert piped.stdout.startswith("running"), piped.stderr
    (kept,) = (tmp_path / "verification" / "evidence" / "thing").iterdir()
    text = kept.read_text(encoding="utf-8")
    assert "- **Outcome:** verified\n" in text and "\n20000\n" in text


@pytest.mark.parametrize(
    ("setting", "args", "code"),
    [("ask", ("--yes",), 0), ("run", (), 0), ("maybe", (), 1)],
)
def test_an_ask_first_recipe_runs_when_agreed_or_allowed(
    tmp_path: Path, setting: str, args: tuple[str, ...], code: int
) -> None:
    env = _harness(tmp_path, "", "### once\nRun: `true`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\nask-first: costs money\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "verification" / "harness.md").write_text(
        f"---\nask-first: {setting}\n---\n", encoding="utf-8"
    )
    result = run_verify("drive", "thing", *args, env=env)
    assert result.returncode == code, result.stdout + result.stderr
    if code == 0:
        assert "verified (" in run_verify("list", env=env).stdout
    else:
        assert "must be `ask` or `run`" in result.stderr


def test_ignored_files_do_not_make_evidence_stale(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### once\nRun: `true`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ncovers: src\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.txt").write_text("a\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (tmp_path / "src" / "link").symlink_to("a.txt")
    _git(tmp_path, "init", "-q")
    assert run_verify("drive", "thing", env=env).returncode == 0
    (tmp_path / "src" / "x.log").write_text("noise\n", encoding="utf-8")
    assert "verified (" in run_verify("list", env=env).stdout
    (tmp_path / "src" / "new.txt").write_text("new\n", encoding="utf-8")
    assert "stale (" in run_verify("list", env=env).stdout


def test_outside_a_repository_an_edit_still_makes_evidence_stale(
    tmp_path: Path,
) -> None:
    env = _harness(tmp_path, "", "### once\nRun: `true`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ncovers: src.txt\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "src.txt").write_text("one\n", encoding="utf-8")
    assert run_verify("drive", "thing", env=env).returncode == 0
    assert "verified (" in run_verify("list", env=env).stdout
    (tmp_path / "src.txt").write_text("two\n", encoding="utf-8")
    assert "stale (" in run_verify("list", env=env).stdout


@pytest.mark.parametrize(
    ("evidence", "shows"),
    [
        (
            [
                ("20260101T000000Z", "one", "unjudged"),
                ("20260101T000001Z", "two", "unreachable"),
            ],
            "unreachable (2026-01-01)",
        ),
        (
            [
                ("20260101T000000Z", "", "verified"),
                ("20260102T000000Z", "one", "failed"),
            ],
            "failed (2026-01-02)",
        ),
        (
            [
                ("20260101T000000Z", "", "verified"),
                ("20260102T000000Z", "ghost", "failed"),
            ],
            "verified (2026-01-01)",
        ),
    ],
)
def test_a_recipe_shows_the_worst_of_its_scenarios(
    tmp_path: Path, evidence: list[tuple[str, str, str]], shows: str
) -> None:
    env = _harness(tmp_path, "", "### one\nRun: `true`\n\n### two\nRun: `true`\n")
    for stamp, scenario, outcome in evidence:
        line = f"- **Scenario:** {scenario}\n" if scenario else ""
        _evidence(tmp_path, stamp, f"# x\n\n{line}- **Outcome:** {outcome}\n")
    assert shows in run_verify("list", env=env).stdout


@pytest.mark.parametrize(
    "args",
    [
        ("list", "a", "b"),
        ("drive", "thing", "--bogus"),
        ("judge", "thing", "x", "maybe"),
    ],
)
def test_usage_errors_exit_2(tmp_path: Path, args: tuple[str, ...]) -> None:
    env = _harness(tmp_path, "")
    assert run_verify(*args, env=env).returncode == 2


def test_output_that_is_not_utf8_is_still_kept(tmp_path: Path) -> None:
    env = _harness(tmp_path, "", "### bytes\nRun: `printf 'a\\377b'`\n")
    # The command's own output passes through as bytes; only the kept copy is decoded.
    result = subprocess.run(
        [str(VERIFY), "drive", "thing"], capture_output=True, env=env
    )
    assert result.returncode == 0, result.stderr
    assert b"a\xffb" in result.stdout
    assert "verified (" in run_verify("list", env=env).stdout


def test_an_empty_evidence_file_is_reported_and_proves_nothing(tmp_path: Path) -> None:
    env = _harness(tmp_path, "")
    _evidence(tmp_path, "20260101T000000Z", "")
    assert "unverified" in run_verify("list", env=env).stdout
    checked = run_verify("check", env=env)
    assert checked.returncode == 1 and "empty" in checked.stdout, checked.stdout


def test_runner_scripts_parse() -> None:
    # A broken runner fails here, not in the first run that needs it.
    for script in (DRIVE, WALK):
        result = subprocess.run(
            ["bash", "-n", str(script)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{script.name}: {result.stderr}"


# No docker on PATH: a dry run that tried to start anything would fail. Node stays reachable for
# the tool itself.
DRY_ENV = {
    "PATH": ":".join(([str(Path(NODE).parent)] if NODE else []) + ["/usr/bin", "/bin"]),
    "HOME": "/nonexistent-home",
}


@pytest.mark.parametrize(
    ("credentials", "named"),
    [
        (
            {"CLAUDE_CODE_OAUTH_TOKEN": "tok", "ANTHROPIC_API_KEY": "key"},
            "CLAUDE_CODE_OAUTH_TOKEN",
        ),
        ({"ANTHROPIC_API_KEY": "key"}, "ANTHROPIC_API_KEY"),
        ({}, "none found"),
    ],
)
def test_drive_dry_run_names_container_credential_and_evidence(
    credentials: dict[str, str], named: str
) -> None:
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md"), "--dry-run"],
        capture_output=True,
        text=True,
        env={**DRY_ENV, **credentials},
    )
    assert result.returncode == 0, result.stderr
    assert "docker run" in result.stdout and "--plugin-dir" in result.stdout
    # Without an init process, the container ignores the signal that should stop the session.
    assert "--init -e TINI_KILL_PROCESS_GROUP=1" in result.stdout
    assert f"credential:  {named}" in result.stdout, result.stdout
    assert "verification/evidence/figure-out/" in result.stdout
    assert "tok" not in result.stdout.replace("CLAUDE_CODE_OAUTH_TOKEN", "")


def test_walk_dry_run_names_container_and_credential() -> None:
    result = subprocess.run(
        [str(WALK), "Find the install steps.", "README.md", "--dry-run"],
        capture_output=True,
        text=True,
        env={**DRY_ENV, "ANTHROPIC_API_KEY": "key"},
    )
    assert result.returncode == 0, result.stderr
    assert "docker run" in result.stdout and '--tools ""' in result.stdout
    assert "--init -e TINI_KILL_PROCESS_GROUP=1" in result.stdout
    assert "credential: ANTHROPIC_API_KEY" in result.stdout


@pytest.mark.parametrize(
    ("kind", "recipe"),
    [("skill", "figure-out"), ("walk", recipes_of_kind("walk")[0].stem)],
)
def test_verify_dry_run_reaches_the_runner_and_writes_no_evidence(
    kind: str, recipe: str
) -> None:
    evidence = REPO_ROOT / "verification" / "evidence" / recipe
    before = sorted(evidence.glob("*.md")) if evidence.is_dir() else []
    command = "drive" if kind == "skill" else "walk"
    result = run_verify(
        command, recipe, "--dry-run", env={**DRY_ENV, "ANTHROPIC_API_KEY": "k"}
    )
    assert result.returncode == 0, result.stderr
    assert "would run" in result.stdout and "docker run" in result.stdout, result.stdout
    after = sorted(evidence.glob("*.md")) if evidence.is_dir() else []
    assert before == after


def test_drive_refuses_a_feature_with_no_recipe() -> None:
    result = subprocess.run(
        [str(DRIVE), "no-such-feature", str(RECIPES / "figure-out.md"), "--dry-run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0 and "no recipe" in result.stderr


def _stub_docker(tmp_path: Path, transcript: str = "") -> Path:
    # Answers every docker call with success; `docker run` writes the given transcript into the
    # directory mounted at /out, standing in for the session.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (tmp_path / "transcript.jsonl").write_text(transcript, encoding="utf-8")
    stub = bin_dir / "docker"
    stub.write_text(
        "#!/bin/sh\n"
        '[ "$1" = run ] || exit 0\n'
        'while [ $# -gt 0 ]; do case "$1" in *:/out) out="${1%:/out}";; esac; shift; done\n'
        f'cp "{tmp_path / "transcript.jsonl"}" "$out/transcript.jsonl"\n'
    )
    stub.chmod(0o755)
    return bin_dir


INIT = {
    "type": "system",
    "subtype": "init",
    "model": "m",
    "plugins": [{"name": "manifest-dev"}],
}


def _drive_with(
    tmp_path: Path, transcript: str, prompt: str = "go\n"
) -> subprocess.CompletedProcess[str]:
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    return subprocess.run(
        [str(DRIVE), "figure-out", str(prompt_file)],
        env={
            "PATH": f"{_stub_docker(tmp_path, transcript)}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "ANTHROPIC_API_KEY": "test-key",
            "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
            "DRIVE_STAMP": "20990101T000000Z",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize(
    ("events", "says"),
    [
        ([{"type": "assistant"}], "no init event"),
        ([{**INIT, "skills": ["manifest-dev:define"]}], "did not load"),
    ],
)
def test_a_session_that_did_not_load_the_skill_is_unreachable(
    tmp_path: Path, events: list[dict[str, object]], says: str
) -> None:
    result = _drive_with(tmp_path, "".join(json.dumps(e) + "\n" for e in events))
    assert result.returncode == 3 and says in result.stderr, result.stderr


def test_a_prompt_with_front_matter_sends_only_its_body(tmp_path: Path) -> None:
    events = [
        {**INIT, "skills": ["manifest-dev:figure-out"]},
        {"type": "result", "num_turns": 1, "result": "done"},
    ]
    result = _drive_with(
        tmp_path,
        "".join(json.dumps(e) + "\n" for e in events),
        "---\ntags: a\n---\nthe body\n",
    )
    assert result.returncode == 0, result.stderr
    sent = (
        tmp_path / "store" / "figure-out" / "20990101T000000Z" / "prompt.md"
    ).read_text(encoding="utf-8")
    assert sent == "the body\n"


def test_drive_never_reuses_an_evidence_directory(tmp_path: Path) -> None:
    # Two drives of one feature started in the same second once shared a directory and
    # interleaved their transcripts. Start two at once with the stamp pinned and a stub `docker`
    # that does nothing, and require two distinct evidence directories.
    bin_dir = _stub_docker(tmp_path)
    store = tmp_path / "store"
    env = {
        "PATH": f"{bin_dir}:/usr/bin:/bin",
        "HOME": str(tmp_path),
        "ANTHROPIC_API_KEY": "test-key",
        "MANIFEST_DEV_FEATURES_EVIDENCE": str(store),
        "DRIVE_STAMP": "20990101T000000Z",
    }
    drives = [
        subprocess.Popen(
            [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for _ in range(2)
    ]
    try:
        for drive in drives:
            drive.communicate(timeout=60)
    finally:
        for drive in drives:
            drive.kill()
            drive.wait()
    made = sorted(p.name for p in (store / "figure-out").iterdir())
    assert made == ["20990101T000000Z", "20990101T000000Z-2"], made


def test_drive_reports_a_session_that_never_started_as_unreachable(
    tmp_path: Path,
) -> None:
    # `verify` records exit 3 as unreachable; a drive that produced no session is never a failure
    # of the skill.
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
        env={
            "PATH": f"{_stub_docker(tmp_path)}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "ANTHROPIC_API_KEY": "test-key",
            "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 3 and "unreachable" in result.stderr, result.stderr


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_drive_fails_fast_when_it_cannot_create_evidence(tmp_path: Path) -> None:
    # Only "another drive holds this directory" may be retried; any other failure stops loudly.
    bin_dir = _stub_docker(tmp_path)
    store = tmp_path / "store"
    (store / "figure-out").mkdir(parents=True)
    (store / "figure-out").chmod(0o555)
    try:
        result = subprocess.run(
            [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
            env={
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "HOME": str(tmp_path),
                "ANTHROPIC_API_KEY": "test-key",
                "MANIFEST_DEV_FEATURES_EVIDENCE": str(store),
                "DRIVE_STAMP": "20990101T000000Z",
            },
            capture_output=True,
            text=True,
            timeout=30,
        )
    finally:
        (store / "figure-out").chmod(0o755)
    assert result.returncode != 0 and "cannot create" in result.stderr, result.stderr


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
@pytest.mark.parametrize(
    ("doctor", "code", "last_line"),
    [("true", 0, "doctor: ok"), ("false", 1, "doctor: not ready")],
)
def test_doctor_runs_the_settings_health_command(
    tmp_path: Path, doctor: str, code: int, last_line: str
) -> None:
    env = _harness(tmp_path, "")
    (tmp_path / "verification" / "harness.md").write_text(
        f"---\nask-first: ask\ndoctor: {doctor}\n---\n", encoding="utf-8"
    )
    result = run_verify("doctor", env=env)
    assert result.returncode == code, result.stdout + result.stderr
    assert result.stdout.strip().splitlines()[-1] == last_line


def _covering(tmp_path: Path, run: str, covers: str) -> dict[str, str]:
    env = _harness(tmp_path, "", f"### once\nRun: `{run}`\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", f"kind: feature\ncovers: {covers}\n"
        ),
        encoding="utf-8",
    )
    return env


@pytest.mark.parametrize("in_repo", [True, False])
def test_links_under_covers_count_by_their_target(
    tmp_path: Path, in_repo: bool
) -> None:
    env = _covering(tmp_path, "true", "src")
    (tmp_path / "src" / "dir").mkdir(parents=True)
    (tmp_path / "src" / "to-dir").symlink_to("dir")
    (tmp_path / "src" / "dangling").symlink_to("nowhere")
    if in_repo:
        _git(tmp_path, "init", "-q")
    drove = run_verify("drive", "thing", env=env)
    assert drove.returncode == 0, drove.stdout + drove.stderr
    assert "verified (" in run_verify("list", env=env).stdout
    (tmp_path / "src" / "dangling").unlink()
    (tmp_path / "src" / "dangling").symlink_to("elsewhere")
    assert "stale (" in run_verify("list", env=env).stdout


def test_a_link_to_a_directory_counts_by_its_target_not_its_contents(
    tmp_path: Path,
) -> None:
    env = _covering(tmp_path, "true", "src")
    for name in ("one", "two"):
        (tmp_path / "src" / name).mkdir(parents=True)
        (tmp_path / "src" / name / "same.txt").write_text("x\n", encoding="utf-8")
    (tmp_path / "src" / "to-dir").symlink_to("one")
    assert run_verify("drive", "thing", env=env).returncode == 0
    (tmp_path / "src" / "to-dir").unlink()
    (tmp_path / "src" / "to-dir").symlink_to("two")  # same contents, new target
    assert "stale (" in run_verify("list", env=env).stdout


def test_a_command_never_outlives_a_killed_tool(tmp_path: Path) -> None:
    marker = tmp_path / "finished"
    env = _covering(tmp_path, f"sleep 4; touch {marker}", "verification/recipes")
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    time.sleep(0.5)  # the line prints just before the command starts
    drive.kill()  # SIGKILL: no handler runs, as when a timeout kills the tool
    drive.wait(timeout=10)
    time.sleep(6)
    assert not marker.exists(), "the command kept running after the tool was killed"


@pytest.mark.parametrize("sig", [signal.SIGHUP, signal.SIGQUIT])
def test_a_closed_terminal_stops_the_run_and_keeps_no_evidence(
    tmp_path: Path, sig: signal.Signals
) -> None:
    marker = tmp_path / "finished"
    env = _covering(tmp_path, f"sleep 2; touch {marker}", "verification/recipes")
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    drive.send_signal(sig)  # to the tool alone; it passes the signal on
    _, err = drive.communicate(timeout=10)
    assert drive.returncode == 130, err
    time.sleep(3)
    assert not marker.exists()
    assert not list((tmp_path / "verification" / "evidence" / "thing").iterdir())


def test_an_interrupted_dry_run_stops(tmp_path: Path) -> None:
    marker = tmp_path / "second"
    env = _harness(
        tmp_path,
        "",
        f"### one\nRun: `sleep 2`\n\n### two\nRun: `touch {marker}`\n",
    )
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "kind: feature\n", "kind: feature\ndry-run: honored\n"
        ),
        encoding="utf-8",
    )
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing", "--dry-run"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("would run [one]")
    time.sleep(0.5)
    os.killpg(drive.pid, signal.SIGINT)
    drive.communicate(timeout=10)
    assert drive.returncode == 130
    assert not marker.exists()


def test_a_command_that_kills_its_own_group_is_failed(tmp_path: Path) -> None:
    env = _covering(tmp_path, "kill -TERM 0", "verification/recipes")
    result = run_verify("drive", "thing", env=env)
    assert result.returncode == 1, result.stdout + result.stderr
    (evidence,) = (tmp_path / "verification" / "evidence" / "thing").iterdir()
    text = evidence.read_text(encoding="utf-8")
    assert "- **Exit code:** 143" in text and "- **Outcome:** failed" in text


def test_one_ctrl_c_stops_a_background_job_too(tmp_path: Path) -> None:
    marker = tmp_path / "background"
    env = _covering(
        tmp_path, f"(sleep 3; touch {marker}) & sleep 3", "verification/recipes"
    )
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    time.sleep(0.5)
    started = time.monotonic()
    os.killpg(drive.pid, signal.SIGINT)  # a background job ignores this one
    drive.communicate(timeout=10)
    assert drive.returncode == 130
    assert time.monotonic() - started < 2, "the run waited on the background job"
    time.sleep(3)
    assert not marker.exists()


def test_a_killed_tool_stops_its_command_before_anyone_reaps_it(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "finished"
    env = _covering(tmp_path, f"sleep 4; touch {marker}", "verification/recipes")
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    time.sleep(0.5)
    os.kill(drive.pid, signal.SIGKILL)  # left a zombie: not waited for until the end
    time.sleep(6)
    assert not marker.exists(), "the command ran on while its tool was a zombie"
    drive.wait(timeout=10)


def test_help_shows_whole_recipe_evidence_under_each_scenario(tmp_path: Path) -> None:
    env = _harness(
        tmp_path,
        "- **Outcome:** verified\n",
        "### one\nRun: `true`\n\n### two\nRun: `true`\n",
    )
    shown = run_verify("help", "thing", env=env).stdout
    assert "one: verified, verification/evidence/thing/20260101T000000Z.md" in shown
    assert "two: verified, verification/evidence/thing/20260101T000000Z.md" in shown


def test_a_drift_line_kept_as_a_list_item_still_marks_the_recipe_stale(
    tmp_path: Path,
) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n")
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8")
        + "\n## Traps\n\n- Drift (2099-01-01): the export now writes JSON\n",
        encoding="utf-8",
    )
    assert "stale (2099-01-01)" in run_verify("list", env=env).stdout


@pytest.mark.parametrize(("sent", "code"), [("INT", 130), ("QUIT", 131)])
def test_a_command_that_signals_its_own_group_ends_the_run_as_failed(
    tmp_path: Path, sent: str, code: int
) -> None:
    # The watchdog ignores these two signals, so the run must clean it up itself.
    env = _covering(tmp_path, f"kill -{sent} 0", "verification/recipes")
    result = subprocess.run(
        [str(VERIFY), "drive", "thing"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    (evidence,) = (tmp_path / "verification" / "evidence" / "thing").iterdir()
    text = evidence.read_text(encoding="utf-8")
    assert f"- **Exit code:** {code}" in text and "- **Outcome:** failed" in text


# Holds the decision in docs/adr/20261014-one-verification-harness-per-project.md.
def test_a_drift_line_holds_until_every_scenario_has_run_since(tmp_path: Path) -> None:
    env = _harness(tmp_path, "- **Outcome:** verified\n", TWO_SCENARIOS)
    recipe = tmp_path / "verification" / "recipes" / "thing.md"
    recipe.write_text(
        recipe.read_text(encoding="utf-8") + "\nDrift (2026-03-01): changed.\n",
        encoding="utf-8",
    )
    _evidence(
        tmp_path,
        "20260401T000000Z",
        "- **Scenario:** one\n- **Outcome:** verified\n",
    )
    assert "stale (2026-03-01)" in run_verify("list", env=env).stdout
    _evidence(
        tmp_path,
        "20260402T000000Z",
        "- **Scenario:** two\n- **Outcome:** verified\n",
    )
    assert "verified (2026-04-01)" in run_verify("list", env=env).stdout


def test_a_killed_tool_lets_its_command_stop_cleanly_first(tmp_path: Path) -> None:
    # SIGTERM before SIGKILL: what a container client needs to stop the session inside.
    marker = tmp_path / "stopped-cleanly"
    env = _covering(
        tmp_path,
        f"trap 'touch {marker}; exit 0' TERM; sleep 30 & wait",
        "verification/recipes",
    )
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    time.sleep(0.5)
    drive.kill()
    drive.wait(timeout=10)
    deadline = time.monotonic() + 5
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    assert marker.exists()


def _start_drive(env: dict[str, str]) -> subprocess.Popen[str]:
    drive = subprocess.Popen(
        [str(VERIFY), "drive", "thing"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert drive.stdout is not None
    assert drive.stdout.readline().startswith("running [once]")
    time.sleep(0.5)  # the line prints just before the command starts
    return drive


def _appears(path: Path, within: float) -> bool:
    deadline = time.monotonic() + within
    while not path.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    return path.exists()


def test_a_job_left_holding_the_output_does_not_hold_the_run(tmp_path: Path) -> None:
    marker = tmp_path / "outlived"
    env = _covering(
        tmp_path, f"(sleep 3; touch {marker}) & echo started", "verification/recipes"
    )
    began = time.monotonic()
    result = subprocess.run(
        [str(VERIFY), "drive", "thing"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert (
        time.monotonic() - began < 1.9
    )  # the job heeds the stop's SIGTERM: no grace waited
    assert result.returncode == 0, result.stdout + result.stderr
    assert not _appears(marker, 4)


@pytest.mark.parametrize(
    ("signals", "trapped"),
    [(("TERM",), "TERM"), (("HUP",), "HUP"), (("INT", "INT"), "TERM")],
)
def test_a_stopped_command_gets_the_grace_to_clean_up(
    tmp_path: Path, signals: tuple[str, ...], trapped: str
) -> None:
    # One SIGTERM or SIGHUP is passed on; a second Ctrl-C forces the stop with SIGTERM. Either
    # way the command's own cleanup runs undisturbed. A command trapping only SIGHUP dies of any
    # stray SIGTERM, so that case fails outright if one is sent while it cleans up.
    marker = tmp_path / "cleaned-up"
    env = _covering(
        tmp_path,
        f"trap '' INT; trap 'sleep 0.5; echo $? >{marker}; exit 0' {trapped}; sleep 30 & wait",
        "verification/recipes",
    )
    drive = _start_drive(env)
    for name in signals:
        drive.send_signal(getattr(signal, f"SIG{name}"))
        time.sleep(0.2)
    try:
        assert drive.wait(timeout=10) == 130
    finally:
        drive.kill()
    assert marker.read_text(encoding="utf-8").strip() == "0"


def test_a_forced_stop_kills_what_ignores_it_after_the_grace(tmp_path: Path) -> None:
    marker = tmp_path / "outlived"
    env = _covering(
        tmp_path,
        f"(trap '' INT TERM; sleep 4; touch {marker}) >/dev/null 2>&1 & trap '' INT; wait",
        "verification/recipes",
    )
    drive = _start_drive(env)
    drive.send_signal(signal.SIGINT)
    time.sleep(0.2)
    drive.send_signal(signal.SIGINT)
    try:
        assert drive.wait(timeout=10) == 130
    finally:
        drive.kill()
    assert not _appears(marker, 6)


def test_a_tool_killed_during_the_grace_still_stops_what_was_left(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "outlived"
    env = _covering(
        tmp_path,
        f"(trap '' TERM; sleep 4; touch {marker}) & echo started",
        "verification/recipes",
    )
    drive = _start_drive(
        env
    )  # the command has ended; its job ignores the stop's SIGTERM
    drive.kill()
    drive.wait(timeout=10)
    assert not _appears(marker, 6)


def test_a_run_with_nothing_left_behind_does_not_wait_the_grace(tmp_path: Path) -> None:
    env = _covering(tmp_path, "echo done", "verification/recipes")
    began = time.monotonic()
    result = run_verify("drive", "thing", env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert time.monotonic() - began < 1.9  # short of the 2s grace


def _failing_docker(tmp_path: Path, code: int, transcript: str = "") -> Path:
    # Answers every docker call with success except `docker run`, which writes a scaffold log
    # (and the given transcript, for a session that started) into the directory mounted at
    # /out, and exits with `code`.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "docker"
    stub.write_text(
        "#!/bin/sh\n"
        '[ "$1" = run ] || exit 0\n'
        'while [ $# -gt 0 ]; do case "$1" in *:/out) out="${1%:/out}";; esac; shift; done\n'
        '[ -n "$out" ] && echo "seed step broke" >"$out/scaffold.log"\n'
        + (
            f"printf '%s' '{transcript}' >\"$out/transcript.jsonl\"\n"
            if transcript
            else ""
        )
        + f"exit {code}\n"
    )
    stub.chmod(0o755)
    return bin_dir


def test_a_drive_whose_container_fails_before_the_session_is_unreachable(
    tmp_path: Path,
) -> None:
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("go\n", encoding="utf-8")
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(prompt_file)],
        env={
            "PATH": f"{_failing_docker(tmp_path, 7)}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "ANTHROPIC_API_KEY": "test-key",
            "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
            "DRIVE_STAMP": "20990101T000000Z",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 3, result.stderr
    assert "seed step broke" in result.stderr and "container exit 7" in result.stderr


@pytest.mark.parametrize(
    ("code", "expected"), [(124, 124), (125, 3), (126, 3), (127, 3), (128, 128), (1, 1)]
)
def test_a_walk_tells_a_container_that_never_ran_from_a_failed_walk(
    tmp_path: Path, code: int, expected: int
) -> None:
    result = subprocess.run(
        [str(WALK), "Find the install steps.", "README.md"],
        env={
            "PATH": f"{_failing_docker(tmp_path, code)}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "ANTHROPIC_API_KEY": "test-key",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == expected, result.stderr


def test_a_drive_whose_container_dies_mid_session_is_unreachable(
    tmp_path: Path,
) -> None:
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("go\n", encoding="utf-8")
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(prompt_file)],
        env={
            "PATH": f"{_failing_docker(tmp_path, 137, json.dumps(INIT))}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "ANTHROPIC_API_KEY": "test-key",
            "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
            "DRIVE_STAMP": "20990101T000000Z",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 3, result.stdout + result.stderr
    assert "exited 137 after the session started" in result.stderr


def test_a_signal_during_a_stop_kills_at_once(tmp_path: Path) -> None:
    env = _covering(
        tmp_path, "trap '' INT TERM; sleep 30 & wait", "verification/recipes"
    )
    drive = _start_drive(env)
    drive.send_signal(signal.SIGINT)
    time.sleep(0.2)
    drive.send_signal(signal.SIGINT)  # the stop begins; the command ignores its SIGTERM
    time.sleep(0.2)
    began = time.monotonic()
    drive.send_signal(signal.SIGINT)
    try:
        assert drive.wait(timeout=10) == 130
    finally:
        drive.kill()
    assert time.monotonic() - began < 1.5  # not the rest of the 2s grace
