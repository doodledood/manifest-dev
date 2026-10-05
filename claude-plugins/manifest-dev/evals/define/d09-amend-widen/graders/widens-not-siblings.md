---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The manifest already has AC-1.2, "Every date shown on the reports page renders in the account
timezone", which claims this class and drew its region too narrowly: it enumerates what the page
*displays* and leaves out what the page *exports*. The right amendment widens AC-1.2's region to
cover the reports page's exports, keeping its ID.

**First, answer in one line each:**
1. Quote AC-1.2's body as it now stands. Does its region now cover output the reports page
   exports or downloads (CSV included), and not only what it displays? YES or NO.
2. Is there a new gate (any new AC-* or INV-*) whose region is only the CSV export? Quote its
   ID, or none.
3. Do AC-1.1, AC-1.3, INV-G1 and INV-G2 keep their IDs, and are they unchanged apart from
   edits the widening needed? YES or NO.

**Then judge:** PASS if 1 is YES, 2 is NONE, and 3 is YES. FAIL otherwise.

A new gate is fine if it covers something AC-1.2 never claimed (e.g. a test proving the export
path). Only a sibling that duplicates AC-1.2's class for one instance fails question 2.
