<p align="center">
  <picture>
    <img src="assets/logo.png" alt="Manifest Dev Logo" width="120" style="background: transparent;">
  </picture>
</p>

# manifest-dev

#### Your agent builds the wrong thing, confidently.

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-15803D" alt="MIT license">
  <img src="https://img.shields.io/badge/loop-verification--first-15803D" alt="Verification-first">
  <img src="https://img.shields.io/badge/runs_in-Claude_Code_·_OpenCode_·_Codex_·_Pi-475569" alt="Runs in four CLIs">
</p>

Not broken code — wrong code. It compiles. The tests pass. And it solves a problem you don't have, because the agent started typing before it understood what you meant.

**`/figure-out` is the pushback.** An adversarial thinking partner. It digs through your codebase on its own and presses on the question that decides the work. It refuses to touch code until you both know what "right" is, holds its position under pushback, and changes its mind when the evidence changes.

```bash
npx skills add doodledood/manifest-dev --skill figure-out
```

```
/figure-out why do half my background jobs silently stall?
```

A minute in, it has read your code and come back with the question you hadn't thought to ask. That first question is the fastest way to find out whether this tool is for you.

**Every skill here works standalone. Take what you want.** No framework to adopt, nothing else to install. If you never run another command from this repo, `/figure-out` still earns its keep.

## The loop was never the hard part

Everyone's writing loops now: the shift from prompting an agent by hand to designing the system that prompts it. But a loop pointed at a shallow understanding just ships the wrong thing faster. And the loop vouches for itself. It runs, declares victory on a confident summary. You find out in review.

The leverage lives upstream of the `while`: understand the problem before anything is built, define what "done" means, then verify it independently. That's the rest of manifest-dev: loop engineering, with a stop condition you can trust.

<table>
  <tr>
    <th align="left">How the loop fails</th>
    <th align="left">The skill that answers it</th>
  </tr>
  <tr>
    <td><strong>It skips understanding.</strong> A loop should be a faster path through a problem you already grasp; skipping that step turns it into a substitute for thinking.</td>
    <td><strong><code>/figure-out</code></strong> is the door you just walked through: adversarial understanding, before anything gets built.</td>
  </tr>
  <tr>
    <td><strong>It has no real stop condition.</strong> "Run until done" is worthless when "done" was never written down.</td>
    <td><strong><code>/define</code></strong> encodes what you'd accept: the acceptance criteria you'd reject in review but wouldn't think to specify up front.</td>
  </tr>
  <tr>
    <td><strong>It fakes "done."</strong> An agent reports success on broken code with total confidence.</td>
    <td><strong><code>/do</code></strong> makes it prove otherwise: every criterion needs evidence under an explicit verification mode, and the default has an independent verifier evaluate every gate.</td>
  </tr>
</table>

manifest-dev puts understanding first, adversarially, before `/define` writes anything down. Most spec-driven tools generate the spec straight from your description, so the spec runs only as deep as what you already said.

manifest-dev rides on top of whatever runs your loop, including your host's own `/loop` and `/goal`, and leaves scheduling jobs and managing worktrees to that runtime. It supplies the part those primitives leave to you: what to verify, and how to know you're actually done.

## Quick Start

The one-skill door is above. The full system installs as a plugin:

```bash
# Claude Code (primary)
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev
```

For OpenCode, Codex CLI, and Pi, see [Multi-CLI Support](#multi-cli-support) below.

Then work through the three beats:

```bash
/figure-out <topic or problem>     # 1. Figure it out — understand before acting
/define <what you want to build>   # 2. Encode what you'd accept into a manifest
/do <manifest-path>                # 3. Execute and verify every criterion inline
/do <manifest-path> --verification per-gate      # opt in to one verifier per gate
/do <manifest-path> --verification self          # opt in to executor verification
/do <manifest-path> --exhaustive-verification    # opt in to re-sampling every judgment gate each round

/auto <what you want to build>     # Or run all three, chained, no approval gates
```

`/define` takes the understanding you reached and *encodes* it into a manifest, auto-invoking `/figure-out` first if you skipped ahead. `/do` implements toward the manifest and can't call it done until every criterion has fresh evidence under the selected mode, keeping a default-on execution log of deviations and dead ends as it goes (`--no-log` skips it). The default `consolidated` mode has one independent verifier evaluate the outstanding gate set each round — one coherent view, one artifact read; opt-in `per-gate` runs one fresh independent verifier per gate for maximum rigor, and opt-in `self` trades independence for the lowest execution cost. `--verifier-model <model>` optionally selects the independent verifier model and is invalid with `self`. Re-verification follows each gate's declared kind: a gate whose verdict comes from a command re-runs in full, while a gate whose verdict is a model's judgment takes one full look and afterwards judges only its prior findings' repairs and what changed since — so runs converge on repaired findings instead of on a review round that happens to come up empty (`--exhaustive-verification` restores full re-sampling). `/auto` chains all three with no waiting and forwards the same execution flags without putting them in the manifest.

For unattended runs of `/do` or `/auto` (the recommended way to run both), set your host's goal-setting or continuation capability to the completion contract those skills print; see the [manifest-dev plugin README](claude-plugins/manifest-dev/README.md#quick-start) for the full contract text and why it's shaped that way.

Babysit an existing PR through review without any manifest-dev setup: `/babysit-pr [pr-url]`. Details in the [manifest-dev-tools README](claude-plugins/manifest-dev-tools).

Pass `--canvas` to `/figure-out` for a refreshable, browser-rendered map of the session alongside the chat, readable on any screen: the crux tree with the question you're standing on marked on it, what's still open around it, and how much ground is still unsurveyed. Annotate it in place and hand your notes back in one paste.

## How It Works

```mermaid
flowchart TD
    A["/figure-out 'problem'"] --> B["Shared understanding"]
    B --> C["/define"]
    C --> D["Manifest = what you'd accept"]
    D --> E["/do manifest.md"]
    E --> F{"For each Deliverable"}
    F --> G["Implement toward ACs"]
    G --> H["Evaluate gates under selected mode"]
    H -->|any FAIL| I["Fix everything the round found"]
    I -->|re-verify per head| H
    H -->|all PASS| J["/done"]
    F -->|risk surfaces| K["Consult trade-offs, adjust approach"]
    K -->|reachable| F
    K -->|stuck| L["/escalate"]
    classDef gate fill:#15803D,stroke:#0F172A,color:#FFFFFF;
    classDef done fill:#0F172A,stroke:#15803D,color:#FFFFFF;
    classDef stop fill:#B45309,stroke:#0F172A,color:#FFFFFF;
    class H gate;
    class J done;
    class L stop;
```

FAIL routes back to a fix; a real blocker (amber) routes to `/escalate`.

## What Changes

Your first pass lands closer to done, and the fix loop cleans up what's left on its own. Writing acceptance criteria also keeps you engaged with your own code. That matters more the more you lean on the agent, right when the codebase starts to feel like someone else wrote it.

> [!TIP]
> Resist the urge to jump in mid-`/do`. It won't nail everything first try; that's expected. You invested in understanding the problem, so let the loop run.

## Who This Is For

You've burned out on the weekly "game-changing AI coding tool" cycle and want something grounded that works. You're an experienced developer who cares more about output quality than raw speed, and you've learned the hard way that AI code needs guardrails more than cheerleading. If you count every cent per token, or want the fastest possible output regardless of what it costs you in review, this isn't your thing.

## Multi-CLI Support

The Claude Code plugins are the source of truth. The same components run in OpenCode, Codex CLI, and Pi through native per-CLI distributions under `dist/`, all carrying the same topology-neutral gate schema and run-level verification modes.

| CLI | Install | Details |
|-----|---------|---------|
| Claude Code | `/plugin install manifest-dev@manifest-dev` | Primary target |
| OpenCode | clone + one config line | [README](dist/opencode/README.md) |
| Codex CLI | `codex plugin marketplace add doodledood/manifest-dev` | [README](dist/codex/README.md) |
| Pi | `pi install git:github.com/doodledood/manifest-dev@main` | [README](dist/pi/README.md) |

Individual skills also install into 18+ agents (Cursor, Copilot, Cline, and more) via `npx skills add doodledood/manifest-dev --skill <name>`.

Each linked README covers that CLI's install, upgrade, and uninstall path. Architecture decisions behind the multi-CLI design are indexed in [`docs/adr/`](docs/adr/README.md).

## Available Plugins

| Plugin | Description |
|--------|--------------|
| [`manifest-dev`](claude-plugins/manifest-dev) | The core workflow (`/figure-out`, `/define`, `/do`, `/done`, `/escalate`, `/auto`, `/figure-out-team`), ticket decomposition (`/ticket-up`, `/next-ticket`), and the verification skills, including `review-code`'s per-dimension quality gates. |
| [`manifest-dev-tools`](claude-plugins/manifest-dev-tools) | Tools alongside the workflow: `/review-pr`, `/babysit-pr`, `/walk-pr` for PR collaboration, plus `/prompt-engineering`, `/handoff`, `/teach-me`, and `/wait-what`. |

Full plugin and skill catalogs live in [`claude-plugins/README.md`](claude-plugins/README.md) and each plugin's own README.

## Development

```bash
# Setup (first time)
./scripts/setup.sh
source .venv/bin/activate

# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

After changing plugin components, run `/sync-tools` to regenerate the `dist/` distributions.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for plugin development guidelines.

## License

MIT

---

*Built by developers who understand LLM limitations, and design around them.*

Follow along: [@aviramkofman](https://x.com/aviramkofman)
