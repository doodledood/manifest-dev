"""Regression fixtures for bounded HTML design triage.

Render checks use a locally available Playwright/Chromium installation. Set
DESIGN_CHECK_NODE_DIR to its package directory and DESIGN_CHECK_CHROMIUM when
needed. Missing browser capability is an explicit skip, never a passing render.
DESIGN_CHECK_TEST_SCRIPT permits running these same fixtures against a baseline.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(
    os.environ.get(
        "DESIGN_CHECK_TEST_SCRIPT",
        str(
            ROOT / "claude-plugins/manifest-dev/skills/design/scripts/design-check.mjs"
        ),
    )
)


def run_check(tmp_path: Path, css: str, body: str) -> str:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node unavailable")
    assert node is not None
    artifact = tmp_path / "artifact with spaces.html"
    artifact.write_text(
        '<!doctype html><html lang="en"><head><title>Probe</title>'
        "<style>body{background:white;color:black}"
        + css
        + "</style></head><body>"
        + body
        + "</body></html>"
    )
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [node, str(SCRIPT), str(artifact)],
        cwd=os.environ.get("DESIGN_CHECK_NODE_DIR", str(tmp_path)),
        capture_output=True,
        text=True,
        check=False,
        timeout=40,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def require_render(output: str) -> None:
    if "Playwright not available" in output or "render checks failed to run" in output:
        if os.environ.get("DESIGN_CHECK_NODE_DIR") or os.environ.get(
            "DESIGN_CHECK_CHROMIUM"
        ):
            pytest.fail("Configured render capability failed: " + output)
        pytest.skip("Render capability unavailable: " + output)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]  # mypy skips pytest imports
    ("css", "body"),
    [
        ("", "<button>Save</button>"),
        (
            "*:focus{outline:none}.absent:focus-visible{color:black}",
            "<button>Save</button>",
        ),
        (
            "p{animation:spin 1s infinite}@keyframes spin{to{transform:rotate(1turn)}}"
            "@media(prefers-reduced-motion:reduce){.absent{color:red}}",
            "<p>Animated</p>",
        ),
    ],
)
def test_source_syntax_never_certifies_focus_or_motion(
    tmp_path: Path, css: str, body: str
) -> None:
    output = run_check(tmp_path, css, body)
    assert "OK       focus-visible" not in output
    assert "OK       reduced-motion" not in output
    assert "FINDING  focus-visible" not in output
    assert "NOTE" in output


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]  # mypy skips pytest imports
    ("css", "body", "reason"),
    [
        ("p{color:rgba(0,0,0,.1)}", "<p>Text</p>", "foreground"),
        (
            "body{background:black;color:white}p{background:rgba(255,255,255,.05)}",
            "<p>Text</p>",
            "background requires compositing",
        ),
        ("main{opacity:.1}", "<main><p>Text</p></main>", "opacity"),
        ("p{color:oklch(95% 0 0)}", "<p>Text</p>", "foreground"),
        (
            "p{background-image:linear-gradient(white,white);color:#eee}",
            "<p>Text</p>",
            "background image",
        ),
        (
            "",
            '<svg width="200" height="100"><text x="10" y="40" fill="white">Text</text></svg>',
            "non-HTML text paint",
        ),
    ],
)
def test_unhandled_paint_is_counted_as_skipped(
    tmp_path: Path, css: str, body: str, reason: str
) -> None:
    output = run_check(tmp_path, css, body)
    require_render(output)
    assert "0 measured, 0 below threshold, 1 skipped" in output
    assert "SKIPPED  contrast:" in output
    assert reason in output
    assert "OK       contrast" not in output


def test_mixed_coverage_keeps_measured_and_skipped_separate(tmp_path: Path) -> None:
    output = run_check(
        tmp_path,
        ".faint{color:rgba(0,0,0,.1)}",
        '<p>Readable</p><p class="faint">Faint</p>',
    )
    require_render(output)
    assert "1 measured, 0 below threshold, 1 skipped" in output
    assert "SKIPPED  contrast:" in output


def test_contrast_threshold_is_not_rounded_up(tmp_path: Path) -> None:
    output = run_check(tmp_path, "p{color:rgb(112,120,125)}", "<p>Text</p>")
    require_render(output)
    assert "4.4952:1 (< 4.5:1)" in output
    assert "1 measured, 1 below threshold, 0 skipped" in output


def test_opaque_readable_text_is_actually_measured(tmp_path: Path) -> None:
    output = run_check(tmp_path, "", "<p>Readable</p>")
    require_render(output)
    assert "1 measured, 0 below threshold, 0 skipped" in output


def test_modern_background_is_unknown_not_transparent(tmp_path: Path) -> None:
    output = run_check(tmp_path, "body{background:oklch(100% 0 0)}", "<p>Text</p>")
    require_render(output)
    assert "unsupported color syntax" in output
    assert "transparent on both" not in output


def test_class_themes_do_not_require_a_media_query(tmp_path: Path) -> None:
    output = run_check(
        tmp_path,
        ".dark{background:black;color:white}",
        "<button onclick=\"document.body.classList.toggle('dark')\">Theme</button>",
    )
    assert "a defect if both themes are claimed" not in output


def test_targets_are_candidates_and_include_checkboxes(tmp_path: Path) -> None:
    output = run_check(
        tmp_path,
        "input{appearance:none;width:8px;height:8px;background:black;margin:0}",
        '<input type="checkbox" aria-label="One"><input type="checkbox" aria-label="Two">'
        '<p>Read <a href="#">this</a>.</p>',
    )
    require_render(output)
    assert "target candidate@320: <input>" in output
    assert (
        "review spacing, equivalent, inline, user-agent and essential exceptions"
        in output
    )
    assert "FINDING  touch target" not in output
    assert "OK       touch targets" not in output


def test_320px_overflow_is_not_hidden_by_390px_success(tmp_path: Path) -> None:
    output = run_check(tmp_path, "main{width:350px}", "<main>Text</main>")
    require_render(output)
    assert "NOTE     overflow@320:" in output
    assert "OK       overflow@390:" in output
