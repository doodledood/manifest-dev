# ADR: Unattended runs flag the user's calls by a disagreement test, not by their own confidence

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
An unattended run — autonomous figure-out, `/define` under `/auto`, `/do`, `run-ticket` — settles many calls with no person present. Some of those calls belong to the user: pricing, brand, a user-facing flow, a vendor, scope. Autonomous figure-out flagged a resolution as a Known Assumption only when its confidence was low, and `/do`, `/done`, `/escalate`, and `run-ticket` reported material decisions in no particular order. A user met each such call only in the shipped result.

A backtest over 40 recorded decisions measured the gap. Agents agreed with the owner on about 85% of agent-level technical calls, but on only 50 to 61% of the owner's own calls. The agent's own confidence did not separate its misses from its hits: "high" confidence agreed 71% of the time and "medium" 68%. So the low-confidence trigger never fired on the calls that mattered. A separate blind check asked one question of each call: "could two careful people with the same evidence reasonably decide this differently, and would the difference matter to the owner?" It caught 7 of 12 misses, and its split matched who actually decided — 12 of 18 owner calls flagged, 1 of 13 agent calls.

## Decision
One shared block defines **the user's call**: a decision where two careful people with the same evidence could reasonably decide it differently, and the difference would matter to the user. The run's confidence does not settle it.

- Autonomous figure-out flags every user's call, and every guess at a fact only the user holds, as a Known Assumption candidate. Before it names the read, it hands the resolved questions, answers removed, to a fresh context to classify. It classifies inline only where no isolated context exists, and says so.
- `/define` marks an `ASM-*` entry that records a user's call, so the user can find it.
- Every report of an unattended run's decisions lists the user's calls first, each with the alternative not taken and what decided it. This covers figure-out's read, the report and execution log of `/do`, `/done`, `/escalate`, and the pull-request description and DONE and ESCALATED records of `run-ticket`.
- Unattended runs still never ask and never wait. Flagging moves a call to where the user looks first; it does not stop the run.

The block is stated, word for word, in each skill that applies it, because a shipped skill cannot read another skill's text. A test fails when any copy differs.

## Alternatives Considered
- **Keep the low-confidence trigger**: the backtest showed confidence does not separate misses from hits, so it does not fire on the user's calls.
- **Ask the agent to predict the owner**: in the backtest, this recovered none of the owner's calls.
- **Give the agent more project records**: adding decision records, the North Star, and rules recovered about 2 of 18 owner calls.
- **Stop unattended runs at each user's call**: this defeats unattended execution. The user's calls are reported first instead, so a user reviews them before the rest.

## Consequences

### Positive
- A user finds the calls that were theirs at the top of each report, with the alternative they can still choose.
- The trigger is the one the backtest tested, and its split matched who actually decided.

### Negative
- The block repeats in six skill files; a test keeps the copies equal, and any change must touch them all.
- The blind check caught 7 of 12 misses, so some user's calls still pass unflagged.
- The separate classification pass costs one more context per autonomous figure-out run.

## Source
- Session: figure-out investigation with a backtest over recorded decisions; aggregate figures only.
- Related: 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals
- Related: 20260907-executors-own-unattended-decisions-within-explicit-bounds
- Amends 20260611-figure-out-spine-owns-epistemics-mode-refs-thin: the autonomous reference's Known Assumption trigger is the user's-call test, not low confidence.
