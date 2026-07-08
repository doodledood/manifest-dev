# ADR: The judgment layer runs in review-pr's manifest mode, not only no-manifest mode

## Status
Accepted

## Context

review-pr operates in two modes. No-manifest mode runs the generic reviewer fleet plus the judgment layer. Manifest mode independently verifies a manifest's acceptance contract against the PR head and skips the generic fleet. The judgment layer asks whether a change earns its keep against the pain it solves.

In manifest mode the premise was, in principle, already settled at `/define` time — which invites the assumption that premise-questioning should be switched off there. That assumption is what this decision examines: does a manifest exempt a PR from premise review, or is a manifest-driven PR exactly the one that needs it?

## Decision

The judgment layer runs in **both** review-pr modes, including manifest mode.

A manifest can lock in a flawed premise. Premise errors — an unnecessary change, a misstated pain, an over-built approach — originate in figure-out/define but only become visible against the concrete artifact. A manifest-driven PR is therefore the case that most needs an independent premise look, not the case to exempt: the manifest is the very thing that could carry the mistake forward unquestioned.

Running it there is safe because the judgment layer is non-blocking (see `20260708-judgment-layer-is-a-review-time-premise-check`). It stacks alongside manifest-mode contract verification and never alters the contract's PASS/FAIL verdict: the acceptance gates are computed exactly as before, and the judgment findings are additive, author-facing questions. Only the attach point differs by mode — the holistic pass in no-manifest mode, an additive step in the manifest-mode path.

## Alternatives Considered

- **Restrict the judgment layer to no-manifest mode**: exempt manifest-driven PRs on the grounds that `/define` already settled the premise — Rejected: this exempts precisely the PRs most able to carry a flawed premise forward, and because the layer is non-blocking there is no contract-verification cost to including it.
- **Let manifest-mode judgment findings affect the contract verdict**: Rejected: premise questions are non-binding by nature (see the related ADR); allowing them to influence a binding gate would halt manifest verification on a human judgment call.

## Consequences

### Positive
- A manifest-driven PR gets an independent premise check, catching define-session misses at the concrete artifact — the flow that most needs the safety net.
- Manifest-mode contract verification is unchanged; the judgment layer is purely additive.

### Negative
- Manifest mode wires one additional step (a small surface increase in the manifest-mode path). If it ever proves noisy despite the evidence-gate, restricting it to no-manifest mode is a one-line scope change.

## Source
- Related: See also 20260708-judgment-layer-is-a-review-time-premise-check
