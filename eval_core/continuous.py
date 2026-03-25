"""Continuous improvement loop — eval → extract patterns → update skills → re-run → measure.

Usage:
    eval-cli improve --template template-safari-lodge --target-score 8.0 --max-iterations 3
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Optional, Callable

from eval_core.actions import parse_requirements_to_actions
from eval_core.config import EvalConfig, ModelConfig
from eval_core.orchestrator import run_eval_for_template
from eval_core.refiners.teacher import TeacherEngine
from eval_core.refiners.diff_gen import generate_diff, save_diff
from eval_core.refiners.applier import apply_to_file
from eval_core.reporters.markdown import MarkdownReporter
from eval_core.runners.claude_code import create_claude_code_runner
from eval_core.runners.bedrock import create_runner
from eval_core.types import TemplateResult, ActionScore, StageScore
from eval_core.versioning.run_manager import RunManager


class ContinuousImprover:
    """Orchestrates the continuous improvement loop."""

    def __init__(
        self,
        config: EvalConfig,
        skills_dir: Path,
        aws_profile: Optional[str] = None,
        on_progress: Optional[Callable] = None,
    ):
        self.config = config
        self.skills_dir = skills_dir
        self.aws_profile = aws_profile
        self.on_progress = on_progress
        self.run_manager = RunManager(config.paths.runs)
        self.reporter = MarkdownReporter()

    async def improve(
        self,
        template: str,
        models: list[str],
        target_score: float = 8.0,
        max_iterations: int = 3,
    ) -> dict:
        """Run the continuous improvement loop.

        Args:
            template: Template name to evaluate.
            models: Model names to evaluate.
            target_score: Average action score target (stop when reached).
            max_iterations: Maximum improvement cycles.

        Returns:
            Dict with iteration history, final scores, and skill changes applied.
        """
        history: list[dict] = []
        skill_changes_applied: list[dict] = []
        best_scores: dict[str, float] = {}

        for iteration in range(1, max_iterations + 1):
            if self.on_progress:
                self.on_progress("loop", template, f"iteration {iteration}/{max_iterations}", "starting")

            # --- Step 1: Run eval ---
            run_dir, run_config = self.run_manager.create_run(
                models=models,
                templates=[template],
                judge_model=self.config.judges["default"].model_id,
                parent_run=history[-1]["run_id"] if history else None,
            )

            all_results: dict[str, list[TemplateResult]] = {}
            for model_name in models:
                model_config = self.config.models[model_name]
                result = await run_eval_for_template(
                    template_name=template,
                    model_name=model_name,
                    model_config=model_config,
                    judge_config=self.config.judges["default"],
                    config=self.config,
                    run_dir=run_dir,
                    aws_profile=self.aws_profile,
                    on_progress=self.on_progress,
                    capture_screenshots=True,
                )
                all_results[model_name] = [result]

                if self.on_progress:
                    self.on_progress(model_name, template, "eval complete",
                                     f"total: {result.template_total:.1f}")

            # --- Step 2: Check if target met ---
            iteration_scores = {}
            all_above_target = True
            for model_name, results in all_results.items():
                r = results[0]
                avg = r.stages[0].average_score if r.stages else 0
                iteration_scores[model_name] = {
                    "total": r.template_total,
                    "average": avg,
                    "actions": [(a.action_name, a.final_score) for s in r.stages for a in s.actions],
                }
                if avg < target_score:
                    all_above_target = False

            history.append({
                "iteration": iteration,
                "run_id": run_config.run_id,
                "scores": iteration_scores,
            })

            # Generate report
            report = self.reporter.generate_report(run_config, all_results)
            self.reporter.save_report(report, run_dir / "report.md")

            if all_above_target:
                if self.on_progress:
                    self.on_progress("loop", template, f"iteration {iteration}",
                                     f"TARGET MET — all models avg >= {target_score}")
                break

            if iteration >= max_iterations:
                if self.on_progress:
                    self.on_progress("loop", template, f"iteration {iteration}",
                                     f"MAX ITERATIONS reached")
                break

            # --- Step 3: Extract low-scoring patterns ---
            low_actions = self._extract_low_actions(all_results, target_score)
            if not low_actions:
                if self.on_progress:
                    self.on_progress("loop", template, f"iteration {iteration}",
                                     "no low-scoring actions to improve")
                break

            if self.on_progress:
                self.on_progress("loop", template, f"iteration {iteration}",
                                 f"found {len(low_actions)} low-scoring action patterns")

            # --- Step 4: Generate skill diffs ---
            teacher_config = self.config.teachers["default"]
            teacher_runner = create_claude_code_runner("teacher", teacher_config)
            teacher = TeacherEngine(runner=teacher_runner)

            for skill_name, actions in low_actions.items():
                skill_path = self.skills_dir / skill_name
                if not skill_path.exists():
                    continue

                skill_content = skill_path.read_text()
                proposal = await teacher.propose_improvements(
                    skill_content=skill_content,
                    model="all models",
                    template=template,
                    low_scoring_actions=actions,
                    target_score=target_score,
                )

                if proposal and proposal.get("changes"):
                    # Generate diff
                    diff = generate_diff(skill_content, proposal["changes"], skill_name)
                    if diff:
                        diff_path = run_dir / "diffs" / f"{skill_name}.diff"
                        save_diff(diff, diff_path)

                        # Save proposal
                        proposal_path = run_dir / "diffs" / f"{skill_name}.json"
                        proposal_path.parent.mkdir(parents=True, exist_ok=True)
                        proposal_path.write_text(json.dumps(proposal, indent=2))

                        if self.on_progress:
                            self.on_progress("teacher", template, skill_name,
                                             f"proposed {len(proposal['changes'])} changes")

            # --- Step 5: Auto-apply diffs (prompt improvements go in automatically) ---
            diffs_dir = run_dir / "diffs"
            if diffs_dir.exists():
                for proposal_file in diffs_dir.glob("*.json"):
                    skill_name = proposal_file.stem
                    skill_path = self.skills_dir / skill_name
                    if not skill_path.exists():
                        continue

                    proposal = json.loads(proposal_file.read_text())
                    changes = proposal.get("changes", [])
                    if changes:
                        applied = apply_to_file(skill_path, changes)
                        if applied:
                            skill_changes_applied.append({
                                "iteration": iteration,
                                "skill": skill_name,
                                "changes": len(changes),
                                "reasoning": proposal.get("reasoning", ""),
                            })
                            if self.on_progress:
                                self.on_progress("apply", template, skill_name,
                                                 f"applied {len(changes)} changes")

            # --- Step 6: Check for convergence ---
            if len(history) >= 2:
                prev_avg = sum(
                    s["average"] for s in history[-2]["scores"].values()
                ) / len(history[-2]["scores"])
                curr_avg = sum(
                    s["average"] for s in history[-1]["scores"].values()
                ) / len(history[-1]["scores"])

                if abs(curr_avg - prev_avg) < 0.3:
                    if self.on_progress:
                        self.on_progress("loop", template, f"iteration {iteration}",
                                         f"CONVERGED — improvement < 0.3 ({prev_avg:.1f} → {curr_avg:.1f})")
                    break

        # Final summary
        return {
            "template": template,
            "iterations": len(history),
            "history": history,
            "skill_changes": skill_changes_applied,
            "final_scores": history[-1]["scores"] if history else {},
            "target_met": all_above_target,
        }

    def _extract_low_actions(
        self,
        results: dict[str, list[TemplateResult]],
        target: float,
    ) -> dict[str, list[ActionScore]]:
        """Group low-scoring actions by skill file."""
        skill_map = {
            "colours": "colour_management.skill.md",
            "fonts": "global_font_management.skill.md",
            "logos": "logo_replacement.skill.md",
            "images": "background_image_changer.skill.md",
            "text": "template_customization.skill.md",
            "layout": "layout_transformation.skill.md",
            "seo": "template_customization.skill.md",
            "accessibility": "template_customization.skill.md",
            "interactivity": "template_customization.skill.md",
        }

        low_by_skill: dict[str, list[ActionScore]] = {}

        for model_name, model_results in results.items():
            for result in model_results:
                for stage in result.stages:
                    for action in stage.actions:
                        if action.final_score < target:
                            skill = skill_map.get(action.category, "template_customization.skill.md")
                            if skill not in low_by_skill:
                                low_by_skill[skill] = []
                            low_by_skill[skill].append(action)

        return low_by_skill
