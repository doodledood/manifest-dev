# Interview Mode: Collaborative

Co-discovery through transparent brainstorming. Model shares findings with reasoning as they emerge, building shared understanding. User contributes naturally when they have relevant context.

## Decision Authority

Shared. The model explores, shares what it finds with reasoning, and the user contributes when they have relevant context. Structured options lock decisions — but understanding is built together through transparent discussion before locking.

## Question Format

Two interaction types:

1. **Transparent sharing** — Share findings, reasoning, and emerging patterns as you discover them. "I'm seeing X in the codebase, which suggests Y. This connects to Z because..." This builds shared understanding of the problem space.

2. **Decision locking** — When a finding needs to become a manifest item, present structured options to lock the decision. Only lock after sufficient shared understanding.

Don't front-load options before the user understands the problem space. Share the finding and reasoning first, then lock. This applies equally to Resolvable task file structures — share the structure and its relevance transparently, then lock the disposition with structured options.

**Scenario presentation**: Share your reasoning transparently before presenting options:

- Weak: "How should we handle rate limits?" → Options: A, B, C, D
- Strong: "I'm seeing external API calls in the payment flow. In production, these could hit rate limits — especially during peak hours when order volume spikes. The failure mode would be orders silently dropping. Given this..." → Options: "Real risk - add to invariants (Recommended)", "Not possible in our setup", "Already handled", "Out of scope"

The transparent reasoning helps the user recognize whether the scenario applies from their domain knowledge, and contribute context you don't have.

## Interview Flow

Protocols are interleaved, not sequential. Findings from one protocol naturally trigger exploration in another:

- Domain grounding reveals a constraint → immediately explore what could go wrong (pre-mortem)
- A pre-mortem scenario surfaces a dependency → check if it holds (backcasting)
- Outside view pattern connects to something found in domain grounding → share the connection

Follow the thread of understanding wherever it leads. The protocols are lenses to apply, not phases to complete. The goal is collaborative understanding so the manifest arises in its best state through the collaboration.

## Checkpoint Behavior

After resolving a cluster of related topics, synthesize the current understanding and invite contribution:

"Here's where we are on [topic area]: [summary of findings, decisions, and open questions]. What am I missing? Does this match what you're seeing?"

Checkpoints serve two purposes: catch interpretation drift AND expand the problem space by inviting the user's domain knowledge. Keep them focused on the current sub-topic — don't summarize everything at once.

## Finding Sharing

Share findings with reasoning as they emerge — don't wait to present conclusions. The user should see your thinking:

- "I found X in the codebase. This is interesting because Y, and it connects to what you said about Z."
- "Looking at similar projects, the common failure mode is X. In our case, this would manifest as Y because of [domain-specific reason]."

Then offer choices for how to encode: "Should this be a hard constraint, or is it more of a known assumption?" with structured options.

## Convergence

Converge when shared understanding is deep enough that both parties are confident. Apply SKILL.md's convergence checklist, but the signal is mutual confidence — the user understands the problem space well enough to validate the manifest, and you've incorporated their domain knowledge into the findings.

Move to synthesis when further exploration would yield diminishing returns for shared understanding. The user can signal "enough" at any point.
