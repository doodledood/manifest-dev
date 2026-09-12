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
