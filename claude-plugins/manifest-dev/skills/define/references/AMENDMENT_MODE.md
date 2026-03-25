# Amendment Mode

Loaded when `--amend <manifest-path>` is present. /define modifies an existing manifest instead of building from scratch.

## Core Behavior

Read the manifest at the given path. Existing decisions (ACs, INVs, PGs, Approach, Trade-offs) are preserved unless directly contradicted by the change request. Make targeted changes — only items affected by the amendment are updated. Add new items, modify contradicted items, or remove items that no longer apply.

## What Triggers Amendment

The conversation context contains the reason — a user's message, a PR review comment, or an explicit change request. Read this context and determine what to change.

## Interview Style

When `--interview` is explicitly provided, use it. Otherwise, inherit the interview style from the manifest's metadata (if recorded) or default to `thorough`. The amendment interview is scoped to the change — not a full re-interview of the entire manifest.

## Two Contexts

### 1. Standalone

User calls `/define --amend <manifest>` directly. Full interactive mode:
- Interview the user about the change
- Run verification loop per mode
- Present summary for approval
- Same as normal /define but starting from existing manifest

### 2. From /do (Autonomous Fast Path)

After Self-Amendment escalation from /do. Detectable from conversation context — /do just called /escalate Self-Amendment. In this context:
- Inherit `--interview` style from manifest metadata
- Make targeted changes based on the escalation context (what the user/reviewer said, which items are affected)
- Skip the verification loop (no manifest-verifier invocation)
- Skip summary-for-approval (auto-approve)
- Write updated manifest in-place (same path)
- Log the amendment in the manifest's `## Amendments` section
- Return manifest path immediately so /do can resume

## What to Preserve

Intent, Approach architecture (unless contradicted), existing ACs/INVs that aren't affected, Process Guidance, Known Assumptions. Execution order may need updating if new deliverables are added.

## What to Change

Add/modify/remove ACs, add new deliverables, update INVs, adjust trade-offs. Use amendment IDs per the manifest's Amendment Protocol (e.g., `INV-G1.1 amends INV-G1`). Always log changes in `## Amendments` with what changed and why.
