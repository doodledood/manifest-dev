# Applied Epistemology & Critical Thinking Transfer to AI-Mediated Research

**Last Updated**: 2026-02-18
**Shelf Life**: Core philosophical frameworks (Toulmin, Bayesian epistemology, virtue epistemology, epistemology of disagreement) are stable — reliable for 5+ years. Calibration research (Tetlock, superforecasting) is empirically grounded and stable for 3-5 years. AI-specific findings (LLM calibration, anti-Bayesian drift) are volatile: 12-18 month shelf life as models improve. The bipolar bias finding (Mandel & Tetlock 2018) is stable and underappreciated.

---

## Key Findings at a Glance

- **Calibration training can backfire**: Mandel & Tetlock (2018) showed treating overconfidence as a unipolar bias risks creating underconfidence. Kelly & Mandel (2024) confirmed empirically: calibration training on 70 intelligence analysts improved interval estimation but **worsened** binary confidence, exacerbating existing underconfidence [PRIMARY]. This directly challenges any CLAUDE.md instruction to "be less confident" — the correction can overshoot.
- **Superforecasting practices transfer well**: Tetlock's superforecasters were 30% more accurate than intelligence officers with classified information. Key practices — decomposition, inside/outside view balance, granular probability expression — map directly to research process rules [PRIMARY].
- **Toulmin argumentation improves AI reasoning**: Critical-Questions-of-Thought (CQoT, 2024) using Toulmin-schema questioning **outperformed chain-of-thought prompting** on MT-Bench reasoning tasks [PRIMARY]. MITRE (2004) found Toulmin structures improved critical evaluation even with minimal training [PRIMARY].
- **LLMs exhibit anti-Bayesian drift**: When challenged, models become MORE confident rather than appropriately updating toward uncertainty [PRIMARY]. Prompting alone is insufficient — structural interventions are required.
- **Epistemic virtues can be operationalized as process rules**: Thoroughness, open-mindedness, carefulness, intellectual courage, and humility map to specific CLAUDE.md process components [PRIMARY: VICS 2024; PRIMARY: AI and Ethics 2025].
- **Disagreement resolution should be context-dependent**: Conciliation for factual disputes among equal-authority sources; steadfastness (preserve both positions) for open questions where further evidence could emerge [PRIMARY: Stanford Encyclopedia].

---

## Definitions

| Term | Definition |
|------|-----------|
| **Calibration** | The degree to which expressed confidence matches actual accuracy. A perfectly calibrated forecaster's 80% predictions come true 80% of the time. |
| **Bipolar bias** | The insight (Mandel & Tetlock 2018) that cognitive biases like overconfidence are not unipolar (always in one direction) — correction can overshoot into the opposite bias (underconfidence). |
| **Bayesian updating** | Revising probability estimates in light of new evidence using Bayes' theorem: P(H\|E) = P(E\|H) × P(H) / P(E). |
| **Toulmin model** | Six-component argument structure: Claim, Grounds, Warrant, Backing, Qualifier, Rebuttal (Toulmin 1958). |
| **Epistemic humility** | Meta-cognitive ability to recognize the limitations of one's beliefs and knowledge. Not synonymous with low confidence — compatible with high confidence where evidence warrants it. |
| **Conciliationism** | Position that discovering an epistemic peer disagrees should prompt belief revision toward the peer's view. |
| **Steadfastness** | Position that it can be rational to maintain one's belief in the face of peer disagreement, grounded in self-trust or asymmetry of evidence access. |
| **Ecological rationality** | Gigerenzer's program showing that fast, frugal heuristics outperform formal optimization in certain well-structured environments. |
| **Anti-Bayesian drift** | Empirically observed LLM behavior of becoming more confident (not less) when encountering counter-evidence. |

---

## Calibration and Superforecasting: The Highest-Value Transfer

### What Superforecasters Do Differently

Tetlock's IARPA-funded Good Judgment Project identified superforecasters who were **30% more accurate than intelligence officers with classified information** [PRIMARY: PMC 2020]. They achieved near-perfect calibration — their 80% predictions came true approximately 80% of the time. The practices that distinguished them:

