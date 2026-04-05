#!/usr/bin/env python3
"""
Namespacing helper for manifest-dev OpenCode distribution.

Adds -manifest-dev suffix to all component names and patches internal
cross-references so skills, agents, and commands reference each other
by their namespaced names.
"""

from __future__ import annotations

import os
import re
import shutil
import sys

SUFFIX = "-manifest-dev"

# Skills that exist in the distribution
SKILL_NAMES = [
    "auto", "define", "do", "done", "escalate",
    "learn-define-patterns", "tend-pr", "tend-pr-tick",
    "figure-out", "stop-thinking-disciplines",
    "thinking-disciplines", "verify",
]

# Agent filenames (without .md)
AGENT_NAMES = [
    "change-intent-reviewer", "code-bugs-reviewer", "code-coverage-reviewer",
    "code-design-reviewer", "code-maintainability-reviewer",
    "code-simplicity-reviewer", "code-testability-reviewer",
    "context-file-adherence-reviewer", "contracts-reviewer",
    "criteria-checker", "define-session-analyzer", "docs-reviewer",
    "manifest-verifier", "type-safety-reviewer",
]

# Command filenames (without .md)
COMMAND_NAMES = [
    "auto", "define", "do", "learn-define-patterns",
    "tend-pr", "figure-out", "stop-thinking-disciplines",
]


def namespace_skill_dir(src: str, dst_parent: str, name: str) -> None:
    """Copy a skill directory with namespaced name and patch SKILL.md."""
    ns_name = name + SUFFIX
    dst = os.path.join(dst_parent, ns_name)

    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # Patch SKILL.md name field
    skill_md = os.path.join(dst, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r") as f:
            content = f.read()

        # Patch the name: field in frontmatter
        content = re.sub(
            r"^(name:\s*)" + re.escape(name) + r"\s*$",
            rf"\g<1>{ns_name}",
            content,
            count=1,
            flags=re.MULTILINE,
        )

        # Patch cross-references to other skills
        content = _patch_cross_references(content)

        with open(skill_md, "w") as f:
            f.write(content)

    # Patch any .md files in subdirectories
    for root, _dirs, files in os.walk(dst):
        for fname in files:
            if fname.endswith(".md") and fname != "SKILL.md":
                fpath = os.path.join(root, fname)
                with open(fpath, "r") as f:
                    content = f.read()
                patched = _patch_cross_references(content)
                if patched != content:
                    with open(fpath, "w") as f:
                        f.write(patched)


def namespace_agent_file(src: str, dst_parent: str, name: str) -> None:
    """Copy an agent file with namespaced name and patch references."""
    ns_name = name + SUFFIX
    dst = os.path.join(dst_parent, ns_name + ".md")
    shutil.copy2(src, dst)

    with open(dst, "r") as f:
        content = f.read()

    content = _patch_cross_references(content)

    with open(dst, "w") as f:
        f.write(content)


def namespace_command_file(src: str, dst_parent: str, name: str) -> None:
    """Copy a command file with namespaced name and patch references."""
    ns_name = name + SUFFIX
    dst = os.path.join(dst_parent, ns_name + ".md")
    shutil.copy2(src, dst)

    with open(dst, "r") as f:
        content = f.read()

    content = _patch_cross_references(content)

    with open(dst, "w") as f:
        f.write(content)


def _patch_cross_references(content: str) -> str:
    """Patch skill, agent, and command cross-references to use namespaced names."""
    # Sort names by length descending to match longest first
    all_names = sorted(SKILL_NAMES + AGENT_NAMES, key=len, reverse=True)

    for name in all_names:
        ns = name + SUFFIX

        # manifest-dev:<skill> -> manifest-dev:<skill>-manifest-dev
        content = content.replace(f"manifest-dev:{name}", f"manifest-dev:{ns}")

        # /skill-name -> /skill-name-manifest-dev (in command references)
        # Only match when followed by word boundary
        content = re.sub(
            rf"(?<![a-zA-Z0-9-])/{re.escape(name)}(?![a-zA-Z0-9-])",
            f"/{ns}",
            content,
        )

        # skills/name/ -> skills/name-manifest-dev/ (path references)
        content = content.replace(f"skills/{name}/", f"skills/{ns}/")

        # Agent name in quoted strings: "agent-name" -> "agent-name-manifest-dev"
        # Only agent names, and only in contexts like agent: or spawn patterns
        if name in AGENT_NAMES:
            # In YAML-like agent: field
            content = re.sub(
                rf'(agent:\s*["\']?)' + re.escape(name) + r'(["\']?)',
                rf"\g<1>{ns}\g<2>",
                content,
            )

    return content


def main() -> None:
    """Run namespacing on all components in a target directory."""
    if len(sys.argv) < 3:
        print("Usage: install_helpers.py <dist-dir> <target-dir>")
        sys.exit(1)

    dist_dir = sys.argv[1]
    target_dir = sys.argv[2]

    # Create target directories
    for subdir in ["skills", "agents", "commands"]:
        os.makedirs(os.path.join(target_dir, subdir), exist_ok=True)

    # Namespace skills
    skills_src = os.path.join(dist_dir, "skills")
    skills_dst = os.path.join(target_dir, "skills")
    for name in SKILL_NAMES:
        src = os.path.join(skills_src, name)
        if os.path.isdir(src):
            namespace_skill_dir(src, skills_dst, name)
            print(f"  skill: {name} -> {name}{SUFFIX}")

    # Namespace agents
    agents_src = os.path.join(dist_dir, "agents")
    agents_dst = os.path.join(target_dir, "agents")
    for name in AGENT_NAMES:
        src = os.path.join(agents_src, f"{name}.md")
        if os.path.exists(src):
            namespace_agent_file(src, agents_dst, name)
            print(f"  agent: {name} -> {name}{SUFFIX}")

    # Namespace commands
    commands_src = os.path.join(dist_dir, "commands")
    commands_dst = os.path.join(target_dir, "commands")
    for name in COMMAND_NAMES:
        src = os.path.join(commands_src, f"{name}.md")
        if os.path.exists(src):
            namespace_command_file(src, commands_dst, name)
            print(f"  command: {name} -> {name}{SUFFIX}")


if __name__ == "__main__":
    main()
