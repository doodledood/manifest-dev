---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Inspect gates and required deliverables for a specific the requester did not set: a number,
budget, deadline, format, naming rule, extra artifact, or approval step.

A hard specific is supported when the request deliberately requires it or an applicable rule
imposes it. Its source must state the actual obligation. An agent-derived proxy or selected
method is working, even if the overall plan was approved; it may be revised on evidence while
preserving the intended result and hard requirements. Recording a choice or citing the plan
does not make it hard. A rationale is not required for a deliberately stated user requirement.

An operational target may be advisory or a clearly revisable working claim with its rationale.
FAIL if an invented specific becomes an independent hard veto, if authority is unclear, or if
revision may excuse the intended result. A rough user aim is not an exact requirement; a firm
user target remains hard even when feasibility is unknown. Ordinary quality assessment is not
an extra product requirement. Otherwise PASS.

The request:

use the define skill for this.

the project: a python 3.12 service with pytest and a docker-compose postgres. its context file
says run `make test` (pytest) and `make typecheck` (mypy --strict) before a change is done. the
invoice sender lives in `invoices/worker.py`: one worker polls the `jobs` table, takes a pending
job, emails the invoice through the email provider's http api, and marks the job `sent`.

here's the read we agreed on earlier:

> **Read: run several workers that claim jobs atomically and make each send idempotent.**
> Invoices go out too slowly with one worker; the user wants two or three. Two failure modes
> come with that: two workers taking the same job, and a worker killed after the email went out
> but before the job was marked sent.
>
> Design: a worker claims with `UPDATE jobs SET status='claimed', claimed_by=$1,
> claimed_at=now() WHERE id = (SELECT id FROM jobs WHERE status='pending' ORDER BY id FOR UPDATE
> SKIP LOCKED LIMIT 1) RETURNING *`. It sends with the provider's idempotency key set to the job
> id, so a resend of the same job is dropped by the provider. A claim older than 10 minutes goes
> back to `pending` (a reaper query run by each worker every minute). The worker marks the job
> `sent` only after the provider returns success.
>
> A throwaway TLA+ model (3 workers, 3 jobs, a crash allowed at any step, checked with TLC)
> found two bugs in simpler variants: without the idempotency key, a crash between send and
> mark-sent followed by a reclaim sends the same invoice twice; without the reclaim timeout, a
> crashed worker's job is never sent. With both in place the model holds `NoDoubleSend` (the
> provider delivers each job at most once) and `EventuallySent` (every job is eventually sent
> once crashes stop).
>
> Assumption the design rests on: the provider keeps idempotency keys for 24 hours, longer than
> the 10-minute reclaim timeout. Confidence: high on the design within the model's bound; the
> model checks the design, not the code.

the repo and the model files aren't available to you here — plan from what's above. i'm afk,
dont ask me anything. write the spec (deliverables, acceptance criteria, and the rules that must
hold) to ./manifest.md in the current directory, not your home directory.
