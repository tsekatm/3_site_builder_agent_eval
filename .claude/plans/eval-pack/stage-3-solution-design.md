# Stage 3: Solution Design & Architecture

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 3 of 6
**Status**: PENDING
**Dependencies**: Stage 2 (HITL Research Approval)
**Blocks**: Stage 4 (HITL Solution Approval)

---

## Objective

Design the complete eval pack architecture: CLI tool, dataset schema, scoring rubrics, refinement engine, Bedrock integration, and run versioning system. Produce implementation-ready specifications.

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 3.1 | CLI Architecture Design | PENDING | worker-1 | Click CLI structure, commands, flags, config, runner adapters | `worker-1/output.md` |
| 3.2 | Dataset Schema Design | PENDING | worker-2 | JSONL schema for each eval stage, golden outputs format, Bedrock compatibility mapping | `worker-2/output.md` |
| 3.3 | Scoring Rubric Design | PENDING | worker-3 | YAML rubric format, per-skill scoring dimensions, composite scoring, threshold definitions | `worker-3/output.md` |
| 3.4 | Refinement Engine Design | PENDING | worker-4 | Teacher model prompting strategy, diff generation, accept/reject UX, re-run loop, convergence criteria | `worker-4/output.md` |
| 3.5 | Infrastructure & Integration Design | PENDING | worker-5 | Terraform (S3 bucket, IAM role), Bedrock BYOI export, run versioning, CI/CD integration | `worker-5/output.md` |

---

## Detailed Task Specifications

### 3.1 CLI Architecture Design

**Goal**: Design a Python Click CLI that orchestrates eval runs.

**Commands to Design**:
```
eval-cli run                    # Run eval against specified model(s)
  --model deepseek-r1|kimi-k2.5|all
  --stage figma|generation|deployment|all
  --dataset <path-to-jsonl>
  --rubric <path-to-rubric-yaml>
  --judge claude-sonnet|claude-opus
  --output-dir <path>           # Default: runs/YYYYMMDD_HHMMSS/
  --bedrock-region us-east-1

eval-cli refine                 # Run teacher model refinement
  --run <run-dir>               # Path to completed run
  --teacher claude-opus
  --target-score 4.0            # Minimum acceptable score
  --max-iterations 5

eval-cli apply                  # Apply skill enhancements
  --run <run-dir>
  --mode all|interactive        # Accept all or cherry-pick
  --skills-dir <path>           # Target skills directory

eval-cli export                 # Export for Bedrock managed eval
  --run <run-dir>
  --format bedrock-jsonl
  --output <path>

eval-cli compare                # Compare two runs
  --run-a <run-dir>
  --run-b <run-dir>

eval-cli history                # List all runs with scores
  --stage figma|generation|deployment
  --limit 10
```

**Design Deliverables**:
- Command tree with all flags and defaults
- Configuration file format (YAML)
- Runner adapter interface (abstract base class)
- Bedrock client wrapper (invoke model, handle streaming)
- Error handling strategy
- Logging and progress reporting

### 3.2 Dataset Schema Design

**Goal**: Define the exact JSONL schema for Figma-to-Template evaluation.

**Dataset Categories for Stage 1 (Figma-to-Template)**:

| Category | Description | Prompt Type | Expected Output Type |
|----------|-------------|-------------|---------------------|
| `figma_extraction` | Extract design tokens from Figma JSON | Figma node JSON + skill prompt | Structured design tokens (colors, fonts, spacing) |
| `html_generation` | Generate HTML from extracted tokens | Design tokens + template ref | Valid HTML/CSS file |
| `colour_application` | Apply colour scheme to template | Template HTML + colour palette | Modified HTML with CSS variables |
| `font_application` | Apply font stack to template | Template HTML + font config | Modified HTML with @font-face |
| `logo_replacement` | Replace placeholder logos | Template HTML + logo URLs | Modified HTML with correct img src |
| `layout_transform` | Transform layout pattern | Template HTML + layout spec | Restructured HTML with new layout |
| `template_staging` | Stage modified template to S3 | Template files + staging config | S3 upload commands + staging URL |
| `end_to_end` | Full Figma-to-staged pipeline | Figma file key + brand config | Staged, viewable template |

**Schema Design Deliverables**:
- JSONL schema per category with field definitions
- Golden output format and storage strategy
- Validation rules (JSON schema for JSONL validation)
- Bedrock `CreateEvaluationJob` compatibility mapping
- Sample dataset entries (3-5 per category)

### 3.3 Scoring Rubric Design

**Goal**: Define how each model response is scored.

**Rubric Dimensions per Category**:

