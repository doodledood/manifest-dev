# Docs review

Find documentation and code comments that have drifted from the code the change touches, and report exactly what needs updating.

**The question for every change: "Does the documentation and the comments still match what the code now does?"**

## What to audit

Audit documentation files AND code comments in changed files against actual code behavior. Report gaps, inaccuracies, stale content, and missing documentation.

Be comprehensive in analysis, precise in reporting. Check every changed file for documentation and comment drift — do not cut corners or skip files. But report only findings that meet the high-confidence bar in the Actionability Filter. Thoroughness in looking; discipline in reporting.

Typical drift to look for:

- Examples, commands, flags, or snippets that would now fail or error
- API signatures, parameters, return shapes, or file paths documented one way but implemented another
- New features or behavior with no documentation at all
- Major behavior changes not reflected in the docs
- Removed features still documented
- Incorrect installation/setup steps
- JSDoc/docstrings with wrong parameter names or types
- Code comments that describe behavior the code no longer has, or stale TODO/FIXME comments

These audit areas are guidance, not exhaustive. If you identify a documentation accuracy issue that fits this dimension but doesn't match a listed area, report it — just respect the out-of-scope boundaries below to keep dimensions orthogonal.

## Actionability filter

Before reporting a documentation issue, it must pass ALL of these criteria. **If a finding fails ANY criterion, drop it entirely.**

1. **In scope** — two modes:
   - **Diff-based review** (default, no paths specified): ONLY report doc issues caused by the code changes. Pre-existing doc problems are strictly out of scope — even if you notice them, do not report them. The goal is ensuring the change doesn't break docs, not auditing all documentation.
   - **Explicit path review** (caller specified files/directories): audit everything in scope. Pre-existing inaccuracies are valid findings since a full review of those paths was requested.
2. **Actually incorrect or missing** — "could add more detail" is not a finding. "This parameter is documented as optional but the code requires it" is a finding.
3. **User would be blocked or confused** — would someone following this documentation fail, get an error, or waste significant time? If yes, report it. If they'd figure it out, it's Low at best.
4. **Not cosmetic** — formatting, wording preferences, and "could be clearer" suggestions are Low priority. Focus on factual accuracy.
5. **Matches doc depth** — don't demand comprehensive API docs in a project with minimal docs. Match the existing documentation style and depth.
6. **High confidence** — you must be certain the documentation is incorrect. "This could be improved" is not sufficient; "this doc says X but the code does Y" is required. If uncertain, don't flag it — an empty report beats uncertain findings.

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

**Documentation issues are capped at Medium** — docs don't cause data loss or security breaches.

- **Medium** — actionable documentation issues:
  - Examples that would fail or error
  - Incorrect API signatures, parameters, or file paths
  - New features with no documentation
  - Major behavior changes not reflected
  - Removed features still documented
  - Incorrect installation/setup steps
  - JSDoc/docstrings with wrong parameter names or types
- **Low** — minor inaccuracies and polish:
  - Minor parameter or option changes not reflected
  - Outdated examples that still work but aren't ideal
  - Missing edge cases or caveats
  - Minor wording improvements
  - Formatting inconsistencies
  - Stale TODO/FIXME comments

**Calibration check:** if you're tempted to mark something higher than Medium, reconsider — even actively misleading docs are Medium because users can recover by reading the code or asking.

## Edge cases

- **No docs exist** — report as a Medium gap and suggest where docs should be created.
- **No code changes affect docs** — report that documentation is up to date, with reasoning.
- **Unclear if a change needs docs** — report as Low with reasoning and let the caller decide.

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

- **Location**: `path/to/doc.md` (line range if applicable) or `path/to/code.ts:line` for comment issues
- **Related code**: `path/to/code.ts:line` the doc describes
- **Current doc/comment says**: quote or summary of what's written now
- **Code actually does**: what the implementation does
- **Suggested update**: the specific text/change needed, or "Remove comment"

Separate documentation-file findings from code-comment findings if both exist, and list any new features/changes with no documentation at all under a missing-documentation grouping. Every issue must cite a specific file:line and have an actionable suggested update. If no issues pass the filter, the PASS report should briefly state what was checked and why docs are up to date.
