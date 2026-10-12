"""Every eval case loads the way `claude plugin eval` loads it.

The harness rejects a case outright on an unknown frontmatter key, a grader field its type does
not take, or a scaffold script that exits non-zero — and it only finds out when a paid suite
run reaches that case. These checks find it first. The key sets mirror the harness's case
schema; when the CLI accepts a new key, add it here in the same change that first uses it.
"""

from __future__ import annotations

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
    with tempfile.TemporaryDirectory() as workdir:
        result = subprocess.run(
            ["bash", str(script)],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=SCAFFOLD_LIMIT_SECONDS,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert any(Path(workdir).iterdir()), "scaffold wrote nothing"


def test_ceiling_grader_matches_the_schemas_ceiling() -> None:
    copies = sorted(EVALS.glob("define/*/graders/ceiling-verbatim.md"))
    assert copies
    pattern = str(_frontmatter(copies[0])[0]["pattern"])
    assert re.search(pattern, SCHEMA.read_text(encoding="utf-8"))
