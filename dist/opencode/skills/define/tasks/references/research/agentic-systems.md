# Agentic AI Systems & Multi-Agent Research Orchestration

**Last Updated**: 2026-02-18
**Shelf Life**: This field barely existed before 2023. Framework capabilities, model capabilities, and best practices shift monthly. Specific benchmark numbers and framework comparisons: 3-6 month shelf life. Architectural patterns (orchestrator-worker, DAG decomposition): 12-18 months — these are stabilizing as patterns but implementations change rapidly. The fundamental tension (multi-agent overhead vs. quality gains) is stable. Revisit all findings by mid-2026.

---

## Key Findings at a Glance

- **Multi-agent orchestration provides only marginal gains (~1.5%) over the strongest single LLM on standard benchmarks** [PRIMARY: Tian et al. 2025], but delivers **90.2% improvement on open-ended research tasks** [PRIMARY: Anthropic 2025]. The value is task-dependent — research is uniquely suited due to inherent parallelizability and path-dependence.
- **41-86.7% failure rates across 7 multi-agent frameworks** [PRIMARY: MAST, NeurIPS 2025 spotlight]. Most failures arise from **inter-agent interactions, not individual agent limitations** — improving base models alone is insufficient.
- **Simple majority voting accounts for most multi-agent gains** attributed to debate [PRIMARY: NeurIPS 2025]. Debate adds value only for complex judgment tasks, not standard reasoning.
- **Specification and system design failures are the largest failure category (~37%)** in multi-agent systems, ahead of inter-agent misalignment (~31%) and task verification (~31%) [PRIMARY: MAST 2025]. Task decomposition quality is the dominant factor in system success.
- **Context engineering has emerged as equal to or more important than architecture design** [PRIMARY: ACE Framework 2025; SECONDARY: Manus 2025]. Treating context as a first-class system with its own lifecycle yields +10.6% improvement on agent tasks.
- **Anthropic explicitly warns against frameworks**: "extra layers of abstraction... obscure underlying prompts and responses, making them harder to debug" [PRIMARY: Anthropic Building Effective Agents].
- **Multi-agent systems use ~15x more tokens than chat** and ~4x more than single-agent interactions [PRIMARY]. Cost-quality frontier is not well-characterized.

---

## Definitions

| Term | Definition |
|------|-----------|
| **Orchestrator-worker** | Architecture where a central agent decomposes tasks, delegates to specialized workers, validates outputs, and synthesizes results. Also called supervisor or hierarchical pattern. |
| **DAG decomposition** | Representing subtasks as nodes in a Directed Acyclic Graph with dependency edges, enabling parallel execution of independent subtasks and dynamic re-decomposition on failure. |
| **MAST** | Multi-Agent System Failure Taxonomy (Cemri et al. 2025). NeurIPS spotlight paper documenting 1,642 annotated failure traces across 7 frameworks. |
| **Context engineering** | Discipline of designing and managing the information provided to AI agents as a first-class system with its own architecture, lifecycle, and constraints. |
| **Monoculture collapse** | When agents built on similar models exhibit correlated vulnerabilities, defeating the independence assumption underlying multi-agent verification. |
| **Pass@k** | Reliability metric measuring success rate across k independent runs. Reveals consistency problems hidden by single-run accuracy (pass@1). |
| **Error-detection asymmetry** | The finding that LLMs cannot identify errors in their own reasoning but CAN correct errors pointed out externally (from D6). |

---

## When Multi-Agent Adds Value (and When It Doesn't)

### The Benchmark Evidence

The most important nuanced finding in this research. Evidence is sharply task-dependent:

**Standard benchmarks favor single-agent or show marginal multi-agent gains**:
- Multi-agent orchestration: 87.4% vs single best LLM 85.9% on GPQA-Diamond — a **1.5% gain** [PRIMARY: Tian et al. 2025]
- Orchestration **fails to capitalize**: at least one agent was correct in 95.5% of cases, but orchestration only reached 87.4% — meaning **8.1% of individually-correct answers are lost** in aggregation [PRIMARY]
- Cognition (Devin creators): "running multiple agents in collaboration only results in fragile systems" [SECONDARY: Cognition 2025]
- Claude Code deliberately chose a single-agent architecture

