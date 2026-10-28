use the define skill for this — amending an existing manifest.

here's the manifest we're executing (save it as ./manifest.md first, then amend that file in
place):

````markdown
# Definition: Weekly activity digest email

## 1. Intent
- **Problem:** Members miss what happened in their workspace during the week, because the only
  record is the in-app activity feed, which they open rarely. (The user ruled on 2026-10-01 that
  the digest is weekly, not daily.)
- **Appetite:** Small — one scheduled email built from the existing activity feed; no new
  settings page.
- **Out of bounds:** INV-G2

## 2. Initial Approach
- **Architecture:** A weekly job reads the member's activity feed for the past seven days and
  sends one plain-text email (AC-1.2) through the existing mail relay. Plain text only, per the
  user's ruling on 2026-10-02.

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
merged into the head — the fixes every run owes on its pull request — a pre-existing issue the
work met whose fix is not a project of its own, and a below-bar finding from a first full look
applied because it improves the work — and work discharging what a criterion required, including
sweeping a changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.

### INV-G2 — No new mail provider

Done when the diff sends mail only through the existing relay client and adds no mail provider
dependency.

Why: the user ruled on 2026-10-03 to stay on the existing relay.

Deterministic gate.

## 5. Known Assumptions
- [ASM-1] User's call (2026-10-02): the digest is plain text only | Default: a single text/plain
  part | Impact if wrong: the email looks bare in rich clients
- [ASM-2] (auto) Send time | Default: Monday 08:00 in the member's timezone | Impact if wrong:
  the email arrives at an awkward hour

## 6. Deliverables

### Deliverable 1: The weekly digest

*What it is, and how it is exercised end-to-end:* a member with a week of activity receives the
digest on Monday morning and reads what happened.

#### AC-1.1 — The digest lists the week's activity

Done when, for a member whose feed holds comments and mentions from the past seven days, the
digest lists every comment and every mention, each with its author and a link, checked by a test
that seeds both kinds.

Deterministic gate.

#### AC-1.2 — The digest is plain text

Done when the sent message has exactly one part, of type text/plain, as AC-1.1's test observes.

Why: the user ruled on 2026-10-02 that the digest is plain text.

Deterministic gate.

#### AC-1.3 — Unsubscribe works

Done when the digest carries an unsubscribe link and following it stops the next digest for that
member, checked by a test.

Deterministic gate.
````

steering, two things:
1. QA: reactions show in the activity feed but are missing from the digest. fix the manifest so
   this is covered.
2. product changed its mind: the digest is HTML now, with a plain-text alternative part for
   clients that can't render HTML.

the repo isn't available to you here. i'm afk, dont ask me anything. the amended manifest goes
to ./manifest.md in the current directory, not your home directory.
