"""Parallel execution engine — runs eval tasks across models concurrently."""

from __future__ import annotations

import asyncio
import random
from typing import Callable, Optional

from botocore.exceptions import ClientError

from eval_core.runners.base import BaseRunner
from eval_core.types import RunnerResponse


class EvalOrchestrator:
    """Orchestrates parallel eval execution across models and prompts."""

    def __init__(self, max_workers: int = 3, max_prompts: int = 5):
        self.max_workers = max_workers
        self.max_prompts = max_prompts

    async def run_all(
        self,
        runners: list[BaseRunner],
        tasks: list[dict],
        on_progress: Optional[Callable] = None,
    ) -> dict[str, list[RunnerResponse]]:
        """Run all tasks across all models concurrently.

        Args:
            runners: List of model runners.
            tasks: List of task dicts with keys: template, stage, action_id, prompt, system_prompt.
            on_progress: Optional callback(model_id, template, status).

        Returns:
            Dict mapping model_id to list of RunnerResponses.
        """
        results: dict[str, list[RunnerResponse]] = {}
        worker_sem = asyncio.Semaphore(self.max_workers)

        async def run_model(runner: BaseRunner):
            async with worker_sem:
                prompt_sem = asyncio.Semaphore(self.max_prompts)
                coros = [
                    self._run_task(runner, task, prompt_sem, on_progress)
                    for task in tasks
                ]
                model_results = await asyncio.gather(*coros, return_exceptions=True)

                # Convert exceptions to error responses
                processed = []
                for r in model_results:
                    if isinstance(r, Exception):
                        processed.append(RunnerResponse(
                            model_id=runner.model_id(),
                            output="",
                            error=str(r),
                        ))
                    else:
                        processed.append(r)

                results[runner.model_id()] = processed

        await asyncio.gather(*[run_model(r) for r in runners])
        return results

    async def _run_task(
        self,
        runner: BaseRunner,
        task: dict,
        semaphore: asyncio.Semaphore,
        on_progress: Optional[Callable],
    ) -> RunnerResponse:
        async with semaphore:
            response = await self._invoke_with_backoff(
                runner,
                task["prompt"],
                task.get("system_prompt", ""),
            )
            if on_progress:
                status = "error" if response.error else "complete"
                on_progress(
                    runner.model_id(),
                    task.get("template", ""),
                    f"{task.get('action_id', '?')}: {status}",
                )
            return response

    async def _invoke_with_backoff(
        self,
        runner: BaseRunner,
        prompt: str,
        system_prompt: str,
        max_retries: int = 3,
    ) -> RunnerResponse:
        """Invoke with exponential backoff on throttling."""
        for attempt in range(max_retries):
            try:
                return await runner.invoke(prompt, system_prompt)
            except ClientError as e:
                if (
                    e.response["Error"]["Code"] == "ThrottlingException"
                    and attempt < max_retries - 1
                ):
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(wait)
                else:
                    return RunnerResponse(
                        model_id=runner.model_id(),
                        output="",
                        error=str(e),
                    )
        return RunnerResponse(
            model_id=runner.model_id(),
            output="",
            error="Max retries exceeded",
        )
