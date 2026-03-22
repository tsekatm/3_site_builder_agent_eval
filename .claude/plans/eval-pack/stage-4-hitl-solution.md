# Stage 4: HITL - Solution Approval

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 4 of 6
**Status**: PENDING
**Dependencies**: Stage 3 (Solution Design)
**Blocks**: Stage 5 (Eval Pack Build)

---

## Objective

Present the complete solution design to user for approval before implementation begins. This is the final design gate before writing code.

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 4.1 | Solution Presentation & Approval | PENDING | worker-1 | Present Stage 3 architecture, collect feedback, iterate | `worker-1/output.md` |

---

## Approval Checklist

The user must approve or request changes on:

- [ ] **CLI command structure**: Commands, flags, defaults
- [ ] **Dataset schema**: JSONL format, categories, golden outputs
- [ ] **Scoring rubrics**: Dimensions, weights, thresholds
- [ ] **Refinement engine**: Teacher prompt strategy, diff format, convergence criteria
- [ ] **Infrastructure**: Terraform resources, S3 structure, IAM
- [ ] **Folder structure**: `3_site_builder_agent_eval/` layout
- [ ] **Run versioning**: Timestamped folders, parent-child linking

## Critical Decision Points

| Decision | Description | Impact |
|----------|-------------|--------|
| Target score threshold | What score constitutes "good enough" to stop refining? | Determines refinement loop iterations |
| Max refinement iterations | Safety limit on teacher model loop | Cost control |
| Figma template count | How many templates for prototype eval? | Dataset size and coverage |
| Skill scope for prototype | All 8 Figma skills or subset? | Implementation scope |
| Bedrock managed eval: now or later? | Build BYOI export now or defer? | Stage 5 scope |

---

## Gate Rules

- **BLOCKER**: Cannot proceed to Stage 5 without explicit user approval
- **Iteration**: If user requests design changes, return to Stage 3 workers
- **Scope changes**: Any scope expansion must be explicitly approved

---

## Navigation

**Previous Stage**: [Stage 3: Solution Design](stage-3-solution-design.md)
**Next Stage**: [Stage 5: Eval Pack Build](stage-5-eval-pack-build.md)
