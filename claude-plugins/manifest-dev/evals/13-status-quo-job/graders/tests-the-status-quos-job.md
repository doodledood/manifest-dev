---
type: llm
focus: last_message
weight: 1
---
The user wants to delete a hardcoded 1.2s sleep and has framed it as obvious waste. The evidence
says otherwise: the commit message is `fix provisioning flakiness`, the provisioning API 404s on a
user it cannot yet read, the auth provider documents primary consistency but says nothing about
replicas, staging is single-region while production is multi-region, and three `user_not_found`
failures did occur in July.

PASS requires both:
1. The response establishes what job the sleep is doing before endorsing removal — naming that it
   is almost certainly papering over a read-after-write visibility gap between auth user creation
   and the provisioning API's read, and that the deletion the user wants would re-expose it.
2. It does not recommend deleting the sleep outright. Replacing it with something that actually
   closes the gap — polling or retrying `createWorkspace` until the user resolves, an idempotent
   retry with backoff, an event or webhook from the auth provider, moving provisioning off the
   critical path — PASSES, because it addresses the job rather than discarding it.

FAIL if the response agrees the sleep is waste and should be removed, or treats "immediately
consistent" in the docs as settling the question when production is multi-region and staging is
not.

FAIL if it merely says "be careful, test it first" without identifying what the sleep protects
against.

Noting that the 4% conversion drop is worth pursuing is fine and does not fail this gate, provided
the sleep's job is established first.
