# DIAGNOSIS — probing fuel

Angles that are easy to under-weight when explaining a symptom — an incident, anomaly, metric shift, or defect — before any fix is in sight. Considerations, not an agenda — most won't apply. Press the load-bearing ones; priority stays yours. Works for code and non-code subjects alike; composes with `CODING.md` + `BUG.md` when the subject is a code defect heading toward a fix.

## Blind-spot probes
- **Symptom reality** — Is the symptom itself trustworthy? The dashboard, metric, alert, or report can be wrong before the system is.
- **Onset** — Did it actually start when you think it did, or is that just when someone first looked? The true start time often reframes the cause.
- **Trigger vs root cause** — What set it off, what made it possible, and what merely made it worse are different answers. Which one is this investigation actually after?
- **Mechanism, not shape** — Can you name the specific variable, value, and sequence at the failure moment? A pattern name ("it's a race", "stale state") is a shape, not a mechanism — keep tracing until it's concrete.
- **One symptom, several causes** — Is this definitely a single cause, or could the symptom be the sum of more than one acting together?
- **Predicted collateral** — If the proposed mechanism is real, what else should it have broken or left behind — and did it?

## Forced trade-offs
- Reproduce first vs trace in place — invest in a controlled repro, or chase the live evidence where it happened?
- Trigger-depth vs root-depth — stop once the trigger is found and mitigated, or keep digging to the mechanism that allowed it?
