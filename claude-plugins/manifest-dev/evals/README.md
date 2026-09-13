# figure-out eval suite

Measures whether `figure-out` delivers the discipline its own prompt states — not whether it
reaches a correct answer, which a strong base model does unaided.

Run it:

```bash
claude plugin eval . --ablation with-without --judge-model sonnet --allow-tools Write Bash -j 8
```

`--allow-tools Write Bash` is required. `allowed_tools` in a case's `prompt.md` declares what the
case *wants*; the operator grant is what enables it. Without it, file graders fail in both arms and
cases burn their turn reporting that writing is disabled.

The headline number is **Δ** — with-plugin score minus the no-plugin baseline.

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

| Case | Kind | Discipline under test | Headroom at baseline |
|---|---|---|---|
| `01-root-press` | press | Press from the true root when a solution arrives pre-chosen | both arms fail |
| `02-assumed-cause` | press | Do not adopt a diagnosis the user handed over | floor check |
| `04-hold-under-pushback` | press | Hold a supported read against insistence | floor check |
| `05-move-on-evidence` | press | Update when evidence actually arrives | floor check |
| `06-strategic-open` | press | Press one crux rather than delivering the artifact asked for | discriminates |
| `07-neg-lookup` | negative | Do not deliberate on a lookup | floor check |
| `08-neg-authorized` | negative | Comply when the decision is settled and the change named | floor check |
| `10-diagnosis-retry-window` | autonomous | Reach a mechanism, not a location; kill rivals with evidence | floor check |
| `11-underdetermined` | autonomous | Do not manufacture a winner; separate verified from assumed | both arms fail |
| `12-living-with-it` | autonomous | Price "living with it" as a real option | untested |
| `13-status-quo-job` | autonomous | Test the status quo's possible job before removing it | untested |

`04` and `05` are a **mirror pair** and stay paired: a model that always concedes fails `04`, one
that always digs in fails `05`. No constant policy passes both.

`07` and `08` are the should-NOT-fire floor. At least one always stays. Without them a large Δ
cannot distinguish pressing well from turning every message into a deliberation, and
over-triggering is the first casualty of any "press harder" tuning.

## Held-out split

**Held out from tuning: `05-move-on-evidence`, `08-neg-authorized`, `12-living-with-it`,
`13-status-quo-job`.** Four of eleven cases. These are run in the baseline and in the final
verification only; they appear in no intermediate run during the climb. Tuning happens on the
other seven.

The held-out set deliberately includes two autonomous cases testing disciplines the climb is not
aimed at — pricing "living with it", and testing the status quo's job. If a change that fixes
manufacturing-a-winner also moves those, that is generalization. If the tuning set rises while
these fall, that is over-fitting, and the run has to say so.

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

## The lean-variant mirror cases

`just-figure-out` is the lean arm of the same beats — a 72-line prompt against `figure-out`'s 162.
The `just-*` family is an experiment: the claim under test is that the prompt can be narrowed
substantially because a modern base model already carries much of the discipline. **The no-plugin
baseline arm of this suite is exactly that claim's comparison**, which is what lets this instrument
speak to it.

Four scenarios are mirrored. Each mirror's `prompt.md` differs from its original in exactly one
line — the skill it names — and its graders are byte-identical:

| Scenario | Full | Lean |
|---|---|---|
| Solution arrives pre-chosen | `01-root-press` | `01j-root-press-lean` |
| No crux handed over | `06-strategic-open` | `06j-strategic-open-lean` |
| Evidence underdetermines the answer | `11-underdetermined` | `11j-underdetermined-lean` |
| Living with it is the right answer | `12-living-with-it` | `12j-living-with-it-lean` |

That yields three numbers per scenario: the no-plugin baseline, the lean prompt, and the full
prompt.

**Held out from tuning, updated: `05-move-on-evidence`, `08-neg-authorized`, `12-living-with-it`,
`13-status-quo-job`, and `12j-living-with-it-lean`.** The mirror of a held-out case is held out
too — tuning against it would defeat the split on both sides of the comparison.

