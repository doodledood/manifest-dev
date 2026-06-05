# Information Science & Library Science Transfer to AI-Mediated Web Research

**Last Updated**: 2026-02-18
**Shelf Life**: Foundational information science models (Bates, Kuhlthau, Ellis) are stable institutions — reliable for 5+ years. Information retrieval theory (BM25, relevance ranking) is stable. AI-specific search findings (LLM-augmented IR, neural retrieval) are volatile: 6-12 month shelf life. Source evaluation frameworks (lateral reading, SIFT) are stable but may need revision as AI-generated web content proliferates.

---

## Key Findings at a Glance

- **Simple keyword searches retrieve only 28-40% of relevant indexed content** [PRIMARY: Walters; PRIMARY: Salvador-Olivan et al. 2019]. AI agents relying on single-query strategies systematically miss a majority of relevant sources — this is the single most consequential finding for CLAUDE.md process improvement.
- **Expert search success is predicted by metacognitive strategies, not query quality** [PRIMARY: Tabatabai & Shore 2005]. Planning, monitoring, and evaluating search progress matter more than crafting better individual queries — implying AI agent design should prioritize search orchestration over query optimization.
- **Lateral reading is the most empirically validated source evaluation technique**: a randomized controlled trial showed 71% improvement in unreliable information detection [PRIMARY: Wineburg et al. 2022]. It maps directly to AI agent capabilities (cross-referencing sources via additional searches).
- **Berry picking (Bates 1989) and iterative search models are foundational**: information seeking is not a single-query-to-result process but an evolving traversal where queries change as understanding develops. Single queries satisfy needs only ~50% of the time [SECONDARY: Stanford IR Book].
- **92.7% of systematic review search strategies contain errors**; 78.1% of those errors affect recall [PRIMARY: Salvador-Olivan et al. 2019]. The most common: missing synonyms (54%), missing morphological variations (49.6%).
- **Counter-evidence**: Natural language queries perform comparably to Boolean for simple known-item searches [PRIMARY: Lowe et al. 2018]. Not every research task requires sophisticated search strategy.

---

## Definitions

| Term | Definition |
|------|-----------|
| **Precision** | Fraction of retrieved documents that are relevant. High precision = few irrelevant results. |
| **Recall** | Fraction of all relevant documents that are retrieved. High recall = few relevant documents missed. |
| **Berry picking** | Bates (1989) model where information seeking involves evolving queries across multiple sources, each yielding partial results ("berries"), rather than a single comprehensive retrieval. |
| **Lateral reading** | Evaluating a source by leaving it and searching for external information about the source's credibility, rather than evaluating the source's content directly (Wineburg & McGrew 2019). |
| **Pearl growing** | Using characteristics of a known relevant source (citation, terminology, authors) to find similar sources. |
| **Block building** | Structuring search strategies around key concepts (blocks) combined with Boolean operators, then searching each block independently. |
| **BM25** | Best Matching 25. Probabilistic relevance ranking algorithm widely used in modern search engines (Robertson & Zaragoza 2009). Incorporates term frequency saturation and document length normalization. |
| **SIFT** | Stop, Investigate the source, Find better coverage, Trace claims to original context. Source evaluation method incorporating lateral reading (Caulfield 2019). |
| **ISP** | Information Search Process (Kuhlthau 1991). Six-stage model of information seeking behavior with affective, cognitive, and physical dimensions. |

---

## The Recall Gap: Why Single Queries Fail

### The Core Problem

The most actionable finding from information science is quantitative: **simple keyword searches miss most relevant content**.

| System | Coverage (what's indexed) | Recall (what's retrieved) | Gap |
|--------|--------------------------|--------------------------|-----|
| Google Scholar | 93% of relevant articles | ~40% via keyword search | 53% missed |
| SSCI | 73% of relevant articles | ~28% via keyword search | 45% missed |
| Google Scholar (for SRs) | 97.2% | First 1,000 results insufficient | Depth ceiling |

[PRIMARY: Walters; PRIMARY: Bramer et al. 2016]

