"""Tests for judge engine."""

import pytest
import json
from unittest.mock import AsyncMock

from eval_core.judges.opus_judge import OpusJudge
from eval_core.types import RunnerResponse, Severity


class TestOpusJudge:
    def _make_judge(self, response_text: str, error: str = None):
        mock_runner = AsyncMock()
        mock_runner.invoke.return_value = RunnerResponse(
            model_id="test-judge",
            output=response_text,
            error=error,
        )
        return OpusJudge(runner=mock_runner, violation_catalogue_yaml="test catalogue")

    @pytest.mark.asyncio
    async def test_no_violations_on_perfect_output(self):
        judge = self._make_judge(json.dumps({
            "violations": [],
            "summary": "Perfect execution",
            "strengths": ["All correct"],
            "critical_issues": [],
        }))
        violations = await judge.evaluate_action(
            "apply-colours", "colour_management", "colours",
            "Apply primary #B85C38", ["Primary: #B85C38"],
            "<html>gold</html>", ":root{}", "<html>agent</html>", ":root{}",
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_parses_violations(self):
        judge = self._make_judge(json.dumps({
            "violations": [
                {
                    "id": "VIS-COLOUR-MISMATCH",
                    "category": "visual",
                    "severity": "moderate",
                    "deduction": -0.5,
                    "file": "css/styles.css",
                    "description": "Wrong primary colour",
                    "evidence": "--primary-color: #FF0000 (expected #B85C38)",
                    "recommendation": "Update to #B85C38",
                }
            ],
            "summary": "Colour mismatch",
            "strengths": [],
            "critical_issues": ["Wrong colour"],
        }))
        violations = await judge.evaluate_action(
            "apply-colours", "colour_management", "colours",
            "Apply primary #B85C38", [],
            "<html></html>", ":root{}", "<html></html>", ":root{}",
        )
        assert len(violations) == 1
        assert violations[0].id == "VIS-COLOUR-MISMATCH"
        assert violations[0].severity == Severity.MODERATE
        assert violations[0].deduction == -0.5

    @pytest.mark.asyncio
    async def test_handles_json_in_markdown_block(self):
        judge = self._make_judge('```json\n{"violations": [], "summary": "ok"}\n```')
        violations = await judge.evaluate_action(
            "test", "test", "test", "test", [],
            "", "", "", "",
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_handles_runner_error(self):
        judge = self._make_judge("", error="ThrottlingException")
        violations = await judge.evaluate_action(
            "test", "test", "test", "test", [],
            "", "", "", "",
        )
        assert len(violations) == 1
        assert violations[0].id == "JUDGE-ERROR"
        assert violations[0].severity == Severity.CRITICAL

    @pytest.mark.asyncio
    async def test_handles_malformed_json(self):
        judge = self._make_judge("This is not JSON at all {broken")
        violations = await judge.evaluate_action(
            "test", "test", "test", "test", [],
            "", "", "", "",
        )
        # Should return parse error violation
        assert len(violations) == 1
        assert "parse" in violations[0].id.lower() or "JUDGE" in violations[0].id

    @pytest.mark.asyncio
    async def test_multiple_violations(self):
        judge = self._make_judge(json.dumps({
            "violations": [
                {"id": "CONTENT-PLACEHOLDER", "category": "content", "severity": "major", "deduction": -1.0, "description": "Unreplaced token"},
                {"id": "A11Y-MISSING-ALT", "category": "accessibility", "severity": "moderate", "deduction": -0.5, "description": "Missing alt"},
                {"id": "PERF-NO-FONT-DISPLAY", "category": "performance", "severity": "minor", "deduction": -0.25, "description": "No swap"},
            ],
            "summary": "Several issues",
        }))
        violations = await judge.evaluate_action(
            "test", "test", "test", "test", [],
            "", "", "", "",
        )
        assert len(violations) == 3
        total = sum(v.deduction for v in violations)
        assert total == -1.75

    @pytest.mark.asyncio
    async def test_invalid_severity_skipped(self):
        judge = self._make_judge(json.dumps({
            "violations": [
                {"id": "V-1", "category": "test", "severity": "invalid_severity", "deduction": -1.0, "description": "bad"},
                {"id": "V-2", "category": "test", "severity": "major", "deduction": -1.0, "description": "good"},
            ],
        }))
        violations = await judge.evaluate_action(
            "test", "test", "test", "test", [],
            "", "", "", "",
        )
        # Invalid severity should be skipped, valid one kept
        assert len(violations) == 1
        assert violations[0].id == "V-2"
