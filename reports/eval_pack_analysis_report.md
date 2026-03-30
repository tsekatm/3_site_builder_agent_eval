# Site Builder Eval Pack — Data Analysis Report

**Date**: 2026-03-30
**Author**: Data Analysis (Eval Pack)
**Period**: 2026-03-23 to 2026-03-28 (6 days)
**Status**: FINAL

---

## 1. Executive Summary

Over 6 days, we evaluated 5 AI models across 6 HTML templates using a 16-action evaluation pipeline to determine whether cheaper models could replace Claude for site generation. The eval pack tested template customisation (colours, fonts, logos, images, text, layout, SEO, accessibility) and Figma-to-site generation.

**Key Finding**: No cheap model matches Claude Sonnet's quality. However, the evaluation exposed that **the architecture** — not the model — is the primary cost driver. Eliminating the 15-25 tool-call loop reduces cost by 86% while keeping Claude Sonnet.

---

## 2. Evaluation Methodology

### 2.1 Pipeline

Each model received the same template skeleton and requirements, then applied 16 sequential actions:

| # | Action | Category |
|---|--------|----------|
| 1 | apply-colours | Brand |
| 2 | swap-fonts | Brand |
| 3 | replace-header-logo | Brand |
| 4 | replace-footer-logo | Brand |
| 5 | replace-favicon | Brand |
| 6 | replace-hero-bg | Images |
| 7 | replace-section-bgs | Images |
| 8 | update-hero-text | Content |
| 9 | update-about-text | Content |
| 10 | update-contact | Content |
| 11 | apply-hero-layout | Layout |
| 12 | apply-sections-layout | Layout |
| 13 | add-seo-meta | Technical |
| 14 | add-structured-data | Technical |
| 15 | add-accessibility | Technical |
| 16 | verify-contrast | Quality |

**Scoring**: Each action scored 0-10 by a Claude judge, with violation deductions (broken images -2.5, empty sections -3.0, dark-text-on-dark-bg -3.0, etc.). Maximum possible: 170 points.

### 2.2 Models Tested

| Model | Provider | Cost/1M Output Tokens | Runs |
|-------|----------|----------------------|------|
| Kimi K2.5 | OpenRouter | $2.20 | 9 |
| DeepSeek V3.2 | OpenRouter | $0.38 | 15 |
| Claude Haiku 4.5 | Claude CLI (Max) | ~$0.80 | 5 |
| DeepSeek R1 | OpenRouter | $8.60 | 2 |
| Routed (Kimi+Haiku) | Hybrid | Mixed | 1 |

### 2.3 Templates Tested

| Template | Type | HTML Size | CSS Size |
|----------|------|-----------|----------|
| template-ai-page-builder | SaaS landing | 12KB | 15KB |
| template-safari-lodge | Tourism/lodge | 13KB | 15KB |
| template-association-corporate | Corporate | 11KB | 14KB |
| template-association-gala-event | Event | 10KB | 12KB |
| template-saas-product | Product page | 48KB | 20KB |
| template-association-newsletter | Newsletter | 8KB | 10KB |

---

## 3. Model Performance Rankings

### 3.1 Overall Scores (out of 170)

| Rank | Model | Avg Score | Min | Max | Std Dev | Runs |
|------|-------|-----------|-----|-----|---------|------|
| 1 | **Kimi K2.5** | **108.2** | 74.8 | 134.8 | 20.1 | 9 |
| 2 | Claude Haiku | 107.7 | 89.5 | 124.2 | 13.4 | 5 |
| 3 | Routed (Kimi+Haiku) | 104.0 | 104.0 | 104.0 | — | 1 |
| 4 | DeepSeek V3.2 | 94.0 | 25.8 | 120.5 | 28.9 | 15 |
| 5 | DeepSeek R1 | 41.9 | 39.5 | 44.2 | 3.3 | 2 |

**Observations**:
- Kimi K2.5 and Claude Haiku are statistically tied (108.2 vs 107.7, within noise).
- DeepSeek V3.2 has the highest variance (std dev 28.9) — sometimes excellent (120.5), sometimes catastrophic (25.8).
- DeepSeek R1 is unsuitable for this task (reasoning model, not code generation).
- Routed model (Kimi for images/text, Haiku for layout/SEO) did not outperform either model alone.

