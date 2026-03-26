"""Automated visual checks — detects issues from HTML/CSS without needing LLM vision.

These checks catch the problems the judge misses because it only reads code:
- Broken images (src contains alt text, local paths, or no valid URL)
- Empty sections (section tags with no visible content)
- Dark text on dark backgrounds (CSS analysis)
- Broken nav layout (ul without proper CSS)
- Missing interactive elements (no JS)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from eval_core.types import Violation, Severity


class HTMLVisualChecker:
    """Checks HTML/CSS for visual issues that render poorly in browser."""

    def __init__(self, html_path: Path, css_path: Optional[Path] = None):
        self.html = html_path.read_text(errors="ignore") if html_path.exists() else ""
        self.css = css_path.read_text(errors="ignore") if css_path and css_path.exists() else ""

    def check_all(self) -> list[Violation]:
        """Run all visual checks."""
        violations: list[Violation] = []
        violations.extend(self.check_broken_images())
        violations.extend(self.check_empty_sections())
        violations.extend(self.check_dark_text_on_dark_bg())
        violations.extend(self.check_broken_nav())
        violations.extend(self.check_missing_interactivity())
        violations.extend(self.check_local_file_paths())
        return violations

    def check_broken_images(self) -> list[Violation]:
        """Detect images with broken/invalid src attributes."""
        violations: list[Violation] = []
        img_tags = re.findall(r'<img\s+[^>]*>', self.html, re.IGNORECASE)

        for img in img_tags:
            src_match = re.search(r'src="([^"]*)"', img)
            alt_match = re.search(r'alt="([^"]*)"', img)

            if not src_match:
                violations.append(Violation(
                    id="VIS-BROKEN-IMAGE",
                    category="visual",
                    severity=Severity.CRITICAL,
                    deduction=-2.5,
                    file="index.html",
                    description="Image tag has no src attribute",
                    evidence=img[:100],
                ))
                continue

            src = src_match.group(1).strip()
            alt = alt_match.group(1).strip() if alt_match else ""

            # Check for common broken patterns
            if not src:
                violations.append(Violation(
                    id="VIS-BROKEN-IMAGE",
                    category="visual",
                    severity=Severity.CRITICAL,
                    deduction=-2.5,
                    file="index.html",
                    description="Image src is empty",
                    evidence=img[:100],
                ))
            elif src == alt or (len(src) > 30 and " " in src and not src.startswith("http")):
                # Alt text used as src (common DeepSeek error)
                violations.append(Violation(
                    id="VIS-BROKEN-IMAGE",
                    category="visual",
                    severity=Severity.CRITICAL,
                    deduction=-2.5,
                    file="index.html",
                    description=f"Image src contains descriptive text instead of URL: '{src[:60]}'",
                    evidence=img[:100],
                ))
            elif not src.startswith(("http://", "https://", "data:", "/")) and "." not in src:
                violations.append(Violation(
                    id="CODE-LOCAL-FILE-PATH",
                    category="code_quality",
                    severity=Severity.CRITICAL,
                    deduction=-2.0,
                    file="index.html",
                    description=f"Image src is not a valid URL: '{src[:60]}'",
                    evidence=img[:100],
                ))

        # Check CSS background-image for broken paths
        bg_images = re.findall(r"background(?:-image)?\s*:\s*url\(['\"]?([^)'\"]*)['\"]\)", self.css)
        for bg in bg_images:
            if bg and not bg.startswith(("http://", "https://", "data:", "/", "../")):
                if " " in bg or len(bg) > 50:
                    violations.append(Violation(
                        id="VIS-BROKEN-IMAGE",
                        category="visual",
                        severity=Severity.CRITICAL,
                        deduction=-2.5,
                        file="css/styles.css",
                        description=f"CSS background-image has invalid URL: '{bg[:60]}'",
                    ))

        return violations

    def check_empty_sections(self) -> list[Violation]:
        """Detect HTML sections that exist but have no visible content."""
        violations: list[Violation] = []

        # Find all section/div with id or class that should have content
        sections = re.findall(
            r'<(?:section|div)\s+[^>]*(?:id|class)="([^"]*)"[^>]*>(.*?)</(?:section|div)>',
            self.html, re.DOTALL | re.IGNORECASE
        )

        for name, content in sections:
            # Strip HTML tags and whitespace
            text_only = re.sub(r'<[^>]+>', '', content).strip()
            if not text_only and len(content) < 50:
                violations.append(Violation(
                    id="STRUCT-EMPTY-SECTION",
                    category="structural",
                    severity=Severity.CRITICAL,
                    deduction=-3.0,
                    file="index.html",
                    description=f"Section '{name}' exists but has no visible content",
                ))

        return violations

    def check_dark_text_on_dark_bg(self) -> list[Violation]:
        """Detect potential dark-on-dark contrast issues from CSS."""
        violations: list[Violation] = []

        # Extract CSS variables
        root_match = re.search(r':root\s*\{([^}]+)\}', self.css)
        if not root_match:
            return violations

        root_block = root_match.group(1)
        vars_dict: dict[str, str] = {}
        for match in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', root_block):
            vars_dict[match.group(1).strip()] = match.group(2).strip()

        text_color = vars_dict.get("--text-color", "").lower()
        bg_color = vars_dict.get("--background-color", "").lower()

        # Check if text is dark AND there are sections with background images
        has_bg_images = bool(re.search(r'background(-image)?\s*:\s*url\(', self.css))
        text_is_dark = self._is_dark_color(text_color)

        if has_bg_images and text_is_dark:
            # Check if there's a --text-secondary variable for light text
            text_secondary = vars_dict.get("--text-secondary", "").lower()
            if not text_secondary or self._is_dark_color(text_secondary):
                violations.append(Violation(
                    id="A11Y-DARK-TEXT-ON-DARK-BG",
                    category="accessibility",
                    severity=Severity.CRITICAL,
                    deduction=-3.0,
                    file="css/styles.css",
                    description=f"Dark text color ({text_color}) used with background images but no light text variable defined",
                ))

        # Check hero section specifically
        hero_match = re.search(r'\.hero[^{]*\{([^}]+)\}', self.css)
        if hero_match:
            hero_css = hero_match.group(1)
            has_hero_bg = bool(re.search(r'background(-image)?\s*:\s*url\(', hero_css))
            hero_color = re.search(r'(?<!background-)color\s*:\s*([^;]+)', hero_css)
            if has_hero_bg and hero_color:
                color_val = hero_color.group(1).strip()
                if self._is_dark_color(color_val):
                    violations.append(Violation(
                        id="A11Y-DARK-TEXT-ON-DARK-BG",
                        category="accessibility",
                        severity=Severity.CRITICAL,
                        deduction=-3.0,
                        file="css/styles.css",
                        description=f"Hero section has background image with dark text color: {color_val}",
                    ))

        return violations

    def check_broken_nav(self) -> list[Violation]:
        """Detect navigation that will render as bullet-point list."""
        violations: list[Violation] = []

        # Check if nav has ul/li but CSS doesn't remove list-style
        has_nav_list = bool(re.search(r'<nav[^>]*>.*?<ul.*?<li', self.html, re.DOTALL | re.IGNORECASE))
        if has_nav_list:
            has_list_none = bool(re.search(r'list-style\s*:\s*none', self.css))
            has_nav_flex = bool(re.search(r'nav.*?\{[^}]*display\s*:\s*flex', self.css, re.DOTALL))
            nav_links_flex = bool(re.search(r'\.nav-links\s*\{[^}]*display\s*:\s*flex', self.css))

            if not has_list_none and not nav_links_flex:
                violations.append(Violation(
                    id="VIS-LAYOUT-BROKEN",
                    category="visual",
                    severity=Severity.CRITICAL,
                    deduction=-3.0,
                    file="css/styles.css",
                    description="Navigation list missing list-style:none — will show bullet points",
                ))

        return violations

    def check_missing_interactivity(self) -> list[Violation]:
        """Check for missing JavaScript interactivity."""
        violations: list[Violation] = []

        has_script = bool(re.search(r'<script', self.html, re.IGNORECASE))
        has_mobile_menu = bool(re.search(r'hamburger|mobile.*menu|menu.*toggle|aria-expanded', self.html, re.IGNORECASE))
        has_smooth_scroll = bool(re.search(r'smooth|scrollIntoView|scroll-behavior', self.html + self.css, re.IGNORECASE))

        if not has_script:
            violations.append(Violation(
                id="INT-NO-JS-FUNCTIONALITY",
                category="interactivity",
                severity=Severity.CRITICAL,
                deduction=-2.0,
                file="index.html",
                description="No JavaScript found — site has no interactivity",
            ))
        else:
            if not has_mobile_menu:
                violations.append(Violation(
                    id="INT-NO-MOBILE-MENU",
                    category="interactivity",
                    severity=Severity.CRITICAL,
                    deduction=-2.5,
                    file="index.html",
                    description="No mobile menu toggle — site unusable on mobile",
                ))
            if not has_smooth_scroll:
                violations.append(Violation(
                    id="INT-NO-SMOOTH-SCROLL",
                    category="interactivity",
                    severity=Severity.MODERATE,
                    deduction=-0.5,
                    file="index.html",
                    description="No smooth scrolling for anchor links",
                ))

        # Check for hover states in CSS
        has_hover = bool(re.search(r':hover', self.css))
        if not has_hover:
            violations.append(Violation(
                id="INT-NO-HOVER-STATES",
                category="interactivity",
                severity=Severity.MAJOR,
                deduction=-1.0,
                file="css/styles.css",
                description="No :hover styles — buttons and cards have no hover feedback",
            ))

        return violations

    def check_local_file_paths(self) -> list[Violation]:
        """Check for local filesystem paths that won't work in browser."""
        violations: list[Violation] = []

        # Common patterns for local paths
        local_patterns = [
            r'src="(?:images/|assets/|/Users/|/home/|C:\\|\.\./)([^"]*)"',
        ]

        for pattern in local_patterns:
            matches = re.findall(pattern, self.html)
            for match in matches:
                # Skip if it's a relative path within the template (css/, js/)
                if match.startswith(("css/", "js/")):
                    continue
                violations.append(Violation(
                    id="CODE-LOCAL-FILE-PATH",
                    category="code_quality",
                    severity=Severity.CRITICAL,
                    deduction=-2.0,
                    file="index.html",
                    description=f"Local file path that won't work in browser: '{match[:60]}'",
                ))

        return violations

    def _is_dark_color(self, color: str) -> bool:
        """Check if a CSS color value is dark (low luminance)."""
        color = color.strip().lower()

        # Handle hex colors
        hex_match = re.match(r'#([0-9a-f]{3,8})', color)
        if hex_match:
            hex_val = hex_match.group(1)
            if len(hex_val) == 3:
                hex_val = ''.join(c * 2 for c in hex_val)
            if len(hex_val) >= 6:
                r, g, b = int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16)
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                return luminance < 0.5

        # Handle named colors
        dark_colors = {"black", "darkblue", "darkred", "darkgreen", "navy", "maroon", "darkgrey", "darkgray"}
        if color in dark_colors:
            return True

        # Handle var() — can't determine, assume not dark
        if "var(" in color:
            return False

        return False
