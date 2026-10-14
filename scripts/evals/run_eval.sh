#!/usr/bin/env bash
# Run a plugin eval suite in the pinned Linux container, detached, writing its JSON result.
#
#   scripts/evals/run_eval.sh <name> <out-json> [extra `claude plugin eval` flags...]
#
# <name>      container name; also how you follow it: `docker logs -f <name>`, `docker wait <name>`
# <out-json>  result path relative to claude-plugins/manifest-dev, e.g.
#             evals/results/hillclimb-define/v2/aggregate-result.json
#
# Example, one hill-climb round (plugin arm only, the define suite's opus judge):
#   scripts/evals/run_eval.sh define-hc-v2 evals/results/hillclimb-define/v2/aggregate-result.json \
#     --tag define --ablation none --judge-model opus
#
# Why a container: on macOS every eval child raises a "Keychain Not Found" dialog (see
# evals/README.md), and a detached container survives the launching session ending. The
# working tree is mounted live, so leave the prompts under test untouched until it exits.
set -euo pipefail

[[ $# -ge 2 ]] || { sed -n '2,13p' "$0"; exit 2; }
name=$1 out=$2
shift 2

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
# shellcheck source=../lib/eval-container.sh
source "$root/scripts/lib/eval-container.sh"

# A Claude subscription token (`claude setup-token`) when one is set, otherwise an API key.
# shellcheck source=../lib/claude-auth.sh
source "$root/scripts/lib/claude-auth.sh"
claude_auth_resolve || exit 1
[[ $CLAUDE_AUTH_ENV == CLAUDE_CODE_OAUTH_TOKEN ]] &&
  echo "run_eval: using your Claude subscription; a full suite is many sessions and counts against its usage limits" >&2

eval_container_ready
mkdir -p "$(dirname "$root/claude-plugins/manifest-dev/$out")"

docker run -d --name "$name" --security-opt seccomp=unconfined --security-opt apparmor=unconfined \
  -e "$CLAUDE_AUTH_ENV" -v "$root":/work -w /work/claude-plugins/manifest-dev \
  "$EVAL_IMAGE" claude plugin eval . --allow-tools Write Bash -j 8 --no-publish --trust-plugin \
  --json "$out" "$@"
echo "started $name — follow with: docker logs -f $name"
