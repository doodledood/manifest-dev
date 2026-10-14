#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr src
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

## Project surfaces

This project keeps its direction, vocabulary, and decision memory in the repo. Read
`NORTH_STAR.md` and `CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — why this project exists and who it's for.
- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
EOF
cat > CONTEXT.md <<'EOF'
# Shelfnote

Tracks borrowed books for a reading club.

## Language

**Loan**:
One book lent to one member, from checkout to return.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Shelfnote

## Who it's for

Volunteer organizers of small reading clubs.

— hypothesis: from the README. 2026-05
EOF
cat > docs/adr/CONVENTIONS.md <<'EOF'
# ADR Conventions

Write a record for a decision that shapes the system or would be costly to reverse.

## Template

```markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label]

## Context
## Decision
## Alternatives Considered
## Consequences
## Source
```

Files are `docs/adr/YYYYMMDD-kebab-case-title.md`. Writing a record is one act: the record,
the restatus of what it changes, and the index.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-05-02 | [Loans are stored in one JSON file](20260502-loans-in-one-json-file.md) | Accepted | Storage |
EOF
cat > docs/adr/20260502-loans-in-one-json-file.md <<'EOF'
# ADR: Loans are stored in one JSON file

## Status
Accepted

## Area
Storage

## Context
A club has at most a few hundred loans.

## Decision
All loans live in `data/loans.json`, written only by `src/store.py`.

## Alternatives Considered
- **SQLite**: more than the club needs.

## Consequences
### Positive
- Nothing to install.
### Negative
- One writer at a time.

## Source
- Session: (none)
EOF
cat > src/store.py <<'EOF'
# Enforces docs/adr/20260502-loans-in-one-json-file.md: the only writer of data/loans.json.
import json, pathlib
PATH = pathlib.Path("data/loans.json")
def save(loans):
    PATH.write_text(json.dumps(loans))
EOF

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
#!/usr/bin/env python3
"""verify — this project's one verification harness.

Run `verify --help` for everything: what can be checked, how, what each status means, and
which checks to ask about before running. Recipes are Markdown files in the recipes
directory; this file reads them and never needs editing to add one.

Standard library only, so it runs wherever Python 3.9+ does.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Where the harness keeps its data. A project that moves it changes these two lines.
ROOT = Path(os.environ.get("VERIFY_ROOT") or Path(__file__).resolve().parent.parent)
DATA = Path(os.environ.get("VERIFY_DATA") or ROOT / "verification")
RECIPES = DATA / "recipes"
EVIDENCE = DATA / "evidence"
SETTINGS = DATA / "harness.md"

EXIT_UNREACHABLE = 3  # a scenario command exits 3 when a prerequisite is missing
EXIT_ASK_FIRST = 4  # this harness refused an ask-first recipe without --yes
OUTCOMES = ("verified", "failed", "unreachable", "unjudged")
STAMP = re.compile(r"(\d{8}T\d{6}Z)(?:-\d+)?")
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# Committed evidence must not carry paths that exist only on the machine that ran it.
DRIFT = re.compile(r"^Drift \((\d{4}-\d{2}-\d{2})\): (.+)$", re.MULTILINE)
LOCAL_PATH = re.compile(r"`?(?:~|/home/[^/\s]+|/tmp|/Users|/private|/var/folders)/[^\s`]*`?")


def die(message: str, code: int = 1) -> None:
    print(f"verify: {message}", file=sys.stderr)
    sys.exit(code)


def front_matter(text: str) -> tuple[dict[str, str], str]:
    """`key: value` lines between `---` fences, and the body after them."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter has no closing `---`")
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"front matter line is not `key: value`: {line!r}")
        meta[key.strip()] = value.strip()
    return meta, text[end + 5 :]


@dataclass
class Scenario:
    name: str
    run: str
    proves: str
    judged: bool  # True: a person or agent reads the evidence; False: the exit code decides


@dataclass
class Recipe:
    name: str
    path: Path
    kind: str
    title: str
    summary: str
    covers: list[str]
    ask_first: str  # the reason, or "" for a recipe that runs freely
    dry_run: bool  # its commands honor VERIFY_DRY_RUN=1
    scenarios: list[Scenario] = field(default_factory=list)
    body: str = ""


def parse_recipe(path: Path) -> Recipe:
    meta, body = front_matter(path.read_text(encoding="utf-8"))
    if "kind" not in meta:
        raise ValueError(f"{path.name}: front matter has no `kind:`")
    title = next((line[2:].strip() for line in body.splitlines() if line.startswith("# ")), "")
    if not title:
        raise ValueError(f"{path.name}: no `# Title` line")
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.lstrip().startswith("#")]
    scenarios = []
    section = re.search(r"^## Scenarios\s*$(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
    if section:
        for block in re.split(r"^### ", section.group(1), flags=re.MULTILINE)[1:]:
            name, _, rest = block.partition("\n")
            run = re.search(r"^Run:\s*`([^`]+)`", rest, re.MULTILINE)
            proves = re.search(r"^Proves:\s*(.+)$", rest, re.MULTILINE)
            check = re.search(r"^Check:\s*(\S+)", rest, re.MULTILINE)
            if not run:
                raise ValueError(f"{path.name}: scenario {name.strip()!r} has no Run: `command` line")
            if check and check.group(1) not in ("read", "exit"):
                raise ValueError(f"{path.name}: scenario {name.strip()!r} Check: must be `read` or `exit`")
            scenarios.append(
                Scenario(
                    name.strip(),
                    run.group(1),
                    proves.group(1).strip() if proves else "",
                    bool(check and check.group(1) == "read"),
                )
            )
    return Recipe(
        name=path.stem,
        path=path,
        kind=meta["kind"],
        title=title,
        summary=paragraphs[0].replace("\n", " ") if paragraphs else "",
        covers=[c.strip() for c in meta.get("covers", "").split(",") if c.strip()],
        ask_first=meta.get("ask-first", ""),
        dry_run=meta.get("dry-run", "") == "honored",
        scenarios=scenarios,
        body=body,
    )


def recipes() -> list[Recipe]:
    if not RECIPES.is_dir():
        die(f"no recipes directory at {RECIPES}")
    return [parse_recipe(p) for p in sorted(RECIPES.glob("*.md"))]


def find(name: str) -> Recipe:
    path = RECIPES / f"{name}.md"
    if not path.exists():
        known = ", ".join(r.name for r in recipes())
        die(f"no recipe {name!r}. Known: {known}")
    return parse_recipe(path)


def settings() -> tuple[dict[str, str], str]:
    if not SETTINGS.exists():
        return {"ask-first": "ask"}, ""
    meta, body = front_matter(SETTINGS.read_text(encoding="utf-8"))
    meta.setdefault("ask-first", "ask")
    if meta["ask-first"] not in ("ask", "run"):
        die(f"{SETTINGS}: ask-first must be `ask` or `run`, not {meta['ask-first']!r}")
    return meta, body.strip()


# --- evidence and statuses -------------------------------------------------------------


@dataclass
class Evidence:
    path: Path
    when: dt.datetime
    scenario: str
    outcome: str


def read_evidence(path: Path) -> Evidence:
    text = path.read_text(encoding="utf-8")
    stamp = STAMP.search(path.stem)
    if stamp:
        when = dt.datetime.strptime(stamp.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
    else:
        date = DATE.search(path.stem)
        if not date:
            raise ValueError(f"{path}: evidence file name carries no stamp or date")
        when = dt.datetime.strptime(date.group(1), "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    outcome = re.search(r"^- \*\*Outcome:\*\* (\w+)", text, re.MULTILINE)
    scenario = re.search(r"^- \*\*Scenario:\*\* (.+)$", text, re.MULTILINE)
    found = outcome.group(1) if outcome else "unjudged"
    if found not in OUTCOMES:
        raise ValueError(f"{path}: outcome {found!r} is not one of {OUTCOMES}")
    return Evidence(path, when, scenario.group(1).strip() if scenario else "", found)


def evidence_for(recipe: Recipe) -> list[Evidence]:
    folder = EVIDENCE / recipe.name
    return sorted((read_evidence(p) for p in folder.glob("*.md")), key=lambda e: e.when) if folder.is_dir() else []


def last_change(paths: list[str]) -> dt.datetime | None:
    """When the covered paths last changed: uncommitted edits count as now."""
    if not paths:
        return None
    git = ["git", "-C", str(ROOT)]
    dirty = subprocess.run([*git, "status", "--porcelain", "--", *paths], capture_output=True, text=True)
    if dirty.returncode == 0 and dirty.stdout.strip():
        return dt.datetime.now(dt.timezone.utc)
    log = subprocess.run([*git, "log", "-1", "--format=%cI", "--", *paths], capture_output=True, text=True)
    if log.returncode != 0 or not log.stdout.strip():
        return None
    return dt.datetime.fromisoformat(log.stdout.strip()).astimezone(dt.timezone.utc)


def status(recipe: Recipe, history: list[Evidence] | None = None) -> str:
    history = evidence_for(recipe) if history is None else history
    drift = DRIFT.findall(recipe.body)
    latest_drift = max(drift) if drift else None
    if latest_drift and (not history or latest_drift[0] >= f"{history[-1].when:%Y-%m-%d}"):
        return f"stale ({latest_drift[0]}): {latest_drift[1]}"
    if not history:
        return "unverified"
    latest = history[-1]
    label = f"{latest.outcome} ({latest.when:%Y-%m-%d})"
    changed = last_change(recipe.covers)
    # A day's slack: evidence dated by day only would otherwise go stale on its own commit.
    if changed and changed.date() > latest.when.date():
        return f"stale ({changed:%Y-%m-%d}): covered files changed after {label}"
    return label


# --- commands ---------------------------------------------------------------------------

HELP = """\
verify — this project's one place to check that its work still does its job.

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
`list` and `help`. This project's setting: ask-first = {policy}.
  ask  run an ask-first recipe only when a person runs it or has agreed; then pass --yes
  run  run them freely
Change it in {settings}. Recipes without the mark run freely.

Statuses (worked out from evidence; nothing to keep current by hand):
  unverified            no evidence yet; proves nothing
  verified (DATE)       the latest run passed
  failed (DATE)         the latest run failed
  unreachable (DATE)    the latest run could not start: a prerequisite was missing
  unjudged (DATE)       the latest run finished; its proof needs reading — see `verify judge`
  stale (DATE): ...     what the recipe covers changed after its latest evidence, or someone
                        found it drifting and added `Drift (DATE): what differs` to the recipe

Evidence: each run writes {evidence}/RECIPE/STAMP.md (command, exit code, outcome, output with
local paths removed). Commit it with the change it checked.

Adding a recipe: copy any file in {recipes}, keep the front matter keys (kind, covers,
ask-first when it applies, dry-run: honored when its commands obey VERIFY_DRY_RUN=1), and give
each scenario a `### name` heading with `Run:`, `Proves:` and, when the exit code cannot decide,
`Check: read`. `verify check` validates it.
"""


def cmd_help() -> None:
    meta, notes = settings()
    print(
        HELP.format(
            recipes=rel(RECIPES), evidence=rel(EVIDENCE), settings=rel(SETTINGS), policy=meta["ask-first"]
        )
    )
    if notes:
        print("This project's notes:\n")
        print(notes)
    print(f"\nRecipes: {len(recipes())}. Run `verify list` to see them.")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def cmd_list(kind: str | None) -> None:
    rows = [(r.name, r.kind, status(r), "ask-first" if r.ask_first else "") for r in recipes()]
    rows = [row for row in rows if kind is None or row[1] == kind]
    if not rows:
        die(f"no recipes of kind {kind!r}")
    widths = [max(len(row[i]) for row in rows) for i in range(3)]
    for name, rkind, rstatus, mark in rows:
        print(f"{name:<{widths[0]}}  {rkind:<{widths[1]}}  {rstatus:<{widths[2]}}  {mark}".rstrip())


def cmd_show(name: str) -> None:
    recipe = find(name)
    history = evidence_for(recipe)
    print(f"{rel(recipe.path)} — {recipe.kind} — {status(recipe, history)}")
    if recipe.ask_first:
        print(f"ask-first: {recipe.ask_first}")
    print(recipe.body.strip())
    print("\nLatest evidence per scenario:")
    for scenario in recipe.scenarios:
        mine = [e for e in history if e.scenario == scenario.name]
        print(f"  {scenario.name}: " + (f"{mine[-1].outcome}, {rel(mine[-1].path)}" if mine else "none"))


def reserve(recipe: Recipe) -> tuple[Path, str]:
    folder = EVIDENCE / recipe.name
    folder.mkdir(parents=True, exist_ok=True)
    stamp = os.environ.get("VERIFY_STAMP") or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate, n = stamp, 1
    while True:
        path = folder / f"{candidate}.md"
        try:
            # Exclusive create: two runs started the same second each get their own file.
            with path.open("x", encoding="utf-8"):
                return path, candidate
        except FileExistsError:
            n += 1
            candidate = f"{stamp}-{n}"


def cmd_drive(name: str, only: str | None, yes: bool, dry: bool, kind: str | None) -> int:
    recipe = find(name)
    if kind and recipe.kind != kind:
        die(f"{name} is of kind {recipe.kind}; use `verify drive {name}`")
    chosen = [s for s in recipe.scenarios if only in (None, s.name)]
    if not chosen:
        die(f"{name} has no scenario {only!r}" if only else f"{name} has no scenarios to run")
    policy = settings()[0]["ask-first"]
    if recipe.ask_first and policy == "ask" and not yes and not dry:
        die(
            f"{name} is ask-first: {recipe.ask_first}. Run it only when a person runs it or has "
            "agreed, then pass --yes.",
            EXIT_ASK_FIRST,
        )
    worst = 0
    for scenario in chosen:
        if dry:
            print(f"would run [{scenario.name}]: {scenario.run}")
            print(f"evidence:  {rel(EVIDENCE / recipe.name)}/<stamp>.md")
            if recipe.dry_run:
                env = {**os.environ, "VERIFY_DRY_RUN": "1"}
                subprocess.run(scenario.run, shell=True, cwd=ROOT, env=env, check=False)
            continue
        path, stamp = reserve(recipe)
        print(f"running [{scenario.name}]: {scenario.run}", flush=True)
        done = subprocess.run(scenario.run, shell=True, cwd=ROOT, capture_output=True, text=True)
        if done.returncode == EXIT_UNREACHABLE:
            outcome = "unreachable"
        elif done.returncode != 0:
            outcome = "failed"
        else:
            outcome = "unjudged" if scenario.judged else "verified"
        output = LOCAL_PATH.sub("[local path]", (done.stdout + done.stderr).strip())
        path.write_text(
            f"# {recipe.name} / {scenario.name} — {stamp}\n\n"
            f"- **Scenario:** {scenario.name}\n"
            f"- **Command:** `{scenario.run}`\n"
            f"- **Exit code:** {done.returncode}\n"
            f"- **Outcome:** {outcome}\n"
            f"- **Proves:** {scenario.proves or '(not stated)'}\n\n"
            f"## Output\n\n{output or '(none)'}\n",
            encoding="utf-8",
        )
        print(done.stdout, end="")
        print(done.stderr, end="", file=sys.stderr)
        print(f"{outcome}: evidence in {rel(path)}")
        worst = max(worst, 0 if outcome in ("verified", "unjudged") else 1)
    return worst


def cmd_judge(name: str, evidence: str, verdict: str, note: str) -> None:
    recipe = find(name)
    path = EVIDENCE / recipe.name / (evidence if evidence.endswith(".md") else f"{evidence}.md")
    if not path.exists():
        die(f"no evidence {rel(path)}")
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(r"^- \*\*Outcome:\*\* \w+", f"- **Outcome:** {verdict}", text, count=1, flags=re.MULTILINE)
    if not count:
        text = text.replace("\n\n", f"\n\n- **Outcome:** {verdict}\n", 1)
    if note:
        text += f"\n## Verdict\n\n{verdict}: {note}\n"
    path.write_text(text, encoding="utf-8")
    print(f"{rel(path)}: {verdict}")


def check_problems() -> list[str]:
    problems = []
    for path in sorted(RECIPES.glob("*.md")):
        try:
            recipe = parse_recipe(path)
        except ValueError as error:
            problems.append(str(error))
            continue
        for covered in recipe.covers:
            if not (ROOT / covered).exists():
                problems.append(f"{path.name}: covers {covered}, which does not exist")
        for scenario in recipe.scenarios:
            # A path counts as a reference when its first directory exists here; an output
            # directory a run creates (artifacts/…) does not, and is left alone.
            for token in re.findall(r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+)", scenario.run):
                if (ROOT / token.split("/")[0]).is_dir() and not (ROOT / token).exists():
                    problems.append(f"{path.name}: scenario {scenario.name} names {token}, which does not exist")
        for item in evidence_for(recipe) if (EVIDENCE / recipe.name).is_dir() else []:
            if item.scenario and item.scenario not in {s.name for s in recipe.scenarios}:
                problems.append(f"{rel(item.path)}: scenario {item.scenario!r} is not in {path.name}")
    return problems


def cmd_check() -> int:
    problems = check_problems()
    for problem in problems:
        print(problem)
    print("check: ok" if not problems else f"check: {len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_doctor() -> int:
    meta, _ = settings()
    problems = check_problems()
    command = meta.get("doctor", "")
    if command:
        done = subprocess.run(command, shell=True, cwd=ROOT, check=False)
        if done.returncode:
            problems.append(f"doctor command failed: {command}")
    for problem in problems:
        print(problem)
    print("doctor: ok" if not problems else "doctor: not ready")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        cmd_help()
        return 0
    parser = argparse.ArgumentParser(prog="verify", add_help=False)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list").add_argument("kind", nargs="?")
    sub.add_parser("help").add_argument("recipe")
    for verb in ("drive", "walk", "eval"):
        p = sub.add_parser(verb)
        p.add_argument("recipe")
        p.add_argument("scenario", nargs="?")
        p.add_argument("--yes", action="store_true")
        p.add_argument("--dry-run", action="store_true")
    j = sub.add_parser("judge")
    j.add_argument("recipe")
    j.add_argument("evidence")
    j.add_argument("verdict", choices=("verified", "failed"))
    j.add_argument("note", nargs="*")
    sub.add_parser("doctor")
    sub.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "list":
        cmd_list(args.kind)
    elif args.command == "help":
        cmd_show(args.recipe)
    elif args.command in ("drive", "walk", "eval"):
        kind = None if args.command == "drive" else args.command
        return cmd_drive(args.recipe, args.scenario, args.yes, args.dry_run, kind)
    elif args.command == "judge":
        cmd_judge(args.recipe, args.evidence, args.verdict, " ".join(args.note))
    elif args.command == "doctor":
        return cmd_doctor()
    elif args.command == "check":
        return cmd_check()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except ValueError as error:
        die(str(error))
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

cat >> CLAUDE.md <<'EOF'
- **Verification** — `scripts/verify`: how this project checks that its work still does its job.
  Run `scripts/verify --help` before saying a change works; a change to something a recipe covers
  updates that recipe and runs it, and a change with no recipe adds one. Ask before running a
  recipe marked ask-first.
EOF
