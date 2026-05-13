# Metaprompting

Loaded when an existing prompt fails in production and you want the model to help diagnose and fix it. Different verb from authoring: instead of writing a prompt from scratch, you use a model to inspect a prompt and its failure traces, then propose a surgical revision — the full prompt redelivered with minimal targeted edits.

The shape is two separate calls — diagnose first, revise second. Skipping the diagnosis step (asking directly for a fix) tends to produce vague or shallow rewrites that miss the real cause.

## Pre-flight check — when metaprompting is the wrong tool

- If the prompt is missing a goal or success criteria entirely, no diagnosis call will surface it — fix the gap directly.
- If the model lacks a capability the prompt is asking for (e.g., reliable arithmetic on long numbers, accurate citations without retrieval), no prompt change will fix it — change the architecture.
- If the failure is a single bug from a typo or contradiction visible on a quick read, just fix it.

## Step 1 — Diagnose only

Feed the model the current system prompt plus a small set of logged failures. Ask for root-cause analysis. **Do not ask for a solution yet.** The output is an analysis of which lines of the prompt are causing which observed behaviors.

**Constraints** to include in the diagnosis call:
- Identify distinct failure modes — name and describe each.
- For each failure mode, quote or paraphrase the specific lines of the system prompt likely causing or reinforcing it. Include contradictions (e.g., "be concise" vs. "err on the side of completeness").
- For each failure mode, briefly explain how those lines steer the agent toward the observed behavior.
- Return the analysis in a structured-but-readable format.

**Example diagnosis prompt**:

```
You are a prompt engineer debugging a system prompt for an agent that
[describe agent purpose].

You are given:

1) The current system prompt:
<system_prompt>
[PASTE PROMPT]
</system_prompt>

2) A small set of logged failures. Each entry has:
- query
- tools_called (as actually executed)
- final_answer (shortened if needed)
- eval_signal (rating, comment, or grader judgment)

<failure_traces>
[PASTE TRACES]
</failure_traces>

Tasks:
1) Identify each distinct failure mode (e.g., tool_usage_inconsistency,
   output_length_drift, autonomy_vs_clarification).
2) For each failure mode, quote or paraphrase the specific lines of the
   system prompt most likely causing or reinforcing it. Include any
   contradictions.
3) Briefly explain how those lines are steering the agent toward the
   observed behavior.

Output format:

failure_modes:
- name: ...
  description: ...
  prompt_drivers:
    - line_or_paraphrase: ...
      why_it_matters: ...
```

## Step 2 — Surgical revision

Feed the diagnosis from Step 1 back into a separate call. Ask for a patch — small explicit edits that resolve the issues without rewriting the prompt.

**Constraints** to include in the revision call:
- Do not redesign the agent from scratch.
- Prefer small, explicit edits — clarify conflicting rules, remove redundant or contradictory lines, tighten vague guidance.
- Make tradeoffs explicit (e.g., "when to prioritize concision over completeness", "exactly when tools must vs. must not be called").
- Keep overall structure and length roughly similar to the original, unless a short consolidation removes obvious duplication.

Re-include the original system prompt verbatim in the revision call — Step 2 doesn't inherit context from Step 1.

**Example revision prompt**:

```
You previously analyzed this system prompt and its failure modes.

System prompt:
<system_prompt>
[PASTE PROMPT]
</system_prompt>

Failure-mode analysis:
[PASTE STEP 1 OUTPUT]

Propose a surgical revision of the system prompt that reduces the observed
issues while preserving the good behaviors.

Constraints:
- Do not redesign from scratch.
- Prefer small, explicit edits.
- Make tradeoffs explicit (when to prioritize X over Y, exactly when tool A
  must vs. must not be called).
- Keep structure and length roughly similar to the original, unless a short
  consolidation removes obvious duplication.

Output:
1) patch_notes: a concise list of changes and the reasoning behind each
   (e.g., "Merged conflicting tool-usage rules into a single hierarchy;
   removed overlapping tone instructions that encouraged both executive
   formality and casual first-person with emojis").
2) revised_system_prompt: the full updated system prompt with edits applied,
   ready to drop in.
```

After applying the patch, re-run the failing queries. Repeat the cycle until the failure modes are resolved.

**Don't stack patches.** If a patch creates new failures, restart at Step 1 with the new failure as input — stacking patches obscures the root cause and produces brittle prompts.

**Stop if the cycle isn't converging.** If repeated cycles produce no improvement on the named failure modes, the issue likely isn't a prompt problem. Revisit the pre-flight check at the top of this file — model capability gaps and missing goals don't fix with metaprompting.

## Pitfalls of the metaprompting workflow itself

**Too many failure types in one metaprompt.** When the failure traces span unrelated failure modes (output too long + tool over-eagerness + unit confusion + hallucinated facts, all in one batch), the diagnosis call struggles to connect threads and the patch call produces shallow fixes. Group similar failures and run the cycle separately for each group. One cycle per coherent failure mode.

**Accepting overly specific patch recommendations.** A single patch call may produce edits that fix the specific traces you fed it but generalize poorly — the model overfits to the examples. Run the patch call multiple times and look for changes that appear across runs; those are cross-cutting suggestions. Treat single-run-only suggestions as candidates for a smaller targeted patch rather than the main fix.

## When to add evals

Metaprompting without evals is iteration in the dark. Once a failure mode is named, write the smallest eval that distinguishes the failing behavior from the desired behavior — even a tiny hand-graded set works. Use it to confirm the patch actually helps before merging.
