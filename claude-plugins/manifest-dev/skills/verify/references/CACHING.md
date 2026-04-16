# Prompt Caching for /verify

Cache-aware prompt composition and launch strategies for verification agents. Reduces input token costs by structuring agent prompts with shared static prefixes that hit Claude's prompt cache.

## Cache Strategies

| Strategy | Shared Prefix | Launch Behavior | Warmup |
|----------|--------------|-----------------|--------|
| `none` | No shared prefix — prompts composed per current behavior | All verifiers launched per mode parallelism rules | No warmup agent |
| `manifest` | Manifest content inlined as static prefix | Grouped by (agent_type, model), staggered launch within groups | Warmup agent checks threshold |
| `max` | Manifest content + execution log inlined as static prefix | Grouped by (agent_type, model), staggered launch within groups | Warmup agent checks threshold |

### `none` (Default)

No caching behavior. Prompts are composed and agents are launched exactly as they would be without the `--cache` flag. This is the baseline — no behavioral change from current /verify.

### `manifest`

Inlines the full manifest content as a static prefix in every agent prompt within a cache group. The manifest is identical across all agents, so after the first agent in a group begins responding, subsequent agents in that group hit the cached prefix (90% input token savings on the shared portion).

### `max`

Inlines both the manifest content AND the execution log as a static prefix. The execution log provides richer context for verifiers (prior attempt history, fix rationale). The log must follow the **append-only constraint** (see below) to preserve the cached prefix across fix-verify cycles.

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
| Sonnet | 2,048 |
| Haiku | 4,096 |

If the shared prefix is below the target model's threshold, caching provides no benefit. The warmup agent checks this and recommends `--cache none` or a model with a lower threshold when applicable.

### Cost Multipliers

| Operation | Multiplier |
|-----------|-----------|
| Cache write (first agent) | 1.25x base input token cost |
| Cache read (subsequent agents) | 0.1x base input token cost |

The first agent in a group pays a 25% write premium. All subsequent agents in the group pay only 10% of the base cost for the cached portion. Break-even occurs at 2 agents per group.

### Concurrent Request Constraint

A cache entry becomes available only after the first response begins. Launching all agents simultaneously means none benefit from caching — each writes its own cache entry independently. This is why staggered launch within groups is required.

### Cache TTL

Cache entries expire after 5 minutes of inactivity. Between fix-verify cycles, the cache may expire if the fix takes longer than 5 minutes. This is expected — the next verify cycle re-primes the cache with the first agent in each group.

## Grouping Strategy

Criteria are partitioned into **cache groups** by the tuple `(agent_type, model)`:

- `agent_type`: The verification agent used — `criteria-checker` (default), or a named subagent (e.g., `prompt-reviewer`, `change-intent-reviewer`)
- `model`: The resolved model for the criterion — `inherit` (session model) or an explicit model override

### Why Named Subagents Form Separate Groups

Named subagents (e.g., `prompt-reviewer`) have different system prompts than `criteria-checker`. Since the system prompt is part of the prefix, agents with different system prompts cannot share cache entries. Each named subagent type forms its own group.

### Why Model Overrides Create Cache Boundaries

Per-model cache isolation means a criterion with `model: sonnet` cannot share cache with a criterion using `model: inherit` (when inherit resolves to opus). Grouping by model ensures all agents in a group target the same cache namespace.

### Efficient Mode Model Upgrades

In efficient mode, criteria-checker agents start on haiku. After 2 failures on the same criterion, the mode upgrades to the inherited (session) model. This upgrade moves the criterion from the `(criteria-checker, haiku)` cache group to `(criteria-checker, inherit)` — a different cache namespace. The remaining haiku-group agents are unaffected, but the upgraded criterion no longer benefits from the haiku group's cached prefix.

### Example Grouping

Given criteria with these verification configs:
- AC-1.1: method=codebase (criteria-checker, inherit)
- AC-1.2: method=codebase (criteria-checker, inherit)
- INV-G5: method=subagent, agent=prompt-reviewer (inherit)
- INV-G6: method=subagent, agent=change-intent-reviewer (inherit)
- AC-6.2: method=subagent, agent=docs-reviewer (inherit)

