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
# <prompt>   A file holding the prompt, exactly as a user would type it. A line reading exactly
#            `<!-- next turn -->` splits it into turns: the first starts the session, and each
#            later one goes into the same session (`--resume`) once it has answered the last.
# --scaffold Builds the scratch project from an eval case's scaffold.sh before the prompt, run
#            in the scratch project with the checkout's path in DRIVE_CHECKOUT.
# --tools    Also loads claude-plugins/manifest-dev-tools (its skills' entries need it).
# --dry-run  Prints the session command, the CLI it would use and where evidence would go;
#            starts nothing. VERIFY_DRY_RUN=1 (set by `scripts/verify drive --dry-run`) does
#            the same.
#
# DRIVE_PLUGINS_AT=<commit> hands the session the plugins as they were at that commit instead of
# as they are in the checkout; the prompt and the scaffold still come from the checkout. Any
# recipe scenario then runs before and after a change with no scenario of its own:
#   DRIVE_PLUGINS_AT=$(git merge-base HEAD origin/main) scripts/verify drive figure-out <scenario> --yes
# The summary records which commit the plugins came from. Report each arm's cost and wall time
# from its summary beside its verdict: a change that adds cost to every run is weighed by what it
# gains for that cost.
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
# skills, the session's cost as the CLI reports it and its wall time, final reply (and each
# turn's reply in a session of several), files written — is printed, which `scripts/verify`
# keeps as the scenario's evidence. A drive that could not start, whose session did not load the plugin or
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

usage() { sed -n '2,27p' "$0"; exit 2; }
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
plugins_from=checkout
if [[ -n ${DRIVE_PLUGINS_AT:-} ]]; then
  plugins_from=$(git -C "$root" rev-parse --verify --quiet "$DRIVE_PLUGINS_AT^{commit}") ||
    die "DRIVE_PLUGINS_AT=$DRIVE_PLUGINS_AT names no commit in this checkout"
  for name in "${plugin_names[@]}"; do
    git -C "$root" cat-file -e "$plugins_from:claude-plugins/$name" 2>/dev/null ||
      die "DRIVE_PLUGINS_AT=$DRIVE_PLUGINS_AT has no claude-plugins/$name"
  done
fi

stamp=${DRIVE_STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}   # DRIVE_STAMP: tests pin it
out="$store/$feature/$stamp"

if [[ $dry == 1 ]]; then
  base=$out; n=1; while [[ -e $out ]]; do n=$((n+1)); out="$base-$n"; done
  echo "would drive: $feature  model=$model  scaffold=${scaffold:-none}"
  echo "project:     $out/project (scratch; the session's working directory)"
  echo "plugins:     copies of ${plugin_names[*]} from $plugins_from under $out/plugins"
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
# One file per turn: the prompt split at each `<!-- next turn -->` line.
python3 - "$out" "$prompt" <<'PY' || unreachable "the prompt has an empty turn; put text between every two <!-- next turn --> lines"
import pathlib, sys
out, text = pathlib.Path(sys.argv[1]), sys.argv[2]
turns, current = [], []
for line in text.splitlines():
    if line.strip() == "<!-- next turn -->":
        turns.append("\n".join(current).strip())
        current = []
    else:
        current.append(line)
turns.append("\n".join(current).strip())
if not all(turns):
    sys.exit(1)
for i, turn in enumerate(turns, 1):
    (out / f"turn-{i}.md").write_text(turn + "\n", encoding="utf-8")
PY

plugins=()
for name in "${plugin_names[@]}"; do
  if [[ $plugins_from == checkout ]]; then
    copy=$(copy_plugin "$name" "$out/plugins") || exit 3
  else
    copy="$out/plugins/$name"
    mkdir -p "$copy" && git -C "$root" archive "$plugins_from:claude-plugins/$name" | tar -x -C "$copy" ||
      unreachable "could not copy claude-plugins/$name at $plugins_from to $out/plugins; free disk space and rerun"
  fi
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

