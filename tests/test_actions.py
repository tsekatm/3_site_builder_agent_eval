"""Tests for action sequence parsing."""

import pytest
from pathlib import Path

from eval_core.actions import parse_requirements_to_actions


class TestParseRequirements:
    def test_parses_sample_requirements(self, sample_requirements):
        seq = parse_requirements_to_actions("template-ai-page-builder", sample_requirements)
        assert seq.template == "template-ai-page-builder"
        assert len(seq.actions) > 0

    def test_has_colour_action(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        names = [a.name for a in seq.actions]
        assert "apply-colours" in names

    def test_has_font_action(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        names = [a.name for a in seq.actions]
        assert "swap-fonts" in names

    def test_actions_are_sequential(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        ids = [a.id for a in seq.actions]
        assert ids == list(range(1, len(ids) + 1))

    def test_no_duplicate_action_names(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        names = [a.name for a in seq.actions]
        assert len(names) == len(set(names))

    def test_each_action_has_description(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        for action in seq.actions:
            assert action.description.strip() != ""

    def test_each_action_has_skill(self, sample_requirements):
        seq = parse_requirements_to_actions("test", sample_requirements)
        for action in seq.actions:
            assert action.skill != ""

    def test_empty_requirements(self, tmp_path):
        req = tmp_path / "requirements.md"
        req.write_text("# Empty\n\nNo sections here.")
        seq = parse_requirements_to_actions("test", req)
        assert len(seq.actions) == 0
