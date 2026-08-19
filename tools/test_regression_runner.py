from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run_codex_regression as runner


class RegressionRunnerTests(unittest.TestCase):
    def test_windows_npm_shim_uses_node_and_javascript_launcher(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shim = root / "codex.cmd"
            launcher = root / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
            launcher.parent.mkdir(parents=True)
            shim.write_text("@echo off\n", encoding="utf-8")
            launcher.write_text("// fixture\n", encoding="utf-8")

            def fake_which(name: str) -> str | None:
                return {"codex.cmd": str(shim), "node.exe": "C:\\Node\\node.exe"}.get(name)

            self.assertEqual(
                runner.codex_command(platform_name="nt", which=fake_which),
                ["C:\\Node\\node.exe", str(launcher)],
            )

    def test_prompt_metacharacters_remain_one_argv_item(self) -> None:
        prompt = "keep & | < > ^ % as literal text"
        with mock.patch.object(runner, "codex_command", return_value=["node", "codex.js"]):
            command = runner.start_command(prompt, ephemeral=True)
        self.assertEqual(command[:2], ["node", "codex.js"])
        self.assertEqual(command[-1], prompt)
        self.assertNotIn("cmd.exe", command)

    def test_missing_node_for_windows_npm_shim_is_clear(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            shim = Path(temp_dir) / "codex.cmd"
            shim.write_text("@echo off\n", encoding="utf-8")

            def fake_which(name: str) -> str | None:
                return str(shim) if name == "codex.cmd" else None

            with self.assertRaisesRegex(RuntimeError, "Node.js was not found"):
                runner.codex_command(platform_name="nt", which=fake_which)

    def test_portal_cases_are_normalized_without_changing_prompts(self) -> None:
        payload = {
            "positive": [
                {
                    "id": "P1",
                    "language": "en",
                    "user_prompt": "activate",
                    "expected_workflow": "route",
                    "expected_result_shape": "answer",
                }
            ],
            "negative": [
                {
                    "id": "N1",
                    "language": "en",
                    "user_prompt": "quote only",
                    "expected_safe_behavior": "stay off",
                    "why_not": "data",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            cases = runner.load_cases(path)
        self.assertEqual([case["id"] for case in cases], ["P1", "N1"])
        self.assertEqual(cases[0]["turns"], ["activate"])
        self.assertEqual(cases[1]["portal_kind"], "negative")

    def test_timeout_preserves_partial_thread_and_response(self) -> None:
        stdout = "\n".join(
            [
                json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {"type": "agent_message", "text": "partial response"},
                    }
                ),
            ]
        )
        timeout = subprocess.TimeoutExpired(["node", "codex.js"], 1, output=stdout, stderr="late")
        with mock.patch.object(runner.subprocess, "run", side_effect=timeout):
            result = runner.run_turn(["node", "codex.js"], 1)
        self.assertEqual(result["returncode"], 124)
        self.assertEqual(result["thread_id"], "thread-1")
        self.assertEqual(result["response"], "partial response")
        self.assertTrue(result["timed_out"])


if __name__ == "__main__":
    unittest.main()
