"""Markdown report generator for eval runs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from eval_core.types import EvalRunConfig, TemplateResult, StageScore, ActionScore


class MarkdownReporter:
    """Generates markdown eval reports."""

    def generate_report(
        self,
        config: EvalRunConfig,
        results: dict[str, list[TemplateResult]],
    ) -> str:
        """Generate a full eval run report.

        Args:
            config: Run configuration.
            results: Dict mapping model_name to list of TemplateResults.
        """
        lines: list[str] = []
        lines.append(f"# Eval Run Report — {config.run_id}")
        lines.append("")
        lines.append(f"**Date**: {config.timestamp}")
        lines.append(f"**Models**: {', '.join(config.models)}")
        lines.append(f"**Templates**: {len(config.templates)}")
        lines.append(f"**Judge**: {config.judge_model}")
        if config.parent_run:
            lines.append(f"**Parent Run**: {config.parent_run}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Score summary table
        lines.append("## Score Summary")
        lines.append("")
        lines.extend(self._score_summary_table(config, results))
        lines.append("")

        # Per-template breakdown
        lines.append("## Per-Template Breakdown")
        lines.append("")
        for template in config.templates:
            lines.extend(self._template_breakdown(template, results))
            lines.append("")

        return "\n".join(lines)

    def _score_summary_table(
        self, config: EvalRunConfig, results: dict[str, list[TemplateResult]],
    ) -> list[str]:
        lines: list[str] = []
        models = config.models

        # Header
        header = "| Template |"
        sep = "|----------|"
        for m in models:
            header += f" {m} |"
            sep += "------|"
        header += " Best |"
        sep += "------|"
        lines.append(header)
        lines.append(sep)

        # Rows
        for template in config.templates:
            row = f"| {template} |"
            scores: dict[str, float] = {}
            for model in models:
                model_results = results.get(model, [])
                tr = next((r for r in model_results if r.template == template), None)
                if tr:
                    scores[model] = tr.template_total
                    row += f" {tr.template_total:.1f} |"
                else:
                    row += " — |"
            best = max(scores, key=scores.get) if scores else "—"
            row += f" {best} |"
            lines.append(row)

        return lines

    def _template_breakdown(
        self, template: str, results: dict[str, list[TemplateResult]],
    ) -> list[str]:
        lines: list[str] = []
        lines.append(f"### {template}")
        lines.append("")

        # Collect all models' results for this template
        models_data: dict[str, TemplateResult] = {}
        for model, model_results in results.items():
            tr = next((r for r in model_results if r.template == template), None)
            if tr:
                models_data[model] = tr

        if not models_data:
            lines.append("*No results*")
            return lines

        # Per-action breakdown for each model
        for model, tr in models_data.items():
            lines.append(f"**{model}** — Total: **{tr.template_total:.1f}**")
            lines.append("")
            for stage in tr.stages:
                lines.append(f"Stage {stage.stage} ({stage.stage_name}): "
                             f"**{stage.stage_total:.1f}** ({stage.action_count} actions, "
                             f"avg {stage.average_score:.1f})")
                if stage.actions:
                    lines.append("")
                    lines.append("| # | Action | Score | Violations | SSIM |")
                    lines.append("|---|--------|-------|------------|------|")
                    for a in stage.actions:
                        v_count = len(a.violations)
                        lines.append(
                            f"| {a.action_id} | {a.action_name} | "
                            f"{a.final_score:.1f} | {v_count} | "
                            f"{a.ssim_score:.2f} |"
                        )
                lines.append("")

            # Top violations
            all_violations = []
            for stage in tr.stages:
                for action in stage.actions:
                    all_violations.extend(action.violations)
            if all_violations:
                top = sorted(all_violations, key=lambda v: v.deduction)[:5]
                lines.append("**Top violations:**")
                for v in top:
                    lines.append(f"- `{v.id}` ({v.severity.value}, {v.deduction}): {v.description}")
                lines.append("")

        return lines

    def save_report(self, report: str, output_path: Path) -> Path:
        """Save report to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        return output_path
