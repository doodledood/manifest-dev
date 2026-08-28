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

The check derives its own subject rather than listing today's sites: it finds the
files that carry a block, so a site added later is compared without this file being
edited, and it finds the files that arm a backstop, so a site that drops or garbles
its block is caught rather than silently skipped.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SEARCH_ROOTS = (ROOT / "claude-plugins", ROOT / "dist")
TEMPLATE_PLUGIN = "PLUGIN_TEMPLATE"

# A file arms a backstop if it names the host capability the backstop looks for.
BACKSTOP_MARKER = "durable-completion-condition capability"

# First line of each shared block. A block is recognized by its opening line, so
# rewording that line makes the site fail the "carries the goal block" check below
# rather than quietly dropping out of the comparison.
GOAL_BLOCK = (
    "Work under the Manifest at <manifest-path> until every Acceptance Criterion"
)
LEDGER_CLAUSE = "Maintain a gate ledger covering every Acceptance Criterion and Global"
CHAIN_PREFIX = "Reach shared understanding of the task, then write a Manifest from it."
ANCHORS = (GOAL_BLOCK, LEDGER_CLAUSE, CHAIN_PREFIX)

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


def anchor_of(block: str) -> str | None:
    """The anchor a fenced block belongs to, or None if it carries no block."""
    return next((anchor for anchor in ANCHORS if block.startswith(anchor)), None)


def copies_by_anchor() -> dict[str, dict[str, list[Path]]]:
    """anchor -> block text -> the files carrying that exact text."""
    found: dict[str, dict[str, list[Path]]] = {anchor: {} for anchor in ANCHORS}
    for path in shipped_markdown():
        for block in fenced_blocks(path):
            anchor = anchor_of(block)
            if anchor is not None:
                found[anchor].setdefault(block, []).append(path)
    return found


def backstop_sites() -> list[Path]:
    return [path for path in shipped_markdown() if BACKSTOP_MARKER in path.read_text()]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def test_every_shared_block_is_one_text() -> None:
    """No anchor may have two variants — that is drift, wherever the copy lives.

    Variants are reported smallest group first, because a single edited copy is
    almost always the offender and listing the untouched majority ahead of it
    buries the one filename the reader needs.
    """
    drifted = []
    for anchor, variants in copies_by_anchor().items():
        if len(variants) > 1:
            by_size = sorted(variants.values(), key=len)
            listing = "\n".join(
                f"    {len(paths)} copy(ies): {', '.join(rel(p) for p in sorted(paths))}"
                for paths in by_size
            )
            drifted.append(f"  {anchor[:60]}...\n{listing}")
    assert not drifted, "shared goal blocks have drifted apart:\n" + "\n".join(drifted)


def test_every_backstop_site_carries_the_goal_block() -> None:
    """A site that arms a backstop emits the goal block, not a variant of its own."""
    missing = [
        rel(path)
        for path in backstop_sites()
        if not any(block.startswith(GOAL_BLOCK) for block in fenced_blocks(path))
    ]
    assert not missing, (
        "these files arm a completion backstop but carry no recognizable goal "
        "block — a reworded opening line reads as absent here:\n  "
        + "\n  ".join(missing)
    )


def test_the_blocks_are_actually_present() -> None:
    """Guards the two checks above from passing vacuously on an empty search."""
    found = copies_by_anchor()
    for anchor in (GOAL_BLOCK, LEDGER_CLAUSE, CHAIN_PREFIX):
        carriers = [p for paths in found[anchor].values() for p in paths]
        assert carriers, f"no file carries the block anchored at: {anchor[:60]}..."
    assert backstop_sites(), "no file arms a completion backstop"
