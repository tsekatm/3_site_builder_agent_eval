"""Claude Code CLI runner — uses the claude CLI for judge/teacher invocations.

Uses the user's Claude Code subscription (Max/Pro), no API credits needed.
Invokes: claude -p --model {model} --output-format json --bare
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from typing import Optional

from eval_core.config import ModelConfig
from eval_core.runners.base import BaseRunner
from eval_core.types import RunnerResponse


class ClaudeCodeRunner(BaseRunner):
    """Invokes Claude via the claude CLI (Claude Code subscription)."""

    def __init__(self, name: str, config: ModelConfig):
        self._name = name
        self._config = config
        # Model alias: "opus", "sonnet", "haiku" or full name
        self._model = config.params.get("cli_model", "opus")

    def model_id(self) -> str:
        return f"claude-code:{self._model}"

    def model_name(self) -> str:
        return self._name

    async def invoke(
        self,
        prompt: str,
        system_prompt: str = "",
        params: dict | None = None,
    ) -> RunnerResponse:
        merged = {**self._config.params, **(params or {})}
        start = time.monotonic()

        # Build the full prompt with system prompt prepended
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        try:
            cmd = [
                "claude",
                "-p",
                "--model", self._model,
                "--output-format", "json",
                "--no-session-persistence",
            ]

            # Add max budget if specified
            max_budget = merged.get("max_budget_usd")
            if max_budget:
                cmd.extend(["--max-budget-usd", str(max_budget)])

            result = subprocess.run(
                cmd,
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=merged.get("timeout_seconds", 300),
            )

            if result.returncode != 0:
                return RunnerResponse(
                    model_id=self.model_id(),
                    output="",
                    error=f"CLI exit code {result.returncode}: {result.stderr[:500]}",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            # Parse JSON output
            output_text = self._parse_output(result.stdout)

            # Strip think blocks if configured
            if self._config.strip_think_blocks and "<think>" in output_text:
                output_text = re.sub(
                    r"<think>.*?</think>", "", output_text, flags=re.DOTALL
                ).strip()

            return RunnerResponse(
                model_id=self.model_id(),
                output=output_text,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except subprocess.TimeoutExpired:
            return RunnerResponse(
                model_id=self.model_id(),
                output="",
                error=f"CLI timed out after {merged.get('timeout_seconds', 300)}s",
                latency_ms=int((time.monotonic() - start) * 1000),
            )
        except Exception as e:
            return RunnerResponse(
                model_id=self.model_id(),
                output="",
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    def _parse_output(self, raw: str) -> str:
        """Parse claude CLI JSON output to extract the response text."""
        raw = raw.strip()

        # Try JSON format first (--output-format json)
        try:
            data = json.loads(raw)
            # JSON output has a "result" field with the text
            if isinstance(data, dict):
                if "result" in data:
                    return data["result"]
                if "content" in data:
                    # May be in content array format
                    content = data["content"]
                    if isinstance(content, list):
                        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
                        return "\n".join(texts)
                    return str(content)
            return raw
        except json.JSONDecodeError:
            # Not JSON, return as plain text
            return raw


def create_claude_code_runner(name: str, config: ModelConfig) -> ClaudeCodeRunner:
    """Factory function to create a ClaudeCodeRunner."""
    return ClaudeCodeRunner(name=name, config=config)
