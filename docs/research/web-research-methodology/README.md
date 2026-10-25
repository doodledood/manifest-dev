# Meta-Research: Optimal Web Research Methodology for AI-Mediated Systems

**Last Updated**: 2026-02-18
**Shelf Life**: This synthesis inherits the shortest shelf life of its components. AI-specific findings (D6, D7): 6-12 months. Established methodology (D1, D2, D3, D4, D5): 3-5 years. Overall: re-evaluate AI-specific recommendations by early 2027; methodology recommendations remain valid through 2028+.

---

## Purpose

This research investigates what established disciplines — systematic review, intelligence analysis, fact-checking, information science, epistemology, AI failure mode analysis, and multi-agent systems research — say about how to conduct high-quality web research. The goal: identify specific, evidence-based improvements to the CLAUDE.md research process, targeting its known weaknesses in claim validation, small factual errors, and the need for multiple adversarial rounds to converge.

---

## Key Findings

### The Evidence Is Clear On

- **Single-query searches miss 60-72% of relevant content** [D4, PRIMARY: Walters]. Multi-query strategies with synonym expansion and iterative reformulation are not optional — they are the difference between comprehensive and systematically incomplete research.
- **Lateral reading is the single most effective source evaluation technique**: 71% improvement in an RCT (n=499) [D3/D4, PRIMARY: Wineburg et al. 2022]. It maps directly to AI agent capabilities and should be a first-class process requirement.
- **Error propagation follows exponential decay**: at 5% per-step error, a 4-step pipeline yields ~81.5% cumulative accuracy [D6, PRIMARY]. This is the fundamental constraint on multi-step research synthesis and the strongest argument for parallel verification over serial processing.
- **LLMs cannot find their own errors but CAN correct them when pointed out** [D6, PRIMARY: ACL Findings 2024]. This error-detection asymmetry is the empirical justification for multi-agent adversarial verification — the current CLAUDE.md architecture is structurally correct.
- **Multi-agent research orchestration yields 90.2% improvement** over single-agent on open-ended research tasks [D7, PRIMARY: Anthropic 2025], but only ~1.5% on standard benchmarks [D7, PRIMARY: Tian et al. 2025]. Research is uniquely suited for multi-agent architecture.
- **Citation fabrication rates of 6-29%** in GPT-4o, inversely correlated with topic familiarity [D6, PRIMARY: JMIR 2025]. Niche topics require aggressive citation verification.
- **Calibration training can backfire**: Mandel & Tetlock (2018) showed debiasing overshoots into underconfidence. Kelly & Mandel (2024) confirmed empirically [D2/D5, PRIMARY]. Any instruction to "be less confident" risks degrading research quality as much as overconfidence does.
- **41-86.7% failure rates** across 7 multi-agent frameworks, with specification failures (task description quality) as the dominant cause [D7, PRIMARY: MAST 2025]. The CLAUDE.md orthogonality requirement directly addresses the top failure mode.

### The Evidence Is Mixed On

- **Structured Analytic Techniques**: Devil's advocacy and pre-mortem have strong empirical support. ACH has contested support — may increase error in some conditions [D2, PRIMARY: Dhami 2019]. Use SATs as structured process discipline, not guaranteed debiasing.
- **Formal epistemological frameworks**: Valuable for complex, novel, uncertain synthesis tasks. But ecological rationality research shows simple heuristics outperform formal methods in well-structured environments [D5, PRIMARY: Gigerenzer 2004]. Discriminate application is key.
- **LLM verbal confidence**: Systematically miscalibrated due to RLHF effects. Base models are often better calibrated than post-trained models [D6, PRIMARY: NeurIPS Workshop 2024]. Verbal confidence expressions are useful for forcing uncertainty reasoning but unreliable as accuracy indicators.

### The Evidence Challenges Our Assumptions About

- **Whether the current process needs major changes**: The CLAUDE.md architecture (decompose → delegate → converge → verify) is empirically validated as the correct pattern for research tasks. Most recommendations are targeted refinements, not architectural overhaul. This supports ASM-2 (current architecture is sound).
- **Whether more adversarial rounds always help**: Bipolar bias means adversarial verification can push toward over-hedging and underconfidence. Adversarial rounds must check for both false positives AND false negatives [D2/D5, PRIMARY: Mandel & Tetlock 2018].
- **Whether AI research is fundamentally unreliable**: When SAFE (search-augmented factuality evaluator) and crowdsourced human annotators disagreed on fact verification, SAFE was correct 76% vs humans 19% [D6, PRIMARY: NeurIPS 2024]. Note: overall agreement is 72%; the 76/19 split applies only to ~100 disagreement cases, and "humans" were crowdsourced annotators, not trained fact-checkers. Still, the narrative of universal AI unreliability is overstated for well-supported domains, though multi-step synthesis remains genuinely fragile.

