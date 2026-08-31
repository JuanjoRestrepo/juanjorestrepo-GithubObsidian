# RAG Evaluation Framework Reference

RAG evaluation must cover two independent layers: retrieval quality (did the right chunks
come back?) and generation quality (did the LLM produce a correct answer from them?).
Evaluate both independently before treating the full pipeline as production-ready.

---

## Metric Reference

### Retrieval Metrics

| Metric | Formula | Interpretation |
|---|---|---|
| **Recall@k** | relevant retrieved / total relevant | Did all correct chunks appear in the top-k? |
| **Precision@k** | relevant retrieved / k | What fraction of top-k results were correct? |
| **MRR** (Mean Reciprocal Rank) | mean(1 / rank of first relevant) | How high does the first correct chunk rank? |
| **NDCG@k** | normalized discounted cumulative gain | Relevance-weighted ranking quality |
| **Hit Rate@k** | queries where ≥1 relevant in top-k / total | Binary: did retrieval find anything useful? |

### Generation Metrics (RAGAS)

| Metric | What It Measures |
|---|---|
| **Faithfulness** | Is every claim in the answer grounded in the retrieved context? |
| **Answer relevance** | Does the answer address the question asked? |
| **Context precision** | Of the retrieved chunks, what fraction are actually relevant? |
| **Context recall** | Does the retrieved context contain all information needed to answer? |

