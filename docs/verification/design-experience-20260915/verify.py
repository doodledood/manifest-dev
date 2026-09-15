#!/usr/bin/env python3
"""Check this pilot's frozen inputs, outputs and links; not a browser/design test."""

import gzip
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
SOURCE = Path("claude-plugins/manifest-dev/skills/design")
INPUTS = json.loads((ROOT / "inputs.json").read_text())


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def original(relative):
    return subprocess.check_output(
        ["git", "show", f"{INPUTS['baseline_commit']}:{SOURCE / relative}"],
        cwd=REPO,
    )


def package_file(arm, relative):
    if arm == "candidate":
        return (REPO / SOURCE / relative).read_bytes()
    if arm == "intermediate":
        archived = "core.md" if relative == "SKILL.md" else relative
        path = ROOT / "snapshots/intermediate" / archived
        if path.exists():
            return path.read_bytes()
        compressed = path.with_suffix(path.suffix + ".gz")
        if compressed.exists():
            return gzip.decompress(compressed.read_bytes())
    return original(relative)


for arm, files in INPUTS["packages"].items():
    for relative, expected in files.items():
        require(
            digest(package_file(arm, relative)) == expected,
            f"Input drift: {arm}/{relative}",
        )

for case, expected in INPUTS["briefs"].items():
    require(
        digest((ROOT / f"briefs/{case}.md").read_bytes()) == expected,
        f"Brief drift: {case}",
    )
require(
    digest((ROOT / "briefs/generation-contract.md").read_bytes())
    == INPUTS["generation_contract_sha256"],
    "Generation contract drift",
)

records = sorted((ROOT / "generation").glob("*.json"))
require(len(records) == 12, "Expected the twelve recorded generations")
expected_sample_targets = set()
for path in records:
    record = json.loads(path.read_text())
    name = record["sample"]
    require(name == path.stem, f"Generation identity mismatch: {path.name}")
    expected_sample_targets.add(f"samples/{name}.html")
    arm = name.rsplit("-", 1)[0]
    package = "baseline" if arm == "baseline-repeat" else arm
    data = (ROOT / f"samples/{name}.html").read_bytes()
    require(digest(data) == record["artifact_sha256"], f"Output drift: {name}")
    require(len(data) == record["artifact_bytes"], f"Byte count drift: {name}")
    require(
        record["skill_sha256"] == INPUTS["packages"][package]["SKILL.md"],
        f"Wrong skill: {name}",
    )
    require(
        record["generator_tools_used"] == ["read"],
        f"Unexpected generation capability: {name}",
    )
    require(not record["post_generation_edits"], f"Recorded output edit: {name}")
    require(
        digest(record["design_note"].encode("utf-8")) == record["design_note_sha256"],
        f"Design note drift: {name}",
    )
    words = len(package_file(package, "SKILL.md").decode().split())
    words += sum(
        len(package_file(package, ref).decode().split())
        for ref in record["references_read"]
    )
    print(f"{name}: hash intact; {words} instruction words read")


class GalleryLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        for key in ("href", "src"):
            if key in values:
                self.paths.append(values[key])


parser = GalleryLinks()
parser.feed((ROOT / "index.html").read_text())
for value in parser.paths:
    parts = urlsplit(value)
    require(
        not parts.scheme and not parts.netloc,
        f"Unexpected external gallery dependency: {value}",
    )
    if parts.path:
        require(
            (ROOT / unquote(parts.path)).exists(), f"Missing gallery target: {value}"
        )
    else:
        require(parts.fragment in parser.ids, f"Missing gallery anchor: {value}")
require(
    {p for p in parser.paths if p.startswith("samples/")} == expected_sample_targets,
    "Gallery sample targets must match the frozen generation inventory",
)

for doc in [ROOT / "README.md", *sorted((ROOT / "reviews").glob("*.md"))]:
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
        parts = urlsplit(target)
        if not parts.scheme and parts.path:
            require(
                (doc.parent / unquote(parts.path)).exists(),
                f"Missing link in {doc.name}: {target}",
            )
print("PASS: frozen identities, twelve outputs, gallery targets and report links")
