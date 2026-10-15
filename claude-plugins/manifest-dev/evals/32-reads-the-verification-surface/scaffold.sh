#!/usr/bin/env bash
set -euo pipefail
mkdir -p src tests
cat > README.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

    python -m shelfnote checkout --member ana --book "Middlemarch"
    python -m shelfnote return --book "Middlemarch"
    python -m shelfnote overdue
    python -m shelfnote export --format csv
EOF
cat > src/shelfnote.py <<'EOF'
import argparse, json, pathlib, sys
DATA = pathlib.Path("data/loans.json")
def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []
def main(argv=None):
    p = argparse.ArgumentParser(prog="shelfnote")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checkout"); c.add_argument("--member"); c.add_argument("--book")
    r = sub.add_parser("return"); r.add_argument("--book")
    sub.add_parser("overdue")
    e = sub.add_parser("export"); e.add_argument("--format", choices=["csv", "json"])
    args = p.parse_args(argv)
    print(args.cmd)
if __name__ == "__main__":
    main()
EOF

mkdir -p scripts verification/recipes
cat > scripts/verify <<'VERIFY_TOOL_EOF'
#!/bin/sh
# Starts this project's verification tool, verify.mts beside this file: TypeScript that Node
# 22.18 or newer (23.6 or newer on Node 23) runs directly. `verify --help` says everything else.
# A project that ports the tool to another language keeps this file's name and replaces
# everything below this comment, the Node check included, with a line that starts the port.
v=$(node --version 2>/dev/null) || { echo "verify: needs Node 22.18 or newer (https://nodejs.org); node was not found" >&2; exit 3; }
major=${v#v}; minor=${major#*.}; major=${major%%.*}; minor=${minor%%.*}
if [ "$major" -lt 22 ] || { [ "$major" -eq 22 ] && [ "$minor" -lt 18 ]; } || { [ "$major" -eq 23 ] && [ "$minor" -lt 6 ]; }; then
  echo "verify: needs Node 22.18 or newer (23.6 or newer on Node 23), which runs TypeScript directly; found $v" >&2
  exit 3
fi
exec node "$(dirname "$0")/verify.mts" "$@"
VERIFY_TOOL_EOF
cat > scripts/verify.mts <<'VERIFY_TOOL_EOF'
// verify — this project's one verification harness.
//
// Run `verify --help` for everything: what can be checked, how, what each status means, and
// which checks to ask about before running. Recipes are Markdown files in the recipes
// directory; this file reads them and never needs editing to add one.
//
// TypeScript with no dependencies, run by Node 22.18 or newer (23.6 or newer on Node 23),
// which strips the types itself.
// `verify` beside this file starts it and says so when Node is missing or too old.

import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { createHash, randomBytes } from "node:crypto";
import { existsSync, fstatSync, lstatSync, mkdirSync, mkdtempSync, openSync, closeSync, readdirSync, readFileSync, readSync, readlinkSync, realpathSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import { arch, availableParallelism, constants, homedir, platform, tmpdir } from "node:os";
import { isAbsolute, join, relative, resolve } from "node:path";

// Where the harness keeps its data. A project that moves it changes these lines.
const ROOT = resolve(process.env.VERIFY_ROOT || join(import.meta.dirname, ".."));
const DATA = resolve(process.env.VERIFY_DATA || join(ROOT, "verification"));
const RECIPES = join(DATA, "recipes");
const EVIDENCE = join(DATA, "evidence");
const SETTINGS = join(DATA, "harness.md");

const EXIT_UNREACHABLE = 3; // a scenario command exits 3 when a prerequisite is missing
const EXIT_ASK_FIRST = 4; // this harness refused a run that needs a person's agreement without --yes
const EXIT_OVER_LINE = 5; // a scenario passed, but its run time crossed its line twice running
const EXIT_USAGE = 2;

const OUTCOMES = ["verified", "failed", "unreachable", "unjudged"] as const;
type Outcome = (typeof OUTCOMES)[number];
// Worst first: a recipe shows the worst of its scenarios' latest outcomes.
const SEVERITY: Record<Outcome, number> = { failed: 3, unreachable: 2, unjudged: 1, verified: 0 };

// Commands a project may declare in its settings to control what it checks. Each one runs
// through `verify <name>`; an undeclared one does not exist for that project.
const CONTROL = {
  start: "start an instance of what the project checks, in a known state, for this run",
  running: "say what instances are running",
  logs: "show an instance's logs and traces",
  reset: "put an instance back in its known state",
  stop: "stop an instance this harness started",
} as const;
type Control = keyof typeof CONTROL;
// Own keys only: `in` would also match what every object inherits, such as `toString`.
const isControl = (name: string): name is Control => Object.hasOwn(CONTROL, name);
// Control commands that act on an instance an earlier invocation started, so they name it.
const NAMES_A_RUN: readonly Control[] = ["logs", "reset", "stop"];

const STAMP = /(\d{8}T\d{6}Z)(?:-(\d+))?/;
const DATE = /(\d{4}-\d{2}-\d{2})/;
// On its own line, or as a list item among the recipe's traps.
const DRIFT = /^(?:[-*] )?Drift \((\d{4}-\d{2}-\d{2})\): (.+)$/gm;
const OUTCOME_LINE = /^- \*\*Outcome:\*\* (\w+)/m;
const COVERS_LINE = /^- \*\*Covers:\*\* (\S+)/m;
const LINE_ENTRY = /^- \*\*Line:\*\* (\S+) (\d+(?:\.\d+)?) s; (.*)$/gm;

/** A crossing counts once this many runs in a row on one kind of machine were over the line. */
const CONFIRMING_RUNS = 2;
/** However short a scenario, its line sits at least this many seconds above what it measured. */
const MIN_HEADROOM_SECONDS = 1;
// The default branches `affected` tries, in order, after origin/HEAD when given no base.
const DEFAULT_BRANCHES = ["origin/main", "origin/master", "main", "master"];
/** How long a failed run waits on the project's `logs:` command before giving up on it. */
const LOGS_TIMEOUT_SECONDS = 60;
/** How much a `logs:` command may print before it is stopped, so it cannot fill the disk. */
const LOGS_MAX_BYTES = 64 * 1024 * 1024;
// A failure's logs keep their end, where the failure is, and say where they were cut.
const LOGS_TAIL_LINES = 200;
const LOGS_TAIL_CHARS = 64 * 1024;

class Problem extends Error {
  readonly code: number;
  constructor(message: string, code = 1) {
    super(message);
    this.code = code;
  }
}

interface Scenario {
  name: string;
  run: string;
  proves: string;
  judged: boolean; // true: a person or agent reads the evidence; false: the exit code decides
  timed: boolean; // false for `Workload: varies`, whose run time is no measure of creep
}

interface Recipe {
  name: string;
  path: string;
  kind: string;
  covers: string[];
  askFirst: string; // the reason, or "" for a recipe that runs freely
  dryRun: boolean; // its commands honor VERIFY_DRY_RUN=1
  scenarios: Scenario[];
  body: string;
}

/** A scenario's time line on one kind of machine, as its latest evidence carries it. */
interface Line {
  base: number; // seconds: the run the line was set or last moved from
  origin: string; // "first run", "lowered", "paid down", or "raised: <reason>"
  frozen?: { level: number; ticket: string }; // an overshoot a debt Ticket holds at this level
  over: number; // runs in a row over the line
}

interface Evidence {
  path: string;
  when: Date;
  order: number; // the -N suffix of runs stamped in the same second; 1 for the first
  scenario: string; // "" for evidence that covered the whole recipe
  outcome: Outcome;
  covers: string; // fingerprint of the covered files when it ran; "" in evidence from before
  machine: string; // "" in evidence from before durations were kept
  duration: number | undefined; // seconds
  lines: Map<string, Line>; // by kind of machine
}

const read = (path: string): string => readFileSync(path, "utf8");
const day = (when: Date): string => when.toISOString().slice(0, 10);
const seconds = (value: number): string => `${value.toFixed(1)} s`;
const rel = (path: string): string => {
  const inside = relative(ROOT, path);
  return inside && !inside.startsWith("..") && !isAbsolute(inside) ? inside : path;
};
const markdownIn = (folder: string): string[] =>
  existsSync(folder) && statSync(folder).isDirectory()
    ? readdirSync(folder).filter((name) => name.endsWith(".md")).sort().map((name) => join(folder, name))
    : [];
const stem = (path: string): string => path.slice(path.lastIndexOf("/") + 1).replace(/\.md$/, "");
const escapeRegExp = (text: string): string => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * Paths that exist only on the machine that ran: this user's home and the temporary directory
 * wherever they are, and the usual places for them elsewhere. Committed evidence carries none.
 */
function localPaths(): RegExp {
  const places = new Set(["/tmp", "/Users", "/private", "/var/folders"]);
  for (const place of [homedir(), tmpdir()]) {
    if (!place || place === "/") continue;
    places.add(place.replace(/\/+$/, ""));
    try {
      places.add(realpathSync(place).replace(/\/+$/, ""));
    } catch {
      // a home or temporary directory that does not exist has no other spelling
    }
  }
  const longestFirst = [...places].sort((a, b) => b.length - a.length).map(escapeRegExp);
  // `~/…`, `/home/<user>/…`, or one of the places above, alone or followed by a path.
  return new RegExp(
    `\`?(?:~\\/[^\\s\`]*|\\/home\\/[^/\\s\`]+(?:\\/[^\\s\`]*)?|(?:${longestFirst.join("|")})(?![\\w.-])(?:\\/[^\\s\`]*)?)\`?`,
    "g",
  );
}

/** `key: value` lines between `---` fences, and the body after them. */
function frontMatter(text: string): [Record<string, string>, string] {
  if (!text.startsWith("---\n")) return [{}, text];
  const end = text.indexOf("\n---\n", 3);
  if (end < 0) throw new Problem("front matter has no closing `---`");
  const meta: Record<string, string> = {};
  for (const line of text.slice(4, end).split("\n")) {
    if (!line.trim()) continue;
    const colon = line.indexOf(":");
    if (colon < 0) throw new Problem(`front matter line is not \`key: value\`: ${JSON.stringify(line)}`);
    meta[line.slice(0, colon).trim()] = line.slice(colon + 1).trim();
  }
  return [meta, text.slice(end + 5)];
}

function parseRecipe(path: string): Recipe {
  const file = stem(path) + ".md";
  const [meta, body] = frontMatter(read(path));
  if (!meta.kind) throw new Problem(`${file}: front matter has no \`kind:\``);
  if (!/^# \S/m.test(body)) throw new Problem(`${file}: no \`# Title\` line`);
  const scenarios: Scenario[] = [];
  const section = /^## Scenarios[ \t]*$([\s\S]*?)(?=^## |(?![\s\S]))/m.exec(body);
  for (const block of section ? (section[1] ?? "").split(/^### /m).slice(1) : []) {
    const newline = block.indexOf("\n");
    const name = (newline < 0 ? block : block.slice(0, newline)).trim();
    const rest = newline < 0 ? "" : block.slice(newline);
    const run = /^Run:\s*`([^`]+)`/m.exec(rest);
    const proves = /^Proves:\s*(.+)$/m.exec(rest);
    const check = /^Check:\s*(\S+)/m.exec(rest);
    const workload = /^Workload:\s*(\S+)/m.exec(rest);
    if (!run?.[1]) throw new Problem(`${file}: scenario '${name}' has no Run: \`command\` line`);
    if (check && check[1] !== "read" && check[1] !== "exit") {
      throw new Problem(`${file}: scenario '${name}' Check: must be \`read\` or \`exit\``);
    }
    if (workload && workload[1] !== "fixed" && workload[1] !== "varies") {
      throw new Problem(`${file}: scenario '${name}' Workload: must be \`fixed\` or \`varies\``);
    }
    scenarios.push({
      name,
      run: run[1],
      proves: proves?.[1]?.trim() ?? "",
      judged: check?.[1] === "read",
      timed: workload?.[1] !== "varies",
    });
  }
  return {
    name: stem(path),
    path,
    kind: meta.kind,
    covers: (meta.covers ?? "").split(",").map((c) => c.trim()).filter(Boolean),
    askFirst: meta["ask-first"] ?? "",
    dryRun: meta["dry-run"] === "honored",
    scenarios,
    body,
  };
}

function recipes(): Recipe[] {
  if (!existsSync(RECIPES)) throw new Problem(`no recipes directory at ${RECIPES}`);
  return markdownIn(RECIPES).map(parseRecipe);
}

function find(name: string): Recipe {
  const path = join(RECIPES, `${name}.md`);
  if (!existsSync(path)) {
    throw new Problem(`no recipe '${name}'. Known: ${recipes().map((r) => r.name).join(", ")}`);
  }
  return parseRecipe(path);
}

interface Settings {
  askFirst: "ask" | "run";
  raise: "ask" | "run";
  doctor: string;
  control: Partial<Record<Control, string>>;
  grace: number; // seconds between SIGTERM and SIGKILL when a run is stopped
  headroom: number; // fraction of a line's measured time allowed for noise
  notes: string;
}

function settings(): Settings {
  const [meta, body] = existsSync(SETTINGS) ? frontMatter(read(SETTINGS)) : [{}, ""];
  const choice = (key: string): "ask" | "run" => {
    const value = meta[key] ?? (key === "ask-first" ? "ask" : "run");
    if (value !== "ask" && value !== "run") {
      throw new Problem(`${rel(SETTINGS)}: ${key} must be \`ask\` or \`run\`, not '${value}'`);
    }
    return value;
  };
  const grace = meta.grace ?? "2";
  if (!/^\d+(?:\.\d+)?$/.test(grace)) {
    throw new Problem(`${rel(SETTINGS)}: grace must be a number of seconds, such as \`2\` or \`0.5\`, not '${grace}'`);
  }
  const headroom = meta.headroom ?? "25%";
  if (!/^\d+(?:\.\d+)?%$/.test(headroom)) {
    throw new Problem(`${rel(SETTINGS)}: headroom must be a percentage, such as \`25%\`, not '${headroom}'`);
  }
  const control: Partial<Record<Control, string>> = Object.create(null);
  for (const name of Object.keys(CONTROL) as Control[]) {
    if (meta[name]) control[name] = meta[name];
  }
  return {
    askFirst: choice("ask-first"),
    raise: choice("raise"),
    doctor: meta.doctor ?? "",
    control,
    grace: Number(grace),
    headroom: Number(headroom.slice(0, -1)) / 100,
    notes: body.trim(),
  };
}

/** Where a run's time is measured: kinds differ, so a line is never compared across them. */
function machineKind(): string {
  const named = process.env.VERIFY_MACHINE?.trim();
  return named ? named.replace(/\s+/g, "-") : `${platform()}-${arch()}-${availableParallelism()}cpu`;
}

/**
 * This invocation's run identity, handed to every command it starts as VERIFY_RUN_ID, so data
 * directories, ports and containers can be per run. `--run ID` names an earlier run's instance;
 * a command started inside a run inherits that run's identity.
 */
function runIdentity(named: string | undefined, needed?: string): string {
  const id = named ?? process.env.VERIFY_RUN_ID;
  if (id !== undefined) {
    if (!/^[A-Za-z0-9][\w.-]*$/.test(id)) {
      const from = named === undefined ? "VERIFY_RUN_ID, inherited from the environment," : `run id '${id}'`;
      throw new Problem(`${from} must be letters, digits, '.', '_' or '-'${named === undefined ? `; it is '${id}'` : ""}`, EXIT_USAGE);
    }
    return id;
  }
  // A fresh identity names no instance, so a command meant for one would act on nothing.
  if (needed) throw new Problem(`verify ${needed}: name the instance with --run ID, the id \`verify start\` printed`, EXIT_USAGE);
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "").replace("T", "-");
  return `${stamp}-${randomBytes(3).toString("hex")}`;
}