1. **Decompose problems** into knowable and unknowable parts
2. **Balance inside and outside views** — "how often do things of this sort happen in situations of this sort?"
3. **Update beliefs skillfully** in response to new evidence
4. **Distinguish degrees of doubt** with numeric probabilities rather than vague verbal qualifiers
5. **Conduct unflinching postmortems** to learn from prediction failures

The overconfidence problem is pervasive: professional economic forecasters report 53% confidence but are correct only 23% of the time [PRIMARY: Collabra 2024]. Human-LLM hybrids using superforecasting prompts improve accuracy 23-43% [PRIMARY].

### The Bipolar Bias Warning

Mandel & Tetlock's (2018) most consequential finding: **the intelligence community treats overconfidence as a unipolar problem requiring reduction, but this ignores underconfidence as an equal and opposite error** [PRIMARY: Frontiers in Psychology]. Training focused solely on reducing overconfidence can overshoot into underconfidence, "watering down the informativeness of intelligence assessments for decision makers with excessive uncertainty."

Kelly & Mandel (2024) confirmed empirically: a commercial calibration training course on 70 intelligence analysts improved interval estimation calibration but **worsened binary event confidence**, exacerbating existing underconfidence [PRIMARY: Applied Cognitive Psychology]. The training shifted bias toward less confidence indiscriminately rather than improving metacognitive monitoring.

Additional evidence that calibration training has limits:
- Martin et al. (2025): Scalable feedback-based training using the Practical Scoring Rule **failed to improve calibration** across two experiments (N=610, N=871) [PRIMARY: Futures & Foresight Science]
- Gruetzemacher et al. (2024): Interactive app-based training "modestly" reduced overconfidence but effects were "preliminary" [PRIMARY]
- For AI systems specifically: reasoning-enhanced LLMs show **worse calibration** (ECE=0.395 for GPT-5.2-XHigh) despite comparable accuracy [PRIMARY]

### Concrete Implementation for CLAUDE.md

**Proposed change**: Modify the confidence expression guidance. Instead of "state confidence levels explicitly" (current), specify: "Express confidence using granular numeric ranges (e.g., '~70-80% confident' rather than 'moderately confident'). Calibrate both directions — both overconfidence AND underconfidence degrade research quality. When evidence strongly supports a conclusion, say so clearly rather than hedging reflexively."

**Feasibility**: Moderate. AI agents can express numeric confidence, but LLM verbal confidence correlates poorly with actual accuracy [PRIMARY: ACL Findings 2025]. The value is in forcing explicit uncertainty reasoning, not in the precision of the number itself.

**What would make this wrong?** If numeric confidence expressions create false precision — readers treating "75% confident" as meaningfully different from "70% confident" when the underlying assessment is imprecise. Mitigation: use ranges rather than point estimates, and accompany numeric expressions with the reasoning chain that produced them.

---

## Bayesian Evidence Evaluation: The Formal Structure

### Core Principles

Bayesian epistemology provides the formal structure for weighing evidence [SECONDARY: Stanford Encyclopedia]:

- **Conditionalization**: Update beliefs by incorporating new evidence — Cr(H|E) = Cr(E|H) × Cr(H) / Cr(E)
- **Likelihood ratios**: Measure evidence strength — how much more likely is the evidence under hypothesis H1 versus H2?
- **Sequential updating**: Each new piece of evidence updates the posterior, which becomes the prior for the next update
- **Prior sensitivity**: When evidence is weak, conclusions are heavily influenced by initial assumptions

**Bayesian Evidence Synthesis (BES)** operationalizes this for research: it combines heterogeneous studies at the hypothesis level via Bayes factors, accommodating different study designs — more flexible than traditional meta-analysis, though it cannot estimate effect sizes [PRIMARY: Behavior Research Methods 2024].

### The "How Many Sources Are Enough?" Question

