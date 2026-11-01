/manifest-dev-tools:write-goal make a goal from this read:

**Read: retry failed webhook deliveries three times with backoff before marking them failed.** Confidence: high.

What it will be: when a webhook delivery gets a 5xx response or times out, the sender retries it up to three more times, waiting 1 s, 4 s and 16 s, then marks the delivery `failed`. A 4xx response is marked `failed` at once, with no retry. Each attempt is logged with the delivery ID and the attempt number.

How it will be checked: `pytest tests/webhooks/test_retry.py` passes, with tests that use a fake clock and a fake endpoint for each case above: three 5xx then success delivers on the fourth attempt; four 5xx marks the delivery failed after the 16 s wait; a 4xx marks it failed with one attempt; a timeout counts as a 5xx. `make test` exits 0.

Scope: only `webhooks/sender.py` and its tests. No new dependency and no schema change.

The change goes up as a pull request against `main`.

Ruled out: a dead-letter queue. No consumer for one exists yet.
