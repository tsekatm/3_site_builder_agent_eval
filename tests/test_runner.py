"""Tests for Bedrock runner and proxy router."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from eval_core.config import ModelConfig
from eval_core.runners.bedrock import BedrockRunner, create_runner
from eval_core.proxy.router import create_anthropic_client, translate_model_id


class TestBedrockRunner:
    def _make_config(self, **overrides):
        defaults = {
            "model_id": "test-model",
            "region": "us-east-1",
            "params": {"temperature": 0.2, "max_tokens": 8192},
            "converse_api": True,
            "strip_think_blocks": False,
        }
        defaults.update(overrides)
        return ModelConfig(**defaults)

    def test_create_runner(self):
        config = self._make_config()
        runner = create_runner("test", config)
        assert runner.model_id() == "test-model"
        assert runner.model_name() == "test"

    def test_model_id(self):
        config = self._make_config(model_id="deepseek.r1-v1:0")
        runner = BedrockRunner("deepseek", config)
        assert runner.model_id() == "deepseek.r1-v1:0"

    def test_strip_think_blocks(self):
        config = self._make_config(strip_think_blocks=True)
        runner = BedrockRunner("test", config)
        result = runner._post_process("<think>reasoning here</think>The actual answer")
        assert result == "The actual answer"

    def test_no_strip_when_disabled(self):
        config = self._make_config(strip_think_blocks=False)
        runner = BedrockRunner("test", config)
        result = runner._post_process("<think>reasoning</think>Answer")
        assert "<think>" in result

    def test_strip_multiline_think(self):
        config = self._make_config(strip_think_blocks=True)
        runner = BedrockRunner("test", config)
        result = runner._post_process(
            "<think>\nStep 1: Think about it\nStep 2: More thinking\n</think>\nFinal answer here"
        )
        assert "Final answer here" in result
        assert "<think>" not in result


class TestProxyRouter:
    def test_translate_to_bedrock(self):
        bedrock_id = translate_model_id("claude-sonnet-4-20250514", to_bedrock=True)
        assert bedrock_id == "anthropic.claude-sonnet-4-20250514-v1:0"

    def test_translate_from_bedrock(self):
        direct_id = translate_model_id("anthropic.claude-opus-4-20250514-v1:0", to_bedrock=False)
        assert direct_id == "claude-opus-4-20250514"

    def test_unknown_model_passthrough(self):
        assert translate_model_id("unknown-model") == "unknown-model"

    def test_translate_deepseek_passthrough(self):
        # DeepSeek IDs are same for direct and Bedrock
        assert translate_model_id("us.deepseek.r1-v1:0") == "us.deepseek.r1-v1:0"


class TestEvalOrchestrator:
    @pytest.mark.asyncio
    async def test_empty_runners(self):
        from eval_core.parallel import EvalOrchestrator
        orch = EvalOrchestrator()
        results = await orch.run_all([], [{"prompt": "test"}])
        assert results == {}

    @pytest.mark.asyncio
    async def test_empty_tasks(self):
        from eval_core.parallel import EvalOrchestrator
        mock_runner = MagicMock()
        mock_runner.model_id.return_value = "test"
        mock_runner.invoke = AsyncMock()

        orch = EvalOrchestrator()
        results = await orch.run_all([mock_runner], [])
        assert "test" in results
        assert len(results["test"]) == 0
