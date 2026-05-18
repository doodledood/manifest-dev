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

1. A **vocabulary token** from a fixed workflow-neutral set: `bash sleep <N>; reinvoke`, `retrigger <check>`, `reply <thread>`, `reply-and-resolve <thread>`, `re-request-review`, `sync-description`. Each token names a literal GitHub-state action — not a workflow step. Because tokens are concrete literal commands the caller (typically `/do`) reads as text and executes naturally, **no special dispatch discipline is required in the caller — the literal-command shape IS the discipline.** The substitution failure modes originally observed (Stop, /loop, busy-wait) happened with prose hints like "suggest waiting" where the model had to invent a mechanism; with literal text like `bash sleep 600; reinvoke` in the agent's output, the model reads and executes the text it sees.

2. **Free-form prose** describing a solvable-but-novel observation, with an optional suggested approach in the same field. The caller reads the prose with LLM judgment and decides what to do — execute a recognized action, route to a human-decision step (`/escalate` in `/do`'s case), amend the work's scope, etc.

The vocabulary is intentionally bounded to workflow-neutral GitHub actions. Workflow-aware tokens (the prior `escalate`) are removed; workflow decisions live caller-side. The prose escape valve makes the vocabulary's boundedness practical.

The multi-line FAIL form uses `Reason:` / `Suggested:` / `Context:` fields per failing gate. Inline `- <gate>: FAIL — <token>` stays valid for terse cases. Prose findings always use multi-line form.

`/do` itself does not change for this design — it reads FAIL bodies as it always has, with its general `/escalate` and amendment routing rules. The trust here is in the LLM-reader-of-the-agent's-output: literal-command tokens get executed because they're literal text the model reads as instructions. No special "execute directives literally; do not substitute" paragraph in `/do` — that was belt-and-suspenders for a problem the vocabulary shape already prevents.

## Alternatives Considered

- **Rigid fixed vocabulary including `escalate`** — the original direction in this same PR. *Rejected mid-PR*: the agent shouldn't carry workflow tokens (it would mirror `/do`'s `/escalate`, leaking workflow awareness across an agent boundary that should be clean); the fixed vocabulary is too rigid for solvable-but-novel observations. The original ADR text is **rewritten in place** to reflect the final design (per the in-PR-override convention — when an ADR introduced in a PR supersedes another from the same PR, the earlier text is rewritten in place rather than left as a separate Superseded record, to reduce `docs/adr/` clutter when a single PR's design is still iterating).
- **Full revert to prose hints with caller judgment (no vocabulary at all)** — *rejected*: caller-judgment-only is exactly what produced the three observed wrong inventions (Stop, `/loop` misuse, busy-wait). Vocabulary tokens for clear cases keep the literal-command shape that prevents those failures; prose handles flexibility for novel cases.
- **Workflow-neutral token replacing `escalate` (e.g., `human-decision-needed`)** — considered, *rejected*: even a renamed token implies the agent knows a workflow step exists. Prose is the better escape valve because it forces the agent to describe the observation (which is useful to the caller) rather than emit a vague "this needs a human" label.
- **Explicit substitution-prevention paragraph in `/do`** — proposed and tried during D1; *removed during this PR's final iteration*: with literal-command vocabulary tokens in the agent's output, the discipline is implicit in the shape (the model reads `bash sleep 600; reinvoke` and executes that text; there's no prose to invent a substitution for). An explicit "don't substitute Stop / `/loop` / `ScheduleWakeup` / busy-wait" paragraph in `/do` is belt-and-suspenders for a problem the vocabulary shape already prevents. Removed to trust model capability and keep `/do` unchanged for this work.

## Consequences

### Positive

- Agent boundary is cleaner: it reports findings, like other reviewer agents (`change-intent-reviewer`, `code-bugs-reviewer`). No workflow leakage across an agent that should be a pure inspector.
- `/do` is unchanged for this work — no cross-file invariant duplication, no special dispatch logic, no D1/D5/D6 carve-out paragraphs added to `/do`'s SKILL.md.
- The vocabulary-token shape IS the literal-execution discipline: the model reads literal text (`bash sleep 600; reinvoke`) and executes it; the substitution failure modes that motivated the rigid-vocabulary direction were prose-hint failures and don't recur with literal-command output.
- Solvable-but-novel cases get accurate description (prose) instead of forced-fit to the wrong vocabulary token.
- The fixed vocabulary stays small and focused (six tokens, all literal GitHub-state actions). New scenarios don't require vocabulary expansion — they use prose findings.

### Negative

- Trust-the-model bet: the design assumes an LLM reader of literal-command tokens executes them as text, rather than substituting "equivalent" mechanisms. The originally-observed three failure modes (Stop, /loop, busy-wait) were prose-hint failures and don't apply to literal-command output by construction — but if a future model invents substitutions even given literal `bash sleep` directives, we'll see it as a regression and may need to re-introduce an explicit discipline rule in `/do`.
- The FAIL output format is slightly less predictable for any tooling that wants to parse it: callers can't assume a finite enum, they must handle prose. In practice the consumer is an LLM (`/do` itself), and LLMs handle both shapes naturally — but the lack of a strict schema is a real change from the rigid-vocabulary direction.
- A reader looking at this ADR's filename (`verifier-fail-hints-are-directives`) and finding it describes "findings, not directives" will notice the mismatch. The filename is a historical artifact of the first commit; the body describes the final shipped design. The in-PR-override convention accepts this filename-vs-body mismatch as the cost of reducing `docs/adr/` clutter.

## Source

- Session: `/figure-out --with-docs` session on 2026-05-18 (this branch). Iterated through implementation amendments D1, D4, D5, and D6 of the manifest at `.manifest/verifier-fail-hints-directives-2026-05-18.md`.
- Manifest: `.manifest/verifier-fail-hints-directives-2026-05-18.md`
- In-PR override note: this ADR was originally written in commit `58375f6` on this branch as "Verifier FAIL hints are directives, not suggestions" with a rigid-vocabulary direction. It was rewritten in place during D6 (this commit) to reflect the final workflow-neutral design. Per the in-PR override convention: an ADR introduced in the same PR that supersedes another ADR from that PR is rewritten in place rather than written as a separate Superseded record, to reduce `docs/adr/` clutter when a single PR's design is still iterating. Once a PR merges, the standard ADR immutability rule applies — future supersedences will use separate `Superseded by` records.
- Related: (none)
