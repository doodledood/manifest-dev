# Ticket Convention

A ticket is a self-sufficient prose work packet: everything needed to pick it up, do it, and judge it done — readable by a person or an agent, with or without manifest-dev. The convention is the contract; a venue (files, GitHub Issues, any tracker) is a rendering of it. Nothing may depend on a venue feature beyond what a venue reference maps.

## Two kinds

The kinds split on one question: is the decision space closed?

- **Shaped ticket** — every decision that shapes the work is already made: no open question remains whose answer would change what gets built or what done means. Someone picks it up and builds; its definition of done says when they're finished.
- **Question ticket** — at least one such question is still open. Someone picks it up and investigates; done means the question is answered with evidence and the answer recorded. Resolving one often spawns shaped tickets.

The write-time test: try to name a question whose answer would change the work or its definition of done. Naming one makes the ticket a question ticket, however much context it already carries — half-investigated work is a question ticket with a thick "what's already known", not a shaped ticket. Choices where any competent answer within the ticket's stated rules is acceptable — naming, internal structure, mechanical detail — are execution, not shaping, and leaving them open does not reopen the kind.

The bar is a property of the ticket's content, never of where it came from: no particular workflow or artifact needs to have produced a shaped ticket, and none makes a ticket shaped while such a question stays open.

The kind is declared on the ticket, so the picker knows which tool to bring.

## The Auto grant

A ticket of either kind may carry **Auto** — an opt-in grant, declared when the ticket is written, that unattended automation may take it end to end: do the work and judge it done, with nobody watching.

- **Granting.** Grant only when neither doing the work nor judging it done needs any human's knowledge, taste, or authority — no done-judgment resting on someone's unstated criteria, no approval, no access an unattended worker won't have, no irreversible act, no decision deferred to mid-flight input. That bar is necessary but never sufficient: the author still chooses, and withheld trust alone is reason enough to withhold. When in doubt, don't grant.
- **Absence is the fence.** A ticket without the grant is not touched by automation at all — no partial work, no prepping half the job. Nothing is ever marked "not auto"; silence already says it, which is also what keeps automation off items in a shared venue that were never tickets. A person may still hand an ungranted ticket to an agent and watch — that is the person working the ticket, outside the grant's jurisdiction.
- **Surprises don't revoke.** A granted ticket's worker can still hit an unexpected blocker; it stops and surfaces rather than deciding what only a person can. That is the exception path working, not evidence the grant was wrong — only a step known at write time to need a person keeps the grant off.

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

- **Destination** — what reaching the end of this effort looks like, in a line or two. Pickers orient to it; "impact" in the priority rule is measured against it.
- **Priority rule override**, when the effort ranks differently than the default below.
- **Context pointers** — the key decision records, and where the effort's reads or logs live, so a cold picker gets effort-level orientation before opening a ticket.

Never put derivable state here: no ticket lists, statuses, or ready/next — anything a close would stale belongs to the tickets themselves, where it can't rot. Where a tracker groups its items natively, that grouping is the tracker's to keep current rather than a list anyone edits.

## Lifecycle

- **Status**: `open` → `done`. Done tickets roll off **by location**: in a file store, closing moves the ticket into a `done/` subfolder beside the open ones; in a tracker, closing the item removes it from open queries. Reading the open set never scales with closed history — the archive is the `done/` folder, the tracker's closed items, and git.
- **Claiming**: mark a ticket claimed (a `Claimed by:` line, an assignee, the venue's equivalent) when you pick it, not when you get around to starting it — the gap between the two is where somebody else picks the same one. Open and unclaimed means takeable; claimed means not.
- **Ready**: a ticket is ready when it is open, unclaimed, and every ticket it depends on is done. Blocked is derived from unmet dependencies, never stored as a status.
- **Closing**: record the outcome on the ticket (the work's landing place, or the question's answer), mark it done and roll it off (move it to `done/`, or close the item), and check what the close changed: tickets it made ready, and outcomes that need interpreting. An outcome that needs judging while no existing ticket depends on this one spawns that question ticket as part of the close — the next thinking step stays reachable through the store, never through someone's initiative.

## Priority

"What should I work on?" reads the ready tickets in this order (a store may state a different rule; the stated rule wins):

1. **Urgent** — a real expiring window. Rare; jumps the queue.
2. **Unblocking** — frees the most other tickets.
3. **Impact** — biggest lever toward the effort's goal.
4. **Cheap** — effort as tiebreak among equals.

## Dependencies and parallelism

Edges are structural only: B depends on A when B genuinely cannot be done or judged without A's outcome. Never encode a preferred working order as a dependency. The cost of parallel pickup is honest and accepted: with one worker, surprises in an early ticket reshape later ones; with parallel workers they don't — only the edges carry ordering, so anything learned that should reshape another ticket must be written onto that ticket when it's learned.

Claiming is what keeps two workers off one ticket, and it does that only where the store is a surface both of them read. A hosted tracker is one. Files in a repository are not, once the workers aren't in the same working copy: a claim written in one clone, worktree, or branch doesn't reach the others until it's merged, so two people can hold the same ticket and neither can tell. Parallel workers on a file store need to be sharing a checkout; otherwise the store belongs somewhere all of them can see it.

## Tidy pass

Occasionally — after a few closes, or when the store feels stale — check it: done tickets closed, stale claims released, statuses honest, priorities still pointing at the effort's goal, tickets that events made moot removed. Anyone can tidy; there is no keeper.
