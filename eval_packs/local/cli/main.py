"""Eval Pack CLI — local mode entry point."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from eval_core.config import load_config, get_enabled_models, EvalConfig
from eval_core.actions import parse_requirements_to_actions
from eval_core.scoring.violations import ViolationCatalogue
from eval_core.versioning.run_manager import RunManager
from eval_core.reporters.markdown import MarkdownReporter

console = Console()


@click.group()
@click.option("--config", "-c", default="eval_config.yaml", help="Config file path")
@click.pass_context
def cli(ctx, config):
    """Site Builder Eval Pack — Local Mode"""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["config_path"] = config


@cli.command()
@click.option("--model", "-m", default="all", help="Model name(s) comma-separated, or 'all'")
@click.option("--model-tag", help="Run models matching this tag")
@click.option("--template", "-t", default="all", help="Template name(s) comma-separated, or 'all'")
@click.option("--stage", "-s", type=click.Choice(["1", "2", "3", "all"]), default="all")
@click.option("--parallel-workers", type=int, help="Override parallel model workers")
@click.option("--output-dir", "-o", help="Override output directory")
@click.option("--dry-run", is_flag=True, help="Show what would run without executing")
@click.pass_context
def run(ctx, model, model_tag, template, stage, parallel_workers, output_dir, dry_run):
    """Run evaluation against configured models."""
    config: EvalConfig = ctx.obj["config"]
    models = get_enabled_models(config, names=model, tag=model_tag)

    if not models:
        console.print("[red]No models matched the filter.[/red]")
        raise SystemExit(1)

    # Resolve templates
    gold_dir = Path(config.paths.gold_standards)
    if template == "all":
        templates = [d.name for d in gold_dir.iterdir()
                     if d.is_dir() and d.name.startswith("template-")
                     and (d / "requirements.md").exists()]
    else:
        templates = [t.strip() for t in template.split(",")]

    if not templates:
        console.print("[red]No templates found.[/red]")
        raise SystemExit(1)

    # Parse actions for each template
    template_actions = {}
    for t in templates:
        req_path = gold_dir / t / "requirements.md"
        if req_path.exists():
            template_actions[t] = parse_requirements_to_actions(t, req_path)

    if dry_run:
        _show_dry_run(models, templates, template_actions, stage)
        return

    # Create run directory
    rm = RunManager(config.paths.runs)
    run_dir, run_config = rm.create_run(
        models=list(models.keys()),
        templates=templates,
        judge_model=config.judges.get("default", list(config.judges.values())[0]).model_id,
    )

    console.print(f"\n[green]Run created: {run_config.run_id}[/green]")
    console.print(f"  Models: {', '.join(models.keys())}")
    console.print(f"  Templates: {len(templates)}")
    console.print(f"  Output: {run_dir}")
    console.print(f"\n[yellow]To execute the eval, Bedrock API calls are required.[/yellow]")
    console.print(f"[yellow]Run directory prepared at: {run_dir}[/yellow]")


@cli.command()
@click.option("--run", "-r", "run_dir", required=True, help="Path to completed run directory")
@click.option("--teacher", default="default", help="Teacher model name from config")
@click.option("--target-score", type=float, default=7.0, help="Minimum acceptable action score")
@click.option("--max-iterations", type=int, default=5, help="Max refinement iterations")
@click.pass_context
def refine(ctx, run_dir, teacher, target_score, max_iterations):
    """Generate skill enhancement proposals from eval results."""
    config: EvalConfig = ctx.obj["config"]
    run_path = Path(run_dir)

    if not run_path.exists():
        console.print(f"[red]Run directory not found: {run_path}[/red]")
        raise SystemExit(1)

    scores_files = list(run_path.rglob("scores.json"))
    if not scores_files:
        console.print("[red]No scores.json found in run directory.[/red]")
        raise SystemExit(1)

    console.print(f"[green]Refine: {run_path.name}[/green]")
    console.print(f"  Teacher: {teacher}")
    console.print(f"  Target score: {target_score}")
    console.print(f"  Max iterations: {max_iterations}")
    console.print(f"  Score files found: {len(scores_files)}")


@cli.command()
@click.option("--run", "-r", "run_dir", required=True, help="Path to run with diffs")
@click.option("--mode", type=click.Choice(["all", "interactive"]), default="interactive")
@click.option("--skills-dir", required=True, help="Target skills directory to patch")
@click.pass_context
def apply(ctx, run_dir, mode, skills_dir):
    """Apply accepted skill enhancement diffs."""
    run_path = Path(run_dir)
    skills_path = Path(skills_dir)

    if not run_path.exists():
        console.print(f"[red]Run directory not found: {run_path}[/red]")
        raise SystemExit(1)

    diffs_dir = run_path / "diffs"
    if not diffs_dir.exists() or not list(diffs_dir.iterdir()):
        console.print("[red]No diffs found in run directory.[/red]")
        raise SystemExit(1)

    diff_files = list(diffs_dir.glob("*.json"))
    console.print(f"[green]Apply diffs: {len(diff_files)} proposals[/green]")
    console.print(f"  Mode: {mode}")
    console.print(f"  Skills dir: {skills_path}")


@cli.command()
@click.option("--run-a", required=True, help="First run directory")
@click.option("--run-b", required=True, help="Second run directory")
@click.pass_context
def compare(ctx, run_a, run_b):
    """Compare scores between two eval runs."""
    path_a = Path(run_a)
    path_b = Path(run_b)

    if not path_a.exists() or not path_b.exists():
        console.print("[red]One or both run directories not found.[/red]")
        raise SystemExit(1)

    console.print(f"[green]Comparing:[/green]")
    console.print(f"  Run A: {path_a.name}")
    console.print(f"  Run B: {path_b.name}")


@cli.command()
@click.option("--template", "-t", help="Filter by template name")
@click.option("--model", "-m", help="Filter by model name")
@click.option("--limit", "-n", type=int, default=10, help="Number of runs to show")
@click.pass_context
def history(ctx, template, model, limit):
    """List past eval runs with scores."""
    config: EvalConfig = ctx.obj["config"]
    rm = RunManager(config.paths.runs)
    runs = rm.list_runs(limit=limit)

    if not runs:
        console.print("[yellow]No runs found.[/yellow]")
        return

    table = Table(title="Eval Run History")
    table.add_column("Run ID", style="cyan")
    table.add_column("Models")
    table.add_column("Templates", justify="right")
    table.add_column("Judge")
    table.add_column("Parent")

    for run_id, config in runs:
        table.add_row(
            run_id,
            ", ".join(config.models),
            str(len(config.templates)),
            config.judge_model[:30],
            config.parent_run or "—",
        )

    console.print(table)


@cli.command()
@click.option("--template", "-t", default="all", help="Template name(s) or 'all' (processes in catalogue order)")
@click.option("--model", "-m", default="all", help="Model name(s) or 'all'")
@click.option("--target-score", type=float, default=8.0, help="Target average action score")
@click.option("--max-iterations", type=int, default=3, help="Max improvement cycles per template")
@click.option("--skills-dir", required=True, help="Path to skills directory to update")
@click.pass_context
def improve(ctx, template, model, target_score, max_iterations, skills_dir):
    """Continuous improvement loop — eval, extract patterns, update skills, re-run."""
    import asyncio
    from eval_core.continuous import ContinuousImprover

    config: EvalConfig = ctx.obj["config"]
    models_dict = get_enabled_models(config, names=model)

    if not models_dict:
        console.print("[red]No models matched.[/red]")
        raise SystemExit(1)

    # Resolve templates in catalogue order
    gold_dir = Path(config.paths.gold_standards)
    if template == "all":
        templates = sorted([
            d.name for d in gold_dir.iterdir()
            if d.is_dir() and d.name.startswith("template-")
            and (d / "requirements.md").exists()
        ])
    else:
        templates = [t.strip() for t in template.split(",")]

    def progress(model_name, tmpl, action, status):
        console.print(f"  [{model_name}] {tmpl} > {action}: {status}")

    improver = ContinuousImprover(
        config=config,
        skills_dir=Path(skills_dir),
        aws_profile="Tebogo-dev",
        on_progress=progress,
    )

    async def run_loop():
        for tmpl in templates:
            console.print(f"\n[bold green]{'='*60}[/bold green]")
            console.print(f"[bold green]IMPROVING: {tmpl}[/bold green]")
            console.print(f"[bold green]Target: {target_score}/10 avg | Max iterations: {max_iterations}[/bold green]")
            console.print(f"[bold green]{'='*60}[/bold green]\n")

            result = await improver.improve(
                template=tmpl,
                models=list(models_dict.keys()),
                target_score=target_score,
                max_iterations=max_iterations,
            )

            console.print(f"\n[bold]{'='*60}[/bold]")
            console.print(f"[bold]RESULT: {tmpl}[/bold]")
            console.print(f"  Iterations: {result['iterations']}")
            console.print(f"  Target met: {result['target_met']}")
            console.print(f"  Skill changes applied: {len(result['skill_changes'])}")
            for sc in result['skill_changes']:
                console.print(f"    - {sc['skill']}: {sc['changes']} changes (iter {sc['iteration']})")
            console.print(f"  Final scores:")
            for m, scores in result['final_scores'].items():
                console.print(f"    {m}: {scores['total']:.1f} (avg {scores['average']:.1f})")
            console.print(f"[bold]{'='*60}[/bold]\n")

    asyncio.run(run_loop())


def _show_dry_run(models, templates, template_actions, stage):
    """Display what would be executed without running."""
    console.print("\n[cyan]DRY RUN — no API calls will be made[/cyan]\n")

    table = Table(title="Eval Plan")
    table.add_column("Template")
    table.add_column("Actions")
    table.add_column("Models")

    for t in templates:
        seq = template_actions.get(t)
        action_count = len(seq.actions) if seq else 0
        table.add_row(t, str(action_count), ", ".join(models.keys()))

    console.print(table)

    total_actions = sum(len(seq.actions) for seq in template_actions.values())
    total_invocations = total_actions * len(models)
    console.print(f"\nTotal actions: {total_actions}")
    console.print(f"Total model invocations: {total_invocations}")
    console.print(f"Stage filter: {stage}")


if __name__ == "__main__":
    cli()
