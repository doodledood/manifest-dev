---
name: setup-manifest-dev
description: 'One-command setup for manifest-dev: auto-detects the plugin install scope (local dev, project, or user) and pre-grants the four permissions needed to run /define and /do without prompts. Triggers: setup manifest-dev, install manifest-dev, configure permissions, permission prompts, run setup.'
user-invocable: true
---

Run the following Bash command to configure manifest-dev permissions:

```bash
python3 << 'PYEOF'
import json, os, sys

HOME = os.path.expanduser("~")
CWD = os.getcwd()

REQUIRED_RULES = [
    "Read(~/.claude/plugins/cache/manifest-dev/manifest-dev/*/**)",
    "Edit(//tmp/manifest-*.md)",
    "Edit(//tmp/define-discovery-*.md)",
    "Edit(//tmp/do-log-*.md)",
]

# Scope detection: local → project → user (most-specific first)
# Local: dev clone — .claude/skills/setup-manifest-dev symlink exists in project
# Project: plugin installed at project level in .claude/plugins/cache/
# User: plugin installed at user level in ~/.claude/plugins/cache/
scope_checks = [
    (
        "local",
        os.path.join(CWD, ".claude", "skills", "setup-manifest-dev"),
        os.path.join(CWD, ".claude", "settings.local.json"),
    ),
    (
        "project",
        os.path.join(CWD, ".claude", "plugins", "cache", "manifest-dev"),
        os.path.join(CWD, ".claude", "settings.json"),
    ),
    (
        "user",
        os.path.join(HOME, ".claude", "plugins", "cache", "manifest-dev"),
        os.path.join(HOME, ".claude", "settings.json"),
    ),
]

detected_scope = None
settings_file = None
for scope, plugin_path, settings_path in scope_checks:
    if os.path.exists(plugin_path):
        detected_scope = scope
        settings_file = settings_path
        break

if detected_scope is None:
    checked_paths = [p for _, p, _ in scope_checks]
    print("Error: manifest-dev plugin not found at any expected location:")
    for p in checked_paths:
        print(f"  - {p}")
    print()
    print("Manual fix: add the following to your ~/.claude/settings.json (user)")
    print("or .claude/settings.json (project) under permissions.allow:")
    for r in REQUIRED_RULES:
        print(f'  "{r}"')
    sys.exit(1)

# Read existing settings (or start fresh)
if not os.path.exists(settings_file):
    settings = {}
else:
    try:
        with open(settings_file) as f:
            settings = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: JSON syntax error in {settings_file}: {e}")
        print("Fix the syntax error manually, then re-run /setup-manifest-dev.")
        sys.exit(1)
    if not isinstance(settings, dict):
        print(f"Error: {settings_file} contains valid JSON but its root is not an object (got {type(settings).__name__}).")
        print("Fix the file so its root is a JSON object {}, then re-run /setup-manifest-dev.")
        sys.exit(1)

# Merge rules (deduplicate by exact string match)
allow = settings.setdefault("permissions", {}).setdefault("allow", [])
added = 0
for r in REQUIRED_RULES:
    if r not in allow:
        allow.append(r)
        added += 1

# Ensure parent directory exists
os.makedirs(os.path.dirname(settings_file), exist_ok=True)

# Write back with proper JSON formatting
with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

status = f"{added} rules added" if added > 0 else "already up to date"
print(f"✓ Detected {detected_scope} scope. Updated {settings_file} with manifest-dev permissions ({status}).")
if added > 0:
    print("  Reload your editor if you have that file open.")
PYEOF
```

Run this command exactly as shown, then report the output to the user.
