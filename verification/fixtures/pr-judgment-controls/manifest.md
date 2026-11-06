# Definition: Sponsor shelf implementation

## 1. Intent
- **Outcome:** Partnerships can reserve up to three of the five visible recommendation slots for sponsored books, with the remaining slots filled by relevance.
- **Outcome evidence:** Read recommendations.py and replay catalog.json.
- **Problem:** Sponsors cannot currently reserve placement.
- **Appetite:** The recommendation selection only.
- **Out of bounds:** None beyond the assignment.

## 2. Initial Approach (Complex Tasks Only)
Use the current ranking function.

## 3. Global Invariants

### INV-G1 — The visible shelf remains bounded
Authority: hard — the requested shelf has five visible slots.
The function returns no more than five books, with no invented entries.
Evidence: Replay catalog.json and inspect the function.
Deterministic gate.

## 4. Process Guidance
- [PG-1] Keep the implementation local.

## 5. Known Assumptions
- [ASM-1] The caller supplies unique books and valid tags. Default: retain the existing input contract. Impact if wrong: separate input validation is needed.

## 6. Deliverables
### Deliverable 1: Sponsor placement
*What it is, and how it is exercised end-to-end:* A caller receives the requested sponsored shelf from the catalog.

#### AC-1.1 — Three sponsored slots
Authority: hard — the requested implementation puts up to three sponsored books ahead of ordinary books within the five-slot result.
Select up to three sponsored books by relevance, then fill available visible slots with remaining books by relevance.
Evidence: Replay catalog.json and inspect recommendations.py.
Deterministic gate.
