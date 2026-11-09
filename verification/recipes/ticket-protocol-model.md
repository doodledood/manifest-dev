---
kind: feature
covers: verification/models, claude-plugins/manifest-dev/skills/ticket-up/references/AUTOMATED_EXECUTION.md, claude-plugins/manifest-dev/skills/ticket-up/references/GITHUB_STORE.md, claude-plugins/manifest-dev/skills/ticket-up/references/FILE_STORE.md, claude-plugins/manifest-dev/skills/ticket-up/references/TICKET_CONVENTION.md, claude-plugins/manifest-dev/skills/orchestrate/SKILL.md, claude-plugins/manifest-dev/skills/orchestrate/references/AUTONOMOUS.md, claude-plugins/manifest-dev/skills/run-ticket/SKILL.md, claude-plugins/manifest-dev/skills/next-ticket/SKILL.md
---
# ticket-protocol-model

A TLA+ model of the Ticket protocol — the attempt record, launches, takeovers, the landing
procedure, the escalation mark, a deferred Ticket's signpost, who set an Auto grant, a person's pick
and the hand run they start under it, and an effort paused by a person or by an orchestrator for
each cause, with the repair Ticket's exception — as `orchestrate`, `run-ticket`, `next-ticket` and
ticket-up's `AUTOMATED_EXECUTION.md` → *Transitions* state them, checked by TLC on fixed
configurations. Example runs show the
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
timeout keep one attempt record, merge only the recorded head, land or hand over every Ticket
marked ready, and adopt a ready mark only from a holder that stopped checking in.

### race-landing
Run: `verification/models/ticket-protocol/check.sh race-landing`
Proves: the same properties with two orchestrators, a takeover, a moved base and a commit a person
pushed to the pull request's branch.

### landing
Run: `verification/models/ticket-protocol/check.sh landing`
Proves: each way a landing cannot merge — a moved head, a moved base, a red check, a review only a
person can give, a pull request closed without merging — ends in a relaunch, an escalation, a
pull request held for the person's approval or the landing.

### person
Run: `verification/models/ticket-protocol/check.sh person`
Proves: a person's claim, close, reopen, merge or escalation mark, with a moved base, never leads
automation to close a Ticket without a landing observed since it was last opened, or to land one
the person marked; a Ticket reopened after its merge is launched again rather than landed.

### deferred
Run: `verification/models/ticket-protocol/check.sh deferred && verification/models/ticket-protocol/check.sh deferred-unreadable`
Proves: two orchestrators never claim a deferred Ticket until its signpost's condition reads as met
at its source, and never claim one whose source cannot be read; the other properties hold meanwhile.

### stopped
Run: `verification/models/ticket-protocol/check.sh stopped`
Proves: when an orchestrator stops for good after its launch and the timeout passes with no check-in
from it, the other orchestrator adopts the ready mark that run left and lands the Ticket, or holds it for a
review only a person gives, and never launches a held pull request again.

### grant
Run: `verification/models/ticket-protocol/check.sh grant && verification/models/ticket-protocol/check.sh grant-bare`
Proves: an orchestrator launches an unclaimed Ticket only when its grant counts or its author has
write access, and lands only a Ticket whose grant counts by who set it — a person with authority
to grant, or the automation identity with a grant decided — through a withdrawal, a grant state
someone without authority set, and one the automation identity set with no grant decided; an
ungranted ready pull request waits for a person, whose merge the orchestrator then records and
closes.

### pause
Run: `verification/models/ticket-protocol/check.sh pause && verification/models/ticket-protocol/check.sh repair && verification/models/ticket-protocol/check.sh pause-person`
Proves: while a person's `Paused:` line or an orchestrator's pause stands, nothing starts in the
effort — no launch, at the sort or at the re-read after writing; no adoption, with a second
orchestrator that may stop; no landing turn — except the repair Ticket an orchestrator's pause
names, and that only while every pause is for a code-fixable cause and no person's line stands; the
effort stays paused while any cause an orchestrator paused it for still fails, one pause per cause;
and once only code-fixable pauses hold it, the repair Ticket lands and its pause lifts. When the
repair Ticket waits on a review only a person gives, the orchestrator stops checking in and leaves
the pause standing, and a later orchestrator lifts it once the repair lands.

