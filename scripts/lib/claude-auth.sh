# Resolve the credential a headless Claude Code run inside a container uses.
# Sourced by scripts/features/drive.sh and scripts/evals/run_eval.sh — one place for the rule.
#
# Two credentials exist:
#   - a Claude subscription: run `claude setup-token` once and export the token it prints as
#     CLAUDE_CODE_OAUTH_TOKEN (the container cannot read the macOS keychain your login lives in).
#     Anthropic documents this token for scripts and CI with the unmodified Claude Code CLI; usage
#     counts against the subscription's limits.
#   - an API key: export ANTHROPIC_API_KEY.
# Each is read from the environment, then from the interactive shell profile. With both present,
# the subscription token is used. Only the chosen one is passed to the container, so the CLI
# inside never has to pick between two.
#
# After sourcing, call `claude_auth_resolve`; it sets CLAUDE_AUTH_ENV to the variable name to pass
# with `docker run -e "$CLAUDE_AUTH_ENV"`, exports that variable, and fails with instructions when
# neither is available.

claude_auth_from_profile() {
  zsh -ic "printf %s \"\${$1:-}\"" 2>/dev/null || true
}

claude_auth_resolve() {
  local token=${CLAUDE_CODE_OAUTH_TOKEN:-} key=${ANTHROPIC_API_KEY:-}
  [[ -n $token || -n $key ]] || {
    token=$(claude_auth_from_profile CLAUDE_CODE_OAUTH_TOKEN)
    [[ -n $token ]] || key=$(claude_auth_from_profile ANTHROPIC_API_KEY)
  }
  unset CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_API_KEY
  if [[ -n $token ]]; then
    export CLAUDE_CODE_OAUTH_TOKEN=$token
    CLAUDE_AUTH_ENV=CLAUDE_CODE_OAUTH_TOKEN
  elif [[ -n $key ]]; then
    export ANTHROPIC_API_KEY=$key
    CLAUDE_AUTH_ENV=ANTHROPIC_API_KEY
  else
    echo "no Claude credential found. Use either:" >&2
    echo "  - a Claude subscription: run \`claude setup-token\` and export CLAUDE_CODE_OAUTH_TOKEN=<token>" >&2
    echo "  - an API key: export ANTHROPIC_API_KEY=<key>" >&2
    return 1
  fi
}
