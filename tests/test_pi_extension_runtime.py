from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_pi_package_is_skill_and_prompt_only() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    assert package["name"] == "@doodledood/manifest-dev-pi"
    assert package["version"] == "1.0.2"
    assert package["pi"] == {
        "skills": ["./dist/pi/skills"],
        "prompts": ["./dist/pi/prompts"],
    }
    assert "extensions" not in package["pi"]
    assert "workspaces" not in package
    assert "exports" not in package
    assert not (ROOT / "pi" / "extensions").exists()
    assert not (ROOT / "packages" / "manifest-dev-pi-tools").exists()


def test_pi_prompt_aliases_expand_to_skills() -> None:
    prompts = ROOT / "dist" / "pi" / "prompts"
    expected = {
        "do.md": "Use the do skill with: $ARGUMENTS",
        "auto.md": "Use the auto skill with: $ARGUMENTS",
        "babysit-pr.md": "Use the babysit-pr skill with: $ARGUMENTS",
    }
    assert {p.name for p in prompts.glob("*.md")} == set(expected)
    for filename, body in expected.items():
        text = (prompts / filename).read_text(encoding="utf-8")
        assert body in text
        assert "description:" in text


def test_pi_runtime_fanout_symbols_are_absent_from_live_sources() -> None:
    live_paths = [
        ROOT / "package.json",
        ROOT / "dist" / "pi" / "README.md",
        ROOT / "dist" / "pi" / ".sync-meta.json",
        ROOT / "dist" / "pi" / "component-namespaces.json",
        ROOT / ".claude" / "skills" / "sync-tools" / "references" / "pi-cli.md",
    ]
    stale = [
        "manifest-verifier-max-concurrent",
        "MANIFEST_DEV_VERIFIER_MAX_CONCURRENT",
        "manifest_dev_request_verification",
        "manifest_dev_report_outcome",
        "WAIT-PENDING",
        "JSON subprocess verifier fanout",
        "runtime-owned verification",
        "done outcome",
    ]
    for path in live_paths:
        text = path.read_text(encoding="utf-8")
        for phrase in stale:
            assert phrase not in text, f"{path}: {phrase}"
