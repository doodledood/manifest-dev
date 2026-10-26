---
tags: [figure-out]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 1
---
use the figure-out skill for this.

[earlier in this conversation]

me: i run a small B2B SaaS — a scheduling tool for clinics, about 400 paying customers. deciding whether to launch a cheaper "Lite" plan. help me think it through.

you: what should a Lite plan do for the business, and which aim wins if two of them pull apart?

me: revenue growth mainly. also keep costs in check, and don't overload the team. revenue is the main one. start with costs, it's simpler.

you: costs first. what would Lite change in your costs?

me: Lite is $49/mo vs Pro at $99/mo. Lite drops live chat support — email only, 48h reply. that saves us the 2 extra support people we planned to hire this year. most of our chat volume is clinics in their first month, setting up calendars and staff accounts.

you: then on costs Lite helps: email-only support for Lite clinics avoids the two planned support hires. i mark costs as: Lite wins. next: team load or revenue?

---

ok, moving on. team load is fine either way, building Lite is about 2 weeks of engineering. revenue now, and deep. our guess: Lite brings ~150 new clinics a year that Pro doesn't get, since price is the top reason in our lost deals. maybe 10% of existing Pro customers downgrade. help me figure out if revenue actually goes up.

(write any notes or logs you keep into the current directory rather than your home directory)
