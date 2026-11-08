"""orchestrate sorts every Ticket in scope into exactly one category.

`orchestrate/SKILL.md`, Start step 5, puts each Ticket into the first category whose conditions
hold, "so it is in exactly one". First-match makes "at most one" automatic; "at least one" is the
claim that can break. A state that fits no category is a Ticket no orchestrator plans, launches or
lands again, and nothing tells the person: a ready pull request whose orchestrator stopped was
stranded that way.

`CATEGORIES` transcribes each category's conditions, quoting the sentences it encodes — in the
sort and in `AUTOMATED_EXECUTION.md` → *Transitions*, which owns each state it names; the quote
check fails when one of them leaves the skill, so the transcription changes with the prose. The
totality check then enumerates every consistent abstract state of an open Ticket and fails on any
that fits no category, printing the states.

Holds docs/adr/20261107-a-ready-mark-whose-orchestrator-stopped-is-adopted-not-relaunched.md.
"""

import itertools
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"
ORCHESTRATE = SKILLS / "orchestrate" / "SKILL.md"
AUTOMATED_EXECUTION = SKILLS / "ticket-up" / "references" / "AUTOMATED_EXECUTION.md"

State = dict[str, object]

# The facts the sort reads about one open Ticket. `owner` is whose run the run facts name (none: no
# attempt record); `outcome` is what that run left, a close included, since a closed Ticket a person
# reopened is open again.
DOMAIN: dict[str, list[object]] = {
    "assignee": ["none", "person", "auto"],
    "author_write": [True, False],
    "auto": [True, False],
    "mark": [True, False],
    "owner": ["none", "mine", "foreign"],
    "live": [True, False],
    "timed_out": [True, False],
    "outcome": ["none", "ready", "answer", "escalation", "close"],
    "merged_before_reopen": [True, False],
    "revision": [True, False],
    "deps": ["closed", "planned", "open"],
    "signpost": ["none", "met", "unmet", "unreadable"],
    "type_passes": [True, False],
}


def consistent(s: State) -> bool:
    if s["owner"] == "none":
        return (
            not s["live"]
            and not s["timed_out"]
            and s["outcome"] == "none"
            and not s["revision"]
        )
    # "A run is **live** until it writes an outcome, while ... its timeout has not passed"
    if s["live"] and (s["outcome"] != "none" or s["timed_out"]):
        return False
    return not (s["merged_before_reopen"] and s["outcome"] != "ready")


def left_alone(s: State) -> bool:
    return bool(
        s["assignee"] == "person"
        or (not s["author_write"] and not s["auto"])
        or s["mark"]
        or (s["owner"] == "foreign" and not s["timed_out"])
        or s["deps"] == "open"
        or s["signpost"] in ("unmet", "unreadable")
        or not s["type_passes"]
    )


def running(s: State) -> bool:
    return bool(s["live"])


def to_land(s: State) -> bool:
    # A foreign run reaching this point has timed out: left_alone took the rest.
    return (
        s["outcome"] == "ready"
        and s["owner"] in ("mine", "foreign")
        and not s["merged_before_reopen"]
    )


def answered(s: State) -> bool:
    return s["outcome"] == "answer" and not s["revision"]


def to_recover(s: State) -> bool:
    return s["assignee"] == "auto" and bool(
        s["outcome"] == "none"
        or (s["outcome"] == "escalation" and not s["mark"])
        or (s["outcome"] == "ready" and s["merged_before_reopen"])
        or s["outcome"] == "close"
        or s["revision"]
    )


def ready(s: State) -> bool:
    # "A Ticket whose open dependencies are all planned joins the plan behind them."
    return s["assignee"] == "none" and bool(s["auto"] or s["author_write"])


