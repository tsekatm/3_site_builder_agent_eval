# Stage 2: HITL - Research Approval

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 2 of 6
**Status**: PENDING
**Dependencies**: Stage 1 (Research)
**Blocks**: Stage 3 (Solution Design)

---

## Objective

Present research findings to user for review and approval before proceeding to solution design. This is a mandatory Human-in-the-Loop gate.

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 2.1 | Research Presentation & Approval | PENDING | worker-1 | Present Stage 1 summary, collect feedback, iterate if needed | `worker-1/output.md` |

---

## Approval Checklist

The user must approve or request changes on:

- [ ] **Bedrock integration approach**: BYOI pattern vs managed eval jobs
- [ ] **Eval framework patterns**: Which patterns to adopt (promptfoo-style CLI? Inspect AI tasks?)
- [ ] **Skill quality rubrics**: Are the scoring dimensions correct? Any missing?
- [ ] **Model selection**: Confirm DeepSeek + Kimi K2.5 + Claude as teacher/judge
- [ ] **Region strategy**: Confirm us-east-1 for eval runs
- [ ] **Dataset format**: JSONL with prompt + referenceResponse + category

## Decision Points

| Decision | Options | Recommendation | User Choice |
|----------|---------|----------------|-------------|
| Primary eval runner | CLI-only / CLI + Bedrock managed / Bedrock-only | CLI + Bedrock managed (hybrid) | TBD |
| Judge model | Claude Sonnet 3.7 / Claude Opus / Both | Claude Sonnet 3.7 (cost-effective judge) | TBD |
| Teacher model (refinement) | Claude Opus / Claude Sonnet | Claude Opus (best reasoning for skill rewrites) | TBD |
| Scoring scale | 0-5 / 0-10 / pass/fail+score | 0-5 (matches Bedrock built-in) | TBD |
| Figma templates source | User-supplied / Figma Community / Both | User-supplied (domain-relevant) | TBD |

---

## Gate Rules

- **BLOCKER**: Cannot proceed to Stage 3 without explicit user approval
- **Iteration**: If user requests changes to research, return to Stage 1 workers
- **Approval format**: User says "approved" / "go" / "proceed" with optional feedback

---

## Navigation

**Previous Stage**: [Stage 1: Research](stage-1-research.md)
**Next Stage**: [Stage 3: Solution Design](stage-3-solution-design.md)
