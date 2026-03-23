"""Scoring engine — 10 minus deductions, no floor (can go negative)."""

from __future__ import annotations

from eval_core.types import ActionScore, StageScore, TemplateResult, Violation


BASE_SCORE = 10.0


def score_action(
    action_id: int,
    action_name: str,
    skill: str,
    category: str,
    violations: list[Violation],
    ssim_score: float = 0.0,
    screenshot_gold: str = "",
    screenshot_agent: str = "",
) -> ActionScore:
    """Score a single action. 10 - deductions, NO FLOOR."""
    capped = _apply_caps(violations)
    total_deductions = sum(v.deduction for v in capped)
    final = BASE_SCORE + total_deductions  # deductions are negative

    return ActionScore(
        action_id=action_id,
        action_name=action_name,
        skill=skill,
        category=category,
        base_score=BASE_SCORE,
        violations=capped,
        total_deductions=total_deductions,
        final_score=final,
        screenshot_gold=screenshot_gold,
        screenshot_agent=screenshot_agent,
        ssim_score=ssim_score,
    )


def score_stage(
    stage: int,
    stage_name: str,
    action_scores: list[ActionScore],
) -> StageScore:
    """Aggregate action scores into a stage score."""
    count = len(action_scores)
    total = sum(a.final_score for a in action_scores)
    avg = total / count if count > 0 else 0.0

    return StageScore(
        stage=stage,
        stage_name=stage_name,
        actions=action_scores,
        action_count=count,
        stage_total=total,
        average_score=avg,
    )


def score_template(
    template: str,
    model: str,
    stages: list[StageScore],
) -> TemplateResult:
    """Aggregate stage scores into a template result."""
    return TemplateResult(
        template=template,
        model=model,
        stages=stages,
        template_total=sum(s.stage_total for s in stages),
    )


def _apply_caps(violations: list[Violation]) -> list[Violation]:
    """Apply max_deduction caps for violations that have per-type limits.

    E.g., CODE-INVALID-HTML has deduction=-0.5 per error but max_deduction=-2.0.
    If there are 10 HTML errors, total is capped at -2.0, not -5.0.
    """
    # Group by violation ID prefix
    from collections import defaultdict
    groups: dict[str, list[Violation]] = defaultdict(list)
    for v in violations:
        groups[v.id.split("-")[0] + "-" + v.id.split("-")[1] if "-" in v.id else v.id].append(v)

    # For now, return all violations as-is. Cap logic will use ViolationCatalogue
    # max_deduction when integrated. The judge already uses catalogue deduction amounts.
    return violations
