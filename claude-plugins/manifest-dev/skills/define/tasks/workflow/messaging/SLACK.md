# SLACK Task Guidance

Slack messaging overlay for workflows using `--medium slack`. Composes with COLLABORATION.md (adds Slack-specific patterns, doesn't duplicate collaboration patterns).

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Channel specified | criteria-checker | Manifest PG or AC references a specific Slack channel for communication |
| Slack MCP available | criteria-checker | Slack MCP tools configured and accessible |

## Risks

- **Wrong channel** — updates posted to a channel stakeholders don't monitor; probe: which channel? is everyone in it?
- **Thread sprawl** — conversation splits across too many threads; probe: how to organize Slack communication per phase?
- **Noisy notifications** — stakeholders over-tagged, start ignoring messages; probe: who needs to be tagged vs just informed?

## Scenario Prompts

- **Stakeholder responds in wrong thread** — answer posted outside the tracked conversation; probe: how to handle scattered responses?
- **Unexpected pushback in Slack** — stakeholder raises concern not covered by interview; probe: how to handle scope changes surfaced via Slack?
- **Slack outage** — messaging medium unavailable during workflow; probe: fallback plan?
- **DM vs channel** — sensitive feedback that shouldn't be public; probe: any communication that needs to be private?

## Trade-offs

- Channel visibility vs DM privacy
- @channel vs @person vs no tag (Slack notification granularity)
- One thread per phase vs one thread per topic
- Verbose updates vs concise status-only

## Defaults

*Domain best practices for this task type.*

- **Tag once per thread** — Tag relevant stakeholders when posting a parent message; don't re-tag in follow-up replies within the same thread
- **Gentle nudges** — When following up on quiet threads, use brief friendly reminders without re-tagging or urgency framing
