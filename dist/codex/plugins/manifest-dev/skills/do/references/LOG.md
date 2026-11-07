# /do: execution logging

The execution log is what lets a run survive context loss and lets a later session audit it.
Execution history lives here, never in the Manifest, which stays the acceptance contract.

## Path

Use the path `SKILL.md` names, resolved before execution starts and surfaced at once. Create the
directory (`~` = `$HOME` / `%USERPROFILE%`), and fall back to a writable temp path only when the
home directory is not writable. The first line is a title naming the Manifest's topic, and the
next names the repository it is about — its remote URL, or its path when it has none — so a later
session's recall can match logs by repository and topic.

When a caller supplies a journal path (for example, the default `/babysit-pr` journal), that
caller-supplied journal *is* the log, and the run's record goes nowhere else. Append one line to
the path `SKILL.md` names pointing to that journal, so a launch on this Manifest without the
caller — after compaction, in a new session, or resuming an escalation — opens that path, follows
its newest pointer and reads the journal. When the caller reinvokes `/do` on it for
a new run, append a `Run initialized` boundary. Recheck the applicability of prior evidence
against the current criteria and subject before carrying it forward. Preserve supported finding
dispositions and verified repairs; a new invocation alone does not erase them.

## Discipline

Append only; correct an old entry with a new one. Read the log before deciding a retry in a
resumed run, and append after meaningful events, not play-by-play. Credentials, tokens and
personal data never enter it — it outlives the run and travels by path — so record where a secret
lives, never its value.

## What a resumed run needs from it

Record what the finished state will not reconstruct on its own:

- **Decisions** — material autonomous choices with their rationale, each reopened decision
  record first with the reason set aside and what reversing would cost, then the user's calls (as
  `SKILL.md` defines them), each with the alternative not taken and what decided it; any
  Appetite revision with its benefit and added complexity.
- **Blockers** — the obligation, the evidence, the intervention needed, and whether it cleared.
- **Departures** — from the Initial Approach, the Deliverable order or a Process Guidance item,
  and why.
- **Dead ends** — fixes tried and reverted, approaches rejected that left no commit; group repairs by their underlying promise and its accepted source, with each attempt and outcome, so new finding IDs or commit wording do not reset the premise history.
- **Outcome and gate state** — assessed criteria, as the Manifest hash that *A changed Manifest*
  below names, and subject, verdicts and their evidence, staleness, and
  whether each judgment gate has taken its full look under its current criteria. Identify relevant local work and external
  observations as well as the repository head. Keep the findings, their dispositions and support,
  and which repairs are verified, so a resumed run can determine what evidence still applies and
  what each continued evaluation must check.
- **Amendments** — what changed, the source authority, why a working revision better served the unchanged Outcome and hard requirements, and which evidence it invalidated.
- **Met on the way** — each pre-existing issue and below-bar finding met, where it came from, and
  whether it was fixed, applied, dismissed with the reason, or left from a continued look; each gigantic issue with why it is a
  project of its own; and a gate bar the run read as suspect with how that settled.
- **Operational steps** — retriggers, waits and environment actions.

## A changed Manifest

`define` rewrites the Manifest in place and the Manifest carries no version, so the log is what
tells a resumed run whether a verdict read the text that stands now. Record with each verdict the
SHA-256 of the Manifest file it was assessed against. Before invoking `define`, append an
`Amendment pending` entry carrying the current hash; after re-reading the result, close it with
the new hash and the gates whose criteria — their text and every Manifest section their claim
reads — changed. On resume, hash the Manifest. A verdict carrying the current hash assessed the
current criteria; one carrying an older hash did too only where closed amendments lead from its
hash to the current one without changing that gate's criteria, and is otherwise unverified. A
pending entry left open means its amendment may not have landed: re-read the Manifest and confirm
it, or make it again.
