#!/usr/bin/env python3
"""Run synthetic Premilume regression or portal cases in isolated Codex conversations.

The runner stores raw model responses only in an explicitly selected output
file, which should remain outside the repository. It does not decide semantic
pass/fail; a reviewer compares each response with the case invariants.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = REPO_ROOT / "evals" / "regression-cases.json"
ACTIVATION_PROMPT = (
    "$premilume-mode Turn mentor mode on for this conversation. "
    "Confirm briefly and describe the roles only as functional response strategies."
)


def codex_command() -> list[str]:
    """Return an argv prefix that never relies on shell parsing."""
    if os.name != "nt":
        resolved = shutil.which("codex")
        if resolved:
            return [resolved]
        raise RuntimeError("Codex CLI was not found on PATH")

    npm_shim = shutil.which("codex.cmd")
    if npm_shim:
        node = shutil.which("node.exe") or shutil.which("node")
        codex_js = Path(npm_shim).resolve().parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
        if not node:
            raise RuntimeError("Codex npm shim was found, but Node.js was not found on PATH")
        if not codex_js.is_file():
            raise RuntimeError(f"Codex npm launcher was not found beside the shim: {codex_js}")
        return [node, str(codex_js)]

    standalone = shutil.which("codex.exe")
    if standalone:
        return [standalone]
    raise RuntimeError("Codex CLI was not found on PATH")


def parse_args() -> argparse.Namespace:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    default_output = Path(tempfile.gettempdir()) / f"premilume-regression-{timestamp}.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180, help="Seconds per Codex turn")
    return parser.parse_args()


def load_cases(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.resolve().read_text(encoding="utf-8"))
    regression = payload.get("cases")
    if isinstance(regression, list):
        return [case for case in regression if isinstance(case, dict)]

    positive = payload.get("positive")
    negative = payload.get("negative")
    if not isinstance(positive, list) or not isinstance(negative, list):
        raise SystemExit("case file must contain a cases array or positive/negative arrays")

    normalized: list[dict[str, object]] = []
    for kind, items in (("positive", positive), ("negative", negative)):
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("user_prompt"), str):
                raise SystemExit(f"invalid {kind} case shape")
            if kind == "positive":
                invariants = [item.get("expected_workflow"), item.get("expected_result_shape")]
            else:
                invariants = [item.get("expected_safe_behavior"), item.get("why_not")]
            normalized.append(
                {
                    "id": item.get("id"),
                    "language": item.get("language"),
                    "initial_state": "OFF",
                    "turns": [item["user_prompt"]],
                    "invariants": [value for value in invariants if isinstance(value, str)],
                    "portal_kind": kind,
                }
            )
    return normalized


def parse_events(stdout: str) -> tuple[str | None, str]:
    thread_id: str | None = None
    last_message = ""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            thread_id = event.get("thread_id")
        item = event.get("item")
        if (
            event.get("type") == "item.completed"
            and isinstance(item, dict)
            and item.get("type") == "agent_message"
            and isinstance(item.get("text"), str)
        ):
            last_message = item["text"]
    return thread_id, last_message.strip()


def run_turn(command: list[str], timeout: int) -> dict[str, object]:
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        thread_id, response = parse_events(stdout)
        return {
            "returncode": 124,
            "thread_id": thread_id,
            "response": response,
            "stderr_tail": "\n".join(stderr.splitlines()[-12:]),
            "timed_out": True,
        }
    thread_id, response = parse_events(completed.stdout)
    return {
        "returncode": completed.returncode,
        "thread_id": thread_id,
        "response": response,
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-12:]),
        "timed_out": False,
    }


def start_command(prompt: str, *, ephemeral: bool) -> list[str]:
    command = [
        *codex_command(),
        "exec",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
    ]
    if ephemeral:
        command.append("--ephemeral")
    command.append(prompt)
    return command


def resume_command(thread_id: str, prompt: str) -> list[str]:
    return [
        *codex_command(),
        "exec",
        "resume",
        "--json",
        thread_id,
        prompt,
    ]


def run_case(case: dict[str, object], timeout: int) -> dict[str, object]:
    case_id = str(case["id"])
    initial_state = case.get("initial_state")
    turns = case.get("turns")
    if initial_state not in {"ON", "OFF"} or not isinstance(turns, list) or not turns:
        return {"id": case_id, "error": "invalid case shape", "turns": []}

    results: list[dict[str, object]] = []
    needs_session = initial_state == "ON" or len(turns) > 1
    thread_id: str | None = None

    if initial_state == "ON":
        activation = run_turn(start_command(ACTIVATION_PROMPT, ephemeral=False), timeout)
        results.append({"phase": "activation", **activation})
        thread_id = activation.get("thread_id") if isinstance(activation.get("thread_id"), str) else None
        if activation["returncode"] != 0 or not thread_id:
            return {"id": case_id, "error": "activation failed", "turns": results}

    for index, prompt in enumerate(turns, start=1):
        if not isinstance(prompt, str):
            return {"id": case_id, "error": "non-string prompt", "turns": results}
        if thread_id:
            result = run_turn(resume_command(thread_id, prompt), timeout)
        else:
            result = run_turn(start_command(prompt, ephemeral=not needs_session), timeout)
            candidate = result.get("thread_id")
            if needs_session and isinstance(candidate, str):
                thread_id = candidate
        results.append({"phase": f"turn-{index}", "prompt": prompt, **result})
        if result["returncode"] != 0:
            return {"id": case_id, "error": f"turn {index} failed", "turns": results}

    return {
        "id": case_id,
        "language": case.get("language"),
        "initial_state": initial_state,
        "portal_kind": case.get("portal_kind"),
        "invariants": case.get("invariants"),
        "error": None,
        "turns": results,
    }


def main() -> int:
    args = parse_args()
    if not 1 <= args.workers <= 4:
        raise SystemExit("--workers must be between 1 and 4")
    cases = load_cases(args.cases)

    print(f"Running {len(cases)} synthetic cases with {args.workers} workers", flush=True)
    by_id: dict[str, dict[str, object]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = {
            executor.submit(run_case, case, args.timeout): str(case.get("id"))
            for case in cases
            if isinstance(case, dict)
        }
        for future in concurrent.futures.as_completed(pending):
            case_id = pending[future]
            try:
                result = future.result()
            except Exception as exc:  # noqa: BLE001 - preserve per-case failure evidence
                result = {"id": case_id, "error": f"runner exception: {exc}", "turns": []}
            by_id[case_id] = result
            label = "OK" if not result.get("error") else "ERROR"
            print(f"[{len(by_id):02d}/{len(cases):02d}] {case_id}: {label}", flush=True)

    ordered = [by_id[str(case["id"])] for case in cases if isinstance(case, dict)]
    output = {
        "schema_version": "1.0",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "plugin": "premilume",
        "synthetic_only": True,
        "semantic_review_required": True,
        "results": ordered,
    }
    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = sum(1 for result in ordered if result.get("error"))
    print(f"Raw synthetic results: {args.output}", flush=True)
    print(f"Execution errors: {errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
