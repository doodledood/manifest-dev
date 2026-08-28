# ADR: Continuation goals emit verbatim from one shared block

## Status
Accepted

## Area
Goal setting

## Context

A `/just-auto` run printed a continuation goal that opened `For the task "<the user's own sentence, reworded>"` and carried three fewer clauses than the skill file holds — the Read-checkpoint definition, the contents of a checkpoint note, and the instruction to record the Manifest's path. The user reported the printed text as a verbatim copy from their terminal.

The goal text had never differed in the repository: the same body appears in both commits that have ever touched `just-auto/SKILL.md` and in all three `dist/` copies. So the loss happened at emission, not in the source.

A controlled probe ran the backstop step through fresh isolated contexts in three prose forms — the inline-quoted prose in use, the same prose in a fenced literal block, and a fenced numbered-conditions rewrite — at two context loads (skill text alone, and after loading the project's resident context files), and again across a restatement boundary where the goal was emitted, substantial work was done, and the active goal was then restated. Twenty-four emissions in total.

The contract body survived intact in 24 of 24, in every form and at every load. The free-text `<task>` substitution did not: it was substantively reworded in 6 of 24, with `nice UX` returning as `with good UX`, `good UX`, and `nice to use`; `landing in` as `landed on`; and `drills` as `its drills`. The instruction producing that slot — *"replaced by a one-line statement of the task"* — is a standing licence to reword, sitting inside the one artifact whose purpose is to be a contract a host checker can hold the run to.

The probe therefore rules out prose form as the mechanism and identifies the free-text slot as the only unstable element, while leaving the reported clause loss unreproduced. That residual is recorded below rather than treated as explained.

Separately, the same contract was hand-maintained at six sites. The gate-ledger field list was byte-identical across `auto`, `do`, and `babysit-pr`, while the stale-gate rule beside it had already drifted into three wordings. Two sites — `/do` and `/babysit-pr` — carried no goal text at all, describing what the contract must require and leaving the model to compose it fresh on every run, which makes paraphrase the design rather than a lapse.

## Decision

Continuation goals are emitted verbatim from shared blocks, with a path as the only substitution.

One canonical goal block states the completion contract. Its single slot is `<manifest-path>`; no site substitutes free prose. Each site instructs the model to emit the block verbatim and not to summarize, shorten, reword, or re-punctuate it. Two further shared blocks carry what only some sites need — a gate-ledger clause for the three sites that verify under a selected mode, and a chain prefix carrying the Read-checkpoint bar for the two sites that run figure-out before a Manifest exists. `babysit-pr` adds a prefix unique to it for the PR-lifecycle terminal condition.

The blocks are duplicated in each shipped file rather than loaded from one shared path, because a skill must stand alone and path resolution differs across four distributions and two plugins. Each block carries a fence label — `goal-block`, `gate-ledger-clause`, `chain-prefix`, `pr-tend-prefix` — so its identity is separable from its own text. That matters more than it reads: a checker keying on the text it verifies cannot see one class of drift, because rewording the line it matches on makes the block stop being a block rather than become a different one, and the remaining copies still agree. Byte-identity is enforced by `tests/test_goal_contract_blocks.py`, which derives the files it checks — it finds the files carrying a block, so a site added later is compared without the test being edited, and it finds the files arming a backstop, so a site that drops or garbles its block is caught rather than silently skipped.

The mutability sentence is written to hold at every site without a per-site variant: *"it changes only through /define, never by direct edit, and a changed gate returns unverified."* `just-do` is genuinely read-only while `/do` self-amends on three routes — mid-run steering, a manifest statement gone false, and the Amendment Envelope's raise-only gate repair — so a block asserting "never edit it" would have been false at three of the five manifest sites, in the direction that has a continuation checker reject a legitimate envelope repair. The sentence keeps the anti-gaming property the older wording carried, since what stops a run making a gate pass by rewriting it is that a changed gate returns unverified, not that the Manifest is immutable.

`figure-out --autonomous` keeps its own Read-level goal and its existing form: no Manifest exists in that workflow, so the canonical block has nothing to name.

## Alternatives Considered

- **Restructure goals into numbered conditions**: the initial hypothesis, on the reasoning that an omission shows as a missing numbered item where a run-on sentence hides it. Rejected on the probe — the numbered arm and the prose arms both preserved the contract in every emission, so the restructure would be machinery heavier than the class it closes, and it scored no better on the slot that actually drifts.
- **Template the slot and leave the prose form alone**: rejected as insufficient on its own. Narrowing the slot is necessary, but two of six sites carried no literal text to template, so they would have kept composing their contract fresh.
- **Load the block from one shared reference file at emission**: the strongest de-duplication, and rejected on distribution mechanics. The block is emitted by five skills across two plugins into four distribution trees whose path resolution differs, and a shipped skill is required to stand alone. Duplication plus an enforcing test buys the same guarantee without a cross-plugin load.
- **Keep the free-text task restatement for checker disambiguation**: rejected. The completion condition names the Manifest, which is self-anchoring once it exists, and the run records its path in a checkpoint note; the disambiguation the free text bought did not pay for a licence to reword the contract.
- **Fold the gate-ledger clause into the canonical block**: rejected because it would push ledger machinery into `just-do` and `just-auto`, which are deliberately the lean executors and carry no ledger today. A separate shared block reaches the three sites that need it while leaving the lean paths as they are.

## Consequences

### Positive

- The contract a host checker holds is the contract the repository authored, at every site.
- The gate-ledger clause and the stale-gate rule beside it collapse from three hand-maintained copies and three wordings to one text each.
- `/do` and `/babysit-pr` gain literal goal text where they previously had none, so their contracts stop being recomposed per run.
- Drift is now a failing test rather than a convention someone has to remember, and the test finds its own subject, so a site added later is covered without anyone remembering to add it.
- The mutability sentence is true at every site, closing a case where a checker could have read a legitimate amendment as a violation.

### Negative

- The reported clause loss remains unreproduced. This decision removes the rewording licence, which is the mechanism the evidence reaches; if the real cause was something the probe could not stage — session compaction, a different serving model — degradation can recur and will need a fix aimed at restatement rather than emission.
- The same block is duplicated in twenty files. That is deliberate, but it means the test is now load-bearing: without it the duplication is worse than what it replaced.
- Three shared blocks plus one site-specific prefix is more structure than a single block would have been, and an author adding a backstop site has to pick which blocks apply.
- Sites carrying a prefix emit a literal `<manifest-path>` token whose meaning the prefix defines, rather than a substituted path, because they arm the backstop before a Manifest exists.

## Source

- Session: probe of 24 emissions across three prose forms, two context loads, and a restatement boundary; results recorded in the investigation log for the session.
- Related: `20260623-use-universal-goal-setting-language` — narrowed by this decision: the capability-based emission boundary stands, but the goal text itself no longer varies per distribution.
- Related: `20260623-use-host-continuation-as-optional-do-backstop` — unchanged; host continuation remains an optional outer backstop.
- Related: `20260624-use-outcome-gated-auto-continuation` — unchanged; the terminal condition stays outcome-gated and the Read bar stays a phase checkpoint before `/define`, both preserved in the chain prefix.
