# Coverage Goals

Five goals that must be met before convergence. Each defines WHAT must be true and a convergence test. Items resolved from any source (conversation, prior research, task files, exploration) count equally.

**In amendment context**, coverage goals apply scoped to the change — not the full manifest. Existing manifest content satisfies goals for unchanged areas.

## Domain Understanding

**What must be true:** You understand the affected area well enough to generate project-specific failure scenarios — not generic ones. You know existing patterns, structure, constraints, and prior decisions relevant to the task.

Understanding comes from any source — conversation context, prior research, code exploration, documentation, user-provided arguments, task files. Don't re-discover what's already known. When understanding is insufficient, fill gaps through whatever means fits the domain — explore code, search docs, ask the user what exploration can't reveal. Scope to what's relevant, not the entire domain.

**What to assess:**
- **Existing patterns** — how similar things are currently done
- **Structure** — components, dependencies, boundaries in the affected area
- **Constraints** — implicit conventions, assumed invariants, existing contracts
- **Prior decisions** — why things are the way they are, when discoverable

**Convergence test:** Can you generate failure scenarios that reference specific components, patterns, or conventions in this context? If yes, sufficient. If only generic failures, gaps remain.

## Reference Class Awareness

**What must be true:** You know what type of task this is, what typically fails in that class, and those base-rate failures inform your failure mode coverage.

Ground the reference class in domain understanding — "refactor of a tightly-coupled module with no tests" is useful; "refactor" is too generic. The reference class should be specific enough that its failure patterns are actionable. Task file warnings are a source.

**Convergence test:** Can you name the reference class and its most common failure modes? Often satisfiable in a single assessment step.

## Failure Mode Coverage

**What must be true:** Failure modes have been anticipated with concrete scenarios, and each has a disposition — encoded as criterion, explicitly scoped out, or mitigated by approach. No dangling scenarios. Mental model alignment checked — your understanding of "done" matches the user's expectation.

**Failure dimensions** — lenses for generating scenarios when gaps exist:

| Dimension | What to imagine |
|-----------|-----------------|
| **Technical** | What breaks at the code/system level? |
| **Integration** | What breaks at boundaries? |
| **Stakeholder** | What causes rejection even if technically correct? |
| **Timing** | What fails later that works now? |
| **Edge cases** | What inputs/conditions weren't considered? |
| **Dependencies** | What external factors cause failure? |

Task files add domain-specific failure scenarios. Scenarios grounded in domain understanding are higher signal than generic templates.

**Scenario disposition** — every scenario resolves to one of:
1. **Encoded as criterion** — becomes INV-G*, AC-*, or Risk Area with detection
2. **Explicitly out of scope** — user confirmed it's acceptable risk
3. **Mitigated by approach** — architecture choice eliminates the failure mode

The active interview mode defines how scenarios are presented and dispositions resolved.

**Convergence test:** Relevant failure dimensions considered, all scenarios have dispositions, and user confirms no major failure modes were missed.

## Positive Dependency Coverage

**What must be true:** Load-bearing assumptions — what must go right for the task to succeed — are surfaced and each is resolved: verified, encoded as invariant, or logged as Known Assumption.

Where failure mode coverage asks "what broke?", positive dependencies ask "what held?" This reveals assumptions you haven't examined.

**What to assess:**
- What existing infrastructure/tooling are you relying on?
- What user behavior are you assuming?
- What needs to stay stable that could change?

The active interview mode defines how dependencies are presented and resolved.

**Convergence test:** Load-bearing assumptions surfaced and each has a disposition.

## Process Self-Audit

**What must be true:** Process self-sabotage patterns — decisions that look reasonable individually but compound into failure — are identified and resolved. **Skip for simple tasks.**

Patterns to watch:
- Small scope additions ("just one more thing")
- Edge cases deferred ("we'll handle that later")
- "Temporary" solutions that become permanent
- Process shortcuts that erode quality

For each pattern, resolve its disposition — add as Process Guidance, encode as verifiable Invariant, accept as low risk, or note it's already covered. The active interview mode defines how patterns are presented and resolved.

**Convergence test:** Complex tasks (per SKILL.md Complexity Triage) have process risks identified and resolved. Simple tasks can skip this goal entirely.