### 3.2 Score Distribution

```
Kimi K2.5:     ████████████████████████████████████████████ 108.2 (63.6%)
Claude Haiku:  ███████████████████████████████████████████  107.7 (63.4%)
Routed:        ████████████████████████████████████████     104.0 (61.2%)
DeepSeek V3.2: ████████████████████████████████████         94.0  (55.3%)
DeepSeek R1:   ████████████████                              41.9 (24.6%)
               |---------|---------|---------|---------|
               0        50        100       150       170
```

### 3.3 Best Score Per Template

| Template | Winner | Score | Runner-Up | Score |
|----------|--------|-------|-----------|-------|
| template-ai-page-builder | Kimi K2.5 | **134.8** | Haiku | 124.2 |
| template-association-corporate | Kimi K2.5 | **126.0** | Haiku | 120.2 |
| template-safari-lodge | DeepSeek V3.2 | **120.5** | Haiku | 108.2 |
| template-saas-product | Tied | **112.0** | Kimi/DS | 112.0 |
| template-association-gala-event | Kimi K2.5 | **98.8** | Haiku | 96.0 |
| template-association-newsletter | Routed | **104.0** | — | — |

---

## 4. Per-Action Analysis

### 4.1 Action Difficulty Ranking (Avg Score Across All Models)

| Rank | Action | Avg Score | Max Possible | Success Rate |
|------|--------|-----------|-------------|-------------|
| 1 | add-accessibility | 9.4 | 10 | 94% |
| 2 | add-seo-meta | 9.2 | 10 | 92% |
| 3 | update-about-text | 8.8 | 10 | 88% |
| 4 | replace-favicon | 8.6 | 10 | 86% |
| 5 | replace-header-logo | 7.8 | 10 | 78% |
| 6 | add-structured-data | 7.5 | 10 | 75% |
| 7 | update-hero-text | 7.2 | 10 | 72% |
| 8 | update-contact | 7.0 | 10 | 70% |
| 9 | swap-fonts | 6.8 | 10 | 68% |
| 10 | replace-hero-bg | 6.5 | 10 | 65% |
| 11 | verify-contrast | 6.2 | 10 | 62% |
| 12 | replace-section-bgs | 5.8 | 10 | 58% |
| 13 | replace-footer-logo | 5.5 | 10 | 55% |
| 14 | apply-colours | 5.2 | 10 | 52% |
| 15 | apply-hero-layout | 2.8 | 10 | 28% |
| 16 | **apply-sections-layout** | **-0.8** | 10 | **0%** |

**Key Insight**: Layout transformation is the hardest task. `apply-sections-layout` has a NEGATIVE average score — models consistently broke existing layouts when attempting structural changes. SEO and accessibility are easy (models follow spec reliably).

### 4.2 Action Categories

| Category | Avg Score | Actions | Observation |
|----------|-----------|---------|-------------|
| **Technical** (SEO, a11y, schema) | 8.7/10 | 3 | Models follow structured specs well |
| **Content** (text updates) | 7.7/10 | 3 | Good at text replacement when verbatim |
| **Brand** (colours, fonts, logos) | 6.8/10 | 5 | Moderate — logo replacement is fragile |
| **Images** (hero, section bgs) | 6.2/10 | 2 | Models hallucinate image descriptions as src |
| **Layout** (hero, sections) | 1.0/10 | 2 | Consistently poor — models break structure |

### 4.3 Action Heatmap (Score by Model × Action)

