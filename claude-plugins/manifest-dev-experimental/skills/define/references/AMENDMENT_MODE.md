# Amendment Mode

/define modifies an existing manifest instead of building from scratch.

## Cumulative Manifest Rule

**The manifest is the canonical source of truth for the PR/branch lifetime — or the entire PR set / branch set in multi-repo cases — not for a single task.** After every amendment, the manifest describes the FULL state: intent, every deliverable (across every repo when multi-repo), every Global Invariant, every Process Guidance entry, every Known Assumption. The latest increment layers onto prior content, never substitutes for it.

**No silent drops.** Prior content preserved by default. Removal is explicit — supersessions logged in the `## Amendments` section with rationale. Read the full prior manifest before changing.

Multi-repo specifics: `MULTI_REPO.md` §f.

**Deferred-auto re-verification after amendment** — when an amendment substantively changes a `method: deferred-auto` criterion's verify block, prior deferred coverage for that criterion is conceptually invalidated. The user is responsible for re-signaling readiness in chat to re-run the amended criterion before the gate clears. (Consistent with user-as-coordinator stance — no automatic invalidation.)

## Trigger

The conversation context carries the reason — user message, PR comment, explicit change request. Read it, determine what to change. Existing decisions (ACs, INVs, PGs, Approach, Trade-offs) preserved unless directly contradicted. Add new items, modify contradicted items, or remove items that no longer apply (with explicit log entry). Coverage applies scoped to the change — not the full manifest.

## Session-Default Detection

Invoked from /define's Pre-flight when chat-derived amendment intent ("also handle X", "change Y", "that's wrong") combines with transcript references to a prior manifest. Skipped when the input plainly references a specific `/tmp/manifest-*.md` path — that signal wins, the named manifest is source of truth (agent confirms with user only if relationship to the new task is unclear).

Detection signals (most-recent / most-specific wins):
1. **In-session completion line** — `Manifest complete: /tmp/manifest-{ts}.md` earlier in transcript. Most recent wins.
2. **Conversation reference** — a `/tmp/manifest-*.md` path mentioned in chat.

When ambiguous (multiple candidates, or signal maps to different concern), ask once: *"I see manifest X in scope — amend it, pick a different one, or start fresh?"*

Compare candidate's Goal + Deliverables against the new task. Apply the matching branch:

### Related (default)

**Amendment is the default.** Only clearly-unrelated work (different problem space, not a continuation/refinement/polish) starts fresh. When ambiguous, amend — a wrong "fresh" silently loses prior content; a wrong "amend" is correctable via the announcement. Announce, then proceed as if amend had been triggered explicitly:

> Detected prior manifest in session: `/tmp/manifest-{ts}.md` (`<title>`). Defaulting to amendment mode — interrupt me if this is unrelated work and I'll start fresh.

### Truly unrelated

Proceed fresh with a one-line note:

> Found prior manifest `<path>` (`<title>`), but new task targets `<different problem space>`. Starting fresh — interrupt me to amend instead if I read this wrong.

### Prior manifest unreadable

Fresh with a note: *"Prior manifest `<path>` is no longer available; starting fresh."*

### No prior manifest

Proceed fresh; no announcement.

## Three Contexts

### 1. Standalone

User invokes /define for amendment directly (or via chat-derived amend intent). Full interactive mode: interview the user about the change (probing via /figure-out when gaps surface), present summary for approval.

### 2. From /do (Autonomous Fast Path)

Caller-context inferred. When /define is invoked from /do's Self-Amendment path (invocation chain shows /do is upstream), it's an autonomous amendment, not interactive. No flag needed — caller context is the signal.

Behavior: no user approval gates. Targeted changes from escalation context. Write updated manifest in-place so /do can resume. Log in `## Amendments`.

### 3. Session-Default

Detected per Session-Default Detection above. When "Related" fires, follow the Standalone path: interview scoped to the change, summary for approval. /auto-driven amendments skip the summary per /auto's autonomous contract; standalone wait for it.

## What to Preserve

Intent, Approach architecture (unless contradicted), unaffected ACs/INVs, Process Guidance, Known Assumptions. Execution order may update if new deliverables are added.

## What to Change

Add/modify/remove ACs, add new deliverables, update INVs, adjust trade-offs. Use amendment IDs per the manifest's Amendment Protocol (e.g., `INV-G1.1 amends INV-G1`). Always log changes in `## Amendments` with what changed and why.
