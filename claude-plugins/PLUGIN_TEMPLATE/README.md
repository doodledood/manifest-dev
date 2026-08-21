# Plugin template

Copy this directory to start a new plugin in this repository.

## Layout

```
your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # required: name, description, version
├── skills/                   # one directory per skill, each with SKILL.md
│   └── example/
│       └── SKILL.md
└── README.md
```

Agents and hooks are also supported; this repository ships skills only.

## Steps

1. Copy the template:

   ```bash
   cp -r claude-plugins/PLUGIN_TEMPLATE claude-plugins/your-plugin-name
   ```

2. Fill in `.claude-plugin/plugin.json`:

   ```json
   {
     "name": "your-plugin-name",
     "description": "What it does",
     "version": "1.0.0"
   }
   ```

3. Write the skills.

4. Register the plugin in the repository's `.claude-plugin/marketplace.json`.

5. Install from your checkout and try it:

   ```bash
   /plugin marketplace add /path/to/manifest-dev
   /plugin install your-plugin-name@manifest-dev
   ```

## Skills

Each skill is a `SKILL.md` under `skills/<name>/`. Its frontmatter `description` is what the agent matches against when deciding whether to invoke it, so write that line for discovery. Users can also invoke a skill directly as `/<name>`.

[`CLAUDE.md`](../../CLAUDE.md) at the repository root carries this repository's conventions. It covers naming, frontmatter rules, when to bump a version, and which files to keep in step.

## Before you open a pull request

- The plugin installs from a local checkout without errors.
- Each skill activates when you'd expect it to, and can be invoked directly.
- The README lists what the plugin ships.
