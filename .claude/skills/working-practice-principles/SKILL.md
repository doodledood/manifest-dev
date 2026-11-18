---
name: working-practice-principles
description: 'Working-practice principles for manifest-dev: how its maintainer wants any change in this project carried out, and why. Use before making any change in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- A job that costs money, runs long or reaches outside the project is first run on a small sample, and that sample's result is read, and shown, before the full run — a fault found on ten items costs ten. Yields when the job cannot be split.
- Work on the project that can be undone goes ahead without waiting; an act that cannot be undone, that reaches people outside the project, or that spends money waits for a named person, whose approval is recorded with the work — waiting on reversible work wastes that person's time, and acting alone on irreversible work spends their trust. Yields where the person delegated that kind of act in advance, in words that name it.
- Work is sized and ordered by people's demand and by constraints beyond the build itself — reviewers' time, money, another party's wait — and never by the amount to be built, though the larger version still lands as thin slices — where building costs little next to review and waiting, holding finished work back for a batch gains nothing. Yields when a deadline outside the project fixes the scope.
- The owner chooses the overall look and flow from rendered options, while the smaller design decisions are taken on their behalf and listed for them — two people can agree on a description and picture different things, and an owner judges best by looking. Yields for a decision that alters what people are able to do or are charged, which goes to the owner.

Before calling any work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
