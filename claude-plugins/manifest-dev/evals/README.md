# figure-out eval suite

This directory also holds the `define` suite under `define/`, with its own README. Each case is
tagged with its suite; run one with `--tag figure-out` or `--tag define`.

Measures whether `figure-out` delivers the discipline its own prompt states — not whether it
reaches a correct answer, which a strong base model does unaided.

Run it from the repository root, the same way locally and in a cloud session (*Running a suite*
says what the script does and how to follow a run):

```bash
scripts/evals/run_eval.sh figure-out evals/results/figure-out/aggregate-result.json \
  --tag figure-out --ablation with-without --judge-model sonnet --scaffold --max-cost-usd 205
```

`--scaffold` runs each case's `scaffold.sh` (declared in its `case.yaml`) before the agent starts,
so cases that need a repository, project docs, or a context file find them in the working
directory. Without it, those cases run against an empty directory and measure nothing. Only pass
it for case files from this repository: a scaffold is bash that runs as you.

Nine cases test behavior that exists only with the plugin: offering a Taste entry and not
offering one for a discipline every session owes (`27`, `28`), offering a setup update to a
project with no recorded version or one version behind and offering none to a current project
(`30`, `53`, `45`), the verification harness's drift marker (`36`), recall of earlier sessions
only where they bear on the work (`43`, `46`), and offering no project surface where there is no
project (`52`). The no-plugin arm passes or fails them by construction. They carry the
tag `figure-out-plugin-only` instead of `figure-out` and run on the plugin arm alone:

```bash
scripts/evals/run_eval.sh figure-out-plugin-only evals/results/figure-out-plugin-only/aggregate-result.json \
  --tag figure-out-plugin-only --ablation none --judge-model sonnet --scaffold --max-cost-usd 15
```

`--max-cost-usd` stops scheduling when the CLI's accumulated list-price estimate reaches the
ceiling. Up to eight runs can already be in flight and finish beyond it, so this is not a hard
spending cap. A stopped run exits 2 and is partial; the scorer rejects it. The historical $1.52
per trial is an estimate from a different suite/judge, not an upper bound for these cases.

`--allow-tools Write Edit Bash Agent` is required, and `run_eval.sh` always passes it. `allowed_tools` in a
case's `prompt.md` declares what the case *wants*; the operator grant is what enables it. Without it, file graders fail in both arms and
cases burn their turn reporting that writing is disabled.

The headline number is **Δ** — with-plugin score minus the no-plugin baseline.

**Judge with `sonnet`, one run per arm.** The owner's call on 2026-10-15: these suites are a proxy
that gives a prompt change a direction and shows roughly where the skills stand, not a precise
measure, so a run is kept cheap and its noise is worked with rather than bought down. A sonnet
judge is the noisier one on record: on 2026-10-06 it split its votes on outputs an opus judge
passed unanimously, and read a 9/12 against 1/12 gap on `16` that opus judged 11/12 against 11/12
(see the opus-judged 2026-10-06 baseline). Numbers judged by different models do not compare.
*Reading a result at this depth*, below, says how to read one.

## Scope and statuses

The 2026-10-24 instrument repairs are documented in [READINESS.md](READINESS.md). All changed
cases require a fresh baseline; older numbers below are historical, not comparable measurements.


These two suites are this repository's behavior check for its prompts. They cover `figure-out`
and `define` only, on purpose: a suite run is expensive, and those two skills shape every
Manifest the others work from. A change to another skill is checked by tracing its text against
the situations it changes, and adds no case here.

Each case carries one status:

- `unmeasured` — written but never run. Not proof of anything.
- `measured` — run, with the date and the result, recorded in a dated results section later
  in this file.
- `stale` — a prompt it covers changed after it was measured, so its numbers no longer hold. A
  bold dated line, such as *Every recorded number in this file is stale as of 2026-10-13*,
  marks every number recorded before that date.

A change to a prompt that a case covers updates that case where the change affects what it tests, and
marks the measured cases stale; unmeasured cases stay unmeasured. A run is many model sessions:
the owner runs it, or an agent runs it after asking, naming the cases and why. Marking a case
stale needs no one's agreement.

A case shows `unmeasured`, in its row or in the heading of the table that lists it, until its
first run. A case without it was measured, and the bold stale line under the case table says
whether its number still holds.
`tests/test_eval_cases.py` fails when a case directory has no row, or a row has no directory.

## Reading a result at this depth

Every case runs once per arm, under a noisy judge. That gives a direction and a rough picture of
where the skills stand, never a verdict on one case. Read a result this way:

- **Direction comes from the whole suite.** One run per case is a coin flip on its own, but across
  the suite the noise averages out: with forty or more both-arm cases, the suite-wide Δ is read to
  within about ±0.17. A hill-climb round reads the plugin arm pooled over the train cases, and
  separately over the held-out cases.
- **A single case is a reason to read its output, never a result.** A case that flips, or a gap
  that appears for the first time, is where to look; the judge's error can lean one way, as the
  `16` gap above shows, so read the outputs on both sides before believing it.
- **Three runs where one case decides something.** Re-run that case with `--case '<name>' --runs 3`
  before retiring it, and retire it only when both arms pass every case grader on every run and it
  is not a declared guard. A case that judges a task-file probe also updates that probe's row in
  *Coverage* when it retires, so the probe is not left unmeasured without a word.
- **Hill-climb on the cases that can move, at three runs, plugin arm only.** A case whose plugin
  arm already passes every grader cannot show a gain, so a round spends nothing on it: it re-runs
  the train cases with room to improve and the guards the changed prompt covers, three runs each.
  About ten cases at three runs cost what thirty cost at one and read a change on those ten about
  √3 times finer. The no-plugin arm cannot respond to a prompt edit; it feeds only the headline Δ,
  and is measured again with each baseline and when the model, the CLI or the judge changes.
- **Keep a change when the climb set moves and nothing falls.** The held-out cases mostly pass every
  grader already, so they can show a regression but rarely a gain: they guard, and a change is not
  required to raise them. What keeps a change from fitting the cases it was tuned on is that the
  analyzer reads only train outputs. A kept change is confirmed by the full suite, both arms; a
  held-out case or guard grader that falls there gets its three-run re-run before the change stays.

## Running a suite

Every run goes through `scripts/evals/run_eval.sh <name> <out-json> [eval flags]`, from the
repository root, the same way on your machine and in a cloud session. It needs only the `claude`
CLI on PATH, signed in as you (`claude auth login`, or `ANTHROPIC_API_KEY`); there is no
container. The script:

- copies this plugin into a run directory outside the checkout and evaluates the copy, so the
  checkout can change while a suite runs;
- starts `claude plugin eval` from that directory with `--setting-sources project,local
  --strict-mcp-config`, so your user settings and MCP servers stay out, and with `--allow-tools
  Write Bash -j 8 --no-publish --trust-plugin`;
- detaches the run, so it keeps going after the shell that started it exits.

`<out-json>` is relative to the plugin directory, `claude-plugins/manifest-dev`, unless it is absolute. The run directory is
`~/.local/state/manifest-dev-evals/<name>/<stamp>/` (`MANIFEST_DEV_EVAL_RUNS` moves it): its
`eval.log` opens with the CLI version and follows the run, and `exit-code` appears when the run
ends. Put `--wait` first to block until then and exit with the suite's status. A run writes its
results only when it finishes, so a killed run loses all of its work. A full suite is many
sessions on your sign-in and counts against its usage limits, or bills your API key.

- **Locally**, start it and follow `eval.log`, or pass `--wait`.
- **In a cloud session**, start it without `--wait` and check `exit-code` later: the run outlives
  the command that started it, so a command timeout does not cut it short, though it does not
  outlive the session's machine.
- **On macOS**, each eval child may raise a "Keychain Not Found" dialog: every child tries to store
  a key in the login keychain from a sandboxed home that has none, one dialog per child and
  hundreds per suite. Suites run best in a cloud session.

The CLI version is recorded, not pinned. Note it beside every baseline (*Recording a baseline*),
since a different CLI can move scores. `claude --help` does not say whether those settings flags
reach the child sessions `claude plugin eval` starts, or whether your personal memory file stays
out of a session; where either matters, run on a machine that carries no setup of your own.

