#!/usr/bin/env bash
# Drive one skill recipe headless and isolated. Skill recipes' scenarios call it, and
# `scripts/verify drive` keeps what it prints as the evidence.
#
#   scripts/drive-skill.sh preflight
#   scripts/drive-skill.sh doctor
#   scripts/drive-skill.sh <feature> <prompt-file> [--scaffold <eval-case-dir>]
#                          [--tools] [--max-turns N] [--dry-run]
#
# preflight  Free: checks that the claude CLI is on PATH and signed in, and starts no session.
#            `scripts/verify doctor` runs it.
# doctor     Starts one throwaway session and checks it loaded the plugins and their skills.
#            Exit 0 = worth driving; exit 3 names what is missing. Uses model quota.
# <feature>  The recipe's file name in verification/recipes/ without `.md` (e.g. figure-out).
# <prompt>   A file holding the prompt, exactly as a user would type it.
# --scaffold Builds the scratch project from an eval case's scaffold.sh before the prompt, run
#            in the scratch project with the checkout's path in DRIVE_CHECKOUT.
# --tools    Also loads claude-plugins/manifest-dev-tools (its skills' entries need it).
# --dry-run  Prints the session command, the CLI it would use and where evidence would go;
#            starts nothing. VERIFY_DRY_RUN=1 (set by `scripts/verify drive --dry-run`) does
#            the same.
#
# Isolation: `claude` runs directly, its working directory a scratch project built in the
# drive's evidence directory, outside this checkout. It is handed a copy of the plugin, never the
# checkout's own directory, and started with no user settings and no MCP servers of yours
# (scripts/lib/claude-cli.sh has the flags), so your settings, hooks and installed plugins do
# not load. It signs in as you: its home is a directory holding a link to every entry of yours
# except ~/.manifest-dev, which starts empty, so recall, which reads ~/.manifest-dev, finds none
# of the Manifests and logs of your own work — records that could name what a scenario grades.
# It is not a sandbox: your home stays reachable by its real path. The links are removed when
# the drive ends, so nothing that follows links through the evidence walks into your home.
#
# Evidence: the transcript, the scratch project, the plugin copies and whatever the session
# wrote under its own ~/.manifest-dev are kept under
# ${MANIFEST_DEV_FEATURES_EVIDENCE:-$HOME/.local/state/manifest-dev-features}/<feature>/<stamp>/,
# which must lie outside this checkout. A summary — CLI version, model, loaded plugins and
# skills, final reply, files written — is printed, which `scripts/verify` keeps as the
# scenario's evidence. A drive that could not start, whose session did not load the plugin or
# the skill, or whose session ended in an error, exits 3 (unreachable) and is not counted.
#
# Needs: the claude CLI on PATH, signed in (`claude auth login`, or ANTHROPIC_API_KEY), and
# python3. The CLI version is recorded, not pinned. MODEL selects the model (default: opus).
set -euo pipefail

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
root=$(cd "$root" && pwd -P)
# shellcheck source=lib/claude-cli.sh
source "$root/scripts/lib/claude-cli.sh"
model=${MODEL:-opus}
store=${MANIFEST_DEV_FEATURES_EVIDENCE:-$HOME/.local/state/manifest-dev-features}

usage() { sed -n '2,21p' "$0"; exit 2; }
die() { echo "drive: $*" >&2; exit 1; }
unreachable() { echo "drive: unreachable — $*" >&2; exit 3; }

[[ $# -ge 1 ]] || usage
feature=$1; shift
prompt_file="" scaffold="" tools=0 max_turns=40 dry=${VERIFY_DRY_RUN:-0}
if [[ $feature == preflight ]]; then
  claude_cli_ready drive
  echo "preflight: ok — $CLAUDE_CLI_VERSION is on PATH and signed in"
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
    --scaffold|--max-turns)
      [[ $# -ge 2 ]] || die "$1 needs a value (see the top of this file)"
      if [[ $1 == --scaffold ]]; then scaffold=$2; else max_turns=$2; fi
      shift 2 ;;
    --tools) tools=1; shift ;;
    --dry-run) dry=1; shift ;;
    *) die "unknown option $1 (see the top of this file)" ;;
  esac
