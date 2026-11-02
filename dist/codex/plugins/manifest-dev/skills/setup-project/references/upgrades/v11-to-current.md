# Upgrading a project from v11: what v12 gives it

A project recording v11 may keep the harness or verify its own way. v12 changes only a kept
harness: its time lines go. A project whose verification bullet names its own way gets none of
this, unless it adopted time lines into its own checks — then the same removal is offered for
those, in their own form.

This item replaces the time-line items of earlier guides: `v4-to-current.md`'s *Scenarios whose
work varies* (`Workload: varies`) and `v6-to-current.md`'s *Time lines into recipes*. A project
reaching this guide from v4 to v10 is offered neither of them, so it never writes a line or a
`Workload:` field on the way to v12.

Find the harness's files through the project's own tool before offering anything, never by
assuming the default `verification/` paths: `verify --help` names the recipes directory and the
settings file, and the project's `verify.mts` (or its port) is the tool.

Offer one item, as a default the project may adapt or decline:

1. **Time lines removed** — all four parts together, since the updated tool refuses what the
   others remove:
   - **The tool update:** the shipped `../harness/verify.mts` (and `verify` entry) shown as a
     difference from the project's own copy, keeping its path lines and customizations, per
     `../VERIFICATION_HARNESS.md` → *The parts*. It has no `line`, `raise` or `freeze` command and
     no exit 5, runs each scenario once, and refuses a leftover time-line field. A ported tool gets
     the same removal in its own language.
   - **Recipe fields:** in every recipe, each scenario's `Line:` lines — whatever follows them,
     `; raised: <reason>` and `; frozen at <seconds> s by <Ticket>` included — and its `Workload:`
     line, deleted. Nothing replaces them.
   - **Settings:** the `headroom:` and `raise:` keys deleted from the settings file's front matter.
   - **Text about lines:** each line that tells a run or a contributor to set, raise, freeze or
     pay down a time line, or to treat exit 5 as a failure, rewritten to *Run time*'s principle or
     deleted — in the settings file's notes, the recipes, the project context file and the
     contributor docs they point to. Search those files rather than reading only the context file,
     and show each line before and after.

   Done when the project's `verify check` passes with the updated tool, a search of its recipes
   and settings finds no `Line:`, `Workload:`, `headroom:` or `raise:` left, and a search of the
   context file and the contributor docs it points to finds no instruction about time lines or
   exit 5 left. Show the
   fields removed. A debt Ticket a freeze named is the project's to close or keep; say which
   Tickets the removed freezes named.

Record the newest surfaces version only after the offer has an answer, as the setup skill
specifies.
