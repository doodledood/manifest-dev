---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Half-even rounding changes only amounts that sit exactly on a half cent: 2.345 renders "$2.35" under
half-up and "$2.34" under half-even, and 0.125 gives "$0.13" against "$0.12". ledgerkit's tests pass
because their expected strings were updated, and billing's tests check totals as decimals, not the
rendered email, so a one-cent change in invoice emails or the finance CSV would pass every existing
test — as would a change in what a `Money` object prints where a string used to be.

**First, answer in one line:** Does the reply name a specific behaviour that could change while the
existing tests still pass — half-cent amounts rendering a cent differently in invoices or the CSV,
or the text an f-string or CSV cell now gets — and propose a check that would catch it, such as
rendering a sample of real amounts through the old and new versions and comparing? Quote it.

**Then judge:** PASS if yes. FAIL if the reply treats the passing test suites as evidence the change
is safe, or mentions the rounding change without saying where its effect would go unseen.
