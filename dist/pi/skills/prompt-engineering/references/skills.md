# Writing a skill

A skill activates a behavior the model wouldn't naturally produce, or activates it with a calibration the default lacks (more relentless, more structured, more skeptical, etc.). The skill's content is whatever closes that gap — no more.

Default to packaging a new capability as a skill rather than an agent: skills are the Agent Skills Open Standard — plugin-bundleable and identical across harnesses — and a general-purpose agent told to activate the skill reproduces agent behavior in nearly all cases. Choose an agent only when you need harness-specific frontmatter (a restricted tool allow-list, an isolated model/subagent type); see `agents.md`.

## Minimum-viable shape

A skill body can be as short as three sentences when goal + expected behavior + one override are all the gap requires. The example below — a "grill me on this plan" skill — illustrates the shape:

```
Interview me relentlessly about every aspect of this plan until we reach
a shared understanding. Walk down each branch of the design tree,
resolving dependencies between decisions one-by-one. For each question,
provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the
codebase instead.
```

Three sentences. Goal ("shared understanding"), expected behavior ("relentlessly," "one at a time," "with recommendation"), one override of natural behavior ("explore the codebase instead of asking"). The model already knows how to interview, prioritize, walk a decision tree — those are not stated.

Start here. Add only when the gap requires it.

## Skills are folders

A skill is a directory, not a file. SKILL.md is the entry; companion files live alongside (`references/`, `assets/`, `scripts/`, config). The file system is part of the context engineering — what lives next to SKILL.md shapes what Claude can reach when the skill fires.

## Description is activation prose

The frontmatter `description` field is what skill discovery scans at session start. Write it as natural-language activation prose, not a keyword dump or human-facing summary.

Pattern: **what the skill does + when to use it + phrases the user actually says**, integrated into prose under 1024 chars (enforced).

Weak: *"Helps with code review."*
Strong: *"Adversarial code review that brings fresh eyes to code changes. Use for PR review, code audit, pre-merge quality checks, or when the user asks to review a PR, audit code, or check changes before merge."*

Do not append labeled keyword lists. Phrases users actually say belong in the sentence where they explain when the skill should activate.

The description is also where downstream agents inherit the skill's framing — if your description says "slim discipline" or "minimize tokens," agents reading the skill list will think that's the discipline before they invoke. Lead with the *principle* the skill embodies.

## Progressive disclosure

When SKILL.md grows, the question to ask is *"does this content need to be in working context every time the skill fires?"* If no, move it to a `references/*.md` file and point to it conditionally from SKILL.md (`see references/X.md when …`).

Real progressive disclosure means the reference does NOT load until a specific trigger fires (a branch, a flag, a failure mode). If SKILL.md mentions the reference's mechanics, or the reference always loads anyway, the split isn't earning anything — inline it.

Subagent prompts that always run also belong inline at the spawn point, not in a separate file. Splitting them just adds an indirection without saving context.

## Gotchas (when you have them)

The highest-signal content in a mature skill. A gotcha names an observed failure mode, the specific behavior to do instead, and is grounded in a real case — not a theoretical risk. Build the gotchas list as the skill is used in anger; don't pre-populate it speculatively.

Three checks: *specific* (names the failure, not a category), *actionable* (says what to do instead), *grounded* (observed, not imagined).

## Setup and stateful skills

Skills that need user-specific configuration (channel names, project IDs, output paths) persist that config in a file inside the skill directory. Read it on invocation; ask only if absent. Re-asking every session is a gap the skill exists to close.

## Naming

Kebab-case throughout. The name reflects what kind of gap the skill closes: an **instruction-based skill performs an action, so it gets a verb phrase** (`review-code`, `review-pr`, `review-prompt`, `poll-slack`, `check-pr`, `compress-prompt`); a **knowledge-based skill is reference/lookup/teaching with no action, so it may be a noun** (`prompt-engineering`, `claude-api`).

## Frontmatter

```yaml
---
name: kebab-case-name       # required, lowercase, hyphens, max 64 chars
description: '…'             # required, natural-language activation prose, max 1024 chars
argument-hint: '<request>'  # optional, shown in slash-command UI
user-invocable: true        # optional, default true; false hides from the command menu
tools: …                    # optional; omit to inherit invoker's tools (recommended)
---
```

Default to omitting `tools` or equivalent capability declarations for skills. In most harnesses, skills should inherit the invoking context's capabilities; declare tools only when the skill intentionally needs a restricted set, which is rare.

## Common skill shapes (not archetypes — observations)

These aren't a taxonomy you route to. They're recurring shapes that show what kind of gap drove each one:

- **Behavior-activator** — short body, goal + expected behavior + 1–2 overrides. Gap is *how* the model approaches the task. (`figure-out`, `do`.)
- **Workflow** — multi-step procedure with explicit branches. Gap is the procedural logic and where it diverges from natural-model defaults. (`define`, `walk-pr`.)
- **Knowledge** — see `knowledge-skills.md`. Gap is data the model doesn't have.
- **Procedural with lookups** — heavier body with tables, paths, contracts. Gap is the specific data flow the model must respect. (`sync-tools`.)

Length scales with what the gap requires. A 600-line skill earned every line if the procedural logic is genuinely 600 lines wide. A 12-line skill is correct when 12 lines close the gap.
