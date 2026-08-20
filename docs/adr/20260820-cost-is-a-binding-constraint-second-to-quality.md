# ADR: Cost is a binding constraint, second to quality

## Status
Accepted

## Area
Positioning

## Context
The North Star's Never list carried cost as a non-goal: "optimizing for token cost or
speed at quality's expense", with spending more to get a better result named as the trade
the project makes. In practice the suite had already grown cost-relief valves out of
necessity, because full-process runs priced on high-end models became practically too
expensive for routine use: the `just-do` and `just-auto` executors run the same Manifest
contract with minimal process, and the `consolidated` and `self` verification modes exist
beside the independent `per-gate` default (per
`20260730-consolidated-default-verification-mode` and
`20260808-restore-per-gate-default-verification-mode`). A stance the project's own
shipped surface repeatedly works around is not the project's stance; the owner ruled the
position forward on 2026-08-20.

This is the first live exercise of the North Star update asymmetry
(`20260820-north-star-lines-carry-states`): a `ruled` position moved on the owner's
explicit ruling, and this record is the remembered why.

## Decision
Cost is a binding constraint, second to quality. Quality remains the deciding axis —
nothing trades quality away for token cost or speed — but affordability on high-end
models is a requirement every workflow must meet, not a dimension the project ignores:
leaner execution and verification paths are first-class citizens of the suite rather
than concessions, and future scoping conversations may weigh practical cost without
betraying the positioning. Unchanged: the "cost optimizers" anti-persona (people whose
primary axis is cost are still not who this is for), and the bounded-not-cheap defect
rule (a run that keeps verifying past its satisfied gates is a workflow defect, never a
meter the user watches). The North Star's Never entry is rewritten accordingly.

## Alternatives Considered
- **Keep the non-goal stance**: rejected — the suite's own shipped valves contradict it,
  and a standing direction the practice works around steers wrong.
- **Make cost a co-primary objective**: rejected — the promise, the audience, and the
  anti-persona are quality-first and unchanged; cost binds, it does not decide.
- **Encode a token- or time-denominated Appetite**: rejected before
  (`20260727-manifest-intent-leads-with-problem-appetite-and-bounds`) and not reopened —
  Appetite stays a complexity-and-surface bound; cost pressure is met by mode choice,
  not by re-denominating the contract.

## Consequences

### Positive
- The North Star states the stance the project actually operates, so sessions anchoring
  on it stop reading the lean paths as departures.
- Cost-motivated design work (cheaper verification, leaner chains) is legitimate
  first-class work rather than something argued around the positioning.

### Negative
- A softer line invites cost-creep pressure toward quality trades; the deciding-axis
  clause and the anti-persona are the boundary that must hold it.

## Source
- Session: owner ruling, 2026-08-20; first exercise of the North Star update flow.
- Related: 20260820-manifest-dev-owns-a-project-north-star, 20260820-north-star-lines-carry-states, 20260727-manifest-intent-leads-with-problem-appetite-and-bounds
