#!/usr/bin/env python3
"""
Install helpers for manifest-dev Gemini CLI extension.

Handles namespacing: adds plugin-owned suffixes to components at install time.
The dist/gemini/ directory keeps original names; this script renames during install.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

NAMESPACE = "manifest-dev"
DEFAULT_SUFFIX = f"-{NAMESPACE}"
KNOWN_MANAGED_SUFFIXES = [DEFAULT_SUFFIX, "-manifest-dev-tools"]
COMPONENT_NAMESPACE_FILE = "component-namespaces.json"


def _load_component_namespaces(src: Path) -> dict[str, object]:
    metadata_path = src / COMPONENT_NAMESPACE_FILE
    if not metadata_path.is_file():
        return {}
    try:
        data = json.loads(metadata_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _metadata_suffixes(metadata: dict[str, object]) -> list[str]:
    suffixes = metadata.get("suffixes")
    if isinstance(suffixes, list):
        values = [suffix for suffix in suffixes if isinstance(suffix, str)]
        if values:
            return sorted(set(values), key=len, reverse=True)
    return KNOWN_MANAGED_SUFFIXES


def _suffix_for(
    metadata: dict[str, object],
    component_type: str,
    name: str,
) -> str:
    components = metadata.get(component_type)
    if isinstance(components, dict):
        suffix = components.get(name)
        if isinstance(suffix, str) and suffix:
            return suffix
    return DEFAULT_SUFFIX


def _strip_suffix(name: str, suffixes: list[str]) -> str:
    """Return a source component name, even if a temp dist is re-used."""
    for suffix in suffixes:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def discover_components(src: Path, suffixes: list[str]) -> tuple[list[str], list[str]]:
    """Discover distributed skill and agent names from the filesystem."""
    skills_dir = src / "skills"
    agents_dir = src / "agents"
    skills = (
        sorted(
            {
                _strip_suffix(path.name, suffixes)
                for path in skills_dir.iterdir()
                if path.is_dir()
            }
        )
        if skills_dir.is_dir()
        else []
    )
    agents = (
        sorted(
            {
                _strip_suffix(path.stem, suffixes)
                for path in agents_dir.glob("*.md")
                if path.is_file()
            }
        )
        if agents_dir.is_dir()
        else []
    )
    return skills, agents


def namespace_skill_dir(
    src_dir: Path,
    dst_dir: Path,
    skill_name: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> None:
    """Copy a skill directory with namespaced name and patch contents."""
    namespaced_name = f"{skill_name}{skill_names[skill_name]}"
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
        content = patch_cross_references(content, skill_names, agent_names)
        skill_md.write_text(content)

    # Patch any other .md files in subdirectories
    for md_file in target.rglob("*.md"):
        if md_file.name == "SKILL.md":
            continue
        content = md_file.read_text()
        patched = patch_cross_references(content, skill_names, agent_names)
        if patched != content:
            md_file.write_text(patched)


def namespace_agent_file(
    src_file: Path,
    dst_dir: Path,
    agent_name: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> None:
    """Copy an agent file with namespaced name and patch contents."""
    namespaced_name = f"{agent_name}{agent_names[agent_name]}"
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
    content = patch_cross_references(content, skill_names, agent_names)

    target.write_text(content)


def patch_cross_references(
    content: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> str:
    """Patch skill and agent cross-references to use namespaced names."""
    # Patch slash command references: /skill-name → /skill-name-manifest-dev
    for skill in sorted(set(skill_names), key=len, reverse=True):
        suffix = skill_names[skill]
        # /skill-name (at word boundary)
        content = re.sub(
            rf"(?<!\w)/{re.escape(skill)}(?=[\s,.\)\]\"'`]|$)",
            f"/{skill}{suffix}",
            content,
        )
        # manifest-dev:skill-name → manifest-dev:skill-name-manifest-dev.
        # Keep the match boundary-aware so shorter overlapping names do not
        # rewrite longer names after they have already been patched.
        for namespace in ("manifest-dev", "manifest-dev-tools"):
            content = re.sub(
                rf"(?<![a-zA-Z0-9-]){re.escape(namespace)}:{re.escape(skill)}"
                r"(?![a-zA-Z0-9-])",
                f"{namespace}:{skill}{suffix}",
                content,
            )

    # Patch agent name references in quoted strings
    for agent in sorted(set(agent_names), key=len, reverse=True):
        suffix = agent_names[agent]
        # Agent names in contexts like "code-bugs-reviewer" or agent: code-bugs-reviewer
        content = re.sub(
            rf"(?<=agent:\s){re.escape(agent)}(?=\s|$|\")",
            f"{agent}{suffix}",
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
    for _event_type, event_hooks in hooks.items():
        for hook_group in event_hooks:
            for hook in hook_group.get("hooks", []):
                if "command" in hook:
                    hook["command"] = patch_command(hook["command"])
                if "name" in hook and not hook["name"].endswith(f"-{NAMESPACE}"):
                    hook["name"] = f"{hook['name']}-{NAMESPACE}"

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
                if hook.get("name", "").endswith(
                    f"-{NAMESPACE}"
                ) or NAMESPACE in hook.get("command", ""):
                    manifest_dev_names.add(hook.get("name"))

        # Filter out old manifest-dev entries
        existing_hooks = existing["hooks"][event_type]
        filtered = []
        for hook_group in existing_hooks:
            remaining_hooks = []
            for hook in hook_group.get("hooks", []):
                if hook.get(
                    "name"
                ) not in manifest_dev_names and NAMESPACE not in hook.get(
                    "command", ""
                ):
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


def build_install_state(settings_path: Path) -> dict:
    """Capture user-owned settings before install so uninstall is conservative."""
    existing: dict = {}
    settings_existed = settings_path.exists()
    if settings_existed:
        try:
            with open(settings_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = {}

    experimental = existing.get("experimental")
    return {
        "version": 1,
        "settings_existed": settings_existed,
        "enable_agents_existed": isinstance(experimental, dict)
        and "enableAgents" in experimental,
    }


def write_install_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def _load_install_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {}
    try:
        with open(state_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _remove_manifest_hooks(existing: dict) -> None:
    hooks = existing.get("hooks")
    if not isinstance(hooks, dict):
        return

    for event_type in list(hooks):
        event_hooks = hooks.get(event_type)
        if not isinstance(event_hooks, list):
            continue

        filtered_groups = []
        for hook_group in event_hooks:
            if not isinstance(hook_group, dict):
                filtered_groups.append(hook_group)
                continue

            remaining_hooks = []
            for hook in hook_group.get("hooks", []):
                if not isinstance(hook, dict):
                    remaining_hooks.append(hook)
                    continue
                name = hook.get("name", "")
                command = hook.get("command", "")
                if name.endswith(f"-{NAMESPACE}") or NAMESPACE in command:
                    continue
                remaining_hooks.append(hook)

            if remaining_hooks:
                hook_group["hooks"] = remaining_hooks
                filtered_groups.append(hook_group)

        if filtered_groups:
            hooks[event_type] = filtered_groups
        else:
            del hooks[event_type]

    if not hooks:
        existing.pop("hooks", None)


def unmerge_settings(settings_path: Path, state_path: Path) -> None:
    """Remove manifest-dev settings while preserving user-owned values."""
    if not settings_path.exists():
        if state_path.exists():
            state_path.unlink()
        return

    try:
        with open(settings_path) as f:
            existing = json.load(f)
    except (json.JSONDecodeError, OSError):
        existing = {}

    state = _load_install_state(state_path)
    _remove_manifest_hooks(existing)

    experimental = existing.get("experimental")
    if (
        isinstance(experimental, dict)
        and not state.get("enable_agents_existed", True)
        and experimental.get("enableAgents") is True
    ):
        experimental.pop("enableAgents", None)
        if not experimental:
            existing.pop("experimental", None)

    if existing or state.get("settings_existed", True):
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w") as f:
            json.dump(existing, f, indent=2)
            f.write("\n")
    else:
        settings_path.unlink()

    if state_path.exists():
        state_path.unlink()


def main() -> int:
    """Run namespacing as standalone script for testing."""
    if len(sys.argv) < 3:
        print("Usage: install_helpers.py <src_dir> <dst_dir>")
        return 1

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    metadata = _load_component_namespaces(src)
    suffixes = _metadata_suffixes(metadata)
    discovered_skill_names, discovered_agent_names = discover_components(src, suffixes)
    skill_names = {
        name: _suffix_for(metadata, "skills", name) for name in discovered_skill_names
    }
    agent_names = {
        name: _suffix_for(metadata, "agents", name) for name in discovered_agent_names
    }

    # Namespace skills
    src_skills = src / "skills"
    dst_skills = dst / "skills"
    dst_skills.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(src_skills.iterdir()):
        if skill_dir.is_dir():
            skill_name = _strip_suffix(skill_dir.name, suffixes)
            namespace_skill_dir(
                skill_dir, dst_skills, skill_name, skill_names, agent_names
            )
            print(f"  skill: {skill_name} -> {skill_name}{skill_names[skill_name]}")

    # Namespace agents
    src_agents = src / "agents"
    dst_agents = dst / "agents"
    dst_agents.mkdir(parents=True, exist_ok=True)

    for agent_file in sorted(src_agents.glob("*.md")):
        agent_name = _strip_suffix(agent_file.stem, suffixes)
        namespace_agent_file(
            agent_file, dst_agents, agent_name, skill_names, agent_names
        )
        print(f"  agent: {agent_name} -> {agent_name}{agent_names[agent_name]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
