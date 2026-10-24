---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Before committing to implementation, the read must reason about the states and orders in which
two workers claim one job and a worker crashes after sending but before marking sent. PASS if
it proposes a concrete check capable of reaching those orders and states the properties it
would test: no duplicate invoice and no invoice silently left unsent. Controlled schedules,
generated event sequences, a small simulation or a model checker can qualify. FAIL if it goes
straight from a proposed design to ordinary happy-path tests, or merely names modeling without
saying what it would settle. Exhaustive model checking is not required when a cheaper adequate
check reaches the relevant counterexample.
