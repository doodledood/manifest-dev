"""manifest-explain answers questions about manifest-dev, close to ASD-STE100.

It restates the glossary in a second register for users, so its term set is held level with
CONTEXT.md and its skill list with the plugin; their meaning stays a review judgment. The owner
asked for about 90% ASD-STE100, so its counted limits are held here and the rest is judged. See
docs/adr/20261015-manifest-explain-answers-questions-about-manifest-dev-in-simplified-english.md.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from tests.test_entry_points import user_invocable

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = (
    REPO_ROOT / "claude-plugins" / "manifest-dev" / "skills" / "manifest-explain"
)
GLOSSARY = SKILL_DIR / "references" / "GLOSSARY.md"
CONTEXT = REPO_ROOT / "CONTEXT.md"

# Maintainer vocabulary: words this repository uses to reason about its own prompts, which no
# user meets in a run. The context file names the first five as maintainer words; Progressive
# Disclosure and Universal Language name how the prompts here are written.
MAINTAINER_TERMS = {
    "Spine",
    "Altitude",
    "Re-host",
    "Door",
    "House",
    "Progressive Disclosure",
    "Universal Language",
}

# ASD-STE100's counted writing rules: a procedural sentence has at most 20 words, a descriptive
# one at most 25, and a paragraph at most 6 sentences. A numbered list item is a procedural step.
PROCEDURAL_MAX = 20
DESCRIPTIVE_MAX = 25
PARAGRAPH_MAX = 6

CONTEXT_TERM = re.compile(r"^\*\*([^*]+)\*\*:\s*$", re.MULTILINE)
EXPLAIN_TERM = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
# Each manifest-explain entry records the fingerprint of the CONTEXT.md entry it was written from, so a
# reworded definition fails until someone rereads the manifest-explain entry and records the new value.
EXPLAIN_FINGERPRINT = re.compile(
    r"^### (.+?)\s*\n<!-- context: ([0-9a-f]{12}) -->$", re.MULTILINE
)
FENCE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
CODE_SPAN = re.compile(r"`[^`\n]+`")
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’/-]*")
SENTENCE_END = re.compile(r"(?<=[.!?])[\"”)]?\s+(?=[A-Z0-9`\"“(/*])")
NUMBERED = re.compile(r"^\d+\.\s+")
BULLET = re.compile(r"^[-*]\s+")


def context_terms() -> set[str]:
    text = CONTEXT.read_text(encoding="utf-8")
    language = text.split("## Language", 1)[1].split("\n## ", 1)[0]
    return set(CONTEXT_TERM.findall(language))


def context_entries() -> dict[str, str]:
    """Each term's whole entry — definition and Avoid line — with whitespace collapsed."""
    text = CONTEXT.read_text(encoding="utf-8")
    language = text.split("## Language", 1)[1].split("\n## ", 1)[0]
    entries = {}
    for match in CONTEXT_TERM.finditer(language):
        rest = language[match.end() :].lstrip("\n").split("\n\n", 1)[0]
        entries[match.group(1)] = " ".join(rest.split())
    return entries


def fingerprint(entry: str) -> str:
    return hashlib.sha256(entry.encode("utf-8")).hexdigest()[:12]


def explain_terms() -> set[str]:
    return set(EXPLAIN_TERM.findall(GLOSSARY.read_text(encoding="utf-8")))


def explain_files() -> list[Path]:
    files = sorted(SKILL_DIR.rglob("*.md"))
    assert SKILL_DIR / "SKILL.md" in files and GLOSSARY in files, files
    return files


def body(text: str) -> str:
    """The prose a reader meets: no frontmatter, fences, comments or link targets."""
    if text.startswith("---\n"):
        text = text.split("\n---\n", 1)[1]
    text = FENCE.sub("", HTML_COMMENT.sub("", text))
    return LINK.sub(r"\1", text)


def words(sentence: str) -> int:
    """STE word count: a code span is one word, as a technical name is."""
    return len(WORD.findall(CODE_SPAN.sub(" CODE ", sentence.replace("**", ""))))