The coverage numbers are reassuring — search engines index most relevant content. But indexing is not retrieval. The gap between what exists and what a single query surfaces is where research quality is lost.

### Why Queries Fail: The Vocabulary Mismatch Problem

Furnas et al. (1987) demonstrated a fundamental barrier: users and documents use different terms for the same concepts [PRIMARY]. This is not a solvable engineering problem — it's a property of natural language. Query expansion (adding synonyms, related terms, morphological variants) yields ~8% recall improvement and ~12% MAP improvement [PRIMARY: Azad & Deepak 2019, reviewing 573 papers], but results are context-dependent and can sometimes reduce precision.

For AI agents specifically: queries are generated from the agent's internal representations, which may not match web content vocabulary. An agent searching for "LLM hallucination mitigation" will miss papers using "factual grounding," "faithful generation," or "confabulation reduction."

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to agent prompt discipline: "For each research facet, generate at minimum 3 semantically distinct query formulations before beginning search. Include synonym variants, alternative phrasings, and domain-specific terminology. Single-query research is insufficient — simple searches miss 60-72% of relevant content."

**Feasibility**: High. AI agents excel at generating query variants — this leverages a core LLM strength. No new tooling required.

**What would make this wrong?** If modern semantic search engines have evolved sufficiently to compensate for vocabulary mismatch automatically, explicit query expansion would be redundant. Evidence suggests semantic matching helps but does not fully solve the problem — 92.7% of search strategies still contain recall-affecting errors even when constructed by human experts [PRIMARY: Salvador-Olivan et al. 2019].

---

## Iterative Search Models: How Expert Researchers Actually Search

### Berry Picking (Bates 1989)

The foundational insight: information seeking is not a single-query-to-result process but an iterative traversal across multiple sources where queries evolve as the searcher learns [PRIMARY: Bates 1989]. Bates identified six strategies:

| Strategy | Description | AI Agent Implementation |
|----------|-------------|------------------------|
| Footnote chasing (backward) | Follow citations from retrieved documents | Extract and search for cited sources |
| Citation searching (forward) | Find what cites a key source | Search "cited by" for key findings |
| Journal run | Browse within specific high-authority domains | Search within known authoritative sites |
| Area scanning | Browse topic-adjacent content | Query for related/adjacent topics |
| Subject searches | Use keyword variants and synonyms | Generate multiple query formulations |
| Author searching | Find other works by identified experts | Search for authors of key sources |

### Kuhlthau's Information Search Process (1991)

Six stages: initiation → selection → exploration → formulation → collection → presentation [PRIMARY: Kuhlthau 1991]. Validated across 20+ years with 385 participants at 21 sites.

The critical finding: **uncertainty increases during exploration before decreasing at formulation** — the "dip" where many searches are abandoned prematurely. The pivot point is "focus formulation," where the searcher develops a coherent perspective on the topic.

**AI relevance**: AI agents may terminate search prematurely because they lack the metacognitive awareness that initial confusion is expected and productive. The dip maps to the experience of finding contradictory or confusing early results — exactly when continued searching is most valuable.

### Expert vs. Novice: What Actually Predicts Success

Tabatabai & Shore (2005) studied 10 novices, 9 intermediates, and 10 experts [PRIMARY]:

- **Success was NOT predicted by**: query quality, types of queries issued, or percentage of relevant documents retrieved
- **Success WAS predicted by**: metacognitive strategies (planning, monitoring, evaluating search progress), patience, and background knowledge about information seeking
- The expert-novice gap was **largest between novices and intermediates**, not between intermediates and experts
- Novices relied on trial-and-error; experts planned ahead
- Marchionini (1995): system-specific experience is **less important** than domain expertise and general information-seeking expertise [PRIMARY]

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Orchestrating Web Research: "Agent prompts should include explicit search planning instructions: (1) formulate initial queries, (2) assess initial results for coverage gaps, (3) reformulate queries based on what's found and what's missing, (4) continue until diminishing returns. Agents should not rely on a single search pass."

