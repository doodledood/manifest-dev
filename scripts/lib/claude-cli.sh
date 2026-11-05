# The explicit Claude CLI instrument: the `claude` CLI on PATH, run
# directly in a scratch project outside the checkout. Used only by the approved Claude
# fallback instruments and the separate Claude-native eval suite.
#
# After sourcing:
#   claude_cli_ready <who>      exits 3 (a missing prerequisite), naming it and the next step,
#                               unless `claude` is on PATH and signed in and python3 is there;
#                               sets CLAUDE_CLI_VERSION. It starts no session.
#   claude_cli_status           prints the CLI version a dry run would use, or that none is there.
#   CLAUDE_ISOLATION            the flags that keep your own setup out of a session:
#                               `--setting-sources project,local` loads no user settings, so
#                               neither your settings, hooks nor the plugins they enable load;
#                               `--strict-mcp-config` loads no MCP server you configured.
#   CLAUDE_SESSION_ENV          the prefix a session starts under: your environment, less
#                               CLAUDECODE, which marks a session already running and would make
#                               this one a nested session of whatever launched the script.
#   copy_plugin <name> <dest>   copies claude-plugins/<name> to <dest>/<name> and prints the
#                               copy's path, so a session can never change the checkout's plugin;
#                               returns 1, saying why, when the copy fails.
#
# What `--setting-sources` does not cover is the CLI's to say: whether your personal memory file
# (~/.claude/CLAUDE.md) stays out is not stated by `claude --help`. The session uses your own
# sign-in, so a session's usage counts against your plan or key like any other.

# shellcheck disable=SC2034 # used by the scripts that source this file
CLAUDE_ISOLATION=(--setting-sources project,local --strict-mcp-config)
# shellcheck disable=SC2034
CLAUDE_SESSION_ENV=(env -u CLAUDECODE)

# An explicit adapter is not a host selector. The parent records the user's grant;
# a known foreign host cannot use this instrument as its same-host fallback.
require_claude_fallback() {
  local who=$1 approval=${MANIFEST_DEV_FALLBACK_APPROVAL:-}
  if [[ -z ${approval//[[:space:]]/} || ${MANIFEST_DEV_FALLBACK_HARNESS:-} != claude ]]; then
    echo "$who: unreachable — this Claude CLI fallback needs explicit user approval and MANIFEST_DEV_FALLBACK_HARNESS=claude; warn and ask what to do" >&2
    exit 3
  fi
  if [[ -z ${CLAUDECODE:-} && ( -n ${CODEX_THREAD_ID:-} || -n ${CODEX_CI:-} ) ]]; then
    echo "$who: unreachable — Claude is not the running host; a fallback must use the same harness, never switch providers" >&2
    exit 3
  fi
}

claude_cli_ready() {
  local who=$1 status
  command -v python3 >/dev/null || {
    echo "$who: unreachable — python3 is not on PATH; install Python 3 and rerun" >&2
    exit 3
  }
  command -v claude >/dev/null || {
    echo "$who: unreachable — the claude CLI is not on PATH; install Claude Code, sign in with \`claude auth login\`, and rerun" >&2
    exit 3
  }
  CLAUDE_CLI_VERSION=$(claude --version 2>/dev/null) || {
    echo "$who: unreachable — \`claude --version\` failed; reinstall the claude CLI and rerun" >&2
    exit 3
  }
  status=$(claude auth status --json 2>/dev/null || true)
  case $(printf '%s' "$status" | python3 -c 'import json,sys
try:
    print("yes" if json.load(sys.stdin).get("loggedIn") else "no")
except Exception:
    print("unknown")' 2>/dev/null) in
    yes) ;;
    no)
      echo "$who: unreachable — the claude CLI is not signed in; run \`claude auth login\` (or export ANTHROPIC_API_KEY) and rerun" >&2
      exit 3 ;;
    *)
      echo "$who: unreachable — could not read the sign-in state from \`claude auth status --json\`; update the claude CLI and rerun" >&2
      exit 3 ;;
  esac
}

claude_cli_status() {
  if ! command -v claude >/dev/null; then
    echo "not on PATH — the run would stop as unreachable"
  else
    echo "$(claude --version 2>/dev/null || echo 'version unknown') (sign-in is checked when it runs)"
  fi
}

copy_plugin() {
  local name=$1 dest=$2
  # Called inside $(...), where set -e does not reach: the caller adds `|| exit 3`.
  mkdir -p "$dest" && cp -R "$root/claude-plugins/$name" "$dest/" || {
    echo "${0##*/}: unreachable — could not copy claude-plugins/$name to $dest; free disk space or fix its permissions and rerun" >&2
    return 1
  }
  # Local eval results can be large and are never part of the plugin.
  rm -rf "$dest/$name/evals/results"
  printf '%s\n' "$dest/$name"
}

# Keep ownership of the foreground model process until it is reaped. A process-group
# stop reaches parent and child together; without a trap the parent can exit first,
# leaving the terminated child as a zombie on hosts whose init does not reap it.
stop_claude_session() {
  trap '' TERM INT
  local child_pid
  for child_pid in $(jobs -p); do
    kill -TERM "$child_pid" 2>/dev/null || true
  done
  wait 2>/dev/null || true
  exit "$1"
}

run_claude_session() {
  local session_dir=$1 session_pid session_status=0
  shift
  trap 'stop_claude_session 143' TERM
  trap 'stop_claude_session 130' INT
  (cd "$session_dir" && exec "$@") &
  session_pid=$!
  wait "$session_pid" || session_status=$?
  trap - TERM INT
  return "$session_status"
}
