# Glossary

Each entry says what the term is and why it exists. The entries are in groups that follow the work:
the Manifest, the run, the investigation of a problem, the project, verification, Tickets, and pull
requests.

## The Manifest and its gates

### Manifest
<!-- context: d036ce7b9fad -->
A Manifest is the file that `/define` writes for one piece of work. It holds the Intent, an Initial
Approach, Global Invariants, Process Guidance, Known Assumptions and Deliverables. It is the
contract for one run: `/do` reads it and makes each of its gates pass. It exists so that "done" is
written before the work starts. An agent with no memory of the conversation can then do the work and
prove it.

### Deliverable
<!-- context: 82b80e1e5a45 -->
A Deliverable is one part of the work in a Manifest. It is a slice that you can complete alone and
use from end to end. A layer such as "the data model" is not a Deliverable, because you can only see
that it exists. Because you can use a Deliverable, its Acceptance Criteria can show that it works.

### Acceptance Criterion
<!-- context: 5d2896084ea1 -->
An Acceptance Criterion is a gate for one Deliverable. It says what "done" means for that
Deliverable and which evidence shows it. `/do` cannot finish while one Acceptance Criterion has no
evidence that it passes. It exists so that each Deliverable has its own measure of "done".

### Global Invariant
<!-- context: e6b12288a208 -->
A Global Invariant is a gate that applies to all Deliverables in a Manifest. It holds a rule that
the whole change must obey, for example "no test becomes weaker". A rule whose violation is unsafe
or permanent always becomes a Global Invariant, so that it binds.

### Gate
<!-- context: 880012b6b782 -->
A gate is an Acceptance Criterion or a Global Invariant. `/do` must make each gate pass, with
evidence, before it reports that the work is done. Each gate is one Gate Text, and it declares its
kind: judgment or deterministic. Gates exist so that "done" is a result that you can examine, not a
claim.

### Gate Text
<!-- context: 3e67f465b2a4 -->
A Gate Text is the one text that a gate is: a title, a body and an optional "why". The body says
what "done" means and which evidence decides it. The title and the "why" add no requirement. The
person who reviews the gate and the agent that evaluates it read the same text. Thus they cannot
read two different requirements.

### Gate Extension
<!-- context: 10b8e7251d4a -->
Gate Extension is how many items a gate examines. An open gate tells the evaluator to find all items
in an area, so it also finds an item that is new tomorrow. A closed gate examines a list that its
author wrote. `/define` sets it when it writes the gate.

### Judgment Gate
<!-- context: 779fbeb37877 -->
A Judgment Gate is a gate that a model decides by judgment, for example a code review. A new
evaluation can find new findings, also when nothing changed. For this reason, `/do` examines it
again with the Ratchet.

### Deterministic Gate
<!-- context: 46b64bda2413 -->
A Deterministic Gate is a gate that a command decides, for example tests, a build or a type check.
The same files always give the same result. `/do` runs it again in full each time that it examines
the gate. Its result does not change by chance, so it needs no Ratchet.

### Ratchet
<!-- context: 169dab6ec6d2 -->
The Ratchet is how `/do` examines a Judgment Gate again after a repair. The first evaluation reads
the full change. Later evaluations check open findings and problems caused or exposed by the new
changes. They carry the earlier criteria, subject state, and finding results. New external evidence
can still show a real failure in material already reviewed.

### Process Guidance
<!-- context: e7359da1f511 -->
Process Guidance is advice in a Manifest about how to do the work. It does not bind. `/do` can
depart from it, but it names each departure in its report, and in its Execution Log when it keeps
one. It exists so that good practice reaches the run, and the run can still adapt where the advice
does not fit. Only Acceptance Criteria and Global Invariants bind.

### Known Assumption
<!-- context: 5724e7b179f1 -->
A Known Assumption is an entry in a Manifest, with an `ASM-` number. It records a decision that the
Manifest uses. The skill took the decision with a default instead of a question, or it is a User's
Call: a decision that is yours to make. It gives the value, the reason and the result if the
decision is wrong. An autonomous choice has the mark `(auto)`, and a User's Call starts with
the words "User's call:". Thus you can examine what was decided, and who decided it.

The Known Assumptions are the only part of a Manifest that tells who decided what. They do not
give the date of a decision. All other parts of the Manifest tell only what is true now. Thus you
can read it without knowing how it was changed after it was first written.

