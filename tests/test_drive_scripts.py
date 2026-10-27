"""Skill drives, document walks and eval suites start the claude CLI directly, isolated.

`scripts/drive-skill.sh`, `scripts/walk.sh` and `scripts/evals/run_eval.sh` run with no
container: each starts `claude` from a scratch directory outside the checkout, hands it a copy
of the plugin rather than the checkout's own directory, and starts it with no user settings and
no MCP servers of the user's (`--setting-sources project,local --strict-mcp-config`, which
`claude --help` describes as loading only the named setting sources and only the MCP servers
given on the command line). The CLI version is recorded, not pinned. Every test here puts a
stand-in `claude` first on PATH that records how it was called, with no `docker` anywhere on
PATH, so a script that still reached for a container would fail.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import signal
import subprocess
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict, TypeVar

import pytest

T = TypeVar("T")

REPO_ROOT = Path(__file__).resolve().parent.parent
DRIVE = REPO_ROOT / "scripts" / "drive-skill.sh"
WALK = REPO_ROOT / "scripts" / "walk.sh"
RUN_EVAL = REPO_ROOT / "scripts" / "evals" / "run_eval.sh"
LIB = REPO_ROOT / "scripts" / "lib" / "claude-cli.sh"
RECIPES = REPO_ROOT / "verification" / "recipes"
PLUGIN = REPO_ROOT / "claude-plugins" / "manifest-dev"
VERSION = "9.9.9 (Claude Code)"
STAMP = "20990101T000000Z"
ISOLATION = ["--setting-sources", "project,local", "--strict-mcp-config"]

# A session the drive accepts: it loaded the copy it was handed and the skill under test.
GOOD: list[dict[str, object]] = [
    {
        "type": "system",
        "subtype": "init",
        "model": "m",
        "plugins": [{"name": "manifest-dev", "path": "{plugin_dir}"}],
        "skills": ["manifest-dev:figure-out"],
    },
    {"type": "result", "num_turns": 1, "result": "done"},
]

STANDIN = r"""#!/usr/bin/env python3
# Stands in for the claude CLI: answers --version and auth status, and records every other call
# (arguments, working directory, environment, session) before acting like a session or a suite.
import json, os, pathlib, sys, time
args = sys.argv[1:]
if args == ["--version"]:
    print(os.environ["STANDIN_VERSION"]); sys.exit(0)
if args[:2] == ["auth", "status"]:
    print(json.dumps({"loggedIn": os.environ.get("STANDIN_LOGGED_IN", "1") == "1"})); sys.exit(0)
if "eval" in args and "--max-cost-usd" in args and args[len(args)-args[::-1].index("--max-cost-usd")] == "0":
    out = pathlib.Path(args[len(args)-args[::-1].index("--json")])
    out.write_text(json.dumps({"claudeVersion": "9.9.9", "costUsd": 0, "partial": True,
                               "partialReason": "cost_ceiling", "cases": []}))
    pathlib.Path(os.environ["STANDIN_RECORD"] + ".preflight").write_text(json.dumps(args))
    if os.environ.get("STANDIN_PREFLIGHT_INVALID"):
        print("1 case file(s) failed to load", file=sys.stderr)
    sys.exit(2)
home = pathlib.Path(os.environ.get("HOME", "/nonexistent"))
links = {p.name: os.readlink(p) if p.is_symlink() else None for p in home.iterdir()} if home.is_dir() else {}
seen = sorted(str(p.relative_to(home)) for p in (home / ".manifest-dev").rglob("*")) if (home / ".manifest-dev").is_dir() else []
with open(os.environ["STANDIN_RECORD"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"args": args, "cwd": os.getcwd(), "env": dict(os.environ),
                        "pid": os.getpid(), "sid": os.getsid(0), "home": links,
                        "seen": seen}) + "\n")
code = int(os.environ.get("STANDIN_EXIT", "0"))
if "eval" in args:
    release = os.environ.get("STANDIN_RELEASE")
    deadline = time.monotonic() + 30
    while release and not os.path.exists(release) and time.monotonic() < deadline:
        time.sleep(0.05)
    if os.environ.get("STANDIN_WRITES_RESULT", "1") == "1":
        out = pathlib.Path(args[args.index("--json") + 1])
        contract = json.loads(out.with_suffix(".instrument.json").read_text())
        cases = []
        for case in contract["cases"]:
            arms = {}
            for arm in (["with", "without"] if contract["ablation"] == "with-without" else ["with"]):
                graders = []
                for g in case["graders"]:
                    diagnostic = g["config"].get("arm") == "with-only" or (g["type"] == "tool_used" and g["config"].get("tool") == "Skill")
                    if arm == "without" and diagnostic:
                        continue
                    graders.append({"name": g["name"], "passed": True, "weight": g["weight"],
                                    "scored": not diagnostic or contract["ablation"] == "none",
                                    "judgeVotes": [True, True, True]})
                arms[arm] = [{"costUsd": 0, "tracePath": f"/stub/{case['name']}/{arm}/{i}/trace.jsonl", "graders": graders} for i in range(case["runs"])]
            cases.append({"name": case["name"], "promptMarkdown": case["prompt"], "graders": case["graders"], "arms": arms,
                          "model": case["sourceModel"], "maxTurns": case["maxTurns"], "timeoutSeconds": case["timeoutSeconds"]})
        out.write_text(json.dumps({"claudeVersion": "9.9.9", "suite": {"ablation": contract["ablation"],
                       "judgeModel": contract["judgeModel"]}, "cases": cases}), encoding="utf-8")
    sys.exit(code)
