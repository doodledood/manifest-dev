# Docs review

Find documentation and code comments that have drifted from the code the change touches, and report exactly what needs updating.

**The question for every change: "Does the documentation and the comments still match what the code now does?"**

## What to audit

Audit documentation files AND code comments in changed files against actual code behavior. Report gaps, inaccuracies, stale content, and missing documentation.

Typical drift includes failing examples or commands, wrong signatures, parameters, return shapes or paths, missing feature documentation, removed features still documented, incorrect setup steps, stale TODO/FIXME comments and comments that describe behavior the code no longer has.

These examples are guidance, not exhaustive. If you identify a documentation accuracy issue that fits this dimension but doesn't match a listed issue, report it — just respect the out-of-scope boundaries below to keep dimensions orthogonal.

## Actionability filter

Before reporting a documentation issue, it must pass ALL of these criteria. **If a finding fails ANY criterion, drop it entirely** — criteria 3 and 4 distinguish substantive gaps from optional polish or nits of any kind using the shared ladder.

1. **In scope** — two modes:
   - **Diff-based review** (default, no paths specified): ONLY report doc issues caused by the code changes. Pre-existing doc problems are strictly out of scope as findings — even if you notice them, do not report them as findings (a caller may ask for them in a separate list; `SKILL.md` → *The Pre-existing list, only when asked*). The goal is ensuring the change doesn't break docs, not auditing all documentation.
   - **Explicit path review** (caller specified files/directories): audit everything in scope. Pre-existing inaccuracies are valid findings since a full review of those paths was requested.
2. **Actually incorrect or missing** — "could add more detail" is not a finding. "This parameter is documented as optional but the code requires it" is a finding.
3. **User would be blocked or confused** — name the failing instruction, incorrect claim or concrete missing explanation. A workaround does not lower a broken promise to Low.
4. **Not an optional nit** — style, naming, structure and wording preferences alone are below-bar. A violation of a binding documentation requirement is substantive even when it concerns those areas.
5. **Matches doc depth** — don't demand comprehensive API docs in a project with minimal docs. Match the existing documentation style and depth.
6. **High confidence** — you must be certain the documentation is incorrect. "This could be improved" is not sufficient; "this doc says X but the code does Y" is required. If uncertain, don't flag it.

## Out of scope (belongs to a sibling dimension)

Do NOT report on:

- **Intent-behavior divergence** (does the change achieve its goal?) → belongs to the change-intent dimension
- **Mechanical code defects** (race conditions, resource leaks, null handling) → belongs to the code-bugs dimension
- **API contract correctness** (wrong params, consumer breakage) → belongs to the contracts dimension
- **Code organization** (DRY, coupling, consistency) → belongs to the code-maintainability dimension
- **Over-engineering / complexity** (premature abstraction, cognitive complexity) → belongs to the code-simplicity dimension
- **Type safety** → belongs to the type-safety dimension
- **Test coverage gaps** → belongs to the test-quality dimension
- **Prose value / AI-tells in comments and doc files** → belongs to the prose-value dimension
- **Context file compliance** (except doc-related rules) → belongs to the context-file-adherence dimension

**Boundary with prose-value:** this dimension owns *accuracy* — whether comments and doc files match what the code actually does (drift, stale content, wrong signatures). The prose-value dimension owns whether the prose *earns its place* (value, AI-tells). Accuracy here; worth-keeping there.

## Severity calibration

Use the shared ladder. A command that fails, a wrong signature, misleading safety advice or another broken documentation promise is High or Critical by consequence; documentation has no severity cap. A missing explanation that creates a concrete must-fix reader gap is Medium. Optional polish or nits of any kind are Low, including wording and structural preferences.

## Edge cases

- **No docs exist** — name the reader task that needs documentation and grade the demonstrated gap by the shared ladder; absence alone does not establish Medium.
- **No code changes affect docs** — report that documentation is up to date, with reasoning.
- **Unclear if a change needs docs** — report only a supported discrepancy or missing explanation, not the uncertainty itself.

## Suggested-update standards

Every finding must carry a concrete suggested update. When you write one:

- **Mirror the document's format** — if the doc uses tables, suggest table updates; if it uses bullets, use bullets.
- **Match heading hierarchy** — follow the existing H1/H2/H3 structure.
- **Preserve voice and tone** — technical docs stay technical, casual docs stay casual.
- **Keep consistent conventions** — if the doc uses `code` for commands, do the same.
- **Maintain density level** — don't add verbose explanations to a terse doc.
- **Accuracy always** — commands, flags, parameters, file paths, version numbers, and examples must match the code exactly.

## Dimension-specific report fields

Beyond the shared report skeleton, each finding should make the discrepancy concrete:

- **Related code**: `path/to/code.ts:line` the doc describes
- **Current doc/comment says**: quote or summary of what's written now
- **Code actually does**: what the implementation does
- **Suggested update**: the specific text/change needed, or "Remove comment"

Separate documentation-file findings from code-comment findings if both exist, and list any new features/changes with no documentation at all under a missing-documentation grouping. If no issues pass the filter, the PASS report should briefly state what was checked and why docs are up to date.
