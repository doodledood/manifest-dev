# WRITING Task Guidance

Base guidance for all text-authoring tasks (articles, emails, marketing copy, social media, creative writing). Source: writing plugin v1.2.0.

## The Core Problem

AI text is measurably more predictable, less varied, and narrower in vocabulary than human writing. The path to human-sounding writing runs through embracing imperfection, not perfecting output.

## Quality Gates

| Aspect | Agent | Fallback | Threshold |
|--------|-------|----------|-----------|
| Vocabulary | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
| Structure | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
| Tone | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
| Rhetoric | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
| Craft | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
| Negative space | writing-reviewer | general-purpose + `references/WRITING-REFERENCE.md` | no HIGH/CRITICAL |
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

**Vocabulary Kill-List** — ~60 statistically flagged AI words/phrases: nouns (delve, tapestry, landscape...), verbs (leverage, harness, navigate...), adjectives (seamless, robust, transformative...), adverbs (seamlessly, meticulously...), stock phrases, hedging phrases, false intensifiers. AI also replaces simple verbs with elaborate alternatives (10%+ decrease).

**Anti-Patterns** — 17 patterns: structural (6: uniform paragraphs, list addiction, formulaic scaffolding, grammar perfection, colon titles, symmetric structure), rhetorical (6: tricolon obsession, perfect antithesis, rhetorical staging, excessive hedging, compulsive signposting, opinion-avoidant framing), tonal (5: uniform register, relentless positivity, equal distance, risk aversion, emotional overreach).

**Punctuation & Formatting** — Em-dashes are the top AI tell (ban entirely). AI overuses emojis, avoids semicolons/contractions, applies Oxford commas consistently. Casual markers ("So," "Anyway," "in my experience") have disproportionate human-feel impact.

**Craft Fundamentals** — Seven human-AI gaps: showing vs telling, specificity from lived experience, strategic omission, rhythm variation, deliberate rule-breaking, humor (AI-complete problem), genuine insight.

**Statistical Signatures** — AI is ~50% more predictable (perplexity), ~38% less varied (burstiness), narrower vocabulary, increasingly predictable as it continues. Target ~7th grade readability.

**Model-Specific Signatures** — ChatGPT: formal, heavy em-dashes, "delve." Gemini: conversational, simple. Claude: literary, flexible. Deepseek: heavy em-dashes, ChatGPT-like.

**Four-Layer Editing** — Five steps surface-to-substance: word-level (kill-list), sentence-level (pattern breaking), structural (meta-commentary removal), content (lived experience), final check (read aloud).

**Negative Space** — AI identified by absence: lived experience, sensory specificity, silence/subtext, genuine messiness, unique perspective.

**Editorial Standards** — Accepted: distinctive voice, subtext, specificity, emotional truth, intentional craft, surprise. Rejected: uniform structure, generic language, no subtext, over-smooth prose, telling not showing.

## Risks

- **Hollow output** — content passes review but lacks writer's genuine substance; probe: was the 70% (writer input) actually provided?
- **Wrong depth** — too technical or too shallow for readers; probe: what does audience already know?
- **Disembodied voice** — lacks specific experiences, opinions, data; probe: check for AUTHOR_VOICE.md?
- **Wrong audience** — language and depth don't match reader; probe: who reads this, what do they know?

## Scenario Prompts

- **Hollow output without substance** — polished prose, no actual insight or lived experience; probe: what writer-specific substance went in before generation?
- **Voice inconsistency** — tone shifts between sections, or doesn't match AUTHOR_VOICE.md; probe: consistent voice throughout? voice doc consulted?
- **Tone mismatch** — doesn't sound like author/brand; probe: check AUTHOR_VOICE.md? brand guidelines?
- **Missing credibility signal** — no reason to trust author; probe: what authority/experience backs this?
- **Wrong reader assumptions** — assumes knowledge reader lacks; probe: what does audience know?
- **Missing prerequisites** — assumes knowledge reader doesn't have; probe: what must reader know first?
- **Missing examples** — abstract explanation, no concrete cases; probe: would examples help?
- **Buried critical info** — important details hidden in middle; probe: what must reader not miss?
- **Relentless positivity kills credibility** — everything framed as great; no honest assessment; probe: are weaknesses acknowledged?
- **Perspective collapse** — writing aggregates so many views it has none; probe: does the author take a position?

## Trade-offs

- Comprehensive vs scannable
- Opinionated vs balanced
- Formal vs accessible
- Polished vs authentic (imperfection signals humanity)
- Specific vs broadly applicable
- Voice consistency vs tonal variation

## Defaults

*Domain best practices for this task type.*

- **Four-layer editing** — Edit beyond vocabulary: word-level (kill-list), sentence-level (structure), paragraph-level (rhetoric/tone), content-level (substance). Never just word replacement
- **Kill-list cross-check** — Full vocabulary kill-list applied to output
