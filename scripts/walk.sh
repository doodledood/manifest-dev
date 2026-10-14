#!/usr/bin/env bash
# Walk one reader task: a fresh reader gets only the named documents and the task. Walk recipes'
# scenarios call it, and `scripts/verify walk` keeps what it prints as the evidence.
#
#   scripts/walk.sh '<task and what the reader should end able to do>' <document>... [--dry-run]
#
# The reader is a model session with no tools and no plugins, in the pinned eval container with
# its own home, so no context file, memory or setting of yours reaches it. The documents are
# given inline. It does the task from them alone and says where it got stuck or had to guess. Its
# reply is the evidence; a person reads it and records the verdict with `scripts/verify judge`.
#
# --dry-run  Prints the container command and the credential it would use; starts nothing.
#            VERIFY_DRY_RUN=1 (set by `scripts/verify walk --dry-run`) does the same.
#
# Needs: docker (colima on macOS) and a Claude credential, resolved as scripts/lib/claude-auth.sh
# says; exits 3 (unreachable) without them. Each walk is one model session and uses quota.
# MODEL selects the model (default: opus).
set -euo pipefail

usage() { sed -n '2,17p' "$0"; exit 2; }
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
# shellcheck source=lib/eval-container.sh
source "$root/scripts/lib/eval-container.sh"
# shellcheck source=lib/claude-auth.sh
source "$root/scripts/lib/claude-auth.sh"

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
  [[ -f $root/$doc ]] || { echo "walk: no document $doc" >&2; exit 1; }
  inline+=$'\n\n'"=== $doc ==="$'\n'"$(cat "$root/$doc")"
done

if [[ $dry == 1 ]]; then
  credential=$( (claude_auth_resolve && echo "$CLAUDE_AUTH_ENV") 2>/dev/null) ||
    credential="none found — the walk would stop as unreachable"
  echo "would walk: ${docs[*]}  model=$model"
  echo "container:  docker run --rm -e <credential> $EVAL_IMAGE"
  echo "            claude -p --model $model --tools \"\" --no-session-persistence <task + documents>"
  echo "credential: $credential"
  echo "evidence:   printed; scripts/verify keeps it"
  exit 0
fi

eval_container_ready
claude_auth_resolve || { echo "walk: unreachable — set a Claude credential (see above)" >&2; exit 3; }

prompt="You are a reader who has never seen this project. Using only the documents below, do this task: $task

Then report: whether you ended able to do it (yes, partly, or no), the steps or facts you relied on, quoted with the section they came from, and every point where you got stuck or had to guess.
$inline"

docker run --rm -e "$CLAUDE_AUTH_ENV" -e PROMPT="$prompt" -e MODEL="$model" "$EVAL_IMAGE" bash -c '
  cd "$(mktemp -d)" && claude -p --model "$MODEL" --tools "" --no-session-persistence "$PROMPT"'