const withRun = (id: string, extra: Record<string, string> = {}): NodeJS.ProcessEnv => ({
  ...process.env,
  ...extra,
  VERIFY_RUN_ID: id,
});

// --- evidence and statuses -------------------------------------------------------------

/** True for a file named as a run summary; any other file beside them is kept detail. */
function isSummary(path: string): boolean {
  return STAMP.test(stem(path)) || DATE.test(stem(path));
}

function parseLines(text: string): Map<string, Line> {
  const lines = new Map<string, Line>();
  for (const [, kind = "", base = "", rest = ""] of text.matchAll(LINE_ENTRY)) {
    const line: Line = { base: Number(base), origin: "", over: 0 };
    for (const part of rest.split("; ")) {
      const frozen = /^frozen at (\d+(?:\.\d+)?) s by (.+)$/.exec(part);
      const over = /^over (\d+)$/.exec(part);
      if (frozen) line.frozen = { level: Number(frozen[1]), ticket: frozen[2] ?? "" };
      else if (over) line.over = Number(over[1]);
      else line.origin = line.origin ? `${line.origin}; ${part}` : part;
    }
    lines.set(kind, line);
  }
  return lines;
}

function renderLines(lines: Map<string, Line>): string {
  return [...lines]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([kind, line]) => {
      const parts = [line.origin];
      if (line.frozen) parts.push(`frozen at ${line.frozen.level.toFixed(1)} s by ${line.frozen.ticket}`);
      if (line.over) parts.push(`over ${line.over}`);
      return `- **Line:** ${kind} ${line.base.toFixed(1)} s; ${parts.join("; ")}\n`;
    })
    .join("");
}

/** A file's text, or undefined when a run beside this one removed it while this one listed it. */
function readIfThere(path: string): string | undefined {
  try {
    return read(path);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    throw error;
  }
}

/** Write a whole file at once, so a run beside this one never reads it half written. */
function writeWhole(path: string, text: string): void {
  const part = join(path, "..", `.${stem(path)}.${process.pid}.partial`);
  writeFileSync(part, text);
  renameSync(part, path);
}

/**
 * A summary's header — the fields above its first `## ` section — and the rest. Fields are read
 * and rewritten in the header only, so a scenario whose output prints a field never sets one.
 */
function splitSummary(text: string): [string, string] {
  const at = text.search(/^## /m);
  return at < 0 ? [text, ""] : [text.slice(0, at), text.slice(at)];
}

/** A header with its lines replaced, after the Duration field, where a run writes them. */
function withLines(head: string, lines: Map<string, Line>): string {
  return head.replace(/^- \*\*Line:\*\* .*\n/gm, "").replace(/^(- \*\*Duration:\*\* .*\n)/m, `$1${renderLines(lines)}`);
}

function readEvidence(path: string): Evidence | undefined {
  const text = readIfThere(path);
  if (text === undefined) return undefined;
  // An empty file is a run that never finished writing; `check` reports it.
  if (!text.trim()) return undefined;
  const stamp = STAMP.exec(stem(path));
  let when: Date;
  if (stamp?.[1]) {
    const s = stamp[1];
    when = new Date(`${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}T${s.slice(9, 11)}:${s.slice(11, 13)}:${s.slice(13, 15)}Z`);
  } else {
    const date = DATE.exec(stem(path));
    if (!date) throw new Problem(`${path}: evidence file name carries no stamp or date`);
    when = new Date(`${date[1]}T00:00:00Z`);
  }
  const [head] = splitSummary(text);
  const outcome = OUTCOME_LINE.exec(head)?.[1] ?? "unjudged";
  if (!(OUTCOMES as readonly string[]).includes(outcome)) {
    throw new Problem(`${path}: outcome '${outcome}' is not one of ${OUTCOMES.join(", ")}`);
  }
  const scenario = /^- \*\*Scenario:\*\* (.+)$/m.exec(head)?.[1]?.trim() ?? "";
  const covers = COVERS_LINE.exec(head)?.[1] ?? "";
  const machine = /^- \*\*Machine:\*\* (\S+)/m.exec(head)?.[1] ?? "";
  const duration = /^- \*\*Duration:\*\* (\d+(?:\.\d+)?) s/m.exec(head)?.[1];
  return {
    path,
    when,
    order: Number(stamp?.[2] ?? 1),
    scenario,
    outcome: outcome as Outcome,
    covers,
    machine,
    duration: duration === undefined ? undefined : Number(duration),
    lines: parseLines(head),
  };
}

const older = (a: Evidence, b: Evidence): number => a.when.getTime() - b.when.getTime() || a.order - b.order;

/** Oldest first; runs stamped in the same second keep the order they were written in. */
function evidenceFor(recipe: Recipe): Evidence[] {
  return markdownIn(join(EVIDENCE, recipe.name))
    .filter(isSummary)
    .map(readEvidence)
    .filter((e): e is Evidence => e !== undefined)
    .sort(older);
}

/** Output of a git command in the project, or "" outside a repository or on failure. */
function git(...args: string[]): string {
  const done = spawnSync("git", ["-C", ROOT, ...args], { encoding: "utf8" });
  return done.status === 0 ? done.stdout : "";
}

const insideRepository = (): boolean => git("rev-parse", "--is-inside-work-tree").trim() === "true";

/** True for a path, relative to the project, under the harness's own evidence. */
function isEvidencePath(path: string): boolean {
  const evidence = rel(EVIDENCE);
  return path === evidence || path.startsWith(`${evidence}/`);
}

/**
 * Every file under the covered paths, tracked or new; outside a repository, every file there.
 * The harness's own evidence is never covered: a recipe cannot go stale by recording a run.
 */
function coveredFiles(paths: string[]): string[] {
  if (insideRepository()) {
    const listed = git("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", ...paths);
    return [...new Set(listed.split("\0").filter((path) => path && !isEvidencePath(path)))].sort();
  }
  // A link is one entry, counted by its target, as git lists it; following it could loop.
  const walk = (path: string): string[] => {
    const full = join(ROOT, path);
    if (isEvidencePath(path)) return [];
    if (isLink(full)) return [path];
    if (!existsSync(full)) return [];
    return statSync(full).isDirectory() ? readdirSync(full).flatMap((name) => walk(join(path, name))) : [path];
  };
  return paths.flatMap(walk).sort();
}

function isLink(path: string): boolean {
  try {
    return lstatSync(path).isSymbolicLink();
  } catch {
    return false;
  }
}

/**
 * What the covered files held: a hash over their paths and contents. Evidence records it when
 * it runs, so a later edit makes it stale however the edit and the evidence are committed.
 */
function fingerprint(paths: string[]): string {
  const hash = createHash("sha256");
  for (const path of coveredFiles(paths)) {
    const full = join(ROOT, path);
    const entry = existsSync(full) || isLink(full) ? lstatSync(full) : undefined;
    // A link counts by where it points; a submodule by the commit it records.
    const content = !entry
      ? "(deleted)"
      : entry.isSymbolicLink()
        ? `link:${readlinkSync(full)}`
        : entry.isFile()
          ? readFileSync(full)
          : `entry:${git("ls-files", "-s", "--", path).trim()}`;
    hash.update(`${path}\0`).update(content).update("\0");
  }
  return `sha256:${hash.digest("hex").slice(0, 16)}`;
}

/** When the covered paths last changed: an uncommitted edit counts from the file's mtime. */
function lastChange(paths: string[]): Date | undefined {
  if (!paths.length) return undefined;
  // -z keeps each entry whole: no quoting, and the leading status column survives.
  const entries = git("status", "--porcelain=v1", "-z", "-uall", "--", ...paths).split("\0");
  const times: number[] = [];
  // Status paths are relative to the repository's top, which may sit above this project.
  const top = git("rev-parse", "--show-toplevel").trim() || ROOT;
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i] ?? "";
    if (entry.length < 4) continue;
    if (entry[0] === "R" || entry[0] === "C") i++; // the next entry is the rename's source
    const path = join(top, entry.slice(3));
    times.push(existsSync(path) ? statSync(path).mtimeMs : Date.now());
  }
  if (times.length) return new Date(Math.max(...times));
  const log = git("log", "-1", "--format=%cI", "--", ...paths).trim();
  return log ? new Date(log) : undefined;
}

/**
 * When evidence entered the history: the commit that first added it, following moves.
 * Evidence is committed with the change it checked, so that commit and the covered change
 * share a time; a later commit to a covered path then makes it stale. Uncommitted evidence
 * counts from its own stamp.
 */
function checkedAt(evidence: Evidence): Date {
  const added = git("log", "--follow", "--diff-filter=A", "--format=%cI", "--", rel(evidence.path)).trim();
  const first = added.split("\n").at(-1);
  return first ? new Date(Math.max(evidence.when.getTime(), new Date(first).getTime())) : evidence.when;
}

/**
 * The latest evidence for each scenario. Evidence naming no scenario covered the whole
 * recipe, so it stands for every scenario until that scenario has newer evidence of its own.
 */
function latestPerScenario(recipe: Recipe, history: Evidence[]): Map<string, Evidence> {
  const names = new Set(recipe.scenarios.map((s) => s.name));
  const latest = new Map<string, Evidence>();
  for (const item of history) {
    if (item.scenario && !names.has(item.scenario)) continue; // `check` reports it
    for (const name of item.scenario ? [item.scenario] : names.size ? [...names] : [""]) {
      latest.set(name, item);
    }
  }
  return latest;
}

/** The time a run may take before it counts as over a line: the line's base plus headroom. */
function limit(base: number, headroom: number): number {
  return Math.max(base * (1 + headroom), base + MIN_HEADROOM_SECONDS);
}

/** The level a run is held to: a frozen overshoot's, or else the line's own. */
function allowance(line: Line, headroom: number): number {
  return limit(line.frozen ? line.frozen.level : line.base, headroom);
}

/** A crossing confirmed on the machine the evidence ran on: what the status should say. */
function crossing(evidence: Evidence, headroom: number): string {
  const line = evidence.lines.get(evidence.machine);
  // Only a verified run measured the check; any other carries the line on without crossing it.
  if (evidence.outcome !== "verified" || !line || line.over < CONFIRMING_RUNS || evidence.duration === undefined) return "";
  const against = line.frozen ? `the ${seconds(line.frozen.level)} its Ticket ${line.frozen.ticket} froze` : `its ${seconds(line.base)} line`;
  return `${evidence.scenario || "the recipe"} took ${seconds(evidence.duration)} against ${against} (with headroom ${seconds(allowance(line, headroom))}) on ${evidence.machine}`;
}

