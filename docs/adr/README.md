# Architecture Decision Records

Accepted design decisions for manifest-dev. ADRs are append-only records of why a direction was chosen; current implementation state may lag an ADR when the ADR describes a staged rollout.

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-05-18 | [github-pr-lifecycle FAIL findings — workflow-neutral, vocabulary or prose](20260518-verifier-fail-hints-are-directives.md) | Accepted | Verifier reporting |
| 2026-05-18 | [Walk-PR depth becomes boundary-first, diff as evidence](20260518-walk-pr-boundary-first-canvas-depth.md) | Accepted | PR review UX |
| 2026-05-31 | [Codex plugin-native distribution (retire installer.sh)](20260531-codex-plugin-native-distribution.md) | Accepted | Codex distribution |
| 2026-06-02 | [Coordinate review-pr and babysit-pr through PR state](20260602-coordinate-review-pr-and-babysit-pr-through-pr-state.md) | Accepted | PR lifecycle |
| 2026-06-02 | [Deliberate on PR review comments at the caller, with confident autonomous push-back](20260602-deliberate-on-pr-review-comments-at-the-caller.md) | Accepted | PR review |
| 2026-06-02 | [Make babysit-pr manifest-aware but manifest-optional](20260602-make-babysit-pr-manifest-aware-but-manifest-optional.md) | Accepted | PR lifecycle |
| 2026-06-02 | [Use CI one-shot cadence for babysit-pr](20260602-use-ci-one-shot-cadence-for-babysit-pr.md) | Accepted | PR lifecycle |
| 2026-06-04 | [figure-out owns domain probing via mirrored probe task files](20260604-figure-out-owns-domain-probing-via-mirrored-task-files.md) | Accepted | Task guidance |
| 2026-06-05 | [Pi-native runtime package as a source surface](20260605-pi-native-runtime-package-source-surface.md) | Accepted | Pi distribution |
| 2026-06-05 | [Runtime owns Harness-level Do verification trigger](20260605-runtime-owns-harness-do-verification-trigger.md) | Accepted | Pi runtime |
| 2026-06-06 | [figure-out provides process trust, kept distinct from define→do's artifact trust](20260606-figure-out-process-trust-vs-define-do-artifact-trust.md) | Accepted | figure-out |
| 2026-06-06 | [Harden figure-out truth-seeking via inline general-case rigor; defer the independent verification pass](20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass.md) | Accepted | figure-out |
| 2026-06-10 | [Own Pi verifier execution with JSON subprocesses](20260610-own-pi-verifier-runner.md) | Accepted | Pi runtime |
