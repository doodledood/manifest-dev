# ADR: manifest-dev-help answers questions about manifest-dev in Simplified Technical English, held level with the glossary

## Status
Accepted

## Area
Positioning

## Decided by
The user

## Context
Users meet the workflow's own terms — recipe, verification harness, ask-first, Fit to Trust,
Lock, Debt — in run reports and in the pull request a project setup makes, and they cannot
follow them. No shipped text answers that. The glossary is this repository's `CONTEXT.md`,
which no installed skill can read and which also holds the words maintainers use about the
prompts. The READMEs explain the workflow but not its vocabulary, how the parts relate, or why
each exists. Adding a user-invocable skill is a decision under
20261013-new-capabilities-live-inside-the-four-workflow-entry-points.

## Decision
- The core plugin ships `manifest-dev-help`, a user-invocable skill that answers any question about
  manifest-dev, with the why: what it is for, its workflow, the autonomy ladder and how to climb it, every product term with why it
  exists, how the parts relate, the practices the skills encode, and what an artifact the workflow wrote
  means. Where its own text does not carry an answer, it reads the skill that owns the behavior and
  names the file it answered from.
- It is an optional extra in that record's sense: the workflow never depends on a user
  invoking it, and its description lets a host reach it when a user asks what a term means.
  The four entry points stay the only names a user must learn.
- It is written close to ASD-STE100 — about 90% of it: short sentences, one topic in each,
  simple words with one meaning — so a reader with any level of English reads one meaning in each
  sentence. The standard's approved dictionary and its ban on -ing forms are not applied, where
  they would cost natural wording.
- It is a hand-written copy of the glossary in a second register, not a link: a shipped skill
  cannot read this repository's `CONTEXT.md`, and in a user's project that file is the user's
  own glossary. Its entries add the why and the relations, which `CONTEXT.md` does not carry.
- It is kept in step with `CONTEXT.md` on every change to it: each of its entries records a
  fingerprint of the `CONTEXT.md` entry it was written from.
- The terms maintainers use only about the prompts stay out of it.
- The name is `manifest-dev-help`. It keeps the word a lost user reaches for, names the product it
  covers, and no host command takes it. A person who needs it is the one least likely to know a
  plugin-qualified name.

## Alternatives Considered
- **Link `CONTEXT.md` from the skill**: no installed skill can reach it, and a user's own
  `CONTEXT.md` is about their project.
- **Make `CONTEXT.md` the single source, rewritten in STE with a why line per term, and
  generate the skill's glossary from it**: drift becomes impossible, but every session in this
  repository loads `CONTEXT.md`, so the why lines would cost load on every turn.
- **`help`**: the first name a lost user types, but in an interactive Claude Code session the
  host's own `/help` takes it, and the user sees the host's help screen with no sign that this
  skill exists.
- **`explain`**: short, but the skill covers manifest-dev only, and a bare verb draws requests to
  explain anything.
- **`manifest-explain`**: no clash, but it names one act, and a user who is lost looks for help
  rather than an explanation.

## Consequences

### Positive
- A user can ask what any part is and why it is there, and get an answer from the plugin they
  installed.
- A change to a `CONTEXT.md` entry cannot land without someone rereading its entry in the skill.

### Negative
- The glossary exists in two registers. The test holds their names and their fingerprints;
  whether the meaning still agrees stays a review judgment.
- Only STE's counted limits are checked mechanically; the rest of its clarity is a review
  judgment.

## Enforced by
partly — `tests/test_manifest_dev_help_skill.py` fails when a `CONTEXT.md` term outside the
maintainer set has no entry in the skill or the skill defines a term `CONTEXT.md` lacks, when a
`CONTEXT.md` entry changes without the fingerprint in its entry, when a user-invocable core skill
is not named in the skill, and when the skill breaks STE's counted limits;
`tests/test_entry_points.py` holds the declared set with `manifest-dev-help` in it. Whether the
meaning agrees with `CONTEXT.md` stays judgment.

## Source
- Session: owner steering while finishing surfaces v5, after a user could not follow the
  concepts in the pull request a project setup made.
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points (an optional
  extra under it; its standing is unchanged)
- Related: 20261015-projects-drive-themselves-as-far-as-each-user-climbs
