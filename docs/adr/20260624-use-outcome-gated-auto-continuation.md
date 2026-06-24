# ADR: Use outcome-gated terminal success for `/auto` continuation

## Status
Accepted

## Context

The 2026-06-23 goal-setting work made unattended runs portable across hosts: source prompts describe a durable goal-setting / continuation capability instead of a single host command, and `/auto` owns one full-chain parent backstop spanning figure-out → define → do.

That parent contract carried the full `figure-out --autonomous` Read bar as part of the full-chain completion condition. This fixed premature phase advancement, but it blurred an older boundary: figure-out buys **process trust**, while define→do buys **artifact trust** through Manifest gates and independent verifier executions. In a later `/auto` run, the final result was acceptable even though the figure-out Read was not properly named. A post-hoc checker could therefore fail on a process narration defect after the downstream Manifest and `/do` evidence had already shown the final outcome was sound.

The repo already has the vocabulary for the distinction: Acceptance Criteria are verifiable gates; Process Guidance is non-verifiable work discipline; and a Host Continuation Backstop is an outer guard rather than a replacement for the Do/Verify Loop.

## Decision

`/auto` continuation contracts use **outcome-gated terminal success**.

The terminal full-chain completion condition is: `/define` has written the Manifest, `/do` has reported `/done`, and every Acceptance Criterion and Global Invariant has fresh independent verifier PASS evidence in the manifest gate ledger. Missing, stale, FAIL, BLOCKED/actionable, or escalation-pending gates remain non-terminal.

When `figure-out --autonomous` runs inside `/auto`, its full-anatomy Read remains required, but as a **Phase Checkpoint before `/define`**, not as a post-hoc terminal failure condition after `/do` has passed. The checkpoint still carries the same Read bar: every load-bearing branch pressed, Evidence Ledger explicit, assumptions separated from verified/inferred claims, independent re-derivation run or explicitly unavailable, rival set no longer moving, confidence/evidence/overturn conditions stated, and diagnosis-shaped work naming the concrete mechanism or earning underdetermination.

Standalone `figure-out --autonomous` is unchanged: when figure-out is the whole run, the Read is the deliverable, so the named full-anatomy Read remains the terminal completion contract.

General rule for future goals and manifests:

> Terminal success criteria should be auditable outcome/artifact conditions. Process rigor belongs in Phase Checkpoints or Process Guidance unless the process artifact itself is the deliverable.

## Alternatives Considered

- **Keep `/auto` terminal completion as “Read named, then Manifest, then `/do` PASS”**: preserves strong child-protocol enforcement, but lets a host checker fail a completed chain on a process-artifact defect even when final Manifest gates pass.
- **Drop the Read bar from `/auto` entirely**: rejected because a weak upstream understanding can still produce a rigorously verified wrong plan; the Read bar remains necessary before `/define` when figure-out runs.
- **Make figure-out independently verifier-gated**: rejected again; figure-out produces understanding and process trust, not a deliverable for `/do`-style verifier fan-out.
- **Treat every process rule as a Manifest gate**: rejected because it violates the manifest boundary: non-verifiable how-to-work guidance belongs in Process Guidance, not Acceptance Criteria.

## Consequences

### Positive

- Host continuation checkers focus terminal success on durable, auditable outcome evidence.
- `/auto` still protects the figure-out → define handoff with the full autonomous Read bar.
- The prompt/docs vocabulary now matches the repo's process-trust vs artifact-trust boundary.
- Future goal contracts get a portable calibration rule instead of accumulating one-off process requirements as pseudo-acceptance criteria.

### Negative

- A completed `/auto` transcript may contain a weakly named Read without making the final run non-terminal, if the issue is discovered only after `/do` has fresh all-gate PASS evidence.
- Reviewers who want strict child-protocol compliance must inspect the phase checkpoint itself, not infer it from terminal `/auto` completion.
- Existing docs/ADRs from 2026-06-23 remain historical context and must be read with this clarification.

## Source

- Session: `figure-out --with-docs --log`, 2026-06-24.
- Investigation log: `/Users/aviram.kofman/.manifest-dev/logs/figure-out-log-20260624-135303.md`.
- User observation: `/auto` produced an acceptable final result even though the Read was not properly named; goal success criteria should focus on final outcome where possible.
- Related: `20260606-figure-out-process-trust-vs-define-do-artifact-trust`; `20260611-figure-out-evidence-ledger-and-independent-rederivation`; `20260623-use-host-continuation-as-optional-do-backstop`; `20260623-use-universal-goal-setting-language`.
