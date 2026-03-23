"""Shared data structures for the eval pack."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MODERATE = "moderate"
    MINOR = "minor"


class Violation(BaseModel):
    id: str
    category: str
    severity: Severity
    deduction: float
    file: Optional[str] = None
    description: str
    evidence: Optional[str] = None
    recommendation: Optional[str] = None


class ActionScore(BaseModel):
    action_id: int
    action_name: str
    skill: str
    category: str
    base_score: float = 10.0
    violations: list[Violation] = Field(default_factory=list)
    total_deductions: float = 0.0
    final_score: float = 10.0
    screenshot_gold: str = ""
    screenshot_agent: str = ""
    ssim_score: float = 0.0


class StageScore(BaseModel):
    stage: int
    stage_name: str
    actions: list[ActionScore] = Field(default_factory=list)
    action_count: int = 0
    stage_total: float = 0.0
    average_score: float = 0.0


class TemplateResult(BaseModel):
    template: str
    model: str
    stages: list[StageScore] = Field(default_factory=list)
    template_total: float = 0.0


class EvalRunConfig(BaseModel):
    run_id: str
    models: list[str]
    templates: list[str]
    judge_model: str
    timestamp: str
    parent_run: Optional[str] = None


class RunnerResponse(BaseModel):
    model_id: str
    output: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    error: Optional[str] = None


class EvalAction(BaseModel):
    id: int
    name: str
    skill: str
    category: str
    description: str
    requirements_section: str
    expected_changes: list[str] = Field(default_factory=list)
    screenshot_before: Optional[str] = None
    screenshot_after: Optional[str] = None


class ActionSequence(BaseModel):
    template: str
    actions: list[EvalAction] = Field(default_factory=list)
