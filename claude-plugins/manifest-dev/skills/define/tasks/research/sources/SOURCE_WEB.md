# Web Source Guidance

Web-specific quality gates, search techniques, and failure modes for research tasks that involve public web sources, published articles, documentation, and external information.

Composes with `RESEARCH.md` (base for all research tasks). This file provides web-specific instantiations of the general research framework.

## Quality Gates

### Web Source Rigor

Instantiates RESEARCH.md's abstract source rigor gates for web sources:

- **Web source authority hierarchy** — Primary sources (official docs, specs, peer-reviewed research) over secondary (established publications, reputable analysis) over tertiary (blogs, forums, outdated material). Claims on tertiary alone are unsubstantiated unless no higher-authority source exists (flagged as gap)
- **Lateral reading** — Sources underpinning key claims evaluated by external reputation (what do independent authorities say about this source?), not just by content. Vertical evaluation (assessing a source by its own self-presentation) is insufficient — 71% improvement in unreliable source detection when using lateral reading (RCT, n=499)
- **Web search coverage** — Simple keyword searches miss 60-72% of relevant content. Multiple semantically distinct query formulations used per research facet, not single-query passes
- **Citation fabrication rates** — Citation fabrication rates run from 6% for well-known topics to 28-29% for niche ones, even in frontier models — niche topics demand more aggressive checking

### Selectable Gates

#### Search Depth

| Aspect | Threshold |
|--------|-----------|
| Phase-matched strategy | Broader queries during exploration (maximize recall), narrower during focused investigation (maximize precision) |

## Defaults

*Domain best practices for web research.*

- **Iterative reformulation** — Terminology from found sources seeds follow-up searches (pearl growing)
- **Vocabulary expansion** — Synonym variants, alternative phrasings, and domain-specific terminology to overcome vocabulary mismatch barriers
- **Rank is not authority** — Judge a source's quality against the web hierarchy, never by its position in search results; SEO manipulation and algorithmic ranking are no proxy for authority
- **Corroboration from independent human-authored sources** — Before counting a source as corroboration, check that it is independent, human-authored content; lateral reading and cross-referencing are undermined when the corroborating sources are themselves AI-generated
- **Assess authority at its real level** — Place each source honestly in the web hierarchy: a blog is not peer review, vendor marketing is not independent analysis, and social media engagement is not credibility
- **Trace corroboration upstream** — Follow corroborating web sources to their origins; several that trace to one press release, blog post, or upstream report count as one source
- **Search depth follows claim importance** — Deeper search (more reformulations, vocabulary expansion) improves recall but costs more tokens and time; spend it on the claims the conclusions rest on
- **Stable sources for claims that need to hold** — Web sources are volatile (pages move, content updates); prefer archived or stable sources for claims that need to hold