### Appetite
<!-- context: 78ddd6db6bcb -->
Appetite is the size of change that a problem is worth. It limits complexity and the size of the
area that changes, not time or tokens. `/do` can increase it before broader work starts, but only
when the benefit to your result is larger than the added complexity. An increase never changes your
exclusions or the requirements that bind. It exists so that a run does not grow the change past what
the problem is worth.

### Quality Gate
<!-- context: 94633852f506 -->
A Quality Gate is a gate that a Task File gives to `/define`. `/define` adds it to the Manifest
without a question, as an Acceptance Criterion or a Global Invariant. It exists so that each kind of
work gets the checks that it usually must have.

### Default
<!-- context: e07a4827d03e -->
A Default is a practice that a Task File gives to `/define`. `/define` adds it to the Manifest as
Process Guidance, without a question. When a violation is unsafe or permanent, the Default becomes a
Global Invariant instead, so that it binds. It exists so that each kind of work gets its usual good
practice without a question to you.

### Task File
<!-- context: fe0621ffd996 -->
A Task File is a file of hints for one kind of work, such as a bug, a feature or a document. The
Task Files of `/figure-out` give questions to ask. The Task Files of `/define` give Quality Gates
and Defaults. The two sets are separate, so each skill can work alone.

### Bearer Test
<!-- context: 163b91c1121d -->
The Bearer Test decides when `/define` can omit an advisory Quality Gate. Each advisory gate
protects a future activity, for example a later change or a later reader. `/define` omits the gate
only when that activity will not occur during the life of the work. It records that fact as a Known
Assumption.

## The run

### Do/Verify Loop
<!-- context: a2124e071283 -->
The Do/Verify Loop is the cycle of `/do`. It does the work, examines each gate, repairs each failure
and reports each blocker. It stops only when all gates pass, or when a person must act.

### Execution Log
<!-- context: dfc703472a78 -->
The Execution Log is a file that `/do` keeps outside the repository for each Manifest. It records
departures from the plan, dead ends and other events of the run. Its name comes from the Manifest,
so a new run of the same Manifest finds it and continues from it. The option `--no-log` disables it.

### Steering Message
<!-- context: b9812c57bb2e -->
A Steering Message is a message that you send to `/do` while it works. `/do` changes the Manifest to
include it, and the run continues. It does not wait for more conversation. Thus you can give a new
direction and then leave again.

### Host Continuation Backstop
<!-- context: f68fc8d2c161 -->
A Host Continuation Backstop is a feature of your agent host that keeps a run active until a goal is
complete. `/do` sets it, with the path of the Manifest in the goal. When the host has no such
feature, `/do` prints the goal for you. It prevents a stop before all gates pass.

### Phase Checkpoint
<!-- context: edb861149c1f -->
A Phase Checkpoint is a condition that must be true before the next phase of a workflow starts. It
is not the end of the work, unless that phase makes the final result. It exists so that one phase
does not give an incomplete result to the next phase.

### User's Call
<!-- context: 41f3fa2ae88a -->
A User's Call is a decision where careful people with the same evidence could disagree in a way that matters to you. Confidence does not decide who has authority. The run honors Retained Decisions and applicable Delegation, then weighs relevant Taste entries. It reports material choices with their alternatives and reasons.

### Taste
<!-- context: fff430ea986a -->
A Taste entry is a personal preference that you approved, kept in a memory file of your host. It has
three parts: the preference, the reason, and when it does not apply.

A skill offers an entry when you state a preference that you want to keep. It also offers one when
you give the same correction again, or reverse one of its decisions and give a reason. It writes the
entry only when you say yes to that text. It exists so that a skill can apply your preference when
you are not present, but only a preference that you approved.

### Skill
<!-- context: f891c4003d65 -->
A skill is a set of instructions that adds a capability to an agent. The manifest-dev skills use the
same text on Claude Code, Codex, OpenCode and Pi, because each of these hosts reads skills. A skill
can start other skills.

### Agent
<!-- context: 3b0b3ea9b2ce -->
An Agent is an isolated execution context that your host gives. manifest-dev uses the word only for
this. A skill can do part of its work in a separate Agent when the host has one. The separate Agent
keeps that work apart from the main conversation.