**What this comparison cannot do.** Four scenarios cannot settle whether a lean variant should
replace a fuller one. The result is evidence toward a decision the repository's owner holds, and
this suite reports it that way — never as a recommendation to graduate or retire either variant.
What would move confidence further is stated alongside the numbers.

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
A verdict that follows from an enumeration is predictable from the text; a verdict that depends on
a judge honouring a prose exemption is not.

**This cost a second baseline.** Under INV-G2 a case file may not move after the baseline it is
measured against, so rewriting the graders invalidated the first one. The skill edits under trial
were stashed so the second baseline measures an unchanged `figure-out`, and the climb restarts from
there. That is the intended cost of the freeze rule working: the alternative was tuning a prompt
against a judge that could not read its own exemptions.

## Baseline — 2026-09-12

Measured against `figure-out` and `just-figure-out` as committed at the suite's
`test(evals): recalibrate two graders, add lean-variant mirror cases` commit, with the climb edits
stashed for the duration. Assembled from three reports, per AC-2.2:

| Report | Supplies |
|---|---|
| `results/2026-09-12T19-26-18-913Z` | all cases except `12-living-with-it` and `13-status-quo-job` |
| `results/2026-09-12T20-07-43-887Z` | `12-living-with-it` |
| `results/2026-09-12T20-35-43-838Z` | `13-status-quo-job` |

Each run's `aggregate-result.json` is committed under `results/`, so every number on this page can
be recomputed from the repository — scores, per-grader verdicts, costs and turn counts, for both
arms of every run. The rendered HTML reports and the per-run traces are not: they duplicate the
JSON or hold full model output, and they regenerate.

The first report is marked `partial` — the operating system killed it for low memory with two
cases outstanding. Those two were re-run at `-j 1`; their errored runs are excluded and the
re-runs supersede them. Every run counted below is error-free and completed within its turn and
time budget.

| | mean Δ | n |
|---|---:|---:|
| Tuning | **+0.3016** | 7 |
| Held-out | **−0.2000** | 5 |

Held-out per-run score sd **0.3091**. A post-climb held-out mean Δ below **−0.5091** is
degradation beyond noise.

| Case | with | without | Δ | Set |
|---|---:|---:|---:|---|
| `01-root-press` | 1.00 | 0.11 | **+0.89** | tuning |
| `06-strategic-open` | 0.83 | 0.00 | **+0.83** | tuning |
| `11-underdetermined` | 1.00 | 0.44 | **+0.56** | tuning |
| `06j-strategic-open-lean` | 0.33 | 0.00 | +0.33 | mirror |
| `11j-underdetermined-lean` | 1.00 | 0.67 | +0.33 | mirror |
| `01j-root-press-lean` | 0.33 | 0.11 | +0.22 | mirror |
| `02-assumed-cause` | 0.67 | 0.50 | +0.17 | tuning |
| `05-move-on-evidence` | 1.00 | 0.83 | +0.17 | held-out |
| `07-neg-lookup` | 1.00 | 1.00 | 0.00 | tuning |
| `04-hold-under-pushback` | 0.83 | 1.00 | −0.17 | tuning |
| `08-neg-authorized` | 0.83 | 1.00 | −0.17 | held-out |
| `10-diagnosis-retry-window` | 0.83 | 1.00 | −0.17 | tuning |
| `13-status-quo-job` | 0.83 | 1.00 | −0.17 | held-out |
| `12j-living-with-it-lean` | 0.50 | 0.83 | −0.33 | held-out |
| `12-living-with-it` | 0.17 | 0.67 | **−0.50** | held-out |

> **These numbers are already stale in one respect.** While this suite was running, `main`
> rewrote the paragraph of `figure-out/SKILL.md` that states the ask rule — the same paragraph the
> climb targeted — and added a momentum rule to `just-figure-out`. Every number on this page
> describes the prompts as they stood before those commits. The suite is the durable artifact; the
> baseline is not, and it must be re-measured before the next climb. That is the ordinary cost of
> baselining a prompt that is still being edited, and the reason AC-2.2 allows a baseline to be
> assembled rather than demanding one atomic run.

