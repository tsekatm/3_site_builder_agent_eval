# Eval Pack Round 2 — Plan

**Date**: 2026-03-30
**Purpose**: Rigorous evaluation + chain-of-thought distillation + fine-tuning dataset preparation
**Status**: DRAFT — Awaiting Approval

---

## 1. Why Round 2

Round 1 was exploratory — small sample sizes, different measurement methods, no confidence intervals. The qualitative findings (layout destruction, image hallucination, skill enhancements) are solid. The quantitative rankings are noise.

Round 2 fixes the methodology AND adds a new goal: **prepare training data for a custom fine-tuned model**. Every judge score, every THINK block, every failure analysis becomes a training signal.

---

## 2. Three Workstreams

```
Workstream A: Rigorous Evaluation (fix Round 1 gaps)
Workstream B: Chain-of-Thought Distillation (THINK blocks via Opus)
Workstream C: Fine-Tuning Dataset Preparation (JSONL export)
```

### Dependencies

```
A (evaluation) ──► B (distillation uses failure data from A)
      │                    │
      └──────────┬─────────┘
                 ▼
            C (dataset combines scored outputs + THINK blocks)
```

---

## 3. Workstream A: Rigorous Evaluation

### 3.1 Fix the Methodology

| Round 1 Issue | Round 2 Fix |
|---------------|-------------|
| Sonnet scored via gold standard, not pipeline | **Run Sonnet through the same 16-action pipeline** |
| 2-15 runs per model | **Minimum 15 runs per model per template** |
| Not all models on all templates | **All models on all 6 templates** |
| No confidence intervals | **Report 95% CI for every score** |
| Judge bias (Claude judging Claude) | **Add second judge (GPT-4o via OpenRouter) on 20% of runs** |
| HTMLVisualChecker optional | **Mandatory on every action** |
| No inter-rater reliability | **Compute Cohen's kappa between Claude judge and GPT-4o judge** |

### 3.2 Evaluation Matrix

| Model | Templates | Runs/Template | Total Runs |
|-------|-----------|--------------|------------|
| Claude Sonnet 4.6 | 6 | 15 | 90 |
| Claude Haiku 4.5 | 6 | 15 | 90 |
| Kimi K2.5 | 6 | 15 | 90 |
| DeepSeek V3.2 | 6 | 15 | 90 |
| **Total** | | | **360 pipeline runs** |