## The investigation of a problem

### Read
<!-- context: 3c7c72e9ab33 -->
A Read is the result of a `/figure-out` session. It is a conclusion with a name, a confidence, the
evidence that it rests on, and what would change it. It exists so that you know how much to trust
the conclusion, not only what it is.

### Evidence Ledger
<!-- context: dee726286415 -->
The Evidence Ledger is the short list of claims that a Read rests on. Each claim shows its source,
and if it is a fact, an inference or a guess. Thus you can examine each claim and see which claims
the conclusion depends on.

### Fog
<!-- context: c4babc364999 -->
Fog is an area that seems important, but that nobody can state as a question yet. `/figure-out` does
not force it into a question. The area becomes clear when a parent question gets an answer, or when
new evidence arrives. A clear question that nobody can answer yet is an open thread, not Fog.

### Parent-before-child Crux Priority
<!-- context: fe9f4a15f456 -->
Parent-before-child Crux Priority is the rule that `/figure-out` obeys when it selects its next
question. It answers the highest open question first, before the details below it. An answer at the
higher level can make the details unnecessary.

## The project

### Autonomy Ladder
<!-- context: ab238c3510bd -->
The Autonomy Ladder describes ways to use manifest-dev. Each part works alone, also inside a team that does not use it.

1. Use one skill on a question or review.
2. Define and verify a finite piece of work.
3. Keep shared direction, words, decisions, and checks in Project Surfaces.
4. Track separate jobs in a Ticket Store.
5. Assign Orchestrate a queue or an outcome, within your chosen authority limits.

These are choices, not a required sequence. You retain the decisions you want to make. The workflow asks when it lacks a required decision, knowledge, or access.

### Projectless Session
<!-- context: 46edcba74847 -->
A Projectless Session is a session with no project behind its topic. Examples are a chat with no
workspace, a home or temporary folder, or a folder with one finished file. In such a session, the
skills offer and build no project surface, and they still do the full work. A project is a folder
with work that later sessions will change, also when it is new. Small work inside a project is still
project work. This exists so that the skills work without a project, and add no project files to a
folder that is not one.

### Project Context File
<!-- context: 3f1af2381d85 -->
The Project Context File is the instruction file that your host reads at the start of each session
in a project. For example, it is `CLAUDE.md` on Claude Code, and `AGENTS.md` on Codex and OpenCode.
The skills find it by detection, not by a fixed name. It connects each session to the Project
Surfaces.

### Project Surfaces
<!-- context: dd25da0ae56a -->
The Project Surfaces are the files that a project keeps for each session and each contributor. They
are its North Star, its Glossary and its Decision Records with their ADR Conventions. A project can
also select a Verification Harness. A section of the Project Context File points each session to them and records
the Surfaces Version. `/setup-project` installs them, and normal runs keep them current. They exist
so that the direction, the words and the decisions of the project live in the repository, not in the
memory of one person.

### North Star
<!-- context: dea968b8ee61 -->
The North Star says what the project is for and whom it serves. Its purpose starts with the progress those people want. It names the goal, principles, measures, bets, and open questions.

A Decision Record holds each chosen option. The North Star lists the titles of current Strategy choices, with their Signposts.

Each position has a dated state: evidence, hypothesis, ruled, or empty. It informs decisions but is not a binding work contract. An authorized ruling changes a position, and a Decision Record remembers who decided and why. Explicit Delegation can cover specified changes. Ends and bounds that the owner retains stay with the owner.

### Glossary
<!-- context: 34518718d381 -->
The Glossary is the vocabulary file of the project, `CONTEXT.md` by default. Each session reads it,
because the Project Context File loads it. It defines each term that the project agreed, so that no
session reads a term with the wrong meaning. A term goes into it when the project agrees on that
term.

### Decision Record
<!-- context: 3938795c14a0 -->
A Decision Record is one file that records a decision with a large effect on later work. It is also
called an ADR. It gives the context, the alternatives, the results, who decided, and the check that
enforces the decision. After it is published, nobody changes its decision. A newer record replaces
or amends it, and the old record says so. It exists so that a later session sees why the project
decided before it decides again.

### Signpost
<!-- context: ce77f9fca2b1 -->
A Signpost is a `Revisit when` line. It names an observable condition and where to read it. On a Decision Record, it names what would reopen the choice. On a deferred Ticket, it names what the work waits for.

