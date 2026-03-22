# Stage 1 Summary: Research Findings

**Stage**: 1 of 6
**Status**: COMPLETE
**Workers**: 4/4 Complete
**Date**: 2026-03-21

---

## Worker 1: Bedrock Evaluations Deep Dive

### Key Findings

1. **BYOI is the core pattern** — We pre-generate responses from DeepSeek/Kimi locally via `InvokeModel`, then feed prompt+response pairs to the Bedrock judge via `CreateEvaluationJob`. This gives us CLI on-demand eval AND Bedrock managed eval compatibility.

2. **Custom metrics** — Up to 10 custom metrics per job, each with a 5,000-char prompt. We can define domain-specific rubrics (HTML quality, CSS variable compliance, content preservation, accessibility) as custom metrics with structured rating scales (0-5).

3. **JSONL schema** — Simple: `{"prompt": "...", "referenceResponse": "...", "category": "...", "modelResponses": [{"response": "...", "modelIdentifier": "..."}]}`. Max 1,000 prompts per job.

4. **Judge models** — Claude 3.5 Sonnet v2 and Claude 3.7 Sonnet are supported as evaluator models for both built-in and custom metrics. Claude 4.x NOT listed as judge yet.

5. **IAM** — Service role needs `bedrock:InvokeModel` + S3 read/write. Trust policy for `bedrock.amazonaws.com`.

6. **Cost** — No service fee. Only model invocation costs. A 100-prompt eval with 3 custom metrics using Claude 3.5 Haiku as judge costs ~$1.13.

### Implications for Design
- Build CLI runner that calls Bedrock `InvokeModel` for generators, stores responses locally
- Export to BYOI JSONL format for Bedrock managed eval jobs
- Use Claude 3.7 Sonnet as judge (supported, high quality)
- Claude Opus 4.6 as teacher for refinement (NOT as Bedrock judge — use directly via API)

---

## Worker 2: Agent Eval Frameworks Survey

### Top 3 Patterns to Adopt

| Pattern | Source | How We'll Use It |
|---------|--------|-----------------|
| **Task abstraction** (Dataset + Solver + Scorer) | Inspect AI | Core eval architecture |
| **Declarative YAML config** | promptfoo | Eval suite definitions, version-controlled |
| **Experiment tracking** (run comparison, scoring over time) | Braintrust | Timestamped runs with delta reporting |

### Additional Patterns
- **Assertion guardrails** (promptfoo): Hard pass/fail checks (valid HTML, no XSS, required sections) alongside soft scoring
- **Multi-metric scoring pipeline** (Inspect AI + DeepEval): Independent scores per dimension, aggregated into composite
- **LLM-as-judge with structured rubrics** (Inspect AI): Chain-of-thought judge prompts with explicit criteria

### Framework Decision
**Build custom** — No single framework covers all needs (Bedrock BYOI + CLI + refinement loop + skill patching). Cherry-pick patterns from Inspect AI, promptfoo, and Braintrust.

---

## Worker 3: Skill Analysis & Golden Outputs

### Skills Mapped to Eval Categories

| Skill | Primary MCP Tool | Eval Category | Key Quality Dimensions |
|-------|-----------------|---------------|----------------------|
| `figma_design_extraction` | `figma_get_design_context` | `figma_extraction` | Correct tool call, all 7 data categories extracted, no manual URL parsing |
| `template_customization` | `template_apply_changes` | `customization` | CSS variables only (no hardcoded), all content replaced, meta tags updated, HTML escaped |
| `template_staging` | `template_copy` | `staging` | Both mandatory params validated, never assumes, version tracked |
| `colour_management` | `template_apply_changes` | `colour_application` | Full inventory scan, dark/light variants, RGB versions, hardcoded fixed, WCAG AA validated |
| `global_font_management` | `template_apply_changes` | `font_application` | Google Fonts link correct, standardized var names, fallback stacks, font-display: swap |
| `logo_replacement` | `template_replace_file` | `logo_replacement` | ALL instances replaced (header+footer), alt text, aria-labels, CSS sizing preserved |
| `background_image_changer` | `template_replace_file` | `image_replacement` | Full inventory by section, overlay preserved, backup, WebP generated |
| `layout_transformation` | `template_apply_changes` | `layout_transform` | Content 100% preserved, responsive 3 breakpoints, semantic HTML, ARIA preserved |

