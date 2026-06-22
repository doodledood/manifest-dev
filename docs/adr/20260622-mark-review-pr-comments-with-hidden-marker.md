# ADR: Identify review-pr's own comments with a hidden marker, not account authorship

## Status
Accepted

## Context
`review-pr` posts its comments **under the operator's own GitHub account** (`skills/review-pr/SKILL.md`) — the same account a human reviewer uses to comment manually. The skill identifies its own prior work purely by authorship: it advances "every unresolved thread we authored or replied to" and resolves from "our prior GitHub reviews/comments/replies" (`skills/review-pr/SKILL.md`). On a shared account, authorship cannot separate the skill's automated output from the human's manual comments.

The concrete failure: a human leaves a manual review comment under the shared reviewer account; on the next one-shot pass, `review-pr`'s "advance our existing threads" step scoops that human comment into its per-comment verifier loop and may auto-reply or resolve a thread the human meant to own.

A related-but-different mechanism already exists: manifest mode tracks its PASS/FAIL comments by a *content* fingerprint (criterion id + finding substance) to avoid re-posting across pushes (`skills/review-pr/references/MANIFEST_MODE.md`). That is content-derived deduplication, not an authorship marker, and it does not tell automated comments apart from human ones.

GitHub strips HTML comments (`<!-- … -->`) from rendered markdown but returns them in raw comment bodies via the API — the established mechanism bots (dependabot, CodeRabbit, GitHub Actions) use to recognize their own comments.

## Decision
Stamp a **hidden HTML-comment marker** on every comment `review-pr` posts, and make **marker presence — not account authorship — the definition of "an automated review-pr comment."**

- **Behavioral gate.** `review-pr`'s "advance our existing threads" step keys on the marker. Unmarked comments on the shared account read as *human* and are left out of the verifier loop.
- **Content.** A constant namespaced identity tag on every posted surface. In **manifest mode** the marker additionally carries the criterion id (already in hand), making the existing `MANIFEST_MODE.md` content-fingerprint criterion match exact. No-manifest findings carry the tag only — no stable per-finding id exists, and the holistic pass already dedups them.
- **Surfaces.** Every body `review-pr` posts, uniformly: new findings, thread replies, summary header, approval body, and manifest PASS/FAIL. One rule, no carve-out.
- **Consumer scope.** `review-pr` is the writer and primary reader. The token is documented as a **shared convention** — spelled canonically once and referenced, not independently restated. `check-pr` gets one awareness line at its existing recurring-bot-comment tracking spot (`skills/check-pr/SKILL.md`), so its content-fingerprint handling can use the marker as an exact signal for `review-pr`'s comments. `babysit-pr` is unchanged: it delegates lifecycle inspection to `/do → check-pr` and grounds comments by intent strength, not bot-vs-human identity.

The marker does **not** replace the content fingerprint: "re-post only when the finding changed" still compares body substance. The marker makes only the *criterion-identification* half exact.

## Alternatives Considered
- **Cosmetic tag (no behavior change)**: stamp the marker but keep account-authorship as the "ours" gate — Rejected. The marker would do nothing; the human-comment-scooping failure persists. The marker only earns its place by becoming the identity boundary.
- **Producer-only, undocumented**: `review-pr` writes and reads the marker as a private internal — Rejected. The moment a second skill (`check-pr`) reads it, it is a cross-tool contract; an undocumented token re-spelled per file drifts. Documenting it once as a convention is the honest cost.
- **Full propagation to `babysit-pr` and `/do`**: make every author-side consumer marker-aware — Rejected as redundant. `check-pr` is the inspection consumer, and the existing content fingerprint already keeps `/do`/`babysit-pr` ingestion loop-safe (`MANIFEST_MODE.md`). Adding marker logic to `babysit-pr`'s top-level prose closes no gap its grounding rules leave open.
- **Per-finding hash in no-manifest mode**: give no-manifest findings a synthetic stable id in the marker — Rejected. Findings have no durable id (anchors and wording shift run to run), and the holistic pass already prunes duplicates against existing PR comments. A new hashing mechanism would add machinery for no current need.

## Consequences

### Positive
- `review-pr` stops re-processing human comments on a shared reviewer account — the stated failure is closed at its root (identity), not patched per-surface.
- Manifest-mode criterion identification becomes exact rather than fuzzy, hardening the existing fingerprint dedup at near-zero cost (the criterion id is already known).
- One uniform rule ("every body `review-pr` posts gets the tag") — nothing for the skill to remember about which surfaces qualify.
- The token is a documented shared convention, so cross-tool readers (`check-pr`) cite one canonical spelling.

### Negative
- Legacy *unmarked* automated comments posted before this change now read as human, so `review-pr` stops advancing its own old threads. Safe-fail direction (it under-acts on its own history rather than over-acts on humans') and self-heals as new marked comments are posted.
- `review-pr`'s "ours" detection gains a marker dependency; the convention must stay in sync across `review-pr` and `check-pr`.
- The whole mechanism is moot if `review-pr` is never run on accounts shared with human reviewers — but the premise is that it is.

## Source
- Session: `/figure-out --with-docs --log` on marking `review-pr`'s own comments to identify automated vs human comments on a shared account (2026-06-22).
- Governs behavior of the `review-pr` and `check-pr` skills.
- Related: 20260619-manifest-aware-review-pr
