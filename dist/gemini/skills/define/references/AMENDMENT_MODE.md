# Amendment Mode

/define modifies an existing manifest instead of building from scratch.

## Cumulative Manifest Rule

**The manifest is the canonical source of truth for the PR/branch lifetime — or, in multi-repo cases, the entire PR set / branch set lifetime — not for a single task.** After every amendment, the manifest must describe the FULL state of every PR it covers: intent, every deliverable (across every repo when multi-repo), every Global Invariant, every Process Guidance entry, every Known Assumption. The latest increment is layered onto the prior content, never substituted for it.

**No silent drops.** When applying an amendment, prior content is preserved by default. Removal is explicit — if a change supersedes an existing AC/INV/PG, the supersession is logged in the `## Amendments` section with rationale. The amendment receiver is responsible for reading the full prior manifest and confirming nothing valuable was lost.

A manifest at any point in time should be readable as "everything currently in scope for this PR/branch (or PR set)," not "the most recent change request." This is what makes the manifest a useful working artifact for the agent and the user across the PR lifecycle.

**Multi-repo specifics** — see `MULTI_REPO.md` §f for the shared-manifest amendment convention.

**Deferred-auto re-verification after amendment** — when an amendment substantively changes a `method: deferred-auto` criterion's verify block (`prompt:`, `command:`, etc.), prior `/verify --deferred` coverage is conceptually invalidated for that criterion. Normal `/verify` always re-runs in-scope criteria so amendments are picked up automatically; deferred-auto bypasses the pass and relies on prior coverage. The user is responsible for re-running `/verify --deferred` for the amended criterion before the gate clears. (Consistent with the user-as-coordinator stance — there is no automatic invalidation mechanism.)

## Core Behavior

Read the manifest at the given path. Existing decisions (ACs, INVs, PGs, Approach, Trade-offs) are preserved unless directly contradicted by the change request. Make targeted changes — only items affected by the amendment are updated. Add new items, modify contradicted items, or remove items that no longer apply (with explicit log entry per the Cumulative Manifest Rule above).

**Coverage goals apply scoped to the change** — not the full manifest. Existing manifest content satisfies goals for unchanged areas.

## What Triggers Amendment

The conversation context contains the reason — a user's message, a PR review comment, or an explicit change request. Read this context and determine what to change.

## Session-Default Detection

`/define` invokes this detection from its Pre-flight when the transcript or conversation references a prior manifest (skipped when `--amend <path>` is explicit, or when the input plainly references a `/tmp/manifest-*.md` path — those signals always win, the named manifest is source of truth, and the agent confirms approach with the user only if its relationship to the new task is unclear).

Detection signals (most-recent / most-specific wins):

1. **In-session completion line** — `Manifest complete: /tmp/manifest-{timestamp}.md` from a prior /define's Complete output appearing earlier in the transcript. Most recent in transcript order wins.
2. **Conversation reference** — a `/tmp/manifest-*.md` path mentioned in the conversation.

When ambiguous (transcript references unrelated work, multiple plausible candidates, or a signal maps to a different concern), ask once: "I see manifest X in scope — amend it, pick a different one, or start fresh?" Don't silently choose.

Once a candidate is identified, read it and compare its Goal + Deliverables against the new task. Apply the matching branch:

### Related (default)

**Amendment is the default.** Only "truly unrelated" work (clearly different problem space, not a continuation, refinement, follow-up, or polish) starts fresh. When ambiguous, default to amendment. The asymmetry is intentional: a wrong "fresh" decision silently loses prior INVs/ACs/PGs; a wrong "amend" decision is correctable via the announcement.

Announce, then proceed as if `--amend <prior-path>` had been passed. Follow the rest of this file from that point. Emit the announcement regardless of interview mode (preserves audit trail in transcript); it is one line and non-blocking:

> Detected prior manifest in session: `/tmp/manifest-{ts}.md` (`<title from H1>`). Defaulting to amendment mode — interrupt me if this is unrelated work and I'll start fresh.

### Truly unrelated

Proceed fresh with a one-line note so the user can correct if needed:

> Found prior manifest `<path>` (`<title>`), but new task targets `<different problem space>`. Starting fresh — interrupt me to amend instead if I read this wrong.

### Prior manifest unreadable

Fall back to fresh with a one-line note:

> Prior manifest `<path>` is no longer available; starting fresh.

### No prior manifest

Proceed fresh; no announcement.

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

Triggered implicitly by `/define`'s in-session detection of a prior related manifest (no explicit `--amend` flag). The detection rules and branches (Related / Truly unrelated / Prior manifest unreadable) live in the **Session-Default Detection** section above. Once detection lands on Related and the agent decides to amend, behavior **follows the Standalone path** — interview scoped to the change (per the active interview mode), verification loop, summary for approval. The interview mode (`thorough` / `minimal` / `autonomous`) is **not** overridden by the trigger context — `/auto` invocations still run autonomously, just amending the prior manifest instead of starting fresh. The user is told upfront via the announcement (per Session-Default Detection) and can verbally redirect to a fresh manifest if the relatedness call was wrong.

## What to Preserve

Intent, Approach architecture (unless contradicted), existing ACs/INVs that aren't affected, Process Guidance, Known Assumptions. Execution order may need updating if new deliverables are added.

## What to Change

Add/modify/remove ACs, add new deliverables, update INVs, adjust trade-offs. Use amendment IDs per the manifest's Amendment Protocol (e.g., `INV-G1.1 amends INV-G1`). Always log changes in `## Amendments` with what changed and why.
