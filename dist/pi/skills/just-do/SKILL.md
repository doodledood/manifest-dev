---
name: just-do
description: 'Goal-based Manifest executor. Reads a Manifest and pursues it with full autonomy: reach a state where every Acceptance Criterion and Global Invariant holds, deciding for itself how to get there. Use when the user asks to just do a manifest, run it goal-based, or execute with minimal process.'
argument-hint: '<manifest-path>'
user-invocable: true
---

Read the Manifest at the given path in full; no path → halt with usage. Your
goal: bring the work to a state where every Acceptance Criterion and Global
Invariant holds, as written. How you get there — order, method, how much
checking and when — is yours to decide.

Acceptance Criteria and Global Invariants are the contract. The Initial
Approach and Process Guidance are advice — depart when the work is better
for it.

The Manifest is read-only. Never edit it. If a premise the Acceptance
Criteria or Global Invariants rest on has gone false, or the user redirects
beyond the Manifest, stop and say so — the user amends via /define and
relaunches. Advisory content gone stale is not a stop: departing from it is
already yours to decide.

Before starting work, arm the completion backstop. If a goal is already
active for this Manifest's path, continue under it. Otherwise, if the harness
provides a goal-setting, continuation, or durable-completion-condition
capability, set this goal: "Every Acceptance Criterion and Global Invariant
in <manifest-path> holds, with evidence from the artifacts the gates name,
and completion has been reported. The Manifest at that path is canonical and
read-only. Record compact checkpoint notes as work proceeds — what changed,
what was verified, what remains, blockers. Stop only when blocked on
something a person must resolve." If it provides none, print that
goal in copy-pasteable form for the user's own continuation mechanism and
proceed with the work. The goal names the Manifest by path and never carries
its content, so amending the Manifest never invalidates the goal.

When genuinely blocked on something only a person can resolve, stop and report
what you tried and what you need. When done, report what changed and your
basis for each Acceptance Criterion and Global Invariant holding.
