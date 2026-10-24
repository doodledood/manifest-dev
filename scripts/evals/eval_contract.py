#!/usr/bin/env python3
"""Inventory a frozen eval copy and validate results against its launch contract.

Claude Code owns schema validation (run_eval.sh uses its zero-cost preflight).
This module reads that validated source to retain the information its result omits.
It also serves the scorer and extractor, so neither can accept an incomplete run.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


class InvalidRunError(ValueError):
    """The evidence cannot support a measurement or comparison."""


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    import yaml

    match = re.fullmatch(r"---\n(.*?)\n---\n?(.*)", path.read_text(), re.S)
    if not match:
        raise InvalidRunError(f"{path}: missing frontmatter")
    data = yaml.safe_load(match[1]) or {}
    if not isinstance(data, dict):
        raise InvalidRunError(f"{path}: frontmatter must be a mapping")
    return data, match[2].strip()


def options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--tag", nargs="+", action="extend", default=[])
    parser.add_argument("--case", default="*")
    parser.add_argument("--runs", type=int)
    parser.add_argument(
        "--ablation", choices=["none", "with-without"], default="with-without"
    )
    parser.add_argument("--model")
    parser.add_argument("--judge-model", default="sonnet")
    parser.add_argument("--eval-dir", default="evals")
    parser.add_argument("--allow-tools", nargs="+", action="extend", default=[])
    parser.add_argument("--disallow-tools", nargs="+", action="extend", default=[])
    parser.add_argument("--scaffold", action="store_true")
    parser.add_argument("--no-scaffold", action="store_false", dest="scaffold")
    parser.add_argument("--mocks", default="record")
    parser.add_argument("--allow-real-servers", action="store_true")
    return parser.parse_known_args(argv)[0]


def diagnostic(grader: dict[str, Any]) -> bool:
    config = grader.get("config", {})
    return config.get("arm") == "with-only" or (
        grader["type"] == "tool_used"
        and config.get("tool") == "Skill"
        and "arm" not in config
    )


def grader_definition(path: Path) -> dict[str, Any]:
    config, body = frontmatter(path)
    config = dict(config)
    name = config.pop("name", path.stem)
    kind = config.pop("type")
    weight = config.pop("weight", 1)
    if kind == "llm":
        config.setdefault("focus", "last_message")
        config.setdefault("criteria", body)
    elif kind == "regex":
        config.setdefault("target", "last_message")
        config.setdefault("flags", "")
        config.setdefault("match", "contains")
        config.setdefault("pattern", body)
    elif kind == "file_exists":
        config.setdefault("exists", True)
    elif kind == "baseline":
        config.setdefault("criteria", body)
    elif kind == "tool_order":
        for key in ("before", "after"):
            if isinstance(config[key], str):
                config[key] = {"tool": config[key]}
    return {"name": name, "type": kind, "weight": weight, "config": config}


def inventory(plugin: Path, argv: list[str], cli_version: str) -> dict[str, Any]:
    import yaml

    args = options(argv)
    evals = plugin / args.eval_dir
    for case_file in evals.rglob("case.yaml"):
        if (
            "results" not in case_file.relative_to(evals).parts
            and not case_file.with_name("prompt.md").exists()
        ):
            raise InvalidRunError(
                f"{case_file}: inventory supports this repository's prose cases; add YAML-only inventory support before running"
            )
    selected = []
    for prompt in sorted(evals.rglob("prompt.md")):
        if "results" in prompt.relative_to(evals).parts:
            continue
        meta, body = frontmatter(prompt)
        case_file = prompt.with_name("case.yaml")
        case = yaml.safe_load(case_file.read_text()) if case_file.exists() else {}
        if set(case) - {"schema_version", "name", "context"}:
            raise InvalidRunError(
                f"{case_file}: mixed YAML execution/graders are not supported by the inventory; put them in prompt.md and graders/"
            )
        name = meta.get("name", case.get("name", prompt.parent.name))
        tags = meta.get("tags", case.get("tags", []))
        if not fnmatch.fnmatchcase(name, args.case) or (
            args.tag and not set(args.tag).intersection(tags)
        ):
            continue
        graders = [
            grader_definition(p)
            for p in sorted((prompt.parent / "graders").glob("*.md"))
        ]
        if not graders:
            raise InvalidRunError(f"{name}: no graders")
        if len({g["name"] for g in graders}) != len(graders):
            raise InvalidRunError(f"{name}: duplicate grader names")
        files = {
            p.relative_to(prompt.parent)
            .as_posix(): hashlib.sha256(p.read_bytes())
            .hexdigest()
            for p in sorted(prompt.parent.rglob("*"))
            if p.is_file()
        }
        execution = {**meta, **case.get("execution", {})}
        runs = (
            args.runs
            if args.runs is not None
            else meta.get("runs", case.get("runs", 3))
        )
        if not isinstance(runs, int) or runs < 1:
            raise InvalidRunError(f"{name}: runs must be positive")
        selected.append(
            {
                "name": name,
                "runs": runs,
                "model": args.model or execution.get("model"),
                "sourceModel": execution.get("model"),
                "maxTurns": execution.get("max_turns", 10),
                "timeoutSeconds": execution.get("timeout_seconds", 300),
                "prompt": body,
                "graders": graders,
                "files": files,
                "instrumentHash": digest(files),
            }
        )
    if not selected:
        raise InvalidRunError("no cases selected; check --case and --tag")
    if len({c["name"] for c in selected}) != len(selected):
        raise InvalidRunError("duplicate selected case names")
    compile_regexes(selected)
    # Shared mocks can alter every case. The skill is intentionally separate: hill-climbs
    # change it, while the measuring instrument must stay fixed.
    shared = {
        p.relative_to(evals).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((evals / "mocks").rglob("*"))
        if p.is_file()
    }
    source = {
        p.relative_to(plugin).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((plugin / "skills").rglob("*"))
        if p.is_file()
    }
    return {
        "schemaVersion": 1,
        "cliVersion": cli_version,
        "argv": argv,
        "ablation": args.ablation,
        "judgeModel": args.judge_model,
        "modelOverride": args.model,
        "resolvedModelIds": "unavailable: CLI records supplied model identifiers, not independently resolved model IDs",
        "behaviorOptions": {
            key: getattr(args, key)
            for key in (
                "allow_tools",
                "disallow_tools",
                "scaffold",
                "mocks",
                "allow_real_servers",
            )
        },
        "sharedInstrumentHash": digest(shared),
        "skillSourceHash": digest(source),
        "cases": selected,
    }


def compile_regexes(cases: list[dict[str, Any]]) -> None:
    """The native preflight parses regex fields but compiles them only after spending."""
    expressions = []
    for case in cases:
        for grader in case["graders"]:
            config = grader["config"]
            for key in ("pattern", "input_match"):
                if key in config:
                    expressions.append(
                        {
                            "name": f"{case['name']}/{grader['name']}/{key}",
                            "pattern": config[key],
                            "flags": (
                                config.get("flags", "") if key == "pattern" else ""
                            ),
                        }
                    )
            for key in ("before", "after"):
                ref = config.get(key)
                if isinstance(ref, dict) and "input_match" in ref:
                    expressions.append(
                        {
                            "name": f"{case['name']}/{grader['name']}/{key}",
                            "pattern": ref["input_match"],
                            "flags": "",
                        }
                    )
    result = subprocess.run(
        [
            "node",
            "-e",
            "for(const r of JSON.parse(require('fs').readFileSync(0,'utf8'))) {"
            "try { new RegExp(r.pattern,r.flags); } catch(e) { console.error(r.name+': '+e.message); process.exitCode=1; }}",
        ],
        input=json.dumps(expressions),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise InvalidRunError(f"invalid JavaScript regex: {result.stderr.strip()}")


def missing_artifact(
    grade: dict[str, Any], definition: dict[str, Any], case_name: str
) -> bool:
    config = definition["config"]
    selector = config.get("focus", config.get("target"))
    if (
        not isinstance(selector, dict)
        or selector.get("source") != "file"
        or grade.get("passed") is not False
    ):
        return False
    path = selector["path"]
    allowed = {
        f'grader threw: case "{case_name}" grader focus file "{path}": path "{path}" does not exist',
        f"grader threw: focus file {path} does not exist",
    }
    return grade.get("explanation") in allowed


def report_inventory(contract: dict[str, Any]) -> str:
    trials = votes = llm = graders = 0
    for case in contract["cases"]:
        arms = (
            ["with", "without"] if contract["ablation"] == "with-without" else ["with"]
        )
        trials += len(arms) * case["runs"]
        graders += len(case["graders"])
        llm += sum(g["type"] in {"llm", "baseline"} for g in case["graders"])
        for arm in arms:
            votes += (
                3
                * case["runs"]
                * sum(
                    g["type"] in {"llm", "baseline"}
                    for g in expected_graders(case, contract, arm)
                )
            )
    return (
        f"{len(contract['cases'])} cases; {trials} agent trials; "
        f"{graders} graders ({llm} LLM); {votes} projected judge votes "
        "(Claude Code 2.1.306: 3 votes per LLM grader; excludes failures/skips)"
    )


def expected_graders(
    case: dict[str, Any], contract: dict[str, Any], arm: str
) -> list[dict[str, Any]]:
    graders = case["graders"]
    if arm == "without" and not all(diagnostic(g) for g in graders):
        return [g for g in graders if not diagnostic(g)]
    return graders


def _unique(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    by_name = {item["name"]: item for item in items}
    if len(by_name) != len(items):
        raise InvalidRunError(f"{label}: duplicate names")
    return by_name


def validate(data: dict[str, Any], contract: dict[str, Any]) -> None:
    if data.get("partial"):
        raise InvalidRunError("partial run; finish or rerun before using it")
    if data.get("errors") or data.get("harnessFailures"):
        raise InvalidRunError("run contains harness errors")
    suite = data.get("suite", {})
    if suite.get("ablation") != contract["ablation"]:
        raise InvalidRunError("ablation differs from launch contract")
    if suite.get("judgeModel") != contract["judgeModel"]:
        raise InvalidRunError("judge model differs from launch contract")
    if suite.get("modelOverride") != contract.get("modelOverride"):
        raise InvalidRunError("model override differs from launch contract")
    if data.get("claudeVersion") != contract["cliVersion"]:
        raise InvalidRunError("CLI version differs from launch contract")
    cases = _unique(data["cases"], "result cases")
    expected = _unique(contract["cases"], "contract cases")
    if cases.keys() != expected.keys():
        raise InvalidRunError(
            f"case roster differs: missing {sorted(expected.keys()-cases.keys())}; "
            f"unexpected {sorted(cases.keys()-expected.keys())}"
        )
    identities: set[str] = set()
    for name, case in cases.items():
        wanted = expected[name]
        for field, source in (
            ("model", "sourceModel"),
            ("maxTurns", "maxTurns"),
            ("timeoutSeconds", "timeoutSeconds"),
        ):
            if case.get(field) != wanted[source]:
                raise InvalidRunError(f"{name}: {field} differs from launch contract")
        definitions = _unique(case["graders"], f"{name} definitions")
        wanted_definitions = _unique(wanted["graders"], f"{name} contract graders")
        if definitions.keys() != wanted_definitions.keys():
            raise InvalidRunError(f"{name}: grader roster changed")
        for gname, definition in definitions.items():
            actual = {
                k: definition.get(k) for k in ("name", "type", "weight", "config")
            }
            if actual != wanted_definitions[gname]:
                raise InvalidRunError(f"{name}/{gname}: grader instrument changed")
        if case.get("promptMarkdown") != wanted["prompt"]:
            raise InvalidRunError(f"{name}: prompt differs from launch contract")
        arms = (
            {"with", "without"} if contract["ablation"] == "with-without" else {"with"}
        )
        if set(case["arms"]) != arms:
            raise InvalidRunError(f"{name}: missing or unexpected arm")
        for arm, runs in case["arms"].items():
            if len(runs) != wanted["runs"]:
                raise InvalidRunError(
                    f"{name}/{arm}: expected {wanted['runs']} repetitions, got {len(runs)}"
                )
            expected_grades = _unique(expected_graders(wanted, contract, arm), name)
            for index, run in enumerate(runs):
                label = f"{name}/{arm}/rep{index}"
                if run.get("error") is not None:
                    raise InvalidRunError(f"{label}: agent error: {run['error']}")
                if run.get("aborted") or run.get("skippedPaidGraders"):
                    raise InvalidRunError(
                        f"{label}: aborted run or skipped paid graders"
                    )
                identity = run.get("tracePath")
                if (
                    not isinstance(identity, str)
                    or not identity
                    or identity in identities
                ):
                    raise InvalidRunError(
                        f"{label}: missing or duplicate trace identity"
                    )
                identities.add(identity)
                grades = _unique(run["graders"], label)
                if grades.keys() != expected_grades.keys():
                    raise InvalidRunError(
                        f"{label}: missing or unexpected grader results"
                    )
                for gname, grade in grades.items():
                    if (
                        type(grade.get("passed")) is not bool
                        or type(grade.get("scored")) is not bool
                    ):
                        raise InvalidRunError(
                            f"{label}/{gname}: missing boolean verdict/scoring flag"
                        )
                    if grade.get("weight") != expected_grades[gname]["weight"]:
                        raise InvalidRunError(f"{label}/{gname}: changed weight")
                    absent = missing_artifact(grade, expected_grades[gname], name)
                    if not absent and re.match(
                        r"(?:grader threw:|skipped:|unavailable:|no mock stand-ins were active)",
                        grade.get("explanation", ""),
                        re.I,
                    ):
                        raise InvalidRunError(
                            f"{label}/{gname}: {grade['explanation']}"
                        )
                    if (
                        expected_grades[gname]["type"] in {"llm", "baseline"}
                        and not absent
                    ):
                        votes = grade.get("judgeVotes")
                        if (
                            not isinstance(votes, list)
                            or len(votes) != 3
                            or any(type(v) is not bool for v in votes)
                        ):
                            raise InvalidRunError(
                                f"{label}/{gname}: incomplete judge votes"
                            )
                        if grade["passed"] != (sum(votes) >= 2):
                            raise InvalidRunError(
                                f"{label}/{gname}: verdict disagrees with judge votes"
                            )
                    if not diagnostic(expected_grades[gname]) and not grade["scored"]:
                        raise InvalidRunError(
                            f"{label}/{gname}: quality grader was not scored"
                        )
                for field in ("costUsd", "judgeCostUsd"):
                    value = run.get(field, 0)
                    if (
                        not isinstance(value, (int, float))
                        or not math.isfinite(value)
                        or value < 0
                    ):
                        raise InvalidRunError(f"{label}: invalid {field}")


def load_result(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    sidecar = path.with_suffix(".instrument.json")
    if not sidecar.is_file():
        raise InvalidRunError(
            f"{path}: missing launch contract {sidecar.name}; rerun through run_eval.sh"
        )
    data, contract = json.loads(path.read_text()), json.loads(sidecar.read_text())
    validate(data, contract)
    return data, contract


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("inventory")
    record.add_argument("plugin", type=Path)
    record.add_argument("--out", type=Path)
    record.add_argument("--cli-version", default="not checked (inventory only)")
    check = sub.add_parser("validate")
    check.add_argument("result", type=Path)
    preflight = sub.add_parser("preflight-check")
    preflight.add_argument("result", type=Path)
    preflight.add_argument("log", type=Path)
    preflight.add_argument("exit_code", type=int)
    args, remaining = parser.parse_known_args()
    if args.command != "inventory" and remaining:
        parser.error(f"unexpected arguments: {remaining}")
    try:
        if args.command == "inventory":
            # REMAINDER starts with -- when separating native CLI arguments.
            argv = remaining[1:] if remaining[:1] == ["--"] else remaining
            contract = inventory(args.plugin, argv, args.cli_version)
            if args.out:
                with args.out.open("x") as stream:
                    json.dump(contract, stream, indent=2)
                    stream.write("\n")
            print(report_inventory(contract))
        elif args.command == "validate":
            load_result(args.result)
            print(f"{args.result}: complete; launch contract matches")
        else:
            data = json.loads(args.result.read_text())
            log = args.log.read_text()
            if (
                args.exit_code != 2
                or data.get("costUsd") != 0
                or data.get("cases") != []
                or data.get("partialReason") != "cost_ceiling"
                or not data.get("partial")
                or re.search(r"✗|case file\(s\) failed to load|parse error", log, re.I)
            ):
                raise InvalidRunError(f"native preflight failed; read {args.log}")
            print("Native CLI preflight: valid, zero cost, no agent or judge trials")
    except (InvalidRunError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"eval contract: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
