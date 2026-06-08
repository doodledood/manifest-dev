# Fact-Checking Methodology for Web Research: Evidence-Based Techniques That Survive Hostile Scrutiny

*Systematic approaches to catching factual errors in research output, drawn from professional journalism, OSINT, and automated verification systems. Optimized for integration into AI-assisted research workflows.*

---

## Definitions

**Evidence tiers** used throughout:

| Tier | Label | Basis |
|------|-------|-------|
| Primary | **[PRIMARY]** | Peer-reviewed studies, official organizational standards, original datasets, practitioner handbooks |
| Secondary | **[SECONDARY]** | Established publications, systematic reviews of primary sources, journalism from credentialed outlets |
| Tertiary | **[TERTIARY]** | Blogs, forums, social media, undated web pages |

**Key terms:**

- **Fact-checking**: Verifying the accuracy of specific factual claims against authoritative sources. Distinct from *editorial review* (style, tone, framing) and *peer review* (methodological validity).
- **Lateral reading**: Evaluating a source's credibility by reading *about* it (via other sources) rather than reading deeper *within* it.
- **Claim decomposition**: Breaking a complex statement into independently verifiable atomic claims.
- **Circular citation**: Multiple sources appearing independent but tracing back to a single origin, creating false corroboration.
- **Provenance**: The chain of custody from an original fact through every intermediary to the version being evaluated.

---

## 1. The Error Landscape: Why Fact-Checking Matters Quantitatively

The base rate of factual error in published content is far higher than most researchers assume.

**Maier (2005)** surveyed 4,800 news sources who were subjects of stories and found **61% of newspaper stories contained at least one factual error** [PRIMARY]. The top three error types were misquotation (59% of errors), inaccurate headlines (18%), and incorrect numbers (15%). This 40-60% error rate has been **remarkably stable across 70+ years of studies**, from Charnley (1936) through Maier (2005) [PRIMARY]. Of errors found, roughly **48% were "hard" factual errors** (verifiably wrong facts) versus "soft" errors (matters of interpretation or emphasis).

**What this means for research**: If professional journalists under editorial review produce errors in 6 of 10 stories, secondary and tertiary web sources almost certainly have equal or higher rates. Any research workflow without systematic verification operates on a foundation where roughly half the inputs may contain errors.

**Silverman's error taxonomy** classifies three types [PRIMARY]: commission (stating something wrong), omission (leaving out crucial context), and emphasis (accurate facts arranged to mislead). Commission errors are catchable through verification; omission and emphasis errors require triangulation across sources with different perspectives.

**Counter-evidence on error rates**: Maier's methodology relies on source self-reports -- sources may perceive accurate reporting as erroneous when it reflects unfavorably. The 61% figure likely overstates *objective* error rates. However, even conservative readings place hard factual errors at 20-30%, still demanding systematic checking [SECONDARY].

### CLAUDE.md Implementation

The error rate data validates the cross-referencing mandate. A single-source claim in a domain with 40-60% base error rates is essentially a coin flip.

---

## 2. Lateral Reading: The Single Most Effective Evaluation Technique

### The Evidence

**Wineburg and McGrew (2019)** conducted a landmark study comparing how professional fact-checkers, historians, and Stanford students evaluated online sources [PRIMARY]. The results were stark:

| Group | Correct evaluations | Primary strategy |
|-------|-------------------|-----------------|
| Professional fact-checkers | **100%** | Lateral reading -- left the page immediately to check what others said about the source |
| Historians | **50%** | Vertical reading -- examined the page's own credentials, "About" pages, design quality |
| Stanford students | **35%** | Surface evaluation -- visual cues, domain names, page aesthetics |

The critical insight is **click restraint**: fact-checkers spent *less* time on any individual source but made better judgments because they read *about* the source rather than *from* it. The historians' deeper engagement with the source material actually hurt accuracy by anchoring them to the source's self-presentation.

**COR (Civic Online Reasoning) curriculum** tested this approach at scale: students trained in lateral reading (n=271) showed **statistically significant improvement** over controls (n=228) in source evaluation accuracy [PRIMARY, Stanford GSE]. This is not merely expert intuition -- it is a teachable, measurable skill.

