---
name: ticket-up
description: 'Author self-sufficient Tickets in the project''s store from a finished Manifest, a direct work request, an open question, or follow-up findings from another Ticket. A Manifest becomes one coherent Shaped Ticket by default; split it by Deliverable only when the caller explicitly wants delegation or parallel pickup. Use when creating Tickets, ticketing up a plan, recording follow-up work, or handing work to a teammate, agent, or later session.'
---

# ticket-up

`ticket-up` is the single Ticket-authoring boundary. It shapes prose, applies the convention, deduplicates, and renders the result through the project's configured venue.

Read `references/TICKET_CONVENTION.md` before emitting. It defines the unit, kinds, anatomy, lifecycle, and priority every venue must preserve.

## Resolve the input and Ticket units

Accept any of these inputs:

- a finished Manifest;
- a direct work request that should enter the store;
- one or more questions that need separate management;
- findings discovered while running a source Ticket, with that source identified.

Without explicit input, use a recent Manifest only when the conversation already establishes it as the intended source; otherwise ask what should become a Ticket.

One Ticket represents one independently schedulable lifecycle. Bundle work that shares one outcome and would be assigned, prioritized, and closed together. Split only where separate ownership, priority, blocking, or closure has real value. Do not turn every Deliverable, question, or minor finding into a Ticket.

Whether to split is one question; where the cut falls is another, and the second is answered the same way whatever the input was. Every Shaped Ticket a split produces is a slice someone can exercise end-to-end on its own — run, read, or otherwise judged in the situation it is for, not merely inspected as present. A Ticket cut along an implementation layer ("the schema", "the endpoints", "the screen") has nothing to run, so its definition of done falls back to checking that something exists and whoever picks it up cannot tell whether the work helped. Re-cut work that arrives framed in layers instead of passing the layers through; renaming a layer does not re-cut it, and a requested layer cut settles scope, not where the cuts fall, so keeping its layers is never a user's call: its scope is kept and its layers re-cut. A Question Ticket is outside this — an investigation has no slice to run, and its done is the answer recorded.

**Manifest input defaults to one Shaped Ticket for the whole Manifest.** Its Deliverables remain an internal execution and verification structure. Split into one Ticket per Deliverable only when the caller explicitly asks for delegation or parallel pickup. Existing Deliverable boundaries are the smallest allowed split: if one is too large, or is a layer rather than something exercisable end to end, amend the Manifest rather than shipping a unit that cannot be judged end to end.

**Question input gets a separate Question Ticket only when the question needs its own lifecycle.** A question that the current work can answer, or that merely records an execution choice, stays inside the containing Ticket. Related questions managed together become one Question Ticket. An explicit request to track or delegate a question establishes that separate lifecycle.

**Follow-up input remains distinct from the source obligation.** Current-scope work stays on the source Ticket; a blocker to its definition of done escalates it. Search the effort's open set first, fold the finding into an existing Ticket when it already covers the work, and group related new findings before authoring. Every emitted follow-up links back to its source and carries the same effort membership unless the finding genuinely belongs elsewhere.

## Translate knowledge, not machinery

A Ticket is a contract with a stranger who may not have manifest-dev. Rewrite the source into the convention's anatomy rather than excerpting it. Could a competent stranger holding only this Ticket understand why the work exists, know its bounds, avoid its traps, and judge it done? Manifest-dev vocabulary in an emitted Ticket fails that test.

For Manifest input, translate the full coherent outcome into one Ticket. Problem and Goal become Why; Appetite and Out of bounds become Scope; all applicable Global Invariants become plain Rules that must hold; risks and assumptions become Watch out for; the Initial Approach remains optional advice; every Deliverable and gate contributes to one plain-prose Definition of done. Gate kinds, codes, and evaluator instructions stay behind.

In explicit split mode, apply the same translation to each Deliverable and copy every applicable Global Invariant into every Ticket. A Deliverable that is a layer rather than something exercisable end-to-end is amended in the Manifest first, per the cut rule above. Do not emit the Manifest's ceiling invariant as a rule; its substance already lives in each Ticket's Scope.

## Auto grant

Grant Auto only when neither doing the work nor judging it done needs human knowledge, taste, or authority, and the grantor chooses to trust unattended execution. When in doubt, withhold.

Two grantors exist. A person grants: directly authoring here, or explicitly reviewing and authorizing Auto for the Ticket here. `orchestrate --autonomous` grants too: it invokes this skill for a Ticket an agent wrote — a debt Ticket it authored, or a follow-up a run wrote — and grants only where the criterion above holds. Record the grantor with the grant, as the venue renders it, so a person can tell an `orchestrate` grant from their own and withdraw it.

A follow-up gets Auto only from one of those grants at this boundary. Without one it carries no Auto, whatever its source carries. The run that found the work never grants it, and merely invoking `run-ticket` manually on a source is not a grant for follow-ups discovered inside that run. Shaped never implies Auto.

Never copy Auto from the source.

## Type, dependencies and deferral

Give each Ticket one type from the store vocabulary when one fits, otherwise none. For one-Ticket Manifest mode, use the chief nature of the complete work. In explicit split mode, type each Deliverable separately. Type never grants execution authority.

Encode `Depends on:` only when one Ticket's outcome is required to do or judge another. Preferred order is not a dependency. A follow-up that is merely related links to its source without blocking on it; add an edge only when the structural need exists.

When the work is to wait until something holds in the world rather than until another Ticket closes — a number crossing a line, a release shipping, a date passing — write the convention's `Revisit when` line: the condition and where it is read, as the venue maps it. Name a source a picker can read, such as a dashboard, a file, a release page or a date; a condition no picker can read keeps the Ticket in front of the person on every pick. A deferral is never a `Depends on:` entry, and a preferred order is never a deferral.

## Choose and render the venue

Read `tickets/store-config.md` first. A project context file may name another fixed location. When neither does, ask once and recommend the project's shared tracker; GitHub Issues is the recommendation when the project has a reachable GitHub remote and no other tracker is in play. Recommend files only where no shared tracker exists or nobody else will pick work, and explain that claims do not cross clones, worktrees, or branches. Record the answer at `tickets/store-config.md`.

**Files.** Read `references/FILE_STORE.md` and follow its mapping.

**GitHub Issues.** Read `references/GITHUB_STORE.md` and follow its mapping.

**Any other tracker.** Read `references/GITHUB_STORE.md` for the required mapping rows, ask what supplies each capability, and write `tickets/<venue>-store.md`. Have `tickets/store-config.md` name the venue and reference that file. An unsupported tracker needs a venue reference, not a refusal.

Before outward-facing creation on a venue this project has not used before, show the planned Tickets, labels, tracking item, and relations and get confirmation. A configured venue already records that choice.

## Report

Present what was authored in a short table: ID, title, kind, type, Auto and its grantor, dependencies, and any `Revisit when` condition, plus where each Ticket landed. In Manifest mode, state whether the default coherent unit or explicit Deliverable split was used. In follow-up mode, include source links and which findings were grouped or deduplicated.

## Gotchas

- A gate may name evaluator machinery a stranger cannot use. Translate its substance into observable done prose.
- A list of small questions is not automatically a list of Question Tickets. The lifecycle test comes first.
- A discovered defect inside the current definition of done is unfinished source work, not a follow-up that makes the source closable.
- A follow-up carries Auto only when a person, or `orchestrate --autonomous` under the criterion, grants it at this `ticket-up` boundary; its source's Auto never carries over.
