"""Eval orchestrator — runs the full per-action evaluation pipeline.

For each template, for each model:
1. Copy template skeleton to run directory (baseline)
2. Screenshot baseline
3. For each action:
   a. Send action instruction to model
   b. Write modified files to action directory
   c. Screenshot the rendered site
   d. Compare screenshot vs gold standard (SSIM)
   e. Judge evaluates: before/after + code diff
   f. Record ActionScore
4. Assemble final site from last action output
5. Aggregate stage scores
6. Generate report
"""

from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path
from typing import Optional, Callable

from eval_core.actions import parse_requirements_to_actions, EvalAction
from eval_core.config import EvalConfig, ModelConfig
from eval_core.folder_compare.tree_diff import FolderComparer
from eval_core.folder_compare.content_diff import ContentComparer
from eval_core.judges.opus_judge import OpusJudge
from eval_core.runners.bedrock import BedrockRunner, create_runner
from eval_core.scoring.scorer import score_action, score_stage, score_template
from eval_core.scoring.violations import ViolationCatalogue
from eval_core.types import (
    ActionScore, StageScore, TemplateResult, Violation, Severity, RunnerResponse,
)
from eval_core.versioning.run_manager import RunManager


# Prompt template for agent model
AGENT_PROMPT = """You are a site builder agent. Apply the following modification to the website files.

## Action: {action_name}
## Skill: {skill}

## Requirements
{description}

## Current index.html
```html
{current_html}
```

## Current css/styles.css
```css
{current_css}
```

## Instructions
Apply ONLY the changes described above. Return your response in this EXACT format:

===HTML===
(the complete modified index.html)
===CSS===
(the complete modified css/styles.css)
===END===

Return the COMPLETE files, not just the changes. Do not add any explanation."""


def _parse_agent_response(response: str, current_html: str, current_css: str) -> tuple[str, str]:
    """Parse agent response into HTML and CSS. Falls back to current files on failure."""
    html = current_html
    css = current_css

    if "===HTML===" in response and "===CSS===" in response:
        parts = response.split("===CSS===")
        html_part = parts[0].split("===HTML===")[-1].strip()
        css_part = parts[-1].split("===END===")[0].strip() if "===END===" in parts[-1] else parts[-1].strip()

        # Strip markdown code fences if present
        for fence in ["```html", "```css", "```"]:
            html_part = html_part.replace(fence, "")
            css_part = css_part.replace(fence, "")

        if html_part.strip():
            html = html_part.strip()
        if css_part.strip():
            css = css_part.strip()
    elif "<html" in response.lower() or "<!doctype" in response.lower():
        # Agent returned just HTML
        html = response.strip()
        for fence in ["```html", "```"]:
            html = html.replace(fence, "")
        html = html.strip()
    elif ":root" in response or "--primary" in response:
        # Agent returned just CSS
        css = response.strip()
        for fence in ["```css", "```"]:
            css = css.replace(fence, "")
        css = css.strip()

    return html, css