A reader checks the condition at its source. A deferred Ticket becomes ready only when that condition holds. A met condition is evidence, not permission to change the choice. Reconsideration needs an Assignment and authority covering it. Otherwise, the reader brings a recommendation to the owner. An unreadable source stays visible as a missing input.

### ADR Conventions
<!-- context: 141f2d9e39ab -->
ADR Conventions is a file in the project that says which decisions get a Decision Record, and how to
write one. A reader can obey it without a tool. Where it exists, it has priority over the default
that the skills ship. Only the time when a skill offers a record stays with the skill.

### Derived Index
<!-- context: b8c119008c14 -->
A Derived Index is the list of the Decision Records, made again from the records each time that one
changes. It says nothing that the records do not say. When it is out of date, you make it again, and
no information is lost.

### Source Surface
<!-- context: fa11287d5ae5 -->
A Source Surface is a project file that people maintain and that is the authority, not an output
that a tool makes. It exists so that the skills know which file is true when a copy disagrees with
it.

### Seed
<!-- context: 60a5d84c2225 -->
A Seed is the first version of the Glossary and the Decision Records that `/setup-project` makes
from the history of a project. It is small on purpose, and it names what it could not find. It is a
start, not a full record.

### Surfaces Version
<!-- context: 6ddec267a226 -->
The Surfaces Version is a number that the Project Context File records. It shows which version of
the `/setup-project` setup the project has. When the number is older than the newest version,
`/figure-out` offers the changes since that version. It is not the version of the plugin.

## Verification

### Verification Harness
<!-- context: 2a0e6dfdb86f -->
The Verification Harness is the one command in a project that agents and people use to find if the
work still does its job. Its `--help` says all about it. It reads one Recipe for each feature,
skill, document walk or eval suite. It also reads one Recipe for the checks that run on all of the
project, such as lint, types and tests. Thus each check that the project keeps is in one place.

While you work, you can run a check command directly. The Evidence that a change works comes from
the harness. The harness writes its Evidence on your computer, in a directory that git ignores, so
the repository keeps no Evidence. To find what a change must run, it reads the change. It can also
start, observe, reset and stop what it examines.

It exists because without it each session must find again how to test the project, and a test that
nobody runs becomes stale.

A harness is optional, but we recommend it. `/setup-project` adds it unless you opt out. A project
can keep its own way to examine its work. The verification line of the Project Context File records
the choice. A harness that is already in the project counts as a choice.

When a project keeps its own way, runs use that way. When a project did not record a choice, runs
use the checks that it has, and their reports offer a harness. Runs never add a harness that the
project did not select. But runs always repair the checks that the project has, when the work
touches them. A broken test gets a repair, and so does a broken recipe.

The shape that `/setup-project` ships is a default, and you can change it to fit
your project. Each harness must give one place to learn how to examine the project. Each harness
must also give an ask-first mark that follows cost, and the Fit to Trust jobs.

### Recipe
<!-- context: c40275c62de6 -->
A Recipe is one Markdown file in the Verification Harness. It says what one part is, how a user
reaches it, the Scenarios that exercise it, and its traps. Recipes exist so that each part of the
project has one place that says how to examine it. A change then finds the recipes that it touches.

A walk recipe gives a document to a new reader, who must do a task from that document alone. An
eval recipe starts a suite of behavior tests. A suite recipe runs the checks that apply to all of
the project, such as lint and tests. Each of its Scenarios calls the command that the project
already has.

### Scenario
<!-- context: 39c884d2c5f3 -->
A Scenario is one exercise in a Recipe: an exact command and what it proves. The Verification
Harness runs it, writes its Evidence and tells you if it passed. It exists so that each claim of a
Recipe has an exact command that anyone can run again.

### Evidence
<!-- context: 85ba87b53562 -->
Evidence is what a gate result or the result of a Scenario rests on. It can be the output of a
command, the summary that a Scenario run writes on your computer, or a quoted part of a file. A pull
request shows its Evidence in its description. A summary claim is not
evidence. In a North Star, "evidence" is also a state, with the same sense: something observed, not
only said.

### Time Line
<!-- context: 789424b3ebff -->
A Time Line is the run time that a Scenario with a fixed workload must stay under. The line stops a
slow increase of test time that nobody sees.

