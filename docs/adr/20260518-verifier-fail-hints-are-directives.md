# ADR: Verifier FAIL hints are directives, not suggestions

## Status
Accepted

## Context

The `github-pr-lifecycle` agent is the only specialized verifier currently in the manifest-dev plugin. It is invoked by `/do` (via `/auto --babysit` → `/define --babysit` → `/do`) as the verifier subagent for the babysit lifecycle Acceptance Criterion. The current contract is that the agent returns `PASS` when the PR is mergeable, otherwise `FAIL` with a "natural-language hint for the caller to dispatch" — and `/do` "consumes the hint with LLM judgment and decides the next step."

In the wild, when a gate FAILs with a suggestion to wait (for example, a reviewer hasn't yet posted approval), three different wrong behaviors have been observed from the caller:

1. **Stopping the session** — the model treats the conversation thread as resumable and ends its turn, assuming something external will ping it back. Nothing does. The babysit silently dies.
2. **Invoking `/loop` without `ScheduleWakeup` wiring** — the model invents a polling loop but the dynamic-loop mechanism requires a `ScheduleWakeup` call it doesn't make, so the loop terminates at the first iteration. Same outcome: session-ends-in-wait.
3. **Busy-waiting / skipping the sleep entirely** — the model re-spawns the verifier immediately, gets the same FAIL hint, re-spawns again. Effectively a no-op wait that hammers the GitHub API and burns context.

All three failures share a single root: the dispatch decision is a judgment call, and three models exercise that judgment three different wrong ways. Prose-shaped "suggest waiting" hints, even when the agent specifies who is being waited on, leave the *operational mechanism* of waiting underspecified. The model invents.

Constraints in play:

- `github-pr-lifecycle` has exactly one caller today: `/do`. (The April-vintage `/tend-pr` and `/tend-pr-tick` skills no longer exist in the plugin; only stale leftover directories remained in `.agents/skills/`, cleaned up in this session.)
- `/do`'s SKILL.md already classifies `waiting` as a non-budget-burning retry shape, but does not specify *how* to wait.
- The agent has the GitHub-state visibility to pick reasonable wait intervals per gate (CI ≈ minutes; reviewers ≈ hours).
- `bash sleep` caps at 600s per command — any longer wait requires multiple cycles, each one re-spawning the verifier.
- Steering already exists as a judgment-parsed plain-English overlay for user customization (retrigger-cap overrides, named approvers, known-flaky CI); extending it costs nothing new.

## Decision

Verifier FAIL hints become **directives**, not prose suggestions. The agent's caller executes them literally; the dispatch judgment is removed.

Specifically:

1. **Hint format.** `github-pr-lifecycle`'s FAIL output uses per-gate directive lines: `- <gate>: FAIL — <directive>`. Each directive is a literal command (`bash sleep 600; reinvoke`, `retrigger <check-name>`, `escalate`) or one of a small fixed vocabulary. No prose context inside the directive line; the `Breakdown:` structure already carries diagnostic context for the log and for human inspection.

2. **`/do`'s discipline rule.** `/do`'s SKILL.md gains an explicit rule: *execute verifier directive lines literally; do not substitute Stop / `/loop` / `ScheduleWakeup` / busy-wait*. The three failure modes are named so the model recognizes the temptations and rejects them.

3. **Wait-cadence policy lives in the agent.** Per-cycle duration is variable based on what's being waited on — CI ≈ 300s, reviewer ≈ 600s, bot ≈ 120s. The agent owns a cycle cap per gate (e.g., 6 cycles ≈ 1hr for reviewers). At cap, the directive switches to `escalate` and `/do` routes to `/escalate`.

4. **Cycle counter threading.** The cycle counter is threaded between `/do` and the agent via the existing `prior-retrigger-context` input mechanism — same shape as the existing CI retrigger counter, extended to also count wait cycles per gate.

5. **Steering customization.** User overrides land in the existing steering surface as a "Wait cadence:" block — judgment-parsed, no schema change. Example:
   ```
   Steering: |
     Wait cadence:
     - Review pending: 1800s per cycle, up to 12 cycles
     - CI pending: keep defaults
   ```

6. **Multi-gate failures.** When multiple gates FAIL, the breakdown lists multiple directive lines. `/do` executes each. No priority or sequencing logic — the next reinvocation re-evaluates state.

## Alternatives Considered

- **B. `/do`'s dispatch discipline owns the wait policy.** `/do`'s SKILL.md says "when a hint suggests waiting, do `bash sleep` + re-verify." The agent stays as a pure descriptor of GitHub state; the executor owns its own dispatch mechanics. — *Rejected:* pure description isn't enough when caller judgment fails reliably. Three observed wrong inventions (Stop, `/loop` misuse, busy-wait) all came from caller judgment on suggestion-shaped hints. Telling `/do` to "interpret 'wait' suggestions correctly" is exactly the discipline that has been observed to fail.

- **C. Delegate to `/tend-pr`.** `/auto --babysit` chains to `/tend-pr`'s `/loop` polling instead of `/do`. `/do` is not in the polling chair at all. — *Rejected:* `/tend-pr` and `/tend-pr-tick` no longer exist in the plugin. The April-vintage skill directories that survived in `.agents/skills/` were stale leftovers, not the current world. Reviving a deleted skill to fix a hint format is the wrong shape of change.

- **D. Harness-native `/loop` + `ScheduleWakeup`.** `/do` detects polling-shaped ACs and wraps them in self-paced `/loop` with `ScheduleWakeup` firing the next iteration. — *Rejected:* heavier architectural change to `/do` (it would have to operate inside `/loop` dynamic mode for babysit). The `bash sleep` + re-spawn pattern is sufficient for the per-cycle wait; `ScheduleWakeup` solves a problem we don't have. May reconsider if `/do` later needs polling for non-PR-lifecycle workloads.

## Consequences

### Positive

- Three observed failure modes (Stop, `/loop` misuse, busy-wait) are blocked by construction — the directive is literal, the model has nothing to interpret.
- Wait-cadence policy lives where the GitHub-state visibility is. The agent picks an interval appropriate to what's holding the PR (CI vs reviewer vs bot scanner).
- Cap policy is encapsulated in the agent. `/do` doesn't have to encode "reviewer waits are longer than CI waits."
- Hint payload is minimal. Diagnostic context (per-gate `Breakdown:`) is separate from the directive, so the log stays informative while the dispatch surface stays terse.
- Steering customization extends the existing judgment-parsed surface — no new fields, no schema change.
- Multi-gate failures stay simple: list multiple directive lines; no priority or scheduling logic in the agent or in `/do`.

### Negative

- The agent gains responsibility for caller-mechanics (specifically, naming `bash sleep` as the wait tool). This couples the inspector to one specific caller's mechanism. If a future caller has a different wait mechanism preference, the agent's directives won't match — would require a new directive vocabulary or per-caller agent variants.
- Per-cycle re-spawn of the inspector is more agent invocations than a single long wait would be. Each ~600s cycle re-invokes the agent to check state and emit the next directive. Cost is real but bounded.
- Wait policy changes require touching the agent (not the caller). Discoverability for "where does the cadence live" shifts from `/do` (the obvious place) to the agent (where the GitHub-state visibility is). Mitigated by steering being the user-facing override surface.
- The agent now needs to track cycle counts per gate via the existing prior-retrigger-context input — a small extension to that mechanism, not a new one, but it adds a dimension to that input's semantics.

## Source

- Session: `/figure-out --with-docs` session on 2026-05-18 (this conversation)
- Manifest: TBD — `/define` run scheduled to follow this ADR to capture the implementation plan
- Related: (none)
