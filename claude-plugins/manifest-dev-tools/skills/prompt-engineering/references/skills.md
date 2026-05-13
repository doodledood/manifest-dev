# Skill Architecture Patterns

Loaded when creating or updating a Claude Code skill. Supplements universal prompt principles with architecture patterns from Anthropic's internal experience with hundreds of skills.

## Skills Are Folders

A skill is a directory, not a markdown file. The file system is context engineering — what lives alongside SKILL.md shapes how Claude executes the skill. Useful companions: reference docs (API signatures, domain knowledge), assets (templates for output artifacts), scripts (composable libraries Claude can invoke or generate against).

## Progressive Disclosure

Don't front-load everything into SKILL.md. Point to companion files Claude should read at appropriate times. SKILL.md declares what's available; Claude loads it when relevant.

**Why**: Monolithic prompts suffer context rot. Splitting content lets Claude load only what the current phase needs, keeping working context focused.

## Gotchas Section

The highest-signal content in any skill. Gotchas encode failure modes Claude actually hits — not theoretical risks, but observed patterns where the skill produces wrong output.

Build gotchas from real failures. Update as new edge cases emerge. A skill with good gotchas outperforms a skill with perfect instructions but no failure-mode awareness.

A good gotcha is specific (names the failure), actionable (says what to do instead), and grounded (observed, not hypothetical).

## Setup & User Context

Skills needing user-specific configuration (channel names, project IDs, preferred formats) should store setup in a config file within the skill directory. If config is absent, ask the user and persist their answers.

**Why**: Asking every session wastes turns. Persisted config makes the skill stateful across invocations.

## Description as Trigger

Claude Code builds a skill listing from descriptions at session start and scans it to match user requests to skills. The description field is a **trigger specification** — write it for the model's matching algorithm, not as a human-readable summary.

Pattern: what the skill does + when to invoke it + terms users actually say. Weak: "Helps with code review." Strong: "Adversarial code review that spawns a fresh-eyes subagent. Use for PR review, code audit, or pre-merge quality check."

## Skill Type Awareness

Skills cluster into recurring categories. Knowing which type you're building surfaces the right patterns:

| Type | Core Pattern |
|------|-------------|
| **Library/API Reference** | Edge cases, footguns, reference snippets for correct usage |
| **Product Verification** | Test/verify output — often paired with scripts for programmatic assertions |
| **Data Fetching & Analysis** | Connects to data stacks — credentials, dashboard IDs, common query workflows |
| **Business Process** | Automates repetitive workflows — benefits from logging previous runs for consistency |
| **Code Scaffolding** | Generates boilerplate — useful when scaffolding has natural-language requirements |
| **Code Quality & Review** | Enforces standards — can include deterministic scripts for robustness |
| **CI/CD & Deployment** | Fetch, push, deploy workflows — may compose with other skills |
| **Runbooks** | Symptom → investigation → structured report |
| **Infrastructure Ops** | Routine maintenance with guardrails for destructive actions |