Bayesian reasoning provides a principled answer: evidence sufficiency depends on the interaction of:
- **Prior probability**: How extraordinary is the claim? (Extraordinary claims require stronger evidence)
- **Evidence strength**: How strong is each piece of evidence? (One strong piece can outweigh many weak ones)
- **Decision threshold**: What level of certainty does the decision require?
- **Evidence diversity**: Diverse evidence sets lead to more robust generalization [PRIMARY: PMC 2019]

This means "corroborate across 2+ independent sources" (current CLAUDE.md guidance) is a reasonable heuristic but not a universal rule. A single authoritative primary source may suffice for uncontroversial claims. Controversial or high-stakes claims may require 5+ independent lines of evidence.

### Limitations for AI Operationalization

- The likelihood ratio is inherently **subjective** — different agents would assign different values
- LLMs exhibit **anti-Bayesian drift**: becoming more confident when challenged rather than appropriately updating [PRIMARY]
- The "problem of old evidence" challenges conditionalization: evidence already incorporated into training data cannot be "newly" processed
- Full Bayesian reasoning requires **logical omniscience** — awareness of all implications of beliefs — which no system achieves

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Research Quality Standards, Cross-referencing: "Evidence sufficiency is proportional to claim stakes and extraordinariness. Routine factual claims: 1-2 authoritative sources sufficient. Contested claims or surprising findings: 3+ independent sources from different methodological traditions. Claims that directly inform recommendations: evidence from multiple independent lines, not just multiple citations within the same research tradition."

**Feasibility**: High as a principle-level guide. The specific number thresholds are heuristics, not formal Bayesian calculations, but they operationalize the underlying principle that evidence requirements scale with claim importance.

**What would make this wrong?** If applying tiered evidence requirements slows research without improving decision quality. Mitigation: keep thresholds simple (2 tiers: routine vs. high-stakes) rather than attempting fine-grained Bayesian calculation.

---

## Toulmin Argumentation: Making Reasoning Chains Explicit

### The Six Components

Toulmin's (1958) model structures arguments into six components [PRIMARY: Argumentation 2005]:

| Component | Role | Research Application |
|-----------|------|---------------------|
| **Claim** | What is being asserted | The research conclusion or recommendation |
| **Grounds** | Evidence supporting the claim | Cited sources and data |
| **Warrant** | The reasoning linking grounds to claim | The inferential step (often implicit and where arguments fail) |
| **Backing** | Support for the warrant itself | Methodological justification for why the inference type is valid |
| **Qualifier** | Degree of confidence | "Probably," "in most cases," "with ~80% confidence" |
| **Rebuttal** | Conditions under which claim fails | "Unless X is true," "except when Y" |

The most valuable component: **warrants**. These are the hidden assumptions linking evidence to claims. Making warrants explicit is where the model adds most value, because **unexposed warrants are where arguments most often fail silently** [PRIMARY: Hitchcock 2005].

### Empirical Evidence for Effectiveness

- **MITRE Corporation (2004)**: Controlled study found Toulmin structures significantly improved critical evaluation of poorly-structured arguments, even with minimal training [PRIMARY]
- **CQoT (2024)**: Critical-Questions-of-Thought, which uses Toulmin-schema-based questioning for LLMs, **outperformed both baseline models and chain-of-thought prompting** on MT-Bench reasoning and math tasks [PRIMARY: arXiv 2024]
- Toulmin observed that "most absolute claims are ultimately false because one counterexample sinks them" — qualifiers and rebuttals are structurally essential

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Intellectual Rigor section: "For each major conclusion, explicitly identify: (1) the evidence (grounds), (2) the reasoning connecting evidence to conclusion (warrant), (3) confidence level (qualifier), and (4) conditions under which the conclusion would not hold (rebuttal). The warrant step is critical — it's where implicit assumptions hide."

**Feasibility**: High. The Toulmin structure maps directly to the existing CLAUDE.md requirement for "argument chain integrity." The specific innovation is requiring explicit warrant identification, which forces the inferential step to be stated rather than assumed.

**What would make this wrong?** If Toulmin-structured output becomes performative — agents producing the six components without genuine reasoning improvement. The MITRE evidence suggests the structure itself improves thinking, but the CQoT evidence is from 2024 and needs replication. Mitigation: adversarial verification should check whether warrants genuinely connect grounds to claims, not just whether they exist.

