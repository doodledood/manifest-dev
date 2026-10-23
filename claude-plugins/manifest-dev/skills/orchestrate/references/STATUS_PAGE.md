# The status page

The status page shows a person where an effort's work stands without asking: the Tickets as a graph of
the order between them, and a separate list of what waits on the person. An effort is the named body of
work the orchestrator runs, with one destination and one front item: the effort's front file or issue in
the Ticket store, where its standing settings live. A check-in is each time the orchestrator reads the
store again and acts on what changed.

One page shows one effort. An orchestrator working several efforts keeps one page for each, every
page holding only its own effort's Tickets and linked from that effort's front item.

The page is a view rebuilt from the store at each check-in. It is never a record of its own: every
fact on it is read from the Tickets and the front item, and nothing the orchestrator decides is read
back from the page.

## One template, one data block

`assets/status-page.html` is the whole page: layout, styles and script, with no code, styles or fonts
loaded from the network. Copy it unchanged. It reads one data block:

```html
<script type="application/json" id="orchestrate-status">
{ ... }
</script>
```

At each check-in, build a fresh snapshot from the store and replace only the JSON between those two
tags. Never edit anything else in the file. Before writing:

- Serialize it as JSON, then replace every `<` with `\u003c` (JSON reads it back as the same character), so a Ticket title can never close the
  script element.
- Check it against the fields below. The page rejects a snapshot whose `schema` is not 1, a required
  field is missing or of the wrong type, or two Tickets share an id. It then keeps showing the last
  snapshot it could read, and tells the person the latest update could not be read.
- Leave out `example`. The sample in the shipped template carries `"example": true`, and the page
  labels such data "Example".

## Where the page goes

Publish the page on the page surface the host offers: a page the host keeps at a link the person can
open, such as an Artifact on Claude or a hosted page elsewhere. Where the host offers none, write it as a
local HTML file. Pick the first that applies:

| The host offers | At the first check-in | At each later check-in | An open view |
|---|---|---|---|
| A page surface with a live data store the page can read (on Claude: an Artifact with its database) | Publish the page with the block filled, and give it read access to the store for viewers and write access for editors only. On Claude, declare the database with the rule `{path: "status", read: "view", write: "admin"}`. | Write the snapshot as the document `status/current`, its top-level fields being the snapshot's. Republish the page with the block rewritten only when the plan ends or the orchestrator stops, so a viewer who cannot read the store still sees the last state. | Updates in place, without a reload, within moments of the write. |
| A page surface that serves files beside the page | Publish the page, and beside it `orchestrate-status.json` holding the snapshot. | Rewrite the block, and rewrite `orchestrate-status.json` with the same snapshot. | Re-reads `orchestrate-status.json` every 15 seconds and updates in place. |
| A page surface with neither | Publish the page. | Republish it with the block rewritten. | Shows the data as of when it was opened, and says how old it is; a reload shows the latest. |
| No page surface | Write `orchestrate-status.html` in a folder outside the repository's tracked files, such as a folder named after the effort under the system's temporary directory, and beside it `orchestrate-status.js` containing `window.ORCHESTRATE_STATUS = <snapshot>;`. Tell the person the file's path. | Rewrite the block in the HTML file, and rewrite `orchestrate-status.js` with the same snapshot. | Re-reads `orchestrate-status.js` every 15 seconds and updates in place; opening the file again shows the latest. |

The page never writes to the store, the data file or anything else. A person who opens it reads it.

Save the page's link on the effort's front item, on a line of its own: `Status page: <link or
path>`. At the start of every plan, and when a new orchestrator session starts on the effort, read
that line and update the page it names instead of making a new one. If the link no longer opens, or
the host will not let you update that page, publish a new one and replace the line: re-read the
front item just before that edit and change nothing else in it, so a `Paused:` line a person added
meanwhile stays.

The page holds Ticket titles and the person's open questions. On a host where pages can be shared,
leave it private unless the person shares it.

## How the page reads the snapshot

