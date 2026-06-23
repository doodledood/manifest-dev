# ADR: Use universal goal-setting language for unattended run backstops

## Status
Accepted

## Context

manifest-dev added unattended-run backstops so long autonomous flows do not stop after the first model turn. The source prompts currently express that backstop using Claude-style `/goal` examples, while the Pi sync reference strips those `/goal` blocks because Pi does not expose that exact command. That creates two problems: the source text names a harness-specific primitive, and the generated distributions need special-case edits to preserve or remove the same intent.

The user clarified the desired boundary: keep universal language so the same prompt intent works across harnesses without special harness logic. The important capability is not the literal `/goal` command; it is a durable, host-level completion condition that keeps or reopens the run until the workflow is actually complete. When a harness exposes that capability, the model should use it directly. When it does not, the model should output the goal text for the user to copy into whatever host mechanism exists.

This matches the prompt-engineering discipline already documented in the project: prompt lines should name portable capabilities in natural language rather than harness-bound primitives, except where the harness-specific primitive is itself the subject of the implementation.

## Decision

Source prompts should describe unattended-run backstops in universal goal-setting language.

The rule is: if the active harness provides a goal-setting, continuation, or durable-completion-condition capability, set the goal automatically using that capability. If no such capability is available, print the same completion condition in a copy-pasteable form for the user to apply manually.

The source prompts should not hardcode `/goal` as the only mechanism, and Pi should not remove the guidance just because its mechanism is not named `/goal`. Distribution-specific conversion may adapt command syntax or examples where a target needs it, but the behavioral intent remains the same across targets: use the harness-native goal-setting capability when available; otherwise surface a manual copy-paste fallback.

The completion condition remains concrete and checkable: figure-out autonomous runs stop only after the Read is named with full anatomy; `/define` handoffs describe manifest-complete execution; `/auto` spans figure-out → define → do; `/do` spans all Acceptance Criteria and Global Invariants PASS plus done. The portable wording changes the mechanism boundary, not the rigor of the backstop.

## Alternatives Considered

- **Keep concrete `/goal` in source and strip it from Pi**: rejected because it bakes one host's primitive into shared prompt assets and makes Pi lose the backstop instead of using its own equivalent capability.
- **Maintain separate harness-specific source prompts**: rejected because it increases drift for a behavior whose intent is portable.
- **Always print copy-pasteable text, even when the harness can set goals directly**: rejected because it makes capable harnesses depend on user manual action and weakens autonomous execution.

## Consequences

### Positive

- The unattended-run backstop becomes a portable behavior instead of a Claude-specific command pattern.
- Pi and future hosts can use their native goal-setting mechanisms without losing the guidance or needing source-level forks.
- Users on less capable harnesses still receive the same concrete completion condition as a manual fallback.
- The source prompt better matches the project's prompt-engineering boundary rule: name the capability, not the mechanism.

### Negative

- The sync tooling and generated distribution checks must distinguish universal goal-setting guidance from target-specific command examples.
- Documentation that currently teaches `/goal` as the recommended form needs wording updates so Claude-style command examples do not look like the only supported mechanism.
- Verification has to check behavior across harnesses at the capability level, which is less grep-simple than checking for a literal `/goal` token.

## Source

- Session: `manifest-dev:figure-out --with-docs --log`, 2026-06-23.
- Investigation log: `~/.manifest-dev/logs/figure-out-log-20260623-102511.md`.
- Related: `20260605-pi-native-runtime-package-source-surface`