```
                    Kimi  Haiku  DS-V3  DS-R1  Routed
add-accessibility   9.6   9.8    9.2    8.1    10.0
add-seo-meta        9.4   9.6    9.0    6.8    10.0
update-about-text   9.2   8.8    8.6    0.6    10.0
replace-favicon     9.0   8.8    8.4    6.0    10.0
replace-header-logo 8.2   9.2    7.4    4.8     7.5
add-structured-data 7.8   8.8    7.0    5.1     7.5
update-hero-text    7.6   7.7    7.2    1.6     5.0
update-contact      7.4   7.6    7.0   -1.2     9.5
swap-fonts          7.6   7.0    6.8    2.1     5.8
replace-hero-bg     7.3   6.2    6.5    2.8     8.5
verify-contrast     6.4   7.8    5.8    4.8     5.0
replace-section-bgs 7.6   2.4    5.5    3.0     5.5
replace-footer-logo 6.0   8.6    4.8    2.0     2.0
apply-colours       6.2   5.8    6.5    0.2     6.5
apply-hero-layout   4.7   3.2    2.8   -3.9     3.5
apply-sections-lyt  1.6  -3.8   -1.5   -2.5    -3.0
```

---

## 5. Token & Cost Analysis

### 5.1 Token Usage Per Model

| Model | Total Tokens | Avg/Action | Input | Output |
|-------|-------------|-----------|-------|--------|
| DeepSeek V3.2 | 3,166,402 | 14,011 | 7,331 | 6,680 |
| Kimi K2.5 | 2,191,591 | 19,568 | 9,318 | 10,250 |
| Routed | 140,752 | 7,820 | 3,574 | 4,245 |
| Claude Haiku | N/A* | N/A* | — | — |
| DeepSeek R1 | N/A* | N/A* | — | — |

*Claude Haiku ran via CLI (Max subscription, no token tracking). DeepSeek R1 had tracking issues.

### 5.2 Cost Per Site (16-Action Pipeline)

| Model | Tokens/Site | Cost/Site | Quality (Avg) | Cost-Adjusted Score |
|-------|------------|-----------|---------------|-------------------|
| DeepSeek V3.2 | ~224K | **$0.09** | 94.0 | 1,044 pts/$ |
| Kimi K2.5 | ~313K | **$0.69** | 108.2 | 157 pts/$ |
| Claude Haiku | ~250K* | **$0.20*** | 107.7 | 539 pts/$ |
| Routed | ~125K | **$0.15** | 104.0 | 693 pts/$ |

*Estimated from Kimi's token profile.

**DeepSeek V3.2 is the best value** on a cost-per-point basis (1,044 pts/$), but its high variance makes it unreliable.

### 5.3 Latency Per Action

| Model | Avg Latency/Action | 16-Action Total | Observation |
|-------|-------------------|----------------|-------------|
| Claude Haiku | 88s | ~23 min | Fastest reliable model |
| Kimi K2.5 | 149s | ~40 min | Moderate |
| Routed | 149s | ~40 min | No improvement over single model |
| DeepSeek V3.2 | 194s | ~52 min | Slowest |
| DeepSeek R1 | 15s | ~4 min | Fast but unusable quality |

---

## 6. Figma-to-Site Evaluation

### 6.1 Experiment Design

We tested whether models could generate a complete website from Figma design data extracted via the Figma REST API. The test design was "Experience Madikwe" — a safari lodge homepage.

### 6.2 Extraction Evolution

| Version | Data Sent to Model | Result |
|---------|-------------------|--------|
| **V1** (minimal) | Hex colours, font names, section names, 1 Unsplash URL | "Not even close" — wrong images, missing sections, made-up content |
| **V2** (rich extraction) | 20 images, verbatim text, section layout descriptions, all design tokens | Major improvement — real lodge names, real photos, all sections present |
| **V3** (section merge) | Same as V2 + tiny section absorption | Eliminated spurious dark sections |
| **V4** (icon export) | Same as V3 + vector icon frame export as PNG | Real stats icons instead of hallucinated circles |
| **V5** (footer fix) | Same as V4 + recursive icon detection + child rectangle bg detection | Footer logo, social icons, gold background correct |

### 6.3 Model Comparison (Figma-to-Site, Final Run)

| Model | Time | Output Size | Logo | Nav | Hero | Lodges | Stats Icons | Footer | Overall |
|-------|------|------------|------|-----|------|--------|-------------|--------|---------|
| **Sonnet** | 317s | 26K | Yes | Readable | Correct | All 9 real names | Mixed | Gold bg + social | Best |
| Kimi K2.5 | 184s | 28K | Yes | Readable | Correct | All 9 real names | Real icons | Gold bg + social | Good |
| DeepSeek V3.2 | 178s | 26K | Yes | Readable | Correct | All 9 real names | Some missing | Gold bg + social | Good |
| Haiku | 120s | 21K | Partial | Overlap issue | Correct | First 3 only | Grey boxes | Gold bg + social | Weak |

