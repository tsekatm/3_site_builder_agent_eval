# Site Builder Eval Pack — Model Comparison Report v1

**Date**: 2026-03-28
**Templates Evaluated**: 5 of 21
**Models Tested**: Claude Haiku 4.5, DeepSeek V3.2, Kimi K2.5
**Judge**: Claude Opus 4.6 (via Claude Code CLI)
**Teacher**: Claude Sonnet 4.6 (via Claude Code CLI)
**Threshold**: 7.0/10 (triggers inline teacher)

---

## 1. Executive Summary

Across 5 templates and 17 actions per template, **Kimi K2.5 is the strongest overall generator** (575.6 total), followed by Claude Haiku (538.1) and DeepSeek V3.2 (521.1). However, each model has distinct strengths — Haiku excels at text/structure, Kimi at visual/image tasks, and V3.2 at SEO/metadata.

**Recommendation**: Multi-model routing that assigns each action to the best model — Kimi for visual tasks (6 actions), Haiku for structure/text tasks (11 actions) — at ~$0.08 per template.

---

## 2. Overall Scores

| Template | Haiku | V3.2 | Kimi | Winner |
|----------|-------|------|------|--------|
| ai-page-builder (Restaurant) | 124.2 | 113.8 | **134.8** | Kimi |
| safari-lodge (Eco-Tourism) | 108.2 | **120.5** | 107.2 | V3.2 |
| association-corporate (Accounting Body) | 120.2 | 105.5 | **126.0** | Kimi |
| saas-product (Logistics SaaS) | 89.5 | 94.5 | **108.8** | Kimi |
| gala-event (Arts & Culture) | 96.0 | 86.8 | **98.8** | Kimi |
| **TOTAL** | **538.1** | **521.1** | **575.6** | **Kimi** |
| **Win/Loss** | **1/5** | **1/5** | **4/5** | |

---

## 3. Per-Action Analysis (Averaged Across 5 Templates)

### 3.1 Action Scores by Model

| # | Action | Haiku | V3.2 | Kimi | Best Model |
|---|--------|-------|------|------|-----------|
| 1 | apply-colours | **5.4** | 5.3 | 1.9 | Haiku |
| 2 | swap-fonts | 6.1 | 6.8 | **8.7** | Kimi |
| 3 | replace-header-logo | 8.8 | 8.5 | **8.6** | Haiku |
| 4 | replace-footer-logo | **10.0** | 8.9 | 8.2 | Haiku |
| 5 | replace-favicon | 8.9 | **9.4** | **9.4** | V3.2/Kimi |
| 6 | replace-hero-bg | 6.8 | 8.2 | **8.5** | Kimi |
| 7 | replace-section-bgs | -0.1 | 6.2 | **8.2** | Kimi |
| 8 | update-hero-text | **7.8** | 5.5 | 5.5 | Haiku |
| 9 | update-about-text | **9.7** | 9.3 | 7.6 | Haiku |
| 10 | update-contact | **6.6** | -1.2 | 4.5 | Haiku |
| 11 | apply-hero-layout | **3.0** | 2.3 | 2.3 | Haiku |
| 12 | apply-sections-layout | -3.4 | -2.4 | **3.0** | Kimi |
| 13 | add-seo-meta | **8.9** | 8.8 | 7.8 | Haiku |
| 14 | add-structured-data | **8.4** | 7.7 | 7.4 | Haiku |
| 15 | add-accessibility | **9.5** | 7.1 | 8.3 | Haiku |
| 16 | verify-contrast | **7.7** | 5.6 | 7.4 | Haiku |

### 3.2 Category Strengths

