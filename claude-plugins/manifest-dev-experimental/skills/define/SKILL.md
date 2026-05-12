---
name: define
description: 'Manifest builder. Turns shared understanding (from /figure-out or transcript) into a Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Auto-invokes /figure-out when the transcript lacks understanding. Use when planning features, scoping refactors, debugging complex issues, or whenever a task needs structured thinking before coding. Triggers: define, manifest, scope, plan, spec out, break down.'
user-invocable: true
---

# /define

Encode shared understanding into a verifiable Manifest at `/tmp/manifest-{timestamp}.md` (where `{timestamp}` is `YYYYMMDD-HHMMSS` UTC). Use the same `{timestamp}` for the discovery log (`/tmp/define-discovery-{timestamp}.md`). The manifest captures: **what we build** (Deliverables + Acceptance Criteria), **how we get there** (Approach — initial direction, expect adjustment), **rules we must follow** (Global Invariants + Process Guidance).

**Front-door: figure-out.** If the transcript lacks shared understanding for this task (no prior `figure-out` invocation, no equivalent grilling conversation), invoke `manifest-dev-experimental:figure-out` first with one announcement line ("no prior understanding detected — grilling first"). When understanding lands, return here to encode.

**Exception:** pure `--amend` invocations skip the figure-out front-door — the existing manifest is the understanding artifact.

## Input

`$ARGUMENTS` = task description, optionally with:

| Flag | Behavior |
|------|----------|
| `--amend <path>` | Amend the existing manifest at `<path>`. Missing argument or path → halt. |
| `--from-do` | Marks amendment as triggered by /do. Used with `--amend`. Routes per Self-Amendment fast path (no summary approval, /do resumes immediately). |
| `--babysit <pr-url>` | Synthesize a lifecycle-only manifest from an existing PR. Routes to `references/BABYSIT_MODE.md`. Missing or inaccessible URL → halt naming the failure. `--babysit` + `--amend` together → halt. |
| `--platform github\|none` | PR-lifecycle platform. When omitted: with `--babysit`, infer from PR URL host; without `--babysit`, infer from `origin` remote (`github.com` → `github`, else `none`). When `--platform github` resolves, `tasks/PR_LIFECYCLE.md` composes onto `tasks/CODING.md`. Invalid value → halt. |
| `--canvas` | Generate a Shared Understanding Canvas alongside the manifest — a visual side-channel the user glances at during the chat to spot misalignment on intent, flow, and scope at a glance. Follow `references/CANVAS_MODE.md` (it owns activation gate, lifecycle, and run-order placement). |

Flags can appear anywhere. If `$ARGUMENTS` has no task text (empty, or only flags), ask: `What would you like to build or change?` Exception: skip this when any amend trigger applies (`--amend` is set, OR `$ARGUMENTS` contains a `/tmp/manifest-*.md` path — bare path counts as routing).

## Pre-flight: resolve manifest context

Resolves to **babysit**, **amend**, or **fresh**.

- `--babysit <pr-url>` set → babysit. Follow `references/BABYSIT_MODE.md`.
- `--amend <path>` set, OR `$ARGUMENTS` contains a `/tmp/manifest-*.md` path → amend. Confirm with user only if the manifest's relationship to the new task is unclear. Follow `references/AMENDMENT_MODE.md`.
- Transcript contains `Manifest complete: /tmp/manifest-*.md` line → read `references/AMENDMENT_MODE.md` "Session-Default Detection"; its branch picks amend or fresh.
- Else → fresh.

## Branch-diff seeding

**Trigger:** Pre-flight resolved to fresh AND the current branch has commits ahead of its base.

**Why:** Work already on the branch belongs in the manifest (Cumulative Manifest Rule — see `references/AMENDMENT_MODE.md`).

**Base inference** (first hit wins): upstream tracking branch → `origin/main` → `origin/master` → ask user once.

If user declines to identify a base, proceed with a fresh manifest and log existing commits as a Known Assumption: `[ASM-N] Branch has commits ahead of unidentified base | Default: treat as out of scope | Impact if wrong: existing work isn't tracked or verified.`

When base is identified: diff branch against base, read diff and commit messages, incorporate existing changeset into manifest's Intent (what's done) and starting Deliverables (work-in-progress as prior context, new ACs added on top for completion + new task).

Skip cleanly when: no commits ahead, or Pre-flight resolved to amend.

## Domain guidance

Domain-specific guidance lives in `tasks/`:

| Domain | Indicators | File |
|--------|------------|------|
| Coding | Any code change (base for Feature, Bug, Refactor) | `tasks/CODING.md` |
| Feature | New functionality, APIs, enhancements | `tasks/FEATURE.md` |
| Bug | Defects, errors, regressions, "not working" | `tasks/BUG.md` |
| Refactor | Restructuring, "clean up", pattern changes | `tasks/REFACTOR.md` |
| PR lifecycle | Shipping a change through CI, review, approvals | `tasks/PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `tasks/PROMPTING.md` |
| Writing | Prose, articles, copy, social, creative (base) | `tasks/WRITING.md` |
| Document | Specs, proposals, reports, formal docs (base: Writing) | `tasks/DOCUMENT.md` |
| Research | Investigations, analyses, comparisons | `tasks/research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials (base: Writing) | `tasks/BLOG.md` |

