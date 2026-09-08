#!/usr/bin/env python3
"""PreToolUse hook: substitute {{INLINE_MANIFEST:<path>}} markers
in Task/Agent tool prompts with the literal file content at that path.

Reads the hook input JSON on stdin (per Claude Code's PreToolUse contract),
and if tool_name is Task/Agent and tool_input.prompt contains the marker,
emits an `updatedInput` with the marker replaced by the file's exact bytes.
Passes through untouched (exit 0, no output) otherwise.
"""

import json
import re
import sys

MARKER_RE = re.compile(r"\A\{\{INLINE_MANIFEST:([^}]+)\}\}")


def main():
    payload = json.load(sys.stdin)
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    prompt = tool_input.get("prompt")

    if tool_name not in ("Task", "Agent") or not prompt:
        return  # passthrough, no output

    m = MARKER_RE.search(prompt)
    if not m:
        return  # no marker present, passthrough

    snapshot_path = m.group(1)
    try:
        with open(snapshot_path) as f:
            manifest_text = f.read()
    except OSError as e:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"inline_manifest_hook: cannot read snapshot {snapshot_path}: {e}",
                    }
                }
            )
        )
        return

    new_prompt = MARKER_RE.sub(lambda _: manifest_text, prompt, count=1)
    merged_input = {**tool_input, "prompt": new_prompt}
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "updatedInput": merged_input,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
