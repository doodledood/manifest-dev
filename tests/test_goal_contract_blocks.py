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

**A block is identified by its fence label, not by any of its own text.** That is the
whole trick, and it is load-bearing: a checker that keys on the text it is verifying
has one class of drift it cannot see — reword the line it matches on and the block
stops being a block, drops out of the comparison, and the survivors still agree. A
label makes identity separable from content, so the same edit surfaces as a second
variant. Body signatures survive only as a guard against the label being removed.

Five properties, because the contract has that many moving parts and locking down
only the goal block leaves the rest free to drift:

1. every shared block is one text wherever it appears;
2. every `dist/` copy carries the same blocks its `claude-plugins/` source does — a
   clause deleted outright from one distribution is silent otherwise;
3. every site arming a Manifest backstop carries the goal block;
4. every such site carries the instruction forbidding paraphrase — the block is only
   half the mechanism, and a prose-tightening pass that leaves fenced content alone
   would strip the other half without a signal;
5. no shared block has lost its label, which would make it invisible to (1) and (2).

The checks derive their own subject rather than listing today's sites, so a site added
later is covered without this file being edited.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

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
# Matched with `Path.match` so the separator stays platform-independent.
# See docs/adr/20260828-continuation-goals-emit-verbatim-from-one-block.md.
NO_MANIFEST_BACKSTOP = ("figure-out/references/autonomous.md",)

# The instruction that makes the block emit verbatim. Whitespace-normalized before
# comparison because it is line-wrapped at some sites and not at others, and the
# trailing pronoun differs between one-block and multi-block sites.
NO_PARAPHRASE = "Do not summarize, shorten, reword, or re-punctuate"

# The rule that keeps the fence label out of what the user sees. The labels exist so a
# block's identity is separable from its text; a site that emits them verbatim prints
# this file's own bookkeeping into someone's terminal. Checked for the same reason as
# NO_PARAPHRASE: it is prose sitting beside fenced content, so a pass that tightens
# prose can strip it without any block changing.
LABEL_NOT_EMITTED = "this file's markers rather than part of what you emit"

Label = Literal["goal-block", "gate-ledger-clause", "chain-prefix", "pr-tend-prefix"]

# Fence label -> a phrase from that block's body. The label is the identity; the
# signature exists only so `test_every_shared_block_is_labelled` can catch a block
# whose label was stripped, which would otherwise make it invisible again. Typing the
# keys as a closed union is what stops `GOAL_BLOCK` and a renamed key drifting apart.
SIGNATURES: dict[Label, str] = {
    "goal-block": "it changes only through the skill that wrote it, never by direct edit",
    "gate-ledger-clause": (
        "explicit or inherited verifier model, latest verdict, evidence"
    ),
    "chain-prefix": (
        "Treat a missing or weak Read checkpoint as a phase defect to repair "
        "before the Manifest is written"
    ),
    "pr-tend-prefix": "Never press merge. Report a wait-only CI state as pending",
}
GOAL_BLOCK: Label = "goal-block"

# The closing delimiter is backreferenced to the opener, so a four-backtick example
# wrapping a three-backtick block parses as one block rather than desynchronizing
# every fence after it. Thirteen shipped files already nest fences that way.
FENCE = re.compile(r"^(`{3,})([^\n]*)\n(.*?)^\1[ \t]*$", re.MULTILINE | re.DOTALL)


def read(path: Path) -> str:
    """Always UTF-8.

    The shipped prose is full of em dashes and curly quotes, so a runner with LANG
    unset would raise instead of returning a verdict — and a gate that errors is a
    gate that is not enforced.
    """
    return path.read_text(encoding="utf-8")


def shipped_markdown() -> list[Path]:
    """Every shipped markdown file, template plugin excluded."""
    return sorted(
        path
        for root in SEARCH_ROOTS
        if root.is_dir()
        for path in root.rglob("*.md")
        if TEMPLATE_PLUGIN not in path.parts
    )


def fenced_blocks(path: Path) -> list[tuple[str, str]]:
    """(fence label, block text) for every fenced block in the file.

    Built from explicit groups rather than `findall`, whose element type silently
    follows the pattern's group count — a `(...)` edit would otherwise change what
    every caller unpacks, with mypy still clean. Here it raises at this line.
    """
    return [(m.group(2), m.group(3)) for m in FENCE.finditer(read(path))]


