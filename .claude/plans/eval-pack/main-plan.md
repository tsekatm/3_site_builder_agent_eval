# EVAL-PACK-001: Site Builder Agent Evaluation Pack

**Project**: Agent/Skill Evaluation & Refinement Pipeline
**Created**: 2026-03-21
**Updated**: 2026-03-22
**Status**: IN PROGRESS — Stage 7 LLD approved, Stage 8 Tier 1 Build in progress
**Owner**: Tebogo Tseka
**Methodology**: Agentic Project Manager (Multi-Stage, Multi-Sub-Plan)

---

## Executive Summary

Build a **folder-based** evaluation pack that tests site builder agents across 3 pipeline stages, scores output against validated gold standard reference sites using a **violation-deduction model** (10 minus deductions, can go negative), and uses Claude Opus 4.6 as the judge model. Models are configurable via YAML and run in parallel.

**Evaluation Pipeline (per template, per model):**

| Stage | Agent Task | Input | Gold Standard |
|-------|-----------|-------|---------------|
| 1. Customise Template | Apply colours, fonts, logos, images, text, layout, SEO, a11y to template skeleton | `bigbeard-templates/` skeleton + `requirements.md` | Validated customised output folder |
| 2. Site Generation | Optimise, validate, package for deployment | Customised template | Validated deployment-ready folder |
| 3. Deployment | Deploy to staging (S3 + CloudFront preview) | Deployment-ready folder | Validated deployed site + config |

**Template Source**: 21 anonymised skeletons in `bigbeard-templates/` (20 existing + 1 HASA CRMP pending)

**Scoring**: 10 per stage, deduct for violations, **can go negative**. Template total = sum of 3 stages (max 30).

---

## Evaluation Architecture

```
Requirements (per template)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent executes 3 stages against requirement                │
│                                                             │
│  Stage 1: Figma → Template  ──► output folder               │
│  Stage 2: Site Generation   ──► output folder               │
│  Stage 3: Deployment        ──► output folder + deploy cfg  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  Eval Engine (per stage)                                    │
│                                                             │
│  1. Structural checks   ──► file tree vs gold standard      │
│  2. Content checks      ──► HTML/CSS validation, text match │
│  3. Visual checks       ──► Playwright screenshot + SSIM    │
│  4. LLM Judge (Opus)    ──► code + screenshot + rubric      │
│     Returns: violation list with deductions                 │
│                                                             │
│  Score = 10 - sum(deductions)   [CAN GO NEGATIVE]           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  Results (per template, per model)                          │
│                                                             │
│  Stage 1: 10 - 2.5 = 7.5                                   │
│  Stage 2: 10 - 4.0 = 6.0                                   │
│  Stage 3: 10 - 1.0 = 9.0                                   │
│  ─────────────────────────                                  │
│  Template Total: 22.5 / 30                                  │
│                                                             │
│  Cross-model comparison + skill enhancement diffs           │
└─────────────────────────────────────────────────────────────┘
```

---

## Gold Standard Reference Structure

Template skeletons already exist in `bigbeard-templates/` (anonymised Big Beard designs). Gold standards are the expected CUSTOMISED output after applying business requirements.

```
bigbeard-templates/                         # INPUT: anonymised skeletons (already exist)
├── technology/ai-page-builder/index.html   # e.g., Chirrup skeleton
├── hospitality/safari-lodge/index.html     # e.g., Etali Safari skeleton
├── ...                                     # 21 templates total

gold-standards/                             # EXPECTED OUTPUT: customised references
├── template-ai-page-builder/
│   ├── requirements.md                     # Business customisation requirements
│   ├── stage-1-customise-template/         # Skeleton + requirements applied
│   │   ├── index.html
│   │   ├── css/
│   │   ├── assets/
│   │   └── manifest.json
│   ├── stage-2-site-generation/            # Optimised, validated, packaged
│   │   ├── index.html
│   │   ├── css/
│   │   ├── js/
│   │   ├── assets/
│   │   └── manifest.json
│   └── stage-3-deployment/                 # Deploy config + staging artifacts
│       ├── site-files/
│       ├── deployment-config.json
│       └── screenshots/                    # Reference screenshots
```

---

## Scoring Model

### Violation-Deduction (10 per stage, no floor)

```
Stage Score = 10 - sum(deductions)
Template Score = Stage 1 + Stage 2 + Stage 3   (max 30)

Score CAN go negative. No floor at 0.
```

### Violation Catalogue

