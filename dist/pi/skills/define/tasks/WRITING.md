# WRITING Task Guidance

Base guidance for all text-authoring tasks (articles, emails, marketing copy, social media, creative writing). Source: writing plugin v1.3.0.

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

## Defaults

*Domain best practices for this task type.*

- **Multi-layer editing** — Edit beyond vocabulary: word-level (kill-list), sentence-level (structure), paragraph-level (rhetoric/tone), content-level (substance). Never just word replacement
- **Kill-list cross-check** — Full vocabulary kill-list applied to output
