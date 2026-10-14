# Resolve the credential a headless Claude Code run inside a container uses.
# Sourced by scripts/features/drive.sh and scripts/evals/run_eval.sh — one place for the rule.
#
# Two credentials exist:
#   - a Claude subscription: run `claude setup-token` once and export the token it prints as
#     CLAUDE_CODE_OAUTH_TOKEN (the container cannot read the macOS keychain your login lives in).
#     Anthropic documents this token for scripts and CI with the unmodified Claude Code CLI, used
#     by the subscriber themselves; its limits assume ordinary individual use.
#   - an API key: export ANTHROPIC_API_KEY. Required for heavy automated volume such as a full
#     eval suite, since the Consumer Terms allow other automated access only via an API key.
# Each is read from the environment, then from the interactive shell profile. With both present,
# the subscription token is used unless the caller asks for --api-key-only. Only the chosen one
# is passed to the container, so the CLI inside never has to pick between two.
#
# After sourcing, call `claude_auth_resolve [--api-key-only]`; it sets CLAUDE_AUTH_ENV to the
# variable name to pass with `docker run -e "$CLAUDE_AUTH_ENV"`, exports that variable, and fails
# with instructions when no allowed credential is available.

claude_auth_from_profile() {
  zsh -ic "printf %s \"\${$1:-}\"" 2>/dev/null || true
}

claude_auth_resolve() {
  local key_only=0 token="" key=${ANTHROPIC_API_KEY:-}
  [[ ${1:-} == --api-key-only ]] && key_only=1
  if [[ $key_only == 0 ]]; then
    token=${CLAUDE_CODE_OAUTH_TOKEN:-}
    [[ -n $token || -n $key ]] || token=$(claude_auth_from_profile CLAUDE_CODE_OAUTH_TOKEN)
  fi
  [[ -n $token || -n $key ]] || key=$(claude_auth_from_profile ANTHROPIC_API_KEY)
  unset CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_API_KEY
  if [[ -n $token ]]; then
    export CLAUDE_CODE_OAUTH_TOKEN=$token
    CLAUDE_AUTH_ENV=CLAUDE_CODE_OAUTH_TOKEN
  elif [[ -n $key ]]; then
    export ANTHROPIC_API_KEY=$key
    CLAUDE_AUTH_ENV=ANTHROPIC_API_KEY
  elif [[ $key_only == 1 ]]; then
    echo "this run needs an API key: export ANTHROPIC_API_KEY=<key>" >&2
    echo "  (a full eval suite is heavy automated use, which a Claude subscription does not cover)" >&2
    return 1
  else
    echo "no Claude credential found. Use either:" >&2
    echo "  - a Claude subscription: run \`claude setup-token\` and export CLAUDE_CODE_OAUTH_TOKEN=<token>" >&2
    echo "  - an API key: export ANTHROPIC_API_KEY=<key>" >&2
    return 1
  fi
}