---

## Evaluation of Current CLAUDE.md Architecture

### What the Current Process Already Does Well

| Current Feature | Evidence Supporting It | Source |
|----------------|----------------------|--------|
| Decompose → delegate → converge → verify pipeline | Orchestrator-worker is the evidence-based best practice for research | D7: Anthropic, Microsoft, Google, AWS patterns |
| Orthogonal agent decomposition with excluded scope | Directly addresses the #1 multi-agent failure mode (specification) | D7: MAST ~37% specification failures (largest single category) |
| Adversarial verification as a separate phase | Matches error-detection asymmetry: LLMs correct when errors are pointed out | D6: ACL Findings 2024 |
| Source authority hierarchy (PRIMARY > SECONDARY > TERTIARY) | Aligns with foundationalist evidence evaluation | D5: epistemological evidence hierarchies |
| Cross-referencing across independent sources | Aligns with coherentist corroboration; validated by convergence analysis | D5: coherentism; D3: circular citation detection |
| Gap honesty requirements | Operationalizes epistemic humility, the virtue most correlated with critical thinking | D5: Nature Reviews Psychology 2022 |
| Anti-confirmation bias searches | Directly addresses the most dangerous research bias | D5: Nickerson 1998; D2: IC tradecraft |
| Multi-angle investigation | Maps to Tetlock's "balance inside and outside views" | D2/D5: superforecasting practices |
| Evidence traceability requirements | Implements provenance tracing, the core fact-checking technique | D3: SIFT, PolitiFact methodology |

### Specific Gaps Identified

| Gap | Impact | Evidence | Recommended Fix |
|-----|--------|----------|----------------|
| **No multi-query search requirement** | 60-72% of relevant content missed by single queries | D4: Walters; Salvador-Olivan 2019 | Add minimum 3 query variants per facet to agent prompts |
| **No lateral reading requirement** | Sources evaluated by content alone (vertical reading) rather than by external reputation | D3/D4: Wineburg 2019 (71% RCT improvement) | Add lateral reading for sources underpinning key claims |
| **No citation verification attack vector** | 6-29% citation fabrication undetected | D6: JMIR 2025 | Add citation existence/accuracy to adversarial verification |
| **No manifest deviation tracking** | Invisible methodology drift post-manifest | D1: PROSPERO evidence on pre-registration value | Add required `## Protocol Deviations` section |
| **No anti-cherry-picking rule** | Sources silently dropped when contradictory | D1: Cochrane Handbook Ch 3 | Explicit rule: sources meeting inclusion criteria cannot be excluded for contradictory findings |
| **No explicit warrant identification** | Hidden reasoning assumptions unexposed | D5: Toulmin model; MITRE 2004; CQoT 2024 | Require stating inferential step connecting evidence to conclusion |
| **No sycophancy-aware prompt framing** | Agent prompts may imply expected findings | D6: 100% sycophantic compliance in medical contexts | Reframe prompts to avoid implying expected results |
| **No context persistence guidance** | Information lost through context compaction | D7: Anthropic, ACE Framework | Add file-based context persistence instructions |
| **Confidence calibrated only in one direction** | Risk of reflexive hedging (underconfidence) | D2/D5: Mandel & Tetlock 2018 bipolar bias | Explicitly warn against BOTH over- and under-confidence |
| **No disagreement classification** | All conflicts treated the same | D5: epistemology of disagreement | Classify conflicts (factual vs. open question) before resolution |
| **GRADE-adapted confidence not implemented** | Evidence tier labels capture source type but not evidence quality dimensions | D1: GRADE Working Group | Add confidence modifiers beyond source classification |
| **No scaling guidance for agent count** | Risk of over-spawning or under-resourcing | D7: Anthropic complexity-to-agent mapping | Add complexity-based agent count guidance |

---

## Prioritized Improvement List

Ranked by **expected impact** (magnitude × evidence strength) per unit of **implementation effort**. Each recommendation maps to a specific CLAUDE.md section or process phase.