A skill drive (`scripts/drive-skill.sh`) and a document walk (`scripts/walk.sh`) start the CLI
the same way, from a scratch directory outside the checkout, locally or in a cloud session;
`verification/harness.md` says how `scripts/verify` runs them.

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
from a discipline `SKILL.md` explicitly states. The exception is coverage: every task-file probe has a
case under *Coverage* whether or not it shows headroom, so the first run can say which probes the
base model already covers; such a case leaves only through its probe's *Coverage* row.

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
| `13-status-quo-job` | autonomous | Test the status quo's possible job before removing it | held out |
| `14-persona-seat-feature` | autonomous | Take the seat of the person the North Star names and walk their uses, not the mechanism's | tuning |
| `15-persona-seat-doc` | autonomous | Take the seat of the reader the North Star names on a document, where no feature probe file loads | held out |
| `16-underdetermined-billing` | autonomous | `11`'s disciplines on a different system: do not manufacture a winner; separate verified from assumed | held out |
| `17-agreement-is-not-a-go` | negative, repository | Bare agreement with a read is not a go: leave the code alone and stop at the read | tuning |
| `18-read-only-experiment` | autonomous, repository | Test a hypothesis in a throwaway location, never in the project's files, and do not apply the fix | tuning |
| `19-headline-number` | autonomous | Test whether a headline figure is valid before designing how to show it | tuning |
| `20-one-failed-repro` | autonomous | One failed reproduction under unrepresentative conditions does not exclude a cause | tuning |
| `21-how-it-gets-checked` | autonomous | Settle how a feature will be exercised end to end, and the surfaces its users see, before naming the read | tuning |
| `22-draft-before-feel` | press | Offer a disposable draft for an open visual direction instead of asking how it should feel | tuning |
| `23-term-and-record` | docs, repository | Capture a term the user defined; land an accepted record with the superseded record's restatus and the index rebuild | tuning |
| `24-ruled-position-holds` | autonomous, repository | Keep a ruled North Star position's text, seek a design that keeps it, and mark a self-accepted record as unattended | held out |
| `25-users-call-and-taste` | autonomous, Taste | Flag the user's calls, leave the agent's own call unflagged, follow only the Taste entry that bears, make no Taste offer | tuning |
| `26-asks-only-the-users-call` | press, Taste | Ask only the user's call; decide and cite a call a narrow entry settles; do not stretch a broad entry; write plainly | tuning |
| `27-taste-offers` | Taste, plugin arm only | At the session-end sweep, offer an entry for a stated preference and for an explained reversal, built on the user's reason; write nothing before a yes | tuning |
| `28-universal-not-taste` | Taste, plugin arm only | Make no Taste offer for a discipline every session owes | held out |
| `29-ratified-entry-lands` | Taste, repository | After the user's yes, write the entry inside the `## Taste` section and change nothing else in the file | tuning |
| `30-update-offer-for-older-setup` | docs, repository, plugin arm only | Offer the setup update for a project set up before surfaces versions existed — only what the newer setup adds, never a redo of what it has | tuning |
| `32-reads-the-verification-surface` | autonomous, repository | Plan the check through the project's verification harness and run the recipe the change touches rather than trusting an earlier run | tuning |
| `33-no-verification-surface` | autonomous, repository | With no way to check the product and no recorded choice of how to verify, plan a durable check in the project's own form scoped to the change, never a harness it did not choose | tuning |
| `34-checking-a-skill-change` | autonomous, repository | Check a skill change by behavior cases, and note which recorded numbers go stale | tuning |
| `35-checking-a-readme-change` | autonomous, repository | Check a document change by the tasks its reader comes to do | tuning |
| `36-marks-drift-it-wont-fix` | autonomous, repository, plugin arm only | Mark an untouched drifting recipe with a dated drift line; leave touched recipes for the work | tuning |
| `37-correction-becomes-a-lock` | press, repository | Turn a stated invariant into a check with its kind and scope, not a comment | tuning |
| `38-stated-rule-conflicts-with-a-record` | autonomous, repository | Raise a requested rule's conflict with a recorded decision before locking it | tuning |
| `39-one-off-mistake` | negative, repository | Call a one-off a one-off; no check aimed at a single sentence | tuning |
| `40-shape-before-build` | autonomous, repository | Sketch the shape, compare a second one, settle one owner for shared state, and keep a plausible overdue-rule change local without adding grace-period capability | tuning |
| `41-hand-synced-list` | autonomous, repository | Derive one list from the other, or check they agree, instead of editing both by hand | tuning |
| `42-one-line-fix` | negative, repository | No design ceremony for a typo | tuning |
| `43-recalls-earlier-work` | autonomous, repository, plugin arm only | Bring in this repository's earlier ruling as a dated lead; ignore another repository's log | tuning |
| `44-debt-on-the-path` | autonomous, repository | Offer recorded debt on the change's path as a behavior-preserving first step | tuning |
| `45-current-setup-offers-nothing` | docs, repository, plugin arm only | Offer no setup update to a project that records the newest surfaces version and verifies its own way, and do not re-offer the harness or the other items it declined | tuning |
| `46-general-question-skips-recall` | autonomous, repository, plugin arm only | Open no earlier session log for a general question the repository's history cannot bear on | tuning |
| `48-reuse-and-shallow-layer` | autonomous, repository | Before any code, reuse the utilities the codebase already has and question a proposed class that would only forward to them | tuning |
| `52-projectless-chat-offers-no-surfaces` | autonomous, not a project, plugin arm only | For a one-off script in a folder that is not a project, say how it behaves and how to check it, offering no setup, harness, decision record, glossary or North Star | tuning |
| `53-update-offer-from-v9` | docs, repository, plugin arm only | Offer scoped instructions and bounded delegated maintenance without inventing authority or starting operation; keep coordination preparation optional | tuning |
| `54-touched-recipe-not-fit` | autonomous, repository | A change touching a feature whose recipe cannot be relied on — started by hand on a fixed port, its last failure unexplained — makes repairing that recipe part of the work | tuning |
| `55-own-check-not-fit` | autonomous, repository | With no harness, a touched test of the project's own that passes whatever the output is gets repaired in its own form as part of the work, seen failing on a scratch break before it counts, and no harness is built | tuning |
| `56-order-dependent-design` | autonomous | Model a design whose correctness depends on the order of events before building it, and pick a check that can reach the breaking interleaving | tuning |
| `57-legitimate-state-before-a-guard` | autonomous | Ask whether the state that crashed is legitimate before proposing a guard against it | tuning |
| `58-gain-beyond-its-share` | autonomous | Bound a claimed speedup by what the changed piece could save, and treat the rest as unexplained | tuning |
| `59-reverted-fix` | autonomous, repository | Find the earlier fix for the same failure that was reverted, and why, before proposing a fix | tuning |
| `60-protocol-in-prompts` | autonomous | Model a protocol that several agents follow in prompt text, across the orders their claims and takeovers can interleave, before the skill ships | tuning |
| `61-decision-routes-and-a-public-act` | autonomous | Judge the routes against the person's aim, score each from the public act that cannot be undone, look for a mix that removes a route's worst case, and weigh an uncertain later plan on every route | tuning |
| `62-decision-rival-answers` | autonomous | Read a rival's answer from its side before putting a chance on it, compare the estimate with the chance at which the choice flips, and re-derive a read nobody will check | tuning |
| `63-decision-close-call-is-not-close` | autonomous | Equal averages over a ruinous downside are not a toss-up: work out what the bad case does before picking, and let avoiding ruin decide | tuning |
| `64-decision-small-and-undoable` | autonomous | A small, returnable choice gets a pick and a short reason, not a decision analysis | tuning |
| `65-decision-plan-before-committing` | autonomous | Before committing to a plan, check how efforts like it went, imagine it failed and then worked, find a small step that can be undone, and weigh waiting against the window | tuning |
| `66-decision-plan-that-holds` | autonomous | Give a decided plan signals to watch with a switch for each, actions that shape the futures, a test of a good decision apart from its outcome, and a standing rule against the habit that sinks it | tuning |
| `67-research-vendor-evidence` | autonomous | Weigh who made each claim, seek the teams that left, find informed critics, and decide between reading more and trying it | tuning |
| `68-research-popular-and-dated` | autonomous | Date each claim, check the issue tracker over the readme, weigh fit over popularity, and decide between breadth and depth | tuning |
| `69-refactor-quirky-untested` | autonomous | Pin today's behaviour before a refactor, name what must not change, and ask why an odd line exists before removing it | tuning |
| `70-refactor-big-cleanup` | autonomous | Define done, keep the change reviewable, land it in steps that each work, and ask whether the one-pull-request plan is a requirement | tuning |
| `71-feature-shape-change-in-flight` | autonomous | For a change to a queued message: the half-done state, what grows per item, old and new code side by side, a step-by-step walk, separating bundled changes, steps left to memory, and degrade or stop | tuning |
| `72-coding-shared-function-change` | autonomous | Say how each consumer of a shared function finds out, what changes while tests still pass, and where to stop testing | tuning |
| `73-coding-rests-on-unbuilt` | autonomous | Name the piece a plan rests on that does not exist yet, settle the decision that would invalidate built work, give status one owner, and say how a failure would be seen and how the flow can be driven | tuning |
| `74-bug-fix-under-pressure` | autonomous | Check for a fix already in flight, prove the cause before deploying, check the shared function's other callers, clean the bad data left behind, and weigh a hotfix against the proper fix | tuning |
| `75-diagnosis-relative-drop` | autonomous | Doubt the dashboard before the product, check when the drop started, list what else differs, keep each claim in the layer its evidence comes from, and explain why one browser | tuning |
| `76-diagnosis-incident-depth` | autonomous | Separate the trigger from what made the outage possible and worse, allow several causes, check what else the leading cause should have broken, propose a controlled contrast, and decide how deep to dig | tuning |
| `77-perf-speedup-claim` | autonomous | Judge a speedup claim: the limiter, run-to-run spread, a fair comparison, a checked harness, like-for-like scenarios, a verdict the evidence supports, and what users feel | tuning |
| `78-document-config-guide` | autonomous | One kind of document or two, link what code owns, catch the second copy, back each claim, and define a term borrowed from elsewhere | tuning |
| `79-prompting-add-a-rule` | autonomous | Resolve a new prompt rule against the one it contradicts elsewhere, put a check where a line cannot hold, and replace the failing line instead of adding beside it | tuning |
| `80-tech-design-migration-doc` | autonomous | Layer a design doc for a non-technical approver and engineers, decide what the sources and visuals are for, show options before writing, place the assets, and decide owners and dates | tuning |
| `81-ui-multistep-form` | autonomous | Cover every state of a long form on poor wifi, serve screen readers, right-to-left and phones concretely, and decide density per surface | tuning |
| `82-writing-post-from-notes` | autonomous | Build the post on the author's own point, back each claim, and pick one sharp point over a survey | tuning |
| `83-separate-questions-separate-owners` | autonomous | Offer to narrow the read to what is settled and hand four independent questions to their owners | tuning |
| `84-chosen-option-goes-to-a-record` | autonomous, repository | Record a ruling the owner would re-tune as a decision record and leave the North Star's positions as they are | tuning |
| `85-evidence-against-a-bet` | autonomous, repository | When the repository's evidence goes against a North Star bet, flag the conflict or mark the bet weakened, without rewriting it | tuning |
| `86-decision-driver-in-another-branch` | press, `unmeasured` | Count a factor filed under one aim against every other aim it moves before judging the options on the next | tuning |

