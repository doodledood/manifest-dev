#!/usr/bin/env python3
"""Compare eval runs per grader, split into train and held-out test cases.

Reads ``claude plugin eval --json`` results (``aggregate-result.json``) and prints
markdown tables: pass counts per grader and split, the mean score per case, and the
cost of each run. A grader that appears in more than one case gets its own row; the
graders unique to one case are pooled as ``case-graders``. Only the ``with`` arm is
scored, so a run made with ``--ablation none`` compares directly to the plugin arm of
a full baseline.

    python3 scripts/evals/score_rounds.py --state <flow>/_state.json \\
        baseline=<path>/aggregate-result.json v1=<flow>/v1/aggregate-result.json

``_state.json`` needs ``train_ids`` and ``test_ids`` (case names). Cases in neither
list are reported under ``other``.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

POOLED = "case-graders"


def load(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(path.read_text())
    if data.get("partial"):
        raise SystemExit(f"{path}: partial run; finish or rerun it before scoring")
    return data


def shared_graders(runs: list[dict[str, Any]]) -> set[str]:
    """Graders that some run carries on more than one case."""
    shared: set[str] = set()
    for data in runs:
        seen = Counter(g["name"] for c in data["cases"] for g in c["graders"])
        shared |= {name for name, n in seen.items() if n > 1}
    return shared


def split_of(case: str, state: dict[str, Any]) -> str:
    if case in state["train_ids"]:
        return "train"
    if case in state["test_ids"]:
        return "test"
    return "other"


def tally(
    data: dict[str, Any], state: dict[str, Any], shared: set[str]
) -> tuple[dict[tuple[str, str], list[int]], dict[str, float], float, int]:
    counts: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    per_case: dict[str, float] = {}
    cost, errors = 0.0, 0
    for case in data["cases"]:
        runs = case["arms"]["with"]
        split = split_of(case["name"], state)
        per_case[case["name"]] = sum(r["score"] for r in runs) / len(runs)
        for run in runs:
            cost += run["costUsd"] + (run.get("judgeCostUsd") or 0)
            errors += bool(run.get("error"))
            for grader in run["graders"]:
                # A with-only grader (`tool_used: Skill`) is a plugin-fired check, not
                # quality; skip it in both ablation modes so rounds stay comparable.
                if not grader["scored"] or grader.get("withOnly"):
                    continue
                key = grader["name"] if grader["name"] in shared else POOLED
                for bucket in ((split, key), ("all", key)):
                    counts[bucket][0] += grader["passed"]
                    counts[bucket][1] += 1
    return counts, per_case, cost, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("runs", nargs="+", help="label=path/to/aggregate-result.json")
    args = parser.parse_args(argv)

    state = json.loads(args.state.read_text())
    labelled = [r.split("=", 1) for r in args.runs]
    datas = {label: load(Path(path)) for label, path in labelled}
    shared = shared_graders(list(datas.values()))
    results = {label: tally(d, state, shared) for label, d in datas.items()}
    labels = list(results)

    print("| grader | split | " + " | ".join(labels) + " |")
    print("|---|---|" + "---|" * len(labels))
    for grader in [*sorted(shared), POOLED]:
        for split in ("train", "test", "other", "all"):
            cells = []
            for label in labels:
                passed, n = results[label][0].get((split, grader), [0, 0])
                cells.append(f"{passed}/{n} ({passed / n:.0%})" if n else "-")
            if any(c != "-" for c in cells):
                print(f"| {grader} | {split} | " + " | ".join(cells) + " |")

    cases = sorted({c for r in results.values() for c in r[1]})
    print("\n| case | split | " + " | ".join(labels) + " |")
    print("|---|---|" + "---|" * len(labels))
    for case in cases:
        cells = [
            f"{results[label][1][case]:.2f}" if case in results[label][1] else "-"
            for label in labels
        ]
        print(f"| {case} | {split_of(case, state)} | " + " | ".join(cells) + " |")

    print()
    for label in labels:
        _, _, cost, errors = results[label]
        print(f"{label}: with-arm cost ${cost:.2f}, errored runs {errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
