# Ticket Convention

A ticket is a self-sufficient prose work packet: everything needed to pick it up, do it, and judge it done — readable by a person or an agent, with or without manifest-dev. The convention is the contract; a venue (files, GitHub Issues, any tracker) is a rendering of it. Nothing may depend on a venue feature beyond what a venue reference maps.

## The Ticket unit

A Ticket is one independently schedulable lifecycle unit. Work belongs together when it shares one outcome and would be assigned, prioritized, blocked, and closed together. A separate Ticket earns its coordination cost only when managing it separately has real value.

Whether to split is one question; where the cut falls is another. Wherever work does split, every shaped ticket it produces stands as a slice someone can exercise end to end on its own — run, read, or otherwise judged in the situation it is for, not merely inspected as present. A ticket cut along an implementation layer — the schema, the endpoints, the screen — has nothing to run, so its definition of done falls back to checking that something exists, and whoever picks it up cannot tell whether the work helped. Work that arrives framed in layers is re-cut rather than passed through; renaming a layer does not re-cut it, and a requested layer cut settles scope, not where the cuts fall, so keeping its layers is never a user's call: its scope is kept and its layers re-cut. A question ticket is outside this: an investigation has no slice to run, only a question to answer.

A finished Manifest therefore becomes one Shaped Ticket by default. Its Deliverables guide execution inside that Ticket. A caller who explicitly wants delegation or parallel pickup may split on those existing Deliverable boundaries, so far as each one is exercisable end to end; where one is a layer rather than a slice that runs, the manifest is amended rather than that boundary shipped as a ticket. The same rule applies to findings and questions: group related items, and do not turn every thought or observation into store state.

## Two kinds

The kinds split on one question: is the decision space closed?

- **Shaped ticket** — every decision that shapes the work is already made: no open question remains whose answer would change what gets built or what done means. Someone picks it up and builds; its definition of done says when they're finished.
- **Question ticket** — at least one such question is still open. Someone picks it up and investigates; done means the question is answered with evidence and the answer recorded. Resolving one often spawns shaped tickets.

The kind test applies after the Ticket unit is justified. A separate Question Ticket exists only when the question needs independent assignment, priority, blocking, or closure. Then try to name a question whose answer would change the work or its definition of done. Naming one makes that unit a Question Ticket, however much context it already carries — half-investigated work is a Question Ticket with a thick "what's already known", not a Shaped Ticket. Choices where any competent answer within the Ticket's stated rules is acceptable — naming, internal structure, mechanical detail — are execution, not shaping, and leaving them open does not reopen the kind.

The bar is a property of the ticket's content, never of where it came from: no particular workflow or artifact needs to have produced a shaped ticket, and none makes a ticket shaped while such a question stays open.

The kind is declared on the ticket, so the picker knows which tool to bring.

## The Auto grant

A ticket of either kind may carry **Auto** — an opt-in grant, given by its grantor as *Who grants* below says,
that unattended automation may take it end to end: do the work, judge it done, and complete any
required landing, with nobody watching. For repository work, end to end includes merging through
the repository's normal protections before the Ticket closes.

- **Granting.** Grant only when neither doing the work nor judging it done needs any human's knowledge, taste, or authority — no done-judgment resting on someone's unstated criteria, no approval, no access an unattended worker won't have, no irreversible act that requires separate human authority beyond the Auto grant, no decision deferred to mid-flight input. Ordinary landing through the repository's declared protections is within Auto; a repository policy that requires human approval is not. That bar is necessary but never sufficient: whoever grants still chooses, and withheld trust alone is reason enough to withhold. When in doubt, don't grant.
- **Who grants.** A person grants: the ticket's author, or someone reviewing it, at the `ticket-up` boundary. `orchestrate --autonomous` also grants, to a ticket an agent wrote, wherever the bar above holds. The run that found the work never grants it. Every grant names its grantor on the ticket, so a person can tell an `orchestrate` grant from their own and withdraw it.
- **Absence means a person finishes it.** A ticket without the grant may still be worked by automation, but never completed or landed by it. Unattended work takes it up only when its author has write access to the repository and no person is assigned to it; the run asks for the person's judgment through the escalation mark wherever it needs it, and stops at a ready pull request — or, for a question ticket, with its answer drafted — for a person to land or accept. A ticket whose author lacks write access is never worked unattended, until a person with write access grants it Auto or approves a plan that includes it. Items in a shared venue that were never tickets stay untouched. Nothing is ever marked "not auto" to keep automation off; silence already says it. A person may also hand an ungranted ticket to an agent and watch — that is the person working the ticket.
- **Surprises don't revoke.** A granted ticket's worker can still hit an unexpected blocker; it stops and surfaces rather than deciding what only a person can. That is the exception path working, not evidence the grant was wrong — only a step known at write time to need a person keeps the grant off.