**Feasibility**: Moderate. Iterative search requires agents to assess their own search progress — a metacognitive capability that may be limited in current LLMs. However, structuring prompts to require explicit "what am I still missing?" reflection after initial results is feasible and maps to the expert metacognitive strategies that predict success.

**What would make this wrong?** If AI agents' fundamentally different information processing means human expert/novice patterns don't transfer. However, the finding that success comes from process orchestration (a transferable concept) rather than cognitive ability (a non-transferable trait) suggests the transfer is valid. The risk is more that agents comply performatively — reporting "gaps assessed" without genuine metacognitive evaluation.

---

## Precision vs. Recall: Managing the Tradeoff Deliberately

### The Unavoidable Tradeoff

Precision and recall are inversely related under most retrieval conditions [PRIMARY: Buckland & Gey 1994]. For AI-mediated research:

- **High precision, low recall**: Agent finds highly relevant sources but misses important evidence. Risk: conclusions based on incomplete evidence.
- **High recall, low precision**: Agent finds most relevant sources but also retrieves much noise. Risk: token budget wasted on irrelevant content; noise confuses LLM reasoning.
- **Distracting passages are worse than random noise**: Semantically related but non-answer content actively degrades LLM performance more than completely irrelevant passages [PRIMARY: recent IR research].

### Block Building and PICO

The block building approach structures searches around key concepts. Evidence on block count [PRIMARY: Eriksen & Frandsen 2018; PRIMARY: Frandsen et al. 2020]:

- **Fewer blocks (P+I)** = higher recall, lower precision
- **More blocks (P+I+C+O)** = higher precision, lower recall
- Optimal for comprehensive research: Population + Intervention + study design; adding Comparison and Outcome elements lowers recall without proportional precision gain

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Research Quality Standards: "Match search strategy to research phase. During exploration: use broader queries (2-3 concept blocks) to maximize recall. During focused investigation: use narrower queries (3-4 blocks) to maximize precision. Never assume a single search pass has captured all relevant content."

**Feasibility**: High. The block-building principle translates directly to how agents decompose research questions into core concepts and search for each. Searching with fewer, broader blocks and filtering post-retrieval may be more effective than constructing a single precise query.

**What would make this wrong?** If AI agents' ability to process large result sets makes the precision-recall tradeoff less critical — i.e., if agents can efficiently filter 100 results down to 10 relevant ones without degraded reasoning. Current evidence suggests LLMs are distracted by near-miss content, making this unlikely.

---

## Source Evaluation: Lateral Reading

### The Most Effective Evaluation Technique

Wineburg & McGrew (2019) compared 10 historians, 10 professional fact-checkers, and 25 Stanford students evaluating online sources [PRIMARY]:

- **100%** of fact-checkers correctly identified unreliable sources
- **50%** of historians failed — despite being PhD-holding domain experts
- **65%** of Stanford students chose a hate site as more credible than a legitimate source
- The decisive difference: fact-checkers **read laterally** (opened new tabs to check source credibility elsewhere); historians and students **read vertically** (stayed on the page and analyzed its content)

A randomized controlled trial (Wineburg et al. 2022) with 499 students found 6 sessions of lateral reading instruction improved unreliable information detection by **71%** vs **25%** for the control group [PRIMARY].

### CRAAP vs. SIFT

The **CRAAP test** (Currency, Relevance, Authority, Accuracy, Purpose) has dominated academic library instruction since 2004 but relies on vertical reading — evaluating a source by examining the source itself. This approach is "vulnerable to manipulation by sophisticated disinformation campaigns" [PRIMARY: Fielding].

The **SIFT method** (Stop, Investigate the source, Find better coverage, Trace claims to original context) incorporates lateral reading and is considered a significant improvement [SECONDARY: Caulfield 2019].

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Research Quality Standards, Source Rigor section: "For sources that key claims depend on, agents must perform lateral reading — executing additional searches to verify the source's credibility and cross-check specific claims before incorporating them. Vertical evaluation (assessing a source based on its own content) is insufficient."

**Feasibility**: High. Lateral reading maps directly to AI agent capabilities — for each source, execute additional web searches about the source's reputation, check if claims are corroborated elsewhere, verify author credentials. This is what fact-checkers do, and it's what makes them 50+ percentage points more accurate than domain experts who read vertically.

