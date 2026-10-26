# ADR: figure-out probes decisions and plans whose outcome depends on futures nobody controls, with no default decision rule

## Status
Accepted; amended by 20261020-figure-out-decision-probes-read-other-parties-name-the-flip-chance-and-look-for-unnamed-aims: the header, States of the world, Value of information and Fundamental objectives gain other parties, the flip chance and unnamed aims; the count stays 13; amended by 20261020-figure-out-stops-a-decision-only-on-shown-reasons: the Value of information stop clause becomes a question whose answer needs shown reasons; amended by 20261025-figure-out-counts-each-driver-against-every-aim-it-moves: adds Drivers across branches; the count becomes 14

## Area
Task guidance

## Decided by
The user

## Context

figure-out picks probe files by the topic's shape (see 20260611-figure-out-task-taxonomy-diagnosis-research-topic-trigger). A choice between options, or a plan, whose outcome depends on futures nobody controls — a launch, a pricing model, which product bet to build — matched none of them and fell through to general probing.

In one observed session on a launch decision, the user had to ask for the method outright: map every plausible future and steer toward the best outcome with least regret. Even with that request in hand, the session missed four things the user then caught: it scored the options on money and reach before the purpose the user had stated; it missed that the first public act (a teaser video) would start a copy clock before launch day; it did not generate the hybrid option that removed the worst cases until pushed; and it ranked an option down for an uncertain remark about later plans instead of weighing the remark on every option. It also treated least regret as the only rule, though that rule fits one shape of decision.

Least regret is one decision rule among several, not a universal one. Savage's minimax-regret criterion fits a one-shot, hard-to-undo choice without credible probabilities; expected value fits repeated or reversible choices with estimable odds; satisficing fits where searching costs more than it gains; robust approaches aim for an option acceptable in every future. A default stance would tilt every read toward whichever rule it names.

## Decision

- **Add `figure-out/tasks/DECISION.md`**, loaded from the `## Probes` topic list for "a decision or plan whose outcome depends on futures nobody controls". In decision theory a plan is a decision made over time — what to do now and on each signal — so one file covers both. A choice that external evidence alone can settle stays with `RESEARCH.md`.
- **No default decision rule.** The file asks which rule fits the choice's shape and the person, from an open set (least regret, best average, avoid ruin, good enough, robust, or another), keeps rough odds in view whatever the rule, and leaves how much downside to accept to the person.
- **Labels are decision-analysis terms of art, each followed by a plain question**, so the named concept brings its body of practice while the question keeps jargon out of what figure-out says to the person.
- **The probes and where each comes from:**
  - *Fundamental objectives*, *States of the world* (including the person's own uncertain later plans), *Irreversibility*, *Dominating hybrid* — the four observed misses; the futures map also by the user's request; objectives before alternatives, and creating better alternatives, from Keeney (1992), *Value-Focused Thinking*.
  - *Decision rule* — the user's ruling for an open set; Savage (1951), Simon (1955 model, 1956 term "satisficing").
  - *Reference class* — Kahneman and Lovallo (1993); Lovallo and Kahneman (2003).
  - *Premortem, then backcast* — Klein (2007), building on Mitchell, Russo and Pennington (1989) on prospective hindsight; Robinson (1982) for backcasting; Duke (2020) for running the premortem first and splitting reasons into decisions and luck.
  - *Decision versus outcome* — Howard (1988) on decision quality; Howard and Abbas (2016); Duke's "resulting" for the mistake it guards against.
  - *Signposts and triggers*, *Shaping actions* — Dewar (2002, after Dewar et al. 1993) on Assumption-Based Planning; Haasnoot et al. (2013) on adaptive policy pathways.
  - *Decision stacking* — Duke (2020).
  - *Value of information* — Howard (1966); Duke's happiness test and quit cost for when to stop.
  - *Precommitment* — Duke's Dr. Evil game (2020); Ainslie (2001) on personal rules.
  - The trade-off, wait to learn versus act — Dixit and Pindyck (1994) on irreversibility and the option value of waiting.
- **Source caveats.** Most sources were checked through abstracts, publisher pages or secondary summaries; Dewar (2002) and Haasnoot et al. (2013) were read in primary text. The figure often quoted from Mitchell, Russo and Pennington (a 30% gain in identifying reasons) overstates what their paper found, so the premortem rests on practice, not on that number. "Resulting" is poker slang that Duke popularized, not her coinage. The Dr. Evil game's attribution to *How to Decide* rests on summaries only.

## Alternatives Considered

- **Least regret as figure-out's default stance in the spine**: Rejected — the rule fits one shape of decision, and an always-loaded default would tilt every read, including the many that are not decisions.
- **No file; rely on general probing**: Rejected — the observed misses happened under general probing, with the user's request for the method in hand.
- **A closed set of decision rules**: Rejected by the user — the rule has to fit the task and the person, and a list presented as complete narrows both.
- **Naming the file `PLANNING.md`**: Rejected — reads as excluding a choice between options, while `DECISION.md` covers plans as decisions made over time.

## Consequences

### Positive
- Decision and planning topics get the angles a capable model skipped in practice, and the rule question stops least regret from being applied where it does not fit.
- The figure-out recipe's `decision` scenario checks that the file loads and that a read shows the four observed-miss angles.

### Negative
- Thirteen probes is near the top of the sibling range; a read may press more of them than a small decision deserves, which the value-of-information probe is there to cut short.
- Eval case `06-strategic-open`, a product-planning topic, will likely load the file; whether that changes its uplift is unmeasured until the suite runs.

## Enforced by
partly — the `decision` scenario in `verification/recipes/figure-out.md` checks that the file loads and that a read shows the observed-miss angles; that no rule is the default and that labels keep a plain question stay judgment.

## Source
- Session: figure-out and define on adding a decision method to figure-out, after a launch decision in another project (2026-10-19).
- Related: see also 20260611-figure-out-task-taxonomy-diagnosis-research-topic-trigger, 20260817-prompt-lines-earn-their-place-by-provenance
