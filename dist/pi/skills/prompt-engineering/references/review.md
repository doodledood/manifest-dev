# Reviewing or updating a prompt

Review is a gap re-audit. For each line, ask: *would the model produce this behavior — or this knowledge, for a knowledge skill — without it?* If the answer is yes, the line is restating a model default; flag it. If no, the line is closing a real gap; keep it.

Update is the same audit applied to a specific change. Find the new gap; close it with the minimum content; re-check that adjacent lines still earn their place after the change. Sometimes the patch *replaces* an existing line rather than adding to it. Net delta can be positive, zero, or negative — calibration, not direction.

## The single review question

> *Would the model produce this behavior without this line?*

Apply it to every line. The line earns its place if and only if the answer is *no, the model wouldn't reach this on its own*.

## The boundary check

> *Does this line still hold at the edges of where this prompt will run?*

A line can earn its place locally and still be brittle. The earn-your-place question is point-wise; the boundary check tests each line against the conditions it'll actually meet. Run both — they catch different failures.

| Edge | Symptom | Fix |
|------|---------|-----|
| **Harness** | Names a primitive bound to one harness: a specific scheduler, prompt, approval, subscription, MCP, or CLI tool by name | State the principle or capability in natural language; let the model pick whatever tool the harness exposes |
| **Scope qualifier** | Rule has a qualifier (`by another reviewer`, `under --loop only`, `in mode X`) that excludes cases the principle should also cover | Drop the qualifier or broaden it to match the principle's reach |
| **Mechanism-as-prescription** | Specific numbers or a fixed sequence stated as the only path (`15→30→60→120 min`, `Max 3 iterations`, a hardcoded tool chain) | State the principle; numbers and sequences become defaults, not the rule |
| **Split of same rule** | Same principle restated in multiple places with slight variations (one general, one mode-specific) | Unify into one rule, delete the splits |
| **Description keyword dump** | Skill or agent description ends with a labeled list of search terms | Fold those phrases into natural-language activation prose |

A line that passes earn-your-place but fails boundary is fragile — works today, breaks the first time the prompt runs in a different harness, mode, or scope. Boundary fixes usually *reword* the line rather than delete it.

## Anti-patterns

| Anti-pattern | Example | Fix |
|--------------|---------|-----|
| **Prescribing HOW** | *"First search, then read, then analyze…"* | State the goal: *"Understand the pattern"* |
| **Capability instructions** | *"Use grep to search"*, *"Read the file"* | Cut unless naming a required input source; the model knows how |
| **Restating model defaults** | *"Be helpful"*, *"use good judgment"*, *"think carefully"* | Cut |
| **Arbitrary limits** | *"Max 3 iterations"*, *"2-4 examples"* | Principle: *"until converged"*, *"as needed"* |
| **Rigid checklists for runtime** | Step-by-step procedure baked in for the model to follow | Convert to goal + constraints. Order-bearing patterns (metaprompting) and author-facing checklists (like this one) are exempt — they're not steps the model follows at runtime. |
| **Weak hedging** | *"Try to"*, *"maybe"*, *"if possible"*, *"when appropriate"* | Direct imperative: *"Do X"* |
| **Absolutes for judgment calls** | *"ALWAYS verify"*, *"NEVER skip"* applied to non-invariants | Decision rule: *"When X, do Y; otherwise Z"* (see `patterns.md`) |
| **Buried critical info** | Safety / output-contract rules mid-paragraph | Surface near the top of the owning section |
| **Over-engineering** | Ten phases for a simple task | Match complexity to the gap |
| **Examples for known behaviors** | *"Here's how to format JSON: …"* | Cut — the model already knows |
| **Why-this-exists framing prose** | Multi-paragraph motivation before the actual rules | Cut — the rule is the rule |
| **Tables for non-tabular content** | A table with two rows of prose | Use prose |

**Carve-outs:**

- *Capability instructions* — specific data-flow (*"read `/etc/config` first"*) is fine; generic capability narration isn't.
- *Weak hedging* — banned as top-level directives. Fine in explanatory prose where the surrounding sentence makes the action concrete.
- *Examples* — known behaviors don't need them, but non-obvious output shape does. For knowledge skills especially, examples often carry information prose can't convey. The check: *would the model produce the right shape without seeing the example?* — see `knowledge-skills.md`.

## Update discipline (bidirectional)

Before each edit, the questions are:

- Does this change close a real gap that exists now and didn't before (or was missed)?
- After this change lands, does any adjacent line stop earning its place? (Common: a new explicit rule obviates an older vague hedge.)
- Am I adding a wall around a single observed failure that won't generalize? (Patch overfitting.)
- Can the change be a *replacement* of an existing line rather than an addition?

Over-engineering signals — when these appear, step back:

- Prompt length doubled or tripled
- Edge cases that won't actually happen
- Clear language rewritten into verbose language for "completeness"
- Examples for behaviors the model already gets right
- New section to address a single instance of failure

Watch for **contradictory rules** and **priority collisions** — two rules that can't both hold (*"be concise"* alongside *"err on the side of completeness"*). Flag and resolve, don't leave both.

Not all repetition is bloat. **Intentional emphasis** reinforces a critical rule — keep duplications that restate true invariants (safety, output contracts, hard constraints). Dedupe duplications that restate a heuristic in different words.

## Pre-ship checks

- Every line earns its place by the review question above (or is logged as an exception).
- The prompt defines WHAT and WHY, not HOW. No procedural step-prescription where the model already knows the procedure.
- Critical ambiguities resolved through user interview; minor ambiguities documented with chosen defaults.
- Domain terms defined where the model wouldn't know them.
- Absolutes (MUST / NEVER / ALWAYS) reserved for true invariants — judgment calls use decision rules.
- No arbitrary numbers (or each one is justified).
- Critical rules surfaced near the top of their owning section, not buried.
- Complexity matches the gap — no section longer than its job requires.
- Emotional tone calibrated — no all-caps urgency, no excessive praise; failure normalized for iterative prompts.
- If user-facing (conversational / customer-facing): Personality section present and calibrated.
- If a skill: directory with SKILL.md + companions; description is natural-language activation prose (what + when + user phrases); see `skills.md`.
- If an agent: every required tool declared in `tools:` frontmatter; see `agents.md`.
- If restructuring: high-signal content preserved, relocated, or folded — not silently dropped.

## Gotchas

- **Rewriting working language for style.** If existing language is unambiguous and effective, don't touch it. The verb that fits is *audit*, not *rewrite-for-taste*.
- **Skipping context discovery on "simple" prompts.** Even simple prompts have hidden constraints. Force discovery before producing output.
- **Converting principles into rigid rules.** *"Stop when converged"* becomes *"Max 5 iterations."* Principles bend; rigid rules create edge cases.
- **Adding examples for behaviors the model already knows.** Examples earn their place only when they demonstrate non-obvious or counter-intuitive shape.
- **Treating "shorter" as the goal.** The goal is closing the gap with the least content that does the job. Sometimes that's shorter; sometimes it's the same length but rebalanced.