### The Technique in Practice

1. **Encounter a claim or source.** Do not read further into it.
2. **Open new tabs.** Search for the source itself: "[source name] credibility," "[source name] bias," "[author name] expertise."
3. **Check what independent authorities say** -- Wikipedia, media bias trackers, professional associations, domain experts writing about (not for) the source.
4. **Evaluate claimed vs. recognized expertise.** A source claiming medical authority should appear in medical databases.
5. **Only then decide whether to engage** with the source's actual content.

### Steelmanning the Opposition

**Against lateral reading**: "This approach privileges establishment consensus. Genuinely novel or contrarian information often comes from sources that mainstream evaluators dismiss."

**Engagement**: This is the strongest counter-argument. Lateral reading creates a conservatism bias -- optimized for *not being fooled* rather than *catching novel truths*. The mitigation: treat it as a filter with known characteristics (high specificity, moderate sensitivity). When lateral reading flags a source as low-credibility but the claim is important, seek the same claim from higher-authority sources rather than accepting it on a lower standard.

### CLAUDE.md Implementation

Lateral reading operationalizes the "Authority hierarchy." When subagents encounter a new source, the first question is "what do other sources say about this source?" -- directly implementing "Source Rigor" requirements and mitigating "Authority inflation" risk.

---

## 3. Claim Decomposition: Breaking Statements Into Verifiable Atoms

### Why Compound Claims Hide Errors

A statement like "Global renewable energy investment reached $500 billion in 2023, driven primarily by Chinese solar manufacturing subsidies" contains at least three independently verifiable claims: (1) the dollar figure, (2) the year, (3) the causal attribution. Error in any one does not invalidate the others, but evaluating the statement as a unit risks accepting all three if one checks out.

### The Decompose-Then-Verify Paradigm

Recent computational fact-checking research has formalized this intuition:

**AFEV (2025)** introduced iterative dynamic extraction -- claims are decomposed into atomic units, and each unit is verified independently. The system dynamically adjusts decomposition granularity based on verification difficulty [PRIMARY].

**DyDecomp (ACL 2025)** uses reinforcement learning to find optimal atomicity for claim decomposition [PRIMARY]. Too coarse, and errors hide inside compound claims. Too fine, and atomic claims lose the context needed for accurate verification (the **decomposition-decontextualization problem**). DyDecomp's key finding: optimal granularity depends on the claim type -- numerical claims benefit from finer decomposition; causal claims require preserving relational context.

**Probabilistic verification framework (2025)** showed a Spearman correlation of **0.88** between decomposed claim-level verification scores and overall document accuracy [PRIMARY]. This validates the approach: verifying atomic claims is a strong proxy for overall accuracy.

### The Decomposition-Decontextualization Tension

The critical practical challenge: decomposing "The vaccine reduced hospitalizations by 90% in adults over 65" makes the "90%" and "adults over 65" meaningless without each other. Over-decomposition strips context; under-decomposition hides errors.

**The KSJ Handbook** addresses this through **line-by-line annotation** [PRIMARY]: mark every factual claim per sentence and verify each against its original source *while preserving sentence context*. The human annotator maintains the relational frame that automated decomposition loses.

### Practical Decomposition Protocol

For each claim in research output:

1. **Identify claim type**: numerical, attributional, temporal, causal, classificatory.
2. **Decompose to verifiable units** while preserving relationships: "X caused Y" becomes "Did X occur?" + "Did Y occur?" + "Is the causal link supported?"
3. **Match each unit to appropriate verification source**: numbers against primary data sources, attributions against original statements, causal claims against studies with appropriate methodology.
4. **Flag where decomposition loses context**: mark any atomic claim that could be misleading if separated from its qualifiers.

### CLAUDE.md Implementation

Claim decomposition parallels the "Orthogonality requirement" for subagent decomposition: units must be independently verifiable but collectively represent the original meaning. The "Gap honesty" standard requires flagging where decomposition may have lost nuance.

---

## 4. Provenance Tracing: Following Claims to Their Origin

### The SIFT Method

