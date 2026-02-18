# RESEARCH Task Guidance

Investigations, analyses, comparisons, technology evaluations. Default posture: **deep, adversarial, multi-angle** — high signal, no stones unturned, conclusions that survive scrutiny and attack.

## Compressed Awareness

**Structural interventions > awareness instructions** — Process rules that force behavior (required sections, structured output, separation of concerns) are more reliable than instructions to "watch for bias." AI agents comply with awareness instructions performatively while still exhibiting bias structurally (convergent finding across systematic reviews, intelligence analysis, epistemology, and AI failure mode research).

**Error propagation is exponential** — P(no error after n steps) = (1-p)^n. At 5% per-step error, a 4-step pipeline yields ~81.5% cumulative accuracy. Each added verification step must reduce per-step error by more than it adds to pipeline length. Parallel verification (multiple independent checks) beats serial processing (each building on the last).

**LLMs cannot find their own errors but CAN correct them when pointed out** — This error-detection asymmetry is the empirical justification for multi-agent adversarial verification. Independent agents checking each other's work is structurally correct.

**Multi-agent research yields 90.2% improvement over single-agent** — For multi-facet research, delegate orthogonal sub-topics to parallel web-researcher sub-agents (each gets assigned AND excluded scope). Main agent decomposes, coordinates, and synthesizes — never researches directly. Probe for process guidance: agent delegation strategy, convergence criteria, adversarial verification depth.

**Ecological rationality boundary** — Simple heuristics outperform formal frameworks in well-structured environments (Gigerenzer). Formal rigor adds value in novel, uncertain, multi-source synthesis — which is the target use case for deep research. Match rigor to task complexity.

## Quality Gates

### Baselines (always enforced)

**Source Rigor**
- **Source credibility** — Key findings backed by credible, identifiable sources, weighted by authority level and claim stakes. Higher-stakes claims demand higher-authority sources. When relying below the level the claim demands, flag it
- **Source authority hierarchy** — Primary sources (official docs, specs, peer-reviewed research) over secondary (established publications, reputable analysis) over tertiary (blogs, forums, outdated material). Claims on tertiary alone are unsubstantiated unless no higher-authority source exists (flagged as gap)
- **Cross-referencing** — Key claims corroborated across independent sources, depth proportional to claim importance. Independence means different organizations, methodologies, and data sources — not multiple citations of the same upstream source
- **Evidence traceability** — Key claims traceable to specific sources; the chain from raw evidence to conclusion is walkable
- **Search coverage** — Simple keyword searches miss 60-72% of relevant content. Multiple semantically distinct query formulations used per research facet, not single-query passes
- **Lateral reading** — Sources underpinning key claims evaluated by external reputation (what do independent authorities say about this source?), not just by content. Vertical evaluation (assessing a source by its own self-presentation) is insufficient — 71% improvement in unreliable source detection when using lateral reading (RCT, n=499)
- **Citation verification** — Cited sources verified to exist and actually support the claims attributed to them. Citation fabrication rates of 6-29% even in frontier models, inversely correlated with topic familiarity — niche topics demand more aggressive checking
- **Anti-cherry-picking** — Sources meeting inclusion criteria (relevant topic, adequate authority) never excluded solely because findings contradict the emerging narrative. Contradictory sources engaged — either by incorporating contrary evidence or documenting why the source's methodology is flawed

**Intellectual Rigor**
- **Counterfactual stress-testing** — Key claims tested against disconfirming evidence — "what would make this wrong?" actively investigated. Conclusions that survive: stated with confidence. Fragile conclusions: flagged with conditions under which they break
- **Opposing evidence & steelmanning** — Strongest possible counter-argument constructed and engaged directly for each key conclusion. Absence of opposing evidence is itself a finding to explain
- **Multi-angle investigation** — Research question examined from multiple independent frames (stakeholder perspectives, time horizons, assumption sets, disciplines) — not just multiple sources within the same frame
- **Investigation depth** — Key claims investigated beyond the first satisfying source; exploration paths documented; depth means multiple independent lines of evidence, not just source count
- **Argument chain integrity** — Every conclusion walkable from raw evidence through intermediate claims to final recommendation. Each inferential step identified (deduction, induction, analogy, authority). Gaps or unsupported leaps flagged
- **Warrant identification** — For key conclusions, the reasoning connecting evidence to claim (the warrant) is stated explicitly, not assumed. Hidden warrants are where arguments fail silently — Toulmin-based questioning outperforms chain-of-thought for LLM reasoning
- **Bipolar calibration** — Confidence calibrated in both directions. Both overconfidence AND underconfidence degrade research quality. When evidence strongly supports a conclusion, stated clearly rather than hedged reflexively. Calibration training that only targets overconfidence risks creating underconfidence (empirically confirmed)

