#!/usr/bin/env python3
"""
Install helpers for manifest-dev Gemini CLI extension.

Handles namespacing: adds -manifest-dev suffix to all components at install time.
The dist/gemini/ directory keeps original names; this script renames during install.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

NAMESPACE = "manifest-dev"
SUFFIX = f"-{NAMESPACE}"

# Skills that are referenced in cross-references
SKILL_NAMES = [
    "auto", "define", "do", "done", "escalate",
    "learn-define-patterns", "tend-pr", "tend-pr-tick",
    "understand", "understand-done", "verify",
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


def namespace_skill_dir(src_dir: Path, dst_dir: Path) -> None:
    """Copy a skill directory with namespaced name and patch contents."""
    skill_name = src_dir.name
    namespaced_name = f"{skill_name}{SUFFIX}"
    target = dst_dir / namespaced_name

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(src_dir, target)

    # Patch SKILL.md name field
    skill_md = target / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        # Update name: field in frontmatter
        content = re.sub(
            r"^(name:\s*)(.+)$",
            rf"\g<1>{namespaced_name}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
        # Patch cross-references to other skills
        content = patch_cross_references(content)
        skill_md.write_text(content)

    # Patch any other .md files in subdirectories
    for md_file in target.rglob("*.md"):
        if md_file.name == "SKILL.md":
            continue
        content = md_file.read_text()
        patched = patch_cross_references(content)
        if patched != content:
            md_file.write_text(patched)


def namespace_agent_file(src_file: Path, dst_dir: Path) -> None:
    """Copy an agent file with namespaced name and patch contents."""
    agent_name = src_file.stem
    namespaced_name = f"{agent_name}{SUFFIX}"
    target = dst_dir / f"{namespaced_name}.md"

    content = src_file.read_text()

    # Update name: field in frontmatter
    content = re.sub(
        r"^(name:\s*)(.+)$",
        rf"\g<1>{namespaced_name}",
        content,
        count=1,
        flags=re.MULTILINE,
    )

    # Patch cross-references
    content = patch_cross_references(content)

    target.write_text(content)


def patch_cross_references(content: str) -> str:
    """Patch skill and agent cross-references to use namespaced names."""
    # Patch slash command references: /skill-name → /skill-name-manifest-dev
    for skill in SKILL_NAMES:
        # /skill-name (at word boundary)
        content = re.sub(
            rf"(?<!\w)/{re.escape(skill)}(?=[\s,.\)\]\"'`]|$)",
            f"/{skill}{SUFFIX}",
            content,
        )
        # manifest-dev:skill-name → manifest-dev:skill-name-manifest-dev
        content = content.replace(
            f"manifest-dev:{skill}",
            f"manifest-dev:{skill}{SUFFIX}",
        )

    # Patch agent name references in quoted strings
    for agent in AGENT_NAMES:
        # Agent names in contexts like "code-bugs-reviewer" or agent: code-bugs-reviewer
        content = re.sub(
            rf"(?<=agent:\s){re.escape(agent)}(?=\s|$|\")",
            f"{agent}{SUFFIX}",
            content,
        )

    return content


def patch_hooks_json(hooks_file: Path, extension_path: str) -> dict:
    """Read hooks.json and patch paths for installed location."""
    with open(hooks_file) as f:
        config = json.load(f)

    # Replace ${extensionPath} with actual path
    def patch_command(cmd: str) -> str:
        return cmd.replace("${extensionPath}", extension_path)

    hooks = config.get("hooks", {})
    for event_type, event_hooks in hooks.items():
        for hook_group in event_hooks:
            for hook in hook_group.get("hooks", []):
                if "command" in hook:
                    hook["command"] = patch_command(hook["command"])

    return config


def merge_settings(settings_path: Path, hook_config: dict) -> None:
    """Additively merge settings into existing settings.json."""
    existing: dict = {}
    if settings_path.exists():
        try:
            with open(settings_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = {}

    # Enable agents
    if "experimental" not in existing:
        existing["experimental"] = {}
    existing["experimental"]["enableAgents"] = True

    # Merge hooks additively
    if "hooks" not in existing:
        existing["hooks"] = {}

    for event_type, new_hooks in hook_config.get("hooks", {}).items():
        if event_type not in existing["hooks"]:
            existing["hooks"][event_type] = []

        # Remove existing manifest-dev hooks (by name)
        manifest_dev_names = set()
        for hook_group in new_hooks:
            for hook in hook_group.get("hooks", []):
                if hook.get("name", "").endswith(f"-{NAMESPACE}") or NAMESPACE in hook.get("command", ""):
                    manifest_dev_names.add(hook.get("name"))

        # Filter out old manifest-dev entries
        existing_hooks = existing["hooks"][event_type]
        filtered = []
        for hook_group in existing_hooks:
            remaining_hooks = []
            for hook in hook_group.get("hooks", []):
                if hook.get("name") not in manifest_dev_names and NAMESPACE not in hook.get("command", ""):
                    remaining_hooks.append(hook)
            if remaining_hooks:
                hook_group["hooks"] = remaining_hooks
                filtered.append(hook_group)

        # Add new hooks
        existing["hooks"][event_type] = filtered + new_hooks

    # Write back
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(existing, f, indent=2)
        f.write("\n")


def main() -> int:
    """Run namespacing as standalone script for testing."""
    if len(sys.argv) < 3:
        print("Usage: install_helpers.py <src_dir> <dst_dir>")
        return 1

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    # Namespace skills
    src_skills = src / "skills"
    dst_skills = dst / "skills"
    dst_skills.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(src_skills.iterdir()):
        if skill_dir.is_dir():
            namespace_skill_dir(skill_dir, dst_skills)
            print(f"  skill: {skill_dir.name} -> {skill_dir.name}{SUFFIX}")

    # Namespace agents
    src_agents = src / "agents"
    dst_agents = dst / "agents"
    dst_agents.mkdir(parents=True, exist_ok=True)

    for agent_file in sorted(src_agents.glob("*.md")):
        namespace_agent_file(agent_file, dst_agents)
        print(f"  agent: {agent_file.stem} -> {agent_file.stem}{SUFFIX}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
