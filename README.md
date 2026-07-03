<p align="center">
  <picture>
    <img src="assets/logo.png" alt="Manifest Dev Logo" width="120" style="background: transparent;">
  </picture>
</p>

# manifest-dev

#### Loop engineering, with a stop condition you can trust.

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-15803D" alt="MIT license">
  <img src="https://img.shields.io/badge/loop-verification--first-15803D" alt="Verification-first">
  <img src="https://img.shields.io/badge/runs_in-Claude_Code_·_OpenCode_·_Codex_·_Pi-475569" alt="Runs in four CLIs">
</p>

I built this because I didn't trust a fully autonomous loop to actually finish the job — not once I'd stepped away mid-run, after I'd already done the work of understanding the problem. Everyone's writing loops now: the shift from prompting your agent by hand to designing the system that prompts it. But the loop was never the hard part. A loop that can't prove it finished is just a faster way to burn tokens: it runs, it declares victory on a confident summary, and you find out in review.

The leverage isn't the `while`. It's defining what "done" means and verifying it independently, so the loop can't mark its own homework.

That's what manifest-dev is. You say what you'd accept. The agent builds toward that bar and checks its own work against every line of it (an independent verifier per criterion) before you ever open the diff. The understanding comes first, with a thinking partner that pushes back instead of nodding along. Then you write down what you'd accept. Then it builds and verifies itself.

It's not a loop runtime. It doesn't schedule jobs or manage worktrees, and it doesn't need to. It rides on top of whatever runs your loop, including your host's own `/loop` and `/goal`. It supplies the part those primitives leave to you: what to verify, and how to know you're actually done.

## Loops fail in three ways. There's a skill for each.

A loop is only as good as the thing that tells it to stop, and the popular patterns skip the three parts that make stopping real.

<table>
  <tr>
    <th align="left">How the loop fails</th>
    <th align="left">The skill that answers it</th>
  </tr>
  <tr>
    <td><strong>It skips understanding.</strong> The loop becomes a way to avoid thinking about the problem, not a way to move faster on one you already grasp.</td>
    <td><strong><code>/figure-out</code></strong> is an adversarial thinking partner. It investigates the code instead of asking you, presses the load-bearing question, and refuses to leap to the edit.</td>
  </tr>
  <tr>
    <td><strong>It has no real stop condition.</strong> "Run until done" is worthless when "done" was never written down.</td>
    <td><strong><code>/define</code></strong> encodes what you'd accept: the acceptance criteria you'd reject in review but wouldn't think to specify up front.</td>
  </tr>
  <tr>
    <td><strong>It fakes "done."</strong> An agent reports success on broken code with total confidence.</td>
    <td><strong><code>/do</code></strong> makes it prove otherwise: one independent verifier per criterion, and it can't reach <code>/done</code> on a self-report.</td>
  </tr>
</table>

Most spec-driven tools take your description and generate a spec, then code — a transcript of what you already said, thin if your understanding was thin. This flips the order: understanding comes first and is adversarial, before `/define` ever writes anything down.

## Who This Is For

You've burned out on the weekly "game-changing AI coding tool" cycle and want something grounded that works. You're an experienced developer who cares more about output quality than raw speed, and you've learned the hard way that AI code needs guardrails more than cheerleading. If you count every cent per token, or want the fastest possible output regardless of what it costs you in review, this isn't your thing.

## Quick Start

```bash
# Claude Code (primary)
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev-marketplace
```

For OpenCode, Codex CLI, and Pi, see [Multi-CLI Support](#multi-cli-support) below.

Then work through the three beats:

```bash
/figure-out <topic or problem>     # 1. Figure it out — understand before acting
/define <what you want to build>   # 2. Encode what you'd accept into a manifest
/do <manifest-path>                # 3. Execute and verify every criterion inline

/auto <what you want to build>     # Or run all three, chained, no approval gates
```

`/figure-out` is the heart of it: a peer that investigates before it claims and holds its position under pushback. `/define` takes the understanding you reached and *encodes* it into a manifest, auto-invoking `/figure-out` first if you skipped ahead. `/do` implements toward the manifest. `/auto` chains all three with no waiting.

For unattended runs of `/do` or `/auto` (the recommended way to run both), set your host's goal-setting or continuation capability to the completion contract those skills print — see the [manifest-dev plugin README](claude-plugins/manifest-dev/README.md#quick-start) for the full contract text and why it's shaped that way.

Babysit an existing PR through review without any manifest-dev setup: `/babysit-pr [pr-url]`. Details in the [manifest-dev-tools README](claude-plugins/manifest-dev-tools).

Pass `--canvas` to `/define` (desktop only) for a **Shared Understanding Canvas**: a live, browser-rendered side-channel where intent, flow, and scope render as you go, alongside the chat.

## How It Works

```mermaid
flowchart TD
    A["/figure-out 'problem'"] --> B["Shared understanding"]
    B --> C["/define"]
    C --> D["Manifest = what you'd accept"]
    D --> E["/do manifest.md"]
    E --> F{"For each Deliverable"}
    F --> G["Implement toward ACs"]
    G --> H["Spawn subagent per AC + Global Invariant"]
    H -->|FAIL| I["Fix that criterion"]
    I --> H
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

Your first pass lands closer to done, and the fix loop cleans up what's left on its own. Writing acceptance criteria also keeps you engaged with your own code — that matters more the more you lean on the agent, right when the codebase starts to feel like someone else wrote it.

> [!TIP]
> Resist the urge to jump in mid-`/do`. It won't nail everything first try; that's expected. You invested in understanding the problem, so let the loop run.

## Multi-CLI Support

The Claude Code plugins are the source of truth. The same components run in OpenCode, Codex CLI, and Pi through native per-CLI distributions under `dist/`, all verifying the same way — a general-purpose subagent or verifier execution per gate.

| CLI | Install | Details |
|-----|---------|---------|
| Claude Code | `/plugin install manifest-dev@manifest-dev-marketplace` | Primary target |
| OpenCode | clone + one config line | [README](dist/opencode/README.md) |
| Codex CLI | `codex plugin marketplace add doodledood/manifest-dev` | [README](dist/codex/README.md) |
| Pi | `pi install git:github.com/doodledood/manifest-dev@main` | [README](dist/pi/README.md) |

Each linked README covers that CLI's install, upgrade, and uninstall path. Architecture decisions behind the multi-CLI design are indexed in [`docs/adr/`](docs/adr/README.md).

## Available Plugins

| Plugin | Description |
|--------|--------------|
| [`manifest-dev`](claude-plugins/manifest-dev) | The core workflow — `/figure-out`, `/define`, `/do`, `/done`, `/escalate`, `/auto`, `/figure-out-team` — and the verification skills, including `review-code`'s per-dimension quality gates. |
| [`manifest-dev-tools`](claude-plugins/manifest-dev-tools) | Tools alongside the workflow: `/review-pr`, `/babysit-pr`, `/walk-pr` for PR collaboration, plus `/prompt-engineering`, `/handoff`, and `/teach-me`. |

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
