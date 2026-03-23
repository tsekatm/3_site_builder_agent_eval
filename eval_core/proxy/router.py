"""Proxy router — factory for creating model clients."""

from __future__ import annotations

from eval_core.config import ModelConfig


# Direct API model ID → Bedrock model ID mapping
MODEL_ID_MAP = {
    "claude-sonnet-4-20250514": "anthropic.claude-sonnet-4-20250514-v1:0",
    "claude-opus-4-20250514": "anthropic.claude-opus-4-20250514-v1:0",
}


def create_anthropic_client(config: ModelConfig):
    """Create Anthropic or AnthropicBedrock client based on config.

    For Claude models: AnthropicBedrock is a drop-in replacement.
    Returns a client with identical .messages.create() interface.
    """
    import anthropic

    if config.region:
        return anthropic.AnthropicBedrock(aws_region=config.region)
    else:
        return anthropic.Anthropic()


def translate_model_id(model_id: str, to_bedrock: bool = True) -> str:
    """Translate between direct API and Bedrock model IDs."""
    if to_bedrock:
        return MODEL_ID_MAP.get(model_id, model_id)
    else:
        reverse = {v: k for k, v in MODEL_ID_MAP.items()}
        return reverse.get(model_id, model_id)
