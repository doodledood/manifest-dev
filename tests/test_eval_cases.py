"""Every eval case loads the way `claude plugin eval` loads it.

The harness rejects a case outright on an unknown frontmatter key, a grader field its type does
not take, or a scaffold script that exits non-zero — and it only finds out when a paid suite
run reaches that case. These checks find it first. The key sets mirror the harness's case
schema; when the CLI accepts a new key, add it here in the same change that first uses it.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "claude-plugins/manifest-dev/evals"
SCHEMA = ROOT / "claude-plugins/manifest-dev/skills/define/references/SCHEMA.md"

TOP_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs"}
TOP_KEYS |= {"expected_outcome"}
EXECUTION_KEYS = {"model", "max_turns", "timeout_seconds", "allowed_tools"}
EXECUTION_KEYS |= {
    "artifact_publish",
    "growthbook_overrides",
    "append_system_prompt",
    "env",
}
CASE_YAML_KEYS = TOP_KEYS | {"context", "execution", "graders"}
CONTEXT_KEYS = {"scaffold_script", "history_file", "add_dirs"}
COMMON_GRADER_KEYS = {"type", "weight", "arm"}
GRADER_KEYS = {
    "regex": {"target", "pattern", "flags", "match"},
    "tool_order": {"before", "after"},
    "tool_used": {"tool", "input_match", "min", "max"},
    "file_exists": {"path", "exists"},
    "llm": {"criteria", "focus"},
    "baseline": {"baseline_file", "criteria"},
}
SCAFFOLD_LIMIT_SECONDS = 120
INLINE_FLAGS = re.compile(r"\(\?[aiLmsux]+\)")

CASES = sorted(
    p.parent for p in EVALS.rglob("*") if p.name in ("prompt.md", "case.yaml")
)
CASES = sorted(set(CASES))
SCAFFOLDS = sorted(EVALS.rglob("scaffold.sh"))


def _frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    assert match, f"{path.relative_to(EVALS)}: no frontmatter"
    data = yaml.safe_load(match.group(1)) or {}
    assert isinstance(
        data, dict
    ), f"{path.relative_to(EVALS)}: frontmatter not a mapping"
    return data, match.group(2)


def _case_id(case: Path) -> str:
    return case.relative_to(EVALS).as_posix()


@pytest.mark.parametrize("case", CASES, ids=_case_id)
def test_case_files_use_only_accepted_keys(case: Path) -> None:
    prompt = case / "prompt.md"
    if prompt.exists():
        data, body = _frontmatter(prompt)
        unknown = set(data) - TOP_KEYS - EXECUTION_KEYS
        assert not unknown, f"prompt.md: unknown keys {sorted(unknown)}"
        assert body.strip(), "prompt.md: empty prompt"
    case_yaml = case / "case.yaml"
    if case_yaml.exists():
        data = yaml.safe_load(case_yaml.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert isinstance(data.get("schema_version"), str)
        assert not set(data) - CASE_YAML_KEYS, f"case.yaml: unknown keys {set(data)}"
        context = data.get("context", {})
        assert not set(context) - CONTEXT_KEYS, f"case.yaml: unknown context {context}"
        scaffold = context.get("scaffold_script")
        if scaffold:
            assert (case / scaffold).is_file(), f"missing scaffold {scaffold}"
        execution = data.get("execution", {})
        assert not set(execution) - EXECUTION_KEYS - {"prompt"}


@pytest.mark.parametrize("case", CASES, ids=_case_id)
def test_graders_use_only_their_types_keys(case: Path) -> None:
    graders = sorted((case / "graders").glob("*.md"))
    assert graders, "case has no graders"
    for grader in graders:
        data, body = _frontmatter(grader)
        kind = data.get("type")
        assert kind in GRADER_KEYS, f"{grader.name}: type {kind!r}"
        unknown = set(data) - COMMON_GRADER_KEYS - GRADER_KEYS[kind]
        assert not unknown, f"{grader.name}: keys {sorted(unknown)} not taken by {kind}"
        assert data.get("arm") in (None, "with-only", "both"), grader.name
        if kind == "llm":
            assert body.strip(), f"{grader.name}: empty rubric"
        if kind == "tool_used" and "max" in data:
            # The harness defaults `min` to 1, so a "never called" grader without `min: 0`
            # fails every run, including the ones that never call the tool.
            assert "min" in data, f"{grader.name}: `max` without `min`"
        for key in ("pattern", "input_match"):
            if key in data:
                # The harness compiles these as JavaScript regular expressions, which take
                # flags in the `flags` field and reject Python's inline `(?i)` groups.
                assert not INLINE_FLAGS.search(str(data[key])), f"{grader.name}: {key}"
                re.compile(str(data[key]))


@pytest.mark.parametrize("script", SCAFFOLDS, ids=lambda p: _case_id(p.parent))
def test_scaffold_runs_in_an_empty_directory(script: Path) -> None:
    # The harness runs a scaffold with HOME set to the run's own temporary home, and some
    # scaffolds write fixture logs there; the user's real HOME must never receive them.
    with (
        tempfile.TemporaryDirectory() as workdir,
        tempfile.TemporaryDirectory() as home,
    ):
        result = subprocess.run(
            ["bash", str(script)],
            cwd=workdir,
            env={**os.environ, "HOME": home},
            capture_output=True,
            text=True,
            timeout=SCAFFOLD_LIMIT_SECONDS,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert any(Path(workdir).iterdir()), "scaffold wrote nothing"


# Holds the decision in docs/adr/20260728-bound-the-acceptance-contract-from-above.md.
def test_ceiling_grader_matches_the_schemas_ceiling() -> None:
    copies = sorted(EVALS.glob("define/*/graders/ceiling-verbatim.md"))
    assert copies
    pattern = str(_frontmatter(copies[0])[0]["pattern"])
    assert re.search(pattern, SCHEMA.read_text(encoding="utf-8"))


def test_rubrics_quote_their_cases_current_request() -> None:
    # A rubric that embeds the request goes stale silently when the prompt is edited.
    stale = []
    for grader in sorted(EVALS.rglob("graders/*.md")):
        text = grader.read_text(encoding="utf-8")
        if "\nThe request:\n" not in text:
            continue
        quoted = text.split("\nThe request:\n", 1)[1]
        _, body = _frontmatter(grader.parent.parent / "prompt.md")
        if " ".join(quoted.split()) != " ".join(body.split()):
            stale.append(_case_id(grader.parent.parent))
    assert not stale, f"rubric request differs from prompt.md: {stale}"


HOME_WRITERS = [
    p for p in SCAFFOLDS if ".manifest-dev" in p.read_text(encoding="utf-8")
]


@pytest.mark.parametrize("script", HOME_WRITERS, ids=lambda p: _case_id(p.parent))
def test_scaffold_writing_home_refuses_a_home_with_logs(script: Path) -> None:
    # Run by hand without a scratch HOME, such a scaffold would plant fixture logs among the
    # user's own, where recall reads them as real history.
    with (
        tempfile.TemporaryDirectory() as workdir,
        tempfile.TemporaryDirectory() as home,
    ):
        logs = Path(home, ".manifest-dev", "logs")
        logs.mkdir(parents=True)
        (logs / "existing.md").write_text("# a real session\n", encoding="utf-8")
        result = subprocess.run(
            ["bash", str(script)],
            cwd=workdir,
            env={**os.environ, "HOME": home},
            capture_output=True,
            text=True,
            timeout=SCAFFOLD_LIMIT_SECONDS,
            check=False,
        )
        assert result.returncode != 0, "ran over a HOME that already holds logs"
        assert "scratch HOME" in result.stderr
        assert [p.name for p in logs.iterdir()] == [
            "existing.md"
        ], "wrote into the user's logs"
        assert not any(Path(workdir).iterdir()), "wrote fixtures before refusing"


CASE_ROW = re.compile(r"^\| `([^`]+)` \|", re.MULTILINE)


def _case_dirs(suite: Path) -> set[str]:
    return {case.name for case in CASES if case.parent == suite}


def _case_table_rows(readme: Path) -> set[str]:
    # Case tables sit under headings that start with "## Cases"; other tables in the same
    # README name graders or prompts, not cases.
    sections = re.split(r"^## ", readme.read_text(encoding="utf-8"), flags=re.MULTILINE)
    return {
        name
        for section in sections
        if re.match(r"Cases\b", section)
        for name in CASE_ROW.findall(section)
    }


CLASSIFICATION_ROW = re.compile(
    r"^\| `([^`]+)` \| (keep|first run decides) \| \S", re.MULTILINE
)


@pytest.mark.parametrize(
    "suite", [EVALS, EVALS / "define"], ids=["figure-out", "define"]
)
def test_every_case_is_classified_with_a_reason(suite: Path) -> None:
    # A run is expensive, so each case says why it stays — measured uplift, a declared guard,
    # or a first run still owed — and a case nobody can justify is the one to retire.
    sections = re.split(
        r"^## ", (suite / "README.md").read_text(encoding="utf-8"), flags=re.MULTILINE
    )
    (section,) = [s for s in sections if s.startswith("Classification\n")]
    rows = set(CLASSIFICATION_ROW.findall(section))
    ids = {case_id for case_id, _ in rows}
    dirs = {name.split("-", 1)[0] for name in _case_dirs(suite)}
    assert not dirs - ids, f"cases with no classification row: {sorted(dirs - ids)}"
    assert not ids - dirs, f"classification rows with no case: {sorted(ids - dirs)}"


# Holds the decision in docs/adr/20261013-runs-build-and-maintain-a-project-verification-surface.md.
@pytest.mark.parametrize(
    "suite", [EVALS, EVALS / "define"], ids=["figure-out", "define"]
)
def test_suite_readme_lists_exactly_its_cases(suite: Path) -> None:
    # The README is the suite's index and carries each case's status; a case missing from it
    # has no status, and a row for a removed case points at nothing.
    dirs, rows = _case_dirs(suite), _case_table_rows(suite / "README.md")
    assert not dirs - rows, f"cases with no README row: {sorted(dirs - rows)}"
    assert not rows - dirs, f"README rows with no case: {sorted(rows - dirs)}"
