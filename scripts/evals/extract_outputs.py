#!/usr/bin/env python3
"""Write each run's judged output and grades to files an analyzer can read.

An eval run keeps, per run, the artifact its file-focused graders judged (the
``evidence`` field) but no transcript once the container exits. This writes, for the
``with`` arm of the chosen cases, ``<case>_rep<k>.md`` (the artifact) and
``<case>_rep<k>.grades.json`` (pass or fail per scored grader) into ``--out``.

    python3 scripts/evals/extract_outputs.py <aggregate-result.json> --out DIR \\
        --cases d01-layer-cut d02-outcome-not-mechanism

Pass only train cases: what the analyzer reads must never include held-out cases. When
the JSON has had its evidence stripped, give ``--report`` the run's ``report.html``,
which still embeds it; the extractor then checks that each recovered run's grades match
the JSON and skips a case where they don't, rather than mislabel its artifacts.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


def evidence_from_json(run: dict[str, Any]) -> str | None:
    for grader in run["graders"]:
        if grader.get("evidence"):
            return str(grader["evidence"])
    return None


def runs_from_report(report: str, case: dict[str, Any]) -> list[tuple[str, str]] | None:
    """(evidence, block) per run of ``case``, in report order, or None if absent."""
    sections = re.split(r"<h2[^>]*>([^<]+)</h2>", report)
    names = sections[1::2]
    if case["name"] not in names:
        return None
    body = sections[2 + 2 * names.index(case["name"])]
    first = re.escape(case["graders"][0]["name"])
    starts = rf'(?=<summary><span class="chip[^"]*">[^<]*</span> <span class="grader-name">{first}</span>)'
    out = []
    for block in re.split(starts, body)[1:]:
        found = re.search(r'<pre class="evidence">(.*?)</pre>', block, re.S)
        out.append((html.unescape(found.group(1)) if found else "", block))
    return out


def report_grades_match(block: str, run: dict[str, Any]) -> bool:
    shown = re.findall(
        r'chip-(pass|fail)[^<]*</span> <span class="grader-name">([^<]+)', block
    )
    expected = {g["name"]: "pass" if g["passed"] else "fail" for g in run["graders"]}
    return bool(shown) and all(expected.get(name) == verdict for verdict, name in shown)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("result", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cases", nargs="+", required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)

    data = json.loads(args.result.read_text())
    report = args.report.read_text() if args.report else None
    args.out.mkdir(parents=True, exist_ok=True)
    by_name = {c["name"]: c for c in data["cases"]}
    status = 0
    for name in args.cases:
        case = by_name.get(name)
        if case is None:
            print(f"{name}: not in {args.result}", file=sys.stderr)
            status = 1
            continue
        runs = case["arms"]["with"]
        texts: list[str | None] = [evidence_from_json(r) for r in runs]
        if any(t is None for t in texts) and report is not None:
            recovered = runs_from_report(report, case) or []
            if len(recovered) < len(runs) or not all(
                report_grades_match(block, run)
                for (_, block), run in zip(recovered, runs, strict=False)
            ):
                print(
                    f"{name}: report runs don't line up with the JSON; skipped",
                    file=sys.stderr,
                )
                status = 1
                continue
            texts = [text for text, _ in recovered[: len(runs)]]
        for k, (run, text) in enumerate(zip(runs, texts, strict=True)):
            grades = {g["name"]: g["passed"] for g in run["graders"] if g["scored"]}
            (args.out / f"{name}_rep{k}.grades.json").write_text(
                json.dumps(grades, indent=1)
            )
            if text:
                (args.out / f"{name}_rep{k}.md").write_text(text)
        print(f"{name}: {len(runs)} runs")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
