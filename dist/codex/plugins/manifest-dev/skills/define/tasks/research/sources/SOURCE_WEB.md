# Web Source Guidance

Web-specific quality gates, search techniques, and failure modes for research tasks that involve public web sources, published articles, documentation, and external information.

Composes with `RESEARCH.md` (base for all research tasks). This file provides web-specific instantiations of the general research framework.

## Compressed Awareness

**Web-researcher sub-agent delegation** — For multi-facet web research, delegate orthogonal sub-topics to parallel web-researcher sub-agents (each gets assigned AND excluded scope). Main agent decomposes, coordinates, and synthesizes — never searches directly. Search coverage improves dramatically: simple keyword searches miss 60-72% of relevant content; multiple semantically distinct query formulations are essential.

## Quality Gates

### Web Source Rigor

Instantiates RESEARCH.md's abstract source rigor gates for web sources:

- **Web source authority hierarchy** — Primary sources (official docs, specs, peer-reviewed research) over secondary (established publications, reputable analysis) over tertiary (blogs, forums, outdated material). Claims on tertiary alone are unsubstantiated unless no higher-authority source exists (flagged as gap)
- **Lateral reading** — Sources underpinning key claims evaluated by external reputation (what do independent authorities say about this source?), not just by content. Vertical evaluation (assessing a source by its own self-presentation) is insufficient — 71% improvement in unreliable source detection when using lateral reading (RCT, n=499)
- **Web search coverage** — Simple keyword searches miss 60-72% of relevant content. Multiple semantically distinct query formulations used per research facet, not single-query passes
- **Citation fabrication rates** — Citation fabrication rates of 6-29% even in frontier models, inversely correlated with topic familiarity — niche topics demand more aggressive checking. Fabrication rates 28-29% for niche vs 6% for well-known topics

### Selectable Gates

#### Search Depth

| Aspect | Threshold |
|--------|-----------|
| Phase-matched strategy | Broader queries during exploration (maximize recall), narrower during focused investigation (maximize precision) |

## Risks

- **Search result bias** — SEO manipulation and algorithmic ranking treated as a proxy for source authority; probe: are we relying on search rank position to determine quality?
- **AI-content pollution** — Lateral reading or cross-referencing undermined when corroborating sources are themselves AI-generated; probe: are corroborating sources genuinely independent human-authored content?
- **Authority inflation (web)** — Blog cited like peer review, vendor marketing cited like independent analysis, social media engagement conflated with credibility; probe: is each source's authority level honestly assessed against the web hierarchy?
- **Circular citation (web)** — Multiple web sources appearing independent but tracing to a single press release, blog post, or upstream report, creating false corroboration; probe: do corroborating sources have genuinely independent upstream origins?

## Trade-offs

- Search depth vs execution cost — deeper search (more reformulations, vocabulary expansion) improves recall but costs more tokens and time; match depth to claim importance
- Recency vs permanence — web sources are volatile (pages move, content updates); prefer archived/stable sources for claims that need to hold

## Defaults

*Domain best practices for web research.*

- **Web-researcher sub-agent delegation** — Parallel web-researcher sub-agents for multi-facet web research, each with assigned AND excluded scope
- **Multi-query coverage** — Multiple semantically distinct query formulations per research facet. Single-query passes miss 60-72% of relevant content
- **Iterative reformulation** — Terminology from found sources seeds follow-up searches (pearl growing)
- **Vocabulary expansion** — Synonym variants, alternative phrasings, and domain-specific terminology to overcome vocabulary mismatch barriers
