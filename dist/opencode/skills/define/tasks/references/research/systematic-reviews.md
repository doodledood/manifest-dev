# Systematic Review Methodology Transfer to AI-Mediated Research

**Last Updated**: 2026-02-17
**Shelf Life**: Core systematic review (SR) frameworks are stable institutions with 3-5 year update cycles (PRISMA last revised 2020, Cochrane Handbook v6.5 current). AI evidence synthesis findings are volatile: 6-12 month shelf life due to rapid capability changes. Revisit AI-specific feasibility assessments by early 2027.

---

## Key Findings at a Glance

- Systematic review methodology offers **process-level controls** (checklists, pre-registration, structured bias assessment) that transfer well to AI research orchestration -- but domain adaptation is non-trivial and historically fails when attempted as direct transplant [PRIMARY: Kitchenham 2007, ACM 2006].
- **GRADE-adapted confidence labeling** is the highest-value transfer: it forces explicit uncertainty quantification at every claim, directly addressing the false-precision bias the CLAUDE.md process already warns against.
- **Protocol pre-specification** (analogous to PROSPERO registration) maps naturally onto the existing manifest system, but the manifest currently lacks deviation tracking -- the mechanism that makes pre-registration actually work.
- **Anti-cherry-picking rules** from inclusion/exclusion criteria fill a structural gap: no existing CLAUDE.md mechanism prevents agents from silently dropping sources that contradict the emerging narrative.
- **Current AI evidence synthesis accuracy is poor**: compounding 5% per-step error rates yields ~81.5% overall accuracy [PRIMARY: A4SLR 2025], and LLM hallucination rates reach 31% in data extraction tasks [PRIMARY: AI Evidence Synthesis 2024]. The RAISE framework (Cochrane/Campbell/JBI 2024-25) explicitly states current evidence "does not support GenAI use in evidence synthesis without human involvement" [PRIMARY].
- Selective adoption outperforms wholesale transfer. Software engineering's attempt to adopt SR methodology wholesale starting ~2004 had "little impact on industry practice" [PRIMARY: Kitchenham 2007].

---

## Definitions

| Term | Definition |
|------|-----------|
| **Systematic review (SR)** | Research method using pre-defined, transparent, reproducible procedures to identify, evaluate, and synthesize all relevant evidence on a specific question. Distinguished from narrative reviews by explicit methodology. |
| **PRISMA** | Preferred Reporting Items for Systematic Reviews and Meta-Analyses. 27-item reporting checklist (Page et al., BMJ 2021). A reporting standard, not a conduct standard. |
| **Cochrane** | International organization producing gold-standard systematic reviews in healthcare. Relevant here for procedural rigor (MECIR standards), not medical content. |
| **GRADE** | Grading of Recommendations, Assessment, Development and Evaluation. Evidence certainty rating across four levels (High/Moderate/Low/Very Low), used by 110+ organizations. |
| **RoB 2** | Risk of Bias 2 tool. Domain-based instrument using structured signaling questions to assess bias in individual studies. |
| **PROSPERO** | International prospective register of systematic reviews. Pre-registration mechanism that locks methodology before results are known. |
| **MECIR** | Methodological Expectations of Cochrane Intervention Reviews. 75 standards classified as mandatory or highly desirable. |

---

## GRADE-Adapted Confidence Assessment: Highest-Value Transfer

### Why This Matters Most

The CLAUDE.md process already uses an evidence tier system (PRIMARY/SECONDARY/TERTIARY) that classifies source authority. What it lacks is a systematic mechanism for **downgrading confidence based on evidence quality dimensions beyond source type**. A claim backed by three primary sources can still be low-confidence if those sources are inconsistent, indirect, or imprecise. GRADE provides exactly this framework.

### The GRADE System and Its Track Record

GRADE rates evidence certainty as High, Moderate, Low, or Very Low [PRIMARY: GRADE Working Group]. A sobering calibration point: only 4% of Cochrane review evidence -- produced by the most rigorous SR methodology in existence -- achieves "High." 27% rates "Low" and 26% "Very Low" [PRIMARY: GRADE Environmental Health 2019]. Honest confidence assessment reveals far more uncertainty than most research processes acknowledge.

### Adapted Downgrading Domains for AI Research

