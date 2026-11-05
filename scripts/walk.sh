#!/usr/bin/env bash
# Prepare scratch inputs and record evidence for a host-owned general-agent walk task.
# The running host starts the agent; no installed CLI or provider marker selects execution.
# See scripts/NATIVE_DRIVES.md for dispatch, parent grading and approved fallback rules.
set -euo pipefail
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
exec python3 "$root/scripts/native_drive.py" walk "$@"
