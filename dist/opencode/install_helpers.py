#!/usr/bin/env python3
"""
Namespace manifest-dev components with -manifest-dev suffix at install time.

Renames files/directories and patches cross-references so components don't
collide with other plugins in shared directories (skills/, agents/, etc.).

Single-pass regex ensures correct handling of overlapping names (e.g., /do
vs /done) and idempotency (won't double-suffix on re-run).

Usage:
    python3 install_helpers.py namespace <dir> [codex|gemini|opencode]
    python3 install_helpers.py merge-settings <source-hooks> <dest-settings>
"""

from __future__ import annotations

import os
import json
import re
import sys
from pathlib import Path

SUFFIX = "-manifest-dev"

# Ordered longest-first within each list to avoid prefix collisions.
SKILLS = [
    "learn-define-patterns",
    "escalate",
    "define",
    "verify",
    "auto",
    "done",
    "do",
]

AGENTS = [
    "context-file-adherence-reviewer",
    "code-maintainability-reviewer",
    "code-testability-reviewer",
    "code-simplicity-reviewer",
    "code-coverage-reviewer",
    "code-design-reviewer",
    "code-bugs-reviewer",
    "type-safety-reviewer",
    "define-session-analyzer",
    "manifest-verifier",
    "criteria-checker",
    "docs-reviewer",
]

# File extensions to patch (text files only).
TEXT_EXTENSIONS = {".md", ".py", ".ts", ".json", ".toml", ".rules", ".txt"}

# Files to never patch (they ARE the namespace tooling).
SKIP_FILES = {"install_helpers.py", "install.sh"}
STATE_VERSION = 2
MANAGED_HOOK_NAMES = {
    "pretool-verify",
    "stop-do-enforcement",
    "post-compact-recovery",
}


def _build_regex() -> tuple[dict[str, str], re.Pattern[str]]:
    """Build replacement map and compiled single-pass regex.

    Negative lookahead (?![a-zA-Z0-9_-]) prevents matching inside
    already-suffixed names or longer identifiers, ensuring idempotency.
    """
    rmap: dict[str, str] = {}

    for name in SKILLS:
        # Context-prefixed patterns (the prefix prevents false positives
        # on common English words like "do", "done", "define").
        rmap[f"/{name}"] = f"/{name}{SUFFIX}"  # /verify
        rmap[f"${name}"] = f"${name}{SUFFIX}"  # $verify (Codex)
        rmap[f"skills/{name}"] = f"skills/{name}{SUFFIX}"  # skills/verify
        rmap[f'":{name}"'] = f'":{name}{SUFFIX}"'  # ":verify"
        rmap[f"':{name}'"] = f"':{name}{SUFFIX}'"  # ':verify'
        rmap[f'"{name}"'] = f'"{name}{SUFFIX}"'  # "verify"
        rmap[f"'{name}'"] = f"'{name}{SUFFIX}'"  # 'verify'
        rmap[f"`{name}`"] = f"`{name}{SUFFIX}`"  # `verify`
        rmap[f"manifest-dev:{name}"] = f"manifest-dev:{name}{SUFFIX}"

    for name in AGENTS:
        # Bare agent names are safe — all are unique multi-hyphenated
        # identifiers that don't collide with English words.
        rmap[name] = f"{name}{SUFFIX}"

    # Sort keys longest-first so the regex engine tries longer matches
    # before shorter ones at each position (e.g., /done before /do).
    sorted_keys = sorted(rmap, key=len, reverse=True)

    parts = [f"(?:{re.escape(k)})(?![a-zA-Z0-9_-])" for k in sorted_keys]
    pattern = re.compile("|".join(parts))
    return rmap, pattern


_RMAP, _RE = _build_regex()


def patch_content(text: str) -> str:
    """Apply all namespace replacements to text (single-pass, idempotent)."""
    return _RE.sub(lambda m: _RMAP[m.group(0)], text)


# ── Filesystem operations ─────────────────────────────────────────────


def rename_skills(base: Path) -> None:
    """Rename skill directories: skills/X -> skills/X-manifest-dev."""
    skills_dir = base / "skills"
    if not skills_dir.is_dir():
        return
    for name in SKILLS:
        src = skills_dir / name
        dst = skills_dir / f"{name}{SUFFIX}"
        if src.is_dir() and not dst.exists():
            src.rename(dst)


def rename_agents(base: Path, ext: str = ".md") -> None:
    """Rename agent files: agents/X.ext -> agents/X-manifest-dev.ext."""
    agents_dir = base / "agents"
    if not agents_dir.is_dir():
        return
    for name in AGENTS:
        src = agents_dir / f"{name}{ext}"
        dst = agents_dir / f"{name}{SUFFIX}{ext}"
        if src.is_file() and not dst.exists():
            src.rename(dst)