**Research tasks strongly favor multi-agent**:
- Anthropic's multi-agent research system achieved **90.2% improvement** over single-agent Claude Opus 4 on internal research evaluation [PRIMARY: Anthropic 2025]
- **90% reduction in research time** for complex queries via parallelization [PRIMARY]
- Research is uniquely suited because: open-ended problems with unpredictable steps; inherently parallelizable facets; path-dependent discovery process

**The reconciliation**: Multi-agent adds value when tasks require (1) genuine parallelization across independent facets, (2) specialization across distinct domains, or (3) context window management beyond a single agent's capacity. It subtracts value when tasks are interdependent, coordination overhead exceeds task complexity, or the strongest single model already performs near-optimally.

### Concrete Implementation for CLAUDE.md

The current CLAUDE.md architecture (orchestrator decomposes → parallel agents research → convergence → adversarial verification) is **exactly the pattern the evidence supports for research tasks**. The evidence validates the current approach rather than suggesting a redesign.

**Proposed refinement**: Add scaling guidance: "Match agent count to genuine task parallelizability. Simple fact-checks: single agent, 3-10 tool calls. Direct comparisons: 2-4 agents. Complex multi-facet research: 7+ agents. Do not default to multi-agent when a single well-prompted agent would suffice."

**What would make this wrong?** If future models with much larger context windows and better instruction following eliminate the need for task decomposition, single-agent approaches might dominate even for research. Conversely, if error propagation mitigation improves substantially, multi-agent could deliver consistent gains on standard benchmarks too.

---

## Multi-Agent Coordination Patterns

### The Four Major Patterns

Independently documented by Microsoft, Google, and AWS [PRIMARY: all three]:

| Pattern | How It Works | Best For | CLAUDE.md Fit |
|---------|-------------|----------|---------------|
| **Orchestrator-Worker (Hierarchical)** | Central agent decomposes, delegates, validates, synthesizes | Complex multi-domain workflows with quality assurance | Current architecture |
| **Sequential/Pipeline** | Agents chained in linear order; each processes prior output | Fixed multi-step transformations | Not recommended for research |
| **Handoff/Routing** | Dynamic delegation based on task assessment | When optimal agent isn't known upfront | Possible for topic-dependent routing |
| **Adaptive Network (Decentralized)** | No central control; agents collaborate directly | Low-latency, high-interactivity | Not recommended for quality-controlled research |

**Topology evidence**: Graph-mesh topology yields the best task score and planning efficiency, outperforming star, tree, and chain structures [PRIMARY: MultiAgentBench, ACL 2025]. Tree topology performs worst.

### Concrete Implementation for CLAUDE.md

The orchestrator-worker pattern is the correct choice for research. The evidence confirms this. **No architecture change recommended** — the current approach is the evidence-based best practice for quality-controlled research tasks.

---

## Task Decomposition: The Specification Problem

### MAST's Key Finding

The MAST study found that **specification and system design failures** account for the largest single category (~37%) of multi-agent failures, followed by inter-agent misalignment (~31%) and task verification/termination (~31%) [PRIMARY: Cemri et al. 2025]. Within specification failures: agents misinterpret tasks, violate constraints, or duplicate work when task descriptions are insufficiently detailed.

### Decomposition Best Practices

Anthropic's production system provides concrete guidance [PRIMARY]:

| Task Complexity | Recommended Agents | Tool Calls per Agent |
|----------------|-------------------|---------------------|
| Simple fact-check | 1 | 3-10 |
| Direct comparison | 2-4 | 10-15 each |
| Complex research | 10+ | Variable |

Each subtask delegation must include [PRIMARY: Anthropic]:
1. A clear objective
2. An output format specification
3. Guidance on tools and sources to use
4. **Explicit task boundaries** (assigned AND excluded scope)

