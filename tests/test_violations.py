"""Tests for violation catalogue."""

import pytest
from pathlib import Path

from eval_core.scoring.violations import ViolationCatalogue
from eval_core.types import Severity


class TestViolationCatalogue:
    def test_loads_catalogue(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        assert len(cat.all()) > 0

    def test_has_all_categories(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        expected = {"structural", "visual", "content", "code_quality", "accessibility", "performance", "interactivity"}
        assert set(cat.categories()) == expected

    def test_get_by_id(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        v = cat.get("STRUCT-MISSING-INDEX")
        assert v is not None
        assert v.severity == Severity.CRITICAL
        assert v.deduction == -5.0

    def test_get_nonexistent(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        assert cat.get("NONEXISTENT") is None

    def test_by_category(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        structural = cat.by_category("structural")
        assert len(structural) == 5

    def test_as_yaml_string(self, violations_yaml_path):
        cat = ViolationCatalogue(violations_yaml_path)
        yaml_str = cat.as_yaml_string()
        assert "STRUCT-MISSING-INDEX" in yaml_str
        assert "critical" in yaml_str
