# WRITING Task Guidance

Base guidance for all text-authoring tasks (articles, emails, marketing copy, social media, creative writing). Source: writing plugin v1.3.0.

## The Core Problem

AI text is measurably more predictable, less varied, and narrower in vocabulary than human writing. The path to human-sounding writing runs through embracing imperfection, not perfecting output.

## Quality Gates

| Aspect | Agent | Fallback | Threshold |
|--------|-------|----------|-----------|
| Vocabulary, Structure, Tone, Rhetoric, Craft, Negative space | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no MEDIUM+ |
| Voice compliance | general-purpose | — | Matches AUTHOR_VOICE.md (conditional: only when doc exists) |
| Readability | general-purpose | — | Accessible to target audience, scannable structure |
| Anti-slop | general-purpose | — | No kill-list vocabulary, hedge words, filler phrases, generic phrasing |
| Accuracy | general-purpose | — | Claims supported, no contradictions |
| Audience fit | general-purpose | — | Language and depth match target reader |
| Clarity | general-purpose | — | No ambiguous terms or undefined jargon |
| Statistical variation | general-purpose | — | Sentence-length variation and vocabulary diversity present; uniform rhythm is an AI tell |

Writing-reviewer severity: CRITICAL = immediately identifiable as AI. HIGH = experienced readers would notice. MEDIUM/LOW = informational only.

## Context to Discover

Writer substance is ~70% of output quality; editing ~20%; prompting ~10%. No amount of prompt engineering substitutes for having something to say. Before defining deliverables for a writing task, probe for:

| Context Type | What to Surface | Probe |
|--------------|-----------------|-------|
| **Key points / thesis** | Writer's actual argument, not a generic topic | What's your take? What are you trying to say? |
| **Personal experience** | Specific anecdotes, firsthand observations, failures | What have you seen / done / learned about this? |
| **Opinions / angle** | What the writer believes, their perspective | What do you think about this? What's your angle? |
| **Specific details** | Names, numbers, dates, places that ground the piece | What concrete details can you provide? |
| **Audience** | Who reads this, what they know, what they should walk away with | Who is this for? What should they take away? |
| **Tone / voice** | How should this feel? Existing AUTHOR_VOICE.md? | Check for AUTHOR_VOICE.md; if absent, ask: what tone? |

## Compressed Domain Awareness

*Detailed reference for all sections below: `references/WRITING-REFERENCE.md` (for verification, not interview context)*

**Vocabulary Kill-List** — ~70 statistically flagged AI words/phrases: nouns (delve, tapestry, landscape...), verbs (leverage, harness, navigate...), adjectives (seamless, robust, transformative...), adverbs (seamlessly, meticulously, moreover, furthermore...), stock phrases, hedging phrases, false intensifiers, **puffery/promotional drift** ("breathtaking," "must-visit," "iconic," "world-class," "rich cultural tapestry," "hidden gem"). AI also replaces simple verbs with elaborate alternatives (10%+ decrease). **Era-tracked**: vocabulary shifts over time (e.g. "delve" peaked 2023–early 2024 then declined; "align with"/"fostering"/"showcasing" rose with later models). Reviewers judge by density/clustering, not single instances.

**Anti-Patterns** — 21 patterns: structural (6: uniform paragraphs, list addiction, formulaic scaffolding, grammar perfection, colon titles, symmetric structure), rhetorical (10: tricolon obsession, perfect antithesis, rhetorical staging, excessive hedging, compulsive signposting, opinion-avoidant framing, **overused conjunctions** stacking — moreover/furthermore/additionally per paragraph, **"myths busted" / contrast-and-correct** strawman openers, **subject puffery** — "a microcosm of..."/"a window into...", **statistical regression to the mean** — concrete details blurred to category-level), tonal (5: uniform register, relentless positivity, equal distance, risk aversion, **encyclopedic-yet-promotional drift** — neutral prompts drift to advertisement-like writing).

