# Claude Code plugins

Two plugins ship from this repository. Install the first if you want the workflow; add the second if you also work on pull requests and prompts.

## Install

```bash
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev
/plugin install manifest-dev-tools@manifest-dev
```

## The plugins

Each one installs on its own:

| Plugin | What it covers |
|--------|----------------|
| [`manifest-dev`](./manifest-dev) | Understanding a problem, writing down what you'd accept, executing against it and verifying the result — with lean `just-*` variants of each beat (`/just-figure-out`, `/just-define`, `/just-do`, `/just-auto`). Also project setup, ticket authoring and execution, design build-and-review (`/design`, `/review-design`), and the review skills the criteria call on. |
| [`manifest-dev-tools`](./manifest-dev-tools) | Pull-request collaboration, prompt authoring and review, teaching, plain-language explainers, handoff between sessions. |

For an unattended run, point your host's goal-setting or continuation capability at the completion contract `/do` prints.

Each plugin's README lists everything it ships. The repository [README](../README.md) covers what the workflow is for and how the pieces fit together.

## Add a plugin

[`PLUGIN_TEMPLATE/`](./PLUGIN_TEMPLATE) is the starting point. [`CLAUDE.md`](../CLAUDE.md) carries the conventions.