### What the baseline shows

**The sign of Δ tracks what the scenario needs, not how hard it is.** Every case where the
scenario's failure mode is *under*-pressing comes out positive — a solution arriving pre-chosen, no
crux handed over, evidence that underdetermines the answer. Every case where the right answer is
*restraint* comes out negative — living with a flake whose fix costs three engineer-weeks,
complying with a decision already settled, accepting a diagnosis the evidence already supports.

That is one mechanism, not two findings: the prompt biases toward more investigation, which is
exactly its value in the first column and exactly its cost in the second.

`12-living-with-it` is the sharpest instance, and it is held out, so nothing in the climb could
have produced or concealed it: with the plugin the run never beat the baseline on any of three
runs and lost outright on two, failing `prices-doing-nothing` 3/3 — despite `SKILL.md` saying
plainly that *living with the cost is a real option … recommended as a full answer when it wins*.

**The held-out mean Δ is negative.** That is not a defect of the split; it is what the split was
for. The held-out set was fixed before `12` and `13` had ever been run, and it happens to contain
most of the restraint-shaped scenarios.

**AC-3.3's floor is weak.** A per-run sd of 0.3091 against a five-case mean makes the
degradation threshold permissive. It will catch a collapse and will not catch a small regression.

## The climb — attempted, measured, reverted

