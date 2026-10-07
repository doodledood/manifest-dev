# figure-out eval suite

This directory also holds the `define` suite under `define/`, with its own README. Each case is
tagged with its suite; run one with `--tag figure-out` or `--tag define`.

Measures whether `figure-out` delivers the discipline its own prompt states — not whether it
reaches a correct answer, which a strong base model does unaided.

Run it:

```bash
claude plugin eval . --tag figure-out --ablation with-without --judge-model opus --allow-tools Write Bash -j 8
```

`--allow-tools Write Bash` is required. `allowed_tools` in a case's `prompt.md` declares what the
case *wants*; the operator grant is what enables it. Without it, file graders fail in both arms and
cases burn their turn reporting that writing is disabled.

The headline number is **Δ** — with-plugin score minus the no-plugin baseline.

**Judge with `opus`.** A sonnet-tier judge disagreed with itself across its three votes on the same
output and failed outputs an opus judge passed unanimously; see the 2026-10-06 baseline. Every
number before that baseline is sonnet-judged and does not compare with it.

## Running on macOS

Run the suites in the Linux container defined by `Dockerfile` in this directory. On macOS, every
eval child tries to store a key in the login keychain from a sandboxed home that has no keychain,
and macOS raises a "Keychain Not Found" dialog per child, hundreds per suite. A container has no
macOS keychain, and a detached container also keeps running if the launching session ends:

```bash
scripts/evals/run_eval.sh figure-out-run evals/results/figure-out-run/aggregate-result.json \
  --tag figure-out --ablation with-without --judge-model opus
```

The script builds the image if it is missing, starts colima if Docker is down, reads
`ANTHROPIC_API_KEY` from the shell profile when the environment lacks it, and starts a named,
detached container; `docker wait <name>` blocks until it exits. The Dockerfile pins the CLI
version; bump it deliberately, since a different CLI can move scores. A run writes its results
only when it finishes, so a killed run loses all of its work.

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
| `16-underdetermined-billing` | autonomous | `11`'s disciplines on a different system: do not manufacture a winner; separate verified from assumed | held out |

Headroom per case comes from the current baseline, not from this table. The 2026-09-14 numbers
below describe an older skill and model, so no case is labelled with them here.

`04` and `05` are a **mirror pair** and stay paired: a model that always concedes fails `04`, one
that always digs in fails `05`. No constant policy passes both.

`07` and `08` are the should-NOT-fire floor. At least one always stays. Without them a large Δ
cannot distinguish pressing well from turning every message into a deliberation, and
over-triggering is the first casualty of any "press harder" tuning.

## Held-out split

**Held out from tuning: `05-move-on-evidence`, `08-neg-authorized`, `13-status-quo-job`,
`15-persona-seat-doc`, and `16-underdetermined-billing`.** Five of fourteen cases. Their scores
decide whether a change is kept, but no analyzer reads their outputs and no edit is drawn from
them. Tuning happens on the other nine.

`12-living-with-it` was held out until 2026-09-14. It is no longer: it was re-run to decide
whether to cut two sentences from the skill, and the cut was made because its grader fell, so it
steered the prompt. `15` takes its place. No feature probe file loads for `15`, so it tests whether
the person's-seat line generalizes beyond the probe that `14` exercises.

The held-out set deliberately includes autonomous cases testing disciplines the climb is not
aimed at: testing the status quo's job, and taking the reader's seat on a document. If a change that fixes
manufacturing-a-winner also moves those, that is generalization. If the tuning set rises while
these fall, that is over-fitting, and the run has to say so.

That half of the set can only show a regression: at the 2026-10-05 baseline `08`, `13`, and `15`
had no headroom in the plugin arm, and `05` moved only on `turn-discipline`. A change that
genuinely improved the tuning hills had almost nowhere on the held-out side to show it. `16` is
the other half — `11`'s disciplines on a system the climb never sees — so a change aimed at them
has to carry to it, as a change aimed at `turn-discipline` has to carry to `05`.

A sibling of `01` was built the same way (a pre-chosen "mark all as read" button in front of a
noisy notification badge) and dropped after its first measurement: both arms pressed from the
root on 12 of 12 runs, so it could only ever show a floor. `presses-from-root` therefore has no
held-out witness, and a change aimed only at it cannot be kept under the rule below until one
exists. `15` stays as a declared
floor check rather than gaining a harder grader: both arms take the reader's seat on every run,
and tightening the rubric until the base model fails would measure the rubric, not the skill.

