# define eval suite

Measures whether `define` encodes a Manifest by the disciplines its own prompt states: not
whether it writes a document shaped like a Manifest, which only the with-plugin arm can do and
which would therefore make every case a vanity win.

Run it from the plugin directory:

```bash
claude plugin eval . --tag define --ablation with-without --judge-model opus --allow-tools Write Bash --scaffold -j 8
```

`--scaffold` runs the `scaffold.sh` that `d16` declares in its `case.yaml`: it starts from a saved
Manifest beside a small repository. Without it, the case runs against an empty directory and
measures nothing. Only pass it for case files from this
repository: a scaffold is bash that runs as you.

Its scope and the meaning of each case's status are in the figure-out suite's README
(`../README.md`, *Scope and statuses*). The headline number is **Δ**, the with-plugin score minus
the no-plugin baseline. Read the figure-out suite's README (`../README.md`) before trusting a Δ
from this one: its rules on decomposing Δ by arm, the noise floor, and changing graders apply here
unchanged.

**The judge is opus, not sonnet.** The CLI's judge must reply with one word, PASS or FAIL, with no
room to reason on the page. On a 20k-character Manifest, a sonnet judge failed whole-document
checks it passes when allowed to reason: a sound Manifest scored FAIL on nearly every vote. An
opus judge matched known answers on a clean Manifest and on a copy with an unstable gate, an
ungated rule, and an invented threshold planted in it. Keep opus here unless that check is
repeated with a cheaper judge.

## Cases added 2026-10-13 — unmeasured

| Case | Discipline under test |
|---|---|
| `d18-map-gate` | A change touching a mapped feature gates that its verification-surface entry is updated and exercised live |
| `d19-workaround-comment` | A workaround comment in touched code becomes a refactor target, not a deletion |
| `d20-preparatory-slice` | When the touched area resists the change, a behavior-preserving restructuring comes first |
| `d21-user-rule-over-default` | A rule the project states overrides a conflicting task-file Default, and the adjustment is recorded |

These have never been run; the first both-arm run decides which stay. **Every number below is stale
as of 2026-10-13**: that change edited define's spine and its task files, so the next baseline
replaces them.

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
  write a spec (`d05`, `d07`) grade the whole trace instead.
- **Every prompt carries the settled understanding and says the user is away.** Without that,
  `define` hands off to figure-out or waits for approval, and the run grades an interview opener.
- **Prompts name the skill**, for the trigger-reliability reasons the figure-out README records.
  `skill-fired` is display-only.

## The calibration grader: too tight or too loose

`gates-are-settleable.md` runs on every case that should produce a spec. It targets the most
expensive failure a Manifest has in execution: a gate written so loosely that evaluators disagree
or keep finding new issues on unchanged work, or so tightly that no work can pass it. Either one
sends `/do` round the repair loop. The judge fails a spec only when it can name a specific gate
that is unstable or unreachable; delegation to a named review with a stated scope counts as
settleable. `d10-loop-bait` is the case built to press it
hardest.

The copies are one rubric: `tests/test_eval_shared_graders.py` fails if they drift. Edit all of them
together.

What it does not catch: a gate that pins an incidental mechanism is settleable, but it still
causes rework when the executor meets the intent another way. `d02` covers that one separately.

## Two more graders on every spec case

Both come from what `manifest-to-goal` keeps when it boils a Manifest down to a standalone
definition of done for an executor with no other context.

- `binding-lives-in-gates.md`: looks for a requirement stated outside the gates (in the problem,
  approach, guidance, or assumptions) that no gate checks. An executor working from the
  gates finds an ungated rule only mid-run, as rework. One rubric across its copies; the drift
  test covers it.
- `no-invented-thresholds.md`: looks for a number, budget, format, report, or sign-off in the
  gates that neither came from the request nor is recorded as an assumption with a reason. A
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
| `d05-conflicting-goals` | Sub-50ms replica reads vs never-stale balances | `conflict-surfaced`, settleable |
| `d06-subjective-anchor` | "Feels dead" with a named reference and a named decider | `quality-anchored`, settleable |
| `d07-neg-no-problem` | **Negative:** cache requested with no problem behind it | `does-not-invent-a-problem` |
| `d08-neg-small` | **Negative:** mechanical rename | `proportionate`, settleable |
| `d09-amend-widen` | Amendment: steering names an instance an existing gate should have claimed | `widens-not-siblings` |
| `d10-loop-bait` | Open-ended absolutes ("excellent", "nothing missing") with the anchors supplied | `bounds-the-open-ends`, settleable |
| `d16-approved-means-handoff` | Interactive: the user approves the digest with "looks good" | `stops-at-the-handoff`, `layout-unchanged` · measured 2026-10-12 |
| `d17-taste-in-encoding` | Taste entries in memory: a narrow one that settles an encoding call, a broad one that tempts dropping a review on a payment step, and a user's call none bears on | `follows-and-cites-the-entry`, `flags-the-users-call`, `broad-entry-drops-nothing`, `no-taste-offer`, `no-taste-write`, `no-taste-edit`, shared three · measured 2026-10-12 |

"Shared three" is `binding-lives-in-gates`, `gates-are-settleable`, and `no-invented-thresholds`.
`d05` also carries `keeps-other-requirements`: resolving the conflict must not lower or drop
another stated requirement without saying so.

Every case that writes a spec also carries two display-only regex graders, never scored:
`ceiling-verbatim` (the ceiling invariant appears verbatim in `manifest.md`; a test ties its
pattern to `SCHEMA.md`) and `handoff-line` (the last message names the Manifest with a
`Manifest complete:` line). They show schema conformance without counting it as uplift, since
the no-plugin arm has no schema to follow.

`d07` and `d08` are the over-planning floor. Keep at least one through any tuning that pushes
`define` to encode harder.

## Held-out split

`d04`, `d06`, and `d08` are held out from tuning: one binding-rule case, one anchoring case, and one
negative. The 2026-10-05 hill-climb used this split; an analyzer reads only the other nine.

## Known limits

- **A case gets files only through its scaffold.** Most prompts describe the codebase inline and
  say it is unavailable. `d16` seeds a Manifest and a small repository with `scaffold.sh`. `d09` predates scaffolds and still asks the agent to save a pasted manifest.
- **One turn of the interview.** The suite measures unattended encoding, plus one interactive
  turn after approval (`d16`). Interview order, re-asking settled ground, and the digest's form
  need a scripted second turn the harness does not run, so they are out of scope.
- **No memory file loads in the sandbox.** `d17` puts the user's memory file in
  `append_system_prompt`.
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
