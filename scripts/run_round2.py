#!/usr/bin/env python3
"""Round 2 Evaluation Runner — fills gaps to reach 3 runs per model-template pair.

Usage:
    python3 scripts/run_round2.py                    # Run all gaps
    python3 scripts/run_round2.py --model kimi-k2.5  # Run one model only
    python3 scripts/run_round2.py --dry-run           # Show what would run
"""

import argparse
import asyncio
import json
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval_core.config import EvalConfig
from eval_core.orchestrator import run_eval_for_template


TEMPLATES = [
    "template-ai-page-builder",
    "template-safari-lodge",
    "template-association-corporate",
    "template-association-gala-event",
    "template-saas-product",
    "template-association-newsletter",
    "template-solar-provider",
    "template-digital-agency",
    "template-community-trust-1",
    "template-hasa-crmp",
]

MODELS = ["claude-sonnet", "claude-haiku", "kimi-k2.5", "deepseek-v3.2"]
TARGET_RUNS = 3


def count_existing_runs(runs_dir: Path) -> dict[tuple[str, str], int]:
    """Count completed runs per (model, template) pair."""
    counts = defaultdict(int)
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir() or not run_dir.name[0].isdigit():
            continue
        for template_dir in run_dir.iterdir():
            if not template_dir.is_dir():
                continue
            template = template_dir.name
            for model_dir in template_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                model = model_dir.name
                if (model_dir / "final").exists() or (model_dir / "scores.json").exists():
                    counts[(model, template)] += 1
    return counts


def build_run_queue(existing: dict, model_filter: str = None) -> list[tuple[str, str, int]]:
    """Build list of (model, template, needed_runs) tuples."""
    queue = []
    for model in MODELS:
        if model_filter and model != model_filter:
            continue
        for template in TEMPLATES:
            existing_count = existing.get((model, template), 0)
            needed = max(0, TARGET_RUNS - existing_count)
            if needed > 0:
                queue.append((model, template, needed))
    return queue


def print_matrix(existing: dict):
    """Print the current coverage matrix."""
    print(f"\n{'Template':<45} {'Sonnet':>8} {'Haiku':>8} {'Kimi':>8} {'DS-V3':>8}")
    print("-" * 85)
    total_done = 0
    total_needed = 0
    for t in TEMPLATES:
        cells = []
        for m in MODELS:
            count = existing.get((m, t), 0)
            needed = max(0, TARGET_RUNS - count)
            total_done += min(count, TARGET_RUNS)
            total_needed += needed
            if count >= TARGET_RUNS:
                cells.append(f"{count}/{TARGET_RUNS} done")
            else:
                cells.append(f"{count}/{TARGET_RUNS} +{needed}")
        print(f"{t:<45} {cells[0]:>8} {cells[1]:>8} {cells[2]:>8} {cells[3]:>8}")
    total_cells = len(MODELS) * len(TEMPLATES) * TARGET_RUNS
    print(f"\nTotal: {total_done}/{total_cells} done, {total_needed} runs needed")


def main():
    parser = argparse.ArgumentParser(description="Round 2 evaluation runner")
    parser.add_argument("--model", choices=MODELS, help="Run one model only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run")
    parser.add_argument("--template", help="Run one template only")
    args = parser.parse_args()

    runs_dir = Path("runs")
    existing = count_existing_runs(runs_dir)

    print("=== ROUND 2 EVALUATION ===")
    print_matrix(existing)

    queue = build_run_queue(existing, model_filter=args.model)

    if args.template:
        queue = [(m, t, n) for m, t, n in queue if t == args.template]

    total_runs = sum(n for _, _, n in queue)
    print(f"\nQueue: {total_runs} runs across {len(queue)} model-template pairs")

    if args.dry_run:
        print("\n[DRY RUN] Would execute:")
        for model, template, needed in queue:
            print(f"  {model} × {template} × {needed} runs")
        return

    if total_runs == 0:
        print("\nAll cells complete. Nothing to run.")
        return

    print(f"\nStarting {total_runs} runs...\n")

    config = EvalConfig.from_yaml("eval_config.yaml")

    for model, template, needed in queue:
        for run_num in range(needed):
            existing_count = existing.get((model, template), 0)
            run_label = f"[{model}] {template} (run {existing_count + run_num + 1}/{TARGET_RUNS})"
            print(f"{'='*70}")
            print(f"  {run_label}")
            print(f"{'='*70}")

            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                run_dir = runs_dir / timestamp / template / model

                model_config = config.models.get(model)
                if not model_config:
                    print(f"  SKIP: model '{model}' not found in eval_config.yaml")
                    continue

                judge_config = config.judges.get("default")
                start = time.monotonic()
                result = asyncio.run(run_eval_for_template(
                    template_name=template,
                    model_name=model,
                    model_config=model_config,
                    judge_config=judge_config,
                    config=config,
                    run_dir=run_dir,
                    aws_profile=config.aws.get("profile"),
                    capture_screenshots=False,
                ))
                elapsed = time.monotonic() - start

                if result:
                    score = result.template_total if hasattr(result, 'template_total') else "N/A"
                    print(f"  DONE: {score}/160 in {elapsed:.0f}s")
                else:
                    print(f"  DONE: completed in {elapsed:.0f}s")

            except Exception as e:
                print(f"  ERROR: {e}")
                continue

    # Final matrix
    print(f"\n{'='*70}")
    print("  ROUND 2 COMPLETE")
    print(f"{'='*70}")
    updated_existing = count_existing_runs(runs_dir)
    print_matrix(updated_existing)


if __name__ == "__main__":
    main()
