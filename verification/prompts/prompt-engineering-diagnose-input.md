/manifest-dev-tools:prompt-engineering our support assistant keeps telling customers the wrong plan. Improve this prompt so it stops.

The system prompt template, with `{customer_record}` filled in per conversation:

```text
You are the support assistant for Ledgerly, an invoicing app. Answer the customer's
question using the customer record below. Be concise and friendly. If the record is
ambiguous, use your best judgment. Never promise refunds.

<customer_record>
{customer_record}
</customer_record>
```

Three logged failures, each with the record as it was filled in:

1. Question: "What plan am I on?"
   Record: `name: Dana Ruiz` · `plan: Pro` · `seats: 5` · `billing_events: [2026-09-02 upgrade Basic→Pro, 2026-10-03 downgrade Pro→Basic]`
   Answer: "You're on the Pro plan with 5 seats."
   Grader: wrong — the customer is on Basic.

2. Question: "Can I use custom invoice branding?" (a Pro feature)
   Record: `name: Omar Haddad` · `plan: Pro` · `seats: 2` · `billing_events: [2026-08-11 downgrade Pro→Basic]`
   Answer: "Yes — custom branding is included in your Pro plan."
   Grader: wrong — Basic does not include branding.

3. Question: "Why was I charged less this month?"
   Record: `name: Li Wen` · `plan: Pro` · `seats: 3` · `billing_events: [2026-10-01 downgrade Pro→Basic]`
   Answer: "You're on Pro, so the charge should be the same; it may be a proration."
   Grader: wrong — the downgrade explains the lower charge.
