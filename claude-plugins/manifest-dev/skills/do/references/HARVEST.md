# do: corrections become locks, and debt stays visible

## The harvest

At each repaired finding, each fixed defect and each correction, ask which check, type or structure would have made
the first version right, and install it where one exists — a lock, so the corrected kind of
mistake fails for every later contributor, with or without this workflow.

- **Strongest rung first:** a type or structure that makes the wrong code fail to compile; a
  lint or architecture test whose error names the fix; an invariant test that states a
  property; one owning site every caller goes through. Prose alone is no lock.
- **The bar:** the class fits one sentence that does not name this case; the lock fails on the
  original mistake (revert the fix and watch it fail); it checks structure rather than a count.
- **Two routes:** an invariant the owner states may be locked on its first occurrence. An
  observed mistake needs a class behind it; "one-off: <why>" is a valid outcome.
- **Intent first:** before locking a stated intent, check it against the project's decision
  records and its current practice. A conflict is raised, not locked.
- **Scope:** every lock declares its scope — production code only, a date cutoff, generated code
  excluded. Where hits inside that scope stay unfixed because fixing them is gigantic, the lock
  fails only when a change adds more. Noisy hits across the repository mean the scope or the rule is wrong, not that the hits
  are debt.
- **Across the repository:** run the lock everywhere and fix its hits on this pull request, in a
  commit of their own; report a cleanup instead only when it is gigantic, as `../SKILL.md` →
  *What holds for every gate* defines it. A lock local to the fix ships with it.
- **The record:** where a decision record's decision is what the lock holds, update the record's
  `Enforced by` line, and give the check a comment citing the record.
- **Friction becomes a command:** where the run had to start something by hand, add a print to
  see its state, or wait on something slow, leave the project's verification able to do that — in
  its harness a control command, a `logs:` command or a faster check, or the same in its own
  scripts — or, where that is gigantic, name the gap as debt.
- **Suppressions:** a new suppression of a lock carries its reason on the suppressing line and is
  reported as debt. It needs no approval to land.

## Comments in touched code

These hold for code the change touches. A comment that only a fix on the way or a repair passes
joins only as `../SKILL.md` → *What holds for every gate* says.

- A comment that explains a workaround in code the project owns is a refactor flag: reshape the
  code so the workaround is no longer needed, and delete the comment. Where the reshape is
  gigantic, report it as debt, naming the symbol to reshape, and leave the comment in place.
- A comment that claims a constraint — "do not remove", "do not change" — gets encoded: add the
  type, test or lint that holds it, then delete the comment. Where encoding it is gigantic, report
  the check that would hold it as debt.
- A comment about something the project cannot change — an external dependency, platform or
  protocol — stays.

## The debt the run leaves

Debt is what the run found and could not fix on its pull request: each gigantic item, as
`../SKILL.md` → *What holds for every gate* defines it — lock hits, a reshape, a constraint to
encode, harness friction, a drifting recipe or a check that runs and passes but is not fit to trust,
whose fix is a project of its own — with why; new suppressions; ask-first recipes the change touched
and did not run, and anything else that needs access, authority or a decision a person retains,
naming what it needs; and a time-line overshoot frozen under a debt Ticket. A failing check across
the whole tree, or one a gate rests on, whose fix is gigantic is a blocker, never debt. The
pre-existing issues the work met that are not gigantic, and below-bar findings, are fixed, applied
or dismissed with a reason, never debt.

- Record each item in the execution log as it is found.
- Hand the list to `/done` or `/escalate`, which name it with the ticket-up offer.
- Every pull request the run opens or updates carries a "Debt left" section listing the same
  items, one line each — what, where, why it was left — whether anyone is watching or not. It is
  the record any runner can read later; the execution log stays on this machine. The description
  also lists the issues fixed on the way, each its own commit, and any test removed as useless or
  tautological, with why.