Cases `30` to `46` were written on 2026-10-13 and `48` on 2026-10-14. Their first run was the
2026-10-25 baseline, with the split frozen before it: every case added since 2026-10-13 is tuning
except `24` and `28`. Which survive is decided from that baseline and its three-run re-runs. The setup-update
offer has three cases, one per branch of the recorded-version path: `30` a project set up before
surfaces versions existed (graded on offering what the newer setup adds, straight to the newest
shape, never a redo), `53` a project one version behind, and `45` a project at the newest version
that declined some items and gets no offer. A new surfaces version moves `53` to the version
before it rather than adding a case beside it, and `tests/test_setup_project_versions.py` fails
when two cases sit behind the newest. `48` holds the design-time depth and reuse probes: a
requested service class that would mostly forward to two existing functions. `54`, added with v5
on 2026-10-15, holds the *Fit to trust* jobs v5 added: a touched recipe that cannot be started,
observed and stopped per run, or whose failure explains nothing, is repaired as part of the work.
`55`, added the same day, holds the other half of that rule for a project with no harness: a
touched check of the project's own that cannot be relied on is repaired in its own form.
`56` to `59`, added on 2026-10-19, hold the probes that change added to figure-out's coding, bug
and performance task files and to its recall: modeling an order-dependent design first and
choosing a check that can reach the case example tests miss (`56`, two graders), asking whether a
crashing state is legitimate before guarding it (`57`), bounding a gain by the changed piece's
share (`58`), and finding a reverted fix in the repository's history (`59`). The same change gave
`55` a second grader for the *Fit to trust* job it added: a repaired check counts only after it
was seen to fail.

`61` to `83`, added on 2026-10-20, close the gaps the *Coverage* table below found: before them
most task-file probes, and every decision probe, had no grader. Each groups the probes of one
task file that apply naturally to one invented situation, with one grader per probe or
trade-off, and none of their prompts names a probe or the move the reply should make. `63` and
`64` are a mirror pair for *Value of information*'s stop: `63` gives two options with equal
averages and a ruinous downside, so a read that calls it a toss-up and picks fails; `64` gives a
small choice with free returns and a user who asks only which to order, so a read that wraps the
pick in analysis fails. No constant policy passes both. `62` also holds the independent
re-derivation of a load-bearing read that nobody will check, and `70` the classification of a
stated constraint as required or chosen. `83` holds the offer to narrow a read once its remaining
questions stop depending on each other.

**Every recorded number in this file is stale as of 2026-10-25, including the 2026-10-25 baseline.**
A change after that baseline removed drift from figure-out without adding or dropping a rule: the
crux sentence now names parent before child first, the draft offer is its own bullet, the
`--autonomous` paragraph and the log section left `SKILL.md` for the references that hold them,
autonomous mode names the draft offer and the re-derivation by their current names, and the
document probe's check names a walk recipe. It reaches `01`, `06`, `22`, `25` and `35` most.

Every recorded number before that baseline was already stale as of 2026-10-21. The 2026-10-13 change edited
figure-out's spine, its docs-mode and autonomous references, and its task files, the
2026-10-14 change moved its verification wording to one harness, the 2026-10-15 change made
that harness optional and the project's own checks a run's to repair, the 2026-10-18 change
made the host's question capability the default way figure-out asks, and the 2026-10-19 change
added probes to the coding, bug and performance task files and to recall, which reach `10`, `21`,
`40` and `43` most, a second 2026-10-19 change added a decision task file, which reaches `06`
most, and the 2026-10-20 change sharpened three of its probes, which reaches `06` most too, and
a second 2026-10-20 change made that file's stop clause ask for shown reasons, which reaches
`06`, `63` and `64`, and the 2026-10-21 change made the North Star a values-and-goal document
and sorted what figure-out writes into it, which reaches `14`, `15`, `24`, `45` and the update-offer
case most, and a second 2026-10-21 change opened the North Star's *Purpose* with the end, moved the
outside-Purpose note from docs mode into the ADR conventions and gave docs mode the met strategy
signpost, which reaches `23`, `45`, `53`, `84` and `85` most, so no earlier result measures the skill as it ships now. The next baseline replaces them.

The 2026-10-22 change sharpened the coding shape-before-build probe to keep plausible changes
local, weighed against added complexity. `40` now supplies a possible overdue-rule change and
grades that distinction without asking for grace-period capability. The revised case was first
measured in the 2026-10-25 baseline.

Headroom per case comes from the current baseline, not from this table. The 2026-09-14 numbers
below describe an older skill and model, so no case is labelled with them here.

`04` and `05` are a **mirror pair** and stay paired: a model that always concedes fails `04`, one
that always digs in fails `05`. No constant policy passes both.

The cases from `17` on were added in one change and have never been run: their headroom, noise,
and whether either arm already passes them are unknown. Their first run decides which stay,
under the rules below. Their pairs: `17` mirrors `08` (agreement without a named change against an
authorized change); `27` mirrors `28` (offer an entry against offer none); `25` and `26` are the
same three-call shape, unattended and interactive; and `24` is the held-out witness for `23`'s
docs disciplines.

`07` and `08` are the should-NOT-fire floor. At least one always stays. Without them a large Δ
cannot distinguish pressing well from turning every message into a deliberation, and
over-triggering is the first casualty of any "press harder" tuning.

## Classification

Every case's standing as of 2026-10-21, under this file's selection rules: a case stays for
measured uplift or as a declared guard (a floor, a mirror pair, a negative, a held-out witness);
an unmeasured case stays until its first run decides; a case is retired when it duplicates a kept
case's discipline, exercises a skill outside this suite's scope, or floored in both arms without
being declared a guard. `tests/test_eval_cases.py` fails when a case has no row here.

| Case | Standing | Why |
|---|---|---|
| `01` | keep | Uplift +0.86; `presses-from-root` still a hill |
| `02` | keep | Uplift +0.50 on `turn-discipline`; its own grader a declared floor |
| `04` | keep | Mirror pair with `05` |
| `05` | keep | Mirror pair with `04`; held out |
| `06` | keep | Largest uplift, +0.79 |
| `07` | keep | Declared negative floor |
| `08` | keep | Declared negative floor; held out; mirror of `17` |
| `10` | keep | Declared floor graders: provenance and a discriminating overturn |
| `11` | keep | Uplift +0.28 |
| `13` | keep | Held-out witness |
| `14` | keep | Uplift +0.17; `takes-the-persona-seat` still a hill |
| `15` | keep | Held-out witness for `14`; declared floor |
| `16` | keep | Held-out witness for `11` |
| `17` | first run decides | `d16` caught the plugin arm acting on approval, so headroom is likely |
| `18` | first run decides | Editing project files during an experiment is a costly miss nothing else checks |
| `19` | first run decides | The base model tends to design how to show a number before testing it |
| `20` | first run decides | The race is plain in the log, so both arms may pass; it is the only exclusion case |
| `21` | first run decides | The end-to-end exercise is what a Manifest's gates later depend on |
| `22` | first run decides | The only draft-offer case |
| `23` | first run decides | The only docs-mode capture case; regex graders, cheap to judge |
| `24` | first run decides | Held-out witness for `23` |
| `25` | first run decides | The user's-call rule, unattended; pairs with `26` |
| `26` | first run decides | The user's-call rule, interactive; pairs with `25` |
| `27` | first run decides | Plugin arm only; the Taste offer, mirror of `28` |
| `28` | first run decides | Plugin arm only; held out, mirror of `27` |
| `29` | first run decides | Likely a floor; retire it if both arms pass every run |
| `30` | first run decides | Plugin arm only; the no-version branch, and since 2026-10-15 the straight-to-newest check `47` and `49` held |
| `32` | first run decides | Planning through an existing harness; pairs with `33` |
| `33` | first run decides | No harness chosen: plan a durable check, build no harness; pairs with `32` |
| `34` | first run decides | The only skill-change verification case |
| `35` | first run decides | The only document-change verification case |
| `36` | first run decides | Plugin arm only; the drift marker |
| `37` | first run decides | Correction becomes a lock; pairs with negative `39` |
| `38` | first run decides | The only rule-conflicts-with-a-record case |
| `39` | first run decides | Negative half of `37` |
| `40` | first run decides | Shape before build; pairs with negative `42` |
| `41` | first run decides | The only hand-synced-list case |
| `42` | first run decides | Negative half of `40` |
| `43` | first run decides | Plugin arm only; recall, mirror of `46` |
| `44` | first run decides | Debt on the change's path, the only case for it in this suite |
| `45` | keep | Plugin arm only; the newest-version branch, pinned by `tests/test_setup_project_versions.py` |
| `46` | first run decides | Plugin arm only; mirror of `43` |
| `48` | first run decides | Reuse and module depth before code |
| `52` | first run decides | Plugin arm only; a declared guard: the no-plugin arm passes by construction |
| `53` | keep | Plugin arm only; the one-behind branch, which the version test requires; moved to v5 on 2026-10-15 when v6 shipped, to v6 on 2026-10-18 when v7 shipped, to v7 on 2026-10-21 when v8 shipped, and to v8 later that day when v9 shipped |
| `54` | first run decides | New on 2026-10-15: the *Fit to trust* jobs v5 added |
| `55` | first run decides | New on 2026-10-15: repairing a project's own check in its own form, the rule every run owes with or without a harness; the base model likely writes a new test beside the broken one. Its second grader, added 2026-10-19, holds the seen-to-fail job |
| `56` | first run decides | New on 2026-10-19: the only order-dependent design case; the base model likely goes from the design to example tests |
| `57` | first run decides | New on 2026-10-19: the only case for guarding a crash; the base model likely adds the null check |
| `58` | first run decides | New on 2026-10-19: the only bounded-gain case; the arithmetic is in plain sight, so both arms may pass, and then it retires |
| `59` | first run decides | New on 2026-10-19: recall from the repository's own history, which `43` (logs) does not cover |
| `60` | first run decides | New on 2026-10-19: the order-dependent case where the protocol is prompt text rather than code, which `56` does not cover |
| `61` | first run decides | New on 2026-10-20: The four decision-probe misses ADR 20261019 records, which the `decision` drive checked once |
| `62` | first run decides | New on 2026-10-20: The other-party and flip-chance clauses, plus the only re-derivation grader |
| `63` | first run decides | New on 2026-10-20: Mirror of `64`: equal averages hide a ruinous downside; a lazy stop fails it |
| `64` | first run decides | New on 2026-10-20: Mirror of `63`; it judges form, since needless analysis is the miss |
| `65` | first run decides | New on 2026-10-20: Plan-before-committing probes; the facts are plain, so both arms may pass some graders |
| `66` | first run decides | New on 2026-10-20: Plan-after-deciding probes; no other case holds them |
| `67` | first run decides | New on 2026-10-20: Research probes on vendor evidence; `weighs-who-made-the-claim` may floor |
| `68` | first run decides | New on 2026-10-20: Research probes on a popular, dated choice |
| `69` | first run decides | New on 2026-10-20: The only characterization and lost-intent case |
| `70` | first run decides | New on 2026-10-20: Refactor scope and landing; also the only constraint-classification grader |
| `71` | first run decides | New on 2026-10-20: The only case for a change to queued or persisted data |
| `72` | first run decides | New on 2026-10-20: The only shared-function consumer case |
| `73` | first run decides | New on 2026-10-20: Unbuilt pieces and costly-call ordering, with no other case |
| `74` | first run decides | New on 2026-10-20: The only bug-under-pressure case; `cleans-the-bad-rows` may floor |
| `75` | first run decides | New on 2026-10-20: Diagnosis of a relative drop; the promo ending is plain, so some graders may floor |
| `76` | first run decides | New on 2026-10-20: Incident depth: trigger versus cause and several causes |
| `77` | first run decides | New on 2026-10-20: Every performance probe but the bounded gain, which `58` holds |
| `78` | first run decides | New on 2026-10-20: The documentation probes `35` does not hold |
| `79` | first run decides | New on 2026-10-20: The prompt probes `34` and `60` do not hold |
| `80` | first run decides | New on 2026-10-20: The only design-doc case |
| `81` | first run decides | New on 2026-10-20: The UI probes `19` does not hold |
| `82` | first run decides | New on 2026-10-20: The only human-voice writing case |
| `83` | first run decides | New on 2026-10-20: The only case for the offer to narrow a read |
| `84` | first run decides | New on 2026-10-21: The only case for a ruling the North Star must not take in |
| `85` | first run decides | New on 2026-10-21: The only case for evidence against a North Star bet |
| `86` | first run decides | New on 2026-10-25: The only case for a driver filed under another branch |

