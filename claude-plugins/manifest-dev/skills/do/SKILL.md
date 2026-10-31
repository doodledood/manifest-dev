---
name: do
description: 'Manifest executor. Reads a Manifest and pursues it with full autonomy: reach a state where every Acceptance Criterion and Global Invariant holds, deciding for itself how to get there. Use when executing a manifest, running a plan, implementing a defined task, or when the user asks to run, execute, implement, or ship a manifest-backed plan. Not when the user has only approved a plan.'
argument-hint: '<manifest-path> [--no-log]'
user-invocable: true
---

Read `../ticket-up/references/AUTHORITY.md` before acting. Keep this assignment, its applicable
authority and retained decisions in every skill handoff; an isolated caller must receive them
explicitly, with the useful intent and evidence.

No path → halt with usage. Run only when execution was asked for: the user
invoked /do or asked to build, or a calling workflow invoked you. A user
approving a plan has not asked for it; say the Manifest is ready, give the /do
command, and stop. Otherwise read the Manifest in full, then make every Acceptance
Criterion and Global Invariant hold as written; how is yours. Those bind; Initial
Approach and Process Guidance advise. When done, report what changed and your basis
per gate.

## Autonomous execution

Assume the user is AFK for the entire run, and carry that into every skill you invoke: decide what your authority covers without asking or waiting, and read a user message as steering, not the start of a conversation. Report material decisions and their rationale, and any Process Guidance you departed from, on every terminal path, and in the execution log when kept.

**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, first honor any explicit retained decision or applicable delegation; then check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list first each decision record the run
reopened, with the reason set aside and what reversing would cost, then the
user's calls, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.

**Taste on reversal.** When a steering message reverses a call the run made and states why, and the reason is a preference another user could want the opposite of — not a behavior every session owes — draft a Taste entry in three parts: the preference, naming the kind of call it covers; the rationale, built on the reason the user stated, never one you inferred; and when it should yield. Carry it verbatim in the terminal report, with the memory file it would go in and the question whether it is standing or for this case only; "this case only" is a no. Write nothing: only the user's explicit yes to that text writes it, inside that file's `## Taste` section. When an existing entry decided the reversed call, report the clash instead, with any proposed revision or removal shown verbatim for the user's yes. Make no other offer. A reaction to a disposable draft drafts an entry only as `references/HARVEST.md` → *A reaction to a draft* says.

Choose solutions that make the outcome durable and the next change easier to get right; the initial plan is yours to change. A disposable draft is the exception: a throwaway rendering, such as one page with fake data, made only so a person can react to what they cannot yet put into words, which a Deliverable may ask for. Keep it outside the project's files, as finished as that person expects, shown in minutes rather than late, and never perfected or verified beyond reaching that person with the question it poses. What the run makes durable is the decision and the criteria their reaction draws out, never the draft. Appetite — the size of change the problem is worth — may be revised by amendment (*Amendments*), never to excuse excess already produced or to lower a gate's bar. Out of bounds exclusions, binding requirements and permissions stay fixed unless the user changes them, and absence from an exclusion list authorizes nothing unrelated.

An obligation is blocked only when no authorized path remains after trying credible alternatives: it needs knowledge, access or authority the run lacks, or a change to a binding requirement. A failed approach is yours to redesign rather than repeat; when two repairs that rest on one premise have both failed a gate, test that premise before a third repair. Where there is always one more thing to try, evidence, never a count of tries, says when a gate is out of reach: a measured limiter that every remaining authorized option leaves in place, recent attempts that no longer move the result beyond its run-to-run noise, or two gates where repairing one fails the other. The burden of proof is the run's: the limiter measured rather than guessed, the attempts distinct approaches aimed at it rather than variations of one idea, and every authorized option that could move it tried; until then the gate is not out of reach, and the work goes on. Any of these, so earned, makes it blocked as needing a change to a binding requirement; its blocker names the best result reached, the limiter, the attempts made and the requirement change that would unblock it, and the bar stays as written. Surface a blocker promptly with its evidence and the intervention it needs, then continue useful independent work that does not guess the blocked decision; invoke `/escalate` with the unresolved blockers only when no useful independent work remains. An external process still running is a wait, never completion.

## Amendments

Invoke `define` with the Manifest path and the decision to amend the plan,
settled assumptions, or Appetite within your delegated authority, or to encode
user steering. Pass the rationale and keep the amendment unattended. Revise
Appetite only when the benefit to the requested outcome justifies the added
complexity and maintenance; the revision names both and applies before broader
work starts. Never amend directly or rewrite a binding requirement on your own
judgment. A false binding premise is a blocker.

Wait for active gate evaluations to finish before amending. If an amendment races
an evaluation, discard that evaluation's verdicts and evaluate the amended file.
Re-read the amended Manifest. Re-verify every gate whose text, subject, or
interpretation changed, including the ceiling when Appetite changes; keep other
evidence only while it remains valid. Report material amendments on every terminal
path and record them in the execution log when kept.

