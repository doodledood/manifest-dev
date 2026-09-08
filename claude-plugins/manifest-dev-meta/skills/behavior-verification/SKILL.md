---
name: behavior-verification
description: 'Get live-traffic proof that a skill/prompt wording change actually changed the model''s behavior, not just a diff that reads like it should. Use when amending a manifest-dev skill/prompt and you want to confirm a tool gets invoked, a structural property of the request holds, or a compliance rate actually moved — via a baseline-vs-amended capture-and-assert framework, not by re-reading the wording.'
argument-hint: '<skill or prompt change to verify>'
user-invocable: true
---

A code-review pass on a skill/prompt wording change can only judge whether the new wording *reads* like it should produce the intended behavior. It cannot confirm the change actually produces that behavior in a real, live LLM call. `scripts/behavior_lab/` is a small framework for getting that proof from real captured traffic instead of from reading the diff.

See `references/EMPIRICAL_VERIFICATION.md` for the full workflow (scenario → arms → run → assert → diff) and the worked example.

This is opt-in tooling for developing manifest-dev itself, not a mandatory gate — see `docs/adr/20260705-empirical-verification-stays-opt-in.md` for why. Running even one arm through a real harness costs live API budget and wall-clock time; reach for this deliberately when a specific wording change's effect is uncertain or risky, not as a default step after every edit.