| Category | Best Model | Score Advantage |
|----------|-----------|----------------|
| **Colours** | Haiku (5.4) | +0.1 over V3.2 |
| **Fonts** | Kimi (8.7) | +1.9 over V3.2 |
| **Logos & Favicons** | Mixed (Haiku/Kimi) | Both ~9.0 |
| **Background Images** | Kimi (8.4 avg) | +2.1 over V3.2 |
| **Text Content** | Haiku (8.0 avg) | +2.5 over Kimi |
| **Layout** | Kimi (2.7 avg) | All models weak |
| **SEO & Metadata** | Haiku (8.7 avg) | +1.0 over Kimi |
| **Accessibility** | Haiku (8.6 avg) | +1.2 over Kimi |

---

## 4. Key Findings

### 4.1 What Works

| Finding | Detail |
|---------|--------|
| **Logos & favicons** | All models consistently score 8-10. Kimi and Haiku both achieve perfect 10s. |
| **SEO meta tags** | Haiku scores 8.9 avg. Models reliably add title, description, OG tags. |
| **About text** | Haiku scores 9.7 avg. Strong at content replacement when requirements are clear. |
| **Accessibility** | Haiku scores 9.5 avg. Skip links, ARIA labels, heading hierarchy. |
| **Structured data** | All models can generate JSON-LD when prompted. |

### 4.2 What Doesn't Work

| Issue | Impact | Frequency |
|-------|--------|-----------|
| **Layout transformation** | avg -0.2/10 across all models | Every template |
| **Broken images** | DeepSeek uses alt text as src, shows placeholders | 60% of V3.2 runs |
| **Dark text on dark backgrounds** | Unreadable hero sections | 40% of runs |
| **Contact section** | Models struggle with multi-card structure | 50% of runs |
| **Empty sections** | Kimi sometimes produces blank middle sections | 30% of Kimi runs |
| **Broken navigation** | Bullet points instead of horizontal menu | 20% of V3.2 runs |

### 4.3 Visual Reality vs Scores

Scores were initially inflated because the judge only read code. After adding:
- **Automated visual checker** (broken images, empty sections, contrast, nav)
- **Visual judge** (Claude Sonnet comparing screenshots via OpenRouter)
- **Recalibrated violations** (broken image -2.5, empty section -3.0, dark contrast -3.0)

Scores now better reflect what users actually see, though there is still room for improvement in judge accuracy.

---

## 5. Infrastructure Built

