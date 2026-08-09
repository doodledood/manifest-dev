# Prompt Caching for /do

Cache-aware prompt composition and launch strategy for `per-gate` verifier executions, built on **staggered launch** — the documented, standard way to raise Claude's prompt-cache hit rate: issue a priming call first, then follow-on calls sharing its prefix before the cache entry would otherwise expire. This reference is loaded per *Caching per-gate launches* in `SKILL.md`, only when two or more gates are eligible in the same `per-gate` round and the active harness provides the mechanical substitution below. Caching, where loaded, is unconditional for that round — there is no separate opt-in flag. Below the model's minimum cacheable token threshold, launch order and prompt shape are unchanged and no cache read occurs.

## Why This Differs From a Per-Criterion Cache Group

An earlier design let each criterion declare its own verifier model, so launches had to be partitioned into per-model cache groups before priming made sense. That field no longer exists: `--verifier-model` (or the inherited default) is a single, explicit choice for the whole run. Every `per-gate` launch in a round therefore already targets one cache namespace — there is nothing left to group by model. The only per-launch variable is the gate ID.

## Prompt Shape

Every verifier envelope in a cached round has two parts, in this order:

1. **Shared block** — the envelope content that is identical for every gate in the round: the framing line, the comparison and verdict-contract text, the multi-repo path map (when present), and the manifest's full content substituted verbatim in place of a marker. Byte-identical across every launch in the round. It must literally begin with the manifest's real opening line (e.g. `# Definition: ...`).
2. **Gate ID** — the specific gate this launch evaluates (or, for a consolidated execution, the set — though consolidated has only one execution per round and never benefits from this). Varies per launch; appended last, never woven into the shared block.

The boundary must be clear: everything before the gate ID is the shared block; the gate ID is the only thing after it.

**Forbidden**: substituting a bracketed placeholder or natural-language cross-reference for the shared block — e.g. `"[MANIFEST — same content as the priming call above, reproduced verbatim]"`. These are never compliant, including as a "same as above" shortcut when the priming call already carries the real text: a verifier judges PASS/FAIL only against what is in its own prompt, and a placeholder cannot register as a cache hit against the priming call's write (the cache is prefix-based; a differing prefix is a cache miss). The one sanctioned exception is Claude Code's `{{INLINE_MANIFEST:<snapshot-path>}}` marker (see "Claude Code: mechanical inlining via PreToolUse hook" below) — a `PreToolUse` hook mechanically resolves it to the real manifest text before any subagent ever sees the prompt, so unlike the forbidden forms above, no subagent ever actually judges PASS/FAIL against unresolved placeholder text, and the executor never hand-composes the copy `SKILL.md`'s *Pointing evaluators at the gate* forbids.

A correctly composed prompt does not isolate the shared block into its own content block — the shared block and the gate ID concatenate into a **single** content block with one `cache_control: ephemeral` breakpoint at the end of that block (see Prefix-Based Matching).

Caching does not change what the evaluator is asked to do. It still evaluates one named gate under the same PASS/FAIL/BLOCKED contract; only the transport of the manifest content — pushed by the harness rather than pulled by the evaluator's own read — and the launch order change.

## Cache Mechanics

### Prefix-Based Matching

Claude's prompt cache is prefix-based: the cache key is the content from the start of the prompt up to a breakpoint. Two prompts that share the same prefix hit the same cache entry. Content after the prefix (the gate ID) does not affect cache lookup. The breakpoint sits at the end of the single content block described in Prompt Shape — there is no separate, earlier breakpoint isolating the manifest text alone.

Ordering matters structurally, not just for cost: because the cache key chains from the very first byte, a gate ID stated *before* the shared block would poison the match for every launch in the round, regardless of how identical the shared block is afterward. This is also why the gate ID cannot be resolved by having each evaluator call its own read on the manifest — that read happens only after the evaluator's first turn, and the first turn already differs per launch (it names the gate), so no shared prefix can form.

### Per-Model Cache Isolation

Cache entries are isolated by model. Since a run's `per-gate` launches all resolve to the one run-level verifier model, this holds automatically within a round and needs no active management — see Why This Differs From a Per-Criterion Cache Group.

### Minimum Cacheable Token Thresholds

The shared block must meet the resolved model's minimum cacheable prompt length, which varies by model version rather than by family:

| Minimum Tokens | Models |
|-----------------|--------|
| 512 | Claude Fable 5, Claude Mythos 5 |
| 1,024 | Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5 |
| 2,048 | Claude Opus 4.7 |
| 4,096 | Claude Opus 4.6, Claude Opus 4.5, Claude Haiku 4.5 |

Don't assume by family — Opus alone spans 1,024 to 4,096 tokens depending on version (Opus 4.8 vs. Opus 4.6/4.5). If the manifest is below the resolved model's threshold, caching provides no benefit — launches still proceed in priming-then-parallel order, just without cache reads.

### Cost Multipliers

| Operation | Multiplier |
|-----------|-----------|
| Cache write (priming call) | 1.25x base input token cost |
| Cache read (each real verifier in the round) | 0.1x base input token cost |

The priming call is pure overhead — it produces no verification output, only a cache write on the shared block's tokens. It pays for itself once at least one other real verifier in the round reads the cache instead of independently paying full cost: for a round of 2 eligible gates, uncached cost is `2x`; primed cost is `1.25x + 2(0.1x) = 1.45x`. This is why a round with exactly one eligible gate skips priming entirely (see Launch Strategy) — a lone verifier would pay the 1.25x write premium with no read side to offset it.

### Cache TTL