## Graders declared as floor checks

The current list of graders that pass in both arms on every run is in the opus-judged
2026-10-06 baseline below. On the superseded 2026-09-14 baseline it was these eight: They are kept
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

**Run results stay out of the repository.** `results/` is gitignored and nothing under it is
committed: a result file carries sandbox paths and, unless stripped, every judged model output,
and the copy goes stale as soon as the CLI, model, judge, or a rubric changes. The record is this
README — each baseline's table, its provenance line, and what it showed. A `results/<run>` name
in a section below is the local run directory it was read from, not a file in the repository.
`tests/test_eval_results_untracked.py` fails if one is added.

## Hill-climbing a prompt against a suite

To improve a skill against one grader while holding the rest, run rounds of
analyze → change → rerun → compare against a recorded baseline. Each round costs roughly what
the baseline's plugin arm did (about $150 for `define` at 6 runs per case). Keep the loop's
state in a gitignored directory under `results/`, for example `results/hillclimb-<suite>/`,
with a `_state.json` holding `train_ids` and `test_ids` and one `vN/` directory per round.

1. **Split once, before round 1.** Use the suite's documented held-out cases as test. An
   analyzer reads only train cases' outputs, and the test score decides whether a change is
   kept.
2. **Extract train outputs** for the analyzer. A finished run keeps each run's judged artifact
   but no transcript:
   `python3 scripts/evals/extract_outputs.py <result.json> --out <dir> --cases <train cases...>`.
   Use `--report <report.html>` when the JSON's evidence has been stripped.
3. **Make one change per round**, sized to clear the noise floor, and save its diff and
   rationale in `vN/`.
4. **Rerun only the plugin arm**, since the no-plugin arm doesn't move:
   `scripts/evals/run_eval.sh <name> evals/results/hillclimb-<suite>/vN/aggregate-result.json --tag <suite> --ablation none --judge-model <the suite's judge>`.
5. **Compare** per grader and split:
   `python3 scripts/evals/score_rounds.py --state <dir>/_state.json baseline=<baseline json> v1=<dir>/v1/aggregate-result.json`.
   Keep the change only if test moves outside noise and no guardrail grader falls.

Once a winner is kept, re-record the full baseline with both arms. The Δ this README reports
is with-arm minus without-arm, and a hill-climb round measures only the first half of it.

## Baseline — 2026-10-06, opus judge

Report `results/figure-out-baseline-20261006c`, with `14-persona-seat-feature` from
`results/figure-out-14-regrade-20261006` after its rubric fix. Skill at `62481855`, graders as
committed with this section, CLI 2.1.289, agent `claude-opus-5-5`, judge `claude-opus-5-5`, 12
runs per arm. This is the number any later prompt change is measured against.

| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| 01-root-press | tuning | 0.89 | 0.03 | +0.86 |
| 02-assumed-cause | tuning | 1.00 | 0.50 | +0.50 |
| 04-hold-under-pushback | tuning | 1.00 | 0.96 | +0.04 |
| 06-strategic-open | tuning | 0.79 | 0.00 | +0.79 |
| 07-neg-lookup | tuning | 1.00 | 1.00 | 0.00 |
| 10-diagnosis-retry-window | tuning | 1.00 | 0.98 | +0.02 |
| 11-underdetermined | tuning | 1.00 | 0.72 | +0.28 |
| 12-living-with-it | tuning | 1.00 | 1.00 | 0.00 |
| 14-persona-seat-feature | tuning | 0.83 | 0.67 | +0.17 |
| 05-move-on-evidence | held out | 1.00 | 0.83 | +0.17 |
| 08-neg-authorized | held out | 1.00 | 1.00 | 0.00 |
| 13-status-quo-job | held out | 1.00 | 1.00 | 0.00 |
| 15-persona-seat-doc | held out | 1.00 | 1.00 | 0.00 |
| 16-underdetermined-billing | held out | 0.96 | 0.96 | 0.00 |

Mean Δ over the 14 cases **+0.20**. It is lower than the sonnet-judged +0.28 below, and the two do
not compare: the judge changed, and so did seven rubrics.

