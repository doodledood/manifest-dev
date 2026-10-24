"""Independently derived from Claude Code 2.1.306 schema + serializer (not a paid run).
Use source below to build a temp plugin; call inventory with ARGV, then validate RESULT.
All expected normalized config fields are literals, independent of eval_contract.py.
"""

from typing import Any

ARGV = [
    "--ablation",
    "none",
    "--runs",
    "1",
    "--model",
    "sonnet",
    "--judge-model",
    "sonnet",
]
SOURCES = {
    "evals/native-case/prompt.md": """---
name: native-case
model: opus
max_turns: 40
timeout_seconds: 900
runs: 3
---

Create manifest.md containing done.

""",
    "evals/native-case/graders/regex.md": """---
type: regex
---

done

""",
    "evals/native-case/graders/order.md": """---
type: tool_order
before: Read
after:
  tool: Write
  input_match: manifest
---
""",
    "evals/native-case/graders/artifact.md": """---
type: llm
focus:
  source: file
  path: manifest.md
---

The manifest says done.

""",
    "evals/native-case/graders/exists.md": """---
type: file_exists
path: manifest.md
---
""",
}
RESULT: dict[str, Any] = {
    "schemaVersion": 1,
    "claudeVersion": "2.1.306",
    "startedAt": "2026-10-24T20:00:00.000Z",
    "durationSeconds": 1,
    "costUsd": 0.1,
    "partial": False,
    "suite": {
        "root": "/fixture/plugin",
        "ablation": "none",
        "modelOverride": "sonnet",
        "judgeModel": "sonnet",
        "threshold": 1,
        "concurrency": 1,
        "plugins": [{"name": "fixture", "path": "/fixture/plugin", "version": "1.0.0"}],
    },
    "cases": [
        {
            "name": "native-case",
            "dir": "/fixture/plugin/evals/native-case",
            "source": "/fixture/plugin/evals/native-case/prompt.md",
            "promptMarkdown": "Create manifest.md containing done.",
            "model": "opus",
            "runsPerCase": 3,
            "timeoutSeconds": 900,
            "maxTurns": 40,
            "graders": [
                {
                    "name": "artifact",
                    "type": "llm",
                    "weight": 1,
                    "graderMarkdown": "The manifest says done.",
                    "config": {
                        "focus": {"source": "file", "path": "manifest.md"},
                        "criteria": "The manifest says done.",
                    },
                },
                {
                    "name": "exists",
                    "type": "file_exists",
                    "weight": 1,
                    "config": {"path": "manifest.md", "exists": True},
                },
                {
                    "name": "order",
                    "type": "tool_order",
                    "weight": 1,
                    "config": {
                        "before": {"tool": "Read"},
                        "after": {"tool": "Write", "input_match": "manifest"},
                    },
                },
                {
                    "name": "regex",
                    "type": "regex",
                    "weight": 1,
                    "config": {
                        "target": "last_message",
                        "flags": "",
                        "match": "contains",
                        "pattern": "done",
                    },
                },
            ],
            "arms": {
                "with": [
                    {
                        "score": 1,
                        "passed": True,
                        "turns": 3,
                        "costUsd": 0.1,
                        "judgeCostUsd": 0.03,
                        "error": None,
                        "tracePath": "/fixture/run/trace.jsonl",
                        "skippedPaidGraders": False,
                        "graders": [
                            {
                                "name": "artifact",
                                "passed": True,
                                "weight": 1,
                                "explanation": "judge votes: PASS PASS FAIL",
                                "withOnly": False,
                                "scored": True,
                                "judgeVotes": [True, True, False],
                                "evidence": "done\n",
                            },
                            {
                                "name": "exists",
                                "passed": True,
                                "weight": 1,
                                "explanation": "manifest.md exists as expected",
                                "withOnly": False,
                                "scored": True,
                            },
                            {
                                "name": "order",
                                "passed": True,
                                "weight": 1,
                                "explanation": "Read@0 precedes Write@1",
                                "withOnly": False,
                                "scored": True,
                            },
                            {
                                "name": "regex",
                                "passed": True,
                                "weight": 1,
                                "explanation": "matched done",
                                "withOnly": False,
                                "scored": True,
                            },
                        ],
                    }
                ]
            },
            "aggregates": {"score": 1, "passRate": 1},
        }
    ],
    "aggregates": {
        "casesTotal": 1,
        "casesPassed": 1,
        "overallScore": 1,
        "overallPassRate": 1,
    },
}