**Consistency & Transparency**
- **Internal consistency** — Findings, analysis, and conclusions don't contradict each other; report audited for contradictions between sections, between evidence and conclusions, and between different claims
- **Assumptions transparency** — Choices and assumptions made during research are explicit and revisable
- **Gap honesty** — Knowledge gaps explicitly stated, never papered over
- **Scope boundaries** — What's in and out of scope stated explicitly
- **Definitional clarity** — Key terms defined and used consistently; comparisons use the same definitions across all options

**Comparisons** (when comparing options)
- **Evaluation symmetry** — Each option evaluated with comparable depth and rigor — no option gets cursory treatment while another gets deep analysis

### Selectable Gates

#### Rigor

| Aspect | Threshold |
|--------|-----------|
| Emergent depth | Dedicated sections, follow-up searches, or scope evolution documented for unexpected findings |
| Question completeness | All dimensions of the research question identified and addressed |
| Quantification | Claims that could be quantified use numbers, not vague qualitative language — "faster" becomes "~2x faster" when evidence supports it |
| Recency | Sources published within the topic's relevance window — fast-moving topics demand recent, stable topics tolerate older |

#### Output Quality

| Aspect | Threshold |
|--------|-----------|
| Synthesis | Findings connected into meaning — "so what?" answered, not just facts listed |
| Output structure | Report organized for the reader's decision flow — navigable, scannable, key insights surfaced not buried |
| Prioritization | When multiple options or findings exist, ranked with explicit criteria — not just listed |

#### Utility

| Aspect | Threshold |
|--------|-----------|
| Actionability | Output enables a decision or next step without further research |
| Follow-up anticipation | Report preempts the reader's likely next questions rather than leaving obvious gaps |

#### Search Depth

| Aspect | Threshold |
|--------|-----------|
| Iterative reformulation | Queries reformulated based on initial results — terminology from found sources seeds follow-up searches (pearl growing finds ~51% of references in systematic reviews) |
| Vocabulary expansion | Synonym variants, alternative phrasings, and domain-specific terminology used — vocabulary mismatch between queries and content is a fundamental recall barrier |
| Phase-matched strategy | Broader queries during exploration (maximize recall), narrower during focused investigation (maximize precision) |

#### Evidence Assessment

| Aspect | Threshold |
|--------|-----------|
| GRADE-adapted confidence | Evidence quality assessed beyond source type — a PRIMARY source can be low-confidence if inconsistent with other evidence, indirect to the question, or imprecise. Dimensions: risk of bias, inconsistency, indirectness, imprecision, publication bias |
| Claim decomposition | Complex claims broken into independently verifiable atoms. Compound claims hide errors — "X reached $500B in 2023 driven by Y" contains three separate verifiable claims |
| Disagreement classification | Source conflicts classified before resolution: factual conflicts → investigate deeper, favor higher authority; open questions → preserve both positions; methodological differences → present both with framing. Never force false consensus on genuine open questions |

#### Process Discipline

| Aspect | Threshold |
|--------|-----------|
| Protocol deviation tracking | Departures from original research plan documented with rationale — pre-registration's value comes from making deviations visible, not preventing them |
| Linchpin analysis | Claims whose failure would collapse most conclusions identified and targeted for strongest verification effort |
| Outside view | Reference class identified — "how often do claims of this sort hold?" applied after initial conclusions to counter anchoring and base rate neglect |

#### AI Robustness

| Aspect | Threshold |
|--------|-----------|
| Sycophancy-aware framing | Research framing avoids implying expected findings — "research the relationship between X and Y, including evidence X does NOT improve Y" rather than "research how X improves Y." AI agents align findings with perceived expectations |
| Niche-topic vigilance | Research on niche or obscure topics flagged for enhanced verification — citation fabrication rates 28-29% for niche vs 6% for well-known topics |
| Parallel verification preference | Multiple agents independently checking the same claims preferred over serial chains where each builds on the last — addresses error propagation and error-detection asymmetry |

## Risks

