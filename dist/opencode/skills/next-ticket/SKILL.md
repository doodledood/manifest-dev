---
name: next-ticket
description: 'Read the project''s ticket store and name the single best ticket to work on now, with the reason. Use when picking up work, asking what''s next, what should I work on, or pulling the next task or ticket from the backlog.'
---

# next-ticket

Find the store, read it, name one ticket. The store follows the ticket convention (`../ticket-up/references/TICKET_CONVENTION.md` — read it if the convention isn't already in context).

**Finding the store.** Check for a store config first (`store-config.md` in the ticket-up skill directory, else at a store root like `tickets/store-config.md`) — it names the venue. Without one, look for `tickets/<effort>/` directories in the project. A GitHub-venue config means the store is that repo's issues under the effort's tracking issue; query instead of reading files. If no store exists anywhere, say so plainly and offer the two ways one appears: `ticket-up` on a finished manifest, or writing tickets by hand under the convention.

**The read.** Read only the open set — the effort's ticket directory (never its `done/` archive), or the tracker's open-issue query — plus the front file for the destination and any priority override; closed history costs nothing. Ready tickets only — open, unclaimed, all dependencies done. Order them by the store's stated priority rule, or the convention's default: urgent → unblocking → impact → cheap, with impact measured against the front file's destination when one exists. Name the single top ticket: its title, kind (shaped means build it; question means figure it out first), and a one-line why-this-one grounded in the rule that put it on top. Multiple efforts with stores → ask which, or read the one the conversation is about.

**Then offer, don't act.** Offer to claim it for the user (write `Claimed by:`, assign the issue), and — by kind — to start executing a shaped ticket or open a figure-out session for a question ticket. Picking is this skill's whole job; working it is the user's call.

**When nothing is ready**, say exactly why: every open ticket blocked (name the blocking edges), everything claimed (name by whom), or the store is empty. A blocked-only store usually means the thing to do is finish or tidy something in flight — say which ticket closing would free the most.

## Gotchas

- Don't silently skip a claimed ticket that looks abandoned — surface it ("claimed by X, untouched; a tidy pass could release it") rather than reassigning on your own.
- Don't rank by what looks interesting or recent; the priority rule is the contract, and the why-line must cite it.
