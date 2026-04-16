# Definition: Prompt Caching Mechanism for /verify

## 1. Intent & Context
- **Goal:** Add cache-aware prompt composition and launch strategies to `/verify` so that multiple verification agents share cached context, reducing input token costs by up to 82% on large manifests.
- **Mental Model:** Claude's prompt cache is prefix-based with a 5-minute TTL. Cache entries are per-model, per-organization, and only available after the first response begins. By structuring agent prompts with a shared static prefix (manifest content) and launching agents in cache-aware order (not all at once), subsequent agents get 90% input token savings on the shared portion. A dedicated warmup agent primes the cache and gauges whether the context meets minimum cacheable token thresholds.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local
- **Cache:** max

## 2. Approach

- **Architecture:**
  - New reference file `skills/verify/references/CACHING.md` — single source of truth for caching mechanics, strategies, and prerequisites
  - New warmup agent `agents/cache-warmup.md` — context gauge + strategy recommender that primes the cache as side effect
  - Modified `/verify` SKILL.md — `--cache` kwarg, cache-aware prompt composition, warmup step, grouped launch strategy
  - Modified `/define` SKILL.md — `cache:` field in manifest Intent schema
  - Modified `/do` SKILL.md — reads `cache:` from manifest, passes `--cache` to /verify

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5 → D6
  - Rationale: D1 is the knowledge foundation. D2 is referenced by D3. D3 is the core mechanism. D4 and D5 are integration points. D6 is housekeeping after all content exists.

- **Risk Areas:**
  - [R-1] Caching mechanics not verifiable from skill level — can't confirm cache hits from prompts | Detect: warmup agent reports context size but actual cache behavior is opaque
  - [R-2] Cache strategy overriding execution mode parallelism causes confusion — mode says "parallel" but --cache says "batched" | Detect: contradictory launch behavior in execution log
  - [R-3] Agent tool block structure is opaque — we infer but can't verify how Claude Code structures API calls internally | Detect: cache savings lower than expected in practice
  - [R-4] Cross-agent cache sharing may not work via Agent tool — the entire mechanism assumes separate Agent tool conversations share organization-level cache, per Anthropic docs. If Agent tool conversations are isolated, no cross-agent cache benefit occurs. | Detect: consistently zero cache_read_input_tokens in API usage dashboard across cached verify runs. Document that the mechanism is speculative on this point and requires empirical validation.

- **Trade-offs:**
  - [T-1] Cache savings vs launch latency → Prefer savings when user opts in via --cache
  - [T-2] Reference file thoroughness vs brevity → Prefer thorough (complex mechanics need clear documentation)
  - [T-3] Warmup agent intelligence vs simplicity → Prefer intelligence (strategy recommendation justifies the agent call cost)

## 3. Global Invariants (The Constitution)

- [INV-G1] Description: Default behavior (`--cache none`) must produce identical verification results and launch patterns as the current /verify without `--cache` — no behavioral regression when caching is not opted into
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Verify that --cache none (the default) produces no behavioral changes compared to the current verify SKILL.md. Check that all launch patterns, prompt composition, and routing remain identical when --cache is absent or set to none."
  ```

- [INV-G2] Description: The shared cached prefix must contain only static content — no timestamps, run IDs, agent-generated commentary, or any content that varies between agents within a single verify run
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md and verify SKILL.md for any instructions that would place dynamic content (timestamps, run IDs, per-criterion data, commentary) in the shared prefix portion of agent prompts. The prefix must be byte-identical across all agents in a group."
  ```

- [INV-G3] Description: Warmup agent failure must not block verification — /verify must fall back to `--cache none` behavior and proceed normally
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for explicit fallback handling when the warmup agent crashes, times out, or returns an error. Must downgrade to --cache none and continue verification."
  ```

- [INV-G4] Description: Cache strategy must not silently override execution mode parallelism — when --cache changes launch behavior from what the mode specifies, the precedence rule must be explicit and documented
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md and verify SKILL.md for explicit precedence rules between --cache strategy and execution mode parallelism. Must state that --cache takes precedence over mode parallelism when active."
  ```