**SIFT** (Stop, Investigate the source, Find better coverage, Trace claims to their origin) provides a lightweight framework for provenance checking [SECONDARY]. The final step -- tracing claims upstream -- is where most errors are caught. A claim cited by Source A, attributed to Source B, may not actually appear in Source B, or may appear with critical caveats stripped away.

### The IMVAIN Framework

**IMVAIN** evaluates information quality on six dimensions [SECONDARY]: **I**ndependent (from the event?), **M**ultiple (corroborating sources?), **V**erifiable (checkable against primary data?), **A**uthoritative (relevant expertise?), **I**nformed (direct knowledge?), **N**amed (identified and accountable?). Each dimension maps to different failure modes -- a source can be authoritative but not independent (a company reporting its own metrics), or named but not informed (a politician commenting outside their expertise).

### PolitiFact's 7-Step Process

PolitiFact's methodology requires verification against **original or primary sources** [PRIMARY]: (1) select claim, (2) contact claimant for evidence, (3) trace to original source, (4) consult experts, (5) assess against primary evidence, (6) determine rating with editorial team, (7) publish with full sourcing. Steps 2-3 are the provenance chain -- errors frequently emerge at intermediary hops where context is lost, numbers rounded, or conditional findings become unconditional assertions.

### Provenance Failure Modes

| Failure | Example | Detection |
|---------|---------|-----------|
| **Citation rot** | Source URL returns 404; claim unverifiable | Check URLs, use Wayback Machine |
| **Context stripping** | "90% effective" cited without "in adults 18-65" | Read the original source, not the citation |
| **Telephone game** | Study says "may contribute to"; tertiary source says "causes" | Trace back through each intermediary |
| **Phantom citation** | Claim attributed to a study that doesn't contain it | Verify the specific claim exists in the cited source |
| **Version drift** | Source updated since citation; original finding revised | Check publication dates and revision histories |

### CLAUDE.md Implementation

Provenance tracing implements "Evidence traceability": the chain from raw evidence to conclusion must be walkable. The "Stale data" risk is a provenance failure mode (version drift).

---

## 5. Circular Citation and the Independence Illusion

### Why Volume Does Not Equal Independence

Three sources confirming a claim provide high confidence *only if they are independent*. If all three trace to a single origin, you have one source with three echoes. This is **citogenesis** -- the creation of apparent citations through circular reference.

### Documented Failure Cases

**Maurice Jarre hoax (2009)**: A student inserted a fabricated quote into Wikipedia; newspapers cited it without attribution; Wikipedia editors then cited the newspapers as sources. Circular validation persisted for weeks [SECONDARY, Slate 2019]. **Jar'Edo Wens (2005-2015)**: A fabricated Aboriginal deity survived on Wikipedia for **10 years**, cited by other sources that reinforced the fabrication [SECONDARY]. **Ronnie Hazlehurst**: A fabricated songwriting credit inserted into his Wikipedia biography appeared in his actual obituary in major publications [SECONDARY].

Shared structure: fabrication enters a high-visibility platform, gets cited by apparently independent sources, and those citations validate the original.

### Detection Techniques

1. **Trace every corroborating source to its origin.** If two sources cite the same third source, you have one data point, not three.
2. **Use the Wikipedia Blame tool** (or equivalent version history tools) to check when specific claims were added and by whom.
3. **Check temporal ordering**: if all citations post-date a single source, independence is suspect.
4. **Look for identical phrasing**: independent sources describing the same fact will typically use different words. Identical or near-identical language suggests copying, not independent confirmation.

### Confidence Calibration

| Independent sources | Confidence level | Caveat |
|----|----|----|
| 1 | Low | Single point of failure |
| 2 | Moderate | Could be coincidental agreement or shared origin |
| **3+** | **High** | If genuinely independent (verified by provenance tracing) |

"Genuinely independent" means: different organizations, different methodologies, different data sources, and no shared upstream citation for the specific claim. Two news articles citing the same press release are one source.

### CLAUDE.md Implementation

