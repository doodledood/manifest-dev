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

**Manifest input defaults to one Shaped Ticket for the whole Manifest.** Its Deliverables remain an internal execution and verification structure. Split into one Ticket per Deliverable only when the caller explicitly asks for delegation or parallel pickup. Existing Deliverable boundaries are the smallest allowed split: if one is too large, amend the Manifest rather than slicing below a unit that can no longer be judged end to end.

**Question input gets a separate Question Ticket only when the question needs its own lifecycle.** A question that the current work can answer, or that merely records an execution choice, stays inside the containing Ticket. Related questions managed together become one Question Ticket. An explicit request to track or delegate a question establishes that separate lifecycle.

**Follow-up input remains distinct from the source obligation.** Current-scope work stays on the source Ticket; a blocker to its definition of done escalates it. Search the effort's open set first, fold the finding into an existing Ticket when it already covers the work, and group related new findings before authoring. Every emitted follow-up links back to its source and carries the same effort membership unless the finding genuinely belongs elsewhere.

## Translate knowledge, not machinery

A Ticket is a contract with a stranger who may not have manifest-dev. Rewrite the source into the convention's anatomy rather than excerpting it. Could a competent stranger holding only this Ticket understand why the work exists, know its bounds, avoid its traps, and judge it done? Manifest-dev vocabulary in an emitted Ticket fails that test.

For Manifest input, translate the full coherent outcome into one Ticket. Problem and Goal become Why; Appetite and Out of bounds become Scope; all applicable Global Invariants become plain Rules that must hold; risks and assumptions become Watch out for; the Initial Approach remains optional advice; every Deliverable and gate contributes to one plain-prose Definition of done. Gate kinds, verification modes, codes, and evaluator instructions stay behind.

In explicit split mode, apply the same translation to each Deliverable and copy every applicable Global Invariant into every Ticket. Do not emit the Manifest's ceiling invariant as a rule; its substance already lives in each Ticket's Scope.

## Auto grant

For an ordinary new Ticket, grant Auto only when neither doing the work nor judging it done needs human knowledge, taste, or authority, and the author chooses to trust unattended execution. When in doubt, withhold.

For a follow-up, first establish whether this `ticket-up` authoring boundary has a fresh human grant for Auto on the new Ticket. A person directly authoring here, or explicitly reviewing and authorizing Auto here, may grant the follow-up independently of its source after the follow-up passes the normal Auto criterion. The person still chooses whether to trust unattended execution; Shaped never implies Auto.

Without that fresh human grant, preserve authority rather than widening it: the source Ticket must carry Auto **and** the follow-up must independently pass the same grant criterion. An unattended or nested authoring step cannot turn an ungranted source into future unattended work. Merely invoking `run-ticket` manually on an ungranted source is not a fresh grant for follow-ups discovered inside that run; a person must separately authorize Auto at this authoring boundary.

Never copy Auto from the source without the independent check.

## Type and dependencies

Give each Ticket one type from the store vocabulary when one fits, otherwise none. For one-Ticket Manifest mode, use the chief nature of the complete work. In explicit split mode, type each Deliverable separately. Type never grants execution authority.

Encode `Depends on:` only when one Ticket's outcome is required to do or judge another. Preferred order is not a dependency. A follow-up that is merely related links to its source without blocking on it; add an edge only when the structural need exists.

## Choose and render the venue

Read `tickets/store-config.md` first. A project context file may name another fixed location. When neither does, ask once and recommend the project's shared tracker; GitHub Issues is the recommendation when the project has a reachable GitHub remote and no other tracker is in play. Recommend files only where no shared tracker exists or nobody else will pick work, and explain that claims do not cross clones, worktrees, or branches. Record the answer at `tickets/store-config.md`.

**Files.** Write each Ticket to `tickets/<effort-slug>/NN-<ticket-slug>.md`. Open with `Kind:`, `Status:`, `Depends on:`, and `Claimed by:`, plus `Auto: yes` when granted and `Type: <value>` when typed. Keep the effort's stable destination, priority override, and context pointers in `tickets/<effort-slug>/README.md`; never add a Ticket list or status summary. Closed Tickets move to `done/`.

**GitHub Issues.** Read `references/GITHUB_STORE.md` and follow its mapping.

**Any other tracker.** Read `references/GITHUB_STORE.md` for the required mapping rows, ask what supplies each capability, and write `tickets/<venue>-store.md`. Have `tickets/store-config.md` name the venue and reference that file. An unsupported tracker needs a venue reference, not a refusal.

Before outward-facing creation on a venue this project has not used before, show the planned Tickets, labels, tracking item, and relations and get confirmation. A configured venue already records that choice.

## Report

Present what was authored in a short table: ID, title, kind, type, Auto, and dependencies, plus where each Ticket landed. In Manifest mode, state whether the default coherent unit or explicit Deliverable split was used. In follow-up mode, include source links and which findings were grouped or deduplicated.

## Gotchas

- A gate may name evaluator machinery a stranger cannot use. Translate its substance into observable done prose.
- A list of small questions is not automatically a list of Question Tickets. The lifecycle test comes first.
- A discovered defect inside the current definition of done is unfinished source work, not a follow-up that makes the source closable.
- A follow-up still needs its own grant decision. Source Auto is required unless a person grants Auto freshly at this `ticket-up` boundary.