- **The graph.** Each Ticket is a card in a column by how many Tickets it waits on: Now, Next, Then,
  Later, After that, then Step 6 and on, with the effort's destination as the Goal at the end. An edge
  is drawn for each dependency, each pair ordered because both touch the same code, and each debt
  source. Attention goes to what needs the person: a Ticket that is stuck (`escalated` or `failed`)
  is a solid red card, one that waits on the person otherwise (`held`, `grant`, `proposal`) a solid
  orange one; a running Ticket stays calm, its colour only in its dot and bar; waiting and landed
  Tickets recede, and the Goal is a quiet card. The "Needs you" button turns solid, red while a
  Ticket is stuck, and the browser tab's title carries the count. A "?" button opens a key to the
  colours and the line styles.
- **An open Ticket.** A card opens to its detail, read top to bottom: the title, then `summary`, then
  a line with the Ticket's link, its type, its pull request (for a held Ticket, in the decision's
  button instead) and, for a Ticket a run found, the Tickets in its `from`; then, where the Ticket
  waits on the person, the decision — the ask, the `pick` and the `risk`, one action under them,
  and the `evidence` folded; then what it solves (`change` as a before and after followed by
  `why`, or `why` alone), how it came up (`foundWhile`), `done` as a checklist, and last where it
  stands. With a fine pointer, hovering a card shows its `summary`
  beside it.
- **What needs the person.** The `needsYou` list, in the order given, is the "Needs you" panel. An item
  that names a Ticket puts a numbered badge on that Ticket's card, the number being the item's place in
  the list.
- **Clocks.** Between check-ins, the page counts each running Ticket's time from its `at`, and the time
  since `checkedAt`. It never moves a Ticket to another phase or status on its own.
- **Stopped check-ins.** Two minutes after `nextCheckAt` passes with no new snapshot, the page warns
  that the orchestrator has stopped checking in. So set `nextCheckAt` to when the next check-in will
  really happen, and leave it out when there will be none.
- **Changes.** Each new snapshot animates only what changed, matched by Ticket id. The person's pan,
  zoom and open detail stay as they were.

## Fields

Times are ISO 8601 strings with a time zone, such as `2026-10-18T09:40:00Z`. A field marked optional
may be left out; `null` counts as left out.

### The snapshot

| Field | Type | Meaning | Where it comes from |
|---|---|---|---|
| `schema` | number, `1` | The data format. The page reads only `1`. | Always `1`. |
| `effort.name` | string | The effort's name, shown as the page's title. | The front item's title. |
| `effort.destination` | string, optional | One sentence on what done means for the effort, shown as the Goal. | The front item's destination. |
| `mode` | `"default"` or `"autonomous"` | How this orchestrator runs: proposing each plan and waiting for approval, or acting on its own (`--autonomous`). | This orchestrator's own invocation. |
| `state` | `"running"`, `"paused"` or `"finished"` | Whether runs are going, the effort is paused, or the plan has ended. | `paused` when the front item carries the pause line; `finished` once the plan has ended, including when the orchestrator stops; `running` otherwise. |
| `coordination` | object, optional | Present only for an assigned outcome. Plan completion alone never means the outcome was achieved. | The current coordination record on the effort's front item. |
| `coordination.state` | `"working"`, `"waiting-evidence"`, `"waiting-decision"`, `"complete"` or `"limit"` | What the outcome assignment needs next; shown above the graph even with no Tickets. | The coordinator's evidence-based continuation decision. |
| `coordination.summary` | nonempty string | A concise account of progress or the unresolved condition; distinguish delivered work from observed use. | The current coordination record. |
| `coordination.next` | nonempty string | The concrete next action or observation, how to resume, or why no continuation remains. Never invent an automatic wake. | The current coordination record's continuation route. |
| `plan` | number | Which plan this is, counted from 1 by this orchestrator on this effort. | This orchestrator's count. |
| `checkedAt` | time | When this check-in read the store. | This check-in. |
| `nextCheckAt` | time, optional | When the next check-in will happen. Leave it out when none will. | This orchestrator's schedule. |
| `maxBatch` | number, optional | How many runs may go at once. Leave it out when there is no limit (`--max-batch none`). | `--max-batch`, or its default. |
| `tickets` | list | The Tickets on the page, described below. | The store. |
| `needsYou` | list | What waits on the person, described below. | The orchestrator's list of what waits on the person. |

