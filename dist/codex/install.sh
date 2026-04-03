#!/usr/bin/env bash
set -euo pipefail

# manifest-dev Codex CLI installer
# Idempotent: safe to run multiple times.
# Installs skills, agents, rules, config, and AGENTS.md with -manifest-dev namespacing.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-.}"

# Resolve to absolute path
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

echo "manifest-dev Codex CLI installer"
echo "================================"
echo "Source:  $SCRIPT_DIR"
echo "Target:  $PROJECT_ROOT"
echo ""

# Directories
SKILLS_DEST="$PROJECT_ROOT/.agents/skills"
AGENTS_DEST="$PROJECT_ROOT/.codex/agents"
RULES_DEST="$PROJECT_ROOT/.codex/rules"
CONFIG_DEST="$PROJECT_ROOT/.codex/config.toml"

# --------------------------------------------------------------------------
# Step 1: Selective cleanup of previous manifest-dev installs
# --------------------------------------------------------------------------
echo "[1/6] Cleaning previous manifest-dev installs..."

# Remove only manifest-dev namespaced skills
find "$SKILLS_DEST" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true

# Remove only manifest-dev namespaced agent TOMLs
find "$AGENTS_DEST" -maxdepth 1 -name "*-manifest-dev*" -type f -exec rm -f {} + 2>/dev/null || true

echo "  Done."

# --------------------------------------------------------------------------
# Step 2: Install skills with namespacing
# --------------------------------------------------------------------------
echo "[2/6] Installing skills..."

mkdir -p "$SKILLS_DEST"

python3 "$SCRIPT_DIR/install_helpers.py" 2>/dev/null || true

# Use Python for namespaced install
python3 - "$SCRIPT_DIR" "$SKILLS_DEST" << 'PYEOF'
import sys
sys.path.insert(0, sys.argv[1])
from install_helpers import install_skills
installed = install_skills(sys.argv[1], sys.argv[2])
for s in installed:
    print(f"  Installed skill: {s}")
print(f"  {len(installed)} skills installed.")
PYEOF

# --------------------------------------------------------------------------
# Step 3: Install agent TOMLs with namespacing
# --------------------------------------------------------------------------
echo "[3/6] Installing agents..."

mkdir -p "$AGENTS_DEST"

python3 - "$SCRIPT_DIR" "$AGENTS_DEST" << 'PYEOF'
import sys
sys.path.insert(0, sys.argv[1])
from install_helpers import install_agents
installed = install_agents(sys.argv[1], sys.argv[2])
for a in installed:
    print(f"  Installed agent: {a}")
print(f"  {len(installed)} agents installed.")
PYEOF

# --------------------------------------------------------------------------
# Step 4: Install rules
# --------------------------------------------------------------------------
echo "[4/6] Installing rules..."

mkdir -p "$RULES_DEST"

python3 - "$SCRIPT_DIR" "$RULES_DEST" << 'PYEOF'
import sys
sys.path.insert(0, sys.argv[1])
from install_helpers import install_rules
installed = install_rules(sys.argv[1], sys.argv[2])
for r in installed:
    print(f"  Installed rule: {r}")
print(f"  {len(installed)} rules installed.")
PYEOF

# --------------------------------------------------------------------------
# Step 5: Merge config.toml additively
# --------------------------------------------------------------------------
echo "[5/6] Merging config.toml..."

mkdir -p "$(dirname "$CONFIG_DEST")"

if [ -f "$CONFIG_DEST" ]; then
    # Additive merge: append manifest-dev sections if not already present
    if grep -q "agents.change-intent-reviewer" "$CONFIG_DEST" 2>/dev/null; then
        echo "  Config already contains manifest-dev agent entries. Skipping merge."
    else
        echo "" >> "$CONFIG_DEST"
        echo "# --- manifest-dev additions (auto-merged) ---" >> "$CONFIG_DEST"
        cat "$SCRIPT_DIR/config.toml" >> "$CONFIG_DEST"
        echo "  Appended manifest-dev config to existing config.toml."
    fi
else
    cp "$SCRIPT_DIR/config.toml" "$CONFIG_DEST"
    echo "  Created new config.toml."
fi

# Patch config.toml agent references with namespace suffix
python3 - "$CONFIG_DEST" << 'PYEOF'
import sys
import re

config_path = sys.argv[1]
SUFFIX = "-manifest-dev"

with open(config_path, "r") as f:
    content = f.read()

# Only patch manifest-dev agent entries that aren't already namespaced
agent_names = [
    "change-intent-reviewer", "code-bugs-reviewer", "code-coverage-reviewer",
    "code-design-reviewer", "code-maintainability-reviewer", "code-simplicity-reviewer",
    "code-testability-reviewer", "context-file-adherence-reviewer", "contracts-reviewer",
    "criteria-checker", "define-session-analyzer", "docs-reviewer",
    "manifest-verifier", "type-safety-reviewer",
]

for name in agent_names:
    # Patch [agents.name] headers
    content = content.replace(
        f"[agents.{name}]",
        f"[agents.{name}{SUFFIX}]"
    )
    # Patch config_file references
    content = content.replace(
        f'config_file = "agents/{name}.toml"',
        f'config_file = "agents/{name}{SUFFIX}.toml"'
    )

with open(config_path, "w") as f:
    f.write(content)

print("  Patched config.toml with namespace suffixes.")
PYEOF

# --------------------------------------------------------------------------
# Step 6: Copy AGENTS.md
# --------------------------------------------------------------------------
echo "[6/6] Installing AGENTS.md..."

if [ -f "$PROJECT_ROOT/AGENTS.md" ]; then
    # Append if not already present
    if grep -q "manifest-dev Agents" "$PROJECT_ROOT/AGENTS.md" 2>/dev/null; then
        echo "  AGENTS.md already contains manifest-dev section. Skipping."
    else
        echo "" >> "$PROJECT_ROOT/AGENTS.md"
        cat "$SCRIPT_DIR/AGENTS.md" >> "$PROJECT_ROOT/AGENTS.md"
        echo "  Appended manifest-dev section to existing AGENTS.md."
    fi
else
    cp "$SCRIPT_DIR/AGENTS.md" "$PROJECT_ROOT/AGENTS.md"
    echo "  Created new AGENTS.md."
fi

echo ""
echo "Installation complete!"
echo ""
echo "Installed components:"
echo "  Skills:  $SKILLS_DEST/*-manifest-dev/"
echo "  Agents:  $AGENTS_DEST/*-manifest-dev.toml"
echo "  Rules:   $RULES_DEST/"
echo "  Config:  $CONFIG_DEST"
echo "  Docs:    $PROJECT_ROOT/AGENTS.md"
echo ""
echo "To verify: codex execpolicy check --pretty --rules $RULES_DEST/default.rules -- git status"
