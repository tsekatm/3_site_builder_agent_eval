"""Per-action evaluation model — parses requirements into discrete scored actions."""

from __future__ import annotations

import re
from pathlib import Path

from eval_core.types import ActionSequence, EvalAction

# Maps requirements.md section headers to action definitions
SECTION_TO_ACTION: dict[str, dict] = {
    "Colours": {
        "name": "apply-colours",
        "skill": "colour_management",
        "category": "colours",
    },
    "Typography": {
        "name": "swap-fonts",
        "skill": "global_font_management",
        "category": "fonts",
    },
    "Font Pairing": {
        "name": "swap-fonts",
        "skill": "global_font_management",
        "category": "fonts",
    },
    "Header Logo": {
        "name": "replace-header-logo",
        "skill": "logo_replacement",
        "category": "logos",
    },
    "Footer Logo": {
        "name": "replace-footer-logo",
        "skill": "logo_replacement",
        "category": "logos",
    },
    "Favicon": {
        "name": "replace-favicon",
        "skill": "logo_replacement",
        "category": "logos",
    },
    "Hero Background": {
        "name": "replace-hero-bg",
        "skill": "background_image_changer",
        "category": "images",
    },
    "Section Backgrounds": {
        "name": "replace-section-bgs",
        "skill": "background_image_changer",
        "category": "images",
    },
    "Hero Section": {
        "name": "update-hero-text",
        "skill": "template_customization",
        "category": "text",
    },
    "About Section": {
        "name": "update-about-text",
        "skill": "template_customization",
        "category": "text",
    },
    "Contact": {
        "name": "update-contact",
        "skill": "template_customization",
        "category": "text",
    },
    "Hero Layout": {
        "name": "apply-hero-layout",
        "skill": "layout_transformation",
        "category": "layout",
    },
    "Sections Layout": {
        "name": "apply-sections-layout",
        "skill": "layout_transformation",
        "category": "layout",
    },
    "Meta Tags": {
        "name": "add-seo-meta",
        "skill": "template_customization",
        "category": "seo",
    },
    "Structured Data": {
        "name": "add-structured-data",
        "skill": "template_customization",
        "category": "seo",
    },
    "Navigation": {
        "name": "add-accessibility",
        "skill": "cross-cutting",
        "category": "accessibility",
    },
    "Colour Contrast": {
        "name": "verify-contrast",
        "skill": "cross-cutting",
        "category": "accessibility",
    },
    "Interactivity": {
        "name": "add-interactivity",
        "skill": "template_customization",
        "category": "interactivity",
    },
}


def parse_requirements_to_actions(
    template: str,
    requirements_path: Path,
) -> ActionSequence:
    """Parse a requirements.md file into an ordered list of eval actions."""
    content = requirements_path.read_text()
    actions: list[EvalAction] = []
    action_id = 1
    seen_names: set[str] = set()

    for section_name, action_def in SECTION_TO_ACTION.items():
        # Skip duplicate action names (e.g., Typography and Font Pairing both map to swap-fonts)
        if action_def["name"] in seen_names:
            continue

        # Search for the section in requirements
        pattern = rf"### {re.escape(section_name)}\n(.*?)(?=\n### |\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match and match.group(1).strip():
            section_content = match.group(1).strip()
            expected = _extract_expected_changes(section_content)

            actions.append(
                EvalAction(
                    id=action_id,
                    name=action_def["name"],
                    skill=action_def["skill"],
                    category=action_def["category"],
                    description=section_content,
                    requirements_section=section_name,
                    expected_changes=expected,
                )
            )
            action_id += 1
            seen_names.add(action_def["name"])

    return ActionSequence(template=template, actions=actions)


def _extract_expected_changes(section_content: str) -> list[str]:
    """Extract bullet-point expected changes from a section."""
    changes: list[str] = []
    for line in section_content.split("\n"):
        line = line.strip()
        if line.startswith("- **"):
            # Extract key: value pairs
            match = re.match(r"- \*\*(.+?)\*\*:\s*(.+)", line)
            if match:
                changes.append(f"{match.group(1)}: {match.group(2)}")
    return changes
