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
4. **Called by /verify only, after a full-suite green pass** - /done is the final step after /verify confirms a **full pass** is green — every AC across every deliverable plus every Global Invariant. Selective-mode green alone is not sufficient (per /verify's hard final gate); /verify auto-triggers a full pass after selective green and only then calls /done.

## Post-Completion Feedback

After /done has been called, the manifest is still the canonical source of truth for the PR/branch — the work isn't necessarily merged, and feedback can still arrive (user comments, PR reviews, second thoughts). The default reflex for any feedback that changes scope or contradicts something settled is the same as during /do (per `do/SKILL.md` Mid-Execution Amendment): **default to amend.**

**Re-entry flow:** when feedback is determined to be amendment-worthy (not a pure question), invoke `/define --amend <manifest-path>` with the feedback as input, then `/do <manifest-path> <log-path> --scope <new-or-affected-deliverables>` to implement the change. /do's selective-mode + mandatory full final gate apply to the re-entry pass — /done won't be reachable again until the full suite is green on the amended manifest.

**Pure questions** about the work that just completed are answered inline — same carve-out as in /do.

**Manifest-in-scope detection** is judgment-based with no session boundary (per `define/SKILL.md` Session-Default Amendment): the manifest most recently associated with the work in this context is the candidate for amendment, regardless of when /done was called or whether the session was compacted in between. When ambiguous, ask the user once.

**No-manifest case:** if /do somehow completed without a manifest in scope (rare — typically /do follows /define), there's nothing to amend; post-completion feedback falls back to inline handling. Fail-open by design.

## Medium Routing

When medium is non-local, /done output goes through the calling context (/verify → /do). No special routing needed — just produce the summary as normal.
