#!/usr/bin/env bash
# Prepare scratch inputs and record evidence for a host-owned general-agent walk task.
# The running host starts the agent; no installed CLI or provider marker selects execution.
# See scripts/NATIVE_DRIVES.md for dispatch, parent grading and approved fallback rules.
set -euo pipefail
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
# Use the project runtime after setup; a system Python may be older than the helper.
native_python="$root/.venv/bin/python"
[[ -x "$native_python" ]] || native_python=python3
exec "$native_python" "$root/scripts/native_drive.py" walk "$@"