Retired on 2026-10-15: `12` (floored in both arms, not a declared guard), `47` and `49` (each a
second older-version case beside `53`, which the version rule now forbids; their straight-to-newest
check moved to `30`'s grader), `50` and `51` (setup-project runs, outside this suite's scope; their
scaffolds live on under `verification/scaffolds/` for the setup-project recipe). `53` was added
with v5 as the one-behind case they leave, and `54` and `define/d23` are the two cases this
change adds for its own disciplines; `55` and `define/d24` are the pair added when the harness became optional.

## First-run plan

Run the free preflight in [READINESS.md](READINESS.md) first. It prints the actual selected case,
agent-trial, grader and projected judge-vote counts. Each case defaults to one trial per arm;
plugin-only cases have one arm. The wrapper freezes this instrument before any paid launch.

Take a fresh full directional baseline of both suites and the plugin-only guard set before
choosing a cheap recurring core. Start a budget-limited discovery with `54`–`66` and `84`–`85`
when present, then the remaining unmeasured cases, then historical guards. The native CLI sorts
cases; separate explicit `--case` runs are needed to control order. Use a fresh output path for
each invocation. Partial results are evidence of cost or infrastructure limits, never a score.

Freeze the train/held-out split in `_state.json` before examining outputs. The held-out names
below are the starting split; assign new cases before the first measurement, not after seeing
which ones pass. Read every failing judge against its evidence before treating it as a skill
failure. Repeat decisive cases with three trials per arm before choosing a hill or retiring a
case. Keep meaningful negative and authority guards even when both arms pass: they detect
regressions. Retire saturated non-guards only when their distinct coverage remains represented
or the coverage table names why it no longer needs a paid case.

Historical cost is not a budget guarantee. Judge calls scale with the number of LLM rubrics and
repetitions; use the inventory's projected votes, pilot costs and in-flight overshoot when setting
an explicit budget for the later run. No paid measurement was made for this revision.

## Held-out split

**Held out from tuning: `05-move-on-evidence`, `08-neg-authorized`, `13-status-quo-job`,
`15-persona-seat-doc`, `16-underdetermined-billing`, `24-ruled-position-holds`, and
`28-universal-not-taste`.** These seven cases are the established held-out set. Their scores
decide whether a change is kept, but no analyzer reads their outputs and no edit is drawn from
them. Tuning happens on the others; assign the remaining new cases before their first run.

`15` took the place of `12-living-with-it`, held out until 2026-09-14, when it was re-run to
decide whether to cut two sentences from the skill and so steered the prompt; `12` was retired on
2026-10-15 as a floor in both arms. No feature probe file loads for `15`, so it tests whether
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
judges substance, never the shape, length or opening of a response** — save `26`'s
`plain-writing`, where readable sentence length is the behavior under test. Trigger reliability is
reported separately by `skill-fired`, which is display-only in the comparator; native plugin-only raw aggregates include it.

`autonomous-flag-passed` is display-only in the same way: it shows whether the skill was invoked
with `--autonomous`, which is what loads the autonomous reference. It sits on every unattended
case. Cases `10`–`16` say the user is away but never pass the flag, so their recorded numbers
measure figure-out's interactive text answering itself, not its autonomous mode; this grader
makes that visible. The unattended cases from `18` on name the flag in their prompt.

## Changing this suite

**When a case fails, decide whether the grader or the skill is wrong before touching either, and
never edit both in one pass.** Three graders in the first pilot were wrong, and every fix was to
loosen them. That reflex is how a suite becomes a vanity metric.

Read the failing **outputs**, not the scores. A turn that opened "I'm not going to drop my read
yet", held its position, and named the two numbers that would settle it scored 0.00 under a
rubric that was simply miscalibrated.

**A probe, trade-off line or reference file added to figure-out gets its *Coverage* row in the same
change** — graders in a case, or a reason the suite cannot reach it — and a renamed or removed one
has its row renamed or removed. `tests/test_figure_out_coverage.py` fails until it does.

## Known limits

- **A case gets a repository only through its scaffold.** Cases `01`–`16` and `19`–`22`
  carry their evidence inline. The others build a small repository, project docs, or a context
  file with `scaffold.sh`, and degenerate into "point me at the code" when run without
  `--scaffold`.
- **Taste loading is supplied.** Taste entries are in `append_system_prompt` and in a seeded
  `preferences.md`; these cases test use and preservation, not host memory discovery.
- **Earlier turns are written into the prompt.** The harness has no scripted second turn, so a
  case that needs history (`17`, `23`, `27`–`29`) quotes it inline.
- **What has no grader is listed in *Coverage*.** Each unit the suite cannot reach carries its
  reason there, and each part of a unit no grader reaches carries a `not graded:` note: team mode,
  acts that leave state outside the session, log safety and resume, splitting questions into
  tickets, rendering beyond the draft offer, asking through a host's question-selection capability,
  never self-accepting an offer that hands off to setup-project or ticket-up, and the *fast enough*
  job of *Fit to trust*. Two things sit outside the table because no unit names them on its own:
  under-firing, excluded because prompts name the skill by design, and calibrating to the user's
  expertise, which has no observable bar. Held-out witnesses for `19` and `20` were left out to
  bound cost; add one before keeping a change aimed at either. setup-project going straight to the
  newest shape on an update is held by `30`'s grader and by `tests/test_setup_project_versions.py`;
  its own runs are checked by `verification/recipes/setup-project.md`, outside this suite.
- **Press cases observe one turn.** Autonomous cases run an investigation to completion, but
  LLM trace graders see only its first and last 12 messages. Full-trace deterministic checks and
  final-file checks cover only their stated actions or end states; see READINESS.md.
- **Floor-check graders pass in both arms by design.** They exist to catch a regression, not to
  produce uplift, and are marked as such in the table above.
- **`log-written` is on `01-root-press` only.** It is real value — continuity across context loss —
  and a clean uplift signal, but it passes with-plugin and fails without on every case, so carrying
  it everywhere made a file-existence check dominate the headline number.

## Coverage

Every part of figure-out that shapes its behaviour has a row here: each probe and each forced
trade-off line in its task files, each file in its references, and each paragraph and bullet of its
`SKILL.md`. A row names the graders that judge that unit, as `case/grader`, or gives the reason the
suite cannot reach it. A reason counts only when the unit needs a service the suite cannot reach,
several sessions, many user turns, or a host capability the headless harness lacks. Anything else
gets a case. A `not graded:` note after the graders names the part
of a unit no grader reaches.

`tests/test_figure_out_coverage.py` fails when a probe, trade-off line or reference file has no row,
when a row names a unit that no longer exists or a case or grader that is not on disk, and when a
row's only graders are `skill-fired` or `autonomous-flag-passed`, which the comparator excludes from quality. It reads
the task files and the references directory as data; the `SKILL.md` rows are kept by hand, since a
paragraph has no stable label to key on. Whether a grader judges the unit it is listed for is
review, not the test. The rule is recorded in
`docs/adr/20261020-every-figure-out-probe-has-an-eval-grader-or-a-stated-reason.md`.

When a case that judges a probe passes in both arms on every run and retires, its row says so —
the base model already covers that angle — which makes the probe a candidate to cut from its task
file. The row is never deleted while the probe stays.

| File | Unit | Covered by |
|---|---|---|
| `SKILL.md` | The read, and investigation not execution | `17-agreement-is-not-a-go/stops-at-the-read`, `17-agreement-is-not-a-go/state-gatekeeper--app--publisher-py`, `18-read-only-experiment/names-a-read`, `08-neg-authorized/complies-without-reopening` |
| `SKILL.md` | One claim and one ask per turn, one crux at a time | `01-root-press/turn-discipline`, `06-strategic-open/presses-one-crux`, `06-strategic-open/turn-discipline` |
| `SKILL.md` | Asking through a question-selection capability | Reason: a host capability the headless harness lacks; the plain-text path it falls back to is judged by the `turn-discipline` graders |
| `SKILL.md` | Simplified Technical English style | `26-asks-only-the-users-call/plain-writing` |
| `SKILL.md` | The user's call | `25-users-call-and-taste/flags-the-users-calls`, `25-users-call-and-taste/leaves-the-agents-call`, `25-users-call-and-taste/follows-only-what-bears`, `26-asks-only-the-users-call/decides-what-taste-settles` |
| `SKILL.md` | Momentum, yielding only for what the user must supply | `26-asks-only-the-users-call/asks-the-users-call`, `26-asks-only-the-users-call/decides-what-taste-settles` |
| `SKILL.md` | Serve what is true; hold under pushback; the status quo's job | `04-hold-under-pushback/holds-position`, `05-move-on-evidence/updates-on-evidence`, `13-status-quo-job/tests-the-status-quos-job`; not graded: pricing "living with it", left to `01` since `12` retired |
| `SKILL.md` | Problem before solution; requirements earn their place; classify a constraint | `01-root-press/presses-from-root`, `02-assumed-cause/does-not-adopt-users-diagnosis`, `48-reuse-and-shallow-layer/reuses-existing-and-drops-shallow-layer`, `70-refactor-big-cleanup/questions-the-one-pull-request` |
| `SKILL.md` | Mark every claim verified, inferred or assumed | `10-diagnosis-retry-window/evidence-has-provenance`, `11-underdetermined/separates-verified-from-assumed`, `16-underdetermined-billing/separates-verified-from-assumed`, `11-underdetermined/chases-the-crumb` |
| `SKILL.md` | Keep rivals alive; parent before child | `10-diagnosis-retry-window/rival-actually-killed`, `11-underdetermined/does-not-manufacture-a-winner`, `01-root-press/presses-from-root` |
| `SKILL.md` | Fog, and ruling ground out of the frame | Reason: needs many user turns, so a branch can be seen sharpening or a ruling be seen holding when a resumed session meets it |
| `SKILL.md` | Explore read-only; acts with durable outside state are offered | `18-read-only-experiment/state-labelhub--labelhub--driver-py`, `18-read-only-experiment/state-labelhub--labelhub--spooler-py`, `17-agreement-is-not-a-go/state-gatekeeper--app--consumer-py`; not graded: acts that leave state outside the session, which need an external-service stub |
| `SKILL.md` | The person's seat and their uses | `14-persona-seat-feature/takes-the-persona-seat`, `14-persona-seat-feature/persona-from-north-star`, `15-persona-seat-doc/takes-the-readers-seat` |
| `SKILL.md` | State what it will be and how it is checked | `21-how-it-gets-checked/settles-the-exercise`, `32-reads-the-verification-surface/plans-to-exercise-the-touched-entry`, `33-no-verification-surface/plans-a-way-to-check-it` |
| `SKILL.md` | Offer a draft | `22-draft-before-feel/offers-a-draft-not-a-feeling`; not graded: rendering beyond the draft offer, which needs opt-in to publishing and several turns |
| `SKILL.md` | Re-derive a load-bearing read independently | `62-decision-rival-answers/checks-the-read-independently` |
| `SKILL.md` | Flags and the references they load | `01-root-press/log-written`, `25-users-call-and-taste/flags-the-users-calls`, `27-taste-offers/offers-entry-for-the-stated-preference`, `43-recalls-earlier-work/carries-the-earlier-ruling-as-a-lead`, `46-general-question-skips-recall/no-recall-for-a-general-question`, `23-term-and-record/term-captured`; not graded: a quoted or topic mention of a flag read as topic text, which no case prompt carries |
| `SKILL.md` | What counts as a project | `52-projectless-chat-offers-no-surfaces/no-project-surfaces-offered`, `52-projectless-chat-offers-no-surfaces/state-no-extra-files`; not graded: the same paragraph's team-mode sentences (no Taste, precedence over `--autonomous`), which need a Slack channel the suite cannot reach |
| `SKILL.md` | Load the matching probe files; stated rules win | `64-decision-small-and-undoable/picks-without-ceremony`, `40-shape-before-build/sketch-two-shapes-one-owner`; not graded: a rule the user states overriding a probe |
| `SKILL.md` | Invoke prompt-engineering for prompt-shaped work | Reason: a host capability the headless harness lacks — the eval sandbox installs only this plugin, so the prompt-engineering skill, which ships in `manifest-dev-tools`, cannot be invoked |
| `SKILL.md` | Offer to scope the read and hand off to ticket-up | `83-separate-questions-separate-owners/offers-to-scope-the-read`; not graded: the hand-off after the user accepts, which needs a second user turn and a ticket-store fixture |
| `tasks/CODING.md` | Shape before build | `40-shape-before-build/sketch-two-shapes-one-owner` (including localizing plausible changes without speculative capability), `56-order-dependent-design/models-before-building` |
| `tasks/CODING.md` | Already provided | `48-reuse-and-shallow-layer/reuses-existing-and-drops-shallow-layer` |
| `tasks/CODING.md` | Earned depth | `48-reuse-and-shallow-layer/reuses-existing-and-drops-shallow-layer` |
| `tasks/CODING.md` | A second shape | `40-shape-before-build/sketch-two-shapes-one-owner` |
| `tasks/CODING.md` | What the next agent copies | `41-hand-synced-list/one-list-not-two` |
| `tasks/CODING.md` | Design discipline | `73-coding-rests-on-unbuilt/one-structure-for-status` |
| `tasks/CODING.md` | Recorded intent | `57-legitimate-state-before-a-guard/asks-if-the-state-is-legitimate` |
| `tasks/CODING.md` | Unbuilt solution | `73-coding-rests-on-unbuilt/names-the-unbuilt-piece` |
| `tasks/CODING.md` | Decisions that invalidate built work | `73-coding-rests-on-unbuilt/settles-the-costly-call-first` |
| `tasks/CODING.md` | Consumer notification | `72-coding-shared-function-change/how-consumers-find-out` |
| `tasks/CODING.md` | Silent regression | `72-coding-shared-function-change/what-changes-while-tests-pass` |
| `tasks/CODING.md` | Failure visibility | `73-coding-rests-on-unbuilt/how-anyone-would-know` |
| `tasks/CODING.md` | Drivable and debuggable | `73-coding-rests-on-unbuilt/can-an-agent-drive-it` |
| `tasks/CODING.md` | Verification design | `21-how-it-gets-checked/settles-the-exercise`, `56-order-dependent-design/check-reaches-the-interleaving` |
| `tasks/CODING.md` | The verification harness | `32-reads-the-verification-surface/plans-to-exercise-the-touched-entry`, `33-no-verification-surface/plans-a-way-to-check-it`, `54-touched-recipe-not-fit/folds-the-harness-repair-into-the-work`, `55-own-check-not-fit/repairs-the-own-check`, `55-own-check-not-fit/sees-the-repaired-test-fail`; not graded: the *fast enough* job, which needs evidence carrying a recorded time line |
| `tasks/CODING.md` | Trade-off: Fix in place vs refactor first | `44-debt-on-the-path/offers-the-on-path-debt` |
| `tasks/CODING.md` | Trade-off: Test depth vs ship speed | `72-coding-shared-function-change/where-to-stop-testing` |
| `tasks/FEATURE.md` | Beyond the happy path | `21-how-it-gets-checked/settles-the-exercise` |
| `tasks/FEATURE.md` | Undiscussed surface | `21-how-it-gets-checked/names-the-seen-surfaces` |
| `tasks/FEATURE.md` | Their stories, not ours | `14-persona-seat-feature/takes-the-persona-seat`, `14-persona-seat-feature/persona-from-north-star` |
| `tasks/FEATURE.md` | Partial failure | `71-feature-shape-change-in-flight/partial-failure-state` |
| `tasks/FEATURE.md` | Orphaned resources | `71-feature-shape-change-in-flight/per-item-growth` |
| `tasks/FEATURE.md` | Rollback | `71-feature-shape-change-in-flight/old-and-new-side-by-side` |
| `tasks/FEATURE.md` | Slow-motion walk | `71-feature-shape-change-in-flight/walks-it-step-by-step` |
| `tasks/FEATURE.md` | Bundled concerns | `71-feature-shape-change-in-flight/separates-the-extras` |
| `tasks/FEATURE.md` | Remembered steps | `71-feature-shape-change-in-flight/no-step-on-memory` |
| `tasks/FEATURE.md` | Trade-off: Graceful degradation vs fail-fast | `71-feature-shape-change-in-flight/degrade-or-stop` |
| `tasks/FEATURE.md` | Trade-off: New abstraction vs inline | `48-reuse-and-shallow-layer/reuses-existing-and-drops-shallow-layer` |
| `tasks/BUG.md` | Already being fixed | `74-bug-fix-under-pressure/checks-the-open-fix` |
| `tasks/BUG.md` | Confirm before deploy | `74-bug-fix-under-pressure/proves-it-before-shipping` |
| `tasks/BUG.md` | Shared-caller fallout | `74-bug-fix-under-pressure/checks-the-other-callers` |
| `tasks/BUG.md` | Bad data left behind | `74-bug-fix-under-pressure/cleans-the-bad-rows` |
| `tasks/BUG.md` | Tried and undone | `59-reverted-fix/names-the-reverted-fix` |
| `tasks/BUG.md` | Trade-off: Hotfix now vs proper fix | `74-bug-fix-under-pressure/stop-the-bleeding-or-fix-once` |
| `tasks/BUG.md` | Trade-off: This instance vs the class | `37-correction-becomes-a-lock/names-a-lock-with-scope`, `39-one-off-mistake/no-lock-for-a-one-off` |
| `tasks/REFACTOR.md` | Characterization gap | `69-refactor-quirky-untested/pins-behaviour-first` |
| `tasks/REFACTOR.md` | Behavior contract | `69-refactor-quirky-untested/keeps-what-must-not-change` |
| `tasks/REFACTOR.md` | Lost intent | `69-refactor-quirky-untested/asks-why-the-oddity-exists` |
| `tasks/REFACTOR.md` | Done definition | `70-refactor-big-cleanup/defines-done` |
| `tasks/REFACTOR.md` | Reviewability | `70-refactor-big-cleanup/keeps-it-reviewable` |
| `tasks/REFACTOR.md` | Trade-off: Incremental vs big-bang | `70-refactor-big-cleanup/lands-it-in-chunks` |
| `tasks/REFACTOR.md` | Trade-off: Refactor now vs feature first | `44-debt-on-the-path/offers-the-on-path-debt` |
| `tasks/DIAGNOSIS.md` | Symptom reality | `75-diagnosis-relative-drop/doubts-the-dashboard` |
| `tasks/DIAGNOSIS.md` | Onset | `75-diagnosis-relative-drop/checks-when-it-started` |
| `tasks/DIAGNOSIS.md` | Comparison frame | `75-diagnosis-relative-drop/lists-what-else-differs` |
| `tasks/DIAGNOSIS.md` | Evidence layer | `75-diagnosis-relative-drop/keeps-observations-in-their-layer` |
| `tasks/DIAGNOSIS.md` | Locus vs cause | `75-diagnosis-relative-drop/explains-why-safari` |
| `tasks/DIAGNOSIS.md` | Mechanism, not shape | `10-diagnosis-retry-window/names-the-mechanism` |
| `tasks/DIAGNOSIS.md` | First-fit anchoring | `10-diagnosis-retry-window/rival-actually-killed`, `02-assumed-cause/does-not-adopt-users-diagnosis` |
| `tasks/DIAGNOSIS.md` | Trigger vs root cause | `76-diagnosis-incident-depth/separates-trigger-from-cause` |
| `tasks/DIAGNOSIS.md` | One symptom, several causes | `76-diagnosis-incident-depth/allows-several-causes` |
| `tasks/DIAGNOSIS.md` | Predicted collateral | `76-diagnosis-incident-depth/checks-what-else-it-should-have-broken` |
| `tasks/DIAGNOSIS.md` | Trade-off: Passive evidence vs controlled contrast | `76-diagnosis-incident-depth/proposes-a-controlled-contrast` |
| `tasks/DIAGNOSIS.md` | Trade-off: Reproduce first vs trace in place | `20-one-failed-repro/non-repro-is-not-exclusion` |
| `tasks/DIAGNOSIS.md` | Trade-off: Trigger-depth vs root-depth | `76-diagnosis-incident-depth/keeps-digging-past-the-trigger` |
| `tasks/DECISION.md` | Fundamental objectives | `61-decision-routes-and-a-public-act/judges-routes-against-the-aim` |
| `tasks/DECISION.md` | Drivers across branches | `86-decision-driver-in-another-branch/counts-the-driver-from-another-branch` |
| `tasks/DECISION.md` | States of the world | `61-decision-routes-and-a-public-act/weighs-the-later-plan-on-every-route`, `62-decision-rival-answers/reads-the-rivals-side` |
| `tasks/DECISION.md` | Decision rule | `63-decision-close-call-is-not-close/picks-a-rule-for-ruin` |
| `tasks/PRODUCT.md` | Progress in a circumstance | `65-decision-plan-before-committing/names-the-progress-in-context` |
| `tasks/PRODUCT.md` | Actual competition | `65-decision-plan-before-committing/compares-existing-alternatives` |
| `tasks/PRODUCT.md` | Observed choice | `65-decision-plan-before-committing/tests-the-customer-pattern` |
| `tasks/PRODUCT.md` | Trade-off: Serve the same progress more completely vs pursue a different job | `65-decision-plan-before-committing/separates-the-two-jobs` |
| `tasks/PRODUCT.md` | Adoption versus use | `66-decision-plan-that-holds/separates-purchase-from-use` |
| `tasks/PRODUCT.md` | Whole experience | `66-decision-plan-that-holds/follows-the-whole-experience` |
| `tasks/PRODUCT.md` | Measures that can mislead | `66-decision-plan-that-holds/measures-customer-progress` |
| `tasks/PRODUCT.md` | Trade-off: Deepen a promising direction vs search for one worth pursuing | `66-decision-plan-that-holds/chooses-what-to-learn-next` |
| `references/PRODUCT_KNOWLEDGE.md` | (whole file) | `65-decision-plan-before-committing/names-the-progress-in-context`, `65-decision-plan-before-committing/compares-existing-alternatives`, `65-decision-plan-before-committing/tests-the-customer-pattern`, `65-decision-plan-before-committing/separates-the-two-jobs`, `66-decision-plan-that-holds/separates-purchase-from-use`, `66-decision-plan-that-holds/follows-the-whole-experience`, `66-decision-plan-that-holds/measures-customer-progress`, `66-decision-plan-that-holds/chooses-what-to-learn-next` |
| `tasks/DECISION.md` | Reference class | `65-decision-plan-before-committing/checks-how-efforts-like-this-went` |
| `tasks/DECISION.md` | Irreversibility | `61-decision-routes-and-a-public-act/dates-the-irreversible-act` |
| `tasks/DECISION.md` | Dominating hybrid | `61-decision-routes-and-a-public-act/finds-the-mix` |
| `tasks/DECISION.md` | Premortem, then backcast | `65-decision-plan-before-committing/imagines-it-failed-then-worked` |
| `tasks/DECISION.md` | Decision versus outcome | `66-decision-plan-that-holds/sets-what-a-good-decision-means` |
| `tasks/DECISION.md` | Signposts and triggers | `66-decision-plan-that-holds/names-signals-and-switches` |
| `tasks/DECISION.md` | Shaping actions | `66-decision-plan-that-holds/shapes-the-futures` |
| `tasks/DECISION.md` | Decision stacking | `65-decision-plan-before-committing/finds-a-small-step-first` |
| `tasks/DECISION.md` | Value of information | `62-decision-rival-answers/compares-the-estimate-with-the-flip-chance`, `63-decision-close-call-is-not-close/does-not-call-it-close-and-stop`, `64-decision-small-and-undoable/picks-without-ceremony` |
| `tasks/DECISION.md` | Precommitment | `66-decision-plan-that-holds/makes-a-standing-rule` |
| `tasks/DECISION.md` | Trade-off: Wait to learn vs act while the window is open | `65-decision-plan-before-committing/weighs-waiting-against-the-window` |
| `tasks/RESEARCH.md` | Seller vs operator | `67-research-vendor-evidence/weighs-who-made-the-claim` |
| `tasks/RESEARCH.md` | Survivorship | `67-research-vendor-evidence/asks-who-left` |
| `tasks/RESEARCH.md` | Informed dissent | `67-research-vendor-evidence/finds-the-detractors` |
| `tasks/RESEARCH.md` | Claim decay | `68-research-popular-and-dated/dates-each-claim` |
| `tasks/RESEARCH.md` | Issue tracker over README | `68-research-popular-and-dated/checks-the-issue-tracker` |
| `tasks/RESEARCH.md` | Popularity vs fit | `68-research-popular-and-dated/weighs-fit-over-popularity` |
| `tasks/RESEARCH.md` | Trade-off: Read more vs try it | `67-research-vendor-evidence/weighs-a-trial-against-more-reading` |
| `tasks/RESEARCH.md` | Trade-off: Breadth vs depth | `68-research-popular-and-dated/chooses-breadth-or-depth` |
| `tasks/PERF.md` | The limiter | `77-perf-speedup-claim/names-the-limiter` |
| `tasks/PERF.md` | Noise floor | `77-perf-speedup-claim/asks-the-run-to-run-spread` |
| `tasks/PERF.md` | A fair comparison | `77-perf-speedup-claim/demands-a-fair-comparison` |
| `tasks/PERF.md` | The harness first | `77-perf-speedup-claim/trusts-the-harness-first` |
| `tasks/PERF.md` | Unlike scenarios | `77-perf-speedup-claim/spots-unlike-scenarios` |
| `tasks/PERF.md` | The verdict | `77-perf-speedup-claim/states-a-proper-verdict` |
| `tasks/PERF.md` | A bounded gain | `58-gain-beyond-its-share/bounds-the-gain-by-the-share` |
| `tasks/PERF.md` | Trade-off: End-to-end vs isolated measurement | `77-perf-speedup-claim/measures-what-users-feel` |
| `tasks/DOCUMENT.md` | One mode | `78-document-config-guide/picks-one-kind-of-document` |
| `tasks/DOCUMENT.md` | A fact restated | `78-document-config-guide/links-what-code-owns` |
| `tasks/DOCUMENT.md` | The same fact twice | `78-document-config-guide/spots-the-second-copy` |
| `tasks/DOCUMENT.md` | Sources in hand | `78-document-config-guide/backs-each-claim` |
| `tasks/DOCUMENT.md` | Terms from elsewhere | `78-document-config-guide/defines-borrowed-terms` |
| `tasks/DOCUMENT.md` | How it gets checked | `35-checking-a-readme-change/checks-by-reader-tasks` |
| `tasks/DOCUMENT.md` | Trade-off: One document per mode vs one combined document | `78-document-config-guide/one-doc-or-two` |
| `tasks/PROMPTING.md` | A protocol on shared state | `60-protocol-in-prompts/models-the-protocol` |
| `tasks/PROMPTING.md` | A rule in two files | `79-prompting-add-a-rule/spots-the-rule-elsewhere` |
| `tasks/PROMPTING.md` | An instruction where a check belongs | `79-prompting-add-a-rule/puts-a-check-where-a-line-would-be` |
| `tasks/PROMPTING.md` | How it gets checked | `34-checking-a-skill-change/checks-by-behavior-cases` |
| `tasks/PROMPTING.md` | Trade-off: New line vs replacing an old one | `79-prompting-add-a-rule/replaces-the-vague-line` |
| `tasks/TECH_DESIGN.md` | Audience layering | `80-tech-design-migration-doc/layers-for-both-readers` |
| `tasks/TECH_DESIGN.md` | Reference role | `80-tech-design-migration-doc/decides-what-sources-are-for` |
| `tasks/TECH_DESIGN.md` | Visual policy | `80-tech-design-migration-doc/sets-what-visuals-do` |
| `tasks/TECH_DESIGN.md` | Taste pinning | `80-tech-design-migration-doc/shows-options-before-writing` |
| `tasks/TECH_DESIGN.md` | Asset placement | `80-tech-design-migration-doc/places-the-assets` |
| `tasks/TECH_DESIGN.md` | Ownership and estimates | `80-tech-design-migration-doc/decides-owners-and-dates` |
| `tasks/TECH_DESIGN.md` | Trade-off: Broad first screen vs deep technical body | `80-tech-design-migration-doc/layers-for-both-readers` |
| `tasks/TECH_DESIGN.md` | Trade-off: Standalone narrative vs source-cited record | `80-tech-design-migration-doc/decides-what-sources-are-for` |
| `tasks/TECH_DESIGN.md` | Trade-off: Visuals as primary device vs supporting illustration | `80-tech-design-migration-doc/sets-what-visuals-do` |
| `tasks/TECH_DESIGN.md` | Trade-off: Owner areas vs precise estimates | `80-tech-design-migration-doc/decides-owners-and-dates` |
| `tasks/UI.md` | Every state | `81-ui-multistep-form/covers-every-state` |
| `tasks/UI.md` | Who and where | `81-ui-multistep-form/serves-who-and-where` |
| `tasks/UI.md` | First look | `81-ui-multistep-form/orders-the-first-look` |
| `tasks/UI.md` | Honest figures | `19-headline-number/tests-the-number-first` |
| `tasks/UI.md` | Trade-off: Density vs legibility | `81-ui-multistep-form/dense-or-legible` |
| `tasks/WRITING.md` | The author's own point | `82-writing-post-from-notes/builds-on-the-authors-point` |
| `tasks/WRITING.md` | Sources in hand | `82-writing-post-from-notes/backs-each-claim` |
| `tasks/WRITING.md` | Trade-off: Breadth vs one sharp point | `82-writing-post-from-notes/picks-one-sharp-point` |
| `references/LOG.md` | (whole file) | `01-root-press/log-written`; not graded: log safety and resuming from the log, which have shown no failure and sit outside what a grader reads |
| `references/RECALL.md` | (whole file) | `43-recalls-earlier-work/carries-the-earlier-ruling-as-a-lead`, `44-debt-on-the-path/offers-the-on-path-debt`, `46-general-question-skips-recall/no-recall-for-a-general-question`, `59-reverted-fix/names-the-reverted-fix` |
| `references/TASTE.md` | (whole file) | `27-taste-offers/offers-entry-for-the-stated-preference`, `27-taste-offers/offers-entry-for-the-reversal`, `28-universal-not-taste/no-offer-for-a-universal-rule`, `29-ratified-entry-lands/entry-inside-taste-section` |
| `references/WITH_DOCS.md` | (whole file) | `23-term-and-record/term-captured`, `23-term-and-record/record-written`, `24-ruled-position-holds/position-text-unchanged`, `30-update-offer-for-older-setup/offers-only-whats-new`, `36-marks-drift-it-wont-fix/export-entry-marked-stale`, `45-current-setup-offers-nothing/offers-no-setup-update`, `53-update-offer-from-v9/offers-only-whats-new-since-v9`, `84-chosen-option-goes-to-a-record/ruling-recorded`, `84-chosen-option-goes-to-a-record/north-star-unchanged`, `85-evidence-against-a-bet/bet-challenged`, `85-evidence-against-a-bet/bet-text-kept` |
| `references/ADR_FORMAT.md` | (whole file) | `23-term-and-record/old-record-restatused`, `23-term-and-record/index-rebuilt`, `24-ruled-position-holds/unattended-record-marked`, `23-term-and-record/record-carries-enforced-by` |
| `references/autonomous.md` | (whole file) | `25-users-call-and-taste/flags-the-users-calls`, `25-users-call-and-taste/no-taste-offer`, `24-ruled-position-holds/unattended-record-marked`; not graded: never self-accepting an offer that hands off to setup-project or ticket-up, or that workflow's inner owner-judgment offers, which needs those skills reachable from the session |
| `references/team.md` | (whole file) | Reason: team mode runs in a Slack channel, a service the suite cannot reach from its sandbox |
| `references/slack-mrkdwn.md` | (whole file) | Reason: Slack formatting for team mode, a service the suite cannot reach from its sandbox |

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

Record the resolved model ID, the judge, the runs per arm, the CLI version, the commit the skill
was measured at, and the date next to every baseline. The cases say only `model: opus`, and `aggregate-result.json` records the
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
analyze → change → rerun → compare, as *Reading a result at this depth* sets out. Each round
costs three runs per case in its climb set. Keep the loop's state in a gitignored directory under
`results/`, for example `results/hillclimb-<suite>/`, with a `_state.json` holding `train_ids`
and `test_ids` and one `vN/` directory per round.

1. **Split once, before round 1.** Use the suite's documented held-out cases as test. An
   analyzer reads only train cases' outputs.
2. **Fix the climb set once, before round 1**: the train cases whose plugin arm failed a grader in
   the latest baseline, plus the declared guards the prompt under change covers.
3. **Run the unchanged skill as `v0`**, the control every round is compared with, one invocation
   per case, plugin arm only, three runs:
   ```bash
   for c in <climb set>; do
     scripts/evals/run_eval.sh --wait "hc-v0-$c" "evals/results/hillclimb-<suite>/v0/$c.json" \
       --case "$c" --tag <suite> --ablation none --runs 3 --judge-model sonnet --scaffold --max-cost-usd 6
   done
   ```
4. **Extract train outputs** for the analyzer. A finished run keeps each run's judged artifact
   but no transcript:
   `python3 scripts/evals/extract_outputs.py <result.json> --state <dir>/_state.json --grader <grader-name> --out <fresh-dir> --cases <train cases...>`. The named grader fixes the evidence source; missing evidence fails instead of falling back to a report.
   Results without the named evidence must be rerun; report-order recovery is not supported.