Without detailed task descriptions, agents "duplicate work, leave gaps, or fail to find necessary information" [PRIMARY].

**DAG-based dynamic decomposition** is strongly preferred over static plans. Static subtask plans cause error propagation: if an early subtask fails, the error cascades [PRIMARY: TDAG, Neural Networks 2025]. Dynamic re-decomposition on failure is critical.

### Concrete Implementation for CLAUDE.md

The CLAUDE.md orthogonality requirement (INV-G3: each agent prompt includes assigned scope AND excluded scope) directly addresses the MAST finding. The evidence validates this as the highest-leverage specification practice.

**Proposed addition**: Add to Orchestrating Web Research: "When launching follow-up waves, provide established findings from previous waves to prevent redundant research. Each follow-up prompt should include: (1) what was already found, (2) what specific gap this agent should fill, (3) what NOT to re-investigate."

**Feasibility**: High. Already partially implemented in PG-5.

---

## Result Aggregation: Voting vs. Debate

### The NeurIPS Proof

A NeurIPS 2025 spotlight paper proved that **simple majority voting accounts for most gains** attributed to multi-agent debate [PRIMARY: "Debate or Vote"]. The authors modeled debate as a stochastic process and proved it induces a martingale over agents' belief trajectories — debate alone does not improve expected correctness. The ensembling (voting) component does the heavy lifting.

However, **debate outperforms voting on complex judgment tasks**, particularly in LLM-as-Judge scenarios [PRIMARY: arXiv 2025]. This suggests aggregation strategy should match task complexity.

**Conformity bias risk**: Agents tend to favor majority-endorsed answers, reducing reasoning accuracy and requiring more debate rounds [PRIMARY: Free-MAD, arXiv 2025]. Most multi-agent debate frameworks do not consistently beat single-agent chain-of-thought [SECONDARY: ICLR 2025 blog].

### Anthropic's Approach

The Anthropic research system uses neither voting nor debate. The lead agent **synthesizes subagent findings and decides whether more research is needed**, followed by a citation agent that verifies attribution [PRIMARY]. This is closer to "structured synthesis by a qualified integrator" than to mechanical aggregation.

### Concrete Implementation for CLAUDE.md

The current CLAUDE.md process uses the Anthropic pattern: main agent synthesizes, doesn't vote or debate. The evidence validates this as appropriate for research. The convergence criteria (classify gaps, launch follow-ups for critical/significant gaps) serves the same function as the Anthropic lead agent's "decides whether more research is needed."

**No architecture change recommended.** The current synthesis-with-convergence-criteria approach is better than either voting or debate for research tasks.

---

## Multi-Agent Failure Modes

### MAST Taxonomy (NeurIPS 2025 Spotlight)

Based on 1,642 annotated traces across 7 frameworks [PRIMARY: Cemri et al. 2025]:

**Category 1 — Specification & System Design**: Flawed instructions or architecture. The dominant category.

**Category 2 — Inter-Agent Misalignment** (most granular):
| Failure Mode | Frequency | CLAUDE.md Mitigation |
|---|---|---|
| Reasoning-action mismatch | 13.2% | Extended thinking mode in agents |
| Task derailment | 7.4% | Explicit scope boundaries in prompts |
| Wrong assumptions without seeking clarification | 6.8% | Structured output format requirements |
| Unexpected conversation resets | 2.2% | File-based context persistence |
| Ignoring other agents' input | 1.9% | Convergence analysis by main agent |
| Withholding crucial information | 0.85% | Structured output templates |

**Category 3 — Task Verification & Termination**: Superficial checks. MAST found verifier agents perform surface-level validation: "Code is accepted if it compiles. Programs are assumed correct if comments appear consistent."

**Framework-specific failure rates**: 33.3-86.7% across all frameworks tested.

**Critical insight**: "Many MAS failures arise from the challenges in inter-agent interactions rather than the limitations of individual agents." Improving base models will be insufficient; organizational design is required [PRIMARY].

### Additional Failure Modes