**Composition.** Code-change tasks combine CODING.md (base quality gates) with domain specifics. Text-authoring tasks combine WRITING.md with content-type guidance. Research composes RESEARCH.md with source-type files in `tasks/research/sources/`. Domains aren't mutually exclusive — "bug fix that requires refactoring" uses both BUG.md and REFACTOR.md.

**PR lifecycle composition.** `PR_LIFECYCLE.md` composes onto CODING.md when `--platform github` resolves. Templates a single AC invoking the `github-pr-lifecycle` agent; the agent owns lifecycle gate logic, and the AC's `verify.prompt:` is the steering surface for per-PR nuances (labels, named approvers, known-flaky CI, retrigger overrides). Multi-repo manifests auto-template the AC per repo declared in `Repos:`.

**Exception.** PROMPTING tasks do NOT compose with CODING.md unless the task also changes executable code.

**Task file content types:**
- **Quality gates** (`## Quality Gates` section with thresholds/criteria) — auto-include as INV-G*. Omit clearly inapplicable with logged reasoning.
- **Defaults** (`## Defaults` section) — encoded pre-interview as PG-*; included in manifest without probing; user reviews and removes if not applicable.
- **Resolvable content** (risks, scenarios, trade-offs) — these are **probing fuel for /figure-out**. Hand to figure-out as topics to grill; encode dispositions as INV/AC/R/T.
- **Compressed awareness** (bold-labeled one-line summaries) — informs probing; no resolution needed.
- **Reference files** (`references/*.md`) — lookup data for verifier agents; don't load during define.

Encode quality gates + Defaults immediately after reading task files. Note in discovery log.

## Multi-repo

When conversation, task description, or branch context indicates multiple repos, read `references/MULTI_REPO.md` for schema additions and cross-repo verification rules.

## Coverage (manifest checks, not interview script)

After synthesizing the manifest, the `manifest-verifier` agent checks five coverage goals against the manifest itself — not as questions you ask the user, but as audits on the artifact:

| Goal | Check on the manifest |
|------|-----------------------|
| Domain Understanding | Project-specific (not generic) failure scenarios encoded as R-* or AC-* |
| Reference Class | Task type named; common failure modes for that class covered |
| Failure Modes | Every anticipated scenario has a disposition (encoded, scoped out, or mitigated by Approach) |
| Positive Dependencies | Load-bearing assumptions surfaced as ASM-* or encoded as INV-G* |
| Process Self-Audit | Scope-creep / edge-case-deferred / "temporary-becomes-permanent" patterns addressed (skippable for narrow scopes — single deliverable, no incremental-addition risk) |

The verifier returns CONTINUE (gaps + questions for figure-out to resolve) or COMPLETE (proceed to summary).

## Approach Section

Include the Approach Section when ANY of: multi-deliverable, unfamiliar domain, architectural decision present, high-risk implementation. Skip when none apply.

- **Architecture** — generate concrete options from existing patterns. Direction (structure, patterns, flow), not script.
- **Execution Order** — propose based on dependencies. Include rationale (why this order — dependencies, risk reduction).
- **Risk Areas** — pre-mortem outputs (`[R-N]`). Each risk has detection criteria. Focus on likely/high-impact, not exhaustive.
- **Trade-offs** — decision criteria for competing concerns. Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**Architecture vs Process Guidance.** Architecture = structural decisions (components, patterns, structure). Process Guidance = methodology constraints (tools, manual vs automated). "Add executive summary covering X, Y, Z" is Architecture. "No bullet points in summary sections" is Process Guidance.

## What the Manifest captures

| Category | What | Examples |
|----------|------|----------|
| Global Invariants (INV-G*) | Negative constraints, ongoing, verifiable | "No breaking changes to public API"; "Don't edit /legacy" |
| Process Guidance (PG-*) | Non-verifiable HOW constraints | "Manual optimization only"; "No bullet points in summary" |
| Deliverables + ACs | Positive milestones (functional/non-functional/process) | "Section X explains concept Y"; "Document under 2000 words"; "Contains 'Executive Summary' section" |

## Discovery log

Maintain `/tmp/define-discovery-{timestamp}.md` as discoveries happen. The log is **append-only** — never rewrite past entries; later entries supersede earlier ones, but earlier text stays. Hard floor: every decision that affects the manifest goes in. Skip routine status pings and restatements of what the user just said. Open the log with what's already understood from context, then narrate as the interview unfolds. **Read the full log before synthesis** — any opened thread without a documented disposition is a gap to resolve. The verifier consumes this log alongside the manifest.

## Encoding disciplines

