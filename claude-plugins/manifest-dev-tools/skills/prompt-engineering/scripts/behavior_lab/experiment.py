"""Generic arm/scenario experiment runner for the empirical skill-behavior
verification framework, plus session-json parsing: turning a captured run
directory's ``diagnostics/*.json`` files into structured records, rollups,
and session attribution.

An **arm** is a named variant to compare — typically "baseline" (current
skill/prompt wording) vs. "amended" (the proposed change) — carrying whatever
harness, model/effort, and prompt-construction config that variant needs. A
**scenario** is the caller-supplied task to run through every arm: a prompt
plus the working directory to run it in. Deliberately no built-in scenario
library or cache-staggering-specific fields (see this manifest's ASM-4) —
callers bring their own scenario.

The session-json parsing functions here generalize
``tests/cache-experiment/analyze.py``'s run-directory-loading functions
(``load_run_calls``, ``summarize_run``, ``attribute_sessions_to_criteria``,
``summarize_run_by_criterion``, ``discover_run_dirs``, ``summarize_arm``) —
ported, not imported (see INV-G2/PG-3) — from "criterion" framing to this
framework's arm/scenario shape.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .harness import Harness, extract_usage

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9_.-]+")
_USAGE_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)


def _slug(value: str) -> str:
    slug = _SAFE_CHARS.sub("-", value).strip("-")
    return slug or "x"


@dataclasses.dataclass(frozen=True)
class Scenario:
    """A caller-supplied task to run through every arm."""

    name: str
    prompt: str
    cwd: str | Path


@dataclasses.dataclass(frozen=True)
class Arm:
    """A named variant: which harness, which model/effort, and how to build the
    prompt actually sent (default: the scenario's prompt unchanged) — no field
    specific to any one experiment's shape (e.g. no inline_manifest/launch_order)."""

    name: str
    harness: Harness
    model: str | None = None
    effort: str | None = None
    build_prompt: Callable[[Scenario], str] = lambda scenario: scenario.prompt


@dataclasses.dataclass(frozen=True)
class RunResult:
    scenario: str
    arm: str
    repeat_index: int
    run_directory: Path
    returncode: int


def compute_run_key(*, scenario: str, arm: str, repeat_index: int) -> str:
    """Pure digest of the identifying run parameters, stable across processes.

    No timestamps, random ids, or process-specific state feed into this —
    only the three identifying inputs — so the same tuple always produces the
    same key, in this process or any other.
    """
    payload = "\x1f".join([scenario, arm, str(repeat_index)])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def run_dir(
    base_dir: Path | str, *, scenario: str, arm: str, repeat_index: int = 0
) -> Path:
    """Deterministic run-scoped directory: same (scenario, arm, repeat_index)
    always yields the same path, so results are locatable from just those
    identifying parameters and re-running lands in the same place rather than
    accumulating new directories."""
    key = compute_run_key(scenario=scenario, arm=arm, repeat_index=repeat_index)
    return (
        Path(base_dir) / _slug(arm) / _slug(scenario) / f"repeat-{repeat_index}" / key
    )


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_experiment(
    scenarios: Sequence[Scenario],
    arms: Sequence[Arm],
    run_dir_base: Path | str,
    *,
    repeat_index: int = 0,
) -> list[RunResult]:
    """Execute every (scenario, arm) pair through its arm's harness adapter,
    capturing diagnostics in a deterministic, inspectable layout under
    ``run_dir_base``."""
    import os

    results = []
    for scenario in scenarios:
        for arm in arms:
            directory = _ensure_dir(
                run_dir(
                    run_dir_base,
                    scenario=scenario.name,
                    arm=arm.name,
                    repeat_index=repeat_index,
                )
            )
            prompt = arm.build_prompt(scenario)
            (directory / "prompt.txt").write_text(prompt, encoding="utf-8")
            (directory / "metadata.json").write_text(
                json.dumps(
                    {
                        "scenario": scenario.name,
                        "arm": arm.name,
                        "repeat_index": repeat_index,
                        "model": arm.model,
                        "effort": arm.effort,
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )

            env_overrides = arm.harness.configure_for_capture(directory)
            invoke_result = arm.harness.invoke(
                prompt, cwd=scenario.cwd, env={**os.environ, **env_overrides}
            )
            (directory / "stdout.log").write_text(
                invoke_result.stdout, encoding="utf-8"
            )
            (directory / "stderr.log").write_text(
                invoke_result.stderr, encoding="utf-8"
            )

            results.append(
                RunResult(
                    scenario=scenario.name,
                    arm=arm.name,
                    repeat_index=repeat_index,
                    run_directory=directory,
                    returncode=invoke_result.returncode,
                )
            )
    return results


# --- Session-json parsing: turn a captured run directory into structured
# records, without re-deriving the SSE decode by hand each time. -----------


def load_run_calls(diagnostics_dir: Path | str) -> list[dict[str, Any]]:
    """Every real (POST, HTTP 200) API call in a run's ``diagnostics/`` folder,
    in capture order, as a flat record: session/agent identity and token
    usage. Non-``/v1/messages`` traffic (e.g. a stray health-check GET) is
    dropped rather than raising, since those aren't calls an experiment is
    measuring."""
    calls = []
    for path in sorted(Path(diagnostics_dir).glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        if entry.get("method") != "POST" or entry.get("response_status") != 200:
            continue
        calls.append(
            {
                "file": path.name,
                "session_id": entry.get("session_id"),
                "agent_id": entry.get("agent_id"),
                "is_subagent": bool(entry.get("is_subagent")),
                "usage": extract_usage(entry.get("response_body")),
            }
        )
    return calls


def summarize_run(diagnostics_dir: Path | str) -> dict[str, Any]:
    """Whole-run rollup: call/session counts and total tokens by kind."""
    calls = load_run_calls(diagnostics_dir)
    sessions: dict[str, int] = {}
    for call in calls:
        sessions[call["session_id"]] = sessions.get(call["session_id"], 0) + 1

    total_tokens = dict.fromkeys(_USAGE_FIELDS, 0)
    for call in calls:
        for field in _USAGE_FIELDS:
            total_tokens[field] += call["usage"][field]

    return {
        "call_count": len(calls),
        "session_count": len(sessions),
        "calls_per_session": sessions,
        "subagent_call_count": sum(1 for c in calls if c["is_subagent"]),
        "total_tokens": total_tokens,
    }


def _text_leaves(obj: Any) -> list[str]:
    """Every string leaf in a nested JSON structure, depth-first — used for
    attribution matching against raw prompt text, since a prompt's literal
    newlines wouldn't survive an escaped-JSON round-trip."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, Mapping):
        leaves = []
        for value in obj.values():
            leaves.extend(_text_leaves(value))
        return leaves
    if isinstance(obj, list):
        leaves = []
        for item in obj:
            leaves.extend(_text_leaves(item))
        return leaves
    return []


def attribute_sessions(
    run_directory: Path | str, prompts_by_label: Mapping[str, str]
) -> dict[str, str]:
    """Map each session_id captured under ``run_directory`` to the label whose
    prompt text is that session's first request, verbatim.

    Diagnostics calls are keyed by the coding agent's own session id, which
    carries no scenario/arm label of its own — but when a run directory's
    harness invocation itself launches multiple independent sessions sharing
    one proxy capture (e.g. several criterion-style sub-invocations run
    against the same scenario), each session's first request's text is that
    invocation's prompt verbatim, so matching it against a caller-supplied
    label->prompt mapping recovers the attribution without new
    instrumentation. A run directory produced by `run_experiment` has exactly
    one label (its own scenario/arm) by construction — this is for the
    multi-invocation-per-run-directory case."""
    run_directory = Path(run_directory)
    first_request_text: dict[str, list[str]] = {}
    for path in sorted((run_directory / "diagnostics").glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        if entry.get("method") != "POST":
            continue
        session_id = entry.get("session_id")
        if session_id in first_request_text:
            continue
        request_body = entry.get("request_body")
        if isinstance(request_body, str):
            request_body = json.loads(request_body) if request_body else {}
        first_request_text[session_id] = _text_leaves(request_body)

    mapping = {}
    for session_id, leaves in first_request_text.items():
        for label, prompt in prompts_by_label.items():
            if prompt and any(prompt in leaf for leaf in leaves):
                mapping[session_id] = label
                break
    return mapping


def summarize_run_by_label(
    run_directory: Path | str, prompts_by_label: Mapping[str, str]
) -> dict[str, dict[str, Any]]:
    """Per-label call count / tokens within one run, via session attribution."""
    run_directory = Path(run_directory)
    session_to_label = attribute_sessions(run_directory, prompts_by_label)
    calls = load_run_calls(run_directory / "diagnostics")

    per_label: dict[str, dict[str, Any]] = {}
    for call in calls:
        label = session_to_label.get(call["session_id"], "_unattributed")
        bucket = per_label.setdefault(
            label, {"call_count": 0, "total_tokens": dict.fromkeys(_USAGE_FIELDS, 0)}
        )
        bucket["call_count"] += 1
        for field in _USAGE_FIELDS:
            bucket["total_tokens"][field] += call["usage"][field]
    return per_label


def discover_run_dirs(run_dir_base: Path | str, arm: str) -> list[Path]:
    """Every captured run directory for one arm, across all scenarios/repeats.

    Mirrors `run_dir`'s layout (``<arm>/<scenario>/repeat-<n>/<key>``) without
    needing the original identifying parameters back — just walks for
    directories that actually contain a ``diagnostics/`` folder."""
    arm_dir = Path(run_dir_base) / _slug(arm)
    if not arm_dir.is_dir():
        return []
    return sorted(p.parent for p in arm_dir.glob("*/repeat-*/*/diagnostics"))


def summarize_arm(run_dir_base: Path | str, arm: str) -> dict[str, Any]:
    """Roll every captured run for one arm up into arm-level totals and per-run detail."""
    run_dirs = discover_run_dirs(run_dir_base, arm)
    per_run = [summarize_run(d / "diagnostics") for d in run_dirs]
    total_tokens = dict.fromkeys(_USAGE_FIELDS, 0)
    for run in per_run:
        for field in _USAGE_FIELDS:
            total_tokens[field] += run["total_tokens"][field]
    return {
        "run_count": len(per_run),
        "run_dirs": [str(d) for d in run_dirs],
        "per_run": per_run,
        "total_calls": sum(r["call_count"] for r in per_run),
        "total_tokens": total_tokens,
    }