record = os.environ.get("STANDIN_WRITES_RECORD")
if record:
    path = pathlib.Path(os.environ["HOME"], ".manifest-dev", record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("a workflow record\n", encoding="utf-8")
time.sleep(float(os.environ.get("STANDIN_SLEEP", "0")))
plugin_dir = args[args.index("--plugin-dir") + 1] if "--plugin-dir" in args else ""
transcript = os.environ.get("STANDIN_TRANSCRIPT", "")
sys.stdout.write(transcript.replace("{plugin_dir}", plugin_dir))
sys.exit(code)
"""


@pytest.fixture(scope="session")
def toolbox(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The system's commands, less any container tool and any real claude."""
    box = tmp_path_factory.mktemp("toolbox")
    for directory in ("/usr/local/bin", "/usr/bin", "/bin"):
        if not os.path.isdir(directory):
            continue
        for entry in os.scandir(directory):
            if entry.name in {"docker", "colima", "podman", "claude"}:
                continue
            target = box / entry.name
            if not target.exists() and os.access(entry.path, os.X_OK):
                target.symlink_to(entry.path)
    # The eval inventory compiles patterns with the same JS RegExp language as Claude.
    if not (box / "node").exists():
        node = shutil.which("node")
        assert node, "scripts/setup.sh requires Node"
        (box / "node").symlink_to(node)
    return box


def lines(events: list[dict[str, object]]) -> str:
    return "".join(json.dumps(e) + "\n" for e in events)


def setup(
    tmp_path: Path, toolbox: Path, *, claude: bool = True, **standin: str
) -> dict[str, str]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    if claude:
        stub = bin_dir / "claude"
        stub.write_text(STANDIN, encoding="utf-8")
        stub.chmod(0o755)
    (tmp_path / "home").mkdir(exist_ok=True)
    (tmp_path / "tmp").mkdir(exist_ok=True)
    return {
        "PATH": f"{bin_dir}:{toolbox}",
        "HOME": str(tmp_path / "home"),
        "TMPDIR": str(tmp_path / "tmp"),
        "MANIFEST_DEV_FEATURES_EVIDENCE": str(tmp_path / "store"),
        "MANIFEST_DEV_EVAL_RUNS": str(tmp_path / "runs"),
        "DRIVE_STAMP": STAMP,
        # Set as it is when a drive is started from inside a session; the drive must drop it.
        "CLAUDECODE": "1",
        "STANDIN_RECORD": str(tmp_path / "calls.jsonl"),
        "STANDIN_VERSION": VERSION,
        **standin,
    }


class Call(TypedDict):
    """One recorded call of the stand-in claude."""

    args: list[str]
    cwd: str
    env: dict[str, str]
    pid: int
    sid: int
    home: dict[str, str | None]
    seen: list[str]


def calls(tmp_path: Path) -> list[Call]:
    record = tmp_path / "calls.jsonl"
    if not record.exists():
        return []
    return json_lines(record.read_text(encoding="utf-8"))


def json_lines(text: str) -> list[Call]:
    """Parse the stand-in's call record, refusing one a writer has not finished."""
    if text and not text.endswith("\n"):
        raise ValueError("call record ends mid-line")
    return [json.loads(line) for line in text.splitlines()]


def after(args: list[str], flag: str) -> str:
    return args[args.index(flag) + 1]


def outside_checkout(path: str) -> bool:
    return not Path(path).resolve().is_relative_to(REPO_ROOT)


def assert_isolated(call: Call) -> None:
    args = call["args"]
    # No user settings (so no settings, hooks or plugins they enable) and none of the user's MCP
    # servers; `user` is the source that would load them.
    assert args[
        args.index("--setting-sources") : args.index("--setting-sources") + 2
    ] == (ISOLATION[:2])
    assert "user" not in after(args, "--setting-sources").split(",")
    assert "--strict-mcp-config" in args
    assert "CLAUDECODE" not in call["env"]
    assert outside_checkout(call["cwd"])


def drive(
    env: dict[str, str],
    *args: str,
    prompt: Path | None = None,
    feature: str = "figure-out",
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(DRIVE), feature, str(prompt or RECIPES / "figure-out.md"), *args],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def convergence_project(
    tmp_path: Path, toolbox: Path, fixture: str, prompt: str, feature: str = "do"
) -> Path:
    """Exercise the real scaffold boundary with a CLI stand-in, never a paid model."""
    env = setup(
        tmp_path,
        toolbox,
        STANDIN_TRANSCRIPT=lines(GOOD).replace(
            "manifest-dev:figure-out", f"manifest-dev:{feature}"
        ),
    )
    result = drive(
        env,
        "--scaffold",
        str(REPO_ROOT / "verification/fixtures" / fixture),
        prompt=REPO_ROOT / "verification/prompts" / prompt,
        feature=feature,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    call = calls(tmp_path)[0]
    assert_isolated(call)
    assert "Proves:" not in call["args"][-1]
    return Path(call["cwd"])


def test_criterion_scaffold_hides_the_standard_from_the_initial_prompt(
    tmp_path: Path, toolbox: Path
) -> None:
    project = convergence_project(
        tmp_path, toolbox, "criterion-discovery", "do-criterion-discovery.md"
    )
    records = json.loads((project / "customers.json").read_text())
    assert [record["id"] for record in records] == ["003", "010"]
    assert records[0]["note"] == "" and "note" not in records[1]
    assert "leading zeros" in (project / "interchange.md").read_text()
    assert "leading zeros" not in calls(tmp_path)[0]["args"][-1]
    assert not (project / "customers-export.json").exists()


def test_research_fixture_supplies_coupled_evidence_and_a_separable_question(
    tmp_path: Path, toolbox: Path
) -> None:
    project = convergence_project(
        tmp_path,
        toolbox,
        "research-delegation",
        "define-research-delegation.md",
        feature="define",
    )
    sources = project / "sources"
    incident = json.loads((sources / "incident.json").read_text())
    with (sources / incident["mapping_file"]).open() as stream:
        mapping = list(csv.DictReader(stream))
    assert [row["customer_ref"] for row in mapping] == [
        request["customer_ref"] for request in incident["requests"]
    ]
    assert mapping == [
        {"source_id": "003", "customer_ref": "3"},
        {"source_id": "014", "customer_ref": "014"},
    ]
    assert [request["status"] for request in incident["requests"]] == [404, 200]
    api = (sources / "api-snapshot.md").read_text()
    assert "v2" in api and incident["api_version"] == "2"
    assert "`003` and `014`" in api and "Leading zeroes are significant" in api
    archive = (sources / "archive-requirements.md").read_text()
    assert "CSV and JSON Lines" in archive and "nested metadata" in archive
    assert not (project / "manifest.md").exists()  # Subject must create the result.
    assert not (project / "README.md").exists()  # Rubric stays outside the subject.


def test_consolidation_fixture_preserves_review_state_and_reproducible_findings(
    tmp_path: Path, toolbox: Path
) -> None:
    transcript: list[dict[str, object]] = [
        {
            "type": "system",
            "subtype": "init",
            "model": "m",
            "plugins": [
                {"name": "manifest-dev"},
                {"name": "manifest-dev-tools"},
            ],
            "skills": ["manifest-dev-tools:review-pr"],
        },
        GOOD[1],
    ]
    result = drive(
        setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(transcript)),
        "--tools",
        "--scaffold",
        str(REPO_ROOT / "verification/fixtures/pr-consolidation"),
        prompt=REPO_ROOT / "verification/prompts/review-pr-consolidation.md",
        feature="review-pr",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    (call,) = calls(tmp_path)
    assert_isolated(call)
    project = Path(call["cwd"])
    packet = json.loads((project / "review.json").read_text())
    previous = subprocess.check_output(
        ["git", "show", f"{packet['reviewed_commit']}:order_export.py"],
        cwd=project,
        text=True,
    )
    (project / "previous.py").write_text(previous)
    result_json = subprocess.check_output(
        [
            "python3",
            "-c",
            "import json, runpy; "
            "order={'id':'003','private_note':'internal','lines':"
            "[{'sku':'B','quantity':2,'unit_price':5},"
            "{'sku':'A','quantity':1,'unit_price':7}]}; "
            "before=runpy.run_path('previous.py')['export_order']; "
            "after=runpy.run_path('order_export.py')['export_order']; "
            "print(json.dumps([before(order),after(order),"
            "after({'id':'003','lines':[]})]))",
        ],
        cwd=project,
        text=True,
    )
    before, after, empty = json.loads(result_json)
    assert before["id"] == "003" and after["id"] == 3  # New regression.
    assert "private_note" in before and "private_note" not in after  # Verified repair.
    assert after["items"] == ["B", "A"] and empty["total"] == 0
    assert after["total"] == 12  # Quantity defect is already tracked in an open thread.
    assert {item["id"] for item in packet["packets"][0]["findings"]} == {
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
    }
    assert packet["packets"][1]["blocked_evaluations"]
    assert packet["reviewed_range"] == (
        f"{packet['reviewed_commit']}..{packet['current_commit']}"
    )
    assert "Proves:" not in call["args"][-1]
    assert not (project / "consolidation.md").exists()
    assert not (project / "README.md").exists()  # Rubric stays outside the subject.
    assert "review-pr" in result.stdout  # Runner retained a summary after cleanup.


# Holds the fixture evidence for 20261024-gate-criteria-and-evidence-travel-with-execution.
def test_review_fixture_has_repair_regression_and_unchanged_findings(
    tmp_path: Path, toolbox: Path
) -> None:
    project = convergence_project(
        tmp_path,
        toolbox,
        "review-continuity",
        "review-code-follow-up.md",
        "review-code",
    )
    prior = (project / "prior-review.md").read_text()
    reviewed = prior.split("Reviewed commit: `", 1)[1].split("`", 1)[0]
    source = subprocess.check_output(
        ["git", "show", f"{reviewed}:order_export.py"], cwd=project, text=True
    )
    (project / "initial-export.py").write_text(source)
    result = subprocess.check_output(
        [
            "python3",
            "-c",
            "import json, runpy; "
            "order={'id':'003','private_note':'internal','lines':"
            "[{'sku':'B','quantity':2,'unit_price':5},"
            "{'sku':'A','quantity':1,'unit_price':7}]}; "
            "print(json.dumps([runpy.run_path(p)['export_order'](order) "
            "for p in ['initial-export.py','order_export.py']]))",
        ],
        cwd=project,
        text=True,
    )
    initial, repaired = json.loads(result)
    assert initial["private_note"] == "internal" and "private_note" not in repaired
    assert initial["total"] == repaired["total"] == 10  # Contract total is 17.
    assert initial["id"] == "003" and repaired["id"] == 3
    assert initial["items"] == repaired["items"] == ["A", "B"]  # Input order is B, A.
    assert "F1:" in prior and "F2:" in prior
    assert "identifier" not in prior and "sort" not in prior


def test_resume_fixture_changes_criteria_and_uncommitted_data_but_not_receipt(
    tmp_path: Path, toolbox: Path
) -> None:
    project = convergence_project(
        tmp_path, toolbox, "evidence-resume", "do-evidence-resume.md"
    )
    receipt = (project / "receipt.txt").read_bytes()
    old_manifest = (project / "manifest.md").read_text()
    for pending in (project / "resumed-inputs").iterdir():
        shutil.copyfile(pending, project / pending.name)
    assert "includes a header" not in old_manifest
    assert "includes a header" in (project / "manifest.md").read_text()
    assert json.loads((project / "orders.json").read_text()) == [
        {"id": "003", "quantity": 2}
    ]
    diff = subprocess.check_output(["git", "diff"], cwd=project, text=True)
    assert "orders.json" in diff and "format.md" in diff and "manifest.md" in diff
    assert (project / "receipt.txt").read_bytes() == receipt
    assert (project / "report.tsv").read_text() == "3,1\n"
    assert (project / "quantity.txt").read_text() == "1\n"
    assert (
        old_manifest.split("#### AC-1.4", 1)[1]
        == (project / "manifest.md").read_text().split("#### AC-1.4", 1)[1]
    )
    assert "AC-1.4: PASS" in (project / "execution-log.md").read_text()


# Holds fixture evidence for 20261024-external-review-feedback-needs-an-adoption-decision.
@pytest.mark.parametrize("fixture,total", [("pr-feedback", 10), ("pr-nits", 17)])
def test_feedback_snapshots_bind_to_the_runner_head_and_preserve_the_code_case(
    tmp_path: Path, toolbox: Path, fixture: str, total: int
) -> None:
    project = convergence_project(tmp_path, toolbox, fixture, "do-external-feedback.md")
    subprocess.run(["python3", "prepare-snapshots.py"], cwd=project, check=True)
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=project, text=True
    ).strip()
    for name in ("pr-state.json", "pr-nits-1.json", "pr-nits-2.json"):
        state = json.loads((project / name).read_text())["pullRequest"]
        assert state["headRefOid"] == head
        assert all(check["headSha"] == head for check in state["statusCheckRollup"])
        assert state["reviewDecision"] == "REVIEW_REQUIRED"
        assert all(
            not thread["isResolved"] for thread in state["reviewThreads"]["nodes"]
        )
    result = subprocess.check_output(
        [
            "python3",
            "-c",
            "from order_export import export_order; "
            "print(export_order({'id':'003','lines':"
            "[{'sku':'B','quantity':2,'unit_price':5},"
            "{'sku':'A','quantity':1,'unit_price':7}]})['total'])",
        ],
        cwd=project,
        text=True,
    )
    assert int(result) == total
    assert not (project / "remote-actions.jsonl").exists()


def test_nit_wave_transition_preserves_prior_observations_code_and_journal(
    tmp_path: Path, toolbox: Path
) -> None:
    project = convergence_project(tmp_path, toolbox, "pr-nits", "do-distinct-nits.md")
    subprocess.run(["python3", "prepare-snapshots.py"], cwd=project, check=True)
    first = (project / "pr-nits-1.json").read_bytes()
    old_head = json.loads(first)["pullRequest"]["headRefOid"]
    code = (project / "order_export.py").read_bytes()
    journal = (
        project / "execution-log.md"
    ).read_bytes() + b"\nFirst advance disposition.\n"
    (project / "execution-log.md").write_bytes(journal)
    subprocess.run(["git", "add", "execution-log.md"], cwd=project, check=True)
    subprocess.run(
        ["python3", "prepare-snapshots.py", "--next-nits"], cwd=project, check=True
    )
    second = json.loads((project / "pr-nits-2.json").read_text())["pullRequest"]
    new_head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=project, text=True
    ).strip()
    assert new_head != old_head and second["headRefOid"] == new_head
    assert all(check["headSha"] == new_head for check in second["statusCheckRollup"])
    assert (project / "pr-nits-1.json").read_bytes() == first
    assert (project / "order_export.py").read_bytes() == code
    assert (project / "execution-log.md").read_bytes() == journal
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", old_head, new_head], cwd=project, text=True
    )
    assert changed.splitlines() == ["fixture-push.txt"]