### Tier 1: Highest Impact, Implement Immediately

| # | Recommendation | CLAUDE.md Section | Evidence | Expected Impact | Effort |
|---|---------------|-------------------|----------|----------------|--------|
| 1 | **Multi-query search requirement** | Orchestrating Web Research → Delegation Constraints | Simple searches miss 60-72% of content [D4] | Critical: addresses largest recall gap | Low: add to agent prompt template |
| 2 | **Lateral reading for key sources** | Research Quality Standards → Source Rigor | 71% improvement in RCT [D3/D4] | High: catches unreliable sources | Low: add behavioral rule |
| 3 | **Citation verification attack vector** | Adversarial Verification → Attack vectors table | 6-29% fabrication rate [D6] | High: catches fabricated citations | Low: add row to existing table |
| 4 | **Sycophancy-aware prompt framing** | Orchestrating Web Research → Agent prompt discipline | 100% sycophantic compliance documented [D6] | High: prevents confirmation-aligned fabrication | Low: prompt reframing guidance |
| 5 | **Anti-cherry-picking rule** | Orchestrating Web Research → new subsection | Cochrane: sources must not be excluded solely for contradictory findings [D1] | High: structural gap in current process | Low: behavioral rule |
| 6 | **Bipolar calibration warning** | Consistency & Transparency section | Empirically confirmed overcorrection risk [D2/D5] | Medium: prevents hedging-induced quality loss | Low: modify existing guidance |

### Tier 2: High Impact, Implement After Tier 1 Validated

| # | Recommendation | CLAUDE.md Section | Evidence | Expected Impact | Effort |
|---|---------------|-------------------|----------|----------------|--------|
| 7 | **GRADE-adapted confidence modifiers** | Research Quality Standards → Source Rigor | GRADE used by 110+ organizations; only 4% of Cochrane evidence rates "High" [D1] | High: forces multi-dimensional evidence assessment | Medium: per-claim evaluation |
| 8 | **Manifest deviation tracking** | New section in research output template | Pre-registration reduces false positives [D1] | Medium: prevents invisible methodology drift | Low: add required section |
| 9 | **Explicit warrant identification** | Intellectual Rigor → Argument chain integrity | CQoT outperforms CoT for LLM reasoning [D5] | Medium: exposes hidden assumptions | Medium: requires analytical step |
| 10 | **Iterative search with reformulation** | Orchestrating Web Research → Agent prompt discipline | Mirrors expert search behavior; pearl growing finds 51% of sources [D4] | Medium: captures additional relevant sources | Medium: agent metacognition required |
| 11 | **Disagreement classification** | Convergence Criteria | Conciliation for facts, steadfastness for open questions [D5] | Medium: prevents forced false consensus | Low: add classification step |
| 12 | **Structural confidence assessment** | Research Quality Standards | RLHF worsens verbal calibration [D6] | Medium: more reliable than verbal confidence | Medium: reframes assessment approach |

### Tier 3: Moderate Impact, Implement When Tiers 1-2 Stable

| # | Recommendation | CLAUDE.md Section | Evidence | Expected Impact | Effort |
|---|---------------|-------------------|----------|----------------|--------|
| 13 | **PRISMA-adapted output checklist** | New output template | ~43% average voluntary compliance shows checklists need structural enforcement [D1] | Medium: standardizes output quality | Medium: template design |
| 14 | **Context persistence guidance** | Orchestrating Web Research | ACE: +10.6% from context engineering; 40% faster from tool descriptions [D7] | Medium: prevents information loss | Low: add guidance |
| 15 | **Agent count scaling guidance** | Orchestrating Web Research → Decomposition Principles | Anthropic: simple=1, comparison=2-4, complex=10+ [D7] | Low-Medium: prevents over/under-spawning | Low: add table |
| 16 | **Linchpin analysis for adversarial targeting** | Adversarial Verification | Focus verification on 3-5 claims whose failure collapses most conclusions [D2] | Medium: more efficient adversarial rounds | Medium: requires analytical step |
| 17 | **Key Assumptions Check post-convergence** | Convergence Criteria → new step | 5-step process; surfaces hidden assumptions [D2] | Medium: catches unstated assumptions | Low: add step |
| 18 | **Outside view prompting** | Research Quality Standards | Tetlock: "How often do things of this sort happen?" [D2/D5] | Low-Medium: counters anchoring | Low: add to agent prompts |

