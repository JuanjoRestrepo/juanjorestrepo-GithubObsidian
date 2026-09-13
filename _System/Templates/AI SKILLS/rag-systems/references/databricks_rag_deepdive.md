# Databricks RAG Deep Dive

Sources: Databricks blog (Leng, Uhlenhuth, Polyzotis 2023); Experian Latte case study;
Databricks official RAG and LLMOps documentation.
Reference code: https://github.com/databrickslabs/doc-qa

---

## 1. LLM Customization Method Decision Framework

Databricks defines four architectural patterns for customizing an LLM with organizational
data. These are **not mutually exclusive** — production systems routinely combine RAG with
fine-tuning for maximum accuracy. The decision matrix below is the authoritative Databricks
reference for this choice.

| Method | Definition | Primary Use Case | Data Requirements | Advantages | Considerations |
|---|---|---|---|---|---|
| **Prompt engineering** | Crafting specialized prompts to guide LLM behavior | Quick, on-the-fly model guidance | None | Fast, cost-effective, no training required | Less control than fine-tuning |
| **RAG** | Combining an LLM with external knowledge retrieval | Dynamic datasets and external knowledge bases | External knowledge base or database (e.g. vector DB) | Dynamically updated context, enhanced accuracy | Increases prompt length and inference computation |
| **Fine-tuning** | Adapting a pretrained LLM to specific datasets or domains | Domain or task specialization | Thousands of domain-specific or instruction examples | Granular control, high specialization | Requires labeled data, computational cost |
| **Pretraining** | Training an LLM from scratch on a domain corpus | Unique tasks or domain-specific corporation | Large datasets (billions to trillions of tokens) | Maximum control, tailored for specific needs | Extremely resource-intensive |

**Decision rule** (Databricks standard): Start with prompt engineering. Add RAG when the
model needs access to external or frequently updated knowledge. Add fine-tuning when RAG
alone cannot achieve the required accuracy or the model needs to learn a new output style
or task format. Only consider pretraining when no existing foundation model fits the domain.

**Why RAG before fine-tuning?** Fine-tuning encodes knowledge into model weights —
knowledge that becomes stale as the underlying data changes. RAG retrieves at query time,
so updates to the knowledge base are immediately reflected with no retraining cycle.
Fine-tuning is better suited to teaching behavioral patterns (tone, format, instruction
following) rather than injecting factual knowledge.

**Combining RAG + fine-tuning** (Experian Latte example): Experian fine-tuned Llama 8B
for task format and response style (how to write a customer support email), then layered
RAG via Databricks AI Search for domain knowledge retrieval (credit score policies, product
descriptions, regulatory content). The combination delivered higher NPS than either
technique alone would have achieved.

---

## 2. Databricks 3-Step Evaluation Pipeline

Source: Leng, Uhlenhuth, Polyzotis — "Best Practices for LLM Evaluation of RAG Applications"
(Databricks Blog, 2023). https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG

This is the standard evaluation pipeline for RAG chatbot quality assessment at Databricks.
It produces automated grades that align with human judgment at >80% exact agreement and
>95% within-one-score agreement.

### Architecture

```
Step 1: Generate Benchmark Dataset
    Documents + Questions
           |
           v
Step 2: Generate Answer Sheets
    For each LLM under evaluation:
    (Question + Context) --> LLM --> Answer
    Stored as: {question, context, answer} triples
           |
           v
Step 3: Generate Grades
    (Question + Context + Answer) --> LLM Judge (GPT-4 / GPT-3.5+examples)
    Output: Correctness (60%) + Comprehensiveness (20%) + Readability (20%)
           |
           v
    Grading Results with reasoning
```

### Step 1: Benchmark Dataset Construction

Construct from 100+ domain-specific question-context pairs. Each pair contains:
- `question`: a realistic user query (e.g. "How do I terminate a Databricks cluster?")
- `context`: the relevant document chunk(s) that should ground the answer

