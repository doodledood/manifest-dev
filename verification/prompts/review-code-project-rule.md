First, in this repository: write `CLAUDE.md` containing exactly this one rule:

    Every module that talks to the database uses the shared module-level `DB = Database()` instance from `db.py`; we do not inject database handles.

Commit that and a file `db.py` with `class Database:` (a `query(sql)` method that returns `[]`) and `DB = Database()` on the default branch. Then create a branch `feature/report`, and commit `report.py` containing:

    from db import DB

    def overdue_count():
        return len(DB.query("select * from loans where overdue"))

Then run /manifest-dev:review-code code-testability on that branch's change against the default branch.
