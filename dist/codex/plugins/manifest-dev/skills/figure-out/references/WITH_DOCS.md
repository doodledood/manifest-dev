# figure-out: --with-docs

Loaded when `--with-docs` appears in args. Adds three behaviors to figure-out: **bootstrap** (initialize CONTEXT.md if missing), **inline glossary captures** (write project vocabulary as terms surface), and **ADR offers** (record decisions worth keeping). Without the flag, this file isn't read.

## Override: these writes ARE the action

The master frame in `SKILL.md` says: *"Clarifying answers feed exploration, not action. Don't leap to the implied move — not the edit, not even the proposal."*

In `--with-docs` mode that frame has two explicit exceptions. **Glossary captures and ADR offers are not deferred work — they are the action of this mode.** Execute them inline as they trigger. Do not batch to the end of the session. Do not wait for the user to ask. The writes are the deliverable; the deferred-action posture does not apply to them.

(The default figure-out posture still applies to everything else — design proposals, code edits, plan synthesis. Only glossary writes and ADR offers carve out.)

## Bootstrap (at session start)

Before pressing the topic, check the documentation surface:

1. **`CONTEXT.md` at repo root** — if it exists, load it as evidence. Project vocabulary is a source the user is already working from.
2. **No `CONTEXT.md`** → propose minimal initialization: *"No CONTEXT.md exists for this repo. Want a minimal scaffold I can grow as terms resolve?"* On accept, write a starter file (project name, one-sentence purpose, empty Language section). On decline, skip the proactive scaffold and don't re-offer it — but subsequent per-turn glossary captures may still create `CONTEXT.md` lazily on first resolution. (The user opted into docs by passing `--with-docs`; declining the scaffold only declines the *proactive* write, not the inline captures that the flag exists for.)
3. **`CONTEXT-MAP.md` at root** → the repo has multiple contexts. Follow the map to the relevant context's `CONTEXT.md`. Ask which context if unclear.
4. **Multiple distinct domains emerge mid-session** → propose splitting via `CONTEXT-MAP.md` + per-context `CONTEXT.md`. Don't do this preemptively; only when the conversation actually crosses domain boundaries.

## Glossary captures (per-turn, inline, no offer)

**After every user response**, check for these signals:

- **A noun got defined** — user used a domain term and stated what they mean by it.
- **A clash with the existing glossary** — user's term conflicts with an existing `CONTEXT.md` entry.
- **A fuzzy term got canonicalized** — agent or user proposed a canonical name for an overloaded term and it stuck.

If any of these fires → **write to `CONTEXT.md` before asking the next question. No offer, no batch.** Capture as it happens. Create `CONTEXT.md` lazily on the first resolution if it doesn't exist (per Bootstrap above).

When the user's term conflicts with the existing glossary, surface the clash as a lead: *"Glossary defines X as A; you seem to mean B — which is it?"*

When the user uses a fuzzy or overloaded term, propose a canonical one: *"'Account' — Customer or User? Different things."* The user's articulation, not your inference, disambiguates.

## ADR offers (two-pass capture)

The ADR gate, format, lifecycle, immutability discipline, and cross-reference rules live in the adjacent **`ADR_FORMAT.md`** — read it. This section only covers *when and how to offer* during a figure-out conversation.

### Pass 1 — per-turn (high-confidence)

**After every user response**, check the ADR gate (see `ADR_FORMAT.md`: category match + Decision Test + anti-patterns). When the gate fires *clearly* on a decision just articulated — user chose B over A with explicit reasoning, a scope boundary just got drawn, a key constraint just got named — **offer immediately**:

> *"This looks ADR-worthy — [name the category and the Decision Test result]. Want me to record it?"*

On accept: write per `ADR_FORMAT.md` (template, MADR sections, filename `YYYYMMDD-kebab-title.md`). Capture alternatives from the conversation you just had — if the user picked B over A, that's exactly what goes in the Alternatives Considered section. If alternatives weren't articulated, ask before writing: *"What did we consider and reject? I want to capture that in Alternatives."*

### Pass 2 — session-end sweep (recall guarantee)

**Before naming the read** (or handing off to `/define`), review the session for ADR candidates that didn't trigger Pass 1. Apply the same gate. Present any survivors as a **batched offer**:

> *"Before we lock this in — these came up that look ADR-worthy: [N items, one line each: title + why]. Record any?"*

For each accepted, write per `ADR_FORMAT.md`. Skip the sweep if the conversation didn't actually produce decisions worth capturing — an empty sweep is fine.

The two-pass shape exists because per-turn alone misses subtle decisions (the gate fires only at high confidence to keep interruption low), and sweep-only loses immediacy (alternatives are freshest right after the decision is made). Both passes together = inline coverage matches what a post-hoc sweep would catch.

## CONTEXT.md format

```md
# {Context Name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
A request placed by a customer for one or more items.
_Avoid_: Purchase, transaction.

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account.

## Relationships

- An **Order** produces one or more **Invoices**.
- An **Invoice** belongs to exactly one **Customer**.

## Flagged ambiguities

- "account" used to mean both **Customer** and **User** — resolved: distinct concepts.
```

Rules:

- One sentence per definition. What it IS, not what it does.
- Bold term names; list aliases under `_Avoid_:` when multiple words competed.
- Show cardinality in Relationships when load-bearing.
- Project-specific vocabulary and conceptual relationships only — no architecture, file paths, code structure, or design decisions. Implementation belongs in ADRs.

## Multi-context repos

If `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map lists each context's path and inter-context relationships; each context's `CONTEXT.md` lives in its module with context-specific ADRs alongside.

When multiple contexts exist, infer which one the current topic belongs to. Ask if unclear.
