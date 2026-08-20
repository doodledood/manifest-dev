# figure-out: docs mode

The loading layer activates this reference only after the investigation is relevant to the active project or one of its mapped contexts. It adds four behaviors from that point: **bootstrap** (load the project's conventions; initialize CONTEXT.md if missing), **inline glossary captures** (write project vocabulary as terms surface), **ADR offers** (record decisions worth keeping), and **North Star updates** (keep the project's standing strategy surface current, under its update asymmetry).

## Override: these writes ARE the action

The master frame in `SKILL.md` says answers and agreement feed exploration, not action — don't leap to the implied move, not the edit, not even the proposal.

When project docs are active, that frame has three explicit exceptions. **Glossary captures, ADR offers, and North Star updates are not deferred work — they are the action of this mode.** Execute them inline as they trigger. Do not batch to the end of the session. Do not wait for the user to ask. The writes are the deliverable; the deferred-action posture does not apply to them. For the North Star the carve-out covers exactly what its asymmetry permits: a status change on evidence executes inline, and a position rewrite executes inline only once the owner has explicitly ruled.

(The default figure-out posture still applies to everything else — design proposals, code edits, plan synthesis. Only these three carve out.)

## Bootstrap (when project relevance exists)

**Load the ADR conventions first.** Read the project's own `docs/adr/CONVENTIONS.md` when it exists — it governs, and a team that edited it meant to. Read the adjacent `ADR_FORMAT.md` when it does not. Either way the bar for what deserves a record is now in context, which is what lets the per-turn ADR check below run without another load.

**Load the project's `NORTH_STAR.md` when it exists** — the standing strategy surface the updates section below keeps current. Where the project context file already imports it, it is in context and needs no second read. Load the project's `docs/NORTH_STAR_CONVENTIONS.md` beside it when one exists: it owns the document's form — fields, states, rendering — and where it or the doc's own header differs from anything remembered here, the project's copy wins; cadence, below, stays this skill's.

**No CONTEXT.md and no `docs/adr/` at all** — the project has never been set up. Offer `manifest-dev:init-context`, which installs the conventions file, the glossary, and the context-file wiring in one pass and can seed them from the project's own history. On accept, invoke it and continue from what it produced. On decline, fall through to the minimal path below and don't re-offer.

Then resolve the active context file and load it if it exists:

1. **`CONTEXT-MAP.md` at root** → the repo has multiple contexts. Follow the map to the relevant context's `CONTEXT.md`. Ask which context if unclear.
2. **No `CONTEXT-MAP.md`** → the active context is the repo-root `CONTEXT.md`.
3. **Active `CONTEXT.md` exists** → load it as evidence. Project vocabulary is a source the user is already working from.
4. **Active `CONTEXT.md` is missing** → offer minimal initialization for that context: *"No CONTEXT.md exists for this repo/context. Want a minimal scaffold I can grow as terms resolve?"* On accept, write a starter file at the active context path (context name, one-sentence purpose, empty Language section). On decline, skip the proactive scaffold and don't re-offer it for that context — but subsequent per-turn glossary captures may still create the active `CONTEXT.md` lazily on first earned resolution. (Declining the scaffold only declines the *proactive* write, not the inline captures that docs mode exists for.)
5. **Multiple distinct domains emerge mid-session** → propose splitting via `CONTEXT-MAP.md` + per-context `CONTEXT.md`. Don't do this preemptively; only when the conversation actually crosses domain boundaries. If the user accepts a split and a relevant per-context `CONTEXT.md` is missing, offer the same minimal initialization for that new context.

## Glossary captures (per-turn, inline, no offer)

**After every counterparty response — or, in self-answered runs, every resolved question —** check for glossary candidates — but write only candidates that pass the earned-entry gate.

A candidate earns entry when it would help a future agent model this project correctly because at least one is true:

- **Project-specific meaning** — the term means something here that ordinary English or generic tool knowledge would not supply.
- **Ambiguity reduction** — confusing it with a near-synonym, alias, or overloaded term would change behavior.
- **Durable workflow boundary** — the term marks where responsibility, authority, completion, or verification changes hands.
- **Load-bearing relationship** — the relationship/cardinality between terms changes how future work should be understood.
- **Observed ambiguity** — the session exposed a clash with existing vocabulary or resolved a fuzzy term into a canonical one.

Do **not** capture merely because a noun was defined. Do not write obvious ordinary terms, generic platform vocabulary without a project-specific meaning, implementation labels, file paths, code structure, design decisions, or one-off explanations. If an existing entry already covers the term, do not rewrite it unless the user's meaning conflicts with it or materially sharpens it.

Signals that can trigger a write after the earned-entry gate passes:

- **A project-language term got defined** — user used a term with project-specific meaning and stated what they mean by it.
- **A load-bearing relationship got stated or changed** — user articulated a relationship or cardinality between project-language terms that would change future understanding.
- **A clash with the existing glossary** — user's term conflicts with an existing `CONTEXT.md` entry.
- **A fuzzy term got canonicalized** — agent or user proposed a canonical name for an overloaded term and it stuck.

If a signal fires and the candidate earns entry → **write to `CONTEXT.md` before asking the next question. No offer, no batch.** Capture as it happens. Create `CONTEXT.md` lazily on the first resolution if it doesn't exist (per Bootstrap above). If the gate does not pass, do not write; keep figuring out.

When the user's term conflicts with the existing glossary, surface the clash as a lead: *"Glossary defines X as A; you seem to mean B — which is it?"*

When the user uses a fuzzy or overloaded term, propose a canonical one: *"'Account' — Customer or User? Different things."* The user's articulation, not your inference, disambiguates.

## ADR offers (two-pass capture)

This section carries the **cadence** — when to raise an ADR during a session, and how the offer is made. The bar itself, and every write-time mechanic, live in the conventions Bootstrap already loaded: the project's `docs/adr/CONVENTIONS.md` where it exists, `ADR_FORMAT.md` otherwise. Apply that bar as loaded rather than a remembered version of it, and where the project's copy differs, the project's copy wins.

Cadence is this file's alone. A project may set what deserves a record and how it is written; it does not set when a session offers to write one.

### Pass 1 — per-turn (high-confidence)

**After every counterparty response — or, in self-answered runs, every resolved question —** check the loaded bar. When it fires *clearly* on a decision just articulated — user chose B over A with explicit reasoning, a scope boundary just got drawn, a key constraint just got named — **offer immediately**:

> *"This looks worth recording — [name the category and the Decision Test result]. Want me to write it up?"*

On accept: write it as the loaded conventions specify — including their whole act, which is the new record plus restatusing whatever it supersedes plus refreshing the index, not the new file alone. Capture alternatives from the conversation you just had — if the user picked B over A, that's exactly what goes in the Alternatives Considered section. If alternatives weren't articulated, ask before writing: *"What did we consider and reject? I want to capture that in Alternatives."*

### Pass 2 — session-end sweep (recall guarantee)

**Before naming the read** (or handing off to `/define`), review the session for candidates that didn't trigger Pass 1. Apply the same loaded bar. Present any survivors as a **batched offer**:

> *"Before we lock this in — these came up that look worth recording: [N items, one line each: title + why]. Record any?"*

For each accepted, write it the same way Pass 1 does. Skip the sweep if the conversation didn't actually produce decisions worth capturing — an empty sweep is fine.

The two-pass shape exists because per-turn alone misses subtle decisions (the check fires only at high confidence to keep interruption low), and sweep-only loses immediacy (alternatives are freshest right after the decision is made). Both passes together = inline coverage matches what a post-hoc sweep would catch.

## North Star updates (per-turn, under the asymmetry)

The loaded doc's own header and the project's conventions file define its states and
rules — apply them as loaded, not a remembered version. What stays here is cadence, and
the one asymmetry the bullets below branch on: **statuses move on evidence, positions
move only on the owner's explicit ruling.**

After every counterparty response — or, in self-answered runs, every resolved question —
check whether the session's findings touched a North Star line:

- **A finding contradicts a stated line** → surface the clash as a lead, exactly like a
  glossary clash: *"The North Star says X; this session found Y — which stands?"* Only
  the user's explicit ruling rewrites the position; on that ruling, write the new
  position inline, set its state, and offer the decision record that remembers why it
  moved (the ADR machinery above — a position change always clears its bar).
- **A finding weakens a line without settling it** → lower the state inline, no offer
  needed (evidence → hypothesis), appending one line naming what would settle it. Never
  touch the position's words.
- **A finding resolves an `empty` or `hypothesis` line** → present the grounds and the
  filled line; the user's yes writes it with the state its grounding earns — `evidence`
  with its date when something happened in the world, `ruled` when the answer is the
  owner's own choice. A `ruled` fill is a position change: offer the decision record
  that remembers it, as on the contradiction branch.
- **Fog that fits no field** → the doc's `Open` section (with what would fill it), or
  nowhere — never forced into a field as content.
- **A resolution too big for its field** → the field keeps the short answer with its
  state; the depth goes to an adjacent linked doc, per the conventions' split rule. The
  field stays the authority the depth details — never the other way around.

In self-answered or unattended runs the ruling path is closed: lower states and flag
contradictions in the session's output, never flip a position. Updates are event-driven —
this check is the whole trigger; there is no review cadence, and the dated states are what
keep staleness visible.

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
