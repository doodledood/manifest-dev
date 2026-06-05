# Patterns

A library of techniques that close specific recurring gaps. Each pattern names the *gap* it closes, what it does, and a concrete shape to adapt. These are not architectural sections — they slot into Constraints, Success, Output, or Stop in a system prompt; into a skill's body where the gap applies; or into an agent's spawn prompt where the agent will hit the failure mode otherwise.

Pick by gap, not by category. Don't add a pattern speculatively — only when the gap it closes is real for this prompt.

## End-of-run verification

**Gap** — the prompt drives an agent producing high-impact or irreversible actions (commits, deletes, deploys) or evidence-grounded output where requirement misses, ungrounded claims, or format drift would cause real damage.

**What it does** — adds a self-check pass after the work looks complete, before the irreversible step. Catches requirement misses, ungrounded claims, and schema drift before they ship.

```
Before any final answer or irreversible step, run a self-check:
does the output cover what the user asked? Are factual claims grounded
in tool output, retrieved content, or supplied context — not memory?
Does the format match what was requested? If the next action has
external consequences, narrate the action plus its parameters and pause
for confirm.

If any check fails, revise before continuing — never paper over a gap.
```

## Per-action narrate-execute-confirm

**Gap** — agents that mutate external state with each tool call (file writes, API calls, deploys) lose recoverability when actions go un-narrated.

**What it does** — applies a tight discipline to every state-changing tool call so each mutation is observable and recoverable. Sibling to end-of-run verification, not a substitute — use both for high-impact agents.

```
Treat every state-changing tool call as narrate → execute → confirm.
The narrate step states what you're about to do and the inputs.
The confirm step states the outcome and what you checked.
Skip neither.
```

## Tool-call escalation rule

**Gap** — agents with search, retrieval, or tool-loop access over-tool ("just one more search") or under-tool depending on phrasing, inflating latency without improving correctness.

**What it does** — names the conditions under which another tool call is warranted and the conditions under which it isn't. Replaces "use tools when needed" (vague — model errs in both directions) with a decision rule the model can apply.

```
Default to the smallest number of searches that answers the question.

Escalate with another search when current results don't answer the core
question, a required fact (id, date, source) is missing, the user asked
for comparison or exhaustive coverage, or a named artifact must be
opened. Otherwise, stop and answer.

Don't search to polish phrasing, add decorative citations, or support
generic wording.
```

Adapt the verbs to the agent's actual tools. The principle is *escalate-on-condition*, not a fixed cap.

## Output contract

**Gap** — the consumer of the output has specific needs (audience, length, structure, voice) and the default "produce a good answer" leads to walls of text, missing structure, or wrong register.

**What it does** — names audience, length envelope, structural choices, and editing posture (improve vs preserve) up front. Output drift often resolves here alone — try this before adding constraints elsewhere.

For a generation task:

```
Audience: senior engineers reviewing a pull request. Familiar with
codebase conventions; unfamiliar with this specific change.

Length: short enough to read in one sitting. Conclusion first,
reasoning second, caveats last.

Structure: short paragraphs. Use bullets only for lists of three or
more parallel items. Headers only when the answer covers more than
one topic.
```

For an editing task:

```
Preserve the original artifact's length, structure, voice, and genre.
Quietly improve clarity, flow, and correctness. Do not add new claims,
new sections, or a more promotional tone unless explicitly asked.
```

## Ambiguity handling

**Gap** — the prompt receives free-form input that may be under-specified, ambiguous, or assume facts the model can't verify. The default behavior (silently picking one interpretation) is the worst option.

**What it does** — gives the model a deterministic rule for when to ask versus when to interpret.

```
When the request is ambiguous or underspecified:
- Ask the smallest number of precise clarifying questions that resolve
  material ambiguity — typically one or two — when missing information
  would materially change the answer or the chosen action.
- Otherwise present the most likely plausible interpretation with
  explicit assumptions, and answer it. Label the assumptions.

When external facts may have changed and tools aren't available:
- Answer in general terms and note that details may have changed since
  the model's training cutoff. Do not invent figures, dates, or sources.

When uncertain, prefer "based on the provided context …" to absolute
claims.
```

## High-risk self-check

**Gap** — the prompt operates in legal, financial, medical, compliance, or safety-sensitive contexts where an overstated claim or unstated assumption causes real harm.

**What it does** — adds a final scan for the failure modes specific to high-risk domains: ungrounded numbers, hidden assumptions, overstrong language. Doesn't replace domain validation; reduces the rate of obvious tells.

```
Before returning an answer in a legal, financial, compliance, medical,
or safety-sensitive context, scan the response for:
- Specific numbers or claims not grounded in the provided context.
- Unstated assumptions the user may not share.
- Overly strong language ("always", "guaranteed", "never").

Soften or qualify any of the above and state assumptions explicitly.
If a claim cannot be grounded, replace it with a description of what
would need to be checked.
```

## Decision rules over absolutes

**Gap** — anywhere a constraint involves a judgment call (when to search, when to ask, when to retry, when to use tool A vs B). Absolutes (MUST / NEVER / ALWAYS) on judgment calls over-fire or under-fire depending on phrasing.

**What it does** — replaces the absolute with an explicit conditional. The model gets a real rule to evaluate.

```
Bad:  Always ask the user before making assumptions.
Rule: When a missing piece of information would materially change the
      chosen action, ask. When it's recoverable from a sensible default
      (and the user can correct course later), proceed and label the
      assumption.

Bad:  Never use tools for simple questions.
Rule: For factual questions about specific entities (people, companies,
      products) prefer tools. For conceptual or definitional questions
      ("how does X work in general") answer from internal knowledge.

Bad:  Always be concise.
Rule: For status updates and acknowledgements: one or two sentences.
      For explanations and recommendations: as long as needed for the
      user to act with confidence.

Bad:  Always cite sources.
Rule: Cite sources for any factual claim about specific entities,
      prices, dates, identifiers, or quoted text. Conceptual statements
      and methodology do not need citation.
```

Reserve absolutes for true invariants — safety rules, output contracts, hard constraints.

## Emotional tone

**Gap** — prompts that activate high-arousal emotional context produce predictable misalignments. Urgency framing ("CRITICAL", "you MUST do this NOW") and excessive praise both shift the model's behavior in measurable ways (sycophancy from positive arousal; corner-cutting and reward-hacking from negative arousal).

**What it does** — keeps the model's emotional context calibrated for trusted-advisor behavior: honest, capable, willing to push back, not desperate.

- Avoid urgency framing, all-caps imperatives, and pressure language. Ordinary modal usage ("must hold", "should return") is fine.
- Avoid excessive praise ("you're amazing at this") and high-stakes framing ("this is critical to my career"). The model reads semantic intensity, not surface keywords.
- For iterative or agentic prompts, normalize failure: *"if this approach doesn't work, try another"* prevents accumulated desperation from driving corner-cutting.
- The emotional tone of the opening propagates through subsequent processing — calibrate early tokens, not just the closing.

---

These patterns compose — pick by gap, not by category. Add them where the gap is real for this prompt, not speculatively.
