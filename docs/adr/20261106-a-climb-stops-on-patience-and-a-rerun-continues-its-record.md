# ADR: A hill-climb stops after rounds with no confirmed gain, and a re-run continues its record

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled four things: a climb stops after rounds bring no confirmed gain; each round learns from the earlier ones; a re-run continues the climb rather than restarting it; and the record lives in the logs figure-out, define and do already keep. The agent drafted the final checks below from the cited sources.

## Context
An improvement loop needs an end it can justify:
- A fixed number of rounds stops a climb that is still gaining, or keeps going after one has stalled.
- Stopping at the first round without a winner quits before the proposals have learned from what lost.
- A run that keeps going after its gates hold breaks the North Star's *Quality decides* principle. So the stop has to be part of the climb's own contract.

OPRO (Yang et al., arXiv 2309.03409) ends when the model can no longer propose solutions that score better. Its proposals draw on the scored trajectory, so reaching that point means informed proposals still lose. Two more points shape how a climb finishes:
- A chain of pairwise wins does not show that the last version beats the first, because judged preferences are not transitive.
- A measure optimized hard enough eventually rewards what it was not meant to (Gao, Schulman and Hilton, arXiv 2210.10760). A result tuned to one measure therefore needs a check the climb did not optimize against.

A climb also ends without proof that its result works in use; only use can show that. `orchestrate` already continues, waits or finishes on outcome evidence across runs (`claude-plugins/manifest-dev/skills/orchestrate/references/OUTCOME.md`).

## Decision
- **The stop.** A climb stops after a set number of consecutive rounds with no confirmed gain. define sets that number for each climb. Every round's proposals draw on the full record, so reaching the stop means proposals that knew everything already tried still lost.
- **A requester's limit comes first.** A limit the requester sets, such as a number of rounds, ends a climb early. The report then says the climb stopped at that limit, not at a plateau.
- **Keeping the original counts as success.** A climb that finds nothing better reports that the original held against everything it tried.
- **The final checks.** Before a climb reports a better version, two checks must pass:
  - that version beats the original head to head, on fresh measurement;
  - it passes a final check the climb did not optimize against. That is held-out cases for a suite and guard measures for a number. For an AI judge, it is a judge from another model family where the host offers one.
- **The record continues across runs.** The record holds each candidate, its result and why it won or lost. It is kept in `/do`'s execution log and carried in the pull request description, where a re-run on any machine can read it. A re-run of the same climb continues from that record. If a re-run has nothing new to try (no new evidence, no direction the record lacks), it stops at once and says so.
- **What comes after.** A finished climb names the evidence from real use that would test its result. Pursuing that evidence across runs stays with `orchestrate`.
- **The stop gate looks backward.** Evaluating the stop gate checks the record and the final comparison. It does not propose new challengers of its own.

## Alternatives Considered
- **A fixed budget of rounds as the default stop.** Not chosen: it ends on the count rather than on the evidence. A requester can still set one as a limit.
- **Stop at the first round without a winner.** Not chosen: it quits before the proposals have learned from what lost.
- **Work through a fixed list of directions named at the start.** Not chosen: the list cannot grow from what the rounds teach.
- **Restart a re-run from the original.** Not chosen: it repeats candidates the record already rejected and spends the same rounds again.

## Consequences

### Positive
- A climb ends on its own evidence, and a re-run costs only what is new.
- A climb that finds nothing better still leaves a record of what was tried and why it lost.
- Reports claim only what was measured, and name what would show the rest.

### Negative
- The stop rule spends several rounds after the last gain before a climb can stop.
- A re-run depends on the pull request carrying the record. A climb without one restarts.
- The record grows with every round, and a long one has to be summarized without losing why candidates lost.

## Enforced by
not yet — `hillclimb` recipe scenarios for two cases: a re-run with nothing new stops at once, and a climb whose measure finds nothing better keeps the original.

## Revisit when
Re-runs of finished climbs keep finding confirmed gains that the first run stopped short of, or climbs run many rounds past their last gain; read in the climbs' pull request descriptions.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261106-an-ai-judge-compares-two-versions-and-never-scores, 20260805-ratchet-judgment-gate-reverification
