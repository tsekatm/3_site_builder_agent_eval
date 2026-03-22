# Site Builder Agent Eval Pack

## Project Purpose

Evaluation pipeline for site builder agent skills. Tests agent skill quality against configurable Bedrock models (DeepSeek, Kimi K2.5, and any future models), uses Claude as teacher/judge for scoring and prompt refinement, and outputs actionable skill enhancement diffs through an iterative HITL refinement loop.

## Pipeline Deployment Tiers

| Tier | Name | Description |
|------|------|-------------|
| Tier 1 | IDE / Local | Runs entirely on developer machine, Bedrock API calls only |
| Tier 2 | Hybrid | Triggered from local CLI, executes on AWS (S3, Bedrock managed eval) |
| Tier 3 | Cloud | Fully hosted on AWS (Step Functions, Lambda, EventBridge) |

## Eval Pipeline Stages (Prototyped Sequentially)

1. **Figma-to-Template** (current prototype)
2. Site Generation (future)
3. Deployment (future)

## Key Rules

- **Models are configurable** — defined in `eval_config.yaml`, not hardcoded
- **Parallel execution** — multiple models and prompts run concurrently
- **HITL at every step** — no stage proceeds without user verification
- **TDD** — all code follows test-driven development
- **Versioned runs** — every eval run stored in `runs/YYYYMMDD_HHMMSS/`
- **Bedrock-compatible** — JSONL datasets work with `CreateEvaluationJob` BYOI pattern
- **Repository isolation** — this repo is separate from `3_site_builder_agent`

## Environments

| Environment | AWS Account | Bedrock Region | Profile |
|-------------|-------------|----------------|---------|
| DEV | 536580886816 | us-east-1 (cross-region) | Tebogo-dev |

## Related Repositories

| Repo | Purpose |
|------|---------|
| `3_site_builder_agent` | The agent/skills being evaluated |
| `2_bbws_agents` | Shared agent definitions |
| `2_bbws_docs` | HLD/LLD documents |

## Plan Location

`.claude/plans/eval-pack/main-plan.md`

## Root Workflow Inheritance

{{include:../CLAUDE.md}}