Circular citation detection operationalizes "Cross-referencing: Key claims corroborated across *independent* sources." The "Shallow depth as breadth" risk materializes exactly when source count substitutes for source independence. Convergence criteria ("Where agents agree, confidence is high") must be qualified: agreement increases confidence only if agents accessed genuinely independent sources.

---

## 6. OSINT Verification Techniques Applied to Research

### Bellingcat's Contribution

The Bellingcat investigative toolkit provides methods originally developed for conflict and human rights investigations that transfer directly to research verification [PRIMARY]:

**Timeline verification**: The most common form of online misinformation is **old content presented as new** [PRIMARY, Bellingcat]. A photograph, statistic, or event from years ago recirculated as current. Detection involves reverse image search, metadata examination, and cross-referencing claimed dates against known event timelines.

**Document metadata analysis**: Digital documents carry creation dates, modification histories, and author information that can confirm or contradict claimed provenance. **Cross-referencing public records**: Organizational claims can be verified against public filings, business registries, and government databases.

### The Investigation-Validation Separation Principle

OSINT methodology enforces strict separation between **investigation** (gathering information) and **validation** (testing against independent evidence) [PRIMARY, GIJN]. This prevents confirmation bias: you test whether findings survive challenge, not whether evidence supports them. This maps directly to the adversarial verification requirement -- hostile scrutiny must be structurally separated from research production.

### CLAUDE.md Implementation

Investigation-validation separation is the foundation for mandatory adversarial verification. The "old content as new" principle maps to the "Data freshness" attack vector and "Recency gap" bias.

---

## 7. Catching Small Factual Errors: The Accuracy Checklist

### Why Small Errors Matter Disproportionately

Small factual errors -- a misspelled name, a wrong date, an incorrect job title -- undermine credibility far beyond their informational significance. If a document gets small, easily-checkable facts wrong, the reader has no basis for trusting its larger, harder-to-check claims. **CJR identified five primary causes of numerical errors** in published work: transposition, unit confusion, false precision, outdated figures, and calculation mistakes [SECONDARY].

**The DOGE $8M/$8B example** illustrates how a single-character numerical error (million vs. billion -- a 1000x difference) can fundamentally alter a claim's meaning and policy implications. Numerical errors are particularly dangerous because they compound: a wrong number used as input to a calculation propagates error through every downstream conclusion.

### The Line-by-Line Annotation Method

From the **KSJ Handbook** [PRIMARY] and **Silverman's verification protocols** [PRIMARY]:

1. Print or display the document. Read each sentence individually.
2. For every factual claim, mark it with its category:
   - **Names**: Correct spelling? Correct first name? (People named "Steven" vs "Stephen" will notice.)
   - **Titles**: Current title? Not a former title? Organization name spelled correctly?
   - **Ages/Dates**: Calculated correctly? Consistent with other dates in the document?
   - **Numbers**: Verified against primary source? Units correct? Order of magnitude correct?
   - **Geography**: City in the right state/country? Distances plausible?
   - **Gender/Pronouns**: Correct for the person referenced?
   - **Attributions**: Did this person actually say this? In this context?
3. Verify each marked claim against its primary source.
4. Apply the **"What else?" review**: After checking what's in the document, ask what's *missing*. Are there obvious facts that should be stated but aren't?

### False Precision Detection

Presenting imprecise information with precise-looking numbers: "The market is worth $4.7 billion" sounds authoritative but may derive from a rough estimate. **Detection**: check whether multiple sources report the same number (common primary source) or different numbers (precision unjustified).

### What We Don't Know About Checklist Effectiveness

**Critical gap**: There is **no controlled study quantifying accuracy checklist effectiveness in journalism or research** [PRIMARY gap, acknowledged across sources]. The recommendation rests on error taxonomy analysis, professional consensus, and aviation/medical analogies -- not direct experimental evidence of error reduction. We recommend an intervention whose mechanism is plausible but whose effect size is unmeasured.

### CLAUDE.md Implementation

The accuracy checklist implements the pre-finalization check "Conclusions are actually supported by the findings," targeting Maier's most common error types. The gap in effectiveness evidence is acknowledged -- we follow this practice because the alternative (no systematic check) has a known 40-60% error rate, making even an unquantified intervention rational.

