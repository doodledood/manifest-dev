"""The ticket protocol model quotes the prose it models, and every quote still stands there.

`verification/models/ticket-protocol/TicketProtocol.tla` models the unattended Ticket protocol
that `orchestrate`, `run-ticket` and ticket-up's references state in prose. Each action and
property carries the sentences it encodes as `\\* Quote <file>: "<sentence>"` comments. A change
to the prose that drops or rewords a quoted sentence fails here, naming the file and the quote,
so the model is updated in the same change. An action that models the world rather than the
protocol carries a `\\* World:` comment instead; a branch that restores an old behavior carries
`\\* Pre-fix:` and quotes nothing, since the text it described is gone on purpose.

Holds the decision in docs/adr/20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes.md.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "verification" / "models" / "ticket-protocol"
MODEL = MODEL_DIR / "TicketProtocol.tla"
SKILLS = ROOT / "claude-plugins" / "manifest-dev" / "skills"

QUOTE = re.compile(r'^\s*\\\* Quote (?P<path>\S+): "(?P<text>.+)"\s*$')
MARK = re.compile(r"^\s*\\\* (Quote \S+:|World:|Pre-fix:)")
DEFINITION = re.compile(r"^(?P<name>[A-Z][A-Za-z]*)(\([^)]*\))?\s*==")


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _model_lines() -> list[str]:
    return MODEL.read_text(encoding="utf-8").splitlines()


def _quotes() -> list[tuple[int, str, str]]:
    return [
        (number, match["path"], match["text"])
        for number, line in enumerate(_model_lines(), start=1)
        if (match := QUOTE.match(line))
    ]


def _comment_block_above(lines: list[str], index: int) -> list[str]:
    block = []
    i = index - 1
    while i >= 0 and lines[i].lstrip().startswith("\\*"):
        block.append(lines[i])
        i -= 1
    return block


def _definitions() -> dict[str, list[str]]:
    lines = _model_lines()
    return {
        match["name"]: _comment_block_above(lines, index)
        for index, line in enumerate(lines)
        if (match := DEFINITION.match(line))
    }


def _next_actions() -> set[str]:
    text = MODEL.read_text(encoding="utf-8")
    body = re.search(r"^Next ==\n(?P<body>(?:[ \t]+.*\n)+)", text, re.MULTILINE)
    assert body, "TicketProtocol.tla has no Next definition"
    return set(re.findall(r"(?<!\\)\b([A-Z][A-Za-z]*)\b", body["body"])) - {"Orchs"}


def _checked_properties() -> set[str]:
    names: set[str] = set()
    for cfg in MODEL_DIR.glob("*.cfg"):
        for line in cfg.read_text(encoding="utf-8").splitlines():
            if match := re.match(r"^(INVARIANTS|PROPERTIES)\s+(?P<names>.+)$", line):
                names.update(match["names"].split())
    return names


def test_the_model_quotes_the_prose_it_models() -> None:
    quotes = _quotes()
    assert len(quotes) >= 20, "the Quote comments in TicketProtocol.tla were not found"


def test_every_quote_mark_carries_a_whole_quoted_sentence() -> None:
    """A Quote mark the quote pattern cannot read would count as marked yet check nothing."""
    unreadable = [
        f"TicketProtocol.tla:{number}: {line.strip()}"
        for number, line in enumerate(_model_lines(), start=1)
        if re.match(r"^\s*\\\* Quote ", line) and not QUOTE.match(line)
    ]
    assert not unreadable, "\n".join(unreadable)


def test_the_recipe_covers_every_file_the_model_quotes() -> None:
    """`verify affected` selects the recipe only for paths its `covers:` line names."""
    recipe = (ROOT / "verification" / "recipes" / "ticket-protocol-model.md").read_text(
        encoding="utf-8"
    )
    covers_line = re.search(r"^covers: (?P<paths>.+)$", recipe, re.MULTILINE)
    assert covers_line, "ticket-protocol-model.md has no covers: line"
    covers = {path.strip() for path in covers_line["paths"].split(",")}
    quoted = {f"claude-plugins/manifest-dev/skills/{path}" for _, path, _ in _quotes()}
    assert not quoted - covers, f"covers: misses {sorted(quoted - covers)}"


def test_every_quoted_sentence_still_stands_in_its_file() -> None:
    missing = []
    for number, path, text in _quotes():
        source = SKILLS / path
        if not source.is_file():
            missing.append(f"TicketProtocol.tla:{number}: {path} does not exist")
            continue
        if _normalize(text) not in _normalize(source.read_text(encoding="utf-8")):
            missing.append(
                f'TicketProtocol.tla:{number}: {path} no longer says "{text}"'
            )
    assert not missing, (
        "The protocol prose changed under the model. Update the model's action and its quote "
        "in the same change, then run `scripts/verify drive ticket-protocol-model`:\n"
        + "\n".join(missing)
    )


def test_every_action_and_checked_property_says_what_it_models() -> None:
    definitions = _definitions()
    unmarked = []
    for name in sorted(_next_actions() | _checked_properties()):
        if name not in definitions:
            unmarked.append(f"{name}: not defined in TicketProtocol.tla")
        elif not any(MARK.match(line) for line in definitions[name]):
            unmarked.append(
                f"{name}: no Quote, World: or Pre-fix: comment directly above it"
            )
    assert not unmarked, "\n".join(unmarked)


def test_the_marks_check_the_model_rather_than_nothing() -> None:
    actions = _next_actions()
    assert {"OClaim", "OLand", "RPush", "WTimeout", "WAnswer"} <= actions
    assert {
        "OneAttemptRecord",
        "ReadyResolves",
        "NoLandWhileEscalated",
    } <= _checked_properties()


def test_java_home_with_an_unusable_launcher_reports_unreachable(
    tmp_path: Path,
) -> None:
    """macOS's launcher can exist without a JDK; presence alone is not capability."""
    import os
    import subprocess

    jdk = tmp_path / "jdk"
    (jdk / "bin").mkdir(parents=True)
    marker = tmp_path / "version-called"
    launcher = jdk / "bin/java"
    launcher.write_text('#!/bin/sh\nprintf "%s" "$1" > "$JAVA_PROBE_MARKER"\nexit 1\n')
    launcher.chmod(0o755)
    result = subprocess.run(
        ["bash", str(MODEL_DIR / "check.sh"), "races"],
        env={**os.environ, "JAVA_HOME": str(jdk), "JAVA_PROBE_MARKER": str(marker)},
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert marker.read_text() == "-version"
    assert result.returncode == 3
    assert "missing: a Java runtime" in result.stderr
    assert "TLC exited" not in result.stderr