| Category | Violation | Severity | Deduction |
|----------|-----------|----------|-----------|
| **Structural** | Missing required file (index.html) | Critical | -3.0 |
| **Structural** | Missing asset referenced in HTML | Major | -1.5 |
| **Structural** | Wrong directory structure | Major | -1.0 |
| **Structural** | Extra/unexpected files | Minor | -0.25 |
| **Visual** | Layout completely broken | Critical | -3.0 |
| **Visual** | Significant visual deviation (SSIM < 0.7) | Major | -2.0 |
| **Visual** | Minor visual deviation (SSIM 0.7-0.9) | Moderate | -1.0 |
| **Visual** | Colour mismatch vs reference | Moderate | -0.5 |
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

### Severity Weights

| Severity | Deduction Range | Meaning |
|----------|----------------|---------|
| Critical | -2.0 to -3.0 | Fundamentally broken |
| Major | -1.0 to -2.0 | Client would reject |
| Moderate | -0.5 to -1.0 | Noticeable but not fatal |
| Minor | -0.25 | Polish issues |

---

## Pipeline Deployment Tiers

| Tier | Name | Where It Runs | Prototype? |
|------|------|---------------|------------|
| **Tier 1** | **IDE / Local** | Developer machine, Bedrock API calls | **YES — built first** |
| **Tier 2** | **Hybrid** | Local CLI → S3 storage + Bedrock managed eval | Built second |
| **Tier 3** | **AWS** | `CreateEvaluationJob` (Bedrock manages judging) | Built third |

---

## Model Configuration & Parallel Execution

Models are configurable via `eval_config.yaml`. Not hardcoded.

```yaml
models:
  deepseek-r1:
    model_id: "us.deepseek.r1-v1:0"
    region: "us-east-1"
    params: { temperature: 0.3, max_tokens: 8192 }
    enabled: true

  deepseek-v3.2:
    model_id: "deepseek.v3.2"
    region: "us-east-1"
    params: { temperature: 0.2, max_tokens: 8192 }
    enabled: true

  kimi-k2.5:
    model_id: "moonshotai.kimi-k2.5"
    region: "us-east-1"
    params: { temperature: 0.2, max_tokens: 16384 }
    enabled: true

judges:
  default:
    model_id: "anthropic.claude-opus-4-20250514"
    region: "us-east-1"
    params: { temperature: 0.0, max_tokens: 8192 }

defaults:
  parallel_workers: 3
  parallel_prompts: 5
```

### CLI

```bash
eval-cli run --model all --template chirrup     # All models, parallel
eval-cli run --model deepseek-r1 --template chirrup --stage 1
eval-cli run --model-tag code-gen               # By tag
eval-cli refine --run <dir> --target-score 7.0
eval-cli apply --run <dir> --mode interactive
eval-cli compare --run-a <dir> --run-b <dir>
eval-cli history --template chirrup
```

### Run Output Structure

```
runs/20260322_143000/
├── config.json
├── template-chirrup/
│   ├── deepseek-r1/
│   │   ├── stage-1-figma-to-template/    # Agent output folder
│   │   ├── stage-2-site-generation/      # Agent output folder
│   │   ├── stage-3-deployment/           # Agent output folder
│   │   ├── screenshots/                  # Rendered screenshots
│   │   └── scores.json                   # Per-stage violations + scores
│   ├── kimi-k2.5/
│   │   └── ...
│   └── comparison.json                   # Cross-model comparison
├── diffs/                                # Skill enhancement proposals
├── report.md                             # Unified report
└── bedrock_export/                       # BYOI JSONL per model
```

---

## Agent Runtime Proxy Router

Agents currently run on Claude SDK. Configurable routing to Bedrock models.

| Phase | What | Effort |
|-------|------|--------|
| Phase 1 | `AnthropicBedrock` drop-in for Claude | 1-2 days |
| Phase 2 | Multi-model eval config | 3-5 days |
| Phase 3 | DeepSeek adapter for non-tool tasks | 2-4 weeks |

**Key constraint**: DeepSeek R1 has **no tool calling** on Bedrock. Full agent execution on R1 not practical. Phase 3 targets non-tool subtasks only.

---

## Stage Progress

