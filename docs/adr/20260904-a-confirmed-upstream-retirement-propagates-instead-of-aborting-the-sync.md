# ADR: A confirmed upstream retirement propagates through the sync instead of aborting it

## Status
Accepted

## Area
Repo layout

## Context

This repository consumes components from `claude-code-plugins` through the `sync-claude-code-plugins` skill. The skill copies agents and skills from that repository's `prompt-engineering` plugin into `.claude/`, and records what it copied in `.claude/.claude-code-plugins-sync.json`. Its deletion invariant is deliberately narrow: only items in that tracked set are eligible for removal when they disappear upstream, which is how project-local content in `.claude/` stays safe from a sync it never opted into.

On 2026-08-17 the upstream repository retired the whole `prompt-engineering` plugin — three agents and three skills, ruled *capability lost, not capability moved*. Five of those six had been synced here on 2026-05-05 and were still present. The shipped `review-pr` skill still told reviewers to reach for two of the retired agents, in the plugin source and in the generated Codex distribution alike, so every prompt-review run was directed at tooling that no longer existed anywhere.

The tracked set listed all five retired components, so the deletion invariant should have reclaimed them on the next sync. It could not, because of the step before it. The pre-flight aborted when the source plugin directory was missing, on the rule that *silent absence is a misconfigured path, not upstream removal*. That rule was right about the risk it guarded — deleting a tracked set because someone mistyped a path, or ran against a half-finished clone, destroys files no run restores. It was wrong in treating one signal as one situation. A retired plugin and a bad path produce an identical absence, so the machinery built to reclaim retired components refused to run in precisely the case it existed for, and went on refusing indefinitely.

The failure is silent in both directions. Nothing here reported a stale copy, and nothing upstream knew this repository had consumed the components at all.

## Decision

Split the missing-source signal into the two situations that produce it, and let a confirmed retirement propagate.

A missing source directory still aborts by default. It stops being an abort only when the source repository's own history confirms a deliberate removal: a healthy full clone, a commit deleting the plugin directory, and a decision record stating the retirement. All of those are required together — a directory absent from a healthy clone with no such history is still read as misconfiguration. Where the evidence cannot be obtained, the abort branch is taken. Aborting costs a stale copy that a later run fixes, and deleting on a wrong reading costs files no run restores, so the asymmetry decides the ambiguous case.

On confirmation the sync runs with an empty source listing. The retired items are then removed by the ordinary `tracked − source` rule rather than by a second deletion path — the invariant that protects untracked content is unchanged, and confirmation only lets the existing rule see a case it was already written for.

The retirement denylist is extended from two entries to seven, covering every component the upstream ruling retired, so an older upstream checkout that still ships them cannot reintroduce them by a copy.

## Alternatives Considered

- **Delete the five components by hand and leave the sync alone.** Rejected: it fixes this instance and leaves the mechanism that stranded it. The next whole-plugin retirement upstream drifts exactly the same way, silently, and is found the next time someone reads a skill that points at something gone.
- **Retire `sync-claude-code-plugins` along with the plugin.** The skill's only source is the retired plugin, so it is arguably machinery with no remaining input, and deleting it would close this drift surface absolutely. Rejected for now: `claude-code-plugins` still exists and may ship something worth consuming again, and the skill carries the territory model for that relationship — the tracked-set discipline and the symlink-safety rules that make a one-way sync into a shared directory safe at all. That knowledge is worth more than the skill costs to keep. Worth revisiting if the relationship stays dormant.
- **Drop the abort entirely and treat a missing source as removal.** Rejected: it inverts the asymmetry above. A mistyped path or a partial clone would delete the tracked set, and the tracked set is the only record of what was consumed.
- **Enforce the rule with a script or a test rather than skill prose.** Rejected as heavier than the class it closes. The sync is an agent-run procedure with no scheduled execution, and a checker would need its own clone of the source repository to say anything useful. The rule an agent reads at the moment it faces the signal is proportionate to a decision made a handful of times a year.

## Consequences

### Positive
- A whole-plugin retirement upstream now reaches this repository through the machinery already built for it, instead of stalling at the pre-flight.
- The protection against a mistyped path or a partial clone is unchanged; the abort narrowed rather than weakened, and the ambiguous case still takes the safe branch.
- The denylist now names every retired component, so the reintroduction risk from a stale upstream checkout is closed for all of them rather than two.

### Negative
- Confirming a removal requires reading the source repository's history, so the sync now depends on the source clone being complete rather than merely present. A shallow or sparse checkout takes the abort branch and reports a stale state a fuller clone would resolve.
- The judgment sits in prose an agent must follow, with nothing mechanical enforcing it. A run that skips the confirmation step and deletes anyway would not be caught here.
- One component of the class is untouched: this repository is itself an upstream for others, and a retirement made here reaches them only through their own sync skills, which live in their repositories and are out of scope for this decision.

## Source
- Session: propagating the upstream 2026-08-17 retirement into this repository, where the stalled pre-flight was found to be the reason the ruling had not arrived
- Related: enforces `claude-code-plugins`' `20260817-prompt-engineering-plugin-retired`, which retired the plugin this sync consumed