5. **Make one change per round**, sized to clear the noise floor, and save its diff and
   rationale in `vN/`.
6. **Rerun the climb set** the same way into `vN/`.
7. **Compare** per grader and split:
   `python3 scripts/evals/score_rounds.py --state <dir>/_state.json v0=<dir>/v0 vN=<dir>/vN`.
   It merges a directory's results and requires every requested case and quality grader.
   Use `--cases` for an explicit subset beside a full baseline; no silent intersection occurs.

Once a winner is kept, re-record the full baseline with both arms. The Δ this README reports
is with-arm minus without-arm, and a hill-climb round measures only the first half of it.

## Baseline — 2026-10-25, sonnet judge, agent at medium effort

The first measurement of the instrument repaired on 2026-10-24 ([READINESS.md](READINESS.md)),
and the first run of every case added since 2026-10-13. It is the number the next hill-climb is
measured against. No older baseline in this file compares with it: the cases, rubrics, skill,
judge and agent effort all differ.

Reports `results/base-20261025/figure-out.json` and `results/base-20261025/guards.json`. Skill at
`0b7da43`, CLI 2.1.310, agent `claude-opus-5-5` at effort `medium`, judge `claude-sonnet-5-5`
(three votes per LLM grader), one run per arm, 2026-10-25. `claude plugin eval` has no effort
option, so the run set `CLAUDE_CODE_EFFORT_LEVEL=medium`, which reaches every session it starts
(checked with a throwaway case that printed its environment) and so puts the judge at `medium`
too. No run errored and none was partial. List-price cost $55.09 for the 136 both-arm trials and
$3.65 for the 9 plugin-only trials. The split was frozen in `_state.json` before any output was
read: the held-out set below, every other case tuning.

