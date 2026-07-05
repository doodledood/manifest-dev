# ADR: Isolate branch-specific verifiers via disposable worktrees, falling back to phase separation

## Status
Accepted

## Context

The same cache-staggering experiment (`tests/cache-experiment/run_arms.py`, postgres-provider-split manifest fixture, arm0/repeat-0) that surfaced the skill-activation gap also surfaced a race hazard: `/do`'s default phase is 1 for every criterion unless the manifest author sets `phase:` explicitly, and criteria within a phase launch in parallel sharing the orchestrator's `cwd`. When one criterion's `verify.prompt` needs a specific branch's actual checked-out working-tree state — not just `git diff`/`git show` content inspection — running `git checkout <branch>` mid-session mutates that shared directory while sibling criteria concurrently read it.

**Excerpt B-1 — concurrent launch timing** (`arm0/35697d565ed/repeat-0/312cf7d63c768be9/diagnostics/*.json`, response `Date` headers), showing all 12 criteria of one repeat launching within a 3-second window and running concurrently against one shared git worktree:
```
INV-G2   start=18:59:51 end=19:01:26 calls=16
AC-2.3   start=18:59:51 end=18:59:54 calls=2
AC-1.1   start=18:59:51 end=19:00:05 calls=5
INV-G1   start=18:59:51 end=19:00:53 calls=14
AC-3.1   start=18:59:52 end=19:03:34 calls=40
```

**Excerpt B-2 — mid-session branch checkouts inside the shared worktree** (`arm0/35697d565ed/repeat-0/312cf7d63c768be9/`, session `8c7e3f23-18f1-48a7-89f3-020d6c6b09b0`, criterion AC-3.1 — "On each branch run `prek run --from-ref upstream/main --stage pre-commit`"), while INV-G1/INV-G2 above are still concurrently running `git diff`/`git show` against the same `cwd`:
```
git checkout 2606/postgres-provider-psycopg3-default -q && git log --oneline -1
git checkout 3ec0d9d0ab -q && git log --oneline -1
...
git status --short && git checkout 46936f93139 -q && git log --oneline -1
```

This generalizes beyond the experiment's own harness: any real manifest with a criterion whose `verify.prompt` needs an actually-checked-out branch, running in the same default phase as siblings that inspect the working tree, is exposed to the same race.

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
- Manifest: `manifest-20260704-163919.md`
- Related: 20260704-require-explicit-skill-tool-invocation-in-verify-prompts
