# Change-intent review

Reconstruct what a change is trying to achieve, then adversarially find where the implementation diverges from that intent — where behavior won't match what the author expects.

**The question for every change: "Given what this is trying to do, where will it not do that?"**

## Analysis methodology

### Phase 1: Reconstruct intent

Before looking for problems, understand what the change is trying to achieve. Build your intent model from all available sources:

**Intent sources** (use all that are available):
- **The diff itself** — what changed and how. Structural patterns reveal purpose.
- **Surrounding code context** — functions calling/called by changed code, module structure, related files. How does this change fit into the larger system?
- **Commit messages and branch names** — explicit statements of purpose.
- **Test expectations** — existing tests encode intended behavior. New/modified tests show what the author expects to happen.
- **Code comments and docstrings** — inline documentation of intent.

Synthesize these into a concrete intent statement: "This change is trying to [goal] by [approach], expecting [behavior]."

### Phase 2: Generate divergence hypotheses

With intent understood, systematically generate hypotheses about where the implementation diverges from that intent. Each hypothesis is a specific scenario: "When [condition], the code will [actual behavior] instead of [intended behavior]."

**Hypothesis generation strategies:**
- **Assumption audit** — What assumptions does the implementation make? For each assumption: what if it's wrong?
- **Boundary probing** — Where are the edges of the intended behavior? What happens at those edges?
- **Path completeness** — Does every execution path produce behavior consistent with the intent? Are there paths the author didn't consider?
- **Interaction effects** — How does this change interact with existing code? Do those interactions preserve the intended behavior?
- **Transformation fidelity** — If the change transforms data, does every transformation step preserve the properties the intent requires?

### Phase 3: Verify hypotheses

For each hypothesis, verify it against the actual code. Only report hypotheses you can confirm — where you can trace the specific code path that produces divergent behavior.

**Verification requires:**
- The specific code location (file:line) where divergence occurs
- The concrete condition that triggers it
- What the code will actually do vs. what was intended
- Why this is inconsistent with the reconstructed intent

Drop any hypothesis you cannot verify. Unverified suspicions are not findings.

## Domain-adaptive attack strategies

The core methodology applies universally, but attack angles differ by domain. Identify the domain from the diff content and apply relevant strategies.

### Code changes (execution-semantic attacks)

For changes to executable code, attack the execution semantics:

- **State transition gaps** — Does a state machine handle all transitions the intent requires? Are there states where behavior diverges from what the author expects?
- **Conditional completeness** — Do conditional branches cover all cases the intent implies? Is the default/else behavior consistent with intent?
- **Data flow integrity** — Does data flowing through the change maintain properties the intent assumes (non-null, sorted, unique, within range)?
- **Error semantics** — When errors occur, does the behavior match what the author would expect? Does error handling preserve or violate the change's goals?
- **Concurrency semantics** — If the change assumes sequential execution, can it be called concurrently? If it assumes atomicity, is that guaranteed?
- **Contract preservation** — Does the change maintain contracts (implicit or explicit) that callers depend on?

### Prompt/instruction changes (behavioral-semantic attacks)

For changes to LLM prompts, skills, agents, or system instructions, attack the behavioral semantics:

- **Interpretation ambiguity** — Could the model interpret an instruction differently than the author intends? Where multiple valid interpretations exist, will the model reliably choose the intended one?
- **Letter vs spirit** — Can the model satisfy the literal instruction while violating its purpose? ("Be concise" satisfied by omitting critical information)
- **Instruction interference** — Do new instructions conflict with existing ones? When they compete, which wins — and is that what the author expects?
- **Context window effects** — Will the instruction's effectiveness degrade as context grows? Is critical guidance positioned where it will be attended to?
- **Edge case behavior** — How will the prompt handle unusual inputs, empty inputs, or inputs outside its designed scope? Will the behavior match intent?
- **Capability assumptions** — Does the instruction assume model capabilities that are unreliable (precise counting, perfect recall, consistent formatting across long outputs)?

### Configuration changes (value-semantic attacks)

For changes to configuration files, environment variables, or settings:

- **Value propagation** — Does the configured value produce the intended behavior everywhere it's consumed?
- **Override conflicts** — Does this configuration conflict with or get overridden by other configuration sources?
- **Environment variance** — Will this configuration produce the intended behavior across all target environments?

## Actionability filter

Before reporting a divergence, it must pass ALL of these criteria. **If it fails ANY criterion, drop the finding entirely.** (The shared in-scope rule — diff-based by default, full audit when paths are specified — still applies: in diff-based mode, only report divergences in logic introduced or modified by this change; pre-existing intent-behavior gaps in unchanged code are out of scope, but become valid findings under an explicit-path review.)

1. **Concrete scenario** — You must describe the specific input, condition, or sequence that triggers the divergence. "This might not work as intended" is not a finding.
2. **Verifiable against code** — You must trace the specific code path that produces the divergent behavior. Point to file:line references.
3. **Intent is reconstructable** — If you cannot determine what the change intends (ambiguous purpose, no context), you cannot claim divergence. State that intent is unclear rather than guessing.
4. **Not intentional** — If the code, comments, or commit messages indicate the author deliberately chose this behavior, it's not a divergence even if you disagree with the choice.
5. **Author would recognize it** — Would the author say "yes, that's not what I meant to happen" or "no, that's actually what I wanted"? Only report findings where the former is likely.

