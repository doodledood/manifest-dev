# Writing an agent

Agents run in isolation. They don't inherit the parent's conversation context, the parent's loaded files, or the parent's tool permissions. The spawn prompt is the agent's entire world.

This isolation creates two specific gaps that natural model behavior won't close on its own.

## Capability declarations

An agent only has the capabilities granted by its frontmatter or harness config. If the job needs command execution, file reading, code search, editing, web/doc lookup, subagent launch, skill invocation, or progress-log writing, the current harness's corresponding capability must be declared. Missing capabilities don't produce a graceful fallback; the agent simply can't perform that action.

Audit: read what the agent does step by step. For every capability mentioned in the prompt (explicit or implicit), check it has the matching declaration. Common implicit needs:

- *"Search the codebase"* requires code search capability
- *"Read this file"* requires file-read capability
- *"Make a change"* requires file-edit capability
- *"Run the tests"* requires command execution
- *"Look up the docs"* requires web or documentation lookup
- *"Spawn a subagent"* requires subagent launch capability
- *"Invoke a skill"* requires skill invocation capability
- *"Write a progress log"* requires file-write capability

Use the current harness's inheritance mechanism when a general-purpose agent should share the parent's permissions.

## Context passing

Because the agent starts fresh, anything it needs to know — the question, the relevant file paths, the constraints, the user's prior decisions — must be in the spawn prompt. The agent has no memory of the parent's conversation, no view of the parent's loaded files, no access to "what the user said earlier."

This is the opposite of how you'd brief a coworker who's been listening to the meeting. Brief the agent like someone who just walked in: state the goal, the inputs, the relevant facts, the constraints, the expected output shape. If the parent learned something the agent needs (a path, a decision, a constraint), pass it explicitly.

Brevity in the spawn prompt is a false economy. The agent can't ask the parent for clarification — what it doesn't know in the prompt, it doesn't know.

## Output shape

Agents return a single message back to the parent. If the parent needs structured data (a list of files, a verdict, a score), say so in the spawn prompt and show the shape. If the parent needs a short summary, say "under 200 words." Without explicit shape, agents tend to over-narrate.

## Frontmatter

```yaml
---
name: agent-name             # required
description: '…'              # required, used in the agent listing
tools: …                     # optional harness-specific capability list
model: inherit               # optional, harness-specific
---
```

## Gotchas

- **Forgetting capabilities the prompt implicitly needs.** An agent told to "report findings to a log file" without file-write capability will fail silently or hallucinate the write.
- **Briefing the agent as if it has parent context.** *"As we discussed, …"* is meaningless to an agent that doesn't see the parent's conversation.
- **Spawning agents for trivial work.** If the parent could do the task in two tool calls, the spawn overhead is wasted. Reserve agents for genuinely parallel or genuinely independent work, or for protecting the parent's context from large result sets.
