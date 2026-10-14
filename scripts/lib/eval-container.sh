# The pinned container every model session this repository starts runs in: the eval image
# claude-plugins/manifest-dev/evals/Dockerfile defines, with its own home and no access to yours.
# Sourced by scripts/drive-skill.sh, scripts/walk.sh and scripts/evals/run_eval.sh.
#
# After sourcing with `root` set to the checkout: EVAL_IMAGE names the image; `eval_container_ready`
# starts Docker (colima on macOS) and builds the image when missing, and exits 3 (unreachable)
# when Docker is not there.
#
# The tag carries the Claude CLI version and a hash of the Dockerfile, so any change to the
# Dockerfile names a new image and is built, never served from an older one under the same tag.

eval_container_dockerfile="$root/claude-plugins/manifest-dev/evals/Dockerfile"
eval_container_cli=$(sed -n 's/.*install.sh | bash -s -- \([0-9.]*\).*/\1/p' "$eval_container_dockerfile")
EVAL_IMAGE="manifest-dev-evals:$eval_container_cli-$(git hash-object "$eval_container_dockerfile" | cut -c1-12)"

eval_container_ready() {
  command -v docker >/dev/null || { echo "unreachable — docker not found; install it (or colima on macOS)" >&2; exit 3; }
  docker info >/dev/null 2>&1 || colima start >/dev/null 2>&1 || { echo "unreachable — docker is not running" >&2; exit 3; }
  docker image inspect "$EVAL_IMAGE" >/dev/null 2>&1 || docker build -q -t "$EVAL_IMAGE" "$root/claude-plugins/manifest-dev/evals" >/dev/null
}
