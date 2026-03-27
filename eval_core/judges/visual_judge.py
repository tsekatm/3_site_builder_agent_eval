"""Visual judge — evaluates agent output by comparing screenshots via vision model.

Uses OpenRouter Claude Sonnet with vision to compare:
1. Gold standard screenshot (what it should look like)
2. Agent output screenshot (what the model produced)
3. Requirements (what was asked)

This catches issues the code-only judge misses: broken images, empty sections,
dark text on dark backgrounds, broken navigation, missing interactivity.
"""

from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from eval_core.types import Violation, Severity


VISUAL_JUDGE_SYSTEM = """You are a senior UX quality assurance judge comparing a website screenshot against a gold standard.

You will receive:
1. GOLD STANDARD screenshot — what the site SHOULD look like
2. AGENT OUTPUT screenshot — what the model actually produced
3. REQUIREMENTS — what the business needs are

Your job: identify every VISUAL issue in the agent's output by comparing it to the gold standard.

Focus on what a USER would see:
- Are images loading or showing broken placeholders / alt text?
- Is text readable (contrast: light text on dark backgrounds)?
- Is the navigation horizontal or broken into bullet points?
- Are sections filled with content or empty/blank?
- Do cards, buttons, and interactive elements look clickable?
- Is the layout structured (grid/flex) or collapsed to single column?
- Does the colour scheme match the requirements?
- Is the hero section complete with background image, overlay, and text?

Return ONLY a JSON object:
{
  "visual_violations": [
    {
      "id": "VIOLATION-ID",
      "severity": "critical|major|moderate|minor",
      "deduction": -N.N,
      "description": "What is visually wrong",
      "location": "Which section of the page"
    }
  ],
  "visual_score": N,
  "summary": "Overall visual assessment in 2 sentences"
}

Use these violation IDs and deductions:
- VIS-BROKEN-IMAGE (-2.5): Image shows alt text or placeholder instead of actual image
- VIS-LAYOUT-BROKEN (-3.0): Section layout completely broken (bullet nav, collapsed grid)
- STRUCT-EMPTY-SECTION (-3.0): Section is blank/empty — no content visible
- A11Y-DARK-TEXT-ON-DARK-BG (-3.0): Text unreadable due to poor contrast
- VIS-COLOUR-MISMATCH (-0.5): Colours don't match brand requirements
- VIS-WRONG-IMAGE (-1.5): Image loads but doesn't match business context
- INT-NO-HOVER-STATES (-1.0): Buttons/cards look flat with no interactive styling
- VIS-MINOR-DEVIATION (-1.0): Minor visual difference from gold standard
- CONTENT-SECTION-MISSING (-3.0): Entire section from requirements not present

visual_score: Rate 0-10 how close the agent output looks to the gold standard.
10 = identical, 7 = acceptable with minor issues, 5 = major issues, 0 = completely wrong."""


VISUAL_JUDGE_PROMPT = """## Requirements Summary
{requirements_summary}

## Action Being Evaluated
{action_name}: {action_description}

Compare the two screenshots. The first is the GOLD STANDARD (correct), the second is the AGENT OUTPUT (being evaluated).

Identify all visual differences and issues. Return JSON only."""


class VisualJudge:
    """Evaluates agent output by comparing screenshots via vision model."""

    def __init__(self, api_key: Optional[str] = None, model: str = "anthropic/claude-sonnet-4"):
        self._api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self._model = model

    async def evaluate(
        self,
        gold_screenshot: Path,
        agent_screenshot: Path,
        action_name: str,
        action_description: str,
        requirements_summary: str,
    ) -> tuple[list[Violation], float]:
        """Compare gold standard and agent screenshots.

        Returns:
            Tuple of (violations, visual_score 0-10).
        """
        if not gold_screenshot.exists() or not agent_screenshot.exists():
            return [], 5.0  # Can't compare without both screenshots

        start = time.monotonic()

        # Encode screenshots
        gold_b64 = base64.b64encode(gold_screenshot.read_bytes()).decode()
        agent_b64 = base64.b64encode(agent_screenshot.read_bytes()).decode()

        prompt = VISUAL_JUDGE_PROMPT.format(
            requirements_summary=requirements_summary[:2000],
            action_name=action_name,
            action_description=action_description[:500],
        )

        body = json.dumps({
            "model": self._model,
            "messages": [
                {"role": "system", "content": VISUAL_JUDGE_SYSTEM},
                {"role": "user", "content": [
                    {"type": "text", "text": "GOLD STANDARD (correct):"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{gold_b64}"}},
                    {"type": "text", "text": "AGENT OUTPUT (being evaluated):"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{agent_b64}"}},
                    {"type": "text", "text": prompt},
                ]},
            ],
            "max_tokens": 2000,
            "temperature": 0.0,
        }).encode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": "https://eval-pack.bigbeard.co.za",
            "X-Title": "Site Builder Eval Pack - Visual Judge",
        }

        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=body,
                headers=headers,
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            output = result["choices"][0]["message"]["content"]
            return self._parse_response(output)

        except Exception as e:
            return [Violation(
                id="JUDGE-ERROR",
                category="visual",
                severity=Severity.MODERATE,
                deduction=-0.5,
                description=f"Visual judge failed: {str(e)[:100]}",
            )], 5.0

    def _parse_response(self, raw: str) -> tuple[list[Violation], float]:
        """Parse visual judge JSON response."""
        # Extract JSON
        json_str = raw.strip()
        if "```" in json_str:
            match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", json_str, re.DOTALL)
            if match:
                json_str = match.group(1)
        elif not json_str.startswith("{"):
            match = re.search(r"\{.*\}", json_str, re.DOTALL)
            if match:
                json_str = match.group(0)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return [], 5.0

        violations = []
        for v in data.get("visual_violations", []):
            try:
                violations.append(Violation(
                    id=v.get("id", "VIS-MINOR-DEVIATION"),
                    category="visual",
                    severity=self._map_severity(v.get("severity", "moderate")),
                    deduction=float(v.get("deduction", -1.0)),
                    description=v.get("description", "Visual issue"),
                    evidence=v.get("location", ""),
                ))
            except (ValueError, KeyError):
                continue

        visual_score = float(data.get("visual_score", 5.0))
        return violations, visual_score

    def _map_severity(self, sev: str) -> Severity:
        mapping = {
            "critical": Severity.CRITICAL,
            "major": Severity.MAJOR,
            "moderate": Severity.MODERATE,
            "minor": Severity.MINOR,
        }
        return mapping.get(sev.lower(), Severity.MODERATE)
