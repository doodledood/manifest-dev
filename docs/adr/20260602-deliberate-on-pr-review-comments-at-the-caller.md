# ADR: Deliberate on PR review comments at the caller, with confident autonomous push-back

## Status
Accepted

## Context

When `/do` tends a PR under PR-lifecycle work (regular `/define`→`/do` on a `github.com` origin, or `babysit-pr`), it acts on findings the `github-pr-lifecycle` agent surfaces — including open review threads. Observed failure: scope explodes from comments. The caller treats a reviewer's (or a bot's) comment as work to satisfy and implements it to make the thread go away, even when the comment is wrong, off-intent, or implies a far larger change than the PR set out to make.

Two structural facts constrain where the fix can live:

1. **The `github-pr-lifecycle` agent is deliberately substance-blind.** It reports PR state and emits a `reply <thread-id>` directive with action-ready context; it never classifies a comment as valid, invalid, false-positive, or pushback-worthy. That blindness is load-bearing — it is what lets `review-pr` (reviewer side) and `babysit-pr` (author side) run on the same PR without the inspection agent taking sides. So comment judgment cannot live in the agent.

2. **The caller's framing biases toward compliance.** `/do` is written with completion pressure — "fix in-scope blockers when it can," "iterate until they pass," with exits only at "pass" or "unrecoverable." There was no foothold for restraint, so blind compliance was the path of least resistance.

The repo already had the *direction* axis for findings (`/do`: reviewer ask beyond intent → amend; terminal → escalate) and the doctrine that "comments are signals, not authority" (PR_LIFECYCLE Defaults, babysit-pr grounding). What was missing was a *validity* axis (is the comment correct?) and a *proportionality* axis (is addressing it in scale with this PR's intent?).

## Decision

Comment judgment lives in the **caller** (`/do`'s finding-handling), not the agent, and it is a **deliberation rule**, not a mode-gated scope matrix.

When acting on **external review input** surfaced as a finding (review comments, bot nits — *not* the manifest's own Acceptance Criteria, which remain authority), `/do` weighs each comment on three axes before acting:

- **Validity** — is it correct?
- **Relevance to this PR's intent** — does addressing it serve what this PR set out to do?
- **Proportionality** — is the change in scale with that intent? (A valid point that requires work beyond the PR's intent is *not* relevant to *this* PR; it belongs in separate work.)

Two outcomes: **adopt** the comments that clear the bar; **push back with reasoning** (a reply, no code change) on the ones that don't — a false positive, or a valid-but-separate-scope ask — rather than implementing to silence the thread.

No size thresholds and no per-mode decision tree. The model judges; the prompt's only job is to name the axes (so "think harder" is not empty) and to legitimize push-back (so completion pressure no longer forces compliance). Proportionality is folded into relevance, so a valid-but-PR-exploding ask is a reasoned push-back, not a blind amend.

**Autonomous push-back is permitted, including against human reviewers, when the caller is confident** (clear false positive, clearly-separate scope), with a respectful reply that leaves human-authored threads open. Where confidence is low — a borderline-valid point or a substantive design objection — the caller surfaces it (interactive) or replies non-committally and leaves it for a human (autonomous), rather than bulldozing a reviewer under the operator's account.

This bet on autonomous judgment is acceptable because `/do` drives to **mergeable, never merged**: every autonomous scope or push-back decision still faces human review at merge time, which bounds the blast radius of a misjudgment.

The rule lands in `/do`'s generic finding-handling, so both regular `/do` and `babysit-pr` inherit it (both route findings through `/do`); the existing babysit-pr and PR_LIFECYCLE "signals, not authority" lines become consistent echoes rather than separate restatements.

## Alternatives Considered

- **Make the `github-pr-lifecycle` agent classify comments (false-positive / pushback-worthy)**: rejected — it breaks the agent's substance-blindness, which is what lets `review-pr` and `babysit-pr` coexist on one PR. A content-neutral "apply judgment here" nudge in the agent's findings was also rejected: it leaks workflow-shaping into a deliberately workflow-neutral agent and becomes habituated boilerplate, and the behavior it targets executes in the caller anyway.
- **Mode-gated scope matrix (autonomous → defer, interactive → amend/escalate)**: rejected — it substitutes a mechanical gate for the judgment that is actually the point, and the obvious mapping was inverted: autonomous "amend" means `/define --autonomous` self-approves scope growth with no human gate, which *reproduces* the scope explosion it was meant to prevent.
- **Blanket "autonomous always defers, never absorbs"**: rejected — too blunt; it suppresses the genuinely-relevant fixes the caller *should* adopt autonomously, and the user explicitly wanted per-comment judgment, not a blanket policy.
- **Size/line-count threshold for "too big"**: rejected — brittle and game-able; reframed "too big" as a *type* question (fix to existing intent vs. new piece of work), which the model can judge reliably where a metric cannot.

## Consequences

### Positive

- Scope explosion from comments is addressed at its real source — the caller's compliance framing — without touching the inspection agent.
- The agent stays substance-blind, preserving `review-pr` / `babysit-pr` coexistence.
- One rule in generic `/do` covers both regular and babysit flows; no per-flow duplication to maintain.
- Push-back is legitimized, so false positives and out-of-scope asks get a reasoned reply instead of unwanted code.
- The judgment-not-thresholds approach keeps the prompt minimal and trusts model capability where it is strong.

### Negative

- Autonomous `/do` self-judges scope and may, when confident-but-wrong, adopt a large ask or push back on a correct human reviewer. The mitigation is structural (mergeable-not-merged → human review at merge) rather than a hard gate, accepted as the cost of full autonomy.
- "Confident vs. low-confidence" is itself a model judgment with no crisp boundary; calibration depends on the model.
- Existing "comments are signals, not authority" lines in babysit-pr and PR_LIFECYCLE now overlap with the richer `/do` rule and should be kept as thin echoes, not allowed to drift into competing restatements.

## Source

- Related: `20260602-make-babysit-pr-manifest-aware-but-manifest-optional`
- Related: `20260602-coordinate-review-pr-and-babysit-pr-through-pr-state`
