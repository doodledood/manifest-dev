# ADR: A figure-out wrapper sweeps existing code for state machines and checks each one

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
State machines hide in application code. Some are explicit: a status type with a transition table. Many are implicit: one status column set by if/else branches in several files, or two boolean flags whose combination is illegal. Their defects live between distant sites. Each site looks correct alone, so the bug shows only when every writer and every event are seen together.

manifest-dev looks for these only at the change in front of it. figure-out's `tasks/CODING.md` *Design discipline* probe asks, for a change being designed, whether a structure such as a state machine should replace branches spread across files. review-code checks a diff: `code-bugs` traces the other writers of a value the diff touches, `change-intent` asks about transition gaps, and `type-safety` flags missing discriminants. Nothing looks at state machines in code that no current change touches.

The owner ran the plain prompt "find all of the implicit state machines in my app" on one of their projects, outside any skill, and it found bugs and risks. That is one run on one project.

20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks rejected a formal-verification skill: a person must know to reach for it, and a design-time probe reaches every coding task instead. That reason holds for designs. It did not weigh latent defects in code that no change touches, which no design-time probe can reach.

## Decision
- A thin discovery wrapper skill invokes figure-out with `--autonomous` and a brief: sweep the repository for implicit and explicit state machines, rebuild each one — its states, the events that move it, every site that writes it — and check it. It takes `figure-out-team`'s wrapper shape: figure-out's discipline carries the investigation, and the wrapper adds only the brief.
- The check is sized to the risk: first an exhaustive walk of every state against every event in a scratch script, and a model checker (such as TLA+ or Alloy) where several writers can interleave. A counterexample becomes a finding only once it is confirmed on the real code — each site by file and line, and the sequence that reaches the bad state — because the model is the run's translation of the code and can be wrong. A model run that finds nothing is reported as what it covered, never as proof.
- The read reports the findings and offers ticket-up, which records them as Tickets carrying debt. The wrapper changes no code.
- The scope is state machines, implicit and explicit, worded to hold in any stack. Other defects that live between distant sites — state with two writers, lists kept in sync by hand, a hidden call order — are outside it.
- The sweep and review use one check text, so the lens cannot drift between them (20261107-review-checks-the-whole-state-machine-a-change-touches).

## Alternatives Considered
- **A stand-alone skill with its own investigation method**: rejected — it would rebuild what figure-out already does: evidence status on each claim, rival explanations, a read with confidence, the ticket-up offer.
- **A whole-tree mode of review-code**: rejected — it adds a mode to a skill built around reviewing a change, and invites whole-tree runs of every other dimension.
- **A figure-out probe file for sweep topics, with no wrapper**: rejected — the fewest parts, but a person must still know to ask for the sweep, which is the gap.
- **A personal skill outside manifest-dev**: rejected — other users never get it, and the owner's Taste prefers a default every user gets.
- **One sweep for the whole class of defects between distant sites**: deferred — only the state-machine lens has evidence, and the owner's Taste generalizes the wording, not the machinery.

## Consequences

### Positive
- Latent state-machine defects in existing code get a way to be found, with evidence, and a path into Tickets.
- The sweep inherits figure-out's investigation discipline with no new method.

### Negative
- A new skill: its description loads in every session, and it needs a recipe and a drive.
- A sweep of a large repository is a long autonomous run; how it divides the repository is the run's judgment.
- The evidence for the lens is one run on one project.

## Enforced by
partly — `tests/test_audit_state_machines.py` fails when the wrapper stops invoking figure-out with `--autonomous` and `--no-docs`, or when the audit and review stop sharing one statement of the method in `review-code/references/code-bugs.md` → *State machines*; `tests/test_entry_points.py` keeps the wrapper listed beside the skills it names. Whether a sweep confirms each planted defect and spares the sound machine stays judgment, read in `verification/recipes/audit-state-machines.md`'s `courier` drive.

## Revisit when
A sweep on a second project returns mostly findings that cannot be confirmed on the code, read in that sweep's report.

## Source
- Session: a figure-out session on whether six prompts for coding agents that the owner came across belong in manifest-dev's core (2026-11-07).
- Related: narrows 20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks; see also 20261013-design-judgment-moves-to-design-time-as-task-file-probes, 20261107-review-checks-the-whole-state-machine-a-change-touches
