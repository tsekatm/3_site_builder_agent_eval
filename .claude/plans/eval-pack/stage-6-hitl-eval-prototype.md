# Stage 6: HITL - Figma Eval Prototype Review

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 6 of 6
**Status**: PENDING
**Dependencies**: Stage 5 (Eval Pack Build)
**Blocks**: None (final stage for prototype; future stages for Site Generation and Deployment)

---

## Objective

Execute the first real eval run against DeepSeek and Kimi K2.5 using the user-supplied Figma templates. Present results, demonstrate the refinement loop, and collect user feedback on the eval pack.

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 6.1 | First Eval Run & Review | PENDING | worker-1 | Run eval against DeepSeek + Kimi, present results, demo refinement loop | `worker-1/output.md` |

---

## Execution Plan

### Step 1: Baseline Eval Run
```bash
# Run eval against all models for Figma stage
eval-cli run --model all --stage figma --rubric rubrics/figma_extraction.yaml --judge claude-sonnet

# Output: runs/YYYYMMDD_HHMMSS/ with scores, responses, report
```

### Step 2: Present Results to User
- Model comparison table (DeepSeek R1 vs Kimi K2.5)
- Per-category score breakdown
- Worst-performing skills identified
- Sample responses side-by-side

### Step 3: Refinement Loop Demo
```bash
# Teacher model generates skill improvements
eval-cli refine --run runs/YYYYMMDD_HHMMSS/ --teacher claude-opus --target-score 4.0 --max-iterations 3

# User reviews and accepts/rejects changes
eval-cli apply --run runs/YYYYMMDD_HHMMSS/ --mode interactive --skills-dir ../3_site_builder_agent/skills/

# Re-run eval to measure improvement
eval-cli run --model all --stage figma --rubric rubrics/figma_extraction.yaml --judge claude-sonnet
```

### Step 4: Score Comparison
```bash
# Compare baseline vs refined
eval-cli compare --run-a runs/YYYYMMDD_143000/ --run-b runs/YYYYMMDD_150000/
```

### Step 5: Bedrock Export Validation
```bash
# Export for Bedrock managed eval
eval-cli export --run runs/YYYYMMDD_HHMMSS/ --format bedrock-jsonl --output bedrock_eval.jsonl

# Validate by creating a Bedrock eval job (dry run)
aws bedrock create-evaluation-job --cli-input-json file://bedrock_job_config.json --dry-run
```

---

## Review Checklist

The user evaluates:

- [ ] **Scores are meaningful**: Do the rubric scores correlate with actual quality?
- [ ] **Model comparison is fair**: Are prompts and conditions equal across models?
- [ ] **Refinement improves scores**: Did the teacher model's changes actually help?
- [ ] **Diffs are actionable**: Are the proposed skill changes sensible and specific?
- [ ] **Accept/reject UX works**: Can user cherry-pick changes easily?
- [ ] **Run versioning is useful**: Can user compare across runs?
- [ ] **Bedrock export is valid**: JSONL passes Bedrock validation?

## Success Metrics for Prototype

| Metric | Target | Measurement |
|--------|--------|-------------|
| Eval run completes | 100% prompts scored | No errors/timeouts |
| Score reproducibility | < 0.3 variance across 3 runs | Same prompt, same model |
| Refinement improvement | > 0.5 point increase | Baseline vs refined score |
| Bedrock compatibility | Valid JSONL export | Bedrock accepts dataset |
| User satisfaction | Thumbs up | Qualitative feedback |

---

## Future Stages (Out of Scope for Prototype)

After Figma-to-Template prototype is validated, the following stages will be planned:

| Stage | Pipeline Phase | Skills to Evaluate |
|-------|---------------|-------------------|
| Site Generation | Phase 2 | template_customization, html_generation, web_design_fundamentals |
| Deployment | Phase 3 | site_staging, site_deployment, S3 sync, CloudFront invalidation |

Each future stage follows the same pattern: dataset creation → eval run → refinement loop → skill enhancement.

---

## Navigation

**Previous Stage**: [Stage 5: Eval Pack Build](stage-5-eval-pack-build.md)
**Next Stage**: None (prototype complete; future: Site Generation eval, Deployment eval)
