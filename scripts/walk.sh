#!/usr/bin/env bash
# Walk one reader task: a fresh reader gets only the named documents and the task. Walk recipes'
# scenarios call it, and `scripts/verify walk` keeps what it prints as the evidence.
#
#   scripts/walk.sh '<task and what the reader should end able to do>' <document>... [--dry-run]
#
# The reader is a model session with no tools and no plugins, run directly by the claude CLI in
# an empty scratch directory outside this checkout, with no user settings and no MCP servers of
# yours (scripts/lib/claude-cli.sh has the flags), so no context file, setting or plugin of
# yours reaches it. The documents are given inline. It does the task from them alone and says
# where it got stuck or had to guess. Its reply, under the CLI version it ran on, is the
# evidence; a person reads it and records the verdict.
#
# --dry-run  Prints the session command and the CLI it would use; starts nothing.
#            VERIFY_DRY_RUN=1 (set by `scripts/verify walk --dry-run`) does the same.
#
# Needs: the claude CLI on PATH and signed in (`claude auth login`, or ANTHROPIC_API_KEY);
# exits 3 (unreachable) without it. Each walk is one model session and uses quota.
# MODEL selects the model (default: opus).
set -euo pipefail

usage() { sed -n '2,19p' "$0"; exit 2; }
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
# shellcheck source=lib/claude-cli.sh
source "$root/scripts/lib/claude-cli.sh"

dry=${VERIFY_DRY_RUN:-0} task="" docs=()
for arg in "$@"; do
  case $arg in
    --dry-run) dry=1 ;;
    *) if [[ -z $task ]]; then task=$arg; else docs+=("$arg"); fi ;;
  esac
done
[[ -n $task && ${#docs[@]} -gt 0 ]] || usage
model=${MODEL:-opus}

inline=""
for doc in "${docs[@]}"; do
  [[ -f $root/$doc ]] || { echo "walk: no document $doc; name it by its path from the checkout's root" >&2; exit 1; }
  inline+=$'\n\n'"=== $doc ==="$'\n'"$(cat "$root/$doc")"
done

if [[ $dry == 1 ]]; then
  echo "would walk: ${docs[*]}  model=$model"
  echo "session:    claude -p --model $model ${CLAUDE_ISOLATION[*]} --tools \"\" --no-session-persistence <task + documents>"
  echo "            in an empty scratch directory outside this checkout"
  echo "cli:        $(claude_cli_status)"
  echo "evidence:   printed; scripts/verify keeps it"
  exit 0
fi

claude_cli_ready walk

prompt="You are a reader who has never seen this project. Using only the documents below, do this task: $task

Then report: whether you ended able to do it (yes, partly, or no), the steps or facts you relied on, quoted with the section they came from, and every point where you got stuck or had to guess.
$inline"

scratch=$(mktemp -d "${TMPDIR:-/tmp}/manifest-dev-walk.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
echo "CLI: $CLAUDE_CLI_VERSION"
status=0
(cd "$scratch" && "${CLAUDE_SESSION_ENV[@]}" claude -p --model "$model" "${CLAUDE_ISOLATION[@]}" \
  --tools "" --no-session-persistence "$prompt") || status=$?
((status == 0)) || echo "walk: the reader session exited $status; read its output above for the cause, then rerun the walk" >&2
exit "$status"
