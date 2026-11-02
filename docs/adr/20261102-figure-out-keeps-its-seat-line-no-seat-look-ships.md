# ADR: figure-out keeps its one seat line; no separate seat look ships

## Status
Accepted

## Area
figure-out

## Decided by
An agent in an unattended run, with no review — applying the rule below, which the user approved in the Manifest for this change after ruling that the form is chosen on evidence, cost included; the delegation covered applying that rule to the results, not changing it.

## Context

figure-out's spine carries one line for the person a read is for: start from the person the North
Star names, narrow to the slice and moment the artifact serves, then "take their seat and
enumerate every use they would make of it" (`20260914-who-its-for-is-consumed-by-figure-outs-seat-taking`,
amended by `20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants`).

In replays of one owner's product sessions, kept outside this repository, the owner had to steer
the agent on product judgment 18 times across feature and design sessions. A page that passed its
interface checks, its tests and four code reviews failed the next morning on journeys outside the
states its proposal described. A Ticket marked fully decided was built without asking what the
person gains. In those replays a separate review pass caught issues the authoring agent skipped.
That suggested moving the look from the person's seat out of the authoring context, into a
reference of its own that derives the person's journeys, walks them on the running product,
compares alternatives at each choice the person would notice against default product stances, and
returns the few findings that change the read.

The North Star's *Quality decides* principle holds that anything adding cost or wait to every run
earns its place by a gain shown on evidence
(`20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence`). Such a look runs on
every read a person will see.

## Decision

figure-out keeps its spine line unchanged and ships no seat look of its own: no seat reference, no
loading-table row for one, no default product stances. `tasks/FEATURE.md`'s *Their stories, not
ours* keeps pressing the seat per user story. Define's journeys gate
(`20261102-features-a-person-uses-are-driven-through-their-journeys`), which showed its gain, is
how a built feature is driven through the person's journeys.

Three forms were compared under a rule fixed before the runs. A form **shows a gain** when, on at
least one of the cases below, it passes by majority where main's line fails by majority; it fails
by majority on no case where main passes by majority; and the guard cases `14`, `98` and the
`draft-is-quick-and-unchecked` drive hold on it. Of the forms showing a gain, the cheaper ships
unless the costlier wins a case the cheaper loses; with none, main's line stays. The forms:

- **main** — the spine line alone.
- **fresh** — the look in its own fresh, isolated context, with eleven default product stances.
- **folded** — the same look taken inside the independent re-derivation figure-out already runs on
  reads costly to get wrong, starting no context of its own; a read the re-derivation skips keeps
  main's line.

Each case ran once per form, with up to two more runs where a pair did not settle, through the
`figure-out` recipe's scenarios, graded by a session that saw each reply under a letter label only,
with a 1–10 score for product decision quality. Cost is the session's reported cost; time is wall
time. `101` is one prompt; `102` to `104` are four-turn sessions in which a decision the person
meets arrives after three turns of engineering.

| Case | Main | Fresh | Folded |
|---|---|---|---|
| `101` offline downloads reached only from Settings | 0 of 2 | 1 of 3 | 0 of 2 |
| `102` invoice send failures only the team hears of | 3 of 3 | 1 of 1 | 1 of 1 |
| `103` an 8-hour session ending mid-essay | 0 of 3 | 0 of 3 | 1 of 3 |
| `104` report links that lock out the clients they are sent to | 2 of 3 | 0 of 3 | 1 of 3 |
| Mean score, cost, time over the cases | 6.3, $0.99, 206 s | 5.5, $1.15, 255 s | 6.7, $1.04, 219 s |

Neither form passed by majority on a case main failed by majority, and both failed `104` by
majority where main passed by majority. The folded form also failed guard `14` three runs of three.
Neither shows a gain, so main's line stays. On one-prompt cases (`94` to `97`), a fresh-context pass
scored 7.7 against 7.3 before it, inside run-to-run noise, at about a third more cost.

## Alternatives Considered

- **Ship the fresh-context look** — not chosen: it cost about a sixth more per read and a quarter
  more time, and lost `104` where main's line held.
- **Ship the folded look** — not chosen: in the long sessions the re-derivation that carries it ran
  in one run of seven, so it behaved like main's line, and it failed guard `14`.
- **Ship the eleven default product stances on their own** — not chosen: the stances were tested
  only inside the look; in the Taste test (`20261102-taste-entry-form-is-chosen-by-a-test`) a
  Taste entry on the skills before the change passed the same moments.
- **A new user-invoked product skill** — not chosen:
  `20261013-new-capabilities-live-inside-the-four-workflow-entry-points`.

## Consequences

### Positive
- No read pays for a second context or a reference whose gain was not shown.
- `101`, `103` and `104` stay as drives main's line does not pass reliably, so a later attempt has
  cases that can show a gain.

### Negative
- The failures in the Context remain open. In `103` every form named the student's loss and then
  recorded it as the owner's decision instead of proposing a change: the gap seen there is in
  proposing a change, not in seeing the person.
- One to three runs per form per case is a direction under the project's run rule, not a precise
  measure.

## Enforced by
none — whether a read takes the person's seat is judgment, measured only by drives of the cases above.

## Revisit when
A proposed change to how figure-out takes the person's seat passes `101` or `103` by majority where main's line fails it, without failing `104` or the guards; read in `claude-plugins/manifest-dev/evals/README.md` → *Is a seat look worth its cost — 2026-11-02*.

## Source
- Session: a `/do` run on a Manifest the user approved, 2026-11-02 (log kept locally). Drive summaries and blind grades are in the pull request that adds this record.
- Related: 20260914-who-its-for-is-consumed-by-figure-outs-seat-taking, 20261102-features-a-person-uses-are-driven-through-their-journeys, 20261102-experience-choices-go-to-the-user-as-options-or-variants, 20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence
