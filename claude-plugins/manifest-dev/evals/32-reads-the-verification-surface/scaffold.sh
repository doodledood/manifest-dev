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
import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdirSync, openSync, closeSync, readdirSync, readFileSync, readlinkSync, rmSync, statSync, writeFileSync } from "node:fs";
import { constants } from "node:os";
import { isAbsolute, join, relative, resolve } from "node:path";

// Where the harness keeps its data. A project that moves it changes these lines.
const ROOT = resolve(process.env.VERIFY_ROOT || join(import.meta.dirname, ".."));
const DATA = resolve(process.env.VERIFY_DATA || join(ROOT, "verification"));
const RECIPES = join(DATA, "recipes");
const EVIDENCE = join(DATA, "evidence");
const SETTINGS = join(DATA, "harness.md");

const EXIT_UNREACHABLE = 3; // a scenario command exits 3 when a prerequisite is missing
const EXIT_ASK_FIRST = 4; // this harness refused an ask-first recipe without --yes
const EXIT_USAGE = 2;

const OUTCOMES = ["verified", "failed", "unreachable", "unjudged"] as const;
type Outcome = (typeof OUTCOMES)[number];
// Worst first: a recipe shows the worst of its scenarios' latest outcomes.
const SEVERITY: Record<Outcome, number> = { failed: 3, unreachable: 2, unjudged: 1, verified: 0 };

const STAMP = /(\d{8}T\d{6}Z)(?:-(\d+))?/;
const DATE = /(\d{4}-\d{2}-\d{2})/;
// On its own line, or as a list item among the recipe's traps.
const DRIFT = /^(?:[-*] )?Drift \((\d{4}-\d{2}-\d{2})\): (.+)$/gm;
const OUTCOME_LINE = /^- \*\*Outcome:\*\* (\w+)/m;
const COVERS_LINE = /^- \*\*Covers:\*\* (\S+)/m;
// Committed evidence must not carry paths that exist only on the machine that ran it.
const LOCAL_PATH = /`?(?:~|\/home\/[^/\s]+|\/tmp|\/Users|\/private|\/var\/folders)\/[^\s`]*`?/g;

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

interface Evidence {
  path: string;
  when: Date;
  order: number; // the -N suffix of runs stamped in the same second; 1 for the first
  scenario: string; // "" for evidence that covered the whole recipe
  outcome: Outcome;
  covers: string; // fingerprint of the covered files when it ran; "" in evidence from before
}

const read = (path: string): string => readFileSync(path, "utf8");
const day = (when: Date): string => when.toISOString().slice(0, 10);
const rel = (path: string): string => {
  const inside = relative(ROOT, path);
  return inside && !inside.startsWith("..") && !isAbsolute(inside) ? inside : path;
};
const markdownIn = (folder: string): string[] =>
  existsSync(folder) && statSync(folder).isDirectory()
    ? readdirSync(folder).filter((name) => name.endsWith(".md")).sort().map((name) => join(folder, name))
    : [];
const stem = (path: string): string => path.slice(path.lastIndexOf("/") + 1).replace(/\.md$/, "");

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
    if (!run?.[1]) throw new Problem(`${file}: scenario '${name}' has no Run: \`command\` line`);
    if (check && check[1] !== "read" && check[1] !== "exit") {
      throw new Problem(`${file}: scenario '${name}' Check: must be \`read\` or \`exit\``);
    }
    scenarios.push({ name, run: run[1], proves: proves?.[1]?.trim() ?? "", judged: check?.[1] === "read" });
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

function settings(): [Record<string, string> & { "ask-first": string }, string] {
  const [meta, body] = existsSync(SETTINGS) ? frontMatter(read(SETTINGS)) : [{}, ""];
  const policy = meta["ask-first"] ?? "ask";
  if (policy !== "ask" && policy !== "run") {
    throw new Problem(`${SETTINGS}: ask-first must be \`ask\` or \`run\`, not '${policy}'`);
  }
  return [{ ...meta, "ask-first": policy }, body.trim()];
}

// --- evidence and statuses -------------------------------------------------------------

/** True for a file named as a run summary; any other file beside them is kept detail. */
function isSummary(path: string): boolean {
  return STAMP.test(stem(path)) || DATE.test(stem(path));
}

function readEvidence(path: string): Evidence | undefined {
  const text = read(path);
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
  const outcome = OUTCOME_LINE.exec(text)?.[1] ?? "unjudged";
  if (!(OUTCOMES as readonly string[]).includes(outcome)) {
    throw new Problem(`${path}: outcome '${outcome}' is not one of ${OUTCOMES.join(", ")}`);
  }
  const scenario = /^- \*\*Scenario:\*\* (.+)$/m.exec(text)?.[1]?.trim() ?? "";
  const covers = COVERS_LINE.exec(text)?.[1] ?? "";
  return { path, when, order: Number(stamp?.[2] ?? 1), scenario, outcome: outcome as Outcome, covers };
}

/** Oldest first; runs stamped in the same second keep the order they were written in. */
function evidenceFor(recipe: Recipe): Evidence[] {
  return markdownIn(join(EVIDENCE, recipe.name))
    .filter(isSummary)
    .map(readEvidence)
    .filter((e): e is Evidence => e !== undefined)
    .sort((a, b) => a.when.getTime() - b.when.getTime() || a.order - b.order);
}

/** Output of a git command in the project, or "" outside a repository or on failure. */
function git(...args: string[]): string {
  const done = spawnSync("git", ["-C", ROOT, ...args], { encoding: "utf8" });
  return done.status === 0 ? done.stdout : "";
}

/** Every file under the covered paths, tracked or new; outside a repository, every file there. */
function coveredFiles(paths: string[]): string[] {
  if (git("rev-parse", "--is-inside-work-tree").trim() === "true") {
    const listed = git("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", ...paths);
    return [...new Set(listed.split("\0").filter(Boolean))].sort();
  }
  // A link is one entry, counted by its target, as git lists it; following it could loop.
  const walk = (path: string): string[] => {
    const full = join(ROOT, path);
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

function status(recipe: Recipe, history: Evidence[] = evidenceFor(recipe)): string {
  const drifts = [...recipe.body.matchAll(DRIFT)].map((m) => [m[1] ?? "", m[2] ?? ""] as const).sort();
  const drift = drifts.at(-1);
  const perScenario = latestPerScenario(recipe, history);
  const latest = [...new Set(perScenario.values())];
  // A scenario that never ran proves nothing, so passing the others does not verify the recipe.
  const unrun = recipe.scenarios.map((s) => s.name).filter((name) => !perScenario.has(name));
  const oldestRun = latest.reduce<Date | undefined>((a, e) => (!a || e.when < a ? e.when : a), undefined);
  // A Drift line holds until every scenario has run since it: one scenario's run repairs only itself.
  if (drift && (!oldestRun || unrun.length || drift[0] >= day(oldestRun))) return `stale (${drift[0]}): ${drift[1]}`;
  if (!latest.length) return "unverified";
  const worst = latest.reduce((a, e) => (SEVERITY[e.outcome] > SEVERITY[a.outcome] ? e : a));
  const oldest = latest.reduce((a, e) => (e.when < a.when ? e : a));
  // The date is the worst scenario's run, or for a recipe whose scenarios all passed, the
  // oldest of their runs: how fresh the weakest proof is.
  const label =
    worst.outcome === "verified" && unrun.length
      ? `unverified (${day(oldest.when)}): no run yet for ${unrun.join(", ")}`
      : `${worst.outcome} (${day(worst.outcome === "verified" ? oldest.when : worst.when)})`;
  if (!recipe.covers.length) return label;
  // Evidence that recorded what it checked is stale when the covered files now differ; older
  // evidence falls back to comparing times.
  const now = latest.some((e) => e.covers) ? fingerprint(recipe.covers) : "";
  const legacy = latest.filter((e) => !e.covers);
  const changed = legacy.length || latest.some((e) => e.covers !== now) ? lastChange(recipe.covers) : undefined;
  const stale = latest.some((e) =>
    e.covers ? e.covers !== now : changed !== undefined && changed.getTime() > checkedAt(e).getTime(),
  );
  return stale ? `stale (${day(changed ?? new Date())}): covered files changed after ${label}` : label;
}

// --- commands ---------------------------------------------------------------------------

const HELP = `verify — this project's one place to check that its work still does its job.

Every check is a recipe: a Markdown file in {recipes} naming what it covers, how a user
reaches it, the scenarios that exercise it (each a command and what it proves), and its traps.
This tool lists them, runs them, keeps their evidence, and works out their status.

Commands:
  verify list [KIND]          every recipe with its kind, status and ask-first mark
  verify help RECIPE          one recipe in full, with each scenario's latest evidence
  verify drive RECIPE [SCENARIO] [--yes] [--dry-run]
                              run a recipe's scenarios (all, or the one named) and keep evidence
  verify walk RECIPE ...      the same, for a recipe of kind walk
  verify eval RECIPE ...      the same, for a recipe of kind eval
  verify judge RECIPE EVIDENCE verified|failed [NOTE]
                              record the verdict on evidence a person or agent had to read
  verify doctor               check the harness's prerequisites (free; starts nothing costly)
  verify check                check every recipe parses and names only paths that exist

When to run it: before saying a change works, when reproducing a reported problem, and when a
change touches what a recipe covers. A change that needs a check no recipe has adds the recipe.

Ask first: a recipe marked ask-first costs something a person should weigh — money or quota,
long run time, load on shared systems, effects outside this repository. Its reason is shown in
\`verify help RECIPE\`. This project's setting: ask-first = {policy}.
  ask  run an ask-first recipe only when a person runs it or has agreed: ask first, naming the
       recipe and why; then pass --yes
  run  run them freely
Change it in {settings}. Recipes without the mark run freely.

Statuses (worked out from evidence; nothing to keep current by hand). A recipe shows the worst
of its scenarios' latest runs:
  unverified            no evidence yet; proves nothing
  unverified (DATE): .. the scenarios that ran passed, and those it names have never run
  verified (DATE)       every scenario's latest run passed; DATE is the oldest of those runs
  failed (DATE)         a scenario's latest run failed
  unreachable (DATE)    a scenario's latest run could not start: a prerequisite was missing
  unjudged (DATE)       a scenario's latest run finished; its proof needs reading — see \`verify judge\`
  stale (DATE): ...     what the recipe covers changed after that evidence, or someone found it
                        drifting and added \`Drift (DATE): what differs\` to the recipe

Evidence: each run writes {evidence}/RECIPE/STAMP.md (command, exit code, outcome, a fingerprint
of the covered files, output with local paths removed). Commit it with the change it checked.
Whatever a command started is stopped when it ends: SIGTERM, then SIGKILL after a grace. An
interrupted run keeps no evidence; a command that crashes is failed.

Adding a recipe: copy any file in {recipes}, keep the front matter keys (kind, covers,
ask-first when it applies, dry-run: honored when its commands obey VERIFY_DRY_RUN=1), and give
each scenario a \`### name\` heading with \`Run:\`, \`Proves:\` and, when the exit code cannot decide,
\`Check: read\`. \`verify check\` validates it.
`;

function cmdHelp(): number {
  const [meta, notes] = settings();
  const fill: Record<string, string> = {
    recipes: rel(RECIPES),
    evidence: rel(EVIDENCE),
    settings: rel(SETTINGS),
    policy: meta["ask-first"],
  };
  console.log(HELP.replace(/\{(\w+)\}/g, (whole, key: string) => fill[key] ?? whole));
  if (notes) console.log(`This project's notes:\n\n${notes}`);
  console.log(`\nRecipes: ${recipes().length}. Run \`verify list\` to see them.`);
  return 0;
}

function cmdList(kind: string | undefined): number {
  // The list shows each status up to its reason; `verify help <recipe>` prints the whole line.
  const rows = recipes()
    .filter((r) => kind === undefined || r.kind === kind)
    .map((r) => [r.name, r.kind, status(r).split(": ")[0] ?? "", r.askFirst ? "ask-first" : ""] as const);
  if (!rows.length) throw new Problem(`no recipes of kind '${kind}'`);
  const width = (i: 0 | 1 | 2): number => Math.max(...rows.map((row) => row[i].length));
  for (const [name, rkind, rstatus, mark] of rows) {
    console.log(`${name.padEnd(width(0))}  ${rkind.padEnd(width(1))}  ${rstatus.padEnd(width(2))}  ${mark}`.trimEnd());
  }
  return 0;
}

function cmdShow(name: string): number {
  const recipe = find(name);
  const history = evidenceFor(recipe);
  console.log(`${rel(recipe.path)} — ${recipe.kind} — ${status(recipe, history)}`);
  if (recipe.askFirst) console.log(`ask-first: ${recipe.askFirst}`);
  console.log(recipe.body.trim());
  console.log("\nLatest evidence per scenario:");
  const latest = latestPerScenario(recipe, history); // the same evidence the status is worked out from
  for (const scenario of recipe.scenarios) {
    const mine = latest.get(scenario.name);
    console.log(`  ${scenario.name}: ${mine ? `${mine.outcome}, ${rel(mine.path)}` : "none"}`);
  }
  return 0;
}

/** A fresh evidence file: two runs started in the same second each get their own. */
function reserve(recipe: Recipe): [string, string] {
  const folder = join(EVIDENCE, recipe.name);
  mkdirSync(folder, { recursive: true });
  const stamp = process.env.VERIFY_STAMP || new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
  for (let n = 1; ; n++) {
    const candidate = n === 1 ? stamp : `${stamp}-${n}`;
    const path = join(folder, `${candidate}.md`);
    try {
      closeSync(openSync(path, "wx"));
      return [path, candidate];
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    }
  }
}

interface Run {
  code: number;
  output: string;
  interrupted: boolean;
}

/** Signals that stop a run: Ctrl-C, a polite kill, a closed terminal, Ctrl-\. */
const STOP_SIGNALS: NodeJS.Signals[] = ["SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT"];

/** Seconds a stop waits between SIGTERM and SIGKILL. */
const GRACE_SECONDS = 2;

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
 * stop sends. The wrapper catches the stop signals, so a signal passed on to the command does not
 * end the wrapper and start a stop while the command is still cleaning up; the command itself
 * gets them as usual, since a caught signal is reset in a child. The command does not inherit
 * the descriptor, and its exit status is the run's.
 */
const WATCHED = [
  `( trap '' TERM HUP; read -r _ <&3; kill -TERM 0; sleep ${GRACE_SECONDS}; kill -KILL 0 ) </dev/null >/dev/null 2>&1 &`,
  "trap : INT TERM HUP QUIT",
  'sh -c "$VERIFY_COMMAND" 3<&-',
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
function runShown(command: string, interrupts: Interrupts): Promise<Run> {
  return new Promise((done, fail) => {
    // Scenario commands take no input: they run unattended, in a process group of their own.
    const child = spawn("sh", ["-c", WATCHED], {
      cwd: ROOT,
      detached: true,
      stdio: ["ignore", "pipe", "pipe", "pipe"],
      env: { ...process.env, VERIFY_COMMAND: command },
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
      });
    });
  });
}

async function cmdDrive(name: string, only: string | undefined, yes: boolean, dry: boolean, kind: string | undefined): Promise<number> {
  const recipe = find(name);
  if (kind && recipe.kind !== kind) throw new Problem(`${name} is of kind ${recipe.kind}; use \`verify drive ${name}\``);
  const chosen = recipe.scenarios.filter((s) => only === undefined || s.name === only);
  if (!chosen.length) throw new Problem(only ? `${name} has no scenario '${only}'` : `${name} has no scenarios to run`);
  if (recipe.askFirst && settings()[0]["ask-first"] === "ask" && !yes && !dry) {
    throw new Problem(
      `${name} is ask-first: ${recipe.askFirst}. Run it only when a person runs it or has agreed, then pass --yes.`,
      EXIT_ASK_FIRST,
    );
  }
  let worst = 0;
  const interrupts = new Interrupts();
  try {
    for (const scenario of chosen) {
      if (dry) {
        console.log(`would run [${scenario.name}]: ${scenario.run}`);
        console.log(`evidence:  ${rel(join(EVIDENCE, recipe.name))}/<stamp>.md`);
        if (recipe.dryRun) {
          spawnSync(scenario.run, { shell: true, cwd: ROOT, stdio: "inherit", env: { ...process.env, VERIFY_DRY_RUN: "1" } });
          // A signal that arrived during the blocking call is handled once the event loop turns.
          await new Promise((resolve) => setImmediate(resolve));
          if (interrupts.interrupted) return 130;
        }
        continue;
      }
      const [path, stamp] = reserve(recipe);
      let written = false;
      try {
        const covers = recipe.covers.length ? fingerprint(recipe.covers) : "";
        console.log(`running [${scenario.name}]: ${scenario.run}`);
        const run = interrupts.interrupted ? undefined : await runShown(scenario.run, interrupts);
        if (!run || run.interrupted) {
          console.error(`interrupted: no evidence kept for [${scenario.name}]`);
          return 130;
        }
        const outcome: Outcome =
          run.code === EXIT_UNREACHABLE ? "unreachable" : run.code !== 0 ? "failed" : scenario.judged ? "unjudged" : "verified";
        writeFileSync(
          path,
          `# ${recipe.name} / ${scenario.name} — ${stamp}\n\n` +
            `- **Scenario:** ${scenario.name}\n` +
            `- **Command:** \`${scenario.run}\`\n` +
            `- **Exit code:** ${run.code}\n` +
            `- **Outcome:** ${outcome}\n` +
            (covers ? `- **Covers:** ${covers}\n` : "") +
            `- **Proves:** ${scenario.proves || "(not stated)"}\n\n` +
            `## Output\n\n${run.output.trim().replace(LOCAL_PATH, "[local path]") || "(none)"}\n`,
        );
        written = true;
        console.log(`${outcome}: evidence in ${rel(path)}`);
        if (outcome === "failed" || outcome === "unreachable") worst = 1;
      } finally {
        // A run that did not finish leaves nothing behind to pass for evidence.
        if (!written) rmSync(path, { force: true });
      }
    }
  } finally {
    interrupts.release();
  }
  return worst;
}

function cmdJudge(name: string, evidence: string, verdict: string, note: string): number {
  if (verdict !== "verified" && verdict !== "failed") {
    throw new Problem("judge: the verdict is `verified` or `failed`", EXIT_USAGE);
  }
  const recipe = find(name);
  const path = join(EVIDENCE, recipe.name, evidence.endsWith(".md") ? evidence : `${evidence}.md`);
  if (!existsSync(path)) throw new Problem(`no evidence ${rel(path)}`);
  let text = read(path);
  text = OUTCOME_LINE.test(text)
    ? text.replace(OUTCOME_LINE, `- **Outcome:** ${verdict}`)
    : text.replace("\n\n", `\n\n- **Outcome:** ${verdict}\n`);
  if (note) text += `\n## Verdict\n\n${verdict}: ${note}\n`;
  writeFileSync(path, text);
  console.log(`${rel(path)}: ${verdict}`);
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
    for (const item of markdownIn(join(EVIDENCE, recipe.name))) {
      if (!isSummary(item)) {
        // Detail kept beside the summaries is fine; a summary whose name lost its stamp is not.
        if (OUTCOME_LINE.test(read(item))) {
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
  const command = settings()[0].doctor ?? "";
  if (command && spawnSync(command, { shell: true, cwd: ROOT, stdio: "inherit" }).status !== 0) {
    problems.push(`doctor command failed: ${command}`);
  }
  for (const problem of problems) console.log(problem);
  console.log(problems.length ? "doctor: not ready" : "doctor: ok");
  return problems.length ? 1 : 0;
}

const USAGE = "usage: verify [--help] {list,help,drive,walk,eval,judge,doctor,check} ...";

async function main(argv: string[]): Promise<number> {
  const [command, ...rest] = argv;
  if (command === undefined || command === "-h" || command === "--help") return cmdHelp();
  const flags = new Set(rest.filter((a) => a.startsWith("--")));
  const args = rest.filter((a) => !a.startsWith("--"));
  const allowed = ["drive", "walk", "eval"].includes(command) ? ["--yes", "--dry-run"] : [];
  const unknown = [...flags].filter((f) => !allowed.includes(f));
  const arity = (min: number, max: number): void => {
    if (unknown.length || args.length < min || args.length > max) {
      throw new Problem(`${USAGE}\nverify ${command}: ${unknown.length ? `unknown option ${unknown.join(" ")}` : "wrong number of arguments"}; see verify --help`, EXIT_USAGE);
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
      return cmdDrive(args[0] ?? "", args[1], flags.has("--yes"), flags.has("--dry-run"), command === "drive" ? undefined : command);
    case "judge":
      arity(3, Infinity);
      return cmdJudge(args[0] ?? "", args[1] ?? "", args[2] ?? "", args.slice(3).join(" "));
    case "doctor":
      arity(0, 0);
      return cmdDoctor();
    case "check":
      arity(0, 0);
      return cmdCheck();
    default:
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