---

## Epistemic Humility: The Calibration of Uncertainty

### What It Is and Isn't

A systematic review identified 18 separate definitions and 20 measures of intellectual humility, converging on: **a meta-cognitive ability to recognize the limitations of one's beliefs and knowledge** [PRIMARY: Nature Reviews Psychology 2022; PRIMARY: JPA 2021].

Key empirical findings:
- Higher intellectual humility correlates with **superior critical thinking** performance, particularly in evaluation, inference, and self-monitoring [PRIMARY]
- It **reduces overconfidence and myside bias** [PRIMARY]
- It is **NOT synonymous with low confidence** — a person can be intellectually humble and highly confident when evidence warrants it

The critical tension, echoing Mandel & Tetlock: **excessive intellectual humility may foster undue caution or indecision**, potentially hindering timely action in high-stakes scenarios.

### Concrete Implementation for CLAUDE.md

**Proposed change**: Revise the gap honesty requirement: "Knowledge gaps must be stated explicitly and honestly — but gap statements should not become reflexive hedging that undermines well-supported conclusions. Uncertainty expression should be proportional to actual uncertainty, not performative."

**Feasibility**: High as a principle. The difficulty is distinguishing genuine uncertainty from performative hedging in practice. A test: does the uncertainty qualifier change the reader's decision? If not, it's noise.

---

## Disagreement Resolution: What to Do When Sources Conflict

### The Philosophical Framework

The epistemology of disagreement offers two main positions [SECONDARY: Stanford Encyclopedia]:

**Conciliationism**: Discovering an epistemic peer disagrees should prompt belief revision. The strong version (Equal Weight View) says split the difference. Empirically correlates with intellectual humility and actively open-minded thinking [PRIMARY: Cambridge Core].

**Steadfastness**: It can be rational to maintain your belief grounded in self-trust, the asymmetry of direct evidence access, or the "correct evaluator" principle [PRIMARY: Christensen 2009].

### Context-Dependent Resolution

The most applicable framework: **match resolution strategy to disagreement type** [PRIMARY: Springer 2025]:

| Disagreement Type | Recommended Strategy | Rationale |
|-------------------|---------------------|-----------|
| Factual, among equal-authority sources | Conciliation (investigate, split if unresolvable) | No further evidence likely to emerge |
| Open question, ongoing investigation | Steadfastness (preserve both positions) | Premature convergence on possibly false conclusion |
| Methodological, across disciplines | Present both with explicit framing | Different disciplines have different valid assumptions |
| Authority asymmetry (primary vs. tertiary) | Weight toward higher authority | Unless specific reasons to doubt the primary source |

A critical self-undermining problem: conciliationism may be self-defeating because there is disagreement about the epistemology of disagreement itself [SECONDARY: Stanford Encyclopedia].

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Convergence Criteria: "When agents return conflicting findings, classify the conflict type before attempting resolution. Factual conflicts: investigate deeper, favor higher-authority sources, split if truly unresolvable. Open-question conflicts: preserve both positions with explicit framing. Never force resolution of genuine open questions into false consensus."

**Feasibility**: High. This operationalizes the existing CLAUDE.md instruction to "present both positions if unresolvable" by adding the classification step that determines when resolution is appropriate vs. when preserving disagreement is the honest approach.

---

## Informal Fallacies: The Highest-Risk Patterns

### The Three Most Dangerous for Research Synthesis

1. **Confirmation bias**: Biased search, interpretation, and memory that confirms preconceptions. Amplified by algorithmic filtering in digital environments [PRIMARY: Nickerson 1998]. The CLAUDE.md process already addresses this via anti-confirmation-bias search requirements, but the evidence suggests structural interventions are insufficient without genuine counter-hypothesis investigation.

2. **Anchoring**: Over-reliance on first information encountered, leading to insufficient adjustment. In research, the first source found can anchor subsequent interpretation [PRIMARY: extensive anchoring literature]. For AI agents: initial search results may disproportionately influence final conclusions.

