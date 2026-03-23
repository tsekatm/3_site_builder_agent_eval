"""Diff applier — applies accepted changes to skill files."""

from __future__ import annotations

from pathlib import Path

from eval_core.refiners.diff_gen import apply_changes


def apply_to_file(skill_path: Path, changes: list[dict]) -> bool:
    """Apply changes to a skill file.

    Args:
        skill_path: Path to the skill .md file.
        changes: List of changes from teacher proposal.

    Returns:
        True if any changes were applied.
    """
    if not skill_path.exists():
        return False

    original = skill_path.read_text()
    modified = apply_changes(original, changes)

    if modified == original:
        return False

    skill_path.write_text(modified)
    return True


def interactive_apply(
    skill_path: Path,
    changes: list[dict],
    mode: str = "interactive",
) -> list[dict]:
    """Apply changes interactively or all at once.

    Args:
        skill_path: Path to skill file.
        changes: List of proposed changes.
        mode: "all" to apply everything, "interactive" for per-change prompts.

    Returns:
        List of accepted changes.
    """
    if mode == "all":
        apply_to_file(skill_path, changes)
        return changes

    accepted: list[dict] = []
    original = skill_path.read_text()

    for i, change in enumerate(changes):
        print(f"\n{'='*60}")
        print(f"Change {i+1}/{len(changes)} — {change.get('section', 'Unknown section')}")
        print(f"{'='*60}")
        print(f"\nRationale: {change.get('rationale', 'N/A')}")
        print(f"\n--- OLD ---")
        print(change.get("old_text", "")[:500])
        print(f"\n+++ NEW +++")
        print(change.get("new_text", "")[:500])
        print()

        while True:
            choice = input("[A]ccept / [R]eject / [S]kip / [Q]uit: ").strip().lower()
            if choice in ("a", "accept"):
                accepted.append(change)
                break
            elif choice in ("r", "reject"):
                break
            elif choice in ("s", "skip"):
                break
            elif choice in ("q", "quit"):
                # Apply what we've accepted so far
                if accepted:
                    apply_to_file(skill_path, accepted)
                return accepted

    if accepted:
        apply_to_file(skill_path, accepted)

    return accepted
