--------------------------- MODULE TicketProtocol ---------------------------
(* A model of manifest-dev's Ticket protocol, for one Ticket.

   The shipped prose is the code this models. Each action and property below carries the
   sentences it encodes as `Quote <file>: "<sentence>"` comments, paths relative to
   claude-plugins/manifest-dev/skills/; tests/test_ticket_protocol_model.py fails when a quoted
   sentence leaves its file. An action that models the world rather than the protocol carries a
   `World:` comment instead, and a branch that restores an old, wrong behavior is marked `Pre-fix:`.

   Scope: one Ticket; the orchestrators in Orchs, sharing one automation identity, each able to
   launch, take over and land; one run per launch; a person who can push to the pull request's
   branch, claim, pick, close or reopen the Ticket, close or approve the pull request, apply the
   escalation mark, answer an escalation, withdraw the Auto grant, and add or remove a `Paused:`
   line; a hand run the person who picked the Ticket starts, writing as the automation identity,
   never told to land; an orchestrator that stops for good, after which its run's timeout passes;
   a base branch that moves at most once; each world event at most once. Liveness holds within
   that bound. The three-failed-launches escalation is outside it: one crash at most.

   Grant provenance: Grant says who set the venue's grant state, and only a person with authority
   to grant, or the automation identity while a grant decision records a grant, makes it count.

   Effort pauses: two causes outside the Ticket can fail, "check" (a required check failing the
   same way on the base, code-fixable) and "outage" (a service that is down). Where Repair holds,
   the Ticket is the repair Ticket for "check", which fails from the start and is fixed when that
   Ticket's pull request merges.

   An orchestrator's read sorts the Ticket as orchestrate/SKILL.md's sort does, into the first
   category whose conditions hold: LeftAlone, Running, ToLand, ToRecover, Ready.

   A deferred Ticket's signpost is world state: its condition reads as met, unmet or unreadable at
   the source it names, as Signpost says at the start, and the world may make it read as met once.

   PreFix names the old behaviors to restore, each a protocol rule as it stood before a fix:
   "stall", the landing check stops with nothing relaunched or escalated when the head, a check
   or a protection fails; "record", a launcher decides from its earlier read whether to create the
   attempt record; "escalated", the lander does not look for the escalation mark; "deferred", a
   launcher does not read a deferred Ticket's signpost; "stranded", a ready mark another
   orchestrator's run left fits no category, so nobody adopts it; "grant", the grant state counts
   whoever set it; "pick", a picker writes its claim as the automation identity; "handrun", a hand
   run stands down on any person's claim, its starter's included; "repair", the repair Ticket runs
   under a person's pause too; and "percause", an effort carries one orchestrator's pause, so a
   second cause's pause is never recorded. Each prefix configuration restores one, and the
   `prefix` scenario of verification/recipes/ticket-protocol-model.md expects TLC to report the
   violation each causes. *)
EXTENDS Integers, Sequences

CONSTANTS Orchs,     \* the orchestrators sharing the automation identity
          Env,       \* the world events this configuration allows, each at most once
          PreFix,    \* the set of old behaviors restored, named above; {} for the protocol as it stands
          MaxRuns,   \* launches per orchestrator, a bound for TLC; no run reaches it
          Signpost,  \* "none" (not deferred), or how its condition reads at the start: "met", "unmet" or "unreadable"
          Hand,      \* the hand run's runner, a model value
          Grant,     \* who set the grant state at the start: "none", "person" (with authority to grant), "decided" (the automation identity, a grant decided), "bare" (the automation identity, none decided) or "other"
          Writer,    \* the Ticket's author has write access to the repository
          Repair     \* the Ticket is the repair Ticket for the cause "check"

None == <<"", 0>>                       \* no run
Live == {"start", "work", "prepush", "push", "prewrite"}
Old(b) == b \in PreFix
Causes == {"check", "outage"}
CodeFixable == {"check"}

VARIABLES
  recs,        \* the attempt-record comments on the Ticket, in the order the venue created them
  claim,       \* "none", "auto" (the automation identity) or "person"
  closed,      \* the Ticket is closed
  autoClosed,  \* automation closed it
  landedNow,   \* a landing was observed since the Ticket was last opened
  mark,        \* the escalation mark
  prOpen, merged, red, review, \* the pull request: open, merged, a required check red, a review still owed
  branch,      \* head commit of the Ticket's stable branch, which is the pull request's head
  base,        \* the target branch's commit
  nextC,       \* the next fresh commit
  used,        \* the world events already spent
  opc,         \* each orchestrator's step; "gone" once it has stopped
  saw,         \* whether it saw an attempt record at its last read
  lview,       \* the head it read from the record before merging
  n,           \* how many runs it has launched
  rpc, rbase, rlocal, rmerged, \* its current run: step, head it built on, commit it made, base it merged
  bad,         \* set when automation merges a Ticket that carries the escalation mark
  label,       \* who set the grant state now: "none", "person", "decided", "bare" or "other"
  picked,      \* a person picked the Ticket
  ppause,      \* a person's `Paused:` line stands on the effort
  opause,      \* the causes an orchestrator's pause stands for
  failing,     \* the causes outside the Ticket that fail now
  noted        \* the causes an orchestrator has written a pause for