- **Insights become criteria.** Every discovery must be encoded — INV-G*, AC-*, PG-*, R-*, T-*, or ASM-* — or explicitly scoped out with logged reasoning.
- **Automate verification.** When a criterion seems to require manual verification, push back: suggest automation, or ask the user for ideas. Manual only as last resort or on explicit request.
- **Verification phases.** Each verify block accepts optional `phase:` (unquoted integer, default 1). Group by iteration speed — faster feedback loops first. Fast checks (bash, agent reviewers) stay in default phase. Slow checks (e2e tests, deploy-dependent) go later. Manual goes last. Omit `phase:` for phase 1; non-contiguous phases valid.

## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]
- **Medium:** local *(default and currently only supported)*

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual | deferred-auto
    phase: 1                       # optional integer, default 1
    timeout: 30s | 5m | 6h | 1d    # optional wall-clock cap (integer + s|m|h|d). Use for lifecycle ACs that legitimately wait (CI polling, approval-wait, deploy cycles) to prevent runaway when the dispatched action is `sleep` repeatedly. Absent → no cap.
    inner_method: subagent | bash | codebase | research   # REQUIRED when method: deferred-auto
    command: "[if bash]"
    agent: "[if subagent]"
    model: "[optional, if subagent — defaults to inherit]"
    prompt: "[if subagent or research, or matching deferred-auto inner_method]"
  ```

*`deferred-auto`: user-triggered; runs only via `/verify --deferred`. Required `inner_method:` names the underlying verifier type. See `references/MULTI_REPO.md` §e for cross-repo semantics.*

## 4. Process Guidance
- [PG-1] Description: ...

## 5. Known Assumptions
- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: ...
    phase: 1
    # ...same fields as INV-G verify
  ```
````

## ID Scheme

| Type | Format | Example | Consumer |
|------|--------|---------|----------|
| Global Invariant | INV-G{N} | INV-G1 | /verify |
| Process Guidance | PG-{N} | PG-1 | /do |
| Risk Area | R-{N} | R-1 | /do (watched) |
| Trade-off | T-{N} | T-1 | /do (consulted) |
| Known Assumption | ASM-{N} | ASM-1 | /verify (audited) |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1 | /verify |

## Verification Loop

After writing the manifest, invoke the verifier:

```
Invoke the manifest-dev-experimental:manifest-verifier agent with: "Manifest: /tmp/manifest-{timestamp}.md | Log: /tmp/define-discovery-{timestamp}.md"
```

Pass only the paths with labels. No summary, no framing, no commentary on the manifest itself — let the verifier assess independently.

The verifier returns **CONTINUE** or **COMPLETE**:
- **CONTINUE** — gap-questions for figure-out to grill the user on. Invoke figure-out with the verifier's questions. When threads resolve, update manifest, re-invoke verifier. **Present verifier findings verbatim** when surfacing to the user — no paraphrasing, no editorializing.
- **COMPLETE** — proceed to Summary.

## Summary for Approval

Digest the manifest into a scannable summary the user approves at a glance. Plain language. No manifest codes (D1, AC-1.1, INV-G3), no YAML, no structured-document vocabulary. Default shape:

- **The plan** — one-line headline of what's being done and why.
- **What I'll build** — work items grouped naturally; don't enumerate every sub-task.
- **Guardrails** — invariants as plain rules.
- **How I'll verify** — brief description of verification approach.

Include an ASCII architecture diagram when the task has multiple components with inter-component flow.

**Test:** if it reads like a compressed manifest (codes, YAML, structured labels in prose; enumerated criteria; abstractions hiding content), rewrite. If it reads like something you'd say to a colleague, it's right.

**After presenting**, wait for the user's response:
- *Approval* ("looks good", "approved") → Complete.
- *Feedback* ("also add X", "change Y") → revise manifest, re-present summary. Do not implement.
- *Explicit /do invocation* → /define is done; /do takes over.
- *Decline* ("scrap this", "cancel") → exit silently without writing the manifest.

## Stopping

The interview style is /figure-out's, not /define's. /define gets out of /figure-out's way for understanding; its own job is encoding.

If the user signals "enough" / "ship it" / "good enough" / "stop asking" during the verifier loop, auto-decide remaining unresolved threads (each gets the recommended default, encoded with `(auto)` annotation and logged in Known Assumptions). Continue through synthesis; expect termination via approval.

If the user explicitly invokes /do: when manifest already written, print `Manifest complete: ...` per Complete and hand off; when synthesis incomplete, finish with auto-decisions, write manifest, hand off without summary approval.

## Complete

Output the manifest path and stop. Substitute placeholders before printing — `{timestamp}` is the manifest's timestamp; `<dir>` is the project directory in the slug form used by `~/.claude/projects/` (path separators replaced with `-`, e.g., `-home-user-manifest-dev` for `/home/user/manifest-dev`); `${CLAUDE_SESSION_ID}` is the env value. If this run iterated on a previous manifest's execution log, substitute the actual log path in the `To execute:` hint; otherwise omit the bracketed clause.

```text
Manifest complete: /tmp/manifest-{timestamp}.md
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do /tmp/manifest-{timestamp}.md [log-file-path if iterating]
```

Auto-decided items (Stopping § above) carry an `(auto)` annotation immediately after the ID (e.g., `[INV-G2] (auto) Description: ...`). Each auto-decided item also appears in Known Assumptions with reasoning.
