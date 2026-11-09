---
name: prompt-principles
description: 'Prompt principles for manifest-dev: how its maintainer wants the shipped skills, references and other prompts written and checked, and why. Use before planning, writing, restructuring, reviewing or verifying a change to a prompt, a skill or an agent in this repository.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Show a prompt change working by driving the behavior cases it touches, new or existing eval cases, through `scripts/verify drive`, rather than asking the maintainer to judge the words — the maintainer judges a prompt change by what it makes a run do, and a drive is the evidence they rely on; a whole eval suite runs only when they ask, because each run is many paid sessions. Yields when the text must be approved as written, such as a public post, or when no case can reach the behavior; then say so.
- Settle a prompt change on one run per arm and accept the noise: each touched case once on the skills before the change and once after, adding runs only where that pair does not settle it — both arms pass, both fail, or a verdict is borderline — every run is a paid model session and more runs get expensive, while one pair is good enough once its noise is accepted. Yields when the decision would be costly to reverse and rests on one borderline pair, or when the maintainer asks for a fuller measurement.
- When a skill grows a flag or a mode, keep what every invocation needs inline in `SKILL.md`, move that mode's bulk to a file under `references/` loaded only when the mode resolves, and keep the trigger in `SKILL.md`, in a `Modes` or `What loads` table beside the flags — otherwise the default invocation carries the whole file to use a fraction of it, and a trigger inside the deferred file can only be read after the load it was meant to gate. Yields when a mode's mechanics run to a paragraph: an indirection costs a load and a reader's place, and can strand a subtle trigger; and prefer restating one rule in two files only where the files cannot reach each other. The decision is `docs/adr/20260703-progressive-disclosure-triggers-live-in-loading-layer.md`.
- Define every term a shipped skill's behavior depends on where the skill first uses it, and defer no definition to the glossary, another skill, or a section a reader may never reach — a skill installed in someone else's project gets its own `SKILL.md` and the references its loading layer names, never this repository's `CONTEXT.md`; `figure-out`'s gloss of *fog* at first use is the pattern. Yields for plain words that carry no project meaning.
- A skill that reads, seeds or writes a user's own context file names *the project context file* resolved by detection, never a fixed filename — the file it means is the user's, on whatever host they run, never this repository's. Hard limit, no trade-off.

Before calling prompt work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