- **Error propagation/cascading**: Single root-cause failure cascades into successive errors, especially in long-horizon tasks [PRIMARY: arXiv 2025]
- **Monoculture collapse**: Agents built on similar models exhibit correlated vulnerabilities [PRIMARY: Gradient Institute 2025]
- **Conformity bias**: Agents reinforce each other's errors, creating false consensus
- **Anthropic production failures**: Spawning 50 subagents for simple queries; endless web searching; work duplication; selecting SEO content farms over academic sources [PRIMARY]

### Concrete Implementation for CLAUDE.md

The CLAUDE.md process already mitigates several of these via scope boundaries, convergence analysis, and adversarial verification. The evidence suggests adding:

**Proposed change**: Add to Orchestrating Web Research, Delegation Constraints: "Guard against over-spawning: match agent count to genuine research facets, not to perceived thoroughness. For each agent, verify that its assigned scope justifies a dedicated research effort."

**What would make this wrong?** If the overhead of deciding "how many agents?" exceeds the cost of launching extra agents. For low-cost research queries, erring toward more agents may be cheaper than optimizing agent count. The concern is more relevant for high-stakes, expensive research.

---

## Context Engineering: The Emerging Discipline

### Why It Matters

Context engineering — treating the information provided to agents as a first-class system — has emerged as potentially **more impactful than architecture changes** [PRIMARY: ACE Framework 2025]:

- The ACE framework showed **+10.6% improvement** on agent tasks through systematic context engineering
- On BrowseComp, **80% of performance variance** is explained by token usage alone [PRIMARY: Anthropic]
- A **40% decrease in task completion time** was achieved simply by improving tool descriptions [PRIMARY: Anthropic]

### Key Practices

Six context layers [PRIMARY: ACE; SECONDARY: Manus]:
1. **System rules**: Invariant instructions and constraints
2. **Memory**: Persistent information across sessions
3. **Retrieved docs**: Dynamically loaded reference material
4. **Tool schemas**: Available tools and their descriptions
5. **Recent conversation**: Interaction history
6. **Current task**: Active objective and state

**Context management strategies** from Anthropic's research system [PRIMARY]:
- Agents save plans to external memory (file system) to persist context
- Agents summarize completed work before new tasks
- Fresh subagents spawned with clean contexts, maintaining continuity via handoffs
- File system used as external memory to prevent "game of telephone" information loss

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Orchestrating Web Research: "For research sessions approaching context limits, use file-based context persistence: write intermediate findings to files and load them as needed rather than relying on conversation history. This prevents information loss through context compaction."

**Feasibility**: High. The execution log pattern already serves this purpose partially. Making it explicit as a context engineering practice would be valuable.

---

## Quality Control in Delegated Research

### The Reliability Problem

The CLEAR Framework documented that agent performance drops from **60% (single-run) to 25% (8-run consistency)** [PRIMARY]. Cost variations of **up to 50x** exist for similar precision levels. This means:

- Single-run accuracy massively overstates real-world reliability
- Systems must be evaluated on consistency, not just best-case performance
- The same query can produce radically different results on different runs

### What Works for Quality Control

- **Independent judge agents**: Not integrated into production workflow, not influenced by reasoning chains. STRATUS achieved **1.5x improvement** in failure mitigation; PwC saw **7x accuracy improvement** through structured validation loops [PRIMARY; SECONDARY]
- **LLM-as-judge evaluation**: Anthropic uses rubrics assessing factual accuracy, citation accuracy, completeness, source quality, and tool efficiency (0.0-1.0 scores) [PRIMARY]
- **Human evaluation**: Still necessary to catch edge cases that automation misses (e.g., agents selecting SEO content farms over academic PDFs) [PRIMARY]

### Concrete Implementation for CLAUDE.md

The adversarial verification system IS the independent judge. The evidence validates this pattern and suggests the verification agents should be explicitly independent: different prompts, ideally different reasoning approaches, from the generation agents.

**Proposed refinement**: "Adversarial verification agents should attack from perspectives NOT used in the original research — they are independent judges, not reviewers of their own work."