Groups:
1. `(criteria-checker, inherit)`: AC-1.1, AC-1.2
2. `(prompt-reviewer, inherit)`: INV-G5
3. `(change-intent-reviewer, inherit)`: INV-G6
4. `(docs-reviewer, inherit)`: AC-6.2

Groups with only one criterion still benefit from system prompt + tools caching (automatic by Claude Code), but not from shared manifest prefix caching.

## Launch Strategy (manifest and max modes)

Within each cache group:

1. **Launch the first agent** in the group and wait for its response to begin (not complete — just begin, confirming the cache write has occurred).
2. **Launch remaining agents** in the group. They share the cached prefix from the first agent.
3. **Process the next group** — repeat steps 1-2.

Groups themselves can be launched concurrently when they target different models (their caches are isolated, so no ordering benefit). Groups targeting the same model should be launched sequentially to maximize cross-group cache hits on the system prompt + tools portion.

**Precedence**: When `--cache` is `manifest` or `max`, this launch strategy overrides the execution mode's parallelism rules. The mode defines how many verifiers to launch concurrently; caching overrides this with group-aware staggered launch to ensure cache hits. The mode's parallelism resumes for `--cache none`.

## Append-Only Log Constraint (max mode)

When using `max` mode, the execution log is part of the shared prefix. For the cached prefix to remain valid across fix-verify cycles:

- The execution log must **only grow** — new entries are appended to the end.
- Earlier portions of the log must **never be modified** (no edits, no deletions, no reordering).
- If earlier log content is modified, the prefix changes and all cache entries are invalidated — every agent pays the full cache-write cost again.

This constraint applies only during `max` mode. In `manifest` mode, the log is not part of the prefix and can be modified freely.

## Warmup Failure Fallback

If the warmup agent crashes, times out, or returns an error:

1. Log the failure (agent error, timeout, or unparseable output).
2. Downgrade to `--cache none` behavior.
3. Proceed with verification using standard (non-cached) prompt composition and mode-defined parallelism.

Verification must never be blocked by a warmup failure. The warmup agent is an optimization — its failure means we lose potential savings, not that verification cannot proceed.

## Prerequisites / Maximum Efficiency

To maximize cache effectiveness, eliminate delays between agent launches within a group. Permission prompts between launches introduce pauses that can exceed the 5-minute cache TTL, wasting the first agent's cache-priming effect.

**Pre-grant agent tool permissions** using one of:

- **settings.json**: Add agent tool permissions to your Claude Code settings so launches proceed without interactive approval
- **--dangerously-skip-permissions**: Run Claude Code with this flag to bypass all permission prompts (appropriate for CI or trusted environments)

Without pre-granted permissions, each agent launch may pause for user approval. In groups with many agents, cumulative delays can exceed the cache TTL, negating the caching benefit.

## Known Limitations

- **Named subagent cache isolation**: Each named subagent type has a unique system prompt, preventing cross-type cache sharing. A manifest with many distinct named subagents (e.g., 5 different reviewer types) gets minimal grouping benefit.
- **Model switch invalidation**: Changing the session model between fix-verify cycles invalidates all `inherit`-model cache entries, since `inherit` resolves to a different model.
- **Minimum token threshold failures**: Small manifests may fall below the minimum cacheable threshold. The warmup agent detects this and recommends `--cache none`.
- **Cross-agent cache sharing is speculative (R-4)**: The entire mechanism assumes that separate Agent tool conversations share the organization-level prompt cache, per Anthropic's documentation of cache scope. If Agent tool conversations are isolated (each gets its own cache namespace), no cross-agent cache benefit occurs. This requires empirical validation — check the API usage dashboard for `cache_read_input_tokens` across cached verify runs. If consistently zero, the Agent tool likely isolates cache per conversation.

## Validation Procedure

To verify caching is working:

1. Run `/verify` with `--cache manifest` or `--cache max` on a manifest with multiple criteria sharing the same (agent_type, model) group.
2. After the run completes, check the **API usage dashboard** for the organization.
3. Look for `cache_read_input_tokens` in the usage breakdown. Non-zero values indicate cache hits.
4. Compare total input token costs between a `--cache none` run and a `--cache manifest` run on the same manifest. The cached run should show lower input token costs proportional to the shared prefix size and number of agents per group.
5. If `cache_read_input_tokens` is consistently zero across multiple cached runs, cross-agent cache sharing may not be supported by the Agent tool — see Known Limitations (R-4).