session=0 turn=1 resume=() started=$(date +%s.%N)
: >"$out/transcript.jsonl"
: >"$out/turn-starts.txt"
while :; do
  # Where this turn's events begin, so the summary reads each turn's reply from its own events.
  wc -l <"$out/transcript.jsonl" >>"$out/turn-starts.txt"
  (cd "$project" && "${CLAUDE_SESSION_ENV[@]}" HOME="$session_home" claude -p --model "$model" "${CLAUDE_ISOLATION[@]}" \
    "${plugins[@]}" "${resume[@]}" --output-format stream-json --verbose --permission-mode bypassPermissions \
    --max-turns "$max_turns" "$(cat "$out/turn-$turn.md")") >>"$out/transcript.jsonl" 2>>"$out/stderr.log" || session=$?
  turn=$((turn+1))
  ((session == 0)) && [[ -f $out/turn-$turn.md ]] || break
  # The next turn goes into the session that answered this one, and only if it answered without
  # an error; the summary below reports a turn that did not.
  sid=$(python3 -c 'import json, sys
# Only the turn that just ran decides: its own events start at the last recorded offset. Lines
# are split on "\n" alone, as `wc -l` counts them; model text can hold other line separators.
start = int(open(sys.argv[2], encoding="utf-8").read().split()[-1])
events = []
for line in open(sys.argv[1], encoding="utf-8").read().split("\n")[start:]:
    try:
        events.append(json.loads(line))
    except ValueError:
        pass
results = [e for e in events if e.get("type") == "result"]
if not results or results[-1].get("is_error"):
    sys.exit(1)
print(next((e["session_id"] for e in reversed(events) if e.get("session_id")), ""))' "$out/transcript.jsonl" "$out/turn-starts.txt") || break
  if [[ -z $sid ]]; then
    echo "drive: turn $((turn-1)) reported no session id to send turn $turn into" >>"$out/stderr.log"
    session=1; break
  fi
  resume=(--resume "$sid")
done
wall=$(python3 -c 'import sys, time; print(round(time.time() - float(sys.argv[1]), 1))' "$started")

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
python3 - "$out" "$feature" "$tools" "$CLAUDE_CLI_VERSION" "$session" "$plugins_from" "$wall" <<'PY'
import json, pathlib, sys
out, feature, tools, cli = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "1", sys.argv[4]
session, plugins_from, wall = int(sys.argv[5]), sys.argv[6], float(sys.argv[7])
# A turn can end in more than one result — a background task that finishes wakes the session
# again — so each turn's reply is the last result among its own events, never the nth result.
starts = [int(n) for n in (out / "turn-starts.txt").read_text(encoding="utf-8").split()]
events, turn_of = [], []
for n, line in enumerate((out / "transcript.jsonl").read_text(encoding="utf-8").split("\n")):
    try:
        events.append(json.loads(line))
    except json.JSONDecodeError:
        continue
    turn_of.append(sum(1 for start in starts if start <= n))
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
results = [e for e in events if e.get("type") == "result"]
result = results[-1] if results else {}
user_turns = len(list(out.glob("turn-*.md")))
replies = []
for t in range(1, len(starts) + 1):
    own = [e for e, k in zip(events, turn_of) if k == t and e.get("type") == "result"]
    replies.append(own[-1] if own else None)
# A resumed session reports its cost so far, every turn included, so the last turn's total is
# the session's. A cost the CLI did not report is said, never shown as zero.
cost = result.get("total_cost_usd")
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
    "plugins_from": plugins_from,
    "other_plugins": other,
    "skills_invoked": used,
    "entry_point": entry_point,
    "turns": sum(r.get("num_turns") or 0 for r in results) if results else None,
    "user_turns": user_turns,
    "cost_usd": round(cost, 4) if isinstance(cost, (int, float)) else "not reported",
    "wall_seconds": wall,
    "result": (result.get("result") or "").strip(),
    "turn_replies": [((r or {}).get("result") or "").strip() for r in replies] if user_turns > 1 else [],
    "files_written": (out / "files-written.txt").read_text(encoding="utf-8").strip(),
    "manifest_dev_records": (out / "manifest-dev-records.txt").read_text(encoding="utf-8").splitlines(),
    "claude_exit": session,
    "ended": result.get("subtype") or "no result event",
}
(out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
# A session that errored after it started (an API error, its turn limit) never finished the
# skill: a drive that did not run, not a skill that wrote nothing.
unanswered = next((t for t, r in enumerate(replies, 1) if r is None or r.get("is_error")), None)
if unanswered is None and len(replies) < user_turns:
    unanswered = len(replies) + 1
if session != 0 or unanswered is not None:
    where = f"turn {unanswered} of {user_turns} got no reply" if unanswered and user_turns > 1 else \
        f"the session ended with {summary['ended']}"
    print(f"drive: unreachable — {where} (claude exit {session}); "
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
cost = s["cost_usd"] if isinstance(s["cost_usd"], str) else f"${s['cost_usd']:.4f}"
turns_note = f" over {s['user_turns']} user turns" if s["user_turns"] > 1 else ""
by_turn = ""
if s["turn_replies"]:
    by_turn = "\n## Each turn and its reply\n"
    for i, reply in enumerate(s["turn_replies"], 1):
        asked = (out / f"turn-{i}.md").read_text(encoding="utf-8").strip()
        by_turn += f"\n### Turn {i}\n\n{asked}\n\n**Reply:**\n\n{reply}\n"
summary = f"""# Drive: {feature} — {stamp}

- **CLI version:** {s['cli_version']}
- **Model:** {s['model']}
- **Plugins loaded:** {', '.join(s['plugins'])} (from {s['plugins_from']})
- **Other plugins loaded:** {', '.join(s['other_plugins']) or 'none'}
- **Skills invoked:** {', '.join(s['skills_invoked']) or '(none)'}
- **Entry point:** {s.get('entry_point', 'not recorded')}
- **Turns:** {s['turns']}{turns_note}
- **Cost:** {cost}
- **Wall time:** {s['wall_seconds']} s

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
{by_turn}"""
dest.write_text(summary, encoding="utf-8")
print(summary)
print(f"full evidence (kept on this machine): {out}")
PY
