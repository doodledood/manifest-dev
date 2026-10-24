#!/usr/bin/env python3
"""Regenerate exact ceiling checks and request quotations from their source files."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "claude-plugins/manifest-dev/evals/define"
SCHEMA = ROOT / "claude-plugins/manifest-dev/skills/define/references/SCHEMA.md"


def generated() -> dict[Path, str]:
    ceiling = SCHEMA.read_text().split("````markdown\n")[-1].split("\n````")[0]
    pattern = r"\s+".join(re.escape(word) for word in ceiling.split())
    # YAML single quotes are escaped by doubling, independently of regex escaping.
    content = (
        "---\ntype: regex\ntarget:\n  source: file\n  path: manifest.md\n"
        f"pattern: '{pattern.replace(chr(39), chr(39) * 2)}'\narm: with-only\n---\n"
    )
    updates = dict.fromkeys(EVALS.glob("*/graders/ceiling-verbatim.md"), content)
    for name in ("binding-lives-in-gates", "no-invented-thresholds"):
        for path in EVALS.glob(f"*/graders/{name}.md"):
            core = path.read_text().split("\nThe request:\n", 1)[0].rstrip()
            request = (
                (path.parent.parent / "prompt.md")
                .read_text()
                .split("---\n", 2)[2]
                .strip()
            )
            updates[path] = core + "\n\nThe request:\n\n" + request + "\n"
    updates.update(state_graders())
    return updates


# The declared fixtures are the authority for final-state guards. Generating from each
# scaffold avoids snapshots that silently omit a newly added source/test/preferences file.
STATE_CASES = {
    "17-agreement-is-not-a-go": (),
    "18-read-only-experiment": (),
    "25-users-call-and-taste": (),
    "27-taste-offers": (),
    "28-universal-not-taste": (),
    "52-projectless-chat-offers-no-surfaces": (),
    "define/d16-approved-means-handoff": ("manifest.md",),
    "define/d17-taste-in-encoding": ("manifest.md",),
}


def state_graders() -> dict[Path, str]:
    updates = {}
    for name, allowed in STATE_CASES.items():
        case = EVALS.parent / name
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            work, home = scratch / "work", scratch / "home"
            work.mkdir()
            home.mkdir()
            subprocess.run(
                ["bash", str(case / "scaffold.sh")],
                cwd=work,
                env={**os.environ, "HOME": str(home)},
                check=True,
                capture_output=True,
                timeout=120,
            )
            files = sorted(p for p in work.rglob("*") if p.is_file())
            for file in files:
                rel = file.relative_to(work).as_posix()
                if rel in allowed:
                    continue
                # (?![\\s\\S]) is an absolute end; JavaScript $ alone permits a trailing newline.
                pattern = "^" + re.escape(file.read_text()) + r"(?![\s\S])"
                pattern = pattern.replace(chr(92) + chr(10), r"\n")
                text = (
                    "---\ntype: regex\ntarget:\n  source: file\n  path: "
                    + rel
                    + "\npattern: '"
                    + pattern.replace("'", "''")
                    + "'\n---\n"
                )
                dest = (
                    case
                    / "graders"
                    / ("state-" + rel.replace("/", "--").replace(".", "-") + ".md")
                )
                updates[dest] = text
            paths = "|".join(re.escape(p) for p in allowed)
            pattern = (
                rf"^(?:(?:{paths})(?:\n|$))*(?![\s\S])" if paths else r"^(?![\s\S])"
            )
            updates[case / "graders/state-no-extra-files.md"] = (
                "---\ntype: regex\ntarget: files\npattern: '" + pattern + "'\n---\n"
            )
    for name, old, new in (
        (
            "23-term-and-record",
            "20260301-orders-close-on-a-rolling-cutoff",
            "20261024-weekly-cutoff",
        ),
        (
            "84-chosen-option-goes-to-a-record",
            "20260601-new-weavers-pay-no-fee-at-first",
            "20261024-new-weavers-pay-no-fee-for-90-days",
        ),
    ):
        case = EVALS.parent / name
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            subprocess.run(
                ["bash", str(case / "scaffold.sh")],
                cwd=scratch,
                env={**os.environ, "HOME": temp},
                check=True,
                capture_output=True,
                timeout=120,
            )
            original = (scratch / "docs/adr" / (old + ".md")).read_text()
        before, after = original.split("## Status\nAccepted", 1)
        pattern = (
            "^"
            + re.escape(before)
            + r"## Status\s+Superseded by[^\n]*"
            + re.escape(new)
            + r"[^\n]*"
            + re.escape(after)
            + r"(?![\s\S])"
        )
        pattern = pattern.replace(chr(92) + chr(10), r"\n")
        updates[case / "graders/old-record-restatused.md"] = (
            "---\ntype: regex\ntarget:\n  source: file\n  path: docs/adr/"
            + old
            + ".md\npattern: '"
            + pattern.replace("'", "''")
            + "'\n---\n"
        )
    return updates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, text in generated().items():
        if not path.exists() or path.read_text() != text:
            stale.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(text)
    if args.check and stale:
        print("Run python3 scripts/evals/sync_graders.py:\n" + "\n".join(stale))
        return 1
    print(
        f"{len(stale)} generated graders {'need updating' if args.check else 'updated'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
