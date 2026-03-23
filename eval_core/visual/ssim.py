"""SSIM (Structural Similarity Index) comparison for screenshots."""

from __future__ import annotations

from pathlib import Path

from eval_core.types import Violation, Severity


def compare_ssim(gold_path: Path, agent_path: Path) -> tuple[float, list[Violation]]:
    """Compare two screenshots using SSIM.

    Args:
        gold_path: Path to gold standard screenshot.
        agent_path: Path to agent output screenshot.

    Returns:
        Tuple of (ssim_score, violations).
        SSIM score is 0.0 to 1.0 (1.0 = identical).
    """
    try:
        from skimage.metrics import structural_similarity
        from PIL import Image
        import numpy as np
    except ImportError:
        # If dependencies not installed, return neutral score with no violations
        return 1.0, []

    if not gold_path.exists() or not agent_path.exists():
        return 0.0, [Violation(
            id="VIS-LAYOUT-BROKEN",
            category="visual",
            severity=Severity.CRITICAL,
            deduction=-3.0,
            description=f"Screenshot missing: gold={gold_path.exists()}, agent={agent_path.exists()}",
        )]

    # Load and convert to grayscale
    gold_img = Image.open(gold_path).convert("L")
    agent_img = Image.open(agent_path).convert("L")

    # Resize agent to match gold if different dimensions
    if gold_img.size != agent_img.size:
        agent_img = agent_img.resize(gold_img.size, Image.Resampling.LANCZOS)

    gold_arr = np.array(gold_img)
    agent_arr = np.array(agent_img)

    # Compute SSIM
    score = structural_similarity(gold_arr, agent_arr)

    # Generate violations based on thresholds
    violations: list[Violation] = []

    if score < 0.7:
        violations.append(Violation(
            id="VIS-MAJOR-DEVIATION",
            category="visual",
            severity=Severity.MAJOR,
            deduction=-2.0,
            description=f"Significant visual deviation (SSIM={score:.3f} < 0.7)",
        ))
    elif score < 0.9:
        violations.append(Violation(
            id="VIS-MINOR-DEVIATION",
            category="visual",
            severity=Severity.MODERATE,
            deduction=-1.0,
            description=f"Minor visual deviation (SSIM={score:.3f}, range 0.7-0.9)",
        ))

    return score, violations
