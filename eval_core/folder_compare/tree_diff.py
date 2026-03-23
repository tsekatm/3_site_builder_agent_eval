"""File tree comparison — structural diff between gold standard and agent output."""

from __future__ import annotations

import re
from pathlib import Path

from eval_core.types import Violation, Severity


class FolderComparer:
    """Compares agent output folder against gold standard folder."""

    def __init__(self, gold_dir: Path, agent_dir: Path):
        self.gold_dir = gold_dir
        self.agent_dir = agent_dir

    def compare(self) -> list[Violation]:
        """Run all structural and content checks, return violations."""
        violations: list[Violation] = []
        violations.extend(self.check_required_files())
        violations.extend(self.check_extra_files())
        violations.extend(self.check_placeholder_tokens())
        violations.extend(self.check_css_variables())
        return violations

    def check_required_files(self) -> list[Violation]:
        """Check that all gold standard files exist in agent output."""
        violations: list[Violation] = []
        for gold_file in self.gold_dir.rglob("*"):
            if not gold_file.is_file():
                continue
            relative = gold_file.relative_to(self.gold_dir)
            agent_file = self.agent_dir / relative

            if not agent_file.exists():
                is_index = relative.name == "index.html"
                violations.append(Violation(
                    id="STRUCT-MISSING-INDEX" if is_index else "STRUCT-MISSING-ASSET",
                    category="structural",
                    severity=Severity.CRITICAL if is_index else Severity.MAJOR,
                    deduction=-3.0 if is_index else -1.5,
                    file=str(relative),
                    description=f"Missing required file: {relative}",
                ))
        return violations

    def check_extra_files(self) -> list[Violation]:
        """Check for unexpected files in agent output not in gold standard."""
        violations: list[Violation] = []
        gold_files = {f.relative_to(self.gold_dir) for f in self.gold_dir.rglob("*") if f.is_file()}

        for agent_file in self.agent_dir.rglob("*"):
            if not agent_file.is_file():
                continue
            relative = agent_file.relative_to(self.agent_dir)
            if relative not in gold_files:
                violations.append(Violation(
                    id="STRUCT-EXTRA-FILES",
                    category="structural",
                    severity=Severity.MINOR,
                    deduction=-0.25,
                    file=str(relative),
                    description=f"Unexpected file not in gold standard: {relative}",
                ))
        return violations

    def check_placeholder_tokens(self) -> list[Violation]:
        """Check for unreplaced {{PLACEHOLDER}} tokens in agent HTML files."""
        violations: list[Violation] = []
        for agent_file in self.agent_dir.rglob("*.html"):
            content = agent_file.read_text(errors="ignore")
            placeholders = re.findall(r"\{\{[A-Z_]+\}\}", content)
            for ph in placeholders:
                violations.append(Violation(
                    id="CONTENT-PLACEHOLDER",
                    category="content",
                    severity=Severity.MAJOR,
                    deduction=-1.0,
                    file=str(agent_file.relative_to(self.agent_dir)),
                    description=f"Unreplaced placeholder token: {ph}",
                    evidence=ph,
                ))
        return violations

    def check_css_variables(self) -> list[Violation]:
        """Check CSS custom properties in agent output vs gold standard."""
        violations: list[Violation] = []
        gold_vars = self._extract_css_variables(self.gold_dir)
        agent_vars = self._extract_css_variables(self.agent_dir)

        for var_name, gold_value in gold_vars.items():
            if var_name not in agent_vars:
                violations.append(Violation(
                    id="CODE-HARDCODED-VALUES",
                    category="code_quality",
                    severity=Severity.MAJOR,
                    deduction=-1.0,
                    description=f"Missing CSS variable: {var_name} (expected: {gold_value})",
                    evidence=f"Gold: {var_name}: {gold_value}",
                ))
            elif agent_vars[var_name] != gold_value:
                violations.append(Violation(
                    id="VIS-COLOUR-MISMATCH",
                    category="visual",
                    severity=Severity.MODERATE,
                    deduction=-0.5,
                    description=f"CSS variable mismatch: {var_name}",
                    evidence=f"Expected: {gold_value}, Got: {agent_vars[var_name]}",
                ))
        return violations

    def _extract_css_variables(self, base_dir: Path) -> dict[str, str]:
        """Extract :root CSS custom properties from all CSS files."""
        variables: dict[str, str] = {}
        for css_file in base_dir.rglob("*.css"):
            content = css_file.read_text(errors="ignore")
            # Match :root { ... } block
            root_match = re.search(r":root\s*\{([^}]+)\}", content)
            if root_match:
                block = root_match.group(1)
                for match in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", block):
                    variables[match.group(1).strip()] = match.group(2).strip()
        return variables
