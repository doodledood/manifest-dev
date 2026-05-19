#!/usr/bin/env python3
"""
Namespacing helper for manifest-dev OpenCode distribution.

Adds -manifest-dev suffix to all component names and patches internal
cross-references so skills, agents, and commands reference each other
by their namespaced names.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys

DEFAULT_SUFFIX = "-manifest-dev"
KNOWN_MANAGED_SUFFIXES = [DEFAULT_SUFFIX, "-manifest-dev-tools"]
COMPONENT_NAMESPACE_FILE = "component-namespaces.json"


def _load_component_namespaces(dist_dir: str) -> dict[str, object]:
    metadata_path = os.path.join(dist_dir, COMPONENT_NAMESPACE_FILE)
    if not os.path.isfile(metadata_path):
        return {}
    try:
        with open(metadata_path) as f:
            data = json.load(f)
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
    """Return a source component name, even if the installer is re-run in place."""
    for suffix in suffixes:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def _names_from_dirs(parent: str, suffixes: list[str]) -> list[str]:
    if not os.path.isdir(parent):
        return []
    return sorted(
        {
            _strip_suffix(name, suffixes)
            for name in os.listdir(parent)
            if os.path.isdir(os.path.join(parent, name))
        }
    )


def _names_from_files(parent: str, suffix: str, suffixes: list[str]) -> list[str]:
    if not os.path.isdir(parent):
        return []
    return sorted(
        {
            _strip_suffix(name[: -len(suffix)], suffixes)
            for name in os.listdir(parent)
            if name.endswith(suffix) and os.path.isfile(os.path.join(parent, name))
        }
    )


def _component_names(
    dist_dir: str,
    suffixes: list[str],
) -> tuple[list[str], list[str], list[str]]:
    return (
        _names_from_dirs(os.path.join(dist_dir, "skills"), suffixes),
        _names_from_files(os.path.join(dist_dir, "agents"), ".md", suffixes),
        _names_from_files(os.path.join(dist_dir, "commands"), ".md", suffixes),
    )


def namespace_skill_dir(
    src: str,
    dst_parent: str,
    name: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> None:
    """Copy a skill directory with namespaced name and patch SKILL.md."""
    ns_name = name + skill_names[name]
    dst = os.path.join(dst_parent, ns_name)

    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # Patch SKILL.md name field
    skill_md = os.path.join(dst, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md) as f:
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
        content = _patch_cross_references(content, skill_names, agent_names)

        with open(skill_md, "w") as f:
            f.write(content)

    # Patch any .md files in subdirectories
    for root, _dirs, files in os.walk(dst):
        for fname in files:
            if fname.endswith(".md") and fname != "SKILL.md":
                fpath = os.path.join(root, fname)
                with open(fpath) as f:
                    content = f.read()
                patched = _patch_cross_references(content, skill_names, agent_names)
                if patched != content:
                    with open(fpath, "w") as f:
                        f.write(patched)


def namespace_agent_file(
    src: str,
    dst_parent: str,
    name: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> None:
    """Copy an agent file with namespaced name and patch references."""
    ns_name = name + agent_names[name]
    dst = os.path.join(dst_parent, ns_name + ".md")
    shutil.copy2(src, dst)

    with open(dst) as f:
        content = f.read()

    content = _patch_cross_references(content, skill_names, agent_names)

    with open(dst, "w") as f:
        f.write(content)


def namespace_command_file(
    src: str,
    dst_parent: str,
    name: str,
    command_names: dict[str, str],
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> None:
    """Copy a command file with namespaced name and patch references."""
    ns_name = name + command_names[name]
    dst = os.path.join(dst_parent, ns_name + ".md")
    shutil.copy2(src, dst)

    with open(dst) as f:
        content = f.read()

    content = _patch_cross_references(content, skill_names, agent_names)

    with open(dst, "w") as f:
        f.write(content)


def _patch_cross_references(
    content: str,
    skill_names: dict[str, str],
    agent_names: dict[str, str],
) -> str:
    """Patch skill, agent, and command cross-references to use namespaced names."""
    # Sort names by length descending to match longest first
    agent_name_set = set(agent_names)
    all_names = sorted(set(skill_names) | set(agent_names), key=len, reverse=True)

    for name in all_names:
        suffix = agent_names[name] if name in agent_name_set else skill_names[name]
        ns = name + suffix

        # manifest-dev:<skill> -> manifest-dev:<skill>-manifest-dev
        content = content.replace(f"manifest-dev:{name}", f"manifest-dev:{ns}")
        content = content.replace(
            f"manifest-dev-tools:{name}",
            f"manifest-dev-tools:{ns}",
        )

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
        if name in agent_name_set:
            # In YAML-like agent: field
            content = re.sub(
                r'(agent:\s*["\']?)' + re.escape(name) + r'(["\']?)',
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
    metadata = _load_component_namespaces(dist_dir)
    suffixes = _metadata_suffixes(metadata)
    discovered_skill_names, discovered_agent_names, discovered_command_names = (
        _component_names(dist_dir, suffixes)
    )
    skill_names = {
        name: _suffix_for(metadata, "skills", name) for name in discovered_skill_names
    }
    agent_names = {
        name: _suffix_for(metadata, "agents", name) for name in discovered_agent_names
    }
    command_names = {
        name: _suffix_for(metadata, "commands", name)
        for name in discovered_command_names
    }

    # Create target directories
    for subdir in ["skills", "agents", "commands"]:
        os.makedirs(os.path.join(target_dir, subdir), exist_ok=True)

    # Namespace skills
    skills_src = os.path.join(dist_dir, "skills")
    skills_dst = os.path.join(target_dir, "skills")
    for name in skill_names:
        src = os.path.join(skills_src, name)
        if os.path.isdir(src):
            namespace_skill_dir(src, skills_dst, name, skill_names, agent_names)
            print(f"  skill: {name} -> {name}{skill_names[name]}")

    # Namespace agents
    agents_src = os.path.join(dist_dir, "agents")
    agents_dst = os.path.join(target_dir, "agents")
    for name in agent_names:
        src = os.path.join(agents_src, f"{name}.md")
        if os.path.exists(src):
            namespace_agent_file(src, agents_dst, name, skill_names, agent_names)
            print(f"  agent: {name} -> {name}{agent_names[name]}")

    # Namespace commands
    commands_src = os.path.join(dist_dir, "commands")
    commands_dst = os.path.join(target_dir, "commands")
    for name in command_names:
        src = os.path.join(commands_src, f"{name}.md")
        if os.path.exists(src):
            namespace_command_file(
                src,
                commands_dst,
                name,
                command_names,
                skill_names,
                agent_names,
            )
            print(f"  command: {name} -> {name}{command_names[name]}")


if __name__ == "__main__":
    main()