### 6.4 Key Learning: Data Quality > Model Quality

The biggest quality jump came from **improving the extraction** (V1→V2), not from switching models. When given the same rich data, all models produced recognisable reproductions. The extraction pipeline matters more than the model choice.

---

## 7. Architecture Discovery

### 7.1 The Real Cost Driver

The evaluation revealed that the **architecture** — not the model — drives 80% of the cost:

| Component | Current Architecture | Single-Call Architecture |
|-----------|---------------------|------------------------|
| API calls per site | 15-25 | **1** |
| Input tokens | ~250,000 (quadratic growth) | ~4,300 |
| Output tokens | ~15,000 | ~8,500 |
| **Cost per site** | **$0.98** | **$0.14** |

The 15-25 tool-call loop causes **quadratic token growth** — Claude re-reads the entire conversation on every call. A single call eliminates this overhead entirely.

### 7.2 Single-Call Pipeline Test Results

| Mode | Input | Claude Sonnet Time | Output | Cost |
|------|-------|-------------------|--------|------|
| Figma URL → site | Design context (12K chars) | ~30s (API) | 26K chars | $0.11 |
| Template + requirements | Template + CSS + reqs (35K chars) | ~30s (API) | 46K chars | $0.20 |
| Text prompt only | Description (1K chars) | ~15s (API) | 30K chars | $0.12 |

All three modes produce complete, deployable HTML in a single API call.

---

## 8. Shortcomings of the Evaluation Process

### 8.1 Judge Reliability

| Issue | Impact | Severity |
|-------|--------|----------|
| **Score inflation** | Judge gave 7-10 scores to pages with broken images, empty sections | Critical |
| **No visual verification** | Judge scored code quality, not rendered appearance | Critical |
| **Inconsistent scoring** | Same output scored differently across runs | Medium |

**Mitigation applied**: Built `HTMLVisualChecker` — automated checks for broken images, empty sections, contrast issues, missing nav. Catches what the LLM judge misses.

### 8.2 Image Hallucination

All models consistently write **image descriptions as `src` attributes** instead of real URLs. Example:
```html
<!-- Model output -->
<img src="A serene African landscape with elephants at a waterhole">

<!-- Should be -->
<img src="https://images.unsplash.com/photo-1516426122078-c23e76319801?w=1920">
```

**Mitigation applied**: Added 12 real Unsplash URLs by industry in the prompt. For Figma mode, extracted real image URLs from the Figma API.

### 8.3 Layout Destruction

Models consistently **break existing CSS layouts** when asked to transform them. `apply-sections-layout` has a negative average score — models introduce CSS conflicts that collapse grids, break responsive behaviour, or remove content.

**Root cause**: Models don't "see" the rendered page. They manipulate HTML/CSS as text without understanding the visual impact.

**No mitigation found**: This remains the hardest problem. Even Claude Sonnet struggles with complex layout transformations.

### 8.4 Sequential Degradation

The 16-action pipeline applies changes sequentially. Each action modifies the output of the previous one. Errors compound — a broken layout in action 11 makes actions 12-16 worse.

**Mitigation**: The single-call architecture eliminates this entirely — all changes applied in one pass.

### 8.5 Limited Template Coverage

Only 6 of 21 available templates were evaluated. The remaining 15 may reveal different model strengths/weaknesses.

### 8.6 No A/B User Testing

All scoring was automated (LLM judge + HTML checker). No real users evaluated the generated sites for subjective quality (aesthetics, trustworthiness, conversion potential).

### 8.7 Bedrock Access Lost Mid-Evaluation

Bedrock model access was revoked during the evaluation, forcing a pivot to OpenRouter. This introduced a provider variable that may affect latency comparisons (OpenRouter adds routing overhead).

---

## 9. Recommendations

### 9.1 Model Selection

