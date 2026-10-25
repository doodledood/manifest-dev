# define eval suite

Measures whether `define` encodes a Manifest by the disciplines its own prompt states: not
whether it writes a document shaped like a Manifest, which only the with-plugin arm can do and
which would therefore make every case a vanity win.

A run is many model sessions: the owner runs it, or an agent runs it after asking, naming the
cases and why. A prompt change marks the cases it covers stale rather than running them, as
`../README.md` → *Scope and statuses* says. Run it from the repository root, through the script
`../README.md` → *Running a suite* describes:

```bash
scripts/evals/run_eval.sh define evals/results/define/aggregate-result.json \
  --tag define --ablation with-without --judge-model sonnet --scaffold -j 8 --max-cost-usd 65
```

`--max-cost-usd` stops scheduling at an estimate, with in-flight overshoot; see [the run contract](../READINESS.md).

`--scaffold` runs the `scaffold.sh` that `d16`, `d17`, and `d20`–`d24` declare in their `case.yaml`: a
saved Manifest beside a small repository for `d16`, a small project for the others. Without it,
those cases run against an empty directory and measure nothing. Only pass it for case files from this
repository: a scaffold is bash that runs as you.

This suite's scope and the meaning of each case's status are in the figure-out suite's README
(`../README.md`, *Scope and statuses*). The headline number is **Δ**, the with-plugin score minus
the no-plugin baseline. Read the figure-out suite's README (`../README.md`) before trusting a Δ
from this one: its rules on decomposing Δ by arm, the noise floor, and changing graders apply here
unchanged.

**The judge is sonnet, at one run per arm**, by the owner's call on 2026-10-15, for the reason
`../README.md` gives: the suites are a cheap proxy for direction, and their noise is worked with
rather than bought down. The risk on record is sharper here. The CLI's judge must reply with one
word, PASS or FAIL, with no room to reason on the page, and on a 20k-character Manifest a sonnet
judge once failed a sound Manifest on nearly every vote, where an opus judge matched known answers.
The graders have since been rewritten to classify before judging, which that check predates. So
before acting on a FAIL from a grader that reads the whole Manifest, read the Manifest it failed.
Numbers judged by different models do not compare.

See [READINESS.md](../READINESS.md) for the 2026-10-24 repairs and evidence limits. Changed
prompts and rubrics are a new instrument; historical results below do not measure it.

## Cases added 2026-10-13 to 2026-10-19

| Case | Discipline under test |
|---|---|
| `d20-preparatory-slice` | When the touched area resists the change, a behavior-preserving restructuring comes first |
| `d21-user-rule-over-default` | A rule the project states overrides a conflicting task-file Default, and the adjustment is recorded |
| `d23-unfit-recipe-repaired-first` | A change touching a feature whose recipe cannot be relied on — started by hand on a fixed port, its last failure unexplained — cuts repairing that recipe as the first Deliverable, and gates that the touched recipe is updated and run. It carries `d18-map-gate`'s grader: same prompt and project, so `d18` was retired into it on 2026-10-15 |
| `d24-own-check-repaired-first` | With no harness, a touched test of the project's own that passes whatever the output is gets repaired in pytest form by the first Deliverable, and no harness is built. The project-own twin of `d23`, and the define half of figure-out's `55` |
| `d25-vague-target` | A speed want with no number and no profile ("make the preview fast", about 25 fps today) binds a floor such as faster than the measured baseline, never an invented frame rate; a higher number may appear only as an advisory aim, even when recorded as an assumption. Its own grader is `floor-not-invented-target` |
| `d26-holes-that-pass-every-gate` | A read of an invoice worker whose design a model already checked still leaves the spec open to wrong results that pass every gate at once: a job marked sent while no invoice was delivered, and an invoice sent twice when the old worker is stopped mid-send during the switch. Its own graders, `no-sent-without-delivery` and `no-double-send-at-switch`, judge whether the spec's gates close those two paths |
| `d22-projectless-manifest-builds-no-harness` | A one-off script outside any project gets a Manifest whose gates check its output, with no harness, recipe, decision record or setup. A guard: the no-plugin arm is expected to pass it, so a Δ of zero is no reason to remove it |

