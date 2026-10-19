---
# Holds the decision in docs/adr/20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
# The limits are double the suite's usual 900 seconds and 40 turns: besides writing the spec, the run searches it for holes, which took about 10 minutes on its own in the 2026-10-19 experiment.
tags: [define]
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
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
