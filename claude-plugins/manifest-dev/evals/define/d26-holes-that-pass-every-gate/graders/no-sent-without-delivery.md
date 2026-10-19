---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The design: several workers claim invoice jobs, send each through an email provider with the
provider's idempotency key set to the job id, and mark the job `sent` only after the provider
returns success. A provider that has already seen a key can answer a repeat without delivering
anything: it may report the earlier request as still in progress, return the stored answer of the
earlier attempt, or refuse the request. An implementation can read such an answer as success.

Trace this path against the spec's gates — every acceptance criterion, invariant, or other check
that must pass before the work counts as done:

1. A worker sends job J. The provider fails, or the worker learns nothing about the outcome.
2. J is sent again with the same key, by the same worker on retry or by another after a reclaim.
3. The provider answers the repeat without delivering the invoice.
4. The worker marks J `sent`. No invoice was ever delivered.

PASS if at least one gate would fail an implementation that behaves this way: for example, a gate
that a job is marked sent only on a provider answer that confirms delivery, a gate that each kind
of repeated-key answer maps to a stated outcome, or a required test that drives a retry after a
failed or unknown send and checks that exactly one invoice is delivered. Also PASS if the spec
names this path and records it as a decided, accepted risk. FAIL if every gate lets it through.
