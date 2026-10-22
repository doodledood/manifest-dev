"""orchestrate's status page: one self-contained template, and a reference that documents what it reads.

The template is copied unchanged into other people's hosts and opened as a local file, so it must stand alone:
a full document in standards mode, nothing loaded from the network, and exactly one data block that the
orchestrator rewrites. The reference and the template describe the same data, and these tests fail when a field,
a status or a phase exists on one side only.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "claude-plugins" / "manifest-dev" / "skills" / "orchestrate"
TEMPLATE = SKILL / "assets" / "status-page.html"
REFERENCE = SKILL / "references" / "STATUS_PAGE.md"
DATA_BLOCK = re.compile(
    r'<script type="application/json" id="orchestrate-status">(.*?)</script>', re.S
)


def template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def reference() -> str:
    return REFERENCE.read_text(encoding="utf-8")


def script() -> str:
    blocks: list[str] = re.findall(r"<script>(.*?)</script>", template(), re.S)
    assert len(blocks) == 1, "the template should carry one inline script"
    return blocks[0]


def sample() -> dict[str, Any]:
    blocks = DATA_BLOCK.findall(template())
    assert len(blocks) == 1, "the template should read exactly one data block"
    data = json.loads(blocks[0])
    assert isinstance(data, dict)
    return data


def declared(name: str, code: str) -> str:
    """The body of the template's `var NAME = {...};` or `var NAME = [...];` table."""
    found = re.search(rf"var {name} = [{{[](.*?)[}}\]];", code, re.S)
    assert found, f"the template no longer declares {name}"
    return found.group(1)


def keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {k for v in value.values() for k in keys(v)}
    if isinstance(value, list):
        return {k for v in value for k in keys(v)}
    return set()


def documented_fields() -> set[str]:
    fields = reference().split("## Fields", 1)[1]
    before, _, after = fields.partition("### Statuses")
    fields = before + after.split("###", 1)[-1]
    names = re.findall(r"^\| `([a-zA-Z.]+)` \|", fields, re.M)
    return {part for name in names for part in name.split(".")}


def test_template_is_a_standalone_document_in_standards_mode() -> None:
    text = template()
    assert text.lower().startswith("<!doctype html>")
    assert '<meta charset="utf-8">' in text


def test_template_loads_nothing_from_the_network() -> None:
    text = template()
    offenders = [
        pattern
        for pattern in (
            r"<script[^>]*\bsrc\s*=",
            r"<link\b",
            r"@import",
            r"url\(\s*['\"]?(?:https?:)?//",
            r"<(?:img|iframe|video|audio|source)\b[^>]*\bsrc\s*=\s*['\"](?:https?:)?//",
        )
        if re.search(pattern, text, re.I)
    ]
    assert not offenders, f"the template loads from the network: {offenders}"


def test_template_links_only_to_http_addresses() -> None:
    assert "/^https?:\\/\\//i.test(url)" in script()


def test_sample_data_is_marked_as_an_example_of_schema_1() -> None:
    data = sample()
    assert data["schema"] == 1
    assert data["example"] is True


def test_reference_documents_every_field_the_sample_carries() -> None:
    missing = keys(sample()) - documented_fields() - {"example"}
    assert not missing, f"fields the reference does not document: {sorted(missing)}"


def test_template_reads_every_field_the_reference_documents() -> None:
    code = script()
    unread = {f for f in documented_fields() if f".{f}" not in code}
    assert not unread, f"documented fields the template never reads: {sorted(unread)}"


def test_reference_documents_every_status_and_phase_the_template_knows() -> None:
    code = script()
    statuses = set(re.findall(r"(\w+):", declared("TONE", code)))
    phases = set(re.findall(r'\["(\w+)", "', declared("PHASES", code)))
    text = reference()
    status_table = text.split("### Statuses", 1)[1].split("###", 1)[0]
    documented_statuses = set(re.findall(r"^\| `(\w+)` \|", status_table, re.M))
    assert statuses == documented_statuses
    assert all(f"`{p}`" in text for p in phases), phases


def test_reference_names_the_data_block_and_the_live_sources_the_template_reads() -> (
    None
):
    text, code = reference(), script()
    for name in ("orchestrate-status.json", "orchestrate-status.js", "status/current"):
        assert name in text and name in code, name
    assert 'id="orchestrate-status"' in text
    assert "window.ORCHESTRATE_STATUS" in text and "window.ORCHESTRATE_STATUS" in code


