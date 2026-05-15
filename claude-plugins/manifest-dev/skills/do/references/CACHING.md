# Prompt Caching for /do

Cache-aware prompt composition and launch strategies for verifier subagents. Reduces input token costs by structuring agent prompts with a shared static prefix (the manifest) that hits Claude's prompt cache. Always on — there is no opt-in flag. When the manifest is below the model's minimum cacheable token threshold, caching silently doesn't activate; launch order and prompt shape are unchanged.

## Prompt Shape

Every verifier prompt has two parts, in this order:

1. **Shared static prefix** — the full manifest content, inlined verbatim. Byte-identical across all agents within a model cache group.
2. **Per-criterion data** — the criterion's `verify.prompt:` field. Varies per agent; never reaches into the prefix.

The boundary between prefix and per-criterion data must be clear. Everything before the criterion-specific content is cached; everything after is unique per agent.

## Cache Mechanics

### Prefix-Based Matching

Claude's prompt cache is prefix-based: the cache key is the content from the start of the prompt up to a breakpoint. Two prompts that share the same prefix hit the same cache entry. Content after the prefix (per-criterion data) does not affect cache lookup.

### Per-Model Cache Isolation

Cache entries are isolated by model. An Opus agent's cached prefix is not available to a Sonnet agent, even if the prefix content is identical. This is why grouping by model is required — mixing models in a group wastes the first agent's cache-priming effect.

### Minimum Cacheable Token Thresholds

The shared prefix must meet minimum token counts to be cached:

| Model | Minimum Tokens |
|-------|---------------|
| Opus | 4,096 |
| Sonnet | 1,024 |
| Haiku | 4,096 |

If the manifest prefix is below the target model's threshold, caching provides no benefit — agents launch in the same grouped order, just without cache reads. No fallback flag is needed; the cache silently doesn't activate.

### Cost Multipliers

| Operation | Multiplier |
|-----------|-----------|
| Cache write (first agent) | 1.25x base input token cost |
| Cache read (subsequent agents) | 0.1x base input token cost |

The first agent in a group pays a 25% write premium. All subsequent agents in the group pay only 10% of the base cost for the cached portion. Break-even occurs at 2 agents per group.

### Concurrent Request Constraint

A cache entry becomes available only after the first response begins. Launching all agents simultaneously means none benefit from caching — each writes its own cache entry independently. This is why staggered launch within groups is required. Parallelism helps most after the first response begins, but it is not the caching contract; the contract is stable-prefix requests issued close together.

### Cache TTL

Cache entries expire after 5 minutes of inactivity. Between fix-verify cycles, the cache may expire if the fix takes longer than 5 minutes. This is expected — the next verify cycle re-primes the cache with the first agent in each group.

## Grouping Strategy

All verifiers are general-purpose subagents (there is no `verify.agent` field). Criteria are partitioned into **cache groups** by resolved `model`:

- `model`: The resolved model for the criterion — value of `verify.model:` (default: inherit from session)

### Why Model Overrides Create Cache Boundaries

Per-model cache isolation means a criterion with `model: sonnet` cannot share cache with a criterion using `model: inherit` (when inherit resolves to opus). Grouping by model ensures all agents in a group target the same cache namespace.

### Example Grouping

Given criteria with these verify blocks:
- AC-1.1: (no model) → `inherit`
- AC-1.2: (no model) → `inherit`
- INV-G5: (no model) → `inherit`
- INV-G6: `model: sonnet` → `sonnet`
- AC-6.2: (no model) → `inherit`

Groups:
1. `inherit`: AC-1.1, AC-1.2, INV-G5, AC-6.2
2. `sonnet`: INV-G6

Groups with only one criterion still benefit from system prompt + tools caching (automatic by Claude Code), but not from shared manifest prefix caching.

## Launch Strategy

Within each phase, for each cache group:

1. **Launch the first agent** in the group and wait for its response to begin (not complete — just begin, confirming the cache write has occurred).
2. **Launch remaining agents** in the group in parallel. They share the cached prefix from the first agent.
3. **Repeat for the next group.**

Groups themselves can be launched concurrently when they target different models (their caches are isolated, so no ordering benefit between groups). Groups targeting the same model should launch sequentially to maximize cross-group cache hits on the system prompt + tools portion.

**Precedence**: Cache grouping controls prompt shape and launch ordering within the phase's parallel execution. It does not restrict parallelism — all criteria within a phase can still run concurrently, just in the staggered order above.

## Prefix Snapshots

For each phase, /do builds the shared prefix from a single immutable snapshot:

1. Determine criteria, cache groups, and launch order for the current phase.
2. Read the manifest exactly once at the start of the phase.
3. Reuse that exact content as the first prompt content for every verifier prompt in the phase.

Do not re-read the manifest between verifier launches. This prevents accidental prefix drift from in-phase edits. If the manifest changes mid-phase (e.g., a Self-Amendment cycle triggered by user feedback), the next phase reads a fresh snapshot — paying one cache miss is cheap relative to the alternative of queueing user feedback for the entire verify chain.

## Prerequisites / Maximum Efficiency

To maximize cache effectiveness, eliminate delays between agent launches within a group. Permission prompts between launches introduce pauses that can exceed the 5-minute cache TTL, wasting the first agent's cache-priming effect.

**Pre-grant agent tool permissions** using one of:

- **settings.json**: Add agent tool permissions to your Claude Code settings so launches proceed without interactive approval
- **--dangerously-skip-permissions**: Run Claude Code with this flag to bypass all permission prompts (appropriate for CI or trusted environments)

Without pre-granted permissions, each agent launch may pause for user approval. In groups with many agents, cumulative delays can exceed the cache TTL, negating the caching benefit.

## Known Limitations

- **All verifiers share system prompt**: Since all verifiers are general-purpose subagents, cache grouping is purely by model. Manifests with many criteria in the same model group get maximum cache benefit.
- **Model switch invalidation**: Changing the session model between fix-verify cycles invalidates all `inherit`-model cache entries, since `inherit` resolves to a different model.
- **Cross-agent cache sharing is speculative**: The mechanism assumes that separate Agent tool conversations share the organization-level prompt cache, per Anthropic's documentation of cache scope. If Agent tool conversations are isolated (each gets its own cache namespace), no cross-agent cache benefit occurs. This requires empirical validation — check the API usage dashboard for `cache_read_input_tokens` across /do runs. If consistently zero, the Agent tool likely isolates cache per conversation.

## Validation Procedure

To verify caching is working:

1. Run `/do` on a manifest with multiple criteria sharing the same model group.
2. After the run completes, check the **API usage dashboard** for the organization.
3. Look for `cache_read_input_tokens` in the usage breakdown. Non-zero values indicate cache hits.
4. Compare total input token costs on a manifest with a single criterion vs. one with several criteria in the same group. The multi-criterion run should show lower per-criterion input token cost proportional to the shared prefix size and number of agents per group.
5. If `cache_read_input_tokens` is consistently zero across multiple runs, cross-agent cache sharing may not be supported by the Agent tool — see Known Limitations.