Auto is durable authority, not mutable queue state. Claiming, retrying, completing, or escalating
an attempt does not remove and reapply it. Open state, claim ownership, and dependencies determine
whether a granted Ticket is runnable. A person directly invoking `run-ticket` on an ungranted
Ticket supplies authority for that supervised run; that does not grant later unattended work.

A follow-up — separate work a run found — receives Auto only through a grant at its own `ticket-up` boundary, after it passes the granting test above: a person's, or `orchestrate --autonomous`'s. Without that grant it carries no Auto, whatever its source carries, and the run that found the work never grants it. A person merely invoking `run-ticket` on a source is not that grant. Whoever grants still chooses; Shaped never implies Auto.

## Type

A ticket may also say what kind of work it is: **bug**, **feature**, **refactor**, **docs**, or **chore**. This is a different question from the two kinds above — the kind says whether the work is decided, the type says what the work is — so a ticket can be shaped or question and carry any type, or none.

- **What each covers.** `bug` — something behaves wrongly and should stop. `feature` — something the product couldn't do before. `refactor` — the same behaviour, differently arranged. `docs` — prose: guides, references, comments, anything written to be read. `chore` — upkeep: dependencies, configuration, tooling.
- **One value, or none.** A ticket names the single type that best describes its work, never several. Where the work genuinely spans two, name the one that covers most of it. Where none of them fits, leave the type off — it is optional, and a ticket without one is a complete ticket.
- **Silence is not a wildcard.** Anything selecting tickets by type — a person filtering the store, or unattended automation given a set of types to work through — passes over a ticket that carries none. A ticket answers only to a type it actually names, so leaving it off is the safe thing to do rather than a gap someone else's query will fill in.
- **A project may use its own set.** These five are a default for stores that don't say otherwise. A project that thinks in different terms writes its own list in the same record that says where its store lives, and that list is then the list.

The type says what a ticket is, never what should be done about it. Which types are worth handing to unattended automation, and in what order anyone widens that, is the decision of whoever runs the automation and belongs wherever they say which tickets to pick up — never on the ticket, which would freeze one operator's policy into work everyone reads.

## Anatomy

A shaped ticket carries, in plain language:

- **Title** — specific to this work, not generic.
- **Why** — the problem this slice relieves and what it must achieve. Enough context that a stranger understands the point without reading anything else.
- **Scope** — how big a change this is worth, and what not to touch.
- **Rules that must hold** — every store-wide rule, copied into every ticket rather than referenced, so a picker who reads only their ticket still knows them.
- **Watch out for** — assumptions that may be wrong, known traps, concepts the picker needs.
- **Suggested approach** *(optional)* — a starting direction, marked as advice the picker may discard.
- **Definition of done** — checks a stranger can judge for themselves, in prose.
- **Depends on** — ticket IDs this one needs finished first. Structural needs only.
- **Revisit when** *(when deferred)* — a condition in the world the work waits for, and where it is read: "the weekly sign-up count passes 50, read on the analytics dashboard". A ticket carrying it is deferred: not worth starting until the condition holds, though no ticket blocks it. A condition another ticket's close settles is a dependency instead. This line is the ticket's signpost, and a picker reads it at the source it names (see *Ready*).
- **Auto** *(when granted)* — the grant above, naming its grantor; a ticket that doesn't carry it is ungranted. A recorded withhold, withdrawal or decline grants nothing and tells `orchestrate --autonomous` the ticket was already judged, so it is not granted again; a person's decline or withdrawal also removes the grant itself, as the venue renders it.
- **Type** *(when one fits)* — one of the types above, naming what kind of work this is; omitted when none of them describes it.
- **Status / Claimed by** — see lifecycle.

A question ticket carries Title, the question itself, why it matters, what's already known, and dependencies/the signpost/the Auto grant/type/status/claim the same way. Its definition of done is built in: the question answered with evidence, recorded where the store says outcomes go.

**No machinery.** A ticket never contains tool-specific vocabulary a stranger wouldn't know: no verification YAML, no gate codes, no references to the manifest or workflow that produced it. If interpreting a ticket requires installing something, the ticket is wrong.