done
if [[ -n $scaffold ]]; then
  [[ -f $scaffold/scaffold.sh ]] || die "no scaffold.sh in $scaffold"
  scaffold=$(cd "$scaffold" && pwd -P)
  case $scaffold in "$root"/*) ;; *) die "scaffold must be inside this checkout" ;; esac
fi
plugin_names=(manifest-dev)
[[ $tools == 1 ]] && plugin_names+=(manifest-dev-tools)

stamp=${DRIVE_STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}   # DRIVE_STAMP: tests pin it
out="$store/$feature/$stamp"

if [[ $dry == 1 ]]; then
  base=$out; n=1; while [[ -e $out ]]; do n=$((n+1)); out="$base-$n"; done
  echo "would drive: $feature  model=$model  scaffold=${scaffold:-none}"
  echo "project:     $out/project (scratch; the session's working directory)"
  echo "plugins:     copies of ${plugin_names[*]} under $out/plugins"
  echo "session:     claude -p --model $model ${CLAUDE_ISOLATION[*]} --plugin-dir <copy>... --max-turns $max_turns <prompt>"
  echo "cli:         $(claude_cli_status)"
  echo "evidence:    $out (full, kept on this machine)"
  echo "summary:     printed; scripts/verify keeps it as the scenario's evidence"
  exit 0
fi

claude_cli_ready drive

# The scratch project lives under the store, so the store must lie outside the checkout, or a
# session working there could change it. Checked before anything is created there.
store=$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$store")
case $store/ in
  "$root"/*) die "the evidence store $store is inside this checkout, where a session could change it; set MANIFEST_DEV_FEATURES_EVIDENCE to a directory outside it" ;;
esac
mkdir -p "$store/$feature" 2>/dev/null ||
  die "cannot create $store/$feature; set MANIFEST_DEV_FEATURES_EVIDENCE to a writable directory outside this checkout"
out="$store/$feature/$stamp"
# Reserve the evidence directory atomically: `mkdir` without -p fails when another drive of
# this feature, started the same second, already holds it, so each drive gets its own.
base=$out n=1
until mkdir "$out" 2>/dev/null; do
  [[ -e $out ]] || die "cannot create $out (is $store writable?)"
  n=$((n+1)); out="$base-$n"
done
stamp=${out##*/}

if [[ $feature == doctor ]]; then
  prompt="reply with the single word ok"; max_turns=1
else
  # An eval case's prompt.md opens with YAML front matter; the session gets only the body below it.
  prompt=$(awk 'NR==1 && /^---$/ {fm=1; next} fm && /^---$/ {fm=0; next} !fm' "$prompt_file")
  printf '%s\n' "$prompt" >"$out/prompt.md"
fi

plugins=()
for name in "${plugin_names[@]}"; do
  copy=$(copy_plugin "$name" "$out/plugins") || exit 3
  plugins+=(--plugin-dir "$copy")
done
project="$out/project"
mkdir "$project"
git -C "$project" init -q
if [[ -n $scaffold ]]; then
  # The scaffold reads the checkout through DRIVE_CHECKOUT and gets a home of its own: one that
  # seeds a home directory is an eval case's, and a drive's session links to the rest of yours.
  scaffolded=0 scaffold_home="$out/scaffold-home"
  mkdir "$scaffold_home"
  (cd "$project" && HOME=$scaffold_home DRIVE_CHECKOUT=$root bash "$scaffold/scaffold.sh") \
    >"$out/scaffold.log" 2>&1 || scaffolded=$?
  if ((scaffolded != 0)); then
    { echo "scaffold.log (last lines):"; tail -n 20 "$out/scaffold.log"; } >&2
    unreachable "the scaffold exited $scaffolded before the session started; fix ${scaffold#"$root"/}/scaffold.sh and rerun"
  fi
  if [[ -n $(ls -A "$scaffold_home") ]]; then
    unreachable "${scaffold#"$root"/}/scaffold.sh seeds a home directory, which a drive would have to write into yours; run that case through its eval suite instead"
  fi
fi
git -C "$project" add -A
git -C "$project" -c user.email=drive@localhost -c user.name=drive -c commit.gpgsign=false \
  -c core.hooksPath=/dev/null commit -qm scaffold --allow-empty
# The session's home: a link to each entry of yours, so it signs in as you, except
# ~/.manifest-dev, which starts empty. Your own records stay out of what it can read.
session_home="$out/home"
mkdir "$session_home"
for entry in "$HOME"/* "$HOME"/.[!.]* "$HOME"/..?*; do
  [[ -e $entry || -L $entry ]] || continue
  [[ ${entry##*/} == .manifest-dev ]] && continue
  ln -s "$entry" "$session_home/${entry##*/}"
done
mkdir "$session_home/.manifest-dev"
trap 'rm -rf "$session_home"' EXIT

session=0
(cd "$project" && "${CLAUDE_SESSION_ENV[@]}" HOME="$session_home" claude -p --model "$model" "${CLAUDE_ISOLATION[@]}" \
  "${plugins[@]}" --output-format stream-json --verbose --permission-mode bypassPermissions \
  --max-turns "$max_turns" "$prompt") >"$out/transcript.jsonl" 2>"$out/stderr.log" || session=$?

