# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Discovery Convergence

For a bug task, /define converges on the **mechanism**, not the **symptom**. This is the discipline that separates a manifest scoped to fix the bug from a manifest scoped to fix the *plausibility* of the bug.

**Mechanism** — A concrete execution trace naming:

- the specific variable or state that holds the wrong value,
- the location (file, line, or function) where it gets that value,
- the value it holds versus what it should,
- the sequence of events (who wrote, captured, read — in what order) that produced the discrepancy.

**Shape** — A bug-pattern name: "stale state," "race condition," "closure problem," "null deref." Shapes are starting points for exploration. They are not stopping points for the manifest.

**Mechanism identification requires code tracing, not just interview.** User interview surfaces what users see (symptoms). Mechanisms surface from reading the files along the observable's path, following the wrong value backwards through its writers and readers, and enumerating callers of shared APIs the value passes through. For bug tasks, code tracing is constitutive, not optional.

**Convergence test** — Can the interview answer, for the bug moment:

> "at line X, variable Y holds value Z because sequence M"

If the answer is a pattern name ("it's a race"), a vague region ("somewhere in the auth flow"), or a shape with no concrete values, the interview is not done. Trace further — read the code, grep for other writers, enumerate callers, follow the value backwards.

**Why this matters** — A manifest scoped from a shape-level hypothesis produces deliverables and ACs that address the *plausibility* of the bug. /do implements them faithfully. Tests pass. Deploy ships. The symptom survives — because the mechanism was never found. The feedback-cycle waste lives at /define closing on a shape, not at /do.

## Risks

- **Environment-specific** - bug only appears under certain conditions (version, OS, config, data state, timing, load); probe: reproduction conditions?
- **Incomplete fix** - works for reported case, fails edge cases
- **Shape-level hypothesis** - hypothesis names a bug pattern (race, stale state, off-by-one) without naming the specific variable, line, or value; probe: can you trace a concrete execution that produces the wrong value?
- **Unenumerated shared caller** - fix touches a callback, context, or shared-state API called elsewhere without inspecting those other callers; probe: who else calls this, and what do they assume?

## Scenario Prompts

- **Data corruption persists** - bug fixed, bad data still there; probe: need migration/cleanup?
- **Performance regression** - fix works but slower; probe: acceptable perf impact?
- **Edge case missed** - fix covers reported case, not variants; probe: other inputs, configurations, user segments, or contexts that could trigger?
- **Multiple bugs masquerading** - one symptom, multiple causes; probe: is this definitely one bug?
- **Hotfix vs proper fix** - pressure to ship fast vs fix right; probe: acceptable to patch now, fix later?
- **Pattern-match masquerading as diagnosis** - "this looks like a race condition" substitutes for tracing the actual mechanism; probe: name the specific variable, line, value, and interleaving — not the pattern.
- **Hypothesis unfalsifiable without deploy** - the only way to confirm the cause is to ship the fix and see; probe: what local check (log, test, code trace) would prove the hypothesis before deploy?
- **Shared-API composition** - a new caller is added to a callback, context, or hook also used elsewhere; probe: what do existing callers assume about call order, captured state, or closure freshness?

## Trade-offs

- Minimal patch vs proper fix
- Single bug vs batch related issues
- Speed vs investigation depth
- Hotfix vs release train

## Defaults

*Domain best practices for this task type.*

- **Establish reproduction** — Exact repro steps before attempting any fix; verify repro is complete and correct
- **Mechanism, not shape** — The hypothesis must name the specific variable, location, value, and sequence at the bug moment. "Stale state" is a shape; a mechanism is concrete. If you cannot state it concretely, keep tracing — read the code along the execution path, follow the wrong value backwards, enumerate callers of shared APIs
- **Regression check** — Identify all callers/dependents of changed code; verify no behavioral regression from the fix
- **Test correctness** — Verify existing tests assert correct behavior, not the buggy behavior
- **Systemic fix assessment** — Identify the class of bug; probe whether a pattern fix prevents recurrence
