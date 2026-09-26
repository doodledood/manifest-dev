"""Run unchanged behavioral checks against permissive and protected owners."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

fixtures = Path(sys.argv[1]).resolve()
checks = Path(__file__).with_name("supported_paths.py")
with tempfile.TemporaryDirectory(prefix="prevention-integration-") as directory:
    run = Path(directory)
    shutil.copyfile(checks, run / "test_supported.py")
    # Both versions use ordinary callers with no duplicated validation.
    shutil.copyfile(fixtures / "case03" / "callers.py", run / "callers.py")
    (run / "additional.py").write_text(
        "from owner import send\n\ndef additional_order(quantity):\n"
        "    return send(quantity)\n"
    )
    for case, expected in (("case01", 1), ("case03", 0)):
        shutil.copyfile(fixtures / case / "owner.py", run / "owner.py")
        result = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-v", "test_supported.py"],
            cwd=run,
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"{case}: exit {result.returncode} (expected {expected})")
        print(result.stderr)
        if result.returncode != expected:
            raise SystemExit("Unexpected behavioral result")