The line is in the Recipe, for one kind of computer. A passed run sets it, with some headroom. Only
the change that changes the check moves its line. It lowers the line when it makes the check faster.
It raises the line only with a reason that it writes beside the line. A freeze that names a debt
Ticket keeps the line at its value.

A run on a different kind of computer shows its time and compares nothing. When a run crosses the
line, the harness runs the Scenario again. The crossing counts only when the second run crosses too.

### Ask-first
<!-- context: dcbbcddc356f -->
Ask-first is the mark on a Recipe whose run has a cost that a person must accept. The cost is money
or quota, load on shared systems, or effects outside the repository. Run time alone is not a cost.
By default, the harness runs such a recipe only with `--yes`, after a person runs it or agrees. This
is why `/do` can ask you before a run.

When nobody can agree, for example in an unattended run, the run leaves the recipe unrun. It names
the run that it owes in its report. The project can change this rule.

### Fit to Trust
<!-- context: 5f2494aca4e7 -->
Fit to Trust says if you can rely on a check for what a change touches. The check can be a recipe
in a harness, or a test, a script or a checklist step of the project. The jobs that the check does
decide it, not the parts that it has. The jobs are:

- A first run of one Scenario from a clean start passes, and its Evidence stays after cleanup.
- You can examine the health of the harness.
- Each run is isolated from the other runs.
- PASS means that the real path worked.
- The checks are fast enough, and none is over its Time Line without a reason.
- You can control what the change touches through the harness or the scripts of the project.
- A failure explains itself.
- The check failed when you made the thing that it checks wrong on purpose, and then you removed
  that change.

When a check that the change touches is not fit to trust, the run repairs it first.

### Lock
<!-- context: ad749d95a942 -->
A Lock is a check that a run adds after a correction, so that the same kind of mistake fails for
each later contributor. It can be a type, a lint rule, a test, or one place that all callers go
through. It has a declared scope. When it finds existing violations that the run does not fix, the
run reports them as Debt.

### Debt
<!-- context: a4cc9cb5c9ce -->
Debt is what a run found and did not fix. Examples are existing violations of a Lock, a comment
about a workaround, and a new suppression. A product regression that the harness found is also Debt.

A run names its Debt in its report, in a "Debt left" section of each pull request, and on its
Ticket. A later run that changes the same code offers to fix it. `/orchestrate` also writes the Debt of
the runs that it lands as new Tickets. Thus nobody forgets the Debt.

## Tickets

### Ticket
<!-- context: b5526f43c013 -->
A Ticket is a work item that holds one unit of work that you can schedule alone. It holds all that a
person or an agent must know to start the work, do it, and decide that it is done. That person does
not have to use manifest-dev. Tickets exist so that the next work is in a store, not in the head of
a person.

### Shaped Ticket
<!-- context: f507be3c12f2 -->
A Shaped Ticket has no open product question that changes what to build or what done means. It states its result in plain words. You may still retain acceptance of the finished artifact. Readiness to work and permission to finish are separate.

### Question Ticket
<!-- context: 9975daec2734 -->
A Question Ticket assigns an inquiry whose answer needs its own owner, priority, or closure. Its result is an answer with evidence, recorded for use or acceptance. An answer that proposes implementation does not assign that implementation.

### Assignment
<!-- context: 8d778b38c693 -->
An Assignment is the activity you or an authorized caller ask for, such as inquiry, review, or delivery. Standing permission does not start it. This keeps a discussion from becoming work nobody assigned.

### Delegation
<!-- context: 10ea7a33cb85 -->
Delegation gives authority to make specified decisions within an Assignment and its scope. A caller cannot pass on authority it lacks. Current instructions, including withdrawals, govern the work.

### Retained Decision
<!-- context: ee58a4e0ec0d -->
A Retained Decision stays with a named person or role. Dependent work waits with a recommendation, evidence, and a way to continue. Acceptance names the artifact and version. Material changes need renewed acceptance.

### Auto
<!-- context: e67cea7f8c61 -->
Auto lets unattended automation complete a Ticket and perform its required landing. Every decision needed for completion must be settled or delegated. Retained acceptance or missing access keeps the grant off.

