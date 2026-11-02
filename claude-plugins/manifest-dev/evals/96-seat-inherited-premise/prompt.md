---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. i'm afk, dont ask me anything.

here's the ticket, it's shaped and ready to build. figure out the build details so i can hand it to define.

> **Ticket 212 — Referral card on the card-frozen screen**
> Status: Shaped. Product decisions settled.
>
> When a customer reports their card lost or stolen in the app, we freeze the card and show the
> "Your card is frozen" screen. Add a card to that screen: "Know someone who'd like a bank that
> acts this fast? Invite them and you both get £20." with an Invite button that opens the share
> sheet. Track impressions and invites.
>
> Open for engineering: which component renders it, how we pass the referral code, how we
> track it.

context: Kestrel is a mobile-only bank for people who mostly use it for day-to-day spending. about 1,900 customers a month report a card lost or stolen. after freezing, the same screen shows "order a replacement card" and "see recent transactions".
