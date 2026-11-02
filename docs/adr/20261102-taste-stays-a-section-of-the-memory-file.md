# ADR: Taste stays a section of the memory file until it outgrows one

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context

Ratified Taste entries are written into a marked `## Taste` section of a memory file: the
user-level one for how a person likes things everywhere, the project context file for how a
project does things (`20260719-taste-persists-by-offer-and-ratify`). That record weighed a
dedicated Taste file and set it aside for the initial shape, leaving extraction as a later
refactor if the section sprawls. It named no point at which to look again.

The question came back when Taste gained more writers and more weight: setup now mines entries
from a project's history (`20261102-setup-offers-taste-entries-mined-from-stated-reasons`), and
the Taste test considered a case line per entry, which would have made each entry longer
(`20261102-taste-entry-form-is-chosen-by-a-test`). A file of its own would be tidier: one home for
the entries, easier to curate, and a writer that owns the whole file instead of one section of a
shared one.

What gives an entry its effect is that it is loaded in every session when a call comes up; the
Taste check at each user's call reads only what is loaded. Every host manifest-dev ships for —
Claude Code, Codex, OpenCode, Pi and Cursor — loads its own context file, so a section inside that
file is resident everywhere. A separate file is resident only where the host imports files into
its context file. Elsewhere it is only as strong as a line telling the session to read it at
start, which a session can skip. Which hosts besides Claude Code import files was not checked when
this was decided. Setup already handles the North Star this way: imported where the host supports
it, read at session start otherwise.

At the time of this decision the largest Taste sections in use held five entries each, this
repository's among them, a few lines inside context files of a few hundred.

This decision sits inside what the North Star's *Purpose* names: keeping the choices a person
retains available to later sessions without restoring them each time.

## Decision

Taste entries stay in a `## Taste` section of the memory file they target, the user-level memory
file or the project context file, and no skill writes them to a file of their own. The section
stays until there is evidence that it grows large enough to bury the rules around it.

## Alternatives Considered

- **A `TASTE.md` of its own, imported from the context file** — not chosen now. On hosts without
  imports it trades guaranteed residency for a read instruction, and residency is what makes an
  entry steer. The tidiness it buys is small while sections hold a handful of entries. It would
  also cost a new setup-project surfaces version (the template, the import line, moving existing
  sections, an upgrade guide) and a change to every skill that writes or reads Taste: figure-out,
  define, do, done, escalate, run-ticket, setup-project's mining and the help glossary.
- **Only add a `Revisit when` line to the 20260719 record in place** — not chosen: the grounds have
  changed since it was written (residency on hosts without imports, more skills that write Taste),
  and an in-place line would leave them recorded nowhere.

## Consequences

### Positive
- Every entry is resident on every host the plugin ships for, with no import support needed.
- No surfaces version, migration or skill change.

### Negative
- Taste shares space with project rules, and a writer must change only its own section of a shared
  file.
- A long section would crowd the context file before anyone notices; the signpost below is the
  only thing that makes that visible.

## Enforced by
partly — `tests/test_shared_blocks.py` pins the user's-call block, which reads entries from "a `## Taste` section of a loaded memory file", word for word in every skill that states it; where an entry is written stays prompt wording in `figure-out/references/TASTE.md` and the other skills that draft entries.

## Revisit when

Any one of these holds:

- A `## Taste` section grows past roughly a screenful or starts to bury the
  project rules around it. Read in the `## Taste` section of this repository's `CLAUDE.md`, and in
  a user's report about their own project or user-level memory file.
- Every host the plugin ships for imports files into its context file, so a separate file loses no
  residency. Read in each host's documentation for its context file; the hosts are the ones
  `dist/` packages for, plus Claude Code.
- A change gives Taste entries a structure that one section of a shared file holds poorly, such as
  fields per entry or worked examples. Read in the pull request that proposes that structure.

## Source
- Session: a `/figure-out` and `/do` session on product judgment, 2026-11-02, where the owner agreed there is no need for a separate Taste file until there is evidence the section gets huge.
- Related: amends 20260719-taste-persists-by-offer-and-ratify (adds the condition for revisiting its rejected dedicated-file alternative); see also 20261102-taste-entry-form-is-chosen-by-a-test, 20261102-setup-offers-taste-entries-mined-from-stated-reasons