def test_the_scripts_parse() -> None:
    # A broken runner fails here, not in the first run that needs it.
    for script in (DRIVE, WALK, RUN_EVAL, LIB):
        result = subprocess.run(
            ["bash", "-n", str(script)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{script.name}: {result.stderr}"


def test_no_container_tool_is_on_the_tests_path(tmp_path: Path, toolbox: Path) -> None:
    env = setup(tmp_path, toolbox)
    for tool in ("docker", "colima", "podman"):
        assert shutil.which(tool, path=env["PATH"]) is None


def test_a_drive_runs_the_cli_isolated_on_a_copy_of_the_plugin(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(
        tmp_path,
        toolbox,
        STANDIN_TRANSCRIPT=lines(GOOD),
        STANDIN_WRITES_RECORD="logs/figure-out-log-1.md",
    )
    result = drive(env)
    assert result.returncode == 0, result.stderr
    assert "docker" not in result.stderr
    (call,) = calls(tmp_path)
    assert_isolated(call)
    out = (tmp_path / "store" / "figure-out" / STAMP).resolve()
    assert Path(call["cwd"]).resolve() == out / "project"
    args = call["args"]
    assert args[:1] == ["-p"]
    plugin_dir = Path(after(args, "--plugin-dir"))
    assert outside_checkout(str(plugin_dir)) and plugin_dir.resolve() != PLUGIN
    assert (plugin_dir / ".claude-plugin" / "plugin.json").read_bytes() == (
        PLUGIN / ".claude-plugin" / "plugin.json"
    ).read_bytes()
    assert Path(call["env"]["HOME"]).resolve() == out / "home"  # the session's own home
    # The CLI version is recorded, in the summary verify keeps and in the full record.
    assert f"- **CLI version:** {VERSION}" in result.stdout
    assert "- **Other plugins loaded:** none" in result.stdout
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["cli_version"] == VERSION
    # What the session wrote under ~/.manifest-dev is listed and kept with the evidence.
    assert summary["manifest_dev_records"] == ["logs/figure-out-log-1.md"]
    assert (out / "manifest-dev" / "logs" / "figure-out-log-1.md").exists()


def test_a_drive_session_cannot_read_the_users_own_records(
    tmp_path: Path, toolbox: Path
) -> None:
    # The user's ~/.manifest-dev holds the Manifests and logs of their own work, which can name
    # what a scenario grades. The session signs in through links to the rest of the user's home,
    # and gets an empty ~/.manifest-dev of its own; what it writes stays out of the user's.
    env = setup(
        tmp_path,
        toolbox,
        STANDIN_TRANSCRIPT=lines(GOOD),
        STANDIN_WRITES_RECORD="logs/figure-out-log-1.md",
    )
    home = Path(env["HOME"])
    earlier = home / ".manifest-dev" / "logs" / "earlier.md"
    earlier.parent.mkdir(parents=True)
    earlier.write_text("an earlier session's log\n", encoding="utf-8")
    sign_in = home / ".claude.json"
    sign_in.write_text("{}", encoding="utf-8")
    result = drive(env)
    assert result.returncode == 0, result.stderr
    out = (tmp_path / "store" / "figure-out" / STAMP).resolve()
    (call,) = calls(tmp_path)
    assert call["home"][".claude.json"] == str(sign_in)
    assert (
        call["home"][".manifest-dev"] is None
    )  # a folder of its own, not a link to the user's
    assert call["seen"] == []
    # The links are gone once the drive ends, so nothing following them walks the user's home.
    assert not Path(call["env"]["HOME"]).exists()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["manifest_dev_records"] == ["logs/figure-out-log-1.md"]
    assert (out / "manifest-dev" / "logs" / "figure-out-log-1.md").exists()
    assert not (home / ".manifest-dev" / "logs" / "figure-out-log-1.md").exists()
    assert earlier.exists()


def test_a_drive_with_tools_hands_in_a_copy_of_each_plugin(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD))
    drive(env, "--tools")
    (call,) = calls(tmp_path)
    args = call["args"]
    dirs = [args[i + 1] for i, a in enumerate(args) if a == "--plugin-dir"]
    assert [Path(d).name for d in dirs] == ["manifest-dev", "manifest-dev-tools"]
    assert all(outside_checkout(d) for d in dirs)


def test_a_drive_names_a_plugin_it_did_not_hand_in(
    tmp_path: Path, toolbox: Path
) -> None:
    plugins = [
        {"name": "manifest-dev", "path": "{plugin_dir}"},
        {"name": "someone-elses", "path": "/elsewhere/someone-elses"},
    ]
    events = [{**GOOD[0], "plugins": plugins}, GOOD[1]]
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(events))
    result = drive(env)
    assert result.returncode == 0, result.stderr
    assert "- **Other plugins loaded:** someone-elses" in result.stdout


def test_a_walk_runs_the_cli_with_no_tools_and_no_plugin(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT="the reader's account\n")
    result = subprocess.run(
        [str(WALK), "Find the install steps.", "README.md"],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith(f"CLI: {VERSION}\n")
    assert "the reader's account" in result.stdout
    (call,) = calls(tmp_path)
    assert_isolated(call)
    args = call["args"]
    assert after(args, "--tools") == "" and "--plugin-dir" not in args
    assert Path(call["cwd"]).resolve().is_relative_to((tmp_path / "tmp").resolve())
    assert not Path(call["cwd"]).exists()  # the scratch directory is removed after


def run_eval(
    env: dict[str, str], out: Path, *flags: str
) -> subprocess.CompletedProcess[str]:
    wait = [f for f in flags if f == "--wait"]
    rest = [f for f in flags if f != "--wait"]
    # Started through a shell of its own, which exits as soon as the script returns.
    command = " ".join(
        [str(RUN_EVAL), *wait, "suite", str(out), "--tag", "define", *rest]
    )
    return subprocess.run(
        ["bash", "-c", command], env=env, capture_output=True, text=True, timeout=60
    )


def wait_for(path: Path, parse: Callable[[str], T], within: float = 20) -> T:
    """Return parse(path's text) once the file exists and its writer has finished it.

    A file can appear before its writer has finished it, so existence alone is no signal that it
    is ready to read: wait until its whole text parses.
    """
    deadline = time.monotonic() + within
    while True:
        try:
            return parse(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, ValueError) as error:
            if time.monotonic() >= deadline:
                raise AssertionError(
                    f"{path} not complete after {within} s: {error}"
                ) from error
        time.sleep(0.05)


def complete_calls(text: str) -> list[Call]:
    """The call record once it holds at least one finished call."""
    record = json_lines(text)
    if not record:
        raise ValueError("no call recorded yet")
    return record


def test_an_eval_run_outlives_the_shell_that_started_it(
    tmp_path: Path, toolbox: Path
) -> None:
    release = tmp_path / "release"
    env = setup(tmp_path, toolbox, STANDIN_RELEASE=str(release))
    out = tmp_path / "results" / "aggregate-result.json"
    result = run_eval(env, out)
    # The launching shell has exited while the suite is still running.
    assert result.returncode == 0, result.stderr
    (call,) = wait_for(tmp_path / "calls.jsonl", complete_calls)
    assert not out.exists()
    assert_isolated(call)
    assert call["sid"] != os.getsid(0)  # a session of its own: no hangup reaches it
    args = call["args"]
    target = Path(after(args, "eval"))
    assert outside_checkout(str(target)) and target.resolve() != PLUGIN
    assert (target / "evals" / "README.md").exists()
    assert Path(call["cwd"]).resolve() == target.parent.resolve()
    assert after(args, "--json") == str(out) and after(args, "--tag") == "define"
    release.touch()
    assert wait_for(out, json.loads)["claudeVersion"] == "9.9.9"
    exit_code = target.parent / "exit-code"
    assert wait_for(exit_code, str.strip) == "0"
    log = (target.parent / "eval.log").read_text(encoding="utf-8")
    assert log.startswith(f"CLI: {VERSION}\n")
    assert str(out) in result.stdout and "eval.log" in result.stdout


def test_an_eval_run_waited_on_exits_with_the_suites_status(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_EXIT="2")
    out = tmp_path / "results" / "partial.json"
    result = run_eval(env, out, "--wait")
    assert result.returncode == 2, result.stderr
    assert "exited 2" in result.stderr and "cost ceiling" in result.stderr
    assert out.exists()


def test_native_preflight_load_error_starts_no_paid_suite(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_PREFLIGHT_INVALID="1")
    out = tmp_path / "results/invalid.json"
    result = run_eval(env, out, "--wait")
    assert result.returncode != 0
    assert "case file(s) failed to load" in result.stderr
    assert calls(tmp_path) == []
    assert not out.exists()
    assert not out.with_suffix(".instrument.json").exists()


def test_preflight_only_records_instrument_without_starting_a_suite(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox)
    out = tmp_path / "results/plan.json"
    result = subprocess.run(
        [str(RUN_EVAL), "--preflight", "inventory", str(out), "--tag", "define"],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert calls(tmp_path) == []
    assert not out.exists()
    assert not out.with_suffix(".instrument.json").exists()
    instrument = next(
        (tmp_path / "runs" / "inventory").glob("*/preflight.instrument.json")
    )
    contract = json.loads(instrument.read_text())
    assert contract["cases"] and contract["cliVersion"] == "9.9.9"
    assert all(
        c["files"] and c["graders"] and c["runs"] == 1 for c in contract["cases"]
    )


def test_an_eval_result_path_is_relative_to_the_plugin_by_default(
    tmp_path: Path, toolbox: Path
) -> None:
    # Resolved against claude-plugins/manifest-dev, whose evals/ directory always exists, and
    # the stand-in writes no result: the test leaves the checkout as it found it, so a test
    # copying the plugin at the same moment never meets a file appearing or vanishing.
    env = setup(tmp_path, toolbox, STANDIN_WRITES_RESULT="0")
    relative = f"evals/results/test-{uuid.uuid4().hex}.json"
    expected = PLUGIN / relative
    try:
        result = subprocess.run(
            [str(RUN_EVAL), "--wait", "suite", relative],
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 1, result.stderr  # no result is not success
        (call,) = calls(tmp_path)
        assert after(call["args"], "--json") == str(expected)
        assert not expected.exists()
    finally:
        expected.with_suffix(".instrument.json").unlink(missing_ok=True)


@pytest.mark.parametrize(
    "command",
    [
        [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
        [str(DRIVE), "preflight"],
        [str(WALK), "Find the install steps.", "README.md"],
        [str(RUN_EVAL), "suite", "/nonexistent/out.json"],
    ],
    ids=["drive", "preflight", "walk", "run_eval"],
)
def test_with_no_claude_on_path_each_script_exits_3_naming_it(
    tmp_path: Path, toolbox: Path, command: list[str]
) -> None:
    env = setup(tmp_path, toolbox, claude=False)
    result = subprocess.run(
        command, env=env, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 3, result.stdout + result.stderr
    assert "the claude CLI is not on PATH" in result.stderr
    assert "claude auth login" in result.stderr  # the next step


def test_a_cli_that_is_not_signed_in_is_unreachable(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_LOGGED_IN="0")
    result = drive(env)
    assert result.returncode == 3 and "not signed in" in result.stderr
    assert calls(tmp_path) == []


def test_preflight_names_the_cli_version_and_starts_no_session(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox)
    result = subprocess.run(
        [str(DRIVE), "preflight"], env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert VERSION in result.stdout and calls(tmp_path) == []


@pytest.mark.parametrize("claude", [True, False])
def test_a_dry_run_names_the_session_and_cli_and_starts_nothing(
    tmp_path: Path, toolbox: Path, claude: bool
) -> None:
    env = setup(tmp_path, toolbox, claude=claude)
    shown = drive(env, "--dry-run")
    walked = subprocess.run(
        [str(WALK), "Find the install steps.", "README.md", "--dry-run"],
        env=env,
        capture_output=True,
        text=True,
    )
    for result in (shown, walked):
        assert result.returncode == 0, result.stderr
        assert "claude -p" in result.stdout and " ".join(ISOLATION) in result.stdout
        assert (VERSION if claude else "not on PATH") in result.stdout
    assert "--plugin-dir" in shown.stdout and "project" in shown.stdout
    assert calls(tmp_path) == [] and not (tmp_path / "store").exists()


def test_a_drive_refuses_a_feature_with_no_recipe(
    tmp_path: Path, toolbox: Path
) -> None:
    result = subprocess.run(
        [str(DRIVE), "no-such-feature", str(RECIPES / "figure-out.md")],
        env=setup(tmp_path, toolbox),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1 and "no recipe" in result.stderr


def test_an_option_missing_its_value_is_named(tmp_path: Path, toolbox: Path) -> None:
    result = drive(setup(tmp_path, toolbox), "--max-turns")
    assert result.returncode == 1 and "--max-turns needs a value" in result.stderr


@pytest.mark.parametrize(
    ("script", "variable"),
    [(DRIVE, "MANIFEST_DEV_FEATURES_EVIDENCE"), (RUN_EVAL, "MANIFEST_DEV_EVAL_RUNS")],
)
def test_a_store_inside_the_checkout_is_refused_before_anything_is_made(
    tmp_path: Path, toolbox: Path, script: Path, variable: str
) -> None:
    inside = REPO_ROOT / "no-such-store"
    env = {**setup(tmp_path, toolbox), variable: str(inside)}
    args = (
        ["figure-out", str(RECIPES / "figure-out.md")]
        if script == DRIVE
        else ["suite", str(tmp_path / "out.json")]
    )
    result = subprocess.run(
        [str(script), *args], env=env, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 1, result.stderr
    assert "inside this checkout" in result.stderr and variable in result.stderr
    assert not inside.exists() and calls(tmp_path) == []


def test_a_run_name_with_a_slash_is_refused(tmp_path: Path, toolbox: Path) -> None:
    result = subprocess.run(
        [str(RUN_EVAL), "a/b", str(tmp_path / "out.json")],
        env=setup(tmp_path, toolbox),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2 and "one plain word" in result.stderr


@pytest.mark.parametrize(
    ("events", "says"),
    [
        ([{"type": "assistant"}], "no init event"),
        ([{**GOOD[0], "skills": ["manifest-dev:define"]}], "did not load"),
    ],
)
def test_a_session_that_did_not_load_the_skill_is_unreachable(
    tmp_path: Path, toolbox: Path, events: list[dict[str, object]], says: str
) -> None:
    result = drive(setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(events)))
    assert result.returncode == 3 and says in result.stderr, result.stderr


def test_a_prompt_with_front_matter_sends_only_its_body(
    tmp_path: Path, toolbox: Path
) -> None:
    prompt = tmp_path / "prompt.md"
    prompt.write_text("---\ntags: a\n---\nthe body\n", encoding="utf-8")
    result = drive(
        setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD)), prompt=prompt
    )
    assert result.returncode == 0, result.stderr
    (call,) = calls(tmp_path)
    assert call["args"][-1] == "the body"


def test_a_drive_never_reuses_an_evidence_directory(
    tmp_path: Path, toolbox: Path
) -> None:
    # Two drives of one feature started in the same second once shared a directory and
    # interleaved their transcripts. Start two at once with the stamp pinned and require two
    # distinct evidence directories.
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD))
    drives = [
        subprocess.Popen(
            [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for _ in range(2)
    ]
    try:
        for each in drives:
            each.communicate(timeout=60)
    finally:
        for each in drives:
            each.kill()
            each.wait()
    made = sorted(p.name for p in (tmp_path / "store" / "figure-out").iterdir())
    assert made == [STAMP, f"{STAMP}-2"], made


def test_a_session_that_wrote_no_transcript_is_unreachable(
    tmp_path: Path, toolbox: Path
) -> None:
    # `verify` records exit 3 as unreachable; a drive that produced no session is never a failure
    # of the skill.
    result = drive(setup(tmp_path, toolbox, STANDIN_EXIT="1"))
    assert result.returncode == 3, result.stderr
    assert "wrote no transcript (claude exit 1)" in result.stderr


def test_a_session_stopped_by_a_signal_is_unreachable(
    tmp_path: Path, toolbox: Path
) -> None:
    result = drive(
        setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD[:1]), STANDIN_EXIT="137")
    )
    assert result.returncode == 3, result.stdout + result.stderr
    assert "stopped by a signal (exit 137) after it started" in result.stderr


@pytest.mark.parametrize(
    ("ended", "code"), [("error_max_turns", "1"), ("error_during_execution", "0")]
)
def test_a_session_that_errored_after_it_started_is_unreachable(
    tmp_path: Path, toolbox: Path, ended: str, code: str
) -> None:
    # The session loaded the skill, then stopped on an error before finishing it: no verdict on
    # the skill, whether or not the CLI's own exit says so.
    errored = {"type": "result", "subtype": ended, "is_error": True, "num_turns": 40}
    result = drive(
        setup(
            tmp_path,
            toolbox,
            STANDIN_TRANSCRIPT=lines([GOOD[0], errored]),
            STANDIN_EXIT=code,
        )
    )
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"ended with {ended} (claude exit {code})" in result.stderr
    (summary,) = (tmp_path / "store" / "figure-out").glob("*/summary.json")
    recorded = json.loads(summary.read_text(encoding="utf-8"))
    assert (recorded["ended"], recorded["claude_exit"]) == (ended, int(code))


@pytest.mark.parametrize("code", ["1", "0"])
def test_a_session_that_ended_with_no_result_is_unreachable(
    tmp_path: Path, toolbox: Path, code: str
) -> None:
    # The CLI crashed after init: there is no result to read, whatever it exited with.
    result = drive(
        setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD[:1]), STANDIN_EXIT=code)
    )
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"ended with no result event (claude exit {code})" in result.stderr


def failing_cp(tmp_path: Path) -> None:
    stub = tmp_path / "bin" / "cp"
    stub.write_text("#!/bin/sh\necho 'cp: no space left on device' >&2\nexit 1\n")
    stub.chmod(0o755)


def test_a_drive_whose_plugin_copy_fails_starts_no_session(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD))
    failing_cp(tmp_path)
    result = drive(env)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "could not copy claude-plugins/manifest-dev" in result.stderr
    assert calls(tmp_path) == []


def test_an_eval_run_whose_plugin_copy_fails_starts_no_suite(
    tmp_path: Path, toolbox: Path
) -> None:
    env = setup(tmp_path, toolbox)
    failing_cp(tmp_path)
    result = run_eval(env, tmp_path / "results" / "aggregate-result.json")
    assert result.returncode == 3, result.stdout + result.stderr
    assert "could not copy claude-plugins/manifest-dev" in result.stderr
    assert calls(tmp_path) == []


def drive_scaffold(
    tmp_path: Path, toolbox: Path, body: str, transcript: str = ""
) -> subprocess.CompletedProcess[str]:
    # A drive takes scaffolds from inside the checkout only, so the test's lives there briefly.
    case = REPO_ROOT / "verification" / "scaffolds" / f"drive-test-{uuid.uuid4().hex}"
    case.mkdir()
    try:
        (case / "scaffold.sh").write_text(body, encoding="utf-8")
        env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=transcript)
        return drive(env, "--scaffold", str(case))
    finally:
        shutil.rmtree(case)


def test_a_scaffold_builds_the_project_from_the_checkouts_path(
    tmp_path: Path, toolbox: Path
) -> None:
    result = drive_scaffold(
        tmp_path,
        toolbox,
        'pwd -P > where; printf %s "$DRIVE_CHECKOUT" > checkout\n',
        lines(GOOD),
    )
    assert result.returncode == 0, result.stderr
    project = tmp_path / "store" / "figure-out" / STAMP / "project"
    assert Path((project / "where").read_text().strip()) == project.resolve()
    assert Path((project / "checkout").read_text()) == REPO_ROOT


def test_the_this_repository_scaffold_copies_the_last_commit(
    tmp_path: Path, toolbox: Path
) -> None:
    # It once read a container's mount of the checkout; it now reads the path the drive passes.
    env = setup(tmp_path, toolbox, STANDIN_TRANSCRIPT=lines(GOOD))
    result = drive(
        env, "--scaffold", str(REPO_ROOT / "verification/scaffolds/this-repository")
    )
    assert result.returncode == 0, result.stderr
    project = tmp_path / "store" / "figure-out" / STAMP / "project"
    assert (project / "CLAUDE.md").is_file() and (
        project / "scripts/drive-skill.sh"
    ).is_file()


def test_a_scaffold_that_seeds_a_home_is_not_driven(
    tmp_path: Path, toolbox: Path
) -> None:
    # A drive's session links to the user's home, so a case that seeds one is an eval's.
    result = drive_scaffold(
        tmp_path,
        toolbox,
        'mkdir -p "$HOME/.manifest-dev/logs"; touch "$HOME/.manifest-dev/logs/x"\n',
    )
    assert result.returncode == 3, result.stderr
    assert "seeds a home directory" in result.stderr and "eval suite" in result.stderr
    assert not (tmp_path / "home" / ".manifest-dev").exists() and calls(tmp_path) == []


def test_a_failed_scaffold_is_unreachable_and_shows_its_log(
    tmp_path: Path, toolbox: Path
) -> None:
    result = drive_scaffold(tmp_path, toolbox, "echo seed step broke\nexit 7\n")
    assert result.returncode == 3, result.stderr
    assert "seed step broke" in result.stderr and "scaffold exited 7" in result.stderr
    assert calls(tmp_path) == []


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_a_drive_fails_fast_when_it_cannot_create_evidence(
    tmp_path: Path, toolbox: Path
) -> None:
    # Only "another drive holds this directory" may be retried; any other failure stops loudly.
    store = tmp_path / "store"
    (store / "figure-out").mkdir(parents=True)
    (store / "figure-out").chmod(0o555)
    try:
        result = drive(setup(tmp_path, toolbox))
    finally:
        (store / "figure-out").chmod(0o755)
    assert result.returncode != 0 and "cannot create" in result.stderr, result.stderr


def test_a_walk_passes_on_a_failed_session_and_says_so(
    tmp_path: Path, toolbox: Path
) -> None:
    result = subprocess.run(
        [str(WALK), "Find the install steps.", "README.md"],
        env=setup(tmp_path, toolbox, STANDIN_EXIT="1"),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 1 and "reader session exited 1" in result.stderr


def test_stopping_a_drive_stops_its_session(tmp_path: Path, toolbox: Path) -> None:
    # The session runs in the drive's process group, so the stop `scripts/verify` sends that group
    # reaches it, as the container's init process once made sure.
    env = setup(tmp_path, toolbox, STANDIN_SLEEP="30")
    running = subprocess.Popen(
        [str(DRIVE), "figure-out", str(RECIPES / "figure-out.md")],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        (call,) = wait_for(tmp_path / "calls.jsonl", complete_calls)
        os.killpg(running.pid, signal.SIGTERM)
        running.wait(timeout=10)
        deadline = time.monotonic() + 5
        while _alive(call["pid"]) and time.monotonic() < deadline:
            time.sleep(0.05)
        assert not _alive(call["pid"])
    finally:
        running.kill()
        running.wait()


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


@pytest.mark.parametrize(
    "out_name, flags", [("result.txt", []), ("result.json", ["--json", "other.json"])]
)
def test_eval_result_path_cannot_be_overridden_before_preflight(
    tmp_path: Path, toolbox: Path, out_name: str, flags: list[str]
) -> None:
    env = setup(tmp_path, toolbox)
    result = subprocess.run(
        [str(RUN_EVAL), "--wait", "suite", str(tmp_path / out_name), *flags],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0
    assert calls(tmp_path) == []
    assert not (tmp_path / "runs").exists()
