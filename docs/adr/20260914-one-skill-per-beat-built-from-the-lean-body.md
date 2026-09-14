# ADR: One skill per beat, built up from the lean body

## Status
Accepted

## Area
Prompt architecture

## Context

For one development cycle the workflow shipped two prompts for every beat: `figure-out`, `define`,
`do` and `auto` alongside `just-figure-out`, `just-define`, `just-do` and `just-auto`. The `just-*`
family was an experiment with an explicit claim — that a modern base model already carries much of
the discipline the longer prompts spell out, so a prompt that states its goal and names the
disciplines by the words that recruit them can do the same work with a fraction of the text. The
pair existed to make that claim testable rather than arguable.

Two prompts per beat is not a stable resting place. Every rule lives in two texts that drift, every
change costs two edits, and a user meeting the workflow has to choose between variants on a
distinction we never managed to explain in a sentence. The experiment had to resolve one way or the
other.

The behavioral eval suite at `claude-plugins/manifest-dev/evals/` was built to settle it for
`figure-out`, the beat where the two prompts differ most (162 lines against 83). Four scenarios
were duplicated into mirror cases naming the lean skill, and three more were measured separately,
so each scenario yielded three numbers: the no-plugin baseline, the lean prompt's score, and the
full prompt's score. All measurements ran at `runs: 12` per case per arm under
`--ablation with-without`, judged by a sonnet-tier judge.

### The measurement

| Scenario | Full prompt | Lean prompt | No-plugin baseline |
|---|---|---|---|
| `01-root-press` | 0.611 | **0.750** | 0.222 |
| `02-assumed-cause` | **0.917** | 0.875 | 0.583 |
| `04-hold-under-pushback` | 0.875 | **0.958** | 0.708 |
| `06-strategic-open` | 0.375 | **0.542** | 0.083 |
| `11-underdetermined` | 0.889 | **0.944** | 0.750 |
| `12-living-with-it` | 0.583 | **0.792** | 0.625 |
| `13-status-quo-job` | 0.917 | **0.958** | 0.958 |

Mean with-arm score: **lean 0.831, full 0.738** — a difference of +0.093, roughly 1.6 standard
errors given a per-run score standard deviation of about 0.37 at twelve runs per cell. Six of seven
scenarios favour the lean prompt; one favours the full prompt.

Two numbers carry caveats that both run against the lean prompt rather than for it. `02`'s lean
cell contains one run that died with an `ENOEXEC` spawn failure and scored 0; excluding it, that
cell reads 0.955 and the scenario flips to the lean prompt. `13`'s lean control arm was destroyed
by an infrastructure kill partway through and is not reported here — the full prompt's control is
shown in its place, and only the lean *with*-arm (clean, twelve runs) enters the comparison.

The comparison is with-arm to with-arm deliberately. Δ over the no-plugin control is the suite's
headline number for asking whether the plugin buys anything at all, but only the with-arm can
respond to a change in our own prompt, so a prompt-versus-prompt question reads the with-arms and
uses the control only to detect drift between measurements.

## Decision

**Converge on one skill per beat, and build each survivor up from its lean body rather than cutting
the long one down.**

The direction matters as much as the outcome. Pruning a long prompt means re-arguing every line
already written, and a draft's own weight reads as evidence that it was needed; the result lands
long. Authoring upward from a short body admits a line only when it carries something the run could
not reach on its own — a user ruling, knowledge outside the run's reach, or a default it
counteracts.

What each beat keeps differs, and only the first is measured:

- **`figure-out`** merges up: every capability of the longer prompt survives — `--team`, docs mode,
  Taste, ADR conventions, `--autonomous`, the investigation log, the probe files — with the bulk
  behind pointers into the existing `references/`, which move over unchanged. 4,623 words became
  1,551.
- **`define`** merges up on the same rule, with parity established by reading both prompts rather
  than by measurement: the task files and their Quality Gates and Defaults, the omission valve and
  bearer test, `--babysit`, multi-repo, gate altitude and gate extension, the Known Assumptions
  triage, criteria pinned by reaction, and the amendment path's rejection of a superseded schema.
  6,266 words became 2,091, with the schema deferred to a reference.
- **`do`** takes the lean body as it stands and is *deliberately* not at parity. The verification
  modes (`per-gate`, `consolidated`, `self`), `--verifier-model`, `--exhaustive-verification`, the
  gate ledger, caller overlays and external-review-input handling are retired. What survives is the
  part that binds: every gate declares its kind, a deterministic gate re-runs in full, a judgment
  gate reads the change once and thereafter judges prior findings' repairs and the delta, gate text
  changes only through the authoring skill, and completion requires fresh evidence per gate.
- **`auto`** takes the lean body as it stands; it stitches the three beats together and owns
  nothing else. Its `--babysit` chaining is retired — `babysit-pr` reaches `define --babysit`
  directly, so the capability keeps a caller.

## Alternatives Considered

- **Keep both families**: the honest reading of a 1.6-standard-error result is that it is
  suggestive rather than conclusive, which argues for more evidence before acting. Rejected because
  the cost of the fork is paid every day in doubled edits and drifting duplicate rules, while the
  evidence, though thin, points one way in six of seven scenarios and in no scenario points the
  other way once the error run is accounted for. Waiting had a known cost and an unknown benefit.
- **Cut the long prompts down to the lean shape**: the same end state by the opposite route.
  Rejected on the authoring principle above — pruning re-argues each line and lands long — and
  because the lean bodies are the artifacts that were actually measured. Cutting down would ship a
  third text nobody has evidence for.
- **Retire the lean family and keep the longer prompts**: rejected by the measurement, which is the
  whole reason the instrument was built.
- **Port `do`'s verification machinery onto the lean body**: rejected by the owner as a deliberate
  narrowing rather than an oversight. The modes bought assurance at a cost in prompt surface and
  run time that the gate-kind discipline already delivers most of.

## Consequences

### Positive
- One text per beat. A rule has one home, and a change is one edit.
- The always-loaded surface of the two heaviest skills drops by about two thirds.
- Users no longer choose between variants on a distinction that resisted a one-sentence
  explanation.
- The instrument that settled it survives: the eval suite, its held-out split, and its two rules for
  reading a number.

### Negative
- `define`, `do` and `auto` are converged on judgment and the owner's ruling, not on measurement —
  no eval case exercises any of them. A capability regression in manifest encoding or execution
  would ship unnoticed and be found in use.
- `do` loses independent verification outright. A run now judges its own work against each gate,
  which is a real reduction in assurance, accepted deliberately.
- `/auto --babysit` is gone as an entry point.
- The mirror cases are retired, so the comparison cannot be re-run: one of the two prompts no longer
  exists. These numbers are the record.

## Source
- Related: Supersedes 20260830-just-do-states-the-floor-and-keys-its-log-to-the-manifest;
  narrows 20260728-move-verification-execution-policy-to-do,
  20260730-consolidated-default-verification-mode,
  20260808-restore-per-gate-default-verification-mode,
  20260810-no-verifier-model-granularity,
  20260805-ratchet-judgment-gate-reverification,
  20260810-gate-altitude-repairs-under-advance-delegation;
  revises the cost position in 20260820-cost-is-a-binding-constraint-second-to-quality.