3. **Base rate neglect**: Ignoring general prevalence information in favor of case-specific details. Professional forecasters consistently fail at this (53% confident, 23% correct) [PRIMARY: Collabra 2024]. For research: neglecting how often a type of claim is true in general when evaluating a specific instance.

### Meta-Fallacies About Bias

There are six fallacies ABOUT biases themselves [PRIMARY: ACS 2020]:
- Thinking that experts are immune to bias
- Thinking that technology eliminates bias
- Thinking that awareness alone is sufficient
- **The blind spot bias**: recognizing bias in others but not yourself

### Debiasing Effectiveness

Mixed overall, but specific approaches show promise [PRIMARY: PMC 2025]:
- **Natural frequency formats**: Presenting base rates as frequencies rather than probabilities significantly improves reasoning (Cochrane-recommended)
- **Reference class forecasting / outside view**: Tetlock's "how often do things of this sort happen?"
- **Analogical reasoning training**: Group discussion transfers to novel bias scenarios
- **Simple awareness training**: Necessary but insufficient

### Concrete Implementation for CLAUDE.md

The CLAUDE.md process already includes extensive bias mitigation. The epistemological evidence validates the current approach and suggests one addition: Add to agent prompt discipline: "After forming initial conclusions from search results, explicitly apply the outside view: 'How often are claims of this type accurate in general?' This counters both anchoring and base rate neglect."

**What would make this wrong?** If agents cannot meaningfully apply the outside view — i.e., they lack calibrated base rate knowledge. Current LLM calibration is poor, so the value is in prompting the reasoning step even if the resulting base rate estimate is imprecise.

---

## Epistemic Virtues as Process Rules

### The Translation

Jason Baehr identifies nine key intellectual virtues [PRIMARY: SEP; PRIMARY: VICS 2024]. The most operationalizable for AI research:

| Virtue | Process Rule | CLAUDE.md Component |
|--------|-------------|---------------------|
| **Thoroughness** | Comprehensive search coverage, multiple angles | Multi-query search, iterative investigation |
| **Open-mindedness** | Actively seek disconfirming evidence | Anti-confirmation bias, counter-searches |
| **Carefulness** | Uncertainty quantification, explicit confidence | GRADE-adapted labeling, qualifiers |
| **Intellectual courage** | Report findings that contradict expectations | PG-9: hidden framing bias mitigation |
| **Intellectual humility** | Acknowledge knowledge gaps, qualify claims | Gap honesty requirement |
| **Honesty** | Transparency about sources, methods, limitations | Evidence traceability, deviation tracking |

Emerging AI research supports this translation: a 2025 paper in *AI and Ethics* demonstrates that epistemic virtues like honesty, thoroughness, clarity, and open-mindedness can guide ML design choices [PRIMARY]. A 2022 paper in *AI & SOCIETY* operationalizes epistemic frameworks as critical questions for AI assessment [PRIMARY].

### Important Limitation

Epistemic situationism — empirical psychology suggesting people often manifest cognitive defects rather than virtues — challenges whether virtues can be reliably instantiated [SECONDARY: SEP]. This actually **supports** structural/procedural safeguards over reliance on "character": don't rely on agents being virtuous; build virtue-aligned behavior into the process structure.

### Concrete Implementation for CLAUDE.md

The CLAUDE.md process already embodies most of these virtues as process rules. The epistemological evidence provides theoretical grounding and validates the approach: structural embodiment of epistemic virtues in process rules is more reliable than relying on agents to spontaneously manifest virtuous reasoning.

---

## Evidence Hierarchies Beyond Source Type

### Foundationalism vs. Coherentism

Two competing models for how evidence justifies belief [SECONDARY: Stanford Encyclopedia]:

**Foundationalism**: Certain "basic beliefs" (direct observations, primary data) are self-justifying and serve as foundations. A single strong authoritative source can anchor a conclusion.

**Coherentism**: Justification arises from mutual support, consistency, and holistic fit among beliefs. Multiple individually weak pieces of evidence can collectively justify a belief through coherence.

