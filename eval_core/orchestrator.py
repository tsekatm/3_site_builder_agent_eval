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
from eval_core.visual.html_visual_checker import HTMLVisualChecker
from eval_core.judges.opus_judge import OpusJudge
from eval_core.judges.visual_judge import VisualJudge
from eval_core.runners.bedrock import BedrockRunner, create_runner
from eval_core.runners.anthropic_direct import AnthropicDirectRunner, create_direct_runner
from eval_core.runners.claude_code import ClaudeCodeRunner, create_claude_code_runner
from eval_core.runners.openrouter import OpenRouterRunner, create_openrouter_runner
from eval_core.scoring.scorer import score_action, score_stage, score_template
from eval_core.scoring.violations import ViolationCatalogue
from eval_core.types import (
    ActionScore, StageScore, TemplateResult, Violation, Severity, RunnerResponse,
)
from eval_core.routing import ModelRouter
from eval_core.versioning.run_manager import RunManager


def _create_runner_auto(name: str, config: ModelConfig, aws_profile: str = None, api_key: str = None):
    """Create the appropriate runner based on config."""
    if config.provider == "claude-code":
        return create_claude_code_runner(name, config)
    elif config.provider == "anthropic-direct":
        return create_direct_runner(name, config, api_key=api_key)
    elif config.provider == "openrouter":
        return create_openrouter_runner(name, config)
    else:
        return create_runner(name, config, aws_profile=aws_profile)


INLINE_TEACHER_PROMPT = """You are a prompt engineering expert. An agent just scored poorly on a site customisation action.

## Action that failed: {action_name}
## Score: {score}/10
## Violations found:
{violations}

## Current agent prompt instructions:
{current_instructions}

## Agent's output (excerpt):
{agent_output_excerpt}

## Task
Analyse WHY the agent failed and provide IMPROVED INSTRUCTIONS that would prevent these violations. Return ONLY the improved instruction text — no explanation, no JSON, no markdown blocks. The instruction should be 2-3 sentences that are specific and actionable."""


