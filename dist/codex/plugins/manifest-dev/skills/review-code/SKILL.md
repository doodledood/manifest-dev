---
name: review-code
description: 'Review a change along one specific quality dimension — bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, defect-class completeness after a fix, or context-file adherence. Loads exactly one dimension reference and audits the diff against it, returning a structured PASS/FAIL report with severities. Use when verifying a change before merge, auditing a diff for a named concern, or running a manifest acceptance gate.'
user-invocable: true
---

# review-code — one dimension per invocation

Audit a change along **one** review dimension and report findings. Load only that dimension's reference.

## Input

`$ARGUMENTS` carries the **dimension** plus optional scope, e.g. `dimension=code-bugs` or `code-bugs src/foo.ts`. A manifest gate's body activates this skill with the dimension under `/do`'s selected evaluator; the gate names the dimension and this skill owns the threshold. If no dimension is given, list the available dimensions and ask which one — one invocation, one dimension.

## Dimensions and thresholds

Load `references/<dimension>.md` for the requested dimension and follow it. Its standards are opinionated defaults: where a rule the user stated, in the session or a context file, or a convention the project states or documents (not a pattern its code merely repeats) differs, that rule governs, a change following it raises no finding, and the report names the rule applied — except a Critical finding on the ladder below, which is still reported, naming the rule that produced it. Every dimension uses the same threshold: no Medium-or-higher findings to PASS.

| Dimension | Reference | Role |
|-----------|-----------|------|
| `change-intent` | `references/change-intent.md` | defect-finder |
| `code-bugs` | `references/code-bugs.md` | defect-finder |
| `contracts` | `references/contracts.md` | defect-finder |
| `type-safety` | `references/type-safety.md` | defect-finder |
| `defect-class` | `references/defect-class.md` | defect-finder |
| `operational-readiness` | `references/operational-readiness.md` | advisory |
| `code-design` | `references/code-design.md` | advisory |
| `code-maintainability` | `references/code-maintainability.md` | advisory |
| `code-simplicity` | `references/code-simplicity.md` | advisory |
| `code-testability` | `references/code-testability.md` | advisory |
| `test-quality` | `references/test-quality.md` | advisory |
| `docs` | `references/docs.md` | advisory |
| `prose-value` | `references/prose-value.md` | advisory |
| `context-file-adherence` | `references/context-file-adherence.md` | advisory |

Roles define what to look for, not different severity bars. **Defect-finders** report divergences, defects, contract mismatches and type holes with a stated trigger. **Advisory** dimensions assess product and quality gaps. Both use the shared severity ladder and threshold below.

**Some dimensions are conditional**, and the caller decides whether they apply before requesting them: `contracts` where the change touches API surfaces or durable data contracts, `type-safety` on typed code, and `defect-class` where the change **fixes a defect**. `defect-class` is the one dimension that takes a defect as input rather than producing one as output — it judges the repair's protection against the demonstrated mechanism and accounts for affected sites, so on a change that fixes nothing it has no input and nothing to judge. Requesting it anyway is not an error; it reports PASS and says no fix was found in scope.

## Determining scope (shared across dimensions)

For a requested follow-up, the caller supplies the prior assessed state and criteria, findings,
verified repairs, and changes since that evaluation; use what applies. Report outstanding findings
and failures introduced or exposed by the intervening changes, with evidence for which prior
findings are repaired. Read context as widely as needed; an old issue on a touched line is not
new merely because the line changed. If the needed prior state is missing, recover it or report
BLOCKED with what is missing, rather than silently reviewing the complete change again.

For a fresh review — including a new standalone review when an earlier report exists — resolve its scope as follows:

1. **Caller specifies files/paths** → review exactly those.
2. **Otherwise** → review the complete change. Resolve the comparison base from the PR target or the repository's remote default branch; ask only if neither can be established. Inspect committed changes with `git diff <base>...HEAD`, staged changes with `git diff --cached`, unstaged changes with `git diff`, and relevant new files from `git ls-files --others --exclude-standard`. Read each new file's contents; a path listing alone is not its diff.
3. **Empty / non-reviewable diff** → ask the caller to clarify scope.

Stay within scope — never audit the whole project unless explicitly asked. Skip generated files (`*.generated.*`, `generated/`, `dist/`, `build/`), lock files, vendored deps (`vendor/`, `node_modules/`, `third_party/`), and binaries.

