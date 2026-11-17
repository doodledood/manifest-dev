# ADR: Design-time probes cover what the reviewers can know, and every shipped default yields to the user's and the project's rules

## Status
Accepted — narrowed by 20261117-a-review-holds-work-to-the-projects-principles-unless-a-person-chose-the-departure: a project principle also raises findings where a shipped default raises none

## Area
Task guidance

## Decided by
The user

## Context
20261013-design-judgment-moves-to-design-time-as-task-file-probes moved part of the reviewers' judgment into figure-out's probes and define's Defaults, but not all of what can be known before code. A mapping of every reviewer's detection categories against the probes found categories knowable at design time that nothing prompted: shallow pass-through modules and options with no present use, reuse of what the framework, codebase, API documentation or context file already provides, which layer owns a decision and what belongs in configuration, call orders and ambient inputs a signature hides, one name with two meanings, growth per item, old and new versions running side by side during a deploy, concurrent runs, where a test's expected values come from, sources for a document's claims, and the empty, failed and stale states of anything a person sees. Each one found only after code costs a review round and a repair. figure-out had no probe file for user-visible artifacts or human-voiced writing, and one listed mirror pair had drifted: define carried no Default for several figure-out CODING probes, so direct and unattended runs skipped them.

20261013-the-users-rules-override-plugin-defaults let a stated rule override define's Defaults only. figure-out's probes and the reviewers' standards said nothing, so a reviewer could flag a change that followed the project's own convention.

## Decision
- A reviewer category that can be known before the artifact exists gets a design-time home: a figure-out probe and the define Default or gate that carries it into a Manifest. A category that needs the written artifact stays with the reviewer. Additions follow the earlier record's limits — one-line questions, only for angles a capable model skips — and fold into an existing line where one fits.
- A category a reviewer gains later brings its design-time probe, or the reason it has none, in the same change.
- figure-out gains probe files for user-visible artifacts and human-voiced writing, since it loads probes by topic and a code probe never loads for a deck or an essay.
- Every shipped default is an opinionated starting point. A rule the user stated, in the session or a context file, or a convention the project states or documents — not a pattern its code merely repeats — governs where it conflicts. A reviewer raises no finding against a change that follows such a rule and names the rule it applied; a critical failure — on each reviewer's own scale: data loss or a security breach in code, a critical functional or access failure in a design, a prompt that misses its goal, a CRITICAL finding on the writing register's own scale — is still reported, naming the rule that produced it. figure-out and define also read the context file's outcome rules — naming, structure, architecture — as constraints on the shape being designed, not only as overrides of defaults. Each skill states this once, where its defaults load.

## Alternatives Considered
- **One probe per reviewer category**: every probe costs attention on every run that loads its file; merged lines carry the same angles for less.
- **Leave it to the reviewers**: each finding then costs a review round and a repair that design time could have avoided.
- **State precedence once, in one skill, and point to it**: a shipped skill stands alone, so a skill that never loads the other would never see the rule.

## Consequences

### Positive
- More work passes review on the first round.
- A project's own conventions stop drawing findings.

### Negative
- figure-out's CODING file and define's CODING Defaults are longer.
- Two more figure-out files to keep in step with define's gates.

## Enforced by
partly — eval case `48-reuse-and-shallow-layer` measures the depth and reuse probes once run, and eval case `d21-user-rule-over-default` measures a stated rule overriding a Default. Whether a probe is needed, and whether a stated rule covers the case at hand, stay judgment.

## Source
- Session: investigation of design-time coverage of the reviewers' findings.
- Extends: 20261013-design-judgment-moves-to-design-time-as-task-file-probes
- Extends: 20261013-the-users-rules-override-plugin-defaults
