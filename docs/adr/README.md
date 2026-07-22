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
| 2026-06-05 | [Pi-native runtime package as a source surface](20260605-pi-native-runtime-package-source-surface.md) | Superseded by [host continuation backstop ADR](20260623-use-host-continuation-as-optional-do-backstop.md) | Pi distribution |
| 2026-06-05 | [Runtime owns Harness-level Do verification trigger](20260605-runtime-owns-harness-do-verification-trigger.md) | Superseded by [host continuation backstop ADR](20260623-use-host-continuation-as-optional-do-backstop.md) | Pi runtime |
| 2026-06-06 | [figure-out provides process trust, kept distinct from define→do's artifact trust](20260606-figure-out-process-trust-vs-define-do-artifact-trust.md) | Accepted | figure-out |
| 2026-06-06 | [Harden figure-out truth-seeking via inline general-case rigor; defer the independent verification pass](20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass.md) | Accepted; deferral lifted by [evidence ledger ADR](20260611-figure-out-evidence-ledger-and-independent-rederivation.md) | figure-out |
| 2026-06-10 | [Own Pi verifier execution with JSON subprocesses](20260610-own-pi-verifier-runner.md) | Superseded by [host continuation backstop ADR](20260623-use-host-continuation-as-optional-do-backstop.md) | Pi runtime |
| 2026-06-11 | [OpenCode plugin-native distribution (retire install.sh)](20260611-opencode-plugin-native-distribution.md) | Accepted; slash UX superseded by [OpenCode slash commands use plugin wrappers](20260611-opencode-slash-commands-use-plugin-wrappers.md) | OpenCode distribution |
| 2026-06-11 | [OpenCode slash commands use plugin wrappers](20260611-opencode-slash-commands-use-plugin-wrappers.md) | Accepted | OpenCode distribution |
| 2026-06-11 | [figure-out's spine owns all epistemics; mode references thin to pure mechanics](20260611-figure-out-spine-owns-epistemics-mode-refs-thin.md) | Accepted | figure-out |
| 2026-06-11 | [figure-out reads ship an Evidence Ledger and earn their terminals; independent re-derivation un-deferred](20260611-figure-out-evidence-ledger-and-independent-rederivation.md) | Accepted | figure-out |
| 2026-06-11 | [figure-out gains DIAGNOSIS and RESEARCH probe files behind a topic-shaped trigger](20260611-figure-out-task-taxonomy-diagnosis-research-topic-trigger.md) | Accepted | Task guidance |
| 2026-06-19 | [Manifest-aware review-pr instead of a standalone GitHub verification plugin](20260619-manifest-aware-review-pr.md) | Accepted | PR review |
| 2026-06-22 | [Identify review-pr's own comments with a hidden marker, not account authorship](20260622-mark-review-pr-comments-with-hidden-marker.md) | Accepted | PR review |
| 2026-06-23 | [Use host continuation as optional `/do` backstop, not a Pi-specific verifier runtime](20260623-use-host-continuation-as-optional-do-backstop.md) | Accepted | Pi distribution |
| 2026-06-23 | [Use universal goal-setting language for unattended run backstops](20260623-use-universal-goal-setting-language.md) | Accepted | Goal setting |
| 2026-06-24 | [Use outcome-gated terminal success for `/auto` continuation](20260624-use-outcome-gated-auto-continuation.md) | Accepted | Goal setting |
| 2026-07-03 | [figure-out gains fog discipline; multi-session orchestration stays out of scope](20260703-figure-out-fog-discipline.md) | Accepted | figure-out |
| 2026-07-03 | [Progressive-disclosure triggers live in the loading layer, never in the deferred reference](20260703-progressive-disclosure-triggers-live-in-loading-layer.md) | Accepted | Prompt architecture |
| 2026-07-05 | [Keep the plugin-first repo layout; no restructure for skill-picker distribution](20260705-keep-plugin-first-layout-npx-skills-compatible.md) | Accepted | Repo layout |
| 2026-07-05 | [Front `/figure-out` as the Door; the define/do loop remains the House](20260705-front-figure-out-as-door-define-do-loop-as-house.md) | Accepted | Positioning |
| 2026-07-07 | [Split the tech-design task profile by workflow role](20260707-split-tech-design-task-profile-by-workflow-role.md) | Accepted | Task guidance |
| 2026-07-08 | [The judgment layer is a review-time premise check, distinct from define's gates](20260708-judgment-layer-is-a-review-time-premise-check.md) | Accepted | PR review |
| 2026-07-08 | [The judgment layer runs in review-pr's manifest mode, not only no-manifest mode](20260708-judgment-layer-runs-in-manifest-mode-as-a-premise-safety-net.md) | Accepted | PR review |
| 2026-07-09 | [/do keeps a default-on execution log; the manifest stays a pure contract](20260709-do-keeps-default-execution-log-manifest-stays-contract.md) | Accepted | do |
| 2026-07-09 | [Re-weight figure-out's SKILL.md by re-hosting — sectioned arc, no extraction, evidence-gated trims](20260709-figure-out-reweight-by-rehosting-not-extraction.md) | Accepted | figure-out |
| 2026-07-09 | [Gate figure-out project docs by topic relevance](20260709-gate-figure-out-project-docs-by-topic-relevance.md) | Accepted | figure-out |
| 2026-07-09 | [Mid-/do steering stays autonomous, audited through Known Assumptions](20260709-mid-do-steering-stays-autonomous.md) | Accepted | do |
| 2026-07-09 | [Process Guidance is binding but unverified](20260709-process-guidance-is-binding-but-unverified.md) | Accepted | do |
| 2026-07-14 | [figure-out roots the crux tree above solution-shaped topics](20260714-figure-out-roots-crux-tree-above-solution-shaped-topics.md) | Accepted | figure-out |
| 2026-07-14 | [figure-out challenges solution existence before descendant design](20260714-figure-out-challenge-solution-existence-before-design.md) | Accepted | figure-out |
| 2026-07-14 | [figure-out classifies stated constraints before they prune options](20260714-figure-out-classifies-constraints-before-they-prune.md) | Accepted | figure-out |
| 2026-07-14 | [figure-out keeps the do-nothing option in the option set](20260714-figure-out-keeps-do-nothing-in-the-option-set.md) | Accepted | figure-out |
| 2026-07-14 | [figure-out scales read depth with stakes and reversibility, not fog alone](20260714-figure-out-scales-read-depth-with-stakes-and-reversibility.md) | Accepted | figure-out |
| 2026-07-19 | [Taste persists by offer-and-ratify, never by silent inference](20260719-taste-persists-by-offer-and-ratify.md) | Accepted | figure-out |
| 2026-07-22 | [`/do` states verification sufficiency, not only necessity](20260722-state-verification-sufficiency-not-only-necessity.md) | Accepted | do |
| 2026-07-22 | [figure-out firms the low-cognitive-load directive to match rigor's modality](20260722-figure-out-firms-low-cognitive-load-directive.md) | Accepted | figure-out |
