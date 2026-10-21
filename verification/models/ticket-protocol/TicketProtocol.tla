--------------------------- MODULE TicketProtocol ---------------------------
(* A model of manifest-dev's unattended Ticket protocol, for one Ticket.

   The shipped prose is the code this models. Each action and property below carries the
   sentences it encodes as `Quote <file>: "<sentence>"` comments, paths relative to
   claude-plugins/manifest-dev/skills/; tests/test_ticket_protocol_model.py fails when a quoted
   sentence leaves its file. An action that models the world rather than the protocol carries a
   `World:` comment instead, and a branch that restores an old, wrong behavior is marked `Pre-fix:`.

   Scope: one Ticket; the orchestrators in Orchs, sharing one automation identity, each able to
   launch, take over and land; one run per launch; a person who can push to the pull request's
   branch, claim, close or reopen the Ticket, close or approve the pull request, apply the
   escalation mark, and answer an escalation;
   a base branch that moves at most once; each world event at most once. Liveness holds within
   that bound. The three-failed-launches escalation is outside it: one crash at most.

   A deferred Ticket's signpost is world state: its condition reads as met, unmet or unreadable at
   the source it names, as Signpost says at the start, and the world may make it read as met once.

   PreFix = TRUE switches four behaviors back to the protocol as it stood before this model: the
   landing check stops with nothing relaunched or escalated when the head, a check or a
   protection fails; a launcher decides from its earlier read whether to create the attempt
   record; the lander does not look for the escalation mark; and a launcher does not read a
   deferred Ticket's signpost. The `prefix` scenario of
   verification/recipes/ticket-protocol-model.md expects TLC to report all four. *)
EXTENDS Integers, Sequences

CONSTANTS Orchs,     \* the orchestrators sharing the automation identity
          Env,       \* the world events this configuration allows, each at most once
          PreFix,    \* TRUE restores the three old behaviors described above
          MaxRuns,   \* launches per orchestrator, a bound for TLC; no run reaches it
          Signpost   \* "none" (not deferred), or how its condition reads at the start: "met", "unmet" or "unreadable"

None == <<"", 0>>                       \* no run
Live == {"start", "work", "prepush", "push", "prewrite"}

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
  opc,         \* each orchestrator's step
  saw,         \* whether it saw an attempt record at its last read
  lview,       \* the head it read from the record before merging
  n,           \* how many runs it has launched
  rpc, rbase, rlocal, rmerged, \* its current run: step, head it built on, commit it made, base it merged
  bad          \* set when automation merges a Ticket that carries the escalation mark

vars == <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
          branch, base, nextC, used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>

Rec(r, rdy, h, b, t) == [run |-> r, ready |-> rdy, head |-> h, base |-> b, timedOut |-> t]
HasRec == Len(recs) > 0
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Where two comments on a Ticket carry the same marker, the comment the venue created first decides"
TheRec == recs[1]
RunOf(o) == <<o, n[o]>>
LiveRun(o) == rpc[o] \in Live
Named(o) == HasRec /\ TheRec.run = RunOf(o)
NamedLive == \E o \in Orchs : Named(o) /\ LiveRun(o)
Owner(o) == HasRec /\ TheRec.run[1] = o
Reopened == merged /\ ~landedNow     \* reopened after its pull request merged
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "The ready mark and the drafted answer name the run that wrote them, and count only while the run facts name that run"
ReadyValid == HasRec /\ TheRec.ready # None /\ TheRec.ready = TheRec.run
\* How the signpost's condition reads at its source now.
CondReads == IF "cond" \in used THEN "met" ELSE Signpost

Init ==
  /\ recs = << >> /\ claim = "none" /\ closed = FALSE /\ autoClosed = FALSE /\ landedNow = FALSE
  /\ mark = FALSE /\ prOpen = TRUE /\ merged = FALSE /\ red = FALSE /\ review = FALSE
  /\ branch = 0 /\ base = 0 /\ nextC = 1 /\ used = {}
  /\ opc = [o \in Orchs |-> "read"] /\ saw = [o \in Orchs |-> FALSE] /\ lview = [o \in Orchs |-> 0]
  /\ n = [o \in Orchs |-> 0]
  /\ rpc = [o \in Orchs |-> "none"] /\ rbase = [o \in Orchs |-> 0] /\ rlocal = [o \in Orchs |-> 0]
  /\ rmerged = [o \in Orchs |-> 0] /\ bad = FALSE

---------------------------------------------------------------------------------------------
(* Orchestrator o *)

