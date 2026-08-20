"""The rendering contract has one home, and figure-out reaches it by invocation.

Two properties, both established by ADR 20260818 (the surface skill owns the rendering
contract) and repaired after its implementing commit added the rules without removing
what they replaced:

1. Every shipped copy of figure-out's SKILL.md directs an *invocation* of chat-surface
   and names the mode. A table row naming the skill with no verb names material and no
   operation, which is how the pointer silently stopped firing.
2. No shipped skill file outside chat-surface states a rule about the visual form a
   turn's text takes.

This is a tripwire on the phrasings that constitute stating form, not a replacement for
reading. A newly invented form rule using none of these words passes here; that judgment
lives with the manifest gate, not with a regex.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_ROOTS = (ROOT / "claude-plugins", ROOT / "dist")

# Phrasings that state how a turn's text should look. Drawn from the text actually
# removed from figure-out and re-pitch, so a literal restoration trips the wire.
FORM_RULE_PHRASES = (
    "alone on the last line",
    "set apart from the prose",
    "lands on it without hunting",
    "short bullets",
    "numbered steps for",
    "paragraphs of two sentences",
    "wall of text",
    "bolded at the front",
    "three-second pass",
)

# A line may name a form when it is handing that choice to the surface skill. These are
# deferrals, not rules — figure-out's "which lines carry the emphasis is the surface
# contract's call" must pass while a restored rule fails.
DEFERRAL_MARKERS = (
    "surface contract's call",
    "surface skill's call",
    "states none of its own",
    "owns which form",
    "owns how a turn is shaped",
)

# The contract's own home, plus the two files the manifest's gate names as outside its
# subject: review-pr's structural defaults govern a GitHub comment published under the
# user's account (a voice-and-platform convention, alongside its no-emoji and
# no-AI-footer rules), and walk-pr's canvas specifies a one-shot interactive artifact
# rather than the form of a turn's text.
EXEMPT_SKILLS = frozenset({"chat-surface", "review-pr", "walk-pr"})

# The directive form CLAUDE.md prescribes, with its mode. Matched as one adjacent
# phrase rather than as separate words: the --surface paragraph also contains
# "a different surface-providing skill to invoke instead", so a loose substring
# search for the verb passes even after the real directive is gone.
INVOCATION = re.compile(
    r"invoke the `(?:manifest-dev:)?chat-surface` skill with: `(?P<mode>text|html)`"
)


def shipped_skill_files() -> list[Path]:
    """Every shipped SKILL.md and reference file, derived from the tree."""
    return sorted(
        path
        for root in SKILL_ROOTS
        for path in root.rglob("skills/**/*.md")
        if path.is_file()
    )


def owning_skill(path: Path) -> str:
    """The skill directory a shipped file belongs to."""
    parts = path.parts
    return parts[parts.index("skills") + 1]


def test_every_figure_out_copy_invokes_chat_surface_with_its_mode() -> None:
    """The loading row carries the directive; the flag paragraph resolves the modes.

    Both are checked separately. Asserting only that *some* line in the file carries a
    verb lets either site rot while the other keeps the test green — which is how a
    passive `--surface` paragraph and an inert table row both shipped at once. The
    directive belongs in the loading row because that row is unconditional, where the
    flag paragraph reads as scoped to runs that passed the flag.
    """
    copies = [
        p
        for p in shipped_skill_files()
        if p.name == "SKILL.md" and owning_skill(p) == "figure-out"
    ]
    assert copies, "no shipped figure-out SKILL.md found"

    for path in copies:
        where = path.relative_to(ROOT)
        lines = path.read_text(encoding="utf-8").splitlines()

        rows = [ln for ln in lines if ln.startswith("|") and "chat-surface" in ln]
        assert (
            len(rows) == 1
        ), f"{where}: expected one chat-surface loading row, found {len(rows)}"
        directive = INVOCATION.search(rows[0])
        assert directive is not None, (
            f"{where}: the loading row carries no imperative invocation of chat-surface naming "
            "its mode. Every other row in that table is a readable path; this one is reached "
            "only by invoking it, and a bare invocation lands in html."
        )
        assert (
            directive.group("mode") == "text"
        ), f"{where}: the loading row names mode {directive.group('mode')!r}; the default is text."

        flag = [ln for ln in lines if ln.startswith("`--surface <name>`")]
        assert (
            len(flag) == 1
        ), f"{where}: expected one --surface paragraph, found {len(flag)}"
        assert "`text`" in flag[0] and "`html`" in flag[0], (
            f"{where}: the --surface paragraph must resolve both modes, since the loading row "
            "defers to it for anything other than the default."
        )


def test_no_shipped_skill_outside_chat_surface_states_a_form_rule() -> None:
    offenders: list[str] = []
    for path in shipped_skill_files():
        if owning_skill(path) in EXEMPT_SKILLS:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            lowered = line.lower()
            if not any(phrase in lowered for phrase in FORM_RULE_PHRASES):
                continue
            if any(marker in lowered for marker in DEFERRAL_MARKERS):
                continue
            offenders.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()[:100]}")

    assert not offenders, (
        "the rendering contract belongs to chat-surface alone; these state form themselves:\n"
        + "\n".join(offenders)
    )
