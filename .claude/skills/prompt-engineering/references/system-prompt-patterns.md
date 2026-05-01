# System Prompt Patterns

Loaded when filling non-trivial sections of the canonical template. Each pattern names *when* it earns its place, *what* it does, and gives a concrete example you can adapt. These are techniques, not architectural sections — they slot into Constraints, Success criteria, Output, or Stop rules in the canonical template.

## End-of-run verification

**When to apply** — the prompt drives an agent that produces high-impact or irreversible actions (commits, deletes, deploys) or evidence-grounded output where requirement misses, ungrounded claims, or format drift would cause real damage.

**What it does** — adds a lightweight self-check pass after the workflow looks complete, before the irreversible step. Catches requirement misses, ungrounded factual claims, and schema drift before they ship.

**Example** (place inside Constraints or just above Stop rules):

```
Before any final answer or irreversible step, run a self-check:
does the output cover what the user asked? Are the factual claims grounded
in tool output, retrieved content, or supplied context — not memory? Does
the format match what was requested? If the next action has external
consequences, narrate the action plus its parameters and pause for confirm.

If any check fails, revise before continuing — never paper over a gap.
```

## Per-action narrate-execute-confirm

**When to apply** — agents that mutate external state with each tool call (file writes, API calls, deploys). Sibling pattern to end-of-run verification, not a substitute. Use both for high-impact agents: per-action for the running discipline, end-of-run for final coverage.

**What it does** — applies a tight discipline to every state-changing tool call so each mutation is observable and recoverable.

**Example** (place inside Constraints):

```
Treat every state-changing tool call as narrate → execute → confirm. The
narrate step states what you're about to do and the inputs. The confirm
step states the outcome and what you checked. Skip neither.
```

## Tool-call escalation rule

**When to apply** — the prompt drives an agent with search, retrieval, or tool-loop access. Without a budget, agents over-tool ("just one more search") inflating latency and cost without improving correctness, or under-tool when it matters.

**What it does** — names the conditions under which another tool call is warranted, and the conditions under which it isn't. Replaces "use tools when needed" (vague — model errs in both directions) with a decision rule the model can apply.

**Example** (place inside Constraints):

```
Default to the smallest number of searches that answers the question.

When current results don't answer the core question, a required fact
(id, date, source) is missing, the user asked for comparison or
exhaustive coverage, or a named artifact must be opened — escalate
with another search. Otherwise, stop and answer.

When you'd search to polish phrasing, add decorative citations, or
support generic wording — don't.
```

Adapt verbs (`retrieval`, `search`, `tool`) to the agent's available tools. The principle is *escalate-on-condition*, not a fixed cap.

## Output contract

**When to apply** — the consumer of the output has specific needs (audience, length, structure, voice) and the default "produce a good answer" leads to walls of text, missing structure, or wrong register.

**What it does** — names the audience, the length envelope, the structural choices, and the editing posture (improve vs. preserve) up front. Output drift often resolves at this layer alone — try this before adding constraints elsewhere.

**Example for a generation task** (place inside Output):

```
Audience: senior engineers reviewing a pull request. Familiar with the codebase
conventions; unfamiliar with this specific change.

Length: short enough to read in one sitting. Conclusion first, reasoning second,
caveats last.

Structure: short paragraphs. Use bullets only for lists of three or more
parallel items. Headers only when the answer covers more than one topic.
```

**Example for an editing task** (place inside Output):

```
Preserve the original artifact's length, structure, voice, and genre. Quietly
improve clarity, flow, and correctness. Do not add new claims, new sections,
or a more promotional tone unless explicitly asked.
```

## Ambiguity handling

**When to apply** — the prompt receives free-form user input that may be under-specified, ambiguous, or assume facts the model can't verify (recent prices, current policies, internal context).

**What it does** — gives the model a deterministic rule for when to ask versus when to interpret. The default behavior — silently picking one interpretation — is the worst option; this pattern chooses between two better options and tells the model which one applies.

**Example** (place inside Constraints or Success criteria):

```
When the request is ambiguous or underspecified:
- Ask the smallest number of precise clarifying questions that resolve
  material ambiguity — typically one or two — when missing information
  would materially change the answer or the chosen action.
- Otherwise present the most likely plausible interpretations with explicit
  assumptions, and answer the most likely one. Label the assumptions.

When external facts may have changed and tools are not available:
- Answer in general terms and state that details may have changed since
  the model's training cutoff. Do not invent figures, dates, or sources.

When uncertain, prefer "based on the provided context …" to absolute claims.
```

## High-risk self-check

**When to apply** — the prompt operates in legal, financial, medical, compliance, or safety-sensitive contexts where an overstated claim or unstated assumption causes real harm.

**What it does** — adds a final scan for the specific failure modes that hurt in high-risk domains: ungrounded numbers, hidden assumptions, overstrong language. Doesn't replace domain validation; reduces the rate of obvious tells.

**Example** (place inside Constraints or just above Stop rules):

```
Before returning an answer in a legal, financial, compliance, medical, or
safety-sensitive context, scan the response for:
- Specific numbers or claims not grounded in the provided context.
- Unstated assumptions the user may not share.
- Overly strong language ("always", "guaranteed", "never").

Soften or qualify any of the above and state assumptions explicitly. If a
claim cannot be grounded, replace it with a description of what would need
to be checked.
```

## Decision rules (alternative to absolutes)

**When to apply** — anywhere a constraint involves a judgment call: when to search, when to ask, when to retry, when to escalate, when to use tool A versus tool B. Absolutes (MUST / NEVER / ALWAYS) on judgment calls produce brittle behavior — either over-fires or under-fires depending on phrasing.

**What it does** — replaces the absolute with an explicit conditional. The model gets a real rule to evaluate instead of a vague directive.

**Examples** (replace the absolute with the rule):

```
Bad:  Always ask the user before making assumptions.
Rule: When a missing piece of information would materially change the chosen
      action, ask. When the missing piece is recoverable from a sensible
      default (and the user can correct course later), proceed and label
      the assumption.

Bad:  Never use tools for simple questions.
Rule: For factual questions about specific entities (people, companies,
      products) prefer tools. For conceptual or definitional questions
      ("how does X work in general") answer from internal knowledge.

Bad:  Always be concise.
Rule: For status updates and acknowledgements: one or two sentences.
      For explanations and recommendations: as long as needed for the user
      to act with confidence.

Bad:  Always cite sources.
Rule: Cite sources for any factual claim about specific entities, prices,
      dates, identifiers, or quoted text. Conceptual statements and
      methodology do not need citation.
```

Reserve absolutes for true invariants — see the "Decision rules over absolutes" cross-cutting principle in SKILL.md for the canonical statement.

---

These patterns compose — pick by failure mode, not by category. Add them where they apply, not speculatively.
