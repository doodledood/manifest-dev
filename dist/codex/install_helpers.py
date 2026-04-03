#!/usr/bin/env python3
"""
Install helpers for manifest-dev Codex CLI distribution.

Handles namespacing: adds -manifest-dev suffix to all components at install time.
The dist/codex/ directory keeps original names; this script renames during install.
"""

import os
import re
import shutil
import sys

NAMESPACE_SUFFIX = "-manifest-dev"


def namespace_skill_dir(skill_name: str) -> str:
    """Return namespaced skill directory name."""
    return skill_name + NAMESPACE_SUFFIX


def namespace_agent_file(agent_name: str) -> str:
    """Return namespaced agent TOML filename."""
    return agent_name + NAMESPACE_SUFFIX + ".toml"


def patch_skill_name(skill_md_path: str, original_name: str) -> None:
    """Patch the name: field in SKILL.md to include namespace suffix."""
    if not os.path.exists(skill_md_path):
        return
    with open(skill_md_path, "r") as f:
        content = f.read()

    namespaced = original_name + NAMESPACE_SUFFIX
    # Patch name: field in frontmatter
    content = re.sub(
        r"^(name:\s*)" + re.escape(original_name) + r"\s*$",
        r"\g<1>" + namespaced,
        content,
        count=1,
        flags=re.MULTILINE,
    )
    with open(skill_md_path, "w") as f:
        f.write(content)


def patch_cross_references(file_path: str) -> None:
    """Patch cross-references to skills and agents within a file."""
    if not os.path.exists(file_path):
        return
    with open(file_path, "r") as f:
        content = f.read()

    original = content

    # Known skill names to namespace
    skill_names = [
        "auto",
        "define",
        "do",
        "done",
        "escalate",
        "learn-define-patterns",
        "tend-pr",
        "tend-pr-tick",
        "understand",
        "understand-done",
        "verify",
    ]

    # Known agent names to namespace
    agent_names = [
        "change-intent-reviewer",
        "code-bugs-reviewer",
        "code-coverage-reviewer",
        "code-design-reviewer",
        "code-maintainability-reviewer",
        "code-simplicity-reviewer",
        "code-testability-reviewer",
        "context-file-adherence-reviewer",
        "contracts-reviewer",
        "criteria-checker",
        "define-session-analyzer",
        "docs-reviewer",
        "manifest-verifier",
        "type-safety-reviewer",
    ]

    # Patch slash command references: /define -> /define-manifest-dev
    for name in skill_names:
        # Slash commands in text
        content = re.sub(
            r"(?<![/\w])/(" + re.escape(name) + r")(?!\w)",
            "/" + name + NAMESPACE_SUFFIX,
            content,
        )

    # Patch agent name references in quotes or as identifiers
    for name in agent_names:
        # Agent names as identifiers (not already suffixed)
        content = re.sub(
            r"(?<!\w)" + re.escape(name) + r"(?!" + re.escape(NAMESPACE_SUFFIX) + r")(?!\w)",
            name + NAMESPACE_SUFFIX,
            content,
        )

    # Patch config_file paths in TOML
    content = re.sub(
        r'(config_file\s*=\s*"agents/)([^"]+)(\.toml")',
        lambda m: m.group(1) + m.group(2) + NAMESPACE_SUFFIX + m.group(3),
        content,
    )

    # Patch agent section headers in TOML
    content = re.sub(
        r"(\[agents\.)([a-z][-a-z0-9]*)(])",
        lambda m: m.group(1) + m.group(2) + NAMESPACE_SUFFIX + m.group(3)
        if m.group(2) in agent_names
        else m.group(0),
        content,
    )

    if content != original:
        with open(file_path, "w") as f:
            f.write(content)


def install_skills(src_dir: str, dest_dir: str) -> list[str]:
    """Install skills with namespacing. Returns list of installed skill names."""
    installed = []
    skills_src = os.path.join(src_dir, "skills")
    if not os.path.isdir(skills_src):
        return installed

    for skill_name in sorted(os.listdir(skills_src)):
        skill_src_path = os.path.join(skills_src, skill_name)
        if not os.path.isdir(skill_src_path):
            continue

        namespaced_name = namespace_skill_dir(skill_name)
        skill_dest_path = os.path.join(dest_dir, namespaced_name)

        # Remove existing namespaced skill if present
        if os.path.exists(skill_dest_path):
            shutil.rmtree(skill_dest_path)

        shutil.copytree(skill_src_path, skill_dest_path)

        # Patch SKILL.md name field
        skill_md = os.path.join(skill_dest_path, "SKILL.md")
        patch_skill_name(skill_md, skill_name)

        installed.append(namespaced_name)

    return installed


def install_agents(src_dir: str, dest_dir: str) -> list[str]:
    """Install agent TOML files with namespacing. Returns list of installed filenames."""
    installed = []
    agents_src = os.path.join(src_dir, "agents")
    if not os.path.isdir(agents_src):
        return installed

    os.makedirs(dest_dir, exist_ok=True)

    for fname in sorted(os.listdir(agents_src)):
        if not fname.endswith(".toml"):
            continue
        agent_name = fname[: -len(".toml")]
        namespaced_fname = namespace_agent_file(agent_name)

        src_path = os.path.join(agents_src, fname)
        dest_path = os.path.join(dest_dir, namespaced_fname)

        shutil.copy2(src_path, dest_path)
        installed.append(namespaced_fname)

    return installed


def install_rules(src_dir: str, dest_dir: str) -> list[str]:
    """Install rules files. Returns list of installed filenames."""
    installed = []
    rules_src = os.path.join(src_dir, "rules")
    if not os.path.isdir(rules_src):
        return installed

    os.makedirs(dest_dir, exist_ok=True)

    for fname in sorted(os.listdir(rules_src)):
        src_path = os.path.join(rules_src, fname)
        dest_path = os.path.join(dest_dir, fname)
        shutil.copy2(src_path, dest_path)
        installed.append(fname)

    return installed


if __name__ == "__main__":
    print("install_helpers.py -- import this module or use install.sh")
    print(f"  Namespace suffix: {NAMESPACE_SUFFIX}")
    sys.exit(0)
