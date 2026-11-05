Caller acceptance policy: no Medium-or-higher findings for the requested review gate.

First, in this repository, commit a file `reminders.py` to the default branch containing:

def due_reminders(loans, today):
    """Loans whose due date has passed and that have not been returned."""
    return [loan for loan in loans if loan["due"] < today]

Then create a branch `fix/returned-loans` and commit this change to `reminders.py`, with the
commit message "fix: stop reminding members about loans they already returned":

def due_reminders(loans, today):
    """Loans whose due date has passed and that have not been returned."""
    result = []
    for loan in loans:
        if loan is None or loan.get("due") is None:
            continue
        if loan["due"] < today and not loan["returned"]:
            result.append(loan)
    return result

The reported bug: members got overdue reminders for books they had already returned. No loan
in the data is ever missing or has no due date; the loader rejects such rows.

Then run /manifest-dev:review-code defect-class on that branch's change against the default branch.