The context represents the chunks that a well-functioning retriever would surface.
Deriving questions from actual user queries is preferred over synthetic generation.

**Benchmark dataset format (JSONL):**
```json
{"question": "What is DenseVector?", "context": "DenseVector represents a dense numerical vector..."}
{"question": "How to terminate a Databricks cluster?", "context": "To terminate a cluster, navigate to the Clusters tab..."}
```

### Step 2: Answer Sheet Generation

Run each LLM candidate against the benchmark dataset. Tested models in the Databricks study:
GPT-4, GPT-3.5, Claude-v1, Llama2-70b-chat, Vicuna-33b, mpt-30b-chat.

**Answer sheet format (JSONL):**
```json
{"question": "...", "context": "...", "answer": "...", "model": "gpt-4"}
```

### Step 3: Grade Generation

Composite score: **Correctness (60%) + Comprehensiveness (20%) + Readability (20%)**.

Correctness is the dominant factor by design. Tune weights for your use case, but Databricks
research confirms Correctness should remain the heaviest-weighted dimension for document Q&A.

---

## 3. LLM-as-Judge Best Practices (Databricks Research Findings)

### Finding 1: LLM-as-judge agrees with humans at >80%

GPT-4 as judge achieves:
- Exact score agreement with human annotators: **>80%**
- Within-one-score agreement: **>95%** (using 0-3 scale)
- Comprehensiveness metric shows lower alignment — confirmed to be the most subjective
  dimension by business stakeholders

**Implication**: LLM-as-judge is a production-viable replacement for human annotation at
the scale required by RAG system iteration. Human annotation should still be used for
periodic ground-truth calibration and for cases where the LLM judge produces low-confidence
scores.

### Finding 2: GPT-3.5 with few-shot examples is 10x cheaper and 3x faster than GPT-4

Without examples, GPT-3.5 produces unusable, inconsistent grades. With one example per
score value, it produces results comparable to GPT-4 with:
- 10x cost reduction
- 3x speed improvement

**Recommended procedure** (Databricks standard):
1. Use a **1-5 grading scale** (or 0-3)
2. Use **GPT-4 zero-shot** first to understand what grading criteria the model infers
3. Calibrate examples from GPT-4's outputs
4. Switch the production judge to **GPT-3.5 with one example per score**

### Finding 3: Low-precision grading scales outperform high-precision scales

High-precision scales (0-10, 0-100) produce inconsistency because:
- Annotators (human and LLM) cannot maintain a stable standard across all integer values
- It is practically impossible to provide distinguishing rubric examples for each point
  (e.g. what separates a 5.1 from a 5.6?)

Recommended scales: **0-3** or **1-5** (Likert-compatible). Binary (0/1) is appropriate
only for simple, unambiguous dimensions like "usable / not usable".

### Finding 4: RAG benchmarks cannot be transferred across use cases

A model that ranks well on general chat benchmarks (writing, math, world knowledge) does
not necessarily perform well on document Q&A. Databricks tested Vicuna-33B: it ranked
close to GPT-3.5 on the lmsys general chat benchmark but significantly underperformed
GPT-3.5 on the Databricks document Q&A benchmark.

**Rule**: always build a use-case-specific benchmark. Never use a general benchmark
to evaluate a RAG application. The skills tested differ: document Q&A requires
reading comprehension and instruction following, not creative writing or math.

### Anti-bias Techniques (Apply to Every Evaluation Run)

| Technique | Why |
|---|---|
| Temperature 0.1 | Reproducibility across judge runs |
| Single-answer grading | Avoids positional bias (pairwise comparison introduces which-answer-comes-first bias) |
| Chain-of-thought before score | Forces the judge to reason before committing to a score; reduces snap judgments |
| Few-shot examples per score | Anchors the judge's interpretation of each point on the scale |

---

## 4. Grading Rubric (0-3 Scale, Databricks Standard)

The following is the validated grading rubric from the Databricks documentation bot study.
Apply it verbatim or adapt the examples to your domain.

