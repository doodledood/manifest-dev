# ADR: New capabilities live inside figure-out, define, do, and auto, and maintain themselves during normal runs

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
Users invoke four skills: figure-out, define, do, and auto. Other skills run only when one of these calls them. A capability that needs its own invocation depends on a person remembering it, and in practice it does not run. The same holds for a maintenance pass that someone must schedule: many projects have no scheduler, CI job, or other infrastructure set up for it.

The concrete case was a project verification surface (a harness plus a feature map). It needs upkeep as the app changes. An upkeep skill that a person must remember goes unrun, and the surface goes stale.

## Decision
- Every new capability is reached through one of the four entry points: as a probe in a figure-out task file, as a Default or Quality Gate in a define task file, as a step inside do, done, or escalate, or as a reference that one of these loads (for example through init-context).
- A project surface that the workflow relies on is maintained during normal runs, when the work touches it. No capability assumes a scheduler, a CI job, or other infrastructure that the user set up.
- Skills outside the four may exist as steps that the four call, or as optional extras. The workflow never depends on a user remembering to invoke them.
- A capability the workflow depends on ships in the core plugin. Core skills call skills in the tools plugin only when those are available, so the workflow cannot depend on them.

## Alternatives Considered
- **Dedicated user-invoked skills** (create a verification harness, maintain it, sweep the repository for repeated corrections): each depends on a person remembering it, so it does not run.
- **Scheduled maintenance passes**: they need infrastructure that many users do not have, and nothing fails visibly when it is missing.
- **Ship such capabilities in the tools plugin**: core may call a tools skill only if it is installed, so a dependency there is optional by construction.

## Consequences

### Positive
- A user learns four names. Everything else arrives through them.
- Maintenance happens where work happens, with no setup step.

### Negative
- A surface that no run touches can go stale until a run touches it.
- The four entry points carry more content, so their task files and references grow.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260705-front-figure-out-as-door-define-do-loop-as-house
