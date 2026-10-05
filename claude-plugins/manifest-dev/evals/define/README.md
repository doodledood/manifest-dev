# define eval suite

Measures whether `define` encodes a Manifest by the disciplines its own prompt states: not
whether it writes a document shaped like a Manifest, which only the with-plugin arm can do and
which would therefore make every case a vanity win.

Run it from the plugin directory:

```bash
claude plugin eval . --tag define --ablation with-without --judge-model opus --allow-tools Write Bash -j 8
```

The headline number is **Δ**, the with-plugin score minus the no-plugin baseline. Read the
figure-out suite's README (`../README.md`) before trusting a Δ from this one: its rules on
decomposing Δ by arm, the noise floor, and changing graders apply here unchanged.

**The judge is opus, not sonnet.** The CLI's judge must reply with one word, PASS or FAIL, with no
room to reason on the page. On a 20k-character Manifest, a sonnet judge failed whole-document
checks it passes when allowed to reason: a sound Manifest scored FAIL on nearly every vote. An
opus judge matched known answers on a clean Manifest and on a copy with an unstable gate, an
ungated rule, and an invented threshold planted in it. Keep opus here unless that check is
repeated with a cheaper judge.

## Baseline — 2026-10-05

Report `results/define-baseline-20261005-1845`. Measured at `9a312219`, CLI 2.1.289, agent
`claude-opus-5-5`, judge `claude-opus-5-5`, 6 runs per arm — pilot depth, so read single-case
moves against the noise rules in `../README.md`. The committed `aggregate-result.json` has each
verdict's judged Manifest stripped; the local HTML report keeps it.

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
  agent's cost is unchanged. The baseline Δ above predates this change and has not been
  re-recorded with both arms.

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

`d07` and `d08` are the over-planning floor. Keep at least one through any tuning that pushes
`define` to encode harder.

## Held-out split

`d04`, `d06`, and `d08` are held out from tuning: one binding-rule case, one anchoring case, one
negative. The 2026-10-05 hill-climb used this split; an analyzer reads only the other seven.

## Known limits

- **No repository.** Every prompt describes the codebase inline and says it is unavailable. A
  case that needs `define` to read real code would degenerate in both arms.
- **One turn of the interview.** The suite measures unattended encoding. Interview quality
  (which questions `define` surfaces, which it auto-decides) is out of scope.
- **The amendment manifest is inline.** Seeding files before a run is undocumented in the CLI,
  so `d09` asks the agent to save the pasted manifest before amending it.
