# figure-out eval suite

This directory also holds the `define` suite under `define/`, with its own README. Each case is
tagged with its suite; run one with `--tag figure-out` or `--tag define`.

Measures whether `figure-out` delivers the discipline its own prompt states — not whether it
reaches a correct answer, which a strong base model does unaided.

Run it:

```bash
claude plugin eval . --tag figure-out --ablation with-without --judge-model sonnet --allow-tools Write Bash -j 8
```

`--allow-tools Write Bash` is required. `allowed_tools` in a case's `prompt.md` declares what the
case *wants*; the operator grant is what enables it. Without it, file graders fail in both arms and
cases burn their turn reporting that writing is disabled.

The headline number is **Δ** — with-plugin score minus the no-plugin baseline.

## Running on macOS

Run the suites in the Linux container defined by `Dockerfile` in this directory. On macOS, every
eval child tries to store a key in the login keychain from a sandboxed home that has no keychain,
and macOS raises a "Keychain Not Found" dialog per child, hundreds per suite. A container has no
macOS keychain, and a detached container also keeps running if the launching session ends:

```bash
docker build -t manifest-dev-evals claude-plugins/manifest-dev/evals
docker run -d --security-opt seccomp=unconfined --security-opt apparmor=unconfined \
  -e ANTHROPIC_API_KEY -v "$PWD":/work -w /work/claude-plugins/manifest-dev \
  manifest-dev-evals claude plugin eval . --tag figure-out --ablation with-without \
  --judge-model sonnet --allow-tools Write Bash -j 4 --no-publish --trust-plugin
```

The Dockerfile pins the CLI version; bump it deliberately, since a different CLI can move scores.

## What the pilots established

Three independent case designs were built and run before this suite settled. Two of them produced
Δ 0.00 because **both arms passed**, and that is the finding worth carrying forward:

- **Interactive opening press** (6 cases). Four of five case-specific graders passed in both arms.
  The base model presses about as well as the plugin on an opening turn.
- **Autonomous diagnosis with a findable mechanism** (`10-diagnosis-retry-window`). Both arms
  scored 1.00 on all four substance graders. The with-arm did two things the baseline did not —
  ran an independent re-derivation, and settled a red herring by executing the arithmetic rather
  than reasoning about it — and neither moved a grader.
- **Autonomous underdetermined** (`11-underdetermined`). Both arms scored 0.33, **failing** the
  same two graders. This is the shape the suite is built on.

**Δ 0.00 means two opposite things, and the difference is everything.** Both arms passing means no
headroom — the case cannot be climbed. Both arms failing a grader traceable to figure-out's own
stated rule means the skill is not delivering its stated discipline, and that is the hill.

Cases are therefore selected for headroom: the with-arm currently fails a substance grader derived
from a discipline `SKILL.md` explicitly states.

## Cases

| Case | Kind | Discipline under test | Split |
|---|---|---|---|
| `01-root-press` | press | Press from the true root when a solution arrives pre-chosen | tuning |
| `02-assumed-cause` | press | Do not adopt a diagnosis the user handed over | tuning |
| `04-hold-under-pushback` | press | Hold a supported read against insistence | tuning |
| `05-move-on-evidence` | press | Update when evidence actually arrives | held out |
| `06-strategic-open` | press | Press one crux rather than delivering the artifact asked for | tuning |
| `07-neg-lookup` | negative | Do not deliberate on a lookup | tuning |
| `08-neg-authorized` | negative | Comply when the decision is settled and the change named | held out |
| `10-diagnosis-retry-window` | autonomous | Reach a mechanism, not a location; kill rivals with evidence | tuning |
| `11-underdetermined` | autonomous | Do not manufacture a winner; separate verified from assumed | tuning |
| `12-living-with-it` | autonomous | Price "living with it" as a real option | tuning |
| `13-status-quo-job` | autonomous | Test the status quo's possible job before removing it | held out |
| `14-persona-seat-feature` | autonomous | Take the seat of the person the North Star names and walk their uses, not the mechanism's | tuning |
| `15-persona-seat-doc` | autonomous | Take the seat of the reader the North Star names on a document, where no feature probe file loads | held out |

Headroom per case comes from the current baseline, not from this table. The 2026-09-14 numbers
below describe an older skill and model, so no case is labelled with them here.

`04` and `05` are a **mirror pair** and stay paired: a model that always concedes fails `04`, one
that always digs in fails `05`. No constant policy passes both.

`07` and `08` are the should-NOT-fire floor. At least one always stays. Without them a large Δ
cannot distinguish pressing well from turning every message into a deliberation, and
over-triggering is the first casualty of any "press harder" tuning.

## Held-out split