function status(recipe: Recipe, history: Evidence[] = evidenceFor(recipe), headroom = settings().headroom): string {
  const drifts = [...recipe.body.matchAll(DRIFT)].map((m) => [m[1] ?? "", m[2] ?? ""] as const).sort();
  const drift = drifts.at(-1);
  const perScenario = latestPerScenario(recipe, history);
  const latest = [...new Set(perScenario.values())];
  // A scenario that never ran proves nothing, so passing the others does not verify the recipe.
  const unrun = recipe.scenarios.map((s) => s.name).filter((name) => !perScenario.has(name));
  const oldestRun = latest.reduce<Date | undefined>((a, e) => (!a || e.when < a ? e.when : a), undefined);
  const worst = latest.reduce<Evidence | undefined>(
    (a, e) => (!a || SEVERITY[e.outcome] > SEVERITY[a.outcome] ? e : a),
    undefined,
  );
  // A run that failed or could not start says more than a proof found outdated, so it shows
  // first: over a Drift line it ran after, and over covered files changed after another run.
  const failing = worst !== undefined && SEVERITY[worst.outcome] >= SEVERITY.unreachable;
  // A Drift line holds until every scenario has run since it: one scenario's run repairs only itself.
  const driftHolds = drift && (!oldestRun || unrun.length || drift[0] >= day(oldestRun));
  if (driftHolds && !(failing && day(worst.when) >= drift[0])) return `stale (${drift[0]}): ${drift[1]}`;
  if (!worst) return "unverified";
  const oldest = latest.reduce((a, e) => (e.when < a.when ? e : a));
  // The date is the worst scenario's run, or for a recipe whose scenarios all passed, the
  // oldest of their runs: how fresh the weakest proof is.
  const notRun = unrun.length ? `no run yet for ${unrun.join(", ")}` : "";
  // Every scenario passed, but one's run time crossed its line on two runs in a row.
  const over = latest.map((e) => [e, crossing(e, headroom)] as const).filter(([, said]) => said);
  const label =
    worst.outcome === "verified"
      ? notRun
        ? `unverified (${day(oldest.when)}): ${notRun}`
        : over.length
          ? `over its line (${day(over[0]?.[0].when ?? oldest.when)}): ${over.map(([, said]) => said).join("; ")}`
          : `verified (${day(oldest.when)})`
      : `${worst.outcome} (${day(worst.when)})${notRun ? `: ${notRun}` : ""}`;
  if (!recipe.covers.length) return label;
  // Evidence that recorded what it checked is stale when the covered files now differ; older
  // evidence falls back to comparing times.
  const now = latest.some((e) => e.covers) ? fingerprint(recipe.covers) : "";
  const legacy = latest.filter((e) => !e.covers);
  const changed = legacy.length || latest.some((e) => e.covers !== now) ? lastChange(recipe.covers) : undefined;
  const outdated = latest.filter((e) =>
    e.covers ? e.covers !== now : changed !== undefined && changed.getTime() > checkedAt(e).getTime(),
  );
  if (!outdated.length) return label;
  if (failing && !outdated.includes(worst)) return label;
  // Name the newest run the change outdated, which need not be the worst run.
  const last = outdated.reduce((a, e) => (e.when > a.when ? e : a));
  const run = `the ${last.outcome} run of ${day(last.when)}`;
  // A fingerprint can differ with no change dated after the run: the run checked an edit that
  // was later undone. Then the files differ from what it checked, and that is all that is known.
  const [since, what] =
    changed && changed > last.when
      ? [changed, `covered files changed after ${run}`]
      : [last.when, `covered files differ from what ${run} checked`];
  return `stale (${day(since)}): ${notRun ? `${what}; ${notRun}` : what}`;
}

// --- commands ---------------------------------------------------------------------------

const HELP = `verify — this project's one place to control what it checks and to check that its
work still does its job.

Every check is a recipe: a Markdown file in {recipes} naming what it covers, how a user
reaches it, the scenarios that exercise it (each a command and what it proves), and its traps.
This tool lists them, runs them, keeps their evidence, and works out their status. It is a
default shape for a harness: adapt it, its settings or its recipes wherever this project is
better served another way, and say so here.

Commands:
  verify list [KIND]          every recipe with its kind, status and ask-first mark
  verify help RECIPE          one recipe in full, with each scenario's latest evidence and line
  verify drive RECIPE [SCENARIO] [--yes] [--dry-run] [--run ID]
                              run a recipe's scenarios (all, or the one named) and keep evidence
  verify walk RECIPE ...      the same, for a recipe of kind walk
  verify eval RECIPE ...      the same, for a recipe of kind eval
  verify affected [BASE]      the recipes whose covered paths changed since BASE, and the changed
                              paths no recipe covers. Without BASE: since the branch left the
                              default branch (origin/HEAD, else ${DEFAULT_BRANCHES.join(", ")})
  verify judge RECIPE EVIDENCE verified|failed [NOTE]
                              record the verdict on evidence a person or agent had to read
  verify raise RECIPE SCENARIO REASON...{raiseYes}
                              move a crossed line up to the latest run, with the reason: the new
                              time is in new tests for new behavior and the old tests are no slower
  verify freeze RECIPE SCENARIO TICKET
                              hold a crossed line's overshoot at the latest run's level while the
                              debt Ticket named pays it down
  verify doctor               check the harness's prerequisites (free; starts nothing costly)
  verify check                check every recipe parses and names only paths that exist
{control}
When to run it: before saying a change works, when reproducing a reported problem, and when a
change touches what a recipe covers. A change that needs a check no recipe has adds the recipe.
Every check without the ask-first mark is free: run it as often as it helps, judging from the
durations its evidence shows.

Ask first: a recipe marked ask-first costs something a person should weigh — money or quota,
load on shared systems or other teams, effects outside this repository. Run time alone is not a
cost. Its reason is shown in \`verify help RECIPE\`. This project's setting: ask-first = {policy}.
  ask  run an ask-first recipe only when a person runs it or has agreed — in the session, or by
       approving a plan whose check runs it: ask first, naming the recipe and why; then pass --yes
  run  run them freely
Change it in {settings}. Recipes without the mark run freely.

Run identity: every command this tool starts gets VERIFY_RUN_ID, one per invocation, so data
directories, ports and containers can be per run and runs can go side by side. \`--run ID\` on a
drive or a control command reaches the instance an earlier run started (\`verify start\` prints its
id); logs, reset and stop need it. A command started inside a run inherits that run's identity.
A control command for an id its instance does not know exits non-zero, saying so.

Statuses (worked out from evidence; nothing to keep current by hand). A recipe shows the worst
of its scenarios' latest runs:
  unverified            no evidence yet; proves nothing
  unverified (DATE): .. the scenarios that ran passed, and those it names have never run
  verified (DATE)       every scenario's latest run passed; DATE is the oldest of those runs
  over its line (DATE): every scenario passed, but one's run time crossed its line on two runs
                        in a row: see Lines below
  failed (DATE)         a scenario's latest run failed
  unreachable (DATE)    a scenario's latest run could not start: a prerequisite was missing
  unjudged (DATE)       a scenario's latest run finished; its proof needs reading — see \`verify judge\`
  stale (DATE): ...     what the recipe covers changed after that evidence (or, when nothing is
                        dated after it, differs from what it checked; DATE is then the run's),
                        or someone found it drifting and added \`Drift (DATE): what differs\` to
                        the recipe. A failed or unreachable run since then shows instead

Lines: an alarm against a check slowly getting slower, and nothing else — a line never decides
when a check runs or who may run it. A scenario's first verified run on a kind of machine sets
its line there (a run needing a verdict counts once judged verified); a run counts as over it
past the line plus headroom ({headroom}, at least ${MIN_HEADROOM_SECONDS} s). One run over is noise until a second in a row confirms it: then the status says so
and \`drive\` exits ${EXIT_OVER_LINE}. A run faster than the line by more than the headroom lowers it. A line
moves up only by \`verify raise\` with its reason{raisePolicy}, or is held by \`verify freeze\` while a
debt Ticket pays the overshoot down; a run past the frozen level is new creep. A scenario whose
work varies — the affected tests, an agent session — says \`Workload: varies\` and gets no line.
Lines live in each scenario's latest evidence, per kind of machine (set VERIFY_MACHINE to name
one, such as a CI runner label); no file is edited by every run. VERIFY_DURATION stands in for
every measured time, for the tool's own tests; leave it unset. When merged branches leave two
summaries, the next run keeps the line allowing the most, so a raise or freeze survives.

Evidence: each run writes {evidence}/RECIPE/STAMP.md (command, exit code, outcome, run identity,
kind of machine, duration, lines, a fingerprint of the covered files, output with local paths
removed) and removes the scenario's older summaries, so the folder keeps one per scenario; the
history stays in git. When a run fails and the project declares \`logs:\`, its output for that run
is kept too. Commit evidence with the change it checked. Whatever a command started is stopped
when it ends: SIGTERM, then SIGKILL after {grace} s (\`grace:\` in {settings}). An interrupted run
keeps no evidence; a command that crashes is failed.

Exit codes: 0 done; 1 a scenario failed or could not start, or a problem; 2 usage; 3 a
prerequisite is missing; 4 refused without a person's agreement (--yes); 5 over a line. A
control command exits with its project command's own code.

Adding a recipe: copy any file in {recipes}, keep the front matter keys (kind, covers,
ask-first when it applies, dry-run: honored when its commands obey VERIFY_DRY_RUN=1), and give
each scenario a \`### name\` heading with \`Run:\`, \`Proves:\` and, when the exit code cannot decide,
\`Check: read\`. \`verify check\` validates it.
`;

function cmdHelp(): number {
  const conf = settings();
  const declared = (Object.keys(CONTROL) as Control[]).filter((name) => conf.control[name]);
  const control = declared.length
    ? `\nControl (this project's commands, declared in {settings}):\n` +
      declared.map((name) => `  verify ${`${name}${name === "running" ? "" : " [--run ID]"}`.padEnd(24)}${CONTROL[name]}: ${conf.control[name]}\n`).join("")
    : "";
  const fill: Record<string, string> = {
    recipes: rel(RECIPES),
    evidence: rel(EVIDENCE),
    settings: rel(SETTINGS),
    policy: conf.askFirst,
    grace: String(conf.grace),
    headroom: `${Math.round(conf.headroom * 1000) / 10}%`,
    raiseYes: conf.raise === "ask" ? " --yes" : "",
    raisePolicy: conf.raise === "ask" ? " and a person's agreement (raise: ask)" : "",
  };
  const text = HELP.replace("{control}", control);
  console.log(text.replace(/\{(\w+)\}/g, (whole, key: string) => fill[key] ?? whole));
  if (conf.notes) console.log(`This project's notes:\n\n${conf.notes}`);
  console.log(`\nRecipes: ${recipes().length}. Run \`verify list\` to see them.`);
  return 0;
}

