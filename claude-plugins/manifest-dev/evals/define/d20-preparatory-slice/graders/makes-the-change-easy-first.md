---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The CLI passes a club-wide days value through cli → scheduler → reminder → format_line;
reminder and format_line also use LOAN_DAYS. Member durations live in data/members.json,
separate from the loan objects. Existing CLI characterization verifies the old 21-day output.

PASS if the plan gives the duration calculation one owner, avoids threading a second policy
parameter through every layer, and pins existing behavior before changing it. If the selected
design needs restructuring, that behavior-preserving preparation must be exercisable before
the changed behavior (a necessary verification repair may come first). A justified small design
that uses the existing boundary without separate preparation may pass; do not demand extra
Deliverables just to match an outline. FAIL if the plan entangles the same duration policy
across layers or changes behavior without checking the starting behavior.
