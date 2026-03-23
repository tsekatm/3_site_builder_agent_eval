"""Content comparison — HTML structure, text content, meta tags."""

from __future__ import annotations

import re
from pathlib import Path
from html.parser import HTMLParser

from eval_core.types import Violation, Severity


class TextExtractor(HTMLParser):
    """Extract visible text content from HTML."""

    def __init__(self):
        super().__init__()
        self.texts: list[str] = []
        self._skip = False
        self._skip_tags = {"script", "style", "noscript"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self.texts.append(text)


class ContentComparer:
    """Compare HTML content between gold standard and agent output."""

    def __init__(self, gold_html_path: Path, agent_html_path: Path):
        self.gold_html = gold_html_path.read_text(errors="ignore") if gold_html_path.exists() else ""
        self.agent_html = agent_html_path.read_text(errors="ignore") if agent_html_path.exists() else ""

    def compare(self) -> list[Violation]:
        violations: list[Violation] = []
        violations.extend(self.check_meta_tags())
        violations.extend(self.check_heading_hierarchy())
        violations.extend(self.check_alt_text())
        violations.extend(self.check_skip_link())
        violations.extend(self.check_responsive_viewport())
        return violations

    def check_meta_tags(self) -> list[Violation]:
        """Check for required meta tags."""
        violations: list[Violation] = []

        required_meta = {
            "description": r'<meta\s+name="description"\s+content="[^"]+">',
            "og:title": r'<meta\s+property="og:title"\s+content="[^"]+">',
            "og:description": r'<meta\s+property="og:description"\s+content="[^"]+">',
            "viewport": r'<meta\s+name="viewport"',
        }

        for name, pattern in required_meta.items():
            if not re.search(pattern, self.agent_html, re.IGNORECASE):
                violations.append(Violation(
                    id="CONTENT-MISSING-META",
                    category="content",
                    severity=Severity.MINOR,
                    deduction=-0.25,
                    file="index.html",
                    description=f"Missing meta tag: {name}",
                ))
        return violations

    def check_heading_hierarchy(self) -> list[Violation]:
        """Check for proper heading hierarchy (single H1, no skipped levels)."""
        violations: list[Violation] = []
        h1_count = len(re.findall(r"<h1[\s>]", self.agent_html, re.IGNORECASE))

        if h1_count == 0:
            violations.append(Violation(
                id="CODE-INVALID-HTML",
                category="code_quality",
                severity=Severity.MODERATE,
                deduction=-0.5,
                file="index.html",
                description="Missing H1 heading",
            ))
        elif h1_count > 1:
            violations.append(Violation(
                id="CODE-INVALID-HTML",
                category="code_quality",
                severity=Severity.MODERATE,
                deduction=-0.5,
                file="index.html",
                description=f"Multiple H1 headings found ({h1_count}). Expected exactly 1.",
                evidence=f"Found {h1_count} H1 tags",
            ))
        return violations

    def check_alt_text(self) -> list[Violation]:
        """Check all img tags have alt attributes."""
        violations: list[Violation] = []
        img_tags = re.findall(r"<img\s+[^>]*>", self.agent_html, re.IGNORECASE)

        for img in img_tags:
            if 'alt=' not in img.lower():
                src_match = re.search(r'src="([^"]*)"', img)
                src = src_match.group(1) if src_match else "unknown"
                violations.append(Violation(
                    id="A11Y-MISSING-ALT",
                    category="accessibility",
                    severity=Severity.MODERATE,
                    deduction=-0.5,
                    file="index.html",
                    description=f"Image missing alt attribute: {src}",
                    evidence=img[:100],
                ))
        return violations

    def check_skip_link(self) -> list[Violation]:
        """Check for skip-to-content link."""
        violations: list[Violation] = []
        if not re.search(r'<a[^>]*href="#main|skip', self.agent_html, re.IGNORECASE):
            violations.append(Violation(
                id="A11Y-NO-SKIP-LINK",
                category="accessibility",
                severity=Severity.MINOR,
                deduction=-0.25,
                file="index.html",
                description="Missing skip-to-content link",
            ))
        return violations

    def check_responsive_viewport(self) -> list[Violation]:
        """Check for responsive meta viewport."""
        violations: list[Violation] = []
        if not re.search(r'<meta\s+name="viewport"', self.agent_html, re.IGNORECASE):
            violations.append(Violation(
                id="CODE-NO-RESPONSIVE",
                category="code_quality",
                severity=Severity.MAJOR,
                deduction=-1.5,
                file="index.html",
                description="Missing responsive viewport meta tag",
            ))
        return violations

    def extract_text(self, html: str) -> list[str]:
        """Extract visible text content from HTML."""
        parser = TextExtractor()
        parser.feed(html)
        return parser.texts