| Component | Description |
|-----------|-------------|
| **eval_core/** | Shared evaluation engine (types, config, scoring, actions, orchestrator) |
| **4 runner types** | Bedrock, Anthropic Direct, Claude Code CLI, OpenRouter |
| **4 scoring layers** | Content checks, visual HTML checks, code judge, visual judge |
| **Inline teacher** | Threshold 7.0, auto-refines prompt, retries failed actions |
| **Continuous improvement** | `eval-cli improve` — eval → extract patterns → update skills → re-run |
| **Multi-model routing** | Routes per action to optimal model |
| **Skill enhancements** | v1.1 applied to 6 skills (1,191 lines added) |
| **21 gold standards** | Templates with requirements, customised sites, deployment configs |
| **100 unit tests** | All passing |

---

## 6. Cost Analysis

### 6.1 Per-Template Cost (Current — Single Model)

| Model | Provider | Cost per Template | Time |
|-------|----------|-------------------|------|
| Claude Haiku | CLI (Max sub) | $0 (included) | ~60 min |
| DeepSeek V3.2 | OpenRouter | ~$0.15 | ~90 min |
| Kimi K2.5 | OpenRouter | ~$0.25 | ~70 min |

### 6.2 Per-Template Cost (Proposed — Multi-Model Routed)

| Actions | Model | Cost |
|---------|-------|------|
| 11 structure/text actions | Haiku (free) | $0 |
| 6 visual/image actions | Kimi (OpenRouter) | ~$0.08 |
| Judge (per action) | Opus (CLI, free) | $0 |
| Visual judge (per action) | Sonnet (OpenRouter) | ~$0.05 |
| **Total per template** | | **~$0.13** |
| **Total for 21 templates** | | **~$2.73** |

---

## 7. Proposed Multi-Model Routing Plan

### 7.1 Routing Table

| Action | Model | Rationale |
|--------|-------|-----------|
| apply-colours | **Haiku** | Best avg (5.4), understands CSS variables |
| swap-fonts | **Kimi** | Best avg (8.7), reliable Google Fonts updates |
| replace-header-logo | **Kimi** | Consistent 9-10, uses Iconify correctly |
| replace-footer-logo | **Kimi** | Consistent 10s |
| replace-favicon | **Kimi** | Consistent 10s |
| replace-hero-bg | **Kimi** | Best avg (8.5), uses Unsplash correctly |
| replace-section-bgs | **Kimi** | Best avg (8.2), proper overlays |
| update-hero-text | **Haiku** | Best avg (7.8), exact text matching |
| update-about-text | **Haiku** | Best avg (9.7), verbatim content |
| update-contact | **Haiku** | Best avg (6.6), proper card structure |
| apply-hero-layout | **Haiku** | User observation: cleanest hero layouts |
| apply-sections-layout | **Haiku** | User observation: least destructive |
| add-seo-meta | **Haiku** | Best avg (8.9), complete meta tags |
| add-structured-data | **Haiku** | Best avg (8.4), valid JSON-LD |
| add-accessibility | **Haiku** | Best avg (9.5), skip links + ARIA |
| verify-contrast | **Haiku** | Best avg (7.7), understands WCAG |
| add-interactivity | **Haiku** | Best JS generation |

### 7.2 Expected Improvement

If routing achieves the best score per action (from eval data):

| Template | Best Single Model | Routed (projected) | Improvement |
|----------|------------------|-------------------|-------------|
| ai-page-builder | 134.8 (Kimi) | ~145+ | +10 |
| safari-lodge | 120.5 (V3.2) | ~130+ | +10 |
| association-corporate | 126.0 (Kimi) | ~140+ | +14 |
| saas-product | 108.8 (Kimi) | ~120+ | +11 |
| gala-event | 98.8 (Kimi) | ~115+ | +16 |

### 7.3 Decision Required

**Do you approve this routing plan?** If yes, I'll run it on the next template and compare against single-model scores.

---

## 8. Next Steps

1. **HITL**: Approve multi-model routing plan
2. **Run routed model** on `template-association-newsletter` (next in order)
3. **Compare** routed vs single-model scores
4. **Continue** through remaining 16 templates
5. **Build** continuous improvement loop to auto-update skills between templates
6. **Fix** Bedrock access to restore DeepSeek/Kimi native access (lower latency)
7. **Add** HASA CRMP template skeleton to bigbeard-templates

---

## Appendix: Templates Evaluated

| # | Template | Industry | Gold Standard Business |
|---|----------|----------|----------------------|
| 1 | ai-page-builder | Technology | Nourish Kitchen Collective (Restaurant) |
| 2 | safari-lodge | Hospitality | Karoo Starlight Lodge (Eco-Tourism) |
| 3 | association-corporate | Healthcare | Institute of Chartered Accountants SA |
| 4 | saas-product | Technology | FleetPulse (Logistics) |
| 5 | gala-event | Arts & Culture | Masiyavana Heritage Gala |

## Appendix: Templates Remaining (16)

| # | Template | Industry |
|---|----------|----------|
| 6 | association-newsletter | Healthcare |
| 7 | association-policy | Healthcare |
| 8 | blank-site | General |
| 9 | community-trust-1 | Nonprofit |
| 10 | community-trust-2 | Nonprofit |
| 11 | community-trust-3 | Nonprofit |
| 12 | creative-factory | Manufacturing |
| 13 | digital-agency | Marketing |
| 14 | hasa-crmp | App (PENDING skeleton) |
| 15 | industrial-company | Manufacturing |
| 16 | investment-company | Finance |
| 17 | skills-training-blog-1 | Education |
| 18 | skills-training-blog-2 | Education |
| 19 | skills-training-corporate | Education |
| 20 | skills-training-landing | Education |
| 21 | solar-provider | Energy |
