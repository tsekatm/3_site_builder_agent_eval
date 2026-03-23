"""Screenshot capture using Playwright."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


VIEWPORT = {"width": 1280, "height": 720}
DISABLE_ANIMATIONS_CSS = """
*, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-delay: 0.01ms !important;
    transition-duration: 0.01ms !important;
    transition-delay: 0.01ms !important;
}
"""


async def capture_screenshot(
    html_path: Path,
    output_path: Path,
    viewport: Optional[dict] = None,
    full_page: bool = True,
) -> Path:
    """Capture a screenshot of an HTML file using Playwright.

    Args:
        html_path: Path to the HTML file to screenshot.
        output_path: Where to save the PNG screenshot.
        viewport: Optional viewport size override.
        full_page: Whether to capture the full page or just the viewport.

    Returns:
        Path to the saved screenshot.
    """
    from playwright.async_api import async_playwright

    vp = viewport or VIEWPORT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport_size=vp)

        # Disable animations for deterministic screenshots
        await page.add_style_tag(content=DISABLE_ANIMATIONS_CSS)

        # Navigate to the HTML file
        await page.goto(f"file://{html_path.resolve()}")

        # Wait for full load
        await page.wait_for_load_state("networkidle")

        # Wait for fonts
        try:
            await page.evaluate("() => document.fonts.ready")
        except Exception:
            pass  # Fonts may not be available in all environments

        # Capture
        await page.screenshot(path=str(output_path), full_page=full_page)

        await browser.close()

    return output_path
