# Stage 1: Research - Eval Frameworks & Patterns

**Parent Plan**: [main-plan.md](main-plan.md)
**Stage**: 1 of 6
**Status**: PENDING
**Dependencies**: None
**Blocks**: Stage 2 (HITL Research Approval)

---

## Objective

Conduct deep research into LLM evaluation frameworks, Bedrock Evaluations integration patterns, agent/skill evaluation methodologies, and analyze current site builder skills to define what "good output" looks like for each skill.

---

## Task Breakdown

| # | Task | Status | Worker | Description | Output |
|---|------|--------|--------|-------------|--------|
| 1.1 | Bedrock Evaluations Deep Dive | PENDING | worker-1 | API patterns, JSONL format, BYOI, judge model options, CLI integration, custom metrics | `worker-1/output.md` |
| 1.2 | Agent Eval Frameworks Survey | PENDING | worker-2 | Survey existing agent eval frameworks (AgentBench, LATS, SWE-bench, Inspect AI, promptfoo, braintrust) | `worker-2/output.md` |
| 1.3 | Skill Analysis & Golden Outputs | PENDING | worker-3 | Analyze all 11 site builder skills, define expected outputs for Figma-to-Template stage, identify measurable quality dimensions | `worker-3/output.md` |
| 1.4 | Model Capability Mapping | PENDING | worker-4 | Map DeepSeek R1/V3, Kimi K2.5 capabilities to site builder skill requirements, identify strengths/weaknesses, region availability | `worker-4/output.md` |

---

## Detailed Task Specifications

### 1.1 Bedrock Evaluations Deep Dive

**Goal**: Produce a reference document for Bedrock Evaluations integration.

**Research Areas**:
- `CreateEvaluationJob` API: all parameters, constraints, error handling
- JSONL dataset format: schema, max prompts (1000), validation rules
- BYOI (Bring Your Own Inference) pattern: pre-generate responses, feed to judge
- LLM-as-Judge: supported judge models (Claude 3.5/3.7 Sonnet, Nova Pro, Llama 3.1 70B, Mistral Large)
- Custom evaluation metrics: `AutomatedEvaluationCustomMetricConfig` for domain-specific scoring
- CLI commands: `create-evaluation-job`, `get-evaluation-job`, `list-evaluation-jobs`, `stop-evaluation-job`
- IAM requirements: service role ARN, S3 permissions, Bedrock invoke permissions
- Cost model: per-prompt pricing for judge + generator invocations
- Limitations: 1000 prompts/job, region constraints, supported model list

**Output**: Structured reference doc with code examples for Python SDK and CLI.

### 1.2 Agent Eval Frameworks Survey

**Goal**: Identify patterns and tools from the broader agent evaluation ecosystem that can inform our eval pack design.

**Frameworks to Investigate**:
- **Inspect AI** (UK AISI): Task-based eval framework, scoring, solvers
- **promptfoo**: CLI-based prompt testing, YAML config, assertion-based scoring
- **Braintrust**: Logging, scoring, experiments, dataset management
- **AgentBench**: Multi-turn agent evaluation across environments
- **SWE-bench**: Code-generation evaluation (relevant for HTML generation)
- **LATS**: Language Agent Tree Search evaluation
- **LangSmith**: LangChain's tracing and evaluation platform
- **Ragas**: RAG-specific evaluation (may inform retrieval quality)

**For Each Framework, Capture**:
- Architecture pattern (CLI, API, managed service)
- Dataset format
- Scoring methodology (rubric-based, assertion-based, LLM-judge)
- Refinement/iteration support
- Bedrock compatibility
- Strengths and weaknesses for our use case

**Output**: Comparison matrix + recommended patterns to adopt.

### 1.3 Skill Analysis & Golden Outputs

**Goal**: Define what "good" looks like for each skill involved in Figma-to-Template pipeline.

**Skills to Analyze (Figma-to-Template stage)**:
1. `figma_design_extraction.skill.md` - Figma REST API, design token extraction
2. `template_customization.skill.md` - Brand and content customization
3. `template_staging.skill.md` - Stage template from source to staging folder
4. `colour_management.skill.md` - Global colour theme with CSS variables
5. `global_font_management.skill.md` - Font management (heading, body, CTA)
6. `logo_replacement.skill.md` - Replace logos across template
7. `background_image_changer.skill.md` - Background image replacement
8. `layout_transformation.skill.md` - 32 modern layout patterns

**For Each Skill, Define**:
- Input specification (what the model receives)
- Expected output specification (what "correct" looks like)
- Quality dimensions (completeness, correctness, format compliance, CSS validity, accessibility)
- Edge cases and failure modes
- Measurable scoring criteria (0-5 scale with rubric descriptions)

**Output**: Skill-by-skill quality rubric + sample golden input/output pairs.

### 1.4 Model Capability Mapping

**Goal**: Understand how DeepSeek and Kimi K2.5 map to the skill requirements.

**Research Areas**:
- DeepSeek R1: Chain-of-thought reasoning, code generation quality, HTML/CSS capability
- DeepSeek V3.1/V3.2: MoE architecture, coding/instruction following, 128K context
- Kimi K2.5: Multimodal (text + image), 128K context, general capabilities
- Benchmark comparison: HumanEval, MBPP, MMLU, MT-Bench scores for code/instruction following
- Region availability matrix (confirm us-east-1 for all)
- Pricing comparison (per-token costs for eval runs)
- Inference parameters: temperature, top_p, max_tokens recommendations for each model
- Known limitations: context window handling, structured output reliability, CSS/HTML generation quality

**Output**: Model comparison matrix with recommendations for eval configuration.

---

## Acceptance Criteria

- [ ] Bedrock Evaluations reference doc covers API, JSONL format, BYOI, CLI, and IAM
- [ ] At least 5 eval frameworks surveyed with comparison matrix
- [ ] All 8 Figma-to-Template skills analyzed with quality rubrics
- [ ] Model capability mapping includes pricing, regions, and parameter recommendations
- [ ] Stage summary synthesizes findings into actionable recommendations for Stage 3

---

## Navigation

**Previous Stage**: None (first stage)
**Next Stage**: [Stage 2: HITL Research Approval](stage-2-hitl-research.md)
