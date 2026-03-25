# COLLABORATION Task Guidance

Multi-stakeholder overlay for tasks involving more than one person. Platform-agnostic — no Slack/GitHub-specific content (those belong in messaging and code-review overlays).

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Stakeholder coverage | criteria-checker | Every identified stakeholder has at least one touchpoint (notification, review request, or approval gate) encoded in manifest |
| Approval chain | criteria-checker | Required approvals encoded as ACs with verification method; no informal "someone should review" |

## Risks

- **Missing stakeholder** — someone who should approve or be notified isn't identified; probe: who else cares about this? who gets impacted?
- **Unclear authority** — multiple people could approve but no one is designated; probe: who is the final decision-maker?
- **Notification without action** — stakeholder notified but no AC captures their required response; probe: is notification sufficient, or is approval needed?
- **Owner bottleneck** — all decisions route to one person; probe: can anyone else unblock?

## Scenario Prompts

- **Stakeholder unavailable** — key approver is on vacation or unresponsive; probe: who is the backup? what's the escalation path?
- **Conflicting stakeholder feedback** — two stakeholders give contradictory input; probe: who has final authority?
- **QA tester finds non-AC issue** — valid concern but not covered by acceptance criteria; probe: does this task need QA? who performs it?
- **Communication overhead** — too many stakeholders slowing progress; probe: which interactions are blocking vs informational?

## Trade-offs

- Inclusive review vs speed (more reviewers = more thoroughness + more delay)
- Formal approval gates vs trust-based sign-off
- Notify everyone vs notify only those who need to act
