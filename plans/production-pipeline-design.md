# Production Pipeline Design — Cost-Optimised Site Builder

**Date**: 2026-03-28
**Purpose**: Replace Claude agent with cheaper models (Kimi/DeepSeek via OpenRouter) for production site generation
**Status**: DESIGN — Awaiting HITL approval

---

## 1. Problem Statement

Current architecture uses Claude (via MCP facade with tool calling) at ~$15/1M output tokens. The eval pack proved that Kimi K2.5 ($2.20/1M) and DeepSeek V3.2 ($0.38/1M) can produce comparable site output at 5-40x lower cost.

**Goal**: Build a production pipeline that uses cheap models to customise templates, with quality gates to ensure output meets standards.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION PIPELINE                       │
│                                                             │
│  ┌──────────┐     ┌──────────────┐     ┌────────────────┐  │
│  │ Request   │────►│ Orchestrator │────►│ Quality Gate   │  │
│  │ (API/CLI) │     │ (Python)     │     │ (auto checks)  │  │
│  └──────────┘     └──────┬───────┘     └───────┬────────┘  │
│                          │                     │            │
│                    ┌─────▼─────┐         ┌─────▼─────┐     │
│                    │ OpenRouter │         │ Deploy     │    │
│                    │ API Call   │         │ (S3 + CF)  │    │
│                    └───────────┘         └───────────┘     │
│                                                             │
│  No MCP. No tool calling. No agent loops.                   │
│  Just: Template + Requirements → API → HTML → S3            │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Flow

```
1. INPUT
   ├── Template skeleton (from bigbeard-templates/ or S3)
   ├── Requirements (business name, colours, fonts, content, images)
   └── Template config (placeholders, CSS variables, image slots)

2. GENERATE (single OpenRouter API call)
   ├── Prompt = template HTML + CSS + requirements + generation rules
   ├── Model = Kimi K2.5 (primary) or DeepSeek V3.2 (fallback)
   └── Response = complete customised HTML + CSS

3. VALIDATE (automated, no LLM)
   ├── HTML visual checker (broken images, empty sections, contrast, nav)
   ├── Placeholder check (no {{TOKENS}} remaining)
   ├── CSS variable check (brand colours applied)
   └── Structure check (required sections present)

4. QUALITY GATE (optional LLM judge for premium tier)
   ├── Screenshot via Playwright
   ├── Visual judge (OpenRouter Claude Sonnet with vision)
   └── Pass/fail decision

5. DEPLOY
   ├── Write to S3 workspace
   ├── Sync to staging bucket
   ├── CloudFront invalidation
   └── Return staging URL
```

### 2.2 Single-Call vs Multi-Action

The eval pack sends 17 separate actions. Production should send **ONE call** with everything:

```
PROMPT:
  "Here is a website template. Customise it for this business.
   Apply ALL of the following changes in a single response:
   - Colours: [palette]
   - Fonts: [pairing]
   - Logo: [Iconify URL]
   - Images: [Unsplash URLs for hero, sections]
   - Text: [hero headline, about, contact details]
   - SEO: [meta tags, JSON-LD]
   - Accessibility: [skip link, ARIA]
   - Interactivity: [mobile menu JS, smooth scroll, hover states]

   Return the complete index.html and styles.css."
```