evars == <<label, picked, ppause, opause, failing, noted>>
vars == <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
          branch, base, nextC, used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* The orchestrators' runs and the hand run.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A **hand run**, one a person starts by invoking `run-ticket` with a bare reference, writes as whatever account its session writes as"
Runners == Orchs \cup {Hand}

Rec(r, rdy, h, b, t) == [run |-> r, ready |-> rdy, head |-> h, base |-> b, timedOut |-> t]
HasRec == Len(recs) > 0
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Where two comments on a Ticket carry the same marker, the comment the venue created first decides"
TheRec == recs[1]
RunOf(r) == <<r, n[r]>>
LiveRun(r) == rpc[r] \in Live
Named(r) == HasRec /\ TheRec.run = RunOf(r)
NamedLive == \E r \in Runners : Named(r) /\ LiveRun(r)
Owner(o) == HasRec /\ TheRec.run[1] = o
Reopened == merged /\ ~landedNow     \* reopened after its pull request merged
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "The ready mark and the drafted answer name the run that wrote them, and count only while the run facts name that run"
ReadyValid == HasRec /\ TheRec.ready # None /\ TheRec.ready = TheRec.run
\* How the signpost's condition reads at its source now.
CondReads == IF "cond" \in used THEN "met" ELSE Signpost
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "It counts when a person with authority to grant set it, or when the automation identity set it while the deciding grant decision records a grant"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A grant state anyone else set, or one the automation identity set with no grant decided, grants nothing, and the Ticket reads as ungranted."
Granted == label \in {"person", "decided"}
\* Pre-fix: the grant state counts whoever set it.
Counts == IF Old("grant") THEN label # "none" ELSE Granted
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "**paused by an orchestrator** while any orchestrator's pause stands, one per cause"
Paused == ppause \/ opause # {}
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Paused only by orchestrator's pauses, each for a code-fixable cause, with no person's `Paused:` line; the Ticket is the repair Ticket a pause names"
\* Pre-fix: the repair Ticket runs under a person's pause too.
RepairLets == Repair /\ "check" \in opause /\ opause \subseteq CodeFixable /\ (~ppause \/ Old("repair"))
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Nothing starts in it — no launch, no landing turn — and live runs finish"
Held == Paused /\ ~RepairLets

Init ==
  /\ label = Grant /\ picked = FALSE /\ ppause = FALSE /\ opause = {}
  /\ failing = (IF Repair THEN {"check"} ELSE {}) /\ noted = {}
  /\ recs = << >> /\ claim = "none" /\ closed = FALSE /\ autoClosed = FALSE /\ landedNow = FALSE
  /\ mark = FALSE /\ prOpen = TRUE /\ merged = FALSE /\ red = FALSE /\ review = FALSE
  /\ branch = 0 /\ base = 0 /\ nextC = 1 /\ used = {}
  /\ opc = [o \in Orchs |-> "read"] /\ saw = [o \in Orchs |-> FALSE] /\ lview = [o \in Orchs |-> 0]
  /\ n = [r \in Runners |-> 0]
  /\ rpc = [r \in Runners |-> "none"] /\ rbase = [r \in Runners |-> 0] /\ rlocal = [r \in Runners |-> 0]
  /\ rmerged = [r \in Runners |-> 0] /\ bad = FALSE

---------------------------------------------------------------------------------------------
(* Orchestrator o *)

\* The sort, category by category, in its order.
\* Quote orchestrate/SKILL.md: "Each Ticket takes the first category below whose conditions hold, so it is in exactly one."
\* Quote orchestrate/SKILL.md: "A run that is not yours belongs to another orchestrator until row *Take over* lets you take its Ticket; leave it alone until then"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Take over** | The run facts name another orchestrator's run whose timeout has passed |"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "when it is deferred, its `Revisit when` condition read as met at the source it names"
\* Quote orchestrate/SKILL.md: "*Left alone*, each with its reason: the state *Dispatchable* or row *Launch* asks for that it lacks"
LeftAlone(o) ==
  \/ closed \/ mark \/ claim = "person"
  \/ HasRec /\ ~Owner(o) /\ ~TheRec.timedOut
  \* Pre-fix: the launcher does not read the signpost.
  \/ ~Old("deferred") /\ Signpost # "none" /\ CondReads # "met"
  \* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "either granted, written by an author with write access to the repository"
  \/ claim = "none" /\ ~Counts /\ ~Writer

\* Quote orchestrate/SKILL.md: "*Running*: its run facts name a live run."
Running == NamedLive

\* Quote orchestrate/SKILL.md: "*To land*: ready to land and not reopened after its merge, under a run of yours or one you adopt before its landing turn (row *Adopt a ready mark*)."
\* Pre-fix: a ready mark another orchestrator's run left fits no category.
ToLand(o) == ReadyValid /\ ~Reopened /\ (Owner(o) \/ ~Old("stranded"))

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "**To recover**: held by automation, no live run, and the last run wrote no outcome"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "marked ready a pull request that merged before the Ticket was reopened"
ToRecover == claim = "auto" /\ (~HasRec \/ ~ReadyValid \/ Reopened)

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "**Ready**: open, unclaimed, every Ticket it depends on closed"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "**Dispatchable**: ready, not escalated"
\* Quote orchestrate/SKILL.md: "*Ready*: dispatchable, and matching any type filter."
Ready == claim = "none"

