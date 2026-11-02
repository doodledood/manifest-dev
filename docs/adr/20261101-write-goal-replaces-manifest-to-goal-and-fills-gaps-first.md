# ADR: write-goal replaces manifest-to-goal, takes any source, and fills its gaps before writing

## Status
Accepted

## Area
Goal setting

## Decided by
The user, for the name, the sources, filling gaps both through figure-out and by direct question, keeping the skill experimental in the tools plugin with no offer from other skills, reviewing the goal as a contract when no Manifest is among the sources, dropping the old name with no alias, and merging the change. An agent under the user's delegation for this change ("take it from here. Merge when done"), with no review, for where the stop-point gap is drawn, the major version bumps, and amending rather than superseding the earlier record.

## Context
`manifest-to-goal` turned only a Manifest into a goal of at most 4,000 characters. A person who had worked a problem out with figure-out, and wanted to hand the work to a host's goal field, had to run /define first. A figure-out read, a Ticket, a handoff or a plain request could not become a goal, and such a source often leaves out the done check or the stop point; with nothing to fill that gap except invention, the goal would make the invention binding. The method `20261025-manifest-to-goal-lists-what-the-goal-owes-and-has-it-read-cold` set — a list of what the goal owes, a draft from it, one cold reading, the bare fence — does not depend on the source being a Manifest. One part of it does: when the source is a Manifest, /define has already reviewed the contract — whether its conditions can all hold, and whether work that misses the outcome would still pass them — so the cold reader checks only fidelity. A goal written from a read is the first written contract for that work, and nobody has reviewed it.

The skill is an experiment. Its first question is whether a goal, pursued through a host's goal capability, can stand in for a Manifest paired with /do. Its second is what happens when understanding goes straight to a goal, with no Manifest at all.

## Decision
The skill is renamed `write-goal` and the old name is removed with no alias. It takes a Manifest, a figure-out read, a Ticket, a handoff, a plain request, or several together, and states what each owes: a Manifest's gates as before; a read's conclusion, what it says will be built and how it will be checked, with each ruled-out branch stated as an exclusion and its evidence, rivals, overturn conditions and unaccepted offers treated as grounds; any other source's settled decisions.

Before listing, it tests that the sources settle the finished outcome, a done check a reader of the goal alone could settle, the limits, and where the work stops. The stop is a gap only when the work would reach an act that cannot be undone or needs approval — merging, deploying, sending, spending — and the source does not say whether to take it; a done check that is the end settles it. A gap that is one clear question is asked directly, one short answer at a time and only about these items. A gap that needs investigation, or cannot yet be put as one question, goes to figure-out with these items as its assignment; its read joins the sources and the test runs again. Where figure-out is not installed, the skill says so and asks, or stops without a goal. No gap is filled by invention.

The rest of the earlier record's method stands, with "the Manifest" read as "the sources"; the cold reader is handed the sources as text, and the draft marks advice it keeps for interpretation as a suggestion. Where no Manifest is among the sources, the same cold reader also reviews the goal as a contract: conditions that cannot all hold together within the stated scope, and holes — a requirement the goal states that no check in it settles, or a check that already passes on the current state while the outcome is missing. A finding the sources cannot settle is a gap, filled the same two ways. The skill stays in manifest-dev-tools while experimental, and figure-out and /define do not offer it.

## Alternatives Considered
- **Names `to-goal` or `goal`**: — Not chosen: `to-goal` reads less like a command, and `goal` clashes with a host's own `/goal` command.
- **Move it to the core plugin and offer it after figure-out and /define**: — Not chosen: the skill is still experimental.
- **Fill every gap through figure-out**: — Not chosen: a read aims at understanding and can stay loose where a goal needs a precise check or stop, so a gap that is one clear question is better asked directly.
- **Fill every gap by direct question**: — Not chosen: a question cannot investigate a gap that cannot yet be stated.
- **Require every source to name a stop point**: — Not chosen: a complete Manifest whose done check is the end would then trip the test.
- **A fidelity-only cold read for every source**: — Not chosen: a goal from a read would go out with no review of whether its checks can tell the outcome from its absence.
- **A second, separate contract reviewer**: — Not chosen: one context already reads the goal cold, and the earlier record chose one context to keep each conversion's cost down.
- **The contract review on Manifests too**: — Not chosen: /define already reviewed the Manifest, and a goal that fixed it would add requirements nobody agreed to.
- **Keep `manifest-to-goal` as an alias**: — Not chosen: the user wanted no backwards compatibility, and a second name misleads about what is live.

## Consequences

### Positive
- A figure-out read, a Ticket or a request becomes a goal without a Manifest in between.
- A goal never carries a done check or stop point the sources and the user did not settle.

### Negative
- `/manifest-to-goal` stops working; manifest-dev-tools moves to 7.0.0.
- A goal written from a read carries none of /define's task-file quality gates unless the sources state them; Manifest → goal remains the path that has them.
- Filling a gap through figure-out costs a figure-out session before the goal.

## Enforced by
partly — the `write-goal` recipe's scenarios: `convert` and `fresh-review` drive the Manifest path and require no gap-filling on a complete Manifest; `from-read` drives a read with a ruled-out branch and an unaccepted offer; `sharp-gap` requires a direct question for an unsettled merge; `fills-gaps` requires figure-out on a done check only the user can settle; `weak-check` requires the goal held back when its only check passes the unchanged code. Whether a run draws each gap correctly stays judgment.

## Revisit when
Runs of goals written by this skill, read in their pull requests' rework and in the work's own checks, show whether a goal can stand in for a Manifest paired with /do; that evidence decides whether the skill leaves experimental status.

## Source
- Session: figure-out read and `/auto` run on 2026-11-01
- Related: amends 20261025-manifest-to-goal-lists-what-the-goal-owes-and-has-it-read-cold