**Why the judge changed.** Re-judging the same outputs of `11` showed a sonnet judge failing three
outputs, splitting its votes on two of them (FAIL PASS FAIL, PASS FAIL FAIL), that an opus judge
passed unanimously, while opus still failed unanimously an output that was genuinely wrong. Several of the earlier climb's conclusions rested on those votes.

**What the rubric audit changed.** Each rubric whose verdicts disagreed across votes was rewritten to
classify before judging:

- `turn-discipline` (all five copies): a two-part question is two asks unless the parts only mean
  something together; listing the questions deferred to later is not an ask; a turn with no
  substantive ask passes; an offer to read code is logistical.
- `presses-from-root` (`01`): the headline position is classified as reframe, verdict, design, or
  bar, and only a reframe passes.
- `presses-one-crux` (`06`): each channel, feature, or workstream is classified as conditional on
  the crux or as plan; a sequenced plan, or two plan items, fails.
- `rival-actually-killed` (`10`): each decoy is classified as removed with evidence, asserted,
  accepted, or absent.
- `separates-verified-from-assumed` (`11`, `16`): the two load-bearing claims are each classified
  as marked or flat, and neither a blanket caveat nor an overturn condition marks a claim.
- `takes-the-persona-seat` (`14`): uses that share one hand-off count once, each use needs a
  consequence, and marking a persona as inferred neither helps nor hurts.

What the opus-judged baseline shows:

- **The uplift sits in pressing and turn discipline**: `01`, `06`, and `02`. `presses-one-crux`
  is 12/12 against 0/12, `presses-from-root` 8/12 against 0/12, and `turn-discipline` 55/60 across
  its five cases against 20/60.
- **`11` keeps real uplift**: `does-not-manufacture-a-winner` 12/12 against 6/12 and
  `separates-verified-from-assumed` 12/12 against 8/12.
- **`16` shows none.** Both arms score 11/12 on `separates-verified-from-assumed`, so the
  held-out witness for `11`'s hill is now a floor. Under the sonnet judge it read as 9/12 against
  1/12; most of that gap was the judge.
- **`10` and `13` are floors in both arms.** The small gaps the sonnet-judged baseline showed there
  came from the judge and, on `10`, from `rival-actually-killed`'s old rubric.
- **Remaining headroom is on tuning cases only** (round 5 below moved the first): `turn-discipline` on `06` (7/12),
  `presses-from-root` on `01` (8/12), and `takes-the-persona-seat` on `14` (8/12). None has a
  held-out witness with headroom, so a change aimed at them can show a regression on the held-out
  set, never generalization.

## Hill-climb round 4 — 2026-10-06, opus judge

Plugin arm only, 12 runs per case, against the baseline above. Two edits in one round, aimed at
graders on different cases so their effects stay separable.

| Edit | Target | Result | Kept |
|---|---|---|---|
| Name an "and" that adds a second thing to answer as a second ask | `turn-discipline` on `06` | 7/12 → 7/12 | no |
| Drop the claim-marking clause | `separates-verified-from-assumed` holds | `11`, `12`, `16` all 12/12 | yes — dropped |

- **`06`'s remaining failures are one shape**: a question about where a claim comes from and what
  it is, joined by "and" ("which is the real complaint, and is that from your own practice?").
  Two wordings aimed at exactly that have now left it unchanged, so it was not worth a third. It
  is also debatable whether a person reads that as two asks.
- **The claim-marking clause was dead weight under the reliable judge**, so it came out. The
  earlier pooled evidence for it (below) was sonnet-judged.
- **Nothing else moved outside noise**: every held-out case scored 1.00, and no floor grader
  dropped. `presses-from-root` read 10/12 and `takes-the-persona-seat` 7/12, inside each
  grader's noise.

The shipped text is round 4's minus the one-ask rewording, that is, the baseline's skill with the
claim-marking clause removed. That exact text was not run as a round of its own.

## Hill-climb round 5 — 2026-10-06, opus judge

Plugin arm only, 12 runs per case, against the opus-judged baseline. Three edits, each aimed at a
grader on a different tuning case. The failing outputs behind each: `06` asked where a claim came
from and what it was in one question; `01` opened by agreeing with the user's chosen fix and
reframed only after; `14` named the cook's uses as a list of destinations and walked none of them
through to what the export must do there.

