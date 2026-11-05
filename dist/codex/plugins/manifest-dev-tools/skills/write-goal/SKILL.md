---
name: write-goal
description: 'Write one standalone goal defining what done means, in at most 4,000 characters, from a Manifest, a figure-out read, a Ticket, a handoff, a plain request or several of them. Use when the user wants to turn this work into a goal, or paste it into a goal field with no file reference behind it.'
argument-hint: '<Manifest, figure-out read, Ticket, handoff or request: a path or inline text>'
user-invocable: true
---

Turn the supplied sources into one standalone goal of at most 4,000 characters. The goal replaces them: the agent that works from it has none of the sources and none of this conversation, so an obligation the goal drops is gone and a requirement it invents becomes binding.

**Sources.** A Manifest — the specification of what to deliver, what counts as done, and the constraints that hold throughout; a figure-out read — a named conclusion with its evidence and what would overturn it, in the conversation or in its log file; a Ticket; a handoff; a plain request; or several of them together. Use the sources identified in the request or conversation; ask which one if the target is missing or ambiguous. Read all of them and the references needed to understand their intent and requirements. Apply explicit user amendments, distinguishing settled decisions from suggestions still under discussion.

What each source owes:
- **A Manifest:** its Outcome and every current Acceptance Criterion and Global Invariant,
  preserving each claim's authority. A hard claim is a deliberately stated user requirement
  or applicable project, safety or permission obligation; it changes only with its source's
  authorization. A working claim is an agent's operational interpretation, revisable on evidence
  while preserving the Outcome and hard requirements. Carry that freedom as well as the current
  target. Evidence methods remain working unless the hard claim explicitly requires them.
  Rationale, Process Guidance and the Initial Approach add no requirements. Overall plan approval
  does not turn working choices into hard claims. Missing authority is a source gap, not a license
  to reclassify an older contract.
- **A read:** its conclusion, intended result, settled requirements and proposed assessment,
  preserving which are hard and which are working. Distinguish an excluded investigation branch
  from an authorized exclusion of later work; carry only the latter as a delivery limit.
  Evidence, rival explanations, overturn conditions and unaccepted offers are grounds, not requirements.
- **Any other source:** its settled decisions. Suggestions still under discussion owe nothing.

**Test for gaps before listing.** The sources must settle four things:
1. The finished outcome.
2. A done check that a reader of the goal alone could settle as done or not done.
3. The limits: scope and exclusions.
4. Where the work stops. A source settles this when its done check is the end, or when it names the stop. It is still a gap when the work would reach an act that cannot be undone or needs someone's approval — merging, deploying, sending, spending — and the source does not say whether to take it: a source that ends at a pull request without saying whether to merge it leaves the stop open.

Fill each gap or contradiction that would materially change the goal before drafting; never fill one by invention. A gap that is one clear question, ask the user directly: one ask at a time, each settled by one short answer, and only about the open items above. A gap that needs investigation, or that cannot yet be put as one clear question, invoke the figure-out skill on: give it the open items above as its assignment — settle these for a goal and return the read — and add the read it returns to the sources, then test again. Where the figure-out skill is not available, say so and ask the gap as a question, or stop without a goal.

**List what the goal owes before drafting.** Write down every obligation the sources owe, as above, and every scope limit, exclusion, stopping limit and approval boundary they state. Drop what a user amendment removed. Requirements that share one check may become one only while each of their conditions survives. When the list cannot fit in 4,000 characters without dropping or weakening an item, ask the user which to cut before drafting.

**Draft from the list.** Open with the finished outcome, then preserve each item's force in plain
language: what must hold, what may be revised on evidence, and what only advises. Use no IDs,
workflow jargon, source pointer or step dependent on the source workflow. Keep the purpose and
rationale that guide interpretation, boundary-defining examples, and qualified assumptions.
Completion requires the intended result and current checks on observed evidence; passing a proxy
alone is insufficient. Material working revisions are explained and affected evidence refreshed.
Concrete commands, skills and artifact names may define success when the source requires them.
Leave execution strategy to the agent. Add no metric, budget, report format, review step or policy
the sources did not specify, and omit policy the known destination already supplies. Count the
goal programmatically, spaces and punctuation included, and revise to at most 4,000 characters;
the ceiling is not a target.

**Have it read cold.** Give one fresh context the goal alone, with this file's path as the standard a goal is held to — it reviews, drafting nothing — and ask what the goal would have it build, what limits it sets, and how it would decide it is done. Then give it the sources as text — a Manifest's file, a read's text and its log path, and for a source that lives only in the conversation the user's settling messages quoted — with the user's amendments and your list, and ask it to work out from the sources what the goal owes, treating your list as a claim to check and the sources as the reference rather than the subject of review. Ask it to report each obligation dropped or weakened, each requirement the sources do not state, each working choice made fixed, each hard claim made revisable, each piece of advice — a method, plan or suggestion the sources do not bind — stated as a requirement, any removed or superseded scope the goal revives, any reference to a source or its IDs, each condition a reader of the goal alone could not settle as done or not done where the sources settle it, and, for each check the sources name, a plausible wrong result the goal would let pass that the check itself would catch. Where no Manifest is among the sources, nobody has yet reviewed the goal as a contract, so also ask it for conditions that cannot all hold together within the stated scope, and for holes: a requirement the goal states that no check in it settles, so work missing it passes every check, or a check that already passes on the current state while the outcome is missing. A requirement a reader can settle directly, by running a command the goal names and reading its output, is settled. Settle every finding in one pass: fix it, or reject it with its reason, then count the goal again. A finding the sources cannot settle is a gap: fill it as above, never by invention. A fix that would take the goal past 4,000 characters is a cut for the user: ask which item to shorten or drop. No second review follows. Where no isolated context is available, run the same two readings yourself, goal first.

Return the goal as one paragraph inside a single plain-text code fence. Below the fence, add one short note only when a finding was rejected, naming it and why, or the review was self-graded; otherwise return the fence alone. This invocation drafts text only: it does not edit a source, set a running goal or begin the work it describes.