## Continuation

Before implementation, including when called by /auto, resolve the absolute Manifest path
and arm the completion backstop: continue under an active goal identifying this same file,
or emit the goal block below verbatim, substituting `<manifest-path>` with the absolute
Manifest path. Do not summarize, shorten, reword, or re-punctuate it. Set it through the
harness's goal-setting, continuation, or durable-completion-condition capability, else print it
copy-pasteable. Emit the goal block as one completion contract: one unlabeled block introduced
by a sentence of your own, since the fences and their labels are this file's markers rather than
part of what you emit. Where a broader parent workflow backstop is already visible
and already requires evidence for every gate — a PR-tend contract, say — operate under it:
do not set or print a second narrower goal.

```goal-block
Work under the Manifest at <manifest-path> until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported. Read this file before resuming execution.

The Manifest is the contract, not the run's to rewrite: it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Assume the user is AFK; make authorized decisions without asking questions. Surface blockers promptly and continue useful independent work. Stop after reporting completion, a blocker requiring a person when no useful independent work remains, or an external wait that this run's no-wait policy makes terminal. Continue while authorized, actionable work remains.
```

## Corrections, debt and the verification harness

Load `references/HARVEST.md` before the run reports, and earlier as soon as it repairs a finding,
fixes a defect, receives a correction or a reaction to a disposable draft, or touches a comment that explains a workaround or claims a
constraint: a correction becomes a lock where a check can hold it, a reaction to a draft steers its direction and locks only what reaches past it, such a comment becomes a refactor flag or
an encoding offer, and the debt the run leaves goes into its report and into every pull request it opens or updates. When the
Manifest gates a verification recipe, or the project keeps a verification harness — named in the
project-surfaces section of the context file, or on disk with no verification bullet there, which
counts as chosen — and the work needs a part it lacks or touches a path no recipe covers, load
`references/VERIFICATION.md`. Wherever a harness is on disk with no bullet, the report suggests recording it.
The harness is the project's choice: where that section names the project's own way of verifying,
verify through the means it names, and recommend no harness. Where the section records no choice and
no harness is on disk, verify through what the project keeps, and recommend a harness in the report.
Either way add any check the change needs in the project's own form and build no harness. In every project, harness or
not, repair a check the change touches that is broken or not fit to trust in its own form, or
report it as debt. A harness belongs to a project:
a repository or working folder
holding, or about to hold, work later sessions will change — a new one the user is starting
counts — which this work concerns. A chat with no workspace, a home or scratch folder, a folder
holding one finished artifact, or a question that does not concern the folder the session runs in
is none. With none, the Manifest's gates are the whole
verification: build no harness and add no project surface. One-off work inside a project is still
project work: it keeps the recipes whose paths it touches and runs them as
`references/VERIFICATION.md` says.

## What holds for every gate

How you verify is yours; these conventions are not. Understand each gate before making the
choices it constrains, including the applicable standards it delegates to a skill or reference.
Use those standards during construction and evaluation, with their thresholds, exceptions, and
trade-offs. This requires neither a preliminary review nor a fixed evaluation order.

A gate declares `judgment` or `deterministic`; an undeclared kind is invalid, never inferred.
Read a gate from the Manifest by ID, never from a copy. Keep track of the criteria and subject
each piece of evidence assessed. Changes to either, or new external evidence, invalidate the
affected evidence; retain what still applies. The subject includes relevant local work and
external state, not just a commit identifier.

A judgment gate reads the full change once, then checks outstanding findings and failures
introduced or exposed by the changes since that evaluation; a deterministic gate re-runs in full.
Give an invoked evaluator that reporting scope, the assessed state, prior findings, verified
repairs, and the intervening changes. Recover missing context rather than silently requesting
another full look. Contextual reading may be wide; touching an old line alone does not make an
old issue new. A fresh standalone review keeps the scope its caller requested. A finding below
a gate's bar, and a pre-existing issue unrelated to the change, is recorded rather than
repaired, since every repair is a delta each judgment gate re-reads; `/done` and `/escalate`
surface them for the user. A bar never moves down on the executor's judgment, and a summary
claim is not evidence.

When external review feedback arrives, directly or through `check-pr`, load
`references/EXTERNAL_REVIEW.md` before acting on it.

## The execution log

Unless `--no-log`, keep an append-only log at `~/.manifest-dev/logs/do-<name>-<hash>.md`,
where `<name>` is the Manifest's filename without extension and `<hash>` the first eight
hex characters of SHA-256 over its absolute path, so every launch on this Manifest reopens
the same log. Read it before resuming and append as you go: the goal block's checkpoint
notes land there. `references/LOG.md` holds what a resumed run needs from it.