- **Source bias** — all sources from same perspective; probe: what viewpoints might disagree?
- **Confirmation bias** — only finding evidence supporting initial hypothesis, including biased search terms; probe: what searches would you run if you believed the *opposite* conclusion?
- **Authority inflation** — source treated as more authoritative than it is (blog cited like peer review, vendor marketing cited like independent analysis); probe: is each source's authority level honestly assessed?
- **Recency gap** — topic evolved since sources published; probe: how fast-moving is this topic?
- **Premature convergence** — stopped at first satisfying answer without testing deeper/adjacent threads; probe: what would another round of curiosity-driven exploration reveal?
- **Single-frame blindness** — entire investigation through one lens (e.g., only technical, only economic); probe: what frames haven't been applied?
- **Shallow depth as breadth** — many sources cited but no claim investigated deeply; probe: for the most important claim, can you trace the full evidence chain?
- **Survivorship bias** — only successful cases visible; failed adoptions and quiet abandonments are undocumented; probe: what would the failures look like?
- **Citation fabrication** — AI generates plausible-sounding but non-existent sources, especially for niche topics (6-29% fabrication rates); probe: have cited sources been independently verified to exist and support the attributed claims?
- **Sycophancy alignment** — research framing implies expected findings, causing AI agents to confirm rather than investigate; probe: could the research question be read as suggesting its own answer?
- **Search result bias** — SEO manipulation and algorithmic ranking treated as a proxy for source authority; probe: are we relying on search rank position to determine quality?
- **Authority mimicry** — confident, authoritative style without factual grounding; probe: does the source's tone match its evidence quality, or is it performing authority?
- **Anti-Bayesian drift** — AI agents become MORE confident rather than less when encountering counter-evidence; probe: did confidence appropriately decrease where counter-evidence surfaced?
- **Circular citation** — multiple sources appearing independent but tracing to a single origin, creating false corroboration; probe: do corroborating sources have genuinely independent upstream origins?
- **AI-content pollution** — lateral reading or cross-referencing undermined when corroborating sources are themselves AI-generated; probe: are corroborating sources genuinely independent human-authored content?
- **Error propagation** — errors compound exponentially across multi-step synthesis pipelines; probe: how many inferential steps between raw evidence and final conclusion? Are steps parallel or serial?
- **False precision** — uncertainty ranges or caveats stripped during synthesis, making tentative findings sound definitive; probe: where did we lose nuance between raw findings and conclusions?

## Scenario Prompts

- **Conclusion unsupported** — findings don't support recommendation; probe: does evidence actually lead to this conclusion?
- **Scope creep dilutes** — research too broad, depth sacrificed; probe: what's the core question?
- **Wrong comparison criteria** — alternatives compared on wrong dimensions; probe: what matters for decision?
- **Missing alternative** — obvious option not considered; probe: what else could solve this?
- **Status quo unexamined** — "do nothing" not analyzed as baseline; probe: what happens if we don't act?
- **Hidden framing bias** — question structure predetermines answer; probe: could this question be asked differently?
- **Audience mismatch** — too technical or too shallow for reader; probe: who consumes this? expertise level?
- **Anomaly ignored** — something surprising surfaced but was glossed over; probe: what didn't fit the pattern?
- **Shelf life unknown** — findings delivered with no indication of temporal validity; probe: when should we re-evaluate?
- **Correlation treated as causation** — observed correlation presented as causal; probe: what alternative explanations exist?
- **Recommendation risk unexamined** — recommended option's failure modes and reversal cost not analyzed; probe: what if this recommendation fails? How hard to reverse?
- **Niche-topic fabrication** — AI-generated claims for obscure topics far less reliable than for well-known ones (28-29% vs 6% fabrication); probe: is this topic niche enough that enhanced verification is warranted?
- **Performative rigor** — checklist compliance without substance; probe: do quality measures reflect genuine quality, or just the appearance of process?
- **Forced false consensus** — open questions resolved as if factual, premature convergence into a single position when genuine uncertainty exists; probe: are we forcing agreement where disagreement is the honest finding?
- **Over-hedging** — adversarial rounds push toward excessive qualification and underconfidence, watering down well-supported conclusions; probe: has adversarial review made the research more accurate, or just less decisive?
- **Context missing** — findings are generic, not grounded in specific constraints; probe: does this apply to our situation?
- **Single-agent tunnel vision** — research done by one agent without parallel sub-agents misses content due to query path dependence and recall gaps (60-72%); probe: does this task have multiple facets that would benefit from parallel web-researcher sub-agents?

## Trade-offs

- Depth vs breadth — default: depth on high-impact claims, breadth only for landscape mapping
- Recency vs authority — fast-moving topics favor recency; stable topics favor authority
- Completeness vs focus — every thread followed must earn its place
- Quantitative evidence vs qualitative insight — prefer quantitative when available, don't discard what resists measurement
- Expert consensus vs emerging contrarian evidence — note both; don't dismiss minority evidence
- Answering the asked question vs reframing to the right question — if the question is flawed, say so
- Exhaustiveness vs signal density — depth doesn't mean noise; optimize for the reader's time
- Structural interventions vs awareness instructions — process rules that force behavior over instructions to "be aware of bias"
- Parallel verification vs serial processing — parallel catches more errors but costs more; serial compounds errors but is cheaper
- Evidence sufficiency scaling — routine claims need 1-2 authoritative sources; contested/high-stakes claims need 3+ independent lines from different methodological traditions
