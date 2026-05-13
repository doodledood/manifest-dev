# Review Checklist & Anti-Patterns

Use during review or before shipping. Each item is a question the prompt should be able to answer yes to (or have logged exception).

## Pre-ship checklist

- [ ] Every line either **steers** (behavior the model wouldn't reach on its own) or **scaffolds** that the slim discipline says to keep. No restated model defaults.
- [ ] Defines WHAT and WHY, not HOW. No procedural step-prescription where the model already knows the procedure.
- [ ] Critical ambiguities resolved; minor ambiguities documented with chosen defaults.
- [ ] Domain terms defined, conventions confirmed, success criteria stated.
- [ ] Absolutes (MUST/NEVER/ALWAYS) reserved for true invariants — judgment calls use decision rules.
- [ ] No arbitrary numbers (or justified if present).
- [ ] Weak language replaced with direct imperatives.
- [ ] Critical rules surfaced near the top of their owning section, not buried mid-paragraph.
- [ ] Complexity matches the task — no section longer than its job requires.
- [ ] Emotional tone calibrated — no all-caps urgency, no excessive praise; failure normalized if iterative.
- [ ] If user-facing (conversational / customer-facing): Personality section present and calibrated.
- [ ] If a skill: directory with SKILL.md + companions; description is a trigger spec (what + when + trigger terms).
- [ ] If an agent: every required tool declared in `tools:` frontmatter.
- [ ] If restructuring: high-signal content preserved, relocated, or folded — not silently dropped.

## Anti-patterns

| Anti-pattern | Example | Fix |
|--------------|---------|-----|
| Prescribing HOW | "First search, then read, then analyze..." | State goal: "Understand the pattern" |
| Capability instructions | "Use grep to search", "Read the file" | Remove — model knows how |
| Restating model defaults | "Be helpful", "use good judgment", "think carefully" | Cut |
| Arbitrary limits | "Max 3 iterations", "2-4 examples" | Principle: "until converged", "as needed" |
| Rigid checklists baked in | Step-by-step procedure for runtime | Convert to goal + constraints. Order-bearing patterns (metaprompting) and author-facing checklists (this file) exempt. |
| Weak hedging | "Try to", "maybe", "if possible", "when appropriate" | Direct imperative: "Do X" |
| Absolutes for judgment calls | "ALWAYS verify", "NEVER skip" applied to non-invariants | Decision rule: "When X, do Y; otherwise Z" |
| Buried critical info | Safety / output-contract rules mid-paragraph | Surface near top of owning section |
| Over-engineering | 10 phases for a simple task | Match complexity to need |
| Examples for known behaviors | "Here's how to format JSON: ..." | Remove — model already knows |
| "Why this exists" framing prose | Multi-paragraph motivation before the rules | Cut — the rule is the rule |
| Tables for non-tabular content | A table with 2 rows of prose | Use prose |

**Notes on carve-outs:**
- *Capability instructions* — specific data-flow ("read `/etc/config` first") is fine; generic capability narration isn't.
- *Weak hedging* — banned as top-level directives. Fine in explanatory prose where the surrounding sentence makes the action concrete.

## Update discipline

Before each edit:

- Does this change address a real failure mode?
- Am I adding complexity to solve a rare case?
- Can this be said in fewer words?
- Am I turning a principle into a rigid rule?

Over-engineering warning signs: prompt length doubled or tripled; edge cases that won't actually happen; "improving" clear language into verbose language; examples for behaviors the model already gets right.

Watch for **contradictory rules** and **priority collisions** ("be concise" alongside "err on the side of completeness"). Flag and resolve.

Not all repetition is bloat. Some is **intentional emphasis** that reinforces a critical rule. Decision rule: when a duplicated line states a true invariant (safety, output contract, hard constraint), keep it; when it restates a heuristic in different words, dedupe.

## Gotchas

- **Rewriting working language for style.** Claude rewrites clear, working prompt text for stylistic preference. If existing language is unambiguous and effective, don't touch it.
- **Skipping context discovery when the task seems obvious.** Even "simple" prompt tasks have hidden constraints — force discovery before producing output.
- **Over-engineering simple prompts.** A 3-line prompt doesn't need 10 sections and a validation checklist.
- **Converting principles into rigid rules.** "Stop when converged" becomes "Max 5 iterations." Principles give flexibility; rigid rules create edge cases.
- **Adding examples for behaviors Claude already knows.** Examples earn their place only when they demonstrate non-obvious or counter-intuitive behavior.
