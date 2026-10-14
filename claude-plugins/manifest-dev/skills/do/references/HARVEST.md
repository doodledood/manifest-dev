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
  excluded. Where hits inside that scope stay unfixed, the lock fails only when a change adds
  more. Noisy hits across the repository mean the scope or the rule is wrong, not that the hits
  are debt.
- **Across the repository:** run the lock everywhere. Fix related hits inside the change's scope;
  report a repository-wide cleanup instead of folding it into the fix. A lock local to the fix
  ships with it.
- **The record:** where a decision record's decision is what the lock holds, update the record's
  `Enforced by` line, and give the check a comment citing the record.
- **Suppressions:** a new suppression of a lock carries its reason on the suppressing line and is
  reported as debt. It needs no approval to land.

## Comments in touched code

- A comment that explains a workaround in code the project owns is a refactor flag: report it as
  debt, naming the symbol to reshape, and leave the comment in place.
- A comment that claims a constraint — "do not remove", "do not change" — gets an encoding offer:
  the type, test or lint that would hold it. Once the constraint is encoded, delete the comment.
- A comment about something the project cannot change — an external dependency, platform or
  protocol — stays.

## The debt the run leaves

Debt is what the run found and did not fix: unfixed lock hits; refactor flags; constraint
comments awaiting encoding; new suppressions; reshapes outside the change's scope; product
regressions the verification harness exposed; a new verification harness the user may remove; ask-first recipes the change touched and did not run.

- Record each item in the execution log as it is found.
- Hand the list to `/done` or `/escalate`, which name it with the ticket-up offer.
- Every pull request the run opens or updates carries a "Debt left" section listing the same
  items, one line each — what, where, why it was left — whether anyone is watching or not. It is
  the record any runner can read later; the execution log stays on this machine.
