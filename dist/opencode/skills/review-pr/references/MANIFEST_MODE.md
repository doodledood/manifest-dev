# Manifest mode (`--manifest <path>`)

In manifest mode the skill independently re-verifies the manifest's contract instead of running the generic `review-code` reviewer fleet — the reviewer-side, per-gate re-execution of the same Acceptance Criteria and Global Invariants that `/do` can run under any of its execution modes. Everything else in the SKILL.md one-shot pass — thread advancement, voice profile, the single batched `comment` review, the user-confirmed-only approval path, `--loop` — is unchanged; only the code-verification half of step 2 branches here.

## Verify the manifest

Read and validate the manifest fully, then spawn one fresh **general-purpose** subagent per Acceptance Criterion and per Global Invariant, each pointed at that gate by ID — given the manifest's absolute path and told to read the gate's text from the file rather than receiving a copy of it — evaluated against the PR head. A gate is a title, a body, an optional why, and a required kind (`judgment` or `deterministic`); a gate carrying a `verify` block of any shape, a gate stating a `phase` — a field the manifest schema no longer has — or a gate with no stated kind is the superseded schema: reject it with a clear request to create a fresh Manifest through `/define` without amending the incompatible file. Manifest review stays independently per-gate regardless of which `/do --verification` mode produced the branch. The reviewer context chooses the active model; model choice is not manifest data. Each subagent returns PASS, FAIL, or BLOCKED.

The generic `review-code` fleet is **not** also run. `/define` default-injects a `review-code` Global Invariant, so generic code-quality review already travels inside the manifest and runs *as* one of these verifications; the manifest is the single source of truth for what "done" requires. Running both would reintroduce a second source of truth and noisy duplicate comments on a contract-driven PR.

## PR-head checkout

Gate bodies execute against the code at PR head (tests, builds, greps). Like `/do` and `babysit-pr`, manifest mode runs against the current working checkout: ensure it is at the PR head SHA before spawning verifiers — check the head out if the runner isn't already on it — and derive head from GitHub each run, never from session memory.

## Posting & approval

Surface each FAIL or BLOCKED as one voice-compliant comment naming the failing criterion (its manifest id) and the verifier's concrete finding, anchored to the file:line the finding points at, else file- or PR-level; submit them through the SKILL.md **Posting** path (a single batched review, decision `comment`). When every criterion PASSes there are zero contract comments to post: take the SKILL.md **Zero comments to post** path — manifest-mode "all green" is the approval signal (user-confirmed in interactive sessions, no PR action under `--loop`/CI).

## Judgment pass (additive premise check)

Run the judgment pass per `references/JUDGMENT_PASS.md` as its **own parallel subagent**, spawned alongside the criterion verifiers in the same manifest-mode pass: the whole-PR question of whether the change earns its keep against the pain it solves. Manifest mode is where it matters most: a manifest can lock in a flawed premise, and the generic fleet is skipped here, so this is the only premise/surface reviewer running. Feed it the manifest's **Intent** as the stated pain, plus the PR head and description.

Like no-manifest mode, fresh judgment generation is **gated to once per PR** — run it only when no prior **judgment-marked** finding (`<!-- manifest-dev:review-pr judgment -->`) exists on the PR (durable GitHub state, not session memory), so once a question has posted, later passes skip regeneration and never re-nag; advancing an existing judgment thread stays with the per-comment verifier and is not gated. As in no-manifest mode, a silent pass posts no judgment marker, so on an all-green PR the pass may re-run on later rounds — bounded and harmless (it stays silent). **Premise-subsumption does not apply here** — there are no fleet findings to subordinate, since the fleet is skipped in manifest mode.

It is **strictly additive** and never touches the contract:

- The contract verdict — every Acceptance Criterion and Global Invariant — is computed exactly as it would be without the pass. A judgment finding never changes a criterion's PASS/FAIL, never blocks, and never gates approval.
- Judgment findings are the distinct non-severity class the reference defines — author-answerable questions, synthesized to one per root **by the judgment subagent itself** (manifest mode skips the holistic pass, so the pass does its own collapsing), posted through the same batched `comment` review and voice. They are **not** criteria, so instead of the `ac=` extension they carry the `judgment` discriminator token (`<!-- manifest-dev:review-pr judgment -->`) and are fingerprinted by finding substance like any other comment.
- The all-green approval signal stays keyed to the contract: when every criterion PASSes, manifest mode is green **even if** the judgment pass posted questions — those are non-blocking and do not withhold the signal. They are still posted; the human decides.

## Fingerprint, don't re-post

PASS/FAIL comments recur every push, so track each by a content fingerprint (criterion id + finding substance), not comment id: re-post a criterion's FAIL only when its finding changes, and prune a FAIL whose criterion now PASSes. This keeps the thread clean and keeps `/do`/`babysit-pr` ingestion — which treats these comments as external review input it judges before acting — from looping on stale repeats. Carry the criterion id inside the SKILL.md self-marker (e.g. `<!-- manifest-dev:review-pr ac=AC-1.2 -->`) so the criterion half of the fingerprint matches exactly; the finding-substance half still reads the rendered body to decide whether the finding changed.

## Cycle summary

The SKILL.md reviewer-fleet and holistic-pass cycle-summary lines do not apply in manifest mode. Instead report, one line per Acceptance Criterion and Global Invariant: its manifest id, PASS/FAIL/BLOCKED, independent per-gate provenance, the reviewer context's model, and the verifier's short finding. Then add one line for the judgment pass: premise questions posted — count and their roots — or `none`, so an all-green contract summary still records that questions were raised.

## Gotchas

- Evaluate each gate from its own text in the manifest and never also run the generic reviewer fleet — the manifest (which `/define` default-injects a `review-code` invariant into) is the single source of truth, and running both reintroduces a second source of truth with duplicate comments.
- Track PASS/FAIL comments by content fingerprint, not comment id — they recur after every push, and re-posting an unchanged FAIL loops `/do`/`babysit-pr` ingestion.