---

## 8. Misinformation Pattern Recognition

### Cross-Platform Agreement as a Signal

**Harvard Misinformation Review (2023)** analyzed 749 matched claims checked by both Snopes and PolitiFact and found **only 1 conflicting verdict** [PRIMARY]. This remarkable agreement rate (99.87%) suggests that for claims that professional fact-checkers evaluate, the methodology is robust -- disagreements arise in selection of what to check, not in checking outcomes.

### Red Flags for Unreliable Content

Synthesized from PolitiFact [PRIMARY], Bellingcat [PRIMARY], and misinformation research [SECONDARY]:

| Red flag | What it signals | Verification action |
|----------|----------------|-------------------|
| Sensational or emotionally charged language | Engagement optimization over accuracy | Check if neutral-language sources report the same facts |
| Absence of citations or named sources | Claim may be fabricated or unverifiable | Apply SIFT: trace claim to origin |
| "Too good to be true" alignment with existing beliefs | Potential confirmation bait | Search specifically for counter-evidence |
| Viral spread with identical phrasing | Copy-paste propagation, not independent verification | Trace to earliest instance; check for original source |
| Single source presented as established fact | Insufficient corroboration | Apply triangulation protocol from Section 5 |
| Precise numbers without methodology | False precision or fabrication | Locate the underlying dataset |
| Claims that perfectly confirm a narrative | Possible cherry-picking | Search for evidence of the opposite conclusion |

### The Human-AI Credibility Gap

**Liu et al. (2025)** found that **AI-generated fact-checks are perceived as less credible** than human-generated ones, even when content is identical [PRIMARY]. Practical implication: verification outputs must be transparent about methodology and sourcing. "This was verified" is insufficient; the verification chain must be visible.

### CLAUDE.md Implementation

The red flags table complements the "Risks & Biases" table. Cross-platform agreement supports convergence criteria. The AI credibility gap reinforces why AI-assisted research must show its verification chain to be trusted.

---

## 9. Automated Verification Systems: Current Capabilities and Limits

### FActScore (EMNLP 2023)

**FActScore** decomposes generated text into atomic facts and verifies each against a knowledge source [PRIMARY]. Key findings:

- **ChatGPT-generated biographies**: only **58% of atomic facts** were supported by Wikipedia evidence
- Cost: **20x cheaper** than human annotation
- Limitation: verification is against a fixed knowledge base (Wikipedia), not against the open web or primary sources

### SAFE (DeepMind 2024)

**SAFE** (Search-Augmented Factuality Evaluator) extends FActScore with web search [PRIMARY]:

- **Agrees with human annotations 72%** of the time
- When SAFE and humans disagree, **SAFE is correct 76%** of the time (verified by independent raters)
- Uses search-augmented retrieval rather than fixed knowledge base

### What Automated Systems Cannot Do

| Capability | Current status | Gap |
|-----------|---------------|-----|
| Verifying atomic factual claims | Strong (SAFE 72-76% accuracy) | Misses context-dependent claims |
| Detecting circular citations | Not addressed | Requires provenance tracing across sources |
| Evaluating source authority | Weak | Systems check *existence* of supporting text, not *authority* of the source |
| Catching omission errors | Not addressed | Requires knowledge of what *should* be present |
| Assessing causal claims | Weak | Correlation vs. causation requires domain reasoning |
| Verifying numerical precision | Moderate | Can check existence of numbers but not appropriateness of precision |

**Kavtaradze (2024)** found that organizations investing in automation subsequently **increased human agency** -- automation handled routine checks, freeing humans for judgment-intensive verification [PRIMARY]. Optimal model: human-AI collaboration, not replacement.

### CLAUDE.md Implementation

Automated systems implement a subset of fact-checking (claim decomposition and atomic verification) but do not replace lateral reading, provenance tracing, or circular citation detection. The multi-wave adversarial verification process should use automated checking for atomic claims while reserving human judgment for source authority, causal reasoning, and completeness. The 58% factual support rate for ChatGPT output establishes a baseline making verification non-optional for any LLM-assisted workflow.