\* Quote orchestrate/SKILL.md: "*Ready*: open, unclaimed, every dependency closed, no escalation mark"
\* Quote orchestrate/SKILL.md: "*To recover*: the automation identity holds its claim, no run is live"
\* Quote orchestrate/SKILL.md: "or marked ready a pull request that merged before the Ticket was reopened"
\* Quote orchestrate/SKILL.md: "A run that is not yours belongs to another orchestrator until its timeout has passed, live or not; leave its Ticket alone until then."
\* Quote ticket-up/references/TICKET_CONVENTION.md: "when it is deferred — its `Revisit when` condition reads as met at the source it names"
\* Quote orchestrate/SKILL.md: "its signpost read as met at its source when it is deferred"
Takeable(o) ==
  /\ ~closed /\ ~mark /\ claim # "person" /\ ~NamedLive /\ n[o] < MaxRuns
  \* Pre-fix: the launcher does not read the signpost.
  /\ PreFix \/ Signpost = "none" \/ CondReads = "met"
  /\ \/ claim = "none"
     \/ claim = "auto" /\ ~HasRec
     \/ claim = "auto" /\ HasRec /\ Owner(o) /\ (~ReadyValid \/ Reopened)
     \/ claim = "auto" /\ HasRec /\ ~Owner(o) /\ TheRec.timedOut

\* Quote orchestrate/SKILL.md: "*To land*: its record is marked ready to land by a run of yours and no run is live, and the Ticket was not reopened after its pull request merged."
ToLand(o) == ~closed /\ claim = "auto" /\ ~mark /\ ReadyValid /\ Owner(o) /\ ~NamedLive /\ ~Reopened

\* Quote orchestrate/SKILL.md: "Read every Ticket in scope whole"
ORead(o) ==
  /\ opc[o] = "read"
  /\ \/ ToLand(o) /\ opc' = [opc EXCEPT ![o] = "land"] /\ UNCHANGED saw
     \/ ~ToLand(o) /\ Takeable(o) /\ opc' = [opc EXCEPT ![o] = "claim"] /\ saw' = [saw EXCEPT ![o] = HasRec]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, lview, n, rpc, rbase, rlocal, rmerged, bad>>

\* Quote orchestrate/SKILL.md: "Claim it and write the launch facts"
\* Quote orchestrate/SKILL.md: "Create the attempt record when the Ticket has none."
\* Quote orchestrate/SKILL.md: "A takeover writes a fresh start time"
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
  /\ opc' = [opc EXCEPT ![o] = IF PreFix THEN "launch" ELSE "verify"]
  /\ UNCHANGED <<closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch, base,
                 nextC, used, saw, lview, rpc, rbase, rlocal, rmerged, bad>>

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
                 base, nextC, used, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>

