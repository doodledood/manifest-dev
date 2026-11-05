/manifest-dev-tools:write-goal turn this manifest into a goal i can paste into the goal field. one amendment, settled: we're dropping the CSV export entirely — JSON export only.

````markdown
# Definition: Usage export API for workspace admins

## 1. Intent
- **Outcome:** Workspace admins can export accurate usage for internal billing and use it from the documentation.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
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

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the work adds nothing beyond what the Deliverables and the other gates require.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

### INV-G2 — No change to billing

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the diff touches no file under `billing/` and no billing table schema.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

### INV-G3 — No new datastore

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the diff adds no database, cache or queue dependency and no migration that creates a
table.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

### INV-G4 — Only workspace admins can export

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_auth.py` passes: a request from a non-admin member, a
member of another workspace, and an anonymous caller each get 403 or 401, and an admin gets 200.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

### INV-G5 — The suite passes

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `make test` exits 0 on the head commit.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

### INV-G6 — No secrets in the repo or the PR

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the diff, commit messages and pull request text contain no token or credential value.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

### INV-G7 — Code review

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the `review-code` skill on the diff reports no finding of High severity in the bugs,
design or maintainability dimensions.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

### INV-G8 — Off until flagged

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the endpoint returns 404 for a workspace without the `usage_export` flag and works for
one with it, as `pytest tests/usage_export/test_flag.py` asserts.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

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

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_range.py` passes: a request with `from` and `to` returns
exactly the days in that closed range, and a range longer than 366 days returns 400.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.2 — Totals match billing

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_totals.py` passes: for every seeded month, the sum of
exported `units` per meter equals the invoiced units for that meter to the unit.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.3 — JSON shape

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_json.py` passes: the body is a JSON array of objects
with exactly the keys `date`, `meter`, `units`, `unit_price_cents`, in that order.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.4 — CSV shape

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_csv.py` passes: a header row `date,meter,units,unit_price_cents`
and one row per day and meter, RFC 4180 quoting.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.5 — Streams large exports

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_stream.py` passes: exporting the 1-million-row fixture
keeps the worker's peak memory growth under 64 MB, measured by its `tracemalloc` snapshot, and returns the first byte before the
whole result is read.

Why: admins of large workspaces export a year at once.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.6 — Rate limited

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_rate.py` passes: a workspace's eleventh export within
one hour gets 429 with a `Retry-After` header.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.7 — Errors are actionable

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when every 4xx the endpoint returns carries a JSON body naming the problem and the field or
header at fault, as `test_range.py`, `test_auth.py` and `test_rate.py` assert.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.8 — Audit logged

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when each successful export writes one `usage.export` audit event with the admin's user ID,
the workspace ID and the range, as `pytest tests/usage_export/test_audit.py` asserts.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.9 — Large results page

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_paging.py` passes: a result over 100,000 rows returns
its first 100,000 and a `Link` header with `rel="next"`, and following every link returns each row
exactly once.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.10 — Filter by meter

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_filter.py` passes: a repeated `meter` parameter limits
rows to those meters, and an unknown meter name returns 400 naming it.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.11 — Response headers

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_headers.py` passes: every 200 carries
`Content-Type: application/json; charset=utf-8` and `Cache-Control: private, no-store`.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.12 — Deleted meters still export

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `pytest tests/usage_export/test_deleted.py` passes: rows for a meter deleted inside the
range still export, under the name the meter had on each day.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-1.13 — Fast enough for the dashboard link

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `make bench-export` reports a p95 under 800 ms over 200 requests for a 31-day export
of the 50-meter bench workspace.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

### Deliverable 2: The docs page

#### AC-2.1 — An admin can export from the docs alone

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when a reader with only the docs page and an admin token runs a working export of last
month's usage on the first try, judged by following the page step by step against a dev server.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-2.2 — The page states the limits

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the page states the 366-day range limit, the hourly rate limit of ten exports, and the
UTC day boundary.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-2.4 — Copyable examples

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the page carries one `curl` example and one Python example, and each, run exactly as
shown against a dev server with an admin token, returns a 200.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-2.3 — The page reads well

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the `review-writing` skill in the docs register reports no Medium or higher finding on
the page.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

### Deliverable 3: The pull request

#### AC-3.1 — The pull request shows it working

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the pull request's description shows the test output on the head commit and a sample
JSON export from a dev server.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-3.3 — Changelog

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when `CHANGELOG.md` gains one line under `Unreleased` naming the endpoint.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.

#### AC-3.2 — Not deployed

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the work stops at a ready pull request: nothing is merged or deployed.
Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
````