---

## Cross-Cutting Themes

Six themes emerged independently across multiple facets. These are the most robust findings because they were discovered through different disciplinary lenses.

### 1. Source Evaluation Convergence

Five disciplines independently developed source evaluation frameworks:

| Discipline | Framework | Core Innovation |
|-----------|-----------|----------------|
| Systematic reviews (D1) | GRADE | Multi-dimensional evidence quality assessment |
| Intelligence analysis (D2) | ICD 203 Standard 1 | Source credibility with confidence separation |
| Fact-checking (D3) | Lateral reading, IMVAIN | Evaluate source by external reputation, not self-presentation |
| Information science (D4) | CRAAP → SIFT evolution | Movement from vertical to lateral evaluation |
| Epistemology (D5) | Foundationalism + coherentism | Anchor in authority AND corroborate across independent sources |

**Synthesis**: The CLAUDE.md authority hierarchy (PRIMARY > SECONDARY > TERTIARY) captures the foundational dimension but misses the GRADE insight: a PRIMARY source can be low-confidence if inconsistent with other evidence, indirect to the question, or imprecise. The most complete source evaluation combines source type (current) + evidence quality dimensions (GRADE) + external reputation check (lateral reading).

### 2. Structured Bias Mitigation

| Discipline | Approach | Key Mechanism |
|-----------|----------|---------------|
| Systematic reviews (D1) | RoB 2 signaling questions | Domain-based structured assessment |
| Intelligence analysis (D2) | SATs, cognitive bias mapping | Process-level interventions at each phase |
| Fact-checking (D3) | Investigation-validation separation | Structural independence between production and checking |
| Epistemology (D5) | Debiasing techniques | Natural frequencies, reference class forecasting, precommitment |
| AI failure modes (D6) | Sycophancy-aware design | Prompt framing to prevent confirmation alignment |

**Synthesis**: The CLAUDE.md process already has extensive bias mitigation. The cross-cutting insight: structural interventions (process rules, separation of concerns) are more reliable than awareness-based interventions (instructions to "watch for bias"). The sycophancy evidence (D6) provides the mechanism: AI agents will comply with awareness instructions performatively while still exhibiting the bias structurally.

### 3. Confidence and Uncertainty Frameworks

| Discipline | Framework | Levels |
|-----------|-----------|--------|
| Systematic reviews (D1) | GRADE | High / Moderate / Low / Very Low |
| Intelligence analysis (D2) | ICD 203 | High / Moderate / Low |
| Epistemology (D5) | Tetlock calibration | Numeric probabilities with ranges |
| AI failure modes (D6) | RLHF calibration paradox | Structural indicators over verbal confidence |

**Synthesis**: All disciplines converge on the need for explicit, multi-level confidence expression. The critical addition from D5/D6: confidence must be calibrated in BOTH directions (the bipolar bias insight), and structural indicators (source agreement, evidence tiers, contradictory evidence) are more reliable than verbal confidence expressions.

### 4. Pre-Specification and Protocol Discipline

| Discipline | Mechanism | Value |
|-----------|-----------|-------|
| Systematic reviews (D1) | PROSPERO registration, PRISMA | Locks methodology before results known |
| Intelligence analysis (D2) | ICD 203 tradecraft standards | Standardizes analytical process |
| Fact-checking (D3) | PolitiFact 7-step protocol | Systematic verification sequence |
| Epistemology (D5) | Precommitment strategies | Makes debiasing structural, not voluntary |

**Synthesis**: The manifest system already functions as protocol pre-specification. The gap: deviation tracking. Pre-registration's value comes from making deviations visible, not from preventing them.

### 5. Error Propagation and Pipeline Reliability

| Discipline | Finding | Implication |
|-----------|---------|-------------|
| Systematic reviews (D1) | 5% per-step error → 81.5% cumulative accuracy | Adding process steps is not free |
| AI failure modes (D6) | Exponential decay formula | Parallel verification preferred over serial chains |
| Agentic systems (D7) | 41-86.7% failure rates in multi-agent systems | Specification quality dominates system quality |

**Synthesis**: The error compounding formula is the most practically consequential quantitative finding. Every added process step must reduce per-step error by more than it adds to pipeline length. This argues for parallel verification (multiple independent checks) over serial processing (each step building on the last).