**Punctuation & Formatting** — Em-dashes are the top AI tell (ban entirely). AI overuses emojis, avoids semicolons/contractions, applies Oxford commas consistently. **Curly quotation marks** ("" '') flag ChatGPT/DeepSeek vs straight (Gemini/Claude) — combinatorial signal, not standalone. **Heading capitalization**: AI defaults to title case even in sentence-case documents — match surrounding style. **Excessive boldface** ("key takeaways" pattern): AI mechanically bolds same phrase repeatedly or redeclares bold phrase in bullet bodies — use sparingly. Casual markers ("So," "Anyway," "in my experience") have disproportionate human-feel impact.

**Craft Fundamentals** — Seven human-AI gaps: showing vs telling, specificity from lived experience, strategic omission, rhythm variation, deliberate rule-breaking, humor (AI-complete problem), genuine insight.

**Statistical Signatures** — AI is ~50% more predictable (perplexity), ~38% less varied (burstiness), narrower vocabulary, increasingly predictable as it continues. Target ~7th grade readability.

**Model-Specific Signatures** — ChatGPT: formal, heavy em-dashes, "delve." Gemini: conversational, simple. Claude: literary, flexible. Deepseek: heavy em-dashes, ChatGPT-like.

**Multi-Layer Editing** — Surface-to-substance: word-level (kill-list), sentence-level (pattern breaking), structural (meta-commentary removal), content (lived experience), final check (read aloud).

**Negative Space** — AI identified by absence: lived experience, sensory specificity, silence/subtext, genuine messiness, unique perspective.

**Editorial Standards** — Accepted: distinctive voice, subtext, specificity, emotional truth, intentional craft, surprise. Rejected: uniform structure, generic language, no subtext, over-smooth prose, telling not showing.

## Risks

- **Hollow output** — content passes review but lacks writer's genuine substance; probe: was the 70% (writer input) actually provided?
- **Disembodied voice** — lacks specific experiences, opinions, data; probe: check for AUTHOR_VOICE.md?
- **Encyclopedic-promotional drift** — neutral/factual register slides into travel-guide or marketing puffery; probe: is the register specific and unlabored, or is it polished-bland with "must-visit"/"world-class" vocabulary?
- **Regression to the mean** — concrete details (names, numbers, dates) get blurred into category-level language during drafting; probe: are specifics restored or did the writer say "I don't know"?

## Scenario Prompts

- **Voice inconsistency** — tone shifts between sections, or doesn't match AUTHOR_VOICE.md; probe: consistent voice throughout? voice doc consulted? brand guidelines?
- **Missing credibility signal** — no reason to trust author; probe: what authority/experience backs this?
- **Wrong reader assumptions** — assumes knowledge reader lacks or doesn't have; probe: what does audience know? what must reader know first?
- **Missing examples** — abstract explanation, no concrete cases; probe: would examples help?
- **Buried critical info** — important details hidden in middle; probe: what must reader not miss?
- **Relentless positivity kills credibility** — everything framed as great; no honest assessment; probe: are weaknesses acknowledged?
- **Perspective collapse** — writing aggregates so many views it has none; probe: does the author take a position?
- **Strawman opener** — piece opens with "While many think X, in fact Y" without a real myth; probe: is there an actual misconception worth correcting, or skip the contrast-and-correct framing?
- **Subject puffery** — arbitrary detail elevated to "a microcosm of..." or "a window into..."; probe: does the piece earn the broader extrapolation, or should it stop at the specific?
- **Conjunction stacking** — moreover/furthermore/additionally appear at AI-typical density across paragraphs; probe: can transitions be cut so sentences carry the logic?

## Trade-offs

- Comprehensive vs scannable
- Opinionated vs balanced
- Formal vs accessible
- Polished vs authentic (imperfection signals humanity)
- Specific vs broadly applicable
- Voice consistency vs tonal variation

## Defaults

*Domain best practices for this task type.*

- **Multi-layer editing** — Edit beyond vocabulary: word-level (kill-list), sentence-level (structure), paragraph-level (rhetoric/tone), content-level (substance). Never just word replacement
- **Kill-list cross-check** — Full vocabulary kill-list applied to output
