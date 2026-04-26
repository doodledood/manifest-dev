# Amendment Mode

/define modifies an existing manifest instead of building from scratch.

## Cumulative Manifest Rule

**The manifest is the canonical source of truth for the PR/branch lifetime — not for a single task.** After every amendment, the manifest must describe the FULL PR state: intent, every deliverable, every Global Invariant, every Process Guidance entry, every Known Assumption. The latest increment is layered onto the prior content, never substituted for it.

**No silent drops.** When applying an amendment, prior content is preserved by default. Removal is explicit — if a change supersedes an existing AC/INV/PG, the supersession is logged in the `## Amendments` section with rationale. The amendment receiver is responsible for reading the full prior manifest and confirming nothing valuable was lost.

A manifest at any point in time should be readable as "everything currently in scope for this PR/branch," not "the most recent change request." This is what makes the manifest a useful artifact for PR descriptions, reviews, and future amendments.

## Core Behavior

Read the manifest at the given path. Existing decisions (ACs, INVs, PGs, Approach, Trade-offs) are preserved unless directly contradicted by the change request. Make targeted changes — only items affected by the amendment are updated. Add new items, modify contradicted items, or remove items that no longer apply (with explicit log entry per the Cumulative Manifest Rule above).

**Coverage goals apply scoped to the change** — not the full manifest. Existing manifest content satisfies goals for unchanged areas.

## What Triggers Amendment

The conversation context contains the reason — a user's message, a PR review comment, or an explicit change request. Read this context and determine what to change.

## Interview Style

When `--interview` is explicitly provided, use it. Otherwise, inherit the interview style from the manifest's metadata (if recorded) or default to `thorough`. The amendment interview is scoped to the change — not a full re-interview of the entire manifest.

## Three Contexts

### 1. Standalone

User calls `/define --amend <manifest>` directly. Full interactive mode:
- Interview the user about the change
- Run verification loop per mode
- Present summary for approval
- Same as normal /define but starting from existing manifest

### 2. From /do (Autonomous Fast Path)

Triggered by `--from-do` flag (e.g., `/define --amend <manifest> --from-do`). This flag is set by /do after Self-Amendment escalation — it signals deterministically that this is an autonomous amendment, not an interactive session.

In /do context, amendment is autonomous and fast — no user approval gates (verification loop, summary approval). Make targeted changes based on the escalation context. Write updated manifest in-place so /do can resume immediately. Log the amendment in the manifest's `## Amendments` section.

### 3. Session-Default

Triggered implicitly by `/define`'s in-session detection of a prior related manifest (no explicit `--amend` flag). See SKILL.md's `## Session-Default Amendment` section for the detection and relatedness rules. Once the agent decides to amend, behavior **follows the Standalone path** — interview scoped to the change (per the active interview mode), verification loop, summary for approval. The interview mode (`thorough` / `minimal` / `autonomous`) is **not** overridden by the trigger context — `/auto` invocations still run autonomously, just amending the prior manifest instead of starting fresh. The user is told upfront via an announcement and can verbally redirect to a fresh manifest if the relatedness call was wrong.

## What to Preserve

Intent, Approach architecture (unless contradicted), existing ACs/INVs that aren't affected, Process Guidance, Known Assumptions. Execution order may need updating if new deliverables are added.

## What to Change

Add/modify/remove ACs, add new deliverables, update INVs, adjust trade-offs. Use amendment IDs per the manifest's Amendment Protocol (e.g., `INV-G1.1 amends INV-G1`). Always log changes in `## Amendments` with what changed and why.
