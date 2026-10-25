# ADR: figure-out records what the lean-body rebuild retired

## Status
Accepted

## Area
figure-out

## Decided by
An agent in an unattended run, with no review — under the user's delegation to carry out and
merge the change that the 2026-10-25 records describe. The delegation covers how this record
rules on each dropped rule. Under it, this record restores no rule to `SKILL.md`.

## Context

The rebuild of 2026-09-14 (`20260914-one-skill-per-beat-built-from-the-lean-body`, commit
`ef9806fa`) rewrote `figure-out/SKILL.md` from 4,445 to 1,438 words, by `wc -w`. It changed no
other figure-out file. Its record says every capability of the longer prompt survives, and the
capabilities it names do. But the spine rules cut in the rewrite were deleted, not moved, and no
record whose rule was cut changed its Status. Seventeen records that are still Accepted state rules
that `SKILL.md` held at `ef9806fa^` and no longer holds, in full or in part.

These rules were found by comparing `SKILL.md` at `ef9806fa^` with the shipped skill files at
`962f09bd` and reading each Accepted record that has the `figure-out` area or states a
figure-out rule. Line numbers below are at `d02a9e25`, relative to
`claude-plugins/manifest-dev/skills/figure-out/`.

The evidence for the rulings:

- The 2026-10-25 eval baseline and the v0/v1 round on `42` and `64` (suite README, *Baseline —
  2026-10-25* and *Hill-climb on proportionate re-checks*).
- In-session simulations of the skill at `962f09bd`, with a restored line and without it. Each
  simulation produced two replies per variant, and two graders per batch graded them blind. These
  are not eval-suite results, and the batches are kept outside the repository.

## Decision

Each dropped rule gets one ruling:

- **Retired**: it is no longer the project's rule.
- **Carried elsewhere**: a shipped file states it, at the line named.
- **Back through this change**: this change restores it to a shipped file, at the line named.
- **Not decided**: no evidence yet supports keeping it or retiring it. A `Revisit when` says what
  would settle it. Until then, it is not in the shipped skill.

