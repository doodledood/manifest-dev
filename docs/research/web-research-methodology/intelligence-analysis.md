# Intelligence Analysis Tradecraft: Structured Techniques for AI-Mediated Web Research

## Key Takeaways

- **Devil's advocacy has the strongest empirical support** of any Structured Analytic Technique — rated most effective of 12 core SATs (Coulthart 2017) [PRIMARY]. The adversarial verification phase should be structured as devil's advocacy with specific attack vectors, not generic criticism.
- **Key Assumptions Check (KAC)** is the highest-value, lowest-overhead technique: 5 steps, directly surfaces hidden assumptions that otherwise slip through synthesis [PRIMARY/SECONDARY — Georgetown SCS; Pherson Associates]
- **Analysis of Competing Hypotheses (ACH)** has **contested empirical support** — peer-reviewed testing showed mixed results and potentially increased error (Dhami 2019) [PRIMARY]. Use as organizational tool, not debiasing guarantee.
- **ICD 203's 9 tradecraft standards** map 1:1 to research document quality dimensions and provide the most actionable quality checklist [PRIMARY — ODNI]
- **Linchpin analysis** focuses adversarial effort where it matters most — on the 3–5 claims whose failure collapses the most conclusions [SECONDARY — O'Reilly; CIA DDI MacEachin]
- **Cognitive biases are bipolar**: overcorrecting overconfidence can produce underconfidence. Adversarial rounds must check for BOTH false positives AND false negatives (Mandel & Tetlock 2018) [PRIMARY]

---

## Structured Analytic Techniques: What the Evidence Shows

### Taxonomy and Empirical Standing

Richards Heuer and Randolph Pherson cataloged 50+ SATs in three categories: **diagnostic** (make assumptions transparent), **contrarian** (challenge current thinking), and **imaginative** (generate new perspectives). [PRIMARY — CIA Tradecraft Primer, 2009; Heuer, Psychology of Intelligence Analysis, 1999]

| Technique | Empirical Support | Overhead | AI Feasibility | Primary Value |
|---|---|---|---|---|
| Devil's Advocacy | **Strong** (Coulthart 2017, meta-analyses) | Low-Medium | HIGH | Challenges dominant interpretation |
| Key Assumptions Check | Moderate (face validity, case studies) | **Low** | **HIGH** | Surfaces hidden assumptions |
| Pre-mortem | **Strong** (Mitchell et al. 1989, ~30% improvement; Klein built on this) | Low | HIGH | Prospective failure analysis |
| Linchpin Analysis | Moderate (case-study based) | Medium | HIGH | Identifies load-bearing claims |
| ACH (Evidence Matrix) | **Contested** (Dhami 2019) | High | Medium | Forces alternative consideration |

**Critical meta-finding**: RAND Corporation (2016) concluded SATs have received "little systematic evaluation" and only 21–40% of IC products used any SAT. Mandel & Tetlock (2018) found the IC "must discard its antiempiricism." [PRIMARY — RAND RR1408; Mandel & Tetlock, Intelligence & National Security]

**What this means for AI research**: Adopt SATs as **structured process discipline** (ensuring certain analytical steps happen), not as guaranteed debiasing mechanisms. The value is in the structure, not in proven debiasing.

---

## Devil's Advocacy: What Makes It Work vs. Theater

**Evidence**: Devil's advocacy is rated the most effective SAT by Coulthart (2017). Meta-analyses confirm DA is more effective than expert approaches. Research shows "dissent, even when wrong, stimulates divergent thinking." [PRIMARY — Coulthart, IJIC; Defense Science Board Red Teaming Report, 2003]

### What Makes Red Teaming Effective (5 Factors)

1. **Genuine independence** from the team being challenged
2. **Deep perspective immersion** — genuinely adopting an alternative viewpoint, not performing criticism
3. **Trained personnel** — the UFMCS Red Team Leader's Course is 720 academic hours
4. **Organizational willingness to act** on findings
5. **Scaling with stakes** — the Bin Laden raid used 3 separate red teams

### What Makes Red Teaming Fail (Historical Cases)

- **Pearl Harbor 1932**: Rear Admiral Yarnell demonstrated exactly how carriers could attack. Findings were ignored. Nine years later, Japan used essentially the same tactics. [SECONDARY]
- **Team A/Team B 1976**: CIA competitive analysis with hawkish selection bias. Conclusions later found "wildly off the mark" — Soviet threat "substantially overestimated." Lesson: adversarial analysis that stacks the deck introduces new biases. [SECONDARY — CIA Museum, CIA internal review 1989]
- **Dutch DISS**: Devil's advocates seen as outsiders lacking qualifications had insights dismissed. [SECONDARY]

**CLAUDE.md implementation**: The adversarial verification phase already embodies devil's advocacy. The tradecraft evidence adds: (a) adversarial agents need genuine independence — different search strategies and evidence base, not just different prompts; (b) structured attack vectors (claim verification, counter-case construction, data freshness) are more effective than generic "find problems"; (c) Team B teaches that adversarial agents should be balanced truth-seekers with a contrarian mandate, not biased problem-finders.

**What would make this wrong**: If adversarial rounds consistently push toward more hedging and lower confidence, they may produce underconfident, over-qualified research that fails to answer the actual question. This is the Mandel/Tetlock bipolar bias insight applied to AI.

---

## Key Assumptions Check (KAC)

**5-step process** [PRIMARY/SECONDARY — Georgetown SCS; Pherson Associates]:

1. State the analytic conclusion clearly
2. Articulate ALL assumptions (stated and unstated) that must be true for the conclusion to hold
3. Challenge each assumption with W-questions (who, what, when, how, why)
4. Refine to only the load-bearing assumptions
5. Consider what information would test weakened assumptions

**Motivating case**: The DC Sniper investigation assumed the sniper was male, acting alone, white, had military training, and drove a white van. Only 2 of 5 assumptions proved correct, catastrophically narrowing the investigation.

**CLAUDE.md implementation**: Add explicit KAC step after convergence. Common unstated assumptions in AI research:
- The first authoritative-looking source is reliable
- Topic boundaries are correctly drawn
- Absence of contrary evidence means consensus
- Recency equals authority
- Search results represent the full landscape of opinion

**What would make this wrong**: KAC adds a step to the process. If performed perfunctorily (listing obvious assumptions without genuine challenge), it adds overhead without value.

**Feasibility**: HIGH. Low overhead, high yield.

---

## Analysis of Competing Hypotheses (ACH)

**What it is**: Heuer's 8-step evidence matrix process. Core innovation: **diagnosticity** — evidence consistent with all hypotheses has zero diagnostic value. Elimination of hypotheses with the most inconsistent evidence, not confirmation of the most consistent. [PRIMARY — Heuer, Psychology of Intelligence Analysis, Chapter 8]

**Contested empirical evidence**: Dhami et al. (2019) tested ACH with 50 real intelligence analysts. ACH-trained analysts did not follow all steps, showed mixed confirmation bias reduction, and ACH may **increase** judgment inconsistency and error. Over half of untrained analysts spontaneously created ACH-style matrices anyway. [PRIMARY — Applied Cognitive Psychology]

**Steelman for ACH**: The matrix structure forces systematic consideration of alternatives, which is inherently valuable even if the debiasing claims are unproven. A practitioner successfully implemented ACH with GPT-4 using multi-step prompting. [SECONDARY — Roberts, sroberts.io]

**Steelman against ACH**: It has not been subject to "sustained scientific scrutiny" (Mandel & Tetlock). Conclusions are sensitive to small changes in evidence selection. It fails to address biases in hypothesis formation. [PRIMARY — Mandel & Tetlock 2018]

**CLAUDE.md implementation**: Use ACH's matrix structure to **organize** evidence against competing interpretations during convergence, but do not rely on it as a debiasing mechanism.

**Feasibility**: MEDIUM. Computationally natural but LLMs struggle with genuine counterfactual reasoning [PRIMARY — CETaS/Turing 2023].

---

## ICD 203 Tradecraft Standards Mapped to Research Quality

ICD 203 (2007, revised 2015) codifies 9 tradecraft standards for IC analytical products [PRIMARY — ODNI]:

| ICD 203 Standard | AI Research Equivalent | Implementation |
|---|---|---|
| 1. Source credibility | Source authority hierarchy | Tag each source High/Medium/Low with rationale |
| 2. Express uncertainties | Confidence levels per finding | Separate confidence from probability |
| 3. Distinguish assumptions from judgments | Separate evidence from interpretation | Mark sourced facts vs. analyst inferences |
| 4. Analysis of alternatives | Consider competing explanations | Require ≥1 alternative per key finding |
| 5. Customer relevance | Address the actual question | Check synthesis answers the posed question |
| 6. Clear argumentation | Traceable evidence chains | Each conclusion traces to specific sources |
| 7. Explain changes | Track finding evolution | Note when new evidence changes assessments |
| 8. Accurate judgments | Factual correctness | Cross-reference across independent sources |
| 9. Effective visuals | Structured formats | Tables and matrices where helpful |

**IC confidence framework**: High / Moderate / Low. Expected distribution: 40–60% Low, 20–30% Moderate, 10–20% High — meaning **most research findings should honestly be rated Moderate or Low**. [SECONDARY]

---

## Linchpin Analysis

**What it is**: Identify critical assumptions on which an entire analysis depends. 4 steps: identify key variables, determine linchpin premises, marshal evidence for each, identify warning signals. [SECONDARY — O'Reilly; introduced by CIA DDI MacEachin, 1993–1996]

**The deletion test**: Remove or reverse a linchpin assumption; if the conclusion collapses, you have a genuine linchpin requiring strong evidentiary support.

**CLAUDE.md implementation**: After synthesis, identify 3–5 claims whose failure collapses the most conclusions. Focus adversarial effort there. This **reduces adversarial rounds** by targeting verification where it matters most.

**Feasibility**: HIGH.

---

## Cognitive Bias Mapping to AI Research Phases

| AI Research Phase | IC Bias Analog | Mitigation |
|---|---|---|
| **Decomposition** | Anchoring; Mirror imaging | Multiple independent decompositions; Starbursting |
| **Delegation/Search** | Confirmation bias; Availability | Counter-hypothesis searches; Source diversity |
| **Convergence** | Groupthink; Premature closure | Independent evidence development; Gap reporting |
| **Adversarial** | Theatrical challenge; Confirmation | Structured attack vectors; Independence |
| **Synthesis** | Overconfidence; Anchoring; False precision | Pre-mortem; Calibration; Linchpin ID |

**Critical nuance**: Biases are **bipolar**. Suppressing overconfidence can trigger underconfidence. Debiasing must be calibrated. [PRIMARY — Mandel & Tetlock, Frontiers in Psychology, 2018]

---

## Counter-Evidence and Steelmanning

### "IC tradecraft is irrelevant to AI research"

IC tradecraft was designed for human analysts on geopolitical questions with deception. AI research operates in a different domain (factual synthesis), with different failure modes (hallucination vs. cognitive bias), and different constraints (speed vs. deliberation).

**Response**: AI agents exhibit functional analogs of cognitive biases — confirmation bias (favoring first-found sources), anchoring (to initial framing), groupthink (parallel agents converging on popular sources). IC process controls address these structural patterns regardless of mechanism. What doesn't transfer: perspective-shifting requiring genuine empathy or cultural understanding.

### SAT effectiveness is contested

Most SATs adopted on face validity. The empirical record is thin (RAND 2016, Dhami 2019). ACH may increase error.

**Response**: Absence of evidence for effectiveness is not evidence of ineffectiveness. Devil's Advocacy and Pre-mortem have genuine empirical support. The recommendation is selective adoption of evidence-backed techniques, not wholesale SAT adoption.

---

## Gaps and Limitations

- **SAT empirical validation**: Thin for most techniques beyond DA and pre-mortem
- **LLM counterfactual reasoning**: Genuine perspective-shifting may exceed current AI capability [PRIMARY — CETaS 2023]
- **Mirror imaging in AI**: Under-explored; no published research
- **Bipolar bias in adversarial rounds**: Risk of over-hedging not systematically studied

## Shelf Life

- **Foundational tradecraft** (Heuer 1999, ICD 203 2015): Stable. **5+ years**.
- **SAT effectiveness evidence** (RAND 2016, Mandel/Tetlock 2018): Current. **3–5 years**.
- **LLM application** (CETaS 2023, Logan 2024): Fast-moving. **12 months**.

No claims in this document rest solely on tertiary sources.

## Source Authority Assessment

| Source | Authority | Tier | Date |
|---|---|---|---|
| Heuer, *Psychology of Intelligence Analysis* (CIA) | Highest — foundational IC text, widely cited | [PRIMARY] | 1999 |
| ICD 203 Analytic Standards (ODNI) | Highest — governing IC directive | [PRIMARY] | 2007/2015 |
| CIA Tradecraft Primer | Highest — official IC publication | [PRIMARY] | 2009 |
| RAND RR1408, SAT evaluation | High — peer-reviewed policy research | [PRIMARY] | 2016 |
| Coulthart, 12 SATs evaluation (IJIC) | High — peer-reviewed journal | [PRIMARY] | 2017 |
| Mandel & Tetlock (I&NS) | High — peer-reviewed, leading researchers | [PRIMARY] | 2018 |
| Mandel & Tetlock (Frontiers in Psychology) | High — peer-reviewed | [PRIMARY] | 2018 |
| Dhami et al., ACH (Applied Cognitive Psychology) | High — peer-reviewed empirical study | [PRIMARY] | 2019 |
| Defense Science Board Red Teaming Report | Highest — DoD advisory body | [PRIMARY] | 2003 |
| CETaS/Turing, LLMs and Intelligence | High — national security think tank | [PRIMARY] | 2023 |
| Logan, LLMs and Pathologies | Moderate — academic analysis | [PRIMARY] | 2024 |
| Georgetown SCS; Pherson Associates | Moderate — practitioner institutions | [PRIMARY/SECONDARY] | Various |
| O'Reilly; CIA DDI MacEachin | Moderate — practitioner/institutional | [SECONDARY] | 1993-1996 |
| Roberts, sroberts.io | Moderate — practitioner blog | [SECONDARY] | Various |
