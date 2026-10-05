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
evals="$root/claude-plugins/manifest-dev/evals"
cli=$(sed -n 's/.*install.sh | bash -s -- \([0-9.]*\).*/\1/p' "$evals/Dockerfile")
image="manifest-dev-evals:$cli"

# The interactive-shell alias that launches Claude Code strips the key; read it from the profile.
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  ANTHROPIC_API_KEY=$(zsh -ic 'printf %s "$ANTHROPIC_API_KEY"' 2>/dev/null || true)
fi
[[ -n "${ANTHROPIC_API_KEY:-}" ]] || { echo "ANTHROPIC_API_KEY is not set" >&2; exit 1; }
export ANTHROPIC_API_KEY

docker info >/dev/null 2>&1 || colima start
docker image inspect "$image" >/dev/null 2>&1 || docker build -t "$image" "$evals"
mkdir -p "$(dirname "$root/claude-plugins/manifest-dev/$out")"

docker run -d --name "$name" --security-opt seccomp=unconfined --security-opt apparmor=unconfined \
  -e ANTHROPIC_API_KEY -v "$root":/work -w /work/claude-plugins/manifest-dev \
  "$image" claude plugin eval . --allow-tools Write Bash -j 8 --no-publish --trust-plugin \
  --json "$out" "$@"
echo "started $name — follow with: docker logs -f $name"