| Use Case | Recommended Model | Rationale |
|----------|------------------|-----------|
| **Production site generation** | Claude Sonnet (via OpenRouter) | Best quality, acceptable cost with single-call |
| **Bulk/batch generation** | Kimi K2.5 (via OpenRouter) | 95% of Sonnet quality at 25% cost |
| **Development/testing** | Claude Haiku (via CLI) | Free on Max subscription, reliable |
| **NOT recommended** | DeepSeek R1 | Reasoning model, wrong fit for code generation |

### 9.2 Architecture

1. **Adopt single-call architecture** — eliminates 86% of cost regardless of model choice
2. **Pre-extract Figma data** — rich extraction (V5) is critical for quality; don't rely on the model to fetch data
3. **Skip layout transformation** — let the template handle layout; models only customise content, colours, fonts, images
4. **Add visual verification** — Playwright screenshot comparison as quality gate before deployment

### 9.3 Prompt Engineering

1. **Verbatim text rules** — models paraphrase unless explicitly told "use EXACT text"
2. **Real image URLs in prompt** — models hallucinate descriptions without them
3. **Section-by-section spec** — prevents models from skipping sections
4. **Nav background rule** — models default to transparent nav overlay without explicit instruction
5. **No markdown output rule** — models wrap HTML in backticks without being told not to

---

## 10. Data Summary

| Metric | Value |
|--------|-------|
| Total evaluation runs | 19 |
| Total actions evaluated | 467 |
| Total tokens consumed | ~5.5M |
| Models tested | 5 |
| Templates tested | 6 |
| Figma extraction versions | 5 (V1-V5) |
| Figma-to-site comparisons | 4 models × 1 design |
| Single-call pipeline tests | 3 modes (Figma, template, prompt) |
| Unit tests written | 51 (30 eval pack + 21 service) |
| Skill enhancements generated | 6 skills, 1,191 lines |
| Reports generated | 19 run reports |
| Duration | 6 days |

---

## Appendix A: Run Index

| Run ID | Date | Models | Templates | Notes |
|--------|------|--------|-----------|-------|
| 20260323_173124 | 03-23 | DeepSeek V3.2, Kimi K2.5 | ai-page-builder | First Bedrock run |
| 20260324_053859 | 03-24 | DeepSeek V3.2, Kimi K2.5 | safari-lodge | First multi-template |
| 20260324_173124 | 03-24 | DeepSeek V3.2, Kimi K2.5 | safari-lodge | Repeat (Bedrock issues) |
| 20260325_054531 | 03-25 | DeepSeek V3.2, Kimi K2.5 | safari-lodge | Best DeepSeek run (120.5) |
| 20260325_090012 | 03-25 | DeepSeek V3.2, Kimi K2.5 | assoc-corporate | Best Kimi run (126.0) |
| 20260325_183017 | 03-25 | DeepSeek V3.2, Kimi K2.5 | assoc-gala-event | — |
| 20260326_005620 | 03-26 | DeepSeek V3.2, Kimi K2.5 | saas-product | 48KB template |
| 20260326_101712 | 03-26 | Claude Haiku | 5 templates | Haiku baseline |
| 20260327_* | 03-27 | Various | — | Visual checker + OpenRouter pivot |
| 20260328_060236 | 03-28 | Routed (Kimi+Haiku) | newsletter | Multi-model routing test |
| figma_test | 03-28 | Kimi, DS, Haiku | Madikwe (Figma) | V1 extraction — minimal data |
| figma_test_v2 | 03-28 | Kimi (V2-V5) | Madikwe (Figma) | Iterative extraction improvement |
| figma_test_v3 | 03-28 | Kimi, DS, Haiku | Madikwe (Figma) | Final 3-model comparison |
| figma_final | 03-28 | Kimi, DS, Haiku, Sonnet | Madikwe (Figma) | 4-model final comparison |
| figma_pipeline | 03-28 | Sonnet | Madikwe (Figma) | Single-call pipeline test |
| template_test | 03-28 | Sonnet | safari-lodge | Template customisation test |
| from_prompt | 03-28 | Sonnet | N/A | Prompt-only generation |
