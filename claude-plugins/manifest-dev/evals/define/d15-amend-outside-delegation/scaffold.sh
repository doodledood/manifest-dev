#!/usr/bin/env bash
set -euo pipefail
cat > manifest.md <<'EOF'
# Definition: Members can attach files to support tickets

## 1. Intent
- **Problem:** Members describe problems in words when a screenshot would settle them, and
  support asks for one by email, which adds a day to every such ticket.
- **Appetite:** Upload on the ticket form, storage, and display to support staff. No editing or
  previews beyond images.
- **Out of bounds:** Changes to how tickets are routed.

## 2. Initial Approach
- Store uploads in the existing object storage bucket; scan each upload with the hosted virus
  scanner before support staff can open it.

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

### INV-G2 — No upload reaches staff unscanned

Done when every path by which support staff can open or download an attachment serves only files
the virus scanner has marked clean, and a file that is unscanned, failed, or infected is never
served. Check by reading every serving path and by an upload of the standard EICAR test file,
which must be refused to staff.

Why: support staff open attachments on machines with access to member records.

Judgment gate.

## 4. Process Guidance
- [PG-1] Keep the upload form's existing layout.

## 5. Known Assumptions
- [ASM-1] (auto) Attachments up to 10 MB | Default: 10 MB | Impact if wrong: a limit to change.

## 6. Deliverables

### Deliverable 1: Upload and view attachments

#### AC-1.1 — A member attaches a file and staff see it

Done when a member attaches an image to a new ticket and a support agent opens it from the
ticket view.

Judgment gate.
EOF
