#!/usr/bin/env python3
"""Prepare and finalize a drive dispatched by the active Codex model harness.

A shell cannot call its parent harness's model tool. Preparation therefore exits 3
with a native request; the caller dispatches it, records the real native result,
then reruns the recipe with MANIFEST_DEV_NATIVE_RUN pointing at that request.
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
        env = {**os.environ, "HOME": str(scaffold_home), "DRIVE_CHECKOUT": str(ROOT)}
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
        "schema": 1,
        "request_id": uuid.uuid4().hex,
        "host": "codex",
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
    owner = next((name for name in catalog if name.endswith(":" + feature)), None)
    if args.mode == "skill" and feature != "doctor" and owner is None:
        fail(f"the copied plugins do not carry skill {feature}")
    entry = Path(catalog[owner]["path"]).read_text() if owner else ""
    worker = f"""You are the isolated native model worker for a behavior drive.
Work only in {project}. The request ID is {request['request_id']}.
Use only the supplied copied skill catalog and references, not installed skills,
parent conversation, home records, or the checkout this copy came from.
Resolve skill names and /manifest-dev:skill invocations from the catalog below.
The target skill is supplied verbatim below. Its relative references resolve from
its catalog path. Its instructions and the scenario govern your work.
Store any ~/.manifest-dev workflow records under {records}; do not read real home records.
Use command/file tools against this scratch project. Do not use connected services
unless the supplied scenario explicitly provides a throwaway service it owns.
For a document-reader request, after reading this input use no tools; answer only
from the included documents. Do not create a receipt or grade yourself. Finish by
returning the actual response through the native harness. The caller records it.
Do not read any verification recipe, rubric, or expected outcome outside this input.
Native host tool catalogs and turn limits differ from CLI hosts; report limitations.

Copied skill catalog:
{json.dumps(catalog, indent=2)}

Target skill, verbatim:
{entry}

Scenario, turn 1:
{user_turns[0]}
"""
    (out / "worker-prompt.md").write_text(worker)
    request["worker_prompt_sha256"] = digest(worker.encode())
    write_json(out / "native-request.json", request)
    return out


def finish(out: Path, args: argparse.Namespace, feature: str, prompt: str) -> None:
    request_path = out / "native-request.json"
    request = json.loads(request_path.read_text())
    if (
        request.get("host") != "codex"
        or request.get("feature") != feature
        or request.get("mode") != args.mode
        or request.get("prompt_sha256") != digest(prompt.encode())
    ):
        fail("the native request does not match this recipe and input")
    result_path = out / "native-result.json"
    if not result_path.is_file():
        print(f"NATIVE_SESSION_REQUEST: {request_path}")
        print(f"Worker input: {out / 'worker-prompt.md'}")
        print(
            "Dispatch through this session's isolated native model capability; a prepared request is not a drive."
        )
        print(
            f"Caller records the actual terminal reply with: python3 {ROOT / 'scripts/native_drive.py'} record {out} --session-id ID --model MODEL --reasoning-effort EFFORT --reply-file FILE"
        )
        print(
            "For multiple user turns, continue the same native session with each request turn, recording --turn N in order."
        )
        print("Then rerun this recipe with:")
        print(f"MANIFEST_DEV_NATIVE_RUN={out}")
        fail(
            "awaiting the calling harness's native model result; no CLI sign-in is required"
        )
    result = json.loads(result_path.read_text())
    if result.get("request_sha256") != digest(request_path.read_bytes()):
        fail("the native result belongs to a different request")
    if (
        result.get("host") != "codex"
        or result.get("status") != "completed"
        or not isinstance(result.get("native_session_id"), str)
        or not result["native_session_id"].strip()
    ):
        fail("the actual native host and session identity are required")
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
    project = Path(request["project"])
    files = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=project, text=True
    )
    summary = {
        "host": "codex",
        "native_session_id": result["native_session_id"],
        "model": result["model"],
        "reasoning_effort": result["reasoning_effort"],
        "plugins_from": request["plugins_from"],
        "delivery": (
            "document snapshots only"
            if request["mode"] == "walk"
            else (
                "copied skill catalog"
                if feature == "doctor"
                else "copied catalog and verbatim target skill"
            )
        ),
        "turns": replies,
        "files_written": files,
        "records": sorted(
            str(p.relative_to(out))
            for p in Path(request["records"]).rglob("*")
            if p.is_file()
        ),
        "wall_seconds": round(time.time() - request["started"], 1),
        "cost_usd": result.get("cost_usd", "not reported by native harness"),
        "requested_max_turns": request["requested_max_turns"],
        "host_enforced_turn_limit": False,
        "transcript": "native host session record; raw terminal replies in native-result.json",
    }
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    print(
        "Native session completed. Its output and artifacts require reading against the recipe; this is not a behavior verdict."
    )


def record() -> None:
    parser = argparse.ArgumentParser(
        description="Caller records an actual native harness terminal reply"
    )
    parser.add_argument("record")
    parser.add_argument("run", type=Path)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", required=True)
    parser.add_argument("--reply-file", required=True, type=Path)
    parser.add_argument("--turn", type=int, default=1)
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
            "host": "codex",
            "native_session_id": args.session_id,
            "request_sha256": digest(request_path.read_bytes()),
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "turns": [],
        }
    )
    if (
        result["native_session_id"] != args.session_id
        or result["model"] != args.model
        or result["reasoning_effort"] != args.reasoning_effort
    ):
        fail("all turns must come from the same native session and settings")
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
        f"Recorded native turn {args.turn}; rerun the original recipe with MANIFEST_DEV_NATIVE_RUN={args.run}"
    )


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "record":
        record()
        return
    args = parse()
    if args.subject == "preflight":
        print(
            "preflight: Codex native dispatch protocol available; no model session or CLI authentication checked"
        )
        return
    feature, prompt = inputs(args)
    if args.dry_run or os.environ.get("VERIFY_DRY_RUN") == "1":
        print(
            f"would drive {feature} through the active Codex native model harness; no Claude CLI or sign-in"
        )
        return
    resumed = os.environ.get("MANIFEST_DEV_NATIVE_RUN")
    out = Path(resumed).resolve() if resumed else prepare(args, feature, prompt)
    finish(out, args, feature, prompt)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        fail(str(exc))