**Held out from tuning: `05-move-on-evidence`, `08-neg-authorized`, `13-status-quo-job`, and
`15-persona-seat-doc`.** Four of thirteen cases. These are run in the baseline and in the final
verification only; they appear in no intermediate run during the climb. Tuning happens on the
other nine.

`12-living-with-it` was held out until 2026-09-14. It is no longer: it was re-run to decide
whether to cut two sentences from the skill, and the cut was made because its grader fell, so it
steered the prompt. `15` takes its place. No feature probe file loads for `15`, so it tests whether
the person's-seat line generalizes beyond the probe that `14` exercises.

The held-out set deliberately includes autonomous cases testing disciplines the climb is not
aimed at: testing the status quo's job, and taking the reader's seat on a document. If a change that fixes
manufacturing-a-winner also moves those, that is generalization. If the tuning set rises while
these fall, that is over-fitting, and the run has to say so.

## Graders declared as floor checks

The current list of graders that pass in both arms on every run is in the 2026-10-05 baseline
below. On the superseded 2026-09-14 baseline it was these eight: They are kept
deliberately, and declared here rather than counted as uplift:

| Grader | Case | What it protects |
|---|---|---|
| `does-not-adopt-users-diagnosis` | `02` | A cause handed over in the prompt is not adopted as the answer |
| `holds-position` | `04` | A supported read is not conceded to insistence |
| `updates-on-evidence` | `05` | A read *is* dropped when evidence actually arrives |
| `answers-without-deliberating` | `07` | A lookup is answered, not turned into a deliberation |
| `decision-file-written` | `08` | An authorized change gets made rather than re-litigated |
| `evidence-has-provenance` | `10` | Claims carry artifacts — quote, `file:line`, output — not assertions |
| `overturn-is-discriminating` | `10` | The stated overturn condition could actually discriminate |
| `chases-the-crumb` | `11` | The detail that does not fit gets pursued, not smoothed over |

**A grader passing in both arms is information, not a defect** — it says the base model already
carries that discipline unprompted, which is exactly what decides how much prompt to spend on it.
What it is not is evidence of uplift, so none of these moves Δ, and none may be cited as showing
the plugin does something.

They are kept because **they are the ones any "press harder" tuning breaks first**. `04` and `05`
are a mirror pair by construction: a model that always concedes fails `05`, one that always digs
in fails `04`, and no constant policy passes both. `07`'s grader is the over-trigger floor. A
climb that raised the tuning mean while flipping any of these to a failure would be a regression
wearing a Δ, and without these graders present nothing in the suite would say so.

## Why the prompts name the skill

Every fire case opens with `use the figure-out skill for this.` This is not a convenience:
figure-out does not auto-activate reliably otherwise. Measured across nine phrasings and twelve
runs —

| Phrasing | Fired |
|---|---|
| `use the figure-out skill for this` | 6/6 |
| `lets figure this out together, dont jump to the fix` | 1/1 |
| `i want us to think this through properly` | 1/1 |
| `lets think this through before we do anything` | 0/1 |
| `i want to actually think this through with you` | 0/1 |
| `still figuring this one out with you` | 0/2 |
| `/manifest-dev:figure-out <topic>` | 0/1 |
| `dig into this on your own … what would change your mind` | 0/1 |
| `figure this out for me. i'm afk …` | 0/1 |

The two that fired were short conversational openers. The six that did not were long, carried
concrete evidence, and looked actionable — including two that paraphrase the skill's own described
deliverable. **figure-out does not auto-fire when the work looks actionable**, which is when it is
most needed. A slash-command prefix does not expand in `prompt.md` and additionally makes the
baseline arm return zero turns, manufacturing a false +1.0 Δ.

Naming the skill contaminates the baseline arm, which may open by reporting the skill is missing.
That contamination is contained in the graders rather than the prompts: **every scored grader
judges substance, never the shape, length or opening of a response.** Trigger reliability is
reported separately by `skill-fired`, which is display-only and never scored.

## Changing this suite

**When a case fails, decide whether the grader or the skill is wrong before touching either, and
never edit both in one pass.** Three graders in the first pilot were wrong, and every fix was to
loosen them. That reflex is how a suite becomes a vanity metric.

Read the failing **outputs**, not the scores. A turn that opened "I'm not going to drop my read
yet", held its position, and named the two numbers that would settle it scored 0.00 under a
rubric that was simply miscalibrated.

## Known limits

- **The sandbox working directory is empty.** Every prompt carries its evidence inline. A case that
  points at a repository degenerates into "point me at the code" in both arms.
- **Press cases observe one turn.** Autonomous cases observe a whole investigation, because
  autonomous mode runs to completion and names a Read in a single run. That is why the suite's
  headroom lives there.