### 6. Counter-Evidence to AI Research Automation

| Source | Finding | Implication |
|--------|---------|-------------|
| D1: RAISE (Cochrane/Campbell/JBI) | "Does not support GenAI use in evidence synthesis without human involvement" | Adversarial verification is non-optional |
| D4: GAIA Benchmark | GPT-4 with plugins 15% vs human 92% on general tasks | AI search capability has fundamental limits |
| D6: Hallucination rates | 20-45% depending on task and domain | Verification must be systematic, not spot-check |
| D7: MAST | 41-86.7% multi-agent failure rates | System design matters more than model capability |
| D6: NeurIPS 2024 | SAFE correct 76% vs crowdsourced annotators 19% on disagreement cases (72% overall agreement) | Specific fact-verification, not synthesis; annotators were not trained fact-checkers |

**Synthesis**: The evidence supports AI-mediated research as capable but requiring structural verification. The current CLAUDE.md adversarial verification is the correct response. The nuance: AI agents are excellent at specific fact-checking tasks but fragile at multi-step synthesis.

---

## Conflicts Between Facets

### Resolved Conflicts

| Conflict | Resolution |
|----------|-----------|
| D2 says ACH has contested support; D5 assumes structured evaluation works | ACH as organizational tool (structuring evidence against hypotheses), not guaranteed debiaser. Use matrix structure for convergence analysis without relying on debiasing claims. |
| D1 says comprehensiveness conflicts with speed; D4 says recall-oriented search needed | Rapid review model: principled abbreviation for lower-stakes research, full recall strategy for high-stakes. Match search depth to research tier. |
| D5 recommends formal epistemological frameworks; D5 also cites Gigerenzer showing simple heuristics can outperform | Discriminate application: formal frameworks for complex novel synthesis (CLAUDE.md target use case); simple heuristics for routine fact-checking. |
| D6 says "don't trust verbal confidence"; D5 says "express confidence in granular ranges" | Compatible: the value of explicit confidence expression is in forcing uncertainty reasoning; structural indicators (source agreement, evidence tiers) should override verbal confidence for decision-making. |

### Convergent Findings (Independent Confirmation)

| Finding | Confirmed Across | Confidence |
|---------|-----------------|------------|
| Bipolar bias in debiasing | D2 (Mandel & Tetlock), D5 (calibration training limits) | High |
| Structural > awareness-based interventions | D1 (22% voluntary compliance), D2 (SATs as process), D5 (situationism), D6 (sycophancy) | High |
| Multi-agent architecture correct for research | D6 (error-detection asymmetry), D7 (90.2% improvement) | High |
| Citation/source independence essential | D3 (circular citation), D4 (lateral reading), D5 (coherentism limits) | High |

---

## Files in This Collection

| File | Description | Tier | Key Contribution |
|------|-------------|------|-----------------|
| `systematic-reviews.md` | PRISMA, GRADE, Cochrane methodology transfer to AI research | Tier 2 | GRADE-adapted confidence labeling; anti-cherry-picking rules; deviation tracking |
| `intelligence-analysis.md` | Structured Analytic Techniques, ICD 203, cognitive bias mapping | Tier 1 | Devil's advocacy structure; Key Assumptions Check; linchpin analysis; bipolar bias |
| `fact-checking.md` | IFCN standards, lateral reading, claim decomposition, provenance | Tier 1 | Lateral reading (71% RCT); claim decomposition; circular citation detection; 40-60% base error rate |
| `information-science.md` | Query formulation, precision/recall, expert search behavior | Tier 2 | 60-72% recall gap from single queries; iterative search models; vocabulary mismatch; pearl growing |
| `epistemology.md` | Calibration, Bayesian reasoning, Toulmin model, epistemic virtues | Tier 1 | Bipolar bias warning; Toulmin warrant identification; disagreement resolution; virtue operationalization |
| `ai-failure-modes.md` | Hallucination taxonomy, sycophancy, error propagation, mitigation | Tier 1 | Error compounding formula; citation fabrication rates; RLHF calibration paradox; error-detection asymmetry |
| `agentic-systems.md` | Multi-agent patterns, decomposition, aggregation, quality control | Tier 2 | 90.2% improvement for research; MAST failure taxonomy; context engineering; single vs. multi-agent evidence |

---

## Sources Summary

Research drew on **150+ sources** across 7 disciplines. Source authority distribution:

| Authority Level | Count | Examples |
|----------------|-------|---------|
| Highest [PRIMARY] | ~25 | Cochrane Handbook, GRADE Working Group, Mandel & Tetlock (Frontiers), Wineburg (TCR), Nature 2024, MAST (NeurIPS 2025) |
| High [PRIMARY] | ~60 | PRISMA (BMJ 2021), Heuer (CIA), FActScore (EMNLP 2023), Bates 1989, Tetlock/GJP, Anthropic research system |
| Moderate [PRIMARY/SECONDARY] | ~40 | CQoT 2024, ACE Framework, VICS 2024, Vectara benchmarks, Cognition blog |
| Lower [SECONDARY/TERTIARY] | ~25 | Framework comparisons, practitioner guides, blog analyses |

No major conclusion rests solely on tertiary sources. Cross-cutting findings are supported by multiple independent primary sources from different disciplines.

---

## Adversarial Stress-Testing

### Counter-Argument 1: "The current process is already near-optimal; these are marginal improvements"

**The argument**: The CLAUDE.md process already implements most of the structural features recommended by adjacent disciplines (multi-agent decomposition, adversarial verification, source hierarchy, gap honesty). The 18 recommended improvements are incremental, not transformative. The overhead of implementing them may exceed the marginal quality gain.

**Engagement**: Partially valid. The architecture IS correct — no facet suggested wholesale replacement. But "near-optimal architecture" does not mean "near-optimal execution." The recall gap (60-72% of content missed by single queries), citation fabrication (6-29%), and the absence of lateral reading represent genuine structural gaps, not marginal improvements. The Tier 1 recommendations (multi-query, lateral reading, citation verification, sycophancy-aware framing, anti-cherry-picking, bipolar calibration) are low-effort, high-impact additions to an already-sound architecture.

### Counter-Argument 2: "Adding process steps to a pipeline with 5% per-step error makes things worse, not better"

**The argument**: D1 and D6 document that errors compound exponentially across pipeline steps. Adding more verification, assessment, and checking steps adds pipeline length, which the compounding formula says reduces overall accuracy.

**Engagement**: This is the most sophisticated counter-argument and it's partially correct. The resolution: distinguish between **serial** process additions (which add pipeline steps) and **parallel** verification (which doesn't add pipeline length but does add error-catching). The Tier 1 recommendations are mostly behavioral rules (lateral reading, anti-cherry-picking, sycophancy-aware framing) that modify existing steps rather than adding new serial steps. The citation verification recommendation IS an additional step, but it specifically targets a 6-29% error class — the per-check benefit exceeds the per-step error cost.

### Counter-Argument 3: "This is technique tourism — collecting frameworks without evidence they improve outcomes"

**The argument**: The research catalogs techniques from 7 disciplines but provides no empirical evidence that implementing them in AI research actually improves output quality. GRADE-adapted labels, Toulmin warrants, Key Assumptions Checks, and lateral reading are all theoretically sound but untested in the specific context of AI-mediated web research. Ioannidis (2025, Journal of Economic Surveys) provides the strongest articulation: meta-research has identified numerous biases and problems, but "there is often little or no evidence that specific recommendations and actions actually lead to improvements and a favorable benefit-harm ratio."

**Engagement**: Valid and the most important limitation of this entire research effort. The strongest mitigating evidence: (a) lateral reading has RCT evidence (71% relative improvement, though absolute scores remained below 50%) even if not tested with AI agents specifically — and a 2025 Italian replication showed no significant improvement in real classroom settings, (b) CQoT shows Toulmin-based questioning outperforms CoT for LLM reasoning, (c) the recall gap from single queries is measured directly, (d) citation fabrication rates are measured directly. The recommendations target documented failure modes with techniques that address the specific mechanism of failure. This is stronger than generic methodology transfer, though weaker than direct experimental validation. Note: AI agents may already perform lateral reading implicitly (searching the web about sources is their default behavior), which could make that specific recommendation redundant rather than transformative.

### Counter-Argument 4: "Rapidly improving AI capabilities will make most of these recommendations obsolete"

**The argument**: Hallucination rates are declining (sub-1% on some benchmarks). Larger context windows reduce the need for multi-agent decomposition. Better RLHF may solve calibration. These recommendations may be solving yesterday's problems.