**Why single-call?**
- Cheaper (1 API call vs 17)
- Faster (~60s vs ~60min)
- No cumulative degradation (each action doesn't break the previous one)
- Models see the full picture, not fragments

---

## 3. Components

### 3.1 Production Orchestrator (`site_generator/`)

```
site_generator/
├── __init__.py
├── generator.py          # Main pipeline orchestrator
├── prompts/
│   ├── single_call.py    # The one-shot generation prompt
│   └── refinement.py     # Optional fix-up prompt for quality failures
├── providers/
│   ├── openrouter.py     # OpenRouter API (Kimi, DeepSeek)
│   ├── claude_cli.py     # Claude Code CLI (fallback for complex layouts)
│   └── base.py           # Abstract provider
├── quality/
│   ├── html_checker.py   # Reuse from eval_core/visual/html_visual_checker.py
│   ├── screenshot.py     # Reuse from eval_core/visual/screenshot.py
│   └── validator.py      # Pass/fail quality gate
├── storage/
│   ├── s3.py             # Read templates, write output
│   └── local.py          # Local filesystem for dev
├── deploy/
│   ├── staging.py        # S3 sync + CloudFront invalidation
│   └── config.py         # Deployment configuration
└── api/
    ├── lambda_handler.py # AWS Lambda entry point
    └── cli.py            # Local CLI for testing
```

### 3.2 Generation Prompt

The prompt is the product — it encodes everything the eval taught us:

```python
GENERATION_PROMPT = """You are a website customisation engine.

## Template
```html
{template_html}
```

```css
{template_css}
```

## Requirements
Business: {business_name} — {tagline}
Industry: {industry}

Colours: primary={primary}, secondary={secondary}, accent={accent}, bg={background}, text={text}
Heading font: {heading_font} (weights: {heading_weights})
Body font: {body_font} (weights: {body_weights})

Hero: headline="{headline}", subtitle="{subtitle}", CTA="{cta_text}"
About: "{about_text}"
Contact: email={email}, phone={phone}, address={address}

## RULES
1. Return COMPLETE index.html and styles.css
2. ALL images must use real URLs starting with https://
   Hero: {hero_unsplash_url}
   Portraits: https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop
   Icons: https://api.iconify.design/mdi/{icon}.svg?color=%23{hex}&width=48&height=48
3. White text on ANY section with background image (overlay rgba(0,0,0,0.6) minimum)
4. Replace ALL {{PLACEHOLDER}} tokens
5. 4-column footer grid
6. Mobile menu with hamburger toggle (JS)
7. Smooth scroll for anchor links (JS)
8. Hover states on all buttons and cards (CSS)
9. Meta tags: title, description, OG tags
10. JSON-LD structured data ({schema_type})
11. Skip-to-content link + ARIA labels

===HTML===
(complete index.html)
===CSS===
(complete styles.css)
===END==="""
```

### 3.3 Quality Gate

Reuse the automated checkers from the eval pack:

```python
from eval_core.visual.html_visual_checker import HTMLVisualChecker

def validate_output(html_path, css_path):
    checker = HTMLVisualChecker(html_path, css_path)
    violations = checker.check_all()

    critical = [v for v in violations if v.severity == "critical"]
    if critical:
        return False, violations  # FAIL — needs regeneration

    total_deduction = sum(v.deduction for v in violations)
    if total_deduction < -5.0:
        return False, violations  # FAIL — too many issues

    return True, violations  # PASS
```

### 3.4 Fallback Strategy

```
1. Try Kimi K2.5 (cheapest winner from eval)
   ├── Pass quality gate? → Deploy
   └── Fail?
       2. Try DeepSeek V3.2 (second cheapest)
          ├── Pass? → Deploy
          └── Fail?
              3. Try Claude Haiku via CLI (reliable, free on Max)
                 ├── Pass? → Deploy
                 └── Fail? → Flag for manual review
```

---

## 4. Cost Comparison

### 4.1 Current (Claude via MCP)

| Component | Cost per Site |
|-----------|--------------|
| Claude Opus/Sonnet (10-50 tool calls) | ~$0.50-$2.00 |
| MCP facade Lambda | ~$0.01 |
| S3/CloudFront | ~$0.01 |
| **Total** | **~$0.52-$2.02** |

### 4.2 Proposed (Single-call via OpenRouter)

| Component | Cost per Site |
|-----------|--------------|
| Kimi K2.5 single call (~20K tokens) | ~$0.05 |
| Quality gate (automated, no LLM) | $0.00 |
| Optional visual judge (premium tier) | ~$0.03 |
| S3/CloudFront | ~$0.01 |
| **Total** | **~$0.06-$0.09** |

### 4.3 Savings

| Metric | Current | Proposed | Savings |
|--------|---------|----------|---------|
| Cost per site | ~$1.00 | ~$0.07 | **93% reduction** |
| Time per site | ~5-10 min | ~1-2 min | **80% faster** |
| 1,000 sites/month | ~$1,000 | ~$70 | **$930/month saved** |
| 10,000 sites/month | ~$10,000 | ~$700 | **$9,300/month saved** |

---

## 5. Implementation Plan

### Phase 1: Prototype (1-2 days)
- Build `site_generator/generator.py` with single-call prompt
- OpenRouter integration (reuse existing runner)
- Local filesystem storage
- Quality gate (reuse `html_visual_checker.py`)
- Test on 5 eval templates

### Phase 2: S3 Integration (1 day)
- Read templates from S3
- Write output to S3 workspace
- Staging deployment (S3 sync + CloudFront)

### Phase 3: API Endpoint (1 day)
- Lambda handler or FastAPI endpoint
- Accept requirements JSON → return staging URL
- Fallback chain (Kimi → DeepSeek → Haiku)

### Phase 4: Integration (2 days)
- Connect to existing site builder frontend
- Replace MCP tool-call flow with single API call
- A/B test: Claude agent vs cheap pipeline

### Phase 5: Production (1 day)
- Deploy to DEV → SIT → PROD
- Monitoring (CloudWatch, cost tracking)
- Quality dashboards

**Total: ~6-7 days**

---

## 6. Risks

| Risk | Mitigation |
|------|-----------|
| Quality drops vs Claude | Quality gate catches issues, fallback to Haiku |
| Large templates exceed context | Truncate CSS, send only relevant sections |
| OpenRouter downtime | Fallback to Claude CLI |
| Model API changes | Abstract behind provider interface |
| Layout quality poor | Route layout to Haiku (multi-model for complex sites) |

---

## 7. Decision Required

**Approve this design to proceed with Phase 1 prototype?**

The prototype reuses eval pack components (OpenRouter runner, quality checker, prompt patterns) and can be tested against the same 21 templates as gold standards.
