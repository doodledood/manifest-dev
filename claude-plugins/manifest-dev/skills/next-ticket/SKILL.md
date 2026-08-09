---
name: next-ticket
description: 'Read the project''s ticket store and name the single best ticket to work on now, with the reason. Use when picking up work, asking what''s next, what should I work on, or pulling the next task or ticket from the backlog.'
---

# next-ticket

Find the store, read it, name one ticket. The store follows the ticket convention (`../ticket-up/references/TICKET_CONVENTION.md` — read it if the convention isn't already in context).

**Finding the store.** Read `tickets/store-config.md` — one fixed, repo-relative location naming the venue. A GitHub-venue config means the store is that repo's issues under the efforts' tracking issues; query instead of reading files. Without that file, don't assume a venue: `tickets/<effort>/` directories mean a file store and can be read directly, but anything else needs asking which venue this project tracks work in, and the answer belongs in `tickets/store-config.md` so it's asked once. A project that keeps its store elsewhere says so in its own context file, already loaded when you run. If no store exists anywhere, say so plainly and offer the two ways one appears: `ticket-up` on a finished manifest, or writing tickets by hand under the convention.

**Choosing the effort.** A store holding several still gets an answer rather than a question back. When the conversation is already about one effort, that's the one. Otherwise enumerate the efforts from the venue itself — the `tickets/<effort>/` directories in a file store, or the effort labels attached to a single open-issues query in GitHub; no index of efforts is kept anywhere, and only efforts with open tickets can win. Start in the one already in flight — holding a claimed ticket, or one closed recently — because finishing beats starting, and this needs nothing written down. With nothing in flight, read each front file's destination and judge which effort matters most now; the convention's rule ranks tickets inside an effort, but its impact term is measured against that effort's own destination, so it cannot rank efforts against each other. Say which effort you picked and why, so one word redirects it. A store wanting a reproducible order states one in its store config; absent that line the pick is derived.

**The read.** Read only the open set — the effort's ticket directory (never its `done/` archive), or the tracker's open-issue query — plus the front file for the destination and any priority override; closed history costs nothing. Ready tickets only — open, unclaimed, all dependencies done. Order them by the store's stated priority rule, or the convention's default: urgent → unblocking → impact → cheap, with impact measured against the front file's destination when one exists. Name the single top ticket: its title, kind (shaped means build it; question means figure it out first), and a one-line why-this-one grounded in the rule that put it on top.

**Then offer, don't act.** Offer to claim it for the user (write `Claimed by:`, assign the issue), and — by kind — to start executing a shaped ticket or open a figure-out session for a question ticket. Picking is this skill's whole job; working it is the user's call.

**When nothing is ready** in the effort you picked, try the next effort by the same judgment before reporting — nothing ready means nothing ready anywhere, and say which efforts you looked through. Then say exactly why: every open ticket blocked (name the blocking edges), everything claimed (name by whom), or the store is empty. A blocked-only store usually means the thing to do is finish or tidy something in flight — say which ticket closing would free the most.

## Gotchas

- Surface a claimed ticket that looks abandoned ("claimed by X, untouched; a tidy pass could release it") and leave the reassignment to a person.
- Rank by the priority rule — it is the contract, and the why-line cites it.
