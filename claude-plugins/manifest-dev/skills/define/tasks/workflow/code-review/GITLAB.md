# GITLAB Task Guidance

GitLab code review overlay for workflows involving merge requests. Composes with WORKFLOW.md and optionally COLLABORATION.md.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| CI pipeline passes | criteria-checker | All pipeline jobs pass for the MR |
| MR approved | criteria-checker | Required number of approvals met, no revoked approvals without re-approval |
| Discussion threads resolved | criteria-checker | All MR discussion threads resolved or responded to |
| GitLab access | criteria-checker | `glab` CLI or GitLab MCP tools available and authenticated |

## Risks

- **Pre-existing pipeline failure** — MR blamed for failures already present on target branch; probe: is pipeline green on main?
- **Bot false positive treated as real** — automated reviewer (Danger, etc.) flags incorrectly; probe: which automated reviewers run on MRs?
- **Approval revoked after changes** — reviewer revoked approval after code was pushed; probe: does re-approval matter after changes?
- **Stale approval** — reviewer approved earlier version, significant changes since; probe: approval rules configured?
- **MR scope mismatch** — reviewer focuses on aspects not relevant to ACs; probe: what should reviewers focus on?

## Scenario Prompts

- **Bot reviewer loop** — automated reviewer keeps finding issues after each push; probe: which bots run? convergence criteria?
- **Reviewer requests out-of-scope change** — valid but beyond manifest scope; probe: how to handle?
- **Multiple approval rounds** — reviewer revokes, re-requests; probe: expected rounds?

## Trade-offs

- Fix every bot finding vs focus on high-severity only
- Resolve discussions immediately vs wait for reviewer
- Detailed MR description vs minimal summary

## Defaults

*Domain best practices for this task type. Auto-included as PG items; user reviews manifest.*

- **Label notes bot vs human** — Before classifying any MR note, label it by author. Known bots: GitLab CI Bot, Danger, Renovate, Dependabot, and any author with `bot` in username or service account type. Handling differs per source
- **Classify before fixing** — Classify every MR note as actionable, false-positive, or needs-clarification against manifest ACs before fixing anything
- **Bot note resolution** — Bot notes don't engage in discussion. Actionable: fix and resolve discussion. False-positive: post brief reason and resolve
- **Human note resolution** — Human notes need acknowledgment. Actionable: fix, reply explaining the fix, wait for reviewer acknowledgment. False-positive: post respectful explanation, wait for acknowledgment
- **Pipeline failure triage** — Compare failing jobs against target branch first (pre-existing failures → skip). Retrigger transient infrastructure failures with empty commit. Only fix genuinely new failures
- **Bot review convergence** — Continue fixing genuinely new non-false-positive issues after each push. Converge when new findings clearly diminish. Log remaining low-severity as follow-ups
