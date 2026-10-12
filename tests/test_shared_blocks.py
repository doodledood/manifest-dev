"""A rule several shipped skills apply must stay word for word the same in each of them.

A shipped skill stands alone, so a rule several skills apply is restated in each of them
rather than referenced. Those copies drift: one gets sharpened and the others keep the old
wording, and the skills then disagree about the same decision. Each shared block is held
here once; this check fails when a file that states it no longer carries it verbatim
(whitespace aside), or when another shipped file starts stating it without being listed.
Changing a block means changing it here and in every listed file in the same edit.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS = REPO_ROOT / "claude-plugins"
SKILLS = "claude-plugins/manifest-dev/skills"

USERS_CALL = """
**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list the user's calls
first, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.
"""

# Each block: its text, a phrase that identifies it, and the files that state it.
BLOCKS: dict[str, tuple[str, str, frozenset[str]]] = {
    "users-call": (
        USERS_CALL,
        "**The user's call.**",
        frozenset(
            {
                f"{SKILLS}/figure-out/SKILL.md",
                f"{SKILLS}/define/SKILL.md",
                f"{SKILLS}/do/SKILL.md",
                f"{SKILLS}/done/SKILL.md",
                f"{SKILLS}/escalate/SKILL.md",
                f"{SKILLS}/run-ticket/SKILL.md",
            }
        ),
    ),
}


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _shipped() -> dict[str, str]:
    return {
        path.relative_to(REPO_ROOT).as_posix(): _normalize(path.read_text("utf-8"))
        for path in sorted(PLUGINS.rglob("*.md"))
    }


@pytest.mark.parametrize("name", sorted(BLOCKS))
def test_block_is_verbatim_in_each_file(name: str) -> None:
    text, _, files = BLOCKS[name]
    shipped = _shipped()
    missing = sorted(f for f in files if _normalize(text) not in shipped[f])
    assert not missing, f"{name} differs or is missing in: {missing}"


@pytest.mark.parametrize("name", sorted(BLOCKS))
def test_block_lives_only_in_declared_files(name: str) -> None:
    _, marker, files = BLOCKS[name]
    stating = {path for path, body in _shipped().items() if marker in body}
    assert stating == files
