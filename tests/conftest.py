"""Shared fixtures for eval pack tests."""

import pytest
from pathlib import Path

from eval_core.config import EvalConfig, load_config
from eval_core.types import Violation, Severity


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def config(project_root) -> EvalConfig:
    return load_config(project_root / "eval_config.yaml")


@pytest.fixture
def violations_yaml_path(project_root) -> Path:
    return project_root / "eval_core" / "scoring" / "violations.yaml"


@pytest.fixture
def gold_standards_dir(project_root) -> Path:
    return project_root / "gold-standards"


@pytest.fixture
def sample_requirements(gold_standards_dir) -> Path:
    return gold_standards_dir / "template-ai-page-builder" / "requirements.md"


@pytest.fixture
def critical_violation() -> Violation:
    return Violation(
        id="STRUCT-MISSING-INDEX",
        category="structural",
        severity=Severity.CRITICAL,
        deduction=-3.0,
        file="index.html",
        description="Missing required file: index.html",
    )


@pytest.fixture
def minor_violation() -> Violation:
    return Violation(
        id="PERF-NO-FONT-DISPLAY",
        category="performance",
        severity=Severity.MINOR,
        deduction=-0.25,
        description="No font-display swap",
    )
