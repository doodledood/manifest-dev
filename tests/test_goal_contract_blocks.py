"""The continuation-goal blocks are one text each, wherever they are emitted.

Every skill that arms an unattended-run backstop hands a host a completion contract.
That contract is emitted verbatim, so the same characters have to appear at every
site and in every `dist/` copy — a site holding a reworded variant ships a different
contract under the same name, and nothing else in the repo would notice.

This is not hypothetical. Before these blocks were consolidated, the gate-ledger
field list was byte-identical across three skills while the stale-gate rule sitting
beside it had already drifted into three separate wordings. A convention that lives
only as a sentence in CLAUDE.md drifts exactly that way, which is why it is checked
here.

**A block is recognized by a phrase in its body, never by its opening line.** That is
the whole trick, and it is load-bearing: matching on the opening line means rewording
that line makes the block unrecognizable rather than different, so it drops out of the
comparison and the remaining copies still agree. A body signature turns the same edit
into a visible second variant.

Four properties, because the contract has four moving parts and locking down only the
goal block leaves the rest free to drift:

1. every shared block is one text wherever it appears;
2. every `dist/` copy carries the same blocks its `claude-plugins/` source does — a
   clause deleted outright from one distribution is silent otherwise;
3. every site arming a Manifest backstop carries the goal block;
4. every such site carries the instruction forbidding paraphrase — the block is only
   half the mechanism, and a prose-tightening pass that leaves fenced content alone
   would strip the other half without a signal.

The checks derive their own subject rather than listing today's sites, so a site added
later is covered without this file being edited.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SEARCH_ROOTS = (ROOT / "claude-plugins", ROOT / "dist")
TEMPLATE_PLUGIN = "PLUGIN_TEMPLATE"

# A file arms a backstop when it both instructs the arming and names the host
# capability that arming looks for. Two signals, because either alone is wrong: the
# capability sentence appears in READMEs and in `define`, which only describe the
# mechanism, while the word "backstop" appears in verification references that merely
# mention one. Neither signal keys on an incidental phrasing — the five Manifest sites
# say "goal-setting, continuation, or durable-completion-condition capability" and
# figure-out says "goal-setting or continuation capability", and harmonizing those is
# an ordinary copy-edit that must not change which files this test examines.
ARMS_A_BACKSTOP = re.compile(r"(?:arm|establish) (?:a|the)[^.]*backstop")
NAMES_THE_CAPABILITY = re.compile(r"goal-setting[^.]*?capability")

# Arms a backstop but carries no Manifest goal block, deliberately: its goal names a
# topic, not a Manifest, because no Manifest exists in that workflow. Excluded by name
# with its reason, rather than by relying on it phrasing the capability differently.
# See docs/adr/20260828-continuation-goals-emit-verbatim-from-one-block.md.
NO_MANIFEST_BACKSTOP = ("figure-out/references/autonomous.md",)

# The instruction that makes the block emit verbatim. Whitespace-normalized before
# comparison because it is line-wrapped at some sites and not at others, and the
# trailing pronoun differs between one-block and multi-block sites.
NO_PARAPHRASE = "Do not summarize, shorten, reword, or re-punctuate"

# name -> a phrase from the block's BODY that identifies it. Never the opening line:
# see the module docstring. Each must be unique to its block across the whole tree,
# which `test_signatures_identify_exactly_one_block` enforces.
BLOCKS = {
    "goal block": "it changes only through /define, never by direct edit",
    "gate-ledger clause": (
        "explicit or inherited verifier model, latest verdict, evidence"
    ),
    "chain prefix": (
        "Record the Manifest's path in a checkpoint note as soon as define reports it"
    ),
    "PR-tend prefix": "Never press merge. Report a wait-only CI state as pending",
}
GOAL_BLOCK = "goal block"

FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)


def shipped_markdown() -> list[Path]:
    """Every shipped markdown file, template plugin excluded."""
    return sorted(
        path
        for root in SEARCH_ROOTS
        if root.is_dir()
        for path in root.rglob("*.md")
        if TEMPLATE_PLUGIN not in path.parts
    )


def fenced_blocks(path: Path) -> list[str]:
    return FENCE.findall(path.read_text())


def name_of(block: str) -> str | None:
    """Which shared block this fenced text is, by body signature."""
    return next((name for name, sig in BLOCKS.items() if sig in block), None)


def blocks_in(path: Path) -> set[str]:
    """Which shared blocks this file carries."""
    return {
        name for block in fenced_blocks(path) if (name := name_of(block)) is not None
    }


def copies_by_block() -> dict[str, dict[str, list[Path]]]:
    """block name -> exact text -> the files carrying that text."""
    found: dict[str, dict[str, list[Path]]] = {name: {} for name in BLOCKS}
    for path in shipped_markdown():
        for block in fenced_blocks(path):
            name = name_of(block)
            if name is not None:
                found[name].setdefault(block, []).append(path)
    return found


def backstop_sites() -> list[Path]:
    """Files arming a backstop that should carry the Manifest goal block."""
    return [
        path
        for path in shipped_markdown()
        if ARMS_A_BACKSTOP.search(text := path.read_text())
        and NAMES_THE_CAPABILITY.search(text)
        and not any(str(path).endswith(skip) for skip in NO_MANIFEST_BACKSTOP)
    ]


def source_skills() -> dict[str, Path]:
    """skill directory name -> its authored SKILL.md under claude-plugins/."""
    return {
        path.parent.name: path
        for path in (ROOT / "claude-plugins").rglob("skills/*/SKILL.md")
        if TEMPLATE_PLUGIN not in path.parts
    }


def dist_copies(skill: str) -> list[Path]:
    return [
        path
        for path in (ROOT / "dist").rglob(f"skills/{skill}/SKILL.md")
        if TEMPLATE_PLUGIN not in path.parts
    ]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def normalized(text: str) -> str:
    return " ".join(text.split())


def test_every_shared_block_is_one_text() -> None:
    """No block may have two variants — that is drift, wherever the copy lives.

    Variants are reported smallest group first, because a single edited copy is
    almost always the offender and listing the untouched majority ahead of it
    buries the one filename the reader needs.
    """
    drifted = []
    for name, variants in copies_by_block().items():
        if len(variants) > 1:
            listing = "\n".join(
                f"    {len(paths)} copy(ies): {', '.join(rel(p) for p in sorted(paths))}"
                for paths in sorted(variants.values(), key=len)
            )
            drifted.append(f"  {name}\n{listing}")
    assert not drifted, "shared goal blocks have drifted apart:\n" + "\n".join(drifted)


def test_dist_copies_carry_the_same_blocks_as_their_source() -> None:
    """A distribution may not quietly ship a skill missing one of its blocks.

    Drift comparison only sees blocks that are present, so a clause deleted outright
    from one `dist/` copy is invisible to it. The authored `claude-plugins/` copy is
    the reference for which blocks that skill owes.
    """
    missing = []
    for skill, src in sorted(source_skills().items()):
        expected = blocks_in(src)
        if not expected:
            continue
        for copy in sorted(dist_copies(skill)):
            gap = expected - blocks_in(copy)
            if gap:
                missing.append(f"  {rel(copy)}\n    missing: {', '.join(sorted(gap))}")
    assert not missing, (
        "these dist copies are missing blocks their claude-plugins/ source carries:\n"
        + "\n".join(missing)
    )


def test_every_backstop_site_carries_the_goal_block() -> None:
    """A site that arms a backstop emits the goal block, not a variant of its own."""
    missing = [rel(p) for p in backstop_sites() if GOAL_BLOCK not in blocks_in(p)]
    assert not missing, (
        "these files arm a completion backstop but carry no recognizable goal "
        "block:\n  " + "\n  ".join(missing)
    )


def test_every_backstop_site_forbids_paraphrase() -> None:
    """The block is half the mechanism; the instruction not to reword it is the rest.

    A prose-tightening pass naturally targets prose and leaves fenced content alone,
    so this instruction is the half that can be removed without any block changing.
    """
    missing = [
        rel(p)
        for p in backstop_sites()
        if normalized(NO_PARAPHRASE) not in normalized(p.read_text())
    ]
    assert not missing, (
        "these files emit a goal block without instructing that it not be reworded:\n"
        "  " + "\n  ".join(missing)
    )


def test_signatures_identify_exactly_one_block() -> None:
    """Every signature must be unique, or two blocks collapse into one comparison."""
    collisions = [
        f"  {name}: also matches {other}"
        for name, sig in BLOCKS.items()
        for other, other_sig in BLOCKS.items()
        if name != other and sig in other_sig
    ]
    assert not collisions, "block signatures overlap:\n" + "\n".join(collisions)


def test_the_blocks_are_actually_present() -> None:
    """Guards the checks above from passing vacuously on an empty search."""
    found = copies_by_block()
    for name in BLOCKS:
        carriers = [p for paths in found[name].values() for p in paths]
        assert carriers, f"no file carries the {name}"
    assert backstop_sites(), "no file arms a completion backstop"
