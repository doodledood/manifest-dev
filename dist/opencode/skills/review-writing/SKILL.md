---
name: review-writing
description: 'Review any prose against this project''s writing standards — a README, a spec, a design doc, a blog post, marketing copy, or a draft you paste in. Detects whether the text is documentation or human-voiced writing, applies that register''s rules plus the rules holding in both, and reports graded findings with the fix. Use when checking a document''s style, asking whether a draft reads as AI-written, reviewing writing before publishing, or asking for a writing review outside a manifest run.'
user-invocable: true
---

# review-writing — review prose in its own register

Report where a text departs from the writing standard that governs it. Review only: you find and
explain, the author decides and edits.

## Input

`$ARGUMENTS` carries what to review — a file path, a directory, a glob, or pasted text. It may
also name a register explicitly (`register=docs`, `register=voice`) to override detection. A
manifest gate's body activates this skill with a register under the run's selected evaluator; the
gate names the register and this skill owns the threshold.

With no argument, review the most recently modified prose file in the working tree and say which
one you picked. If that is ambiguous or nothing prose-shaped has changed, ask what to review
rather than guessing.

## Registers and thresholds

Two registers, mutually exclusive. Each has its own rules, and applying the wrong set produces
findings the author should ignore — which costs more than reviewing nothing. The threshold is the
bar a text must clear to PASS in that register:

| Register | What it covers | Rules | Threshold (PASS requires) |
|----------|----------------|-------|---------------------------|
| `docs` | Specs, proposals, reports, formal and technical documentation, READMEs, reference material, API docs | `../define/references/DOCS-STYLE-REFERENCE.md` | no MEDIUM-or-higher findings |
| `voice` | Articles, blog posts, marketing and social copy, newsletters, narrative, creative writing | `../define/references/WRITING-REFERENCE.md` | no MEDIUM-or-higher findings |

Each register brings the shared floor with it: `../define/references/PROSE-FLOOR-REFERENCE.md`
holds the rules common to both, including the accessibility and inclusive-language floors, and a
finding from the floor is graded and reported on the same footing as one from the register. There
is no separate floor-only invocation.

The two thresholds sit at the same grade and still mean different things, because each register's
severity anchor measures something different — what the prose costs a reader, against how
identifiable it is as AI-written. Grade by the anchor of the register you applied, and never
convert a finding from one scale to the other.

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
line, and note that the other register's rules were not applied. Don't split one text across two
registers.

Where detection is genuinely balanced, say so and ask, rather than picking silently. An explicit
`register=` argument always wins and needs no explanation.

## Precedence

A project's own style sheet or `AUTHOR_VOICE.md` outranks the shipped references — this is the
one home for that rule, and it applies to every register. Before reviewing, look for one in the
project; where it states a rule that differs from the reference, the project's rule governs and
the reference's version raises no finding. Say in the report which style source you applied.

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
