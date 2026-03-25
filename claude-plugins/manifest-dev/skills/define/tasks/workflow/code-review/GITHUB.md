# GITHUB Task Guidance

GitHub code review overlay for workflows involving pull requests. Default for code tasks with workflow indicators (any CODING + WORKFLOW composition). Composes with WORKFLOW.md and optionally COLLABORATION.md.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| CI pipeline passes | criteria-checker | All workflow check runs pass for the PR |
| PR approved | criteria-checker | Required number of approvals met, zero outstanding changes_requested |
| Review comments addressed | criteria-checker | All PR review comments resolved or responded to |
| GitHub access | criteria-checker | `gh` CLI or GitHub MCP tools available and authenticated |

## Risks

- **Pre-existing CI failure** — PR blamed for failures already present on base branch; probe: is CI green on main?
- **Bot false positive treated as real** — automated reviewer flags something incorrectly, wasting a fix cycle; probe: which automated reviewers run on PRs?
- **Human comment ignored as bot-like** — legitimate human feedback dismissed; probe: who are the known bot accounts?
- **Stale approval** — reviewer approved an earlier version, code changed significantly since; probe: does re-approval matter?
- **Review scope mismatch** — reviewer focuses on style while AC requires architecture review; probe: what should reviewers focus on?

## Scenario Prompts

- **Bot reviewer infinite loop** — automated reviewer keeps finding new issues after each fix push; probe: which automated reviewers run? how to know when to stop fixing?
- **Reviewer requests out-of-scope change** — valid improvement but beyond the manifest's scope; probe: how to handle scope additions from review?
- **Multiple review rounds** — reviewer requests changes, fixes pushed, new issues found; probe: expected review rounds?

## Trade-offs

- Fix every bot finding vs focus on high-severity only
- Resolve threads immediately vs wait for reviewer acknowledgment
- Detailed PR description vs minimal summary

## Defaults

*Domain best practices for this task type. Auto-included as PG items; user reviews manifest.*

- **Label comments bot vs human** — Before classifying any review comment, label it by author. Known bots: Bugbot, Cursor, CodeRabbit, Dependabot, Renovate, and any author with `[bot]` suffix or app-type account. Handling differs per source
- **Classify before fixing** — Classify every review comment as actionable (real issue, clear fix), false-positive (premise incorrect or doesn't apply), or needs-clarification (unclear whether it applies) against manifest ACs before fixing anything
- **Bot comment resolution** — Bot comments don't engage in discussion. Actionable: fix and resolve thread. False-positive: post brief reason ("Reviewed — false positive: [reason]") and resolve thread
- **Human comment resolution** — Human comments need acknowledgment. Actionable: fix, post reply explaining the fix, wait for reviewer to approve before resolving. False-positive: post respectful explanation, wait for acknowledgment before resolving
- **CI failure triage** — Compare failing checks against base branch first (pre-existing failures are not the PR's responsibility — skip). Retrigger transient infrastructure failures (DNS errors, flaky tests) with empty commit. Only investigate and fix genuinely new failures caused by the PR
- **Bot review convergence** — After each fix push, automated reviewers may re-scan and produce new findings. Continue fixing genuinely new non-false-positive issues. Converge when new findings clearly diminish in frequency and severity. Log remaining low-severity items as follow-ups
