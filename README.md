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

Install the plugin:

```bash
/plugin list
/plugin install manifest-dev@manifest-dev-marketplace
```

## The manifest-dev Plugin

Manifest-driven development workflows with verification gates. Separate **what to build** (Deliverables) from **rules to follow** (Global Invariants), then execute autonomously with enforced verification.

### Core Workflow

- `/define` - Manifest builder with proactive interview. YOU generate candidates, user validates (no open-ended questions)
- `/do` - Manifest executor. Iterates deliverables, satisfies ACs, then verifies all criteria pass

### How It Works

```
/define "task" --> Interview --> Manifest file
                      |
                      |-- Intent & Context
                      |-- Deliverables (with ACs)
                      |-- Approach (architecture, order, risks, trade-offs)
                      +-- Global Invariants & Process Guidance
                                     |
                                     v
/do manifest.md --> Execute --> /verify --> /done
```

### Task-Specific Guidance

`/define` is domain-agnostic. Task-specific guidance loads conditionally:

| Task Type | When Loaded |
|-----------|-------------|
| Code | APIs, features, fixes, refactors, tests |
| Document | Specs, proposals, reports, articles, docs |
| Research | Research, investigation, analysis |
| Blog | Blog posts, content writing |

### Review Agents

Parallel review agents for code quality:

- Bug detection, type safety, maintainability
- Simplicity, testability, coverage, docs
- CLAUDE.md adherence checking

### Hooks

Enforced verification gates:
- Can't stop without verification passing or proper escalation
- Can't escalate without attempting verification first

## Repository Structure

```
manifest-dev/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/
│   └── manifest-dev/          # The plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/            # Review and verification agents
│       ├── hooks/             # Verification enforcement hooks
│       └── skills/            # /define, /do, /verify, /done, /escalate
├── docs/                      # Foundational documents
│   ├── CUSTOMER.md
│   ├── LLM_CODING_CAPABILITIES.md
│   ├── LLM_TRAINING.md
│   └── PROMPTING.md
├── tests/
│   └── hooks/                 # Hook test suite
├── CLAUDE.md
└── README.md
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guide and [CLAUDE.md](./CLAUDE.md) for development commands.

## License

MIT