\* Quote orchestrate/SKILL.md: "Start a new agent session"
OLaunch(o) ==
  /\ opc[o] = "launch"
  /\ rpc' = [rpc EXCEPT ![o] = "start"] /\ opc' = [opc EXCEPT ![o] = "wait"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, saw, lview, n, rbase, rlocal, rmerged, bad>>

\* Quote orchestrate/SKILL.md: "Check in whenever a run or a landing turn ends"
OWait(o) ==
  /\ opc[o] = "wait" /\ ~LiveRun(o)
  /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>

Escalate(o) ==   \* the escalation record and mark go on first, then the claim is released
  /\ mark' = TRUE /\ claim' = "none" /\ opc' = [opc EXCEPT ![o] = "read"]
  /\ UNCHANGED <<recs, saw, n>>

Relaunch(o) ==   \* launch the run again, which writes fresh run facts
  /\ opc' = [opc EXCEPT ![o] = "claim"] /\ saw' = [saw EXCEPT ![o] = TRUE]
  /\ UNCHANGED <<recs, claim, mark, n>>

\* The landing turn, ticket-up/references/AUTOMATED_EXECUTION.md *Landing* steps 1 to 4.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "It stops when the Ticket is closed, carries the escalation mark, or a person holds the claim"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A merged pull request counts as the Ticket's landing only when the Ticket was not reopened after that merge"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the base has moved since the base commit the record names, the run merges the base in"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the head is not the one the record names, or a required check fails, `orchestrate` relaunches the run to repair it"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A Ticket reopened after its merge is new work: the lander stops"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When the merge waits only on a review the repository requires, the Ticket waits on the person's list as a held pull request, with no escalation mark"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "When another protection needs what no run can give, or the pull request was closed without merging, the lander writes the escalation record"
\* Quote orchestrate/SKILL.md: "it keeps the turn meanwhile"
OLand(o) ==
  /\ opc[o] = "land"
  \* Pre-fix: the lander does not look for the escalation mark.
  /\ IF closed \/ claim = "person" \/ (mark /\ ~PreFix) \/ ~ReadyValid \/ ~Owner(o) \/ Reopened
     THEN opc' = [opc EXCEPT ![o] = "read"] /\ UNCHANGED <<recs, claim, mark, saw, n, closed, autoClosed, landedNow>>
     ELSE IF merged /\ landedNow   \* a person merged it since the Ticket was opened
     THEN /\ closed' = TRUE /\ autoClosed' = TRUE /\ opc' = [opc EXCEPT ![o] = "read"]
          /\ UNCHANGED <<recs, claim, mark, saw, n, landedNow>>
     ELSE IF ~PreFix /\ TheRec.base # base
     THEN Relaunch(o) /\ UNCHANGED <<closed, autoClosed, landedNow>>
     ELSE IF PreFix /\ (TheRec.base # base \/ branch # TheRec.head \/ red \/ review \/ ~prOpen)
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
  /\ UNCHANGED <<prOpen, merged, red, review, branch, base, nextC, used, rpc, rbase, rlocal, rmerged, bad>>

\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "Merges with the head pinned"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "A Ticket closes only after its landing is observed"
OMerge(o) ==
  /\ opc[o] = "merge"
  /\ IF branch = lview[o] /\ prOpen /\ ~merged /\ HasRec /\ TheRec.base = base
        /\ ~closed /\ claim # "person" /\ (~mark \/ PreFix)   \* Pre-fix: the mark is not looked for
     THEN /\ merged' = TRUE /\ landedNow' = TRUE /\ closed' = TRUE /\ autoClosed' = TRUE
          /\ bad' = (bad \/ mark) /\ opc' = [opc EXCEPT ![o] = "read"]
     ELSE /\ opc' = [opc EXCEPT ![o] = "land"] /\ UNCHANGED <<merged, landedNow, closed, autoClosed, bad>>
  /\ UNCHANGED <<recs, claim, mark, prOpen, red, review, branch, base, nextC, used, saw, lview, n,
                 rpc, rbase, rlocal, rmerged>>

---------------------------------------------------------------------------------------------
(* The current run of orchestrator o, whose run ID is RunOf(o) *)

\* Quote run-ticket/SKILL.md: "stops when a person other than the identity it writes as is assigned, when the Ticket is closed, or — on an unattended run — when the escalation mark is on"
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "stops without writing when the run ID there is not its own"
Stops(o) == ~Named(o) \/ closed \/ claim = "person" \/ mark

\* Quote run-ticket/SKILL.md: "there is nothing to redo only when the pull request's head is the head the record names and the base has not moved"
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
                 branch, base, nextC, used, opc, saw, lview, n, bad>>

\* Quote run-ticket/SKILL.md: "Before each checkpoint, merge the target base in when it has moved"
RWork(o) ==
  /\ rpc[o] = "work"
  /\ rlocal' = [rlocal EXCEPT ![o] = nextC] /\ nextC' = nextC + 1
  /\ rmerged' = [rmerged EXCEPT ![o] = base] /\ rpc' = [rpc EXCEPT ![o] = "prepush"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, used, opc, saw, lview, n, rbase, bad>>

\* Quote run-ticket/SKILL.md: "Re-read the record and the Ticket before each write and each push"
RPrePush(o) ==
  /\ rpc[o] = "prepush"
  /\ rpc' = [rpc EXCEPT ![o] = IF Stops(o) THEN "stopped" ELSE "push"]
  /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                 branch, base, nextC, used, opc, saw, lview, n, rbase, rlocal, rmerged, bad>>

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
                 saw, lview, n, rlocal, rmerged, bad>>

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
                 base, nextC, used, opc, saw, lview, n, rbase, rlocal, rmerged, bad>>

---------------------------------------------------------------------------------------------
(* The world: each event at most once, when its configuration allows it *)

Event(e) == e \in Env /\ e \notin used /\ used' = used \cup {e}

\* World: a person, GitHub's "Update branch" or a bot adds a commit to the pull request's branch.
WPush == /\ Event("push") /\ ~closed /\ prOpen /\ ~merged
         /\ branch' = nextC /\ nextC' = nextC + 1
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        base, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: other work lands on the target branch, so the base moves.
WBase == /\ Event("base") /\ base' = base + 1
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        branch, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a required check fails after the ready mark.
WRed == /\ Event("red") /\ ~merged /\ red' = TRUE
        /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, review, branch,
                       base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a protection starts requiring a review only a person can give.
WReview == /\ Event("review") /\ ~merged /\ review' = TRUE
           /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: someone with write access approves the pull request.
WApprove == /\ Event("approve") /\ review /\ review' = FALSE
            /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, branch,
                           base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person applies the escalation mark to hold automation off.
WMark == /\ Event("mark") /\ ~closed /\ mark' = TRUE
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, prOpen, merged, red, review, branch,
                        base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person closes the pull request without merging it.
WPrClose == /\ Event("prclose") /\ prOpen /\ ~merged /\ prOpen' = FALSE
            /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, merged, red, review, branch,
                           base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person merges the pull request.
WMerge == /\ Event("pmerge") /\ prOpen /\ ~merged /\ ~closed /\ merged' = TRUE /\ landedNow' = TRUE
          /\ UNCHANGED <<recs, claim, closed, autoClosed, mark, prOpen, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person assigns themselves the Ticket.
WClaim == /\ Event("claim") /\ ~closed /\ claim' = "person"
          /\ UNCHANGED <<recs, closed, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person closes the Ticket.
WClose == /\ Event("close") /\ ~closed /\ closed' = TRUE
          /\ UNCHANGED <<recs, claim, autoClosed, landedNow, mark, prOpen, merged, red, review, branch,
                         base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a person reopens a Ticket automation closed, for example after a revert.
WReopen == /\ Event("reopen") /\ closed /\ autoClosed
           /\ closed' = FALSE /\ autoClosed' = FALSE /\ landedNow' = FALSE
           /\ UNCHANGED <<recs, claim, mark, prOpen, merged, red, review, branch,
                          base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>
\* World: a live run's session dies before it writes an outcome.
WCrash == /\ Event("crash") /\ \E o \in Orchs : LiveRun(o) /\ rpc' = [rpc EXCEPT ![o] = "dead"]
          /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                         branch, base, nextC, opc, saw, lview, n, rbase, rlocal, rmerged, bad>>
\* World: the recorded run's timeout passes; its orchestrator stops a run still going.
WTimeout == /\ Event("timeout") /\ HasRec
            /\ recs' = [recs EXCEPT ![1].timedOut = TRUE]
            /\ rpc' = [o \in Orchs |-> IF Named(o) /\ LiveRun(o) THEN "dead" ELSE rpc[o]]
            /\ UNCHANGED <<claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                           branch, base, nextC, opc, saw, lview, n, rbase, rlocal, rmerged, bad>>

\* World: the deferred Ticket's condition comes true, or its source becomes readable and shows it met.
WCond == /\ Event("cond") /\ Signpost \in {"unmet", "unreadable"}
         /\ UNCHANGED <<recs, claim, closed, autoClosed, landedNow, mark, prOpen, merged, red, review,
                        branch, base, nextC, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>

\* Quote orchestrate/SKILL.md: "clearing the mark also clears any automation claim"
\* Quote ticket-up/references/GITHUB_STORE.md: "removes the `escalated` label and any automation assignee"
WAnswer == /\ mark /\ mark' = FALSE /\ prOpen' = (prOpen \/ ~merged) /\ claim' = "none"
           /\ UNCHANGED <<recs, closed, autoClosed, landedNow, merged, red, review, branch, base, nextC,
                          used, opc, saw, lview, n, rpc, rbase, rlocal, rmerged, bad>>

Next ==
  \/ \E o \in Orchs : ORead(o) \/ OClaim(o) \/ OVerify(o) \/ OLaunch(o) \/ OWait(o) \/ OLand(o) \/ OMerge(o)
  \/ \E o \in Orchs : RStart(o) \/ RWork(o) \/ RPrePush(o) \/ RPush(o) \/ RWriteReady(o)
  \/ WPush \/ WBase \/ WRed \/ WReview \/ WApprove \/ WMark \/ WPrClose \/ WMerge \/ WClaim \/ WClose
  \/ WReopen \/ WCrash
  \/ WTimeout \/ WAnswer \/ WCond

Fair == \A o \in Orchs :
          /\ WF_vars(ORead(o)) /\ WF_vars(OClaim(o)) /\ WF_vars(OVerify(o)) /\ WF_vars(OLaunch(o))
          /\ WF_vars(OWait(o)) /\ WF_vars(OLand(o)) /\ WF_vars(OMerge(o))
          /\ WF_vars(RStart(o)) /\ WF_vars(RWork(o)) /\ WF_vars(RPrePush(o)) /\ WF_vars(RPush(o))
          /\ WF_vars(RWriteReady(o))

Spec == Init /\ [][Next]_vars /\ Fair

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

\* Property: a deferred Ticket is launched only after its condition reads as met at its source;
\* unmet or unreadable, it is never claimed.
\* Quote ticket-up/references/TICKET_CONVENTION.md: "A deferred ticket whose source the picker cannot read is not ready and not out of sight"
LaunchedOnlyWhenMet == [][\A o \in Orchs : (opc[o] = "read" /\ opc'[o] = "claim") => (Signpost = "none" \/ CondReads = "met")]_vars

\* Property: every Ticket marked ready to land is landed, handed to a person through an
\* escalation record, taken by a person (claimed or closed), or held for a review only a person
\* gives, within the model's bound.
\* Quote ticket-up/references/AUTOMATED_EXECUTION.md: "No Ticket keeps a landing turn while nothing works toward its landing."
ReadyResolves == [](ReadyValid /\ ~closed => <>(closed \/ mark \/ claim = "person" \/ review))
=============================================================================
