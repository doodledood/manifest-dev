#!/usr/bin/env python3
"""
Namespace manifest-dev components with -manifest-dev suffix at install time.

Renames files/directories and patches cross-references so components don't
collide with other plugins in shared directories (skills/, agents/, etc.).

Single-pass regex ensures correct handling of overlapping names (e.g., /do
vs /done) and idempotency (won't double-suffix on re-run).

Usage:
    python3 install_helpers.py namespace <dir> [codex|gemini|opencode]
"""

from __future__ import annotations

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
    if len(sys.argv) < 3 or sys.argv[1] != "namespace":
        print(
            f"Usage: {sys.argv[0]} namespace <dir> [codex|gemini|opencode]",
            file=sys.stderr,
        )
        sys.exit(1)
    namespace(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "gemini")
