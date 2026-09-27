# ADR: Design spends the person's attention and names the defaults to avoid

## Status
Accepted

## Area
Design skills

## Context

After 20260924-design-starts-from-the-person-and-their-moment, the `design` skill produced varied, subject-led work, but its owner kept rejecting the same things in blind review: too many parts competing for attention, app screens showing every panel at once, drawn clip art standing in for imagery, pages that sat still, and the same cream or warm-brown ground on unrelated subjects.

A general instruction to avoid generic output does not fix this. The model swaps one default for its nearest neighbour; asked to avoid cream, it produced a darker "espresso" version of the same palette. Naming the specific patterns it falls into, while telling it that each is a default rather than a ban, gives it something concrete to steer away from without forbidding a pattern the subject calls for.

Rounds 5 to 12 continued the blind comparisons of the earlier record. Each round built the same briefs under two versions of the skill in isolated contexts, with a minimal outcome-only builder prompt, and the owner picked between shuffled, unlabelled results:

1. **Round 5:** a list copied from a published example of this technique banned patterns outright, including cream grounds that some subjects want. It was discarded. The replacement framing, "defaults to avoid, not rules", came from this round.
2. **Round 6:** the draft was no better than the shipped skill or no skill on a first draft; a work-tool brief looked poor in every version.
3. **Round 7:** attention as the budget, decided at each moment, a short list of overspending patterns, and a done condition that stops. It beat the shipped skill on 4 of 5 briefs.
4. **Round 8:** the opening adds what we want from the person alongside what they came to do. It tied (3 of 5), with visibly more distinct pages, and was kept.
5. **Round 9:** list entries for stillness and flat rendering. 4 of 5. The flat-rendering entry made builders draw more, not better.
6. **Round 10:** builders could now use photographs. The flat-rendering entry was replaced by drawn stand-ins for imagery; entries for changes that snap, more parts than the moment needs, and the same ground every time were added. 4 of 5. The version without the ground entry used a warm paper ground on three of five pages; the version with it used none.
7. **Round 11:** five app briefs. Walking the person's journeys first, and entries for everything visible at once, decoration standing in for hierarchy, and every surface on one plane. 4 of 5.
8. **Round 12:** entries for surface material (shadows, tonal gradients, translucency) and toy styling. 2 of 5; not adopted.

These results come from one judge, one model, five briefs per round, and HTML artifacts only. Builds of the same version varied widely, and run-to-run noise was not measured.

## Decision

The skill keeps the person-and-moment opening and adds, in order:

- **What we want from the person** — to understand, act, trust, come back — served together with what they came to do.
- **Attention as the budget.** At each moment, decide what matters most and give it the most. Find those moments by walking the person's journeys first — the first time, the everyday task, something gone wrong — so each step shows what that step needs and the rest stays one step away.
- **A named list of the ways designs most often go wrong**, stated as defaults to avoid rather than rules, each usable whenever the request asks for it or the subject and moment call for it: prose where a visual would carry the point, saying a thing twice, motion that keeps going, a page that sits still or changes that snap, effects that obscure content, drawn stand-ins for imagery, more parts than the moment needs, everything visible at once, decoration standing in for hierarchy, every surface on one plane, the same ground every time, and spectacle before the point.
- **A done condition that stops.** Looking once as that person at each of those moments, they get what they came for, we get what we wanted, it feels the way the moment asks, and nothing is left whose removal they'd miss. Further passes are refinement the requester can ask for.

The workspaces guide keeps the information for each decision together "and nothing that decision doesn't need", since its earlier wording read as permission to show everything.

## Alternatives Considered

- **A general instruction to avoid generic design:** swaps one default for its neighbour, the failure this record exists to address.
- **A list of banned patterns:** removed choices some subjects need; replaced by the defaults-to-avoid framing in round 5.
- **Entries for surface material and toy styling:** lost round 12, 2 of 5.
- **A rule specific to work tools:** the journeys and app entries cover the same failure while applying to every artifact.
- **Keep the shipped text:** lost round 7, 4 of 5, and every later version beat its predecessor or tied.

## Consequences

### Positive

- The failures the owner named — clip art, the habitual cream ground, crowded app screens, stillness — each have a named entry, and the builds show them receding.
- The done condition gives a first draft a stopping point without inviting endless self-review.
- The list grows by entry: a newly observed default is added as one named line rather than a rewrite.

### Negative

- Named lists improved each version relative to the previous one without reaching the owner's bar for overall finish. Results still read to the owner as flat or cartoonish; round 12, which aimed at that directly, did not help. Closing that gap likely needs a different lever than more entries.
- The list reflects one judge's rejections on one model. Entries may encode that taste or that model's defaults rather than something general, and a newer model may not share the defaults it names.
- Early rounds restricted builders to inline graphics, which contributed to the flatness being judged; results before round 10 mix the skill's effect with that restriction.
- Each entry is load on every design run. The list needs pruning when an entry stops describing what the model actually does.

## Source

- Session: blind A/B comparison rounds 5–12 of the design skill, continued from the series in 20260924-design-starts-from-the-person-and-their-moment.
- Related: amends 20260924-design-starts-from-the-person-and-their-moment; see also 20260925-design-composes-artifacts-and-creative-directions.
