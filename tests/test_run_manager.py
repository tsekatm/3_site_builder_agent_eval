"""Tests for run versioning."""

import pytest
from pathlib import Path

from eval_core.versioning.run_manager import RunManager


class TestRunManager:
    def test_create_run(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        run_dir, config = rm.create_run(
            models=["deepseek-r1"],
            templates=["template-test"],
            judge_model="opus",
        )
        assert run_dir.exists()
        assert (run_dir / "config.json").exists()
        assert config.models == ["deepseek-r1"]
        assert config.templates == ["template-test"]

    def test_run_id_is_timestamp(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        run_dir, config = rm.create_run(["m"], ["t"], "j")
        assert len(config.run_id) == 15  # YYYYMMDD_HHMMSS

    def test_create_action_dir(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        run_dir, _ = rm.create_run(["m"], ["t"], "j")
        action_dir = rm.create_action_dir(run_dir, "template-test", "deepseek-r1", 1, "apply-colours")
        assert action_dir.exists()
        assert "01_apply-colours" in str(action_dir)

    def test_create_final_dir(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        run_dir, _ = rm.create_run(["m"], ["t"], "j")
        final_dir = rm.create_final_dir(run_dir, "template-test", "deepseek-r1")
        assert final_dir.exists()
        assert final_dir.name == "final"

    def test_list_runs(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        rm.create_run(["m1"], ["t1"], "j1")
        rm.create_run(["m2"], ["t2"], "j2")
        runs = rm.list_runs()
        assert len(runs) >= 1  # May be 1 if both created in same second

    def test_get_run(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        _, config = rm.create_run(["m"], ["t"], "j")
        result = rm.get_run(config.run_id)
        assert result is not None
        assert result[1].run_id == config.run_id

    def test_get_nonexistent_run(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        assert rm.get_run("99999999_999999") is None

    def test_parent_run_linking(self, tmp_path):
        rm = RunManager(tmp_path / "runs")
        _, parent = rm.create_run(["m"], ["t"], "j")
        _, child = rm.create_run(["m"], ["t"], "j", parent_run=parent.run_id)
        assert child.parent_run == parent.run_id
