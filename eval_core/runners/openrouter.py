"""OpenRouter runner — multi-model hub via OpenAI-compatible API.

Supports DeepSeek, Kimi, and any model on openrouter.ai.
Requires OPENROUTER_API_KEY environment variable or api_key parameter.
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import Optional

import urllib.request
import urllib.error

from eval_core.config import ModelConfig
from eval_core.runners.base import BaseRunner
from eval_core.types import RunnerResponse


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterRunner(BaseRunner):
    """Invokes models via the OpenRouter API (OpenAI-compatible)."""

    def __init__(self, name: str, config: ModelConfig, api_key: Optional[str] = None):
        self._name = name
        self._config = config
        self._api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")

    def model_id(self) -> str:
        return self._config.model_id

    def model_name(self) -> str:
        return self._name

    async def invoke(
        self,
        prompt: str | list,
        system_prompt: str = "",
        params: dict | None = None,
    ) -> RunnerResponse:
        """Invoke the model. prompt can be a string or a list of content
        blocks (multipart) for vision models."""
        merged = {**self._config.params, **(params or {})}
        start = time.monotonic()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        # Support both str and list (multipart vision content)
        messages.append({"role": "user", "content": prompt})

        body = {
            "model": self._config.model_id,
            "messages": messages,
            "max_tokens": merged.get("max_tokens", 8192),
            "temperature": merged.get("temperature", 0.2),
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": "https://eval-pack.bigbeard.co.za",
            "X-Title": "Site Builder Eval Pack",
        }

        try:
            req = urllib.request.Request(
                OPENROUTER_BASE_URL,
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=merged.get("timeout_seconds", 600)) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            output_text = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})

            # Strip think blocks if configured
            if self._config.strip_think_blocks and "<think>" in output_text:
                output_text = re.sub(
                    r"<think>.*?</think>", "", output_text, flags=re.DOTALL
                ).strip()

            return RunnerResponse(
                model_id=self._config.model_id,
                output=output_text,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            return RunnerResponse(
                model_id=self._config.model_id,
                output="",
                error=f"HTTP {e.code}: {error_body[:200]}",
                latency_ms=int((time.monotonic() - start) * 1000),
            )
        except Exception as e:
            return RunnerResponse(
                model_id=self._config.model_id,
                output="",
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )


def create_openrouter_runner(
    name: str,
    config: ModelConfig,
    api_key: Optional[str] = None,
) -> OpenRouterRunner:
    """Factory function to create an OpenRouterRunner."""
    return OpenRouterRunner(name=name, config=config, api_key=api_key)
