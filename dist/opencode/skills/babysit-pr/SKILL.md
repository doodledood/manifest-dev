---
name: babysit-pr
description: 'Thin PR babysitting wrapper for manifest-dev. Use when the user wants to tend an existing GitHub PR through CI, review threads, description sync, and mergeability, or asks to babysit a PR with or without an existing manifest.'
argument-hint: '<pr-url> | --manifest <path>'
user-invocable: true
---

Babysit an existing PR by delegating to the manifest workflow. Do not implement lifecycle logic here.

**Inputs.** Accept either a PR URL or `--manifest <path>`. A manifest path means lifecycle intent already exists; skip synthesis. A PR URL means invoke `manifest-dev:define` with `--babysit <pr-url> --autonomous`, read its `Manifest complete:` path, then continue. Both `--manifest` and PR URL together → halt: pick one.

**Execution.** After resolving the manifest path, tell the operator the recommended unattended command:

```text
/goal /do <manifest-path>
```

Print the command exactly. `/goal` is the operator's turn-continuation wrapper; `/do` owns the contract: it reads the manifest, runs the `github-pr-lifecycle` verifier, handles wait/retrigger/reply/sync findings, and stops via `/done` or `/escalate`. This skill is only the entrypoint.

**Boundary.** Never press merge, never force-push, and never push to a base branch. The target is mergeable, not merged.

**Failure handling.** If `manifest-dev:define` is unavailable, returns no manifest path, or rejects the PR URL, stop and surface the reason. If the user supplied `--manifest`, do not inspect or rewrite it before handing it to `/do`.