### Correctness (weight: 60%)

| Score | Criterion | Example |
|---|---|---|
| 0 | Completely incorrect, off-topic, or contradicts the correct answer | Question: "How to terminate a cluster?" Answer: empty string, or "I don't know" |
| 1 | Provides some relevance, answers one aspect correctly | "Databricks cluster is a computing environment..." (defines but does not answer) |
| 2 | Mostly correct but missing or hallucinating one critical aspect | Correct navigation steps, but claims "button to terminate all clusters at once" |
| 3 | Fully correct, no major aspect missing | Complete step-by-step termination procedure with no errors |

### Comprehensiveness (weight: 20%)

| Score | Criterion | Example |
|---|---|---|
| 0 | Completely incorrect (comprehensiveness is zero when correctness is zero) | — |
| 1 | Correct but too short; a major portion of the answer is truncated or missing | First step only, then "(rest missing)" |
| 2 | Correct and covers main aspects but missing detail on one minor aspect | All steps listed but no explanation of what each step does |
| 3 | Correct and covers all main aspects of the question | Complete answer with all steps and sufficient explanation |

### Readability (weight: 20%)

| Score | Criterion | Example |
|---|---|---|
| 0 | Completely unreadable; full of symbols or repeated words, no meaning can be extracted | "You you you you will need a..." repeated ad nauseam |
| 1 | Slightly readable; irrelevant symbols or repetition present, but a meaning can be inferred | Partial repetition that degrades but does not eliminate comprehension |
| 2 | Correct and mostly readable; one obvious readability issue present | Correct answer with trailing ellipsis "Click Terminate…………………….." or one repeated phrase |
| 3 | Correct and fully reader-friendly; no obvious issues | Clean, well-structured, no redundant or missing information |

### Final Composite Score

```
final_score = 0.60 * correctness + 0.20 * comprehensiveness + 0.20 * readability
```

---

## 5. Python Implementation: Databricks-Style LLM-as-Judge

