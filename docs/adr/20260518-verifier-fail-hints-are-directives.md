# ADR: github-pr-lifecycle FAIL findings — workflow-neutral, vocabulary or prose

## Status
Accepted

## Context

The `github-pr-lifecycle` agent inspects a GitHub PR and reports whether it's mergeable. When it isn't, the agent reports what's blocking — and the *shape* of that report has been the design question this ADR settles.

The starting direction (this same PR, first commit) was **rigid per-gate directive vocabulary** including a workflow-aware `escalate` token. The motivation was real: in earlier prose-hint designs, three failure modes were observed in the wild when callers tried to act on a "suggest waiting" hint — they stopped the session (assuming external wakeup), invoked `/loop` without wiring (effectively stopping), or busy-waited (re-invoking the verifier without an intervening sleep). The literal-execution discipline came from there.

Two further iterations during the same PR exposed problems with the rigid vocabulary:

1. **`escalate` is a workflow-aware token.** It mirrors `/do`'s `/escalate` skill and assumes the agent knows about manifest-execution workflow. Other reviewer agents in the codebase (`change-intent-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, etc.) don't carry workflow tokens — they report findings; callers decide workflow. The PR-lifecycle agent should follow the same pattern.

2. **Fixed vocabulary is too rigid for solvable-but-novel observations.** A CI failure with an unusual fingerprint shouldn't be force-fit to a bare `retrigger` (which says nothing about the fingerprint) or to terminal `escalate` (which gives up on something that might be solvable). The vocabulary covers known clean cases; novel observations need a different escape valve.

The substitution-prevention rule (no `Stop` / `/loop` / `ScheduleWakeup` / busy-wait for `bash sleep` directives) is still load-bearing — it prevents the originally-observed three failure modes. Where it lives has changed: it's now in `/do`'s SKILL.md only (it was previously also restated in the agent file).

## Decision

The `github-pr-lifecycle` agent emits per-gate **findings** in FAIL responses. Each finding's `Suggested:` field carries one of two things:

1. A **vocabulary token** from a fixed workflow-neutral set: `bash sleep <N>; reinvoke`, `retrigger <check>`, `reply <thread>`, `reply-and-resolve <thread>`, `re-request-review`, `sync-description`. Each token names a literal GitHub-state action — not a workflow step. The caller (typically `/do`) executes the token verbatim; substitution-prevention discipline applies (declared in `/do`'s SKILL.md).

2. **Free-form prose** describing a solvable-but-novel observation, with an optional suggested approach in the same field. The caller reads the prose with LLM judgment and decides what to do — execute a recognized action, route to a human-decision step (`/escalate` in `/do`'s case), amend the work's scope, etc.

The vocabulary is intentionally bounded to workflow-neutral GitHub actions. Workflow-aware tokens (the prior `escalate`) are removed; workflow decisions live caller-side. The prose escape valve makes the vocabulary's boundedness practical: when something doesn't fit cleanly, the agent describes it instead of forcing it.

The multi-line FAIL form uses `Reason:` / `Suggested:` / `Context:` fields per failing gate. Inline `- <gate>: FAIL — <token>` stays valid for terse cases where the suggested action is a single vocabulary token and no context would help (`retrigger flake-check`, `re-request-review`). Prose findings always use multi-line form.

Substitution-prevention rules (no `Stop` / `/loop` / `ScheduleWakeup` / busy-wait) live in `/do`'s SKILL.md only — the agent declares the literal-execution expectation for vocabulary tokens; `/do` enforces it.

## Alternatives Considered

- **Rigid fixed vocabulary including `escalate`** — the original direction in this same PR. *Rejected mid-PR*: the agent shouldn't carry workflow tokens (it would mirror `/do`'s `/escalate`, leaking workflow awareness across an agent boundary that should be clean); the fixed vocabulary is too rigid for solvable-but-novel observations. The original ADR text is **rewritten in place** to reflect the final design (per the in-PR-override convention — when an ADR introduced in a PR supersedes another from the same PR, the earlier text is rewritten in place rather than left as a separate Superseded record, to reduce `docs/adr/` clutter when a single PR's design is still iterating).
- **Full revert to prose hints with caller judgment (no vocabulary at all)** — *rejected*: caller-judgment-only is exactly what produced the three observed wrong inventions (Stop, `/loop` misuse, busy-wait). Vocabulary tokens for clear cases preserve literal-execution discipline where it matters most; prose handles flexibility for novel cases.
- **Workflow-neutral token replacing `escalate` (e.g., `human-decision-needed`)** — considered, *rejected*: even a renamed token implies the agent knows a workflow step exists. Prose is the better escape valve because it forces the agent to describe the observation (which is useful to the caller) rather than emit a vague "this needs a human" label.
- **Keep substitution-prevention rule duplicated in both agent and `/do`** — *rejected during D4–D6 cleanup*: the cross-file duplication was earlier defended as "invariant duplication" (per the prompt-engineering review checklist), but with the agent moving to workflow-neutrality, the rule's natural owner is the executor (`/do`). The agent's declaration of vocabulary tokens implies literal execution; `/do`'s SKILL.md spells out the discipline.

## Consequences

### Positive

- Agent boundary is cleaner: it reports findings, like other reviewer agents (`change-intent-reviewer`, `code-bugs-reviewer`). No workflow leakage across an agent that should be a pure inspector.
- Solvable-but-novel cases get accurate description (prose) instead of forced-fit to the wrong vocabulary token.
- The caller (`/do`) owns workflow decisions including `/escalate` routing — single source of truth for workflow logic, no parallel state across agent and skill.
- Substitution-prevention rules consolidate in `/do`; no cross-file duplication of the same invariant.
- The fixed vocabulary stays small and focused (six tokens, all literal GitHub-state actions). New scenarios don't require vocabulary expansion — they use prose findings.

### Negative

- `/do` does more LLM-judgment work (interpreting prose findings) — slight increase in the surface where caller judgment can fail. Mitigated by: (a) vocabulary tokens still cover the common cases where judgment most-often failed (wait directives especially); (b) prose findings include both the agent's observation and a suggested approach, so judgment has substrate to work with, not raw GitHub state.
- Substitution-prevention now lives in a single place (`/do`); if `/do` drifts, the rule could be weakened without the agent's side being a guard. Trade-off: clarity of ownership over cross-file invariant duplication.
- The FAIL output format is slightly less predictable for any tooling that wants to parse it: callers can't assume a finite enum, they must handle prose. In practice the consumer is an LLM (`/do` itself), and LLMs handle both shapes naturally — but the lack of a strict schema is a real change from the rigid-vocabulary direction.
- A reader looking at this ADR's filename (`verifier-fail-hints-are-directives`) and finding it describes "findings, not directives" will notice the mismatch. The filename is a historical artifact of the first commit; the body describes the final shipped design. The in-PR-override convention accepts this filename-vs-body mismatch as the cost of reducing `docs/adr/` clutter.

## Source

- Session: `/figure-out --with-docs` session on 2026-05-18 (this branch). Iterated through implementation amendments D1, D4, D5, and D6 of the manifest at `.manifest/verifier-fail-hints-directives-2026-05-18.md`.
- Manifest: `.manifest/verifier-fail-hints-directives-2026-05-18.md`
- In-PR override note: this ADR was originally written in commit `58375f6` on this branch as "Verifier FAIL hints are directives, not suggestions" with a rigid-vocabulary direction. It was rewritten in place during D6 (this commit) to reflect the final workflow-neutral design. Per the in-PR override convention: an ADR introduced in the same PR that supersedes another ADR from that PR is rewritten in place rather than written as a separate Superseded record, to reduce `docs/adr/` clutter when a single PR's design is still iterating. Once a PR merges, the standard ADR immutability rule applies — future supersedences will use separate `Superseded by` records.
- Related: (none)
