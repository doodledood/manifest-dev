---
name: code-review
description: 'Review a change along one specific quality dimension — bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, or CLAUDE.md adherence. Loads exactly one dimension reference and audits the diff against it, returning a structured PASS/FAIL report with severities. Use when verifying a change before merge, auditing a diff for a named concern, or running a manifest acceptance gate.'
user-invocable: true
---

# code-review — one dimension per invocation

Audit a change along **one** review dimension and report findings. This skill is the single home for the quality reviewers that used to be separate agents; each dimension's detection content lives in its own reference file and loads only when requested (progressive disclosure).

## Input

`$ARGUMENTS` carries the **dimension** plus optional scope, e.g. `dimension=code-bugs` or `code-bugs src/foo.ts`. Callers (manifest verifiers) typically spawn a general-purpose agent and activate this skill with the dimension. If no dimension is given, list the available dimensions and ask which one — never audit "everything at once"; one invocation = one dimension.

## Dimensions and thresholds

Load `references/<dimension>.md` for the requested dimension and follow it. The threshold is the bar a change must clear to PASS on that dimension:

| Dimension | Reference | Role | Threshold (PASS requires) |
|-----------|-----------|------|---------------------------|
| `change-intent` | `references/change-intent.md` | defect-finder | no LOW-or-higher findings |
| `code-bugs` | `references/code-bugs.md` | defect-finder | no LOW-or-higher findings |
| `contracts` | `references/contracts.md` | defect-finder | no LOW-or-higher findings |
| `type-safety` | `references/type-safety.md` | defect-finder | no LOW-or-higher findings |
| `operational-readiness` | `references/operational-readiness.md` | advisory | no MEDIUM-or-higher findings |
| `code-design` | `references/code-design.md` | advisory | no MEDIUM-or-higher findings |
| `code-maintainability` | `references/code-maintainability.md` | advisory | no MEDIUM-or-higher findings |
| `code-simplicity` | `references/code-simplicity.md` | advisory | no MEDIUM-or-higher findings |
| `code-testability` | `references/code-testability.md` | advisory | no MEDIUM-or-higher findings |
| `test-quality` | `references/test-quality.md` | advisory | no MEDIUM-or-higher findings |
| `docs` | `references/docs.md` | advisory | no MEDIUM-or-higher findings |
| `prose-value` | `references/prose-value.md` | advisory | no MEDIUM-or-higher findings |
| `context-file-adherence` | `references/context-file-adherence.md` | advisory | no MEDIUM-or-higher findings |

The split is structural: **defect-finders** report only certain divergences/defects/contract-mismatches/type-holes — every LOW there is real signal. **Advisory** dimensions surface taste-level improvements where LOW is usually could-be-better, not is-broken.

## Determining scope (shared across dimensions)

1. **Caller specifies files/paths** → review exactly those.
2. **Otherwise** → diff against the base branch: `git diff origin/main...HEAD && git diff`. If `origin/main` is an unknown revision, retry `origin/master`; if neither resolves and no base is given, ask for the base branch.
3. **Empty / non-reviewable diff** → ask the caller to clarify scope.

Stay within scope — never audit the whole project unless explicitly asked. Skip generated files (`*.generated.*`, `generated/`, `dist/`, `build/`), lock files, vendored deps (`vendor/`, `node_modules/`, `third_party/`), and binaries.

**Reading scope ≠ reporting scope.** The diff bounds what you *report* (defaults: only issues introduced or exposed by the change). It does not bound what you *read* — trace mechanisms wherever they lead (existing callers, shared state, upstream writers) so boundary issues between changed and unchanged code stay visible. Read widely; report narrowly.

This skill is **read-only**: never modify repository files; write only to `/tmp/` for analysis artifacts. The author implements fixes from your report.

## Severity ladder (shared)

- **Critical** — blocks release: data loss, corruption, security breach, or complete failure for all users; no workaround.
- **High** — blocks merge: core/happy-path functionality broken for common inputs.
- **Medium** — edge cases, degraded behavior, or failures needing multiple preconditions.
- **Low** — rare scenarios with workarounds, or (for advisory dimensions) taste-level could-be-better.

Each dimension's reference refines these with domain-specific calibration — defer to it.

## Report format (shared)

```
# Code Review — <dimension>

**Dimension**: <dimension>
**Threshold**: no LOW+ | no MEDIUM+
**Status**: PASS | FAIL
**Files analyzed**: [...]

## Findings
### Finding #1: [title]
- **Location**: `file:line`
- **Severity**: Critical | High | Medium | Low
- **Description**: [what's wrong]
- **Impact**: [what it breaks / why it matters]
- **Recommended fix**: [specific change]

## Summary
- Critical: N | High: N | Medium: N | Low: N
- Verdict: PASS if no finding meets/exceeds the dimension threshold, else FAIL.
```

An empty report (Status: PASS) is a valid, expected outcome. Do not invent findings to fill it.

## Verifier contract (PASS / FAIL / BLOCKED)

When invoked as a manifest acceptance gate, end with one verdict:

- **PASS** — no finding at or above the dimension's threshold.
- **FAIL** — at least one finding meets/exceeds the threshold; the findings list is the fix hint.
- **BLOCKED** — the dimension can't be evaluated yet (e.g., the change can't be located, a needed external doc is unreachable). Say what blocks it and what would unblock it.

## Gotchas

- **One ref only.** Load exactly the reference for the requested dimension. Loading several defeats progressive disclosure and blurs the orthogonality boundaries each dimension defines against its neighbors.
- **Respect the role threshold.** Reporting a LOW on an advisory dimension as if it blocks (or dropping a LOW on a defect-finder) miscalibrates the gate.
- **Certainty over suspicion** (defect-finders). "This might be a bug" is not reportable; "this WILL fail when X" is. An empty report beats false positives.
- **Don't cross dimensions.** Each reference lists what it owns and what belongs to a sibling dimension. A maintainability smell is not a bug; a type hole is not a design critique. Report only what the loaded dimension owns; let the other dimensions' invocations catch the rest.