\* Quote orchestrate/SKILL.md: "Read every Ticket in scope whole"
\* Quote orchestrate/SKILL.md: "from then on it sorts as below like one of yours (*Taking over*)"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "so no other orchestrator adopts the mark while its holder checks in"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "the effort not paused unless *Launch a repair Ticket* applies"
ORead(o) ==
  /\ opc[o] = "read" /\ ~LeftAlone(o) /\ ~Running /\ ~Held
  /\ \/ ToLand(o) /\ Owner(o) /\ opc' = [opc EXCEPT ![o] = "land"] /\ UNCHANGED saw
     \/ ToLand(o) /\ ~Owner(o) /\ n[o] < MaxRuns /\ opc' = [opc EXCEPT ![o] = "adopt"] /\ UNCHANGED saw
     \/ ~ToLand(o) /\ (ToRecover \/ Ready) /\ n[o] < MaxRuns
        /\ opc' = [opc EXCEPT ![o] = "claim"] /\ saw' = [saw EXCEPT ![o] = HasRec]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Adopting a ready mark: the run facts and the mark take a run ID of o's own, with a fresh start
\* time, the head and base kept, and no run started; the next read is the re-read after writing.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Adopt a ready mark** | Ready to land, the timeout of the run that wrote the mark passed, and no live run | An orchestrator |"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "keeps the head and base commits the mark names, the launch count and whether the last launch repaired a landing, and starts no run"
\* Quote orchestrate/SKILL.md: "Re-read the Ticket after an adoption"
OAdopt(o) ==
  /\ opc[o] = "adopt"
  /\ LET r == <<o, n[o] + 1>> IN
     /\ n' = [n EXCEPT ![o] = @ + 1]
     /\ recs' = [recs EXCEPT ![1] = [@ EXCEPT !.run = r, !.ready = r, !.timedOut = FALSE]]
  /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch, base,
                 nextC, used, saw, lview, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Quote orchestrate/SKILL.md: "Claim it and write the launch facts"
\* Quote orchestrate/SKILL.md: "Create the attempt record when the Ticket has none."
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "The run facts name a run of its own with a fresh start time, so its timeout runs from the takeover"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A comment edit replaces the whole comment, so the last writer wins"
OClaim(o) ==
  /\ opc[o] = "claim"
  /\ LET r == <<o, n[o] + 1>> IN
     \* An assignee a person set stays: the automation identity is added beside it.
     /\ claim' = (IF claim = "person" THEN "person" ELSE "auto") /\ n' = [n EXCEPT ![o] = @ + 1]
     \* Pre-fix and fixed alike, the launcher acts on what it read: a record it saw is edited in
     \* place, and with none seen it creates one. The fix adds the re-read in OVerify.
     /\ recs' = IF saw[o] /\ HasRec
                THEN [recs EXCEPT ![1] = [@ EXCEPT !.run = r, !.timedOut = FALSE]]
                ELSE Append(recs, Rec(r, None, 0, 0, FALSE))
  \* Pre-fix: no re-read after writing; the launcher starts its run at once.
  /\ opc' = [opc EXCEPT ![o] = IF Old("record") THEN "launch" ELSE "verify"]
  /\ UNCHANGED <<closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch, base,
                 nextC, used, saw, lview, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Quote orchestrate/SKILL.md: "Re-read the Ticket after writing"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A writer whose comment is not the first removes its own and stands down"
