# Select the model interface of the session driving the check. A nested Claude
# session has its own marker even when its parent was Codex. A standalone shell
# retains the existing Claude driver; mere CLI availability never changes hosts.
model_host() {
  if [[ -n ${CLAUDECODE:-} ]]; then
    echo claude
  elif [[ -n ${CODEX_THREAD_ID:-} || -n ${CODEX_CI:-} ]]; then
    echo codex
  else
    echo claude
  fi
}
