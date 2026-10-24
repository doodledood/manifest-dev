#!/usr/bin/env python3
"""Compare eval runs per grader, split into train and held-out test cases.

Reads ``claude plugin eval --json`` results (``aggregate-result.json``) and prints
markdown tables: pass counts per grader and split, the mean score per case, and the
cost of each run. A grader that appears in more than one case gets its own row; the
graders unique to one case are pooled as ``case-graders``. Only the ``with`` arm is
scored, so a run made with ``--ablation none`` compares directly to the plugin arm of
a full baseline.

    python3 scripts/evals/score_rounds.py --state <flow>/_state.json \\
        v0=<flow>/v0 v1=<flow>/v1

Each run is one ``aggregate-result.json`` or a directory whose ``*.json`` results are
merged, for a round run one case per invocation. Each needs the launch-time
``*.instrument.json`` written by run_eval.sh. Every requested case must be present;
the measurement instrument must match across rounds. Repetitions may differ when
each run fulfills its own launch contract. Diagnostics never count as quality.

``_state.json`` needs ``train_ids`` and ``test_ids`` (case names). Cases in neither
list are reported under ``other``.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from eval_contract import InvalidRunError, diagnostic, load_result

POOLED = "case-graders"


def load(path: Path) -> dict[str, Any]:
    """One result file, or every ``*.json`` result in a directory merged into one."""
    paths = (
        sorted(
            p for p in path.glob("*.json") if not p.name.endswith(".instrument.json")
        )
        if path.is_dir()
        else [path]
    )
    if not paths:
        raise SystemExit(f"{path}: no result files")
    cases: list[dict[str, Any]] = []
    contracts: dict[str, Any] = {}
    for each in paths:
        data, contract = load_result(each)
        cases.extend(data["cases"])
        for case in contract["cases"]:
            contracts[case["name"]] = {
                "case": {k: v for k, v in case.items() if k != "runs"},
                **{
                    k: contract[k]
                    for k in (
                        "cliVersion",
                        "judgeModel",
                        "sharedInstrumentHash",
                        "behaviorOptions",
                    )
                },
            }
    names = Counter(c["name"] for c in cases)
    if repeated := sorted(n for n, k in names.items() if k > 1):
        raise SystemExit(
            f"{path}: cases in more than one result: {', '.join(repeated)}"
        )
    return {"cases": cases, "contracts": contracts}


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


def plugin_fired(case: dict[str, Any]) -> set[str]:
    """Graders that check the skill fired rather than output quality.

    Under ``--ablation with-without`` the CLI leaves them out of the score; under
    ``none`` it scores them. Dropping them in both modes keeps rounds comparable.
    """
    return {g["name"] for g in case["graders"] if diagnostic(g)}


def tally(
    data: dict[str, Any],
    state: dict[str, Any],
    shared: set[str],
    cases: set[str],
) -> tuple[dict[tuple[str, str], list[int]], dict[str, float], dict[str, float], int]:
    counts: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    per_case: dict[str, float] = {}
    cost = {"agent": 0.0, "judge": 0.0}
    errors = 0
    for case in data["cases"]:
        if case["name"] not in cases:
            continue
        runs = case["arms"]["with"]
        split = split_of(case["name"], state)
        skip = plugin_fired(case)
        scores = []
        for run in runs:
            # costUsd already includes the judge's share.
            judge = run.get("judgeCostUsd") or 0
            cost["agent"] += run["costUsd"] - judge
            cost["judge"] += judge
            errors += bool(run.get("error"))
            kept = [g for g in run["graders"] if g["name"] not in skip]
            weight = sum(g["weight"] for g in kept)
            if not weight:
                raise InvalidRunError(f"{case['name']}: no quality graders")
            scores.append(sum(g["weight"] * g["passed"] for g in kept) / weight)
            for grader in kept:
                key = grader["name"] if grader["name"] in shared else POOLED
                for bucket in ((split, key), ("all", key)):
                    counts[bucket][0] += grader["passed"]
                    counts[bucket][1] += 1
        per_case[case["name"]] = sum(scores) / len(scores) if scores else float("nan")
    return counts, per_case, cost, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--cases",
        nargs="+",
        help="Explicit subset; default is every train/test case in state",
    )
    parser.add_argument("runs", nargs="+", help="label=path/to/aggregate-result.json")
    args = parser.parse_args(argv)

    state = json.loads(args.state.read_text())
    train, test = state["train_ids"], state["test_ids"]
    if len(set(train + test)) != len(train + test):
        raise InvalidRunError("train/test IDs overlap or repeat")
    labelled = [r.split("=", 1) for r in args.runs]
    if any(len(r) != 2 for r in labelled) or len({r[0] for r in labelled}) != len(
        labelled
    ):
        raise InvalidRunError("runs need distinct label=path arguments")
    datas = {label: load(Path(path)) for label, path in labelled}
    fired = {n for d in datas.values() for c in d["cases"] for n in plugin_fired(c)}
    shared = shared_graders(list(datas.values())) - fired
    carried = [{c["name"] for c in d["cases"]} for d in datas.values()]
    common = set(args.cases if args.cases else train + test)
    if not common or common - set(train + test):
        raise InvalidRunError(
            "requested cases must be a nonempty subset of the frozen train/test split"
        )
    for (label, _data), names in zip(datas.items(), carried, strict=True):
        if missing := common - names:
            raise InvalidRunError(
                f"{label}: missing requested cases: {', '.join(sorted(missing))}"
            )
    reference = next(iter(datas.values()))
    for label, data in datas.items():
        for name in common:
            if data["contracts"][name] != reference["contracts"][name]:
                raise InvalidRunError(
                    f"{label}/{name}: measurement instrument or runtime changed"
                )
    if left_out := sorted(set.union(*carried) - common):
        print(f"Explicit comparison subset; not scored: {', '.join(left_out)}\n")
    results = {label: tally(d, state, shared, common) for label, d in datas.items()}
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
        print(
            f"{label}: with-arm cost ${cost['agent'] + cost['judge']:.2f} "
            f"(agent ${cost['agent']:.2f}, judge ${cost['judge']:.2f}), "
            f"errored runs {errors}"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InvalidRunError, OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f"score_rounds: {error}") from error
