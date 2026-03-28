"""Figma design extraction and prompt building for site generation.

Public API:
    extract_design(figma_url, access_token) -> DesignContext
    build_prompt(context, include_screenshot) -> dict
"""

from eval_core.figma.extractor import FigmaDesignExtractor, DesignContext
from eval_core.figma.prompt_builder import DesignPromptBuilder

__all__ = ["FigmaDesignExtractor", "DesignContext", "DesignPromptBuilder"]
