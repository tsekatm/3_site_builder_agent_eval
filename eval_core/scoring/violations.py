"""Violation catalogue loader."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from eval_core.types import Severity


class ViolationDef:
    """A violation definition from the catalogue."""

    def __init__(self, id: str, description: str, severity: str, deduction: float, max_deduction: Optional[float] = None):
        self.id = id
        self.description = description
        self.severity = Severity(severity)
        self.deduction = deduction
        self.max_deduction = max_deduction

    def __repr__(self) -> str:
        return f"ViolationDef({self.id}, {self.severity.value}, {self.deduction})"


class ViolationCatalogue:
    """Loads and provides access to the violation catalogue."""

    def __init__(self, catalogue_path: Path):
        self._violations: dict[str, ViolationDef] = {}
        self._categories: dict[str, list[ViolationDef]] = {}
        self._load(catalogue_path)

    def _load(self, path: Path) -> None:
        with open(path) as f:
            raw = yaml.safe_load(f)

        for category_name, category_data in raw.get("categories", {}).items():
            self._categories[category_name] = []
            for v in category_data.get("violations", []):
                vdef = ViolationDef(
                    id=v["id"],
                    description=v["description"],
                    severity=v["severity"],
                    deduction=v["deduction"],
                    max_deduction=v.get("max_deduction"),
                )
                self._violations[v["id"]] = vdef
                self._categories[category_name].append(vdef)

    def get(self, violation_id: str) -> Optional[ViolationDef]:
        return self._violations.get(violation_id)

    def all(self) -> list[ViolationDef]:
        return list(self._violations.values())

    def by_category(self, category: str) -> list[ViolationDef]:
        return self._categories.get(category, [])

    def categories(self) -> list[str]:
        return list(self._categories.keys())

    def as_yaml_string(self) -> str:
        """Return the catalogue as YAML for inclusion in judge prompts."""
        lines = []
        for cat, vdefs in self._categories.items():
            lines.append(f"{cat}:")
            for v in vdefs:
                lines.append(f"  - {v.id}: {v.description} ({v.severity.value}, {v.deduction})")
        return "\n".join(lines)
