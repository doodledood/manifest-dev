#!/usr/bin/env python3
"""
Namespace manifest-dev components with -manifest-dev suffix at install time.

Renames files/directories and patches cross-references so components don't
collide with other plugins in shared directories (skills/, agents/, etc.).

Single-pass regex ensures correct handling of overlapping names (e.g., /do
vs /done) and idempotency (won't double-suffix on re-run).

Usage:
    python3 install_helpers.py namespace <dir> [codex|gemini|opencode]
    python3 install_helpers.py merge-config <source-config> <dest-config>
"""

from __future__ import annotations

import json
import os
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

MANAGED_CONFIG_START = "# >>> manifest-dev managed config >>>"
MANAGED_CONFIG_END = "# <<< manifest-dev managed config <<<"
MANAGED_STATE_PREFIX = "# manifest-dev-shared-state: "
CONFIG_HEADER = (
    "# manifest-dev configuration for Codex CLI\n"
    "# Merge relevant sections into your .codex/config.toml\n"
)
STATE_VERSION = 2
DEFAULT_SHARED_VALUES = {
    "features.multi_agent": "true",
    "agents.max_threads": "6",
    "agents.max_depth": "1",
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


def _extract_managed_agent_tables(source_text: str) -> str:
    matches = list(re.finditer(r"(?m)^\[agents\.[^\]]+\]\s*$", source_text))
    if not matches:
        raise ValueError("No [agents.<name>] tables found in source config.")
    return source_text[matches[0].start() :].strip() + "\n"


def _table_pattern(table_name: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^(\[{re.escape(table_name)}\]\n)(.*?)(?=^\[|\Z)")


def _table_match(text: str, table_name: str) -> re.Match[str] | None:
    return _table_pattern(table_name).search(text)


def _get_table_body(text: str, table_name: str) -> str | None:
    match = _table_match(text, table_name)
    if not match:
        return None
    return match.group(2)


def _get_table_key_value(text: str, table_name: str, key: str) -> str | None:
    body = _get_table_body(text, table_name)
    if body is None:
        return None
    match = re.search(rf"(?m)^{re.escape(key)}\s*=\s*(.*)$", body)
    if not match:
        return None
    return match.group(1).strip()


def _table_list_contains_value(text: str, table_name: str, key: str, value: str) -> bool:
    current_value = _get_table_key_value(text, table_name, key)
    if current_value is None:
        return False
    return f'"{value}"' in current_value


def _parse_quoted_list(raw_value: str | None) -> list[str] | None:
    if raw_value is None:
        return None
    return re.findall(r'"([^"]*)"', raw_value)


def _strip_managed_config_block(text: str) -> str:
    pattern = re.compile(
        rf"\n?{re.escape(MANAGED_CONFIG_START)}\n.*?\n{re.escape(MANAGED_CONFIG_END)}\n?",
        flags=re.DOTALL,
    )
    return pattern.sub("\n", text)


def _extract_embedded_state(text: str) -> dict[str, object]:
    match = re.search(
        rf"{re.escape(MANAGED_CONFIG_START)}\n{re.escape(MANAGED_STATE_PREFIX)}(.*?)\n",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return {}
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def _strip_manifest_agent_tables(text: str) -> str:
    names = "|".join(re.escape(f"{name}{SUFFIX}") for name in AGENTS)
    pattern = re.compile(
        rf"(?ms)^\[agents\.(?:{names})\]\n.*?(?=^\[|\Z)",
    )
    return pattern.sub("", text)


def _strip_manifest_header(text: str) -> str:
    if text.startswith(CONFIG_HEADER):
        text = text[len(CONFIG_HEADER) :]
    return text


def _upsert_key_in_table_body(body: str, key: str, value: str) -> str:
    line = f"{key} = {value}"
    pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    if pattern.search(body):
        return pattern.sub(line, body, count=1)

    if body and not body.endswith("\n"):
        body += "\n"
    return body + line + "\n"


def _has_key_in_table_body(body: str, key: str) -> bool:
    pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    return pattern.search(body) is not None


def _ensure_missing_table_keys(
    text: str,
    table_name: str,
    keys: list[tuple[str, str]],
) -> str:
    match = _table_match(text, table_name)
    if match:
        body = match.group(2)
        for key, value in keys:
            if not _has_key_in_table_body(body, key):
                body = _upsert_key_in_table_body(body, key, value)
        return text[: match.start()] + match.group(1) + body + text[match.end() :]

    if text and not text.endswith("\n"):
        text += "\n"
    if text.strip():
        text += "\n"
    lines = [f"[{table_name}]"] + [f"{key} = {value}" for key, value in keys]
    return text + "\n".join(lines) + "\n"


def _ensure_list_value_in_table(
    text: str,
    table_name: str,
    key: str,
    value: str,
) -> str:
    match = _table_match(text, table_name)
    list_value = f'["{value}"]'
    if not match:
        return _ensure_missing_table_keys(text, table_name, [(key, list_value)])

    header, body = match.group(1), match.group(2)
    key_pattern = re.compile(rf"(?m)^({re.escape(key)}\s*=\s*)(\[.*\])$")
    key_match = key_pattern.search(body)
    if not key_match:
        body = _upsert_key_in_table_body(body, key, list_value)
        return text[: match.start()] + header + body + text[match.end() :]

    existing_list = key_match.group(2)
    if f'"{value}"' in existing_list:
        return text

    inner = existing_list[1:-1].strip()
    merged_list = f'[{inner}, "{value}"]' if inner else list_value
    body = key_pattern.sub(rf"\1{merged_list}", body, count=1)
    return text[: match.start()] + header + body + text[match.end() :]


def _ensure_table_keys(
    text: str,
    table_name: str,
    keys: list[tuple[str, str]],
) -> str:
    match = _table_match(text, table_name)
    if match:
        body = match.group(2)
        for key, value in keys:
            body = _upsert_key_in_table_body(body, key, value)
        return text[: match.start()] + match.group(1) + body + text[match.end() :]

    if text and not text.endswith("\n"):
        text += "\n"
    if text.strip():
        text += "\n"
    lines = [f"[{table_name}]"] + [f"{key} = {value}" for key, value in keys]
    return text + "\n".join(lines) + "\n"


def _remove_key_from_table(
    text: str,
    table_name: str,
    key: str,
    expected_value: str | None = None,
) -> str:
    match = _table_match(text, table_name)
    if not match:
        return text

    header, body = match.group(1), match.group(2)
    key_pattern = re.compile(rf"(?m)^({re.escape(key)}\s*=\s*)(.*)$")
    key_match = key_pattern.search(body)
    if not key_match:
        return text

    current_value = key_match.group(2).strip()
    if expected_value is not None and current_value != expected_value:
        return text

    body = key_pattern.sub("", body, count=1)
    body = re.sub(r"\n{3,}", "\n\n", body).lstrip("\n")
    return text[: match.start()] + header + body + text[match.end() :]


def _remove_list_value_from_table(text: str, table_name: str, key: str, value: str) -> str:
    match = _table_match(text, table_name)
    if not match:
        return text

    header, body = match.group(1), match.group(2)
    key_pattern = re.compile(rf"(?m)^({re.escape(key)}\s*=\s*)(\[.*\])$")
    key_match = key_pattern.search(body)
    if not key_match:
        return text

    items = re.findall(r'"([^"]*)"', key_match.group(2))
    if value not in items:
        return text

    items = [item for item in items if item != value]
    if items:
        rendered = "[" + ", ".join(f'"{item}"' for item in items) + "]"
        body = key_pattern.sub(rf"\1{rendered}", body, count=1)
    else:
        body = key_pattern.sub("", body, count=1)

    body = re.sub(r"\n{3,}", "\n\n", body).lstrip("\n")
    return text[: match.start()] + header + body + text[match.end() :]


def _remove_empty_table(text: str, table_name: str) -> str:
    match = _table_match(text, table_name)
    if not match:
        return text
    if match.group(2).strip():
        return text
    return text[: match.start()] + text[match.end() :]


def _normalize_config_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.lstrip("\n").rstrip()
    if not text:
        return ""
    return text + "\n"


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


def _build_config_state(existing_text: str, config_existed: bool) -> dict[str, object]:
    return {
        "version": STATE_VERSION,
        "config_existed": config_existed,
        "original_keys": {
            "features.multi_agent": _get_table_key_value(existing_text, "features", "multi_agent"),
            "agents.max_threads": _get_table_key_value(existing_text, "agents", "max_threads"),
            "agents.max_depth": _get_table_key_value(existing_text, "agents", "max_depth"),
        },
        "original_lists": {
            "agents.project_doc_fallback_filenames": _parse_quoted_list(
                _get_table_key_value(
                    existing_text,
                    "agents",
                    "project_doc_fallback_filenames",
                )
            ),
        },
    }


def _normalize_state(existing_text: str, state: dict[str, object], config_existed: bool) -> dict[str, object]:
    if isinstance(state.get("original_keys"), dict) and isinstance(state.get("original_lists"), dict):
        return {
            "version": STATE_VERSION,
            "config_existed": bool(state.get("config_existed", config_existed)),
            "original_keys": state["original_keys"],
            "original_lists": state["original_lists"],
        }

    added_keys = state.get("added_keys", {})
    added_lists = state.get("added_list_values", {})
    if not isinstance(added_keys, dict) or not isinstance(added_lists, dict):
        return _build_config_state(existing_text, config_existed)

    normalized = _build_config_state(existing_text, config_existed)
    original_keys = normalized.get("original_keys", {})
    if isinstance(original_keys, dict):
        for key in DEFAULT_SHARED_VALUES:
            if added_keys.get(key):
                original_keys[key] = None

    current_list = _parse_quoted_list(
        _get_table_key_value(existing_text, "agents", "project_doc_fallback_filenames")
    )
    original_lists = normalized.get("original_lists", {})
    if isinstance(original_lists, dict):
        if isinstance(current_list, list) and "CLAUDE.md" in current_list and "CLAUDE.md" in added_lists.get("agents.project_doc_fallback_filenames", []):
            original_lists["agents.project_doc_fallback_filenames"] = [
                item for item in current_list if item != "CLAUDE.md"
            ]
        else:
            original_lists["agents.project_doc_fallback_filenames"] = current_list

    normalized["config_existed"] = bool(state.get("config_existed", config_existed))
    return normalized


def merge_config(
    source_config_path: str,
    dest_config_path: str,
    state_path: str | None = None,
) -> None:
    source_text = Path(source_config_path).read_text(encoding="utf-8")
    managed_tables = _extract_managed_agent_tables(source_text).rstrip()

    dest_path = Path(dest_config_path)
    config_existed = dest_path.exists()
    existing_text = dest_path.read_text(encoding="utf-8") if config_existed else ""
    merged_text = existing_text if config_existed else CONFIG_HEADER
    state = _normalize_state(existing_text, _load_state(state_path), config_existed)
    managed_block = (
        f"{MANAGED_CONFIG_START}\n"
        f"{MANAGED_STATE_PREFIX}{json.dumps(state, sort_keys=True)}\n"
        f"{managed_tables}\n"
        f"{MANAGED_CONFIG_END}\n"
    )

    merged_text = _strip_managed_config_block(merged_text)
    merged_text = _strip_manifest_agent_tables(merged_text)
    merged_text = _ensure_missing_table_keys(
        merged_text,
        "features",
        [("multi_agent", "true")],
    )
    merged_text = _ensure_missing_table_keys(
        merged_text,
        "agents",
        [
            ("max_threads", "6"),
            ("max_depth", "1"),
        ],
    )
    merged_text = _ensure_list_value_in_table(
        merged_text,
        "agents",
        "project_doc_fallback_filenames",
        "CLAUDE.md",
    )

    merged_text = merged_text.rstrip() + "\n\n" + managed_block
    dest_path.write_text(merged_text, encoding="utf-8")
    _write_state(state_path, state)


def unmerge_config(dest_config_path: str, state_path: str | None = None) -> None:
    dest_path = Path(dest_config_path)
    if not dest_path.exists():
        return

    current_text = dest_path.read_text(encoding="utf-8")
    loaded_state = _load_state(state_path)
    if not loaded_state:
        loaded_state = _extract_embedded_state(current_text)
    state = _normalize_state(current_text, loaded_state, dest_path.exists())

    merged_text = _strip_managed_config_block(current_text)
    merged_text = _strip_manifest_agent_tables(merged_text)

    original_keys = state.get("original_keys", {})
    if not isinstance(original_keys, dict):
        original_keys = {}
    for dotted_key, default_value in DEFAULT_SHARED_VALUES.items():
        table_name, key = dotted_key.split(".", 1)
        current_value = _get_table_key_value(merged_text, table_name, key)
        if original_keys.get(dotted_key) is None and current_value == default_value:
            merged_text = _remove_key_from_table(
                merged_text,
                table_name,
                key,
                default_value,
            )

    original_lists = state.get("original_lists", {})
    if not isinstance(original_lists, dict):
        original_lists = {}
    current_list = _parse_quoted_list(
        _get_table_key_value(
            merged_text,
            "agents",
            "project_doc_fallback_filenames",
        )
    )
    original_list = original_lists.get("agents.project_doc_fallback_filenames")
    if isinstance(current_list, list) and "CLAUDE.md" in current_list:
        if original_list is None:
            if current_list == ["CLAUDE.md"]:
                merged_text = _remove_list_value_from_table(
                    merged_text,
                    "agents",
                    "project_doc_fallback_filenames",
                    "CLAUDE.md",
                )
        elif isinstance(original_list, list):
            if [item for item in current_list if item != "CLAUDE.md"] == original_list:
                merged_text = _remove_list_value_from_table(
                    merged_text,
                    "agents",
                    "project_doc_fallback_filenames",
                    "CLAUDE.md",
                )

    merged_text = _remove_empty_table(merged_text, "features")
    merged_text = _remove_empty_table(merged_text, "agents")
    merged_text = _strip_manifest_header(merged_text)
    merged_text = _normalize_config_text(merged_text)

    if merged_text:
        dest_path.write_text(merged_text, encoding="utf-8")
    else:
        dest_path.unlink()

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
            (
                f"Usage: {sys.argv[0]} namespace <dir> [codex|gemini|opencode]\n"
                f"   or: {sys.argv[0]} merge-config <source-config> <dest-config> [state-file]\n"
                f"   or: {sys.argv[0]} unmerge-config <dest-config> [state-file]"
            ),
            file=sys.stderr,
        )
        sys.exit(1)
