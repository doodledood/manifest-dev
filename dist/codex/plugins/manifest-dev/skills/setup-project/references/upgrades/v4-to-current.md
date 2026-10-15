# Upgrading a project from v4 to v5

A project recording v4 already has a verification harness. v5 makes it control what it checks,
hold check run time against creep, keep one summary per scenario, find what a diff touches, and
narrow the ask-first mark to cost.

Offer, each as its own item:

1. **The tool update** — the shipped `../harness/verify.mts` (and `verify` entry) shown as a
   difference from the project's own copy, so its customizations stay visible; a ported tool gets
   the same commands and evidence fields described in `../VERIFICATION_HARNESS.md` → *The parts*.
   Older evidence keeps its status; the next run of each scenario leaves one summary, and a
   fixed-workload scenario starts its time line.
2. **Control commands**, per `../VERIFICATION_HARNESS.md` → *The parts*: `start`, `running`,
   `logs`, `reset` and `stop` declared in `harness.md` where the project's existing scripts already
   start, observe or stop what it runs, each on the run's `VERIFY_RUN_ID` in place of a fixed data
   directory or port; none where the project runs nothing.
3. **Ask-first marks given for run time** — each recipe whose `ask-first` reason is run time
   alone, offered for removal of the mark; a mark whose reason names cost stays.
4. **Scenarios whose work varies** — an agent session, a document walk, the affected tests — get
   `Workload: varies`, per `../VERIFICATION_HARNESS.md` → *Time lines*, so ordinary run-to-run
   variation never reads as creep.
5. **The context-file bullet** — v5's wording from `../NORTH_STAR_FORMAT.md` → *The
   project-surfaces section*: unmarked recipes are free to run as often as they help, and the
   ask-first reason is cost, never time.

Once every item has an answer, record v5.