function cmdList(kind: string | undefined): number {
  const { headroom } = settings();
  // The list shows each status up to its reason; `verify help <recipe>` prints the whole line.
  const rows = recipes()
    .filter((r) => kind === undefined || r.kind === kind)
    .map((r) => [r.name, r.kind, status(r, evidenceFor(r), headroom).split(": ")[0] ?? "", r.askFirst ? "ask-first" : ""] as const);
  if (!rows.length) throw new Problem(`no recipes of kind '${kind}'`);
  const width = (i: 0 | 1 | 2): number => Math.max(...rows.map((row) => row[i].length));
  for (const [name, rkind, rstatus, mark] of rows) {
    console.log(`${name.padEnd(width(0))}  ${rkind.padEnd(width(1))}  ${rstatus.padEnd(width(2))}  ${mark}`.trimEnd());
  }
  return 0;
}

function describeLines(evidence: Evidence, headroom: number): string {
  return [...evidence.lines]
    .map(([kind, line]) => {
      const held = line.frozen ? `, frozen at ${seconds(line.frozen.level)} by ${line.frozen.ticket}` : "";
      const over = line.over ? `, ${line.over} run(s) over` : "";
      return `line ${seconds(line.base)} on ${kind} (${line.origin}${held}; over past ${seconds(allowance(line, headroom))}${over})`;
    })
    .join("; ");
}

function cmdShow(name: string): number {
  const recipe = find(name);
  const history = evidenceFor(recipe);
  const { headroom } = settings();
  console.log(`${rel(recipe.path)} — ${recipe.kind} — ${status(recipe, history, headroom)}`);
  if (recipe.askFirst) console.log(`ask-first: ${recipe.askFirst}`);
  console.log(recipe.body.trim());
  console.log("\nLatest evidence per scenario:");
  const latest = latestPerScenario(recipe, history); // the same evidence the status is worked out from
  for (const scenario of recipe.scenarios) {
    const mine = latest.get(scenario.name);
    const took = mine?.duration !== undefined ? `, ${seconds(mine.duration)} on ${mine.machine}` : "";
    const lines = mine?.lines.size ? `; ${describeLines(mine, headroom)}` : "";
    console.log(`  ${scenario.name}: ${mine ? `${mine.outcome}, ${rel(mine.path)}${took}${lines}` : "none"}`);
  }
  return 0;
}

// A run holds its evidence name with a marker beside it, never an empty summary: `check` and
// another run's status would read an empty summary as a run that never finished.
const RESERVED = /^\.(.+)\.reserved$/;

/**
 * A fresh evidence name, held by a marker until the summary is written over it: two runs
 * started in the same second each get their own. Returns the summary's path, its stamp and
 * the marker to remove once the run ends.
 */
function reserve(recipe: Recipe): [string, string, string] {
  const folder = join(EVIDENCE, recipe.name);
  mkdirSync(folder, { recursive: true });
  const stamp = process.env.VERIFY_STAMP || new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
  // After the run it replaces, not into a name that run freed: a reused name would sort first.
  const taken = readdirSync(folder)
    .map((name) => new RegExp(`^\\.?${stamp}(?:-(\\d+))?\\.(?:md|reserved)$`).exec(name))
    .filter((m): m is RegExpExecArray => m !== null)
    .map((m) => Number(m[1] ?? 1));
  for (let n = Math.max(0, ...taken) + 1; ; n++) {
    const candidate = n === 1 ? stamp : `${stamp}-${n}`;
    const path = join(folder, `${candidate}.md`);
    const marker = join(folder, `.${candidate}.reserved`);
    try {
      writeFileSync(marker, `${process.pid}\n`, { flag: "wx" });
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
      continue;
    }
    if (!existsSync(path)) return [path, candidate, marker];
    rmSync(marker, { force: true });
  }
}

/** True while the process that wrote a reservation marker is still running. */
function holderAlive(marker: string): boolean {
  const pid = Number(readIfThere(marker)?.trim());
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return (error as NodeJS.ErrnoException).code === "EPERM";
  }
}

interface Run {
  code: number;
  output: string;
  interrupted: boolean;
  seconds: number;
}

/** Signals that stop a run: Ctrl-C, a polite kill, a closed terminal, Ctrl-\. */
const STOP_SIGNALS: NodeJS.Signals[] = ["SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT"];

/** Send a signal to a process group that may already be gone. */
function signalGroup(pid: number, signal: NodeJS.Signals): void {
  try {
    process.kill(-pid, signal);
  } catch {
    // the group already ended
  }
}

/** Hand a command's process group to its watchdog to stop, by closing the watchdog's pipe. */
function stop(child: ChildProcess): void {
  child.stdio[3]?.destroy();
}

function stopping(child: ChildProcess): boolean {
  return child.stdio[3]?.destroyed === true;
}

/**
 * Ctrl-C and termination while a scenario runs. Installed before a run reserves its evidence
 * file, so a signal at any point leaves that file to be removed rather than killing the tool.
 * The first signal is passed on to the running command's process group. A second hands the
 * group to its watchdog to stop; one more, or a signal once the command's shell is gone, kills
 * the group at once. A group still in its grace when the tool exits is left to its watchdog.
 */
class Interrupts {
  interrupted = false;
  child: ChildProcess | undefined;
  private readonly handle = (signal: NodeJS.Signals): void => {
    const child = this.child;
    if (child?.pid !== undefined) {
      if (stopping(child)) signalGroup(child.pid, "SIGKILL");
      else if (this.interrupted) stop(child);
      else signalGroup(child.pid, signal);
    }
    this.interrupted = true;
  };
  constructor() {
    for (const signal of STOP_SIGNALS) process.on(signal, this.handle);
  }
  release(): void {
    for (const signal of STOP_SIGNALS) process.off(signal, this.handle);
  }
}

/**
 * Runs the scenario command in a process group of its own beside a watchdog that stops the
 * group: SIGTERM, which a container client passes on to the session inside, then SIGKILL for
 * whatever outlasts the grace. It waits on descriptor 3, a pipe whose other end only this tool
 * holds, and stops the group when that end closes: when this tool closes it (the command's
 * shell has ended, or a stop was asked for), and when this tool is gone, however it died, even
 * before anyone reaps it. So a command never outlives the tool, and what it leaves behind is
 * stopped even if the tool dies during the grace. The watchdog ignores the SIGTERM and SIGHUP a
 * stop sends. The command's shell then replaces the one that started the watchdog, so the process
 * this tool watches is the command's own: a signal passed on to it ends the run only once the
 * command's shell has finished with it, and no stop starts while that shell is still cleaning up.
 * A child of a shell that does not handle the signal is stopped with the rest of the group once
 * the shell has died of it. The command does not inherit the descriptor, and its exit status is
 * the run's.
 */
const watched = (grace: number): string =>
  [
    `( trap '' TERM HUP; read -r _ <&3; kill -TERM 0; sleep ${grace}; kill -KILL 0 ) </dev/null >/dev/null 2>&1 &`,
    'exec sh -c "$VERIFY_COMMAND" 3<&-',
  ].join("\n");

// Output keeps being collected when whoever reads this tool's output goes away (`| head`).
let echo = true;
for (const stream of [process.stdout, process.stderr]) {
  stream.on("error", (error: NodeJS.ErrnoException) => {
    if (error.code !== "EPIPE") throw error;
    echo = false;
  });
}

/** Run a scenario's command, showing its output as it arrives and keeping a copy. */
function runShown(command: string, interrupts: Interrupts, env: NodeJS.ProcessEnv, grace: number): Promise<Run> {
  return new Promise((done, fail) => {
    const began = performance.now();
    // Scenario commands take no input: they run unattended, in a process group of their own.
    const child = spawn("sh", ["-c", watched(grace)], {
      cwd: ROOT,
      detached: true,
      stdio: ["ignore", "pipe", "pipe", "pipe"],
      env: { ...env, VERIFY_COMMAND: command },
    });
    interrupts.child = child;
    const [, stdout, stderr] = child.stdio;
    if (!stdout || !stderr) throw new Error("the command's output pipes were not opened");
    const chunks: Buffer[] = [];
    stdout.on("data", (chunk: Buffer) => {
      chunks.push(chunk);
      if (echo) process.stdout.write(chunk);
    });
    stderr.on("data", (chunk: Buffer) => {
      chunks.push(chunk);
      if (echo) process.stderr.write(chunk);
    });
    child.on("error", fail);
    // The command's shell is gone, however it ended: stop what it left behind (a background job
    // still holding the output), so the run can end and nothing outlives it.
    child.on("exit", () => stop(child));
    child.on("close", (code, signal) => {
      interrupts.child = undefined;
      done({
        // A command that died by a signal nobody sent here failed, the way a shell reports it.
        code: code ?? 128 + (signal ? constants.signals[signal] : 0),
        // Invalid UTF-8 becomes U+FFFD rather than stopping the run.
        output: Buffer.concat(chunks).toString("utf8"),
        interrupted: interrupts.interrupted,
        seconds: (performance.now() - began) / 1000,
      });
    });
  });
}

/**
 * What a passing run does to the scenario's line on this machine, and what to say about it.
 * The previous lines come from the scenario's latest evidence; every other machine's are kept.
 */
