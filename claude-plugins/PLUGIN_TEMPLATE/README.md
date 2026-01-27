# Plugin Template

Starting point for creating Claude Code plugins.

## Structure

```
your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: metadata
├── agents/                   # Specialized agents
│   └── example-agent.md
├── skills/                   # Skills (user and auto-invoked)
│   └── example/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   └── hooks.json
└── README.md
```

## Setup

1. Copy this template:
   ```bash
   cp -r claude-plugins/PLUGIN_TEMPLATE claude-plugins/your-plugin-name
   ```

2. Edit `.claude-plugin/plugin.json`:
   ```json
   {
     "name": "your-plugin-name",
     "description": "What it does",
     "version": "1.0.0"
   }
   ```

3. Add components as needed

4. Register in `.claude-plugin/marketplace.json`

5. Test locally:
   ```bash
   /plugin marketplace add /path/to/manifest-dev
   /plugin install your-plugin-name@manifest-dev-marketplace
   ```

## Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers skills based on semantic matching with the description
- **User-invoked**: Users invoke via `/skill-name` (controlled by `user-invocable` frontmatter)

See [CLAUDE.md](../../CLAUDE.md) for detailed guidelines.

## Testing

- [ ] Plugin installs without errors
- [ ] Agents are accessible
- [ ] Skills activate in appropriate contexts

## Resources

- [CLAUDE.md](../../CLAUDE.md) - Development guidelines
- [Claude Code Docs](https://code.claude.com/docs)