async def run_eval_for_template(
    template_name: str,
    model_name: str,
    model_config: ModelConfig,
    judge_config: ModelConfig,
    config: EvalConfig,
    run_dir: Path,
    aws_profile: Optional[str] = None,
    on_progress: Optional[Callable] = None,
    capture_screenshots: bool = True,
) -> TemplateResult:
    """Run full per-action evaluation for one template with one model.

    Args:
        template_name: e.g., "template-ai-page-builder"
        model_name: e.g., "deepseek-v3.2"
        model_config: Model configuration
        judge_config: Judge model configuration
        config: Full eval config
        run_dir: Run output directory
        aws_profile: AWS SSO profile name
        on_progress: Callback(model, template, action, status)
        capture_screenshots: Whether to capture Playwright screenshots

    Returns:
        TemplateResult with per-action scores
    """
    gold_dir = Path(config.paths.gold_standards) / template_name / "stage-2-site-generation"
    templates_base = Path(config.paths.templates)

    # Find the template skeleton
    template_skeleton = _find_template_skeleton(template_name, templates_base)
    if not template_skeleton:
        return _error_result(template_name, model_name, "Template skeleton not found")

    # Parse requirements into actions
    req_path = Path(config.paths.gold_standards) / template_name / "requirements.md"
    if not req_path.exists():
        return _error_result(template_name, model_name, "requirements.md not found")

    action_seq = parse_requirements_to_actions(template_name, req_path)
    if not action_seq.actions:
        return _error_result(template_name, model_name, "No actions parsed from requirements")

    # Create model output directory
    model_dir = run_dir / template_name / model_name
    model_dir.mkdir(parents=True, exist_ok=True)

    # Copy template skeleton as baseline (action 0)
    baseline_dir = model_dir / "actions" / "00_baseline"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    _copy_template_skeleton(template_skeleton, baseline_dir)

    # Read baseline files
    current_html = (baseline_dir / "index.html").read_text() if (baseline_dir / "index.html").exists() else ""
    current_css = ""
    for css_path in baseline_dir.rglob("*.css"):
        current_css = css_path.read_text()
        break

    # Screenshot baseline
    if capture_screenshots and (baseline_dir / "index.html").exists():
        await _capture_screenshot(baseline_dir / "index.html", baseline_dir / "screenshot.png")

    # Read gold standard
    gold_html = (gold_dir / "index.html").read_text() if (gold_dir / "index.html").exists() else ""
    gold_css = ""
    for css_path in gold_dir.rglob("*.css"):
        gold_css = css_path.read_text()
        break

    # Create runners
    agent_runner = create_runner(model_name, model_config, aws_profile)
    judge_runner = create_runner("judge", judge_config, aws_profile)
    catalogue = ViolationCatalogue(Path(config.paths.violations))
    judge = OpusJudge(runner=judge_runner, violation_catalogue_yaml=catalogue.as_yaml_string())

    # Run each action sequentially
    action_scores: list[ActionScore] = []

    for action in action_seq.actions:
        if on_progress:
            on_progress(model_name, template_name, action.name, "running")

        action_dir = model_dir / "actions" / f"{action.id:02d}_{action.name}"
        action_dir.mkdir(parents=True, exist_ok=True)

        # Send action to agent model
        prompt = AGENT_PROMPT.format(
            action_name=action.name,
            skill=action.skill,
            description=action.description,
            current_html=current_html[:30000],
            current_css=current_css[:15000],
        )

        response = await agent_runner.invoke(prompt)

        if response.error:
            # Agent failed — record critical violation
            action_scores.append(score_action(
                action.id, action.name, action.skill, action.category,
                violations=[Violation(
                    id="STRUCT-MISSING-INDEX",
                    category="structural",
                    severity=Severity.CRITICAL,
                    deduction=-3.0,
                    description=f"Agent invocation failed: {response.error}",
                )],
            ))
            continue

        # Parse agent response into HTML + CSS
        new_html, new_css = _parse_agent_response(response.output, current_html, current_css)

        # Write output files
        (action_dir / "index.html").write_text(new_html)
        css_dir = action_dir / "css"
        css_dir.mkdir(exist_ok=True)
        (css_dir / "styles.css").write_text(new_css)

        # Save raw response for debugging
        (action_dir / "raw_response.txt").write_text(response.output)
        (action_dir / "meta.json").write_text(json.dumps({
            "model": model_name,
            "action": action.name,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "latency_ms": response.latency_ms,
        }, indent=2))

        # Screenshot
        screenshot_path = action_dir / "screenshot.png"
        if capture_screenshots and (action_dir / "index.html").exists():
            await _capture_screenshot(action_dir / "index.html", screenshot_path)

        # SSIM comparison (if gold screenshot exists)
        ssim_score = 0.0
        ssim_violations: list[Violation] = []
        # Gold screenshots would be at gold-standards/template/screenshots/NN_action.png
        # For now, compare against gold final if no per-action gold screenshots exist
        # TODO: Add per-action gold screenshots

        # Automated checks
        auto_violations: list[Violation] = []
        content_comparer = ContentComparer(
            gold_dir / "index.html",
            action_dir / "index.html",
        )
        auto_violations.extend(content_comparer.compare())

        # Judge evaluation
        judge_violations = await judge.evaluate_action(
            action_name=action.name,
            skill=action.skill,
            category=action.category,
            action_description=action.description,
            expected_changes=action.expected_changes,
            gold_html=gold_html,
            gold_css=gold_css,
            agent_html=new_html,
            agent_css=new_css,
        )

        # Combine all violations (dedup by id)
        all_violations = auto_violations + judge_violations + ssim_violations
        seen_ids: set[str] = set()
        deduped: list[Violation] = []
        for v in all_violations:
            key = f"{v.id}:{v.description[:50]}"
            if key not in seen_ids:
                seen_ids.add(key)
                deduped.append(v)

        # Score this action
        action_result = score_action(
            action.id, action.name, action.skill, action.category,
            violations=deduped,
            ssim_score=ssim_score,
            screenshot_gold="",
            screenshot_agent=str(screenshot_path) if screenshot_path.exists() else "",
        )
        action_scores.append(action_result)

        # Save action score
        (action_dir / "score.json").write_text(
            json.dumps(action_result.model_dump(), indent=2, default=str)
        )

        # Update current state for next action
        current_html = new_html
        current_css = new_css

        if on_progress:
            on_progress(model_name, template_name, action.name,
                        f"done ({action_result.final_score:.1f}/10)")

    # Write final state
    final_dir = model_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    (final_dir / "index.html").write_text(current_html)
    css_final = final_dir / "css"
    css_final.mkdir(exist_ok=True)
    (css_final / "styles.css").write_text(current_css)

    if capture_screenshots and (final_dir / "index.html").exists():
        await _capture_screenshot(final_dir / "index.html", final_dir / "screenshot.png")

    # Aggregate into stage score
    stage = score_stage(stage=2, stage_name="site-generation", action_scores=action_scores)

    # Build template result
    result = score_template(template_name, model_name, [stage])

    # Save aggregated scores
    (model_dir / "scores.json").write_text(
        json.dumps(result.model_dump(), indent=2, default=str)
    )

    return result