DeepSeek R1 and Routed dropped (insufficient evidence they're viable).

### 3.3 Estimated Compute

- 360 runs × 16 actions × ~3 min/action = ~288 hours
- With 4-way parallelism: ~72 hours (~3 days)
- OpenRouter cost: ~$50-80 (mostly Sonnet runs)

### 3.4 Scoring Improvements

**Two-judge system**:
```
Every action scored by:
  1. Primary judge: Claude Sonnet (existing OpusJudge)
  2. Secondary judge: GPT-4o (on 20% of runs, random sample)
  3. HTMLVisualChecker: mandatory automated checks (100% of runs)

Final score = Primary judge score + HTMLVisualChecker deductions
Inter-rater reliability = Cohen's kappa on the 20% overlap
```

**Blind judging**: Strip model name from output before sending to judge. The judge sees only the HTML/CSS, not which model produced it.

---

## 4. Workstream B: Chain-of-Thought Distillation

### 4.1 The Problem

Cheaper models fail on hard tasks (layout, colours, images) not because they can't follow instructions, but because **there are no instructions to follow**. They just start writing CSS. The THINK block pattern forces a pre-flight checklist before code generation.

### 4.2 Opus as Teacher — Three-Step Process

For each failed action:

**Step 1: Failure Analysis** (Opus reviews the output)
```
INPUT:  Failed action output + gold standard + judge score + violations
OUTPUT: Root cause — not "the CSS was wrong" but "the model didn't
        inventory existing grid containers before adding new ones"
```

**Step 2: THINK Block Draft** (Opus writes the checklist)
```
OUTPUT: 5-8 step pre-flight checklist (each step < 15 words)
        Verification gates, not explanations.
        Pattern: INVENTORY → PLAN → EXECUTE → VERIFY
```

**Step 3: Validation** (Opus checks for redundancy)
```
CHECK: Is this redundant with existing skill content?
CHECK: Is it under 8 steps?
CHECK: Would it have prevented the specific failure?
```

### 4.3 Target Actions (Ordered by Gap from Sonnet)

| Priority | Action | Avg Gap | Current Skill | THINK Block Needed |
|----------|--------|---------|--------------|-------------------|
| **P0** | apply-sections-layout | -10.2 | `layout_transformation.skill.md` | Yes — inventory + namespace |
| **P0** | apply-hero-layout | -5.4 | `layout_transformation.skill.md` | Yes — hero-specific gates |
| **P1** | apply-colours | -3.3 | `colour_management.skill.md` | Yes — variable mapping |
| **P1** | replace-section-bgs | -2.8 | `background_image_changer.skill.md` | Yes — overlay + contrast |
| **P1** | update-contact | -2.7 | `template_customization.skill.md` | Yes — field mapping |
| **P2** | replace-hero-bg | -2.3 | `background_image_changer.skill.md` | Yes — URL validation |
| **P2** | swap-fonts | -2.4 | `global_font_management.skill.md` | Yes — cascade checklist |
| **P2** | replace-footer-logo | -2.5 | `logo_replacement.skill.md` | Yes — path resolution |

### 4.4 THINK Block Format (Standard)

```markdown
## THINK before {action_name}:
1. {INVENTORY step — what exists now}
2. {INVENTORY step — what needs to change}
3. {PLAN step — how to change it safely}
4. {EXECUTE step — the actual change}
5. {VERIFY step — diff/check after change}
```

**Constraints**:
- Max 8 steps
- Each step < 15 words
- No explanations — only imperatives (LIST, FIND, MAP, CHECK, VERIFY)
- Must be testable — a judge can verify each step was followed

### 4.5 Draft THINK Blocks (P0 Actions)

**apply-sections-layout**:
```markdown
## THINK before transforming section layout:
1. LIST every existing grid/flex container and its children count
2. NOTE which CSS classes control responsive breakpoints
3. IDENTIFY content that will be displaced by the new layout
4. WRITE the new layout using ONLY the existing class namespace
5. VERIFY no content was removed — diff section count before/after
6. TEST: responsive breakpoints still collapse to single column at 768px
```

**apply-hero-layout**:
```markdown
## THINK before transforming hero layout:
1. FIND the hero section element and its current CSS position/display
2. LIST all child elements (heading, subheading, CTA, background image)
3. NOTE the current text alignment and overlay opacity
4. APPLY the new layout pattern WITHOUT removing any child elements
5. VERIFY the background image is still visible behind the overlay
6. CHECK text is readable (white text on dark overlay, min rgba(0,0,0,0.5))
```

**apply-colours**:
```markdown
## THINK before applying brand colours:
1. FIND the :root or CSS custom property declarations
2. MAP each new brand colour to an existing variable name
3. CHANGE only the variable declarations, never the usage sites
4. CHECK text-on-background contrast for every pairing (min 4.5:1)
5. VERIFY buttons and links use the accent colour, not the background colour
```

### 4.6 Measurement — Do THINK Blocks Work?

Run two evaluation batches (Round 2):

| Batch | Skills Version | Purpose |
|-------|---------------|---------|
| **Batch 1** | Current skills (no THINK blocks) | Baseline |
| **Batch 2** | Skills + THINK blocks | Measure improvement |

Compare scores per action between batches. If THINK blocks work:
- P0 actions should improve by ≥3 points
- P1 actions should improve by ≥1.5 points
- No other actions should regress

---

## 5. Workstream C: Fine-Tuning Dataset Preparation

### 5.1 Why Fine-Tune

The THINK blocks improve prompt quality, but every model still re-reads them on every call. A fine-tuned model **internalises** the reasoning patterns, eliminating the prompt overhead.

### 5.2 Training Data Format (JSONL)

Each training example is one action from one run:

```jsonl
{
  "messages": [
    {
      "role": "system",
      "content": "You are a website customisation expert. Apply the requested change to the HTML/CSS."
    },
    {
      "role": "user",
      "content": "## Action: apply-sections-layout\n## Skill: layout_transformation\n## THINK block:\n1. LIST every existing grid/flex...\n\n## Current HTML:\n{html}\n\n## Current CSS:\n{css}\n\n## Requirements:\n{requirements}"
    },
    {
      "role": "assistant",
      "content": "## Thinking:\n1. Found 3 grid containers: .features-grid (3 cols), .cards-grid (2 cols), .footer-grid (4 cols)\n2. Breakpoints: 768px collapses to 1 col, 1024px to 2 cols\n3. New bento layout will affect .features-grid only\n4. Using existing .features-grid class, changing grid-template to bento pattern\n5. All 6 feature cards preserved\n\n## Output:\n{correct_html}\n\n{correct_css}"
    }
  ],
  "metadata": {
    "action": "apply-sections-layout",
    "template": "template-safari-lodge",
    "model": "claude-sonnet-4.6",
    "score": 9.0,
    "judge": "claude-sonnet-4.6",
    "violations": [],
    "run_id": "20260401_001",
    "think_steps_followed": [true, true, true, true, true]
  }
}
```

### 5.3 Dataset Composition

| Source | Examples | Quality Filter |
|--------|---------|---------------|
| **Sonnet outputs scoring ≥ 8.0** | ~1,200 (90 runs × ~14 passing actions) | High quality — use as positive examples |
| **Sonnet outputs scoring < 8.0** | ~180 (layout/colour failures) | Include with Opus-corrected output |
| **Kimi/Haiku outputs scoring ≥ 9.0** | ~200 (SEO, a11y, text actions) | Cheap model can do these — positive examples |
| **Opus failure analysis** | ~180 | The "thinking" trace showing WHY the correct approach works |
| **Total** | **~1,760 training examples** |

### 5.4 Quality Gates for Training Data

Every training example must pass:

1. **Score ≥ 8.0** (or Opus-corrected if < 8.0)
2. **HTMLVisualChecker: 0 critical violations**
3. **THINK steps verifiable** — judge confirms each step was followed
4. **Complete HTML** — has `<!DOCTYPE>`, `</html>`, no backticks
5. **No hallucinated images** — all `src` attributes start with `https://`

### 5.5 Export Pipeline

```
Round 2 runs (360)
    │
    ▼
Score + judge + visual checker
    │
    ▼
Filter: score ≥ 8.0 AND 0 critical violations
    │
    ▼
Opus teacher: analyse failures, write thinking traces
    │
    ▼
Format as JSONL (messages + metadata)
    │
    ▼
Split: 80% train / 10% validation / 10% test
    │
    ▼
Upload to fine-tuning provider (Anthropic / OpenAI / Together)
```

---

## 6. Skill Enhancement Process (Opus Teacher Loop)

### 6.1 Per-Action Enhancement Cycle

```
For each of the 8 target actions:

1. COLLECT: All failed outputs (score < 7.0) from Round 2 Batch 1
2. ANALYSE: Opus reviews each failure alongside the gold standard
   - What reasoning step was missing?
   - What would have prevented this specific failure?
3. DRAFT: Opus writes a THINK block (5-8 steps, < 15 words each)
4. VALIDATE: Check against existing skill — no redundancy, no bloat
5. INJECT: Add THINK block to the skill file
6. TEST: Run Batch 2 with updated skills
7. MEASURE: Compare Batch 1 vs Batch 2 scores for this action
8. ITERATE: If improvement < 1.5 points, Opus revises the THINK block
```

### 6.2 Skill File Changes (Estimated)

| Skill File | THINK Blocks Added | Lines Added | Actions Covered |
|-----------|-------------------|-------------|----------------|
| `layout_transformation.skill.md` | 2 | ~12 | sections-layout, hero-layout |
| `colour_management.skill.md` | 1 | ~5 | apply-colours |
| `background_image_changer.skill.md` | 2 | ~10 | hero-bg, section-bgs |
| `template_customization.skill.md` | 1 | ~5 | update-contact |
| `global_font_management.skill.md` | 1 | ~5 | swap-fonts |
| `logo_replacement.skill.md` | 1 | ~5 | replace-footer-logo |
| **Total** | **8** | **~42 lines** | 8 actions |

Not 1,191 lines like Round 1. **42 lines of surgical THINK blocks** targeting specific failure modes.

---

## 7. Judge Improvements for Fine-Tuning Quality

### 7.1 Structured Judge Output

The judge must produce structured, machine-parseable output for the training dataset:

```json
{
  "action": "apply-sections-layout",
  "score": 7.5,
  "violations": [
    {"id": "LAYOUT-GRID-BROKEN", "severity": "major", "deduction": -2.0,
     "description": "3-column grid collapsed to single column",
     "location": ".features-grid", "line": 145}
  ],
  "think_steps_verified": {
    "step_1_inventory": true,
    "step_2_breakpoints": true,
    "step_3_displaced": false,
    "step_4_namespace": true,
    "step_5_content_check": false
  },
  "reasoning": "Model inventoried grid containers but did not check for displaced content. Step 3 failure led to missing 2 feature cards."
}
```

### 7.2 THINK Step Verification

The judge doesn't just score the output — it **verifies each THINK step was followed**:

```
THINK step 1: "LIST every existing grid/flex container"
Judge checks: Does the output preserve all grid containers from the input?
Result: true/false

THINK step 5: "VERIFY no content was removed"
Judge checks: Does output have same number of sections/cards as input?
Result: true/false
```

This produces per-step success rates that identify which reasoning gates models skip.

### 7.3 Judge Calibration Protocol

Before Round 2 starts:

1. **Gold set**: 20 pre-scored examples (5 per quality tier: 0-3, 4-6, 7-8, 9-10)
2. **Claude judge** scores the gold set
3. **GPT-4o judge** scores the same gold set
4. **Compute Cohen's kappa** — target ≥ 0.7 (substantial agreement)
5. **If kappa < 0.7**: revise judge prompt until calibrated

---

## 8. Deliverables

| # | Deliverable | Workstream | Output |
|---|------------|-----------|--------|
| D1 | 360 evaluated runs with CI | A | `runs/round2/` with scores.json per run |
| D2 | Inter-rater reliability report | A | Cohen's kappa, agreement matrix |
| D3 | 8 THINK blocks injected into skills | B | 6 skill files updated (~42 lines) |
| D4 | Batch 1 vs Batch 2 comparison | B | Per-action improvement measurement |
| D5 | JSONL fine-tuning dataset (~1,760 examples) | C | `datasets/finetune_v1.jsonl` |
| D6 | Dataset quality report (coverage, score distribution) | C | `reports/dataset_quality.md` |
| D7 | Updated eval report V3 with Round 2 data | A | `reports/eval_pack_analysis_report_v3.md` |

---

## 9. Timeline

| Day | Activity |
|-----|----------|
| 1 | Judge calibration (gold set + kappa). Draft THINK blocks for P0 actions. |
| 2-3 | Batch 1: 180 runs (4 models × 6 templates × ~8 runs each, no THINK blocks) |
| 3 | Opus failure analysis on Batch 1 results. Finalise all 8 THINK blocks. |
| 4-5 | Batch 2: 180 runs (same matrix, WITH THINK blocks) |
| 5 | Score comparison, identify improvements. Opus refines blocks that didn't help. |
| 6 | JSONL export, dataset quality checks, train/val/test split |
| 7 | Final report V3 with Round 2 data, CI, and THINK block impact analysis |

---

## 10. Approval Required

Before starting:
1. **Budget**: ~$50-80 OpenRouter costs for 360 runs
2. **Templates**: Confirm the 6 templates (or add more from the 21 available)
3. **Models**: Confirm 4 models (Sonnet, Haiku, Kimi, DeepSeek V3.2)
4. **Fine-tuning target**: Which provider? (Anthropic, OpenAI, Together AI)
