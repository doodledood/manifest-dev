#!/usr/bin/env bash
# Drive one skill recipe headless and isolated. Skill recipes' scenarios call it, and
# `scripts/verify drive` keeps what it prints as the evidence.
#
#   scripts/drive-skill.sh preflight
#   scripts/drive-skill.sh doctor
#   scripts/drive-skill.sh <feature> <prompt-file> [--scaffold <eval-case-dir>]
#                          [--tools] [--max-turns N] [--dry-run]
#
# preflight  Free: checks Docker, the image and a credential, and starts no session.
#            `scripts/verify doctor` runs it.
# doctor     Starts one throwaway session and checks it loaded the plugins and their skills.
#            Exit 0 = worth driving; exit 1 names what is missing. Uses model quota.
# <feature>  The recipe's file name in verification/recipes/ without `.md` (e.g. figure-out).
# <prompt>   A file holding the prompt, exactly as a user would type it.
# --scaffold Builds the scratch project from an eval case's scaffold.sh before the prompt.
# --tools    Also loads claude-plugins/manifest-dev-tools (its skills' entries need it).
# --dry-run  Prints the container command, the credential it would use and where evidence would
#            go; starts nothing. VERIFY_DRY_RUN=1 (set by `scripts/verify drive --dry-run`) does
#            the same.
#
# Isolation: the session runs in the pinned eval container (claude-plugins/manifest-dev/evals/
# Dockerfile) with its own home and a scratch project, the checkout mounted read-only. Nothing
# reads or writes your ~/.manifest-dev, and the container is removed when the drive ends.
#
# Evidence: the full transcript, the scratch project and the session's ~/.manifest-dev are kept
# under ${MANIFEST_DEV_FEATURES_EVIDENCE:-$HOME/.local/state/manifest-dev-features}/<feature>/<stamp>/
# (outside the checkout, so `git clean` never touches it), and a summary — prompt, loaded
# plugins and skills, final reply with local paths removed, files written — is printed, which
# `scripts/verify` keeps as the committed evidence. A drive whose session did not load the
# plugin or the skill exits 3 (unreachable) and is not counted.
#
# Needs: docker (colima on macOS), and a Claude credential — a subscription token from
# `claude setup-token` in CLAUDE_CODE_OAUTH_TOKEN, or an API key in ANTHROPIC_API_KEY
# (scripts/lib/claude-auth.sh says which is used).
# MODEL selects the model (default: opus).
set -euo pipefail

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
# shellcheck source=lib/eval-container.sh
source "$root/scripts/lib/eval-container.sh"
# shellcheck source=lib/claude-auth.sh
source "$root/scripts/lib/claude-auth.sh"
image=$EVAL_IMAGE
model=${MODEL:-opus}
store=${MANIFEST_DEV_FEATURES_EVIDENCE:-$HOME/.local/state/manifest-dev-features}

usage() { sed -n '2,21p' "$0"; exit 2; }
die() { echo "drive: $*" >&2; exit 1; }
unreachable() { echo "drive: unreachable — $*" >&2; exit 3; }

