# Ticket Convention

A ticket is a self-sufficient prose work packet: everything needed to pick it up, do it, and judge it done — readable by a person or an agent, with or without manifest-dev. The convention is the contract; a venue (files, GitHub Issues, any tracker) is a rendering of it. Nothing may depend on a venue feature beyond what a venue reference maps.

## The Ticket unit

A Ticket is one independently schedulable lifecycle unit. Work belongs together when it shares one outcome and would be assigned, prioritized, blocked, and closed together. A separate Ticket earns its coordination cost only when managing it separately has real value.

A finished Manifest therefore becomes one Shaped Ticket by default. Its Deliverables guide execution inside that Ticket. A caller who explicitly wants delegation or parallel pickup may split on those existing Deliverable boundaries. The same rule applies to findings and questions: group related items, and do not turn every thought or observation into store state.

## Two kinds

The kinds split on one question: is the decision space closed?

- **Shaped ticket** — every decision that shapes the work is already made: no open question remains whose answer would change what gets built or what done means. Someone picks it up and builds; its definition of done says when they're finished.
- **Question ticket** — at least one such question is still open. Someone picks it up and investigates; done means the question is answered with evidence and the answer recorded. Resolving one often spawns shaped tickets.

The kind test applies after the Ticket unit is justified. A separate Question Ticket exists only when the question needs independent assignment, priority, blocking, or closure. Then try to name a question whose answer would change the work or its definition of done. Naming one makes that unit a Question Ticket, however much context it already carries — half-investigated work is a Question Ticket with a thick "what's already known", not a Shaped Ticket. Choices where any competent answer within the Ticket's stated rules is acceptable — naming, internal structure, mechanical detail — are execution, not shaping, and leaving them open does not reopen the kind.

The bar is a property of the ticket's content, never of where it came from: no particular workflow or artifact needs to have produced a shaped ticket, and none makes a ticket shaped while such a question stays open.

The kind is declared on the ticket, so the picker knows which tool to bring.

## The Auto grant

A ticket of either kind may carry **Auto** — an opt-in grant, declared when the ticket is written,
that unattended automation may take it end to end: do the work, judge it done, and complete any
required landing, with nobody watching. For repository work, end to end includes merging through
the repository's normal protections before the Ticket closes.

- **Granting.** Grant only when neither doing the work nor judging it done needs any human's knowledge, taste, or authority — no done-judgment resting on someone's unstated criteria, no approval, no access an unattended worker won't have, no irreversible act that requires separate human authority beyond the Auto grant, no decision deferred to mid-flight input. Ordinary landing through the repository's declared protections is within Auto; a repository policy that requires human approval is not. That bar is necessary but never sufficient: the author still chooses, and withheld trust alone is reason enough to withhold. When in doubt, don't grant.
- **Absence is the fence.** A ticket without the grant is not touched by automation at all — no partial work, no prepping half the job. Nothing is ever marked "not auto"; silence already says it, which is also what keeps automation off items in a shared venue that were never tickets. A person may still hand an ungranted ticket to an agent and watch — that is the person working the ticket, outside the grant's jurisdiction.
- **Surprises don't revoke.** A granted ticket's worker can still hit an unexpected blocker; it stops and surfaces rather than deciding what only a person can. That is the exception path working, not evidence the grant was wrong — only a step known at write time to need a person keeps the grant off.

Auto is durable authority, not mutable queue state. Claiming, retrying, completing, or escalating
an attempt does not remove and reapply it. Open state, claim ownership, and dependencies determine
whether a granted Ticket is runnable. A person directly invoking `run-ticket` on an ungranted
Ticket supplies authority for that supervised run; that does not grant later unattended work.

A follow-up authored without a fresh human Auto grant at its own `ticket-up` boundary receives Auto only when its source carries Auto and the follow-up independently passes the granting test above. This keeps unattended and nested execution from widening its own authority. A person merely invoking `run-ticket` on an ungranted source does not change that rule for follow-ups discovered inside the run.

