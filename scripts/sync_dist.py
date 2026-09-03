#!/usr/bin/env python3
"""Regenerate the Codex distribution's skill payload from the plugin source, or check it.

Codex installs a plugin into its own cache, so its plugin directories must be
self-contained: ``dist/codex/plugins/<plugin>/skills`` is a byte-identical copy of
``claude-plugins/<plugin>/skills``. OpenCode and Pi read the source tree directly and
need no copy. Everything else under ``dist/`` (plugin manifests, the OpenCode plugin
entry, the Pi prompt aliases, the READMEs) is hand-maintained.

    python3 scripts/sync_dist.py          # regenerate the copies
    python3 scripts/sync_dist.py --check  # exit 1 if any copy differs from its source
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ("manifest-dev", "manifest-dev-tools")


def source_dir(plugin: str) -> Path:
    return ROOT / "claude-plugins" / plugin / "skills"


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


def check() -> int:
    drift = [
        d
        for plugin in PLUGINS
        for d in differences(source_dir(plugin), target_dir(plugin))
    ]
    if drift:
        print("dist/codex is out of date; run scripts/sync_dist.py:", file=sys.stderr)
        for line in drift:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("dist/codex matches source")
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
