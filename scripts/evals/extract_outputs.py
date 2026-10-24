#!/usr/bin/env python3
"""Extract a named grader's evidence from complete, instrument-validated runs.

Use only train cases. The output directory must be empty, so a failed extraction
cannot leave stale artifacts looking current. HTML recovery is intentionally not
supported: matching grades and display order do not establish run identity.

    python3 scripts/evals/extract_outputs.py result.json --out DIR \\
        --state _state.json --cases d01-layer-cut --grader binding-lives-in-gates
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from eval_contract import InvalidRunError, diagnostic, load_result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("result", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--cases", nargs="+", required=True)
    parser.add_argument(
        "--grader", required=True, help="Exact grader whose evidence should be analyzed"
    )
    args = parser.parse_args(argv)

    data, contract = load_result(args.result)
    state = json.loads(args.state.read_text())
    if set(state["train_ids"]) & set(state["test_ids"]):
        raise InvalidRunError("train and held-out cases overlap")
    if len(set(args.cases)) != len(args.cases):
        raise InvalidRunError("requested cases repeat")
    if set(args.cases) - set(state["train_ids"]):
        raise InvalidRunError(
            "extraction is limited to the frozen train IDs; held-out evidence stays sealed"
        )
    if args.out.exists() and any(args.out.iterdir()):
        raise InvalidRunError(f"{args.out}: output directory must be empty")
    by_name = {c["name"]: c for c in data["cases"]}
    instruments = {c["name"]: c for c in contract["cases"]}
    outputs: list[tuple[str, str, dict[str, Any]]] = []
    for name in args.cases:
        if name not in by_name:
            raise InvalidRunError(f"{name}: not in result")
        case = by_name[name]
        definitions = {g["name"]: g for g in case["graders"]}
        if args.grader not in definitions:
            raise InvalidRunError(f"{name}: no grader named {args.grader}")
        definition = definitions[args.grader]
        source = definition["config"].get("focus", definition["config"].get("target"))
        if not source:
            raise InvalidRunError(
                f"{name}/{args.grader}: grader has no evidence selector"
            )
        for k, run in enumerate(case["arms"]["with"]):
            grade = next(g for g in run["graders"] if g["name"] == args.grader)
            evidence = grade.get("evidence")
            if not isinstance(evidence, str):
                raise InvalidRunError(
                    f"{name}/with/rep{k}/{args.grader}: missing text evidence"
                )
            metadata = {
                "case": name,
                "arm": "with",
                "repetition": k,
                "tracePath": run["tracePath"],
                "resultStartedAt": data.get("startedAt"),
                "grader": args.grader,
                "source": source,
                "instrumentHash": instruments[name]["instrumentHash"],
                "grades": {
                    g["name"]: g["passed"]
                    for g in run["graders"]
                    if not diagnostic(definitions[g["name"]])
                },
            }
            outputs.append((f"{name}_rep{k}", evidence, metadata))
    # Validate everything before writing anything. This is one extraction, never a partially
    # successful training set whose absent hard cases quietly disappear.
    args.out.mkdir(parents=True, exist_ok=True)
    for name, evidence, metadata in outputs:
        (args.out / f"{name}.md").write_text(evidence)
        (args.out / f"{name}.grades.json").write_text(
            json.dumps(metadata, indent=2) + "\n"
        )
    print(
        f"{len(outputs)} artifacts extracted from {args.grader}; source metadata retained"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InvalidRunError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"extract_outputs: {error}", file=sys.stderr)
        raise SystemExit(1) from error
