# ADR: A target of unknown reach binds a floor and advises an aim

## Status
Superseded by 20261106-source-authority-governs-acceptance-and-revision

## Area
define

## Decided by
The user

## Context
When a session wants a measurable result — "fast", "small", "quick to load" — and nobody has established how far it can go, `/define` must still write a gate that passes or fails. Binding the hoped-for number turns a wish into a requirement nobody checked, and `/do` then pursues it with no way to tell "not yet" from "not possible". The user's case: "fast" became a fixed FPS number, and `/do` kept trying to reach it. The user asked for such a target to stay "in a plausible range" rather than a hard number.

## Decision
A target whose reachability the session did not establish binds a floor and advises an aim. The gate holds the floor — a sourced specific like any other, or a behavior such as faster than a measured baseline — and the hoped-for value goes to Process Guidance as the aim, so the run reaches for it without being trapped by it. A number the user stated stays binding: attended, `/define` asks whether it is a firm requirement or an aim; unattended, it stays binding and an assumption records that its reachability was not established.

## Alternatives Considered
- **Bind the hoped-for number**: — Not chosen: it is the failure this decision exists to stop.
- **Bind only a measured improvement, with no aim**: — Not chosen: the run loses the direction the user wanted, and the aim costs nothing while it binds nothing.
- **A measurement-first Deliverable that sets the number mid-run**: — Not chosen: gate text changes only on the user's say-so, so an unattended run could not apply the number it measured.
- **Turn a user's stated number into an aim**: — Not chosen: an explicit requirement is the user's to relax, which is why attended `/define` asks.

## Consequences

### Positive
- A vague want yields a gate the run can pass, and the aim still steers it.
- The user meets an unchecked number of their own as a question before execution, not as a stall during it.

### Negative
- A floor such as "faster than the baseline" accepts a small gain the user may have hoped would be larger; the aim and the report carry that gap.

## Enforced by
partly — the define eval case `d25-vague-target` grades a vague speed want against an invented frame rate; whether a given Manifest follows the rule is judgment, which the fresh review of `20261018-define-reviews-each-new-manifest-in-a-fresh-context` also checks.

## Source
- Session: figure-out read and define run on 2026-10-18
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context, 20261018-do-names-the-evidence-that-puts-a-gate-out-of-reach, 20260727-gate-text-changes-on-the-users-say-so
