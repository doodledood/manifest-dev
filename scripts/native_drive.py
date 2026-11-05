#!/usr/bin/env python3
"""Snapshot fixtures and bind evidence for a host-owned general-agent task.

A shell cannot call its parent harness's model tool. Preparation therefore exits 3
with a request; the host dispatches the scenario, records the actual agent result,
then reruns the recipe with MANIFEST_DEV_DRIVE_RUN pointing at that request.
Neither preparation nor an incomplete/error result counts as a completed drive.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> None:
    print(f"native drive: unreachable — {message}", file=sys.stderr)
    raise SystemExit(3)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def turns(prompt: str) -> list[str]:
    result = [part.strip() for part in prompt.split("<!-- next turn -->")]
    if not all(result):
        fail("the prompt has an empty turn")
    return result


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["skill", "walk"])
    parser.add_argument("subject")
    parser.add_argument("inputs", nargs="*")
    parser.add_argument("--scaffold", type=Path)
    parser.add_argument("--tools", action="store_true")
    parser.add_argument("--max-turns", type=int, default=40)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def inputs(args: argparse.Namespace) -> tuple[str, str]:
    if args.mode == "walk":
        if not args.inputs:
            fail("a walk needs documents")
        documents = []
        for name in args.inputs:
            path = ROOT / name
            documents.append(f"# Document: {name}\n\n{path.read_text()}")
        return "document-reader", (
            "Using only the supplied documents, do this reader task: "
            + args.subject
            + "\nReport whether you could do it, quote the facts you relied on, and name gaps.\n\n"
            + "\n\n".join(documents)
        )
    if args.subject == "doctor":
        return (
            "doctor",
            "Inspect the supplied skill catalog and reply with ok. Execute no workflow.",
        )
    if len(args.inputs) != 1:
        fail("a skill drive needs one prompt file")
    if not (ROOT / "verification/recipes" / f"{args.subject}.md").is_file():
        fail("the skill recipe does not exist")
    prompt = Path(args.inputs[0]).read_text()
    if prompt.startswith("---\n"):
        prompt = prompt.split("---\n", 2)[2]
    return args.subject, prompt


def snapshot(out: Path, names: list[str], revision: str) -> dict[str, dict[str, str]]:
    catalog = {}
    for name in names:
        target = out / "plugins" / name
        if revision == "checkout":
            shutil.copytree(
                ROOT / "claude-plugins" / name,
                target,
                ignore=shutil.ignore_patterns(
                    "node_modules", "evals", "results", "__pycache__"
                ),
            )
        else:
            target.mkdir(parents=True)
            archive = subprocess.check_output(
                ["git", "-C", str(ROOT), "archive", f"{revision}:claude-plugins/{name}"]
            )
            subprocess.run(["tar", "-x", "-C", str(target)], input=archive, check=True)
        shutil.rmtree(target / "evals", ignore_errors=True)
        for skill in sorted((target / "skills").glob("*/SKILL.md")):
            catalog[f"{name}:{skill.parent.name}"] = {
                "path": str(skill),
                "sha256": digest(skill.read_bytes()),
            }
    return catalog


def prepare(args: argparse.Namespace, feature: str, prompt: str) -> Path:
    store = Path(
        os.environ.get(
            "MANIFEST_DEV_FEATURES_EVIDENCE",
            str(Path.home() / ".local/state/manifest-dev-features"),
        )
    ).resolve()
    if store == ROOT or ROOT in store.parents:
        fail("the evidence store must be outside this checkout")
    out = (
        store
        / feature
        / f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"
    )
    out.mkdir(parents=True)
    project = out / "project"
    project.mkdir()
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    revision = os.environ.get("DRIVE_PLUGINS_AT", "checkout")
    if revision != "checkout":
        revision = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "--verify", f"{revision}^{{commit}}"],
            text=True,
        ).strip()
    names = ["manifest-dev"] + (["manifest-dev-tools"] if args.tools else [])
    catalog = snapshot(out, names, revision) if args.mode == "skill" else {}
    if args.scaffold:
        fixture = args.scaffold.resolve()
        if ROOT not in fixture.parents or not (fixture / "scaffold.sh").is_file():
            fail("the scaffold must be a repository fixture with scaffold.sh")
        scaffold_home = out / "scaffold-home"
        scaffold_home.mkdir()
        # Preserve the inherited runtime/auth environment; only the scaffold's explicit
        # HOME isolation matches the existing CLI driver. No credentials are copied.
        env = {
            **os.environ,
            "HOME": str(scaffold_home),
            "DRIVE_CHECKOUT": str(ROOT),
            # Apple Python otherwise writes import caches into this isolated HOME,
            # which is not fixture data and must not trigger the seeding guard.
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        with (out / "scaffold.log").open("w") as log:
            result = subprocess.run(
                ["bash", str(fixture / "scaffold.sh")],
                cwd=project,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
        if result.returncode:
            fail(
                f"scaffold failed with {result.returncode}; see {out / 'scaffold.log'}"
            )
        if any(scaffold_home.iterdir()):
            fail(
                "the scaffold seeds a home directory; use its dedicated eval instrument"
            )
    subprocess.run(["git", "add", "-A"], cwd=project, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=drive@localhost",
            "-c",
            "user.name=drive",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-qm",
            "scaffold",
            "--allow-empty",
        ],
        cwd=project,
        check=True,
    )
    records = out / "records"
    records.mkdir()
    user_turns = turns(prompt) if args.mode == "skill" else [prompt]
    request = {
        "schema": 2,
        "request_id": uuid.uuid4().hex,
        "execution": "general-agent",
        "feature": feature,
        "mode": args.mode,
        "project": str(project),
        "records": str(records),
        "plugins_from": revision,
        "catalog": catalog,
        "model": os.environ.get("MODEL", "inherit"),
        "reasoning_effort": os.environ.get("MODEL_REASONING_EFFORT", "inherit"),
        "requested_max_turns": args.max_turns,
        "host_enforced_turn_limit": False,
        "prompt_sha256": digest(prompt.encode()),
        "turns": user_turns,
        "started": time.time(),
        "source_sha256": {
            str(path.relative_to(out)): digest(path.read_bytes())
            for path in sorted((out / "plugins").rglob("*"))
            if path.is_file()
        },
    }
    write_json(out / "skill-catalog.json", catalog)
    worker = f"""Working directory: {project}
