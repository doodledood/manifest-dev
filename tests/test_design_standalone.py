"""Keep design standalone and its evaluator's supporting files reachable."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest

ROOT = Path(__file__).parent.parent
SKILL_DIRS = (
    ROOT / "claude-plugins/manifest-dev/skills/design",
    ROOT / "dist/codex/plugins/manifest-dev/skills/design",
)


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=("source", "codex"))
def test_references_resolve_in_an_isolated_install(
    skill_dir: Path, tmp_path: Path
) -> None:
    isolated = tmp_path / "design"
    shutil.copytree(skill_dir, isolated, symlinks=True)
    assert (isolated / "SKILL.md").is_file()
    for document in isolated.rglob("*.md"):
        assert document.resolve().is_relative_to(isolated)
        text = document.read_text(encoding="utf-8")
        targets = re.findall(r"\]\(([^)]+)\)", text)
        targets += re.findall(r"`([^`\n]+\.(?:md|py|mjs|js))`", text)
        for target in targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            local = (document.parent / unquote(url.path)).resolve()
            assert local.is_relative_to(isolated), (document.name, target)
            assert local.is_file(), (document.name, target)


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=("source", "codex"))
def test_prompts_do_not_delegate_to_another_skill(skill_dir: Path) -> None:
    # Guard the invocation syntax that made the original implementation a wrapper.
    invocation = re.compile(r"\b(?:invoke|activate)\b[^.!?]*\bskill\b", re.IGNORECASE)
    for document in skill_dir.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        assert not invocation.search(text), document


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=("source", "codex"))
def test_entrypoint_stays_design_guidance(skill_dir: Path) -> None:
    # Bounded guard against the execution vocabulary removed from this prompt.
    # Reference titles and external pages are not execution instructions.
    execution = re.compile(
        r"\b(?:build(?:s|ing)?|implement(?:s|ed|ing|ation)?|"
        r"render(?:s|ed|ing)?|verif(?:y|ies|ied|ying|ication)|"
        r"repair(?:s|ed|ing)?|deliver(?:s|ed|ing|y)?)\b",
        re.IGNORECASE,
    )
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert not execution.search(text), skill_dir


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=("source", "codex"))
def test_review_support_paths_resolve(skill_dir: Path) -> None:
    review_dir = skill_dir.with_name("review-design")
    for document in review_dir.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        targets = re.findall(r"`(?:node )?([^`\s]+\.(?:md|mjs))(?: [^`]*)?`", text)
        for target in targets:
            local = (document.parent / target).resolve()
            assert local.is_relative_to(skill_dir.parent.resolve()), target
            assert local.is_file(), (document.name, target)
    assert (review_dir / "scripts/design-check.mjs").is_file()
    assert not skill_dir.with_name("design-v2").exists()