RAGAS (https://github.com/explodinggradients/ragas) provides Python implementations of
all four generation metrics using an LLM-as-judge approach. It requires no labeled dataset
for generation evaluation — only (question, retrieved_context, answer) triples.

---

## Evaluation Dataset Design

A good evaluation dataset must be built before you can iterate on the system. This is
what the BettaTech transcript describes as the "juego de pruebas" (test set). Design it
following these rules:

1. **Cover diverse query types**: factual lookup, aggregation, semantic/conceptual, multi-hop.
   For hybrid systems, include both SQL-type and semantic-type queries.
2. **Label expected retrievals**: for each query, record which doc_id(s) and chunk_index(es)
   should be in the top-k. This is the ground truth for recall and precision calculation.
3. **Label expected answers**: brief canonical answers for generation metrics.
4. **Minimum size**: 20 queries per domain before results are statistically meaningful.
   Scale to 100+ for production sign-off.
5. **Sourced from real users when possible**: if the system is deployed, collect failed
   queries or low-confidence answers as seeds for the eval set.

---

## Evaluation Harness

```python
"""rag_evaluator.py — Automated retrieval evaluation harness."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass
class EvalQuery:
    """A single evaluation query with ground truth.

    Attributes:
        query_id: Unique identifier.
        query_text: Natural language query.
        expected_doc_ids: Set of doc_ids that should appear in top-k results.
        expected_chunk_indices: Optional mapping doc_id -> expected chunk indices.
        canonical_answer: Expected answer text (for generation eval).
    """

    query_id: str
    query_text: str
    expected_doc_ids: set[str]
    expected_chunk_indices: dict[str, list[int]] = field(default_factory=dict)
    canonical_answer: str = ""


@dataclass
class EvalResult:
    """Result of a single query evaluation.

    Attributes:
        query_id: Corresponding EvalQuery identifier.
        retrieved_doc_ids: doc_ids returned by the retriever.
        hit: True if at least one expected doc_id was retrieved.
        precision_at_k: Fraction of retrieved results that were relevant.
        recall_at_k: Fraction of relevant results that were retrieved.
        reciprocal_rank: 1/rank of first relevant result (0 if not found).
    """

    query_id: str
    retrieved_doc_ids: list[str]
    hit: bool
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float


@dataclass
class EvalReport:
    """Aggregate evaluation report over a dataset.

    Attributes:
        model_name: Embedding model used.
        distance_metric: Distance metric used.
        chunk_tokens: Chunk size in tokens.
        overlap_tokens: Overlap in tokens.
        top_k: Number of results retrieved per query.
        hit_rate: Fraction of queries with at least one relevant result.
        mean_precision: Mean precision@k across all queries.
        mean_recall: Mean recall@k across all queries.
        mrr: Mean Reciprocal Rank across all queries.
        false_negative_count: Queries with zero relevant results retrieved.
        results: Per-query results.
    """

    model_name: str
    distance_metric: str
    chunk_tokens: int
    overlap_tokens: int
    top_k: int
    hit_rate: float
    mean_precision: float
    mean_recall: float
    mrr: float
    false_negative_count: int
    results: list[EvalResult]

    def log_summary(self) -> None:
        """Emit the report summary at INFO level."""
        logger.info(
            "EvalReport | model=%s metric=%s chunk=%d overlap=%d top_k=%d | "
            "hit=%.3f prec=%.3f rec=%.3f mrr=%.3f fn=%d",
            self.model_name,
            self.distance_metric,
            self.chunk_tokens,
            self.overlap_tokens,
            self.top_k,
            self.hit_rate,
            self.mean_precision,
            self.mean_recall,
            self.mrr,
            self.false_negative_count,
        )

    def to_dict(self) -> dict:
        """Serialize report to a JSON-compatible dict."""
        return {
            "model_name": self.model_name,
            "distance_metric": self.distance_metric,
            "chunk_tokens": self.chunk_tokens,
            "overlap_tokens": self.overlap_tokens,
            "top_k": self.top_k,
            "hit_rate": self.hit_rate,
            "mean_precision": self.mean_precision,
            "mean_recall": self.mean_recall,
            "mrr": self.mrr,
            "false_negative_count": self.false_negative_count,
        }


class RetrievalEvaluator:
    """Runs a labeled eval set against a retriever and computes metrics.

    Args:
        retrieve_fn: Callable that accepts a query string and returns a list
                     of dicts, each with at minimum a 'doc_id' key.
        top_k: Number of results to retrieve per query (must match retriever config).
        model_name: Embedding model identifier (for report metadata).
        distance_metric: Distance metric name (for report metadata).
        chunk_tokens: Chunk size in tokens (for report metadata).
        overlap_tokens: Overlap in tokens (for report metadata).
    """

    def __init__(
        self,
        retrieve_fn: Callable[[str], list[dict]],
        top_k: int,
        model_name: str,
        distance_metric: str,
        chunk_tokens: int,
        overlap_tokens: int,
    ) -> None:
        self._retrieve = retrieve_fn
        self._top_k = top_k
        self._model_name = model_name
        self._distance_metric = distance_metric
        self._chunk_tokens = chunk_tokens
        self._overlap_tokens = overlap_tokens

    def evaluate(self, eval_set: list[EvalQuery]) -> EvalReport:
        """Run the full eval set and return an EvalReport.

        Args:
            eval_set: List of EvalQuery objects with ground truth.

        Returns:
            EvalReport with per-query and aggregate metrics.
        """
        results: list[EvalResult] = []

        for q in eval_set:
            try:
                retrieved = self._retrieve(q.query_text)
            except Exception as exc:
                logger.error("Retrieval failed for query '%s': %s", q.query_id, exc)
                retrieved = []

            retrieved_ids = [r["doc_id"] for r in retrieved]
            relevant_retrieved = {
                r for r in retrieved_ids if r in q.expected_doc_ids
            }

            precision = len(relevant_retrieved) / max(self._top_k, 1)
            recall = len(relevant_retrieved) / max(len(q.expected_doc_ids), 1)
            hit = len(relevant_retrieved) > 0

            rr = 0.0
            for rank, doc_id in enumerate(retrieved_ids, start=1):
                if doc_id in q.expected_doc_ids:
                    rr = 1.0 / rank
                    break

            results.append(
                EvalResult(
                    query_id=q.query_id,
                    retrieved_doc_ids=retrieved_ids,
                    hit=hit,
                    precision_at_k=precision,
                    recall_at_k=recall,
                    reciprocal_rank=rr,
                )
            )

        n = max(len(results), 1)
        return EvalReport(
            model_name=self._model_name,
            distance_metric=self._distance_metric,
            chunk_tokens=self._chunk_tokens,
            overlap_tokens=self._overlap_tokens,
            top_k=self._top_k,
            hit_rate=sum(r.hit for r in results) / n,
            mean_precision=sum(r.precision_at_k for r in results) / n,
            mean_recall=sum(r.recall_at_k for r in results) / n,
            mrr=sum(r.reciprocal_rank for r in results) / n,
            false_negative_count=sum(not r.hit for r in results),
            results=results,
        )

    def save_report(self, report: EvalReport, path: Path) -> None:
        """Persist the evaluation report as JSON.

        Args:
            report: EvalReport to serialize.
            path: Output file path.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(report.to_dict(), fh, indent=2)
        logger.info("Eval report saved to %s", path)
```

---

## Continuous Evaluation Loop

The evaluation loop should be run whenever any of the following parameters change:
- Embedding model
- Chunk size or overlap
- Distance metric
- top_k
- Distance threshold

Compare reports across parameter configurations using mean_recall as the primary metric
(retrieval must find the right content before generation quality matters) and MRR as the
secondary metric (ranking quality). Only improve generation-side parameters after retrieval
recall > 0.85 on your eval set.

**Parameter sweep order** (evaluate each independently before combining):
1. Embedding model (highest impact)
2. Chunk size (second highest impact)
3. Distance metric (third)
4. top_k and distance threshold (final tuning)

---

## Evaluation Dataset JSONL Format

```json
{"query_id": "q001", "query_text": "How does RAG work?", "expected_doc_ids": ["doc_rag_intro"], "canonical_answer": "RAG retrieves relevant context from a knowledge base and passes it to an LLM to generate grounded answers."}
{"query_id": "q002", "query_text": "Which products cost under $100?", "expected_doc_ids": ["products_table"], "canonical_answer": "Product A ($45), Product B ($89)."}
```

Each line is a JSON object matching the `EvalQuery` schema. Store alongside the skill
under `eval/rag_eval_set.jsonl` and version-control it with the codebase.

---

## Two-Layer Evaluation Model

Evaluation must cover both independent layers separately. Running only generation evaluation
is the most common error in RAG system development.

```
Layer 1: Retrieval Quality
    Input:  (query, ground-truth doc_ids)
    Metrics: Hit Rate@k, Precision@k, Recall@k, MRR, NDCG@k
    Tools:   RetrievalEvaluator (this file), RAGAS context_precision / context_recall
    Target:  Recall@k > 0.85 before advancing to generation evaluation

Layer 2: Generation Quality
    Input:  (query, retrieved_context, generated_answer)
    Metrics: Correctness, Comprehensiveness, Readability (Databricks standard)
             Faithfulness, Answer relevance (RAGAS)
    Tools:   DatabricksLLMJudge, RAGAS, MLflow Evaluation API
    Target:  Mean composite score > 2.5/3.0 (Databricks scale) or > 0.8 (RAGAS normalized)
```

**Rule**: do not optimize generation quality until retrieval recall exceeds the threshold.
Poor retrieval is the root cause of most generation failures — the LLM cannot generate a
correct answer from irrelevant chunks regardless of its capability.

---

## LLM-as-Judge: Databricks Standard

Source: Leng, Uhlenhuth, Polyzotis — Databricks Blog 2023.
Full implementation: `references/databricks_rag_deepdive.md`.

The Databricks documentation bot study established the following validated findings for
production-grade LLM-as-judge evaluation of document Q&A RAG systems:

**Core composite metric:**
```
composite = 0.60 * correctness + 0.20 * comprehensiveness + 0.20 * readability
```

**Recommended procedure:**
1. Build a domain-specific benchmark of 100+ question-context pairs. Never reuse general
   benchmarks (chat, math, writing) — RAG performance does not transfer across use cases.
2. Use GPT-4 zero-shot to generate initial grades and derive rubric examples.
3. Calibrate grading examples (one per score per dimension) from GPT-4's outputs.
4. Switch the production judge to GPT-3.5-turbo-16k + few-shot examples: 10x cheaper,
   3x faster, comparable quality.
5. Always apply: temperature=0.1, single-answer grading, chain-of-thought reasoning.
6. Use 0-3 or 1-5 scale. Avoid 0-10 or 0-100 — they produce inconsistent grades.
7. Track all runs in MLflow: params (chunk_size, model, metric), metrics (composite),
   artifacts (per-question grades JSONL, grades table).

**Human-LLM judge alignment (validated on Databricks documentation bot):**
- Exact score agreement: >80% for Correctness and Readability
- Within-one-score agreement: >95%
- Comprehensiveness is the most subjective dimension; lowest alignment (~70%)
