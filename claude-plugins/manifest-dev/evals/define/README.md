# define eval suite

Measures whether `define` encodes a Manifest by the disciplines its own prompt states: not
whether it writes a document shaped like a Manifest, which only the with-plugin arm can do and
which would therefore make every case a vanity win.

Run it from the plugin directory:

```bash
claude plugin eval . --tag define --ablation with-without --judge-model sonnet --allow-tools Write Bash -j 8
```

The headline number is **Δ**, the with-plugin score minus the no-plugin baseline. Read the
figure-out suite's README (`../README.md`) before trusting a Δ from this one: its rules on
decomposing Δ by arm, the noise floor, and changing graders apply here unchanged.

**Status: not yet piloted.** No case here has been run. Expect some cases to show no headroom
(both arms pass), which removes them, and some graders to need calibration. Both are decided by
reading outputs, never by loosening a grader until it passes.

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
sends `/do` round the repair loop. The judge lists every gate and classifies it SETTLEABLE,
UNSTABLE, or UNREACHABLE before giving a verdict. `d10-loop-bait` is the case built to press it
hardest.

The copies are one rubric: `tests/test_eval_shared_graders.py` fails if they drift. Edit all of them
together.

What it does not catch: a gate that pins an incidental mechanism is settleable, but it still
causes rework when the executor meets the intent another way. `d02` covers that one separately.

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

## Held-out split (proposed)

Hold out `d04`, `d06`, and `d08` from tuning: one binding-rule case, one anchoring case, one
negative. Fix the split after the pilot drops any cases, before the baseline.

## Known limits

- **No repository.** Every prompt describes the codebase inline and says it is unavailable. A
  case that needs `define` to read real code would degenerate in both arms.
- **One turn of the interview.** The suite measures unattended encoding. Interview quality
  (which questions `define` surfaces, which it auto-decides) is out of scope.
- **The amendment manifest is inline.** Seeding files before a run is undocumented in the CLI,
  so `d09` asks the agent to save the pasted manifest before amending it.
