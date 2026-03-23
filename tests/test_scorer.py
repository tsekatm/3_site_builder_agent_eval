"""Tests for scoring engine."""

import pytest
from eval_core.scoring.scorer import score_action, score_stage, score_template, BASE_SCORE
from eval_core.types import Violation, Severity


class TestScoreAction:
    def test_perfect_score_no_violations(self):
        result = score_action(
            action_id=1, action_name="apply-colours",
            skill="colour_management", category="colours",
            violations=[],
        )
        assert result.final_score == 10.0
        assert result.total_deductions == 0.0

    def test_single_critical_violation(self, critical_violation):
        result = score_action(
            action_id=1, action_name="apply-colours",
            skill="colour_management", category="colours",
            violations=[critical_violation],
        )
        assert result.final_score == 7.0  # 10 - 3.0
        assert result.total_deductions == -3.0

    def test_single_minor_violation(self, minor_violation):
        result = score_action(
            action_id=1, action_name="apply-colours",
            skill="colour_management", category="colours",
            violations=[minor_violation],
        )
        assert result.final_score == 9.75  # 10 - 0.25

    def test_score_can_go_negative(self):
        violations = [
            Violation(id=f"V-{i}", category="structural", severity=Severity.CRITICAL,
                      deduction=-3.0, description=f"Critical issue {i}")
            for i in range(5)
        ]
        result = score_action(
            action_id=1, action_name="test",
            skill="test", category="test",
            violations=violations,
        )
        assert result.final_score == -5.0  # 10 - 15.0

    def test_no_floor_at_zero(self):
        violations = [
            Violation(id="V-1", category="structural", severity=Severity.CRITICAL,
                      deduction=-3.0, description="Issue 1"),
            Violation(id="V-2", category="visual", severity=Severity.CRITICAL,
                      deduction=-3.0, description="Issue 2"),
            Violation(id="V-3", category="content", severity=Severity.CRITICAL,
                      deduction=-2.0, description="Issue 3"),
            Violation(id="V-4", category="content", severity=Severity.MAJOR,
                      deduction=-1.5, description="Issue 4"),
            Violation(id="V-5", category="code_quality", severity=Severity.MAJOR,
                      deduction=-1.5, description="Issue 5"),
            Violation(id="V-6", category="accessibility", severity=Severity.MODERATE,
                      deduction=-0.5, description="Issue 6"),
        ]
        result = score_action(
            action_id=1, action_name="test",
            skill="test", category="test",
            violations=violations,
        )
        # 10 - 3 - 3 - 2 - 1.5 - 1.5 - 0.5 = -1.5
        assert result.final_score == -1.5

    def test_ssim_score_stored(self):
        result = score_action(
            action_id=1, action_name="test",
            skill="test", category="test",
            violations=[], ssim_score=0.85,
        )
        assert result.ssim_score == 0.85


class TestScoreStage:
    def test_aggregates_action_scores(self):
        actions = [
            score_action(1, "a1", "s1", "c1", violations=[]),      # 10.0
            score_action(2, "a2", "s2", "c2", violations=[]),      # 10.0
            score_action(3, "a3", "s3", "c3", violations=[
                Violation(id="V-1", category="content", severity=Severity.MAJOR,
                          deduction=-1.5, description="Issue"),
            ]),                                                       # 8.5
        ]
        stage = score_stage(stage=2, stage_name="site-generation", action_scores=actions)
        assert stage.action_count == 3
        assert stage.stage_total == 28.5  # 10 + 10 + 8.5
        assert stage.average_score == pytest.approx(9.5)

    def test_empty_actions(self):
        stage = score_stage(stage=1, stage_name="test", action_scores=[])
        assert stage.action_count == 0
        assert stage.stage_total == 0.0
        assert stage.average_score == 0.0


class TestScoreTemplate:
    def test_template_total(self):
        stages = [
            score_stage(1, "s1", [score_action(1, "a", "s", "c", violations=[])]),  # 10.0
            score_stage(2, "s2", [score_action(1, "a", "s", "c", violations=[])]),  # 10.0
            score_stage(3, "s3", [score_action(1, "a", "s", "c", violations=[])]),  # 10.0
        ]
        result = score_template("template-test", "deepseek-r1", stages)
        assert result.template_total == 30.0

    def test_template_with_violations(self):
        v = Violation(id="V-1", category="content", severity=Severity.CRITICAL,
                      deduction=-2.0, description="Missing text")
        stages = [
            score_stage(1, "s1", [score_action(1, "a", "s", "c", violations=[v])]),  # 8.0
            score_stage(2, "s2", [score_action(1, "a", "s", "c", violations=[v])]),  # 8.0
            score_stage(3, "s3", [score_action(1, "a", "s", "c", violations=[])]),   # 10.0
        ]
        result = score_template("template-test", "kimi-k2.5", stages)
        assert result.template_total == 26.0
