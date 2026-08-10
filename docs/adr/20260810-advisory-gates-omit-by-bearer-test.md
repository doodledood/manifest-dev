# ADR: Advisory gates omit by a bearer test at define time

## Status
Accepted

## Area
define

## Context

A manifest's verification cost decomposes as per-round cost times round count
(20260810-no-verifier-model-granularity). The Ratchet bounded the multiplier
(20260805-ratchet-judgment-gate-reverification); what remains is the per-round floor: a code
manifest fields thirteen judgment-gate readings, each reading the whole change, at a cost
roughly invariant to diff size. That floor is proportionate on a large feature and
disproportionate on a small fix — small runs carry the worst verification-to-work ratio in the
system, and they are also where the findings are worth least, because judgment-gate findings
are generated rather than enumerated: a capable reviewer produces one more defensible Medium
on any non-trivial diff, however good the work, and each marginal Medium buys a repair round.

Two prior positions frame the tension. 20260810-no-verifier-model-granularity recorded
"drop advisory dimensions from the default gate set" as the one cost lever with real mass that
does not return as repair rounds — and recorded the maintainer rejecting it wholesale as a
quality cut. Separately, `/define` already holds an omission valve for task-file Quality Gates
("omit clearly inapplicable with stated reasoning") and already names Appetite as the criterion
for "how much to gate beyond what task files supply" — an authority that stopped just short of
the auto-encoded task-file set itself.

The initial proposal keyed omission to predicted model competence — drop gates the model
"will likely do a good enough job on by itself." Analysis inverted it: a gate the model
satisfies passes its one full look and never buys a repair round, so dropping it saves an
addend; the expensive gates are the ones that fail with marginal findings, which they do
regardless of how good the work is. The selector had to key on the manifest, not the model.

## Decision

Widen `/define`'s existing task-file omission valve: an advisory-tier Quality Gate may also be
omitted when the manifest's surface and stakes leave that dimension's findings without a real
bearer. The criterion is a **bearer test**:

Each advisory dimension protects a specific future activity — maintainability, simplicity, and
design fitness protect future modification; testability and test quality protect future
regression-catching; docs and prose value protect future readers; operational readiness
protects production operation; context-file adherence protects the next contributor meeting
consistent code. **The gate stays when that activity will actually occur on this manifest's
surface within the artifact's life; it drops when the costs its findings would name have no
bearer, or the bearer's exposure is trivial.** A one-shot internal script has no future reader,
so docs drops; code scheduled for deletion has no future modifier, so maintainability drops; a
one-line change on a payment path keeps the full sweep despite its tiny Appetite, because
bearers are everywhere on it. This is the same move the advisory severity floor made at
verification time — a Medium must name the concrete cost that earns the grade — applied one
step earlier: at encoding time, ask whether any such cost could have a bearer here.

Operating rules:

- **The full set is the default and doubt includes.** Omission is the argued exception, never
  the baseline.
- **A stated judgment test, not Appetite bands.** Any rule keyed to size alone misfires on the
  small-surface, high-stakes edge; the test weighs surface and consequence together.
- **Every omission logs the missing bearer as a fact** — "no future reader exists",
  "scheduled for deletion" — never a probability judgment ("unlikely to find much"). This is
  what keeps the valve safe to operate unsupervised.
- **The valve operates on autonomous runs too**, where cost bites hardest; the fact-based
  logged reasoning is the post-hoc audit there. On attended runs the user reviews the resulting
  gate set at summary approval.
- **Never eligible:** the four defect-finding dimensions, deterministic project gates,
  safety-critical Global Invariants, and the ceiling invariant. Thresholds never move, and
  verification independence never downgrades — the correctness floor is not where the taste
  churn comes from.
- **A mid-run discovery that an omitted dimension had a bearer** is evidence the encoding
  judgment failed — routed as an amendment or escalation like any other manifest gap, never a
  silent re-add or a silent skip.

This narrows, and does not reverse, 20260810-no-verifier-model-granularity's recorded
rejection: dropping advisory dimensions from the *default set* stays rejected; what is now
permitted is per-manifest omission of the gates whose findings would land on nobody.

## Alternatives Considered

- **Key omission to predicted model competence** (the original framing): rejected. It
  identifies the gates that are cheap to keep — likely passes cost one reading — while the
  cost mass sits in gates that fail with marginal findings, which a competence predictor
  cannot identify because judgment finding spaces stay generative over good work.
- **Appetite bands** ("below N files, drop the advisory tier"): rejected. Bands cannot see
  stakes, so they fire wrong exactly on the small-but-critical edge that most needs the full
  sweep.
- **Structural absence as the sole criterion** (omit only when the surface contains none of
  the dimension's material — the stricter form an independent re-derivation of this decision
  proposed): rejected as the whole test. It is strictly contained in the bearer test and
  misses the lifetime and exposure cases — deletion-scheduled code, one-shot artifacts — that
  carry much of the waste. Its unsupervised-safety concern is absorbed instead as the
  fact-not-probability logging rule.
- **Run small manifests in consolidated verification mode**: rejected. Already available as a
  run-level flag; it saves only repeated orientation, still fields every advisory reader, and
  those readers still generate the marginal Mediums that buy repair rounds.
- **Do nothing — the bill is the price** (the position 20260810-no-verifier-model-granularity
  recorded): rejected for the per-manifest case. A diff-size-independent floor charged against
  surfaces whose findings have no bearer is spend that buys no quality, which the project's own
  stance names a workflow defect; the wholesale rejection stands.
- **Restrict the valve to attended runs**: rejected. Unattended runs are where verification
  cost concentrates; disabling the valve there guts it where it earns most, and the fact-based
  omission log keeps autonomous drops auditable after the fact.
- **Hold a core advisory subset that never drops** (e.g. simplicity, maintainability):
  rejected. The correctness floor is already held by the never-eligible gates, and a held core
  re-imports fixed overhead onto exactly the runs the valve exists to relieve.

## Consequences

### Positive

- Small-surface runs shed both the fixed advisory reading floor and the marginal-finding
  repair rounds — the two costs this session traced to gates whose findings land on nobody.
- The quality bar is untouched where it is real: every dimension with a bearer still encodes,
  the correctness floor never drops, and thresholds do not move.
- Omissions are auditable from the manifest alone — each names the missing bearer as a fact a
  reviewer can check.
- No new machinery, fields, or flags: the change recalibrates an existing omission valve and
  extends an authority (Appetite's) `/define` already holds.

### Negative

- The saving is reasoned from billing and round mechanics, not measured; no post-Ratchet
  cost distribution exists to confirm how much mass the valve actually reaches.
- An encoding-time misjudgment — a bearer that existed but was not seen — removes a reading
  that would have caught something, and the loss surfaces only downstream. The
  fact-not-probability rule and doubt-includes default lean against it; nothing detects it.
- `/define` gains a judgment surface under cost pressure. Drops appearing on large-surface or
  high-stakes manifests would mean the test is misfiring and needs hardening — that is the
  overturn signal to watch.
- On autonomous runs the audit is post-hoc only.

## Source

- Session: figure-out investigation, 2026-08-10 — ADR corpus, `/define`'s encoding rules, and
  `CODING.md`'s gate set read at source; independent evidence-only re-derivation run, which
  converged on the lever's location and the never-eligible floor and proposed the stricter
  structural-absence criterion recorded above.
- Related: 20260810-no-verifier-model-granularity (narrows its recorded wholesale rejection),
  20260805-ratchet-judgment-gate-reverification, 20260728-bound-the-acceptance-contract-from-above,
  20260808-restore-per-gate-default-verification-mode