**Engagement**: Some recommendations WILL become less critical as models improve (citation verification if fabrication rates drop to <1%, sycophancy-aware framing if alignment improves). But structural recommendations (multi-query search, lateral reading, deviation tracking, anti-cherry-picking, warrant identification) address epistemic fundamentals that don't change with model capability. The shelf life assessment distinguishes between volatile AI-specific recommendations and stable methodology recommendations.

### Counter-Argument 5: "The research itself contains the errors it warns about"

**The argument**: Adversarial verification of these documents found 3 critical factual errors: the MAST "79% specification failures" was actually ~37% (the 0.79 was a Cohen's Kappa inter-annotator agreement score), the SAFE paper venue was misattributed as COLM when it was NeurIPS, and GAIA benchmark numbers were wrong in 2 of 3 documents that cited them. These are exactly the "small inaccuracies" the research claims to address.

**Engagement**: Deeply ironic and fully acknowledged. These errors were caught during adversarial verification and corrected — demonstrating both the problem (AI-mediated research produces exactly these errors) and the solution (adversarial verification catches them). The MAST error is particularly instructive: a metric name (Cohen's Kappa) was confused with a failure rate percentage, a classic confabulation pattern where the model generates a plausible-sounding but incorrect interpretation of a number from a paper. The GAIA inconsistency (correct in one document, wrong in two others) demonstrates that convergence analysis can miss cross-document consistency failures.

### Identified Gaps from Adversarial Verification

The following gaps were identified during adversarial verification and are acknowledged rather than patched:

1. **Adversarial search/RAG poisoning**: The research assumes web search returns genuine results, but recent evidence shows ~250 malicious documents can poison RAG retrieval (PoisonedRAG, USENIX Security 2025). This is an uncovered failure mode specific to web-search-dependent research.

2. **Context degradation ("lost in the middle")**: Maximum effective context window can differ from claimed by up to 99% (Paulsen 2025). Models show 30%+ performance drops for information in the middle of context. This within-step degradation is not captured by the error compounding formula.

3. **Collective intelligence / aggregation theory**: The convergence phase uses unstructured qualitative synthesis. Empirically-validated aggregation methods (accuracy-weighted, confidence-weighted) from collective intelligence research could improve this (Kameda et al. 2022, Nature Reviews Psychology).

4. **Anti-cherry-picking dependency**: Recommendation #5 (anti-cherry-picking) should not be implemented without simultaneously implementing #7 (GRADE-adapted confidence). Including contradictory sources without quality weighting creates "garbage in" risk.

5. **Lateral reading redundancy for AI agents**: AI agents already perform something like lateral reading by default (searching the web about sources). The 71% RCT improvement was measured in humans correcting a human cognitive limitation (vertical reading fixation) that AI agents may not share.

---

## Shelf Life Assessment

| Component | Reliability | Basis |
|-----------|------------|-------|
| Architecture validation (decompose → delegate → converge → verify) | 2-3 years | Pattern is stabilizing; may be disrupted by much larger context windows |
| Recall gap / multi-query requirement | 5+ years | Fundamental property of information retrieval |
| Lateral reading effectiveness | 5+ years | Epistemic principle; RCT-validated |
| Citation fabrication rates (specific numbers) | 3-6 months | Model-dependent; improving rapidly |
| Error compounding formula | Indefinite | Mathematical relationship |
| Sycophancy patterns | 12-18 months | Active research area; mitigation improving |
| GRADE-adapted confidence | 5+ years | Institutional framework; slow-moving |
| Multi-agent failure taxonomy (MAST) | 12-18 months | New frameworks emerging |
| Bipolar bias insight | 5+ years | Empirically confirmed; stable psychological finding |
| Specific benchmark numbers | 3-6 months | Rapidly evolving |

**Overall**: Re-evaluate AI-specific recommendations (Tiers 1-2 items 3, 4, 12) by early 2027. Methodology recommendations (items 1, 2, 5, 6, 8, 9, 11) remain valid through 2028+.

---

*Research conducted February 2026. Seven parallel web-researcher agents across seven disciplines, followed by convergence analysis, synthesis, and three-wave adversarial verification (claim verification, counter-case construction, missing alternatives). Three critical factual errors found and corrected during adversarial verification; five significant qualifications added. No critical or significant research gaps identified after Wave 1. All findings are meta-research — research about research methodology — and carry the inherent limitation that no technique has been empirically validated specifically for AI-mediated web research.*
