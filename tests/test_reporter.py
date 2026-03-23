"""Tests for markdown report generator."""

import pytest

from eval_core.reporters.markdown import MarkdownReporter
from eval_core.scoring.scorer import score_action, score_stage, score_template
from eval_core.types import EvalRunConfig, Violation, Severity


class TestMarkdownReporter:
    def _make_config(self):
        return EvalRunConfig(
            run_id="20260323_120000",
            models=["deepseek-r1", "kimi-k2.5"],
            templates=["template-test"],
            judge_model="opus",
            timestamp="2026-03-23T12:00:00Z",
        )

    def _make_results(self):
        v = Violation(id="V-1", category="content", severity=Severity.MAJOR,
                      deduction=-1.5, description="Wrong text")
        a1 = score_action(1, "apply-colours", "colour", "colours", violations=[])
        a2 = score_action(2, "swap-fonts", "font", "fonts", violations=[v])
        stage = score_stage(2, "site-generation", [a1, a2])
        tr = score_template("template-test", "deepseek-r1", [stage])

        a3 = score_action(1, "apply-colours", "colour", "colours", violations=[])
        a4 = score_action(2, "swap-fonts", "font", "fonts", violations=[])
        stage2 = score_stage(2, "site-generation", [a3, a4])
        tr2 = score_template("template-test", "kimi-k2.5", [stage2])

        return {
            "deepseek-r1": [tr],
            "kimi-k2.5": [tr2],
        }

    def test_generates_report(self):
        reporter = MarkdownReporter()
        config = self._make_config()
        results = self._make_results()
        report = reporter.generate_report(config, results)
        assert "# Eval Run Report" in report
        assert "20260323_120000" in report

    def test_report_has_score_summary(self):
        reporter = MarkdownReporter()
        report = reporter.generate_report(self._make_config(), self._make_results())
        assert "## Score Summary" in report
        assert "template-test" in report

    def test_report_has_template_breakdown(self):
        reporter = MarkdownReporter()
        report = reporter.generate_report(self._make_config(), self._make_results())
        assert "## Per-Template Breakdown" in report
        assert "apply-colours" in report

    def test_report_shows_violations(self):
        reporter = MarkdownReporter()
        report = reporter.generate_report(self._make_config(), self._make_results())
        assert "Wrong text" in report

    def test_save_report(self, tmp_path):
        reporter = MarkdownReporter()
        report = "# Test Report\nContent here"
        path = reporter.save_report(report, tmp_path / "report.md")
        assert path.exists()
        assert path.read_text() == report
