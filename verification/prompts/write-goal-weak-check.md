/manifest-dev-tools:write-goal turn this read into a goal:

**Read: make `export` stream rows to the output file instead of loading the whole table into memory first.** Confidence: high.

What it will be: `reports export <table> <file>` writes rows to the file as it reads them from the database cursor, so memory stays flat however large the table is. The output file stays byte-for-byte the same as today's.

How it will be checked: `make test` passes.

Scope: only `reports/export.py`. No new dependency.

The work stops at a ready pull request; nothing is merged or released.

Evidence: `reports/export.py:58` calls `cursor.fetchall()` and builds the whole file in a list before writing it. The existing tests in `tests/test_export.py` export a 20-row fixture table and compare the file to `tests/fixtures/expected.csv`; `make test` passes on the current code.
