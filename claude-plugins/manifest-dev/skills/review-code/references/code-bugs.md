# Code-bugs review

Audit the change for mechanical defects — runtime failures, resource issues, and structural code flaws — detectable from code patterns rather than intent-behavior analysis.

## Reasoning discipline

Two reasoning modes are required, both applied to every review:

- **Pattern-matching** — walks the categories below, flagging code whose shape matches a known defect pattern (race, leak, unhandled rejection, dangerous default). Fast. Catches bugs visible in isolated snippets.
- **Mechanism tracing** — follows specific values through specific code paths. For every value the diff writes or reads, ask: who else writes it, who else reads it, what does each closure capture vs. re-read, and what sequence of calls or captures could produce a wrong value? For every new caller of an existing function, hook, context, or callback, enumerate the existing callers and compare assumptions about call order, captured state, and freshness. Catches composition bugs that pattern-matching cannot see — because the bug lives in the *interaction* between changed and unchanged code, not in either snippet alone.

A finding from either mode passes through the same Actionability Filter below.

## State machines

<!-- One statement of the method, used by review and by the audit-state-machines skill; see docs/adr/20261107-review-checks-the-whole-state-machine-a-change-touches.md. -->

A state machine is a value whose changes follow a lifecycle: a set of states and the events that move it between them. It is **explicit** when the code names it — a status type with a transition table, or one function that owns every change. It is **implicit** when nothing does — a status set by branches in several files, or flags whose combinations act as states (`loading` and `failed` both true). Its bugs live between its sites: each site looks correct alone.

When the scope writes a state machine, or reads one to decide what happens next:

1. **Rebuild the whole machine**, not only the part in scope: every state, every event that moves it, and every site that writes it, by file and line, across the repository, including code the scope does not touch. For an implicit machine, the states are the value combinations its writers can produce. The rules it must keep come from the code's own guards, its documents, and what its readers assume.
2. **Check every state against every event, as deep as the risk warrants.** Enumerate inline for a small machine with one writer; walk every reachable state with a script outside the project for a larger one; use a model checker (TLA+ or Alloy, for example) where several writers can interleave. Look for a bad state that can be reached, a transition the rules forbid, a state with no way out, a combination that means nothing, and two writers whose interleaving loses a change. Where the scope only displays a state, checking that the displayed states exist is enough.
3. **Confirm every counterexample on the real code** before it counts: trace its sequence through the actual sites, or run it. The model is your translation of the code and can be wrong; a counterexample the code does not reproduce is dropped. The confirmed sequence is the finding's trigger.
4. **A model that finds nothing proves nothing.** Say what it covered — its states, events and writers — never that the machine is correct.

A machine can also be written as instructions that runs, agents or people follow — a prompt, a skill, a runbook that says who sets a status or a claim, and when. Check it the same way. Its sites are the rules, by file and line, and its writers are the runs that follow them. A counterexample counts once you quote the rule that allows each step of its sequence, and nothing in the text forbids that step.

In a review of a change, the Actionability Filter's *In scope* applies: a bug the change introduced or exposed is in scope, including one now reachable only through writers the change did not touch. Report it with Category `State machine`. A transition the author meant differently, with no mechanical defect, belongs to the change-intent dimension; a missing discriminant in a type belongs to the type-safety dimension.

## Bug detection categories

Walk the categories as failure-mode lenses, not as a checklist — a finding in one category does not stop analysis of others, and a bug that fits this dimension but matches no listed category is still reportable. Respect the Out of Scope boundaries to maintain orthogonality. For large diffs, batch related files (same directory, same module) to manage analysis context.

The items listed under each category are examples of the pattern, not a closed set. If a defect matches the category's spirit but isn't bulleted, it still counts. Thoroughness in looking; discipline in reporting — the Actionability Filter decides what ships to the report.

**Category 1 — Race Conditions & Concurrency**
- Async state changes without proper synchronization
- Concurrent access to shared mutable state
- Time-of-check to time-of-use (TOCTOU) vulnerabilities
- Deadlocks, livelocks

*Report requires naming the specific writers and readers and the interleaving or sequence that produces the wrong value — not just "race condition possible."*

**Category 2 — Data Loss**
- Operations during state transitions that may fail silently
- Missing persistence of critical state changes
- Overwrites without proper merging
- Incomplete transaction handling

**Category 3 — Edge Cases**
- Empty arrays, null, undefined handling
- Type coercion issues and mismatches
- Boundary conditions (zero, negative, max values)
- Unicode, special characters, empty strings

**Category 4 — Error Handling** (focus on RUNTIME FAILURES)
- Unhandled promise rejections that crash the app
- Swallowed exceptions that hide errors users should see
- Missing try-catch on operations that will throw
- Generic catch blocks hiding specific errors

Note: Inconsistent error handling PATTERNS belong to the code-maintainability dimension.

**Category 5 — State Inconsistencies**
- Context vs storage synchronization gaps
- Stale cache serving outdated data
- Orphaned references after deletions
- Partial updates leaving inconsistent state

*Report requires naming the specific state, its writers and readers, and the sequence that leaves it inconsistent — not just "state sync gap" or "cache may be stale."*

Note: Implicit dependencies on execution order belong to the code-maintainability dimension. This category focuses on state that IS explicitly managed but becomes inconsistent.

**Category 6 — Resource Leaks**
- Unclosed file handles, connections, streams
- Event listeners not cleaned up
- Timers/intervals not cleared
- Memory accumulation in long-running processes