**Reading scope ≠ reporting scope.** The diff bounds what you *report* (defaults: only issues introduced or exposed by the change). It does not bound what you *read* — trace mechanisms wherever they lead (existing callers, shared state, upstream writers) so boundary issues between changed and unchanged code stay visible. Read widely; report narrowly. Within the resolved scope, examine every file against every category the loaded reference lists — do not cut corners or skip areas — and report only the findings that clear its bar for reporting (its actionability filter, or for defect-class its acceptance rules).

**The Pre-existing list, only when asked.** When the caller asks for it on a fresh full look, add a `## Pre-existing` section: issues the loaded dimension owns that you noticed in code you read for the change, that the change neither introduced nor exposed, and that would clear the dimension's bar for reporting if the change had introduced them — its actionability criteria other than being in scope: a stated trigger on a defect-finder, a stated cost for a Medium on an advisory dimension, and no advisory Lows. The caller fixes them on its pull request. They are not findings: they never count toward the verdict or the summary counts. Leave the section out unless asked, and on every follow-up even when asked: a follow-up's scope stays outstanding findings and what the intervening changes introduced or exposed.

This skill is **read-only**: never modify repository files; write only to `/tmp/` for analysis artifacts. The author implements fixes from your report.

## Severity ladder (shared)

- **Critical** — blocks release: data loss, corruption, security breach, or complete failure for all users; no workaround.
- **High** — correctness, safety, a broken promise, or wrong behavior. Rarity, unusual preconditions and a workaround do not turn a substantive defect into polish.
- **Medium** — a clear product or quality gap a careful reviewer would insist on fixing before shipping; name the concrete cost.
- **Low** — presentation, polish or taste that does not change the underlying promise.

Grade by consequence, not confidence or frequency. Dimension examples apply this ladder; they cannot lower it. All Critical, High and Medium findings block. A correctness or safety finding received as Low still blocks: correct its grade from the evidence rather than filtering it out. Presentation-only Lows are below-bar; the caller batches useful fixes from the first review and leaves new such nits on repair reviews. An explicit binding requirement still holds, including one about presentation.

## Report format (shared)

```
# Code Review — <dimension>

**Dimension**: <dimension>
**Threshold**: no MEDIUM+
**Status**: PASS | FAIL
**Files analyzed**: [...]

## Prior findings (follow-ups only)
- [prior finding]: repaired | unresolved — [evidence]

## Findings
### Finding #1: [title]
- **Location**: `file:line`
- **Severity**: Critical | High | Medium | Low
- **Description**: [what's wrong]
- **Trigger**: [the condition under which the defect manifests — the concrete input, state, or sequence that produces the failure, or for a static mismatch such as a contract or signature divergence, the call or consumer path that reaches it — required on defect-finder dimensions]
- **Impact**: [what it breaks / why it matters — a Medium finding must name the concrete cost that earns that grade: the future change it makes harder, the reader or operator task it defeats, or the condition under which behavior degrades]
- **Recommended fix**: [specific change]

## Pre-existing (only when the caller asked, on a fresh full look)
- [title] — `file:line` — [the issue, with its trigger or cost] — [recommended fix]

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
- **Apply the shared threshold.** A Low label never discharges a correctness or safety failure. Check the consequence before applying the threshold.
- **Reportability is a stated trigger, not a confidence level** (defect-finders). Name the condition under which the defect manifests: "this WILL fail when X", with X written down. Where the defect is static rather than sequential — a contract or signature mismatch that is wrong on every call — the trigger is the call or consumer path that reaches it. A finding that cannot name its trigger is not reportable however strongly you suspect it — "this might be a bug", "this looks fragile", "this could break under load" all fail the test. Someone reading only the finding must be able to tell whether it clears this bar, which is what holds the bar in one place across reviewers rather than moving it with whoever is reading. A stated trigger is necessary rather than sufficient — each dimension's own bar for reporting (its actionability filter, or for defect-class its acceptance rules) still applies on top of it.
- **A Medium is a stated cost, not a strength of feeling** (all dimensions). Medium is a blocking grade, so it carries the same auditability the defect-finders get from a stated trigger: name the cost in the finding — the change made harder, the task defeated, the condition under which behavior degrades — specifically enough that someone reading only the finding can tell the grade is earned. A finding whose case rests on "could be cleaner", "feels off", or "not ideal" has not named one, and sits at Low. Each dimension's own calibration still applies on top.
- **Stay inside the loaded dimension.** Each reference lists what it owns and what belongs to a sibling dimension. A maintainability smell is not a bug; a type hole is not a design critique. Report only what the loaded dimension owns; let the other dimensions' invocations catch the rest.
