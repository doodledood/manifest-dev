"""The ADR index is a rebuild of the records, byte for byte.

`docs/adr/CONVENTIONS.md` → *The index* says every column is derived from the records and a
rebuild produces the same bytes. Nothing checked it, so rows drifted whenever a record was
restatused without its row. This test is the rebuild: it fails with the rows that differ.
"""

from __future__ import annotations

import re
from pathlib import Path

ADR = Path(__file__).resolve().parent.parent / "docs" / "adr"
INDEX = ADR / "README.md"
HEADER = "# Architecture Decision Records\n\n| Date | ADR | Status | Area |\n|------|-----|--------|------|\n"
RECORD_NAME = re.compile(r"`?\[?(\d{8}-[a-z0-9-]+)\]?(?:\(\1\.md\))?`?")


def _field(text: str, heading: str, record: Path) -> str:
    match = re.search(rf"^## {heading}\n(.+)$", text, re.MULTILINE)
    assert match, f"{record.name} has no `## {heading}` line"
    return match.group(1).strip()


def rebuild() -> str:
    rows = []
    for record in sorted(
        p for p in ADR.glob("*.md") if p.name not in ("README.md", "CONVENTIONS.md")
    ):
        text = record.read_text(encoding="utf-8")
        title = re.search(r"^# ADR: (.+)$", text, re.MULTILINE)
        assert title, f"{record.name} has no `# ADR: ` heading"
        status = RECORD_NAME.sub(
            lambda m: f"[{m.group(1)}]({m.group(1)}.md)", _field(text, "Status", record)
        )
        date = f"{record.name[:4]}-{record.name[4:6]}-{record.name[6:8]}"
        rows.append(
            f"| {date} | [{title.group(1).strip()}]({record.name}) | {status} | "
            f"{_field(text, 'Area', record)} |"
        )
    return HEADER + "\n".join(rows) + "\n"


# Holds the decision in docs/adr/20260809-adr-index-is-derived-from-the-records.md.
def test_adr_index_equals_a_rebuild_from_the_records() -> None:
    expected = rebuild()
    actual = INDEX.read_text(encoding="utf-8")
    if actual == expected:
        return
    rows = [
        f"- {a}\n+ {e}"
        for a, e in zip(actual.splitlines(), expected.splitlines(), strict=False)
        if a != e
    ]
    raise AssertionError(
        "docs/adr/README.md differs from a rebuild of the records (CONVENTIONS.md → "
        "The index); rewrite it from the records:\n"
        + ("\n".join(rows[:10]) or "rows match; line endings or row count differ")
    )


STANDING_CHANGED_BY = re.compile(
    r"(?i)\b(?:superseded|narrowed|amended|replaced|retired|lifted)(?: in part)? by "
    r"\[?`?(\d{8}-[a-z0-9-]+)"
)


# Holds CONVENTIONS.md → *Immutability*: deleting a draft, or changing which records it
# supersedes, narrows or amends, gives back the Status each record had before it. A record's
# Status naming a record that is gone, or one that no longer names it back, is that restatus left
# behind — the old decision drops out of effect, from the index and the strategy list, with
# nothing in force replacing it.
def test_every_status_names_a_record_that_names_it_back() -> None:
    records = {
        p.stem: p.read_text(encoding="utf-8")
        for p in ADR.glob("*.md")
        if p.name not in ("README.md", "CONVENTIONS.md")
    }
    stale = []
    for name, text in sorted(records.items()):
        for later in STANDING_CHANGED_BY.findall(
            _field(text, "Status", ADR / f"{name}.md")
        ):
            if later not in records:
                stale.append(f"{name}: its Status names {later}, which does not exist")
            elif name not in records[later]:
                stale.append(
                    f"{name}: its Status names {later}, which never names it back"
                )
    assert not stale, (
        "a record's Status says a record changed its standing, but that record is gone or "
        "no longer names it; give the record back its earlier Status, or name it in the "
        "later record's Source:\n" + "\n".join(stale)
    )
