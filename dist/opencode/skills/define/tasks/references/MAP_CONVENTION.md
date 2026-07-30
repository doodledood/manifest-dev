# Map Convention

A map is the one system that answers "what needs doing" for an effort too large for one deliberation — whatever the effort's size, from a gnarly multi-week task to a multi-year venture. It holds the effort's direction — questions being worked, work in flight, what's settled, what's ruled out — so direction lives in an artifact instead of in someone's head. The convention is venue-neutral: every rule is stated over items, statuses, links, and views. Local files are the default rendering; any tracker can host the same convention (see Venues).

## Item kinds

Two kinds, with different lifecycles:

- **Decision item** — a question ("pricing model?"). Worked by deliberation, sized to one session. Resolution leaves residue: the answer becomes a **standing decision** that keeps constraining the map until it stops mattering or the frame moves. Research is a decision item — a question answered by evidence.
- **Work item** — execution spawned by a resolved decision ("integrate vendor X"). The map holds a pointer with status; detail lives in the item or its delivery home (a manifest, a delivery board). Completion leaves nothing on the page — the item rolls off entirely, and history lives in the archive (files + git, or the tracker's closed items).

An item too big for one session splits; one that can't be split yet is fog, not an item.

## The front page

The front page is a **view, not a ledger** — it answers "what governs us now, and what's next," never "what happened." It stays around one screen at its own altitude for the map's whole life, however long that is:

- **Destination** — what reaching the end looks like, in a line or two every session orients to before picking an item.
- **Standing decisions** — only the resolved decisions that still constrain choices. One that stopped mattering rolls off the page; its item record remains as archive.
- **Frontier** — open, unblocked items of both kinds, ordered by the priority rule below, each showing status, claim state, and what blocks it.
- **Not yet specified (fog)** — in-scope ground not yet statable as items, held un-sliced; a patch may graduate into several items or none.
- **Out of scope** — ground consciously ruled beyond the destination, each ruling with its why. Returns only if the destination moves.

Everything else — resolved history, work detail, discussion — lives in item records, one place each; the page gists and links, never restates.

## Priority

Default frontier order (override per map by stating a different rule on the front page):

1. **Urgent** — a real expiring window (deadline, closing opportunity). Rare; jumps the queue.
2. **Unblocking** — opens the most other items, or the decision most likely to reshape the map.
3. **Impact** — biggest lever toward the destination.
4. **Cheap** — effort as tiebreak among equals.

"What should I work on?" = read the frontier top-down.

## Sub-maps

When a resolved decision opens an effort that is itself many decisions over time, don't dump its items onto the parent: create a child map with its own destination, and give the parent one line + link. Each map stays one screen at its own altitude; fog and rulings live on the map they belong to.

## Closer protocol

Whoever closes an item updates the map — there is no central keeper. Every generated map seeds a condensed copy of this protocol in its own body, so any closer — a manifest-dev session, an autonomous run, a colleague who has never heard of either — inherits the process from the artifact:

1. Record the outcome in the item: the answer with its why, or the work's completion.
2. Update the front page: a resolved decision becomes a standing decision if it still constrains; a completed work item leaves the page.
3. Graduate any fog the outcome made statable into new items; re-wire blocking.
4. If the outcome spawns work, create the work item (pointer + status) and route execution to its delivery home.

**Claiming:** before working an item, mark it claimed (a `claimed-by:` line, an assignee, or the venue's equivalent). An open unclaimed item is takeable; a claimed one isn't.

The seeded rules also cover deliberation: **standing decisions bind any session working inside the effort** — challenge one only deliberately, naming it — and **deliberation sessions don't edit the map**; their outcomes land through this closer protocol. Seeding both means every consumer — any tool, any person — inherits the handling rules from the artifact itself.

## Steward pass

Closers keep items correct; nobody keeps the whole. Periodically — after several closes, or on a stated cadence — run a **steward pass**: a plain deliberation session with the map as its topic. Does the frontier still point at the destination? Apply the roll-off closers skipped, merge sloppy updates, retire stale fog, propose sub-map splits, surface drift for the owner to rule on. The steward gardens the view; it does not approve closes.

## Scale and lifetime

A map is scoped to its effort, not to a project: an ephemeral map for one big task is as legitimate as a standing multi-year map, and a repo can hold several at different altitudes. Lifetime follows the effort — and so does stewarding: cadence proportionate to how long the map lives, which for a short-lived map may mean never.

Maps end. When the destination is reached — or abandoned — close the map: mark it closed, archive it (the venue's archive, or just history), and land any residue that outlives it — a standing decision still binding beyond the effort graduates to the parent map or a durable decision record; everything else goes down with the map.

## Venues

- **Local files (default):** a front-page file plus one file per item, in a directory the manifest names (e.g. `plans/<effort>/`); work items as thin pointer files; archive = the item files and git history.
- **Issue tracker:** map = a parent issue whose body is the front page; items = child issues; claim = assignee; blocking = native relations; roll-off = closing. The front-page body still carries destination, standing decisions, fog, rulings, and the seeded closer protocol.

The convention is the contract; the venue is a rendering. A manifest encoding a map names its venue explicitly, and nothing may depend on a venue feature beyond what this page maps.
