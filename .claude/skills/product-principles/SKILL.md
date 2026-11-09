---
name: product-principles
description: 'Product principles for manifest-dev: how its maintainer wants calls about what the plugin does for its users made, and why. Use before planning, designing, building or reviewing a skill step, a mode, a default or an offer that manifest-dev ships.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- When a call shapes behavior manifest-dev ships — a skill step, a mode, a default, an offer — prefer a sensible default every user gets with no setup, changeable through channels people already use (their stated rules, their context file, their project's own copy of a convention), worded to hold across the many kinds of project the plugin runs in rather than one project, host or case — in the maintainer's words, "have defaults baked in with options to change and override, and keep things general when possible, since the product here applies to many, many use cases." Yields when no single default fits a known group of users: let the default follow what the session can see, rather than adding a setting or a question; and when generalizing would widen the work beyond the job at hand: generalize the wording, not the machinery.

Before calling product work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
