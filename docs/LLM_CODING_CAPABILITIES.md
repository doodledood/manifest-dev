# LLM coding capabilities: implications for workflow design

Evidence reviewed: 2026-10-24.

This note informs workflow design for coding agents built on large language models (LLMs).
It does not set universal limits on what an agent can do. Findings depend on the model,
task, tools, instructions, and surrounding workflow. Keep those conditions attached when
drawing conclusions.

## What the sources support

**A workaround can outlive the limitation it addressed.** In its long-running application
experiments, Anthropic used context resets with Sonnet 4.5, then removed them when Opus 4.5
largely stopped the premature wrapping-up behavior those resets addressed. The same report
retained separate evaluation to address weak self-assessment. A model change can retire one
mechanism while leaving another useful.
[Source: Harness design for long-running application development, March 2026](https://www.anthropic.com/research/harness-design-long-running-apps)

**Context guidance needs the model and task attached.** Anthropic's context-engineering
guidance recommends retrieving information as needed and preserving relevant state across
long tasks. It describes degradation as a gradient that varies by model. Our inference is
that selective loading and recoverable progress are useful design options; this evidence
does not establish a universal limit on files, variables, or usable context percentage.
[Source: Effective context engineering for AI agents, September 2025](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

**Completion needs evidence from the work.** In Anthropic's multi-session web-app experiments,
agents sometimes left undocumented partial work or reported completion before the requested
behavior worked. Progress records, incremental implementation, and exercising the running
application helped in that setup. These observations do not establish a success rate for all
coding agents.
[Source: Effective harnesses for long-running agents, November 2025](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

**Separate agents have both benefits and costs.** Anthropic reports enterprise cases where
folding specialists into one agent with skills improved results and reduced handoffs. It
also describes uses for separate contexts: parallel work, context isolation, verification,
and permission boundaries. We take this as support for choosing boundaries around the work
and information needed, rather than assigning one agent to every named role.
[Source: When to fold subagents into your main agent loop, October 2026](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)

## How this project uses those findings

These are project design choices, not claims that the sources prove manifest-dev works:

- Cut work into outcomes that can be exercised in their intended use. Size follows the
  outcome and its dependencies, not an arbitrary number of files, minutes, or agents.
- Preserve the goal, decisions, remaining work, and evidence across interruptions.
  Let the executing workflow choose how to manage its context.
- Keep connected reasoning together when shared information helps. Use another context
  when independent judgment, substantial separate reading, parallel work, or different
  permissions justify it.
- Inspect relevant source code and documentation before relying on claims about a system.
  Establish completion from the agreed criteria and relevant evidence; a confident summary
  or another agent's approval alone does not demonstrate the requested behavior. Make
  missing evidence and blocked work visible.
- Let agents act within delegated authority while preserving the choices the owner retains.
  A capability limitation does not determine who has authority to decide.
- Revise guidance when actual use shows that a restriction no longer helps, or that a
  simpler workflow loses something important.

The [North Star](../NORTH_STAR.md) states the project's direction; the skills and accepted
[decision records](adr/README.md) own their specific workflow rules. The [slicing decision](adr/20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty.md)
remains grounded in exercisable acceptance; its historical capability claims are not current
limits on models.