def rename_commands(base: Path) -> None:
    """Rename command files (OpenCode): commands/X.md -> commands/X-manifest-dev.md."""
    cmds_dir = base / "commands"
    if not cmds_dir.is_dir():
        return
    for name in SKILLS:
        src = cmds_dir / f"{name}.md"
        dst = cmds_dir / f"{name}{SUFFIX}.md"
        if src.is_file() and not dst.exists():
            src.rename(dst)


def patch_skill_frontmatter(base: Path) -> None:
    """Ensure SKILL.md name: field matches the suffixed directory name."""
    skills_dir = base / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        # Find frontmatter boundary (second ---)
        end_idx = content.index("---", 3)
        frontmatter = content[:end_idx]
        rest = content[end_idx:]

        def _fix_name(m: re.Match[str]) -> str:
            prefix, old_name = m.group(1), m.group(2)
            if old_name.endswith(SUFFIX):
                return m.group(0)
            return f"{prefix}{old_name}{SUFFIX}"

        new_fm = re.sub(
            r"^(name:\s*)(\S+)",
            _fix_name,
            frontmatter,
            count=1,
            flags=re.MULTILINE,
        )
        if new_fm != frontmatter:
            skill_md.write_text(new_fm + rest, encoding="utf-8")


def patch_files(base: Path) -> None:
    """Walk all text files under base and apply content replacements."""
    for root, _dirs, files in os.walk(base):
        for fname in files:
            if fname in SKIP_FILES:
                continue
            fpath = Path(root) / fname
            if fpath.suffix not in TEXT_EXTENSIONS:
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            patched = patch_content(content)
            if patched != content:
                fpath.write_text(patched, encoding="utf-8")


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _load_state(state_path: str | None) -> dict[str, object]:
    if not state_path:
        return {}
    path = Path(state_path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_state(state_path: str | None, state: dict[str, object]) -> None:
    if not state_path:
        return
    Path(state_path).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _build_settings_state(
    settings: dict[str, object],
    settings_existed: bool,
) -> dict[str, object]:
    experimental = settings.get("experimental")
    enable_agents_present = False
    enable_agents_value: object | None = None
    if isinstance(experimental, dict) and "enableAgents" in experimental:
        enable_agents_present = True
        enable_agents_value = experimental.get("enableAgents")

    return {
        "version": STATE_VERSION,
        "settings_existed": settings_existed,
        "original_experimental": dict(experimental) if isinstance(experimental, dict) else None,
        "experimental": {
            "enableAgents": {
                "present": enable_agents_present,
                "value": enable_agents_value,
            }
        },
        "hooks_added": {},
    }


def _normalize_state(
    settings: dict[str, object],
    state: dict[str, object],
    settings_existed: bool,
) -> dict[str, object]:
    if not (
        isinstance(state.get("experimental"), dict)
        and "original_experimental" in state
        and isinstance(state.get("hooks_added"), dict)
    ):
        return _build_settings_state(settings, settings_existed)

    return {
        "version": STATE_VERSION,
        "settings_existed": bool(state.get("settings_existed", settings_existed)),
        "original_experimental": state.get("original_experimental"),
        "experimental": dict(state["experimental"]),
        "hooks_added": dict(state["hooks_added"]),
    }


def _collect_hook_names(entries: list[object]) -> set[str]:
    names: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue
        for hook in hooks:
            if isinstance(hook, dict):
                name = hook.get("name")
                if isinstance(name, str):
                    names.add(name)
    return names


def _entry_contains_named_hook(entry: object, names: set[str]) -> bool:
    if not isinstance(entry, dict):
        return False
    hooks = entry.get("hooks")
    if not isinstance(hooks, list):
        return False
    for hook in hooks:
        if isinstance(hook, dict) and hook.get("name") in names:
            return True
    return False


def merge_settings(
    source_hooks_path: str,
    dest_settings_path: str,
    state_path: str | None = None,
) -> None:
    """Merge manifest-dev's Gemini settings requirements additively."""
    source_data = json.loads(Path(source_hooks_path).read_text(encoding="utf-8"))

    dest_path = Path(dest_settings_path)
    settings_existed = dest_path.exists()
    if settings_existed:
        settings = json.loads(dest_path.read_text(encoding="utf-8"))
    else:
        settings = {}
    state = _normalize_state(settings, _load_state(state_path), settings_existed)

    experimental = settings.setdefault("experimental", {})
    if not isinstance(experimental, dict):
        raise ValueError("'experimental' must be an object when present")
    experimental["enableAgents"] = True

    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("'hooks' must be an object when present")

    source_hooks = source_data.get("hooks", {})
    if not isinstance(source_hooks, dict):
        raise ValueError("Source hooks.json must contain a top-level 'hooks' object")

    hooks_added = state.setdefault("hooks_added", {})
    if not isinstance(hooks_added, dict):
        raise ValueError("State hooks_added must be an object when present")

    for event_name, event_entries in source_hooks.items():
        if not isinstance(event_entries, list):
            raise ValueError(f"hooks.{event_name} must be a list")

        existing_entries = hooks.setdefault(event_name, [])
        if not isinstance(existing_entries, list):
            raise ValueError(f"settings.hooks.{event_name} must be a list when present")

        seen = {_canonical_json(entry) for entry in existing_entries}
        recorded = hooks_added.setdefault(event_name, [])
        if not isinstance(recorded, list):
            raise ValueError(f"State hooks_added.{event_name} must be a list when present")
        recorded_seen = {_canonical_json(entry) for entry in recorded}
        for entry in event_entries:
            marker = _canonical_json(entry)
            if marker not in seen:
                existing_entries.append(entry)
                seen.add(marker)
                if marker not in recorded_seen:
                    recorded.append(entry)
                    recorded_seen.add(marker)

    dest_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    _write_state(state_path, state)


def unmerge_settings(
    source_hooks_path: str,
    dest_settings_path: str,
    state_path: str | None = None,
) -> None:
    """Remove manifest-dev's Gemini settings requirements additively."""
    dest_path = Path(dest_settings_path)
    if not dest_path.exists():
        return

    source_data = json.loads(Path(source_hooks_path).read_text(encoding="utf-8"))
    settings = json.loads(dest_path.read_text(encoding="utf-8"))
    state = _normalize_state(settings, _load_state(state_path), dest_path.exists())

    hooks = settings.get("hooks")
    if isinstance(hooks, dict):
        removal_hooks = state.get("hooks_added", source_data.get("hooks", {}))
        if isinstance(removal_hooks, dict):
            for event_name, entries in removal_hooks.items():
                existing_entries = hooks.get(event_name)
                if not isinstance(existing_entries, list):
                    continue
                if not isinstance(entries, list):
                    continue

                removal_markers = {_canonical_json(entry) for entry in entries}
                removal_names = _collect_hook_names(entries) & MANAGED_HOOK_NAMES
                filtered = [
                    entry
                    for entry in existing_entries
                    if _canonical_json(entry) not in removal_markers
                    and not _entry_contains_named_hook(entry, removal_names)
                ]
                if filtered:
                    hooks[event_name] = filtered
                else:
                    hooks.pop(event_name, None)

        if not hooks:
            settings.pop("hooks", None)

    experimental = settings.get("experimental")
    if isinstance(experimental, dict):
        exp_state = state.get("experimental", {})
        enable_agents_state = None
        if isinstance(exp_state, dict):
            enable_agents_state = exp_state.get("enableAgents")
        original_experimental = state.get("original_experimental")

        if isinstance(enable_agents_state, dict):
            present = bool(enable_agents_state.get("present"))
            previous_value = enable_agents_state.get("value")
            current_value = experimental.get("enableAgents")
            current_without_enable = dict(experimental)
            current_without_enable.pop("enableAgents", None)

            if not present:
                if current_value is True and (
                    (original_experimental is None and not current_without_enable)
                    or current_without_enable == original_experimental
                ):
                    experimental.pop("enableAgents", None)
            elif "enableAgents" not in experimental:
                experimental["enableAgents"] = previous_value
            else:
                experimental["enableAgents"] = previous_value

        if not experimental:
            settings.pop("experimental", None)

    if settings:
        dest_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    elif not state.get("settings_existed", True):
        dest_path.unlink()
    else:
        dest_path.write_text("{}\n", encoding="utf-8")

    if state_path:
        state_file = Path(state_path)
        if state_file.exists():
            state_file.unlink()


# ── Codex config merge (TOML) ───────────────────────────────────────


def merge_config(
    source_config_path: str,
    dest_config_path: str,
    state_path: str | None = None,
) -> None:
    """Merge manifest-dev's Codex config sections into an existing config.toml."""
    source_path = Path(source_config_path)
    dest_path = Path(dest_config_path)

    source_text = source_path.read_text(encoding="utf-8")

    if dest_path.exists():
        dest_text = dest_path.read_text(encoding="utf-8")
    else:
        dest_text = ""

    # Simple TOML merge: append sections that don't exist yet
    # Check for manifest-dev marker sections
    marker = "# manifest-dev configuration"
    if marker in dest_text:
        # Already merged — replace the manifest-dev block
        # Find start of manifest-dev section and replace to end or next non-manifest section
        lines = dest_text.split("\n")
        new_lines: list[str] = []
        in_manifest_block = False
        for line in lines:
            if marker in line:
                in_manifest_block = True
                continue
            if in_manifest_block:
                # Skip until we find a line that's clearly not ours
                # (non-empty, non-comment, not starting with known manifest-dev keys)
                continue
            new_lines.append(line)
        dest_text = "\n".join(new_lines).strip()

    if dest_text and not dest_text.endswith("\n"):
        dest_text += "\n"

    merged = dest_text + "\n" + source_text if dest_text.strip() else source_text
    dest_path.write_text(merged, encoding="utf-8")

    if state_path:
        _write_state(state_path, {"version": STATE_VERSION, "merged": True})


def unmerge_config(
    dest_config_path: str,
    state_path: str | None = None,
) -> None:
    """Remove manifest-dev sections from Codex config.toml."""
    dest_path = Path(dest_config_path)
    if not dest_path.exists():
        return

    text = dest_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    new_lines: list[str] = []
    skip_section = False

    for line in lines:
        # Detect manifest-dev sections
        if line.strip().startswith("[agents.") and any(
            agent in line for agent in [
                "criteria-checker", "code-bugs-reviewer", "code-design-reviewer",
                "code-simplicity-reviewer", "code-maintainability-reviewer",
                "code-coverage-reviewer", "code-testability-reviewer",
                "type-safety-reviewer", "docs-reviewer",
                "context-file-adherence-reviewer", "manifest-verifier",
                "define-session-analyzer",
            ]
        ):
            skip_section = True
            continue
        if skip_section:
            if line.strip().startswith("[") and not line.strip().startswith("[agents."):
                skip_section = False
            elif line.strip().startswith("[agents."):
                # Another agent section — check if it's ours
                if not any(agent in line for agent in [
                    "criteria-checker", "code-bugs-reviewer", "code-design-reviewer",
                    "code-simplicity-reviewer", "code-maintainability-reviewer",
                    "code-coverage-reviewer", "code-testability-reviewer",
                    "type-safety-reviewer", "docs-reviewer",
                    "context-file-adherence-reviewer", "manifest-verifier",
                    "define-session-analyzer",
                ]):
                    skip_section = False
                else:
                    continue
            else:
                continue

        # Remove manifest-dev specific top-level settings
        if "# manifest-dev configuration" in line:
            skip_section = True
            continue
        if line.strip() == "project_doc_fallback_filenames" and "CLAUDE.md" in line:
            continue

        new_lines.append(line)

    result = "\n".join(new_lines).strip()
    if result:
        dest_path.write_text(result + "\n", encoding="utf-8")
    else:
        dest_path.write_text("{}\n", encoding="utf-8")

    if state_path:
        state_file = Path(state_path)
        if state_file.exists():
            state_file.unlink()


# ── Main entry point ──────────────────────────────────────────────────


def namespace(base_dir: str, cli_type: str = "gemini") -> None:
    """Rename and patch all components in base_dir."""
    base = Path(base_dir)

    # 1. Rename files and directories
    rename_skills(base)
    rename_agents(base, ".toml" if cli_type == "codex" else ".md")
    if cli_type == "opencode":
        rename_commands(base)

    # 2. Patch SKILL.md name: frontmatter
    patch_skill_frontmatter(base)

    # 3. Patch content cross-references in all text files
    patch_files(base)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "namespace":
        namespace(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "gemini")
    elif len(sys.argv) == 4 and sys.argv[1] == "merge-settings":
        merge_settings(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1] == "merge-settings":
        merge_settings(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 4 and sys.argv[1] == "unmerge-settings":
        unmerge_settings(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1] == "unmerge-settings":
        unmerge_settings(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 4 and sys.argv[1] == "merge-config":
        merge_config(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1] == "merge-config":
        merge_config(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 3 and sys.argv[1] == "unmerge-config":
        unmerge_config(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "unmerge-config":
        unmerge_config(sys.argv[2], sys.argv[3])
    else:
        print(
            f"Usage: {sys.argv[0]} namespace <dir> [codex|gemini|opencode]\n"
            f"       {sys.argv[0]} merge-settings <source-hooks> <dest-settings> [state-file]\n"
            f"       {sys.argv[0]} unmerge-settings <source-hooks> <dest-settings> [state-file]\n"
            f"       {sys.argv[0]} merge-config <source-config> <dest-config> [state-file]\n"
            f"       {sys.argv[0]} unmerge-config <dest-config> [state-file]",
            file=sys.stderr,
        )
        sys.exit(1)
