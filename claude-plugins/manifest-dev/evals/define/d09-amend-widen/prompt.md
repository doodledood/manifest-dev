---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this — amending an existing manifest.

here's the manifest we're executing (save it as ./manifest.md first, then amend that file in
place):

````markdown
# Definition: Account timezone in customer-facing dates

## 1. Intent
- **Problem:** Customers see dates in UTC on the reports page instead of their account's
  timezone, so "yesterday's" numbers are labelled with the wrong day for anyone west of London.
- **Appetite:** Small — make the reports page honor the account timezone; no new settings.
- **Out of bounds:** INV-G2

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing beyond what the Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Problem, Appetite, and Out of bounds as the intent. Read the Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — and work discharging what a criterion required, including sweeping a
changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.

### INV-G2 — No change to how timezones are stored

Done when the diff leaves the account timezone column, its type, and its write path unchanged.

Deterministic gate.

## 5. Known Assumptions
- [ASM-1] Account timezone is always set | Default: fall back to UTC if null | Impact if wrong:
  some accounts keep seeing UTC

## 6. Deliverables

### Deliverable 1: Reports page in account timezone

*What it is, and how it is exercised end-to-end:* a customer in a non-UTC account opens the
reports page and reads dates and day boundaries in their own timezone.

#### AC-1.1 — Report day boundaries follow the account timezone

Done when, for an account set to America/Los_Angeles, a report for "yesterday" covers midnight to
midnight Los Angeles time, checked by a test that seeds events either side of UTC midnight.

Deterministic gate.

#### AC-1.2 — Every date shown on the reports page renders in the account timezone

Enumerate every date or timestamp the reports page displays — table cells, chart axes, headers,
tooltips — by reading the page's components. Done when each one formats through the account
timezone, with zero rendered in UTC.

Judgment gate.

#### AC-1.3 — Existing report tests still pass

Done when the reports test suite passes.

Deterministic gate.
````

steering from QA: the CSV you download from the reports page ("export") still has every
timestamp in UTC. fix the manifest so this gets covered.

the repo isn't available to you here. i'm afk, dont ask me anything. the amended
manifest goes to ./manifest.md in the current directory, not your home directory.