# Each category, in the skill's order, with the sentences its conditions encode: the sort's own,
# and the states and rows of AUTOMATED_EXECUTION.md → *Transitions* it names.
CATEGORIES: list[tuple[str, Callable[[State], bool], list[str]]] = [
    (
        "left alone",
        left_alone,
        [
            "*Left alone*, each with its reason: the state *Dispatchable* or row *Launch* asks "
            "for that it lacks, or the type filter.",
            "**Ready**: open, unclaimed, every Ticket it depends on closed, and, when it is "
            "deferred, its `Revisit when` condition read as met at the source it names",
            "**Dispatchable**: ready, not escalated, and either granted, written by an author "
            "with write access to the repository",
            "A run that is not yours belongs to another orchestrator until row *Take over* lets "
            "you take its Ticket; leave it alone until then",
            "| **Take over** | The run facts name another orchestrator's run whose timeout has "
            "passed |",
        ],
    ),
    ("running", running, ["*Running*: its run facts name a live run."]),
    (
        "to land",
        to_land,
        [
            "*To land*: ready to land and not reopened after its merge, under a run of yours or "
            "one you adopt before its landing turn (row *Adopt a ready mark*).",
            "| **Adopt a ready mark** | Ready to land, the timeout of the run that wrote the mark "
            "passed, and no live run |",
        ],
    ),
    (
        "answered",
        answered,
        ["*Answered*: an answer drafted, no trusted revision pending and no live run."],
    ),
    (
        "to recover",
        to_recover,
        [
            "*To recover*: the state of that name.",
            "**To recover**: held by automation, no live run, and the last run wrote no "
            "outcome, wrote an escalation whose mark is now gone, marked ready a pull request "
            "that merged before the Ticket was reopened, or closed the Ticket, which was then "
            "reopened; or a trusted revision request is pending.",
        ],
    ),
    (
        "ready",
        ready,
        [
            "*Ready*: dispatchable, and matching any type filter.",
            "A Ticket whose open dependencies are all planned joins the plan behind them.",
        ],
    ),
]


def category(s: State) -> str | None:
    return next((name for name, holds, _ in CATEGORIES if holds(s)), None)


def states() -> list[State]:
    every = (
        dict(zip(DOMAIN, values, strict=True))
        for values in itertools.product(*DOMAIN.values())
    )
    return [s for s in every if consistent(s)]


def flat(text: str) -> str:
    return " ".join(text.split())


def test_each_category_transcribes_sentences_that_still_stand() -> None:
    skill = flat(ORCHESTRATE.read_text(encoding="utf-8"))
    assert "Each Ticket takes the first category below whose conditions hold" in skill
    skill += " " + flat(AUTOMATED_EXECUTION.read_text(encoding="utf-8"))
    missing = [
        f"{name}: {quote}"
        for name, _, quotes in CATEGORIES
        for quote in quotes
        if flat(quote) not in skill
    ]
    assert not missing, (
        "orchestrate's sort changed under this transcription; update its category here:\n"
        + "\n".join(missing)
    )


def test_every_ticket_state_fits_a_category() -> None:
    gaps = [s for s in states() if category(s) is None]
    assert not gaps, f"{len(gaps)} states fit no category, for example:\n" + "\n".join(
        str(s) for s in gaps[:10]
    )


def test_a_ready_mark_whose_orchestrator_stopped_is_to_land() -> None:
    """The case that was stranded: another orchestrator's run marked ready, then it stopped."""
    s: State = {
        "assignee": "auto",
        "author_write": True,
        "auto": True,
        "mark": False,
        "owner": "foreign",
        "live": False,
        "timed_out": True,
        "outcome": "ready",
        "merged_before_reopen": False,
        "revision": False,
        "deps": "closed",
        "signpost": "none",
        "type_passes": True,
    }
    assert category(s) == "to land"
    assert category({**s, "timed_out": False}) == "left alone"


def test_a_ticket_its_own_run_closed_is_recovered_once_reopened() -> None:
    """A Question Ticket its Auto run closed, which a person then reopened."""
    s: State = {
        "assignee": "auto",
        "author_write": True,
        "auto": True,
        "mark": False,
        "owner": "mine",
        "live": False,
        "timed_out": False,
        "outcome": "close",
        "merged_before_reopen": False,
        "revision": False,
        "deps": "closed",
        "signpost": "none",
        "type_passes": True,
    }
    # The claim outlived the close: the run stopped between the two writes.
    assert category(s) == "to recover"
    # Released with the close, as the convention's *Closing* says, it is ready work.
    assert category({**s, "assignee": "none"}) == "ready"