A person grants it at Ticket-up. Orchestrate in autonomous mode can grant it to agent-written work under the same rule. The run that found the work never grants it. The grant names its giver, and a withdrawal remains effective.

Without Auto, eligible automation can prepare an answer or artifact, but a person accepts or lands it. A grant never overrides team protections or narrower instructions.

### Ticket Type
<!-- context: fc28de71e25e -->
A Ticket Type is an optional name for the main kind of a Ticket. An operator uses it to select which
Tickets automation does now. A Ticket with no type never matches a type query.

### Effort
<!-- context: 441c3358d642 -->
An Effort is a named body of work in a Ticket Store. It has one destination, one front file and its
own Tickets. A store can hold more than one Effort. It exists so that one store can hold separate
goals, and each Ticket is ranked against the goal of its own Effort.

### Ticket Store
<!-- context: 3389daf479d6 -->
A Ticket Store is where the Tickets of an Effort are: files in the repository, GitHub Issues, or
your own tracker. The project selects it one time and records it. The rules for what a Ticket holds
are the same in each store, and the store only holds the Tickets.

### Venue Reference
<!-- context: f5668a2dd019 -->
A Venue Reference tells the skills how to do each Ticket operation in one store. manifest-dev ships
one for each store that it supports. For your own tracker, a skill writes one from your description.

### Ticket-up
<!-- context: 357e871e39dc -->
Ticket-up is the one place that writes Tickets: the `/ticket-up` skill. It makes Tickets from a
finished Manifest, a direct request, an open question or a follow-up. A Manifest becomes one Shaped
Ticket by default. It becomes one Ticket for each Deliverable only when you ask for that.

### Run Ticket
<!-- context: 979a935fa02f -->
Run Ticket receives one exact Ticket and claims or recovers it. A Question Ticket goes to inquiry. Shaped work goes to delivery, using its finite Manifest where one exists. It records progress, authority, and results on the same Ticket.

A later attempt resumes those records. The run returns an answer or ready artifact, and lands only when authorized and told to. It does not choose work from the store.

### Escalation Mark
<!-- context: 47eef5f47d48 -->
An Escalation Mark is the record on a Ticket that says that a person must act. Unattended automation
does not take a Ticket with this mark. A person can still take it. When the person answers, they
remove the mark, or `/orchestrate` records the answer and removes it. When the mark goes, a claim
that automation left on the Ticket goes too.

### Orchestrate
<!-- context: bf7edea1a93b -->
Orchestrate coordinates a finite queue or an explicitly assigned outcome. It dispatches separate jobs through Run Ticket and lands eligible work one Ticket at a time. An outcome assignment can also commission inquiry and shaping, then use results to choose the next useful move.

By default it proposes a plan and waits. Autonomous mode acts within the assignment. Neither mode grants a broader assignment. An empty queue ends queue work, but does not prove an outcome was achieved.

Tickets, git, and a compact coordination record hold recovery state. The status page is a view of those records. It shows progress, evidence waits, retained decisions, and the next step. Automatic continuation needs a capability the host already offers; manifest-dev adds no scheduler.

## Pull requests

### Babysit PR
<!-- context: 8baaaa9a130b -->
Babysit PR is a workflow for the author of a pull request. It takes the pull request through CI,
review comments, its description and merge conflicts until it can merge. It never merges. It is in
the manifest-dev-tools plugin.

### Review PR
<!-- context: 6022e96df9f5 -->
Review PR is a workflow for a reviewer of a pull request. It examines the change and replies in the
review threads. It does not take the role of the author. It is in the manifest-dev-tools plugin.

### Judgment Layer
<!-- context: 534115120511 -->
The Judgment Layer is a set of questions that Review PR asks about a change. Is the change
necessary? Is the problem real? Is the size of the change correct for the problem? These questions
do not bind. They help the author decide if the change is worth its cost.

### PR Grounding
<!-- context: 5e11c71434fc -->
PR Grounding is the order of evidence that Babysit PR obeys when it decides if it must fix a blocker
on a pull request. Because of it, a new comment does not win over a stronger source only because it
is new.

### CI One-Shot
<!-- context: 67528e0927f6 -->
A CI One-Shot is a Babysit PR run with no person present. It does the steps that it can do now.
When it can only wait, it stops and reports that it waits. It exists so that CI can advance a
pull request when no person watches it.
