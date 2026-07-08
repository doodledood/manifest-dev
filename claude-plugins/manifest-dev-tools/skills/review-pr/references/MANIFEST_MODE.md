# Manifest mode (`--manifest <path>`)

In manifest mode the skill independently re-verifies the manifest's contract instead of running the generic `review-code` reviewer fleet — the reviewer-side, optionally cross-model re-execution of the same Acceptance Criteria and Global Invariants that `/do` runs in-session. Everything else in the SKILL.md one-shot pass — thread advancement, voice profile, the single batched `comment` review, the user-confirmed-only approval path, `--loop` — is unchanged; only the code-verification half of step 2 branches here.

## Verify the manifest

Read the manifest fully, then spawn one **general-purpose** subagent per Acceptance Criterion and per Global Invariant, each driven by that criterion's `verify.prompt:` **verbatim** — no rewording — evaluated against the PR head. This is the same fanout `/do` runs in-session (`manifest-dev:do`): the optional `verify.model:` selects the subagent's model — running on a different tool/model is where the cross-model independence comes from — and `phase:` ordering is respected, serial across phases and parallel within. Each subagent returns PASS, FAIL, or BLOCKED.

The generic `review-code` fleet is **not** also run. `/define` default-injects a `review-code` Global Invariant, so generic code-quality review already travels inside the manifest and runs *as* one of these verifications; the manifest is the single source of truth for what "done" requires. Running both would reintroduce a second source of truth and noisy duplicate comments on a contract-driven PR.

## PR-head checkout

`verify.prompt`s execute the code at PR head (tests, builds, greps). Like `/do` and `babysit-pr`, manifest mode runs against the current working checkout: ensure it is at the PR head SHA before spawning verifiers — check the head out if the runner isn't already on it — and derive head from GitHub each run, never from session memory.

## Posting & approval

Surface each FAIL or BLOCKED as one voice-compliant comment naming the failing criterion (its manifest id) and the verifier's concrete finding, anchored to the file:line the finding points at, else file- or PR-level; submit them through the SKILL.md **Posting** path (a single batched review, decision `comment`). When every criterion PASSes there are zero contract comments to post: take the SKILL.md **Zero comments to post** path — manifest-mode "all green" is the approval signal (user-confirmed in interactive sessions, no PR action under `--loop`/CI).

## Judgment pass (additive premise check)

Run the judgment pass per `references/JUDGMENT_PASS.md` as its **own parallel subagent**, spawned alongside the criterion verifiers in the same manifest-mode pass: the whole-PR question of whether the change earns its keep against the pain it solves. Manifest mode is where it matters most: a manifest can lock in a flawed premise, and the generic fleet is skipped here, so this is the only premise/surface reviewer running. Feed it the manifest's **Intent** as the stated pain, plus the PR head and description.

Like no-manifest mode, fresh judgment generation is **gated to once per PR** — run it only when no prior judgment finding exists on the PR (self-marker, durable GitHub state, not session memory), so it fires on the first pass and is skipped on later loop rounds and re-runs; advancing an existing judgment thread stays with the per-comment verifier and is not gated. **Premise-subsumption does not apply here** — there are no fleet findings to subordinate, since the fleet is skipped in manifest mode.

It is **strictly additive** and never touches the contract:

- The contract verdict — every Acceptance Criterion and Global Invariant — is computed exactly as it would be without the pass. A judgment finding never changes a criterion's PASS/FAIL, never blocks, and never gates approval.
- Judgment findings are the distinct non-severity class the reference defines — author-answerable questions, synthesized to one per root, posted through the same batched `comment` review and voice. They are **not** criteria, so they carry the base self-marker (no `ac=` id) and are fingerprinted by finding substance like any other comment.
- The all-green approval signal stays keyed to the contract: when every criterion PASSes, manifest mode is green **even if** the judgment pass posted questions — those are non-blocking and do not withhold the signal. They are still posted; the human decides.

## Fingerprint, don't re-post

PASS/FAIL comments recur every push, so track each by a content fingerprint (criterion id + finding substance), not comment id: re-post a criterion's FAIL only when its finding changes, and prune a FAIL whose criterion now PASSes. This keeps the thread clean and keeps `/do`/`babysit-pr` ingestion — which treats these comments as external review input it judges before acting — from looping on stale repeats. Carry the criterion id inside the SKILL.md self-marker (e.g. `<!-- manifest-dev:review-pr ac=AC-1.2 -->`) so the criterion half of the fingerprint matches exactly; the finding-substance half still reads the rendered body to decide whether the finding changed.

## Cycle summary

The SKILL.md reviewer-fleet and holistic-pass cycle-summary lines do not apply in manifest mode. Instead report, one line per Acceptance Criterion and Global Invariant: its manifest id, PASS/FAIL/BLOCKED, the model used, and the verifier's short finding. Then add one line for the judgment pass: premise questions posted — count and their roots — or `none`, so an all-green contract summary still records that questions were raised.

## Gotchas

- Run each `verify.prompt` verbatim and never also run the generic reviewer fleet — the manifest (which `/define` default-injects a `review-code` invariant into) is the single source of truth, and running both reintroduces a second source of truth with duplicate comments.
- Track PASS/FAIL comments by content fingerprint, not comment id — they recur after every push, and re-posting an unchanged FAIL loops `/do`/`babysit-pr` ingestion.
