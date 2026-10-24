<p align="center">
  <img src="assets/logo.png" alt="manifest-dev logo" width="140">
</p>

# manifest-dev

Hand your agent a task. Get back work you can trust.

manifest-dev is a set of free, open-source skills for coding agents. With it, your agent works out what you mean, writes down what done means, and calls nothing finished until every check passes. Use one skill, finish a defined task, or assign a project outcome while keeping the decisions you care about.

**[See it explained →](https://doodledood.github.io/manifest-dev/)** — the available paths, one scene at a time.

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

## Coordinate an outcome or run a queue

`/orchestrate lending` proposes a plan over the lending effort's ready Tickets and waits for approval by default. `--autonomous` runs within the assignment without those plan approvals. A finite queue assignment ends when its work is exhausted; the flag does not turn it into ongoing project operation.

For outcome coordination, give the outcome, relevant evidence, and limits. For example:

```text
/orchestrate help readers get the next available book without volunteer chasing.
Use the lending report and support cases. You may investigate and propose work.
I retain product direction, final acceptance, sending, and spending. Work this round only.
```

The coordinator can commission inquiry or delivery, read results, and continue, wait, ask, or finish. Every independently managed job gets a Ticket before dispatch. Related source messages can form one case; routine reasoning needs no separate Tickets. Completed code is delivery evidence. Whether people use it and achieve the intended result is a separate question.

One status page shows progress, evidence waits, and what needs you. A wait names its recommendation, evidence, risk, and next step. Continuation uses an available host wake or a manual resume; manifest-dev adds no scheduler. Missing evidence or access gets a concrete acquisition step or ask.

## Decide what to delegate

An **assignment** says what to do now: investigate, review, build, or coordinate. **Delegation** says which decisions it may make inside that work. Existing skill defaults remain; you only need to state adjustments. `/setup-project` reads existing instructions and shows the exact shared or personal text before saving new choices. When you accept coordination, it asks which decisions you keep. A run with no person present flags those offers and writes nothing. Shared rules live in the project's context file or a reachable companion; personal rules stay in your private instructions.

You can delegate visual direction and still retain acceptance of the rendered result. Accepting a version does not accept a materially changed version. Technical delegation also preserves a team's required review. A worker keeps the intent, evidence, and current authority through handoffs and stops dependent work at a retained decision.

**Auto** on a Ticket permits full completion under its grant and repository rules. A Ticket without Auto can still be investigated or prepared up to the retained decision: a Question returns an answer, while implementation can return a ready pull request. Feedback resumes the same job. The flag, a tool, a source message, or a new Ticket never supplies wider authority.

Isolated checks can expose instruction defects; reliable sustained project progress, and autonomous business operation in particular, remain to be established through actual use.

## Choose an entry point

Choose what you need; there is no required sequence:

- **Understand a question** — `/figure-out` investigates and recommends. It does not start implementation. Product questions can explore what people are trying to accomplish, what they use today, and what would make them try or keep using a solution.
- **Finish defined work** — `/define` makes a finite Manifest; `/do` executes it. `/auto` combines understanding, definition, and execution when that is the assignment.
- **Prepare a project** — `/setup-project` connects its existing direction, words, decisions, and checks. It resolves coordination settings only when you want them, and starts no work.
- **Track or work one job** — `/ticket-up` writes a Question Ticket for inquiry or a Shaped Ticket ready for delivery; `/next-ticket` selects one; `/run-ticket` works that exact Ticket. An inquiry can go directly from `/figure-out` to `/ticket-up` without a Manifest.
- **Coordinate work** — `/orchestrate` proposes a queue plan or pursues an explicitly assigned outcome. `--autonomous` acts within that assignment and its limits.

Each choice works on its own, including inside a team that does not use manifest-dev. The [plugin README](claude-plugins/manifest-dev/README.md) explains each skill.

## What it costs

More effort up front, less checking after. manifest-dev is free and open source (MIT). It spends more tokens and time before building than prompting an agent directly, and unattended runs spend them on work you may still turn down. It's built for experienced developers who would rather put the effort in before building than review afterwards. If shipping fastest is all that matters, a plain agent fits better.

## What's in it

Two plugins ship from this repository:

| Plugin | What it covers |
|--------|----------------|
| [`manifest-dev`](claude-plugins/manifest-dev) | Standalone inquiry, finite work, optional outcome coordination, project setup, ticket authoring and execution, first-principles design with composable guides and optional measurement tools (`/design`), artifact review, and the review skills the criteria call on |
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
