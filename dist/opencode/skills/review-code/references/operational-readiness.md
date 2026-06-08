# Operational-readiness review

Find changes that look acceptable in code review but will fail, degrade, or become unsafe when deployed, retried, scaled, rolled back, or run in CI.

**The question for every change: "What happens after this ships and the runtime starts applying pressure?"**

## Trigger surface

Focus on changes touching runtime/deploy surfaces: infrastructure, environment/config files, secrets, auth/public exposure, migrations, workers, queues, cron, retries, background jobs, observability, CI, expensive tests, performance-sensitive paths, external service clients, or operational runbooks.

Skip ordinary application logic unless it changes one of those operational surfaces.

## What to inspect

Be comprehensive in analysis, precise in reporting. Inspect every operational surface in scope, but report only concrete risks that pass the Actionability Filter.

### Deployment & Environment Wiring

- Required environment variables, secrets, feature flags, permissions, or config entries missing from one or more runtime environments
- Stage/prod/dev config inheritance or override mistakes
- Public vs internal endpoint exposure mismatches
- Manual provisioning, deploy ordering, or service dependency steps not accounted for
- Rollback incompatibility: old and new versions cannot safely coexist during a rolling deploy

### Data & Migration Safety

- Migrations, backfills, schema changes, or data shape changes that are not forward/backward compatible during deploy
- Non-idempotent jobs or scripts that may be rerun by deploy/retry automation
- Partial-failure paths that leave durable state inconsistent
- Cleanup/removal work that forgets dependent resources

### Asynchrony, Retries & Background Work

- Workers, queues, cron, webhooks, or scheduled jobs that are not safe under retry, replay, concurrency, or duplicate delivery
- Delay/scheduling handled in ad hoc code when the runtime already provides a scheduling primitive
- Missing acknowledgement/failure semantics that can drop or duplicate work
- Long-running work added to request paths instead of async runtime

### Runtime Cost, Scale & CI

- N+1 calls or per-item external IO on paths that run at production scale
- Memory, file descriptor, connection, or process growth in long-running processes
- CI/test changes that materially slow or destabilize the pipeline without necessity
- Expensive polling, sleeps, or broad test commands where targeted checks would verify the change

### Observability & Operability

- New failure modes without logs, metrics, traces, stable error codes, or grouping that lets operators diagnose them
- Error handling that hides operationally important context or creates noisy/unstable grouping
- Missing operational breadcrumbs for retries, workflow IDs, job IDs, external request IDs, or environment identity
- Runbook or deployment notes missing when the change requires human action to operate safely

## Actionability filter

Before reporting an operational risk, it must pass ALL criteria:

1. **In scope** — In diff-based review, report only operational risks introduced or affected by this change. In explicit path review, pre-existing risks are valid.
2. **Concrete failure mode** — Name the runtime condition and outcome: deploy order, missing config, duplicate event, rollback, scale, CI path, or operator action that fails.
3. **Evidence-backed** — Cite code, config, docs, deployment files, tests, or established neighboring patterns. Do not report generic "may be slow" or "could be risky" concerns.
4. **Operationally meaningful** — The risk affects deployment, production safety, data durability, security exposure, operability, CI reliability, or runtime cost enough to change behavior.
5. **Fixable in context** — Provide a specific mitigation: config addition, idempotency guard, generated/runtime primitive, migration sequence, targeted check, observability field, or rollout note.
6. **Not intentionally accepted** — If the change documents the trade-off and the operational risk is consciously accepted, do not report it unless the evidence shows the mitigation is incomplete.

## Out of scope (belongs to a sibling dimension)

Do NOT report on:

- Pure code correctness with no operational dimension → belongs to the code-bugs dimension
- API request/response contract mismatch → belongs to the contracts dimension
- General design fitness or misplaced responsibility with no runtime/deploy consequence → belongs to the code-design dimension
- Test coverage gaps or tautological tests → belongs to the test-quality dimension
- Pure security analysis beyond operational exposure/config evidence → belongs to security review
- Style, naming, or formatting unless they obscure an operationally important contract
- Speculative performance improvements without a concrete scale path

**Rule of thumb:** If the issue needs the phrase "after deploy", "under retry", "during rollback", "at production scale", "in CI", or "for operators" to explain why it matters, it belongs here. If it is just wrong code, wrong API usage, or messy structure, route to the neighboring dimension.

## Severity calibration

- **Critical** — Will block deploy, expose private functionality/data, corrupt durable data, or make rollback impossible for a primary runtime path. Must be fixed before shipping.
- **High** — Likely production or CI failure under normal rollout, retry, scale, or environment conditions. Must be fixed before merge.
- **Medium** — Operational fragility under plausible but narrower conditions: duplicate delivery, one environment missing config, noisy observability, slow CI path, non-critical cleanup gap. Should be fixed soon.
- **Low** — Minor operational polish with concrete value: clearer runbook note, more useful log field, small CI targeting improvement. Can be follow-up.

**Calibration check**: High/Critical findings require a specific runtime sequence. If you cannot describe the sequence, downgrade or drop.

## Dimension-specific report fields

Beyond the shared report skeleton, each finding for this dimension should make the operational scenario explicit:

- **Category**: Deployment & Environment Wiring | Data & Migration Safety | Asynchrony, Retries & Background Work | Runtime Cost, Scale & CI | Observability & Operability
- **Runtime Condition**: the concrete deploy/retry/rollback/scale/CI/operator condition that triggers it
- **Failure Mode**: what fails or degrades
- **Evidence**: code/config/docs/pattern evidence
- **Impact**: who/what is affected
- **Recommended fix**: the specific mitigation

If no risks pass the filter, the PASS report should briefly state which operational surfaces were checked.