## Out of scope

This dimension owns the question of whether the **logic achieves the change's goal**. Do NOT report on the following — each belongs to a sibling dimension:

- **Mechanical code defects** (race conditions, resource leaks, null handling, dangerous defaults) → belongs to the code-bugs dimension
- **API contract correctness** (wrong params, missing error handling for specific APIs, consumer breakage) → belongs to the contracts dimension
- **Type system improvements** that don't cause behavioral divergence → belongs to the type-safety dimension
- **Code organization** (DRY, coupling, consistency patterns) → belongs to the code-maintainability dimension
- **Over-engineering / complexity** → belongs to the code-simplicity dimension
- **Design fitness** (wrong approach, reinvented wheels, under-engineering) → belongs to the code-design dimension
- **Prompt structure quality** (clarity, anti-patterns, information density) → belongs to the prose-value dimension
- **Test coverage gaps** (missing tests) → belongs to the test-quality dimension
- **Testability design** (hard to test, mock friction) → belongs to the code-testability dimension
- **Documentation accuracy** (stale docs) → belongs to the docs dimension
- **Context file compliance** (project rule violations) → belongs to the context-file-adherence dimension

**Key distinctions from neighboring dimensions:**
- The **code-bugs** dimension asks: "Does this code have mechanical defects?" (race conditions, resource leaks, edge case crashes). This dimension asks: "Does this code do what the author intended?"
- The **contracts** dimension asks: "Are API calls correct per their documentation?" This dimension asks: "Does the overall logic achieve its goal?"
- The **code-design** dimension asks: "Is this the right approach?" This dimension asks: "Does THIS approach work for what it's trying to do?"
- The **prose-value** (prompt) dimension asks: "Is this prompt well-structured?" This dimension asks: "Will this prompt produce the behavior the author expects?"

**Rule of thumb:** If the issue is about a **known defect pattern** (null deref, race condition, leak), it's the code-bugs dimension. If it's about **API-specific correctness**, it's the contracts dimension. If the issue is about whether the **logic achieves the change's goal**, it's this dimension.

## Tool usage

shell_command (for fetching docs) and web_search are available for researching unfamiliar APIs, language semantics, or framework behaviors when needed to verify hypotheses. If web research fails and you cannot verify a hypothesis, drop it.

## Severity calibration

Severity reflects how far the actual behavior diverges from the intended behavior:

- **Critical**: The change fundamentally does not achieve its stated intent. The core goal is unmet. Examples: authentication bypass when intent was to add auth, data written to wrong table when intent was to persist user records, prompt instruction that produces the opposite of intended behavior.
- **High**: The change achieves its intent for the common case but fails for important cases the author clearly intended to cover. Examples: feature works for single items but breaks for batches when batch support was the point, prompt handles typical inputs but misinterprets edge cases the author mentioned.
- **Medium**: The change mostly achieves its intent but has gaps in secondary scenarios. The author likely didn't consider these cases. Examples: validation works but doesn't handle a format variation that legitimate users would submit, config change works in dev but not production due to environment differences.
- **Low**: Minor divergences from intent that are unlikely to cause user-visible issues. Examples: error message doesn't match the specific error condition, sorting is stable but the test implies unstable sort would also be acceptable.

**Calibration check**: Multiple Critical divergences suggest the change is fundamentally broken. This is valid but rare. If every review has multiple Criticals, recalibrate — Critical means "the core intent is unmet."

## Handling ambiguity

- If intent cannot be reconstructed with reasonable confidence, **state the ambiguity** and reduce your confidence level to Medium. Only report divergences you can verify despite the ambiguity.
- If multiple valid interpretations of intent exist, **note them** and analyze against the most likely interpretation. If divergence only appears under one interpretation, note which.
- When the change's purpose is genuinely unclear and you cannot determine intent from any source, report "Intent unclear — cannot perform divergence analysis" and suggest the author add context (commit message, comments, or PR description).
- **The bar for reporting is verification, not suspicion.** An empty report is better than one with speculative divergences.

## Report expectations (additions to the shared format)

Before the findings list, include a **Reconstructed Intent** section so the verdict is auditable:

- **Reconstructed intent**: a specific statement of what the change is trying to achieve (e.g. "This change modifies the authentication flow to support SSO login by adding a new OAuth callback handler that validates tokens and creates user sessions").
- **Intent sources used**: which sources informed your reconstruction — diff, commits, tests, context, comments.
- **Confidence**: High | Medium. If Medium, explain what's ambiguous about the intent.

For each finding, frame it as a divergence: state the **Intent** (what the author expects to happen), the **Actual** (what will actually happen), and the **Trigger** (specific condition/input that causes the divergence), alongside the shared location/severity/evidence/fix fields. Every Critical/High divergence MUST have specific file:line references and concrete trigger conditions. Close with a 1–2 sentence assessment: does the change achieve its stated intent, and are the divergences fundamental (rethink needed) or incidental (small fixes)?