---

## 10. Integrated Verification Protocol for Research Workflows

Drawing from all preceding sections, a practical verification protocol:

**Phase 1 -- Source Evaluation** (before accepting evidence): (1) Lateral reading, (2) IMVAIN assessment, (3) Classify by evidence tier.

**Phase 2 -- Claim Verification** (after collecting evidence): (4) Decompose claims into atomic verifiable units, (5) Provenance trace key claims to original sources, (6) Circular citation check on corroborated claims, (7) Accuracy checklist for names, titles, dates, numbers, geography, attributions.

**Phase 3 -- Synthesis Validation** (after writing conclusions): (8) Separate investigation from validation (different agent/person validates than produced), (9) Red flag scan against misinformation patterns, (10) Document methodology transparency per IFCN Principles 2 and 4.

### When to Apply Which Depth

| Research context | Required phases | Rationale |
|-----------------|----------------|-----------|
| Quick factual lookup | Phase 1 + Phase 2 (key claims only) | Low stakes; lateral reading catches bad sources; spot-check numbers |
| Comparative analysis | All three phases, full depth | Recommendations depend on accuracy; evaluation symmetry requires equal verification |
| High-stakes recommendation | All three phases + second-pass adversarial verification | Errors have real consequences; redundant checking justified |

---

## Adversarial Stress-Testing

### Strongest counter-argument: "Systematic fact-checking is too costly for the accuracy improvement it delivers"

**The argument**: No controlled study demonstrates that accuracy checklists reduce error rates in practice. The 40-60% error rate from Maier persists despite decades of fact-checking methodology development. The marginal cost of verifying every claim against primary sources exceeds the marginal benefit, especially when most errors are inconsequential. Resources spent on verification would be better spent on broader research coverage.

**Engagement**: (1) The persistent 40-60% rate reflects *absence* of systematic checking in routine journalism, not its failure -- publications with dedicated fact-checkers (The New Yorker, Der Spiegel) have substantially lower error rates, though exact figures lack controlled comparisons. (2) The cost calculus has shifted: FActScore is 20x cheaper than human annotation; SAFE outperforms humans on 76% of disagreements. (3) "Most errors are inconsequential" is itself unsubstantiated; Maier found 48% were hard errors, and the DOGE $8M/$8B example shows single-character errors can have policy-scale consequences.

### Counter-argument: "This methodology is Western-centric"

**The argument**: IFCN, PolitiFact, Snopes, Bellingcat, and the academic studies cited are overwhelmingly from Western institutions. Fact-checking norms, source authority hierarchies, and verification standards may not transfer to non-Western information environments where institutional trust structures differ.

**Engagement**: Legitimate limitation. The core techniques (lateral reading, provenance tracing, claim decomposition) are epistemically universal. But the *application* -- which sources count as authoritative, which databases to cross-reference -- is culturally situated. Research covering non-Western topics should supplement with region-specific source evaluation frameworks. This gap is acknowledged.

### Counter-argument: "The backfire effect means corrections can make things worse"

**The argument**: Correcting misinformation can entrench it through the backfire effect, making fact-checking counterproductive.

**Engagement**: The backfire effect is now **largely disputed** in the literature. Wood and Porter (2019) failed to replicate it across multiple experiments and found that corrections generally work as intended -- reducing belief in false claims. The original findings appear to have been overstated. This counter-argument, while historically prominent, does not survive current evidence. Fact-checking and correction remain net positive.

---

## Limitations and Open Questions

1. **No AI baseline for research error rates.** LLM-generated text has ~58% factual support (FActScore), but no equivalent measurement exists for AI-assisted workflows *with* verification steps.
2. **Checklist effectiveness is unquantified.** The recommendation rests on face validity and professional consensus, not experimental evidence.
3. **Automation gaps are significant.** Current systems verify claim existence but not source authority, completeness, or causal reasoning.
4. **Good-faith assumption.** These techniques target errors, not deliberate fabrication, which requires different methods.
5. **Scale constraints.** Full provenance tracing for every claim is impractical. The protocol must be applied proportionally -- critical claims get full treatment; supporting details get spot-checks.

