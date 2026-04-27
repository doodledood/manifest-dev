---
name: done
description: 'Completion marker for the /do workflow. Outputs hierarchical execution summary showing Global Invariants respected and all Deliverables completed. Called by /verify after all criteria pass, not directly.'
user-invocable: false
---

# /done - Completion Marker

## Goal

Output a completion summary showing what was accomplished, organized by the Manifest hierarchy.

## Input

`$ARGUMENTS` = completion context (optional)

## What to Do

Read the execution log and manifest. Output a summary that shows:

1. **Intent** - What was the goal
2. **Global Invariants** - All respected
3. **Deliverables** - Each with its ACs, all passing
4. **Key changes** - Files modified, commits made
5. **Tradeoffs applied** - How preferences were used

When the manifest declares `Repos:` (multi-repo), `/done` still fires **once per manifest** — not once per repo. /verify's "every AC across every deliverable" rule is preserved unchanged; for multi-repo, that means every AC in every repo's deliverables must pass before `/done` is called. This is achievable because `/verify` injects the cross-repo path prefix (`Available repos: ...`) on every pass when `Repos:` is declared, so verifiers can reach all repos during normal flow.

The multi-repo summary additionally lists which **repos' deliverables were verified in this run** — providing a clear inventory of what landed across the changeset.

**`/done` is gated on no deferred-auto criteria pending.** When the manifest contains `method: deferred-auto` criteria that have not yet been verified green via `/verify --deferred`, `/verify` does NOT call `/done` — it routes to `/escalate` with type "Deferred-Auto Pending" instead, telling the user to run `/verify --deferred` when prerequisites are in place. Only after deferred-auto criteria pass via `--deferred` does a subsequent normal `/verify` pass reach `/done`. See `define/references/MULTI_REPO.md` §e/§g and `verify/SKILL.md` "Deferred-Pending Escalation".

Single-repo manifests (no `Repos:` field) get the standard summary unchanged — no repo list, no deferred-auto note. The deferred-auto-pending escalation rule applies regardless of multi-repo (any manifest with deferred-auto criteria, single- or multi-repo, gates /done the same way).

## Output Format

```markdown
## Execution Complete

All global invariants pass. All acceptance criteria verified.

### Intent
**Goal:** [from manifest]

### Global Invariants
| ID | Description | Status |
|----|-------------|--------|
| INV-G1 | ... | PASS |

### Deliverables

#### Deliverable 1: [Name]
| ID | Description | Status |
|----|-------------|--------|
| AC-1.1 | ... | PASS |

**Key Changes:**
- [file] - [what changed]

---

### Tradeoffs Applied
| Decision | Preference | Outcome |
|----------|------------|---------|

### Files Modified
| File | Changes |
|------|---------|

---
Manifest execution verified complete.

*Post-completion feedback defaults to amending this manifest. Send a message describing the change; pure questions are answered inline.*
```

The trailing italic line is **mandatory** in /done's output — it surfaces the post-completion default-to-amend rule into the parent transcript so the model has a recent reminder when feedback arrives after /done.

## Principles

1. **Mirror manifest structure** - Hierarchy should match: Intent → Global Invariants → Deliverables
2. **Show evidence** - Link changes to deliverables, describe behavioral changes (not just file lists)
3. **Adapt detail to complexity** - Simple task = condensed output. Complex task = full hierarchy.
4. **Called by /verify only, after a full-suite green pass** - /done is the final step after /verify confirms a **full pass** is green — every AC across every deliverable plus every Global Invariant — **AND no `deferred-auto` criteria are pending** (when pending deferred-auto criteria exist, /verify routes to /escalate "Deferred-Auto Pending" instead of calling /done; see narrative above and `verify/SKILL.md` Deferred-Pending Escalation). Selective-mode green alone is not sufficient (per /verify's hard final gate); /verify auto-triggers a full pass after selective green and only then calls /done.

## Post-Completion Feedback

After /done has been called, the manifest is still the canonical source of truth for the PR/branch — or the **PR set / branch set** in the multi-repo case — because the work isn't necessarily merged, and feedback can still arrive (user comments, PR reviews, second thoughts). The default reflex for any feedback that changes scope or contradicts something settled is the same as during /do (per `do/SKILL.md` Mid-Execution Amendment): **default to amend.**

**Re-entry flow.** When feedback is amendment-worthy (not a pure question), perform both of the following steps in order:

1. **Amend the manifest.** Invoke the `manifest-dev:define` skill with: `<feedback> --amend <manifest-path>`. The amendment runs in the manifest's recorded `Interview:` style — autonomous manifests amend without questions, thorough manifests probe per `thorough.md`, minimal manifests do light probing. (See `define/references/AMENDMENT_MODE.md` for the full inheritance rule.) Wait for /define to return; note the manifest path.

2. **Re-execute.** Invoke the `manifest-dev:do` skill with: `<manifest-path> <log-path> --scope <new-or-affected-deliverables>`. `<log-path>` is the existing execution log /do wrote during the original run (available from the conversation context — /do logged its creation at the start of execution); pass it so /do appends rather than starting fresh, per `do/SKILL.md`'s "iteration on previous work" contract. Infer `--scope` from the amendment log entries — the deliverables newly added or modified by step 1. When the amendment touches a Global Invariant or the scope is genuinely unclear, omit `--scope` so /do runs full. /do's mandatory full final gate (per `verify/SKILL.md` "Hard final gate") runs unconditionally before /done becomes reachable, so a too-narrow scope still cannot land a regression — /verify auto-triggers a full pass after selective green.

**Both steps are mandatory.** Stopping after step 1 leaves the manifest amended but unimplemented and unverified — the same failure mode as silent scope drift, just shifted: the manifest now claims scope that no code satisfies. The amendment loop guard from `do/SKILL.md` Mid-Execution Amendment (R-7 — consecutive Self-Amendments without external user/PR input escalate as Proposed Amendment for human decision) applies to this re-entry path too; runaway oscillation is bounded.

**Routing feedback to amend vs. inline.** Pure questions about the work that just completed are answered inline — same carve-out as in /do.
- *Inline (answer in the current turn):* "What does AC-1.1 require?" / "Why did you choose approach A?" / "Where's the execution log?"
- *Amend (run the two-step chain above):* "Also handle X." / "Change Y to Z." / "That's wrong, it should be …" / "Add a check for …"
- *When ambiguous, amend.* Silent scope drift is the worse failure.

**Manifest-in-scope detection** is judgment-based with no session boundary (per `define/SKILL.md` Session-Default Amendment): the manifest most recently associated with the work in this context is the candidate for amendment, regardless of when /done was called or whether the session was compacted in between. When ambiguous, ask the user once.

**No-manifest case:** if /do somehow completed without a manifest in scope (rare — typically /do follows /define), there's nothing to amend; post-completion feedback falls back to inline handling. Fail-open by design.

## Medium Routing

When medium is non-local, /done output goes through the calling context (/verify → /do). No special routing needed — just produce the summary as normal.