```python
"""databricks_llm_judge.py — LLM-as-judge evaluator following Databricks best practices."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Callable

logger = logging.getLogger(__name__)

# Grading function signature injected into the LLM judge prompt.
# The judge is instructed to call this function with its reasoning and scores.
_GRADING_FUNCTION_SCHEMA = {
    "name": "grading_function",
    "description": "Submit grading scores and reasoning for a question-context-answer triple.",
    "parameters": {
        "type": "object",
        "properties": {
            "correctness_reasoning": {
                "type": "string",
                "description": "One-sentence reasoning for the correctness score.",
            },
            "correctness_score": {
                "type": "integer",
                "enum": [0, 1, 2, 3],
                "description": "Correctness score (0-3).",
            },
            "comprehensiveness_reasoning": {
                "type": "string",
                "description": "One-sentence reasoning for the comprehensiveness score.",
            },
            "comprehensiveness_score": {
                "type": "integer",
                "enum": [0, 1, 2, 3],
                "description": "Comprehensiveness score (0-3).",
            },
            "readability_reasoning": {
                "type": "string",
                "description": "One-sentence reasoning for the readability score.",
            },
            "readability_score": {
                "type": "integer",
                "enum": [0, 1, 2, 3],
                "description": "Readability score (0-3).",
            },
        },
        "required": [
            "correctness_reasoning", "correctness_score",
            "comprehensiveness_reasoning", "comprehensiveness_score",
            "readability_reasoning", "readability_score",
        ],
    },
}

# Few-shot system prompt with one example per score for each dimension.
# Chain-of-thought enforced via "reasoning" fields before each score.
_JUDGE_SYSTEM_PROMPT = """
You are an impartial judge evaluating the quality of an AI assistant's answer
to a question, given a specific context. You must evaluate three dimensions:

CORRECTNESS (how accurately the answer addresses the question):
- Score 0: Completely incorrect, off-topic, or contradicts the correct answer.
  Example Q: "How to terminate a Databricks cluster?" A: "I don't know."
- Score 1: Partially correct; answers one aspect but misses the core answer.
  Example Q: Same. A: "Databricks cluster is a cloud computing environment..." (describes but does not answer)
- Score 2: Mostly correct but missing or hallucinating one critical detail.
  Example Q: Same. A: Correct navigation steps but claims a "terminate all clusters" button exists.
- Score 3: Fully correct, no major aspect missing.
  Example Q: Same. A: Complete step-by-step termination procedure, no errors.

COMPREHENSIVENESS (how fully the answer covers all aspects of the question):
- Score 0: Completely incorrect (zero comprehensiveness when correctness is zero).
- Score 1: Correct but truncated; major part of the answer is missing.
- Score 2: Correct and covers main aspects but missing detail on one minor part.
- Score 3: Correct and covers all main aspects with sufficient explanation.

READABILITY (how readable and free of redundancy/noise the answer is):
- Score 0: Completely unreadable (repeated words, symbols, no extractable meaning).
- Score 1: Slightly readable; some repetition or noise, but meaning can be inferred.
- Score 2: Mostly readable with one obvious issue (trailing symbols, one repeated phrase).
- Score 3: Clean, well-structured, fully reader-friendly.

Provide one sentence of reasoning for each dimension BEFORE giving the score.
Call the grading_function with your reasoning and scores.
""".strip()

_USER_PROMPT_TEMPLATE = """
Question: {question}

Context: {context}

Answer: {answer}
""".strip()


@dataclass
class GradeResult:
    """Result of a single LLM-as-judge evaluation.

    Attributes:
        question: Evaluated question.
        answer: Evaluated answer.
        correctness_score: Score 0-3.
        comprehensiveness_score: Score 0-3.
        readability_score: Score 0-3.
        composite_score: Weighted composite (0.6*C + 0.2*Comp + 0.2*R).
        correctness_reasoning: Judge's reasoning for correctness score.
        comprehensiveness_reasoning: Judge's reasoning for comprehensiveness score.
        readability_reasoning: Judge's reasoning for readability score.
        model_judge: LLM used as judge.
    """

    question: str
    answer: str
    correctness_score: int
    comprehensiveness_score: int
    readability_score: int
    composite_score: float
    correctness_reasoning: str
    comprehensiveness_reasoning: str
    readability_reasoning: str
    model_judge: str

    @classmethod
    def from_function_call(
        cls,
        question: str,
        answer: str,
        payload: dict,
        model_judge: str,
    ) -> "GradeResult":
        """Construct from a parsed grading_function call payload.

        Args:
            question: The evaluated question.
            answer: The evaluated answer.
            payload: Parsed dict from the LLM tool/function call.
            model_judge: Name of the LLM judge used.

        Returns:
            Populated GradeResult.
        """
        c = payload["correctness_score"]
        comp = payload["comprehensiveness_score"]
        r = payload["readability_score"]
        composite = round(0.60 * c + 0.20 * comp + 0.20 * r, 4)
        return cls(
            question=question,
            answer=answer,
            correctness_score=c,
            comprehensiveness_score=comp,
            readability_score=r,
            composite_score=composite,
            correctness_reasoning=payload["correctness_reasoning"],
            comprehensiveness_reasoning=payload["comprehensiveness_reasoning"],
            readability_reasoning=payload["readability_reasoning"],
            model_judge=model_judge,
        )


class DatabricksLLMJudge:
    """LLM-as-judge evaluator following Databricks documentation bot best practices.

    Uses function/tool calling to enforce structured output. Apply anti-bias
    techniques: temperature=0.1, single-answer grading, chain-of-thought reasoning,
    few-shot examples per score (embedded in system prompt).

    Args:
        llm_fn: Callable accepting (system_prompt, user_prompt, tools, temperature)
                and returning the raw tool call payload dict. Adapt to your LLM client.
        model_name: LLM identifier for logging (e.g. 'gpt-3.5-turbo-16k').
        temperature: Judge temperature. Default 0.1 for reproducibility.
    """

    def __init__(
        self,
        llm_fn: Callable[..., dict],
        model_name: str,
        temperature: float = 0.1,
    ) -> None:
        self._llm = llm_fn
        self._model_name = model_name
        self._temperature = temperature

    def grade(
        self, question: str, context: str, answer: str
    ) -> GradeResult | None:
        """Grade a single question-context-answer triple.

        Args:
            question: The user question.
            context: The retrieved context provided to the answering model.
            answer: The model's answer to evaluate.

        Returns:
            GradeResult with scores and reasoning, or None if the LLM call fails.
        """
        user_prompt = _USER_PROMPT_TEMPLATE.format(
            question=question, context=context, answer=answer
        )
        try:
            payload = self._llm(
                system_prompt=_JUDGE_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                tools=[_GRADING_FUNCTION_SCHEMA],
                temperature=self._temperature,
            )
            return GradeResult.from_function_call(
                question=question,
                answer=answer,
                payload=payload,
                model_judge=self._model_name,
            )
        except Exception as exc:
            logger.error("LLM judge call failed for question '%s...': %s", question[:60], exc)
            return None

    def grade_batch(
        self,
        answer_sheets: list[dict],
    ) -> list[GradeResult]:
        """Grade a batch of answer sheets.

        Args:
            answer_sheets: List of dicts, each with 'question', 'context', 'answer' keys.

        Returns:
            List of GradeResult objects (None entries filtered out).
        """
        results: list[GradeResult] = []
        for sheet in answer_sheets:
            result = self.grade(
                question=sheet["question"],
                context=sheet["context"],
                answer=sheet["answer"],
            )
            if result is not None:
                results.append(result)
        logger.info(
            "Graded %d/%d answer sheets (judge: %s)",
            len(results),
            len(answer_sheets),
            self._model_name,
        )
        return results

    def aggregate(self, results: list[GradeResult]) -> dict:
        """Compute aggregate statistics over a graded batch.

        Args:
            results: List of GradeResult objects from grade_batch.

        Returns:
            Dict with mean scores per dimension and composite, plus model name.
        """
        n = max(len(results), 1)
        return {
            "model_judge": self._model_name,
            "n": len(results),
            "mean_correctness": round(
                sum(r.correctness_score for r in results) / n, 4
            ),
            "mean_comprehensiveness": round(
                sum(r.comprehensiveness_score for r in results) / n, 4
            ),
            "mean_readability": round(
                sum(r.readability_score for r in results) / n, 4
            ),
            "mean_composite": round(
                sum(r.composite_score for r in results) / n, 4
            ),
        }
```

