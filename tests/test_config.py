"""Tests for configuration loading."""

import pytest
from pathlib import Path

from eval_core.config import load_config, get_enabled_models, EvalConfig


class TestLoadConfig:
    def test_loads_valid_config(self, config):
        assert isinstance(config, EvalConfig)
        assert len(config.models) > 0

    def test_has_all_three_models(self, config):
        assert "deepseek-r1" in config.models
        assert "deepseek-v3.2" in config.models
        assert "kimi-k2.5" in config.models

    def test_has_judge(self, config):
        assert "default" in config.judges
        assert config.judges["default"].params["temperature"] == 0.0

    def test_has_teacher(self, config):
        assert "default" in config.teachers

    def test_has_paths(self, config):
        assert config.paths.gold_standards == "./gold-standards"
        assert config.paths.runs == "./runs"

    def test_has_defaults(self, config):
        assert config.defaults.parallel_workers == 3
        assert config.defaults.parallel_prompts == 5

    def test_missing_config_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_config(tmp_path / "nonexistent.yaml")


class TestGetEnabledModels:
    def test_all_returns_enabled(self, config):
        models = get_enabled_models(config)
        assert len(models) == 3

    def test_filter_by_name(self, config):
        models = get_enabled_models(config, names="deepseek-r1")
        assert len(models) == 1
        assert "deepseek-r1" in models

    def test_filter_by_tag(self, config):
        models = get_enabled_models(config, tag="multimodal")
        assert len(models) == 1
        assert "kimi-k2.5" in models

    def test_filter_by_multiple_names(self, config):
        models = get_enabled_models(config, names="deepseek-r1,kimi-k2.5")
        assert len(models) == 2

    def test_deepseek_r1_no_converse(self, config):
        assert config.models["deepseek-r1"].converse_api is False
        assert config.models["deepseek-r1"].strip_think_blocks is True