| # | Stage / Sub-Step | Status | Sub-Plan |
|---|-----------------|--------|----------|
| | **RESEARCH PHASE** | | |
| **1** | **Research (v2)** | **COMPLETE** | [View](stage-1-research.md) |
| 1.1 | Folder-based site evaluation patterns | COMPLETE | — |
| 1.2 | Visual & rendered site evaluation | COMPLETE | — |
| 1.3 | Violation-based scoring model | COMPLETE | — |
| 1.4 | LLM-as-judge for multi-file artifacts | COMPLETE | — |
| 1.5 | Gold standard validation patterns | COMPLETE | — |
| 1.6 | Agent runtime proxy routing | COMPLETE | — |
| 1.7 | Bedrock evaluations integration | COMPLETE | — |
| 1.8 | Model capability mapping | COMPLETE | — |
| | | | |
| **2** | **HITL: Research Approval** | **COMPLETE** | [View](stage-2-hitl-research.md) |
| 2.1 | Present research v2 for verification | COMPLETE | — |
| 2.2 | Confirm scoring model (10 - deductions, negative ok) | COMPLETE | — |
| 2.3 | Confirm folder-based eval approach | COMPLETE | — |
| 2.4 | Confirm judge model (Opus 4.6) | COMPLETE | — |
| 2.5 | Confirm proxy router approach | COMPLETE | — |
| 2.6 | Final research approval | COMPLETE | — |
| | | | |
| | **HLD PHASE** | | |
| **3** | **HLD: High-Level Design (All Tiers)** | **COMPLETE** | [3.7_HLD](../../../2_bbws_docs/HLDs/3_site_builder/3.7_Site_Builder_Eval_Pack_HLD.md) |
| 3.1 | System context & scope (3 tiers, 3 pipeline stages) | COMPLETE | — |
| 3.2 | Gold standard reference site architecture | COMPLETE | — |
| 3.3 | Eval engine architecture (structural + content + visual + judge) | COMPLETE | — |
| 3.4 | Component architecture (shared core, CLI, runners, judge) | COMPLETE | — |
| 3.5 | Model configuration & parallel execution | COMPLETE | — |
| 3.6 | Agent runtime proxy router architecture | COMPLETE | — |
| 3.7 | Data flow per tier (local / hybrid / aws) | COMPLETE | — |
| 3.8 | Scoring model & violation catalogue | COMPLETE | — |
| 3.9 | Non-functional requirements (cost, performance, versioning) | COMPLETE | — |
| 3.10 | HLD document assembly | COMPLETE | — |
| | | | |
| **4** | **HITL: HLD Approval** | **COMPLETE** | — |
| 4.1 | Present HLD for review | COMPLETE | — |
| 4.2 | Walk through architecture decisions | COMPLETE | — |
| 4.3 | Collect feedback & iterate | COMPLETE (no changes) | — |
| 4.4 | Final HLD approval | COMPLETE (2026-03-22) | — |
| | | | |
| | **GOLD STANDARD CREATION** | | |
| **5** | **Create Gold Standard Reference Sites** | **COMPLETE** | [View](stage-5-gold-standards.md) |
| 5.1 | Select Figma templates (21 templates) | COMPLETE | — |
| 5.2 | Define requirements per template (21 requirements.md) | COMPLETE | — |
| 5.3 | Stage 1 reference: Templates exist in bigbeard-templates/ | COMPLETE | — |
| 5.4 | HITL: Verify Stage 1 (templates already validated) | COMPLETE | — |
| 5.5 | Stage 2 reference: 21 customised sites (Claude Opus) | COMPLETE | — |
| 5.6 | HITL: Verify Stage 2 (user reviewed 4 sites, approved) | COMPLETE | — |
| 5.7 | Stage 3 reference: 21 deployment configs | COMPLETE | — |
| 5.8 | HITL: Verify Stage 3 (deployment configs) | COMPLETE | — |
| 5.9 | ~~Screenshots~~ → moved to Stage 8 (eval engine captures at runtime) | N/A | — |
| 5.10 | Commit gold standards to git | COMPLETE (5a7bbb2) | — |
| | *Note: Single-page gold standards for prototype. Multi-page expansion planned for future iteration.* | | |
| | | | |
| | **TIER 1 — IDE / LOCAL** | | |
| **6** | **LLD: Tier 1 (IDE / Local)** | **COMPLETE** | [3.7.1_LLD](../../../2_bbws_docs/LLDs/3_site_builder/3.7.1_LLD_Eval_Pack_Tier1_Local.md) |
| 6.1 | Shared core module specification (`eval_core/`) | COMPLETE | — |
| 6.2 | CLI command specification | COMPLETE | — |
| 6.3 | Bedrock runner specification | COMPLETE | — |
| 6.4 | Model config schema (`eval_config.yaml`) | COMPLETE | — |
| 6.5 | Parallel execution engine specification | COMPLETE | — |
| 6.6 | Folder comparison engine specification | COMPLETE | — |
| 6.7 | Visual comparison specification (Playwright + SSIM) | COMPLETE | — |
| 6.8 | Judge prompt specification (code + screenshot + rubric) | COMPLETE | — |
| 6.9 | Violation catalogue specification (YAML format) | COMPLETE | — |
| 6.10 | Scoring engine specification (10 - deductions, no floor) | COMPLETE | — |
| 6.11 | Refinement engine specification | COMPLETE | — |
| 6.12 | Run versioning specification | COMPLETE | — |
| 6.13 | Report generation specification | COMPLETE | — |
| 6.14 | Proxy router specification (AnthropicBedrock) | COMPLETE | — |
| 6.15 | Test plan (TDD) | COMPLETE | — |
| 6.16 | LLD document assembly | COMPLETE | — |
| | | | |
| **7** | **HITL: Tier 1 LLD Approval** | **COMPLETE** | — |
| 7.1 | Present Tier 1 LLD for review | COMPLETE | — |
| 7.2 | Walk through specifications | COMPLETE | — |
| 7.3 | Collect feedback & iterate | COMPLETE (added per-action eval model v1.1) | — |
| 7.4 | Final Tier 1 LLD approval | COMPLETE (2026-03-23) | — |
| | | | |
| **8** | **Build: Tier 1 (IDE / Local)** | **COMPLETE** | 100 tests passing |
| 8.1 | Project scaffold & shared core | COMPLETE | — |
| 8.2 | Model config loader | COMPLETE | — |
| 8.3 | Bedrock runners + proxy router | COMPLETE | — |
| 8.4 | Parallel execution engine | COMPLETE | — |
| 8.5 | Folder comparison engine | COMPLETE | — |
| 8.6 | Visual comparison (Playwright + SSIM) | COMPLETE | — |
| 8.7 | Judge engine (Opus multimodal: code + screenshots) | COMPLETE | — |
| 8.8 | Scoring engine (violations → deductions → score) | COMPLETE | — |
| 8.9 | Refinement engine (teacher + diff + apply) | COMPLETE | — |
| 8.10 | Run versioning | COMPLETE | — |
| 8.11 | Report generation | COMPLETE | — |
| 8.12 | CLI commands | COMPLETE | — |
| 8.13 | Integration testing | COMPLETE (100 unit tests) | — |
| | | | |
| **9** | **Execute: Tier 1 — Eval Run** | PENDING | [View](stage-9-tier1-execution.md) |
| 9.1 | Baseline eval run (all models, all templates, all 3 stages) | PENDING | — |
| 9.2 | Present baseline results for verification | PENDING | — |
| 9.3 | Refinement loop (teacher generates skill diffs) | PENDING | — |
| 9.4 | Present diffs for HITL accept/reject | PENDING | — |
| 9.5 | Apply changes & re-run | PENDING | — |
| 9.6 | Present refined results for verification | PENDING | — |
| | | | |
| **10** | **HITL: Tier 1 Results Review** | PENDING | [View](stage-10-hitl-tier1-results.md) |
| 10.1 | Full evaluation report | PENDING | — |
| 10.2 | Cross-model comparison per stage | PENDING | — |
| 10.3 | Score trajectory (baseline → refined) | PENDING | — |
| 10.4 | Skill enhancement summary | PENDING | — |
| 10.5 | Lessons learned & Tier 1 sign-off | PENDING | — |
| | | | |
| | **TIER 2 — HYBRID (Local → AWS)** | | |
| **11** | **LLD: Tier 2 (Hybrid)** | PENDING | [View](stage-11-lld-tier2.md) |
| 11.1 | S3 storage adapter specification | PENDING | — |
| 11.2 | Bedrock `CreateEvaluationJob` integration (BYOI) | PENDING | — |
| 11.3 | CLI `--mode hybrid` specification | PENDING | — |
| 11.4 | CLI `export` command specification | PENDING | — |
| 11.5 | Terraform specification (S3, IAM) | PENDING | — |
| 11.6 | Test plan (Tier 2) | PENDING | — |
| 11.7 | LLD document assembly | PENDING | — |
| | | | |
| **12** | **HITL: Tier 2 LLD Approval** | PENDING | [View](stage-12-hitl-lld-tier2.md) |
| 12.1 | Present Tier 2 LLD | PENDING | — |
| 12.2 | Collect feedback & iterate | PENDING | — |
| 12.3 | Final Tier 2 LLD approval | PENDING | — |
| | | | |
| **13** | **Build: Tier 2 (Hybrid)** | PENDING | [View](stage-13-tier2-build.md) |
| 13.1 | Terraform: S3 bucket + IAM role | PENDING | — |
| 13.2 | S3 storage adapter | PENDING | — |
| 13.3 | Bedrock `CreateEvaluationJob` integration | PENDING | — |
| 13.4 | CLI `--mode hybrid` + `export` | PENDING | — |
| 13.5 | Integration testing | PENDING | — |
| | | | |
| **14** | **HITL: Tier 2 Results Review** | PENDING | [View](stage-14-hitl-tier2-results.md) |
| 14.1 | Demo hybrid run | PENDING | — |
| 14.2 | Verify S3 storage | PENDING | — |
| 14.3 | Tier 2 sign-off | PENDING | — |
| | | | |
| | **TIER 3 — AWS (Bedrock Managed Evaluations)** | | |
| **15** | **LLD: Tier 3 (AWS)** | PENDING | [View](stage-15-lld-tier3.md) |
| 15.1 | `CreateEvaluationJob` integration (BYOI + custom metrics) | PENDING | — |
| 15.2 | Custom metric definitions | PENDING | — |
| 15.3 | BYOI dataset preparation | PENDING | — |
| 15.4 | IAM eval service role specification | PENDING | — |
| 15.5 | CLI `--mode aws` specification | PENDING | — |
| 15.6 | Results parser specification | PENDING | — |
| 15.7 | Test plan (Tier 3) | PENDING | — |
| 15.8 | LLD document assembly | PENDING | — |
| | | | |
| **16** | **HITL: Tier 3 LLD Approval** | PENDING | [View](stage-16-hitl-lld-tier3.md) |
| 16.1 | Present Tier 3 LLD | PENDING | — |
| 16.2 | Collect feedback & iterate | PENDING | — |
| 16.3 | Final Tier 3 LLD approval | PENDING | — |
| | | | |
| **17** | **Build: Tier 3 (AWS)** | PENDING | [View](stage-17-tier3-build.md) |
| 17.1 | Terraform: IAM eval service role | PENDING | — |
| 17.2 | BYOI dataset builder | PENDING | — |
| 17.3 | Custom metric definitions | PENDING | — |
| 17.4 | CLI `--mode aws` | PENDING | — |
| 17.5 | Results parser | PENDING | — |
| 17.6 | Integration testing | PENDING | — |
| | | | |
| **18** | **HITL: Tier 3 Results & Final Sign-Off** | PENDING | [View](stage-18-hitl-final.md) |
| 18.1 | Demo Bedrock managed eval job | PENDING | — |
| 18.2 | Compare Tier 1 vs Tier 3 scores | PENDING | — |
| 18.3 | Cost analysis | PENDING | — |
| 18.4 | Final sign-off: all 3 tiers operational | PENDING | — |

