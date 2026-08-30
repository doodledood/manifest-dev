# ADR: a shared contract block names the beat, not one arm's skill

## Status
Accepted — narrowed by 20260830-a-contract-slot-exists-only-where-its-value-is-known: the chain prefix's path-recording clause moves into the goal block and the `<manifest-path>` slot is removed; the beat-naming rule this record set stands.

## Area
Goal setting

## Context

`20260828-continuation-goals-emit-verbatim-from-one-block` made four contract blocks byte-identical wherever they appear, enforced by `tests/test_goal_contract_blocks.py`. Two of those blocks are emitted by both workflow arms: the goal block by `/do`, `/auto`, `/just-do`, `/just-auto`, and `/babysit-pr`, and the chain prefix by `/auto` and `/just-auto`.

Both named the regular arm's skills in their bodies. The goal block's mutability sentence read *"it changes only through /define"*; the chain prefix said *"before /define"* twice, *"Where figure-out runs"*, *"after /do has fresh all-gate PASS evidence"*, and *"as soon as define reports it"*.

That was accurate while one arm existed. `20260830-rendering-contract-folds-into-figure-out` shipped `just-figure-out` and `just-define` and re-pointed `just-auto` to chain just-figure-out → just-define → just-do, and the blocks did not follow — they could not, because byte-identity across both arms is exactly what the test enforces. A `/just-do` run therefore emitted a host contract telling it the Manifest changes only through `/define`, a skill that run never invokes; `just-do`'s own prose said so in the same file, one screen above.

The wrong half of that is not obvious from inside either arm. The contract is emitted to a host that holds the run to it, so an amendment through `/just-define` reads as a violation of the text the run itself printed, and the lean arm's whole point is that it needs no per-site variant to behave correctly.

`20260828` chose the mutability sentence deliberately, for a reason that still holds: it must be true at every site without a per-site variant, since `just-do` is read-only while `/do` self-amends on three routes. The defect is not that reasoning but its expression — it reached for the skill that happened to write manifests when the property it needed was *whichever skill wrote this one*.

## Decision

**A block shared across both arms names the beat, not the skill that performs it in one of them.**

- The goal block's mutability sentence becomes *"it changes only through the skill that wrote it, never by direct edit, and a changed gate returns unverified."* It is true at every site in both arms, resolves to `/define` under `/do` and `/just-define` under `/just-do`, and keeps the anti-gaming property intact — what stops a run making a gate pass by rewriting it is still that a changed gate returns unverified.
- The chain prefix names phases: *an investigation phase* rather than figure-out, *before the Manifest is written* rather than before `/define`, and *after execution has fresh all-gate PASS evidence* rather than after `/do`. Its checkpoint instruction records the path *as soon as the Manifest-writing step reports it*.
- Prose outside the shared blocks keeps naming skills. `/auto` still says `phase checkpoint before /define`, because that sentence is `/auto`'s alone and `/define` is what `/auto` runs. The rule binds the shared text, not the file around it.
- `just-do`'s own prose, which is not shared, now points at `/just-define` — inside the just-\* world, skills refer to just-\* skills.

The test's block signatures move with the text in the same change. A signature left behind still passes, because it is matched against block bodies rather than required to be found; the check would simply stop catching an unlabelled block, which is the one class of drift the labels exist to expose.

## Alternatives Considered

- **Give the lean arm its own variants of both blocks**: Rejected — it is precisely the drift `20260828` closed. Two texts under one contract name is the failure that record was written about, and the test would fail by design rather than by accident.
- **Leave the wording and accept the inaccuracy**: Rejected — the contract is emitted to a host that enforces it, so an inaccurate clause is not cosmetic: it can have a continuation checker reject a legitimate `/just-define` amendment. It also leaves `just-do` contradicting itself within one file.
- **Add a second slot alongside `<manifest-path>` for the amending skill's name**: Rejected — `20260828` removed the only free-text slot because a substitution licence is what the emission evidence showed drifting. A new slot re-opens that class to save one phrase.
- **Retire the shared chain prefix and let each auto skill carry its own**: Rejected — the Read-checkpoint bar is one decision (`20260624-use-outcome-gated-auto-continuation`), and splitting its text to fix four skill names would leave two copies of a bar nobody would keep in step.
- **Rename the lean skills so the shared text is accidentally true**: Rejected — naming a skill to satisfy a sentence inverts the dependency, and the two arms exist to be told apart.

## Consequences

### Positive
- The contract a host holds is true in both arms, so a lean-arm amendment through `/just-define` no longer reads as a violation of the run's own printed text.
- The rule is a property a future author can apply without knowing this history: text emitted by both arms names beats, text belonging to one names its skills.
- `just-do` stops contradicting itself between its prose and the block it emits.

### Negative
- *The skill that wrote it* is one indirection vaguer than a skill name for a reader who only ever uses one arm; the block trades a little immediacy for being true everywhere.
- The rule has no enforcement of its own. Byte-identity is tested; whether a shared block's wording is arm-neutral is a judgment made when the block is edited, and a future block can reintroduce a skill name with the suite still green.
- Two published records now quote the superseded mutability sentence in their bodies. Their bodies are immutable, so the cost is paid with a Status cross-reference rather than an edit.

## Source
- Session: follow-up to the chat-surface retirement and just-\* world, 2026-08-30, prompted by the lean chain's blocks still naming the regular arm after `just-auto` was re-pointed.
- Related: 20260828-continuation-goals-emit-verbatim-from-one-block — narrowed by this record: the one-text-per-block property and the no-per-site-variant requirement both stand; only the wording that satisfies them changes.
- Related: 20260830-rendering-contract-folds-into-figure-out — the record that shipped the lean arm this one repairs the blocks for.
- Related: 20260623-use-universal-goal-setting-language — the same move one level up: name the capability rather than the harness primitive, here the beat rather than the skill.