Available skill snapshots and references: {out / 'skill-catalog.json'}
Use these copies for any skill the task calls for; scripts inside them are available.
Keep workflow records under {records}. Use no parent conversation, installed skill
copies, personal records, source checkout, verification recipes or expected outcomes.
Do not inspect other agents or their messages, including agent-inventory tools. A fresh
reviewer receives only this scenario's allowed inputs; spawn it directly when needed.
Use connected services only if the task supplies a throwaway service it owns.
For a document-reader task, after reading this brief answer from its included
documents without further tools. Return your actual response and artifacts to
the caller; the caller records completion and judges the behavior separately.

{user_turns[0]}
"""
    (out / "worker-prompt.md").write_text(worker)
    request["worker_prompt_sha256"] = digest(worker.encode())
    request["catalog_sha256"] = digest((out / "skill-catalog.json").read_bytes())
    write_json(out / "native-request.json", request)
    return out


def check_execution(out: Path, request_path: Path, result: dict[str, object]) -> None:
    """The caller owns capability checks and the user's fallback grant."""
    capability = out / "capability.json"
    if result.get("execution") == "general-agent":
        if capability.exists() or result.get("fallback_approval"):
            fail("general agents were reported unavailable; warn and ask what to do")
        return
    if result.get("execution") != "approved-script" or not capability.exists():
        fail(
            "a script fallback requires a recorded missing capability and explicit user approval"
        )
    blocked = json.loads(capability.read_text())
    approval = result.get("fallback_approval")
    if (
        not isinstance(approval, str)
        or not approval.strip()
        or blocked.get("harness") != result.get("harness")
        or blocked.get("request_sha256") != digest(request_path.read_bytes())
    ):
        fail("the approved script fallback must use the same host harness and request")


