---
kind: feature
covers: verification/models, claude-plugins/manifest-dev/skills/ticket-up/references/AUTOMATED_EXECUTION.md, claude-plugins/manifest-dev/skills/ticket-up/references/GITHUB_STORE.md, claude-plugins/manifest-dev/skills/ticket-up/references/TICKET_CONVENTION.md, claude-plugins/manifest-dev/skills/orchestrate/SKILL.md, claude-plugins/manifest-dev/skills/run-ticket/SKILL.md
---
# ticket-protocol-model

A TLA+ model of the unattended Ticket protocol — the attempt record, launches, takeovers, the
landing procedure, the escalation mark and a deferred Ticket's signpost, as `orchestrate`, `run-ticket` and ticket-up's
`AUTOMATED_EXECUTION.md` state them — checked by TLC on fixed configurations. Example runs show the
protocol working on the orders of events someone thought of; the model checks every order of
events within its bound. It is a maintainer check: nothing here ships.

## How a user reaches it

- `scripts/verify drive ticket-protocol-model`, or one configuration directly with
  `verification/models/ticket-protocol/check.sh <config>`.
- `verify affected` selects it when a protocol file it quotes changes. Each action in
  `TicketProtocol.tla` quotes the sentences it encodes, and `tests/test_ticket_protocol_model.py`
  fails when one of them leaves its file — a change to the protocol prose then changes the model
  with it.
- Each `.cfg` beside the model opens with a comment saying what it explores.

## Scenarios

### races
Run: `verification/models/ticket-protocol/check.sh races`
Proves: two orchestrators sharing the automation identity, a run that dies and a takeover after a
timeout keep one attempt record, merge only the recorded head, and land or hand over every Ticket
marked ready.
Line: 4.8 s on linux-x64-4cpu

### race-landing
Run: `verification/models/ticket-protocol/check.sh race-landing`
Proves: the same properties with two orchestrators, a takeover, a moved base and a commit a person
pushed to the pull request's branch.
Line: 30.2 s on linux-x64-4cpu

### landing
Run: `verification/models/ticket-protocol/check.sh landing`
Proves: each way a landing cannot merge — a moved head, a moved base, a red check, a review only a
person can give, a pull request closed without merging — ends in a relaunch, an escalation, a
pull request held for the person's approval or the landing.
Line: 2.7 s on linux-x64-4cpu

### person
Run: `verification/models/ticket-protocol/check.sh person`
Proves: a person's claim, close, reopen, merge or escalation mark, with a moved base, never leads
automation to close a Ticket without a landing observed since it was last opened, or to land one
the person marked; a Ticket reopened after its merge is launched again rather than landed.
Line: 2.5 s on linux-x64-4cpu; raised: the person configuration explores a person applying the escalation mark

### deferred
Run: `verification/models/ticket-protocol/check.sh deferred && verification/models/ticket-protocol/check.sh deferred-unreadable`
Proves: two orchestrators never claim a deferred Ticket until its signpost's condition reads as met
at its source, claim it once the world makes it met, and never claim one whose source cannot be
read; the other properties hold meanwhile.
Line: 2.5 s on linux-x64-4cpu

### prefix
Run: `verification/models/ticket-protocol/check.sh --expect-violation prefix-record && verification/models/ticket-protocol/check.sh --expect-violation prefix-stall && verification/models/ticket-protocol/check.sh --expect-violation prefix-escalated && verification/models/ticket-protocol/check.sh --expect-violation prefix-deferred`
Proves: the check can fail. With the protocol switched back to its four old behaviors, TLC reports
a second attempt record, a landing that stalls, a landing of a Ticket a person marked escalated and
a claim of a Ticket whose signpost reads as unmet, each with its trace; the scenario fails when any
is not reported.
Line: 3.4 s on linux-x64-4cpu; raised: a third configuration, prefix-escalated, shows NoLandWhileEscalated can fail

## Gotchas

- Needs Java 11 or newer and the pinned TLA+ tools at `.tools/tla2tools.jar`, which
  `scripts/setup.sh` downloads and checks against `verification/models/tla2tools.pin`. A missing
  runtime or jar, or a jar with another checksum, exits 3, which `verify` records as unreachable,
  never passed.
- The model's bound is in its header: one Ticket, each world event at most once, at most one crash.
  A stall that needs more than that is not checked here, nor is the launch count's escalation after
  three failed launches or landing repairs.
- Orchestrators never stop in the model, so a takeover after a timeout is checked for safety, but
  no liveness property needs one.
- A run's re-read and the write after it are taken as one step, since they are adjacent calls. The
  launcher's earlier read and its write are separate steps: that window is the race the first
  created comment settles.
- `--expect-violation` configs check exactly one property each, so a reported violation is that
  property's.
- TLC writes its state files to a temporary directory, never into the checkout.