---

## Project Output Structure

```
3_site_builder_agent_eval/
├── CLAUDE.md
├── eval_config.yaml                    # Configurable model registry
├── pyproject.toml
├── .claude/                            # TBT mechanics
│
├── eval_core/                          # Shared core (all tiers)
│   ├── runners/
│   ├── judges/
│   ├── refiners/
│   ├── scoring/
│   ├── visual/                         # Playwright + SSIM
│   ├── folder_compare/                 # Structural + content diff
│   └── reporters/
│
├── eval-packs/
│   ├── local/                          # Tier 1
│   │   ├── cli/
│   │   └── tests/
│   ├── hybrid/                         # Tier 2
│   │   ├── cli/
│   │   ├── terraform/
│   │   └── tests/
│   └── aws/                            # Tier 3
│       ├── cli/
│       ├── terraform/
│       └── tests/
│
├── gold-standards/                     # Validated reference sites
│   └── template-{name}/
│       ├── requirements.md
│       ├── stage-1-figma-to-template/
│       ├── stage-2-site-generation/
│       └── stage-3-deployment/
│
├── runs/                               # Timestamped eval runs
│   └── YYYYMMDD_HHMMSS/
│
├── research/                           # Research outputs
│   └── research.md
│
└── tests/                              # Cross-tier tests
```