**What would make this wrong?** If the web becomes so saturated with AI-generated content that lateral reading leads to unreliable corroborating sources (AI citing AI). This is an emerging concern without definitive evidence yet, but it suggests lateral reading should verify source independence (are corroborating sources genuinely independent, or derivative?).

---

## Query Reformulation: When and How to Iterate

### Evidence for Iteration

Single queries satisfy information needs only ~50% of the time [SECONDARY: Stanford IR Book]. Key findings on reformulation:

- **ExpandSearch (2025)**: RL-trained reformulation into multiple semantically-enriched variants significantly improves retrieval recall. Paraphrasing (lexical variation) is the primary mechanism — vocabulary mismatch is a greater challenge than semantic breadth [PRIMARY].
- **IterCQR (NAACL 2024)**: Iterative query reformulation using IR signals as reward achieves state-of-the-art, demonstrating progressive improvement through iteration [PRIMARY].
- **Ruthven (2003)**: Counterintuitively, human searchers are **less likely than machine-based systems** to make good query expansion decisions [PRIMARY]. AI agents may actually have an advantage over human searchers in systematic query expansion.
- **Relevance feedback**: Using initial results to inform subsequent queries "mostly works" and tends to outperform global analysis (query-independent expansion) [SECONDARY: Stanford IR Book].

### Pearl Growing

Pearl growing — using characteristics of a known relevant source to find similar sources — accounts for up to **51% of references found** in systematic reviews [PRIMARY: Schlosser et al. 2006]. The technique is particularly valuable for interdisciplinary topics where terminology varies across fields.

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to agent prompt discipline: "After initial search results, agents must: (1) identify the most relevant source found, (2) extract its key terminology, cited authors, and referenced works, (3) use these as seeds for follow-up queries (pearl growing). Agents must also generate at least one reformulated query using different terminology for the same concept."

**Feasibility**: High. Pearl growing and query reformulation leverage core LLM capabilities. The 51% finding means that omitting pearl growing means missing roughly half the sources that the most rigorous search methodologies find.

---

## Taxonomy and Classification Principles

### Faceted Classification for Research Decomposition

Ranganathan's (1933) faceted classification provides principles directly applicable to research decomposition [PRIMARY]:

- Decompose subjects into **mutually exclusive, collectively exhaustive** facets (orthogonal dimensions)
- Use an **analytico-synthetic** approach: analyze complex topics into simple concepts, then synthesize
- Multidimensional faceted hierarchies are more accessible than one-dimensional taxonomies [PRIMARY: Uddin & Janecek 2007]

### Controlled Vocabularies

**25-33%** of records retrieved by keyword searches would be lost without controlled vocabulary subject headings [PRIMARY: Gross & Taylor 2005]. Combining controlled vocabulary with free text yields the most comprehensive results.

### Concrete Implementation for CLAUDE.md

The CLAUDE.md process already implements faceted classification via its orthogonality requirement for agent decomposition. The information science evidence validates this approach and suggests it could be made more explicit: "Decompose research topics along orthogonal facets (by entity, dimension, time horizon, perspective) — this is the analytico-synthetic approach from classification theory, empirically shown to improve both coverage and navigability."

**What would make this wrong?** If the overhead of formal faceted decomposition exceeds the benefit for typical research tasks. The 25-33% retrieval gain from controlled vocabularies suggests the benefit is substantial, but this comes from academic database contexts — the transfer to web search may be weaker.

---

## Known Limitations of Web Search for Research

### Systematic Biases

- **SEO manipulation**: Less relevant content appears more relevant due to intentional optimization. Users (and agents) trust search ranking as a neutral relevance indicator, which it is not [PRIMARY: search engine manipulation research].
- **Filter bubbles**: More nuanced than originally theorized. Multi-university research found ideological differences emerge in **user click behavior**, not in what search engines surface [PRIMARY: Rutgers/Stanford/Northeastern study]. Self-imposed filtering (confirmation bias in query formulation) may matter more than algorithmic filtering.
- **Recency bias**: Search algorithms favor recent content, potentially surfacing newer-but-lower-quality content over older-but-more-authoritative sources.
- **Algorithmic opacity**: Search algorithms are proprietary black boxes, making it impossible to fully characterize their biases [PRIMARY].
- **LLM-generated content feedback loop**: Neural retrievers are biased toward LLM-generated content, creating a potential quality degradation cycle.

