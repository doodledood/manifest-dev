---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The manifest was amended after QA reported that the reports page's CSV export still shows UTC.
An amended manifest should read as if written today for the current task.

**First, answer in one line each:**
1. Is there a date anywhere in the manifest that records when something was decided or changed
   (such as "ruled on 2026-…" or "updated 2026-…")? Dates that are task content — a timestamp used
   as test data, a deadline — do not count. YES or NO.
2. Outside the Known Assumptions section, is there historical narration of how the contract
   changed? Current source authority beside a claim (for example, the user's deliberate timezone
   requirement) is required provenance, not historical narration. An `(auto)` mark is not history.
   YES or NO.
3. Does any section still state that downloads or exports stay in UTC, or carry text saying that
   rule changed ("previously…", "no longer…", "updated to…", "was…")? A Problem that describes
   today's defect does not count as stating the rule; change text counts wherever it sits. YES or NO.

**Then judge:** PASS if all three are NO. FAIL otherwise.
