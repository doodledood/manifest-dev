---
name: review-code
description: 'Review a change along one specific quality dimension — bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, defect-class completeness after a fix, or context-file adherence. Loads exactly one dimension reference and reports findings graded by consequence; applies a caller-supplied acceptance policy when a gate verdict is requested. Use when verifying a change before merge, auditing a diff for a named concern, or running a manifest acceptance gate.'
user-invocable: true
---

# review-code — one dimension per invocation

Audit a change along **one** review dimension and report findings. Load only that dimension's reference.

## Input

`$ARGUMENTS` carries the **dimension** plus optional scope, e.g. `dimension=code-bugs` or `code-bugs src/foo.ts`. A caller requesting a gate verdict also supplies the claims to assess and any deliberately required severity, category or approval policy. A Manifest gate carries its claim and source authority; its Evidence names the dimension. If no dimension is given, list the available dimensions and ask which one — one invocation, one dimension.

## Dimensions and thresholds

Load `references/<dimension>.md` for the requested dimension and follow it. Its standards are opinionated defaults: where a rule the user stated, in the session or a context file, or a convention the project states or documents (not a pattern its code merely repeats) differs, that rule governs, a change following it raises no finding, and the report names the rule applied — except a Critical finding on the ladder below, which is still reported, naming the rule that produced it. Classify findings by consequence; the caller chooses the acceptance threshold and handling policy.

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

Roles define what to look for. **Defect-finders** report divergences, defects, contract mismatches and type holes with a stated trigger. **Advisory** dimensions assess product and quality gaps. Both use the shared severity ladder; neither role decides which findings the caller must address.

**Some dimensions are conditional**, and the caller decides whether they apply before requesting them: `contracts` where the change touches API surfaces or durable data contracts, `type-safety` on typed code, and `defect-class` where the change **fixes a defect**. `defect-class` is the one dimension that takes a defect as input rather than producing one as output — it judges the repair's protection against the demonstrated mechanism and accounts for affected sites, so on a change that fixes nothing it has no input and nothing to judge. Requesting it anyway is not an error; it reports no fix found in scope and applies any supplied acceptance policy.

## Determining scope (shared across dimensions)

For a requested follow-up, the caller supplies the prior assessed state and criteria, findings,
supported dispositions, verified repairs, and changes since that evaluation; use what applies. Criteria
that changed since that evaluation make this a fresh review, scoped as below, since work the old
criteria did not reach has never been reviewed. Otherwise report outstanding findings
and failures introduced or exposed by the intervening changes, with evidence for which prior
findings are repaired. Read context as widely as needed; an old issue on a touched line is not
new merely because the line changed. If the needed prior state is missing, recover it or report
BLOCKED with what is missing, rather than silently reviewing the complete change again. A new ID
or repeated assertion does not reopen an evidenced disposition; changed code, criteria, argument or
evidence can. Assess its support independently rather than requiring agreement with a previous reviewer.

For a fresh review — including a new standalone review when an earlier report exists — resolve its scope as follows:

1. **Caller specifies files/paths** → review exactly those.
2. **Otherwise** → review the complete change. Resolve the comparison base from the PR target or the repository's remote default branch; ask only if neither can be established. Inspect committed changes with `git diff <base>...HEAD`, staged changes with `git diff --cached`, unstaged changes with `git diff`, and relevant new files from `git ls-files --others --exclude-standard`. Read each new file's contents; a path listing alone is not its diff.
3. **Empty / non-reviewable diff** → ask the caller to clarify scope.

Stay within scope — never audit the whole project unless explicitly asked. Skip generated copies, lock files, vendored dependencies and binaries. Establish which files are generated from the repository's ownership or build rules; a directory named `dist/` or `build/` may also contain source-owned files that need review.

**Reading scope ≠ reporting scope.** The diff bounds what you *report* (defaults: only issues introduced or exposed by the change). It does not bound what you *read* — trace mechanisms wherever they lead (existing callers, shared state, upstream writers) so boundary issues between changed and unchanged code stay visible. Read widely; report narrowly. Within the resolved scope, examine every file against every category the loaded reference lists — do not cut corners or skip areas — and report only the findings that clear its bar for reporting (its actionability filter, or for defect-class its acceptance rules).

**The Pre-existing list, only when asked.** When the caller asks for it on a fresh full look, add a `## Pre-existing` section: issues the loaded dimension owns that you noticed in code you read for the change, that the change neither introduced nor exposed, and that would clear its actionability criteria other than scope: a stated trigger on a defect-finder and a stated cost for a Medium on an advisory dimension. Honor the caller's requested severities and categories; the caller decides how to handle this list. They are not findings: they never count toward the verdict or summary counts. Leave the section out unless asked, and on every follow-up even when asked: a follow-up's scope stays outstanding findings and what the intervening changes introduced or exposed.

This skill is **read-only**: never modify repository files; write only to `/tmp/` for analysis artifacts. The author implements fixes from your report.

## Severity ladder (shared)

- **Critical** — data loss, corruption, security breach, or complete failure for all users; no workaround.
- **High** — correctness, safety, a broken promise, or wrong behavior. Rarity, unusual preconditions and a workaround do not turn a substantive defect into polish.
- **Medium** — a clear product or quality gap a careful reviewer would insist on fixing before shipping; name the concrete cost.
- **Low** — polish or a nit of any kind: style, naming, structure, or otherwise.