---

## Shelf Life

| Component | Reliability window | Basis |
|-----------|-------------------|-------|
| IFCN Code of Principles | **3-5 years** | Institutional standard, slow revision cycle |
| Lateral reading evidence (Wineburg/McGrew) | **3-5 years** | Robust experimental design; replication evidence |
| Maier error rate findings | **3-5 years** | 70-year stable trend; unlikely to shift |
| Claim decomposition techniques | **2-3 years** | Active research area; methods improving rapidly |
| Automated verification (FActScore, SAFE) | **12 months** | Fast-moving field; capabilities and benchmarks will shift substantially |
| Misinformation detection patterns | **2-3 years** | Red flags are stable; specific examples and platform dynamics evolve |

---

No claims in this document rest solely on tertiary sources.

## Source Authority Assessment

| Source | Authority | Tier | Date |
|---|---|---|---|
| Maier, *Journalism & Mass Communication Quarterly* | High — peer-reviewed, 70-year replication chain | [PRIMARY] | 2005 |
| Wineburg & McGrew, *Teachers College Record* | Highest — peer-reviewed, landmark study | [PRIMARY] | 2019 |
| Stanford GSE COR curriculum evaluation | High — institutional RCT | [PRIMARY] | Various |
| IFCN Code of Principles (Poynter) | Highest — governing professional standard | [PRIMARY] | Various |
| AFEV iterative dynamic extraction | High — peer-reviewed | [PRIMARY] | 2025 |
| DyDecomp (*ACL 2025*) | Highest — top-tier venue | [PRIMARY] | 2025 |
| KSJ Science Editors' Handbook | High — authoritative practitioner handbook | [PRIMARY] | Various |
| PolitiFact methodology documentation | High — major fact-checking organization | [PRIMARY] | Various |
| Bellingcat verification toolkit | High — leading OSINT organization | [PRIMARY] | Various |
| GIJN verification methodology | High — professional journalism network | [PRIMARY] | Various |
| FActScore (*EMNLP 2023*) | Highest — top-tier venue | [PRIMARY] | 2023 |
| SAFE (DeepMind, *NeurIPS 2024*) | Highest — top-tier venue, major lab | [PRIMARY] | 2024 |
| Liu et al., AI fact-check credibility | High — peer-reviewed | [PRIMARY] | 2025 |
| Kavtaradze, automation study | High — peer-reviewed | [PRIMARY] | 2024 |
| Harvard Misinformation Review | High — peer-reviewed | [PRIMARY] | 2023 |
| Wood & Porter, backfire replication failure | High — peer-reviewed replication | [PRIMARY] | 2019 |
| Silverman error taxonomy | Moderate — practitioner handbook | [PRIMARY] | Various |
| SIFT method (Caulfield) | Moderate — practitioner-developed | [SECONDARY] | Various |
| IMVAIN framework | Moderate — practitioner-developed | [SECONDARY] | Various |
| CJR numerical error analysis | Moderate — established journalism publication | [SECONDARY] | Various |
| Slate circular citation analysis | Moderate — established publication | [SECONDARY] | 2019 |

*Sources: Maier, "Setting the Record Straight" (Journalism & Mass Communication Quarterly, 2005); Wineburg & McGrew, "Lateral Reading and the Nature of Expertise" (Teachers College Record, 2019); Stanford GSE COR curriculum evaluation; IFCN Code of Principles (ifcncodeofprinciples.poynter.org); RAND Truth Decay report; AFEV iterative dynamic extraction (2025); DyDecomp (ACL 2025); KSJ Science Editors' Handbook; PolitiFact methodology documentation; SIFT method (Caulfield); IMVAIN framework; Bellingcat verification toolkit; GIJN verification methodology; Slate circular citation analysis (2019); Harvard Misinformation Review cross-platform study (2023); Liu et al. AI fact-check credibility study (2025); FActScore (EMNLP 2023); SAFE (DeepMind 2024); Kavtaradze automation study (2024); Silverman error taxonomy; CJR numerical error analysis; Wood & Porter backfire effect replication failure (2019). Research conducted February 2026.*
