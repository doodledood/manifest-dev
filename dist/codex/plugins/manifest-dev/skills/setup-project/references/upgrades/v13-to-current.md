# Upgrading a project from v13: what v14 gives it

Offer the applicable changes separately, comparing with the project's own wording before replacing
anything.

1. **A deleted or retargeted draft gives back what it changed:** add the sentence that follows the
   draft rule in `../../../figure-out/references/ADR_FORMAT.md` → *Immutability* to the same place in
   the project's `docs/adr/CONVENTIONS.md`. Where a record's Status in the project names a record
   that does not exist, or one that does not name it back, show it beside this item: it is a
   restatus a deleted or retargeted draft left behind, and the person decides whether the record
   gets its earlier Status back.
2. **The tool update**, for a project that keeps the harness: the shipped `../harness/verify.mts`
   shown as a difference from the project's own copy, keeping its path lines and customizations,
   per `../VERIFICATION_HARNESS.md` → *The parts*. A scenario keeps the summary of the run that
   finished last, and `help` reports that one, however two drives overlapped. A ported tool gets
   the same change in its own language. A project whose verification bullet names its own way
   gets none of this.

Record the newest surfaces version only after each applicable offer has an answer, as the setup
skill specifies.
