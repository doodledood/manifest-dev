# figure-out: --with-docs

Loaded when args contain `--with-docs`. Adds glossary and ADR persistence; without the flag, this file isn't read and default figure-out applies.

## Glossary probe

Before discussing code or domain, read the project's vocabulary. If `CONTEXT.md` exists at the repo root, load it. If `CONTEXT-MAP.md` exists at the root, follow it to the relevant context's `CONTEXT.md`. Project vocabulary is evidence — load it like any other source the user is working from.

When the user's term conflicts with the existing glossary, surface the clash as a lead. *"Glossary defines X as A; you seem to mean B — which is it?"*

When the user uses a fuzzy or overloaded term, propose a canonical one and ask. *"'Account' — Customer or User? Different things."* The user's articulation, not your inference, disambiguates.

When a term resolves, update `CONTEXT.md` inline — no offer, no batch. Capture as it happens. Create the file lazily on the first resolution.

## ADR offers

ADRs are heavier than glossary entries. Offer one only when all three fire:

1. **Hard to reverse** — changing the call later carries meaningful cost.
2. **Surprising without context** — a future reader will wonder why it was done this way.
3. **Result of a real trade-off** — genuine alternatives existed; one was picked for specific reasons.

When the gate fires, offer — don't write. *"This looks ADR-worthy: hard-to-reverse, surprising, real trade-off. Want me to record it?"* On accept, write to `docs/adr/{NNNN}-{slug}.md` with the next sequential number. Create `docs/adr/` lazily on the first ADR.

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
- Project-specific concepts only.

## ADR format

`docs/adr/{NNNN}-{slug}.md` with sequential numbering.

```md
# {Short title of the decision}

{1 to 3 sentences: context, decision, why.}
```

That's the default. Optional sections only when they earn their place: Status (`proposed | accepted | deprecated | superseded by ADR-NNNN`), Considered Options, Consequences.

## Multi-context repos

If `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map lists each context's path and inter-context relationships; each context's `CONTEXT.md` lives in its module with context-specific ADRs alongside.

When multiple contexts exist, infer which one the current topic belongs to. Ask if unclear.