Cache entries expire after 5 minutes of inactivity. Between fix-verify rounds, the cache may expire if the repair takes longer than 5 minutes. This is expected — the next round's priming call re-primes it.

## Launch Strategy

For each `per-gate` round:

1. **One eligible gate**: launch that gate's verifier directly. No priming call — there's no second launch in the round to read back the cache, so priming would be pure overhead (see Cost Multipliers).
2. **Two or more eligible gates**: launch a dedicated priming call first — the shared block plus a fixed instruction to acknowledge receipt and perform no verification work. There's no signal that exposes "the first launch's response has begun" separately from "the first launch's response has completed" for an ordinary tool-call launch; making the priming call do no real work collapses that distinction, since a no-op reply returns immediately. Wait for the priming call to complete, then launch every real verifier for the round's remaining eligible gates in parallel — each carries the same shared block plus its own gate ID.
3. **Repeat for the next round** (e.g. after a repair cycle re-marks gates eligible).

**Precedence**: This controls prompt shape and launch ordering within the round's parallel execution. It does not restrict parallelism — every real verifier in the round still launches and runs concurrently, just after the round's priming call (if any) completes.

## Prefix Snapshots

For each round, /do builds the shared block from a single immutable snapshot:

1. Determine the round's eligible gates and launch order.
2. Read the manifest exactly once at the start of the round and write it to a frozen per-round snapshot file (a plain copy of that read, not the live manifest path).
3. Compose every verifier prompt in the round — including the priming call — against that snapshot's content as the shared block.

Do not re-read the manifest between launches within a round. The primary reason is correctness, not cache economics: a verifier launched mid-round against a snapshot that an amendment has since changed on disk could pass or fail a gate against wording that no longer matches what's on disk — the same hazard `SKILL.md`'s *Amendments do not land mid-evaluation* names for the uncached default. Reading once and reusing the buffer eliminates that risk within the round. If the manifest changes mid-round, the next round reads a fresh snapshot — its verifiers see the amendment; only the round already in flight when the amendment landed does not.

### Claude Code: mechanical inlining via PreToolUse hook

On Claude Code, the plugin ships a `PreToolUse` hook (`hooks/inline_manifest_hook.py`, registered declaratively via `hooks/hooks.json`) that removes the model from the manifest-reproduction path. Instead of pasting the snapshot's text into the prompt by hand, compose the shared block as the literal marker `{{INLINE_MANIFEST:<snapshot-path>}}` followed by the gate ID. Before the Task tool call reaches the subagent, the hook reads `<snapshot-path>`, substitutes its exact bytes for the marker, and merges the result into `tool_input` (never a bare replacement — replacing would drop `description`/`subagent_type` and break the call). The hook fails closed: if the snapshot file can't be read, it denies the tool call with a reason naming the unreadable path rather than launching a verifier with a dangling marker.

This hook is what makes the substitution executor-blind rather than merely instructed — it is the mechanism `SKILL.md`'s *Caching per-gate launches* requires before this reference is loaded at all. On a harness without a `PreToolUse`-equivalent mechanism, this reference does not apply; `per-gate` launches proceed at their default cost, pointed at the gate by path and ID as usual (see *Pointing evaluators at the gate* in `SKILL.md`) rather than falling back to the executor typing the manifest text in by hand.

## Prerequisites / Maximum Efficiency

To maximize cache effectiveness, eliminate delays between launches within a round. Permission prompts between launches introduce pauses that can exceed the 5-minute cache TTL, wasting the priming call's effect.

Reduce that pause without lowering your permission bar more than necessary:

- **settings.json**: Pre-grant the specific agent tool permissions `/do` needs so launches proceed without interactive approval. This is the safest option — it grants only what's needed.
- **Auto permission mode**: If pre-granting specific permissions isn't practical, run the session in Claude Code's `auto` permission mode rather than a fully permissive one — it still lets subagent launches proceed without interactive prompts while leaving other tool categories gated.

Without one of these, each launch may pause for user approval; in rounds with many eligible gates, cumulative delays can exceed the cache TTL and negate the caching benefit.

## Known Limitations

- **Cross-agent cache sharing is unconfirmed**: the mechanism assumes separate Agent-tool subagent calls share the organization-level prompt cache. If they're isolated per conversation, no cross-agent cache benefit occurs regardless of priming. Check `cache_read_input_tokens` on the API usage dashboard across `/do` runs — if it's consistently zero, the Agent tool likely isolates cache per conversation.
- **Priming overhead on a cache miss**: if cross-agent cache sharing doesn't hold, a multi-gate round still pays the priming call's 1.25x write cost on the shared block's tokens with no offsetting read benefit. This is the realistic worst case, not a catastrophic one — see Cost Multipliers.
- **Verifier-model change invalidates the whole ledger anyway**: `SKILL.md`'s *Reconciling the ledger* already treats a run-level verifier-model change as invalidating the active gate ledger, so there is no separate cache-specific invalidation rule to track here.

## Validation Procedure

To check whether caching is helping on your own manifests:

1. Run `/do` on a manifest where a `per-gate` round has several eligible gates.
2. After the run completes, check the **API usage dashboard** for the organization.
3. Look for `cache_read_input_tokens` in the usage breakdown. Non-zero values indicate cache hits.
4. Compare total input token cost on a round with one eligible gate vs. one with several. The multi-gate round should show lower per-gate input token cost, proportional to the shared block's size and the number of gates in the round.
5. If `cache_read_input_tokens` is consistently zero across multiple runs, cross-agent cache sharing may not be supported by the Agent tool — see Known Limitations.
