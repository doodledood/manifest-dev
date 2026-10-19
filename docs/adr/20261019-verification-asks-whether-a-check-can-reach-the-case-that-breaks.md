# ADR: Verification asks whether a check can reach the case that breaks, and names the kind of check

## Status
Accepted — amended by 20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate: define's review searches a Manifest for holes, and extends an existing design model with its gates to do so, while proving a Manifest stays rejected; and by 20261019-test-quality-asks-whether-a-kept-test-reaches-the-case-that-breaks-a-guarantee: the question also reaches pull-request review through test-quality

## Area
Task guidance

## Decided by
The user

## Context
figure-out and define settle how a change will be verified before it is built, and both lean on
example tests. Some correctness depends on the order of events — two writers, a retry, a crash
halfway — or must hold for every input, and example tests rarely reach the case that breaks it.
Formal methods reach those cases, since a model checker explores every order of events within a
bound, and a model of manifest-dev's own ticket protocol found a stall and a duplicate record that
the review had missed. The question was how much of that to bring into the shipped prompts.

## Decision
- Where correctness depends on the order of events or holds for every input, verification design
  asks whether example tests can reach the case that breaks, and where they cannot, uses the
  cheapest check that can: generated inputs or call sequences on the real code, then a model
  checker for an order-dependent design, then a verifier on the code where the language has one,
  and a proof only where no bound is enough. That check becomes a recipe or a test like any other.
- A design whose correctness depends on the order of events is modeled in scratch and the model
  checked before the design is built; what the model finds becomes design decisions and gates.
  The model is throwaway by default and kept as a check only where the design will keep changing.
- Rules that several runs, agents or people follow on the same state get the same question when
  they are written as prompt text rather than code, since a protocol in prose breaks the same way.
- Modeling is a default with a trigger, never a must: the run decides whether the risk warrants a
  model and how deep it goes. What binds is what a model finds, once it becomes a gate.
- The shipped prompts name the question and the kind of check, with a tool or two as examples —
  such as TLA+ or Alloy for a design, Kani for Rust code — never as the required one.
- The changes go into the existing task files' probes and Defaults, coding and prompting, in
  figure-out and define alike, as their mirror pairs require. No skill is added, and nothing
  model-checks a Manifest's own text.

## Alternatives Considered
- **A formal-verification skill**: a new skill a person must know to reach for,
  against the North Star's "nothing to memorize"; the question in the probe reaches every coding
  task instead.
- **Name no tool**: fits every stack, but leaves a run without a concrete place to start.
- **Require a named tool**: concrete, but fits one stack each and dates quickly.
- **Require a model for every order-dependent design**: models written to satisfy the rule rather
  than to find a defect, at a cost the North Star binds.
- **Translate a Manifest's gates into a formal language and check them**: the translation of prose
  into logic is the unreliable step, and a proof over a wrong translation looks like strong
  evidence while proving nothing.

## Consequences

### Positive
- Order-dependent and every-input designs get a check that can fail on the case that breaks them.

### Negative
- A model in scratch costs time before building, and drifts unless it is kept as a check.
- Which check is cheapest stays the run's judgment.

## Enforced by
partly — eval cases `56-order-dependent-design` (a design in code) and `60-protocol-in-prompts`
(a protocol in prompt text) measure figure-out's half once run; that a named tool stays an example
stays judgment.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice, and a model of
  the ticket protocol (2026-10-19).
- Related: see also 20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes,
  20261019-a-check-counts-only-after-it-was-seen-to-fail
