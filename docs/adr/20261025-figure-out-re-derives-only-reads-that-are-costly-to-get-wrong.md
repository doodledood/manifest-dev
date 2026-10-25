# ADR: figure-out's autonomous mode re-derives and re-classifies only reads that are costly to get wrong

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context

`figure-out/references/autonomous.md` treated every autonomous read as load-bearing. It sent the
user's-call classification of every read to a fresh context, said that `SKILL.md`'s independent
re-derivation "always runs before naming", and its completion contract required the
re-derivation "run or explicitly unavailable". `SKILL.md` itself states the re-derivation for a
read that "is load-bearing and nobody will audit it", as
`20260611-figure-out-evidence-ledger-and-independent-rederivation` decided, so the reference was
stricter than the spine and the record it implements.

The cost fell on small asks. The 2026-10-25 eval baseline (`claude-plugins/manifest-dev/evals/README.md`,
*Baseline — 2026-10-25*) names `42` (a one-word typo fix) and `64` (a choice between a $38 and a
$42 lamp with free returns) as the plugin arm's biggest loss: both fall from 1.00 to 0.00. The
rebuild of 2026-09-14 had also dropped the dial that scaled a read's depth with what rides on it
(`20260714-figure-out-scales-read-depth-with-stakes-and-reversibility`).

In-session simulations measured the change before it shipped. Each variant produced two
replies, and two graders per batch graded them blind. These are not eval-suite results.

- Small asks (`42`, `64`): every reply on the unchanged prompt (`962f09bd`) called for a
  re-check (4 of 4). With
  the conditional rule, in several variants, no reply did (0 of 16). On `64` the repository's own
  rubric passed both replies with the change, against 1 of 2 and 0 of 2 for the unchanged prompt in two
  batches.
- A deep outage diagnosis (`76`): with the change, every reply still called for the re-check
  (4 of 4) and scored as deep as the unchanged prompt on the case's five graders.

The eval-suite comparison of the unchanged and changed skill on `42` and `64` is recorded in the
suite README's results section for this change.

## Decision

In autonomous mode, the independent re-derivation and the fresh-context classification of the
user's calls run wherever the read is load-bearing — acting on it would be costly or hard to undo.
A read whose miss costs only a cheap reversal is self-graded, classifies inline, and says so in
one line; the depth of the whole read follows the same scale. The completion contract and the
parent contract carry the same condition. `SKILL.md` needs no change: its re-derivation bullet
already states the condition.

## Alternatives Considered

- **Keep the re-check on every autonomous read**: the absence of an auditor is real in every
  autonomous run — rejected because on cheap, reversible reads the re-check costs more than a
  miss and drives the over-investigation the baseline measured.
- **Restore the stakes dial in `SKILL.md`'s spine**: tested beside a spine causal-model line;
  rejected here because the measured cost sits in autonomous mode's rule, so the fix belongs
  where that rule lives.

## Consequences

### Positive
- Small, reversible autonomous asks get a short read without a second context.
- The reference and the spine state the re-derivation under the same condition.

### Negative
- Whether a read is cheap to reverse is itself a judgment the run can get wrong; a costly read
  misjudged as cheap loses its re-check. `62-decision-rival-answers`, whose graders hold the
  re-derivation of a load-bearing read, is the case that would show it.

## Enforced by
partly — `62-decision-rival-answers` (`independent-check-called`, `checks-the-read-independently`) and `64-decision-small-and-undoable` (`picks-without-ceremony`) in the figure-out eval suite; whether a read is load-bearing stays judgment

## Revisit when
`62`'s re-derivation graders fail on the plugin arm where they passed before this change, read in the figure-out suite README's results sections.

## Source
- Session: a figure-out investigation and `/auto` run on figure-out's question quality, 2026-10-25; simulation batches and blind keys kept outside the repository.
- Related: 20260611-figure-out-evidence-ledger-and-independent-rederivation
- Related: 20260714-figure-out-scales-read-depth-with-stakes-and-reversibility
- Related: 20261025-figure-out-records-what-the-lean-body-rebuild-retired