### handoff
Run: `verification/models/ticket-protocol/check.sh handoff`
Proves: once a person picks a Ticket, no orchestrator launches, adopts or lands it, even after the
hand run they start under their claim dies and its timeout passes, or after the person marks it
escalated and answers, which clears only an automation claim; that hand run never stands down
on its starter's claim; and once the person merges a pull request marked ready, the orchestrator, a
picker reading the store or a run that starts on it records the landing and closes the Ticket,
whoever holds its claim.

### prefix
Run: `f=0; for c in record stall escalated deferred stranded grant dispatch pick handrun repair percause handclose checkins; do verification/models/ticket-protocol/check.sh --expect-violation prefix-$c || f=1; done; exit $f`
Proves: the check can fail. Each prefix configuration restores one old behavior, a rule as it stood
before a fix, and TLC reports, with its trace: a second attempt record; a landing that stalls; a
landing of a Ticket a person marked escalated; a claim of a Ticket whose signpost reads as unmet; a
ready Ticket stranded once its orchestrator stopped; a landing, and a launch, on a grant state set
by someone without authority; an orchestrator recovering a Ticket a person picked, once the picker
wrote its claim as the automation identity; a hand run standing down on its starter's claim; the
repair Ticket starting under a person's `Paused:` line; an effort unpaused while an outage
persists, once it carried one pause rather than one per cause; a person's merge left unrecorded
while they hold the claim; and an orchestrator checking in without end on a pause only the person
can clear. The scenario fails when any is not
reported.

## Gotchas

- Uses `JAVA_HOME/bin/java` when set, otherwise `java` on PATH; it checks the runtime, not merely the presence of a launcher. For a Homebrew keg-only JDK, set `JAVA_HOME` to its JDK home before running.
- Needs Java 11 or newer and the pinned TLA+ tools at `.tools/tla2tools.jar`, which
  `scripts/setup.sh` downloads and checks against `verification/models/tla2tools.pin`. A missing
  runtime or jar, or a jar with another checksum, exits 3, which `verify` records as unreachable,
  never passed.
- Acceptance criteria and non-commit subject state stay fixed in this model; successful work abstracts adequate evidence and settled mandatory work. The `run-ticket` recipe's `acceptance-recovery` scenario checks changed criteria, external state and pending work. This model does not establish those judgments.
- The model's bound is in its header: one Ticket, each world event at most once, at most one crash.
  The one Ticket stands for every Ticket of its effort that fails on a cause, so the count of
  Tickets row *Pause by an orchestrator* asks for is not checked; nor is withholding or an
  orchestrator's own grant, a stale claim's release, or a person's pause ending the orchestrator's
  work on the effort, which the model treats as the orchestrator starting nothing there.
- A grant withdrawn between the landing's authority check and its merge is not caught: the model
  takes the merge as the next call, as the prose does. Likewise a pause that arrives during a
  landing turn already begun lets that turn finish.
- *Dispatchable*'s third branch, a plan a person with write access approved, is not modelled: the
  model's orchestrator plans for itself, so `LaunchesOnlyDispatchable` checks a grant that counts or
  an author with write access. Nor is a hand run told to land: the model's hand run stops at its
  ready mark.
  A stall that needs more than that is not checked here, nor is the launch count's escalation after
  three failed launches or landing repairs.
- `PreFix` names the old behaviors a configuration restores; passing configurations set it to
  `{}`. A new prefix configuration restores one behavior, so another cannot hide its violation.
- An orchestrator stops at most once, and only in `stopped` and `prefix-stranded`, where the run's
  timeout then passes, and in `pause-person`, where it stops because every pause left waits on the
  person and a later orchestrator may start after it; elsewhere orchestrators never stop, so a
  takeover after a timeout is checked for safety there, and no liveness property needs one.
  `pause-person` checks no `ReadyResolves`: once every orchestrator has stopped, a ready mark waits
  for the next one, as the prose intends.
- A run's re-read and the write after it are taken as one step, since they are adjacent calls. The
  launcher's earlier read and its write are separate steps: that window is the race the first
  created comment settles.
- `--expect-violation` configs check exactly one property each, so a reported violation is that
  property's.
- TLC writes its state files to a temporary directory, never into the checkout.
