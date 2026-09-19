# Empirical skill-behavior verification

A code-review pass on a skill/prompt wording change can only judge whether the
new wording *reads* like it should produce the intended behavior. It cannot
confirm the change actually produces that behavior in a real, live LLM call —
whether a tool gets invoked, whether a structural property of the request
holds, whether a compliance rate actually moved. `scripts/behavior_lab/` is a
small framework for getting that proof from real captured traffic instead of
from reading the diff.

## Workflow

1. **Propose the amendment.** Have both the current wording (baseline) and
   the proposed wording (amended) available — e.g. two branches, or two
   copies of the skill file.
2. **Define a scenario.** A `Scenario` (`experiment.py`) is the task you want
   to exercise the target behavior: a prompt and the working directory to run
   it in. Nothing built-in ships here — bring the exact task that exposes the
   behavior you're checking (e.g. the actual verifier prompt that should or
   shouldn't invoke a given tool).
3. **Define the baseline and amended arms.** An `Arm` names a variant: which
   `Harness` adapter runs it, optionally which model/effort, and how to turn
   the scenario into the actual prompt sent (default: unchanged). Point the
   baseline arm's harness at a checkout with the current wording, and the
   amended arm's harness at a checkout with the proposed wording.
4. **Run.** `experiment.run_experiment(scenarios, arms, run_dir_base)` executes
   every (scenario, arm) pair through its harness adapter, capturing every
   real request/response through a logging reverse proxy
   (`proxy.py`/`harness.configure_for_capture`) into a deterministic,
   inspectable run directory.
5. **Assert.** Decode a run's captured calls via `transcript.decode_calls_for_run`
   (which calls the harness adapter's `decode_call` per raw entry — do not use
   `experiment.load_run_calls` here, that returns a usage-only summary with no
   `request_body`/`response_body`, so it can't be decoded), then check the
   target behavior with `assertions.assert_tool_invoked` (or a custom
   predicate) and compare arms in one call with `assertions.diff_arms`.
6. **Read the diff.** `diff_arms` returns per-arm compliance — read it
   directly to see whether the amended wording actually moved the behavior,
   rather than trusting that it should have.

```python
from behavior_lab.harness import ClaudeCodeHarness
from behavior_lab.experiment import Arm, Scenario, run_experiment
from behavior_lab.transcript import decode_calls_for_run
from behavior_lab.assertions import assert_tool_invoked, diff_arms

scenario = Scenario(name="verify-inv-g2", prompt=open("verify_prompt.txt").read(), cwd="/path/to/baseline-checkout")
arms = [
    Arm(name="baseline", harness=ClaudeCodeHarness()),
    Arm(name="amended", harness=ClaudeCodeHarness()),  # point cwd at the amended checkout instead
]
results = run_experiment([scenario], arms, run_dir_base="~/behavior-lab-runs")

calls_by_arm = {
    r.arm: decode_calls_for_run(ClaudeCodeHarness(), r.run_directory / "diagnostics")
    for r in results
}
print(diff_arms(calls_by_arm, lambda calls: assert_tool_invoked(calls, "Skill")))
# {"baseline": False, "amended": True}
```

## Harness coverage today

Only **Claude Code** is implemented (`ClaudeCodeHarness` in `harness.py`) —
routes traffic through `proxy.py`'s reverse proxy and decodes real
Anthropic-API SSE/chunked responses.

**Codex** and **Pi** are stubbed (`CodexHarness`/`PiHarness`), raising
`NotImplementedError` from every method. Both CLIs are confirmed to support
redirecting to a local proxy — Codex via `openai_base_url` in
`~/.codex/config.toml`, Pi via `baseUrl` in `~/.pi/agent/models.json` — so
adding a real adapter for either is a matter of implementing `invoke` against
that config mechanism and writing that CLI's own wire-format decoder for
`decode_call` (its request/response shapes differ from Anthropic's
SSE/chunked format `harness.py` already decodes). No live Codex/Pi traffic
was available when this framework was built, so those decoders don't exist
yet — the interface is ready for them.

## This is opt-in, not a mandatory gate

Nothing in this repo's workflow requires running `behavior_lab` before a
skill/prompt wording change ships. Running even one arm through a real
harness burns live API budget and real wall-clock time — this is a deliberate
action a developer takes when they want live-traffic proof for a specific
change, not something a verifier, skill, or CI check triggers automatically.
See `docs/adr/20260705-empirical-verification-stays-opt-in.md` for the
rationale and the alternatives (a mandatory gate, a sampled/budget-capped
gate) that were considered and rejected.
