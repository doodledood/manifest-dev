/manifest-dev-tools:manifest-to-goal turn this manifest into a goal i can paste into the goal field. one amendment, settled: we're dropping the CSV export entirely — JSON export only.

````markdown
# Definition: Usage export API for workspace admins

## 1. Intent
- **Problem:** Workspace admins who bill their teams internally copy usage numbers out of the
  dashboard by hand each month, and the numbers drift from what billing charged.
- **Appetite:** Medium — one authenticated export endpoint over the existing usage tables, its
  docs page, and the tests; no new storage, no change to billing.
- **Out of bounds:** INV-G2, INV-G3

## 2. Initial Approach
- **Architecture:** A `GET /v2/workspaces/{id}/usage/export` handler streams rows from the
  existing `usage_daily` table, serialized as CSV or JSON by an `Accept` header. Start with the
  JSON serializer, then add CSV.

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized
Done when the work adds nothing beyond what the Deliverables and the other gates require.
Judgment gate.

### INV-G2 — No change to billing
Done when the diff touches no file under `billing/` and no billing table schema.
Deterministic gate.

### INV-G3 — No new datastore
Done when the diff adds no database, cache or queue dependency and no migration that creates a
table.
Deterministic gate.

### INV-G4 — Only workspace admins can export
Done when `pytest tests/usage_export/test_auth.py` passes: a request from a non-admin member, a
member of another workspace, and an anonymous caller each get 403 or 401, and an admin gets 200.
Deterministic gate.

### INV-G5 — The suite passes
Done when `make test` exits 0 on the head commit.
Deterministic gate.

### INV-G6 — No secrets in the repo or the PR
Done when the diff, commit messages and pull request text contain no token or credential value.
Judgment gate.

### INV-G7 — Code review
Done when the `review-code` skill on the diff reports no finding of High severity in the bugs,
design or maintainability dimensions.
Judgment gate.

## 4. Process Guidance
- [PG-1] Write the serializer tests before the handler.
- [PG-2] Profile the streaming path with a 1-million-row fixture before tuning anything.
- [PG-3] Keep handler functions under 40 lines.

## 5. Known Assumptions
- [ASM-1] (auto) Days are UTC calendar days, matching `usage_daily` | Impact if wrong: totals
  shift by a day near midnight

## 6. Deliverables

### Deliverable 1: The export endpoint

#### AC-1.1 — Returns the requested date range
Done when `pytest tests/usage_export/test_range.py` passes: a request with `from` and `to` returns
exactly the days in that closed range, and a range longer than 366 days returns 400.
Deterministic gate.

#### AC-1.2 — Totals match billing
Done when `pytest tests/usage_export/test_totals.py` passes: for every seeded month, the sum of
exported `units` per meter equals the invoiced units for that meter to the unit.
Deterministic gate.

#### AC-1.3 — JSON shape
Done when `pytest tests/usage_export/test_json.py` passes: the body is a JSON array of objects
with exactly the keys `date`, `meter`, `units`, `unit_price_cents`, in that order.
Deterministic gate.

#### AC-1.4 — CSV shape
Done when `pytest tests/usage_export/test_csv.py` passes: a header row `date,meter,units,unit_price_cents`
and one row per day and meter, RFC 4180 quoting.
Deterministic gate.

#### AC-1.5 — Streams large exports
Done when `pytest tests/usage_export/test_stream.py` passes: exporting the 1-million-row fixture
keeps the worker's peak memory growth under the bound below and returns the first byte before the
whole result is read.

Why: admins of large workspaces export a year at once. The bound is 64 MB of peak memory growth,
measured by the test's `tracemalloc` snapshot.

Deterministic gate.

#### AC-1.6 — Rate limited
Done when `pytest tests/usage_export/test_rate.py` passes: a workspace's eleventh export within
one hour gets 429 with a `Retry-After` header.
Deterministic gate.

#### AC-1.7 — Errors are actionable
Done when every 4xx the endpoint returns carries a JSON body naming the problem and the field or
header at fault, as `test_range.py`, `test_auth.py` and `test_rate.py` assert.
Deterministic gate.

#### AC-1.8 — Audit logged
Done when each successful export writes one `usage.export` audit event with the admin's user ID,
the workspace ID and the range, as `pytest tests/usage_export/test_audit.py` asserts.
Deterministic gate.

### Deliverable 2: The docs page

#### AC-2.1 — An admin can export from the docs alone
Done when a reader with only the docs page and an admin token runs a working export of last
month's usage on the first try, judged by following the page step by step against a dev server.
Judgment gate.

#### AC-2.2 — The page states the limits
Done when the page states the 366-day range limit, the hourly rate limit of ten exports, and the
UTC day boundary.
Judgment gate.

#### AC-2.3 — The page reads well
Done when the `review-writing` skill in the docs register reports no Medium or higher finding on
the page.
Judgment gate.

### Deliverable 3: The pull request

#### AC-3.1 — The pull request shows it working
Done when the pull request's description shows the test output on the head commit and a sample
JSON export from a dev server.
Judgment gate.

#### AC-3.2 — Not deployed
Done when the work stops at a ready pull request: nothing is merged or deployed.
Deterministic gate.
````