Their first both-arm run was the 2026-10-25 baseline below; it and the three-run re-runs it calls for decide which stay. **Every number below is stale
as of 2026-10-19**: the 2026-10-13 change edited define's spine and its task files, the
2026-10-14 change moved its verification wording to one harness, the 2026-10-15 change made
that harness optional and the project's own checks a run's to repair, and the 2026-10-18 change
made define ask through the host's question capability by default, batching its key calls, and
added the proof gate to its pull-request task file. A second 2026-10-18 change made define hand
each new Manifest to a fresh context for review before its digest, list every bound number in the
digest, and encode a target whose reachability the session did not establish as a binding floor
plus an advisory aim — which reaches every case that writes a spec, `d05` and `d10` most. The
2026-10-19 change added Defaults to the coding and performance task files — check a design whose
correctness depends on the order of events by a check that can reach it, model it first, ask
whether a crashing state is legitimate before guarding it, bound a gain by the changed piece's
share — and a *Fit to trust* job, and had the review name for each gate a plausible wrong result
it would fail; that reaches every coding case, `d20`, `d23` and `d24` most. A second 2026-10-19
change had the review also search each new Manifest for holes — wrong results that pass every gate
at once — which reaches every case that writes a spec, and runs inside each case's existing turn
and time limits. Before trusting the numbers from the first both-arm run after it, check that no
spec case now ends at one of those limits. The 2026-10-21 change made the North Star a
values-and-goal document and moved `d23`'s project to surfaces v8, which reaches `d23` only through
its scaffold; a later change that day shipped v9 and moved it again, the same way. The next
baseline replaces them.

The 2026-10-22 change sharpened the coding sketch Default to keep plausible changes local,
weighed against added complexity. Its encoding is not graded by a define case; figure-out's
`40-shape-before-build` grades the design distinction before encoding, rather than duplicating
that scenario here. The affected coding cases were first measured in the 2026-10-25 baseline; earlier results are stale.

The 2026-10-24 change removed the task file's stale claim of mandatory late advisory review and
allowed reasoned declines of correct but optional PR comments. These affect executor guidance;
the define suite does not measure repeated review or external-feedback convergence. The `do`,
`review-code`, `check-pr`, and `babysit-pr` recipes carry unmeasured scenarios for those behaviors.
Earlier define measurements are stale; the 2026-10-25 baseline replaces them.

The 2026-10-24 research change makes delegation conditional on the inquiry, permits direct
source inspection by the coordinator, and removes the web overlay's duplicate prescription.
No case in this suite grades that research guidance. The `define` recipe's `research-delegation`
drive covers its encoding and remains **unmeasured**; its fixture check does not establish model
behavior or research quality, and the 2026-10-25 baseline does not cover it.