function nextLines(previous: Map<string, Line>, machine: string, took: number, headroom: number): [Map<string, Line>, string] {
  const lines = new Map(previous);
  const line = previous.get(machine);
  if (!line) {
    lines.set(machine, { base: took, origin: "first run", over: 0 });
    return [lines, `line set at ${seconds(took)} on ${machine}`];
  }
  const allowed = allowance(line, headroom);
  if (took > allowed) {
    const over = line.over + 1;
    lines.set(machine, { ...line, over });
    const against = line.frozen ? `the level Ticket ${line.frozen.ticket} froze` : "its line";
    return over >= CONFIRMING_RUNS
      ? [lines, `over its line: ${seconds(took)} against ${seconds(allowed)} (${against}) on ${machine}, ${over} runs in a row. Pay it down, or \`verify raise\` with the reason, or \`verify freeze\` with the debt Ticket`]
      : [lines, `over its line once: ${seconds(took)} against ${seconds(allowed)} on ${machine}; a second run over it confirms the crossing`];
  }
  if (line.frozen && took <= limit(line.base, headroom)) {
    lines.set(machine, { base: line.base, origin: "paid down", over: 0 });
    return [lines, `the overshoot Ticket ${line.frozen.ticket} froze is paid down: back under the ${seconds(line.base)} line`];
  }
  if (!line.frozen && limit(took, headroom) <= line.base) {
    lines.set(machine, { base: took, origin: "lowered", over: 0 });
    return [lines, `line lowered from ${seconds(line.base)} to ${seconds(took)} on ${machine}`];
  }
  lines.set(machine, { ...line, over: 0 });
  return [lines, ""];
}

/**
 * The lines a scenario's next run starts from. Normally one summary carries them; after two
 * branches merge, each branch's summary carries its own until the next run folds them into one.
 * Per kind of machine the line allowing the most wins, so a raise or a freeze recorded on either
 * branch survives the fold.
 */
function carriedLines(history: Evidence[], scenario: string, headroom: number): Map<string, Line> {
  const lines = new Map<string, Line>();
  for (const item of history) {
    if (item.scenario !== scenario) continue;
    for (const [kind, line] of item.lines) {
      const held = lines.get(kind);
      if (!held || allowance(line, headroom) > allowance(held, headroom)) lines.set(kind, line);
    }
  }
  return lines;
}

/** "a, b and c": the scenarios a recipe has, for a message naming one it does not. */
function scenarioNames(recipe: Recipe): string {
  const names = recipe.scenarios.map((s) => s.name);
  return names.length > 1 ? `${names.slice(0, -1).join(", ")} and ${names.at(-1)}` : (names[0] ?? "none");
}

/**
 * VERIFY_DURATION, when set, stands in for every measured run time, as VERIFY_STAMP stands in for
 * the clock, so a test of the line rules plants a duration rather than waiting it out.
 */
function plantedDuration(): number | undefined {
  const planted = process.env.VERIFY_DURATION;
  if (planted === undefined) return undefined;
  if (!/^\d+(?:\.\d+)?$/.test(planted)) throw new Problem(`VERIFY_DURATION must be a number of seconds, not '${planted}'`, EXIT_USAGE);
  return Number(planted);
}

/** Remove the scenario's summaries older than the one just written; git keeps the history. */
function replaceOlder(recipe: Recipe, scenario: string, kept: Evidence): void {
  for (const item of evidenceFor(recipe)) {
    if (item.path !== kept.path && item.scenario === scenario && older(item, kept) < 0) rmSync(item.path, { force: true });
  }
}

/** The last `bytes` of an open file, how many lines the whole file holds, and whether it held more. */
function tailOf(fd: number, bytes: number): [string, number, boolean] {
  const size = fstatSync(fd).size;
  const chunk = Buffer.alloc(1024 * 1024);
  let lines = 0;
  for (let at = 0; at < size; ) {
    const read = readSync(fd, chunk, 0, chunk.length, at);
    if (read <= 0) break;
    for (let k = 0; k < read; k++) if (chunk[k] === 0x0a) lines++;
    at += read;
  }
  const start = Math.max(0, size - bytes);
  const tail = Buffer.alloc(size - start);
  if (tail.length) readSync(fd, tail, 0, tail.length, start);
  return [tail.toString("utf8"), lines, start > 0];
}

/**
 * The project's `logs:` output for a run, for evidence that has to explain a failure. It goes
 * to a file rather than a pipe, so a process the command leaves running cannot hold the run
 * open; the command runs in its own process group, killed when it ends, times out, prints more
 * than the cap, or the tool is asked to stop. Only the file's end is read back.
 */
async function logsFor(command: string, id: string, scrub: RegExp): Promise<string> {
  const folder = mkdtempSync(join(tmpdir(), "verify-logs-"));
  const file = join(folder, "output");
  const fd = openSync(file, "w+");
  let printed: string;
  let total: number;
  let partial: boolean;
  let ended: string;
  try {
    const child = spawn(command, { shell: true, cwd: ROOT, env: withRun(id), stdio: ["ignore", fd, fd], detached: true });
    let why = "";
    const kill = (reason: string): void => {
      why ||= reason;
      if (child.pid !== undefined) signalGroup(child.pid, "SIGKILL");
    };
    const timer = setTimeout(() => kill(`did not finish within ${LOGS_TIMEOUT_SECONDS} s`), LOGS_TIMEOUT_SECONDS * 1000);
    const watch = setInterval(() => {
      if (fstatSync(fd).size > LOGS_MAX_BYTES) kill(`printed more than ${LOGS_MAX_BYTES / 1024 / 1024} MB and was stopped`);
    }, 250);
    // The command has a process group of its own, so a stop asked of the tool has to reach it here.
    const onStop = (): void => kill("was stopped with the run");
    for (const signal of STOP_SIGNALS) process.on(signal, onStop);
    try {
      const [code, signal] = await new Promise<[number | null, NodeJS.Signals | null]>((done, fail) => {
        child.once("error", fail);
        child.once("exit", (c, s) => done([c, s]));
      });
      ended = why || (code === 0 ? "" : `exited ${code ?? signal}`);
    } finally {
      clearTimeout(timer);
      clearInterval(watch);
      for (const signal of STOP_SIGNALS) process.off(signal, onStop);
      if (child.pid !== undefined) signalGroup(child.pid, "SIGKILL"); // whatever it left running
    }
    [printed, total, partial] = tailOf(fd, LOGS_TAIL_CHARS * 4);
  } finally {
    closeSync(fd);
    rmSync(folder, { recursive: true, force: true });
  }
  const whole = printed.trim();
  let tail = whole.split("\n").slice(-LOGS_TAIL_LINES).join("\n");
  if (tail.length > LOGS_TAIL_CHARS) tail = tail.slice(-LOGS_TAIL_CHARS);
  const shown = tail.split("\n").length;
  const all = Math.max(total + (printed.endsWith("\n") ? 0 : 1), shown);
  const cut = partial || tail.length < whole.length ? ` (its last ${shown} of ${all} lines)` : "";
  const output = tail.replace(scrub, "[local path]") || "(none)";
  const said = ended ? `The logs command \`${command}\` ${ended}; what it printed${cut}:` : `From \`${command}\`${cut}:`;
  return `## Logs\n\n${said.replace(scrub, "[local path]")}\n\n${output}\n`;
}

async function cmdDrive(
  name: string,
  only: string | undefined,
  yes: boolean,
  dry: boolean,
  kind: string | undefined,
  named: string | undefined,
): Promise<number> {
  const recipe = find(name);
  if (kind && recipe.kind !== kind) throw new Problem(`${name} is of kind ${recipe.kind}; use \`verify drive ${name}\``);
  const chosen = recipe.scenarios.filter((s) => only === undefined || s.name === only);
  if (!chosen.length) {
    throw new Problem(only ? `${name} has no scenario '${only}'; its scenarios are ${scenarioNames(recipe)}` : `${name} has no scenarios to run`);
  }
  const conf = settings();
  if (recipe.askFirst && conf.askFirst === "ask" && !yes && !dry) {
    throw new Problem(
      `${name} is ask-first: ${recipe.askFirst}. Run it only when a person runs it or has agreed, then pass --yes.`,
      EXIT_ASK_FIRST,
    );
  }
  const id = runIdentity(named);
  const planted = plantedDuration();
  const machine = machineKind();
  const scrub = localPaths();
  let worst = 0;
  const interrupts = new Interrupts();
  try {
    for (const scenario of chosen) {
      if (dry) {
        console.log(`would run [${scenario.name}]: ${scenario.run}`);
        console.log(`evidence:  ${rel(join(EVIDENCE, recipe.name))}/<stamp>.md`);
        if (recipe.dryRun) {
          spawnSync(scenario.run, { shell: true, cwd: ROOT, stdio: "inherit", env: withRun(id, { VERIFY_DRY_RUN: "1" }) });
          // A signal that arrived during the blocking call is handled once the event loop turns.
          await new Promise((resolve) => setImmediate(resolve));
          if (interrupts.interrupted) return 130;
        }
        continue;
      }
      const carried = carriedLines(evidenceFor(recipe), scenario.name, conf.headroom);
      const [path, stamp, marker] = reserve(recipe);
      let written = false;
      try {
        const covers = recipe.covers.length ? fingerprint(recipe.covers) : "";
        console.log(`running [${scenario.name}] as run ${id}: ${scenario.run}`);
        const run = interrupts.interrupted ? undefined : await runShown(scenario.run, interrupts, withRun(id), conf.grace);
        if (!run || run.interrupted) {
          console.error(`interrupted: no evidence kept for [${scenario.name}]`);
          return 130;
        }
        const took = planted ?? run.seconds;
        const outcome: Outcome =
          run.code === EXIT_UNREACHABLE ? "unreachable" : run.code !== 0 ? "failed" : scenario.judged ? "unjudged" : "verified";
        const passed = outcome === "verified" || outcome === "unjudged";
        // Only a verified run measures the check: a failure can end at any point, and an
        // unjudged run is measured when it is judged verified. The others carry the lines on.
        const [lines, said] =
          scenario.timed && outcome === "verified"
            ? nextLines(carried, machine, took, conf.headroom)
            : [scenario.timed ? carried : new Map<string, Line>(), ""];
        const logs = !passed && conf.control.logs ? `\n${await logsFor(conf.control.logs, id, scrub)}` : "";
        if (interrupts.interrupted) {
          console.error(`interrupted: no evidence kept for [${scenario.name}]`);
          return 130;
        }
        writeWhole(
          path,
          `# ${recipe.name} / ${scenario.name} — ${stamp}\n\n` +
            `- **Scenario:** ${scenario.name}\n` +
            `- **Command:** \`${scenario.run}\`\n` +
            `- **Exit code:** ${run.code}\n` +
            `- **Outcome:** ${outcome}\n` +
            (covers ? `- **Covers:** ${covers}\n` : "") +
            `- **Run:** ${id}\n` +
            `- **Machine:** ${machine}\n` +
            `- **Duration:** ${seconds(took)}\n` +
            renderLines(lines) +
            `- **Proves:** ${scenario.proves || "(not stated)"}\n\n` +
            `## Output\n\n${run.output.trim().replace(scrub, "[local path]") || "(none)"}\n` +
            logs,
        );
        written = true;
        const kept = readEvidence(path);
        if (kept) replaceOlder(recipe, scenario.name, kept);
        console.log(`${outcome} in ${seconds(took)}: evidence in ${rel(path)}`);
        if (said) console.log(said);
        if (outcome === "failed" || outcome === "unreachable") worst = 1;
        else if (kept && crossing(kept, conf.headroom) && worst === 0) worst = EXIT_OVER_LINE;
      } finally {
        // A run that did not finish leaves nothing behind to pass for evidence.
        if (!written) rmSync(path, { force: true });
        rmSync(marker, { force: true });
      }
    }
  } finally {
    interrupts.release();
  }
  return worst;
}