def _find_template_skeleton(template_name: str, templates_base: Path) -> Optional[Path]:
    """Map template-name to bigbeard-templates path."""
    TEMPLATE_MAP = {
        "template-ai-page-builder": "technology/ai-page-builder",
        "template-saas-product": "technology/saas-product",
        "template-digital-agency": "marketing/digital-agency",
        "template-safari-lodge": "hospitality/safari-lodge",
        "template-solar-provider": "energy/solar-provider",
        "template-industrial-company": "manufacturing/industrial-company",
        "template-creative-factory": "manufacturing/creative-factory",
        "template-association-corporate": "healthcare/association-corporate",
        "template-association-gala-event": "healthcare/association-gala-event",
        "template-association-newsletter": "healthcare/association-newsletter",
        "template-association-policy": "healthcare/association-policy",
        "template-investment-company": "finance/investment-company",
        "template-community-trust-1": "nonprofit/community-trust-1",
        "template-community-trust-2": "nonprofit/community-trust-2",
        "template-community-trust-3": "nonprofit/community-trust-3",
        "template-skills-training-blog-1": "education/skills-training-blog-1",
        "template-skills-training-blog-2": "education/skills-training-blog-2",
        "template-skills-training-corporate": "education/skills-training-corporate",
        "template-skills-training-landing": "education/skills-training-landing",
        "template-blank-site": "blank/blank-site",
        "template-hasa-crmp": "healthcare/hasa-crmp",
    }
    rel_path = TEMPLATE_MAP.get(template_name)
    if not rel_path:
        return None
    full_path = templates_base / rel_path
    return full_path if full_path.exists() else None


def _copy_template_skeleton(src: Path, dst: Path) -> None:
    """Copy template skeleton files to destination."""
    for src_file in src.rglob("*"):
        if src_file.is_file() and src_file.name not in ("preview.html", "preview.png", "metadata.json", "template-config.json"):
            rel = src_file.relative_to(src)
            dst_file = dst / rel
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)


async def _capture_screenshot(html_path: Path, output_path: Path) -> bool:
    """Capture screenshot, return True on success."""
    try:
        from eval_core.visual.screenshot import capture_screenshot
        await capture_screenshot(html_path, output_path)
        return True
    except Exception as e:
        # Screenshot capture is best-effort — don't fail the eval
        print(f"    [warn] Screenshot failed: {e}")
        return False


def _error_result(template: str, model: str, error: str) -> TemplateResult:
    """Create an error TemplateResult."""
    v = Violation(
        id="EVAL-ERROR", category="structural", severity=Severity.CRITICAL,
        deduction=-10.0, description=error,
    )
    action = score_action(0, "error", "error", "error", violations=[v])
    stage = score_stage(0, "error", [action])
    return score_template(template, model, [stage])
