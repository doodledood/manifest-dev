---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Compare the request below with the spec's gates: acceptance criteria, invariants, or other
checks that must pass before completion. Account for each explicit outcome, scope boundary,
exclusion, safety rule, and retained decision. Judge the work being specified, not instructions
to the planner such as where to save this spec. Then inspect binding claims elsewhere in the spec.

FAIL if a specific requirement is missing entirely, weakened, or left only as advice or an
assumption. A broader gate may cover it in different words. Incidental implementation proposals
and a requested layer grouping are not fixed requirements unless deliberately chosen as the
outcome. Do not invent additional requirements. Problem description, rationale and optional
suggestions are not binding by themselves. A safety rule that is only partly judgeable from the
artifact may gate that part and record the remainder in an assumption naming its independent
enforcement. This narrow case preserves the rule; it does not authorize weakening it or merely
labeling it an assumption. PASS only when no such omission or weakening remains.

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
