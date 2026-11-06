# ADR: A hill-climb stops after rounds with no confirmed gain, and a re-run continues its record

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled five things: a climb stops after rounds bring no confirmed gain, by default two in a row; a quick climb stops at the first; each round learns from the earlier ones; a re-run continues the climb rather than restarting it; and the record lives in the logs figure-out, define and do already keep. The agent drafted the final checks below from the cited sources.

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
- **The stop.** A climb stops after consecutive rounds with no confirmed gain: by default two in a thorough climb and one in a quick climb. define may set another number for a climb. Every round's proposals draw on the full record, so reaching the stop means proposals that knew everything already tried still lost. The round that would meet the stop includes a bold attempt; in a climb that makes one change a round, that change is the bold one. With a staged measure, the stop counts full-measure confirmations, not cheap-check rounds.
- **A requester's limit comes first.** A limit the requester sets, such as a number of rounds, ends a climb early. The report then says the climb stopped at that limit, not at a plateau.
- **Keeping the original counts as success.** A climb that finds nothing better reports that the original held against everything it tried, and names the smallest difference its measure could detect.
- **The final comparison.** Before a climb reports a better version, that version beats the original head to head, on fresh measurement, before a judge independent of the loop. For a number or a suite, that is a fresh measurement plus checks the climb did not optimize against, such as held-out cases. For an AI judge, it is a judge that took no part in the rounds: from another model family where the host offers one in a thorough climb, and a fresh judge comparing in both orders in a quick one. A staged climb compares on the full measure, and several objectives are shown one by one against the original.
- **The record continues across runs.** The record keeps one line per attempt (what changed, the result on each objective, kept or why not), with older losing attempts rolled into one line per round once it passes 50 lines; kept versions, confirmations and what was recorded before round 1 stay whole, since the gates are judged on them. It lives in `/do`'s execution log, or in a file in the project the requester names so a re-run on another machine finds it, with the Manifest naming where; and in the pull request description only where the requester had the work pushed. A re-run finds the earlier climb's Manifest and amends it through define, reading the record, plus any results from real use the requester supplies, and proposes nothing it rejected. With nothing new to try, it stops before proposing.
- **What comes after.** A finished climb names the evidence from real use that would test its result. A climb toward a behavior hands its leading versions over for such a test, and a later run reads the results as its measure. That hand-over is the one change of measure that continues the record rather than starting a new climb: the record marks the switch, and versions kept on the offline measure count as candidates until those results confirm them. Pursuing that evidence across runs stays with `orchestrate`.
- **The stop gate looks backward.** Evaluating the stop gate checks the record and the final comparison. It does not propose new challengers of its own.

## Alternatives Considered
- **A fixed budget of rounds as the default stop.** Not chosen: it ends on the count rather than on the evidence. A requester can still set one as a limit.
- **Stop at the first round without a winner, in every climb.** Not chosen for a thorough climb: it quits before the proposals have learned from what lost. It is the quick climb's default, where the requester wants a fast improvement and the report says a thorough climb would go further.
- **Work through a fixed list of directions named at the start.** Not chosen: the list cannot grow from what the rounds teach.
- **Restart a re-run from the original.** Not chosen: it repeats candidates the record already rejected and spends the same rounds again.

## Consequences

### Positive
- A climb ends on its own evidence, and a re-run costs only what is new.
- A climb that finds nothing better still leaves a record of what was tried and why it lost.
- Reports claim only what was measured, and name what would show the rest.

### Negative
- The stop rule spends several rounds after the last gain before a climb can stop.
- A re-run on another machine finds the record only where the work was pushed; otherwise it starts a new record.
- Rolling older rounds into one line each can lose detail on why an early candidate lost.

## Enforced by
`tests/test_hillclimb.py` (`test_stop_rule_defaults_and_rerun_continue_the_record`) fails when the define task file drops the stop defaults, the bold attempt before stopping, the re-run's stop with nothing new, or the record's bound. Whether a climb kept its record faithfully stays judgment, read in the `hillclimb` recipe's re-run and already-at-its-best scenarios.

## Revisit when
Re-runs of finished climbs keep finding confirmed gains that the first run stopped short of, or climbs run many rounds past their last gain; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own, 20260805-ratchet-judgment-gate-reverification
