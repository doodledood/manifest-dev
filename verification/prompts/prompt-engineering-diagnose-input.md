/manifest-dev-tools:prompt-engineering our support assistant keeps telling customers the wrong plan. Improve this prompt so it stops.

The system prompt template; `{customer_record}` is filled in per conversation from our account service:

```text
You are the support assistant for Ledgerly, an invoicing app. Answer the customer's
question using the customer record below. Be concise and friendly. If the record is
ambiguous, use your best judgment. Never promise refunds.

<customer_record>
{customer_record}
</customer_record>
```

Three logged failures:

1. Question: "What plan am I on?"
   Answer: "You're on the Pro plan with 5 seats."
   Grader: wrong plan.

2. Question: "Can I use custom invoice branding?" (a Pro feature)
   Answer: "Yes — custom branding is included in your Pro plan."
   Grader: wrong plan.

3. Question: "Why was I charged less this month?"
   Answer: "You're on Pro, so the charge should be the same; it may be a proration."
   Grader: wrong plan; misses why the charge dropped.

Raw request logs for those three conversations, attached as exported:

```text
conv 1 | customer_record: {id: c_88213, name: Dana Ruiz, email: dana@ruizdesign.co, locale: en-US, tz: America/Denver, created: 2024-03-11, plan: Pro, seats: 5, invoices_sent_30d: 41, payment_method: card ****4412, tax_region: US-CO, support_tier: standard, billing_events: [2026-09-02 upgrade Basic->Pro, 2026-10-03 downgrade Pro->Basic], last_login: 2026-10-29, flags: [beta_reports]}
conv 2 | customer_record: {id: c_10457, name: Omar Haddad, email: omar@haddad.io, locale: en-GB, tz: Europe/London, created: 2023-07-02, plan: Pro, seats: 2, invoices_sent_30d: 9, payment_method: sepa ****0931, tax_region: GB, support_tier: standard, billing_events: [2026-08-11 downgrade Pro->Basic], last_login: 2026-10-30, flags: []}
conv 3 | customer_record: {id: c_33902, name: Li Wen, email: li.wen@lwstudio.com, locale: en-US, tz: America/Los_Angeles, created: 2025-01-19, plan: Pro, seats: 3, invoices_sent_30d: 17, payment_method: card ****7720, tax_region: US-CA, support_tier: priority, billing_events: [2026-10-01 downgrade Pro->Basic], last_login: 2026-10-31, flags: [early_access]}
```
