# ADR: figure-out writes in Simplified Technical English style by default

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
figure-out's turns already follow a plain-language floor and a one-claim shape. Its messages still read too dense: the maintainer could not answer one question until it was rewritten in ASD-STE100 (Simplified Technical English) style. ASD-STE100 sets sentence-length limits — 20 words for an instruction, 25 for a description — and prefers the active voice, common words, and one term for one thing.

## Decision
Everything figure-out writes for people follows ASD-STE100 writing rules by default. That covers turns, the read, offers, log entries, and team posts. The rules used are short sentences, active voice, common words, and one term for one thing. The strict STE dictionary is not required; the target is about 90% conformance, for easier reading rather than strict compliance. The user's own instructions on style win, with no flag needed.

## Alternatives Considered
- **Strict ASD-STE100, dictionary included**: the dictionary bans many precise words; the goal is easier reading, not certification.
- **Keep the plain-language floor alone**: the floor did not prevent the dense message that had to be rewritten.
- **A style flag**: the user's own instructions already override the default without a flag.

## Consequences

### Positive
- Turns read faster, especially for a reader not fluent in the topic.
- A named standard gives the writer and a reviewer the same measure.

### Negative
- Some ideas take more sentences to state.
- The style applies only to figure-out; other skills keep their own registers.

## Source
- Session: figure-out investigation of how figure-out reaches its user.
- Related: 20260803-figure-out-turn-carries-one-concrete-claim
