# Site Builder Agent Eval Pack

An evaluation framework for AI code generators that produce multi-file artifacts (websites). Tests models across 16 sequential actions, scores output using a violation-deduction model, and drives skill improvements through empirical failure analysis.

## Why This Exists

Most LLM benchmarks evaluate text — single functions, code patches, or isolated snippets. This framework evaluates **complete deployable websites**: HTML, CSS, JavaScript, and assets working together as a system.

A correct `index.html` paired with broken `styles.css` is a broken site. The evaluation must understand that relationship.

## How It Works

### 4-Layer Evaluation Stack

| Layer | Component | What It Catches |
|-------|-----------|----------------|
| 1 | `FolderComparer` | Missing files, wrong structure, extra artifacts |
| 2 | `ContentComparer` | Missing text, paraphrased content, invalid meta tags |
| 3 | `HTMLVisualChecker` | Broken images, dark-on-dark text, empty sections, missing interactivity |
| 4 | `OpusJudge` | Multimodal LLM judge (code + screenshot + rubric) |

### Violation-Deduction Scoring

```
Score = 10 - sum(deductions)
```

Every action starts at 10. Each violation subtracts a fixed deduction. Scores can go negative. 22 violation types across 7 categories (structural, visual, content, code quality, accessibility, interactivity, performance) with severity tiers from critical (-5.0) to minor (-0.25).

### 16-Action Pipeline

Each model processes 16 sequential actions per template:

- **Brand** (5): colours, fonts, header logo, footer logo, favicon
- **Images** (2): hero background, section backgrounds
- **Content** (3): hero text, about text, contact info
- **Layout** (2): hero layout, sections layout
- **Technical** (3): SEO meta, structured data, accessibility
- **Quality** (1): contrast verification

Actions are sequential — errors compound, just like in production.

## Results Summary

Tested 5 models across 467 actions over 6 days:

| Model | Score | % of Max | Cost/Site | Variance |
|-------|-------|----------|-----------|----------|
| Claude Sonnet 4.6 | 149.5/160 | 93.4% | $1.05 | Baseline |
| Kimi K2.5 | 108.2/160 | 67.6% | $0.42 | High (SD 20.1) |
| Claude Haiku 4.5 | 107.7/160 | 67.3% | $0.35 | Low (SD 13.4) |
| DeepSeek V3.2 | 94.0/160 | 58.8% | $0.07 | Highest (SD 28.9) |
| DeepSeek R1 | 41.9/160 | 26.2% | $0.20 | Unsuitable |

Key findings:
- **Layout transformation averages -0.8/10** — every model makes pages worse
- **SEO and accessibility score 9+/10** — structured tasks are token-native
- **All models hallucinate image URLs** — writing descriptions as `src` attributes
- **Models paraphrase content 30% of the time** instead of using verbatim text
- **Data quality > model quality** — improving Figma extraction had more impact than switching models

## Project Structure

```
3_site_builder_agent_eval/
├── eval_core/                    # Shared evaluation engine (63 Python files)
│   ├── runners/                  # Model runners (Bedrock, Direct, Claude Code, OpenRouter)
│   ├── judges/                   # Opus multimodal judge + visual judge
│   ├── scoring/                  # Scorer + violation catalogue (22 types)
│   ├── visual/                   # HTMLVisualChecker + Playwright screenshots + SSIM
│   ├── folder_compare/           # Structural tree diff + content diff
│   ├── figma/                    # Figma API extraction → prompt builder
│   ├── refiners/                 # Inline teacher for prompt improvement
│   ├── reporters/                # HTML/Markdown report generation
│   ├── orchestrator.py           # Main eval pipeline orchestrator
│   └── routing.py                # Multi-model router
├── eval_packs/local/             # CLI + test harness
├── gold-standards/               # 21 hand-verified reference templates
│   ├── template-ai-page-builder/
│   ├── template-safari-lodge/
│   ├── template-saas-product/
│   └── ... (21 templates)
├── reports/                      # Analysis reports
├── research/                     # Research documentation
├── skill_enhancements/           # 6 production skill improvement diffs
├── scripts/                      # Utility scripts
├── tests/                        # Unit tests
├── eval_config.yaml              # Model registry (configurable)
└── pyproject.toml                # Package configuration
```

## Gold Standards

21 reference templates covering landing pages, SaaS products, corporate sites, events, safari lodges, training portals, and more. Each includes:

- `requirements.md` — business customisation spec (brand, content, layout)
- `stage-1-customise-template/` — skeleton with spec applied
- `stage-2-site-generation/` — optimised and validated
- `stage-3-deployment/` — deploy config and manifest

All hand-built, git-committed, and human-verified.

## Models Supported

Configured via `eval_config.yaml`. Currently tested:

| Model | Provider | Status |
|-------|----------|--------|
| Claude Sonnet 4.6 | Claude Code CLI | Gold standard |
| Claude Haiku 4.5 | Claude Code CLI | Enabled |
| Kimi K2.5 | OpenRouter | Enabled |
| DeepSeek V3.2 | OpenRouter | Enabled |
| DeepSeek R1 | OpenRouter | Disabled (unsuitable for code gen) |

Adding a new model: add an entry to `eval_config.yaml` with model ID, provider, and parameters.

## Setup

### Prerequisites

- Python 3.11+
- AWS account with Bedrock access (for Bedrock runner)
- OpenRouter API key (for OpenRouter models)
- Playwright (for visual screenshots)

### Install

```bash
# Clone
git clone https://github.com/tsekatm/3_site_builder_agent_eval.git
cd 3_site_builder_agent_eval

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Install Playwright browsers
playwright install chromium
```

### Configure

```bash
# Copy and edit environment variables
cp .env.example .env
# Add: OPENROUTER_API_KEY, AWS_PROFILE
```

### Run Tests

```bash
pytest tests/ -v
```

## Skill Enhancements

The evaluation drove 1,191 lines of improvements across 6 production skills:

| Skill | Before | Projected | Lines Added |
|-------|--------|-----------|-------------|
| Layout Transformation | 0.8/5 | 2.8+ | 250 |
| Template Customisation | 3.5/5 | 4.2+ | 220 |
| Background Images | 3.5/5 | 4.3+ | 210 |
| Colour Management | 2.1/5 | 3.5+ | 180 |
| Font Management | 2.0/5 | 3.8+ | 145 |
| Logo Replacement | 4.5/5 | 4.8+ | polish |

Diffs are in `skill_enhancements/`.

## Blog Series

This work is documented in a 7-part article series:

1. [Beyond Text: How We Built an Evaluation Framework for Multi-File AI Outputs](https://dev.to/tsekatm/beyond-text-how-we-built-an-evaluation-framework-for-multi-file-ai-outputs-1d10)
2. 5 Models, 467 Actions, 1 Winner (coming soon)
3. Building an LLM Judge That Doesn't Lie (coming soon)
4. The $0.07 vs $1.05 Question (coming soon)
5. Why Every LLM Breaks CSS Layouts (coming soon)
6. Data Quality > Model Quality (coming soon)
7. From Eval Failures to Production Skills (coming soon)

## License

MIT
