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
caller-supplied journal *is* the log — no second file. When the caller reinvokes `/do` on it for
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
- **Dead ends** — fixes tried and reverted, approaches rejected that left no commit.
- **Gate state** — assessed criteria and subject, verdicts and their evidence, staleness, and
  whether each judgment gate has taken its full look. Identify relevant local work and external
  observations as well as the repository head. Keep the findings, their dispositions and support,
  and which repairs are verified, so a resumed run can determine what evidence still applies and
  what each continued evaluation must check.
- **Amendments** — what changed, which gates it unverified, and the assumptions it added.
- **Met on the way** — each pre-existing issue and below-bar finding met, where it came from, and
  whether it was fixed, applied or dismissed with the reason; each gigantic issue with why it is a
  project of its own; and a gate bar the run read as suspect with how that settled.
- **Operational steps** — retriggers, waits and environment actions.
