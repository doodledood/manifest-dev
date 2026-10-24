"""Bind replay observations, optionally injecting the next fixture-owned push."""

import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--next-nits", action="store_true")
args = parser.parse_args()
if args.next_nits:
    # Stage only this marker so the first advance's code and journal remain inspectable.
    Path("fixture-push.txt").write_text("Fixture-owned push before the second review wave.\n")
    subprocess.run(["git", "add", "fixture-push.txt"], check=True)
    subprocess.run(
        ["git", "commit", "--only", "-qm", "Fixture: advance review wave", "--", "fixture-push.txt"],
        check=True,
    )
    paths = [Path("pr-nits-2.json")]
else:
    paths = [Path("pr-state.json"), *sorted(Path(".").glob("pr-nits-*.json"))]

head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
for path in paths:
    state = json.loads(path.read_text())
    state["pullRequest"]["headRefOid"] = head
    for check in state["pullRequest"]["statusCheckRollup"]:
        check["headSha"] = head
    for thread in state["pullRequest"]["reviewThreads"]["nodes"]:
        for comment in thread["comments"]["nodes"]:
            comment["commit"]["oid"] = head
    path.write_text(json.dumps(state, indent=2) + "\n")
