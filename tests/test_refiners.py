"""Tests for refinement engine."""

import pytest
from pathlib import Path

from eval_core.refiners.diff_gen import generate_diff, apply_changes
from eval_core.refiners.applier import apply_to_file


class TestDiffGenerator:
    def test_generates_diff(self):
        original = "Line 1\nApply colours to CSS variables\nLine 3"
        changes = [{
            "old_text": "Apply colours to CSS variables",
            "new_text": "Apply colours to CSS variables. ALWAYS generate dark/light variants.",
            "section": "Output Format",
            "rationale": "Missing variants",
        }]
        diff = generate_diff(original, changes, "colour_management.skill.md")
        assert diff is not None
        assert "---" in diff
        assert "+++" in diff
        assert "dark/light variants" in diff

    def test_no_diff_if_no_match(self):
        original = "Line 1\nLine 2"
        changes = [{"old_text": "nonexistent text", "new_text": "replacement"}]
        diff = generate_diff(original, changes)
        assert diff is None

    def test_multiple_changes(self):
        original = "AAA\nBBB\nCCC"
        changes = [
            {"old_text": "AAA", "new_text": "XXX"},
            {"old_text": "CCC", "new_text": "ZZZ"},
        ]
        diff = generate_diff(original, changes)
        assert diff is not None
        assert "XXX" in diff
        assert "ZZZ" in diff


class TestApplyChanges:
    def test_applies_single_change(self):
        result = apply_changes("Hello World", [{"old_text": "World", "new_text": "Earth"}])
        assert result == "Hello Earth"

    def test_applies_multiple_changes(self):
        result = apply_changes("A B C", [
            {"old_text": "A", "new_text": "X"},
            {"old_text": "C", "new_text": "Z"},
        ])
        assert result == "X B Z"

    def test_no_change_if_no_match(self):
        result = apply_changes("Original", [{"old_text": "Missing", "new_text": "New"}])
        assert result == "Original"


class TestApplyToFile:
    def test_applies_to_file(self, tmp_path):
        skill = tmp_path / "test.skill.md"
        skill.write_text("Old content here")

        result = apply_to_file(skill, [{"old_text": "Old", "new_text": "New"}])
        assert result is True
        assert skill.read_text() == "New content here"

    def test_no_change_returns_false(self, tmp_path):
        skill = tmp_path / "test.skill.md"
        skill.write_text("Content")

        result = apply_to_file(skill, [{"old_text": "Missing", "new_text": "New"}])
        assert result is False

    def test_missing_file_returns_false(self, tmp_path):
        result = apply_to_file(tmp_path / "nonexistent.md", [])
        assert result is False
