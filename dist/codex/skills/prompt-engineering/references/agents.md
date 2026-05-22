# Writing an agent

Agents run in isolation. They don't inherit the parent's conversation context, the parent's loaded files, or the parent's tool permissions. The spawn prompt is the agent's entire world.

This isolation creates two specific gaps that natural model behavior won't close on its own.

## Tool declarations

An agent only has the tools listed in its `tools:` frontmatter. If the agent's job needs Bash, Read, Grep, Edit, WebFetch — every one of those must appear. Missing tools don't produce a graceful fallback; the agent simply can't perform that action.

Audit: read what the agent does step by step. For every capability mentioned in the prompt (explicit or implicit), check it has the matching tool. Common implicit needs:

- *"Search the codebase"* → Grep, Glob, or Bash
- *"Read this file"* → Read
- *"Make a change"* → Edit or Write
- *"Run the tests"* → Bash
- *"Look up the docs"* → WebFetch or WebSearch
- *"Spawn a subagent"* → TaskCreate
- *"Invoke a skill"* → Skill or SlashCommand
- *"Write a progress log"* → Write

Omit `tools:` entirely to inherit the parent's tool set — useful for general-purpose agents where the parent's permissions are appropriate.

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
tools: Bash, Read, Grep, …   # explicit list, or omit to inherit
model: inherit               # optional; inherit, opus, sonnet, haiku
---
```

## Gotchas

- **Forgetting tools the prompt implicitly needs.** An agent told to "report findings to a log file" without `Write` in `tools:` will fail silently or hallucinate the write.
- **Briefing the agent as if it has parent context.** *"As we discussed, …"* is meaningless to an agent that doesn't see the parent's conversation.
- **Spawning agents for trivial work.** If the parent could do the task in two tool calls, the spawn overhead is wasted. Reserve agents for genuinely parallel or genuinely independent work, or for protecting the parent's context from large result sets.
