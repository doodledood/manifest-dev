# Upgrading a project from v6: what v7 gives it

A project recording v6 may keep the harness or verify its own way. v7 changes only a kept
harness: it commits no evidence and keeps no status, and each timed scenario's time line moves
from its latest evidence into its recipe, where only the change that changes that check moves it.
A project whose verification bullet names its own way gets none of these items.

Find the harness's directories through the project's own tool before offering anything, never by
assuming the default `verification/` paths: `verify --help` names the recipes directory,
`verify help RECIPE` names each scenario's latest evidence file, and the path lines at the top of
the project's `verify.mts` (or what its port uses in their place) say where the evidence directory
is. Every item below acts on those paths.

Offer, each as its own item and as a default the project may adapt or decline where its own way
already does the job. Item 1 goes first, before the tool update and before any evidence is
removed, since the evidence is where the lines are read from:

1. **Time lines into recipes** — for each scenario whose latest evidence summary carries a line, a
   `- **Line:** <kind of machine> <seconds> s; …` field in its header (the project's current
   `verify help RECIPE` shows it too), one `Line: <seconds> s on <kind of machine>` under that
   scenario in its recipe, one per kind of machine, per `../VERIFICATION_HARNESS.md` → *Run
   time*. A raise keeps its reason as `; raised: <reason>`, a freeze keeps its level and Ticket
   as `; frozen at <seconds> s by <Ticket>`, and nothing else in the field is carried: `first
   run`, `lowered` and `paid down` say only how the line got there, and a count of crossings
   (`over N`) is dropped because the new tool confirms a crossing within one drive. A scenario
   with no line, or with `Workload: varies`, gets none. Show the lines written; where no summary
   carries one, say there were none to move.
2. **The tool update** — the shipped `../harness/verify.mts` (and `verify` entry) shown as a
   difference from the project's own copy, keeping its path lines and its customizations, per
   `../VERIFICATION_HARNESS.md` → *The parts*: it reads lines from recipes and writes them only
   through `verify line`, `raise` and `freeze`, keeps no status (`judge` goes), and has git ignore
   the evidence directory. A ported tool gets the same behavior in its own language.
3. **Committed evidence removed** — after item 1, every file git tracks under the evidence
   directory is removed from the repository (`git rm -r --cached` leaves this machine's copies in
   place), and the directory is ignored: the updated tool writes its own ignore file there on its
   next run, and where the tool was not updated the project's `.gitignore` lists the directory.
   Confirm with `git check-ignore` on a file there before calling it done.
4. **Lines that tell runs to commit evidence** — each line that tells a run or a contributor to
   commit its evidence, or to read a recipe's status, rewritten so runs report what a drive found
   and leave its evidence uncommitted: in the project context file, in the harness's settings file
   and recipes, and in the contributor docs the context file or the harness points to, such as a
   pre-submission checklist. Search those files for it rather than reading only the context file.
   The verification bullet keeps its newest wording from `../NORTH_STAR_FORMAT.md` → *The
   project-surfaces section*, which v7 leaves unchanged. Show each line before and after, wherever
   in its file it sits.