---

## Deliverables

| # | Deliverable | Location | Stage |
|---|-------------|----------|-------|
| 1 | Research report (v2) | `research/research.md` | 1 |
| 2 | Approved research | Stage 2 | 2 |
| 3 | HLD document | `2_bbws_docs/HLDs/` | 3 |
| 4 | Approved HLD | Stage 4 | 4 |
| 5 | **Gold standard reference sites** | `gold-standards/` | 5 |
| 6 | Tier 1 LLD | `2_bbws_docs/LLDs/` | 6 |
| 7 | Approved Tier 1 LLD | Stage 7 | 7 |
| 8 | Tier 1 eval pack (local) | `eval-packs/local/` | 8 |
| 9 | Tier 1 eval results | `runs/` | 9 |
| 10 | Tier 1 sign-off | Stage 10 | 10 |
| 11 | Tier 2 LLD | `2_bbws_docs/LLDs/` | 11 |
| 12 | Tier 2 eval pack (hybrid) | `eval-packs/hybrid/` | 13 |
| 13 | Tier 2 sign-off | Stage 14 | 14 |
| 14 | Tier 3 LLD | `2_bbws_docs/LLDs/` | 15 |
| 15 | Tier 3 eval pack (aws) | `eval-packs/aws/` | 17 |
| 16 | Final sign-off | Stage 18 | 18 |