# Prompt template for agent model
AGENT_PROMPT = """You are a site builder agent customising a website template for a client.

## Business Context
{business_context}

## Action: {action_name}
## Skill: {skill}

## Requirements for this action
{description}

## Current index.html
```html
{current_html}
```

## Current css/styles.css
```css
{current_css}
```

## CRITICAL RULES
1. Apply the changes described in the requirements above
2. For ALL images (hero backgrounds, section backgrounds, logos, icons, gallery):
   - Use Unsplash for photos: https://images.unsplash.com/photo-ID?w=WIDTH&h=HEIGHT&fit=crop
   - Use Iconify for icons/logos: https://api.iconify.design/mdi/ICON-NAME.svg?color=%23HEX&width=W&height=H
   - Choose images that match the business industry
3. TEXT CONTRAST ON DARK BACKGROUNDS IS CRITICAL:
   - Any section with a background image MUST have a dark overlay (rgba(0,0,0,0.6) minimum)
   - Text on dark backgrounds or background images MUST be white (#FFFFFF) or very light
   - NEVER use dark text colours (brown, black, dark grey) on sections with background images
   - Hero sections, CTA sections, and any section with background-image need --text-secondary (#FFFFFF) not --text-color
   - NEVER use local file paths like images/logo.png or assets/images/
4. Replace ALL {{PLACEHOLDER}} tokens with actual business content
5. Keep the template structure intact — modify content and styling, don't restructure HTML
6. Return COMPLETE files, not fragments

## LAYOUT RULES (apply when modifying layout or structure)
- Hero section: Use full-viewport height with background image, dark overlay, and centered white text. Keep hero simple — headline, subtitle, description, feature pills, optional CTA button. No cards or complex layouts inside the hero.
- Features/services section: Use CSS Grid (repeat(3, 1fr) on desktop). Each card has icon + heading + description. Responsive: 2 columns at 1024px, 1 column at 768px.
- Alternating rows: Use flexbox with row/row-reverse. Image on one side, text on the other. Stack vertically on mobile.
- Footer: 4-column grid (1.5fr repeat(3, 1fr)). Columns: brand/tagline, navigation links, hours/info, contact details. Stack on mobile.
- ALL grids must have responsive breakpoints at 1024px and 768px.
- Use CSS variables for spacing (gap, padding), not hardcoded pixel values.

## CONTACT SECTION RULES
- Create a dedicated contact section with individual cards per location
- Each card: address, phone (wrapped in tel: link), hours
- Add a separate email card with mailto: link
- CTA button should link to phone (tel:) not email
- Footer contact column must mirror the contact section data
- Add JSON-LD structured data (LocalBusiness/Restaurant/Organization) with address, phone, email

## CONTENT REPLACEMENT RULES
- Copy text EXACTLY from the requirements — do not paraphrase, summarise, or reword
- Feature card titles and descriptions must match requirements word-for-word
- Hero headline, subtitle, and description must be exact matches
- Business name must appear consistently in header, footer, meta title, JSON-LD
- Contact details (phone, email, address) must be identical everywhere they appear

## Response Format
Return your response in this EXACT format (no markdown, no explanation):

===HTML===
(the complete modified index.html)
===CSS===
(the complete modified css/styles.css)
===END==="""


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
    api_key: Optional[str] = None,
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

    # Extract business context from requirements (first few sections)
    req_content = req_path.read_text()
    business_context = _extract_business_context(req_content)

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

    # Create runners (auto-detect: direct API for Claude, Bedrock for others)
    agent_runner = _create_runner_auto(model_name, model_config, aws_profile, api_key)
    judge_runner = _create_runner_auto("judge", judge_config, aws_profile, api_key)

    # Multi-model router (if model_name is "routed", use per-action routing)
    router = None
    if model_name == "routed":
        router = ModelRouter(models=config.models)
    catalogue = ViolationCatalogue(Path(config.paths.violations))
    judge = OpusJudge(runner=judge_runner, violation_catalogue_yaml=catalogue.as_yaml_string())

    # Create visual judge (uses OpenRouter with vision)
    import os
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    visual_judge = VisualJudge(api_key=openrouter_key) if openrouter_key else None

    # Read requirements summary for visual judge
    req_summary = ""
    if req_path.exists():
        req_text = req_path.read_text()
        # Extract business profile + brand section for visual context
        for section in ["Business Profile", "Brand Amendments", "Hero Section"]:
            import re as _re
            match = _re.search(rf"## {section}\n(.*?)(?=\n## |\Z)", req_text, _re.DOTALL)
            if match:
                req_summary += f"\n{section}:\n{match.group(1).strip()}\n"

    # Run each action sequentially
    action_scores: list[ActionScore] = []
    learned_instructions: dict[str, str] = {}  # category → improved instructions
    inline_teacher_threshold = 7.0  # Score below this triggers inline teacher

    for action in action_seq.actions:
        if on_progress:
            on_progress(model_name, template_name, action.name, "running")

        action_dir = model_dir / "actions" / f"{action.id:02d}_{action.name}"
        action_dir.mkdir(parents=True, exist_ok=True)

        # Build prompt with any learned instructions for this category
        extra_instructions = learned_instructions.get(action.category, "")
        prompt = AGENT_PROMPT.format(
            business_context=business_context,
            action_name=action.name,
            skill=action.skill,
            description=action.description,
            current_html=current_html[:30000],
            current_css=current_css[:15000],
        )
        if extra_instructions:
            prompt += f"\n\n## IMPORTANT — Learned from previous actions\n{extra_instructions}"

        # Route to optimal model per action (if router enabled)
        current_runner = agent_runner
        if router:
            routed_model_name, routed_config = router.get_model_for_action(action.name)
            current_runner = _create_runner_auto(routed_model_name, routed_config, aws_profile, api_key)
            if on_progress:
                on_progress(routed_model_name, template_name, action.name,
                            f"routed to {routed_model_name}")

        response = await current_runner.invoke(prompt)

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

        # Visual checks (catches broken images, empty sections, contrast, broken nav, missing JS)
        css_path = action_dir / "css" / "styles.css"
        visual_checker = HTMLVisualChecker(action_dir / "index.html", css_path if css_path.exists() else None)
        auto_violations.extend(visual_checker.check_all())

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

        # Visual judge (screenshot comparison via OpenRouter vision)
        visual_judge_violations: list[Violation] = []
        if visual_judge and capture_screenshots and screenshot_path.exists():
            gold_screenshot = gold_dir / "screenshots" / f"{action.id:02d}_{action.name}.png"
            if not gold_screenshot.exists():
                # Fall back to gold final screenshot
                gold_screenshot = gold_dir / "screenshots" / "final.png"
            # Use the gold standard HTML screenshot as reference if no dedicated screenshot
            if not gold_screenshot.exists() and (baseline_dir / "screenshot.png").exists():
                gold_screenshot = baseline_dir / "screenshot.png"

            if gold_screenshot.exists():
                vj_violations, vj_score = await visual_judge.evaluate(
                    gold_screenshot=gold_screenshot,
                    agent_screenshot=screenshot_path,
                    action_name=action.name,
                    action_description=action.description[:300],
                    requirements_summary=req_summary,
                )
                visual_judge_violations = vj_violations
                ssim_score = vj_score / 10.0  # Normalize to 0-1

                if on_progress and vj_violations:
                    on_progress(model_name, template_name, action.name,
                                f"visual judge: {len(vj_violations)} issues (score {vj_score:.0f}/10)")

        # Combine all violations (dedup by id)
        all_violations = auto_violations + judge_violations + ssim_violations + visual_judge_violations
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

        # --- INLINE TEACHER (Option C: refine prompt automatically) ---
        if action_result.final_score < inline_teacher_threshold and judge_runner:
            if on_progress:
                on_progress(model_name, template_name, action.name,
                            f"score {action_result.final_score:.1f} < {inline_teacher_threshold} — teacher refining prompt")

            violations_text = "\n".join(
                f"  [{v.severity.value}] {v.id}: {v.description} ({v.deduction})"
                for v in deduped
            )
            teacher_prompt = INLINE_TEACHER_PROMPT.format(
                action_name=action.name,
                score=f"{action_result.final_score:.1f}",
                violations=violations_text,
                current_instructions=action.description[:2000],
                agent_output_excerpt=response.output[:2000],
            )

            teacher_response = await judge_runner.invoke(
                teacher_prompt,
                system_prompt="You are a prompt engineering expert. Return only the improved instruction text.",
            )

            if teacher_response.output and not teacher_response.error:
                improved = teacher_response.output.strip()
                # Store learned instruction for this category
                existing = learned_instructions.get(action.category, "")
                learned_instructions[action.category] = (
                    f"{existing}\n{improved}" if existing else improved
                )

                # Save teacher output for debugging
                (action_dir / "teacher_refinement.txt").write_text(
                    f"Score: {action_result.final_score}\n"
                    f"Category: {action.category}\n"
                    f"Learned instruction:\n{improved}"
                )

                if on_progress:
                    on_progress(model_name, template_name, action.name,
                                f"teacher refined prompt for category '{action.category}'")

                # RETRY the action with improved prompt
                retry_prompt = AGENT_PROMPT.format(
                    business_context=business_context,
                    action_name=action.name,
                    skill=action.skill,
                    description=action.description,
                    current_html=current_html[:30000],
                    current_css=current_css[:15000],
                ) + f"\n\n## IMPORTANT — Learned from previous attempt\n{improved}"

                retry_response = await agent_runner.invoke(retry_prompt)

                if not retry_response.error:
                    retry_html, retry_css = _parse_agent_response(
                        retry_response.output, current_html, current_css
                    )

                    # Re-judge the retry
                    retry_judge_violations = await judge.evaluate_action(
                        action.name, action.skill, action.category,
                        action.description, action.expected_changes,
                        gold_html, gold_css, retry_html, retry_css,
                    )

                    retry_auto = ContentComparer(
                        gold_dir / "index.html", action_dir / "index.html",
                    ).compare()

                    retry_all = retry_auto + retry_judge_violations
                    retry_deduped: list[Violation] = []
                    retry_seen: set[str] = set()
                    for v in retry_all:
                        key = f"{v.id}:{v.description[:50]}"
                        if key not in retry_seen:
                            retry_seen.add(key)
                            retry_deduped.append(v)

                    retry_result = score_action(
                        action.id, action.name, action.skill, action.category,
                        violations=retry_deduped,
                        ssim_score=ssim_score,
                    )

                    # Keep the better score
                    if retry_result.final_score > action_result.final_score:
                        if on_progress:
                            on_progress(model_name, template_name, action.name,
                                        f"retry improved: {action_result.final_score:.1f} → {retry_result.final_score:.1f}")
                        action_result = retry_result
                        new_html, new_css = retry_html, retry_css

                        # Update output files with retry
                        (action_dir / "index.html").write_text(new_html)
                        (action_dir / "css" / "styles.css").write_text(new_css)
                        (action_dir / "raw_response_retry.txt").write_text(retry_response.output)

                        # Re-screenshot
                        if capture_screenshots:
                            await _capture_screenshot(action_dir / "index.html", screenshot_path)
                    else:
                        if on_progress:
                            on_progress(model_name, template_name, action.name,
                                        f"retry didn't improve: {retry_result.final_score:.1f} ≤ {action_result.final_score:.1f}")

        # --- END INLINE TEACHER ---

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


