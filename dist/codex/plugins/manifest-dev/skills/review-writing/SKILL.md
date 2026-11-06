---
name: review-writing
description: 'Review any prose against its register''s writing standard — a README, a spec, a design doc, a blog post, marketing copy, or a draft you paste in. Detects whether the text is documentation or human-voiced writing, applies that register''s rules plus the rules holding in both, and reports graded findings with the fix. Use when checking a document''s style, asking whether a draft reads as AI-written, reviewing writing before publishing, or asking for a writing review outside a manifest run.'
user-invocable: true
---

# review-writing — review prose in its own register

Report where a text departs from the writing standard that governs it. Review only: you find and
explain, the author decides and edits.

## Input

`$ARGUMENTS` carries what to review — a file path, a directory, a glob, or pasted text. It may
also name a register explicitly (`register=docs`, `register=voice`) to override detection. A
manifest gate's Evidence activates this skill with a register under the run's selected evaluator; the
gate names the register and its caller-chosen acceptance policy.

With no argument, review the most recently modified prose file in the working tree and say which
one you picked. If that is ambiguous or nothing prose-shaped has changed, ask what to review
rather than guessing.

## Registers and thresholds

Two registers, each with its own rules. Classify findings by consequence; the caller supplies any acceptance policy:

| Register | What it covers | Rules |
|----------|----------------|-------|
| `docs` | Specs, proposals, reports, formal and technical documentation, READMEs, reference material, API docs | `../define/references/DOCS-STYLE-REFERENCE.md` |
| `voice` | Articles, blog posts, marketing and social copy, newsletters, narrative, creative writing | `../define/references/WRITING-REFERENCE.md` |

Each register brings the shared floor with it: `../define/references/PROSE-FLOOR-REFERENCE.md`
holds the rules common to both, including the accessibility and inclusive-language floors, and a
finding from the floor is graded and reported on the same footing as one from the register. There
is no separate floor-only invocation.

Both registers grade by consequence: High covers wrong meaning or a broken promise, Medium
covers a clear quality gap that must be fixed before shipping, and Low is polish or a nit
of any kind: style, naming, structure, or otherwise. The loaded register anchors name its concrete
audience costs. An explicit requirement remains binding; a correctness or safety failure or broken
binding promise received as Low is regraded from evidence before applying the caller's policy.

The caller supplies the acceptance claims and any deliberately required severity or category
policy. For a claim-based gate, connect each alleged failure to the intended reader, meaning or
effect and show the concrete cost; a grade alone does not defeat the claim. Preserve explicit
thresholds when supplied. Without a requested gate, return classifications without a verdict;
if a verdict is requested without recoverable claims or policy, ask or report BLOCKED. Missing
necessary evidence remains unresolved, and an empty findings list alone does not prove quality.

**Load exactly two references**: the floor, plus the one register's. Never load both register
files for one text — their rules contradict each other by design, and a finding drawn from the
wrong one is noise.

The paths above are where these files sit when the whole plugin is installed. Where they are
absent — a single-skill install, or a host that lays skills out differently — search for them by
name before giving up, and where they genuinely cannot be found, say so and report only the
findings you can support without them rather than reviewing against remembered rules.

### Detecting the register

Read enough of the text to judge what it is for. Documentation instructs or specifies: it tells a
reader how something works or how to do something, and its value is in being followed. Human-voiced
writing persuades, narrates, or entertains: it carries a perspective, and its value is in being
read.

Where a text genuinely mixes both — a tutorial opening with a story, a launch post that becomes
reference material — take the register of its dominant body, say which you took and why in one
line, and note that the other register's rules were not applied.

Where detection is genuinely balanced, say so and ask, rather than picking silently. An explicit
`register=` argument always wins and needs no explanation.

## Precedence

A project's own style sheet or `AUTHOR_VOICE.md`, and any rule the user stated in the session or a
context file, outrank the shipped references — in every register. Before reviewing, look for them;
where one states a rule that differs from the reference, it governs and the reference's version raises no finding — except a CRITICAL finding on the
applied register's scale, which is still reported, naming the rule. Say in the report which style source you applied.

## Reporting

Report each finding with:

- the severity and the rule area
- the exact quoted prose, with its location
- what the rule requires, and why this instance fails it
- the concrete fix — the rewritten line where one line is enough, the shape of the change where it isn't

Order findings by severity, then by position in the text.

A clean text is a real result: say so plainly, name the register and reference set you applied,
and stop. Never pad a report with marginal findings to look thorough — a manufactured finding
costs the author more attention than it returns. When the text has many instances of one pattern,
report the pattern once with two or three examples and a count, rather than one finding per
instance.

Where a rule's application to this text is a judgment call, say that in the finding instead of
grading it as a defect.

## Scope, and what this is not

This skill reviews **prose the user points it at**, on request, in any register.

It does not overlap the `prose-value` dimension of `review-code`, which asks a
different question on a different surface: whether prose *inside a code change* — code comments
and repo doc files in a diff — earns its place at all. That dimension is diff-scoped and runs as
part of a code review; this skill reads a whole text on demand and judges it against a style
standard. Reviewing a README before publishing it is this skill; catching a comment that restates
the line below it during a code review is that dimension.

If the user asks for the fixes to be applied after seeing the report, that is a separate request
and ordinary editing.