---

## Agent Prompt Engineering for Research

### Evidence-Based Practices

Layering multiple prompting techniques produces the best results [PRIMARY: Qian 2025 systematic review of 50+ techniques]:
- **Role/persona framing**: Set expertise level and voice
- **Chain-of-thought scaffolding**: Explicit reasoning steps
- **Structured output format**: Reduces hallucination and improves parsing
- **ReAct pattern**: Reasoning + action interleaving for tool-augmented workflows

For research agents specifically [PRIMARY: Anthropic]:
- Embed **scaling rules** in prompts: agents struggle to judge how much effort a task deserves
- Provide **explicit tool selection heuristics**
- Use **extended thinking** for planning and evaluation
- Implement **just-in-time context**: maintain lightweight identifiers, load data dynamically
- Instill **good heuristics rather than rigid rules** based on how skilled humans approach research
- Let models themselves suggest prompt improvements

### Concrete Implementation for CLAUDE.md

The current agent prompt discipline (assigned scope, excluded scope, output format guidance) aligns with Anthropic's recommendations. The addition: embed scaling rules that match effort to task complexity, since agents cannot judge this independently.

---

## Benchmarks and the Production Gap

### Current State

| Benchmark | Key Results | Caveat |
|-----------|-------------|--------|
| GAIA | 15% (GPT-4 2023) → 75% (H2O.ai 2025) | General assistant tasks |
| SWE-bench Verified | 2% (2023) → ~75% (2025) | Contamination concerns: "mounting evidence models are contaminated" |
| MultiAgentBench (ACL 2025) | Graph-mesh best; cognitive planning +3% | Multi-agent specific |
| CLEAR Framework | 60% → 25% with consistency testing | Reveals reliability illusion |

**The production gap**: Less than **10% of enterprises** report scaling AI agents in any individual function [SECONDARY: McKinsey 2025]. This suggests the gap between benchmark performance and real-world deployment remains enormous.

---

## Prioritized Recommendations

### P1: Implement Immediately

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Scaling guidance for agent count | Add complexity-to-agent-count mapping | Prevents over-spawning for simple tasks; ensures sufficient agents for complex ones | Low: guidance, not constraint |
| Follow-up wave context provision | Provide established findings when launching follow-up agents | Prevents redundant re-research (MAST specification failure) | Low: already partially in PG-5 |
| File-based context persistence | Explicit instruction to use files as external memory | Prevents information loss through context compaction | Low: operationalizes existing practice |

### P2: Implement After P1 Validated

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Independent adversarial perspectives | Verification agents must use different analytical angles from generation agents | Prevents correlated failures (monoculture) in verification | Medium: harder to specify "different" |
| Embedded scaling rules in agent prompts | Agents receive explicit effort-matching guidance | Prevents under/over-research by subagents | Low: prompt-level addition |

### P3: Implement When P1-P2 Are Stable

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Consistency evaluation (pass@k) | Evaluate research quality across multiple independent runs for high-stakes topics | Catches reliability problems hidden by single-run accuracy | High: cost multiplier |
| Model diversity for verification | Different models for generation vs. verification | Breaks monoculture correlation | Medium: operational complexity |

---

## Knowledge Gaps

1. **Research-specific multi-agent evaluation is missing**: Anthropic's 90.2% improvement is from internal evaluation. No independently replicated benchmark exists specifically for multi-agent research quality. [Gap severity: Significant]
2. **Cost-quality frontier is uncharacterized**: Multi-agent systems use 15x more tokens than chat. The optimal cost-quality tradeoff for research is not well-studied. [Gap severity: Significant]
3. **Error propagation mitigation is unsolved**: Current interventions yield only +14% improvement and remain "insufficiently low for real-world deployment" [PRIMARY]. This is a fundamental limitation, not an engineering gap. [Gap severity: Significant]
4. **Conformity bias in homogeneous agent pools**: Most systems use the same model for all agents, creating correlated failures that aggregation strategies cannot fix. How much model diversity is needed is unknown. [Gap severity: Minor]
5. **Missing decomposition granularity comparison**: While "balanced" granularity is consistently recommended, no study systematically tested coarse vs. fine decomposition with controlled variables. [Gap severity: Minor]