- [INV-G5] Description: All changes pass prompt quality review — no ambiguous instructions, no conflicting rules, clear hierarchy, information-dense
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review all modified and new files in skills/verify/, skills/do/, skills/define/, and agents/ for prompt quality. Focus on: clarity of caching instructions, no contradictions between CACHING.md and SKILL.md sections, no prescriptive HOW language, and structural coherence."
  ```

- [INV-G6] Description: All changes pass intent analysis — changes achieve stated purpose without behavioral divergence
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Analyze all changed files. Intent: add opt-in prompt caching to /verify with --cache none|manifest|max, warmup agent, grouped launch strategy, and manifest/do integration. Check for behavioral divergences from this intent."
  ```

- [INV-G7] Description: Requirements traceability — every specified requirement maps to implementation, nothing lost between manifest and deliverables
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: inherit
    prompt: "Cross-reference this manifest's acceptance criteria against the actual file changes. Every requirement (--cache kwarg, warmup agent, grouping, permissions note, manifest field, /do passthrough, R-4 documentation) must map to a concrete implementation. Report any requirements not covered by changes."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] High-signal changes only — every modification must address a real caching failure mode or integration requirement. Don't add speculative features or handle hypothetical edge cases.
- [PG-2] Permissions pre-granting for maximum efficiency — note in CACHING.md that pre-granting agent tool permissions (via settings.json or --dangerously-skip-permissions) eliminates permission-prompt delays between batched agent launches, maximizing cache TTL utilization.
- [PG-3] When --cache overrides mode parallelism, document the precedence explicitly — users must understand that opting into caching changes their launch pattern.
- [PG-4] (auto) The warmup agent definition should follow the "Description as trigger" pattern — description is a trigger specification, not a summary.
- [PG-5] (auto) Reference file uses progressive disclosure — CACHING.md contains mechanics details, SKILL.md has a brief pointer section.
- [PG-6] Scope boundary — caching mechanism only. Do not add non-caching features to /verify, /do, or /define during this task. Changes to these files are limited to cache: field, --cache kwarg, and cache-aware launch/composition.

## 5. Known Assumptions

- [ASM-1] Claude Code's automatic caching behavior persists and places cache breakpoints at system prompt and tool definition boundaries | Default: current behavior continues | Impact if wrong: system prompt + tools not cached, reduces but doesn't eliminate benefit
- [ASM-2] Per-model cache isolation continues — different models never share cache | Default: current behavior per Anthropic docs | Impact if wrong: grouping by model becomes unnecessary (harmless over-optimization)
- [ASM-3] Minimum cacheable token thresholds remain at current levels (Opus: 4096, Sonnet: 2048, Haiku: 4096) | Default: current thresholds | Impact if wrong: warmup agent's threshold table becomes stale — update the reference file
- [ASM-4] We cannot control cache breakpoint placement through the Agent tool — Claude Code manages breakpoints automatically | Default: inferred from Agent tool API (not directly verified) | Impact if wrong: could add explicit breakpoints for finer-grained caching — a beneficial surprise

## 6. Deliverables (The Work)

### Deliverable 1: Caching Reference File
*New file: `claude-plugins/manifest-dev/skills/verify/references/CACHING.md`*

**Acceptance Criteria:**
- [AC-1.1] Description: Documents three cache strategies (`none`, `manifest`, `max`) with clear descriptions of what each does — shared prefix content, launch behavior, and warmup behavior
  ```yaml
  verify:
    method: codebase
    prompt: "Check skills/verify/references/CACHING.md for documentation of all three cache strategies (none, manifest, max). Each must describe: what content is inlined as shared prefix, launch ordering behavior, and warmup agent behavior."
  ```

- [AC-1.2] Description: Documents cache mechanics relevant to /verify — prefix matching, per-model isolation, minimum cacheable token thresholds per model, cache write/read cost multipliers, and the 'response must begin before cache is available' constraint
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for: prefix-based matching explanation, per-model cache isolation, minimum token thresholds table (Opus 4096, Sonnet 2048, Haiku 4096), cost multipliers (write 1.25x, read 0.1x), and the concurrent request constraint."
  ```

- [AC-1.3] Description: Documents the grouping strategy — criteria partitioned by (agent_type, model) tuples, with explanation of why named subagents and model-upgraded criteria form separate cache groups
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for grouping strategy documentation. Must describe (agent_type, model) partitioning, why named subagents form separate groups, and how efficient mode's model upgrade creates a cache boundary."
  ```