| Edit | Target | Baseline · v4 · v5 | Kept |
|---|---|---|---|
| One ask is one that one short answer settles | `turn-discipline` on `06` | 7/12 · 7/12 · 10/12 | yes |
| State the problem first, ahead of any lean on the stated solution | `presses-from-root` on `01` | 8/12 · 10/12 · 9/12 | no |
| Walk every use through to what it asks of the artifact | `takes-the-persona-seat` on `14` | 8/12 · 7/12 · 8/12 | no |

- **The `06` gain replicated.** Cases `01`–`08` re-run on the shipped text (the one-ask edit
  alone) gave `06` 11/12, so 21/24 across both runs against 14/24 on the two before. Held-out `05`
  stayed 12/12 in both, and `07`, `08`, and every other floor grader passed every run.
- **The other two edits bought nothing** and were reverted. `presses-from-root` read 7/12 on the
  confirmation run with its text unchanged, so its spread across rounds (7 to 10) is noise, and
  both hills are left where they were.
- `06` has no held-out witness of its own beyond `05`, which was already at ceiling, so this is a
  tuning-set gain that held out without regressing anything rather than a demonstrated
  generalization.

## Before and after this round of work, opus judge — 2026-10-06

Plugin arm only, 12 runs per case. `main`'s `figure-out` text (`results/fo-main`) against the
shipped text (`results/hillclimb-figure-out2/v5-confirm` for `01`–`08`, `…/final-1x` for
`10`–`16`), with the no-plugin arm from the opus-judged baseline. Mean case score: 0.76 without
the plugin, 0.90 with `main`'s text, 0.96 with the shipped text, so Δ moves from +0.14 to +0.20.

- **The whole gain is `turn-discipline`**: `02` 5/12 → 12/12 and `06` 4/12 → 11/12, with held-out
  `05` 10/12 → 12/12 in the same direction.
- **Nothing fell outside noise.** `01` and `14` are where they were (`presses-from-root` 7/12 →
  7/12, `takes-the-persona-seat` 6/12 → 7/12).

## Hill-climb on the persona seat — 2026-10-07, opus judge

Aimed at `takes-the-persona-seat` on `14`, the weakest grader left. Plugin arm only. Results in
`results/hillclimb-persona/`. Round 1 ran on `10`–`16` and once more on `14` alone; round 2 ran on
`10`–`16`, on the full suite, and four more times on `14` alone, so its `14` count matches the
unchanged text's 72 runs. Every case's `14` counts are pooled.

**This grader is noisier than 12 runs suggest.** Six measurements of `14` on text that does not
touch the persona line read 8, 7, 8, 6, 7, and 10 of 12: 46/72, or 64%. A single round moving it
by two runs says nothing; read pooled counts.

**Diagnosis.** A run with transcripts kept (`--keep-temp`) showed the failing runs do take the
cook's seat: their logs list the cook's uses one by one. The final read then folds them into a
single hand-off ("a text to their partner, Notes, Reminders: all take plain text") and stops where
the list leaves the app, never following it to the store, a partner shopping, or the next shop,
where different requirements appear. One run moved its whole spec into a side file and left a
summary in the reply.

| Round | Edit to the persona line | `14` pooled | Kept |
|---|---|---|---|
| — | unchanged text | 46/72 (64%) | — |
| 1 | each use, with what it asks of the artifact, is evidence the read carries | 15/24 (63%) | no |
| 2 | each use followed past where it leaves the artifact to where it ends | 51/72 (71%) | no |

- **Round 1 did nothing.**
- **Round 2 looked better at 36 runs (75%) and faded at 72 (71%)**: its last four runs of `14`
  read 8 each. Seven points over 72 runs a side is under one standard error, so it was not kept.
  This is the trap the noise note above describes: an early lead on a noisy grader regresses.
- **Every guard held in both rounds.** The full-suite run of round 2 scored every case at or near
  its baseline (`06` `turn-discipline` 9/12, inside the 10–11 it reads on the shipped text).
- **What is left to try** is outside the persona line: the `FEATURE` probe file, or the case
  itself, whose request names the mechanism's four parts and asks to hand the result straight
  to `/define`, which pulls the read toward the spec.

## Baseline — 2026-10-06, sonnet judge

**Superseded** by the opus-judged baseline above. Its judge mis-scored several graders, so its Δ
and the climb conclusions drawn from it do not stand.

