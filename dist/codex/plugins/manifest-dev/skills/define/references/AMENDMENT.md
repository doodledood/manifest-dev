# Amendment

A manifest path means amend. Read it fully. Validate the Outcome and every gate against the
current schema first: a title, Authority, a claim body, Evidence, an optional why and a stated
kind. Missing Outcome or authority, a `verify` block, a `phase`, or a missing kind means an
incompatible schema — stop and require fresh generation, without
passing the incompatible Manifest as an amendment input. Never translate,
migrate, or partially preserve it, and offer no migration path.

Otherwise change only what the amendment reaches, and leave the whole file
reading as current state (`SKILL.md` → *Write the current state*).

- **Replace, don't add.** Delete what the amendment replaces rather than keeping
  it beside the new text, and replace a Known Assumption it supersedes rather
  than adding a second. A deleted item's ID is retired, never reused, and nothing
  is renumbered. Items the amendment does not touch keep their text and IDs,
  except that anything *Write the current state* excludes is removed wherever it
  sits: removing it changes no requirement. The decision such text records,
  where it still holds, moves, undated, into Known Assumptions — a `User's call:` entry when the user
  made it — unless an entry already records it. Then search the Manifest for each
  deleted ID and resolve every reference to it.
- **Reconcile the frame, not just the leaves.** An amendment that widens scope or
  changes a stated rule leaves Intent, the Architecture, the order rationale and
  any scope-bounding guidance describing the older, smaller task — and they read
  as unaffected precisely because nothing is editing them. Re-read them against
  what the manifest now covers, and re-read existing gates for under-coverage
  over the widened area.
- **An instance report locates the missed obligation.** Ask which claim should cover it,
  then distinguish a claim drawn too narrowly from an inadequate evidence method or an
  evaluation that missed evidence. Repair that part in place. Broaden the claim only when
  its region was too narrow; do not add a sibling criterion for each reported instance.
- **A changed decision needs adequate coverage.** Check the behavior and obligations the
  change affects. Update an existing claim or its Evidence where it already covers them;
  add a criterion only for an uncovered result. A revisable design choice stays in the
  Approach or Evidence rather than becoming an acceptance end merely because it changed.

An amendment from an unattended executor is unattended: self-answer within the
caller's delegation, ask no questions, and wait for no approval. A working claim or evidence
method can change on evidence that the replacement better serves the unchanged Outcome and
hard requirements. Identify what the old check got wrong, the replacement's basis, and what
evidence must be refreshed. A failed check alone does not justify changing it. Overall plan
approval is not a reason to block this correction. A hard claim changes only with authority
from its source; a missing rationale never makes it working. Validate a
delegated Appetite revision before applying it: the broader work serves the
requested outcome, its benefit justifies the added complexity and maintenance,
it has not already been done as excess, and it crosses no explicit exclusion or
hard requirement. Preserve those requirements unless authorized steering explicitly
changes them. A request outside that delegation returns an evidenced blocker
without changing the Manifest.