---

## Source Authority Assessment

| Source | Authority | Notes |
|--------|-----------|-------|
| MAST / Cemri et al. (NeurIPS 2025) | Highest [PRIMARY] | NeurIPS spotlight; 1,642 traces; 7 frameworks |
| Anthropic Research System (2025) | High [PRIMARY] | Most detailed production research system account |
| Anthropic Building Effective Agents (2024) | High [PRIMARY] | Foundational patterns document |
| Debate or Vote (NeurIPS 2025) | High [PRIMARY] | Formal proof (martingale); peer-reviewed |
| Tian et al. (2025) Beyond Strongest LLM | High [PRIMARY] | Single vs. multi-agent comparison |
| MultiAgentBench (ACL 2025) | High [PRIMARY] | Topology comparison |
| TDAG (Neural Networks 2025) | High [PRIMARY] | Dynamic decomposition |
| ReSo (EMNLP 2025) | High [PRIMARY] | DAG decomposition + reward models |
| Microsoft Azure AI Patterns | High [PRIMARY] | Enterprise architecture patterns |
| Google ADK Patterns | High [PRIMARY] | Multi-agent pattern documentation |
| AWS Agentic AI Patterns | High [PRIMARY] | Orchestration patterns |
| ACE Framework (2025) | Moderate [PRIMARY] | Context engineering; +10.6% result |
| Gradient Institute (2025) | High [PRIMARY] | Cascading failures, monoculture |
| Cognition "Don't Build Multi-Agents" | Moderate [SECONDARY] | Important counter-evidence |
| Manus Context Engineering | Moderate [SECONDARY] | Production context engineering lessons |
| Qian (2025) Prompting systematic review | Moderate [PRIMARY] | 50+ technique survey |

No claims rest solely on tertiary sources.

---

## Adversarial Stress-Testing

**Strongest counter-argument encountered**: Multi-agent research orchestration is unnecessary complexity. Cognition (Devin creators) says "running multiple agents in collaboration only results in fragile systems." Claude Code chose single-agent architecture. The 1.5% gain on GPQA-Diamond doesn't justify the 15x token cost. **Response**: This is valid for standard benchmarks and well-defined tasks. But the 90.2% improvement on open-ended research tasks (Anthropic's own production system) and the 90% time reduction for complex queries represent a categorically different value proposition. Research has properties (parallelizable facets, path-dependent discovery, context window demands) that make multi-agent architecture uniquely justified. The CLAUDE.md target use case — deep, adversarial, multi-angle research — is exactly this category.

**Second strongest counter-argument**: The 41-86.7% failure rates across all tested multi-agent frameworks (MAST) suggest the technology is fundamentally unreliable. Building on a foundation with >40% failure rate is reckless. **Response**: The MAST failures are dominated by specification problems (task description quality), not fundamental architectural limitations. The CLAUDE.md process already addresses the top specification failure mode (scope boundaries) through its orthogonality requirement. The remaining failure modes (inter-agent misalignment) are real but manageable through structured output formats, convergence analysis, and adversarial verification — all existing CLAUDE.md features.

**Third counter-argument**: Context engineering alone (+10.6% improvement, 40% faster task completion) may deliver more value than multi-agent architecture. Investment should go into better prompts and context management for single agents, not into coordination overhead. **Response**: Not mutually exclusive. Context engineering improves individual agent performance within a multi-agent system. The CLAUDE.md process benefits from both: better agent prompts AND multi-agent orchestration. The evidence suggests both are necessary — neither alone is sufficient for the quality level the process targets.

**Unresolved tension**: The evidence strongly supports multi-agent for research but the cost-quality frontier is uncharacterized. It's possible that 80% of the quality could be achieved at 20% of the cost with fewer, better-prompted agents. Without systematic cost-quality data, the optimal agent count remains a judgment call.