**Critical challenge**: Formal impossibility theorems (Bovens & Hartmann; Olsson) show that **no way to formalize coherence guarantees that greater coherence increases the probability of joint truth** [SECONDARY: Stanford Encyclopedia]. A highly coherent system of beliefs can be completely divorced from reality.

**Practical resolution**: Anchor findings in authoritative primary sources wherever possible (foundationalism), AND cross-reference across independent sources for coherence (coherentism). Neither alone is sufficient. This maps directly to the CLAUDE.md dual requirement: authority hierarchy (foundational) AND cross-referencing (coherentist).

### Concrete Implementation for CLAUDE.md

The current dual approach (authority hierarchy + cross-referencing) is epistemologically sound. The addition: make explicit that cross-referencing checks **independence** of sources, not just agreement. Three sources that all cite the same underlying study provide foundational support, not coherentist corroboration.

---

## Counter-Evidence: When Formal Frameworks Hurt

### Gigerenzer's Ecological Rationality

Fast and frugal heuristics outperform formal optimization in some environments, particularly well-structured ones with clear cues [PRIMARY: Gigerenzer 2004]. This means:

- Not every research task benefits from maximum epistemological formality
- Simple heuristics ("trust the highest-authority source") may be perfectly adequate for routine fact-checking
- Formal frameworks add most value in novel, uncertain, multi-source synthesis tasks — which is the CLAUDE.md target use case

### The Counter-Argument to This Entire Document

**Strongest counter-argument**: Informal, intuitive reasoning by skilled practitioners may be "good enough" for most research, and adding formal epistemological structure creates overhead without proportionate benefit. Expertise partly consists of knowing when NOT to formalize.

**Response**: This is valid for well-structured, familiar domains. But the CLAUDE.md process targets novel, uncertain, multi-source synthesis — exactly where Gigerenzer's research shows formal structure adds value. The recommendation is discriminate application: full epistemological machinery for high-stakes comprehensive research; lighter touch for routine queries.

---

## Prioritized Recommendations

### P1: Implement Immediately

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Bipolar calibration awareness | Modify confidence guidance to warn against BOTH overconfidence and underconfidence | Prevents reflexive hedging that degrades research quality | Low: awareness-level change |
| Explicit warrant identification | Add to argument chain integrity: require stating the inferential step connecting evidence to conclusion | Exposes hidden assumptions where arguments fail | Low: CQoT evidence supports this |
| Context-dependent disagreement resolution | Add conflict classification before resolution | Prevents forcing false consensus on genuinely open questions | Low: formalizes existing "present both positions" guidance |

### P2: Implement After P1 Validated

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Tiered evidence sufficiency | Scale source requirements to claim stakes/extraordinariness | Better resource allocation; prevents both under- and over-investigation | Medium: threshold calibration may be wrong |
| Outside view prompting | Add reference class forecasting step after initial conclusions | Counters anchoring and base rate neglect | Medium: agents' base rate knowledge may be unreliable |
| Source independence verification | Require checking whether corroborating sources are genuinely independent | Prevents circular corroboration | Low: small additional check per key claim |

### P3: Implement When P1-P2 Are Stable

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Granular numeric confidence | Express confidence as ranges (70-80%) rather than verbal qualifiers | Forces explicit uncertainty reasoning | Medium: false precision risk; verbal confidence in LLMs is poorly calibrated |
| Toulmin template for key conclusions | Structured Claim/Grounds/Warrant/Qualifier/Rebuttal for top-level conclusions | Makes reasoning fully auditable | Medium: template fatigue risk |

---

## Knowledge Gaps