A person directly authoring the follow-up through `ticket-up`, or explicitly reviewing and authorizing Auto at that authoring boundary, may grant the new Ticket independently of source Auto after it passes the same granting test. The person still chooses whether to grant; Shaped never implies Auto.

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
- **Auto** *(when granted)* — the grant above, declared by the author; a ticket that doesn't carry it is ungranted, and nothing marks the negative.
- **Type** *(when one fits)* — one of the types above, naming what kind of work this is; omitted when none of them describes it.
- **Status / Claimed by** — see lifecycle.

A question ticket carries Title, the question itself, why it matters, what's already known, and dependencies/the Auto grant/type/status/claim the same way. Its definition of done is built in: the question answered with evidence, recorded where the store says outcomes go.

**No machinery.** A ticket never contains tool-specific vocabulary a stranger wouldn't know: no verification YAML, no gate codes, no references to the manifest or workflow that produced it. If interpreting a ticket requires installing something, the ticket is wrong.

**Write for the shelf.** A ticket may sit open while the codebase moves under it. Describe interfaces and behavior — what changes, and how a stranger can tell it worked — not file paths and line numbers, which go stale; name a file only when the file itself is the deliverable.

## The front file

Each effort's store carries one small front file (in a file store, a README beside the tickets; in a tracker, the tracking item's body) holding only content that doesn't change as tickets close:

- **Destination** — what reaching the end of this effort looks like, in a line or two. Pickers use it to judge what project value is delayed when a Ticket waits.
- **Priority rule override**, when the effort ranks differently than the default below.
- **Context pointers** — the key decision records, and where the effort's reads or logs live, so a cold picker gets effort-level orientation before opening a ticket.

Never put derivable state here: no ticket lists, statuses, or ready/next — anything a close would stale belongs to the tickets themselves, where it can't rot. Where a tracker groups its items natively, that grouping is the tracker's to keep current rather than a list anyone edits.

## Lifecycle