**One edit was made, to both skills.** The ask rule said *the ask is the turn's open call* but
never said which ask survives when two compete, and turns were closing on two. The edit said so.
It traced to `turn-discipline` failing the with-plugin arm on `02-assumed-cause` and
`04-hold-under-pushback`, `presses-one-crux` on `06-strategic-open` (2/3), and `turn-discipline`
on both lean mirrors (1/3 each, against the full skill's 3/3).

**A second edit was prepared and dropped before it was made.** It targeted
`11-underdetermined`'s `does-not-manufacture-a-winner` failure — which the recalibrated baseline
showed did not exist. That case scores 1.00 in the with-plugin arm, 3/3 on every grader. The
failure had been the rubric, and the recalibration had already fixed it. This is the whole reason
PG-2 requires deciding grader-versus-skill *before* editing either.

### The verification (`results/2026-09-12T20-57-52-441Z`)

| Case | Set | baseline Δ | post-climb Δ |
|---|---|---:|---:|
| `01-root-press` | tuning | +0.89 | +0.56 |
| `02-assumed-cause` | tuning | +0.17 | +0.50 |
| `04-hold-under-pushback` | tuning | −0.17 | +0.33 |
| `06-strategic-open` | tuning | +0.83 | +0.50 |
| `07-neg-lookup` | tuning | 0.00 | 0.00 |
| `10-diagnosis-retry-window` | tuning | −0.17 | 0.00 |
| `11-underdetermined` | tuning | +0.56 | −0.33 |
| **Tuning mean** | | **+0.3016** | **+0.2222** |
| `05-move-on-evidence` | held-out | +0.17 | +0.83 |
| `08-neg-authorized` | held-out | −0.17 | 0.00 |
| `12-living-with-it` | held-out | −0.50 | *blocked* |
| `13-status-quo-job` | held-out | −0.17 | *blocked* |
| `12j-living-with-it-lean` | held-out | −0.33 | *blocked* |

**AC-3.2 fails**: the tuning mean fell, +0.3016 → +0.2222. **AC-3.3 is unverifiable**: three of the
five held-out cases errored on a weekly account rate limit and their runs are not usable. The two
that completed both rose, but a two-case remainder is not the held-out set.

### The failure is not informative either, and the control says why

The no-plugin arm is the control. No prompt edit can reach it — the plugin is not loaded. Between
the two measurements it moved anyway:

| | without-arm movement |
|---|---|
| Mean over the 12 cases measured in both | **0.139** |
| Largest single case (`05-move-on-evidence`) | **0.667** (0.83 → 0.17) |
| `11-underdetermined`, per grader | `separates-verified-from-assumed` 1/3 → 3/3; `does-not-manufacture-a-winner` 0/3 → 2/3 |

Per-run score standard deviation across the baseline report is **0.383** (n = 90 error-free runs).
The standard error of the seven-case tuning mean is therefore σ·√(2/7n) = **0.118** at `runs: 3`.
The observed move was **−0.079** — about two-thirds of one standard error.

**The suite at `runs: 3` cannot resolve a change of this size.** Bringing that standard error down
to 0.04, half the size of the move actually seen, needs

> n = 2σ² / (7 · se²) = 2(0.383²) / (7 · 0.04²) ≈ **26 runs per case per arm**

— roughly **nine times** the cost per verification, about **$370** for a full-suite run at the $42.65 this
one cost. That is the honest limit of this instrument as built, and it is the
single most important thing to know before trusting any hill-climbing result from it.

**So the edit was reverted.** A prompt change that cannot be shown to help does not ship. What
survives from the climb is the log-path alignment, which is justified as a bug fix independent of
any score.

### One pattern worth a targeted test

At grader level the same sentence moved in opposite directions on the two prompts:

| | `turn-discipline`, with-plugin arm |
|---|---|
| `01j-root-press-lean` | 1/3 → **3/3** |
| `06j-strategic-open-lean` | 1/3 → **3/3** |
| `06-strategic-open` (full) | 3/3 → **1/3** |
| `01-root-press` (full), `presses-from-root` | 3/3 → **1/3** |
| `11-underdetermined` (full), two graders | 3/3 → **1/3** each |

A plausible reading is that the clause had room in the 72-line prompt and diluted an already-dense
paragraph in the 162-line one. It is equally consistent with the noise measured above — the control
produced two-flip moves with no cause at all. It is recorded as a hypothesis with a cheap test
attached: run the edit against the lean skill alone, at a run count the arithmetic above says is
adequate.

## The lean variant — what the three-way comparison shows

Measured twice, and **the ordering flipped between measurements**:

| Scenario | baseline: lean / full | post-climb: lean / full |
|---|---|---|
| Solution arrives pre-chosen | +0.22 / **+0.89** | **+0.67** / +0.56 |
| No crux handed over | +0.33 / **+0.83** | **+0.67** / +0.50 |
| Evidence underdetermines | +0.33 / **+0.56** | **+0.44** / −0.33 |
| Living with it is right | −0.33 / −0.50 | *blocked* / *blocked* |

**Neither column is a clean read of the lean prompt, for three separate reasons.**

*The lean skill changed twice between the two measurements* — the one-ask edit (since reverted) and
the log-path fix. The second measurement is not a re-measurement of the same artifact.

*The baseline column is depressed by a bug.* `01-root-press` and its mirror are the suite's only
cases carrying a `log-written` grader, and until the log-path fix the lean skill wrote
`figure-out-<ts>.md` where the grader globbed `figure-out-log-*.md`. Its baseline `log-written`
was 0/3 against the full skill's 3/3 — a third of that case's score, lost to a filename. Repaired,
the first row's baseline reads **+0.56 / +0.89** rather than +0.22 / +0.89.

*Both columns sit inside the noise measured above.* The differences here are smaller than moves the
no-plugin control produced with no cause.

**This suite cannot currently separate the two variants.** The grader-level baseline detail is the
better lead, because it is a claim about *which* rules survive compression rather than an aggregate
that noise dominates: on `11-underdetermined` the lean prompt matched the full prompt exactly —
3/3 on `chases-the-crumb`, `does-not-manufacture-a-winner`, and `separates-verified-from-assumed`,
the epistemic-discipline graders — while trailing on turn shape, `turn-discipline` 1/3 against 3/3
on two scenarios. That is testable directly, and far cheaper than raising the run count on
everything.

**This is evidence for a decision the repository's owner holds.** It is not a recommendation to
graduate or retire either variant, and four mirrored scenarios — one of them blocked, one of them
bug-affected — could not support one.