Report `results/figure-out-baseline-20261006`. The skill with the two edits the hill-climb below
kept, CLI 2.1.289, agent `claude-opus-5-5`, judge `claude-sonnet-5-5`, 12 runs per arm. The
plugin arm is the climb's round 3 (`--ablation none`); the no-plugin arm comes from a both-arm run
of the same day on the same CLI, agent, and judge, which the skill text cannot reach. Plugin-arm
scores leave out `skill-fired`, as the CLI does under `with-without`. 
| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| 01-root-press | tuning | 0.83 | 0.00 | +0.83 |
| 02-assumed-cause | tuning | 0.96 | 0.50 | +0.46 |
| 04-hold-under-pushback | tuning | 0.96 | 0.83 | +0.12 |
| 06-strategic-open | tuning | 0.83 | 0.00 | +0.83 |
| 07-neg-lookup | tuning | 1.00 | 1.00 | 0.00 |
| 10-diagnosis-retry-window | tuning | 0.92 | 0.88 | +0.04 |
| 11-underdetermined | tuning | 0.89 | 0.33 | +0.56 |
| 12-living-with-it | tuning | 1.00 | 1.00 | 0.00 |
| 14-persona-seat-feature | tuning | 0.79 | 0.38 | +0.42 |
| 05-move-on-evidence | held out | 1.00 | 0.71 | +0.29 |
| 08-neg-authorized | held out | 1.00 | 1.00 | 0.00 |
| 13-status-quo-job | held out | 0.92 | 1.00 | −0.08 |
| 15-persona-seat-doc | held out | 1.00 | 0.92 | +0.08 |
| 16-underdetermined-billing | held out | 0.88 | 0.54 | +0.33 |

Mean Δ over the 14 cases **+0.28**, against +0.21 on the amended 2026-10-05 baseline.

- **The gain is in `turn-discipline`**: 55/60 with the plugin across the five cases that carry it,
  against 37/60 before the climb and 14/60 without the plugin. Held-out `05` went from 4/12 to
  12/12.
- **Every floor grader still passes every plugin run**, the four the climb could most easily have
  broken among them: `holds-position`, `updates-on-evidence`, `answers-without-deliberating`, and
  `complies-without-reopening`.
- **`separates-verified-from-assumed` is the softest number here.** Its 12-run counts on `11` and
  `16` ranged from 4 to 11 across this climb's runs, so read the hill-climb section's pooled
  figures, not one row.
- **`13-status-quo-job` sits just below the no-plugin arm** (0.92 against 1.00):
  `incident-evidence-used` is 10/12 with the plugin and 12/12 without. It was 10/12 against 11/12
  at the previous baseline, so this is not new, but it is the one case where the plugin trails.

## Hill-climb on turn discipline and claim marking — 2026-10-06, sonnet judge

**Sonnet-judged.** Round 4 above re-tested its claim-marking conclusion under the opus judge and
reversed it.

Plugin arm only, 12 runs per case, same CLI, agent, and judge as the baseline, the split above.
Rounds live under `results/hillclimb-figure-out/` (gitignored); the committed record is this
section and the baseline above.

An analyzer read only the tuning cases' outputs. It traced 14 of the 15 `turn-discipline` failures
to two shapes, both breaking the skill's own one-ask rule: a request for code or data carrying no
expected result, with a bare fallback ask after it ("if you can't share the code, tell me X"); and
two questions inside one ask. On `11`, failing reads stated their inferences flatly under a single
blanket caveat ("this rests only on the logs you pasted"), where passing reads tagged each step
where it was stated.

| Round | Skill text | `turn-discipline` tuning · held out | `separates-…` tuning · held out |
|---|---|---|---|
| baseline | — | 33/48 · 4/12 | 18/24 · 9/12 |
| v1 | one-ask edit + claim-marking clause | 45/48 · 12/12 | 19/24 · 10/12 |
| v2 | one-ask edit + marking moved into the read's definition | 40/48 · 11/12 | 21/24 · 10/12 |
| final | one-ask edit only (both arms) | 40/48 · 11/12 | 16/24 · 5/12 |
| v3 (kept) | v1 text again | 43/48 · 12/12 | 20/24 · 9/12 |

- **The one-ask edit** — a request for code, data, or a check carries the result you expect, and
  one ask excludes a second question folded in or a fallback — was kept on its first round and
  replicated in every round after it.
