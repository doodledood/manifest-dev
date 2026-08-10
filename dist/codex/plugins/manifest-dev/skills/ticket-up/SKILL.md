---
name: ticket-up
description: 'Turn a finished Manifest into self-sufficient tickets anyone can pick up — a teammate, an agent, or a future session, with or without manifest-dev. Emits one plain-prose ticket per Deliverable plus explicit dependency edges, into the project''s own tracker, GitHub Issues, or files in the repo — on a venue asked once per project and recorded there. Use when splitting a manifest into tickets, delegating work, parallelizing execution, or when the user asks to ticket up, break into tickets, or create tickets from a plan.'
---

# ticket-up

Input: a manifest path. Without one, look for the most recent manifest in `~/.manifest-dev/manifests/` and confirm it's the intended one; if none exists, ask what to ticket up — a manifest is the input, so a session without one runs `/define` first.

The move: one ticket per Deliverable, plus the dependency edges between them. Each Deliverable is already a vertical slice — finishable on its own, exercisable end-to-end — so it maps to a ticket whole — split below it and the fragments could no longer be judged done. If a Deliverable is too big for one ticket, the cut is wrong in the manifest — fix it there. A one-Deliverable manifest legitimately yields one ticket.

Read `references/TICKET_CONVENTION.md` before emitting — it defines what a ticket is, its anatomy, lifecycle, and priority; the tickets you write must satisfy it.

## Translation: knowledge travels, machinery stays

The manifest is a contract between /define and /do. A ticket is a contract with a stranger who may have neither. So translate, don't excerpt: take each manifest section into the anatomy slot the convention defines for it, rewritten in the ticket's own words.

The self-sufficiency test before emitting each ticket: could a competent stranger holding only this ticket understand why the work exists, know its bounds, avoid its traps, and judge it done? Manifest-dev vocabulary appearing anywhere in a ticket is a failure of this test. The convention's anatomy plus that test settle most of the mapping. Two things they don't:

| From the manifest | Into each ticket |
|---|---|
| Global Invariants | **Rules that must hold** — copied into *every* ticket, as plain rules stripped of verification wording |
| A gate's kind, the verification mode, gate/PG/ASM codes | **Stays behind.** Executor policy, meaningless outside manifest-dev |

## The Auto grant

Decide the convention's Auto grant per ticket as you emit. Grant it only when the criterion holds — neither doing the work nor judging it done needs any human's knowledge, taste, or authority — and nothing about the ticket calls for withholding trust; when in doubt, withhold. Manifest tickets often qualify, the deciding having happened before they were written, but an approval, credentials the picker won't have, or an irreversible act keeps the grant off however settled the ticket is. Absence is safe by design — an ungranted ticket waits for a person — so a wrong withhold costs a human glance where a wrong grant costs an unattended run doing what it shouldn't.

## Dependency edges

The manifest's Deliverable order is uncertainty-based — least-proven first so one executor learns early. That order is not dependency: encode a `Depends on:` edge only where one Deliverable's outcome is genuinely required by another, and leave everything else parallel. When in doubt, leave the edge out and note the relationship under Watch out for instead.

## Where the tickets go

**The venue lives at `tickets/store-config.md`, or gets asked for once.** One fixed, repo-relative location holds it, whatever the venue turns out to be. Read it first: when it names a venue, use that and don't ask. Same for a project that keeps its store elsewhere and says so in its own context file, already loaded when you run — follow it and skip the ask. A venue someone has already named is settled, whatever it names; it isn't a recommendation to weigh against your own.

**When nothing names one, ask — and recommend the project's shared tracker.** Never choose in silence, since a run that creates a store without having asked has chosen for the user. What makes the recommendation is claiming: it is what keeps two people off one ticket, and it only does that where the store is a surface both of them read. Any hosted tracker is one, so recommend the tracker this project already runs; GitHub Issues is the one to name when the project has a GitHub remote the session can reach and nothing else is in play. Recommend files where there is no shared tracker — no remote, or work nobody else will touch — and say what choosing them costs: a file store's claims are versioned repo content, so they never cross clones, worktrees, or branches, and two sessions in separate checkouts will pick the same ticket without either noticing. Write the answer to `tickets/store-config.md` so no later run asks again.

**Files.** Write one markdown file per ticket to `tickets/<effort-slug>/NN-<ticket-slug>.md` at the project root (create it), NN ordered by a sensible starting sequence. Each file opens with `Kind:`, `Status:`, `Depends on:`, `Claimed by:` lines — plus `Auto: yes` when the grant is declared; no `Auto:` line means ungranted — then the anatomy. Write the effort's front file (`tickets/<effort-slug>/README.md`) alongside, per the convention: destination distilled from the manifest's Problem and Appetite, any priority override, context pointers — and no ticket list or status, ever. Closed tickets get moved to `tickets/<effort-slug>/done/`. Confirm the effort slug with the user when it isn't obvious from the manifest title.

**GitHub Issues.** When the config names GitHub, or the user chooses it, read `references/GITHUB_STORE.md` and follow its mapping.

**Any other tracker.** An unsupported tracker is a mapping to author, not a request to refuse. Say plainly that none ships for this one — the user should know the mapping is being written from their answers rather than shipped and exercised — then write it. Read `references/GITHUB_STORE.md` for the shape and ask what fills the same rows here: what the store and the front file are, what a ticket is, how efforts group, how kind and dependencies are expressed, what claiming is, what returns the open set, what makes a ticket ready, how closing and roll-off work, and what a tidy pass does there. Write it to `tickets/<venue>-store.md`, and have `tickets/store-config.md` name the venue and point at it rather than carry the mapping itself. Readiness is the row to get right: a store whose record never says what takeable means is a store where claiming coordinates nothing.

## After emitting

If the manifest's read named a successor question ticket — "the verdicts are in: what changed, what moves next?" — mint it now, with edges to the emitted tickets it judges: their IDs exist only at this point, which is why the read names it and this skill wires it. Offer the same when any emitted ticket's definition of done is a verdict rather than a shipped artifact (an experiment, a test, a probe): a verdict needs a judge, and the judge is a ticket, not someone's initiative.

Present the ticket list with its edges — a short table: ID, title, kind, depends-on — and where they landed. Question tickets (from figure-out handoffs or written by hand) live in the same store under the same convention; this skill emits shaped ones. The `next-ticket` skill reads any store following the convention.

## Gotchas

- The pull to keep manifest wording is strong and wrong: a gate body names evaluators and skills ("activate the review skill") — a stranger has neither. Rewrite as the check's substance ("prose reads clean to a careful reviewer; no contradictions with existing docs"). A gate's why is already context rather than requirement, so it feeds the ticket's own framing rather than its definition of done.
- Copying the invariants into every ticket feels redundant; do it anyway. The one picker who reads only their own ticket is the one the convention exists for.
- Don't emit the manifest's ceiling/scope-conformance invariant as a rule — "add nothing the tickets don't require" is meaningless to someone holding one ticket. Its substance already lives in each ticket's Scope line.