| Record | Rule cut | Ruling | Grounds |
|---|---|---|---|
| `20260714-figure-out-scales-read-depth-with-stakes-and-reversibility` | Read depth follows what rides on the read, not only fog | Back through this change for autonomous mode (`references/autonomous.md:26-27`, under `20261025-figure-out-re-derives-only-reads-that-are-costly-to-get-wrong`). Not decided for interactive mode | In simulation, a restored spine line left the re-check on every small autonomous ask, because the reference's own rule overrode it. The autonomous edit stopped it, and the eval round agrees (re-check reported in 4 of 6 v0 replies, 0 of 6 v1). No interactive case measures depth by stakes. Revisit when an interactive case fails for depth that does not fit the stakes, in the suite README |
| `20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass`, `20260606-figure-out-process-trust-vs-define-do-artifact-trust` | Take the outside view (base rates) before locking the read | Carried elsewhere for decisions and plans (`tasks/DECISION.md:10`, *Reference class*). The spine line is not decided | In simulation, without the line, 1 of 4 replies on plan estimates lacked a base rate. On a cost choice, the line named the usual answer in 2 of 4 replies, against 0 of 4. With it, the lamp choice (`64`) failed its rubric 2 of 2. Revisit when a read on a plan, estimate or forecast misses a base rate that the user or a later result supplies |
| `20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass` | Regenerate the rival set as findings open or close ground | Retired. Rival discipline is carried at `SKILL.md:84` and `references/autonomous.md:10` | In simulation, the prompt at `962f09bd` added a new rival where findings opened one, in 2 of 2 replies, without the line |
| `20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass` | Corroborating sources must be independent, not echoes of one origin | Not decided. `SKILL.md:83` keeps the check that a citation exists and supports its claim | Nothing tested it. Revisit when a read leans on corroborating sources that turn out to share one origin |
| `20260611-figure-out-evidence-ledger-and-independent-rederivation` | "Underdetermined" is earned by running every discriminating probe | Carried elsewhere (`references/autonomous.md:10`; `tasks/DIAGNOSIS.md:19`). The interactive spine copy is retired | In two simulated interactive diagnoses, the prompt at `962f09bd` refused to name a cause it could not support and found a probe still left to run (2 of 2, twice) |
| `20260611-figure-out-evidence-ledger-and-independent-rederivation` | A judgment read states its trade-off boundary; the anatomy collapses when there are no evidence claims | Not decided. `SKILL.md:14-15` keeps confidence, evidence and overturn conditions | Nothing tested it. Revisit when a judgment read leaves out where its trade-off flips, or a read with no evidence claims carries an empty ledger |
| `20260611-figure-out-evidence-ledger-and-independent-rederivation` | Re-derivation also runs on request, from gathered evidence only, and may report that the evidence underdetermines | Not decided. The load-bearing trigger and the self-graded disclosure remain in `SKILL.md` | Nothing tested it. Revisit when a user asks for an independent check and does not get one, or a re-derivation collects new evidence |
| `20260611-figure-out-evidence-ledger-and-independent-rederivation` | Only load-bearing claims carry provenance into the turn; "verified" needs a logged artifact | Not decided. `SKILL.md:79-80` keeps voiced status; `references/LOG.md:37` keeps the artifact rule for the log | Nothing tested it. Revisit when turns carry provenance on every claim, or a claim marked verified has no logged artifact |
| `20260611-figure-out-spine-owns-epistemics-mode-refs-thin` | All epistemics, convergence rules included, live in the spine | Retired for autonomous mode. Its stop rule, its earned-underdetermined rule and its depth scale live in `references/autonomous.md:10, 26-27` | In simulation, a spine line could not change behavior that the reference's fixed rule set: all 16 small-ask replies, across every spine variant, still asked for the re-check. The change belongs in the file that holds the rule |
| `20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint` | Before naming a read that implies making something, list the user-judged surfaces never discussed and give each a fate | Carried elsewhere for feature work (`tasks/FEATURE.md:11`, *Undiscussed surface*). The read-naming copy is not decided | Nothing tested it. Revisit when something figure-out shaped is built with a surface the session never discussed, and the user rejects that surface |
| `20260826-sensing-the-output-is-a-precondition-of-naming-a-read` | Stating the output and offering a render come before naming the read; a decline is an accepted default | Carried elsewhere in part (`SKILL.md:110, 120-121`; `references/autonomous.md:19`). The precondition and the decline rule are not decided | Nothing tested it. Revisit when a read is named before the output it implies is stated, and the user rejects that output |
| `20260826-prototyping-and-scratch-are-one-mechanism` | Show the draft rather than describe it; polish is not the axis | Carried elsewhere in part (`SKILL.md:127`, `137-138`). Show-don't-narrate and polish-is-not-the-axis are not decided | Nothing tested it. Revisit when a session describes a draft it could show, or polishes one past the question being judged |
| `20260714-figure-out-challenge-solution-existence-before-design` | Keep, remove or fold each element on benefit against cost, settled from evidence first, for each child too | Carried elsewhere in part (`SKILL.md:74-75`, `95`). The per-child repeat and the benefit-against-cost wording are not decided | Nothing tested it. Revisit when a read keeps a component or step whose need the session never tested |
| `20260714-figure-out-roots-crux-tree-above-solution-shaped-topics` | Open at the problem with the best-supported guess; say nothing about it when the problem is already established | Carried elsewhere in part (`SKILL.md:73-74`, `23`). The silent-when-established clause is not decided | Nothing tested it. Revisit when a session reopens a problem the user had already established |
| `20260714-figure-out-keeps-do-nothing-in-the-option-set` | Living with the problem is priced on the same evidence, in every mode | Carried elsewhere (`SKILL.md:69-70`, which applies in every mode) | The spine line states the rule. Pricing on the same evidence is how the spine weighs every option |
| `20260803-figure-out-turn-carries-one-concrete-claim` | Concrete beats abstract; each part's first line carries the information | Carried elsewhere in part (`SKILL.md:23`, `42-45`). The two clauses are not decided | Nothing tested it. Revisit when a turn's lead line or claim stays abstract where a concrete one was available |
| `20260810-universal-discipline-belongs-in-the-prompt` | A term of art the user has not met fails the plain-words bar | Not decided. `SKILL.md:42-45` keeps common words | Nothing tested it. Revisit when a turn uses a term the user has not met and the user asks what it means |
| `20260809-figure-out-budgets-the-whole-turn-not-its-bold-lines` | Low reading load is the default, and a ratified Taste entry can bend it | Carried elsewhere in part (`SKILL.md:21`). The Taste bend is not decided | Nothing tested it. Revisit when a user with a Taste entry for denser turns gets the default load |
| `20260726-figure-out-narrows-presentation-no-trim-clause` | The load comes off how a turn reads, never off what was investigated | Carried elsewhere (`SKILL.md:59-60`) | The spine keeps the investigation going through discoverable questions, whatever the turn shows |
| `20260820-pointer-fallbacks-need-a-compressible-target` | The prompt-engineering pointer keeps an "if available" guard and an inline fallback | Not decided. `SKILL.md:203-205` has a bare pointer | Nothing tested it. Revisit when a session meets a prompt-shaped topic with the prompt-engineering skill not installed |
| `20260709-figure-out-reweight-by-rehosting-not-extraction` | The six-section arc and its deliberate duplication | Retired | The rebuild replaced the arc, under `20260914-one-skill-per-beat-built-from-the-lean-body` |

## Alternatives Considered

- **Restore the dropped rules to `SKILL.md`**: the simulations showed a need for none of the lines
  tried in the spine (depth by stakes, outside view and rival regeneration, earned
  underdetermined). The outside-view line made a small choice heavier. Rejected.
- **Retire every rule the rebuild dropped**: most were never tested either way, and retiring them
  would claim evidence the project does not have. Rejected for the untested rules, which are
  marked not decided instead.

## Consequences

### Positive
- Every Accepted figure-out record says in its Status what the shipped skill no longer carries,
  so a later session does not cite a rule that is not there.
- Each untested rule has a condition that would settle it.

### Negative
- Many rules stay not decided, so a gap one of them covered can still occur.
- The rulings rest on simulations of a few cases, not on suite runs.

## Enforced by
none — whether a dropped rule's gap shows up is read from sessions and eval results; each `Revisit when` above names where

## Revisit when
A `Revisit when` condition in the table above is met, read in figure-out logs or the suite README's results sections.

## Source
- Session: a figure-out investigation and `/auto` run on figure-out's question quality, 2026-10-25; simulation batches and blind keys kept outside the repository.
- Related: 20260914-one-skill-per-beat-built-from-the-lean-body
- Related: 20261025-figure-out-re-derives-only-reads-that-are-costly-to-get-wrong
- Related: 20261025-figure-out-counts-each-driver-against-every-aim-it-moves
