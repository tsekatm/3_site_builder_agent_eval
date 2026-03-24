"""Direct Anthropic API runner — bypasses Bedrock, uses api.anthropic.com."""

from __future__ import annotations

import os
import re
import time
from typing import Optional

from eval_core.config import ModelConfig
from eval_core.runners.base import BaseRunner
from eval_core.types import RunnerResponse


class AnthropicDirectRunner(BaseRunner):
    """Invokes Claude models via the direct Anthropic API (not Bedrock)."""

    def __init__(self, name: str, config: ModelConfig, api_key: Optional[str] = None):
        self._name = name
        self._config = config
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

        import anthropic
        self._client = anthropic.Anthropic(api_key=self._api_key)

    def model_id(self) -> str:
        return self._config.model_id

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

        try:
            kwargs = {
                "model": self._config.model_id,
                "max_tokens": merged.get("max_tokens", 8192),
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            if "temperature" in merged:
                kwargs["temperature"] = merged["temperature"]

            response = self._client.messages.create(**kwargs)

            output_text = response.content[0].text
            usage = response.usage

            # Strip think blocks if configured
            if self._config.strip_think_blocks and "<think>" in output_text:
                output_text = re.sub(
                    r"<think>.*?</think>", "", output_text, flags=re.DOTALL
                ).strip()

            return RunnerResponse(
                model_id=self._config.model_id,
                output=output_text,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except Exception as e:
            return RunnerResponse(
                model_id=self._config.model_id,
                output="",
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )


def create_direct_runner(
    name: str,
    config: ModelConfig,
    api_key: Optional[str] = None,
) -> AnthropicDirectRunner:
    """Factory function to create an AnthropicDirectRunner."""
    return AnthropicDirectRunner(name=name, config=config, api_key=api_key)
