# ADR: figure-out's decision probes read other parties from their side, name the flip chance, and look for unnamed aims

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context

`figure-out/tasks/DECISION.md` (see 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures) gave figure-out thirteen probes for a choice or plan whose outcome depends on futures nobody controls. A review of those probes against a standard decision-theory curriculum — the decision table, rules without odds, expected value, utility, subjective probability, updating, value of information, sequential decisions, small and large worlds, game theory, the behavioural findings, calibration — found most of it covered or applied by a capable model unprompted, and three holes.

- **Other parties.** The file framed every uncertainty as a future the plan "has to live with". When part of the uncertainty is another party whose move answers the person's — a rival answering a price, a buyer reading an offer — that is the wrong model: their move is not a fixed state with a chance. The Stanford Encyclopedia of Philosophy entry "Game Theory" (Ross, rev. 2023, §1) calls the distinction between acting on a passive world and acting on one that anticipates you "fundamental". In the session that motivated the file, a public teaser that would let copiers start early was caught only by the user, and was absorbed under irreversibility rather than named as a strategic response.
- **The flip chance.** *Value of information* asked "how wrong can they be?" without the tool that answers it: the chance at which the choice would flip, which lets a person compare a rough estimate with a threshold instead of producing an exact probability. This is the threshold approach Pauker and Kassirer (1980, *New England Journal of Medicine* 302:1109–1117) set out for test-or-treat decisions, and the indifference probability of the standard decision-analysis texts.
- **Unnamed aims.** *Fundamental objectives* asked only for the aims in the person's own words. Bond, Carlson and Keeney (2008, *Management Science*) found that people "consistently omitted nearly half of the objectives that they later identified as personally relevant", and that 35% of one sample missed their most important one.

## Decision

- **Fold all three into existing probes; the count stays 13.**
  - The header keeps the index line's scope phrase, "futures nobody controls" (read as the outcome nobody controls), and adds that part of that uncertainty can be another party's answer to the person's move.
  - *States of the world* drops "the plan has to live with each of them" and asks which future is really another party's move, to be read from their side — what each move gets them, and whether a threat or promise they state would hold — before any chance is put on it.
  - *Value of information* asks at what chance the choice would flip, and whether the person's estimate sits clearly on one side of it.
  - *Fundamental objectives* asks which aims the person holds but has not named.
- **The figure-out `SKILL.md` index line is unchanged.** Widening it was not decided; the header is worded so it does not contradict it.

## Alternatives Considered

- **A separate probe for other parties**: Rejected — it would push the file to fourteen probes, past the sibling range, for an angle that sits naturally inside the futures probe.
- **Testing the current file on a counterparty decision before editing**: Rejected by the user in favour of editing now with a scenario that exercises the result.
- **Leaving the file as is**: Rejected by the user.
- **Adding the normative core — the decision table, expected value, utility, Bayes**: Rejected — a capable model applies these unprompted when it compares options, and task files carry only angles a model skips.
- **Widening the `SKILL.md` index line to "futures the person doesn't control"**: Not taken here — it changes when the file loads, which was outside the change agreed.

## Consequences

### Positive
- Decisions against a rival, a buyer or a counterparty get the strategic reading the file framed out, and a person who cannot name a probability gets a threshold to compare against.

### Negative
- No run compared the unedited file on the same counterparty decision, so the new clauses' uplift is unmeasured. The other-party edit should be reversed if a counterparty drive on the unedited file already reads the rival's side, or if eval case `06-strategic-open` loses uplift once the suite runs.
- The unnamed-aims clause has no scenario: a prompt cannot state an aim the person did not name without naming it.

## Enforced by
partly — the `decision-counterparty` scenario in `verification/recipes/figure-out.md` checks that the file loads for a counterparty decision and that a read reasons from the rival's side and states the flip chance; the `decision` scenario re-checks the angles the file already drew out. The unnamed-aims clause and the probe wording stay judgment.

## Source
- Session: a review of the decision probes against a decision-theory curriculum (2026-10-20). Sources: the Stanford Encyclopedia of Philosophy "Game Theory" §1 and Bond, Carlson and Keeney (2008), each checked at source; Pauker and Kassirer (1980), checked through bibliographic listings and secondary summaries only.
- Related: amends 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures
