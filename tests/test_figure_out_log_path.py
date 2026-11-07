"""figure-out's log and model paths are unique per session, not per second.

Sessions started in the same second — parallel agents, a run that launches several — once
shared `figure-out-log-{timestamp}.md` and its models folder, so two investigations appended to
one journal and saved over each other's models. The path rule now carries a random id beside the
timestamp, the file is created only where the path is free, and the models folder takes the
log's timestamp and id.
"""

from __future__ import annotations

import re
from pathlib import Path

LOG = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins"
    / "manifest-dev"
    / "skills"
    / "figure-out"
    / "references"
    / "LOG.md"
)


def test_log_and_models_paths_carry_an_id_beside_the_timestamp() -> None:
    text = re.sub(r"\s+", " ", LOG.read_text(encoding="utf-8"))
    paths = re.findall(r"`~/\.manifest-dev/(?:logs|models)/[^`]*`", text)
    assert paths, f"{LOG.name} names no log or models path"
    for path in paths:
        assert "{timestamp}-{id}" in path, (
            f"{LOG.name} names {path}; a timestamp alone collides between sessions started "
            "in the same second, so every log and models path carries `{timestamp}-{id}`"
        )
    assert (
        "only where that path does not exist yet" in text
    ), f"{LOG.name} must say the log is created only where its path is free"