- **Status**: `open` → `done`. Done tickets roll off **by location**: in a file store, closing moves the ticket into a `done/` subfolder beside the open ones; in a tracker, closing the item removes it from open queries. Reading the open set never scales with closed history — the archive is the `done/` folder, the tracker's closed items, and git.
- **Claiming**: mark a ticket claimed (a `Claimed by:` line, an assignee, the venue's equivalent) when you pick it, not when you get around to starting it — the gap between the two is where somebody else picks the same one. Open and unclaimed means takeable; a human claim pauses automation. A claim held by the store's stable automation identity represents work in progress or an interrupted attempt the scheduled recovery path may resume after the host's single-flight guard admits it.
- **Ready**: a ticket is ready when it is open, unclaimed, and every ticket it depends on is done. Blocked is derived from unmet dependencies, never stored as a status.
- **Closing**: record the outcome on the Ticket (the merged or otherwise landed work, or the question's recorded answer), mark it done and roll it off (move it to `done/`, or close the item), and check what the close changed: Tickets it made ready, and outcomes that need interpreting. A branch or mergeable pull request is not a landed repository outcome. Create a Question Ticket for interpretation only when that question needs an independently managed lifecycle; otherwise record or answer it with the current outcome.
- **Escalating an attempt**: record the blocker, attempts, evidence, preserved-work references, and human input needed on the same Ticket. Leave it open, retain Auto when present, and transfer or preserve its claim for human continuation. The human records continuation context and releases the claim after resolving the blocker; the ordinary readiness rule then returns the Ticket to unattended eligibility. Escalation ends an execution attempt, not the Ticket's work, and never makes dependents ready.

## Automated execution

Issue events are a fast path for ready Auto Tickets. A scheduled `sweep-tickets` invocation is the
correctness path: it resumes one interrupted automation-owned Ticket, or otherwise selects one
ready Auto Ticket, invokes `run-ticket`, and stops. Closing one Ticket naturally makes a dependent
Ticket eligible for a later sweep; no ready label or label pulse is needed.

Both paths use one trigger adapter contract: stable automation identity, canonical per-Ticket
single-flight, finite provider retries, and one terminal infrastructure-failure handoff to a
configured person. Those are runner responsibilities, not Ticket fields. See
`AUTOMATED_EXECUTION.md` for the integration boundary.

## Priority

A store may state a different priority rule; that explicit rule wins. Otherwise choose among ready Tickets by **expected project value lost while work waits**, not by a fixed urgency, unblocking, impact, or cheapness ladder.

Compare the strongest candidates in the orderings that actually compete. If A goes first, ask what project value is lost while B waits for the constrained resource A occupies; reverse the comparison for B first. Prefer the ordering with lower expected loss. Count material consequences of delay: ongoing or expiring harm, durable benefit that starts later, downstream work whose earliest useful start actually moves, and information whose later arrival worsens or delays a material decision. These are causes of the same loss, not independent scores to add twice.

That comparison needs an estimate worth trusting, and one shape of effort cannot supply one. Three things are true of it at once: a Ticket's payoff arrives long after the work; no one can tell afterwards which Ticket produced which part of the result, because the channel mixes every Ticket's contribution with movement nobody controls; and most Tickets return almost nothing while a few carry the effort. Where all three hold — content libraries and discovery portfolios are the usual shape — a per-Ticket estimate is invented, and ranking two invented numbers ranks nothing. Miss any one of them and the default still works: outcomes that arrive late but land attributably can still be estimated, and so can a slow, evenly-paying effort.

Such an effort states its own rule in its front file: a mix across the classes of work it does, each class ranked by something a picker can observe without predicting the outcome, and the mix revised against results read over batches rather than per Ticket. Ranking inside a declared class is that observable, not a delay-loss comparison in miniature — the estimate is no more trustworthy for the narrower field. A picker meeting a qualifying effort that has not declared a rule picks by the default and says the effort needs one, rather than inventing a mix mid-pick. Everywhere the three do not hold together, per-Ticket comparison stays right.

Where a Ticket's payoff is unknown and a cheap look would settle it, rank the look by its upside against what looking costs, rather than by the expected value of the work it might justify. On that footing a probe can outrank a well-understood Ticket worth more in expectation: its value is the commitment it lets the project avoid, which the expected value of the work never prices. Cheap is relative to the work it would settle — a look costing most of what building costs settles nothing worth having. This is not the delayed-information cost above, which prices information for a decision already known to be pending.

Use current **executor-native serial time** only when duration materially changes what another Ticket loses by waiting. For a human-facing picker, the constrained time is interactive human attention until the human-dependent uncertainty or authority is resolved; routine implementation an AI can continue afterward is not human duration. For unattended work, use current end-to-end agent execution and landing time. Do not infer days from traditional feature size or apply a fixed agent-speed multiplier. When plausible runtimes are all short relative to the value consequences, treat them as effectively equal; shorter work is then only a tiebreak.

Unless the conversation explicitly scopes an effort or the store declares an intentional effort order, a human-facing picker compares ready Tickets across efforts and reads the relevant effort destinations to judge the consequences. Continuity with an effort already in flight is only a tiebreak. Auto is not intrinsic priority, but it can affect allocation when project context or configured automation establishes that unattended capacity is actually available soon enough to take that work; the marker alone proves authority, not that such a runner exists. Type is never a priority input.

An unattended picker first applies its own eligibility boundary — including Auto and configured filters — then uses the same delay-loss rule for new work inside that set. Recovery of an interrupted owned attempt remains ahead of starting new work because it is lifecycle recovery, not a fresh backlog choice.

## Dependencies and parallelism

Edges are structural only: B depends on A when B genuinely cannot be done or judged without A's outcome. Never encode a preferred working order as a dependency. The cost of parallel pickup is honest and accepted: with one worker, surprises in an early ticket reshape later ones; with parallel workers they don't — only the edges carry ordering, so anything learned that should reshape another ticket must be written onto that ticket when it's learned.

Claiming is what keeps two workers off one ticket, and it does that only where the store is a surface both of them read. A hosted tracker is one. Files in a repository are not, once the workers aren't in the same working copy: a claim written in one clone, worktree, or branch doesn't reach the others until it's merged, so two people can hold the same ticket and neither can tell. Parallel workers on a file store need to be sharing a checkout; otherwise the store belongs somewhere all of them can see it.

## Tidy pass

Occasionally — after a few closes, or when the store feels stale — check it: done tickets closed, stale claims released, statuses honest, priorities still pointing at the effort's goal, tickets that events made moot removed. Anyone can tidy; there is no keeper.