def unavailable() -> None:
    parser = argparse.ArgumentParser(
        description="Record missing general agents; ask the user"
    )
    parser.add_argument("unavailable")
    parser.add_argument("run", type=Path)
    parser.add_argument("--harness", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    if not args.harness.strip() or not args.reason.strip():
        fail("the current harness and missing capability must be named")
    write_json(
        args.run / "capability.json",
        {
            "harness": args.harness,
            "reason": args.reason,
            "request_sha256": digest((args.run / "native-request.json").read_bytes()),
        },
    )
    fail(
        "general agents unavailable: "
        + args.reason
        + ". Warn and ask the user what to do; a same-host script needs explicit approval. Never switch providers automatically."
    )


def finish(out: Path, args: argparse.Namespace, feature: str, prompt: str) -> None:
    request_path = out / "native-request.json"
    request = json.loads(request_path.read_text())
    if (
        request.get("schema") != 2
        or request.get("execution") != "general-agent"
        or request.get("feature") != feature
        or request.get("mode") != args.mode
        or request.get("prompt_sha256") != digest(prompt.encode())
    ):
        fail("the native request does not match this recipe and input")
    result_path = out / "native-result.json"
    if not result_path.is_file():
        print(f"HOST_AGENT_REQUEST: {request_path}")
        print(f"Scenario brief: {out / 'worker-prompt.md'}")
        print(
            "The host starts a fresh general agent with the scenario as its brief; preparation is incomplete evidence."
        )
        print(
            f"Caller records the actual reply with: {sys.executable} {ROOT / 'scripts/native_drive.py'} record {out} --harness HOST --session-id ID --model MODEL --reasoning-effort EFFORT --reply-file FILE"
        )
        print(
            "For multiple user turns, continue the same native session with each request turn, recording --turn N in order."
        )
        print("Then rerun this recipe with:")
        print(f"MANIFEST_DEV_DRIVE_RUN={out}")
        print(
            "Without general agents, warn and ask what to do. Only an explicitly approved same-host script may substitute; never auto-switch providers."
        )
        fail("awaiting the host's general-agent result; no CLI sign-in is required")
    result = json.loads(result_path.read_text())
    if result.get("request_sha256") != digest(request_path.read_bytes()):
        fail("the native result belongs to a different request")
    if (
        not isinstance(result.get("harness"), str)
        or not result["harness"].strip()
        or not isinstance(result.get("session_id"), str)
        or not result["session_id"].strip()
    ):
        fail("the actual host harness and session identity are required")
    if result.get("status") != "completed":
        fail(
            "the host result is incomplete or failed; every requested turn must complete"
        )
    check_execution(out, request_path, result)
    for key in ("model", "reasoning_effort"):
        if (
            not isinstance(result.get(key), str)
            or not result[key].strip()
            or (request[key] != "inherit" and result[key] != request[key])
        ):
            fail(f"native {key} is missing or differs from the requested setting")
    replies = result.get("turns", [])
    if len(replies) != len(request["turns"]):
        fail("not every requested user turn has a native result")
    for asked, reply in zip(request["turns"], replies, strict=True):
        if (
            reply.get("input_sha256") != digest(asked.encode())
            or reply.get("status") != "completed"
            or not isinstance(reply.get("reply"), str)
            or not reply["reply"].strip()
        ):
            fail("a native turn failed, is incomplete, or belongs to another input")
    # Hash every companion as well as the entrypoint: a changed reference is changed input.
    expected_sources = request["source_sha256"]
    current_sources = {
        str(path.relative_to(out)): digest(path.read_bytes())
        for path in sorted((out / "plugins").rglob("*"))
        if path.is_file()
    }
    if current_sources != expected_sources:
        fail("a copied skill or companion changed during its drive")
    if (
        digest((out / "worker-prompt.md").read_bytes())
        != request["worker_prompt_sha256"]
    ):
        fail("the worker input changed during its drive")
    if digest((out / "skill-catalog.json").read_bytes()) != request["catalog_sha256"]:
        fail("the supplied resource catalog changed during its drive")
    project = Path(request["project"])
    files = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=project, text=True
    )
    summary = {
        "harness": result["harness"],
        "execution": result["execution"],
        "fallback_approval": result.get("fallback_approval", ""),
        "session_id": result["session_id"],
        "model": result["model"],
        "reasoning_effort": result["reasoning_effort"],
        "plugins_from": request["plugins_from"],
        "delivery": (
            "document snapshots only"
            if request["mode"] == "walk"
            else "scenario brief and copied resources"
        ),
        "turns": replies,
        "files_written": files,
        "records": sorted(
            str(p.relative_to(out))
            for p in Path(request["records"]).rglob("*")
            if p.is_file()
        ),
        "wall_seconds": round(time.time() - request["started"], 1),
        "cost_usd": result.get("cost_usd", "not reported by host harness"),
        "requested_max_turns": request["requested_max_turns"],
        "host_enforced_turn_limit": False,
        "transcript": "host session record; raw terminal replies in native-result.json",
    }
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    print(
        "Host session completed. The parent must judge its output and artifacts against the recipe; this is not a behavior verdict."
    )