---

## 6. MLflow Integration for RAG Evaluation

Databricks recommends MLflow as the evaluation tracking layer for all RAG pipeline
experiments. The MLflow Evaluation API (v2.4+) provides side-by-side model comparison;
v2.6 adds built-in LLM metrics.

```python
"""mlflow_rag_eval.py — Log RAG evaluation results to MLflow."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import mlflow
import pandas as pd

logger = logging.getLogger(__name__)


def log_rag_evaluation(
    experiment_name: str,
    run_name: str,
    aggregate: dict,
    grade_results: list[dict],
    params: dict,
) -> str:
    """Log a RAG evaluation run to MLflow.

    Args:
        experiment_name: MLflow experiment name (e.g. 'rag-doc-qa-eval').
        run_name: Descriptive run name (e.g. 'gpt35-chunk500-cosine').
        aggregate: Aggregate metrics dict from DatabricksLLMJudge.aggregate().
        grade_results: List of per-question grade dicts for artifact logging.
        params: Pipeline configuration params to log (chunk_size, overlap, model, etc.).

    Returns:
        MLflow run ID.
    """
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        # Log pipeline configuration as params
        mlflow.log_params(params)

        # Log aggregate evaluation metrics
        mlflow.log_metrics(
            {
                "mean_correctness": aggregate["mean_correctness"],
                "mean_comprehensiveness": aggregate["mean_comprehensiveness"],
                "mean_readability": aggregate["mean_readability"],
                "mean_composite": aggregate["mean_composite"],
            }
        )

        # Log per-question grades as artifact
        grades_path = Path("/tmp/grade_results.jsonl")
        with grades_path.open("w") as fh:
            for grade in grade_results:
                fh.write(json.dumps(grade) + "\n")
        mlflow.log_artifact(str(grades_path), artifact_path="evaluation")

        # Log grades as a pandas DataFrame for MLflow UI table view
        df = pd.DataFrame(grade_results)
        mlflow.log_table(data=df, artifact_file="evaluation/grades_table.json")

        logger.info(
            "Logged RAG eval run '%s' (ID: %s) | composite=%.4f",
            run_name,
            run.info.run_id,
            aggregate["mean_composite"],
        )
        return run.info.run_id


# Recommended params dict structure for RAG evaluation runs:
EXAMPLE_PARAMS = {
    "embedding_model": "text-embedding-3-small",
    "chunk_tokens": 500,
    "overlap_tokens": 80,
    "distance_metric": "cosine",
    "top_k": 4,
    "distance_threshold": 0.6,
    "llm_answerer": "gpt-4",
    "llm_judge": "gpt-3.5-turbo-16k",
    "judge_temperature": 0.1,
    "grading_scale": "0-3",
    "correctness_weight": 0.60,
    "comprehensiveness_weight": 0.20,
    "readability_weight": 0.20,
}
```