- [AC-1.4] Description: Contains a Prerequisites/Maximum Efficiency section documenting that permissions should be pre-granted via settings.json or --dangerously-skip-permissions to eliminate permission-prompt delays between batched launches
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for a section about pre-granting permissions. Must mention both settings.json and --dangerously-skip-permissions as methods, and explain why permission prompts between launches reduce cache effectiveness."
  ```

- [AC-1.5] Description: Documents the append-only constraint for `max` mode — execution log content must only grow (never modify earlier portions) to preserve cached prefix across fix-verify cycles
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for documentation of the append-only log constraint in max mode. Must explain why earlier prefix stays cached when log appends, and what breaks if earlier log content is modified."
  ```

- [AC-1.6] Description: Documents warmup failure fallback — if warmup agent crashes, /verify downgrades to --cache none and proceeds
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for warmup failure handling documentation. Must state fallback to --cache none on warmup crash/timeout/error."
  ```

- [AC-1.7] Description: Documents known limitations — named subagent cache isolation, model switch invalidation, minimum token threshold failures, and R-4 (cross-agent cache sharing is speculative, requires empirical validation)
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for a known limitations section covering: named subagent cache isolation, model switch invalidation, minimum token threshold failures, and that cross-agent cache sharing via Agent tool is speculative and requires empirical validation."
  ```

- [AC-1.8] Description: Documents a manual validation procedure for verifying caching effectiveness — checking API usage dashboard for cache_read_input_tokens after cached verify runs
  ```yaml
  verify:
    method: codebase
    prompt: "Check CACHING.md for a validation procedure section. Must describe how to verify caching is working by checking API usage dashboard for cache_read_input_tokens."
  ```

### Deliverable 2: Warmup Agent Definition
*New file: `claude-plugins/manifest-dev/agents/cache-warmup.md`*

**Acceptance Criteria:**
- [AC-2.1] Description: Agent definition with name, description (trigger-pattern: what + when + triggers), and tools declared (Read and Bash — Bash required for token counting API call)
  ```yaml
  verify:
    method: codebase
    prompt: "Check agents/cache-warmup.md for valid agent frontmatter: name, description following trigger pattern (what + when + triggers), and tools list including both Read and Bash."
  ```

- [AC-2.2] Description: Agent reads the shared context (manifest content, optionally execution log for max mode), calls the Claude token counting API (`POST /v1/messages/count_tokens` via curl with `$ANTHROPIC_API_KEY`) to get an accurate token count, falls back to character estimation (1 token per 3–4 chars) if the API call fails or `ANTHROPIC_API_KEY` is unset, and compares result against the target model's minimum cacheable threshold
  ```yaml
  verify:
    method: codebase
    prompt: "Check agents/cache-warmup.md for instructions to: read manifest content, optionally read execution log, call the token counting API (POST /v1/messages/count_tokens) via curl to get an accurate count, fall back to character estimation if the API call fails or ANTHROPIC_API_KEY is unset, and compare result against model-specific minimum thresholds."
  ```

- [AC-2.3] Description: Agent recommends cache strategy override when context is below threshold — including suggesting a model with a lower minimum (e.g., Sonnet 2048 vs Opus 4096) when applicable
  ```yaml
  verify:
    method: codebase
    prompt: "Check agents/cache-warmup.md for strategy recommendation logic: when below threshold, suggest --cache none or suggest switching to a model with lower minimum. Must reference specific model thresholds."
  ```

- [AC-2.4] Description: Agent returns structured output that /verify can parse — recommended strategy, token count labeled "exact" (API-sourced) or "estimated" (fallback), model threshold, and whether caching is effective
  ```yaml
  verify:
    method: codebase
    prompt: "Check agents/cache-warmup.md for a defined output format. Must include: recommended strategy, token count labeled 'exact' (from API) or 'estimated' (from fallback), model threshold, and effectiveness assessment."
  ```

### Deliverable 3: Verify SKILL.md Updates
*Modified file: `claude-plugins/manifest-dev/skills/verify/SKILL.md`*

