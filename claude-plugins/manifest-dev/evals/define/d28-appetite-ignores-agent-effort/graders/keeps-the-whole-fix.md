---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Three of 23 hand-rolled retry loops double-charged, and the other 20 share the same pattern. The
fix that would be right if effort were free moves every one of the 23 processor calls onto one
retry path that always sends an idempotency key. The tech lead's two-sprint estimate is for people
writing the code; coding agents do the build, so the work they control — changing 23 call sites
and testing them — does not bound the size of the change. The size is bounded by complexity and
surface: one retry path, the call sites, nothing new beyond that.

**First, answer in one line each:**
1. Do the Deliverables and gates cover all 23 call sites moving to the one retry path, rather than
   only the three that double-charged, with the rest deferred?
2. Does the Appetite, or any Deliverable, gate or assumption, bound or justify the size of the
   change by engineer time, developer-days, sprints, weeks, team size or effort to build?

**Then judge:** PASS if the answer to 1 is yes and to 2 is no. FAIL otherwise.
