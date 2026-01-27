# manifest-dev

Front-load the thinking so AI agents get it right the first time.

## Who This Is For

Experienced developers frustrated by hype-driven AI coding tools. If you're tired of chasing the latest "game-changing" prompt that produces code you spend hours debugging, this plugin offers a grounded alternative.

**Our approach:**
- Workflows designed around how LLMs actually work, not how we wish they worked
- Quality over speed -- invest upfront, ship with confidence
- Simple to use, sophisticated under the hood

## Installation

Add the marketplace:

```bash
/plugin marketplace add https://github.com/doodledood/manifest-dev
```

Browse and install:

```bash
/plugin list
/plugin install manifest-dev@manifest-dev-marketplace
```

## What It Does

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants). Every criterion has explicit verification; execution can't stop without verification passing or escalation.

### Core Skills

| Skill | Description |
|-------|-------------|
| `/define` | Verification-first requirements builder with proactive interview. YOU generate candidates, user validates. |
| `/do` | Autonomous execution with enforced verification gates. Iterates deliverables, satisfies ACs, calls /verify. |

### Internal Skills

| Skill | Purpose |
|-------|---------|
| `/verify` | Runs all verifications, reports by type and deliverable |
| `/done` | Outputs hierarchical completion summary |
| `/escalate` | Structured escalation with type-aware context |

### Hooks

Hooks enforce workflow integrity automatically:
- **Stop hook** -- Prevents premature stopping. Can't stop without verification passing or proper escalation.
- **Escalate gate** -- Requires /verify before /escalate. No lazy escalation without attempting verification.

### Workflow

```
/define "task" --> Interview --> Manifest file
                                     |
/do manifest.md --> Execute deliverables --> /verify
                                               |
                         All pass --> /done     |
                         Stuck --> /escalate    |
                         Failures --> Fix --> /verify again
```

## Repository Structure

```
manifest-dev/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/
│   ├── manifest-dev/          # The manifest-dev plugin
│   │   ├── agents/            # Specialized agents (verifier, reviewers)
│   │   ├── skills/            # /define, /do, /verify, /done, /escalate
│   │   └── hooks/             # Stop enforcement, escalation gating
│   └── PLUGIN_TEMPLATE/       # Template for new plugins
├── docs/                      # Research & guidelines
│   ├── CUSTOMER.md            # Who we build for
│   ├── LLM_CODING_CAPABILITIES.md  # LLM strengths/limitations
│   ├── LLM_TRAINING.md        # How LLMs are trained
│   └── PROMPTING.md           # First-principles prompting
├── tests/                     # Hook test suite
└── README.md
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for plugin development guidelines.

## License

MIT
