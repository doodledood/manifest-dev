<p align="center">
  <img src="assets/logo.png" alt="manifest-dev logo" width="140">
</p>

# manifest-dev

Hand your agent a task. Get back work you can trust.

manifest-dev is a set of free, open-source skills for coding agents. With it, your agent works out what you mean, writes down what done means, and calls nothing finished until every check passes. Use one skill, or climb five levels to a queue of work that runs on its own while you make the calls only you can make.

**[See it explained →](https://doodledood.github.io/manifest-dev/)** — the five levels, one scene at a time.

## Install

Claude Code is the primary target. Inside a Claude Code session, run:

```text
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev
```

Codex, Pi, OpenCode, and Cursor (and with it Grok Bot) install it too ([other CLIs](#other-clis)). Every skill also works on its own: `npx skills add doodledood/manifest-dev --skill figure-out` installs just one.

## Start with one real question

In the repository you want to work on:

```text
/figure-out why do half my background jobs silently stall?
```

Ask about the bug you keep putting off. When a term or a step is unclear, ask `/manifest-dev-help`: it answers any question about manifest-dev in plain, simple English, with the reason behind each part.

## One piece of work

**First, it works out what you mean.** `/figure-out` reads your code, finds the question that decides the work, and asks you only what the code can't answer, with its recommended answer first.

**Then you agree what done means.** `/define` writes a Manifest: the pieces of work (Deliverables), a check each one must pass (Acceptance Criteria), and rules that hold across all of them (Global Invariants).

**It builds until every check passes.** `/do` builds against the Manifest. A failed check sends that piece back to be fixed, and done means every check passed on fresh evidence. `/do` assumes you are away: it decides without asking, reports the decisions it made for you, and raises a blocker as soon as it finds one.

`/auto` runs all three steps in one go.

**What you review: a pull request that shows the change working.** When the work ships as a pull request, its top reads in about a minute. It says what changed and why, shows the change working with screenshots or command output, and lists the decisions it made for you and the debt it left — what it found and didn't fix.

## A project that remembers

`/setup-project`, run once, gives your project a **North Star**: one file that says what the project is for and for whom, how it measures progress, and what it never does. The choices made along the way go in decision records. Every session reads it before it decides what's worth doing.

It also keeps the project's words, decisions, and checks: a glossary of its terms, a record of each decision and why it was made, and one command that checks the project still works. That command is recommended, not required: a project that already verifies its own way keeps doing so. Every run keeps these current where its work touches them. It also turns a mistake someone caught into a check that catches it next time, and offers the debt it left to the next change through that code.

## A shared queue

**Work waits as Tickets anyone can pick up.** A Ticket carries all a person or an agent needs to do one piece of work and know it's done. `/ticket-up` writes them, into GitHub Issues, files in the repository, or a tracker you describe; `/next-ticket` picks the one whose wait costs most.

**Auto** is the mark that says a Ticket needs no one's judgment to finish and land.

**New work is planned with you.** An effort is one goal and its own Tickets. You think it through together with `/figure-out`, and `/ticket-up` turns what you settled into the effort's Tickets.

## The queue runs

**Many Tickets at once, each after the work it depends on.** `/orchestrate` proposes a plan and runs it after you approve: each Ticket in its own session, landed one at a time. Auto Tickets land on their own; the rest stop at a ready pull request for you to land. The debt they leave becomes new Tickets. One status page shows what is running and what waits on you, and says in plain words what each Ticket is for.

**With `--autonomous`, it keeps going on its own.** A scheduler you already run starts `/orchestrate --autonomous`. It starts a new run whenever one finishes, up to the number it may run at once, until no ready work remains. It gives Auto to Tickets that agents wrote, wherever no one's judgment is needed.

The loop keeps turning, and you step in where it needs you — for judgment, taste, or authority:

| Runs without you | Waits for you |
|---|---|
| Auto Tickets, end to end, including the ones `--autonomous` grants | Landing a Ticket without Auto |
| Tickets without Auto, up to a ready pull request | Escalations: a question only you can answer |
| | Tickets from people without write access |
| | A review the repository requires from a person |
| | A cause that paused an effort, such as a check failing on the base branch |
| | Planning a new effort, and each plan in the default mode |

Each item that waits for you comes with the answer it recommends, the risk of taking it, and the evidence behind it, so you can decide without opening the pull request.

## What to run at each level

Each level works without the ones above it, and without anyone else on your team using manifest-dev. What it adds to a shared repository is plain files and plain instructions. Run these to reach each level:

1. **One skill** — install the plugin, then `/figure-out` with a question.
2. **One piece of work** — `/auto` with a task (or `/figure-out`, `/define`, `/do` one step at a time).
3. **A project that remembers** — `/setup-project`, once.
4. **A shared queue** — `/ticket-up` writes work as Tickets; `/next-ticket` picks the next one.
5. **The queue runs** — `/orchestrate`, then approve its plan; or `/orchestrate --autonomous` from a scheduler you already run. Mark a Ticket Auto when it needs no one's judgment.

That is everything to remember. The skills handle the rest themselves, and the [plugin README](claude-plugins/manifest-dev/README.md) explains each one.

## What it costs

More effort up front, less checking after. manifest-dev is free and open source (MIT). It spends more tokens and time before building than prompting an agent directly, and unattended runs spend them on work you may still turn down. It's built for experienced developers who would rather put the effort in before building than review afterwards. If shipping fastest is all that matters, a plain agent fits better.

## What's in it

Two plugins ship from this repository:

| Plugin | What it covers |
|--------|----------------|
| [`manifest-dev`](claude-plugins/manifest-dev) | The workflow itself, project setup, ticket authoring and execution, first-principles design with composable guides and optional measurement tools (`/design`), artifact review, and the review skills the criteria call on |
| [`manifest-dev-tools`](claude-plugins/manifest-dev-tools) | Pull-request collaboration, prompt work, standalone goals from Manifests (`/manifest-to-goal`), teaching, explaining, and handoff between sessions |

Each plugin's README lists what it ships.

## Other CLIs

The Claude Code plugins are the source, and the same skill text serves every host: OpenCode, Pi and Cursor read it from the source tree, and Codex installs a generated copy under `dist/`.

| CLI | Install |
|-----|---------|
| Claude Code | `/plugin marketplace add doodledood/manifest-dev`, then `/plugin install manifest-dev@manifest-dev` — [above](#install) |
| Codex CLI | `codex plugin marketplace add doodledood/manifest-dev` — [details](dist/codex/README.md) |
| Pi | `pi install git:github.com/doodledood/manifest-dev@main` — [details](dist/pi/README.md) |
| OpenCode | clone, then add one path to your config — [details](dist/opencode/README.md) |
| Cursor, Grok Bot | copy the two plugin folders into `~/.cursor/plugins/local`; from the Cursor Marketplace, and so in Grok Bot, once it is listed — [details](dist/cursor/README.md) |

Individual skills install into many other agents through `npx skills add doodledood/manifest-dev --skill <name>`.

Decisions behind the multi-CLI design are indexed in [`docs/adr/`](docs/adr/README.md).

## Development

Setup needs Python 3.10+ and Node 22.18+, and Java 11+ only for the ticket protocol model
(`scripts/verify drive ticket-protocol-model`).

```bash
./scripts/setup.sh
source .venv/bin/activate

scripts/check.sh --fix                # lint and format, typecheck, test while iterating
scripts/verify drive property-suite   # the same checks through the harness, before a pull request
```

Run `python3 scripts/sync_dist.py` after changing plugin components; the test suite fails when a generated copy drifts.

## Contributing

This is built for its author's own projects and shared as it's used. See [CONTRIBUTING.md](./CONTRIBUTING.md) for how the plugins are put together.

## License

MIT
