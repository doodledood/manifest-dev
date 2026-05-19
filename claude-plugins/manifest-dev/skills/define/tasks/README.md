# Task Files — Composition Rules

Each task type in `tasks/` carries domain-specific encoder data: quality gates (auto-include as INV-G*), Defaults (auto-include as PG-*), and reference data for verifier agents. Probing of the conversation is figure-out's job — task files don't carry probing fuel.

## Domains

| Domain | Indicators | File |
|--------|------------|------|
| Coding | Any code change; includes default reviewer gates for intent, bugs, operational readiness, design, tests, docs, and context adherence | `CODING.md` |
| Feature | New functionality, APIs, enhancements | `FEATURE.md` |
| Bug | Defects, errors, regressions, "not working", "broken" | `BUG.md` |
| Refactor | Restructuring, "clean up", pattern changes | `REFACTOR.md` |
| PR lifecycle | Shipping a change through CI, review, approvals | `PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `PROMPTING.md` |
| Writing | Prose, articles, copy, social, creative (base) | `WRITING.md` |
| Document | Specs, proposals, reports, formal docs (base: Writing) | `DOCUMENT.md` |
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials (base: Writing) | `BLOG.md` |

## Composition

- Code-change tasks combine `CODING.md` (base quality gates) with the domain specific (FEATURE / BUG / REFACTOR).
- Text-authoring tasks combine `WRITING.md` with the content-type guidance (BLOG / DOCUMENT).
- Research composes `research/RESEARCH.md` with source-type files in `research/sources/`.
- Domains aren't mutually exclusive: a "bug fix that requires refactoring" uses both `BUG.md` and `REFACTOR.md`.
- **PR lifecycle composition** — `PR_LIFECYCLE.md` composes onto `CODING.md` when the local `origin` remote points at `github.com` (auto-detected). Templates a single AC invoking the `github-pr-lifecycle` agent; the agent owns lifecycle gate logic; the AC's `verify.prompt:` is the steering surface for per-PR nuances (labels, named approvers, known-flaky CI, retrigger overrides). Multi-repo manifests auto-template the AC per repo declared in `Repos:`.
- **Exception:** PROMPTING tasks do NOT compose with CODING unless the task also changes executable code. PROMPTING has its own quality gates.

## Task file content types

- **Quality gates** (`## Quality Gates` section) — auto-include as INV-G*. Omit clearly inapplicable with stated reasoning.
- **Defaults** (`## Defaults` section) — encoded pre-interview as PG-*. Included in manifest without probing; user reviews and removes if not applicable.
- **Reference files** (`references/*.md` inside each task domain) — lookup data for verifier agents; not loaded during /define.

Encode quality gates and Defaults immediately after reading task files — before figure-out's conversation kicks off. Surface each as it lands so the dialogue carries the encoding decisions forward.
