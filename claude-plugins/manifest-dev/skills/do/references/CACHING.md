# Prompt Caching for /do

Cache-aware prompt composition and launch strategy for verifier subagents, built on **staggered launch** — the documented, standard way to raise Claude's prompt-cache hit rate: issue a priming call first, then follow-on calls sharing its prefix before the cache entry would otherwise expire. Caching is unconditional — there is no opt-in flag. Below the model's minimum cacheable token threshold, launch order and prompt shape are unchanged and no cache read occurs.

Internal benchmarking during development showed a ~28% reduction in input-token cost, a figure that held across two separate benchmark runs. Treat this as a directional result, not a guarantee — see Validation Procedure to check the effect on your own manifests.

## Prompt Shape

Every verifier prompt has two parts, in this order:

1. **Shared block** — the full manifest content, inlined verbatim. Byte-identical across all agents within a `verify.model` group.
2. **Per-criterion data** — the criterion's `verify.prompt:` field. Varies per agent; never reaches into the shared block.

The boundary must be clear: everything before the criterion-specific content is the shared block; everything after is unique per agent.

## Cache Mechanics

### Prefix-Based Matching

Claude's prompt cache is prefix-based: the cache key is the content from the start of the prompt up to a breakpoint. Two prompts that share the same prefix hit the same cache entry. Content after the prefix (per-criterion data) does not affect cache lookup.

### Per-Model Cache Isolation

Cache entries are isolated by model. An Opus agent's cached prefix is not available to a Sonnet agent, even if the prefix content is identical. This is why grouping by model is required — mixing models in a group wastes the priming call's effect.

### Minimum Cacheable Token Thresholds

The shared block must meet the resolved model's minimum cacheable prompt length, which varies by model version rather than by family:

| Minimum Tokens | Models |
|-----------------|--------|
| 512 | Claude Fable 5, Claude Mythos 5 |
| 1,024 | Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5 |
| 2,048 | Claude Opus 4.7 |
| 4,096 | Claude Opus 4.6, Claude Opus 4.5, Claude Haiku 4.5 |

Don't assume by family — Opus alone spans 1,024 to 4,096 tokens depending on version (Opus 4.8 vs. Opus 4.6/4.5). If the manifest is below the resolved model's threshold, caching provides no benefit — agents still launch in the grouped order, just without cache reads.

### Cost Multipliers

| Operation | Multiplier |
|-----------|-----------|
| Cache write (priming call) | 1.25x base input token cost |
| Cache read (each real verifier in the group) | 0.1x base input token cost |

The priming call is pure overhead — it produces no verification output, only a cache write on the manifest tokens. It pays for itself once at least one other real verifier in the group reads the cache instead of each independently paying full cost: for a group of 2, uncached cost is `2x`; primed cost is `1.25x + 2(0.1x) = 1.45x`. This is why groups of exactly one criterion skip priming entirely (see Grouping Strategy) — a lone verifier would pay the 1.25x write premium with no read side to offset it.

### Cache TTL

Cache entries expire after 5 minutes of inactivity. Between fix-verify cycles, the cache may expire if the fix takes longer than 5 minutes. This is expected — the next verify cycle re-primes the cache.

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

Groups with only one criterion still benefit from system prompt + tools caching (automatic by Claude Code), but skip manifest-prefix priming — see Launch Strategy.

## Launch Strategy

Within each phase, for each cache group:

1. **Groups of one criterion**: launch that criterion's verifier directly. No priming call — there's no second agent in the group to read back the cache, so priming would be pure overhead (see Cost Multipliers).
2. **Groups of two or more criteria**: launch a dedicated priming call first — the shared manifest block plus a fixed instruction to acknowledge receipt and perform no verification work. There's no signal that exposes "the first agent's response has begun" separately from "the first agent's response has completed" for an ordinary tool-call launch; making the priming call do no real work collapses that distinction, since a no-op reply returns immediately. Wait for the priming call to complete, then launch every real verifier in the group in parallel — each carries the same manifest block plus its own `verify.prompt:`.
3. **Repeat for the next group.**

Groups themselves can be launched concurrently when they target different models (their caches are isolated, so no ordering benefit between groups). Groups targeting the same model should launch sequentially to maximize cross-group cache hits on the system prompt + tools portion.

**Precedence**: Cache grouping controls prompt shape and launch ordering within the phase's parallel execution. It does not restrict parallelism — all real verifiers within a group still launch and run concurrently, just after the group's priming call (if any) completes.

## Prefix Snapshots

For each phase, /do builds the shared block from a single immutable snapshot:

1. Determine criteria, cache groups, and launch order for the current phase.
2. Read the manifest exactly once at the start of the phase.
3. Reuse that exact content as the shared block for every verifier prompt — including the priming call — in the phase.

Do not re-read the manifest between verifier launches. The primary reason is correctness, not cache economics: a verifier launched mid-phase against a snapshot that a Self-Amendment cycle has since changed on disk could pass or fail a criterion against wording that no longer matches what's on disk. Reading once and reusing the buffer eliminates that risk within a phase. If the manifest changes mid-phase, the next phase reads a fresh snapshot — its verifiers see the amendment; only the phase already in flight when the amendment landed does not.

## Prerequisites / Maximum Efficiency

To maximize cache effectiveness, eliminate delays between agent launches within a group. Permission prompts between launches introduce pauses that can exceed the 5-minute cache TTL, wasting the priming call's effect.

Reduce that pause without lowering your permission bar more than necessary:

- **settings.json**: Pre-grant the specific agent tool permissions `/do` needs so launches proceed without interactive approval. This is the safest option — it grants only what's needed.
- **Auto permission mode**: If pre-granting specific permissions isn't practical, run the session in Claude Code's `auto` permission mode rather than a fully permissive one — it still lets subagent launches proceed without interactive prompts while leaving other tool categories gated.

Without one of these, each agent launch may pause for user approval; in groups with many agents, cumulative delays can exceed the cache TTL and negate the caching benefit.

## Known Limitations

- **Cross-agent cache sharing is unconfirmed**: the mechanism assumes separate Agent-tool subagent calls share the organization-level prompt cache. If they're isolated per conversation, no cross-agent cache benefit occurs regardless of grouping or priming. Check `cache_read_input_tokens` on the API usage dashboard across `/do` runs — if it's consistently zero, the Agent tool likely isolates cache per conversation.
- **Priming overhead on a cache miss**: if cross-agent cache sharing doesn't hold, a multi-criterion group still pays the priming call's 1.25x write cost on the manifest tokens with no offsetting read benefit. This is the realistic worst case, not a catastrophic one — see Cost Multipliers.
- **Model switch invalidation**: changing the session model between fix-verify cycles invalidates all `inherit`-model cache entries, since `inherit` resolves to a different model.

## Validation Procedure

To verify caching is working on your own manifests, rather than relying on the ~28% figure above:

1. Run `/do` on a manifest with multiple criteria sharing the same model group.
2. After the run completes, check the **API usage dashboard** for the organization.
3. Look for `cache_read_input_tokens` in the usage breakdown. Non-zero values indicate cache hits.
4. Compare total input token costs on a manifest with a single criterion vs. one with several criteria in the same group. The multi-criterion run should show lower per-criterion input token cost proportional to the shared block's size and the number of agents per group.
5. If `cache_read_input_tokens` is consistently zero across multiple runs, cross-agent cache sharing may not be supported by the Agent tool — see Known Limitations.
