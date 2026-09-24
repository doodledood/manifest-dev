# ADR: figure-out settles an artifact's own person before drafting, and shows variants while the visual direction is undecided

## Status
Accepted

## Area
figure-out

## Context

figure-out's spine sends a session into the seat of the person the North Star names under *Who it's for* whenever the read implies making something. That person is the whole project's audience. A specific artifact usually serves a narrower slice of them in one moment: a pricing page serves someone already comparing prices, and a release deck serves existing users checking what changed.

The design skill now works from exactly that slice and moment. It asks who is here, what they came to do, and how long they will stay. It also lets the request set how strongly the artifact should make them feel something. figure-out's draft step passed the design skill only the iteration's question and rough fidelity, so neither the person nor any stated strength reached it.

The draft step also defaulted to one artifact, a default set in PR #327, with variants only on request. In the blind comparisons behind `20260924-design-starts-from-the-person-and-their-moment`, the judge ranked deliberately different pages readily and was unsure when the options were close. Prompts that differed without aiming at a specific difference converged on the same concept for a given brief. In the same comparisons, a prompt that had the model reason out a feeling and a guardrail produced plainer work.

## Decision

figure-out's spine changes in two places, both as clauses on existing bullets:

1. **The seat names the artifact's own person.** Start from the North Star's *Who it's for*, then name the narrower slice and moment the artifact serves where it has one, and take that seat.
2. **The draft step settles the person, then shows the choice.** Before the first draft, settle what that person came to do and what we want from the artifact, asking only what the conversation has not answered. Do not ask for a feeling in the abstract. A visual draft whose direction is still open opens with two or three variants. Each variant gives a different answer to the open choice, either how it should feel and how strongly, or the visual idea. The variants share the same content and sit side by side with a way to switch. After the user chooses, the loop continues with one artifact. The design skill receives the person, their moment, and our goal, along with any feeling or strength the user named. It also receives the difference each variant explores, and the question and fidelity for the iteration as a whole.

Non-visual drafts and visual drafts whose direction is settled keep the one-artifact default.

## Alternatives Considered

- **A design probe file in figure-out's task files:** probe files carry angles the model forgets. This gap is an input missing at a handoff, and the seat rule already lives in the spine for the reasons its record gives.
- **Ask for the intended feeling before drafting:** the blind comparisons found that a model-reasoned feeling brief produced plainer work. A choice between variants lets the user answer by reacting to concrete options.
- **Variants without a named difference:** in the blind comparisons, pages from prompts that named no difference converged on the same concept, which gives the user near-copies to choose between.
- **Keep one draft for every case:** cheaper, but it asks for a taste judgment without a comparison at the point where the direction is least settled.

## Consequences

### Positive

- The design skill receives the person and moment it is written to work from.
- The first visual choice becomes a comparison between distinct options.
- A feeling or strength the user states reaches the design skill, and otherwise the variants surface it.

### Negative

- The first draft round of an open visual direction costs two to three times as much.
- The change is untested in a live figure-out session.
- Variants still depend on naming a real difference; if they converge anyway, one draft with a pointed question would serve better.

## Source

- Amends 20260914-who-its-for-is-consumed-by-figure-outs-seat-taking: the seat rule and its placement stand; who sits in the seat now narrows to the artifact's own audience.
- Related: 20260924-design-starts-from-the-person-and-their-moment
