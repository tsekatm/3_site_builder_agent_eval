"""Abstract base runner for model invocation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from eval_core.types import RunnerResponse


class BaseRunner(ABC):
    """Abstract base for all model runners."""

    @abstractmethod
    async def invoke(
        self,
        prompt: str,
        system_prompt: str = "",
        params: dict | None = None,
    ) -> RunnerResponse:
        """Invoke the model and return a response."""
        ...

    @abstractmethod
    def model_id(self) -> str:
        """Return the model identifier."""
        ...

    @abstractmethod
    def model_name(self) -> str:
        """Return the human-readable model name."""
        ...
