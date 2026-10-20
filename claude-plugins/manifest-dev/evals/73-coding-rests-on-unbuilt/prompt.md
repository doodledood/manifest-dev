---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

we run a courier app for local shops. customers want live delivery status on the tracking page — picked up, in transit, out for delivery, delivered — without refreshing. the plan is to use the carrier's push events so the page updates the moment a parcel moves. i haven't asked the carrier about that yet; their api docs only describe a `GET /shipments/{id}` endpoint. today the status is set by if/else branches in four places: `dispatch.py`, `scan_webhook.py` (our own warehouse scanners), `driver_api.py` and the nightly `reconcile.py` job, each overwriting one `status` column on `deliveries`. ops also wants returns, where a delivered parcel goes back to in transit; product hasn't decided whether that's allowed. when a status gets stuck today, we hear about it when the customer phones support, about 25 calls a week. to see a status change locally, a developer books a real test shipment with the carrier and waits a day. figure out what this feature should be so we can hand it to /define next. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