---

## 7. Case Study: Experian "Latte" — RAG + Fine-Tuning in Production

Source: Databricks official customer case study (2025).

### Business Context

Experian (1.1 billion people's data, 150 million active businesses, 22,000 employees,
32 countries) built "Latte" to automate contact center email responses for credit score
inquiries. Goal: automate 35%+ of 1,000+ daily customer emails.

### Technical Architecture

```
Data Foundation (Databricks Lakehouse)
        |
        +-- Structured data (policies, product descriptions, regulatory content)
        +-- Unstructured data (support transcripts, FAQ documents)
        |   (Cleaned and made GenAI-ready via Databricks data pipelines)
        |
        v
Fine-Tuning Pipeline (LLMOps)
        |
        +-- Synthetic data generation: MPT -> DBRX (richer instruction datasets)
        +-- Base model: Llama 8B (open source, hosted in protected environment)
        +-- Fine-tuning runtime: Databricks (86 hrs -> 8 hrs; some runs < 1 hr at ~$100)
        |
        v
RAG Layer (Databricks AI Search)
        |
        +-- Vector stores built per use case (credit score, product info, regulatory)
        +-- Semantic retrieval: understands query intent regardless of phrasing
        +-- Replaced ChromaDB: faster response times + better retrieval quality
        |   Example: "freeze my credit" == "lock my report" (semantic equivalence)
        |
        v
Deployment & Governance
        |
        +-- Model Serving: flexible hosting and internal access control
        +-- AI Gateway: unified endpoint with rate limiting and cost controls
        +-- Unity Catalog + MLflow: full lineage (synthetic data -> fine-tune -> serving)
        +-- Agent Evaluation: continuous output testing against internal benchmarks
        +-- AI Functions: classify incoming questions by topic to identify automation candidates
```

### Results

| Metric | Before | After | Change |
|---|---|---|---|
| Customer NPS | Baseline | +8 points | +8% lift |
| Emails handled autonomously | 0% | 35%+ | — |
| Fine-tuning time | 86 hours | 8 hours (production runs < 1 hr) | -91% |
| Fine-tuning cost (production) | High | ~$100 per run | — |
| LLM token throughput (vs prior cloud) | 1x | 6x (early), 3x (optimized) | — |

### Key Architecture Decisions and Lessons