- **The claim-marking clause** — a claim is marked where it is stated, since a blanket caveat
  elsewhere marks nothing — moved held-out `16` by one run in v1 and was dropped by the keep rule.
  The both-arm verification run without it then fell to 4/12 on `11` and 5/12 on `16`. Pooled over
  every run of those two cases, the clause stands at 72/96 (four measurements, each 71–79%) against
  24/48 without it (two measurements, 63% and 38%), about three standard errors apart. It was
  restored. Held-out `16` alone gives 37/48 against 14/24, the same direction on less evidence.
- **The v2 placement was not kept.** It matched v1 on its target and slipped one or two runs on
  several other graders (`presses-one-crux`, `prices-doing-nothing`, `turn-discipline` on three
  cases). Each slip is inside the noise; together they pointed one way, and v1's placement costs
  nothing to prefer.
- **What this round taught about the keep rule.** One round's held-out case against one baseline
  could not see a 25-point effect on a grader this noisy; pooling the same grader across rounds
  could. For a grader whose 12-run count swings by several runs on unchanged text, compare pooled
  runs before reverting, not a single round.

## Baseline — 2026-10-05

**Superseded** by both 2026-10-06 baselines above; kept as the hill-climb's starting point.

Report `results/figure-out-baseline-20261005-1845`. Measured at `9a312219`, CLI 2.1.289,
agent `claude-opus-5-5`, judge `claude-sonnet-5-5`, 12 runs per arm, run in the container
`Dockerfile` defines.

| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| 01-root-press | tuning | 0.83 | 0.03 | +0.81 |
| 02-assumed-cause | tuning | 0.71 | 0.50 | +0.21 |
| 04-hold-under-pushback | tuning | 0.88 | 0.79 | +0.08 |
| 06-strategic-open | tuning | 0.79 | 0.00 | +0.79 |
| 07-neg-lookup | tuning | 1.00 | 1.00 | 0.00 |
| 10-diagnosis-retry-window | tuning | 0.92 | 0.90 | +0.02 |
| 11-underdetermined † | tuning | 0.81 | 0.33 | +0.47 |
| 12-living-with-it | tuning | 0.96 | 1.00 | −0.04 |
| 14-persona-seat-feature | tuning | 0.79 | 0.50 | +0.29 |
| 05-move-on-evidence | held out | 0.67 | 0.63 | +0.04 |
| 08-neg-authorized | held out | 1.00 | 1.00 | 0.00 |
| 13-status-quo-job | held out | 0.92 | 0.96 | −0.04 |
| 15-persona-seat-doc | held out | 1.00 | 1.00 | 0.00 |
| 16-underdetermined-billing ‡ | held out | 0.88 | 0.54 | +0.33 |

Mean Δ over the 14 cases **+0.21** (+0.19 over the original 13 before the two amendments below).

† **Re-measured 2026-10-06** (`results/figure-out-11-regrade-20261006`, same commit, CLI, agent
and judge) after a fix to `does-not-manufacture-a-winner`. The rubric counted only the two rivals
it lists, so a response that argued pool exhaustion down from the log timestamps while keeping
two rivals of its own alive, each with a deciding check, scored as manufacturing a winner. It now
counts any rival the response raises and says that arguing one of the listed pair down is ranking,
not closing. The grader moved from 8/12 to 11/12 with the plugin and from 3/12 to 0/12 without:
what looked like a hill was the rubric. `separates-verified-from-assumed` is the hill left on `11`
(6/12 against 0/12).

‡ **Added 2026-10-06** (`results/figure-out-heldout-new-20261006`, same commit, CLI, agent and
judge). `does-not-manufacture-a-winner` passes every run in both arms, a floor check;
`separates-verified-from-assumed` is 9/12 against 1/12, the held-out witness for `11`'s hill.

- **The uplift sits in pressing:** `01`, `06`, `11`, `14`, and `02`. `presses-one-crux` (12/12 vs
  0/12), `log-written` (12/12 vs 0/12), and `turn-discipline` on `01` (11/12 vs 1/12) carry most
  of it.
- **`12-living-with-it` no longer regresses.** `prices-doing-nothing` is 11/12 with the plugin
  against 12/12 without; the 2026-09-14 gap of −0.25 is gone.
- **`15-persona-seat-doc` has no headroom.** Its one grader passes every run in both arms; it is
  kept as a declared floor check (see the held-out split).
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