1. **LLM anti-Bayesian drift is documented but not well-characterized**: The finding that LLMs become more confident when challenged is striking but comes from limited studies. The mechanisms and prevalence across models are not well understood. [Gap severity: Significant]
2. **Calibration training for AI is nascent**: Most calibration research targets humans. Whether Tetlock's practices transfer to AI agents via prompting is theoretically plausible but empirically untested. [Gap severity: Significant]
3. **Toulmin + AI evidence is thin**: CQoT (2024) is a single study. Replication needed. The MITRE study tested humans, not AI. [Gap severity: Minor]
4. **Impossibility theorems undermine coherentism**: No formal coherence measure guarantees truth approximation. Cross-referencing is practically useful but lacks iron-clad theoretical foundation. [Gap severity: Minor — practically manageable]
5. **Ecological rationality boundary is unclear**: Gigerenzer's work shows formal frameworks can hurt in well-structured environments, but the boundary between "well-structured" and "complex/novel" environments is not precisely defined for AI research tasks. [Gap severity: Minor]
6. **Limited primary philosophy engagement**: Research relied mostly on secondary accounts (encyclopedias, reviews) rather than direct engagement with primary philosophical texts. [Gap severity: Minor]

---

## Source Authority Assessment

| Source | Authority | Notes |
|--------|-----------|-------|
| Mandel & Tetlock (2018) Bipolar bias | Highest [PRIMARY] | Frontiers in Psychology; foundational correction to debiasing literature |
| Kelly & Mandel (2024) Calibration training | High [PRIMARY] | Applied Cognitive Psychology; empirical confirmation |
| Tetlock superforecasting (PMC 2020) | High [PRIMARY] | IARPA-funded, extensively replicated |
| Porter et al. (2022) Intellectual humility | High [PRIMARY] | Nature Reviews Psychology |
| MITRE (2004) Toulmin evaluation | High [PRIMARY] | Controlled empirical study |
| Hitchcock (2005) Good reasoning on Toulmin | High [PRIMARY] | Argumentation journal |
| Nickerson (1998) Confirmation bias | Highest [PRIMARY] | Definitive review; 5,000+ citations |
| Stanford Encyclopedia entries | High [SECONDARY] | Peer-reviewed; regularly updated |
| Martin et al. (2025) Scoring rule training | High [PRIMARY] | Two large-N experiments |
| Bayesian Evidence Synthesis (2024) | High [PRIMARY] | Behavior Research Methods |
| CQoT (2024) | Moderate [PRIMARY] | arXiv; single study, not yet peer-reviewed |
| VICS (2024) | High [PRIMARY] | PMC peer-reviewed |
| Gigerenzer (2004) Ecological rationality | Highest [PRIMARY] | Foundational counter-evidence |
| AI and Ethics (2025) Virtues for ML | High [PRIMARY] | Peer-reviewed |
| Collabra (2024) Overprecision | High [PRIMARY] | Peer-reviewed |

No claims rest solely on tertiary sources.

---

## Adversarial Stress-Testing

**Strongest counter-argument encountered**: Formal epistemological frameworks are unnecessary overhead for AI-mediated research. Gigerenzer's ecological rationality shows that simple heuristics outperform formal optimization in well-structured environments, and most research tasks are routine enough for heuristic approaches. **Response**: Valid for simple fact-checking and known-item retrieval. The CLAUDE.md process targets deep, adversarial, multi-angle research — exactly the complex, novel environment where ecological rationality research shows formal structures add value. The recommendation is discriminate application, not universal formalization.

**Second strongest counter-argument**: LLM anti-Bayesian drift and poor verbal calibration mean that epistemological instructions in prompts may be ineffective — agents will comply performatively without genuine reasoning improvement. **Response**: This is the most serious concern. The CQoT evidence suggests Toulmin structures DO improve LLM reasoning, but it's a single study. The mitigation strategy is structural: use explicit warrant identification and disagreement classification as verifiable process steps, not just aspirational instructions. Adversarial verification provides the backstop.

**Third counter-argument**: The bipolar bias finding applies to human calibration training but may not transfer to AI systems. LLMs may not "overshoot" in the same way humans do. **Response**: The existing evidence on LLM confidence (reasoning-enhanced models showing WORSE calibration) suggests the analog exists — more processing doesn't automatically improve confidence quality. The recommendation (calibrate in both directions) is a low-cost insurance against both failure modes.

**Unresolved tension**: This document recommends explicit uncertainty quantification (qualifiers, numeric confidence, gap statements) while also warning that excessive hedging degrades research quality (bipolar bias). The optimal balance between honest uncertainty and decisive communication is context-dependent and cannot be specified algorithmically.
