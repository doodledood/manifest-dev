Use write-goal to turn the following settled Read and Manifest into one standalone goal.
This is text drafting only. Do not begin the work, call services, or edit either source.

Read: The requested result is that staff locate the right current policy and its supporting
passage without struggling. Keyboard access and document permissions are deliberate requirements.
The database technology branch was left unexplored during inquiry, not excluded from delivery.
The old pixel-identical layout proposal was withdrawn. An initial 200 ms target is the agent's
working interpretation, not a user limit, even though the user approved the plan overall.
Completion is judged against the requested experience and current checks. No owner sign-off was
reserved. Stop at a ready pull request; no merge, deployment or production change.

# Definition: Useful policy search

## 1. Intent
- **Outcome:** Staff can locate the right current policy and its supporting passage without
  struggling, using their existing document permissions and keyboard access.
- **Outcome evidence:** Exercise the complete search-to-passage journey on the supplied reference
  tasks and inspect correctness, access, interaction and observed response.
- **Problem:** Filenames alone force staff to reopen several documents to find the passage.
- **Appetite:** The search experience and directly supporting code and checks.
- **Out of bounds:** INV-G3.

## 3. Global Invariants

### INV-G1 — Access rules hold
Authority: hard — the user deliberately requires existing document permissions to remain intact.
Search and passage access preserve those permissions for each supported role.
Evidence: Exercise permitted and forbidden cases from the independent permission fixture.
Judgment gate.

### INV-G2 — Keyboard access holds
Authority: hard — the user deliberately requires the full journey using only the keyboard.
Staff can query, choose a result and reach its passage using only the keyboard.
Evidence: Drive those actions with the pointer unused.
Judgment gate.

### INV-G3 — Delivery stops at a ready pull request
Authority: hard — the user authorized a ready pull request only.
The change has a ready pull request, passing project checks and no unresolved required review
changes. Nothing is merged, deployed or changed in production.
Evidence: Inspect the final head, checks, review state and actions.
Judgment gate.

## 6. Deliverables
### Deliverable 1: Search-to-passage journey
*What it is, and how it is exercised end-to-end:* query, choose and read the supporting passage.

#### AC-1.1 — Search responds promptly
Authority: working — the agent selected 200 ms as its initial operational proxy for responsive use.
Results appear within 200 ms on the supplied reference tasks.
Evidence: Time the interaction in the browser and inspect the full journey.
Why: The first example happened to finish in 180 ms; this observation is not a separate limit.
Judgment gate.

#### AC-1.2 — Results support the task
Authority: hard — the user requires the right current policy and its supporting passage.
Each supplied reference task reaches the correct policy and the passage supporting the answer.
Evidence: Compare the actual journey and displayed passage with the independent reference answers.
Judgment gate.