**Category 7 — Dangerous Defaults**
- `timeout = 0` or `timeout = Infinity` (hangs forever or never times out)
- `retries = Infinity` or unbounded retry loops
- `validate = false`, `skipValidation = true` (skips safety checks by default)
- `secure = false`, `verifySSL = false` (insecure by default)
- `dryRun = false` (destructive by default when dry-run exists)
- `force = true`, `overwrite = true` (destructive by default)
- `limit = 0` meaning "no limit" (unbounded operations)

The test: "If a tired developer calls this with minimal args, will something bad happen?"

**Category 8 — Fail Loudly**
- Stub or placeholder implementations that silently run the wrong behavior instead of throwing with a clear error message
- Partial implementations that return a default/empty value when the code path should not be reached yet
- `TODO` or `not implemented` paths that return success or silently no-op instead of failing explicitly

The test: "If this unfinished code path is hit in production, will anyone notice?"

Note: This is about code paths that should fail explicitly but don't. If the stub causes a runtime crash or data loss, it's also a Category 3 issue. If the stub produces wrong output that diverges from the change's intent, it's also a change-intent concern. If the code is simply unused (never called), that's dead code — the code-maintainability dimension owns it. If the implementation is incomplete in scope but works correctly for what it handles, that's under-engineering — the code-design dimension owns it. Fail Loudly is specifically about code paths that ARE reached but silently produce wrong behavior instead of failing.

## Actionability filter

Before reporting a bug, it must pass ALL of these criteria. **If it fails ANY criterion, drop the finding entirely.**

1. **In scope** — Two modes:
   - **Diff-based review** (default): Report bugs introduced or exposed by the change, including failures in unchanged code newly reached by it. Name the changed trigger; unrelated pre-existing bugs remain out of scope.
   - **Explicit path review** (caller specified): Audit everything in scope. Pre-existing bugs are valid findings.
2. **Discrete and actionable** — One clear issue with one clear fix. Not "this whole approach is wrong."
3. **Provably affects code — at mechanism level** — You must identify the specific code path that breaks as a concrete mechanism, not a category label. The finding must name the variable, location, value (vs. expected), and sequence of events that produces the wrong behavior. "Race condition possible on userId" is a shape — reject. "useEffect at line 42 reads `userIdRef.current` after the cleanup at line 58 clears it; second fire produces `undefined`" is a mechanism — accept. The test: can you answer *"at line X, variable Y holds value Z because sequence M"*? If not, you have a hypothesis, not a finding — keep tracing or drop it.
4. **Concrete failure, not optional hardening** — Missing error handling or validation must produce the traced failure above. Similar omissions nearby do not establish that the failure was knowingly accepted; only evidence of that accepted tradeoff can exclude it.
5. **Accepted behavior** — An explicit accepted behavior or trade-off can rule out an alleged bug. The presence of a condition or a repair comment is not acceptance of its failure; an implementation choice cannot waive the accepted contract.
6. **Unambiguous unintended behavior** — Would the bug cause behavior the author clearly did not intend? If intent is unclear, if the code's behavior is unclear, or if several interpretations exist and you cannot determine which is correct, drop the finding.

## Out of scope (orthogonality boundaries)

Do NOT report on (owned by other dimensions):
- **Purpose-level gaps without a mechanical defect** (does the chosen behavior achieve the intended goal?) → the change-intent dimension. A traced mechanical defect, including broken bounds that omit data, stays here even when it also violates the change's intent.
- **API contract correctness** (wrong params, missing error handling for specific APIs, consumer breakage) → the contracts dimension
- **Type system improvements** that don't cause runtime bugs → the type-safety dimension
- **Maintainability concerns** (DRY, coupling, consistency patterns) → the code-maintainability dimension
- **Over-engineering / complexity** → the code-simplicity dimension
- **Design fitness** (wrong approach, reinvented wheels, under-engineering) → the code-design dimension
- **Documentation quality** → the docs dimension
- **Test coverage gaps** → the test-quality dimension
- **Testability design** (hard to test, mock friction) → the code-testability dimension
- **Context file compliance** → the context-file-adherence dimension
- Security vulnerabilities requiring static analysis (injection, auth design) → separate security audit
- Performance optimizations (unless causing functional bugs)

**Key distinctions from neighboring dimensions:**
- **change-intent** asks: "Does this change do what the author intended?" (intent-behavior analysis). This dimension asks: "Does this code have mechanical defects?" (runtime failures, resource issues, structural flaws).
- **contracts** asks: "Are API calls correct per documentation?" (evidence-based contract verification). This dimension asks: "Will this code crash or leak resources?" (code-pattern defects).

**Rule of thumb:** A purpose-level disagreement without a mechanical defect belongs to change-intent. A concrete broken index, bound or state transition remains a mechanical defect even when the accepted purpose explains why its result is wrong. If it requires API DOCUMENTATION to verify (wrong params, missing error codes), it's the contracts dimension. If it's a defect pattern recognizable from the CODE STRUCTURE alone (race condition, null deref, resource leak, dangerous default), it's this dimension.

Note: Security issues causing **runtime failures** (crashes, data corruption) ARE in scope. Security issues requiring **static analysis** are out of scope.

**Tool usage**: Fetching pages and searching the web are available for researching unfamiliar APIs or ambiguous language semantics. If web research fails and you still cannot name the input, state, or sequence that produces the failure, drop the finding entirely.

## Severity calibration

Use the shared ladder. Wrong results, omitted data, stale substantive information and incorrect error behavior are High or Critical by consequence, even under unusual preconditions or with a workaround. A must-fix quality gap is Medium. Polish or nits of any kind are Low; a cosmetic location alone does not establish that.

## Report expectations (this dimension)

Beyond the shared report format: add a **Category** field naming the category from the detection list above. Where a code snippet showing the bug clarifies the finding, include it. The shared format's required **Trigger** field carries the conditions that produce the failure.