Grade by consequence, not confidence or frequency. Dimension examples apply this ladder; they cannot lower it. Regrade a correctness or safety failure or broken binding promise received as Low from the evidence before any caller filtering. A binding requirement can concern style, naming or structure. Severity does not decide whether a finding is addressed, posted or blocking: those are caller policies, not part of the Low definition.

## Caller policy

The Manifest or another caller owns acceptance. For a claim-based gate, a finding fails it when
the evidence establishes a concrete violation of that claim or an applicable source obligation,
including a material quality cost in the artifact's supported use or expected maintenance.
Severity describes consequence; it does not substitute for that argument. A missing criterion
does not erase the requested result or its source obligations: report the coverage gap as well.
Do not turn an unsupported improvement preference into a new obligation.

A deliberately supplied severity or category policy still applies. The same Low may fail a
caller's Low-inclusive gate and pass a different caller's Medium+ gate without changing severity.
Choosing to address a Low does not raise its severity. Report classifications without a verdict
when no gate is requested. If a verdict is requested without an acceptance policy recoverable
from claims or explicit handling instructions, ask for it or report BLOCKED; do not invent a
threshold. Batching, repair scope and final finding dispositions belong to the caller. Its
reasoned rejection is not a claim amendment; evidence that the current claim is wrong calls for
amendment, while a real failure or necessary missing evidence remains unresolved.

## Report format (shared)

```
# Code Review — <dimension>

**Dimension**: <dimension>
**Acceptance policy**: [caller-supplied, for a requested gate]
**Status**: PASS | FAIL | BLOCKED [requested gates only]
**Files analyzed**: [...]

## Prior findings (follow-ups only)
- [prior finding]: repaired | rejected with support | unresolved — [evidence; new evidence that reopens it, if any]

## Findings
### Finding #1: [title]
- **Location**: `file:line`
- **Severity**: Critical | High | Medium | Low
- **Description**: [what's wrong]
- **Acceptance basis**: [the claim or source obligation contradicted, or the concrete quality cost; identify a proposed improvement as such]
- **Trigger**: [the condition under which the defect manifests — the concrete input, state, or sequence that produces the failure, or for a static mismatch such as a contract or signature divergence, the call or consumer path that reaches it — required on defect-finder dimensions]
- **Impact**: [what it breaks / why it matters — a Medium finding must name the concrete cost that earns that grade: the future change it makes harder, the reader or operator task it defeats, or the condition under which behavior degrades]
- **Recommended fix**: [specific change]

## Pre-existing (only when the caller asked, on a fresh full look)
- [title] — `file:line` — [the issue, with its trigger or cost] — [recommended fix]

## Summary
- Critical: N | High: N | Medium: N | Low: N
- Verdict (requested gates only): apply the caller's acceptance policy to the classified findings.
```

An empty report is a valid, expected outcome. Do not invent findings to fill it.

## Verifier contract (PASS / FAIL / BLOCKED)

When invoked as a gate with the caller's acceptance policy, end with one verdict:

- **PASS** — the evidence supports the assessed claims under the caller's policy, with no unresolved contradictory finding or material uncertainty.
- **FAIL** — evidence establishes a failure under that policy; name the defeated claim or explicitly required threshold. The findings are evidence for the caller to assess, not authority to add requirements.
- **BLOCKED** — necessary evidence or authority is missing (e.g., the change can't be located, a needed external doc is unreachable). Say what remains unverified and what would settle it. An empty findings list alone does not prove the claim.

## Gotchas

- **One ref only.** Load exactly the reference for the requested dimension. Loading several defeats progressive disclosure and blurs the orthogonality boundaries each dimension defines against its neighbors.
- **Classify before policy.** A Low label never discharges a correctness or safety failure or a broken binding promise. Check the consequence before applying the caller's policy.
- **Reportability is a stated trigger, not a confidence level** (defect-finders). Name the condition under which the defect manifests: "this WILL fail when X", with X written down. Where the defect is static rather than sequential — a contract or signature mismatch that is wrong on every call — the trigger is the call or consumer path that reaches it. A finding that cannot name its trigger is not reportable however strongly you suspect it — "this might be a bug", "this looks fragile", "this could break under load" all fail the test. Someone reading only the finding must be able to tell whether it clears this bar, which is what holds the bar in one place across reviewers rather than moving it with whoever is reading. A stated trigger is necessary rather than sufficient — each dimension's own bar for reporting (its actionability filter, or for defect-class its acceptance rules) still applies on top of it.
- **A Medium is a stated cost, not a strength of feeling** (all dimensions). Name the cost in the finding — the change made harder, the task defeated, the condition under which behavior degrades — specifically enough that someone reading only the finding can tell the grade is earned. A finding whose case rests on "could be cleaner", "feels off", or "not ideal" has not named one, and sits at Low. Each dimension's own calibration still applies on top.
- **Stay inside the loaded dimension.** Each reference lists what it owns and what belongs to a sibling dimension. A maintainability smell is not a bug; a type hole is not a design critique. Report only what the loaded dimension owns; let the other dimensions' invocations catch the rest.
