"""Multi-model routing — assigns the best model per action based on eval data.

Routes actions to the optimal model:
- Kimi K2.5: fonts, logos, images, section backgrounds (best visual output)
- Claude Haiku: colours, text content, contact, layout, SEO, accessibility, interactivity
- Fallback: Kimi K2.5 for any unmatched action

This routing is based on 5 templates of eval data (575 total actions evaluated).
"""

from __future__ import annotations

from typing import Optional

from eval_core.config import ModelConfig


# Action → model routing table
# Based on eval results across 5 templates (ai-page-builder, safari-lodge,
# association-corporate, saas-product, gala-event)
ACTION_ROUTING: dict[str, str] = {
    # Kimi K2.5 — best at visual/image tasks
    "swap-fonts":           "kimi-k2.5",     # avg 8.3 vs Haiku 5.7
    "replace-header-logo":  "kimi-k2.5",     # avg 8.7, consistent 10s
    "replace-footer-logo":  "kimi-k2.5",     # avg 10.0 across all templates
    "replace-favicon":      "kimi-k2.5",     # avg 10.0 across all templates
    "replace-hero-bg":      "kimi-k2.5",     # avg 8.5 vs Haiku 3.0
    "replace-section-bgs":  "kimi-k2.5",     # avg 8.5 vs Haiku 3.0

    # Claude Haiku — best at text, structure, and reasoning tasks
    "apply-colours":        "claude-haiku",  # avg 5.5 (best of bad options)
    "update-hero-text":     "claude-haiku",  # avg 8.3 vs Kimi 5.5
    "update-about-text":    "claude-haiku",  # avg 9.5 vs Kimi 5.5
    "update-contact":       "claude-haiku",  # avg 7.0 vs Kimi 2.2
    "apply-hero-layout":    "claude-haiku",  # user observation: cleanest layouts
    "apply-sections-layout":"claude-haiku",  # user observation: cleanest layouts
    "add-seo-meta":         "claude-haiku",  # avg 8.9 vs Kimi 7.8
    "add-structured-data":  "claude-haiku",  # avg 8.5 vs Kimi 7.0
    "add-accessibility":    "claude-haiku",  # avg 8.5 vs Kimi 7.5
    "verify-contrast":      "claude-haiku",  # avg 7.5 vs Kimi 7.0
    "add-interactivity":    "claude-haiku",  # best JS generation
}

# Default model for any action not in the routing table
DEFAULT_MODEL = "kimi-k2.5"


class ModelRouter:
    """Routes each action to the optimal model based on eval data."""

    def __init__(
        self,
        models: dict[str, ModelConfig],
        routing: Optional[dict[str, str]] = None,
        default: str = DEFAULT_MODEL,
    ):
        self.models = models
        self.routing = routing or ACTION_ROUTING
        self.default = default

    def get_model_for_action(self, action_name: str) -> tuple[str, ModelConfig]:
        """Return (model_name, model_config) for the given action.

        Falls back to default model if action not in routing table
        or if the routed model is not available.
        """
        model_name = self.routing.get(action_name, self.default)

        # Fall back if model not available
        if model_name not in self.models or not self.models[model_name].enabled:
            model_name = self.default
            if model_name not in self.models or not self.models[model_name].enabled:
                # Use first available model
                for name, config in self.models.items():
                    if config.enabled:
                        return name, config
                raise ValueError("No enabled models available")

        return model_name, self.models[model_name]

    def get_routing_plan(self, action_names: list[str]) -> list[dict]:
        """Generate a routing plan showing which model handles each action.

        Returns list of {action, model, provider, reason}.
        """
        plan = []
        for action in action_names:
            model_name, config = self.get_model_for_action(action)
            reason = "routed (eval data)" if action in self.routing else "default"
            plan.append({
                "action": action,
                "model": model_name,
                "provider": config.provider,
                "reason": reason,
            })
        return plan

    def get_cost_estimate(self, action_names: list[str], avg_tokens: int = 5000) -> dict:
        """Estimate cost for the routing plan.

        Args:
            action_names: List of action names.
            avg_tokens: Average tokens per action (input + output).

        Returns:
            Dict with per-model costs and total.
        """
        model_counts: dict[str, int] = {}
        for action in action_names:
            model_name, _ = self.get_model_for_action(action)
            model_counts[model_name] = model_counts.get(model_name, 0) + 1

        # Approximate costs per 1M tokens
        COST_PER_1M = {
            "kimi-k2.5": 0.45 + 2.20,       # input + output (OpenRouter)
            "deepseek-v3.2": 0.26 + 0.38,    # input + output (OpenRouter)
            "claude-haiku": 0.0,              # Max subscription (free)
        }

        costs = {}
        total = 0.0
        for model, count in model_counts.items():
            tokens = count * avg_tokens
            cost = (tokens / 1_000_000) * COST_PER_1M.get(model, 0)
            costs[model] = {"actions": count, "est_tokens": tokens, "est_cost_usd": cost}
            total += cost

        return {"per_model": costs, "total_cost_usd": total}

    def summary(self) -> str:
        """Human-readable routing summary."""
        kimi_actions = [a for a, m in self.routing.items() if m == "kimi-k2.5"]
        haiku_actions = [a for a, m in self.routing.items() if m == "claude-haiku"]

        lines = [
            "Multi-Model Routing Plan",
            "=" * 40,
            f"\nKimi K2.5 ({len(kimi_actions)} actions — visual/image tasks):",
        ]
        for a in kimi_actions:
            lines.append(f"  - {a}")

        lines.append(f"\nClaude Haiku ({len(haiku_actions)} actions — text/structure/reasoning):")
        for a in haiku_actions:
            lines.append(f"  - {a}")

        lines.append(f"\nDefault fallback: {self.default}")
        return "\n".join(lines)
