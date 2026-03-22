# EVAL-PACK-001: Research Report (v2)

**Project**: Site Builder Agent Evaluation Pack
**Stage**: 1 (Research)
**Status**: COMPLETE
**Date**: 2026-03-22 (revised from 2026-03-21)
**HITL Verified**: PENDING

---

## Table of Contents

1. [Folder-Based Site Evaluation](#1-folder-based-site-evaluation)
2. [Visual & Rendered Site Evaluation](#2-visual--rendered-site-evaluation)
3. [Violation-Based Scoring (10 Minus Deductions)](#3-violation-based-scoring)
4. [LLM-as-Judge for Multi-File Artifacts](#4-llm-as-judge-for-multi-file-artifacts)
5. [Expected Outcome Validation (Gold Standards)](#5-expected-outcome-validation)
6. [Agent Runtime Proxy Routing](#6-agent-runtime-proxy-routing)
7. [Bedrock Evaluations Integration](#7-bedrock-evaluations-integration)
8. [Model Capability Mapping](#8-model-capability-mapping)
9. [Consolidated Recommendations](#9-consolidated-recommendations)

---

# 1. Folder-Based Site Evaluation

## 1.1 How Code/Site Generation Benchmarks Evaluate Multi-File Outputs

**SWE-bench**: Evaluates patches applied to real repos. Model generates a patch, applied to file tree, existing test suite runs. Binary pass/fail. Treats output as structured artifact, not text.

**DevBench**: Evaluates LLMs constructing entire multi-file codebases from a PRD. Covers 22 repos across Python, C/C++, Java, JavaScript. Runs project test suites against generated code.

**Design2Code** (Stanford SALT Lab, NAACL 2025): Most directly relevant. 484 real-world webpages evaluated with:
- **CLIP similarity**: Visual similarity via CLIP embeddings
- **Block-match**: Matched visual element blocks (area comparison)
- **Text matching**: Character-level Sorensen-Dice similarity
- **Position matching**: Element positioning fidelity
- **Color matching**: Color fidelity of matched elements

Code: https://github.com/NoviScl/Design2Code

**Screenshot-to-Code** (abi/screenshot-to-code): 16 reference screenshots, generate code, render, screenshot output, measure "replication accuracy."

## 1.2 Directory Comparison Patterns

| Level | What It Compares | Tools |
|-------|-----------------|-------|
| **Structural** | File tree — expected files present? | `diff -r`, custom tree walker |
| **Content** | File contents — HTML structure, CSS values, text | DOM parser, CSS parser, regex |
| **Hash** | Byte-level identity | MD5/SHA256 checksums |

**Handling non-deterministic parts:**
- Strip timestamps, random IDs, Vite content hashes before comparison
- Parse HTML to DOM tree, serialize to canonical form (eliminates whitespace diffs)
- Compare asset content rather than filenames (content hashes change per build)
- Selective comparison: only compare deterministic sections

## 1.3 Recommended Three-Tier Evaluation

```
Agent Output Folder
        |
        v
[Tier 1: Structural]   ──> File tree validation, required files present
        |
        v
[Tier 2: Content]      ──> HTML/CSS validation, CSS variable checks, text content
        |
        v
[Tier 3: Visual]       ──> Screenshot capture + SSIM/CLIP comparison vs reference
        |
        v
[Tier 4: LLM Judge]    ──> Opus receives: code files + screenshot + reference + rubric
        |                    Returns: structured violation list with deductions
        v
[Score Aggregation]     ──> Final score = 10.0 - sum(deductions), capped at [0, 10]
```

---

# 2. Visual & Rendered Site Evaluation

## 2.1 Visual Regression Tools

| Tool | Type | Key Feature |
|------|------|-------------|
| **Playwright** | Open-source, headless | Built-in `toHaveScreenshot()` with pixelmatch; Chromium/Firefox/WebKit |
| **BackstopJS** | Open-source | Multi-viewport comparison, HTML diff reports |
| **Percy** | Commercial | AI visual review agent, draws bounding boxes, 40% fewer false positives |

## 2.2 Screenshot Comparison Techniques

| Technique | What It Measures | Tolerance | Best For |
|-----------|-----------------|-----------|----------|
| **Pixel diff** (pixelmatch) | Pixel-by-pixel identity | Low (anti-aliasing sensitive) | Same-environment comparison |
| **SSIM** (Structural Similarity) | Luminance, contrast, structure | Medium | "Does it look the same to a human?" |
| **CLIP similarity** | Semantic visual similarity | High | High-level layout/design fidelity |
| **Perceptual diff** | Human perception model | Medium | Cross-browser comparison |

## 2.3 DOM Comparison

Parse both reference and generated HTML into DOM trees, then compare:
- Tree structure (nesting hierarchy, element types)
- Attribute matching (classes, IDs, ARIA)
- Text content (fuzzy matching)
- CSS computed styles (colours, fonts, spacing)

## 2.4 Multimodal LLM as Visual Judge

**WebDevJudge** (2025) key findings:
- Code alone is more informative than screenshots alone for the judge
- **Both code + screenshots together yield the best results**
- 4-dimension Likert scoring: Functionality, UI Quality, Code Quality, Interactivity
- Query-grounded rubric trees achieve 89.7% inter-annotator agreement (vs 63% for MT-Bench)

## 2.5 Consistent Screenshot Capture (Playwright)

```javascript
// Best practices for deterministic screenshots
await page.setViewportSize({ width: 1280, height: 720 });
await page.waitForLoadState('networkidle');
await page.evaluate(() => document.fonts.ready);
// Disable animations
await page.addStyleTag({ content: '* { animation: none !important; transition: none !important; }' });
await page.screenshot({ fullPage: true, path: 'output.png' });
```

---

# 3. Violation-Based Scoring

## 3.1 Scoring Model: 10 Minus Deductions

Start at 10. Deduct for each violation found. Floor at 0.

```
Final Score = max(0, 10.0 - sum(deductions))
```

Follows patterns from SonarQube (technical debt scoring) and axe-core (accessibility severity weighting).

## 3.2 Violation Catalogue

| Category | Violation | Severity | Deduction |
|----------|-----------|----------|-----------|
| **Structural** | Missing required file (index.html) | Critical | -3.0 |
| **Structural** | Missing asset file referenced in HTML | Major | -1.5 |
| **Structural** | Extra/unexpected files | Minor | -0.25 |
| **Structural** | Wrong directory structure | Major | -1.0 |
| **Visual** | Layout completely broken | Critical | -3.0 |
| **Visual** | Significant visual deviation (SSIM < 0.7) | Major | -2.0 |
| **Visual** | Minor visual deviation (SSIM 0.7-0.9) | Moderate | -1.0 |
| **Visual** | Color mismatch vs reference | Moderate | -0.5 |
| **Content** | Missing text content from requirements | Critical | -2.0 |
| **Content** | Incorrect text content | Major | -1.5 |
| **Content** | Placeholder text not replaced | Major | -1.0 |
| **Content** | Missing meta tags | Minor | -0.25 |
| **Code Quality** | Invalid HTML (W3C errors) | Moderate | -0.5/error (max -2.0) |
| **Code Quality** | Invalid CSS | Moderate | -0.5/error (max -2.0) |
| **Code Quality** | Hardcoded values instead of CSS variables | Major | -1.0 |
| **Code Quality** | No responsive breakpoints | Major | -1.5 |
| **Accessibility** | Missing alt text | Serious | -0.5/instance |
| **Accessibility** | Insufficient colour contrast | Serious | -0.5 |
| **Accessibility** | Missing ARIA labels | Moderate | -0.25 |
| **Performance** | Unoptimized images (>500KB) | Minor | -0.25 |
| **Performance** | No font-display: swap | Minor | -0.25 |

## 3.3 Severity Weighting Rationale

| Severity | Deduction Range | Meaning |
|----------|----------------|---------|
| **Critical** | -2.0 to -3.0 | Fundamentally broken — missing core files, completely wrong layout |
| **Major** | -1.0 to -2.0 | Client would reject — wrong content, broken responsive |
| **Moderate** | -0.5 to -1.0 | Noticeable but not deal-breaking — validation errors, minor visual drift |
| **Minor** | -0.25 | Polish issues — missing optimizations, minor accessibility gaps |

---

# 4. LLM-as-Judge for Multi-File Artifacts

## 4.1 Feeding a Folder to the Judge

Inline all file contents in the prompt:
```
## Output Folder Contents

### index.html
[contents]

### css/styles.css
[contents]

### assets/manifest.json
[contents]
```

Context budget for Claude Opus 4.6 (1M context):
- Typical site folder: 10K-50K tokens
- Reference folder: 10K-50K tokens
- Rubric + instructions: 2K-5K tokens
- Screenshot images: 1K-5K tokens each
- **Total**: Well within 1M, even generously

## 4.2 Multimodal Judging: Code + Screenshots

Feed BOTH code files AND rendered screenshots. WebDevJudge research confirms this yields best results — screenshots catch visual issues the judge misses from code alone.

## 4.3 Structured Judge Output

```json
{
  "violations": [
    {
      "id": "V-001",
      "category": "structural",
      "severity": "critical",
      "deduction": -3.0,
      "file": "index.html",
      "description": "Missing closing </body> tag",
      "evidence": "Line 145: file ends without </body>",
      "recommendation": "Add </body></html> closing tags"
    }
  ],
  "total_deductions": -4.5,
  "final_score": 5.5,
  "summary": "Site renders but has structural issues...",
  "dimension_scores": {
    "structural": 7.0,
    "visual": 8.0,
    "content": 6.0,
    "code_quality": 5.5,
    "accessibility": 9.0
  }
}
```

## 4.4 Judge Consistency

- **Temperature 0**: Essential for reproducibility (variance < 0.3 across runs)
- **Structured rubrics**: Dramatically improve consistency vs open-ended evaluation
- **3-run median**: Running judge 3 times, taking median score improves reliability
- **Rubric trees**: Decompose criteria into verifiable sub-criteria (89.7% agreement)

---

# 5. Expected Outcome Validation

## 5.1 Gold Standard Management

**Golden file testing pattern**: Reference output is a committed folder. Tests generate new output and compare against golden files. Update with `--update` flag.

**Workflow:**
1. Agent produces output folder from requirement
2. Automated pre-checks run (structural, HTML/CSS validation, accessibility, screenshot)
3. Human reviewer sees rendered site + code + check results
4. Reviewer approves (becomes gold standard) or rejects
5. Approved gold standard committed to git with metadata

## 5.2 Versioning

- Tag gold standards with template version: `gold/v1.2/` vs `gold/v1.3/`
- When template changes, regenerate, review, and commit new gold standards in same PR
- Layered baselines: full expected output + scenario deltas

## 5.3 Partial Matching (Avoid Brittleness)

| Strategy | What It Checks | Tolerance |
|----------|---------------|-----------|
| Structural assertions | Specific DOM elements exist | High |
| CSS variable assertions | Custom properties set correctly | Low |
| Text content assertions | Key text appears | Medium |
| Regex matching | Predictably varying content | Medium |
| Threshold visual (SSIM > 0.9) | Visual similarity | Configurable |

---

# 6. Agent Runtime Proxy Routing

## 6.1 Current State

Site builder agents run on Claude SDK (`anthropic.Anthropic()`). Direct API calls to Anthropic.

## 6.2 Claude SDK → Bedrock: Drop-In Replacement

```python
# Current (direct API)
client = anthropic.Anthropic(api_key="sk-ant-...")

# Bedrock (drop-in replacement, identical interface)
client = anthropic.AnthropicBedrock(aws_region="us-east-1")

# Same messages.create() call, same tool format, same everything
response = client.messages.create(
    model="anthropic.claude-sonnet-4-20250514-v1:0",  # Bedrock model ID
    ...
)
```

**Key finding**: `AnthropicBedrock` is a near-zero-effort swap for Claude models. Identical interface, only auth and model ID differ.

## 6.3 Proxy Router Options

| Option | Effort | Scope |
|--------|--------|-------|
| **Python factory function** | Low (1-2 days) | Claude direct ↔ Claude Bedrock |
| **LiteLLM proxy** | Medium | Multi-provider, OpenAI-format normalisation |
| **PortKey AI Gateway** | Medium | Multi-provider, observability built-in |
| **Custom adapter layer** | High | Full control, model-specific shims |

## 6.4 Multi-Model Feasibility

| Feature | Claude (works) | DeepSeek R1 (breaks) | Kimi K2.5 (partial) |
|---------|---------------|---------------------|---------------------|
| Tool/function calling | Native | **No support** | Client-side (buggy) |
| Structured JSON output | Reliable | Inconsistent | Good |
| System prompts | Full | Different behaviour | Supported |
| Multi-turn tool loops | Native | Must manually orchestrate | Partial |
| Image input | Yes | No | Yes |
| Converse API | Yes | **Not supported** | Yes |

**Critical finding**: DeepSeek R1 has **no tool calling** on Bedrock. Site builder agents use MCP tools heavily (10-50 tool calls per task). Running the full agent on R1 is not practical without a substantial shim layer.

## 6.5 Recommended Proxy Architecture

```
┌─────────────────────────────────────────┐
│          Agent Logic (unchanged)         │
│   (tool definitions, system prompts)     │
├─────────────────────────────────────────┤
│           Model Adapter Layer            │
│  ┌───────────────┐ ┌──────────────────┐ │
│  │ Claude Adapter │ │ DeepSeek Adapter │ │
│  │ (pass-through) │ │ - Tool→prompt    │ │
│  │               │ │ - <think> strip  │ │
│  │               │ │ - JSON parser    │ │
│  └───────────────┘ └──────────────────┘ │
├─────────────────────────────────────────┤
│     Transport (Bedrock / Direct API)     │
└─────────────────────────────────────────┘
```

## 6.6 Phased Implementation

| Phase | What | Effort | Value |
|-------|------|--------|-------|
| **Phase 1** | Claude direct ↔ Claude Bedrock swap | 1-2 days | Cost/latency comparison, Bedrock validation |
| **Phase 2** | Eval pack multi-model config | 3-5 days | Same task, multiple models, compare output |
| **Phase 3** | DeepSeek R1 for non-tool subtasks | 2-4 weeks | Cost savings on content generation only |

## 6.7 Cost & Latency

| Dimension | Anthropic Direct | Bedrock Claude | Bedrock DeepSeek R1 |
|-----------|-----------------|----------------|---------------------|
| Pricing | ~$3/$15 per 1M in/out | ~$3/$15 per 1M | ~$1.35/$5.40 per 1M |
| TTFT | 200-800ms | 300-1200ms | Similar to Bedrock |
| Cross-region penalty | N/A (global) | +80-120ms (eu-west-1 → us-east-1) | +80-120ms |
| Tool calling | Full | Full | **None** |

No significant cost penalty for Claude on Bedrock vs direct API.

---

# 7. Bedrock Evaluations Integration

## 7.1 Relevance to Folder-Based Eval

Bedrock `CreateEvaluationJob` is designed for **prompt-in/text-out** evaluation. Our eval is **folder-based**. However, Bedrock is still useful for:

- **Tier 3 (AWS mode)**: Submit BYOI datasets with pre-generated responses for managed judge scoring
- **Custom metrics**: Define up to 10 domain-specific scoring prompts (max 5,000 chars each)
- **Built-in metrics**: `Builtin.Correctness`, `Builtin.Completeness`, `Builtin.FollowingInstructions`

## 7.2 BYOI Pattern (Tier 3 Integration)

For Tier 3 (AWS mode), we can:
1. Run agent locally (Tier 1) → produces output folder
2. Serialize output folder contents + judge analysis into a text response
3. Package as BYOI JSONL: `{"prompt": "requirement", "modelResponses": [{"response": "serialized_judge_output", "modelIdentifier": "deepseek-r1"}]}`
4. Submit to Bedrock `CreateEvaluationJob` with custom metrics for meta-evaluation

## 7.3 Key Bedrock Constraints

| Constraint | Value |
|-----------|-------|
| Max prompts per job | 1,000 |
| Max custom metrics | 10 |
| Max metric prompt | 5,000 chars |
| Dataset format | JSONL in S3 |
| Supported judge models | Claude 3.5/3.7 Sonnet, Nova Pro, Llama 3.1 70B, Mistral Large |
| Region | us-east-1 (broadest), af-south-1 not supported |

---

# 8. Model Capability Mapping

## 8.1 Model Specs

| Spec | DeepSeek R1 | DeepSeek V3.2 | Kimi K2.5 | Claude Opus 4.6 |
|------|-------------|---------------|-----------|-----------------|
| Model ID | `us.deepseek.r1-v1:0` | `deepseek.v3.2` | `moonshotai.kimi-k2.5` | `anthropic.claude-opus-4-20250514` |
| Context | 128K/8K | 128K/8K | 128K/16K | 1M/32K |
| Image input | No | No | Yes | Yes |
| Tool calling (Bedrock) | No | Client-side | Client-side (buggy) | Full |
| Reasoning | Yes (`<think>`) | No | No | Yes |

## 8.2 Pricing

| Model | Input (/1M) | Output (/1M) | Per 100-prompt eval |
|-------|------------|-------------|---------------------|
| DeepSeek R1 | $1.35 | $5.40 | ~$4.90 |
| DeepSeek V3.2 | $0.74 | $2.22 | ~$2.10 |
| Kimi K2.5 | $0.60 | $3.00 | ~$2.60 |
| Claude Sonnet 4.6 (judge) | $3.00 | $15.00 | ~$13.20 |
| Claude Opus 4.6 (judge/teacher) | $5.00 | $25.00 | ~$4.40 (20 iter) |

**Total per full eval cycle: ~$27**

## 8.3 Region Availability

None of DeepSeek/Kimi available in eu-west-1 or af-south-1. Evals run from us-east-1.

## 8.4 Inference Parameters

| Param | DeepSeek R1 | DeepSeek V3.2 | Kimi K2.5 | Claude (judge) |
|-------|-------------|---------------|-----------|----------------|
| temperature | 0.3 | 0.2 | 0.2 | 0.0 |
| max_tokens | 8192 | 8192 | 16384 | 4096 |

## 8.5 Risks

| Risk | Model | Mitigation |
|------|-------|-----------|
| 8K output truncates HTML | DeepSeek R1/V3.2 | Use Kimi K2.5 (16K) |
| No tool calling | DeepSeek R1 | Text-based extraction or skip tool-heavy skills |
| Converse API bugs | Kimi K2.5 | InvokeModel fallback |
| Reasoning tokens billed | DeepSeek R1 | Strip `<think>`; budget 3x |

---

# 9. Consolidated Recommendations

## 9.1 Evaluation Architecture

**Folder-based, violation-deduction scoring, multimodal LLM judge.**

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Eval unit | Output folder (not text response) | Agent produces multi-file sites |
| Scoring | 10 minus deductions | Interpretable, maps to SonarQube/axe patterns |
| Violation catalogue | 5 categories, 4 severity levels | Covers structural, visual, content, code, accessibility |
| Visual comparison | Playwright + SSIM | Open-source, deterministic, headless |
| LLM judge | Claude Opus 4.6 (multimodal) | Code + screenshot together yield best results |
| Gold standards | Git-committed reference folders | Golden file testing pattern, versioned by template |
| Judge consistency | Temperature 0, 3-run median, rubric trees | Proven < 0.3 variance |

## 9.2 Runtime Architecture

**Proxy router with phased implementation.**

| Phase | What | When |
|-------|------|------|
| Phase 1 | `AnthropicBedrock` drop-in for Claude | Tier 1 build |
| Phase 2 | Multi-model eval config | Tier 1 execution |
| Phase 3 | DeepSeek adapter for non-tool tasks | After Tier 1 validated |

## 9.3 Decisions for HITL Approval

| Decision | Recommendation |
|----------|---------------|
| Scoring model | 10 minus deductions (not 0-5 additive) |
| Judge model | Claude Opus 4.6 (multimodal: code + screenshots) |
| Teacher model | Claude Opus 4.6 (same, for skill refinement) |
| Visual comparison | Playwright + SSIM |
| Gold standard management | Git-committed reference folders |
| Agent runtime proxy | `AnthropicBedrock` drop-in (Phase 1) |
| Region | us-east-1 for evals |

## 9.4 Tools to Integrate

| Tool | Purpose | Eval Tier |
|------|---------|-----------|
| Playwright | Screenshot capture + visual comparison | Structural/Visual |
| pixelmatch / SSIM | Pixel and structural similarity | Visual |
| W3C Nu HTML Checker | HTML validation | Content |
| axe-core | Accessibility audit | Content |
| Claude Opus 4.6 | LLM-as-judge (multimodal) | Judge |
| Design2Code metrics | CLIP similarity (optional) | Visual |

## 9.5 Sources

- [Design2Code (Stanford SALT)](https://github.com/NoviScl/Design2Code)
- [WebDevJudge](https://arxiv.org/html/2510.18560v1)
- [SWE-bench](https://www.swebench.com/SWE-bench/)
- [DevBench](https://arxiv.org/html/2403.08604v1)
- [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- [SonarQube Metrics](https://docs.sonarsource.com/sonarqube-server/2025.3/user-guide/code-metrics/metrics-definition)
- [Lighthouse Accessibility Scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring)
- [axe-core](https://github.com/dequelabs/axe-core)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [Bedrock CreateEvaluationJob API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateEvaluationJob.html)
- [Bedrock BYOI Pattern](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-prompt-datasets-judge.html)
- [Bedrock Custom Metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-custom-metrics-prompt-formats.html)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [DeepSeek R1 Model Card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-deepseek-deepseek-r1.html)
- [Kimi K2.5 Model Card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-moonshot-ai-kimi-k2-5.html)