**Acceptance Criteria:**
- [AC-3.1] Description: Parses `--cache none|manifest|max` from arguments. Default: `none`. Invalid value produces error and halts (consistent with --mode behavior): "Invalid cache strategy '<value>'. Valid strategies: none | manifest | max". *(Amended: manifest cache: fallback removed — /do handles passthrough via AC-5.1)*
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for --cache argument parsing. Must: accept none|manifest|max, default to none, error and halt on invalid values with specific error message format."
  ```

- [AC-3.2] Description: When --cache is `manifest` or `max`, /verify loads CACHING.md reference file and follows its rules for warmup, prompt composition, grouping, and launch strategy
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for a section that loads references/CACHING.md when --cache is manifest or max."
  ```

- [AC-3.3] Description: Cache-aware prompt composition — when caching is active, agent prompts are structured with shared static prefix (manifest content, optionally execution log for max) first, followed by per-criterion data. Prefix must be byte-identical across all agents in a group.
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for cache-aware prompt composition rules. Must describe: shared prefix first (manifest, optionally log for max), per-criterion data last, byte-identical prefix within groups."
  ```

- [AC-3.4] Description: Warmup step — before launching real verifiers, spawn the cache-warmup agent with the shared context and target model. Use its recommendation to potentially override the cache strategy. On warmup failure, fall back to --cache none.
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for warmup step: spawn cache-warmup agent, pass shared context and model, consume recommendation, override strategy if recommended, fall back to none on failure."
  ```

- [AC-3.5] Description: Grouped launch strategy — criteria partitioned by (agent_type, model), launched in cache-aware order within each group. First agent in each group must start responding before remaining agents launch.
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for grouped launch: partition by (agent_type, model), first agent response before rest launch within each group."
  ```

- [AC-3.6] Description: When --cache is active, /verify logs cache strategy, grouping decisions, and launch order to the execution log for observability
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for instructions to log cache strategy, groups, and launch order when --cache is active."
  ```

- [AC-3.7] Description: Explicit precedence rule — --cache launch strategy overrides execution mode parallelism when active. Stated clearly so there is no ambiguity.
  ```yaml
  verify:
    method: codebase
    prompt: "Check verify SKILL.md for explicit precedence: --cache overrides execution mode parallelism when manifest or max."
  ```

### Deliverable 4: Manifest Schema Update (/define)
*Modified file: `claude-plugins/manifest-dev/skills/define/SKILL.md`*

**Acceptance Criteria:**
- [AC-4.1] Description: Manifest schema template includes `cache:` field in Intent section with format `none | manifest | max`, marked optional with default `none`
  ```yaml
  verify:
    method: codebase
    prompt: "Check define SKILL.md's manifest schema template for a cache: field in Intent section. Must show none|manifest|max, be optional, default to none."
  ```

- [AC-4.2] Description: Brief comment explains cache: controls caching intensity during /verify
  ```yaml
  verify:
    method: codebase
    prompt: "Check define SKILL.md for a description of the cache: field explaining it controls caching intensity during /verify."
  ```

### Deliverable 5: /do Passthrough
*Modified file: `claude-plugins/manifest-dev/skills/do/SKILL.md`*

**Acceptance Criteria:**
- [AC-5.1] Description: /do reads `cache:` from manifest Intent section and passes as `--cache <value>` when invoking /verify. When absent, does not pass --cache.
  ```yaml
  verify:
    method: codebase
    prompt: "Check do SKILL.md for instructions to read cache: from manifest and pass as --cache to /verify. When absent, must not pass --cache."
  ```

- [AC-5.2] Description: The /verify invocation example in /do's constraints is updated to show --cache as optional parameter
  ```yaml
  verify:
    method: codebase
    prompt: "Check do SKILL.md's constraints section for /verify invocation example including --cache as optional parameter."
  ```

### Deliverable 6: Housekeeping (READMEs + Version Bump)
*Per CLAUDE.md requirements when adding new components*

**Acceptance Criteria:**
- [AC-6.1] Description: Plugin version bumped (minor) in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` — new feature (caching mechanism)
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "git diff HEAD -- 'claude-plugins/manifest-dev/.claude-plugin/plugin.json' | grep -E '^[+-].*version' | head -5"
  ```

- [AC-6.2] Description: Three READMEs updated per sync checklist — root `README.md`, `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md` — reflecting new cache-warmup agent and CACHING.md reference file
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: inherit
    phase: 2
    prompt: "Check that root README.md, claude-plugins/README.md, and claude-plugins/manifest-dev/README.md reflect the new cache-warmup agent and CACHING.md reference file. These were added as part of the prompt caching mechanism."
  ```
