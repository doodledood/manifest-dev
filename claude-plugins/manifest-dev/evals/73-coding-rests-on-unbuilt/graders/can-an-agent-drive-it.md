---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Today a developer sees a status change only by booking a real carrier shipment and waiting a day, so
neither a developer nor an agent can run the flow on demand, watch each status move, or reproduce a
stuck delivery.

**First, answer in one line:** Does the reply propose a way to drive and observe the status flow on
demand — a fake carrier or recorded carrier events replayed in local or test runs, a command that
steps a delivery through its statuses, a readable history of each delivery's moves — so it can be
debugged without a real shipment? Quote it.

**Then judge:** PASS if yes. FAIL if checking still depends on real test shipments, or the reply
mentions tests without saying how carrier events would be produced for them.