`tickets` holds the current plan's Tickets, those written at this plan's check-ins, Tickets in scope
that the orchestrator leaves alone, and the Tickets proposed for the next plan. Tickets from earlier
plans drop off, so the page stays the size of one plan. The order of the list is the plan order:
Tickets are read, and reached with the keyboard, in that order, each followed by the Tickets that
wait on it.

For an outcome assignment, include `coordination` at every check-in. A finished plan with an empty
queue can still be `waiting-evidence` or `waiting-decision`. Use `complete` only when the outcome's
completion terms have evidence, not when delivery ended. Put a retained decision in `needsYou` too,
with its recommendation and evidence. Keep the summary short; link detailed records from the front
item. Older queue-only snapshots remain valid without `coordination`.

### A Ticket

| Field | Type | Meaning | Where it comes from |
|---|---|---|---|
| `id` | string | The Ticket's id as the store shows it, such as `#131`. Unique on the page, and never `goal`. | The Ticket. |
| `title` | string | The Ticket's title. | The Ticket. |
| `summary` | string, optional | One plain sentence on what the Ticket changes and for whom, for a person who never saw it. A snapshot from an older orchestrator may lack it; the page then says the Ticket has no summary yet. | Derived from the Ticket's Title and Why, or a question Ticket's question. |
| `why` | string, optional | The problem the Ticket relieves, in a sentence or two. | The Ticket's Why, or a question Ticket's "why it matters". |
| `change` | object, optional | What a person would see before and after the Ticket lands: `before` and `after`. | The Ticket's Why and Definition of done, only where they describe a concrete before and after. |
| `change.before` | string | Today, in a line. | As `change`. |
| `change.after` | string | After the Ticket lands, in a line. | As `change`. |
| `done` | list of strings, optional | How anyone can tell it worked, one check per item; shown as met once the Ticket has landed. | The Ticket's Definition of done; for a question Ticket, the question answered with evidence. |
| `type` | `"bug"`, `"feature"`, `"refactor"`, `"docs"` or `"chore"`, optional | What kind of work it is. | The Ticket's Type. |
| `foundWhile` | string, optional | For a Ticket a run found, what that run saw that led to it. | The Ticket's source link and Why. |
| `url` | string, optional | The Ticket's address. Only an `http://` or `https://` address becomes a link. | The Ticket. |
| `status` | string, one of the statuses below | Where the Ticket stands. | See the statuses below. |
| `phase` | string, optional | For a `running` or `escalated` Ticket, the step its run is at: `understand`, `define`, `build`, `verify`, `ready` (a ready pull request) or `land` (at its landing turn). | The progress in the Ticket's attempt record: the one marked record where the run keeps its Manifest, its progress and its run facts; `land` is the orchestrator's own, while it takes that Ticket's landing turn. |
| `at` | time, optional | For `running`, when this run started; for `landed`, when it landed. | The attempt record, or the pull request's merge time. |
| `pr` | object, optional | The Ticket's pull request: `id` (string, such as `#205`) and `url` (string, optional). | The attempt record or the venue's link between the Ticket and its pull request. |
| `note` | string, optional | One sentence the person would want, such as why the Ticket is left alone, or that the base moved. | This check-in's reading of the Ticket. |
| `dependsOn` | list of ids, optional | Tickets this one depends on. | The Ticket's dependencies in the store. |
| `after` | list of ids, optional | Tickets this one runs after because both touch the same code. | This plan's ordering. |
| `from` | list of ids, optional | Tickets whose debt this one was written from. | The Ticket's source link. |
| `kind` | `"debt"` or `"refactor"`, optional | A Ticket the orchestrator wrote from debt, or a structural refactor it proposes. | The Ticket's source link and how it was written. |
| `grant` | string, `null` or `"never"`, optional | For a Ticket an agent wrote: who granted it Auto, the grant that lets automation take it end to end; `null` while no one has; `"never"` where the person explicitly retains direction, including a refactor proposal without delegated direction. | The grant line on the Ticket. |
| `auto` | `false`, optional | Set on a Ticket in the plan that does not carry Auto: it runs to its retained decision or acceptance, which can concern a Read, another artifact or landing a pull request. | The Ticket's Auto grant. |