def validate(snapshot: dict[str, Any]) -> bool:
    """The template's own `valid()`, run in Node on one snapshot."""
    code = script()
    tables = "\n".join(
        re.search(rf"var {name} = .*?;\n", code, re.S).group(0)  # type: ignore[union-attr]
        for name in ("PHASES", "TONE", "TYPE_NAME")
    )
    start = code.index("  function strings(")
    end = code.index("  function apply(")
    program = (
        tables + code[start:end] + "process.stdout.write(String(valid(JSON.parse("
        "require('fs').readFileSync(0, 'utf8')))));"
    )
    done = subprocess.run(
        ["node", "-e", program],
        input=json.dumps(snapshot),
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return done.stdout == "true"


def test_the_sample_snapshot_is_valid() -> None:
    assert validate(sample())


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("plan",), None),
        (("plan",), "3"),
        (("mode",), "fast"),
        (("state",), "stopped"),
        (("tickets", 0, "status"), "done"),
        (("tickets", 0, "status"), ["running"]),
        (("tickets", 0, "phase"), "review"),
        (("tickets", 0, "kind"), "chore"),
        (("tickets", 0, "auto"), True),
        (("needsYou", 0, "pick"), 1),
        (("needsYou", 0, "risk"), ["low"]),
        (("needsYou", 0, "evidence"), {"gates": 14}),
        (("tickets", 0, "summary"), 7),
        (("tickets", 0, "why"), ["a", "b"]),
        (("tickets", 0, "foundWhile"), {"run": "#132"}),
        (("tickets", 0, "done"), "it works"),
        (("tickets", 0, "done"), ["it works", 2]),
        (("tickets", 0, "change"), "before and after"),
        (("tickets", 0, "change"), {"before": "a"}),
        (("tickets", 0, "change"), {"after": "b"}),
        (("tickets", 0, "change"), {"before": "a", "after": 2}),
        (("tickets", 0, "type"), "epic"),
    ],
)
def test_a_snapshot_outside_the_schema_is_refused(
    path: tuple[str | int, ...], value: object
) -> None:
    # Data is untyped input, and the page renders whatever valid() lets in; a value the reference
    # does not allow keeps the last good view instead.
    snapshot = sample()
    target: Any = snapshot
    for step in path[:-1]:
        target = target[step]
    target[path[-1]] = value
    assert not validate(snapshot), path


@pytest.mark.parametrize("field", ["pick", "risk", "evidence"])
def test_a_waiting_item_without_its_recommendation_risk_or_evidence_is_still_valid(
    field: str,
) -> None:
    # The fields help the person decide; an orchestrator that has none to give still shows the item.
    snapshot = sample()
    assert (
        field in snapshot["needsYou"][0]
    ), f"the sample's first waiting item lost `{field}`"
    del snapshot["needsYou"][0][field]
    assert validate(snapshot)


NEW_TICKET_FIELDS = ("summary", "why", "change", "done", "type", "foundWhile")


@pytest.mark.parametrize("field", NEW_TICKET_FIELDS)
def test_a_ticket_without_one_explanation_field_is_still_valid(field: str) -> None:
    # Each field explains the Ticket to a person; an orchestrator with nothing to derive it from
    # leaves it out, and the page still shows the Ticket.
    snapshot = sample()
    carriers = [t for t in snapshot["tickets"] if field in t]
    assert carriers, f"no Ticket in the sample carries `{field}`"
    for ticket in carriers:
        del ticket[field]
    assert validate(snapshot)


def test_a_snapshot_written_before_the_explanation_fields_is_still_valid() -> None:
    # Orchestrators already running write schema-1 snapshots without these fields.
    snapshot = sample()
    for ticket in snapshot["tickets"]:
        for field in NEW_TICKET_FIELDS:
            ticket.pop(field, None)
    assert snapshot["schema"] == 1
    assert validate(snapshot)


def test_the_page_names_every_ticket_type_the_reference_documents() -> None:
    names = set(re.findall(r"(\w+):", declared("TYPE_NAME", script())))
    row = re.search(r"^\| `type` \| (.*?) \|", reference(), re.M)
    assert row, "STATUS_PAGE.md no longer documents `type`"
    assert names == set(re.findall(r'`"(\w+)"`', row.group(1)))