### Concrete Implementation for CLAUDE.md

**Proposed change**: Add to Research Risks & Biases table: "Search result bias — web search results are shaped by SEO manipulation, recency bias, and algorithmic ranking. Agents should not treat search ranking as a proxy for source authority. Probe: Are we relying on search rank position to determine source quality?"

**Feasibility**: High. Awareness-level intervention that requires no new tooling.

---

## Prioritized Recommendations

### P1: Implement Immediately

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Multi-query search requirement | Add minimum 3 query variants per facet to agent prompt discipline | Addresses 60-72% recall gap from single queries | Low: worst case is marginal overhead from redundant searches |
| Lateral reading for key sources | Add to Source Rigor: lateral verification for sources underpinning key claims | 71% improvement in unreliable source detection (RCT evidence) | Low: small additional search cost per key source |
| Search rank ≠ authority | Add to Risks & Biases: explicit warning against treating search position as authority signal | Prevents SEO-manipulated content from anchoring conclusions | Low: awareness-level change |

### P2: Implement After P1 Validated

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Iterative search with reformulation | Add search planning → assessment → reformulation cycle to agent prompts | Captures sources missed by initial queries; mirrors expert search behavior | Medium: agent metacognitive assessment may be unreliable |
| Pearl growing protocol | Add citation/terminology chaining after initial results | Up to 51% of relevant sources found via this technique | Low: leverages core LLM capabilities |
| Phase-matched precision/recall | Broader queries for exploration, narrower for focused investigation | Better resource allocation across search phases | Medium: requires agents to correctly identify current phase |

### P3: Implement When P1-P2 Are Stable

| Recommendation | Change to CLAUDE.md | Expected Impact | Risk if Wrong |
|---------------|---------------------|----------------|---------------|
| Explicit faceted decomposition labeling | Label decomposition facets by type (entity, dimension, time, perspective) | Validates existing orthogonality approach with classification theory | Low: formalization of existing practice |
| Click restraint | Agents evaluate search snippets before fetching full pages | Reduces token waste on irrelevant content | Low: minor efficiency gain |

---

## Knowledge Gaps

1. **AI-specific recall rates for web research are unmeasured**: Most recall research comes from academic database contexts (Google Scholar, MEDLINE, SSCI). How these transfer to general web search APIs used by AI agents is assumed but not directly measured. [Gap severity: Significant]
2. **The "14% AI vs 78% human" statistic could not be located**: The closest analogues are GAIA benchmark data (GPT-4 with plugins 15% vs human 92%) and Google Scholar recall figures. The specific figure may come from an unpublished study or a specific task context not captured by available research. [Gap severity: Minor]
3. **Transfer validity**: Most information science research studied human searchers, not AI agents. Behavioral strategies appear transferable but the underlying cognitive mechanisms differ fundamentally. No rigorous studies directly test whether implementing information science techniques in AI agents improves outcomes. [Gap severity: Significant]
4. **Controlled vocabulary debate remains unresolved**: The 60+ year debate between controlled vocabulary and free text searching remains without definitive resolution, though combined approaches outperform either alone. [Gap severity: Minor]
5. **AI-generated content pollution**: The growing prevalence of AI-generated web content may undermine lateral reading if corroborating sources are themselves AI-generated. This is an emerging concern without definitive evidence. [Gap severity: Significant — growing]
6. **LLM-augmented IR shows limited evidence of improvement**: Beierle (2024) found "little experimental evidence" that LLMs improve information retrieval. One study found LLM-generated queries improved precision but **reduced recall** — the opposite of what comprehensive research needs. [Gap severity: Minor]

---

## Source Authority Assessment

