# ADR: A help skill explains manifest-dev in Simplified Technical English, held level with the glossary

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
- The core plugin ships `help`, a user-invocable skill that explains manifest-dev: what it is
  for, its workflow, the autonomy ladder and how to climb it, every product term with why it
  exists, how the parts relate, and the practices the skills encode.
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
- It is kept in step with `CONTEXT.md` on every change to it: each help entry records a
  fingerprint of the `CONTEXT.md` entry it was written from.
- The terms maintainers use only about the prompts stay out of it.
- The name is `help`. In an interactive Claude Code session, the host's own `/help` command
  takes the bare name, so there the skill is reached by its plugin-qualified name or by its
  description. Codex and Pi have no such clash.

## Alternatives Considered
- **Link `CONTEXT.md` from the skill**: no installed skill can reach it, and a user's own
  `CONTEXT.md` is about their project.
- **Make `CONTEXT.md` the single source, rewritten in STE with a why line per term, and
  generate help's glossary from it**: drift becomes impossible, but every session in this
  repository loads `CONTEXT.md`, so the why lines would cost load on every turn.
- **A name no host built-in can shadow, such as `manifest-help`**: the owner asked for `help`.
  The qualified name and the description still reach it where the bare name is taken.

## Consequences

### Positive
- A user can ask what any part is and why it is there, and get an answer from the plugin they
  installed.
- A change to a `CONTEXT.md` entry cannot land without someone rereading its help entry.

### Negative
- The glossary exists in two registers. The test holds their names and their fingerprints;
  whether the meaning still agrees stays a review judgment.
- Only STE's counted limits are checked mechanically; the rest of its clarity is a review
  judgment.

## Enforced by
partly — `tests/test_help_skill.py` fails when a `CONTEXT.md` term outside the maintainer set
has no help entry or help defines a term `CONTEXT.md` lacks, when a `CONTEXT.md` entry changes
without its help entry's fingerprint, when a user-invocable core skill is not named in help, and
when help breaks STE's counted limits; `tests/test_entry_points.py` holds the
declared set with `help` in it. Whether help's meaning agrees with `CONTEXT.md` stays judgment.

## Source
- Session: owner steering while finishing surfaces v5, after a user could not follow the
  concepts in the pull request a project setup made.
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points (an optional
  extra under it; its standing is unchanged)
- Related: 20261015-projects-drive-themselves-as-far-as-each-user-climbs