def record() -> None:
    parser = argparse.ArgumentParser(
        description="Caller records an actual native harness terminal reply"
    )
    parser.add_argument("record")
    parser.add_argument("run", type=Path)
    parser.add_argument("--harness", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", required=True)
    parser.add_argument("--reply-file", required=True, type=Path)
    parser.add_argument("--turn", type=int, default=1)
    parser.add_argument("--fallback-approval", default="")
    parser.add_argument(
        "--status", choices=["completed", "failed"], default="completed"
    )
    args = parser.parse_args()
    request_path = args.run / "native-request.json"
    request = json.loads(request_path.read_text())
    path = args.run / "native-result.json"
    result = (
        json.loads(path.read_text())
        if path.exists()
        else {
            "harness": args.harness,
            "execution": (
                "approved-script" if args.fallback_approval else "general-agent"
            ),
            "fallback_approval": args.fallback_approval,
            "session_id": args.session_id,
            "request_sha256": digest(request_path.read_bytes()),
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "turns": [],
        }
    )
    if (
        result["session_id"] != args.session_id
        or result["harness"] != args.harness
        or result.get("fallback_approval", "") != args.fallback_approval
        or result["model"] != args.model
        or result["reasoning_effort"] != args.reasoning_effort
    ):
        fail("all turns must come from the same native session and settings")
    check_execution(args.run, request_path, result)
    if args.turn != len(result["turns"]) + 1 or args.turn > len(request["turns"]):
        fail("record native replies once, in requested turn order")
    reply = args.reply_file.read_text()
    if not reply.strip():
        fail("the actual native reply must not be empty")
    result["turns"].append(
        {
            "input_sha256": digest(request["turns"][args.turn - 1].encode()),
            "status": args.status,
            "reply": reply,
        }
    )
    result["status"] = (
        args.status if len(result["turns"]) == len(request["turns"]) else "incomplete"
    )
    write_json(path, result)
    print(
        f"Recorded host turn {args.turn}; rerun the original recipe with MANIFEST_DEV_DRIVE_RUN={args.run}"
    )


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "record":
        record()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "unavailable":
        unavailable()
        return
    args = parse()
    if args.subject == "preflight":
        print(
            "preflight: snapshot/evidence helper ready; caller must check for fresh general agents. Without them, warn and ask; no CLI authentication or agent capability checked here."
        )
        return
    feature, prompt = inputs(args)
    if args.dry_run or os.environ.get("VERIFY_DRY_RUN") == "1":
        print(
            f"would prepare {feature} for a fresh general agent in the running host; no CLI or provider selection"
        )
        store = Path(
            os.environ.get(
                "MANIFEST_DEV_FEATURES_EVIDENCE",
                str(Path.home() / ".local/state/manifest-dev-features"),
            )
        )
        print(f"evidence: {store / feature / '<run>'}")
        return
    resumed = os.environ.get("MANIFEST_DEV_DRIVE_RUN")
    out = Path(resumed).resolve() if resumed else prepare(args, feature, prompt)
    finish(out, args, feature, prompt)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        fail(str(exc))