| Source | Authority | Notes |
|--------|-----------|-------|
| Bates (1989) Berry picking | Highest [PRIMARY] | Foundational; 3,000+ citations |
| Kuhlthau (1991) ISP | Highest [PRIMARY] | Validated 20+ years, 385 participants |
| Wineburg & McGrew (2019) Lateral reading | High [PRIMARY] | Published in Teachers College Record |
| Wineburg et al. (2022) COR RCT | High [PRIMARY] | Randomized controlled trial, n=499 |
| Tabatabai & Shore (2005) Expert/novice | High [PRIMARY] | Small n (29) but rigorous methodology |
| Salvador-Olivan et al. (2019) Search errors | High [PRIMARY] | 137 systematic reviews analyzed |
| Robertson & Zaragoza (2009) BM25 | High [PRIMARY] | Definitive BM25 reference |
| Furnas et al. (1987) Vocabulary problem | High [PRIMARY] | Foundational finding |
| Azad & Deepak (2019) QE survey | High [PRIMARY] | 573 papers reviewed |
| Gross & Taylor (2005) Controlled vocabulary | High [PRIMARY] | Replicated finding |
| Schlosser et al. (2006) Pearl growing | High [PRIMARY] | 51% finding |
| Eriksen & Frandsen (2018) PICO impact | High [PRIMARY] | Direct block-count evidence |
| Lowe et al. (2018) Boolean vs NL | High [PRIMARY] | Counter-evidence on search complexity |
| Walters — Google Scholar recall | High [PRIMARY] | Key recall figures |
| Bramer et al. (2016) Coverage study | High [PRIMARY] | 97.2% coverage finding |
| Stanford IR Book (Manning et al.) | High [SECONDARY] | Standard reference |
| Beierle (2024) Search still matters | High [PRIMARY] | LLM-augmented IR limitations |
| Caulfield (2019) SIFT | Moderate [SECONDARY] | Practitioner-developed |
| ExpandSearch (2025) | Moderate [PRIMARY] | Recent, single study |
| IterCQR (NAACL 2024) | High [PRIMARY] | Peer-reviewed venue |

No claims rest solely on tertiary sources.

---

## Adversarial Stress-Testing

**Strongest counter-argument encountered**: Simple keyword searches are sufficient for most AI research tasks. Natural language queries perform comparably to Boolean for known-item searches [PRIMARY: Lowe et al. 2018], and modern semantic search compensates for vocabulary mismatch. The elaborate iterative strategies recommended here add overhead without proportionate benefit. **Response**: This is valid for simple fact-checking and known-item retrieval. But for comprehensive research — where the question is "what exists on this topic?" rather than "find this specific thing" — the 60-72% recall gap from single queries is catastrophic. The CLAUDE.md process explicitly targets deep, adversarial research, not quick lookups. The recommendation is discriminate application: sophisticated search for comprehensive research, simple queries for targeted fact-checking.

**Second strongest counter-argument**: Information science research studied human searchers; AI agents process information fundamentally differently. Expert metacognition may not transfer to AI agents because LLMs lack genuine self-awareness about their search progress. **Response**: The transfer claim is about process structure (iterate, reformulate, assess coverage), not about cognitive mechanisms. Agents can be instructed to follow iterative search protocols regardless of whether they possess genuine metacognition. The risk is performative compliance (agent reports "gaps assessed" without genuine assessment) — this is real and acknowledged in Knowledge Gaps, but structural process improvement is still preferable to no process.

**Third counter-argument**: AI-generated web content pollution may render lateral reading unreliable — cross-referencing sources when sources themselves are AI-generated creates circular corroboration. **Response**: This is an emerging and genuinely concerning risk. The mitigation is to add source independence verification: check whether corroborating sources are genuinely independent or derivative. This is noted as a growing knowledge gap.

**Unresolved tension**: The document recommends iterative, multi-query search strategies that consume more tokens and time, while the CLAUDE.md process also values efficiency. Whether the recall improvement justifies the resource cost depends on research stakes — high-stakes comprehensive research clearly benefits, while lower-stakes tasks may not.
