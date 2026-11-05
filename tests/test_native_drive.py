"""A prepared native handoff never stands in for a completed model drive."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRIVE = ROOT / "scripts/drive-skill.sh"


def native_env(tmp_path: Path) -> dict[str, str]:
    env = {
        **os.environ,
        "CODEX_CI": "1",
        "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "runs"),
        "MODEL": "gpt-6.1-sol",
        "MODEL_REASONING_EFFORT": "xhigh",
    }
    env.pop("CLAUDECODE", None)
    env.pop("MANIFEST_DEV_NATIVE_RUN", None)
    return env


def call(env: dict[str, str], *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(DRIVE),
            "review-code",
            "verification/prompts/review-code-rare-correctness.md",
            *extra,
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )


def prepare(tmp_path: Path) -> tuple[dict[str, str], Path, dict[str, Any]]:
    env = native_env(tmp_path)
    result = call(env)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "NATIVE_SESSION_REQUEST:" in result.stdout
    assert "no CLI sign-in is required" in result.stderr
    out = next((tmp_path / "runs/review-code").iterdir())
    request = json.loads((out / "native-request.json").read_text())
    return env, out, request


def receipt(out: Path, request: dict[str, Any]) -> dict[str, Any]:
    return {
        "host": "codex",
        "status": "completed",
        "native_session_id": "fixture-native-session",
        "request_sha256": hashlib.sha256(
            (out / "native-request.json").read_bytes()
        ).hexdigest(),
        "model": "gpt-6.1-sol",
        "reasoning_effort": "xhigh",
        "turns": [
            {
                "input_sha256": hashlib.sha256(t.encode()).hexdigest(),
                "status": "completed",
                "reply": "Fixture terminal reply, not behavioral proof.",
            }
            for t in request["turns"]
        ],
    }


def test_native_prepare_has_copied_skill_and_no_success(tmp_path: Path) -> None:
    _, out, request = prepare(tmp_path)
    assert not (out / "summary.json").exists()
    worker = (out / "worker-prompt.md").read_text()
    target = Path(request["catalog"]["manifest-dev:review-code"]["path"])
    assert target.read_text() in worker
    assert "Proves:" not in worker
    assert not (out / "plugins/manifest-dev/evals").exists()
    assert Path(request["project"]).is_relative_to(out)
    assert Path(request["records"]).is_relative_to(out)


def test_completed_native_result_is_finalized_as_readable_evidence(
    tmp_path: Path,
) -> None:
    env, out, request = prepare(tmp_path)
    (out / "native-result.json").write_text(json.dumps(receipt(out, request)))
    result = call({**env, "MANIFEST_DEV_NATIVE_RUN": str(out)})
    assert result.returncode == 0, result.stderr
    summary = json.loads((out / "summary.json").read_text())
    assert summary["host"] == "codex" and summary["model"] == "gpt-6.1-sol"
    assert summary["cost_usd"] == "not reported by native harness"
    assert "not a behavior verdict" in result.stdout


@pytest.mark.parametrize(
    "fault",
    [
        "request",
        "host",
        "status",
        "model",
        "reasoning_effort",
        "turn",
        "input",
        "error",
        "copy",
        "reference",
        "worker",
    ],
)
def test_incomplete_or_wrong_native_evidence_cannot_pass(
    tmp_path: Path, fault: str
) -> None:
    env, out, request = prepare(tmp_path)
    result = receipt(out, request)
    if fault == "request":
        result["request_sha256"] = "different"
    elif fault in {"host", "status", "model", "reasoning_effort"}:
        result[fault] = "different"
    elif fault == "turn":
        result["turns"] = []
    elif fault == "input":
        result["turns"][0]["input_sha256"] = "different"
    elif fault == "error":
        result["turns"][0]["status"] = "failed"
    elif fault == "copy":
        Path(request["catalog"]["manifest-dev:review-code"]["path"]).write_text(
            "changed"
        )
    elif fault == "reference":
        entry = Path(request["catalog"]["manifest-dev:review-code"]["path"])
        (entry.parent / "references/code-bugs.md").write_text("changed")
    elif fault == "worker":
        (out / "worker-prompt.md").write_text("changed")
    (out / "native-result.json").write_text(json.dumps(result))
    finished = call({**env, "MANIFEST_DEV_NATIVE_RUN": str(out)})
    assert finished.returncode == 3
    assert not (out / "summary.json").exists()


def test_claude_marker_wins_in_a_nested_claude_session(tmp_path: Path) -> None:
    result = subprocess.run(
        ["bash", "-c", "source scripts/lib/model-host.sh; model_host"],
        cwd=ROOT,
        env={**native_env(tmp_path), "CLAUDECODE": "1"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "claude"


def test_native_dry_run_does_not_prepare_or_call_a_cli(tmp_path: Path) -> None:
    result = call(native_env(tmp_path), "--dry-run")
    assert result.returncode == 0
    assert "active Codex native model harness" in result.stdout
    assert not (tmp_path / "runs").exists()


def test_codex_never_runs_an_installed_claude_cli(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    marker = tmp_path / "foreign-cli-called"
    stub = bin_dir / "claude"
    stub.write_text(f'#!/bin/sh\ntouch "{marker}"\nexit 99\n')
    stub.chmod(0o755)
    env = native_env(tmp_path)
    result = call({**env, "PATH": f'{bin_dir}:{env["PATH"]}'})
    assert result.returncode == 3 and "NATIVE_SESSION_REQUEST:" in result.stdout
    assert not marker.exists()


def test_codex_suite_refuses_the_foreign_instrument_before_auth(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            str(ROOT / "scripts/evals/run_eval.sh"),
            "--preflight",
            "native-case",
            str(tmp_path / "result.json"),
        ],
        cwd=ROOT,
        env=native_env(tmp_path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
    assert "Claude-native plugin-eval instrument" in result.stderr
    assert "auth login" not in result.stderr
    assert not (tmp_path / "result.json").exists()


def test_native_record_preserves_one_session_across_ordered_turns(
    tmp_path: Path,
) -> None:
    env = native_env(tmp_path)
    prompt = tmp_path / "turns.md"
    prompt.write_text("First input.\n<!-- next turn -->\nSecond input.\n")
    command = [str(DRIVE), "review-code", str(prompt)]
    started = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    assert started.returncode == 3
    out = next((tmp_path / "runs/review-code").iterdir())
    reply = tmp_path / "reply.txt"
    reply.write_text("Actual fixture reply.")
    recorder = [
        "python3",
        str(ROOT / "scripts/native_drive.py"),
        "record",
        str(out),
        "--session-id",
        "same-native-session",
        "--model",
        "gpt-6.1-sol",
        "--reasoning-effort",
        "xhigh",
        "--reply-file",
        str(reply),
    ]
    for turn in (1, 2):
        recorded = subprocess.run(
            [*recorder, "--turn", str(turn)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert recorded.returncode == 0, recorded.stderr
        finished = subprocess.run(
            command,
            cwd=ROOT,
            env={**env, "MANIFEST_DEV_NATIVE_RUN": str(out)},
            capture_output=True,
            text=True,
        )
        assert finished.returncode == (3 if turn == 1 else 0), finished.stderr
    duplicate = subprocess.run(
        [*recorder, "--turn", "2"], cwd=ROOT, env=env, capture_output=True, text=True
    )
    assert duplicate.returncode == 3


def test_walk_document_turn_marker_is_content(tmp_path: Path) -> None:
    document = tmp_path / "document.md"
    document.write_text("A literal marker: <!-- next turn --> is documentation.")
    result = subprocess.run(
        [str(ROOT / "scripts/walk.sh"), "Read the document", str(document)],
        cwd=ROOT,
        env=native_env(tmp_path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
    out = next((tmp_path / "runs/document-reader").iterdir())
    request = json.loads((out / "native-request.json").read_text())
    assert len(request["turns"]) == 1
    assert "<!-- next turn -->" in request["turns"][0]
