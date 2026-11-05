# Guard for the separate, explicitly Claude-native eval instrument only.
# General-agent drives do not use this provider marker or select a CLI.
model_host() {
  if [[ -n ${CLAUDECODE:-} ]]; then
    echo claude
  elif [[ -n ${CODEX_THREAD_ID:-} || -n ${CODEX_CI:-} ]]; then
    echo codex
  else
    echo claude
  fi
}