def _extract_business_context(requirements_text: str) -> str:
    """Extract business profile and key details from requirements for the agent prompt."""
    import re
    lines = []

    # Extract Business Profile section
    profile_match = re.search(
        r"## Business Profile\n(.*?)(?=\n## )", requirements_text, re.DOTALL
    )
    if profile_match:
        lines.append(profile_match.group(1).strip())

    # Extract Brand Amendments > Colours
    colours_match = re.search(
        r"### Colours\n(.*?)(?=\n### |\n## )", requirements_text, re.DOTALL
    )
    if colours_match:
        lines.append("\nBrand Colours:\n" + colours_match.group(1).strip())

    # Extract Hero Section
    hero_match = re.search(
        r"### Hero Section\n(.*?)(?=\n### |\n## )", requirements_text, re.DOTALL
    )
    if hero_match:
        lines.append("\nHero Content:\n" + hero_match.group(1).strip())

    # Extract Contact
    contact_match = re.search(
        r"### Contact\n(.*?)(?=\n## )", requirements_text, re.DOTALL
    )
    if contact_match:
        lines.append("\nContact:\n" + contact_match.group(1).strip())

    # Extract About
    about_match = re.search(
        r"### About Section\n(.*?)(?=\n### |\n## )", requirements_text, re.DOTALL
    )
    if about_match:
        lines.append("\nAbout:\n" + about_match.group(1).strip())

    return "\n".join(lines) if lines else "No business context available"


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
