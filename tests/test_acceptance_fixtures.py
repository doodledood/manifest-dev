"""Independent controls for review-acceptance behavior scenarios.

ADR: 20261106-review-evidence-serves-substantive-acceptance.
These prove the seeded failures and viable control, not agent behavior.
"""

import json
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "verification/fixtures"


def test_sample_green_does_not_prove_the_real_export(tmp_path: Path) -> None:
    shutil.copytree(
        FIXTURES / "acceptance-execution/project", tmp_path, dirs_exist_ok=True
    )
    sample = subprocess.run(
        [sys.executable, "check.py"], cwd=tmp_path, capture_output=True
    )
    assert sample.returncode == 0
    subprocess.run([sys.executable, "exporter.py"], cwd=tmp_path, check=True)
    expected = [{"id": "a", "label": "First"}, {"id": "a", "label": "Second"}]
    assert json.loads((tmp_path / "records.json").read_text()) == expected
    assert json.loads((tmp_path / "output.json").read_text()) == expected[1:]
    # The later authority change opens another reachable failure in the same code.
    shutil.copyfile(tmp_path / "later-inputs/records.json", tmp_path / "records.json")
    subprocess.run([sys.executable, "exporter.py"], cwd=tmp_path, check=True)
    assert {"id": "b", "label": ""} not in json.loads(
        (tmp_path / "output.json").read_text()
    )


def test_mocked_unit_check_and_real_preview_have_different_evidence(
    tmp_path: Path,
) -> None:
    shutil.copytree(
        FIXTURES / "acceptance-review/project", tmp_path, dirs_exist_ok=True
    )
    tests = subprocess.run(
        [sys.executable, "-m", "unittest"], cwd=tmp_path, capture_output=True
    )
    assert tests.returncode == 0, tests.stderr.decode()
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "from full_export import export; print(len(export([{'id':'a','label':'A'}, {'id':'b','label':'B'}])))",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert (
        probe.stdout.strip() == "1"
    )  # Full export owes two; the green mock never calls it.


def test_limiter_has_a_real_impossible_case_and_a_viable_alternative() -> None:
    plain = (FIXTURES / "acceptance-limiter/project/plain/source.txt").read_bytes()
    flexible = (
        FIXTURES / "acceptance-limiter/project/compressed/source.txt"
    ).read_bytes()
    assert plain == flexible == b"x" * 300
    assert len(plain) > 100  # Raw-only encoding cannot meet the receiver's hard cap.
    encoded = zlib.compress(flexible)
    assert len(encoded) <= 100
    assert zlib.decompress(encoded) == flexible