function evidencePath(recipe: Recipe, evidence: string): string {
  const path = join(EVIDENCE, recipe.name, evidence.endsWith(".md") ? evidence : `${evidence}.md`);
  if (!existsSync(path)) throw new Problem(`no evidence ${rel(path)}`);
  return path;
}

function cmdJudge(name: string, evidence: string, verdict: string, note: string): number {
  if (verdict !== "verified" && verdict !== "failed") {
    throw new Problem("judge: the verdict is `verified` or `failed`", EXIT_USAGE);
  }
  const recipe = find(name);
  const path = evidencePath(recipe, evidence);
  const before = readEvidence(path);
  let [head, body] = splitSummary(read(path));
  head = OUTCOME_LINE.test(head)
    ? head.replace(OUTCOME_LINE, `- **Outcome:** ${verdict}`)
    : head.replace("\n\n", `\n\n- **Outcome:** ${verdict}\n`);
  if (note) body += `\n## Verdict\n\n${verdict}: ${note}\n`;
  // An unjudged run carried its lines unmeasured; judged verified, it measures them now.
  const timed = recipe.scenarios.find((s) => s.name === before?.scenario)?.timed === true;
  let said = "";
  if (before?.outcome === "unjudged" && verdict === "verified" && timed && before.duration !== undefined && before.machine) {
    const [lines, moved] = nextLines(before.lines, before.machine, before.duration, settings().headroom);
    said = moved;
    head = withLines(head, lines);
  }
  writeWhole(path, head + body);
  console.log(`${rel(path)}: ${verdict}`);
  if (said) console.log(said);
  const kept = readEvidence(path);
  return kept && crossing(kept, settings().headroom) ? EXIT_OVER_LINE : 0;
}

/**
 * Move a crossed line on purpose: up to the latest run with its reason, or held at the latest
 * run's level by a debt Ticket. Either is written into that run's evidence, where the next run
 * reads its line, never into a file every run edits.
 */
function cmdMoveLine(how: "raise" | "freeze", name: string, scenario: string, said: string, yes: boolean): number {
  const recipe = find(name);
  const declared = recipe.scenarios.find((s) => s.name === scenario);
  if (!declared) throw new Problem(`${name} has no scenario '${scenario}'; its scenarios are ${scenarioNames(recipe)}`);
  if (!declared.timed) throw new Problem(`${name} / ${scenario} says \`Workload: varies\`, so it has no line to ${how}`);
  const what = how === "raise" ? "the reason the time was earned" : "the debt Ticket that will pay it down";
  if (!said.trim()) throw new Problem(`${how}: give ${what}: verify ${how} ${name} ${scenario} ${how === "raise" ? "REASON..." : "TICKET"}`, EXIT_USAGE);
  const conf = settings();
  if (how === "raise" && conf.raise === "ask" && !yes) {
    throw new Problem(`raising a line needs a person here (raise: ask in ${rel(SETTINGS)}): ask, then pass --yes`, EXIT_ASK_FIRST);
  }
  const latest = latestPerScenario(recipe, evidenceFor(recipe)).get(scenario);
  const line = latest?.lines.get(latest.machine);
  if (!latest || latest.scenario !== scenario || !line || latest.duration === undefined) {
    throw new Problem(`${name} / ${scenario} has no run with a line yet; drive it first`);
  }
  // Only a verified run measured the check; a failed one can end at any point.
  if (latest.outcome !== "verified") {
    throw new Problem(
      latest.outcome === "unjudged"
        ? `${name} / ${scenario}: its latest run is unjudged; judge it (\`verify judge\`) before moving its line`
        : `${name} / ${scenario}: its latest run is ${latest.outcome} and measured nothing; drive it to a pass first`,
    );
  }
  if (latest.duration <= allowance(line, conf.headroom)) {
    throw new Problem(
      `${name} / ${scenario} is not over its line (${seconds(latest.duration)} against ${seconds(allowance(line, conf.headroom))} on ${latest.machine}); nothing to ${how}`,
    );
  }
  const clean = said.trim().replace(/;/g, ",").replace(/\s+/g, " ");
  const moved: Line =
    how === "raise"
      ? { base: latest.duration, origin: `raised: ${clean}`, over: 0 }
      : { base: line.base, origin: line.origin, frozen: { level: latest.duration, ticket: clean }, over: 0 };
  const lines = new Map(latest.lines).set(latest.machine, moved);
  const [head, body] = splitSummary(read(latest.path));
  writeWhole(latest.path, withLines(head, lines) + body);
  console.log(
    how === "raise"
      ? `${name} / ${scenario}: line raised to ${seconds(latest.duration)} on ${latest.machine} (${clean}); say why in the change's description too`
      : `${name} / ${scenario}: overshoot frozen at ${seconds(latest.duration)} on ${latest.machine} by ${clean}; a run past it is new creep`,
  );
  console.log(`commit ${rel(latest.path)} with the change`);
  return 0;
}

function cmdControl(name: Control, named: string | undefined): number {
  const command = settings().control[name];
  if (!command) {
    throw new Problem(
      `this project declares no \`${name}:\` command; add \`${name}: <command>\` to the front matter of ${rel(SETTINGS)} to ${CONTROL[name]}`,
      EXIT_USAGE,
    );
  }
  const id = runIdentity(named, NAMES_A_RUN.includes(name) ? name : undefined);
  if (name === "start") console.log(`run ${id}: reach this instance later with --run ${id}`);
  const done = spawnSync(command, { shell: true, cwd: ROOT, stdio: "inherit", env: withRun(id) });
  if (done.error) throw done.error;
  return done.status ?? 128 + (done.signal ? constants.signals[done.signal] : 0);
}

/** Paths changed since a base, relative to the project: committed, staged, unstaged and new. */
function changedSince(base: string): string[] {
  const top = git("rev-parse", "--show-toplevel").trim();
  // Relative to the repository's top, which may sit above this project.
  const fromTop = [
    ...git("diff", "--name-only", "-z", "--no-renames", base, "--").split("\0"),
    ...git("ls-files", "-z", "--others", "--exclude-standard", "--full-name").split("\0"),
  ].filter(Boolean);
  // git reports real paths, so a project reached through a link compares by its real path.
  const root = realpathSync(ROOT);
  return [...new Set(fromTop.map((path) => relative(root, join(top, path))))]
    .filter((path) => path && !path.startsWith(".."))
    .sort();
}

/** Where the branch left the default branch: origin/HEAD, else the first of DEFAULT_BRANCHES. */
function defaultBase(): [string, string] {
  const remote = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD").trim();
  for (const branch of [remote, ...DEFAULT_BRANCHES].filter(Boolean)) {
    const fork = git("merge-base", "HEAD", branch).trim();
    if (fork) return [fork, `where this branch left ${branch}`];
  }
  // Comparing with the last commit instead would hide everything this branch committed.
  throw new Problem(
    `affected: no default branch to compare with (origin/HEAD, ${DEFAULT_BRANCHES.join(", ")}); name one: verify affected BASE`,
    EXIT_USAGE,
  );
}

function covering(recipe: Recipe, path: string): boolean {
  return (
    path === rel(recipe.path) ||
    recipe.covers.some((c) => {
      const cover = c.replace(/\/+$/, "");
      return cover === "." || path === cover || path.startsWith(`${cover}/`);
    })
  );
}