An id in `dependsOn`, `after` or `from` that is not on the page draws no edge.

Write `summary`, `why`, `change`, `done`, `foundWhile` and `note` in plain words a person who never
saw the Ticket understands: no gate codes, branch names or workflow terms. Always write `summary`; leave any
other of them out when the Ticket holds nothing to derive it from, rather than inventing it, and
give `change` only where the Ticket describes a concrete before and after. A project whose Tickets
use their own types gives `type` only for these five.

### Statuses

| Status | Shown as | When |
|---|---|---|
| `running` | its phase, with the time it has run | A live run holds the Ticket: its attempt record names the run and its session, written by the automation identity, and the run is live as `../../ticket-up/references/AUTOMATED_EXECUTION.md` → *The attempt record* defines it. |
| `landed` | Landed, with the time | Its pull request merged and the Ticket closed. |
| `held` | Your look | It stopped at a ready pull request or a drafted answer that waits for the person: it has no Auto, or its landing needs the person. |
| `escalated` | Your answer | It carries an escalation mark: the record on the Ticket that says a person is needed. |
| `failed` | Launch failed | Its session failed to start three times, and it went to a person. |
| `grant` | Grant Auto? | An agent wrote it, and in default mode it waits for the person to grant Auto. |
| `proposal` | Your call | A structural refactor the orchestrator proposes, because one area keeps producing debt. |
| `queued` | Up next | In the plan and ready, waiting for a free run slot. |
| `waiting` | After its open dependencies, or Up next | In the plan, waiting on the Tickets in its `dependsOn` or `after`. |
| `skipped` | Left alone | In scope, but automation may not take it: for example, its author lacks write access, or a person is assigned. Say why in `note`. |
| `proposed` | Proposed | In the next plan the orchestrator proposes, not yet approved. |

While the state is `paused`, `queued` and `waiting` Tickets show as Paused.

### What needs the person

Order `needsYou` by what waiting costs: the item whose wait holds back the most work, or loses the most,
comes first.

| Field | Type | Meaning |
|---|---|---|
| `ask` | string | What the person is asked, in one sentence. |
| `ticket` | id, optional | The Ticket the ask is about. Its card gets the item's number as a badge, and the item opens its detail. |
| `detail` | string, optional | What the person needs to answer, and where an answer counts: in the orchestrator's conversation, or on the venue. |
| `pick` | string, optional | The answer the orchestrator recommends, such as "Merge it." |
| `risk` | string, optional | What could go wrong if the person takes that answer. |
| `evidence` | string, optional | What the recommendation rests on: the gates that passed and what they did not check, the failing check, or the blocker. |
| `cost` | string, optional | What the wait holds back, such as "#153 depends on it". |
| `startLine` | string, optional | A line the person copies to start a session, such as the start line for a deep-planning session. The page shows it with a Copy button. |

Every item the orchestrator keeps on its list of what waits on the person is here: held pull
requests, escalations, launches that went to a person, Tickets awaiting a grant, refactor proposals,
planning sessions to start, a common cause that paused the effort, and the next plan to approve.
Each is its own item, never a count standing in for several. Give each the `pick`, `risk` and
`evidence` that let the person decide it from the page; the page shows them under the ask, and in
the Ticket's detail.
