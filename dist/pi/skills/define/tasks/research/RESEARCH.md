# RESEARCH Task Guidance

Investigations, analyses, comparisons, technology evaluations. Default posture: **deep, adversarial, multi-angle** — high signal, no stones unturned, conclusions that survive scrutiny and attack.

## Data Sources

Research tasks may span multiple data sources. Each source type has its own credibility model, failure modes, and retrieval techniques. Probe for which sources are relevant; load source-specific guidance files when available.

| Source Type | Indicators | Source File | Probe |
|-------------|------------|-------------|-------|
| **Web** | Public information, published sources, external research | `sources/SOURCE_WEB.md` | Does this task require searching the public web, published articles, documentation, or external sources? |

When no source file exists for a relevant source type, the general quality gates below still apply — the LLM probes source-specific failure cases adaptively using the abstract principles.

**Source file note**: Quality gates below reference abstract principles (credibility, cross-referencing, fabrication, etc.). Source files instantiate these for their source type with specific hierarchies, techniques, and rates. Load applicable source files for specifics.

## Quality Gates

### Baselines (always enforced)

**Source Rigor**
- **Source credibility** — Key findings backed by credible, identifiable sources, weighted by authority level and claim stakes. Higher-stakes claims demand higher-authority sources. When relying below the level the claim demands, flag it
- **Source authority assessment** — Source authority assessed per source type — each data source has its own credibility hierarchy. Higher-stakes claims demand higher-authority sources within the relevant source type
- **Cross-referencing** — Key claims corroborated across independent sources, depth proportional to claim importance. Independence means different organizations, methodologies, and data sources — not multiple citations of the same upstream source
- **Evidence traceability** — Key claims traceable to specific sources; the chain from raw evidence to conclusion is walkable
- **Source coverage** — Coverage verified across the source's retrieval mechanisms — single-pass queries risk missing relevant content
- **External reputation assessment** — Source reputation assessed externally — what do independent parties say about this source? — not just by the source's own self-presentation
- **Citation verification** — Cited sources verified to exist and actually support the claims attributed to them. AI agents fabricate citations; verification intensity should scale with topic obscurity and claim stakes
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

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Emergent depth | criteria-checker | Dedicated sections, follow-up searches, or scope evolution documented for unexpected findings |
| Question completeness | criteria-checker | All dimensions of the research question identified and addressed |
| Quantification | criteria-checker | Claims that could be quantified use numbers, not vague qualitative language — "faster" becomes "~2x faster" when evidence supports it |
| Recency | criteria-checker | Sources published within the topic's relevance window — fast-moving topics demand recent, stable topics tolerate older |

#### Output Quality

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Synthesis | general-purpose | Findings connected into meaning — "so what?" answered, not just facts listed |
| Output structure | general-purpose | Report organized for the reader's decision flow — navigable, scannable, key insights surfaced not buried |
| Prioritization | general-purpose | When multiple options or findings exist, ranked with explicit criteria — not just listed |

#### Utility

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Actionability | general-purpose | Output enables a decision or next step without further research |
| Follow-up anticipation | general-purpose | Report preempts the reader's likely next questions rather than leaving obvious gaps |

#### Evidence Assessment

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| GRADE-adapted confidence | general-purpose | Evidence quality assessed beyond source type — a PRIMARY source can be low-confidence if inconsistent with other evidence, indirect to the question, or imprecise. Dimensions: risk of bias, inconsistency, indirectness, imprecision, publication bias |
| Claim decomposition | criteria-checker | Complex claims broken into independently verifiable atoms. Compound claims hide errors — "X reached $500B in 2023 driven by Y" contains three separate verifiable claims |
| Disagreement classification | general-purpose | Source conflicts classified before resolution: factual conflicts → investigate deeper, favor higher authority; open questions → preserve both positions; methodological differences → present both with framing. Never force false consensus on genuine open questions |

#### Process Discipline

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Protocol deviation tracking | criteria-checker | Departures from original research plan documented with rationale — pre-registration's value comes from making deviations visible, not preventing them |
| Linchpin analysis | general-purpose | Claims whose failure would collapse most conclusions identified and targeted for strongest verification effort |
| Outside view | general-purpose | Reference class identified — "how often do claims of this sort hold?" applied after initial conclusions to counter anchoring and base rate neglect |
| Adversarial convergence | general-purpose | Adversarial findings descended in severity across waves — not merely absent. Final wave attacked from new angles. Conclusions became more accurate, not more hedged (bipolar check) |

## Defaults

*Domain best practices for this task type.*

- **Multi-agent delegation** — For multi-facet research, delegate orthogonal sub-topics to parallel source-type-appropriate sub-agents (each gets assigned AND excluded scope). Main agent decomposes, coordinates, and synthesizes — never researches directly
- **Parallel verification over serial** — Multiple agents independently checking the same claims, not serial chains where each builds on the last
- **Sycophancy-aware framing** — Frame research questions to avoid implying expected findings. Include explicit counter-hypothesis: "research X, including evidence X does NOT hold"
- **Rigor-task fit** — Formal rigor for novel, uncertain, or multi-source synthesis. Simpler heuristics for well-structured, single-source tasks
- **Niche-topic vigilance** — Enhanced verification for less-documented topics where AI fabrication rates are higher
- **Genuine quality over performative rigor** — Quality measures must reflect genuine quality, not checklist compliance. Process without substance is worse than no process
- **Preserve genuine disagreement** — Open questions stay open. Don't force false consensus when genuine uncertainty exists. Disagreement is a valid finding
- **Calibrated confidence** — Don't water down well-supported conclusions through excessive hedging. Adversarial review should make research more accurate, not less decisive
