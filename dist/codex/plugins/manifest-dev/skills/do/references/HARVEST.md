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
- **Friction becomes a command:** where the run had to start something by hand or add a print to
  see its state, leave the project's verification able to do that — in its harness a control
  command or a `logs:` command, or the same in its own scripts — within the change's scope, or
  name the gap as debt. A slow check is sped up within scope or named in the report with where its
  time goes; it is never debt.
- **Suppressions:** a new suppression of a lock carries its reason on the suppressing line and is
  reported as debt. It needs no approval to land.

## A reaction to a draft

A disposable draft is a throwaway rendering made only to get a person's reaction (`../SKILL.md` →
*Autonomous execution* says how one is made). A reaction to it is not a correction: the draft was
made to be reacted to, so nothing went wrong that a check should stop. By default the reaction
steers the direction the draft was made to settle, and the design behind it, and installs no lock
and drafts no Taste entry.

Capture every reaction, whatever else it does. The direction picked and each criterion the
reaction surfaced go, through an amendment (`../SKILL.md` → *Amendments*), into the Manifest — as
gates on the real work where they bind it, and as Known Assumptions recording the person's call —
into the Ticket the work is tracked on, and into a decision record where the choice meets the
project's bar for one. They never go back into the draft, which changes again only when the person
asks for another draft.

Lock only what the reaction shows reaches past the draft:

- **A requirement or constraint on the real work** — something the built thing must do whatever
  it looks like — is an invariant the person stated: take it through the harvest above, at the
  strongest rung that holds it. Lock it where the run holds real work a check can cover; until
  that work exists, capture it as that work's requirement, and the run that builds it locks it.
- **A personal lean the person states as reaching beyond this artifact, with a reason**, is
  drafted as a Taste entry for their yes, the way `../SKILL.md` → *Taste on reversal* describes,
  whether or not it reverses a call this run made. A lean with no stated reason is captured only.

When it is unclear whether a reaction reaches past the draft, capture it and do not lock it or
draft a Taste entry: a missed lock costs one later correction, while a wrong one binds every later
contributor to a rule nobody meant.

Three reactions to a dashboard draft:

- "Go with B, but less dense." Direction only: the Manifest records B at lower density as the
  person's call and the real dashboard's gate builds to it. No lock, no Taste entry.
- "These totals have to match the ledger to the cent — we've been burned before." A requirement on
  the real work: captured as a gate on the real dashboard, and locked at the strongest rung that
  holds it — here an invariant test that the totals reconcile with the ledger — once the real code
  exists.
- "In anything you mock up for me, put the numbers first — I scan for them before anything else."
  A personal lean with a reason, reaching past this draft: captured in the Manifest as the
  person's call and drafted as a Taste entry for their yes. No lock.

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
regressions the verification harness exposed; ask-first recipes the change touched and did not run; harness friction left unfixed, other than run time; a touched check, in any form, left broken or not fit to trust.

- Record each item in the execution log as it is found.
- Hand the list to `/done` or `/escalate`, which name it with the ticket-up offer.
- Every pull request the run opens or updates carries a "Debt left" section listing the same
  items, one line each — what, where, why it was left — whether anyone is watching or not. It is
  the record any runner can read later; the execution log stays on this machine.
