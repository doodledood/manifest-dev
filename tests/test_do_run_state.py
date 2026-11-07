"""`/do`'s run state survives the events the environment can produce.

A run's state is instructions, not code: which evidence a verdict still stands on, which
log a relaunch opens, which path a run ends on. Each test here holds one rule whose absence
let a verdict outlive what it assessed, or let a run's record go somewhere a later launch
cannot find it. They pin the rule's wording in every shipped copy, since a copy that loses
the clause ships the hole again under the same skill name.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "claude-plugins/manifest-dev/skills"
CODEX = ROOT / "dist/codex/plugins/manifest-dev/skills"


def flat(relative: str) -> list[tuple[Path, str]]:
    """Every shipped copy of one skill file, whitespace-normalized."""
    copies = []
    for base in (SOURCE, CODEX):
        path = base / relative
        copies.append((path, re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))))
    return copies


# A gate broadened in place by an amendment kept its ID and its PASS: the next evaluation
# was a continued look, reporting only what the intervening code changes introduced, so
# unchanged code the broadened claim now covers was never judged, and a finding dismissed
# as outside the old claim stayed dismissed. A change to a gate's criteria — its text and
# the Manifest sections its claim reads — takes a new full look and reopens dispositions,
# and the ceiling, which reads the whole Manifest, re-verifies after every amendment.
def test_changed_criteria_take_a_new_full_look() -> None:
    for path, text in flat("do/SKILL.md"):
        assert (
            "When a judgment gate's criteria change, its next evaluation is a new full look"
            in text
        ), path
        assert (
            "A gate's criteria are its text and every Manifest section its claim reads"
            in (text)
        ), path
        assert "re-verifies after every amendment" in text, path
        assert "the ceiling when Appetite changes" not in text, path
        assert (
            "new code, changed criteria, argument or evidence can reopen them" in text
        ), path
    for path, text in flat("review-code/SKILL.md"):
        assert (
            "Criteria that changed since that evaluation make this a fresh review"
            in (text)
        ), (path)
        assert "changed code, criteria, argument or evidence can" in text, path
    for path, text in flat("do/references/LOG.md"):
        assert "taken its full look under its current criteria" in text, path


# `define` rewrites the Manifest in place and the Manifest carries no version. A run that
# stopped between that write and its next log entry resumed holding verdicts recorded by
# gate ID alone, so it kept PASS on text that had changed. Each verdict records the hash
# of the Manifest it read, an amendment is marked pending before `define` runs and closed
# after the re-read, and a resumed run trusts a verdict only where the hashes say its
# criteria did not move.
def test_a_resumed_run_detects_a_changed_manifest() -> None:
    for path, text in flat("do/references/LOG.md"):
        assert "## A changed Manifest" in text, path
        assert (
            "Record with each verdict the SHA-256 of the Manifest file it was assessed"
            " against" in text
        ), path
        assert (
            "append an `Amendment pending` entry carrying the current hash" in text
        ), path
        assert "and is otherwise unverified" in text, path
        assert "A pending entry left open means its amendment may not have landed" in (
            text
        ), path
    for path, text in flat("do/SKILL.md"):
        assert (
            "mark the amendment pending there before invoking `define` and close it after"
            " the re-read" in text
        ), path


# A caller-supplied journal (babysit-pr's) was the log, with nothing at the path `/do`
# keys to the Manifest. A launch without the caller — after compaction, in a new session,
# or resuming an escalation whose report named no log — opened that path, found it empty,
# and lost the dispositions, dead ends and full-look state. The Manifest-keyed path now
# points to the journal, and the escalation report names the log the resumed run reads.
def test_every_launch_on_a_manifest_finds_its_log() -> None:
    for path, text in flat("do/references/LOG.md"):
        assert "caller-supplied journal" in text, path
        assert (
            "Append one line to the path `SKILL.md` names pointing to that journal"
            in (text)
        ), (path)
        assert "follows its newest pointer and reads the journal" in text, path
        assert "no second file" not in text, path
    for path, text in flat("do/SKILL.md"):
        assert (
            "where a caller supplied a journal, by the pointer `references/LOG.md` → *Path*"
            in text
        ), path
        assert "and the execution log's path when one is kept" in text, path
    for path, text in flat("escalate/SKILL.md"):
        assert "Name the execution log's path when `/do` kept one" in text, path
        assert "with the log path this report named" in text, path


# Nothing claims a Manifest, so two `/do` runs on one file both amend it through `define`
# and the last write wins: run A reported done against a contract that was no longer in
# the file, and an amendment could vanish. Before amending and before reporting
# completion, the run compares the file's hash with the one it last read or wrote, and a
# difference makes the changed gates unverified and restores a lost amendment.
def test_a_manifest_changed_by_another_writer_is_noticed() -> None:
    for path, text in flat("do/SKILL.md"):
        assert "Hash the Manifest each time you read it" in text, path
        assert (
            "Before amending and before reporting completion, hash it again" in text
        ), path
        assert (
            "treat as unverified each gate whose criteria changed or can no longer be shown"
            " unchanged" in text
        ), path
        assert (
            "make again any amendment of this run's that the file no longer carries"
            in (text)
        ), path
