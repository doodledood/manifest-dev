# ADR: An AI judge in a hill-climb compares two versions against the goal, never scores, and ships after it is measured

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled four things: the judge compares A against B with the goal, the person and their moment in front of it; it uses no score scale and no example versions; it serves any kind of artifact; and it is measured before it ships. The agent drafted the voting practices below from the cited sources.

## Context
Some goals have no number. Does a page serve the person arriving at it? Does a document answer its reader? Do a prompt's outputs read the way the task needs? For goals like these, the measure is a model's judgment.

A language model's judgment is noisy and biased in known ways:
- **Position.** On real A/B-tested interface pairs, judges favored the second image, and their accuracy when both orders had to agree was near or below chance (WiserUI-Bench, arXiv 2505.05026).
- **Self-enhancement.** Some judges favor their own outputs, and their choices also lean on position (Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, 2023).
- **Non-transitivity.** Judged preferences between pairs are not transitive (Xu, Ruis, Rocktäschel and Kirk, *Investigating Non-Transitivity in LLM-as-a-Judge*, ICML 2025).
- **Self-refinement.** A model that refines its own work against its own judgment amplifies its bias (Xu et al., *Pride and Prejudice*, ACL 2024).

Context changes the picture:
- **Thin or no context.** Studies that gave the judge little or no purpose found it near chance on interface designs (WiserUI-Bench; DesignPref, arXiv 2511.20513; TASTE, arXiv 2605.20731).
- **Rich context.** SimAB (arXiv 2603.01024) gave the judge the conversion goal and the audience, and balanced the order over many votes. It matched about two thirds of historical A/B test outcomes, and more on the cases it was confident about. Its sample was a few dozen tests, so its error bars are wide.

No study found tests a context-rich pairwise judge on larger redesigns or on how a design feels. Its reliability as the measure for a climb is unmeasured.

## Decision
- **The judge compares; it never scores.** An AI judge in a climb compares two versions and says which one better serves the stated goal for the stated person in their moment, or that they tie. It never scores on a scale. It is shown no example of a good version, because an example pulls every candidate toward itself.
- **The judge is designed for its task.** It sees each version as the person meets it:
  - a page rendered at the person's device and in the state they arrive in;
  - a prompt run on the same inputs;
  - a document read as its reader.

  It also sees the goal, the person, their moment and what must not change. It does not see which version is newer or who made it.
- **Votes are fresh, blind and balanced.** Every vote comes from a fresh judge that did not make the candidates, under neutral labels, in both orders. A comparison keeps taking votes until one version is clearly ahead or a vote cap set by define is reached. A close result is a tie, and a tie keeps the incumbent. A new leader is confirmed on fresh votes before it replaces the incumbent.
- **This kind ships only after it is measured.** The judge is measured on pairs whose better version is already known, from real use where that exists, against a bar fixed before the measurement runs. Climbs whose measure is a number or a suite ship first.

## Alternatives Considered
- **A scored rubric, for example 1 to 10 per criterion.** Not chosen: a score asks the judge to hold a scale steady across calls with nothing to anchor it, and it puts unlike tasks on one scale. A choice between two concrete versions is a question the judge can answer.
- **Example or reference versions as anchors.** Not chosen: the climb then moves toward resembling the example instead of serving the goal.
- **The generating model judges its own candidates.** Not chosen: it amplifies its own bias.
- **Ship the judge together with the measurable kinds.** Not chosen: no evidence yet shows the judge reliable enough to steer a climb unattended.

## Consequences

### Positive
- Each judgment answers one concrete question, with the context a person deciding it would need.
- Position bias and noise stay inside the tie zone instead of moving the climb.
- Measuring before shipping turns "the judge is good enough" into a recorded result.

### Negative
- Each comparison costs several judge sessions, in both orders.
- A judge without real-use data cannot know what the person would actually do. A climb's result is a well-argued candidate, not proof.
- Climbs whose goal needs a judge wait for the measurement.

## Enforced by
not yet — two checks. An ask-first judge-measurement recipe holds the shipping bar. A `hillclimb` recipe scenario reads a climb's record for both orders, fresh judges and the confirmation of each new leader.

## Revisit when
The judge measurement misses its bar, or climbs' final checks overturn the judge's winners more often than they confirm them; read in the measurement's recorded result and the climbs' pull request descriptions.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Related: 20261106-a-climb-designs-its-measure-and-search-for-its-task, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record, 20260901-design-skill-pair-distills-research-eval-deferred
