# Ticket Convention

A ticket is a self-sufficient prose work packet: everything needed to pick it up, do it, and judge it done — readable by a person or an agent, with or without manifest-dev. The convention is the contract; a venue (files, GitHub Issues, any tracker) is a rendering of it. Nothing may depend on a venue feature beyond what a venue reference maps.

## Two kinds

- **Shaped ticket** — ready to execute. Someone picks it up and builds; its definition of done says when they're finished.
- **Question ticket** — needs figuring out first. Someone picks it up and investigates; done means the question is answered with evidence and the answer recorded. Resolving one often spawns shaped tickets.

The kind is declared on the ticket, so the picker knows which tool to bring.

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
- **Status / Claimed by** — see lifecycle.

A question ticket carries Title, the question itself, why it matters, what's already known, and dependencies/status/claim the same way. Its definition of done is built in: the question answered with evidence, recorded where the store says outcomes go.

**No machinery.** A ticket never contains tool-specific vocabulary a stranger wouldn't know: no verification YAML, no gate codes, no references to the manifest or workflow that produced it. If interpreting a ticket requires installing something, the ticket is wrong.

## The front file

Each effort's store carries one small front file (in a file store, a README beside the tickets; in a tracker, the tracking item's body) holding only content that doesn't change as tickets close:

- **Destination** — what reaching the end of this effort looks like, in a line or two. Pickers orient to it; "impact" in the priority rule is measured against it.
- **Priority rule override**, when the effort ranks differently than the default below.
- **Context pointers** — the key decision records, and where the effort's reads or logs live, so a cold picker gets effort-level orientation before opening a ticket.
- **Store config** — venue details, when not already in a store config file.

Never put derivable state here: no ticket lists, statuses, or ready/next — anything a close would stale belongs to the tickets themselves, where it can't rot. (A tracker's grouping item may carry an open-tickets list as its native mechanics; done entries drop off at close.)

## Lifecycle

- **Status**: `open` → `done`. Done tickets roll off **by location**: in a file store, closing moves the ticket into a `done/` subfolder beside the open ones; in a tracker, closing the item removes it from open queries. Reading the open set never scales with closed history — the archive is the `done/` folder, the tracker's closed items, and git.
- **Claiming**: before working a ticket, mark it claimed (a `Claimed by:` line, an assignee, the venue's equivalent). Open and unclaimed means takeable; claimed means not.
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

## Tidy pass

Occasionally — after a few closes, or when the store feels stale — check it: done tickets closed, stale claims released, statuses honest, priorities still pointing at the effort's goal, tickets that events made moot removed. Anyone can tidy; there is no keeper.
