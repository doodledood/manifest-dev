---
name: do
description: 'Manifest executor. Reads a Manifest and pursues it with full autonomy: reach a state where every Acceptance Criterion and Global Invariant holds, deciding for itself how to get there. Use when executing a manifest, running a plan, implementing a defined task, or when the user asks to run, execute, implement, or ship a manifest-backed plan. Not when the user has only approved a plan.'
argument-hint: '<manifest-path> [--no-log]'
user-invocable: true
---

No path → halt with usage. Run only when execution was asked for: the user
invoked /do or asked to build, or a calling workflow invoked you. A user
approving a plan has not asked for it; say the Manifest is ready, give the /do
command, and stop. Otherwise read the Manifest in full, then make every Acceptance
Criterion and Global Invariant hold as written; how is yours. Those bind; Initial
Approach and Process Guidance advise. When done, report what changed, your basis
per gate, and material autonomous decisions with their rationale.

## Autonomous execution

Assume the user is AFK for the entire run. Make authorized decisions without asking questions or waiting for approval; carry this posture into every skill you invoke. A user message supplies steering, not a promise to stay for a conversation. Discover missing facts where possible, otherwise choose a defensible assumption within your authority and report material decisions and their rationale on every terminal path and in the execution log when kept.

**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list the user's calls
first, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.

**Taste on reversal.** When a steering message reverses a call the run made and states why, and the reason is a preference another user could want the opposite of — not a behavior every session owes — draft a Taste entry in three parts: the preference, naming the kind of call it covers; the rationale, built on the reason the user stated, never one you inferred; and when it should yield. Carry it verbatim in the terminal report, with the memory file it would go in and the question whether it is standing or for this case only; "this case only" is a no. Write nothing: only the user's explicit yes to that text writes it, inside that file's `## Taste` section. When an existing entry decided the reversed call, report the clash instead, with any proposed revision or removal shown verbatim for the user's yes. Make no other offer.

Choose solutions that make the requested outcome durable and subsequent work easier to do correctly. Address recurring friction and opportunities for error at their source when the benefit justifies the added complexity. The initial plan is yours to change. Appetite — the size of change the problem is worth — may be revised through the authoring skill before broader work starts when the benefit to this outcome justifies the added complexity and maintenance. Explicit Out of bounds exclusions, binding requirements, and permissions remain fixed unless the user changes them; absence from an exclusion list does not authorize unrelated improvements. Never revise Appetite to excuse excess already produced or use it to lower a gate's bar.

A blocked obligation has no viable authorized path after investigating credible alternatives: proceeding requires unavailable knowledge or access, new authority, or a change to a binding requirement. A failed approach or difficult decision calls for investigation and redesign, not automatically for escalation. Stop repeating attempts that yield no new evidence or progress; identify the missing intervention when viable recovery paths are exhausted.

Surface an established blocker promptly with its evidence and the intervention needed, then continue useful independent work that does not depend on guessing the blocked decision. A blocker notice is not a terminal escalation. Every route to `/escalate` in this skill applies only when no useful independent work remains; invoke it then with the unresolved blockers. An external process still progressing is a wait, governed by the run's waiting policy, never successful completion.

## Amendments

Invoke `define` with the Manifest path and the decision to amend the plan,
settled assumptions, or Appetite within your delegated authority, or to encode
user steering. Pass the rationale and keep the amendment unattended. An Appetite
revision names the benefit to the requested outcome and the added complexity and
maintenance; apply it before broader work starts. Never amend directly or rewrite
a binding requirement on your own judgment. A false binding premise is a blocker;
a failed approach is yours to replace.

Wait for active gate evaluations to finish before amending. If an amendment races
an evaluation, discard that evaluation's verdicts and evaluate the amended file.
Re-read the amended Manifest. Re-verify every gate whose text, subject, or
interpretation changed, including the ceiling when Appetite changes; keep other
evidence only while it remains valid. Report material amendments on every terminal
path and record them in the execution log when kept.

## Continuation

Before implementation, including when called by /auto, resolve the absolute Manifest path
and arm the completion backstop: continue under an active goal identifying this same file,
or emit the blocks below verbatim, substituting `<manifest-path>` with the absolute Manifest path.
Where a broader parent workflow backstop is already visible and already requires evidence for every
gate — a PR-tend contract, say — operate under it: do not set or print a second narrower goal.
Do not summarize, shorten, reword, or re-punctuate them. Set them through the harness's
goal-setting, continuation, or durable-completion-condition capability, else print them
copy-pasteable. Emit the goal block, as one completion contract:
one unlabeled block introduced by a sentence of your own, since the fences and their
labels are this file's markers rather than part of what you emit.

```goal-block
Work under the Manifest at <manifest-path> until every Acceptance Criterion and Global Invariant in it holds, each with evidence from the artifacts that gate names, and completion has been reported. Read this file before resuming execution.

The Manifest is the contract, not the run's to rewrite: it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified.

Record compact checkpoint notes as work proceeds: what changed, what was verified, what remains, blockers.

Assume the user is AFK; make authorized decisions without asking questions. Surface blockers promptly and continue useful independent work. Stop after reporting completion, a blocker requiring a person when no useful independent work remains, or an external wait that this run's no-wait policy makes terminal. Continue while authorized, actionable work remains.
```

## Corrections, debt and the verification surface

When the run repairs a finding or receives a correction, and before it reports, load
`references/HARVEST.md`: a correction becomes a lock where a check can hold it, and the debt the
run leaves goes into its report and into every pull request it opens or updates. When the
Manifest gates a verification-surface entry, or the work needs a surface the project lacks or
touches a path the surface has no entry for, load `references/VERIFICATION.md`.

## What holds for every gate

A gate declares `judgment` or `deterministic`; an undeclared kind is invalid, never
inferred. Read a gate from the Manifest by ID, never from a copy. For repository
work, compare against the repository's actual remote-tracking default branch,
unless the gate names another subject. Include relevant staged, unstaged, and
untracked work when the artifact being judged includes local changes. A judgment gate reads the full change once, then only
prior findings' repairs and the delta; a deterministic gate re-runs in full. A finding
below a gate's bar is recorded — in the execution log when kept — and left
unrepaired, because every repair is a new delta that each judgment gate re-reads. A
pre-existing issue the run meets on its own, rather than one a gate reported, is fixed when
it is related to the current change and otherwise recorded the same way; `/done` and `/escalate` surface both for the user to
decide. A bar never moves down on
the executor's judgment, and a summary claim is not evidence: obtain the missing
evidence, or report a blocker while continuing useful independent work.

## The execution log

Unless `--no-log`, keep an append-only log at `~/.manifest-dev/logs/do-<name>-<hash>.md`,
where `<name>` is the Manifest's filename without extension and `<hash>` the first eight
hex characters of SHA-256 over its absolute path. Fixing the scheme is what reopens the
same Manifest's log on every launch and keeps two manifests sharing a basename in
different directories apart. Read it before resuming and append as you go: it is where
the goal block's checkpoint notes land. `references/LOG.md` holds the entry shape
and append discipline — not its path rule.