The five GRADE downgrading domains adapt to web research as follows [PRIMARY: GRADE Working Group; adapted by analysis]:

| GRADE Domain | AI Research Adaptation | What It Catches |
|--------------|----------------------|-----------------|
| Risk of bias | Source credibility and methodology transparency | Marketing masquerading as analysis, undisclosed conflicts |
| Inconsistency | Agreement across independent sources | Claims that look solid from one source but contradict others |
| Indirectness | How directly evidence addresses the research question | Analogical reasoning presented as direct evidence |
| Imprecision | Specificity of claims and data | Vague qualitative claims where quantitative data should exist |
| Publication bias | Asymmetry in available evidence | Vendor-dominated search results, missing negative findings |

Three upgrading factors (large effect size, dose-response gradient, plausible confounding) have limited but non-zero applicability. When multiple independent sources converge without coordination, confidence increases.

### Concrete Implementation for CLAUDE.md

**Proposed change**: After the existing evidence tier label on each claim, add a confidence modifier. Format: `[PRIMARY | High confidence]` or `[PRIMARY | Low confidence: inconsistency, indirectness]`. This forces evaluation across the five domains, not just source classification.

**Feasibility**: Moderate. AI agents can apply four of five domains but will struggle with publication bias (requires awareness of what *should* exist but doesn't). Recommended for P1 with publication bias as aspirational.

**What would make this wrong?** Per-claim GRADE assessment could slow synthesis without improving decisions. Mitigation: apply full assessment only to claims that directly inform recommendations; lightweight labeling for supporting claims. This matches GRADE's own guidance that "effort should be proportional to the importance of the outcome" [PRIMARY: GRADE Working Group].

---

## Protocol Pre-Specification and Deviation Tracking

### The Evidence for Pre-Registration

Pre-registration is one of the most empirically validated interventions against researcher degrees of freedom. Kaplan and Irvin documented a "dramatic drop in positive results" after mandatory clinical trial pre-registration, confirming that post-hoc methodology adjustment inflates findings [PRIMARY: Nosek 2018; PRIMARY: Lakens 2024]. PROSPERO-registered reviews show significantly higher quality than unregistered ones [PRIMARY: PROSPERO].

### Current State in the CLAUDE.md Process

The research manifest already functions as a protocol, structurally analogous to PROSPERO registration. However, a critical piece is missing: **deviation tracking**. Pre-registration's value comes not from preventing all deviations but from making them visible and justified.

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add a `## Protocol Deviations` section to research output. Any departure from the manifest -- changed research questions, dropped agents, added scope, modified quality thresholds -- must be documented with rationale. This is a lightweight change with high anti-bias value.

**Feasibility assessment**: High. The manifest is already written before execution. Tracking deviations requires only that the synthesizing agent compare its actual process against the manifest and report differences. No new capability required.

**Failure mode**: Deviation tracking becomes performative -- agents list deviations without honestly assessing whether they biased results. Mitigation: adversarial verification agents should specifically check whether protocol deviations systematically favor one conclusion.

---

## Anti-Cherry-Picking: Inclusion/Exclusion Discipline

### The Gap This Fills

The CLAUDE.md process has strong guidance on source authority and cross-referencing, but no explicit rule preventing the subtle dropping of inconvenient sources. In SR methodology, inclusion/exclusion criteria are pre-specified and critically: **sources are never excluded solely because findings contradict the emerging narrative** [PRIMARY: Cochrane Handbook Ch 3; PRIMARY: AHRQ].

### PICO Adaptation for AI Research

The PICO framework (Population, Intervention, Comparison, Outcome) was designed for clinical questions but adapts to research decomposition [PRIMARY: Cochrane Handbook Ch 3]:

| PICO Element | Medical SR | AI Research Adaptation |
|--------------|-----------|----------------------|
| Population | Patient group | Topic scope / domain boundaries |
| Intervention | Treatment studied | Approach, technology, or method under investigation |
| Comparison | Alternative treatment | Alternative approaches or status quo |
| Outcome | Health outcome measured | Decision criteria that findings must address |

**Counter-evidence on PICO transfer**: SE's attempt to adopt PICO directly "doesn't map well" [PRIMARY: Kitchenham 2007]. The *structural discipline* of pre-specified scope transfers, but specific categories need domain reformulation.

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to the Orchestrating Web Research section: "Sources meeting inclusion criteria (relevant topic, adequate authority level) must never be excluded solely because findings contradict the emerging narrative. Contradictory sources must be engaged -- either by incorporating contrary evidence or by documenting why the source's methodology is flawed."

**Feasibility**: High. Behavioral rule, verifiable during adversarial review.

**What would make this wrong?** Could give undue weight to low-quality contrarian sources. Mitigation: existing authority hierarchy still applies. A tertiary blog contradicting primary sources gets noted as a gap, not elevated.

---

## PRISMA-Adapted Output Checklist

### Selective Transfer from 27 Items

Of PRISMA's 27 items [PRIMARY: Page et al., BMJ 2021], 10 adapt meaningfully to AI research output. The remaining 17 are specific to meta-analytic statistics or registration databases with no AI analog.

Critical insight: Cochrane Reviews score highest on PRISMA compliance because of **mandatory editorial enforcement**, not voluntary guidelines. General SRs show only ~43% average adherence [PRIMARY: Ivaldi 2024]. Checklists work only when enforced structurally.

### The 10 Transferable Items

| PRISMA Item | AI Research Adaptation | Enforcement Mechanism |
|-------------|----------------------|----------------------|
| Eligibility criteria | Pre-specified source inclusion/exclusion rules | Include in manifest |
| Information sources | List of search engines, databases, and domains queried | Agent output template |
| Search strategy | Actual search queries used by each agent | Agent output template |
| Selection process | How sources were screened and selected | Agent output template |
| Risk of bias in studies | Source credibility assessment per authority hierarchy | Required section in output |
| Certainty assessment | GRADE-adapted confidence labels on key claims | Required per-claim labels |
| Study selection flow | Count of sources found, screened, included, excluded with reasons | Summary table in output |
| Certainty of evidence | Overall confidence in conclusions | Required concluding assessment |
| Limitations | Acknowledged gaps and weaknesses | Required section in output |
| Protocol reference | Link to manifest or protocol that governed research | Header metadata |

### Concrete Implementation for CLAUDE.md

**Proposed change**: Build these 10 items into the output template as required sections. Weight toward items that catch real problems (certainty assessment, limitations, search flow) over documentation overhead (protocol reference in low-stakes research).

**Feasibility**: Moderate. Risk is template fatigue for small research tasks. Mitigate with tiered application: full checklist for comprehensive research, abbreviated for quick lookups. "Enforcement" means structurally embedded in the output template, not referenced as optional guidelines -- the ~43% average voluntary compliance rate proves aspirational checklists fail [PRIMARY: Ivaldi 2024].

---

## Bias Assessment via Adapted RoB 2 Signaling Questions

### Domain-Based Assessment Structure

RoB 2 uses structured signaling questions within defined domains, feeding into algorithm-based bias judgments [PRIMARY: RoB 2]. The key innovation: **bias assessment becomes systematic rather than impressionistic** -- instead of a vague sense that a source "seems biased," the assessor works through specific domains with defined questions.

### Adapted Domains for Web Sources

| Domain | Signaling Questions | Risk Levels |
|--------|-------------------|-------------|
| **Source selection bias** | Were sources identified through comprehensive search? Could search strategy systematically miss contrary evidence? | Low / Some concerns / High |
| **Methodology/provenance bias** | Does the source disclose methodology? Is there commercial interest? Is the author identifiable and credentialed? | Low / Some concerns / High |
| **Missing information bias** | Are key caveats, limitations, or contrary findings absent? Does the source acknowledge uncertainty? | Low / Some concerns / High |
| **Measurement/extraction bias** | Could information have been extracted inaccurately? Are claims verifiable against cited sources? | Low / Some concerns / High |
| **Reporting selection bias** | Does the source selectively report favorable results? Is there asymmetry between methods and conclusions? | Low / Some concerns / High |

### Feasibility and Limitations

RoB 2 takes ~28 minutes per study; ROBINS-I takes 3-7 hours [PRIMARY: tool comparison study]. A lightweight AI adaptation targeting three domains (source selection, methodology/provenance, missing information) could run in seconds as a structured prompt.

**Calibration warning**: 75% of studies rated "Low risk" by NOS were rated higher risk by ROBINS-I [PRIMARY: tool comparison study] -- tool choice determines outcome. Use bias assessment for structured thinking, not false precision.

### Concrete Implementation for CLAUDE.md

**Proposed change**: For high-stakes research (P2), require agents to assess the top 3-5 most influential sources against the adapted domains. Do not apply to every source -- only those on which key conclusions depend.

**What would make this wrong?** The >50% error rate for LLMs in automated bias assessment [PRIMARY: AI Evidence Synthesis 2024] is a real risk. Mitigation: use bias assessment as a structured thinking prompt, not an automated pass/fail gate. The value is in forcing the questions to be asked, not in the algorithmic judgment.

---

## Where Systematic Review Methodology Does Not Transfer

### Software Engineering's Cautionary Tale

EBSE attempted wholesale SR methodology adoption starting ~2004. Result: PICO didn't map to SE research questions, costs were disproportionate to benefits, and the approach had "little impact on industry practice" [PRIMARY: Kitchenham 2007; PRIMARY: ACM 2006]. The lesson: **domain adaptation is not optional** -- techniques must be reformulated for the target domain, not just relabeled.

### AI-Specific Accuracy Limitations

Current evidence on AI performance in evidence synthesis is sobering [PRIMARY: A4SLR 2025; PRIMARY: AI Evidence Synthesis 2024]:

| Task | AI Error Rate | Implication |
|------|--------------|-------------|
| Overall SR pipeline (5% per-step error) | ~81.5% cumulative accuracy | Errors compound across multi-step processes |
| Data extraction | 31% hallucination rate | Factual claims require verification |
| Automated bias assessment | >50% error rate | Cannot be trusted as automated judgment |

The RAISE framework (Cochrane/Campbell/JBI 2024-25) represents current expert consensus: GenAI in evidence synthesis requires human oversight [PRIMARY]. For CLAUDE.md: adversarial verification is not optional overhead but a necessary correction for systematic AI error.

Even human-conducted SRs are error-prone: 75% of meta-analyses contain at least one error [PRIMARY: Uttley JCE 2023]. This suggests structured process controls are worth pursuing precisely because the alternative -- unstructured review -- is worse.

### The Steelman Against Transferring SR Methodology

**Strongest counter-argument**: SR methodology was designed for synthesizing controlled experiments where errors kill people. AI-mediated web research operates on uncontrolled sources, qualitative judgments, and lower stakes. Three specific risks:

1. **Overhead disproportionate to value**: Full GRADE assessment of every claim is orders of magnitude more work than warranted.
2. **False rigor**: SR-style checklists may create an *appearance* of rigor without substance -- data quality is too low for the machinery to improve it.
3. **Wrong failure modes**: SR guards against p-hacking and underpowered studies. AI failures are hallucination and shallow synthesis -- different problems.

**Engagement**: Points 1 and 3 inform the selective approach here (tiered application, adapting *principles* not procedures). Point 2 is the most dangerous: performative rigor can only be mitigated by adversarial verification testing substance, not form.

---

## Prioritized Recommendations

Ordered by expected value (impact on research quality per unit of implementation effort).

### P1: Implement Immediately

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| GRADE-adapted confidence labels | Add downgrading-domain modifiers to evidence tier labels | Catches false precision, forces uncertainty quantification | Low: worst case is minor overhead on claim labeling |
| Manifest deviation tracking | Add required `## Protocol Deviations` section to research output | Prevents invisible methodology drift | Low: worst case is an extra section occasionally reading "None" |
| Anti-cherry-picking rule | Add explicit rule that sources meeting inclusion criteria cannot be excluded for contradictory findings | Prevents confirmation bias at source selection stage | Low: existing authority hierarchy prevents noise amplification |

### P2: Implement After P1 Validated

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| PRISMA-adapted output checklist (10 items) | Create tiered output template with required sections | Standardizes output quality, catches missing elements | Medium: template fatigue if over-applied |
| RoB 2-adapted source assessment | Require structured bias assessment for key sources in high-stakes research | Forces systematic source evaluation | Medium: AI bias assessment error rates are high |
| Search flow accounting | Require agents to report sources found/screened/included/excluded | Enables audit of source selection process | Low: documentation overhead only |

### P3: Implement When P1-P2 Are Stable

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| MECIR-style mandatory/desirable quality tiers | Classify CLAUDE.md quality standards as mandatory vs. desirable | Enables principled abbreviation for lower-stakes research | Medium: wrong classification could weaken standards |
| Pre-specified heterogeneity handling | Rules for when agent findings conflict | Standardizes conflict resolution | Low: current ad-hoc approach may work well enough |
| Dual-agent cross-verification | Independent agents verify each other's key findings for high-stakes research | Catches hallucination and extraction errors | Medium: doubles agent cost; value depends on error rates |

---

## Knowledge Gaps

1. **No empirical validation of adapted frameworks**: All adapted domains and checklists in this document are theoretical transfers. No empirical data exists on whether GRADE-adapted confidence labels actually improve AI research output quality. This is an inherent limitation of a methodology-transfer analysis. [Gap severity: Significant]
2. **Optimal tier thresholds**: When should full GRADE assessment apply versus lightweight labeling? The "proportional to stakes" principle is sound but the specific threshold is undefined. [Gap severity: Minor]
3. **Agent compliance with behavioral rules**: The anti-cherry-picking rule and deviation tracking depend on agent behavioral compliance. No data on how reliably current LLMs follow such meta-cognitive instructions under realistic conditions. [Gap severity: Significant]
4. **Interaction effects between controls**: Implementing multiple SR-adapted controls simultaneously may create unexpected interactions (e.g., bias assessment flagging sources that the anti-cherry-picking rule requires including). [Gap severity: Minor]
5. **Error compounding with added steps**: Adding process steps (checklist, bias assessment, deviation tracking) reduces per-step error types but adds more steps to the pipeline. The A4SLR finding that 5% per-step error compounds to ~81.5% accuracy suggests this trade-off deserves empirical attention. [Gap severity: Significant]

---

## Source Authority Assessment

| Source | Authority | Notes |
|--------|-----------|-------|
| Page et al., BMJ 2021 (PRISMA) | Highest | 13,000+ citations, official PRISMA statement |
| Cochrane Handbook v6.5 | Highest | Institutional gold standard for SR methodology |
| GRADE Working Group | High | 110+ organizations including WHO |
| Kitchenham 2007 / ACM 2006 | High | Foundational EBSE papers |
| RAISE 2024-25 | High | Joint Cochrane/Campbell/JBI position |
| A4SLR 2025 | Moderate-High | Rapidly evolving field; may not generalize beyond tested models |
| Nosek 2018 / Lakens 2024 | High | Lakens notably includes counter-evidence to pre-registration |
| Ivaldi 2024 | Moderate | Single study on PRISMA compliance rates |
| Uttley JCE 2023 | Moderate | Striking finding (75% error rate) would benefit from replication |
| AI Evidence Synthesis 2024 | Moderate | Hallucination rates are model-dependent, may improve rapidly |

No claims rest solely on tertiary sources.

---

## Adversarial Stress-Testing

**Strongest counter-argument encountered**: SR methodology is designed for controlled experiments with quantifiable outcomes; transferring it to qualitative web research may produce performative rigor rather than real quality improvement. **Response**: Valid concern that informed the selective-transfer approach throughout. Only structural principles (pre-specification, explicit confidence, deviation tracking) are transferred, not the specific statistical machinery. The risk of performative rigor is mitigated by adversarial verification testing substance over form.

**Second strongest counter-argument**: AI error rates in evidence synthesis tasks (31% hallucination in extraction, >50% in bias assessment) may make structured bias assessment theater -- the tool is too unreliable to produce trustworthy results. **Response**: This is why the recommendation uses bias assessment as a *structured thinking prompt* rather than an automated gate. The value is in forcing the right questions to be asked, even if the answers require human judgment. The adversarial verification layer provides the backstop.

**Third counter-argument**: The 22% PRISMA compliance rate in general SRs suggests that checklists without enforcement are ineffective, and AI agents may similarly ignore or perfunctorily complete checklist items. **Response**: Valid, and directly addressed by recommending structural embedding (required template sections) rather than aspirational guidelines. Agent compliance is acknowledged as a knowledge gap.

**Unresolved tension**: The document recommends adding process controls while simultaneously citing evidence that more pipeline steps compound errors. Whether the error-reduction from structured assessment outweighs the error-introduction from added steps is an empirical question this analysis cannot answer.
