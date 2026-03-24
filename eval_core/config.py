"""Configuration loader for eval_config.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    model_id: str
    region: str = "us-east-1"
    provider: str = "bedrock"  # "bedrock" or "anthropic-direct"
    params: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    converse_api: bool = True
    strip_think_blocks: bool = False
    enabled: bool = True


class PathsConfig(BaseModel):
    gold_standards: str = "./gold-standards"
    templates: str = "../bigbeard-templates"
    runs: str = "./runs"
    violations: str = "./eval_core/scoring/violations.yaml"


class DefaultsConfig(BaseModel):
    parallel_workers: int = 3
    parallel_prompts: int = 5
    timeout_seconds: int = 120
    judge_runs: int = 1


class EvalConfig(BaseModel):
    models: dict[str, ModelConfig] = Field(default_factory=dict)
    judges: dict[str, ModelConfig] = Field(default_factory=dict)
    teachers: dict[str, ModelConfig] = Field(default_factory=dict)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)


def load_config(path: str | Path = "eval_config.yaml") -> EvalConfig:
    """Load and validate eval configuration from YAML."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    return EvalConfig(**raw)


def get_enabled_models(
    config: EvalConfig,
    names: str = "all",
    tag: Optional[str] = None,
) -> dict[str, ModelConfig]:
    """Get enabled models, optionally filtered by name or tag."""
    models = {k: v for k, v in config.models.items() if v.enabled}

    if names != "all":
        selected = {n.strip() for n in names.split(",")}
        models = {k: v for k, v in models.items() if k in selected}

    if tag:
        models = {k: v for k, v in models.items() if tag in v.tags}

    return models
