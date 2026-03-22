# Stage 5: Eval Pack Build (Figma Prototype)

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 5 of 6
**Status**: PENDING
**Dependencies**: Stage 4 (HITL Solution Approval)
**Blocks**: Stage 6 (HITL Eval Prototype Review)

---

## Objective

Implement the eval pack for the Figma-to-Template prototype stage. This includes the CLI tool, dataset creation, scoring rubrics, refinement engine, Bedrock integration, and run versioning.

---

## Environment Configuration

### DEV (Eval Execution)
| Setting | Value |
|---------|-------|
| AWS Account | 536580886816 |
| Bedrock Region | us-east-1 (cross-region for model access) |
| S3 Bucket | 3-0-site-builder-eval-dev |
| AWS Profile | Tebogo-dev |

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 5.1 | Project Scaffold & Config | PENDING | worker-1 | Create `3_site_builder_agent_eval/` repo, pyproject.toml, CLAUDE.md, folder structure | Repo skeleton |
| 5.2 | CLI Core & Runners | PENDING | worker-2 | Click CLI, Bedrock runner adapter, model invocation, response collection | `cli/main.py`, `cli/runners/` |
| 5.3 | Dataset Creation | PENDING | worker-3 | JSONL datasets for Figma-to-Template using user-supplied Figma templates | `datasets/figma_to_template/` |
| 5.4 | Judge & Scoring Engine | PENDING | worker-4 | Claude judge integration, rubric loading, per-prompt scoring, composite scoring | `cli/judges/`, `rubrics/` |
| 5.5 | Refinement Engine | PENDING | worker-5 | Teacher model loop, diff generation, accept/reject UX, skill file patching | `cli/refiners/` |
| 5.6 | Infrastructure & Versioning | PENDING | worker-6 | Terraform (S3, IAM), run versioning, Bedrock JSONL export, report generation | `terraform/`, `cli/reporters/` |

---

## Detailed Task Specifications

### 5.1 Project Scaffold & Config

**TDD**: Write tests first for config loading, directory creation, validation.

**Deliverables**:
- `3_site_builder_agent_eval/` directory structure (per main-plan.md)
- `pyproject.toml` with dependencies (click, boto3, pyyaml, rich, difflib)
- `CLAUDE.md` with eval pack instructions
- `.gitignore` (exclude runs/, .env, terraform state)
- `tests/test_cli.py` - CLI smoke tests (RED first)
- Config schema (YAML) with defaults

### 5.2 CLI Core & Runners

**TDD**: Write failing tests for `eval-cli run`, runner invocation, response parsing.

**Implementation**:
```python
# cli/main.py
@click.group()
def cli(): pass

@cli.command()
@click.option('--model', type=click.Choice(['deepseek-r1', 'kimi-k2.5', 'all']))
@click.option('--stage', type=click.Choice(['figma', 'generation', 'deployment', 'all']))
@click.option('--dataset', type=click.Path(exists=True))
@click.option('--rubric', type=click.Path(exists=True))
@click.option('--judge', default='claude-sonnet')
@click.option('--output-dir', default=None)  # Auto-generates timestamp
@click.option('--bedrock-region', default='us-east-1')
def run(model, stage, dataset, rubric, judge, output_dir, bedrock_region):
    ...
```

**Runner Adapter Interface**:
```python
class BaseRunner(ABC):
    @abstractmethod
    def invoke(self, prompt: str, params: dict) -> RunnerResponse: ...

class BedrockRunner(BaseRunner):
    def __init__(self, model_id: str, region: str): ...
    def invoke(self, prompt: str, params: dict) -> RunnerResponse: ...
```

**Bedrock Model IDs**:
- DeepSeek R1: `deepseek.r1-v1:0`
- Kimi K2.5: `moonshotai.kimi-k2.5`
- Claude Sonnet (judge): `anthropic.claude-sonnet-4-20250514` or latest
- Claude Opus (teacher): `anthropic.claude-opus-4-20250514` or latest

### 5.3 Dataset Creation

**TDD**: Write validation tests for JSONL schema compliance.

**Process**:
1. User supplies Figma template file keys
2. Create JSONL entries per category (extraction, html_gen, colour, font, logo, layout, staging, e2e)
3. Each entry: `{"prompt": "...", "referenceResponse": "...", "category": "figma_extraction"}`
4. Golden outputs derived from existing MCP facade tool outputs (known-good responses)
5. Validate all entries against Bedrock JSONL schema