### Cross-Cutting Rubric (0-5 scale)

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Correctness | 30% | Output matches expected behavior |
| Completeness | 25% | All required elements present |
| Format Compliance | 20% | Follows skill output format |
| Code Quality | 15% | HTML/CSS validity, accessibility |
| Instruction Following | 10% | Adheres to skill instructions |

### Critical Finding
`template_apply_changes` is the workhorse tool — used by 5 of 8 skills. Eval must verify models use batched changes (single tool call) rather than sequential calls.

---

## Worker 4: Model Capability Mapping

### Model Comparison

| Dimension | DeepSeek R1 | DeepSeek V3.2 | Kimi K2.5 |
|-----------|-------------|---------------|-----------|
| HumanEval | ~80% | Not published | **99%** |
| IFEval | Not published | Not published | **94%** |
| Context | 128K in / 8K out | 128K in / 8K out | 128K in / **16K out** |
| Image input | No | No | **Yes** |
| Tool calling (Bedrock) | **No** | Client-side | Client-side (buggy) |
| Reasoning mode | Yes (`<think>`) | No | No |
| Pricing (in/out per 1M) | $1.35 / $5.40 | **$0.74 / $2.22** | $0.60 / $3.00 |

### Best Model per Skill

| Skill | Best Candidate | Why |
|-------|----------------|-----|
| `figma_design_extraction` | **Kimi K2.5** | Multimodal — can process Figma screenshots |
| `template_customization` | **DeepSeek V3.2** | Fast, direct, cheapest |
| `colour_management` | **DeepSeek V3.2** | CSS variable manipulation is straightforward |
| `font_management` | **DeepSeek V3.2** | Direct CSS changes, no reasoning needed |
| `layout_transformation` | **DeepSeek R1** | Complex reasoning benefits chain-of-thought |
| `logo_replacement` | **DeepSeek V3.2** | Simple search-and-replace |
| `background_image_changer` | **Kimi K2.5** | Visual verification of placement |
| `template_staging` | **DeepSeek V3.2** | Simple file operations |

### Critical Risks

| Risk | Model | Mitigation |
|------|-------|-----------|
| 8K output truncates full-page HTML | DeepSeek R1/V3.2 | Use Kimi K2.5 (16K) for full-page tasks, or split into sections |
| No tool calling on Bedrock | DeepSeek R1 | Use text-based extraction, not function-calling |
| Converse API bugs (premature end_turn) | Kimi K2.5 | Fall back to `InvokeModel` API |
| Reasoning tokens billed as output | DeepSeek R1 | Strip `<think>` blocks; budget 3x output tokens |
| No models in eu-west-1 or af-south-1 | All | Run evals from `us-east-1` |

### Cost Estimate per Full Eval Run (100 prompts, 3 models)
- DeepSeek R1: ~$4.90
- DeepSeek V3.2: ~$2.10
- Kimi K2.5: ~$2.60
- Claude Sonnet judge (300 outputs): ~$13.20
- Claude Opus teacher (20 refinement iterations): ~$4.40
- **Total: ~$27 per eval cycle**

---

## Consolidated Recommendations for Stage 3 (Solution Design)

### Architecture
1. **Custom Python CLI** — Cherry-pick patterns (Inspect AI tasks, promptfoo YAML, Braintrust tracking)
2. **Hybrid execution** — CLI on-demand (InvokeModel) + Bedrock managed (BYOI JSONL export)
3. **Region**: `us-east-1` for all eval infrastructure

### Eval Flow
```
YAML config → CLI runner → InvokeModel (generators) → Store responses →
Judge (Claude 3.7 Sonnet) → Scores → Teacher (Claude Opus 4.6) →
Skill diffs → HITL accept/reject → Apply → Re-run → Compare
```

### Scoring
- 5 dimensions, weighted composite (0-5 scale)
- Hard assertions (valid HTML, no content loss) as guardrails
- Custom Bedrock metrics for managed eval export

### Models
- **Generators**: DeepSeek R1 + V3.2 + Kimi K2.5 (all three, each has strengths)
- **Judge**: Claude 3.7 Sonnet (Bedrock-supported evaluator) at temperature 0.0
- **Teacher/Refiner**: Claude Opus 4.6 (direct API, not Bedrock eval) for skill enhancement

### Dataset
- JSONL per category (8 categories for Figma-to-Template)
- Max 1,000 prompts per job (Bedrock limit)
- Golden outputs from MCP facade tool responses + manual curation
