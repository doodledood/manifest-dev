"""Headless drives and eval runs work with a Claude subscription or an API key.

`scripts/lib/claude-auth.sh` picks the credential both container scripts pass in. A subscription
login lives in the macOS keychain, which a container cannot read, so the subscription path is the
long-lived token `claude setup-token` prints. These tests run the real `drive.sh` with a stub
`docker` that records what it was given, and a stub `zsh` so the developer's own shell profile
never leaks in.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRIVE = REPO_ROOT / "scripts" / "features" / "drive.sh"
PROMPT = REPO_ROOT / "docs" / "features" / "README.md"


def run_drive(
    tmp_path: Path, credentials: dict[str, str]
) -> tuple[subprocess.CompletedProcess[str], str]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    record = tmp_path / "docker-run.txt"
    docker = bin_dir / "docker"
    docker.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = run ]; then\n'
        f'  printf "%s\\n" "$@" > {record}\n'
        f'  env | grep -E "^(CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_API_KEY)=" >> {record}\n'
        "fi\n"
        "exit 0\n"
    )
    zsh = bin_dir / "zsh"
    zsh.write_text("#!/bin/sh\nexit 0\n")
    for stub in (docker, zsh):
        stub.chmod(0o755)
    env = {
        "PATH": f"{bin_dir}:/usr/bin:/bin",
        "HOME": str(tmp_path),
        "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
        **credentials,
    }
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(PROMPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result, record.read_text() if record.exists() else ""


def passed_flags(recorded: str) -> list[str]:
    lines = recorded.splitlines()
    return [lines[i + 1] for i, arg in enumerate(lines[:-1]) if arg == "-e"]


def credentials_seen(recorded: str) -> set[str]:
    """Credential variables the container would receive: passed by name and set in its env."""
    names = {"CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY"}
    env = {line.split("=", 1)[0] for line in recorded.splitlines() if "=" in line}
    return names & set(passed_flags(recorded)) & env


def test_subscription_token_alone_is_passed_in(tmp_path: Path) -> None:
    _, recorded = run_drive(tmp_path, {"CLAUDE_CODE_OAUTH_TOKEN": "tok"})
    assert credentials_seen(recorded) == {"CLAUDE_CODE_OAUTH_TOKEN"}
    assert "CLAUDE_CODE_OAUTH_TOKEN=tok" in recorded.splitlines()


def test_api_key_alone_is_passed_in(tmp_path: Path) -> None:
    _, recorded = run_drive(tmp_path, {"ANTHROPIC_API_KEY": "key"})
    assert credentials_seen(recorded) == {"ANTHROPIC_API_KEY"}
    assert "ANTHROPIC_API_KEY=key" in recorded.splitlines()


def test_subscription_token_wins_when_both_are_set(tmp_path: Path) -> None:
    _, recorded = run_drive(
        tmp_path, {"CLAUDE_CODE_OAUTH_TOKEN": "tok", "ANTHROPIC_API_KEY": "key"}
    )
    assert credentials_seen(recorded) == {"CLAUDE_CODE_OAUTH_TOKEN"}
    assert not any(
        line.startswith("ANTHROPIC_API_KEY=") for line in recorded.splitlines()
    )


def test_no_credential_fails_with_both_ways_to_get_one(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("docker", "zsh"):
        stub = bin_dir / name
        stub.write_text("#!/bin/sh\nexit 0\n")
        stub.chmod(0o755)
    result = subprocess.run(
        [str(DRIVE), "figure-out", str(PROMPT)],
        env={
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0
    assert (
        "claude setup-token" in result.stderr and "ANTHROPIC_API_KEY" in result.stderr
    )


def test_eval_suite_uses_a_subscription_token_when_set(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    record = tmp_path / "docker-run.txt"
    docker = bin_dir / "docker"
    docker.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = run ]; then\n'
        f'  printf "%s\\n" "$@" > {record}\n'
        f'  env | grep -E "^(CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_API_KEY)=" >> {record}\n'
        "fi\n"
        "exit 0\n"
    )
    zsh = bin_dir / "zsh"
    zsh.write_text("#!/bin/sh\nexit 0\n")
    for stub in (docker, zsh):
        stub.chmod(0o755)
    result = subprocess.run(
        [str(REPO_ROOT / "scripts/evals/run_eval.sh"), "n", "evals/results/x.json"],
        env={
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "CLAUDE_CODE_OAUTH_TOKEN": "tok",
            "ANTHROPIC_API_KEY": "key",
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert credentials_seen(record.read_text()) == {"CLAUDE_CODE_OAUTH_TOKEN"}
    assert "usage limits" in result.stderr