**BLOCKER**: Requires user-supplied Figma templates. Placeholder dataset created with synthetic entries until templates provided.

### 5.4 Judge & Scoring Engine

**TDD**: Write tests for rubric loading, score calculation, judge prompt construction.

**Judge Flow**:
1. Load rubric YAML for the category
2. Construct judge prompt: system + rubric + prompt + model_response + reference_response
3. Invoke Claude (judge) via Bedrock
4. Parse structured JSON score response
5. Calculate composite score (weighted dimensions)
6. Write to `scores.json`

**Judge Prompt Template**:
```
You are evaluating an AI model's response to a site builder task.

## Rubric
{rubric_yaml}

## Original Prompt
{prompt}

## Expected Response
{reference_response}

## Model Response
{model_response}

## Instructions
Score each dimension 0-5. Return JSON:
{
  "dimensions": {
    "correctness": {"score": N, "reasoning": "..."},
    "completeness": {"score": N, "reasoning": "..."},
    ...
  },
  "composite_score": N,
  "overall_reasoning": "..."
}
```

### 5.5 Refinement Engine

**TDD**: Write tests for diff generation, skill patching, convergence detection.

**Teacher Model Flow**:
1. Load low-scoring prompts from `scores.json` (below target_score)
2. For each low-scoring skill:
   - Read current skill file from `3_site_builder_agent/skills/`
   - Construct teacher prompt with skill text + eval results
   - Teacher proposes changes as structured JSON
   - Generate unified diff
   - Save to `runs/*/diffs/`
3. Present diffs to user via CLI:
   ```
   === Proposed Changes for figma_design_extraction.skill.md ===
   Score: 2.8 → estimated 3.5+

   --- a/skills/figma_design_extraction.skill.md
   +++ b/skills/figma_design_extraction.skill.md
   @@ -45,7 +45,9 @@
    ... diff content ...

   [A]ccept / [R]eject / [S]kip / [Q]uit:
   ```
4. Apply accepted diffs
5. Re-run eval automatically
6. Report score delta

### 5.6 Infrastructure & Versioning

**TDD**: Write tests for run directory creation, config snapshotting, report generation.

**Terraform** (`terraform/main.tf`):
```hcl
resource "aws_s3_bucket" "eval" {
  bucket = "3-0-site-builder-eval-dev"
}

resource "aws_iam_role" "eval" {
  name = "site-builder-eval-role"
  # Bedrock invoke + S3 permissions
}
```

**Run Versioning**:
- Auto-create `runs/YYYYMMDD_HHMMSS/` on each `eval-cli run`
- Snapshot config, dataset path, model, rubric into `config.json`
- Track parent_run for refinement chains
- `eval-cli history` reads all run dirs and displays score table

**Report Generation** (`cli/reporters/markdown_report.py`):
- Per-model score summary
- Per-category breakdown
- Score trajectory (if refinement run)
- Proposed skill changes summary
- Bedrock export readiness status

---

## Prerequisites (per Environment)

### DEV
- [ ] Bedrock model access enabled for DeepSeek R1, Kimi K2.5, Claude Sonnet/Opus in us-east-1
- [ ] S3 bucket created via Terraform
- [ ] IAM role created via Terraform
- [ ] User has supplied at least 1 Figma template for dataset creation

---

## Acceptance Criteria

- [ ] `eval-cli run --model all --stage figma` executes successfully against Bedrock
- [ ] Scores are generated for all dataset entries per model
- [ ] `eval-cli refine --run <dir>` produces skill enhancement diffs
- [ ] `eval-cli apply --run <dir> --mode interactive` presents accept/reject UX
- [ ] Applied changes update skill files in `3_site_builder_agent/skills/`
- [ ] Re-run shows measurable score change
- [ ] `eval-cli export --run <dir>` produces valid Bedrock JSONL
- [ ] All runs versioned in timestamped folders
- [ ] All code has passing tests (TDD)

---

## Navigation

**Previous Stage**: [Stage 4: HITL Solution Approval](stage-4-hitl-solution.md)
**Next Stage**: [Stage 6: HITL Eval Prototype Review](stage-6-hitl-eval-prototype.md)