[[ $# -ge 1 ]] || usage
feature=$1; shift
prompt_file="" scaffold="" tools=0 max_turns=40 dry=${VERIFY_DRY_RUN:-0}
if [[ $feature == preflight ]]; then
  eval_container_ready
  claude_auth_resolve || unreachable "set a Claude credential (see above)"
  echo "preflight: ok — docker is up, $image is built, credential: $CLAUDE_AUTH_ENV"
  exit 0
fi
if [[ $feature != doctor ]]; then
  [[ $# -ge 1 ]] || usage
  prompt_file=$1; shift
  [[ -f $root/verification/recipes/$feature.md ]] || die "no recipe verification/recipes/$feature.md"
  [[ -f $prompt_file ]] || die "no prompt file $prompt_file"
fi
while [[ $# -gt 0 ]]; do
  case $1 in
    --scaffold) scaffold=$2; shift 2 ;;
    --tools) tools=1; shift ;;
    --max-turns) max_turns=$2; shift 2 ;;
    --dry-run) dry=1; shift ;;
    *) die "unknown option $1 (see --help at the top of this file)" ;;
  esac
done
if [[ -n $scaffold ]]; then
  [[ -f $scaffold/scaffold.sh ]] || die "no scaffold.sh in $scaffold"
  scaffold=$(cd "$scaffold" && pwd -P)
  case $scaffold in "$root"/*) ;; *) die "scaffold must be inside this checkout" ;; esac
fi

stamp=${DRIVE_STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}   # DRIVE_STAMP: tests pin it
out="$store/$feature/$stamp"
# Reserve the evidence directory atomically: `mkdir` without -p fails when another drive of
# this feature, started the same second, already holds it, so each drive gets its own.
reserve() {
  mkdir -p "$store/$feature"
  local base=$out n=1
  until mkdir "$out" 2>/dev/null; do
    [[ -e $out ]] || die "cannot create $out (is $store writable?)"
    n=$((n+1)); out="$base-$n"
  done
  chmod 777 "$out"; stamp=${out##*/}
}
plugins=(--plugin-dir /repo/claude-plugins/manifest-dev)
[[ $tools == 1 ]] && plugins+=(--plugin-dir /repo/claude-plugins/manifest-dev-tools)