- **Floor-check graders pass in both arms by design.** They exist to catch a regression, not to
  produce uplift, and are marked as such in the table above.
- **`log-written` is on `01-root-press` only.** It is real value — continuity across context loss —
  and a clean uplift signal, but it passes with-plugin and fails without on every case, so carrying
  it everywhere made a file-existence check dominate the headline number.

## The comparison this suite was also used for

For one round, four of these scenarios were duplicated into mirror cases that named a shorter
draft of the skill instead of the shipped one, so each scenario yielded three numbers: the
no-plugin baseline, the shorter prompt, and the longer one. That comparison is finished and the
mirrors are retired — the shorter prompt became the shipped one, and there is no second variant
left to measure against. The numbers and the reasoning are recorded in
`docs/adr/20260914-one-skill-per-beat-built-from-the-lean-body.md`.

What the episode leaves behind for this suite is the shape of the instrument rather than the
result: **the no-plugin arm is the comparison that matters**, because it is the only one that says
whether the prompt is buying anything over a capable base model. A mirror case comparing two
versions of our own prompt is a tool to reach for when a rewrite is on the table, not a permanent
fixture.

## Grader calibration — why two rubrics were rewritten

The first baseline exposed two graders whose verdicts could not be predicted from reading the
output. `turn-discipline` failed `02-assumed-cause`, a turn carrying one claim in two parts and a
single ask with its own guess. `does-not-manufacture-a-winner` failed a response that ranked its
rivals, kept a rival register, stated moderate confidence, named a deciding check, and explicitly
refused to design off the read.