OVerify(o) ==
  /\ opc[o] = "verify"
  /\ IF Named(o) /\ ~closed /\ ~mark /\ claim # "person"
     THEN /\ opc' = [opc EXCEPT ![o] = "launch"] /\ UNCHANGED recs
     ELSE /\ recs' = IF HasRec /\ TheRec.run = RunOf(o) THEN recs
                     ELSE SelectSeq(recs, LAMBDA x : x.run # RunOf(o))
          /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                 base, nextC, used, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Quote orchestrate/SKILL.md: "Start a new agent session"
OLaunch(o) ==
  /\ opc[o] = "launch"
  /\ rpc' = [rpc EXCEPT ![o] = "start"] /\ opc' = [opc EXCEPT ![o] = "wait"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, saw, lview, n, rbase, rlocal, rmerged, bad, evars>>

\* Quote orchestrate/SKILL.md: "Check in whenever a run or a landing turn ends"
OWait(o) ==
  /\ opc[o] = "wait" /\ ~LiveRun(o)
  /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

Escalate(o) ==   \* the escalation record and mark go on first, then the claim is released
  /\ mark' = TRUE /\ claim' = "none" /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<recs, saw, n>>

Relaunch(o) ==   \* launch the run again, which writes fresh run facts
  /\ opc' = [opc EXCEPT ![o] = "claim"] /\ saw' = [saw EXCEPT ![o] = TRUE]
  /\ UNCHANGED <<recs, claim, mark, n>>

\* The landing turn, ticket-up/references/AUTOMATED_EXECUTION.md *Landing* steps 1 to 4.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "when the Ticket is closed; when a person holds the claim other than the identity it writes as or, on a hand run, the person who started it; or, on an unattended run or landing, when the Ticket is escalated"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A merged pull request counts as the Ticket's landing only when the Ticket was not reopened after that merge"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the base has moved since the base commit the record names, the run merges the base in"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the head is not the one the record names, or a required check fails, `orchestrate` relaunches the run to repair it"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A Ticket reopened after its merge is new work: the lander stops"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the merge waits only on a review the repository requires, the Ticket waits on the person's list as a held pull request, with no escalation mark"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When another protection needs what no run can give, or the pull request was closed without merging, the lander escalates"
\* Quote orchestrate/SKILL.md: "it keeps the turn meanwhile"
OLand(o) ==
  /\ opc[o] = "land"
  \* Pre-fix: the lander does not look for the escalation mark.
  /\ IF closed \/ claim = "person" \/ (mark /\ ~Old("escalated")) \/ ~ReadyValid \/ ~Owner(o) \/ Reopened
     THEN opc' = [opc EXCEPT ![o] = "read"] /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
     ELSE IF merged /\ landedNow   \* a person merged it since the Ticket was opened
     THEN /\ closed' = TRUE /\ autoClosed' = TRUE /\ claim' = "none" /\ opc' = [opc EXCEPT ![o] = "read"]
          /\ UNCHANGED <<recs, mark, saw, n, landedNow>>
     ELSE IF ~Counts   \* ungranted: it waits for a person to land it; the turn passes
     THEN opc' = [opc EXCEPT ![o] = "read"] /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
     ELSE IF ~Old("stall") /\ TheRec.base # base
     THEN Relaunch(o) /\ UNCHANGED <<closed, autoClosed, landedNow>>
     ELSE IF Old("stall") /\ (TheRec.base # base \/ branch # TheRec.head \/ red \/ review \/ ~prOpen)
     \* Pre-fix: the protections refuse a branch behind the base, and the lander "reports the
     \* current state and stops" for that and every other failure; nothing is relaunched.
     THEN opc' = [opc EXCEPT ![o] = "read"] /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
     ELSE IF branch # TheRec.head \/ red
     THEN Relaunch(o) /\ UNCHANGED <<closed, autoClosed, landedNow>>
     ELSE IF ~prOpen
     THEN Escalate(o) /\ UNCHANGED <<closed, autoClosed, landedNow>>
     ELSE IF review      \* held for the person's approval; the turn passes
     THEN opc' = [opc EXCEPT ![o] = "read"] /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
     ELSE /\ opc' = [opc EXCEPT ![o] = "merge"]
          /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
  /\ lview' = [lview EXCEPT ![o] = IF HasRec THEN TheRec.head ELSE 0]
  /\ UNCHANGED <<prOpen, merged, red, review, branch, base, nextC, used, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Merges with the head pinned"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A Ticket closes only after its landing is observed"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "closes the Ticket, and then releases the automation claim"
\* World: the repair Ticket's merge makes its check pass on the base.
OMerge(o) ==
  /\ opc[o] = "merge"
  /\ IF branch = lview[o] /\ prOpen /\ ~merged /\ HasRec /\ TheRec.base = base
        /\ ~closed /\ claim # "person" /\ (~mark \/ Old("escalated"))   \* Pre-fix: the mark is not looked for
     THEN /\ merged' = TRUE /\ landedNow' = TRUE /\ closed' = TRUE /\ autoClosed' = TRUE
          /\ claim' = "none" /\ bad' = (bad \/ mark) /\ opc' = [opc EXCEPT ![o] = "read"]
          /\ failing' = IF Repair THEN failing \ {"check"} ELSE failing
     ELSE /\ opc' = [opc EXCEPT ![o] = "land"] /\ UNCHANGED <<merged, landedNow, closed, autoClosed, claim, bad, failing>>
  /\ UNCHANGED <<recs, mark, prOpen, red, review, branch, base, nextC, used, saw, lview, n,
                 rpc, rbase, rlocal, rmerged, label, picked, ppause, opause, noted>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Pause by an orchestrator** | An effort whose Tickets fail on a cause outside them"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "with no orchestrator's pause naming that cause"
\* World: the one Ticket stands for as many of the effort's Tickets as the row asks to fail on the cause.
\* Pre-fix: an effort carries one orchestrator's pause, and a second cause's pause removes itself.
OPause(o) ==
  /\ opc[o] = "read"
  /\ \E c \in failing \ opause :
       /\ opause' = IF Old("percause") /\ opause # {} THEN opause ELSE opause \cup {c}
       /\ noted' = noted \cup {c}
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                 label, picked, ppause, failing>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "That pause removed; the effort stays paused while any other stands"
\* Quote orchestrate/SKILL.md: "An orchestrator's pause keeps the check-ins going: at each, check its cause, and lift it as row *Lift a pause* says."
OLift(o) ==
  /\ opc[o] = "read"
  /\ \E c \in opause \ failing : opause' = opause \ {c}
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                 label, picked, ppause, failing, noted>>

---------------------------------------------------------------------------------------------
(* The current run of runner r — an orchestrator's, or the hand run — whose run ID is RunOf(r) *)

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "when the Ticket is closed; when a person holds the claim other than the identity it writes as or, on a hand run, the person who started it; or, on an unattended run or landing, when the Ticket is escalated"
\* Quote run-ticket/SKILL.md: "stand down where `../ticket-up/references/AUTOMATED_EXECUTION.md` → *Transitions*, row *Stand down*, says"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "when the run ID in the record is not its own"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Hand run** | Open, whatever its grant or escalation mark"
\* Pre-fix: a hand run stands down on any person's claim, its starter's included.
Stops(r) == ~Named(r) \/ closed \/
            (IF r = Hand THEN Old("handrun") /\ claim = "person" ELSE claim = "person" \/ mark)

\* Quote run-ticket/SKILL.md: "there is nothing to redo only when the pull request's head is the head the record names, the base has not moved, and the recorded evidence still applies to the current criteria and actual subject, including relevant external state"
\* World: these configurations keep acceptance criteria and non-commit subject state fixed.
\* RWork abstracts successful verification and settlement of mandatory work. Evidence validity
\* under a changed criterion or receiver is outside this concurrency model; the acceptance-recovery
\* native scenario exercises that decision, not this check.
RStart(o) ==
  /\ rpc[o] = "start"
  /\ IF Stops(o) THEN /\ rpc' = [rpc EXCEPT ![o] = "stopped"] /\ UNCHANGED <<rbase, rlocal, rmerged>>
     ELSE IF TheRec.ready # None /\ branch = TheRec.head /\ TheRec.base = base
             /\ prOpen /\ ~merged /\ ~red /\ ~review
     THEN /\ rpc' = [rpc EXCEPT ![o] = "prewrite"] /\ rlocal' = [rlocal EXCEPT ![o] = branch]
          /\ rmerged' = [rmerged EXCEPT ![o] = base] /\ UNCHANGED rbase
     ELSE /\ rpc' = [rpc EXCEPT ![o] = "work"] /\ rbase' = [rbase EXCEPT ![o] = branch]
          /\ UNCHANGED <<rlocal, rmerged>>
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, opc, saw, lview, n, bad, evars>>

\* Quote run-ticket/SKILL.md: "Before each checkpoint, merge the target base in when it has moved"
RWork(o) ==
  /\ rpc[o] = "work"
  /\ rlocal' = [rlocal EXCEPT ![o] = nextC] /\ nextC' = nextC + 1
  /\ rmerged' = [rmerged EXCEPT ![o] = base] /\ rpc' = [rpc EXCEPT ![o] = "prepush"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, used, opc, saw, lview, n, rbase, bad, evars>>

\* Quote run-ticket/SKILL.md: "Re-read the record and the Ticket before each write and each push"
RPrePush(o) ==
  /\ rpc[o] = "prepush"
  /\ rpc' = [rpc EXCEPT ![o] = IF Stops(o) THEN "stopped" ELSE "push"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, opc, saw, lview, n, rbase, rlocal, rmerged, bad, evars>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "git rejects a push that does not build on the branch's head"
\* Quote run-ticket/SKILL.md: "a rejected push from a stale run stops it, and the run the record names merges what is there and pushes again"
\* Quote run-ticket/SKILL.md: "Push coherent checkpoints"
RPush(o) ==
  /\ rpc[o] = "push"
  /\ IF branch = rbase[o]
     THEN /\ branch' = rlocal[o] /\ rpc' = [rpc EXCEPT ![o] = "prewrite"]
          /\ prOpen' = TRUE /\ merged' = FALSE /\ red' = FALSE /\ UNCHANGED rbase
     ELSE IF Named(o)
     THEN /\ rbase' = [rbase EXCEPT ![o] = branch] /\ rpc' = [rpc EXCEPT ![o] = "work"]
          /\ UNCHANGED <<branch, prOpen, merged, red>>
     ELSE /\ rpc' = [rpc EXCEPT ![o] = "stopped"] /\ UNCHANGED <<branch, prOpen, merged, red, rbase>>
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, review, base, nextC, used, opc,
                 saw, lview, n, rlocal, rmerged, bad, evars>>

\* A run's re-read and the write after it are adjacent calls, so the model takes them as one
\* step. The window left between them costs at most a relaunch: the lander's head check and the
\* pinned merge still hold.
\* Quote run-ticket/SKILL.md: "set the run facts: ready to land at the verified head commit, against the base commit the gates passed against"
\* Quote run-ticket/SKILL.md: "Re-read the record and the Ticket before each write and each push"
RWriteReady(o) ==
  /\ rpc[o] = "prewrite"
  /\ IF Stops(o)
     THEN rpc' = [rpc EXCEPT ![o] = "stopped"] /\ UNCHANGED recs
     ELSE /\ recs' = [recs EXCEPT ![1] = Rec(RunOf(o), RunOf(o), rlocal[o], rmerged[o], FALSE)]
          /\ rpc' = [rpc EXCEPT ![o] = "done"]
  /\ UNCHANGED <<claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                 base, nextC, used, opc, saw, lview, n, rbase, rlocal, rmerged, bad, evars>>

---------------------------------------------------------------------------------------------
(* The world: each event at most once, when its configuration allows it *)

Event(e) == e \in Env /\ e \notin used /\ used' = used \cup {e}

\* World: a person, GitHub's "Update branch" or a bot adds a commit to the pull request's branch.
WPush == /\ Event("push") /\ ~closed /\ prOpen /\ ~merged
         /\ branch' = nextC /\ nextC' = nextC + 1
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        base, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: other work lands on the target branch, so the base moves.
WBase == /\ Event("base") /\ base' = base + 1
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        branch, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a required check fails after the ready mark.
WRed == /\ Event("red") /\ ~merged /\ red' = TRUE
        /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, review, branch,
                       base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a protection starts requiring a review only a person can give.
WReview == /\ Event("review") /\ ~merged /\ review' = TRUE
           /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: someone with write access approves the pull request.
WApprove == /\ Event("approve") /\ review /\ review' = FALSE
            /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, branch,
                           base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person applies the escalation mark to hold automation off.
WMark == /\ Event("mark") /\ ~closed /\ mark' = TRUE
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, prOpen, merged, red, review, branch,
                        base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person closes the pull request without merging it.
WPrClose == /\ Event("prclose") /\ prOpen /\ ~merged /\ prOpen' = FALSE
            /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, merged, red, review, branch,
                           base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person merges the pull request.
WMerge == /\ Event("pmerge") /\ prOpen /\ ~merged /\ ~closed /\ merged' = TRUE /\ landedNow' = TRUE
          /\ UNCHANGED <<recs, claim, closed, autoClosed, mark, prOpen, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person assigns themselves the Ticket.
WClaim == /\ Event("claim") /\ ~closed /\ claim' = "person"
          /\ UNCHANGED <<recs, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person closes the Ticket.
WClose == /\ Event("close") /\ ~closed /\ closed' = TRUE
          /\ UNCHANGED <<recs, claim, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a person reopens a Ticket automation closed, for example after a revert.
WReopen == /\ Event("reopen") /\ closed /\ autoClosed
           /\ closed' = FALSE /\ autoClosed' = FALSE /\ landedNow' = FALSE
           /\ UNCHANGED <<recs, claim, mark, prOpen, merged, red, review, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>
\* World: a live run's session dies before it writes an outcome.
WCrash == /\ Event("crash") /\ \E r \in Runners : LiveRun(r) /\ rpc' = [rpc EXCEPT ![r] = "dead"]
          /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                         branch, base, nextC, opc, saw, lview, n, rbase, rlocal, rmerged, bad, evars>>
\* World: the recorded run's timeout passes; its orchestrator stops a run still going. Where the
\* configuration lets an orchestrator stop, the timeout passes after it has stopped. A Ticket held
\* ready to land times out only once its holder has stopped, since the holder refreshes its start
\* time at each check-in. Nobody holds a hand run's ready mark, and no orchestrator stops a hand run.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "That timeout stands for the holder's absence, not the run's age"
\* Quote orchestrate/SKILL.md: "On each Ticket you hold ready to land, Auto or not, refresh the start time"
WTimeout == /\ Event("timeout") /\ HasRec /\ ("ostop" \in Env => "ostop" \in used)
            /\ ~(ReadyValid /\ TheRec.run[1] \in Orchs /\ opc[TheRec.run[1]] # "gone")
            /\ recs' = [recs EXCEPT ![1].timedOut = TRUE]
            /\ rpc' = [r \in Runners |-> IF r \in Orchs /\ Named(r) /\ LiveRun(r) THEN "dead" ELSE rpc[r]]
            /\ UNCHANGED <<claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                           branch, base, nextC, opc, saw, lview, n, rbase, rlocal, rmerged, bad, evars>>

\* World: an orchestrator's session ends for good (a host limit, the person closing it, its own
\* stop) while its run, if any, goes on; a later orchestrator takes a new ID.
WOStop == /\ Event("ostop") /\ \E o \in Orchs : opc[o] \in {"read", "wait"} /\ opc' = [opc EXCEPT ![o] = "gone"]
          /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                         branch, base, nextC, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* World: the deferred Ticket's condition comes true, or its source becomes readable and shows it met.
WCond == /\ Event("cond") /\ Signpost \in {"unmet", "unreadable"}
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        branch, base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Not escalated, and any automation claim cleared too"
\* Quote ticket-up/references/GITHUB_STORE.md: "removes the `escalated` label and any automation assignee"
WAnswer == /\ mark /\ mark' = FALSE /\ prOpen' = (prOpen \/ ~merged) /\ claim' = "none"
           /\ UNCHANGED <<recs, closed, autoClosed, landedNow, merged, red, review, branch, base, nextC,
                          used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad, evars>>

\* World: a person adds a `Paused:` line to the effort's front item.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Pause by a person** | An effort | A person, adding a `Paused:` line | Paused by a person, until a person removes the line |"
WPPause == /\ Event("ppause") /\ ppause' = TRUE
           /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                          label, picked, opause, failing, noted>>
\* World: the person removes their line; only a person does.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Only a person removes a person's line"
WPUnpause == /\ Event("punpause") /\ ppause /\ ppause' = FALSE
             /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                            base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                            label, picked, opause, failing, noted>>
\* World: a service the effort's Tickets need goes down, a cause no change to code fixes.
WOutage == /\ Event("outage") /\ failing' = failing \cup {"outage"}
           /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                          label, picked, ppause, opause, noted>>
\* World: the service comes back.
WUp == /\ Event("up") /\ "outage" \in failing /\ failing' = failing \ {"outage"}
       /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                      base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                      label, picked, ppause, opause, noted>>
\* World: someone without authority to grant sets the grant state on an ungranted Ticket.
WForge == /\ Event("forge") /\ label = "none" /\ label' = "other"
          /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                         picked, ppause, opause, failing, noted>>
\* World: a person withdraws the grant.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "| **Decline or withdraw** | Any | A person | Judged and ungranted, with any grant removed |"
\* Quote ticket-up/references/GITHUB_STORE.md: "A person withdraws a grant by removing the label"
WWithdraw == /\ Event("withdraw") /\ label # "none" /\ label' = "none"
             /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                            base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                            picked, ppause, opause, failing, noted>>

\* A person, or a picker in their name, picks the Ticket and claims it.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "a picker never writes the claim as the automation identity"
\* Quote next-ticket/SKILL.md: "a claim written as the store config's automation identity — the account unattended runs claim with — would read as an interrupted unattended attempt, which unattended work then resumes on the Ticket the person is working"
\* Pre-fix: the picker writes its claim as the session's account, which is the automation identity.
PPick == /\ Event("pick") /\ ~closed /\ claim = "none"
         /\ claim' = (IF Old("pick") THEN "auto" ELSE "person") /\ picked' = TRUE
         /\ UNCHANGED <<recs, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                        base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad,
                        label, ppause, opause, failing, noted>>

\* The person who picked the Ticket starts a hand run on it, at most once.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "no live run of another named, unless the person says that run is gone"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "The run claims, leaving a claim the person who started it holds in their name, writes its launch facts and is live"
\* Quote run-ticket/SKILL.md: "Without it, this is a hand run: mint a run ID and write the launch facts yourself"
HStart == /\ picked /\ rpc[Hand] = "none" /\ ~closed /\ ~NamedLive
          /\ LET r == <<Hand, n[Hand] + 1>> IN
             /\ n' = [n EXCEPT ![Hand] = @ + 1]
             /\ recs' = IF HasRec THEN [recs EXCEPT ![1] = [@ EXCEPT !.run = r, !.timedOut = FALSE]]
                         ELSE Append(recs, Rec(r, None, 0, 0, FALSE))
          /\ claim' = IF claim = "none" THEN "auto" ELSE claim
          /\ rpc' = [rpc EXCEPT ![Hand] = "start"]
          /\ UNCHANGED <<closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, used, opc, saw, lview, rbase, rlocal, rmerged, bad, evars>>

Next ==
  \/ \E o \in Orchs : ORead(o) \/ OAdopt(o) \/ OClaim(o) \/ OVerify(o) \/ OLaunch(o) \/ OWait(o) \/ OLand(o) \/ OMerge(o)
  \/ \E o \in Orchs : OPause(o) \/ OLift(o)
  \/ \E r \in Runners : RStart(r) \/ RWork(r) \/ RPrePush(r) \/ RPush(r) \/ RWriteReady(r)
  \/ WPush \/ WBase \/ WRed \/ WReview \/ WApprove \/ WMark \/ WPrClose \/ WMerge \/ WClaim \/ WClose
  \/ WReopen \/ WCrash
  \/ WTimeout \/ WAnswer \/ WCond \/ WOStop
  \/ WPPause \/ WPUnpause \/ WOutage \/ WUp \/ WForge \/ WWithdraw \/ PPick \/ HStart

Fair == /\ \A o \in Orchs :
             /\ WF_vars(ORead(o)) /\ WF_vars(OAdopt(o)) /\ WF_vars(OClaim(o)) /\ WF_vars(OVerify(o)) /\ WF_vars(OLaunch(o))
             /\ WF_vars(OWait(o)) /\ WF_vars(OLand(o)) /\ WF_vars(OMerge(o)) /\ WF_vars(OPause(o)) /\ WF_vars(OLift(o))
        /\ \A r \in Runners :
             /\ WF_vars(RStart(r)) /\ WF_vars(RWork(r)) /\ WF_vars(RPrePush(r)) /\ WF_vars(RPush(r))
             /\ WF_vars(RWriteReady(r))

\* World: time passes, so once an orchestrator has stopped, its run's timeout passes.
Spec == Init /\ [][Next]_vars /\ Fair /\ WF_vars(WTimeout /\ "ostop" \in used)

---------------------------------------------------------------------------------------------
(* Properties *)

\* Property: one attempt record decides the Ticket; a second comment with its marker lasts only
\* until its writer's re-read, which removes it.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Each Ticket has one attempt record"
OneAttemptRecord == Len(recs) <= 1 \/ \E o \in Orchs : opc[o] = "verify"

\* Property: a push lands on the branch only when it builds on the branch's head, so a push from
\* a run the record no longer names is rejected or is a commit the named run builds on.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "git rejects a push that does not build on the branch's head"
PushesBuildOnHead == [][\A o \in Orchs : (rpc[o] = "push" /\ rpc'[o] = "prewrite") => branch = rbase[o]]_vars

\* Property: automation merges only at the head the record named when the lander read it.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Merges with the head pinned"
MergesOnlyRecordedHead == [][\A o \in Orchs : (opc[o] = "merge" /\ opc'[o] # "merge" /\ ~merged /\ merged') => branch = lview[o]]_vars

\* Property: automation closes a Ticket only after a landing observed since it was last opened.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A Ticket closes only after its landing is observed"
ClosedOnlyWhenLanded == autoClosed => landedNow

\* Property: automation never merges a Ticket that carries the escalation mark.
\* Quote ticket-up/references/TICKET_CONVENTION.md: "Unattended dispatch never touches a Ticket carrying the escalation mark"
NoLandWhileEscalated == ~bad

\* Holds docs/adr/20261021-the-north-star-opens-with-its-end-and-signposts-reopen-choices-and-deferred-work.md.
\* Property: a deferred Ticket is launched only after its condition reads as met at its source;
\* unmet or unreadable, it is never claimed.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A deferred Ticket whose source cannot be read is not ready"
LaunchedOnlyWhenMet == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] = "claim") => (Signpost = "none" \/ CondReads = "met")]_vars

\* Property: every Ticket marked ready to land is landed, handed to a person through an
\* escalation record, taken by a person (claimed or closed), or held for a review only a person
\* gives, within the model's bound; or it waits on a person to land it or on its effort's pause.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "No Ticket keeps a landing turn while nothing works toward its landing."
\* An ungranted Ticket waits for a person to land it, and a held effort for its pause to lift.
ReadyResolves == [](ReadyValid /\ ~closed => <>(closed \/ mark \/ claim = "person" \/ review \/ ~Granted \/ Held))

\* Property: an orchestrator adopts a ready mark only from a holder that has stopped, so a Ticket
\* held ready to land never changes hands while its holder still checks in.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "so no other orchestrator adopts the mark while its holder checks in"
AdoptsOnlyFromAStoppedHolder == [][\A o \in Orchs : (opc[o] = "adopt" /\ opc'[o] = "read") => (TheRec.run[1] \notin Orchs \/ opc[TheRec.run[1]] = "gone")]_vars

\* Property: a ready pull request held only for a review a person gives is never launched again.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A ready pull request or drafted answer uses its existing held state instead; it is never redispatched merely because acceptance has not arrived."
HeldNotRedispatched == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] = "claim") =>
    ~(ReadyValid /\ review /\ ~red /\ prOpen /\ ~merged /\ branch = TheRec.head /\ TheRec.base = base)]_vars

\* Holds docs/adr/20261108-the-ticket-protocols-moves-have-one-owning-table.md for the areas below.
\* Property: an orchestrator lands a Ticket only when its grant counts by who set the grant state.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "never an orchestrator on an ungranted Ticket, which only a person lands"
LandsOnlyGranted == [][\A o \in Orchs : (opc[o] = "land" /\ opc'[o] = "merge") => Granted]_vars

\* Property: an orchestrator launches an unclaimed Ticket only when it is dispatchable: its grant
\* counts, or its author has write access.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "either granted, written by an author with write access to the repository"
LaunchesOnlyDispatchable == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] = "claim" /\ claim = "none") => (Granted \/ Writer)]_vars

\* Property: no orchestrator launches, adopts or lands a Ticket a person picked.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "**To recover**: held by automation, no live run"
NeverTakesAPick == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] \in {"claim", "adopt", "land"}) => ~picked]_vars

