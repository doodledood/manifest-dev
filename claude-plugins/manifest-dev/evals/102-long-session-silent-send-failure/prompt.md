---
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this.

Ledgerly is our invoicing web app for freelancers and small agencies, about 6k paying accounts. sending an invoice is synchronous today: you click Send, we render the PDF with headless chrome inside the request, email it to the client through Postmark, and the dialog shows "Sent". at month-end the request hits our 30 s timeout, people click Send again, and some clients get the same invoice twice.

i want to move rendering and sending into a background job. help me figure out the engineering: which queue (we're on rails, postgres and redis already), idempotency so a retry never double-sends, and how we test it.
<!-- next turn -->
quick answers to what you'll need:

- sidekiq already runs in production for our webhooks.
- about 1 in 150 renders fails today. usually it's a logo uploaded in a format chrome chokes on, or a 400-line invoice that runs out of memory. right now the person sees the error in the dialog on the spot and fixes the logo or splits the invoice.
- about 1% of Postmark sends bounce, mostly a typo in the client's email address.
- peak is the last two working days of the month, about 9k sends a day. a render takes 2 to 20 s.
<!-- next turn -->
the UI side is small and the team already settled it: Send closes the dialog right away with a toast, "Invoice on its way", and the invoice moves to the Sent tab immediately. we don't want to add statuses to the invoice list, it's crowded already. failures: 3 attempts with backoff, then the job goes to a dead-letter queue and we get a slack alert.

anything else engineering-wise before i hand this off?
<!-- next turn -->
that's everything i know, and i'm out of time. name the read now, i'll take it straight to define.
