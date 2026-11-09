# Manifest mode (`--manifest <path>`)

In manifest mode the skill re-verifies the manifest's contract instead of running the generic `review-code` reviewer fleet — the reviewer-side assessment of the same Outcome, Acceptance Criteria and Global Invariants that `/do` works to satisfy. Everything else in the SKILL.md one-shot pass — thread advancement, voice profile, the single batched `comment` review, the user-confirmed-only approval path, `--loop` — is unchanged; only the code-verification half of step 2 branches here.

## Verify the manifest

Read and validate the Manifest fully, then assess its Outcome and every current Acceptance
Criterion and Global Invariant against the PR head. The Outcome is the requested result, assessed
as judgment ID `OUTCOME`; passing chosen checks alone is insufficient. A gate has a title,
Authority, claim body, Evidence, optional why and a required kind (`judgment` or `deterministic`).
Hard authority identifies a deliberately stated user requirement or applicable project, safety
or permission obligation. Working authority identifies an agent's revisable operational claim.
Evidence methods are working unless a hard claim explicitly requires them. Missing Outcome,
authority or kind, or a retired `verify` block or `phase`, requires fresh definition through
`define`; do not guess permission to weaken an older contract.

Follow SKILL.md's review organization rule; related claims and Outcome assessment may share a
context, but each retains its own verdict and evidence. Read each by ID from the file rather
than a supplied copy. Inspect the artifact and applicable evidence regardless of how the author
verified it; an author's verdict is not evidence. Assess the current contract without waiving
working claims or adding unsupported preferences. Read supported finding dispositions and their
evidence when supplied; test their grounds, rather than treating reviewer agreement as another
requirement. A contrary verdict names the new evidence or error in those grounds. A deliberately
required approval remains separate. A mistaken working claim is an amendment
finding, with its source and observed conflict; an amended claim needs fresh affected evidence.
The reviewer context chooses the active model, not the Manifest. Return PASS, FAIL or BLOCKED
with concrete evidence for each gate and the Outcome.

On a continued loop wake, pass each evaluator its applicable checkpoint: assessed criteria and
subject, reporting scope, outstanding findings, supported dispositions and accepted-promise
history, verified repairs, and intervening changes.
Judgment gates check those repairs and failures introduced or exposed by the changes; deterministic
checks run in full. Changed criteria or external evidence invalidate affected results even without
a new commit. A fresh explicit invocation keeps the independent review scope requested by its caller.

Run only the Manifest's Outcome assessment and gates for contract verification. A specialized quality gate activates its reviewer through that gate; do not add the generic fleet beside it.

## PR-head checkout

Gate bodies execute against the code at PR head (tests, builds, greps). Like `/do` and `babysit-pr`, manifest mode runs against the current working checkout: ensure it is at the PR head SHA before assessing the gates — check the head out if the runner isn't already on it — and derive head from GitHub each run, never from session memory.

## Posting & approval

Surface each FAIL or BLOCKED as one voice-compliant comment naming the failing criterion (its manifest id) and the verifier's concrete finding, anchored to the file:line the finding points at, else file- or PR-level; submit them through the SKILL.md **Posting** path (a single batched review, decision `comment`). When the Outcome and every criterion PASS there are zero contract comments to post: take the SKILL.md **Zero comments to post** path — manifest-mode "all green" is the approval signal (user-confirmed in interactive sessions, no PR action under `--loop`/CI).

## Judgment pass (additive premise check)

Activate the `review-pr-judgment` skill under the same review organization rule. Give it the inputs SKILL.md's **Judgment pass** names, adding the Manifest's Intent as the stated pain; SKILL.md's **Judgment continuation** rule applies unchanged.

**Premise-subsumption does not apply here** — there are no fleet findings to subordinate, since the fleet is skipped in manifest mode.

It is **strictly additive** and never touches the contract:

- The contract verdict — the Outcome and every Acceptance Criterion and Global Invariant — is computed exactly as it would be without the pass. A judgment finding never changes a criterion's PASS/FAIL, never blocks, and never gates approval.
- Judgment findings are author-answerable questions with no severity, one per root as the pass returns them, posted through the same batched `comment` review and voice. They are **not** criteria, so instead of the `ac=` extension they carry the `judgment` discriminator token (`<!-- manifest-dev:review-pr judgment -->`) and are fingerprinted by finding substance like any other comment.
- The all-green approval signal stays keyed to the contract: when the Outcome and every criterion PASS, manifest mode is green **even if** the judgment pass posted questions — those are non-blocking and do not withhold the signal. Show the judgment recommendation and any reservation in the approval question and confirmed approval body as SKILL.md requires; contract green alone is not reviewer endorsement.

## Fingerprint, don't re-post

PASS/FAIL comments recur every push, so track each by a content fingerprint (criterion id + finding substance), not comment id: re-post a criterion's FAIL only when its finding changes, and prune a FAIL whose criterion now PASSes. This keeps the thread free of stale repeats. Carry the criterion id inside the SKILL.md self-marker (e.g. `<!-- manifest-dev:review-pr ac=AC-1.2 -->`) so the criterion half of the fingerprint matches exactly; the finding-substance half still reads the rendered body to decide whether the finding changed.

## Cycle summary

The SKILL.md reviewer-fleet and holistic-pass cycle-summary lines do not apply in manifest mode. Instead report, one line for the Outcome and per Acceptance Criterion and Global Invariant: its manifest id, PASS/FAIL/BLOCKED, supporting evidence, and the assessment's short finding. State the actual review context and model; shared context can be reported once for the gates it assessed. Include the judgment assessment where SKILL.md's **Cycle summary** places it. Contract acceptance and the recommendation about shipping stay distinct, including after an informed trade-off settles a thread.