def units(text: str) -> list[tuple[str, str]]:
    """Each paragraph, list item and table cell, with its kind: step, item, cell or paragraph."""
    found: list[tuple[str, str]] = []
    for block in re.split(r"\n\s*\n", body(text)):
        current: list[str] = []
        kind = "paragraph"
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("|"):
                if not re.fullmatch(r"[|:\-\s]+", stripped):
                    found.extend(
                        ("cell", c.strip()) for c in stripped.strip("|").split("|")
                    )
                continue
            starts_item = NUMBERED.match(stripped) or BULLET.match(stripped)
            if starts_item and current:
                found.append((kind, " ".join(current)))
                current = []
            if starts_item:
                kind = "step" if NUMBERED.match(stripped) else "item"
                stripped = (
                    NUMBERED.sub("", stripped)
                    if kind == "step"
                    else BULLET.sub("", stripped)
                )
            current.append(stripped)
        if current:
            found.append((kind, " ".join(current)))
    return [(kind, unit) for kind, unit in found if unit]


def sentences(unit: str) -> list[str]:
    return [s for s in SENTENCE_END.split(unit) if words(s)]


def ste_problems(text: str) -> list[str]:
    """What breaks one of ASD-STE100's counted limits."""
    problems = []
    for kind, unit in units(text):
        parts = sentences(unit)
        if len(parts) > PARAGRAPH_MAX:
            problems.append(
                f"{len(parts)} sentences (max {PARAGRAPH_MAX}): {unit[:80]}…"
            )
        limit = PROCEDURAL_MAX if kind == "step" else DESCRIPTIVE_MAX
        for sentence in parts:
            if words(sentence) > limit:
                problems.append(f"{words(sentence)} words (max {limit}): {sentence}")
    return problems


def test_every_glossary_term_has_an_explain_entry_and_explain_defines_no_other() -> (
    None
):
    expected = context_terms() - MAINTAINER_TERMS
    actual = explain_terms()
    assert not MAINTAINER_TERMS - context_terms(), (
        f"maintainer terms no longer in CONTEXT.md: {sorted(MAINTAINER_TERMS - context_terms())};"
        " remove them from MAINTAINER_TERMS"
    )
    assert actual == expected, (
        f"Missing from {GLOSSARY.relative_to(REPO_ROOT)}: {sorted(expected - actual)} — add a"
        f" `### Term` entry saying what it is and why it exists, in ASD-STE100. Not in CONTEXT.md:"
        f" {sorted(actual - expected)} — add the term to CONTEXT.md, or remove the entry. A term"
        " only maintainers use goes in MAINTAINER_TERMS instead."
    )


def test_explain_names_every_user_invocable_skill() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    missing = sorted(s for s in user_invocable("manifest-dev") if f"`/{s}`" not in text)
    assert not missing, (
        f"manifest-explain/SKILL.md does not name {missing}: add each as `/name` with when a user reaches"
        " for it."
    )


def test_explain_keeps_the_counted_ste_rules() -> None:
    problems = [
        f"{path.relative_to(REPO_ROOT)}: {problem}"
        for path in explain_files()
        for problem in ste_problems(path.read_text(encoding="utf-8"))
    ]
    assert not problems, "ASD-STE100:\n" + "\n".join(problems)


def test_the_ste_counter_catches_each_rule() -> None:
    long_step = "1. " + " ".join(["Read"] + ["the"] * 20) + "."
    long_sentence = " ".join(["The"] + ["file"] * 25) + "."
    long_paragraph = " ".join(["It is short."] * 7)
    assert ste_problems("1. " + " ".join(["Read"] + ["the"] * 19) + ".") == []
    for text in (long_step, long_sentence, long_paragraph):
        assert ste_problems(text), text
    assert (
        ste_problems("Run `a very long command with many many words in it` now.") == []
    )
    assert ste_problems("The run is starting.") == []


def test_every_explain_entry_was_written_from_the_current_context_entry() -> None:
    recorded = dict(EXPLAIN_FINGERPRINT.findall(GLOSSARY.read_text(encoding="utf-8")))
    entries = context_entries()
    problems = []
    for term in sorted(explain_terms() & set(entries)):
        current = fingerprint(entries[term])
        if recorded.get(term) != current:
            problems.append(
                f"{term}: CONTEXT.md's entry changed since its manifest-explain entry was written. Reread"
                f" `### {term}` in {GLOSSARY.relative_to(REPO_ROOT)}, make it agree, then set the"
                f" line under its heading to <!-- context: {current} -->"
            )
    assert not problems, "\n".join(problems)
