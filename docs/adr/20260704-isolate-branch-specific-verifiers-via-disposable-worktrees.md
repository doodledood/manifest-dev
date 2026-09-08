# ADR: Isolate branch-specific verifiers via disposable worktrees, falling back to phase separation

## Status
Accepted

## Context

The same investigation that surfaced the skill-activation gap also surfaced a race hazard in `/do`'s execution model: `/do`'s default phase is 1 for every criterion unless the manifest author sets `phase:` explicitly, and criteria within a phase launch in parallel, sharing the orchestrator's working directory (`cwd`). Diagnostic timing showed a full set of same-phase verifier sessions launching within a few seconds of each other and running concurrently for minutes against that one shared directory.

When one criterion's `verify.prompt` needs a specific branch's actual checked-out working-tree state — not just `git diff`/`git show` content inspection — running `git checkout <branch>` mid-session mutates that shared directory. A captured session doing exactly this (checking out a sequence of branches in place to run project tooling "on each branch") ran concurrently with sibling criteria that were still reading the same directory via `git diff`/`git show`, so the checkout and the reads raced against each other.

This generalizes beyond any one harness: any real manifest with a criterion whose `verify.prompt` needs an actually-checked-out branch, running in the same default phase as siblings that inspect the working tree, is exposed to the same race.

## Decision

Encode both a primary fix and a fallback as complementary Defaults, not just one:
1. **Primary — disposable worktree isolation.** When a `verify.prompt` needs a specific branch's actual checked-out state, the prompt should have the verifier isolate via `git worktree add <tmp-dir> <branch>` (removed after use) instead of `git checkout <branch>` in the shared working directory.
2. **Fallback — phase separation.** When a dedicated worktree isn't practical (e.g. tooling that must run from the repo's exact original path), the criterion gets its own `phase:` so it never runs concurrently with a sibling that also touches the shared tree.

This guidance is added to `define/tasks/CODING.md`'s Defaults section (authoring side) and cross-referenced from `do/SKILL.md` (execution side), so both the manifest author and the `/do` runtime carry the same hazard awareness.

## Alternatives Considered
- **Worktree isolation only**: Rejected per user decision — some tooling must run from the repo's exact original path (can't relocate to a temp worktree), so a worktree-only Default would leave that case unguided.
- **Phase separation only**: Rejected per user decision — always serializing branch-checkout criteria into their own phase is more conservative than necessary when a disposable worktree is practical, and forfeits the parallelism `/do`'s phase model is designed to exploit.
- **Change `/do`'s runtime to auto-detect branch-mutating verifiers and force serialization**: Rejected — `verify.prompt` is free-form natural language; reliably detecting "this prompt will checkout a branch" without executing it isn't feasible, and it would add runtime complexity for a hazard that's cheap to guide around at authoring time.

## Consequences

### Positive
- Manifest authors get concrete, actionable guidance (the exact command shape) rather than a vague "be careful about concurrency," so they can apply it without inventing worktree-cleanup mechanics from scratch.
- The guidance is symmetric across `/define` (authoring) and `/do` (execution), so an author who only reads `do/SKILL.md` still learns the hazard exists.

### Negative
- The Default doesn't retroactively fix manifests already authored without this guidance; those criteria remain exposed to the race until amended.
- Worktree isolation adds setup/teardown overhead (creating and removing a temp worktree) versus an in-place checkout, though this is bounded and disposable.

## Source
- Related: 20260704-require-explicit-skill-tool-invocation-in-verify-prompts