git -C "$project" status --porcelain >"$out/files-written.txt"
# What the session wrote under its own ~/.manifest-dev, copied beside the rest.
: >"$out/manifest-dev-records.txt"
if [[ -d $session_home/.manifest-dev ]]; then
  (cd "$session_home/.manifest-dev" && find . -type f | sed 's|^\./||' | sort) \
    >"$out/manifest-dev-records.txt"
fi
while IFS= read -r record; do
  mkdir -p "$out/manifest-dev/$(dirname "$record")"
  cp "$session_home/.manifest-dev/$record" "$out/manifest-dev/$record"
done <"$out/manifest-dev-records.txt"

# No transcript means no session ran: the CLI failed before it started, and the skill was never
# tried.
if [[ ! -s $out/transcript.jsonl ]]; then
  [[ -s $out/stderr.log ]] && { echo "stderr.log (last lines):"; tail -n 20 "$out/stderr.log"; } >&2
  unreachable "the session wrote no transcript (claude exit $session); read stderr.log in $out for why, then rerun"
fi
# A session stopped by a signal (killed, out of memory) left a partial record: a drive that never
# finished, not a skill that wrote nothing. Its own error exits are read with its result below.
((session <= 128)) || unreachable "the session was stopped by a signal (exit $session) after it started; its partial record is in $out — rerun the drive"
python3 - "$out" "$feature" "$tools" "$CLAUDE_CLI_VERSION" "$session" <<'PY'
import json, pathlib, sys
out, feature, tools, cli = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "1", sys.argv[4]
session = int(sys.argv[5])
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
loaded = init.get("plugins", [])
plugins = {p["name"] for p in loaded}
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
# A plugin the drive did not hand in means the session reached your own setup; the summary says so.
copies = str(out / "plugins") + "/"
other = sorted(p["name"] for p in loaded
               if not (str(p.get("path", "")).startswith(copies) or (not p.get("path") and p["name"] in need)))
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
    "cli_version": cli,
    "model": init.get("model"),
    "plugins": sorted(f'{p["name"]}@{p.get("version", "")}' for p in loaded if p["name"] in need),
    "other_plugins": other,
    "skills_invoked": used,
    "entry_point": entry_point,
    "turns": result.get("num_turns"),
    "result": (result.get("result") or "").strip(),
    "files_written": (out / "files-written.txt").read_text(encoding="utf-8").strip(),
    "manifest_dev_records": (out / "manifest-dev-records.txt").read_text(encoding="utf-8").splitlines(),
    "claude_exit": session,
    "ended": result.get("subtype") or "no result event",
}
(out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
# A session that errored after it started (an API error, its turn limit) never finished the
# skill: a drive that did not run, not a skill that wrote nothing.
if session != 0 or not result or result.get("is_error"):
    print(f"drive: unreachable — the session ended with {summary['ended']} (claude exit {session}); "
          f"read transcript.jsonl in {out}, raise --max-turns if it ran out of turns, then rerun",
          file=sys.stderr)
    sys.exit(3)
PY

if [[ $feature == doctor ]]; then
  echo "doctor: ok — plugin and skills load in an isolated session"; rm -rf "$out"; exit 0
fi
python3 - "$out" "$out/summary.md" "$feature" "$stamp" <<'PY'
import json, pathlib, sys
out, dest, feature, stamp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], sys.argv[4]
s = json.loads((out / "summary.json").read_text(encoding="utf-8"))
# scripts/verify keeps this summary as the scenario's evidence and removes local paths from it
# then; the full record stays on this machine.
prompt = (out / "prompt.md").read_text(encoding="utf-8").strip()
files = s["files_written"] or "(none)"
records = "\n".join(s["manifest_dev_records"]) or "(none)"
summary = f"""# Drive: {feature} — {stamp}

- **CLI version:** {s['cli_version']}
- **Model:** {s['model']}
- **Plugins loaded:** {', '.join(s['plugins'])}
- **Other plugins loaded:** {', '.join(s['other_plugins']) or 'none'}
- **Skills invoked:** {', '.join(s['skills_invoked']) or '(none)'}
- **Entry point:** {s.get('entry_point', 'not recorded')}
- **Turns:** {s['turns']}

## Prompt

{prompt}

## Files written in the scratch project

```
{files}
```

## Written under the session's .manifest-dev

```
{records}
```

## Final reply

{s['result']}
"""
dest.write_text(summary, encoding="utf-8")
print(summary)
print(f"full evidence (kept on this machine): {out}")
PY