---

## Success Criteria

### Gate: Design
- [ ] HLD and all LLDs approved before code
- [ ] Gold standard reference sites created and HITL-approved

### Gate: Tier 1 — IDE / Local
- [ ] Agent executes 3 stages, produces output folders
- [ ] Judge scores each stage against gold standard (10 - deductions)
- [ ] Negative scores reported correctly
- [ ] Cross-model comparison works
- [ ] Refinement loop improves scores
- [ ] No AWS infrastructure needed

### Gate: Tier 2 — Hybrid
- [ ] Results stored in S3
- [ ] Bedrock managed eval via BYOI works

### Gate: Tier 3 — AWS
- [ ] `CreateEvaluationJob` with custom metrics succeeds
- [ ] Tier 1 vs Tier 3 scores are comparable

---

## Dependencies

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| Figma templates (user-supplied) | PENDING | Needed for Stage 5 |
| Bedrock model access in us-east-1 | TBD | DeepSeek, Kimi, Claude |
| Playwright installed | TBD | For screenshot capture |

---

## Navigation

| Sub-Plan | Phase | Description |
|----------|-------|-------------|
| [Stage 1: Research](stage-1-research.md) | Research | Folder-based eval, proxy routing, models |
| [Stage 2: HITL](stage-2-hitl-research.md) | Research | Verify research findings |
| [Stage 3: HLD](stage-3-hld.md) | Design | High-Level Design (all tiers) |
| [Stage 4: HITL](stage-4-hitl-hld.md) | Design | Approve HLD |
| [Stage 5: Gold Standards](stage-5-gold-standards.md) | Reference | Create + validate reference sites |
| [Stage 6: LLD Tier 1](stage-6-lld-tier1.md) | Tier 1 | Low-Level Design (IDE/Local) |
| [Stage 7: HITL](stage-7-hitl-lld-tier1.md) | Tier 1 | Approve Tier 1 LLD |
| [Stage 8: Build Tier 1](stage-8-tier1-build.md) | Tier 1 | IDE/Local eval pack |
| [Stage 9: Execute Tier 1](stage-9-tier1-execution.md) | Tier 1 | Eval runs + refinement |
| [Stage 10: HITL](stage-10-hitl-tier1-results.md) | Tier 1 | Tier 1 results + sign-off |
| [Stage 11: LLD Tier 2](stage-11-lld-tier2.md) | Tier 2 | Low-Level Design (Hybrid) |
| [Stage 12: HITL](stage-12-hitl-lld-tier2.md) | Tier 2 | Approve Tier 2 LLD |
| [Stage 13: Build Tier 2](stage-13-tier2-build.md) | Tier 2 | Hybrid mode |
| [Stage 14: HITL](stage-14-hitl-tier2-results.md) | Tier 2 | Tier 2 sign-off |
| [Stage 15: LLD Tier 3](stage-15-lld-tier3.md) | Tier 3 | Low-Level Design (AWS) |
| [Stage 16: HITL](stage-16-hitl-lld-tier3.md) | Tier 3 | Approve Tier 3 LLD |
| [Stage 17: Build Tier 3](stage-17-tier3-build.md) | Tier 3 | Bedrock managed eval |
| [Stage 18: HITL](stage-18-hitl-final.md) | Tier 3 | Final sign-off |