**Write for the shelf.** A ticket may sit open while the codebase moves under it. Describe interfaces and behavior — what changes, and how a stranger can tell it worked — not file paths and line numbers, which go stale; name a file only when the file itself is the deliverable.

## The front file

Each effort's store carries one small front file (in a file store, a README beside the tickets; in a tracker, the tracking item's body) holding only content that doesn't change as tickets close:

- **Destination** — what reaching the end of this effort looks like, in a line or two. Pickers use it to judge what project value is delayed when a Ticket waits.
- **Priority rule override**, when the effort ranks differently than the default below.
- **Context pointers** — the key decision records, and where the effort's reads or logs live, so a cold picker gets effort-level orientation before opening a ticket.
- **Standing automation settings**, when set — a pause line that stops unattended work from starting anything new in the effort, and the link to its status page. `orchestrate` reads and writes them.

Never put derivable state here: no ticket lists, statuses, or ready/next — anything a close would stale belongs to the tickets themselves, where it can't rot. Where a tracker groups its items natively, that grouping is the tracker's to keep current rather than a list anyone edits.

## Lifecycle

- **Status**: `open` → `done`. Done tickets roll off **by location**: in a file store, closing moves the ticket into a `done/` subfolder beside the open ones; in a tracker, closing the item removes it from open queries. Reading the open set never scales with closed history — the archive is the `done/` folder, the tracker's closed items, and git.
- **Claiming**: mark a ticket claimed (a `Claimed by:` line, an assignee, the venue's equivalent) when you pick it, not when you get around to starting it — the gap between the two is where somebody else picks the same one. Open and unclaimed means takeable; a human claim pauses automation. A claim held by the store's stable automation identity represents work in progress, work waiting to land, or an interrupted attempt; whether a run still holds the ticket is read from the run facts its attempt record carries, never from the claim (`AUTOMATED_EXECUTION.md`).
- **Ready**: a ticket is ready when it is open, unclaimed, every ticket it depends on is done, and — when it is deferred — its `Revisit when` condition reads as met at the source it names. Every picker reads that source each time it sorts the store, so a condition that comes true is noticed by the next pick rather than by whoever happens to remember it. A deferred ticket whose source the picker cannot read is not ready and not out of sight: the picker names it to the person with that source, and never edits the line on the strength of a source it could not read. Blocked and deferred are derived from unmet dependencies and unmet conditions, never stored as a status. Readiness is the same question for everyone; unattended execution narrows it further with the escalation mark and with the grant or its author's write access, per *Automated execution* below.
- **Closing**: record the outcome on the Ticket (the merged or otherwise landed work, or the question's recorded answer), mark it done and roll it off (move it to `done/`, or close the item), and check what the close changed: Tickets it made ready, and outcomes that need interpreting. A branch or mergeable pull request is not a landed repository outcome. Create a Question Ticket for interpretation only when that question needs an independently managed lifecycle; otherwise record or answer it with the current outcome.
- **Escalating an attempt**: record the blocker, attempts, evidence, preserved-work references, and the human input needed on the same Ticket, as a handoff record carrying a mark automation can recognize. Leave it open, retain Auto when present, and release the claim. The mark, not a claim, is what holds automation off: unattended dispatch skips a marked Ticket, while the Ticket stays open and unclaimed so a picker ranks it against everything else and the person named in the handoff can take it. A venue reference maps how the mark renders — a label where the venue has them, and otherwise the marker the handoff record itself carries, which any venue can hold. After resolving the blocker, that person records the continuation context and clears the mark — or answers in `orchestrate`'s conversation, which records it and clears the mark for them — and clearing the mark also clears any claim automation left on it, which returns the Ticket to unattended eligibility. Escalation ends an execution attempt, not the Ticket's work, and never makes dependents ready.

## Automated execution

`orchestrate` is the unattended dispatch path. It runs ready Tickets, each through `run-ticket` in
its own session, recovers interrupted attempts from the run facts on each Ticket, and lands
finished work one Ticket at a time. A person may still run `run-ticket` by hand on any Ticket.

Unattended dispatch never touches a Ticket carrying the escalation mark, and tests for it where it
decides: releasing the claim leaves an escalated Ticket looking like ordinary ready work, so a
skipped test restarts the attempt the escalation ended. Closing one Ticket makes a dependent ready
for the next check-in; no ready label or label pulse is needed.

The attempt record, the completion record and the one landing procedure are in
`AUTOMATED_EXECUTION.md`. They live on the Ticket, not in Ticket fields a person edits.

## Priority

A store may state a different priority rule; that explicit rule wins. Otherwise choose among ready Tickets by **expected project value lost while work waits**, not by a fixed urgency, unblocking, impact, or cheapness ladder.

Compare the strongest candidates in the orderings that actually compete. If A goes first, ask what project value is lost while B waits for the constrained resource A occupies; reverse the comparison for B first. Prefer the ordering with lower expected loss. Count material consequences of delay: ongoing or expiring harm, durable benefit that starts later, downstream work whose earliest useful start actually moves, and information whose later arrival worsens or delays a material decision. These are causes of the same loss, not independent scores to add twice.

That comparison needs an estimate worth trusting, and one shape of effort cannot supply one. Three things are true of it at once: a Ticket's payoff arrives long after the work; no one can tell afterwards which Ticket produced which part of the result, because the channel mixes every Ticket's contribution with movement nobody controls; and most Tickets return almost nothing while a few carry the effort. Where all three hold — content libraries and discovery portfolios are the usual shape — a per-Ticket estimate is invented, and ranking two invented numbers ranks nothing. Miss any one of them and the default still works: outcomes that arrive late but land attributably can still be estimated, and so can a slow, evenly-paying effort.

Such an effort states its own rule in its front file: spread the picks across the kinds of work it does, rank inside a kind by something a picker can observe without predicting the outcome, and judge the spread over a batch of closed Tickets rather than per Ticket. The picker names those kinds itself, from the work actually in front of it, and reads the recently closed set to see which have gone untouched; a shortage there breaks a tie the observable leaves even. That is why the front file carries the rule rather than a roster of kinds — a roster becomes the shape every later pick gets matched into, and can hold only what was obvious the day it was written. Ranking inside a kind is that observable, not a delay-loss comparison in miniature — the estimate is no more trustworthy for the narrower field. A picker meeting a qualifying effort whose front file states no such rule picks by the default and says the effort needs one, rather than inventing a spread mid-pick. Everywhere the three do not hold together, per-Ticket comparison stays right.

Where a Ticket's payoff is unknown and a cheap look would settle it, rank the look by its upside against what looking costs, rather than by the expected value of the work it might justify. On that footing a probe can outrank a well-understood Ticket worth more in expectation: its value is the commitment it lets the project avoid, which the expected value of the work never prices. Cheap is relative to the work it would settle — a look costing most of what building costs settles nothing worth having. This is not the delayed-information cost above, which prices information for a decision already known to be pending.

Use current **executor-native serial time** only when duration materially changes what another Ticket loses by waiting. For a human-facing picker, the constrained time is interactive human attention until the human-dependent uncertainty or authority is resolved; routine implementation an AI can continue afterward is not human duration. For unattended work, use current end-to-end agent execution and landing time. Do not infer days from traditional feature size or apply a fixed agent-speed multiplier. When plausible runtimes are all short relative to the value consequences, treat them as effectively equal; shorter work is then only a tiebreak.

Unless the conversation explicitly scopes an effort or the store declares an intentional effort order, a human-facing picker compares ready Tickets across efforts and reads the relevant effort destinations to judge the consequences. Continuity with an effort already in flight is only a tiebreak. Auto is not intrinsic priority, but it can affect allocation when project context or configured automation establishes that unattended capacity is actually available soon enough to take that work; the marker alone proves authority, not that such a runner exists. Type is never a priority input.

An unattended picker first applies its own eligibility boundary — including Auto and configured filters — then uses the same delay-loss rule for new work inside that set. Recovery of an interrupted owned attempt remains ahead of starting new work because it is lifecycle recovery, not a fresh backlog choice.

## Dependencies and parallelism

Edges are structural only: B depends on A when B genuinely cannot be done or judged without A's outcome. Never encode a preferred working order as a dependency. The cost of parallel pickup is honest and accepted: with one worker, surprises in an early ticket reshape later ones; with parallel workers they don't — only the edges carry ordering, so anything learned that should reshape another ticket must be written onto that ticket when it's learned.

Claiming is what keeps two workers off one ticket, and it does that only where the store is a surface both of them read. A hosted tracker is one. Files in a repository are not, once the workers aren't in the same working copy: a claim written in one clone, worktree, or branch doesn't reach the others until it's merged, so two people can hold the same ticket and neither can tell. Parallel workers on a file store need to be sharing a checkout; otherwise the store belongs somewhere all of them can see it.

## Tidy pass

Occasionally — after a few closes, or when the store feels stale — check it: done tickets closed, stale claims released, statuses honest, priorities still pointing at the effort's goal, tickets that events made moot removed. Anyone can tidy; there is no keeper.
