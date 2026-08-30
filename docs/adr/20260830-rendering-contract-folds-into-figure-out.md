# ADR: the rendering contract folds into figure-out, and chat-surface is retired

## Status
Accepted

## Area
Prompt architecture

## Context

The rendering contract lived in `chat-surface`, a standalone skill figure-out loaded before every turn, with two modes and one other consumer (`re-pitch`). In use, neither mode earned its keep:

- **html mode went unused.** It rendered the conversation into a live HTML page beside the terminal — structurally the same secondary-surface arrangement whose failure retired the crux-map canvas ([20260818-chat-surface-replaces-the-crux-map-canvas](20260818-chat-surface-replaces-the-crux-map-canvas.md)): the answers still arrive in the terminal, and a page beside the primary surface goes unread. The counter-example that works, `eli5`, works because its artifact *is* the deliverable, not a mirror of the chat.
- **text mode restricted more than it helped.** The contract had already collapsed once on this diagnosis — [20260821-rendering-contract-judges-the-whole-turn](20260821-rendering-contract-judges-the-whole-turn.md) cut eight per-element rules to five on provenance and flagged that if turns kept reading badly under it, the fix was an external check rather than firmer wording. What remained still prescribed form vocabulary (monospace shapes, fencing, emphasis ownership) that the model re-derives from an audience model on its own.
- `re-pitch`, the second consumer, carried most of its own audience guidance inline and was judged not to earn its keep either.

[20260818-surface-skill-owns-the-rendering-contract](20260818-surface-skill-owns-the-rendering-contract.md) had rejected a separate terminal-surface skill because one paragraph "does not earn a marketplace entry, three distribution copies, two symlink sets, and README rows." With the contract reduced to a few sentences and html mode unused, `chat-surface` itself fails that same bar — the fold is the corpus's own logic applied, not a reversal.

The same session ruled a broader bet: the full figure-out/define pair spends much of its length on coined vocabulary that recruits no priors, and a lean arm should exist beside them the way `just-do` sits beside `/do` — compressed by provenance, with the regular skills as backbone.

## Decision

Retire `chat-surface` and `re-pitch` everywhere — skill directories, all three `dist/` trees, both symlink sets, the single-home pin test, README and registry rows — and fold the rendering contract into figure-out's own turn section as three audience-model sentences: the reader has limited attention and must be able to re-enter a turn at a glance; several things of one kind get a form with one slot each, so a dropped member shows; the ask is set apart at the end. Beyond that, form is the model's own call. The one-slot sentence is the only form rule kept from the whole contract, because it carries the one observed failure (a prose turn silently dropped two of eight audit items).

Alongside the fold, ship a temporary lean arm: `just-figure-out` and `just-define`, goal-based counterparts to figure-out and define with the same functional coverage compressed into pretrained language, fully self-contained (own task-file copies, own schema copy — duplicated deliberately, so promoting one to main is a bare rename), self-referential within the just-* world, with `just-auto` re-pointed to chain just-figure-out → just-define → just-do. The regular figure-out/define/do stay untouched beyond the fold, as the control arm, until one arm is chosen.

## Alternatives Considered

- **Keep chat-surface, text mode only**: delete html mode and keep the skill as the contract's home — Rejected: a few principle sentences fail the marketplace-entry bar the corpus itself set, and the split home was the reason figure-out's default path once reached no contract at all.
- **Fold the whole five-rule contract verbatim**: relocate without compressing — Rejected: only the one-slot rule has an observed failure behind it; the rest restates what an audience model already recruits, which is the over-specification the fold exists to remove.
- **Share one schema file between define and just-define**: a common `references/SCHEMA.md` both point at, eliminating drift — Rejected by ruling: the just-* world must be promotable by bare rename, so each skill carries its own copy; drift is accepted as the temporary world's cost.
- **Hold chat-surface in the control arm**: retire it only from the lean path — Rejected by ruling: nobody uses it in either arm; keeping it would preserve a surface already judged dead.

## Consequences

### Positive
- Every figure-out turn is shaped by three resident sentences instead of a skill load; the default path cannot miss the contract, and the coined vocabulary the contract carried stops costing tokens in every session.
- The repo sheds a marketplace entry, three distribution copies, two symlink sets, a pin test, and README rows for a capability nobody used.
- The lean arm gives the compression bet a real A/B: same contracts, minimal process, switchable by rename.

### Negative
- The completeness discipline now rests on one sentence in figure-out; if silent omissions return, the contract has no dedicated home to strengthen.
- Deliberate duplication between define and just-define (schema) and figure-out and just-figure-out (task files) can drift silently — accepted for the world's intended short life, with a byte-identity tripwire test as the known repair if it outlives that.
- html-mode rendering is gone entirely; a future need for rendered output starts from the artifact-as-deliverable shape (eli5), not from a revived chat mirror.

## Source

- Supersedes 20260818-chat-surface-replaces-the-crux-map-canvas (the chat-surface replacement it shipped; the crux-map canvas it retired stays retired — its secondary-surface diagnosis is a ground for this decision)
- Supersedes 20260818-surface-skill-owns-the-rendering-contract
- Supersedes 20260819-surface-modes-name-their-output-format
- Supersedes 20260821-rendering-contract-judges-the-whole-turn
- Related: 20260820-pointer-fallbacks-need-a-compressible-target (its motivating instance — figure-out's chat-surface pointer — is retired; its rule stands for future cross-plugin pointers)
- Session: figure-out session, 2026-08-30 (investigation log kept outside the repo)
