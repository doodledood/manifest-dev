---
name: verify
description: 'Runs verifiers for Global Invariants and Acceptance Criteria from a Manifest. Spawns verifier agents in parallel within each phase, aggregates, routes outcome to /done or /escalate. Normally invoked by /do; users invoke `/verify --deferred` to run user-triggered deferred-auto criteria.'
user-invocable: true
---

Spawn verifiers for the in-scope criteria; aggregate; route the outcome to /done or /escalate. Phases run sequentially (Phase N+1 launches only when Phase N passes); criteria within a phase run concurrently. Route by criterion `method:` per `references/ROUTING.md` — bash/codebase/research → criteria-checker; subagent → the named agent; manual → /escalate; deferred-auto → skipped on normal passes, routed by `inner_method:` under `--deferred` (missing `inner_method:` → halt).

**Selective vs full with auto-final gate.** `--scope D1,D2` runs selective (in-scope ACs + all globals); absent → degenerates to full. After a true-selective green pass, auto-trigger a full pass via internal `--final` self-invocation — unconditional safety net for cross-deliverable regressions. /done is unreachable from selective green alone. Verifier prompts follow `references/PROMPT_FORMAT.md` strictly — three sections, **no framing** (no severity thresholds, no implementation context, no opinions, no leading language); the verify block's `prompt:` is authored by /define and passed verbatim.

**Outcome routing** in `references/OUTCOMES.md`. **Pass log contract** in `references/PASS_LOG.md` — every invocation appends a structured block; consumers MUST read the `deferred` flag first (under `deferred: true`, `result: pass` means deferred-auto criteria green, not the whole manifest) and skip `deferred: true` blocks when scanning for next-pass scope. **Deferred-auto** = automatically verifiable but user-triggered: normal passes skip; uncovered ones block /done (route to /escalate "Deferred-Auto Pending"); `--deferred` runs ONLY them, inherits `--scope`, never calls /done from itself, instructs user to re-invoke normal /verify on green. **Don't handle user feedback mid-pass** — messages are feedback to the caller (/do, or the user who invoked `--deferred`), not /verify. Verifier crash / timeout / unusable output → criterion FAIL with note that verification itself failed (not the criterion).

**Input.** `<manifest-path> <log-path> [--scope D1,D2,...] [--deferred]`. Either path missing → halt with usage. Manifest missing → halt. Log missing → create empty (must always be appendable). `--final` is internal; /do never passes it, users never pass it.
