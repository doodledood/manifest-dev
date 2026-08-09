# ADR: The init-context skill lives in the core plugin, not in tools

## Status
Accepted

## Area
Repo layout

## Context

A new skill was needed to install manifest-dev's project surfaces — the glossary, the ADR conventions, and the context-file wiring — into a repository that has none, optionally seeding them from the project's own history. The obvious home looked like `manifest-dev-tools`, on the reasoning that this is a one-shot setup utility rather than part of the `figure-out → define → do` loop.

That reasoning does not survive contact with what the two plugins actually contain. `manifest-dev-tools` holds babysit-pr, handoff, prompt-engineering, re-pitch, review-pr, review-prompt, teach-me and walk-pr; none of them writes a project source surface. Core holds several skills that are equally outside the loop — check-pr, review-code and poll-slack — and they are there because a Manifest or `figure-out-team` invokes them. The dividing line in practice is not loop membership but invocation: core holds what core invokes.

Two facts forced the decision. The skill authors `CONTEXT.md` and `docs/adr/`, which core's figure-out already owns and now reads back at bootstrap. And figure-out's Bootstrap step needs to hand off to the skill when a project has neither — `.claude-plugin/marketplace.json` lists the two plugins as independent entries with no dependency edge, so a reference from core into tools would be broken by construction for anyone who installed core alone.

## Decision

`init-context` ships in the core `manifest-dev` plugin. figure-out's `WITH_DOCS.md` Bootstrap offers it when a project has no `CONTEXT.md` and no `docs/adr/`, replacing the bare minimal-scaffold write that step used to perform.

The rule this settles, for future placement questions: **core holds what core invokes**; tools holds user-invoked utilities that nothing in core reaches for.

## Alternatives Considered

- **Place it in `manifest-dev-tools`**: Matches the intuition that setup is adjacent to the workflow rather than inside it — Rejected: core could then never delegate to it, since the plugins have no dependency edge, and the skill writes exactly the surfaces core owns. The intuition also mis-describes the existing split, which already keeps three non-loop skills in core.
- **Grow figure-out's Bootstrap instead of adding a skill**: No new component, and the behavior already half-exists there — Rejected: bootstrap runs at the start of a deliberation session, while this is a deliberate one-shot repository setup that a user may want without any investigation, including from a harness where figure-out is not the entry point.
- **Duplicate the setup behavior in both plugins**: Each plugin self-sufficient — Rejected: two owners writing one file to different standards is the drift mechanism this whole change set exists to remove.

## Consequences

### Positive
- figure-out can delegate rather than scaffolding a weaker version of the same file.
- One owner for the project surfaces, so the conventions they carry cannot diverge between two writers.
- A reusable placement rule that explains the existing membership of both plugins.

### Negative
- Core grows another skill, and core is the plugin every user installs.
- Users who installed only `manifest-dev-tools` do not get the setup path at all.

## Source
- Session: figure-out session, 2026-08-09
- Related: 20260705-keep-plugin-first-layout-npx-skills-compatible
- Related: 20260809-adr-conventions-ship-as-project-knowledge
