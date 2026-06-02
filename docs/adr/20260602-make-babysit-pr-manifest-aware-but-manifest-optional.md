# ADR: Make babysit-pr manifest-aware but manifest-optional

## Status
Accepted

## Context

`babysit-pr` should work for existing pull requests without requiring the user to author a manifest first. At the same time, it should not blindly treat the newest CI failure or review comment as the full specification. Reviewer comments are useful signals, but they may be local, stale, disputed, out of scope, or inconsistent with the PR's actual intent.

The workflow already has strong machinery for autonomous execution: `/define` creates a Manifest, `/do` executes and verifies it, and `github-pr-lifecycle` reports PR lifecycle blockers. The design question is whether no-manifest babysitting should bypass that machinery and act directly on PR state, or synthesize enough manifest structure to keep the execution contract intact.

## Decision

`babysit-pr` always runs through manifest machinery. A user-authored manifest is optional.

When the user supplies `--manifest <path>`, that manifest is the strongest grounding source and the lifecycle run executes against it. Review comments and CI failures are interpreted against the manifest; requests that exceed or conflict with the manifest route through amendment or escalation rather than being silently implemented.

When no manifest is supplied, `babysit-pr` synthesizes an internal PR-lifecycle manifest from **PR Grounding**: the ordered evidence available from the pull request. The grounding hierarchy is:

1. Explicit user-supplied Manifest.
2. PR-linked or confidently discovered Manifest.
3. PR title and description.
4. Commit messages and current diff.
5. PR comments and review threads.

The synthesized manifest gives `/do` an execution contract while still preserving zero-setup PR babysitting. The PR description is especially important when no manifest exists; if it is stale or too thin to resolve a substantive code decision, that ambiguity lowers autonomy.

Comments are signals, not authority. `babysit-pr` reconciles comments against stronger intent sources before deciding whether a blocker is in scope to fix.

## Alternatives Considered

- **Require a manifest for babysitting**: rejected because PR babysitting should work on existing PRs with no manifest-dev setup. Forcing manifest authoring would make the tool too heavy for the common "watch this PR and get it green" use case.
- **Run directly from PR state without a manifest**: rejected because it bypasses `/do`'s execution and verification contract and makes the workflow too reactive to the latest comment or CI failure.
- **Treat comments as the specification when no manifest exists**: rejected because comments can be stale, local, contradictory, or outside the PR's intended scope. They should influence the run, not define it by recency.
- **Fuzzy-discover manifests from repository files by default**: rejected as a default because accidentally selecting the wrong manifest is worse than synthesizing from PR state. Discovery is allowed only when the PR metadata or repository convention makes the match high-confidence.

## Consequences

### Positive

- Existing PRs remain zero-setup: `/babysit-pr [url]` can run without a user-authored manifest.
- `/do` remains the execution engine, preserving verifier loops, amendment semantics, and escalation behavior.
- Reviewer comments are grounded against PR intent instead of becoming drive-by specs.
- CI babysitting can auto-fix trusted writable PRs while retaining an intent boundary for substantive changes.

### Negative

- No-manifest runs depend on the quality of PR descriptions and commit history; thin PR metadata lowers autonomy for code changes.
- Synthesized lifecycle manifests may need amendment when new comments reveal missing or changed intent.
- High-confidence manifest discovery requires conservative heuristics; otherwise the workflow must fall back to PR-grounded synthesis.

## Source

- Session: `/figure-out --with-docs` session on 2026-06-02.
- Related: `20260602-coordinate-review-pr-and-babysit-pr-through-pr-state`