Both rubrics had the same shape: a requirement followed by a list of exemptions ("these do NOT
count as failures"). A sonnet-tier judge applied the requirement and skipped the exemptions.

Both were rewritten to **enumerate before judging** — the judge must first list and classify what
it found (every ask, classified substantive or logistical; the stated cause, and whether a live
rival and a deciding observation are present), and only then reach a verdict on that classification.
The enumeration happens in the judge's head: every LLM grader opens by telling it to work
privately and reply with one word, because the CLI's judge must answer exactly PASS or FAIL and
scores anything written out as FAIL. `tests/test_eval_shared_graders.py` enforces that opening
line. A verdict that follows from an enumeration is predictable from the text; a verdict that depends on
a judge honouring a prose exemption is not.

**This cost a second baseline.** Under INV-G2 a case file may not move after the baseline it is
measured against, so rewriting the graders invalidated the first one. The skill edits under trial
were stashed so the second baseline measures an unchanged `figure-out`, and the climb restarts from
there. That is the intended cost of the freeze rule working: the alternative was tuning a prompt
against a judge that could not read its own exemptions.

## Recording a baseline

Record the resolved model ID, the CLI version, the commit the skill was measured at, and the date
next to every baseline. The cases say only `model: opus`, and `aggregate-result.json` records the
CLI version but not the model, which is how the baseline below went stale unnoticed when the
model changed.

## Baseline — 2026-10-05

Report `results/figure-out-baseline-20261005-1845`. Measured at `9a312219`, CLI 2.1.289,
agent `claude-opus-5-5`, judge `claude-sonnet-5-5`, 12 runs per arm, run in the container
`Dockerfile` defines. The committed `aggregate-result.json` has each verdict's judged output
stripped; the local HTML report keeps it. This is the number any later prompt change is measured
against.

| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| 01-root-press | tuning | 0.83 | 0.03 | +0.81 |
| 02-assumed-cause | tuning | 0.71 | 0.50 | +0.21 |
| 04-hold-under-pushback | tuning | 0.88 | 0.79 | +0.08 |
| 06-strategic-open | tuning | 0.79 | 0.00 | +0.79 |
| 07-neg-lookup | tuning | 1.00 | 1.00 | 0.00 |
| 10-diagnosis-retry-window | tuning | 0.92 | 0.90 | +0.02 |
| 11-underdetermined | tuning | 0.75 | 0.42 | +0.33 |
| 12-living-with-it | tuning | 0.96 | 1.00 | −0.04 |
| 14-persona-seat-feature | tuning | 0.79 | 0.50 | +0.29 |
| 05-move-on-evidence | held out | 0.67 | 0.63 | +0.04 |
| 08-neg-authorized | held out | 1.00 | 1.00 | 0.00 |
| 13-status-quo-job | held out | 0.92 | 0.96 | −0.04 |
| 15-persona-seat-doc | held out | 1.00 | 1.00 | 0.00 |

Mean Δ over the 13 cases **+0.19**.

- **The uplift sits in pressing:** `01`, `06`, `11`, `14`, and `02`. `presses-one-crux` (12/12 vs
  0/12), `log-written` (12/12 vs 0/12), and `turn-discipline` on `01` (11/12 vs 1/12) carry most
  of it.
- **`12-living-with-it` no longer regresses.** `prices-doing-nothing` is 11/12 with the plugin
  against 12/12 without; the 2026-09-14 gap of −0.25 is gone.
- **`15-persona-seat-doc` has no headroom.** Its one grader passes every run in both arms, so it
  measures nothing while it stays in the held-out set. It needs a harder grader or a replacement
  before the held-out mean can say anything about the person's-seat line.
- **Floor graders at this baseline** pass every run in both arms: `holds-position`,
  `updates-on-evidence`, `answers-without-deliberating`, `complies-without-reopening`,
  `decision-file-written`, `evidence-has-provenance`, `names-the-mechanism`,
  `overturn-is-discriminating`, `chases-the-crumb`, `tests-the-status-quos-job`, and
  `takes-the-readers-seat`.

## Superseded baseline — the converged skill, 2026-09-14

**Superseded.** Measured at `ef9806fa` on CLI 2.1.270 with the model `opus` resolved to at the
time. Since then the skill has changed (the person's-seat line, the FEATURE probe, the rewritten
draft step), the model has changed, and several graders were corrected (case 10's timestamps,
case 01's opening clause, case 04's exemption list, `turn-discipline`'s treatment of offers). Kept
for its reasoning, not as a comparison point.

Reports `results/2026-09-14T07-23-48-511Z` (all cases), `results/2026-09-14T09-32-13-181Z`
(case 13, re-run once after its first runs died on a session limit), and
`results/2026-09-14T09-51-23-378Z`, `…T09-56-46-362Z`, `…T10-14-49-348Z` (cases 04, 11, 12,
measured once more after two sentences the first run implicated were cut). 11 cases, `runs: 12`
per arm, `--ablation with-without`, sonnet judge. This is the number any later prompt change is
measured against.

| Case | Merged with | Merged control | Merged Δ | Lean with | With-arm move |
|---|---|---|---|---|---|
| 01-root-press | 0.889 | 0.083 | +0.806 | 0.750 | +0.139 |
| 02-assumed-cause | 0.917 | 0.542 | +0.375 | 0.875 | +0.042 |
| 04-hold-under-pushback | 0.875 | 0.750 | +0.125 | 0.958 | -0.083 |
| 06-strategic-open | 0.625 | 0.083 | +0.542 | 0.542 | +0.083 |
| 11-underdetermined | 1.000 | 0.556 | +0.444 | 0.944 | +0.056 |
| 12-living-with-it | 0.500 | 0.750 | -0.250 | 0.792 | -0.292 |
| 13-status-quo-job | 0.917 | 0.917 | +0.000 | 0.958 | -0.041 |
| 05-move-on-evidence | 0.917 | 0.667 | +0.250 | — | — |
| 07-neg-lookup | 1.000 | 1.000 | +0.000 | — | — |
| 08-neg-authorized | 1.000 | 1.000 | +0.000 | — | — |
| 10-diagnosis-retry-window | 1.000 | 1.000 | +0.000 | — | — |

Mean Δ over the 11 cases **+0.24**. The "Lean with" column is the earlier measurement of the
shorter prompt this skill was built up from; the seven-case with-arm move is −0.014, a fifth of a
standard error, so the merge held on the mean. `12-living-with-it` did not hold: `prices-doing-nothing`
fell 8/12 → 4/12 → 1/12 across lean → merged → cut, and the with-arm now sits below the control.
Every failing turn reframes "fix or live with it" as a false binary and lands on a third action.
The open hypothesis, recorded in the ADR named above, is the independent re-derivation bullet the
merge added; it has not been tested. A mean that passes is not permission to stop reading the rows.

### Two rules for reading any number this suite produces

**1. Decompose every Δ by arm before believing it.** Δ = with − without, and only the with-arm can
respond to a prompt edit. A Δ that improves because the no-plugin control got *worse* is not an
improvement. This is not hypothetical: in the previous round the held-out set appeared to improve
by +0.300, of which +0.233 came from two cases where the with-plugin score did not move by a single
point and the control arm simply collapsed.

**2. Know the noise floor before attributing a move to a change.** In the previous round, three
cases were measured twice against an identical prompt roughly forty minutes apart. Mean |Δ
difference| was **0.111**, max **0.167**, on text that did not change by a character. Per-run score
sd was 0.378 across 180 runs, putting the standard error of a seven-case mean at ~0.117 at
`runs: 3`. A move smaller than that is not evidence of anything. Resolving a ~0.08 effect takes
roughly **26 runs per case per arm**.
