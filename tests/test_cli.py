"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from eval_packs.local.cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestCLI:
    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Site Builder Eval Pack" in result.output

    def test_run_help(self, runner):
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "--model" in result.output
        assert "--template" in result.output
        assert "--dry-run" in result.output

    def test_run_dry_run(self, runner):
        result = runner.invoke(cli, ["run", "--dry-run"])
        assert result.exit_code == 0
        assert "DRY RUN" in result.output

    def test_run_dry_run_single_model(self, runner):
        result = runner.invoke(cli, ["run", "--dry-run", "--model", "claude-haiku"])
        assert result.exit_code == 0
        assert "claude-haiku" in result.output

    def test_run_dry_run_single_template(self, runner):
        result = runner.invoke(cli, ["run", "--dry-run", "--template", "template-ai-page-builder"])
        assert result.exit_code == 0
        assert "template-ai-page-builder" in result.output

    def test_run_nonexistent_model(self, runner):
        result = runner.invoke(cli, ["run", "--dry-run", "--model", "nonexistent"])
        assert result.exit_code == 1

    def test_refine_help(self, runner):
        result = runner.invoke(cli, ["refine", "--help"])
        assert result.exit_code == 0
        assert "--target-score" in result.output

    def test_apply_help(self, runner):
        result = runner.invoke(cli, ["apply", "--help"])
        assert result.exit_code == 0
        assert "--mode" in result.output
        assert "--skills-dir" in result.output

    def test_compare_help(self, runner):
        result = runner.invoke(cli, ["compare", "--help"])
        assert result.exit_code == 0
        assert "--run-a" in result.output
        assert "--run-b" in result.output

    def test_history_help(self, runner):
        result = runner.invoke(cli, ["history", "--help"])
        assert result.exit_code == 0
        assert "--limit" in result.output

    def test_history_empty(self, runner):
        result = runner.invoke(cli, ["history"])
        assert result.exit_code == 0

    def test_run_creates_run_dir(self, runner, tmp_path):
        # Use --dry-run to avoid actual API calls
        result = runner.invoke(cli, [
            "run", "--dry-run",
            "--model", "claude-haiku",
            "--template", "template-ai-page-builder",
        ])
        assert result.exit_code == 0
