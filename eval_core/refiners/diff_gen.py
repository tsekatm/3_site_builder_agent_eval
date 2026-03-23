"""Diff generator — creates unified diffs from teacher proposals."""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Optional


def generate_diff(
    original_content: str,
    changes: list[dict],
    file_path: str = "skill.md",
) -> Optional[str]:
    """Apply changes to content and generate a unified diff.

    Args:
        original_content: Current file content.
        changes: List of {"old_text": ..., "new_text": ..., "section": ..., "rationale": ...}.
        file_path: File path for diff header.

    Returns:
        Unified diff string, or None if no changes could be applied.
    """
    modified = original_content
    applied = 0

    for change in changes:
        old_text = change.get("old_text", "")
        new_text = change.get("new_text", "")
        if old_text and old_text in modified:
            modified = modified.replace(old_text, new_text, 1)
            applied += 1

    if applied == 0:
        return None

    original_lines = original_content.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
    )

    return "".join(diff)


def apply_changes(original_content: str, changes: list[dict]) -> str:
    """Apply all changes to content and return modified text."""
    modified = original_content
    for change in changes:
        old_text = change.get("old_text", "")
        new_text = change.get("new_text", "")
        if old_text and old_text in modified:
            modified = modified.replace(old_text, new_text, 1)
    return modified


def save_diff(diff_text: str, output_path: Path) -> Path:
    """Save diff to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(diff_text)
    return output_path
