"""Run directory management — creates and manages timestamped eval runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from eval_core.types import EvalRunConfig


class RunManager:
    """Manages eval run directories under runs/YYYYMMDD_HHMMSS/."""

    def __init__(self, runs_dir: str | Path = "./runs"):
        self.runs_dir = Path(runs_dir)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def create_run(
        self,
        models: list[str],
        templates: list[str],
        judge_model: str,
        parent_run: Optional[str] = None,
    ) -> tuple[Path, EvalRunConfig]:
        """Create a new timestamped run directory and return (path, config)."""
        now = datetime.now(timezone.utc)
        run_id = now.strftime("%Y%m%d_%H%M%S")
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        config = EvalRunConfig(
            run_id=run_id,
            models=models,
            templates=templates,
            judge_model=judge_model,
            timestamp=now.isoformat(),
            parent_run=parent_run,
        )

        # Write config snapshot
        config_path = run_dir / "config.json"
        config_path.write_text(json.dumps(config.model_dump(), indent=2))

        return run_dir, config

    def create_action_dir(
        self,
        run_dir: Path,
        template: str,
        model: str,
        action_id: int,
        action_name: str,
    ) -> Path:
        """Create directory for a specific action's output."""
        action_dir = run_dir / template / model / "actions" / f"{action_id:02d}_{action_name}"
        action_dir.mkdir(parents=True, exist_ok=True)
        return action_dir

    def create_final_dir(self, run_dir: Path, template: str, model: str) -> Path:
        """Create directory for the final state output."""
        final_dir = run_dir / template / model / "final"
        final_dir.mkdir(parents=True, exist_ok=True)
        return final_dir

    def list_runs(self, limit: int = 10) -> list[tuple[str, EvalRunConfig]]:
        """List recent runs, newest first."""
        runs = []
        for run_dir in sorted(self.runs_dir.iterdir(), reverse=True):
            if run_dir.is_dir() and (run_dir / "config.json").exists():
                config_data = json.loads((run_dir / "config.json").read_text())
                runs.append((run_dir.name, EvalRunConfig(**config_data)))
                if len(runs) >= limit:
                    break
        return runs

    def get_run(self, run_id: str) -> Optional[tuple[Path, EvalRunConfig]]:
        """Get a specific run by ID."""
        run_dir = self.runs_dir / run_id
        config_path = run_dir / "config.json"
        if not config_path.exists():
            return None
        config_data = json.loads(config_path.read_text())
        return run_dir, EvalRunConfig(**config_data)