\* Property: a hand run stands down only when the record names another run or the Ticket is
\* closed, never on the claim of the person who started it.
\* Quote run-ticket/SKILL.md: "row *Hand run* for a hand run"
HandRunKeepsItsStartersClaim == [][(LiveRun(Hand) /\ rpc'[Hand] = "stopped") => (~Named(Hand) \/ closed)]_vars

\* Property: nothing starts in a paused effort but the repair Ticket an orchestrator's pause names,
\* and that only while every pause is for a code-fixable cause and no person's line stands.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Nothing starts in it — no launch, no landing turn — and live runs finish"
NothingStartsWhilePaused == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] \in {"claim", "adopt", "land"}) =>
    (~Paused \/ (Repair /\ "check" \in opause /\ opause \subseteq CodeFixable /\ ~ppause))]_vars

\* Property: an effort stays paused while a cause an orchestrator paused it for still fails.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "That pause removed; the effort stays paused while any other stands"
PausedWhileACauseFails == noted \cap failing # {} => opause # {}

\* Property: once only code-fixable pauses hold the effort and no person's line stands, the repair
\* Ticket lands and its pause lifts.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "*Launch* and *Land* apply to it as though the effort were not paused"
RepairLifts == []("check" \in opause /\ ~ppause /\ "outage" \notin failing =>
    <>("check" \notin opause \/ ppause \/ "outage" \in failing))
=============================================================================
