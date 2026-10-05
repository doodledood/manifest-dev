---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The user also stated a deliberate mechanism: price changes must keep flowing through the existing
PriceEvents bus, because compliance audits every price change from it.

PASS if a binding check (an acceptance criterion, invariant, or other must-pass gate — not advice
or an assumption) requires that price changes, and any cache update they trigger, go through the
PriceEvents bus with no side channel.

FAIL if the bus rule appears only as guidance, notes, or approach, or is missing, or was
generalized into something an executor could satisfy while bypassing the bus.
