"""State rules of the pull-request skills that a run cannot recover from GitHub alone.

Each test holds one rule an audit of the skills' own state machines found missing, with the
counterexample it stops in its docstring. The rules are prompt text, so the tests check the
text in the source skill and its Codex copy.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = "manifest-dev-tools/skills"


def _copies(rel: str) -> list[Path]:
    return [
        ROOT / "claude-plugins" / TOOLS / rel,
        ROOT / "dist/codex/plugins" / TOOLS / rel,
    ]


def _text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_babysit_resumes_the_manifest_its_journal_recorded() -> None:
    """Run 1 synthesizes M1, the user amends M1, run 2 must tend M1, not a fresh M2.

    Without the resume rule, every run without `--manifest` asked define for a new lifecycle
    Manifest holding only the baseline gates, so /do never judged the amended gate.
    """
    for path in _copies("babysit-pr/SKILL.md"):
        text = _text(path)
        assert (
            "resume the Manifest an earlier tend of this PR recorded in its journal"
            in text
        ), path
        assert (
            "only when no recorded Manifest file still exists, invoke `define`" in text
        ), path
        assert (
            "Each run boundary records the Manifest path this run tends" in text
        ), path
        assert "pass `--manifest` to keep a tended Manifest" in text, path
        assert "`/do` is the sole journal consumer" not in text, path


def test_review_range_has_one_owner_with_the_descent_check() -> None:
    """A one-shot pass after a force-push must not review `old-head..new-head`.

    The one-shot rule used the prior review's head as the lower bound with no descent check,
    while the loop reference fell back to the full diff when the head no longer descended:
    after a rebase the one-shot range held commits outside the PR and missed rewritten ones.
    """
    for path in _copies("review-pr/SKILL.md"):
        text = _text(path)
        assert "**Review range.** The lower bound is the head our latest prior" in text
        assert "has moved past the bound and still descends from it" in text, path
        assert "no longer descends from the bound" in text, path
        assert "last-reviewed-by-us..current-head" not in text, path
    for path in _copies("review-pr/references/LOOP.md"):
        text = _text(path)
        assert "`SKILL.md` → *Review range*" in text, path
        assert "no longer descends" not in text, path


def test_a_thread_resolved_without_a_fix_is_verified_and_reopened() -> None:
    """The author resolves our defect thread with no fix; the next pass must not read it addressed.

    Only unresolved threads were verified, and consolidation pruned findings an existing thread
    covered, so a resolved-but-unfixed thread dropped out of tracking and the PR read as
    addressed.
    """
    for path in _copies("review-pr/SKILL.md"):
        text = _text(path)
        assert (
            "every thread opened by our finding that someone other than this account resolved"
            in text
        ), path
        assert (
            "| Disposition | Unresolved thread | Thread someone else resolved |" in text
        )
        assert "Reopen it, post the reply; keep it pending." in text, path
    for path in _copies("review-pr-thread-verify/SKILL.md"):
        text = _text(path)
        assert "whether the thread is resolved, and by whom" in text, path
        assert "A resolution is not a fix" in text, path
        assert "`still-pending` — The thread is unresolved" in text, path


def test_posting_prunes_against_marker_comments_read_just_before() -> None:
    """Two review-pr invocations on one PR at once must not both post the same findings.

    Each pruned against the PR as it read it at the start, so neither saw the other's
    comments and both posted.
    """
    for path in _copies("review-pr/SKILL.md"):
        text = _text(path)
        assert (
            "Just before submitting, re-read the PR's comments carrying our marker"
            in text
        )
        assert "a second invocation running on the same PR at once" in text, path


def test_a_thread_reply_already_posted_is_not_posted_again() -> None:
    """A pass stopped between posting a concession and resolving must not concede twice.

    The next pass found the thread still unresolved, got the same disposition and drafted
    reply back, and posted it again.
    """
    for path in _copies("review-pr/SKILL.md"):
        text = _text(path)
        assert (
            "Post a drafted reply only when, read fresh just before posting, our latest message"
            " on that thread does not already say it" in text
        ), path


def test_babysit_ci_runs_one_tend_per_pr_and_stops_on_a_moved_head() -> None:
    """Two `--ci` runs on one PR post duplicate replies; a rejected push had no next step.

    The CI cadence decision accepted that users may need concurrency controls, but the skill
    never told them, and nothing said what to do when a push came back non-fast-forward.
    """
    for path in _copies("babysit-pr/SKILL.md"):
        text = _text(path)
        assert "Run one tend per PR at a time" in text, path
        assert "a concurrency group keyed to the PR" in text, path
        assert "When a push is rejected as not a fast-forward" in text, path
        assert "push nothing from the stale checkout" in text, path
        assert "under `--ci`, end the run reporting the new head" in text, path


def test_babysit_backstop_stops_when_a_person_merges_the_pr() -> None:
    """A person merges the tended PR: /do now ends there, so the outer backstop must too.

    /do's own goal block stops on a person settling the work from outside, but the tend's
    prefix and goal block, which own the outer backstop, named only mergeable, a blocker or a
    terminal wait, so they held the run open on a merged PR.
    """
    for path in _copies("babysit-pr/SKILL.md"):
        text = _text(path)
        assert "until it is mergeable, a person merges it, or a blocker" in text, path
        assert (
            "or a person settling the work from outside, such as by merging its pull request"
            in text
        ), path
        assert "its *How a run ends* names" in text, path
        assert "stops via `/done`, `/escalate`, or CI pending-summary" not in text, path
