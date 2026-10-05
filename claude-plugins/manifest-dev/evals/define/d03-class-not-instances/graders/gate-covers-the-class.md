---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The user reported three places dates render in UTC (invoice PDF, weekly email, reports page) and
said outright that formatting is scattered and there are probably more. The defect is a class:
any date shown to a customer that ignores the account timezone.

**First, quote** the gate or gates that check timezone-correct dates. For each, answer one line:
does the gate's body make the evaluator find customer-facing date output across the product — by
naming a region and a way to enumerate it (e.g. every call site that formats a date for display,
every template, every outbound document) — or does it list fixed surfaces? Answer **REGION** or
**INVENTORY**.

**Then judge:** PASS if at least one gate is REGION. FAIL if every timezone gate is INVENTORY,
meaning it checks only named surfaces, however many it names.

Naming the three reported surfaces as examples *inside* a region-wide gate is fine.
