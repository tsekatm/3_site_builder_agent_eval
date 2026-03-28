"""Tests for DesignPromptBuilder."""

import pytest

from eval_core.figma.extractor import (
    DesignContext,
    Section,
    ColourPalette,
    TypographySystem,
)
from eval_core.figma.prompt_builder import DesignPromptBuilder


@pytest.fixture
def sample_context():
    """Build a minimal DesignContext for testing."""
    return DesignContext(
        file_name="Experience Madikwe",
        node_name="Home",
        node_id="1:864",
        dimensions={"width": 1920, "height": 4457},
        sections=[
            Section(
                name="Hero",
                semantic_role="hero",
                layout_description="full-width background image; text left-aligned with dark overlay",
                texts=[
                    {
                        "text": "Join Us for an Unforgettable African Safari Experience",
                        "font_family": "Marcellus",
                        "font_size": 64,
                        "font_weight": 400,
                        "text_colour": "#ffffff",
                        "text_align": "LEFT",
                    },
                ],
                images=[
                    {
                        "node_name": "hero-bg",
                        "temp_url": "https://figma-export.s3.amazonaws.com/hero.png",
                        "width": 1920,
                        "height": 926,
                        "parent_section": "Hero",
                    },
                ],
                background={"type": "image", "image": {
                    "temp_url": "https://figma-export.s3.amazonaws.com/hero.png",
                }},
                y_position=0,
                width=1920,
                height=926,
            ),
            Section(
                name="Lodges",
                semantic_role="grid",
                layout_description="3x3 image grid (9 items)",
                texts=[
                    {
                        "text": "Choosing a Lodge",
                        "font_family": "Marcellus",
                        "font_size": 40,
                        "font_weight": 400,
                        "text_colour": "#1c1c1c",
                        "text_align": "CENTER",
                    },
                ],
                images=[
                    {
                        "node_name": f"lodge-{i}",
                        "temp_url": f"https://figma-export.s3.amazonaws.com/lodge{i}.png",
                        "width": 516,
                        "height": 356,
                        "parent_section": "Lodges",
                    }
                    for i in range(1, 4)
                ],
                y_position=1200,
                width=1920,
                height=1000,
            ),
            Section(
                name="Footer",
                semantic_role="footer",
                layout_description="4-column layout; background: #997a4d",
                texts=[
                    {
                        "text": "PARK RANGER Phone: +27183509938",
                        "font_family": "Avenir",
                        "font_size": 16,
                        "font_weight": 350,
                        "text_colour": "#ffffff",
                        "text_align": "LEFT",
                    },
                ],
                images=[],
                background={"type": "colour", "value": "#997a4d"},
                y_position=4089,
                width=1920,
                height=368,
            ),
        ],
        colours=ColourPalette(
            all_colours=[
                {"hex": "#760906", "source": "fills"},
                {"hex": "#48631b", "source": "fills"},
                {"hex": "#fdfaf7", "source": "fills"},
            ],
            primary="#760906",
            secondary="#48631b",
            accent="#f78e1e",
            background="#fdfaf7",
            text_primary="#1c1c1c",
            text_secondary="#ffffff",
        ),
        typography=TypographySystem(
            heading_font="Marcellus",
            body_font="Avenir",
            all_styles=[
                {"font_family": "Marcellus", "font_size": 64, "font_weight": 400},
                {"font_family": "Avenir", "font_size": 18, "font_weight": 350},
            ],
        ),
        screenshot_url="https://figma-export.s3.amazonaws.com/screenshot.png",
    )


class TestDesignPromptBuilder:
    def test_build_returns_system_and_user(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        assert "system_prompt" in result
        assert "user_content" in result
        assert isinstance(result["system_prompt"], str)
        assert isinstance(result["user_content"], str)

    def test_build_with_screenshot_returns_multipart(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=True)
        content = result["user_content"]
        assert isinstance(content, list)
        assert content[0]["type"] == "image_url"
        assert content[0]["image_url"]["url"] == "https://figma-export.s3.amazonaws.com/screenshot.png"
        assert content[1]["type"] == "text"

    def test_prompt_includes_all_sections(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "Hero" in text
        assert "Lodges" in text
        assert "Footer" in text
        assert "Section 1:" in text
        assert "Section 2:" in text
        assert "Section 3:" in text

    def test_prompt_includes_verbatim_text(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "Join Us for an Unforgettable African Safari Experience" in text
        assert "Choosing a Lodge" in text
        assert "PARK RANGER Phone: +27183509938" in text

    def test_prompt_includes_image_urls(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "https://figma-export.s3.amazonaws.com/hero.png" in text
        assert "https://figma-export.s3.amazonaws.com/lodge1.png" in text

    def test_prompt_includes_colours(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "#760906" in text
        assert "#48631b" in text
        assert "#fdfaf7" in text

    def test_prompt_includes_typography(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "Marcellus" in text
        # Avenir should be substituted to Nunito Sans
        assert "Nunito Sans" in text

    def test_prompt_includes_image_manifest(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        text = result["user_content"]
        assert "Complete Image Manifest" in text
        assert "hero-bg" in text
        assert "lodge-1" in text

    def test_system_prompt_has_rules(self, sample_context):
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=False)
        system = result["system_prompt"]
        assert "EXACT text" in system
        assert "EXACT image URLs" in system
        assert "===HTML===" in system

    def test_prompt_without_screenshot_is_string(self, sample_context):
        sample_context.screenshot_url = ""
        builder = DesignPromptBuilder()
        result = builder.build(sample_context, include_screenshot=True)
        # No screenshot URL -> should fall back to string
        assert isinstance(result["user_content"], str)