**Why RAG over fine-tuning alone?** Credit score policies and regulatory content change
frequently. Fine-tuning cannot accommodate real-time content updates without retraining.
RAG handles dynamic knowledge; fine-tuning handles response style and format.

**Why open-source Llama 8B over GPT-4?** Regulatory requirements (data sovereignty, PII
handling) prohibited sending customer data to an external API. Hosting open-source models
in a Databricks-managed environment maintained compliance without sacrificing quality
after fine-tuning.

**Why DBRX for synthetic data?** Transition from MPT to DBRX produced richer instruction
datasets and improved prompt handling, allowing the team to experiment more rapidly without
manual annotation. DBRX is Databricks' own open-source LLM, fully integrated into the
Mosaic AI platform.

**Human-in-the-loop launch strategy**: Latte was deployed with a human review step for
all generated emails. Automation percentage was increased as confidence in the model
accumulated (monitoring via Agent Evaluation and AI Functions classification).

**Access control at retrieval level**: AI Functions were used to classify incoming
questions by topic, enabling selective exposure of retrieval results by user role.
(Reference to the JetBlue/BlueBot pattern: different teams see different retrieval scopes.)

---

## 8. Databricks RAG Service Reference

| Service | Role in RAG Pipeline | Notes |
|---|---|---|
| **Databricks AI Search** | Vector store + semantic retrieval | Managed; replaces self-hosted ChromaDB/pgvector for Databricks-native stacks |
| **Databricks Vector Search** | Low-level vector index (Delta Lake backed) | Integrates with Unity Catalog; auto-refreshes from Delta tables |
| **MLflow LangChain / PyFunc flavors** | Package retrieval logic as versioned model artifact | Enables reproducible RAG pipeline deployment |
| **Mosaic AI Model Serving** | Serve fine-tuned or foundation LLMs | Supports Llama, Mistral, DBRX, and external models via Model Gateway |
| **Mosaic AI Model Gateway** | Unified API for OpenAI, Anthropic, open-source LLMs | Cost controls, rate limits, key management, audit logging |
| **Unity Catalog** | Governance and lineage for vectors, models, and data | Required for enterprise RAG with audit requirements |
| **MLflow Evaluation API (v2.4+)** | Side-by-side LLM output comparison | Tracks answer sheets and grades as first-class MLflow artifacts |
| **MLflow LLM Metrics (v2.6+)** | Built-in: toxicity, perplexity, answer similarity | Extend with custom LLM-as-judge metrics |
| **Agent Evaluation** | Continuous output quality testing in production | Tests against internal benchmarks; used by Experian for Latte QA |
| **AI Functions** | SQL-native LLM inference inside Delta Lake queries | Used for classification, routing, and automated labeling |
| **DBRX** | Databricks open-source LLM for synthetic data generation | Preferred for instruction dataset creation inside the Databricks environment |

---

## 9. Experiment Calibration Reference

Summary of Databricks research findings for tuning LLM-as-judge configurations:

| Parameter | Recommendation | Evidence |
|---|---|---|
| Grading scale | 0-3 or 1-5 | Balances precision with annotator/judge consistency |
| Judge LLM (production) | GPT-3.5-turbo-16k + few-shot | 10x cheaper, 3x faster than GPT-4; comparable quality with examples |
| Judge LLM (calibration) | GPT-4 zero-shot | Use to generate initial examples for each score level |
| Temperature | 0.1 | Reproducibility across repeated judge runs |
| Grading mode | Single-answer | Eliminates positional bias from pairwise comparison |
| Reasoning | Chain-of-thought before score | Reduces snap judgments; improves consistency |
| Examples | One per score per dimension | Required for GPT-3.5; not necessary for GPT-4 |
| Correctness weight | 60% | Dominant dimension; tune only if output style is equally important |
| Comprehensiveness weight | 20% | Subjective; lowest human-LLM agreement |
| Readability weight | 20% | High human-LLM agreement; good signal for output quality |
| Benchmark reuse | Never across use cases | RAG benchmarks do not transfer; build domain-specific datasets |
