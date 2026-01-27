# RESEARCH Task Guidance

Task-specific guidance for research deliverables: investigations, analyses, comparisons, competitive reviews, technology evaluations.

## Research-Specific Interview Probes

Surface these dimensions that the general /define flow won't naturally cover:

- **Question type**: Comparison, recommendation, how-to, landscape survey, competitive analysis, factual lookup? Classification drives decomposition strategy and evidence rigor.
- **Sub-question decomposition**: Break the main question into sub-questions. Each becomes an AC or deliverable section—this IS the research architecture.
- **Source authority expectations**: What counts as authoritative for this topic? Probe using the hierarchy below. Encode as INV-G.
- **Recency requirements**: Fast-moving topics (frameworks, AI/ML, cloud) need sources from last 12 months. Stable topics (algorithms, design patterns) accept up to 5 years. When unsure: yearly major versions = fast-moving.
- **Cross-referencing rigor**: How many independent sources must agree for a claim to be verified? (Recommended: 2+ for key findings in Summary/Recommendations)
- **Conflict handling**: When authoritative sources disagree—present both positions (Contested), or attempt resolution?

## Research Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Source credibility | general-purpose | All cited sources rated Medium+ authority; no Low-authority-only claims in key findings |
| Cross-referencing | general-purpose | Claims in Summary/Recommendations verified across 2+ independent sources |
| Recency | general-purpose | Sources current per recency requirements; publication dates noted |
| Objectivity | general-purpose | Balanced presentation; dissenting views included |
| Gap honesty | general-purpose | Unanswered questions and knowledge gaps explicitly stated |

**Source Authority Hierarchy** (encode in Process Guidance for implementer reference):
- **High**: Official documentation, peer-reviewed research, engineering blogs from the product's creator
- **Medium**: Established tech publications (InfoQ, ThoughtWorks Radar), well-regarded engineering blogs (Netflix, Stripe, Uber), Stack Overflow answers with 50+ upvotes plus code examples or citations
- **Low**: Personal blogs without credentials, tutorials lacking citations, forums, outdated content

**Encoding**: Add selected gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: general-purpose
  model: opus
  prompt: "Review research for [quality aspect]. Source authority: High = official docs, peer-reviewed, creator blogs; Medium = established publications, top SO answers; Low = personal blogs, forums, outdated. Flag key findings backed only by Low-authority sources."
```

## Research Architecture

For research tasks, **Architecture = decomposition strategy**. Generate concrete options:

- **By sub-question**: Each sub-question → deliverable section. Best for focused investigations.
- **By source type**: Primary → secondary → synthesis. Best for literature reviews.
- **By perspective**: Stakeholder A → Stakeholder B → synthesis. Best for competitive analysis.
- **By phase**: Broad exploration → targeted gap-filling → synthesis. Best for landscape surveys.

## Research-Specific Risks

These are research failure modes the general pre-mortem won't surface:

- **Source bias**: All sources from same perspective or organization
- **Confirmation bias**: Only finding evidence supporting initial hypothesis
- **Recency gap**: Topic evolved since most-cited sources were published
- **Coverage gap**: Sub-question has no authoritative sources
- **Conflicting authorities**: High-authority sources directly contradict each other

## Research-Specific Trade-offs

- **Depth vs. breadth**: Deep analysis of fewer sources vs. broad survey of many
- **Recency vs. authority**: Recent blog post vs. older peer-reviewed paper
- **Completeness vs. focus**: Covering every angle vs. answering the core question well

## Research-Specific AC Patterns

**Coverage**
- "Covers [topic] from [N]+ independent sources rated Medium+ authority"
- "All [N] sub-questions addressed with evidence"
- "Addresses counterarguments to [thesis]"

**Source Quality**
- "All claims in Summary/Recommendations cite 2+ independent sources"
- "No key finding relies solely on Low-authority sources"
- "Source authority rated (High/Medium/Low) for each citation"

**Rigor**
- "Conflicting sources identified and both positions presented"
- "Confidence level stated per sub-question (High/Medium/Low/Contested/Inconclusive)"
- "Limitations and knowledge gaps explicitly stated"

**Synthesis**
- "Findings synthesized into [recommendations / comparison matrix / evidence summary]"
- "Source summary table: Source, Authority rating, Date, What it provided"

## Research-Specific Process Guidance Patterns

Research accumulates findings across many searches—context rot is the primary failure mode. Encode relevant items as PG-*:

- "Maintain research notes file; write findings AFTER each search batch, BEFORE next search; read full notes BEFORE synthesis"
- "Self-critique periodically: check source diversity, recency, confirmation bias, coverage gaps"
- "Rate every source using the authority hierarchy before citing"
- "When search yields no results, try alternative query formulations before marking gap"
