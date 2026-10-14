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
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFY = REPO_ROOT / "scripts" / "verify"
SHIPPED_VERIFY = (
    REPO_ROOT
    / "claude-plugins"
    / "manifest-dev"
    / "skills"
    / "setup-project"
    / "references"
    / "harness"
    / "verify"
)
RECIPES = REPO_ROOT / "verification" / "recipes"
DRIVE = REPO_ROOT / "scripts" / "drive-skill.sh"
WALK = REPO_ROOT / "scripts" / "walk.sh"

INVOCABLE_FALSE = re.compile(r"^user-invocable:\s*false\s*$", re.MULTILINE)
SECTION = r"\*([^*\n]+)\*"
POINTER = re.compile(rf"`([\w./-]+\.(?:md|html))` → ({SECTION}(?: and {SECTION})*)")


def run_verify(
    *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFY), *args],
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
def test_this_repositorys_tool_is_the_shipped_one() -> None:
    assert VERIFY.read_bytes() == SHIPPED_VERIFY.read_bytes(), (
        "scripts/verify differs from the tool setup-project ships; change the shipped copy "
        "(with a new surfaces version) and copy it here"
    )


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


def _harness(tmp_path: Path, history: str) -> dict[str, str]:
    data = tmp_path / "verification"
    (data / "recipes").mkdir(parents=True)
    (data / "recipes" / "thing.md").write_text(
        "---\nkind: feature\n---\n# Thing\n\nDoes a thing.\n\n## Scenarios\n\n"
        "### once\nRun: `true`\nProves: it runs.\n",
        encoding="utf-8",
    )
    if history:
        (data / "evidence" / "thing").mkdir(parents=True)
        (data / "evidence" / "thing" / "20260101T000000Z.md").write_text(
            history, encoding="utf-8"
        )
    return {**os.environ, "VERIFY_ROOT": str(tmp_path), "VERIFY_DATA": str(data)}


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


def test_runner_scripts_parse() -> None:
    # A broken runner fails here, not in the first run that needs it.
    for script in (DRIVE, WALK):
        result = subprocess.run(
            ["bash", "-n", str(script)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{script.name}: {result.stderr}"


# No docker on PATH: a dry run that tried to start anything would fail.
DRY_ENV = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent-home"}


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


def _stub_docker(tmp_path: Path) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "docker"
    stub.write_text("#!/bin/sh\nexit 0\n")
    stub.chmod(0o755)
    return bin_dir


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
