# Reader tasks

Each entry is one task a reader comes to a document to do. Statuses and how to walk an entry are
in `README.md` beside this file.

## Decide whether manifest-dev is worth trying

- **Where:** `README.md` → *The three things, and where they live* and *What it costs*; `site/index.html` → *Intro*
- **Ends able to:** say what problem it solves and what it costs them to adopt.
- **Status:** unverified

## Install it in Claude Code

- **Where:** `README.md` → *Install*
- **Ends able to:** install the marketplace and the plugin, and start a first `/figure-out`.
- **Status:** unverified

## Install it in another CLI

- **Where:** `README.md` → *Other CLIs*; `dist/codex/README.md` → *Install* and *Parity with Claude Code*; `dist/opencode/README.md` → *Install* and *Parity with Claude Code*; `dist/pi/README.md` → *Install* and *Parity with Claude Code*
- **Ends able to:** install it in Codex, OpenCode, or Pi, and name what differs from Claude Code.
- **Status:** unverified

## Pick the entry point for a piece of work

- **Where:** `README.md` → *The workflow*; `claude-plugins/manifest-dev/README.md` → *The three beats*
- **Ends able to:** choose between `/figure-out`, `/define`, `/do`, and `/auto` for a given task.
- **Status:** unverified

## Know what persists between runs

- **Where:** `README.md` → *The codebase gets easier to change, run by run*; `claude-plugins/manifest-dev/README.md` → *What the workflow maintains*; `site/index.html` → *Weeks later*
- **Ends able to:** name what a later run inherits from an earlier one, and where each piece lives.
- **Status:** unverified

## Estimate what it costs

- **Where:** `README.md` → *What it costs*
- **Ends able to:** judge whether a task is worth the workflow's extra time and tokens.
- **Status:** unverified

## Set a project up

- **Where:** `claude-plugins/manifest-dev/README.md` → *Project surfaces*
- **Ends able to:** say what setting a project up installs, and how an older setup gets updates.
- **Status:** unverified

## Run it unattended

- **Where:** `claude-plugins/manifest-dev/README.md` → *Run it unattended*
- **Ends able to:** start an unattended run and say where it stops for a person.
- **Status:** unverified

## Read a Manifest

- **Where:** `claude-plugins/manifest-dev/README.md` → *Manifest sections*
- **Ends able to:** read a Manifest and say what each section binds.
- **Status:** unverified

## Find which plugin ships a skill

- **Where:** `claude-plugins/README.md` → *The plugins*
- **Ends able to:** name the plugin that ships a given skill and install only that one.
- **Status:** unverified

## Add a plugin

- **Where:** `CONTRIBUTING.md` → *Plugin Development Process*; `claude-plugins/README.md` → *Add a plugin*
- **Ends able to:** create a plugin from the template, register it in the marketplace, and test it locally.
- **Status:** unverified

## Contribute a change

- **Where:** `CONTRIBUTING.md` → *Pull Request Process*; `README.md` → *Development*
- **Ends able to:** run the checks a pull request needs and open one.
- **Status:** unverified

## Try the workflow from the site

- **Where:** `site/index.html` → *Try it*
- **Ends able to:** install it and run a first session from the site alone.
- **Status:** unverified

## Pick the tools skill for a job

- **Where:** `claude-plugins/manifest-dev-tools/README.md` → *Pull requests* and *Prompts* and *People and sessions*
- **Ends able to:** name the tools skill that reviews another author's pull request, tends the reader's own, reviews a prompt, or hands a session to a fresh agent.
- **Status:** unverified

## Review a change outside a run

- **Where:** `claude-plugins/manifest-dev/README.md` → *Review and verification*
- **Ends able to:** pick the review skill for code, prose, or a design, or check a pull request's readiness, and invoke it directly.
- **Status:** unverified

## Get design direction for an artifact

- **Where:** `claude-plugins/manifest-dev/README.md` → *First-principles design*
- **Ends able to:** ask `/design` for direction on an artifact and know which skill evaluates the result.
- **Status:** unverified

## Deliberate with people who cannot share a session

- **Where:** `claude-plugins/manifest-dev/README.md` → *Conversation*
- **Ends able to:** run a figure-out deliberation in a Slack channel or thread with `/figure-out-team`.
- **Status:** unverified