def blocks_in(path: Path) -> set[Label]:
    """Which labelled shared blocks this file carries."""
    return {
        label for raw, _ in fenced_blocks(path) for label in SIGNATURES if raw == label
    }


def copies_by_block() -> dict[Label, dict[str, list[Path]]]:
    """label -> exact text -> the files carrying that text."""
    found: dict[Label, dict[str, list[Path]]] = {label: {} for label in SIGNATURES}
    for path in shipped_markdown():
        for raw, text in fenced_blocks(path):
            for label in SIGNATURES:
                if raw == label:
                    found[label].setdefault(text, []).append(path)
    return found


def backstop_sites() -> list[Path]:
    """Files arming a backstop that should carry the Manifest goal block."""
    return [
        path
        for path in shipped_markdown()
        if ARMS_A_BACKSTOP.search(text := read(path))
        and NAMES_THE_CAPABILITY.search(text)
        and not any(path.match(skip) for skip in NO_MANIFEST_BACKSTOP)
    ]


def source_skills() -> dict[str, Path]:
    """skill directory name -> its authored SKILL.md under claude-plugins/.

    Keyed by bare name because `dist/` lays the plugins out differently per target;
    `test_skill_names_are_unique_across_plugins` is what makes that key safe.
    """
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
    for label, variants in copies_by_block().items():
        if len(variants) > 1:
            listing = "\n".join(
                f"    {len(paths)} copy(ies): {', '.join(rel(p) for p in sorted(paths))}"
                for paths in sorted(variants.values(), key=len)
            )
            drifted.append(f"  {label}\n{listing}")
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


def test_skill_names_are_unique_across_plugins() -> None:
    """`source_skills` and `dist_copies` key on the bare skill name.

    Two plugins shipping a skill of the same name would silently drop one source
    from the parity check and compare the survivor against the other plugin's
    distribution. Cheaper to forbid the collision than to carry the ambiguity.
    """
    names: dict[str, list[str]] = {}
    for path in (ROOT / "claude-plugins").rglob("skills/*/SKILL.md"):
        if TEMPLATE_PLUGIN not in path.parts:
            names.setdefault(path.parent.name, []).append(rel(path))
    clashes = [f"  {n}: {', '.join(p)}" for n, p in names.items() if len(p) > 1]
    assert not clashes, (
        "these skill names exist in more than one plugin, so the name is no longer a "
        "safe key here:\n" + "\n".join(clashes)
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
        if normalized(NO_PARAPHRASE) not in normalized(read(p))
    ]
    assert not missing, (
        "these files emit a goal block without instructing that it not be reworded:\n"
        "  " + "\n  ".join(missing)
    )


def test_every_backstop_site_keeps_the_fence_label_out_of_the_emission() -> None:
    """Emitting a block verbatim must not mean emitting its fence label.

    The labels are identity markers for the checks in this file, not contract text. A
    site that says only "emit the block below verbatim" invites a faithful reader to
    print the fence and its label too, which is what a user reported seeing.
    """
    missing = [
        rel(p)
        for p in backstop_sites()
        if normalized(LABEL_NOT_EMITTED) not in normalized(read(p))
    ]
    assert not missing, (
        "these files emit a goal block without saying the fence label is not part of "
        "what to emit:\n  " + "\n  ".join(missing)
    )


def test_every_shared_block_is_labelled() -> None:
    """A shared block that lost its fence label would be invisible to every check."""
    unlabelled = [
        f"  {rel(path)}: a block matching {label!r} is labelled {raw!r}"
        for path in shipped_markdown()
        for raw, text in fenced_blocks(path)
        for label, sig in SIGNATURES.items()
        if sig in text and raw != label
    ]
    assert not unlabelled, (
        "these fenced blocks are shared contract blocks but are not labelled as "
        "such, so nothing compares them:\n" + "\n".join(unlabelled)
    )


def test_the_blocks_are_actually_present() -> None:
    """Guards the checks above from passing vacuously on an empty search."""
    found = copies_by_block()
    for label in SIGNATURES:
        carriers = [p for paths in found[label].values() for p in paths]
        assert carriers, f"no file carries the {label} block"
    assert backstop_sites(), "no file arms a completion backstop"