if [[ $dry == 1 ]]; then
  base=$out; n=1; while [[ -e $out ]]; do n=$((n+1)); out="$base-$n"; done; stamp=${out##*/}
  credential=$( (claude_auth_resolve && echo "$CLAUDE_AUTH_ENV") 2>/dev/null) ||
    credential="none found — the drive would stop as unreachable"
  echo "would drive: $feature  model=$model  scaffold=${scaffold:-none}"
  echo "container:   ${EVAL_RUN[*]} -e <credential> -v <checkout>:/repo:ro -v <evidence>:/out $image"
  echo "             claude -p --model $model ${plugins[*]} --max-turns $max_turns <prompt>"
  echo "credential:  $credential"
  echo "evidence:    $out (full, kept on this machine)"
  echo "summary:     printed; scripts/verify keeps it under verification/evidence/$feature/"
  exit 0
fi

eval_container_ready
claude_auth_resolve || unreachable "set a Claude credential (see above)"

if [[ $feature == doctor ]]; then
  # Under $store, not mktemp: colima shares only the home directory with the container.
  prompt="reply with the single word ok"; max_turns=1; out="$store/doctor/$stamp"
  reserve
else
  # An eval case's prompt.md opens with YAML front matter; the session gets only the body below it.
  prompt=$(awk 'NR==1 && /^---$/ {fm=1; next} fm && /^---$/ {fm=0; next} !fm' "$prompt_file")
  reserve
  printf '%s\n' "$prompt" >"$out/prompt.md"
fi
scaffold_in=""
[[ -n $scaffold ]] && scaffold_in="/repo/${scaffold#"$root"/}/scaffold.sh"

container=0
"${EVAL_RUN[@]}" -e "$CLAUDE_AUTH_ENV" -e PROMPT="$prompt" -e SCAFFOLD="$scaffold_in" \
  -v "$root":/repo:ro -v "$out":/out "$image" bash -c '
    set -euo pipefail
    mkdir -p /tmp/scratch && cd /tmp/scratch && git init -q
    [[ -n $SCAFFOLD ]] && bash "$SCAFFOLD" >/out/scaffold.log 2>&1
    git add -A >/dev/null 2>&1 && git -c user.email=d@d -c user.name=drive commit -qm scaffold --allow-empty
    claude -p --model '"$model"' '"${plugins[*]}"' --output-format stream-json --verbose \
      --permission-mode bypassPermissions --max-turns '"$max_turns"' "$PROMPT" >/out/transcript.jsonl 2>/out/stderr.log || true
    git status --porcelain >/out/files-written.txt
    git diff >/out/scratch.diff; git ls-files --others --exclude-standard -z | xargs -0 -r tar -cf /out/untracked.tar
    [[ -d $HOME/.manifest-dev ]] && tar -cf /out/home-manifest-dev.tar -C "$HOME" .manifest-dev || true
  ' || container=$?

# No transcript means no session ran: the container, the scaffold or the credential failed, and
# the skill was never tried.
if [[ ! -s $out/transcript.jsonl ]]; then
  [[ -s $out/scaffold.log ]] && { echo "scaffold.log (last lines):"; tail -n 20 "$out/scaffold.log"; } >&2
  unreachable "the session wrote no transcript (container exit $container); see $out/stderr.log"
fi
python3 - "$out" "$feature" "$tools" <<'PY'
import json, pathlib, sys
out, feature, tools = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "1"
events = []
for line in (out / "transcript.jsonl").read_text(encoding="utf-8").splitlines():
    try:
        events.append(json.loads(line))
    except json.JSONDecodeError:
        pass
init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
if init is None:
    print("drive: unreachable — the session produced no init event; see stderr.log in " + str(out), file=sys.stderr)
    sys.exit(3)
plugins = {p["name"] for p in init.get("plugins", [])}
skills = set(init.get("skills", []))
need = {"manifest-dev"} | ({"manifest-dev-tools"} if tools else set())
missing = sorted(need - plugins)
if feature != "doctor":
    owner = "manifest-dev-tools" if tools and f"manifest-dev-tools:{feature}" in skills else "manifest-dev"
    if f"{owner}:{feature}" not in skills:
        missing.append(f"skill {owner}:{feature}")
if missing:
    print(f"drive: unreachable — the session did not load {missing}; not counted as a drive", file=sys.stderr)
    sys.exit(3)
result = next((e for e in reversed(events) if e.get("type") == "result"), {})
used = sorted({b.get("input", {}).get("skill", "") for e in events if e.get("type") == "assistant"
               for b in e.get("message", {}).get("content", []) if b.get("type") == "tool_use" and b.get("name") == "Skill"} - {""})
prompt_path = out / "prompt.md"
if prompt_path.exists():
    first = prompt_path.read_text(encoding="utf-8").lstrip().split(maxsplit=1)
    if first and first[0].startswith("/") and first[0][1:] in skills:
        used = sorted(set(used) | {first[0][1:] + " (slash command)"})
entry_point = "slash command" if any(u.endswith("(slash command)") for u in used) else (
    "skill named in the prompt" if used else "none observed")
summary = {
    "model": init.get("model"),
    "plugins": sorted(f'{p["name"]}@{p.get("version", "")}' for p in init.get("plugins", []) if p["name"].startswith("manifest-dev")),
    "skills_invoked": used,
    "entry_point": entry_point,
    "turns": result.get("num_turns"),
    "result": (result.get("result") or "").strip(),
    "files_written": (out / "files-written.txt").read_text(encoding="utf-8").strip() if (out / "files-written.txt").exists() else "",
}
(out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
PY

if [[ $feature == doctor ]]; then
  echo "doctor: ok — plugin and skills load in an isolated session"; rm -rf "$out"; exit 0
fi
python3 - "$out" "$out/summary.md" "$feature" "$stamp" <<'PY'
import json, pathlib, sys
out, dest, feature, stamp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], sys.argv[4]
s = json.loads((out / "summary.json").read_text(encoding="utf-8"))
# scripts/verify keeps this summary as committed evidence and removes local paths from it then;
# the full record stays on this machine.
prompt = (out / "prompt.md").read_text(encoding="utf-8").strip()
files = s["files_written"] or "(none)"
summary = f"""# Drive: {feature} — {stamp}

- **Model:** {s['model']}
- **Plugins loaded:** {', '.join(s['plugins'])}
- **Skills invoked:** {', '.join(s['skills_invoked']) or '(none)'}
- **Entry point:** {s.get('entry_point', 'not recorded')}
- **Turns:** {s['turns']}

## Prompt

{prompt}

## Files written in the scratch project

```
{files}
```

## Final reply

{s['result']}
"""
dest.write_text(summary, encoding="utf-8")
print(summary)
print(f"full evidence (kept on this machine, not committed): {out}")
PY
