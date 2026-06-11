# ADR: OpenCode slash commands use plugin wrappers

## Status
Accepted

## Context

The OpenCode plugin-native distribution ADR retired the old OpenCode installer and its copied command files. That direction still holds: package-local skills registered through the plugin avoid shared Agent Skills directory bleed, and uninstall remains one config-line removal plus deleting the clone.

However, live use against OpenCode v1.17.x and current upstream docs showed that the slash-command premise in the earlier ADR was too broad. OpenCode discovers Agent Skills and exposes them to the model through the native `skill` tool. The TUI `/` autocomplete is command-backed; discovered skills do not necessarily appear there as invocable slash entries.

manifest-dev still needs `/figure-out`, `/define`, `/do`, `/auto`, `/babysit-pr`, `/review-pr`, `/prompt-engineering`, and the other user-facing workflows to be discoverable through OpenCode's `/` autocomplete. Reintroducing generated command files under `dist/opencode/commands/` or copied files under `~/.config/opencode/commands/` would revive the installer-era cleanup, duplication, and stale-file problems the plugin-native architecture was meant to remove.

## Decision

Keep the OpenCode distribution plugin-native, but make slash UX explicit: the OpenCode plugin's `config` hook registers command wrappers in `cfg.command` for bundled skills whose source `user-invocable` frontmatter is missing or `true`.

Each wrapper uses the skill's description and a command template of:

```text
Use the <skill-name> skill with: $ARGUMENTS
```

The plugin scans package-local `skills/*/SKILL.md` at startup, so adding, removing, or changing skill frontmatter through sync-tools changes the wrapper set without a hardcoded command list. It does not register wrappers for `user-invocable: false` helpers such as `done` and `escalate`, and it does not overwrite an existing user or project command with the same name.

No command files are generated or copied. The command layer is runtime config mutation owned by the same plugin that registers `skills.paths` and `instructions`.

## Alternatives Considered

- **Rely on native skill discovery only**: keeps the plugin simpler, but `/` autocomplete does not show the workflows users expect; users must write prompts like "use the figure-out skill" instead of invoking `/figure-out`.
- **Reintroduce generated command files in `dist/opencode/commands/`**: would make commands explicit as files, but the plugin path does not load package-local command files the way it can register package-local skills. Installing those files would require copying into user config or project config, recreating installer-era stale artifacts.
- **Copy command files into `~/.config/opencode/commands/`**: restores autocomplete, but violates the plugin-native no-footprint decision, complicates uninstall/update, and can collide with user-owned commands.
- **Hardcode wrappers in the plugin**: simple initially, but every skill add/remove/rename would require plugin code edits. Scanning frontmatter keeps sync-tools as the source of truth.

## Consequences

### Positive

- Users get `/figure-out`, `/define`, `/do`, `/auto`, `/babysit-pr`, `/review-pr`, `/prompt-engineering`, and other user-invocable workflows in OpenCode slash autocomplete.
- Internal helpers remain model-loadable skills but stay out of the slash menu.
- Existing user/project commands are respected; local command customization can intentionally shadow manifest-dev wrappers.
- The plugin-native install/uninstall story remains clean: one repo clone, one `plugin` config entry, no copied command files.
- The wrapper set follows source skill frontmatter through sync-tools instead of a separate hardcoded list.

### Negative

- Slash invocation is a prompt wrapper, not a first-class skill invocation primitive. The model still has to respond by loading the named skill.
- OpenCode's command namespace is bare and shared; a user/project `/do` command can shadow manifest-dev's wrapper.
- The plugin now parses enough YAML frontmatter to read flat `name`, `description`, and `user-invocable` values; if skill frontmatter becomes more complex, the parser may need to be replaced with a real YAML parser or kept within the supported flat subset.

## Source

- Session: Pi/OpenCode install debugging, 2026-06-11
- Evidence: local `opencode debug skill` discovered all 18 bundled skills; asking the model to use `figure-out` worked; `/` autocomplete did not show the skills until command wrappers were added.
- Upstream docs: `https://opencode.ai/docs/skills`, `https://opencode.ai/docs/commands`, `https://opencode.ai/docs/config` — skills are exposed through the `skill` tool; slash commands are command-backed.
- Related: Supersedes the slash-UX mechanism assumed in `20260611-opencode-plugin-native-distribution`; keeps its plugin-native install decision.
