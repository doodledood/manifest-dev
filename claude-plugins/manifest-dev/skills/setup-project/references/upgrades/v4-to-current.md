# Upgrading a project from v4: what v5 gives it

A project recording v4 already has a verification harness. v5 makes the harness optional, so the
project may keep it or set it aside for its own way of verifying; set aside, its files stay or go
as the user says, since the own-way bullet, not the files, records the choice. A kept harness
controls what it checks, holds check run time against creep, finds what a diff touches, and
narrows the ask-first mark to cost.

Offer, each as its own item and as a default the project may adapt or decline where its own way
already does the job. The harness is recommended, but the project may opt out of it whole and keep
its own way of verifying: then offer none of the harness items, and offer instead the own-way form
of the verification bullet from `../NORTH_STAR_FORMAT.md` → *The project-surfaces section*, naming
its commands and steps, so no figure-out, define or do run builds or offers one:

1. **The tool update** — the shipped `../harness/verify.mts` (and `verify` entry) shown as a
   difference from the project's own copy, so its customizations stay visible; a ported tool gets
   the same commands described in `../VERIFICATION_HARNESS.md` → *The parts*.
2. **Control commands**, per `../VERIFICATION_HARNESS.md` → *The parts*: `start`, `running`,
   `logs`, `reset` and `stop` declared in `harness.md` where the project's existing scripts already
   start, observe or stop what it runs, each on the run's `VERIFY_RUN_ID` in place of a fixed data
   directory or port; none where the project runs nothing.
3. **Ask-first marks given for run time** — each recipe whose `ask-first` reason is run time
   alone, offered for removal of the mark; a mark whose reason names cost stays.
4. **Scenarios whose work varies** — an agent session, a document walk, the affected tests — get
   `Workload: varies`, per `../VERIFICATION_HARNESS.md` → *Run time*, so ordinary run-to-run
   variation never reads as creep.
5. **The context-file bullet** — the newest wording from `../NORTH_STAR_FORMAT.md` → *The
   project-surfaces section*, which says unmarked recipes are free to run as often as they help
   and gives cost, never time, as the ask-first reason.
