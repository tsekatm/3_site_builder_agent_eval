"""Bedrock runner — invokes models via AWS Bedrock Converse or InvokeModel API."""

from __future__ import annotations

import json
import re
import time
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from eval_core.config import ModelConfig
from eval_core.runners.base import BaseRunner
from eval_core.types import RunnerResponse


class BedrockRunner(BaseRunner):
    """Invokes Bedrock models using Converse API (with InvokeModel fallback)."""

    def __init__(self, name: str, config: ModelConfig, aws_profile: str | None = None):
        self._name = name
        self._config = config
        session = boto3.Session(profile_name=aws_profile) if aws_profile else boto3.Session()
        self._client = session.client("bedrock-runtime", region_name=config.region)

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
            if self._config.converse_api:
                return await self._invoke_converse(prompt, system_prompt, merged, start)
            else:
                return await self._invoke_raw(prompt, system_prompt, merged, start)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            return RunnerResponse(
                model_id=self._config.model_id,
                output="",
                error=f"{error_code}: {e.response['Error']['Message']}",
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    async def _invoke_converse(
        self, prompt: str, system_prompt: str, params: dict, start: float,
    ) -> RunnerResponse:
        kwargs: dict = {
            "modelId": self._config.model_id,
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {
                "temperature": params.get("temperature", 0.2),
                "maxTokens": params.get("max_tokens", 8192),
            },
        }
        if system_prompt:
            kwargs["system"] = [{"text": system_prompt}]

        response = self._client.converse(**kwargs)

        output_text = response["output"]["message"]["content"][0]["text"]
        usage = response.get("usage", {})

        output_text = self._post_process(output_text)

        return RunnerResponse(
            model_id=self._config.model_id,
            output=output_text,
            input_tokens=usage.get("inputTokens", 0),
            output_tokens=usage.get("outputTokens", 0),
            latency_ms=int((time.monotonic() - start) * 1000),
        )

    async def _invoke_raw(
        self, prompt: str, system_prompt: str, params: dict, start: float,
    ) -> RunnerResponse:
        """Fallback for models without Converse API support (e.g., DeepSeek R1)."""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        body = {
            "prompt": full_prompt,
            "max_tokens": params.get("max_tokens", 8192),
            "temperature": params.get("temperature", 0.2),
        }

        response = self._client.invoke_model(
            modelId=self._config.model_id,
            contentType="application/json",
            body=json.dumps(body),
        )

        result = json.loads(response["body"].read())

        # Handle different response formats per model family
        output_text = ""
        if "choices" in result:
            output_text = result["choices"][0].get("message", {}).get("content", "")
        elif "output" in result:
            output_text = result["output"]
        elif "completion" in result:
            output_text = result["completion"]
        else:
            output_text = json.dumps(result)

        output_text = self._post_process(output_text)

        return RunnerResponse(
            model_id=self._config.model_id,
            output=output_text,
            latency_ms=int((time.monotonic() - start) * 1000),
        )

    def _post_process(self, output: str) -> str:
        """Post-process model output (e.g., strip DeepSeek R1 think blocks)."""
        if self._config.strip_think_blocks and "<think>" in output:
            output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()
        return output


def create_runner(name: str, config: ModelConfig, aws_profile: str | None = None) -> BedrockRunner:
    """Factory function to create a BedrockRunner from config."""
    return BedrockRunner(name=name, config=config, aws_profile=aws_profile)