function cmdAffected(base: string | undefined): number {
  if (!insideRepository()) throw new Problem("affected compares with git history; run it inside a repository");
  const [ref, from] = base === undefined ? defaultBase() : [base, base];
  if (!git("rev-parse", "--verify", "--quiet", `${ref}^{commit}`).trim()) {
    throw new Problem(`affected: '${ref}' is not a commit here; name a branch, tag or commit`, EXIT_USAGE);
  }
  const changed = changedSince(ref).filter((path) => !isEvidencePath(path));
  const all = recipes();
  const { headroom } = settings();
  const touched = all.filter((r) => changed.some((path) => covering(r, path)));
  const uncovered = changed.filter((path) => !all.some((r) => covering(r, path)));
  console.log(`${changed.length} path(s) changed since ${from}${base === undefined ? ` (${ref.slice(0, 12)})` : ""}`);
  console.log(touched.length ? "\nRecipes these changes touch:" : "\nNo recipe covers these changes.");
  for (const r of touched) {
    console.log(`  ${r.name}  ${r.kind}  ${status(r, evidenceFor(r), headroom).split(": ")[0] ?? ""}${r.askFirst ? "  ask-first" : ""}`);
  }
  if (uncovered.length) {
    console.log("\nChanged paths no recipe covers:");
    for (const path of uncovered) console.log(`  ${path}`);
  }
  return 0;
}

function checkProblems(): string[] {
  const problems: string[] = [];
  for (const path of markdownIn(RECIPES)) {
    let recipe: Recipe;
    try {
      recipe = parseRecipe(path);
    } catch (error) {
      if (!(error instanceof Problem)) throw error;
      problems.push(error.message);
      continue;
    }
    const file = `${recipe.name}.md`;
    for (const covered of recipe.covers) {
      if (!existsSync(join(ROOT, covered))) problems.push(`${file}: covers ${covered}, which does not exist`);
    }
    for (const scenario of recipe.scenarios) {
      // A path counts as a reference when its first directory exists here; an output
      // directory a run creates (artifacts/…) does not, and is left alone.
      for (const [token] of scenario.run.matchAll(/(?<![\w/.-])(?:[\w.-]+\/)+[\w.-]+/g)) {
        const top = join(ROOT, token.split("/")[0] ?? "");
        if (existsSync(top) && statSync(top).isDirectory() && !existsSync(join(ROOT, token))) {
          problems.push(`${file}: scenario ${scenario.name} names ${token}, which does not exist`);
        }
      }
    }
    const names = new Set(recipe.scenarios.map((s) => s.name));
    const folder = join(EVIDENCE, recipe.name);
    for (const name of existsSync(folder) ? readdirSync(folder) : []) {
      // A live run's marker is how it holds its name; one whose run is gone was left by a kill.
      if (RESERVED.test(name) && !holderAlive(join(folder, name))) {
        problems.push(`${rel(join(folder, name))}: left by a run that was killed; delete it`);
      }
    }
    for (const item of markdownIn(folder)) {
      if (!isSummary(item)) {
        // Detail kept beside the summaries is fine; a summary whose name lost its stamp is not.
        if (OUTCOME_LINE.test(splitSummary(read(item))[0])) {
          problems.push(`${rel(item)}: reads as a run summary but its name carries no stamp or date`);
        }
        continue;
      }
      let found: Evidence | undefined;
      try {
        found = readEvidence(item);
      } catch (error) {
        if (!(error instanceof Problem)) throw error;
        problems.push(error.message);
        continue;
      }
      if (!found) problems.push(`${rel(item)}: empty — a run that never finished; delete it`);
      else if (found.scenario && !names.has(found.scenario)) {
        problems.push(`${rel(item)}: scenario '${found.scenario}' is not in ${file}`);
      }
    }
  }
  return problems;
}

function cmdCheck(): number {
  const problems = checkProblems();
  for (const problem of problems) console.log(problem);
  console.log(problems.length ? `check: ${problems.length} problem(s)` : "check: ok");
  return problems.length ? 1 : 0;
}

function cmdDoctor(): number {
  const problems = checkProblems();
  const command = settings().doctor;
  if (command && spawnSync(command, { shell: true, cwd: ROOT, stdio: "inherit", env: withRun(runIdentity(undefined)) }).status !== 0) {
    problems.push(`doctor command failed: ${command}`);
  }
  for (const problem of problems) console.log(problem);
  console.log(problems.length ? "doctor: not ready" : "doctor: ok");
  return problems.length ? 1 : 0;
}

const USAGE = `usage: verify [--help] {list,help,drive,walk,eval,affected,judge,raise,freeze,doctor,check,${Object.keys(CONTROL).join(",")}} ...`;

async function main(argv: string[]): Promise<number> {
  const [command, ...rest] = argv;
  if (command === undefined || command === "-h" || command === "--help") return cmdHelp();
  // `--run ID` (or `--run=ID`) carries a value; every other option is a bare flag.
  const flags = new Set<string>();
  const args: string[] = [];
  let run: string | undefined;
  for (let i = 0; i < rest.length; i++) {
    const arg = rest[i] ?? "";
    if (arg === "--run") {
      flags.add(arg);
      run = rest[++i] ?? "";
    } else if (arg.startsWith("--run=")) {
      flags.add("--run");
      run = arg.slice("--run=".length);
    } else if (arg.startsWith("--")) flags.add(arg);
    else args.push(arg);
  }
  const control = isControl(command) ? command : undefined;
  const allowed = ["drive", "walk", "eval"].includes(command)
    ? ["--yes", "--dry-run", "--run"]
    : command === "raise"
      ? ["--yes"]
      : control && control !== "running"
        ? ["--run"]
        : [];
  const unknown = [...flags].filter((f) => !allowed.includes(f));
  const arity = (min: number, max: number): void => {
    if (unknown.length || args.length < min || args.length > max || run === "") {
      const why = unknown.length ? `unknown option ${unknown.join(" ")}` : run === "" ? "--run needs a run id" : "wrong number of arguments";
      throw new Problem(`${USAGE}\nverify ${command}: ${why}; see verify --help`, EXIT_USAGE);
    }
  };
  switch (command) {
    case "list":
      arity(0, 1);
      return cmdList(args[0]);
    case "help":
      arity(1, 1);
      return cmdShow(args[0] ?? "");
    case "drive":
    case "walk":
    case "eval":
      arity(1, 2);
      return cmdDrive(args[0] ?? "", args[1], flags.has("--yes"), flags.has("--dry-run"), command === "drive" ? undefined : command, run);
    case "affected":
      arity(0, 1);
      return cmdAffected(args[0]);
    case "judge":
      arity(3, Infinity);
      return cmdJudge(args[0] ?? "", args[1] ?? "", args[2] ?? "", args.slice(3).join(" "));
    case "raise":
    case "freeze":
      arity(2, Infinity);
      return cmdMoveLine(command, args[0] ?? "", args[1] ?? "", args.slice(2).join(" "), flags.has("--yes"));
    case "doctor":
      arity(0, 0);
      return cmdDoctor();
    case "check":
      arity(0, 0);
      return cmdCheck();
    default:
      if (control) {
        arity(0, 0);
        return cmdControl(control, run);
      }
      throw new Problem(`${USAGE}\nverify: unknown command '${command}'`, EXIT_USAGE);
  }
}

main(process.argv.slice(2)).then(
  (code) => {
    process.exitCode = code;
  },
  (error: unknown) => {
    if (!(error instanceof Problem)) throw error;
    console.error(`verify: ${error.message}`);
    process.exitCode = error.code;
  },
);
VERIFY_TOOL_EOF
chmod +x scripts/verify
cat > verification/harness.md <<'EOF'
---
ask-first: ask
---
- Run commands from the repository root with Python 3; nothing else to start.
EOF
cat > verification/recipes/checkout.md <<'EOF'
---
kind: feature
covers: src/shelfnote.py
---
# Check out a book

A member borrows a book; the loan is recorded with today's date.

## How a user reaches it

- `python3 src/shelfnote.py checkout --member <name> --book <title>`

## Scenarios

### run
Run: `python3 src/shelfnote.py checkout --member ana --book Middlemarch`
Proves: the loan appears in `data/loans.json` with today's date.
Check: read

EOF
cat > verification/recipes/overdue.md <<'EOF'
---
kind: feature
covers: src/shelfnote.py
---
# Overdue list

Lists the loans past their due date.

## How a user reaches it

- `python3 src/shelfnote.py overdue`

## Scenarios

### run
Run: `python3 src/shelfnote.py overdue`
Proves: every loan older than 21 days is listed once, oldest first.
Check: read

EOF
cat > verification/recipes/export.md <<'EOF'
---
kind: feature
covers: src/shelfnote.py
---
# Export

Writes every loan out for a spreadsheet.

## How a user reaches it

- `python3 src/shelfnote.py export --csv`

## Scenarios

### run
Run: `python3 src/shelfnote.py export --csv`
Proves: a CSV with one row per loan is written to stdout.
Check: read

EOF
mkdir -p verification/evidence/checkout
cat > verification/evidence/checkout/20260930T101500Z.md <<'EOF'
# checkout / run — 20260930T101500Z

- **Scenario:** run
- **Command:** `python3 src/shelfnote.py checkout --member ana --book Middlemarch`
- **Exit code:** 0
- **Outcome:** verified

Judged: the output matched what the scenario proves.
EOF
mkdir -p verification/evidence/export
cat > verification/evidence/export/20260811T090000Z.md <<'EOF'
# export / run — 20260811T090000Z

- **Scenario:** run
- **Command:** `python3 src/shelfnote.py export --csv`
- **Exit code:** 0
- **Outcome:** verified

Judged: the output matched what the scenario proves.
EOF