| Dimension | Weight | Description | 0 (Fail) | 3 (Acceptable) | 5 (Excellent) |
|-----------|--------|-------------|-----------|-----------------|----------------|
| Correctness | 30% | Output matches expected behavior | Wrong output or errors | Mostly correct with minor issues | Exact match or better |
| Completeness | 25% | All required elements present | Major elements missing | Most elements present | All elements present |
| Format Compliance | 20% | Follows skill output format | Wrong format | Mostly correct format | Perfect format |
| Code Quality | 15% | HTML/CSS validity, best practices | Invalid code | Valid but verbose | Clean, semantic, accessible |
| Instruction Following | 10% | Adheres to skill instructions | Ignores instructions | Partially follows | Exact adherence |

**Composite Score**: Weighted average across dimensions.

**Thresholds**:
- `< 2.0`: FAIL - Major issues, skill needs significant rework
- `2.0 - 3.0`: BELOW_THRESHOLD - Refinement needed
- `3.0 - 4.0`: ACCEPTABLE - Minor improvements possible
- `4.0 - 5.0`: EXCELLENT - Skill performs well with this model

**Design Deliverables**:
- YAML rubric format specification
- Per-category rubric definitions
- Composite scoring algorithm
- Judge prompt template (how Claude scores using the rubric)
- Score interpretation guide

### 3.4 Refinement Engine Design

**Goal**: Design the teacher model loop that improves skills based on eval results.

**Refinement Loop**:
```
1. Run eval → scores.json
2. Identify skills scoring < target_score
3. For each low-scoring skill:
   a. Teacher model analyzes: skill text + prompt + model response + score + rubric
   b. Teacher proposes enhancement (diff to skill.md)
   c. Diff saved to runs/*/diffs/
4. Present diffs to user (HITL)
5. User accepts all / cherry-picks
6. Apply accepted diffs to skills/*.skill.md
7. Re-run eval → new scores.json
8. Compare scores (improvement delta)
9. If target_score not met AND iterations < max → goto 3
10. Final report with score trajectory
```

**Teacher Model Prompt Strategy**:
- System prompt: "You are a prompt engineering expert specializing in agent skill optimization"
- Include: current skill text, eval prompt, model response, expected response, score, rubric
- Output: structured JSON with `reasoning`, `proposed_changes[]`, `expected_improvement`
- Each change: `{section, old_text, new_text, rationale}`

**Design Deliverables**:
- Refinement loop state machine
- Teacher model prompt templates
- Diff format specification (unified diff compatible)
- Accept/reject CLI UX (interactive mode with `y/n/s(kip)/q(uit)`)
- Convergence criteria (score plateau detection)
- Score trajectory visualization (markdown table per iteration)

### 3.5 Infrastructure & Integration Design

**Goal**: Design the Terraform, Bedrock export, and versioning infrastructure.

**Terraform Resources**:
- S3 bucket: `3-0-site-builder-eval-dev` (datasets, results, exports)
- IAM role: `site-builder-eval-role` (Bedrock invoke, S3 read/write)
- IAM policy: scoped to specific Bedrock model ARNs + S3 bucket ARN

**Run Versioning**:
```
runs/
├── 20260321_143000/            # First run
│   ├── config.json             # Frozen run config
│   ├── scores.json             # Scores per prompt per model
│   ├── responses/              # Raw model responses
│   │   ├── deepseek_r1/
│   │   └── kimi_k2_5/
│   ├── diffs/                  # Proposed skill changes
│   ├── report.md               # Human-readable summary
│   └── bedrock_export.jsonl    # Bedrock-compatible export
│
├── 20260321_150000/            # Refinement run 1
│   ├── config.json
│   ├── scores.json
│   ├── parent_run: "20260321_143000"  # Links to parent
│   └── ...
```

**Design Deliverables**:
- Terraform module specification
- S3 folder structure
- Run config schema (JSON)
- Bedrock JSONL export mapping
- Git integration (auto-commit skill changes after apply)

---

## Acceptance Criteria

- [ ] CLI command tree fully specified with all flags, defaults, and examples
- [ ] JSONL dataset schema validated against Bedrock `CreateEvaluationJob` requirements
- [ ] Scoring rubrics defined for all 8 Figma-to-Template categories
- [ ] Refinement engine loop fully specified with teacher prompts and convergence criteria
- [ ] Terraform resources defined following naming conventions
- [ ] Run versioning schema supports parent-child relationships (refinement chains)

---

## Navigation

**Previous Stage**: [Stage 2: HITL Research Approval](stage-2-hitl-research.md)
**Next Stage**: [Stage 4: HITL Solution Approval](stage-4-hitl-solution.md)
