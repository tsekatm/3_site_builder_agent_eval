"""Teacher model — proposes skill file improvements based on eval results."""

from __future__ import annotations

import json
from typing import Optional

from eval_core.runners.base import BaseRunner
from eval_core.types import ActionScore

TEACHER_SYSTEM_PROMPT = """You are a prompt engineering expert specialising in AI agent skill optimisation.

You review agent skill files that produced poor evaluation results and propose targeted improvements.

Return ONLY a JSON object (no markdown, no explanation):
{
  "reasoning": "Why these changes will help",
  "changes": [
    {
      "section": "Section of the skill file to modify",
      "old_text": "Current text to find and replace",
      "new_text": "Improved replacement text",
      "rationale": "Why this specific change addresses the violations"
    }
  ],
  "expected_improvement": "Estimated score improvement (e.g., '+1.5 points')"
}

Rules:
- Propose MINIMAL changes — only what's needed to fix the violations
- old_text must be an EXACT substring of the current skill file
- Each change should address a specific violation or group of violations
- Do not rewrite the entire skill file — surgical edits only"""

TEACHER_PROMPT_TEMPLATE = """## Skill File Being Evaluated
```
{skill_content}
```

## Eval Results
**Model**: {model}
**Template**: {template}

### Low-Scoring Actions
{low_scoring_actions}

## Task
Propose changes to the skill file that would help the agent avoid these specific violations. Focus on the lowest-scoring actions first."""


class TeacherEngine:
    """Uses a teacher model to propose skill improvements."""

    def __init__(self, runner: BaseRunner):
        self.runner = runner

    async def propose_improvements(
        self,
        skill_content: str,
        model: str,
        template: str,
        low_scoring_actions: list[ActionScore],
        target_score: float = 7.0,
    ) -> Optional[dict]:
        """Propose skill file improvements based on eval results.

        Args:
            skill_content: Current skill file text.
            model: Model name that was evaluated.
            template: Template name.
            low_scoring_actions: Actions scoring below target.
            target_score: Minimum acceptable score.

        Returns:
            Dict with reasoning, changes, and expected_improvement, or None on failure.
        """
        actions_text = self._format_low_actions(low_scoring_actions, target_score)
        if not actions_text:
            return None

        prompt = TEACHER_PROMPT_TEMPLATE.format(
            skill_content=skill_content[:20000],
            model=model,
            template=template,
            low_scoring_actions=actions_text,
        )

        response = await self.runner.invoke(prompt, system_prompt=TEACHER_SYSTEM_PROMPT)
        if response.error:
            return None

        return self._parse_response(response.output)

    def _format_low_actions(self, actions: list[ActionScore], target: float) -> str:
        lines = []
        for a in actions:
            if a.final_score < target:
                lines.append(f"\n**Action {a.action_id}: {a.action_name}** (score: {a.final_score:.1f}/{a.base_score})")
                lines.append(f"Skill: {a.skill} | Category: {a.category}")
                for v in a.violations:
                    lines.append(f"  - [{v.severity.value}] {v.id}: {v.description} ({v.deduction})")
        return "\n".join(lines) if lines else ""

    def _parse_response(self, raw: str) -> Optional[dict]:
        raw = raw.strip()
        if raw.startswith("```"):
            import re
            match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", raw, re.DOTALL)
            if match:
                raw = match.group(1)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None
