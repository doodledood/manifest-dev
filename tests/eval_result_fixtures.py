"""Small saved-result fixtures at the native CLI / launch-contract boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def grader(
    name: str, passed: bool, scored: bool = True, *, diagnostic: bool = False
) -> dict[str, Any]:
    return {
        "name": name,
        "type": "llm",
        "config": {
            "focus": {"source": "file", "path": "manifest.md"},
            "criteria": f"{name} rubric",
            **({"arm": "with-only"} if diagnostic else {}),
        },
        "scored": scored,
        "weight": 1,
        "passed": passed,
        "evidence": f"{name} evidence",
        "judgeVotes": [passed, passed, passed],
    }


def case(name: str, runs: list[list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "name": name,
        "promptMarkdown": f"request {name}",
        "model": "opus",
        "maxTurns": 40,
        "timeoutSeconds": 900,
        "graders": [
            {k: g[k] for k in ("name", "type", "weight", "config")} for g in runs[0]
        ],
        "arms": {
            "with": [
                {
                    "costUsd": 1.0,
                    "graders": gs,
                    "tracePath": f"/fixture/{name}/with/{index}/trace.jsonl",
                }
                for index, gs in enumerate(runs)
            ]
        },
    }


def write(path: Path, *cases: dict[str, Any], ablation: str = "none") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "claudeVersion": "2.1.306",
        "suite": {"ablation": ablation, "judgeModel": "sonnet"},
        "cases": list(cases),
    }
    contract = {
        "schemaVersion": 1,
        "cliVersion": "2.1.306",
        "judgeModel": "sonnet",
        "ablation": ablation,
        "sharedInstrumentHash": "fixed-shared-fixture",
        "behaviorOptions": {},
        "cases": [
            {
                "name": c["name"],
                "runs": len(c["arms"]["with"]),
                "prompt": c["promptMarkdown"],
                "graders": c["graders"],
                "model": "opus",
                "sourceModel": c["model"],
                "maxTurns": c["maxTurns"],
                "timeoutSeconds": c["timeoutSeconds"],
                "files": {"prompt.md": c["name"]},
                "instrumentHash": f"fixed-{c['name']}",
            }
            for c in cases
        ],
    }
    path.write_text(json.dumps(data))
    path.with_suffix(".instrument.json").write_text(json.dumps(contract))
    return path


def edit_result(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(path.read_text())
    return data