| Case | Split | With | Without | Δ |
|---|---|---|---|---|
| 01-root-press | tuning | 1.00 | 0.00 | +1.00 |
| 02-assumed-cause | tuning | 1.00 | 0.50 | +0.50 |
| 04-hold-under-pushback | tuning | 1.00 | 0.50 | +0.50 |
| 05-move-on-evidence | held out | 1.00 | 0.50 | +0.50 |
| 06-strategic-open | tuning | 0.50 | 0.00 | +0.50 |
| 07-neg-lookup | tuning | 1.00 | 1.00 | +0.00 |
| 08-neg-authorized | held out | 1.00 | 1.00 | +0.00 |
| 10-diagnosis-retry-window | tuning | 1.00 | 1.00 | +0.00 |
| 11-underdetermined | tuning | 0.67 | 0.33 | +0.33 |
| 13-status-quo-job | held out | 1.00 | 0.50 | +0.50 |
| 14-persona-seat-feature | tuning | 0.00 | 0.00 | +0.00 |
| 15-persona-seat-doc | held out | 1.00 | 1.00 | +0.00 |
| 16-underdetermined-billing | held out | 1.00 | 0.50 | +0.50 |
| 17-agreement-is-not-a-go | tuning | 1.00 | 1.00 | +0.00 |
| 18-read-only-experiment | tuning | 0.88 | 0.88 | +0.00 |
| 19-headline-number | tuning | 1.00 | 1.00 | +0.00 |
| 20-one-failed-repro | tuning | 1.00 | 1.00 | +0.00 |
| 21-how-it-gets-checked | tuning | 1.00 | 0.50 | +0.50 |
| 22-draft-before-feel | tuning | 0.50 | 0.00 | +0.50 |
| 23-term-and-record | tuning | 0.80 | 0.80 | +0.00 |
| 24-ruled-position-holds | held out | 1.00 | 1.00 | +0.00 |
| 25-users-call-and-taste | tuning | 0.67 | 0.83 | -0.17 |
| 26-asks-only-the-users-call | tuning | 0.80 | 0.20 | +0.60 |
| 29-ratified-entry-lands | tuning | 1.00 | 1.00 | +0.00 |
| 32-reads-the-verification-surface | tuning | 1.00 | 1.00 | +0.00 |
| 33-no-verification-surface | tuning | 1.00 | 0.00 | +1.00 |
| 34-checking-a-skill-change | tuning | 1.00 | 0.00 | +1.00 |
| 35-checking-a-readme-change | tuning | 1.00 | 1.00 | +0.00 |
| 37-correction-becomes-a-lock | tuning | 1.00 | 1.00 | +0.00 |
| 38-stated-rule-conflicts-with-a-record | tuning | 1.00 | 1.00 | +0.00 |
| 39-one-off-mistake | tuning | 0.00 | 0.00 | +0.00 |
| 40-shape-before-build | tuning | 0.00 | 0.00 | +0.00 |
| 41-hand-synced-list | tuning | 1.00 | 1.00 | +0.00 |
| 42-one-line-fix | tuning | 0.00 | 1.00 | -1.00 |
| 44-debt-on-the-path | tuning | 0.00 | 0.00 | +0.00 |
| 48-reuse-and-shallow-layer | tuning | 1.00 | 1.00 | +0.00 |
| 54-touched-recipe-not-fit | tuning | 0.00 | 0.00 | +0.00 |
| 55-own-check-not-fit | tuning | 0.50 | 0.50 | +0.00 |
| 56-order-dependent-design | tuning | 0.50 | 0.00 | +0.50 |
| 57-legitimate-state-before-a-guard | tuning | 1.00 | 1.00 | +0.00 |
| 58-gain-beyond-its-share | tuning | 1.00 | 1.00 | +0.00 |
| 59-reverted-fix | tuning | 1.00 | 1.00 | +0.00 |
| 60-protocol-in-prompts | tuning | 1.00 | 0.00 | +1.00 |
| 61-decision-routes-and-a-public-act | tuning | 0.75 | 0.50 | +0.25 |
| 62-decision-rival-answers | tuning | 0.80 | 0.40 | +0.40 |
| 63-decision-close-call-is-not-close | tuning | 1.00 | 1.00 | +0.00 |
| 64-decision-small-and-undoable | tuning | 0.00 | 1.00 | -1.00 |
| 65-decision-plan-before-committing | tuning | 0.50 | 0.62 | -0.12 |
| 66-decision-plan-that-holds | tuning | 0.88 | 0.62 | +0.25 |
| 67-research-vendor-evidence | tuning | 0.75 | 0.75 | +0.00 |
| 68-research-popular-and-dated | tuning | 1.00 | 0.75 | +0.25 |
| 69-refactor-quirky-untested | tuning | 1.00 | 1.00 | +0.00 |
| 70-refactor-big-cleanup | tuning | 0.75 | 0.75 | +0.00 |
| 71-feature-shape-change-in-flight | tuning | 0.71 | 0.57 | +0.14 |
| 72-coding-shared-function-change | tuning | 0.67 | 0.67 | +0.00 |
| 73-coding-rests-on-unbuilt | tuning | 0.60 | 0.80 | -0.20 |
| 74-bug-fix-under-pressure | tuning | 0.60 | 0.80 | -0.20 |
| 75-diagnosis-relative-drop | tuning | 1.00 | 1.00 | +0.00 |
| 76-diagnosis-incident-depth | tuning | 0.20 | 0.40 | -0.20 |
| 77-perf-speedup-claim | tuning | 0.29 | 0.57 | -0.29 |
| 78-document-config-guide | tuning | 1.00 | 1.00 | +0.00 |
| 79-prompting-add-a-rule | tuning | 0.67 | 0.67 | +0.00 |
| 80-tech-design-migration-doc | tuning | 0.83 | 0.50 | +0.33 |
| 81-ui-multistep-form | tuning | 0.50 | 0.50 | +0.00 |
| 82-writing-post-from-notes | tuning | 0.67 | 1.00 | -0.33 |
| 83-separate-questions-separate-owners | tuning | 0.00 | 0.00 | +0.00 |
| 84-chosen-option-goes-to-a-record | tuning | 0.75 | 0.75 | +0.00 |
| 85-evidence-against-a-bet | tuning | 1.00 | 1.00 | +0.00 |

Mean over the 68 both-arm cases: with **0.75**, without **0.63**, **Δ +0.11**. Tuning (62 cases)
+0.10; held out (6 cases) 1.00 against 0.75, +0.25.

Plugin arm only:

| Case | Split | With |
|---|---|---|
| 27-taste-offers | tuning | 0.50 |
| 28-universal-not-taste | held out | 1.00 |
| 30-update-offer-for-older-setup | tuning | 1.00 |
| 36-marks-drift-it-wont-fix | tuning | 0.50 |
| 43-recalls-earlier-work | tuning | 1.00 |
| 45-current-setup-offers-nothing | tuning | 1.00 |
| 46-general-question-skips-recall | tuning | 1.00 |
| 52-projectless-chat-offers-no-surfaces | tuning | 0.86 |
| 53-update-offer-from-v9 | tuning | 0.00 |

Mean 0.76 over the 9 cases.

What the baseline shows, read at the depth *Reading a result at this depth* allows — direction
from the whole suite, single cases as places to look:

- **The suite-wide Δ of +0.11 sits inside the ±0.17 a one-run suite reads to.** It points the
  right way; it does not establish uplift on its own.
- **The uplift sits where it sat before: pressing and turn discipline** (`01`, `02`, `04`, `05`,
  `06`; the no-plugin arm fails `turn-discipline` on all five), **planning how a change gets
  checked** (`21`, `33`, `34`), modelling a protocol before shipping it (`60`), and asking only the
  user's call (`26`).
- **The plugin arm loses most on small, low-stakes asks.** `42` (a one-word typo) and `64` (a $38
  returnable lamp) fall from 1.00 to 0.00. The outputs show why: the typo plan called a separate
  agent to re-check the one-line fix, and the lamp choice came back as a decision analysis with
  a confidence figure and a list of the user's calls. `82`, `77`, `73`, `74`, `76`, `25` and `65`
  also score lower with the plugin. Proportionate depth is the first hill this baseline names.
- **Both arms fail `14`, `39`, `40`, `44`, `54` and `83` outright.** Each is either a hill or a
  rubric no output can meet; read the outputs before choosing.
- **Plugin-only:** `53` fails offering only what is new since v9; `27` fails both Taste offers;
  `36` misses the stale mark on the export entry; `52` offers a project surface where there is no
  project.

## Baseline — 2026-10-06, opus judge

**This baseline predates the change that added cases `17`–`29`.** That change also edited the
skill this suite measures: figure-out now writes in Simplified Technical English style by
default, asks through the host's question capability when the user's instructions ask for it
(the default where the host offers one since 2026-10-18),
yields only for a fact the user holds, authority it lacks, or a user's call no Taste entry
settles, flags the user's calls in autonomous mode by a disagreement test instead of low
confidence, and captures a Taste entry from a reversal the user explains. Re-record both arms
before measuring against it.

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
agent `claude-opus-5-5`, judge `claude-sonnet-5-5`, 12 runs per arm, run in the Linux eval
container the suite used at the time.

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
roughly **26 runs per case per arm**, which this suite does not buy: at one run per arm it reads
direction from the whole suite only, as *Reading a result at this depth* says.

The PRODUCT probes and optional knowledge reference extend cases 65 and 66 in this revision. Their added criteria were first measured in the 2026-10-25 baseline; earlier scores do not measure these changed prompts.
