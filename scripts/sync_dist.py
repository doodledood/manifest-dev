#!/usr/bin/env python3
"""Regenerate the Codex distribution's skill payload from the plugin source, or check it.

Codex installs a plugin into its own cache, so its plugin directories must be
self-contained: ``dist/codex/plugins/<plugin>/skills`` is a byte-identical copy of
``claude-plugins/<plugin>/skills``. OpenCode and Pi read the source tree directly and
need no copy. Everything else under ``dist/`` (plugin manifests, the OpenCode plugin
entry, the Pi prompt aliases, the READMEs) is hand-maintained.

It also copies the verification tool setup-project ships (``references/harness/verify`` and
``verify.mts``) to this repository's ``scripts/`` and into the eval scaffolds that seed a
harness, so one edit to the shipped tool reaches every copy.

    python3 scripts/sync_dist.py          # regenerate the copies
    python3 scripts/sync_dist.py --check  # exit 1 if any copy differs from its source
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ("manifest-dev", "manifest-dev-tools")


def source_dir(plugin: str) -> Path:
    return ROOT / "claude-plugins" / plugin / "skills"


HARNESS = ROOT / "claude-plugins/manifest-dev/skills/setup-project/references/harness"
TOOL_FILES = ("verify", "verify.mts")
EVALS = ROOT / "claude-plugins/manifest-dev/evals"
EMBEDDED = re.compile(
    r"(cat > scripts/(verify(?:\.mts)?) <<'VERIFY_TOOL_EOF'\n)(.*?\n)(VERIFY_TOOL_EOF\n)",
    re.S,
)


def tool_copies() -> dict[Path, str]:
    """Each file that must carry the shipped tool, with the text it must hold."""
    tool = {name: (HARNESS / name).read_text(encoding="utf-8") for name in TOOL_FILES}
    wanted = {ROOT / "scripts" / name: text for name, text in tool.items()}
    for scaffold in sorted(EVALS.rglob("scaffold.sh")):
        text = scaffold.read_text(encoding="utf-8")
        if "VERIFY_TOOL_EOF" in text:
            wanted[scaffold] = EMBEDDED.sub(
                lambda m: m.group(1) + tool[m.group(2)] + m.group(4), text
            )
    return wanted


def target_dir(plugin: str) -> Path:
    return ROOT / "dist" / "codex" / "plugins" / plugin / "skills"


def differences(src: Path, dst: Path) -> list[str]:
    """Every path at which ``dst`` is not a byte-identical mirror of ``src``."""
    if not dst.exists():
        return [f"{dst}: missing"]
    found: list[str] = []

    def walk(cmp: filecmp.dircmp, rel: Path) -> None:
        for name in cmp.left_only:
            found.append(f"{rel / name}: only in source")
        for name in cmp.right_only:
            found.append(f"{rel / name}: only in copy")
        for name in cmp.diff_files + cmp.funny_files:
            found.append(f"{rel / name}: differs")
        for name, sub in cmp.subdirs.items():
            walk(sub, rel / name)

    walk(filecmp.dircmp(src, dst, ignore=[]), Path(dst.name))
    return found


def regenerate() -> None:
    for plugin in PLUGINS:
        src, dst = source_dir(plugin), target_dir(plugin)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=False)
        print(f"copied {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    for path, text in tool_copies().items():
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            print(f"copied the shipped verify tool into {path.relative_to(ROOT)}")


def check() -> int:
    drift = [
        d
        for plugin in PLUGINS
        for d in differences(source_dir(plugin), target_dir(plugin))
    ] + [
        f"{path.relative_to(ROOT)}: differs from the shipped verify tool"
        for path, text in tool_copies().items()
        if path.read_text(encoding="utf-8") != text
    ]
    if drift:
        print("copies are out of date; run scripts/sync_dist.py:", file=sys.stderr)
        for line in drift:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("dist/codex and the tool copies match source")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--check", action="store_true", help="report drift instead of regenerating"
    )
    args = parser.parse_args(argv)
    if args.check:
        return check()
    regenerate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
