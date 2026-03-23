"""Multimodal LLM judge — evaluates agent output per action using Claude Opus."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from eval_core.runners.base import BaseRunner
from eval_core.types import Violation, Severity

SYSTEM_PROMPT = """You are an expert web developer and quality assurance judge evaluating a site builder agent's output.

You will receive:
1. The ACTION that the agent was asked to perform
2. The REQUIREMENTS for this specific action
3. The GOLD STANDARD output (created by Claude Opus — the reference)
4. The AGENT OUTPUT (created by the model being evaluated)
5. The VIOLATION CATALOGUE with severity levels and deduction amounts

Your job: identify every violation in the agent output by comparing it against the gold standard and requirements. Be thorough — check every element, every CSS variable, every text replacement, every image, every meta tag relevant to this specific action.

Return ONLY a JSON object with this exact structure (no markdown, no explanation):
{
  "violations": [
    {
      "id": "VIOLATION-ID-FROM-CATALOGUE",
      "category": "structural|visual|content|code_quality|accessibility|performance",
      "severity": "critical|major|moderate|minor",
      "deduction": -N.N,
      "file": "filename or null",
      "description": "What is wrong",
      "evidence": "Specific line/element showing the issue",
      "recommendation": "How to fix it"
    }
  ],
  "summary": "Brief overall assessment of this action",
  "strengths": ["What the agent did well"],
  "critical_issues": ["Most impactful problems"]
}

Rules:
- Use EXACT deduction amounts from the violation catalogue
- Do NOT invent violation IDs — use only IDs from the catalogue
- Do NOT report violations that don't exist — only actual differences
- Focus ONLY on the specific action being evaluated, not the whole site
- If the action was performed perfectly, return an empty violations array"""


ACTION_PROMPT_TEMPLATE = """## Action: {action_name}
**Skill**: {skill}
**Category**: {category}

## Requirements for this Action
{action_description}

## Expected Changes
{expected_changes}

## Gold Standard — index.html (relevant section)
```html
{gold_html}
```

## Gold Standard — css/styles.css (relevant section)
```css
{gold_css}
```

## Agent Output — index.html
```html
{agent_html}
```

## Agent Output — css/styles.css
```css
{agent_css}
```

## Violation Catalogue
{violation_catalogue}

Evaluate the agent's execution of this specific action. Return violations as JSON."""


class OpusJudge:
    """Multimodal judge using Claude Opus to evaluate per-action output."""

    def __init__(self, runner: BaseRunner, violation_catalogue_yaml: str):
        self.runner = runner
        self.catalogue_yaml = violation_catalogue_yaml

    async def evaluate_action(
        self,
        action_name: str,
        skill: str,
        category: str,
        action_description: str,
        expected_changes: list[str],
        gold_html: str,
        gold_css: str,
        agent_html: str,
        agent_css: str,
    ) -> list[Violation]:
        """Evaluate a single action's output against gold standard."""
        prompt = ACTION_PROMPT_TEMPLATE.format(
            action_name=action_name,
            skill=skill,
            category=category,
            action_description=action_description,
            expected_changes="\n".join(f"- {c}" for c in expected_changes) if expected_changes else "N/A",
            gold_html=gold_html[:15000],   # Truncate to avoid context overflow
            gold_css=gold_css[:10000],
            agent_html=agent_html[:15000],
            agent_css=agent_css[:10000],
            violation_catalogue=self.catalogue_yaml,
        )

        response = await self.runner.invoke(prompt, system_prompt=SYSTEM_PROMPT)

        if response.error:
            return [Violation(
                id="JUDGE-ERROR",
                category="structural",
                severity=Severity.CRITICAL,
                deduction=-3.0,
                description=f"Judge invocation failed: {response.error}",
            )]

        return self._parse_violations(response.output)

    def _parse_violations(self, raw_output: str) -> list[Violation]:
        """Parse judge response into Violation objects."""
        json_str = self._extract_json(raw_output)
        if not json_str:
            if raw_output.strip():
                return [Violation(
                    id="JUDGE-PARSE-ERROR",
                    category="structural",
                    severity=Severity.MODERATE,
                    deduction=-0.5,
                    description="Could not extract JSON from judge response",
                    evidence=raw_output[:200],
                )]
            return []

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return [Violation(
                id="JUDGE-PARSE-ERROR",
                category="structural",
                severity=Severity.MODERATE,
                deduction=-0.5,
                description="Failed to parse judge response as JSON",
                evidence=raw_output[:200],
            )]

        violations = []
        for v in data.get("violations", []):
            try:
                violations.append(Violation(
                    id=v.get("id", "UNKNOWN"),
                    category=v.get("category", "structural"),
                    severity=Severity(v.get("severity", "moderate")),
                    deduction=float(v.get("deduction", -0.5)),
                    file=v.get("file"),
                    description=v.get("description", "No description"),
                    evidence=v.get("evidence"),
                    recommendation=v.get("recommendation"),
                ))
            except (ValueError, KeyError):
                continue

        return violations

    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from response, handling markdown code blocks."""
        # Try direct JSON parse first
        text = text.strip()
        if text.startswith("{"):
            return text

        # Try ```json ... ``` blocks
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try finding JSON object in text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)

        return None
