#!/usr/bin/env python3
"""
General-purpose adapter: runs a Claude Code hook and translates output to Gemini format.

Usage: python gemini_adapter.py <path-to-claude-hook>

Input: Gemini hook JSON on stdin (compatible with Claude Code input format)
Output: Gemini-format JSON on stdout

Translation:
- hookSpecificOutput.permissionDecision: "deny" -> decision: "deny"
- hookSpecificOutput.permissionDecisionReason -> reason
- hookSpecificOutput.additionalContext -> systemMessage
- continue field passed through
"""

import json
import sys
import subprocess


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: gemini_adapter.py <claude-hook-path>", file=sys.stderr)
        sys.exit(1)

    claude_hook = sys.argv[1]
    stdin_data = sys.stdin.read()

    result = subprocess.run(
        [sys.executable, claude_hook],
        input=stdin_data,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        sys.exit(result.returncode)

    if not result.stdout.strip():
        sys.exit(0)

    try:
        claude_output = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.exit(0)

    hook_specific = claude_output.get("hookSpecificOutput", {})
    gemini_output = {}

    if hook_specific.get("permissionDecision") == "deny":
        gemini_output["decision"] = "deny"
        gemini_output["reason"] = hook_specific.get("permissionDecisionReason", "")

    if "additionalContext" in hook_specific:
        gemini_output["systemMessage"] = hook_specific["additionalContext"]

    # Pass through top-level fields that are already Gemini-compatible
    for key in ("decision", "reason", "systemMessage", "continue"):
        if key in claude_output and key not in gemini_output:
            gemini_output[key] = claude_output[key]

    if gemini_output:
        print(json.dumps(gemini_output))

    sys.exit(0)


if __name__ == "__main__":
    main()
