# WORKFLOW Task Guidance

Base guidance for tasks with a multi-step lifecycle: produce → review → approve → deliver. Domain-agnostic — works for code, writing, research, or any domain.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Phase assignment | criteria-checker | Phases ordered by iteration speed: fast local checks (lint, tests, reviewers) → E2E/integration tests (before PR — may require deployment to staging; if so, monitor deploy readiness, run tests, fix failures autonomously) → CI on PR → review approval → QA. No external wait in Phase 1. |
| Lifecycle coverage | criteria-checker | Every lifecycle stage (produce, review, approve) has at least one AC or INV-G with verification |

## Risks

- **Phase misordering** — expensive checks (review approval, CI) run before cheap checks (lint, tests), wasting external cycles on broken work; probe: what's the cheapest check that could fail?
- **Missing external gate** — task requires external approval but no AC encodes it; probe: who needs to sign off before this is done?
- **Unbounded external wait** — polling for CI/review with no timeout or escalation plan; probe: what if the external system doesn't respond in time?

## Scenario Prompts

- **Review rejection after passing verification** — all automated checks pass but human reviewer rejects for reasons not covered by ACs; probe: what would a reviewer check that automated gates don't?
- **E2E requires deployment** — E2E/integration tests need a running environment (staging, preview, local docker); probe: does E2E need a deployment? which environment? how to monitor deploy readiness before running tests?
- **Mid-execution scope change** — user says "also do X" or reviewer requests something not in the manifest during execution; probe: should scope changes be auto-amended or require explicit user approval? how complex are likely mid-execution changes?
- **Phase 3 context decay** — by review phase, implementation context has degraded; probe: how complex is this task? will review handling need full implementation context?

## Trade-offs

- QA phase vs trust automated verification
- Escalate immediately vs wait for external response
- Amend manifest on review feedback vs scope-out as follow-up

## Defaults

*Domain best practices for this task type.*

- **Structured manifest amendments** — When review reveals gaps not covered by existing ACs, amend the manifest with: what changed, which review comment triggered it, and reasoning for comments that were evaluated but not encoded
- **Escalate at phase boundaries** — When an external dependency blocks progress (CI pending, review not started, QA not complete), escalate rather than busy-waiting. Log what's done, what's blocking, and how to resume
