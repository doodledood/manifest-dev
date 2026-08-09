# ADR: Walk-pr triages captured input before drafting comments

## Status
Accepted

## Area
PR review

## Context
Walk-pr ends by turning the reviewer's captured responses into a posted PR review. The prior contract synthesized draft comments from every captured response and presented them as one batched plan for approval. A real walk exposed two failures. First, captured input is not homogeneous: alongside settled calls, the highest-value entries were questions ("does the design doc justify this deviation?") and objections whose answers lived in code, ADRs, or upstream design documents — and investigating them routinely flipped or reshaped the would-be comment. Drafting them directly would have posted wrong or premature comments under the reviewer's name. Second, a batched approval table recreated exactly the overload the walk exists to prevent.

## Decision
In every walk-pr mode, the end-of-walk phase triages each captured item into one of three kinds before anything is drafted: (a) settled calls that become draft comments, (b) questions the agent must answer from the code, ADRs, and upstream design documents before drafting — including fetching the design doc when the PR implements one, since design-vs-implementation deviations are prime review material, and (c) drops that generate nothing. Proposed comments are then confirmed with the reviewer one item at a time, and posted together as a single PR review only after all items lock.

## Alternatives Considered
- **Draft a comment from every captured response (prior contract)**: Rejected; treats questions as verdicts. Observed answers from code and design docs changed or eliminated proposed comments.
- **Batched plan-of-comments approval (prior contract)**: Rejected; a table of all comments at once reproduces the text-wall overload the walk's one-idea-at-a-time discipline exists to prevent.
- **Triage in canvas mode only**: Rejected; review integrity should not depend on presentation medium — chat-mode walks capture the same mix of calls and questions.

## Consequences

### Positive
- Posted reviews carry only investigated, confirmed positions; questions get answered instead of published.
- One-at-a-time confirmation keeps the end phase inside the same attention contract as the walk itself.
- Design-doc deviations surface systematically rather than by luck.

### Negative
- The end phase takes longer — investigation plus per-item confirmation instead of one batched approval.
- More agent turns per walk; the reviewer must stay engaged through the confirmation sequence.

## Source
- Session: figure-out session reworking walk-pr (2026-07-30), drawing on the paste-back phase of a real walk where investigation flipped several would-be comments.
- Related: 20260730-walk-pr-attention-contract-picture-not-document