The review runs in a fresh context, which this suite's sessions cannot start, so define reviews
its own Manifest here and says the review was self-graded. No case holds the per-gate wrong-result
question; the `define` recipe's `fresh-review` drive checks it instead. `d26` holds the search for
holes on that self-graded path, graded by whether the spec closes two holes the search found in the
2026-10-19 experiment; the `define` recipe's `hole-search` drive puts the same prompt through the
fresh-context path. The other 2026-10-19 Defaults have their cases in
the figure-out suite (`56` to `58`), where the same probes are asked before a Manifest exists, and
a define case for each would test the same probe twice at twice the runs. The
headless harness offers no question capability, so the cases measure define's plain-text path. A single 2026-10-14 drive of `d01` (not a measurement) found define keeping the
requested layer cut as a user's call; define's slicing rule now says a requested cut is never one,
and a re-drive came back re-cut (that drive's evidence is not kept in the repository).

## Baseline — 2026-10-25, sonnet judge, agent at medium effort

The first measurement of the instrument repaired on 2026-10-24 ([READINESS.md](../READINESS.md))
and the first run of `d20`–`d27`. It is the number the next hill-climb is measured against; no
older result in this file compares with it.

Report `results/base-20261025/define.json`. Skill at `0b7da43`, CLI 2.1.310, agent
`claude-opus-5-5` at effort `medium`, judge `claude-sonnet-5-5` (three votes per LLM grader), one
run per arm, 2026-10-25. `claude plugin eval` has no effort option, so the run set
`CLAUDE_CODE_EFFORT_LEVEL=medium`, which reaches every session it starts and so puts the judge at
`medium` too. No run errored, none was partial, and no run ended at its turn or time limit.
List-price cost $37.70 for 40 trials. The split was frozen before any output was read: held out
`d04`, `d06`, `d08`, `d27`; every other case tuning.

| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| d01-layer-cut | tuning | 0.50 | 0.50 | +0.00 |
| d02-outcome-not-mechanism | tuning | 0.60 | 0.60 | +0.00 |
| d03-class-not-instances | tuning | 0.50 | 0.50 | +0.00 |
| d04-unsafe-binds | held out | 0.50 | 0.75 | -0.25 |
| d05-conflicting-goals | tuning | 1.00 | 1.00 | +0.00 |
| d06-subjective-anchor | held out | 0.75 | 0.75 | +0.00 |
| d07-neg-no-problem | tuning | 1.00 | 0.00 | +1.00 |
| d08-neg-small | held out | 0.50 | 0.50 | +0.00 |
| d09-amend-widen | tuning | 0.00 | 0.00 | +0.00 |
| d10-loop-bait | tuning | 0.50 | 0.75 | -0.25 |
| d16-approved-means-handoff | tuning | 1.00 | 1.00 | +0.00 |
| d17-taste-in-encoding | tuning | 0.67 | 0.78 | -0.11 |
| d20-preparatory-slice | tuning | 1.00 | 1.00 | +0.00 |
| d21-user-rule-over-default | tuning | 1.00 | 0.00 | +1.00 |
| d22-projectless-manifest-builds-no-harness | tuning | 1.00 | 1.00 | +0.00 |
| d23-unfit-recipe-repaired-first | tuning | 1.00 | 0.50 | +0.50 |
| d24-own-check-repaired-first | tuning | 1.00 | 0.00 | +1.00 |
| d25-vague-target | tuning | 0.75 | 0.50 | +0.25 |
| d26-holes-that-pass-every-gate | tuning | 0.60 | 0.40 | +0.20 |
| d27-explicit-target | held out | 1.00 | 1.00 | +0.00 |

Mean over the 20 cases: with **0.74**, without **0.58**, **Δ +0.17**. Tuning (16 cases) +0.22;
held out (4 cases) 0.69 against 0.75, -0.06.

What the baseline shows, as a direction rather than a verdict on any one case:

- **The uplift comes from the rules only the plugin carries:** a project rule over a Default
  (`d21`), repairing an unfit check first (`d23`, `d24`), and not inventing a problem (`d07`).
  `d25` and `d26` gain smaller amounts.
- **`no-invented-thresholds` failed all ten judged runs in both arms**, unanimously. A grader no
  output passes measures nothing yet. The CLI flags its input as long (one Manifest ran to 28k
  characters), the risk *Known limits* names. Read the failing Manifests before treating it as a
  skill failure or tuning against it.
- **`gates-are-settleable` passes 4/10 with the plugin against 9/10 without.** It is the plugin
  arm's loss on `d04` (the held-out drop) and `d17`, and it fails beside other graders on `d01`–`d03`
  and `d26`. This is the first hill the baseline names, after the threshold grader is read.
- **`d10` loses on `bounds-the-open-ends`**, which only the plugin arm fails.
- **`d09` scores 0 in both arms** on `widens-not-siblings`: a hill, or a rubric no output meets.
- **`d01`–`d03` and `d08` show no Δ.** `d02` and `d03` are the retirement watch under
  *Classification*; this run repeats the pattern on one run, so their three-run re-run decides.

## First measurement of `d11`–`d17` — 2026-10-12

CLI 2.1.296, agent `claude-opus-5-5`, judge `claude-opus-5-5`, 6 runs per arm, skill at
`4d7b988` (`d16`'s row is its re-run at `802e81e`, after the fixes below). 84 runs, $127, about $1.52 a run.
These cases only; `d01`–`d10` are not re-recorded yet.

| Case | With | Without | Δ | What separates the arms |
|---|---|---|---|---|
| `d11-experienced-wait` | 0.92 | 0.42 | +0.50 | shared graders only; `gates-the-experienced-wait` 6/6 in both arms |
| `d12-true-not-present` (held out) | 0.92 | 0.38 | +0.54 | shared graders only; `gates-truth-and-edges` 6/6 in both arms |
| `d13-owner-keeps-the-yes` | 1.00 | 0.57 | +0.43 | shared graders only; both case graders 6/6 in both arms |
| `d14-small-but-risky` | 0.96 | 0.50 | +0.46 | shared graders only; `keeps-the-defect-checks` 6/6 in both arms |
| `d15-amend-outside-delegation` (held out) | 1.00 | 1.00 | 0.00 | nothing: both arms keep the rule and raise the blocker on every run |
| `d16-approved-means-handoff` | 1.00 | 0.33 | +0.67 | `stops-at-the-handoff` 6/6 against 1/6; `layout-unchanged` 6/6 against 3/6 |
| `d17-taste-in-encoding` | 0.93 | 0.63 | +0.30 | `follows-and-cites-the-entry` 6/6 against 0/6; `flags-the-users-call` 6/6 against 3/6 |

- **`d16` found a defect, now fixed.** At `4d7b988` every plugin run scored 0: after
  "looks good" the run executed the Manifest. Two causes: `define` never said to stop after its
  handoff, whose lines for callers read as an instruction, and the outer agent called `/do` on a
  plan's approval without loading `define` at all. `define` now stops after the handoff, and
  `/do` runs only when execution was asked for. The re-run passed every plugin run. `d16`'s
  seeded Manifest also lacked the ceiling invariant, so `ceiling-verbatim` could not pass; it
  carries it now.
- **The plugin runs stopped without loading `define` on the `d16` re-run** (`skill-fired` 0/6,
  so `handoff-line` 0/6): the `/do` description now says it is not for an approved plan, and the
  agent answered from that. The behavior the case scores held on every run.
- **`d11`–`d15` were removed after this run.** Each case's own graders passed every run in both
  arms, so the base model already does what it targets: an experienced wait gated on the device,
  edge cases in a data summary, the owner's yes kept, a defect review on a small money change, a
  binding rule kept through an unattended amendment. `d11`–`d14` separated the arms only on the
  shared graders, which `d01`–`d10` already measure, and `d15` on nothing. At about $1.52 a run
  they bought no signal the suite lacked. Rebuild one only if the plugin is seen to regress there.

## Baseline — 2026-10-06, after the threshold rubric fix

**This baseline predates a change that edited `define` and this suite.** `define` now states the
shared rule for the user's calls (two careful people with the same evidence could reasonably
decide differently, and the difference would matter to the user), checks the user's Taste entries
at those calls, marks an `ASM-*` entry that records one, and offers a Taste entry when the user
reverses an earlier call and says why. The same change added `d16` and `d17` and gave `d05` a scored
grader, `keeps-other-requirements`, moved from the retired `evals-define/` pilot. `d05`'s recorded
number no longer compares: it now carries one more scored grader. Re-record both arms before
measuring against this.

Report `results/define-baseline-20261006b`. Skill at `62481855`, graders as committed with this
section, CLI 2.1.289, agent `claude-opus-5-5`, judge `claude-opus-5-5`, 6 runs per arm, $189. It
re-measures the suite after `no-invented-thresholds` was clarified (all eight copies): the grader
now also scans required deliverables, names a required report or write-up (a runbook, change
notes, a release or support note) as a specific the request must have asked for, and counts the
severity bar a review gate applies.

| Case | With | Without | Δ |
|---|---|---|---|
| d01-layer-cut | 1.00 | 0.25 | +0.75 |
| d02-outcome-not-mechanism | 1.00 | 0.50 | +0.50 |
| d03-class-not-instances | 0.92 | 0.71 | +0.21 |
| d04-unsafe-binds | 0.96 | 0.38 | +0.58 |
| d05-conflicting-goals | 0.67 | 0.50 | +0.17 |
| d06-subjective-anchor | 0.92 | 0.50 | +0.42 |
| d07-neg-no-problem | 1.00 | 1.00 | 0.00 |
| d08-neg-small | 0.96 | 0.46 | +0.50 |
| d09-amend-widen | 0.50 | 0.00 | +0.50 |
| d10-loop-bait | 0.88 | 0.50 | +0.38 |

Mean Δ over the 10 cases **+0.40**.

- **`d08` was noise.** The plugin arm is back to 0.96, `binding-lives-in-gates` 5/6 and
  `proportionate` 6/6, so the drop the previous baseline asked about did not replicate.
- **`d05` was the threshold hill the old rubric hid**: `no-invented-thresholds` 0/6 in both arms.
  Each plugin run carried at least one specific the request never set: a required runbook or
  design-doc write-up in five of six, otherwise a tolerance, sample size, run length, or second
  pass bar inside a larger check. The old rubric did not count write-ups.
- **Other headroom**: `widens-not-siblings` on `d09` (3/6) and `gates-are-settleable` on `d10`
  (3/6), both on tuning cases.

## Hill-climb on invented thresholds, round 2 — 2026-10-06

Plugin arm only, 6 runs per case, against the baseline above, split as below (held out `d04`,
`d06`, `d08`). One edit: `define`'s rule on specifics names where they slip in — a tolerance,
sample size, or run length; a second pass bar beside the stated one; a sign-off; an artifact
beyond the change itself, such as a runbook or design doc — and asks for a reread of every gate
body before handoff.

| Grader | Split | Baseline | Round |
|---|---|---|---|
| `no-invented-thresholds` | tuning | 23/30 | 27/30 |
| `no-invented-thresholds` | held out | 16/18 | 16/18 |
| `binding-lives-in-gates` | tuning · held out | 28/30 · 16/18 | 27/30 · 15/18 |
| `gates-are-settleable` | tuning · held out | 26/30 · 18/18 | 28/30 · 17/18 |

- **Kept.** `d05` went from 0/6 to 5/6 on its target, and the held-out set held at 16/18.
- **Watch `binding-lives-in-gates`** on `d05` (5/6 → 4/6) and `d06` (5/6 → 4/6). Each is one run
  inside six-run noise, but both point the same way, and the next both-arm baseline should say
  whether the drop is real.
- The held-out set could not show a gain here: it was already near its ceiling on the target
  grader.

## Baseline — 2026-10-06

**Superseded** by the re-measure above: `no-invented-thresholds` has changed since.

Report `results/define-baseline-20261006`. Measured at `03025008` (after the threshold
hill-climb below), CLI 2.1.289, agent `claude-opus-5-5`, judge `claude-opus-5-5`, 6 runs per arm,
$191.

| Case | With | Without | Δ |
|---|---|---|---|
| d01-layer-cut | 0.96 | 0.21 | +0.75 |
| d02-outcome-not-mechanism | 0.97 | 0.67 | +0.30 |
| d03-class-not-instances | 1.00 | 0.67 | +0.33 |
| d04-unsafe-binds | 0.96 | 0.38 | +0.58 |
| d05-conflicting-goals | 0.88 | 0.50 | +0.38 |
| d06-subjective-anchor | 0.92 | 0.50 | +0.42 |
| d07-neg-no-problem | 1.00 | 1.00 | 0.00 |
| d08-neg-small | 0.79 | 0.42 | +0.37 |
| d09-amend-widen | 0.50 | 0.00 | +0.50 |
| d10-loop-bait | 0.83 | 0.50 | +0.33 |

Mean Δ over the 10 cases **+0.40**, against +0.41 on 2026-10-05 — the same headline from a
different mix, so read it by arm.

- **The plugin arm rose on the cases the threshold change aimed at:** `d04` 0.79 → 0.96, `d05`
  0.71 → 0.88, `d10` 0.67 → 0.83, `d03` 0.83 → 1.00. `no-invented-thresholds` is now 39/48 with
  the plugin against 6/48 without.
- **The no-plugin arm moved too**, by up to ±0.17 a case with nothing changed on its side — `d02`,
  `d03`, `d08`, and `d10` up, `d01` down. That is the noise the figure-out README describes, and it
  is why the mean held while the plugin arm improved.
- **Watch `d08`.** The plugin arm fell 1.00 → 0.79: `binding-lives-in-gates` 3/6 and
  `proportionate` 5/6 on the mechanical rename. Six runs cannot separate a regression from noise;
  the next define baseline should say which.
- **Little headroom is left in the plugin arm.** `d09`'s `widens-not-siblings` (3/6) is the one
  case-level hill, on a single tuning case with no held-out sibling, so a climb on it cannot be
  judged on the held-out set yet.

## Baseline — 2026-10-05

**Superseded** by the 2026-10-06 baseline above; kept for the hill-climb below, which measured
against it.

Report `results/define-baseline-20261005-1845`. Measured at `9a312219`, CLI 2.1.289, agent
`claude-opus-5-5`, judge `claude-opus-5-5`, 6 runs per arm — pilot depth, so read single-case
moves against the noise rules in `../README.md`.

| Case | With | Without | Δ |
|---|---|---|---|
| d01-layer-cut | 1.00 | 0.33 | +0.67 |
| d02-outcome-not-mechanism | 0.93 | 0.53 | +0.40 |
| d03-class-not-instances | 0.83 | 0.54 | +0.29 |
| d04-unsafe-binds | 0.79 | 0.46 | +0.33 |
| d05-conflicting-goals | 0.71 | 0.38 | +0.33 |
| d06-subjective-anchor | 0.83 | 0.50 | +0.33 |
| d07-neg-no-problem | 1.00 | 1.00 | 0.00 |
| d08-neg-small | 1.00 | 0.29 | +0.71 |
| d09-amend-widen | 0.67 | 0.00 | +0.67 |
| d10-loop-bait | 0.67 | 0.33 | +0.33 |

Mean Δ over the 10 cases **+0.41**.

- **Requirements living in gates is the widest gap.** `binding-lives-in-gates` passes 5–6 of 6
  with the plugin and 0–1 of 6 without on every case that carries it.
- **Slicing, proportion, and amendment show clean case-level uplift:** `slices-not-layers` 6/6
  vs 0/6, `proportionate` 6/6 vs 0/6, `widens-not-siblings` 4/6 vs 0/6.
- **Invented thresholds are the open hill.** `no-invented-thresholds` is low in both arms — 0/6
  with the plugin on `d05`, 1/6 on `d10`, 2/6 on `d04` and `d06`. `define` still writes bars the
  request never set, which is the too-tight half of a looping Manifest.
- **Eight case graders show no headroom** and act as floor checks: `binds-outcome-not-cron`,
  `keeps-deliberate-mechanism`, `gate-covers-the-class`, `safety-rules-bind`,
  `conflict-surfaced`, `quality-anchored`, `does-not-invent-a-problem`, and
  `bounds-the-open-ends` pass every run in both arms. Their cases stay, since each still
  separates the arms on a shared grader; `d07` stays as the over-planning floor.

The 2026-10-05 pilot before this ran with a sonnet judge and rubrics the one-word reply could not
hold; its shared-grader numbers are not comparable and are not kept.

## Hill-climb on invented thresholds — 2026-10-05

Two rounds against `no-invented-thresholds`, plugin arm only (`--ablation none`), 6 runs per case,
same CLI, agent, and judge as the baseline, train/test split as below. Reports
`results/define-hillclimb-v1-20261005` and `results/define-hillclimb-v2-20261005`.

| Grader | Baseline | v1 | v2 (kept) |
|---|---|---|---|
| no-invented-thresholds, train | 14/30 | 24/30 | 22/30 |
| no-invented-thresholds, test | 10/18 | 15/18 | 18/18 |
| gates-are-settleable, train · test | 28/30 · 18/18 | 24/30 · 18/18 | 28/30 · 16/18 |
| binding-lives-in-gates, train · test | 27/30 · 17/18 | 28/30 · 17/18 | 27/30 · 16/18 |
| case graders | 64/66 | 64/66 | 65/66 |
| agent cost per suite | $23.73 | $23.37 | $23.60 |

- **v1** added a floor rule to `SKILL.md`: every specific in a gate has a source. A value the
  request never set enters a gate only when derived from a stated requirement, said in its why,
  or as an `(auto)` assumption the gate cites. Every failing train Manifest had stated chosen
  numbers, windows, write-ups, or sign-offs as requirements; the passing ones already filed
  them as assumptions.
- **v2** closed a hole v1 opened: two `d05` Manifests left a zero-failure gate's evidence set
  open ("at least these, plus any others"), which no finite run completes. The coverage clause
  now requires a closed list or count.
- **Read with care.** The threshold gain replicates across both rounds (39/48 and 40/48 against
  24/48). The test settleable and binding dips in v2 are one run each on `d04` and `d06` and sit
  inside the noise. The opus judge spends roughly twice as much grading the new Manifests; the
  agent's cost is unchanged. The 2026-10-06 baseline re-records both arms with this change in.

## How the cases are built

- **Each case plants one trap** that a rule in `define/SKILL.md` exists to catch: a request cut
  by layer, an incidental mechanism stated next to the real outcome, three instances of a broader
  class, a safety rule mentioned in passing, two requirements that cannot both hold, and so on.
- **Every scored grader judges substance meaningful in any spec format.** The baseline arm has no
  Manifest schema, so no grader checks IDs, gate kinds, section names, or schema conformance.
  It does check that a safety rule *binds* rather than sits in guidance, that a gate ranges over a
  class rather than a list, and that a subjective check has an anchor.
- **The spec is graded from the file.** Each run gets a fresh home directory, so the prompt asks
  for `./manifest.md` in the working directory, and graders read it with
  `focus: {source: file, path: manifest.md}`. The two cases whose right answer may be to *not*
  write a spec (`d05`, `d07`) grade the first and last 12 trace messages instead; unseen middle actions are not established.
- **Every prompt carries the settled understanding and says the user is away.** Without that,
  `define` hands off to figure-out or waits for approval, and the run grades an interview opener.
- **Prompts name the skill**, for the trigger-reliability reasons the figure-out README records.
  `skill-fired` is display-only.

## The calibration grader: too tight or too loose

`gates-are-settleable.md` is shared by the general spec-encoding cases. It targets the most
expensive failure a Manifest has in execution: a gate written so loosely that evaluators disagree
or keep finding new issues on unchanged work, or so tightly that no work can pass it. Either one
sends `/do` round the repair loop. The judge fails a spec only when it can name a specific gate
that is unstable or unreachable; a command, BLOCKED label or named review does not excuse a contradictory or unreachable condition. `d10-loop-bait` is the case built to press it
hardest.

The copies are one rubric: `tests/test_eval_shared_graders.py` fails if they drift. Edit all of them
together.

What it does not catch: a gate that pins an incidental mechanism is settleable, but it still
causes rework when the executor meets the intent another way. `d02` covers that one separately.

## Shared requirement and threshold graders

Both come from what `manifest-to-goal` keeps when it boils a Manifest down to a standalone
definition of done for an executor with no other context.

- `binding-lives-in-gates.md`: compares the original request with the gates, including requirements
  omitted from the entire Manifest, then checks claims elsewhere in the document. An executor working from the
  gates finds an ungated rule only mid-run, as rework. One rubric across its copies; the drift
  test covers it.
- `no-invented-thresholds.md`: looks for a number, budget, format, report, or sign-off in the
  gates that neither came from the request nor has an explicit, cited assumption with a value, rationale and impact. An invented target of
  unknown reachability stays advisory even when recorded; a number the user requires still binds. A
  convention the stated stack already fixes, such as a standard HTTP status code, is fine. This is the too-tight half that `gates-are-settleable` cannot see: an invented bar is
  still settleable. It skips checks that review the change itself, which `define` adds by design.
  Each copy embeds its case's request, since a grader reading the file cannot see the prompt, so
  the copies differ by case. Regenerate them if a prompt changes.

## Cases

| Case | Trap | Scored graders |
|---|---|---|
| `d01-layer-cut` | Plan handed over cut by layer (model → API → UI) | `slices-not-layers`, settleable |
| `d02-outcome-not-mechanism` | Incidental cron next to the real freshness bound; a deliberate audit-bus rule | `binds-outcome-not-cron`, `keeps-deliberate-mechanism`, settleable |
| `d03-class-not-instances` | Three reported surfaces of a scattered timezone defect | `gate-covers-the-class`, settleable |
| `d04-unsafe-binds` | Shared-staging, re-runnable, and no-prod rules mentioned in passing | `safety-rules-bind`, settleable |
| `d05-conflicting-goals` | Sub-50ms replica reads vs never-stale balances | `conflict-surfaced`, `keeps-other-requirements` |
| `d06-subjective-anchor` | "Feels dead" with a named reference and a named decider | `quality-anchored`, settleable |
| `d07-neg-no-problem` | **Negative:** cache requested with no problem behind it | `does-not-invent-a-problem` |
| `d08-neg-small` | **Negative:** mechanical rename | `proportionate`, settleable |
| `d09-amend-widen` | Amendment: steering names an instance an existing gate should have claimed | `widens-not-siblings` |
| `d10-loop-bait` | Open-ended absolutes ("excellent", "nothing missing") with the anchors supplied | `bounds-the-open-ends`, settleable |
| `d16-approved-means-handoff` | Interactive: the user approves the digest with "looks good" | `stops-at-the-handoff`, generated final-state guards · changed guards first measured 2026-10-25 |
| `d17-taste-in-encoding` | Taste entries in memory: a narrow one that settles an encoding call, a broad one that tempts dropping a review on a payment step, and a user's call none bears on | `follows-and-cites-the-entry`, `flags-the-users-call`, `broad-entry-drops-nothing`, `no-taste-offer`, generated final-state guards, shared three · changed guards first measured 2026-10-25 |
| `d27-explicit-target` | Firm 2-second export target with unknown reachability | `keeps-the-explicit-target` |

"Shared three" is `binding-lives-in-gates`, `gates-are-settleable`, and `no-invented-thresholds`.
`d05` also carries `keeps-other-requirements`: resolving the conflict must not lower or drop
another stated requirement without authorization. A stated assumption is not authorization.

The original schema-check cases also carry display-only regex graders, never scored by the comparator:
`ceiling-verbatim` (the ceiling invariant appears verbatim in `manifest.md`; a test ties its
pattern to `SCHEMA.md`) and `handoff-line` (the last message names the Manifest with a
`Manifest complete:` line). They show schema conformance without counting it as uplift, since
the no-plugin arm has no schema to follow.

`d07` and `d08` are the over-planning floor. Keep at least one through any tuning that pushes
`define` to encode harder.

## Classification

Every case's standing as of 2026-10-18, under the selection rules in `../README.md`: measured
uplift or a declared guard keeps a case, an unmeasured case stays until its first run decides, and
a duplicate, an out-of-scope skill, or an undeclared floor in both arms retires it.
`tests/test_eval_cases.py` fails when a case has no row here.

| Case | Standing | Why |
|---|---|---|
| `d01` | keep | Uplift +0.75 |
| `d02` | keep | Uplift +0.50, but on the shared graders only: its own graders floored on 2026-10-05, the pattern that retired `d11`–`d14`. Retire it if the next baseline repeats that |
| `d03` | keep | Uplift +0.21; the same watch as `d02` |
| `d04` | keep | Held out; uplift +0.58 |
| `d05` | keep | Conflict guard: no artifact is a valid outcome; preserve every explicit requirement without assuming authority to weaken it |
| `d06` | keep | Held out; uplift +0.42 |
| `d07` | keep | Declared negative floor |
| `d08` | keep | Held-out negative; uplift +0.50 |
| `d09` | keep | A hill: the plugin arm scores 0.50 |
| `d10` | keep | Uplift +0.38 on settleable gates |
| `d16` | keep | Uplift +0.67 |
| `d17` | keep | Uplift +0.30 |
| `d20` | first run decides | The base model tends to thread a change through resisting code rather than prepare it |
| `d21` | first run decides | The only case for a project rule overriding a Default |
| `d22` | keep | Declared guard: the no-plugin arm is expected to pass; run once for status |
| `d23` | first run decides | New on 2026-10-15: define's rule that an unfit touched recipe is repaired first, plus the touched-recipe gate `d18` held |
| `d24` | first run decides | New on 2026-10-15: the same rule for a check of the project's own, with no harness |
| `d25` | first run decides | New on 2026-10-18: a vague speed want encoded as a floor plus an aim, the case for define's floor-plus-aim rule. The review runs in a fresh context only where the suite allows one; the `define` recipe's `fresh-review` drive covers that |
| `d26` | first run decides | New on 2026-10-19: the review's search for holes, on the self-graded path; the `define` recipe's `hole-search` drive covers the fresh-context path |
| `d27` | first run decides | Held out: the explicit 2-second user target must bind even when reachability is unknown; mirror for d25 |

Retired on 2026-10-15: `d18-map-gate`, folded into `d23`, which has the same prompt and project
and now carries its grader.

Retired on 2026-10-24: `d19-workaround-comment` judged an execution/code-review duty, not a spec outcome. Its ADR now names the missing review-code check honestly.

## First-run plan

Use [the free inventory and preflight](../READINESS.md) for current counts. Run one trial per arm
for a fresh directional baseline; prioritize `d23`/`d24`, `d20`/`d21` and the `d25`/`d27` mirror
when splitting a budget. Keep `d22` as a guard. Read failing judge verdicts against their exact
artifact before choosing a skill change, and repeat decisive cases at three trials per arm.
The historical $1.52 per trial is an estimate, not a bound. No current behavioral uplift or
judge agreement has been measured. `d02`/`d03` remain candidates for retirement after fresh
results because their old signal came from shared graders; they are not removed on stale data.

## Held-out split

`d04`, `d06`, and `d08` are the original held-out binding-rule, anchoring and negative cases
used in the 2026-10-05 hill-climb. `d27` joins them in this revision as the explicit-target mirror.
Freeze the full split before inspecting outputs, and let the analyzer read only training cases.

## Known limits

- **A case gets files only through its scaffold.** Most prompts describe the codebase inline and
  say it is unavailable. `d16` seeds a Manifest and a small repository with `scaffold.sh`, and
  `d20`–`d24` a small project. `d17` seeds its preference file. `d09` predates scaffolds and still asks the agent to save a pasted manifest.
- **Many judge graders read the whole Manifest.** The inventory reports current counts. File-focused graders read
  `manifest.md` entire, often near 20k characters, where the CLI's guidance is a regex for long
  output and the judge for short output; it is where the sonnet judge failed a sound Manifest.
  A property a pattern can settle (a section present, a gate kind declared) moves to a `regex`
  grader when its case is next edited, taking it off the judge; one that needs the whole document,
  such as a requirement no gate checks, stays with the judge, and its FAIL is read against the
  Manifest before anything is done about it.
- **One turn of the interview.** The suite measures unattended encoding, plus one interactive
  turn after approval (`d16`). Interview order, re-asking settled ground, and the digest's form
  need a scripted second turn the harness does not run, so they are out of scope.
- **Taste loading is supplied.** `d17` supplies preferences in `append_system_prompt` and seeds
  `preferences.md`; final-state checks cover edits through any tool, not host memory discovery.
- **Not covered, by choice.** Babysit mode needs a GitHub stand-in, and multi-repo Manifests need
  two repositories. Handing off to figure-out when understanding is missing has shown no failure
  and only the plugin arm can do it. Composing writing registers and visual gates is partly
  covered by `d06` and `d10`. Checking that every gate declares its kind and that each `(auto)`
  item pairs with an `ASM-*` entry needs a judge over the whole Manifest on every run, which
  costs more than it would show; `ceiling-verbatim` covers the one schema element that ships
  verbatim. Raising a conflict and flagging the user's call already have `d05` and `d17`; the
  reversal offer in `define` is checked by reading its text. A stale Intent after an amendment,
  and a reversed decision left without a gate, have a guard in the skill and `d09` covers
  amendment. Build one when a miss shows in use.
- **Disciplines with no case yet**, ranked by what a miss would cost, each waiting on a miss seen
  in use or a budget for one more case (this change held the suite to its size): reading earlier
  work (logs, Manifests, open Tickets, pull requests' debt) before encoding, and noting an old
  surfaces version, which needs fixtures of earlier sessions (figure-out's `43` and `46` cover
  recall); an approved Manifest whose gate runs an ask-first recipe carrying the agreement to run
  it, which needs an approval a grader can see; a project with nothing that can check the work
  getting a first Deliverable that adds such a check in its own form, never a harness it did not
  choose (figure-out's `33` covers the read); a criterion pinned
  by reacting to something concrete becoming a gate; an `Enforced by: not yet` check on the
  work's path getting built; and the *fast enough* job of *Trust the check*, a touched check over
  its time line repaired first, which needs evidence carrying a recorded line (figure-out's
  README names the same gap).
