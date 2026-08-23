# Advanced RAG Patterns Reference

Covers: Hybrid RAG (vector + SQL routing), Text-to-SQL with SQL injection prevention,
Agentic RAG, hybrid dense+sparse search, reranking, caching, model routing,
full automated indexing pipeline, and production observability.

---

## Hybrid RAG: Intent Router

The intent router is the core of a Hybrid RAG system. It classifies each incoming query
and dispatches it to the appropriate retrieval path.

```python
"""intent_router.py — LLM-based query intent classification for hybrid RAG."""

from __future__ import annotations

import logging
from enum import StrEnum

logger = logging.getLogger(__name__)

_ROUTE_PROMPT = """
You are a query routing classifier for a hybrid RAG system.
Given a user query, classify it as one of:
  - VECTOR: semantic, conceptual, or descriptive queries that cannot be answered
             by a direct SQL predicate (e.g., "something for back pain")
  - SQL: queries requiring exact values, aggregations, or relational filtering
         (e.g., "products under $100", "how many invoices are pending")
  - HYBRID: queries that need both (e.g., "affordable ergonomic chairs that are in stock")

Respond with ONLY the class name: VECTOR, SQL, or HYBRID.

Query: {query}
""".strip()


class RouteClass(StrEnum):
    """Canonical route classes for query dispatch."""

    VECTOR = "VECTOR"
    SQL = "SQL"
    HYBRID = "HYBRID"


class IntentRouter:
    """Routes queries to vector, SQL, or hybrid retrieval paths.

    Args:
        llm_fn: Callable that accepts a prompt string and returns a completion string.
                Temperature must be 0 for deterministic routing.
    """

    def __init__(self, llm_fn: object) -> None:
        self._llm = llm_fn

    def classify(self, query: str) -> RouteClass:
        """Classify a query into a retrieval route.

        Args:
            query: Raw user query string.

        Returns:
            RouteClass enum value.
        """
        prompt = _ROUTE_PROMPT.format(query=query)
        try:
            raw: str = self._llm(prompt)  # type: ignore[operator]
            label = raw.strip().upper()
            return RouteClass(label)
        except (ValueError, Exception) as exc:
            logger.warning(
                "Intent classification failed ('%s'), defaulting to VECTOR: %s",
                query,
                exc,
            )
            return RouteClass.VECTOR
```

---

## Text-to-SQL Handler

```python
"""text_to_sql.py — Validated text-to-SQL handler with injection prevention."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

import sqlparse

logger = logging.getLogger(__name__)

# Blocked DML/DDL keywords — reject any generated SQL containing these.
_BLOCKED_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|EXEC|EXECUTE)\b",
    re.IGNORECASE,
)

_SQL_GENERATE_PROMPT = """
You are a read-only SQL assistant. Generate a single SELECT query to answer the question.

Rules:
- Use ONLY the tables and columns listed in the schema below.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, EXEC.
- Include LIMIT {row_limit} unless the query already limits rows.
- Return ONLY the SQL statement, no explanation.

Schema:
{schema}

Question: {question}
""".strip()


@dataclass
class SQLResult:
    """Result of a text-to-SQL execution.

    Attributes:
        query: Generated and validated SQL string.
        rows: Fetched rows as list of dicts.
        error: Error message if execution failed; None on success.
    """

    query: str
    rows: list[dict[str, Any]]
    error: str | None = None


class TextToSQLHandler:
    """Converts natural language questions to validated SELECT SQL and executes them.

    Args:
        llm_fn: Callable that accepts a prompt and returns the SQL string.
        execute_fn: Callable that accepts a SQL string and returns list[dict].
        schema_str: Inline schema description injected into the SQL generation prompt.
        row_limit: Hard LIMIT appended to all generated queries.
    """

    def __init__(
        self,
        llm_fn: object,
        execute_fn: object,
        schema_str: str,
        row_limit: int = 50,
    ) -> None:
        self._llm = llm_fn
        self._execute = execute_fn
        self._schema = schema_str
        self._row_limit = row_limit

    def run(self, question: str) -> SQLResult:
        """Generate, validate, and execute a SQL query for the given question.

        Args:
            question: Natural language question from the user.

        Returns:
            SQLResult with the generated query, rows, and any error.
        """
        prompt = _SQL_GENERATE_PROMPT.format(
            schema=self._schema,
            question=question,
            row_limit=self._row_limit,
        )
        try:
            raw_sql: str = self._llm(prompt)  # type: ignore[operator]
            sql = self._validate(raw_sql.strip())
        except ValueError as exc:
            logger.warning("SQL validation rejected query: %s", exc)
            return SQLResult(query="", rows=[], error=str(exc))

        logger.info("Executing generated SQL: %s", sql)
        try:
            rows: list[dict] = self._execute(sql)  # type: ignore[operator]
            return SQLResult(query=sql, rows=rows)
        except Exception as exc:
            logger.error("SQL execution failed: %s", exc)
            return SQLResult(query=sql, rows=[], error=str(exc))

    def _validate(self, sql: str) -> str:
        """Validate that the generated SQL is a safe SELECT statement.

        Args:
            sql: Raw SQL string from the LLM.

        Returns:
            Validated (and LIMIT-appended) SQL string.

        Raises:
            ValueError: If the SQL fails any safety check.
        """
        # 1. Block DML/DDL keywords
        if _BLOCKED_PATTERN.search(sql):
            raise ValueError(f"Blocked keyword detected in generated SQL: {sql[:200]}")

        # 2. Confirm statement type is SELECT via sqlparse
        parsed = sqlparse.parse(sql)
        if not parsed or parsed[0].get_type() != "SELECT":
            raise ValueError(f"Generated statement is not SELECT: {sql[:200]}")

        # 3. Append LIMIT if absent
        if not re.search(r"\bLIMIT\b", sql, re.IGNORECASE):
            sql = sql.rstrip(";") + f" LIMIT {self._row_limit};"

        return sql
```

---

## Automated Indexing Pipeline

```python
"""indexing_pipeline.py — Incremental, idempotent RAG indexing pipeline."""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)


@dataclass
class IndexState:
    """Persisted indexing state for a single document.

    Attributes:
        doc_id: Document identifier.
        source_hash: SHA-256 of source text at last successful index.
        indexed: True if currently indexed and up-to-date.
        model_name: Embedding model used at last index.
        chunk_count: Number of chunks produced at last index.
    """

    doc_id: str
    source_hash: str
    indexed: bool
    model_name: str
    chunk_count: int


class IndexStateStore:
    """Persists indexing state as a JSONL file (replace with DB in production).

    Args:
        path: Path to the state file.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._state: dict[str, IndexState] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            with self._path.open() as fh:
                for line in fh:
                    rec = json.loads(line)
                    self._state[rec["doc_id"]] = IndexState(**rec)

    def get(self, doc_id: str) -> IndexState | None:
        return self._state.get(doc_id)

    def save(self, state: IndexState) -> None:
        self._state[state.doc_id] = state
        with self._path.open("w") as fh:
            for s in self._state.values():
                fh.write(json.dumps(s.__dict__) + "\n")

    def needs_indexing(self, doc_id: str, text: str, model_name: str) -> bool:
        """Return True if the document is new, modified, or used a different model."""
        current_hash = hashlib.sha256(text.encode()).hexdigest()
        state = self.get(doc_id)
        if state is None:
            return True
        return (
            state.source_hash != current_hash
            or state.model_name != model_name
            or not state.indexed
        )


def iter_documents(source_dir: Path) -> Iterator[tuple[str, str]]:
    """Yield (doc_id, text) pairs from a directory of .txt files.

    Args:
        source_dir: Directory containing .txt documents.

    Yields:
        Tuples of (doc_id, text content).
    """
    for path in sorted(source_dir.glob("*.txt")):
        doc_id = path.stem
        text = path.read_text(encoding="utf-8")
        yield doc_id, text


class IndexingPipeline:
    """Incremental indexing pipeline: detect changes -> chunk -> embed -> upsert.

    Args:
        chunker: Object with a chunk(text, doc_id) method returning list of Chunk.
        embedder: Object with an embed(texts) method returning list of vectors.
        vector_writer: Callable accepting (chunks, vectors) to upsert into the store.
        state_store: IndexStateStore for change detection and state tracking.
        model_name: Embedding model identifier for state tracking.
        batch_size: Number of documents processed per pipeline invocation.
    """

    def __init__(
        self,
        chunker: object,
        embedder: object,
        vector_writer: object,
        state_store: IndexStateStore,
        model_name: str,
        batch_size: int = 20,
    ) -> None:
        self._chunker = chunker
        self._embedder = embedder
        self._writer = vector_writer
        self._states = state_store
        self._model_name = model_name
        self._batch_size = batch_size

    def run(self, documents: list[tuple[str, str]]) -> dict[str, int]:
        """Process a batch of documents, skipping those already indexed.

        Args:
            documents: List of (doc_id, text) tuples.

        Returns:
            Dict with 'indexed' and 'skipped' counts.
        """
        indexed = skipped = 0

        for doc_id, text in documents[: self._batch_size]:
            if not self._states.needs_indexing(doc_id, text, self._model_name):
                logger.debug("Skipping unchanged doc '%s'", doc_id)
                skipped += 1
                continue

            try:
                chunks = self._chunker.chunk(text, doc_id)  # type: ignore[union-attr]
                texts = [c.text for c in chunks]
                vectors = self._embedder.embed(texts)  # type: ignore[union-attr]
                self._writer(chunks, vectors)  # type: ignore[operator]

                content_hash = hashlib.sha256(text.encode()).hexdigest()
                self._states.save(
                    IndexState(
                        doc_id=doc_id,
                        source_hash=content_hash,
                        indexed=True,
                        model_name=self._model_name,
                        chunk_count=len(chunks),
                    )
                )
                logger.info(
                    "Indexed doc '%s': %d chunks | model=%s",
                    doc_id,
                    len(chunks),
                    self._model_name,
                )
                indexed += 1

            except Exception as exc:
                logger.error("Failed to index doc '%s': %s", doc_id, exc)
                self._states.save(
                    IndexState(
                        doc_id=doc_id,
                        source_hash="",
                        indexed=False,
                        model_name=self._model_name,
                        chunk_count=0,
                    )
                )

        return {"indexed": indexed, "skipped": skipped}
```

---

## Hybrid Dense + Sparse Search (BM25 + Vector)

Combining BM25 (keyword/lexical matching) with vector similarity handles both exact term
matches and semantic matches. Dense-only retrieval misses queries with rare or domain-specific
terms (serial numbers, product codes, acronyms). Sparse-only misses semantic matches.

```python
"""hybrid_retriever.py — BM25 + vector fusion retrieval using RRF."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


def reciprocal_rank_fusion(
    dense_results: list[dict],
    sparse_results: list[dict],
    k: int = 60,
) -> list[dict]:
    """Fuse dense and sparse ranked lists using Reciprocal Rank Fusion.

    RRF score = 1 / (k + rank). Lower rank = higher score. Results are
    merged and re-ranked by combined score. k=60 is the standard default
    from Cormack et al. (2009).

    Args:
        dense_results: Ordered list of dicts from vector retrieval (rank 0 = best).
        sparse_results: Ordered list of dicts from BM25 retrieval (rank 0 = best).
        k: RRF smoothing constant (default: 60).

    Returns:
        Merged and re-ranked list of result dicts with 'rrf_score' key added.
    """
    scores: dict[str, float] = {}
    payloads: dict[str, dict] = {}

    for rank, result in enumerate(dense_results):
        doc_key = f"{result['doc_id']}:{result.get('chunk_index', 0)}"
        scores[doc_key] = scores.get(doc_key, 0.0) + 1.0 / (k + rank + 1)
        payloads[doc_key] = result

    for rank, result in enumerate(sparse_results):
        doc_key = f"{result['doc_id']}:{result.get('chunk_index', 0)}"
        scores[doc_key] = scores.get(doc_key, 0.0) + 1.0 / (k + rank + 1)
        payloads.setdefault(doc_key, result)

    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [
        {**payloads[key], "rrf_score": score}
        for key, score in fused
    ]
```

---

## Reranking

Reranking improves precision by applying a cross-encoder model to the top-k candidate
chunks returned by the first-stage retriever. Cross-encoders are more accurate than
bi-encoders but too slow for first-stage retrieval over large corpora.

```python
"""reranker.py — Cross-encoder reranking of first-stage retrieval results."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """Reranks candidate chunks using a cross-encoder model.

    Args:
        model: A sentence_transformers.CrossEncoder instance.
        top_n: Number of final results after reranking.
    """

    def __init__(self, model: object, top_n: int = 3) -> None:
        self._model = model
        self._top_n = top_n

    def rerank(
        self, query: str, candidates: list[dict]
    ) -> list[dict]:
        """Score and rerank candidates with the cross-encoder.

        Args:
            query: Original user query.
            candidates: First-stage retrieval results (list of dicts with 'text').

        Returns:
            Top-n candidates re-sorted by cross-encoder score (descending).
        """
        pairs = [(query, c["text"]) for c in candidates]
        scores = self._model.predict(pairs)  # type: ignore[union-attr]
        ranked = sorted(
            zip(candidates, scores), key=lambda x: x[1], reverse=True
        )
        return [
            {**candidate, "rerank_score": float(score)}
            for candidate, score in ranked[: self._top_n]
        ]
```

**Recommended cross-encoder models:**
- `cross-encoder/ms-marco-MiniLM-L-6-v2` — fast, English, strong for general Q&A
- `cross-encoder/ms-marco-MiniLM-L-12-v2` — higher accuracy, English
- `BAAI/bge-reranker-large` — open-source, strong multilingual performance

---

## Response Caching

Cache LLM responses for repeated or near-duplicate queries to reduce latency and token cost.
Use semantic caching (embed the query and check similarity against a cache index) rather
than exact-string caching.

```python
"""semantic_cache.py — Embedding-based semantic cache for LLM responses."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A cached query-response pair.

    Attributes:
        query_embedding: Embedding of the original query.
        response: Cached LLM response text.
    """

    query_embedding: NDArray[np.float32]
    response: str


class SemanticCache:
    """In-memory semantic cache using cosine similarity for cache lookup.

    Args:
        similarity_threshold: Minimum cosine similarity to consider a cache hit.
                              Tuned experimentally; 0.97 is a conservative default.
        max_size: Maximum number of entries before FIFO eviction.
    """

    def __init__(
        self, similarity_threshold: float = 0.97, max_size: int = 500
    ) -> None:
        self._threshold = similarity_threshold
        self._max_size = max_size
        self._entries: list[CacheEntry] = []

    def get(self, query_embedding: NDArray[np.float32]) -> str | None:
        """Return a cached response if a sufficiently similar query exists.

        Args:
            query_embedding: Embedding of the incoming query.

        Returns:
            Cached response string, or None on cache miss.
        """
        best_score = 0.0
        best_response: str | None = None
        q_norm = query_embedding / max(np.linalg.norm(query_embedding), 1e-10)

        for entry in self._entries:
            e_norm = entry.query_embedding / max(
                np.linalg.norm(entry.query_embedding), 1e-10
            )
            score = float(np.dot(q_norm, e_norm))
            if score > best_score:
                best_score = score
                best_response = entry.response

        if best_score >= self._threshold:
            logger.debug("Cache hit: similarity=%.4f", best_score)
            return best_response
        return None

    def set(
        self, query_embedding: NDArray[np.float32], response: str
    ) -> None:
        """Store a query-response pair in the cache.

        Args:
            query_embedding: Embedding of the query.
            response: LLM response to cache.
        """
        if len(self._entries) >= self._max_size:
            self._entries.pop(0)  # FIFO eviction
        self._entries.append(CacheEntry(query_embedding=query_embedding, response=response))
```

---

## Production Observability

Every RAG pipeline invocation must emit structured logs covering all stages. Use structured
JSON logging and attach these fields to every log record.

```python
"""observability.py — Structured logging schema for RAG pipeline traces."""

from __future__ import annotations

import json
import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from typing import Generator


@dataclass
class RAGTrace:
    """Structured trace for a single RAG pipeline invocation.

    Attributes:
        query_id: Unique identifier for this request.
        query_text: Raw user query.
        route: Intent route (VECTOR, SQL, HYBRID).
        retrieved_doc_ids: List of retrieved document identifiers.
        retrieved_scores: Similarity scores for retrieved chunks.
        cache_hit: True if response was served from cache.
        embedding_latency_ms: Time to embed the query in milliseconds.
        retrieval_latency_ms: Time for vector/SQL retrieval in milliseconds.
        generation_latency_ms: Time for LLM generation in milliseconds.
        total_latency_ms: End-to-end latency in milliseconds.
        error: Error message if any stage failed; None on success.
    """

    query_id: str
    query_text: str
    route: str = ""
    retrieved_doc_ids: list[str] = field(default_factory=list)
    retrieved_scores: list[float] = field(default_factory=list)
    cache_hit: bool = False
    embedding_latency_ms: float = 0.0
    retrieval_latency_ms: float = 0.0
    generation_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    error: str | None = None

    def emit(self, logger: logging.Logger) -> None:
        """Emit the trace as a structured JSON log record at INFO level."""
        logger.info(json.dumps(asdict(self)))


@contextmanager
def timed(trace: RAGTrace, field_name: str) -> Generator[None, None, None]:
    """Context manager that measures elapsed time and stores it in a trace field.

    Args:
        trace: RAGTrace to update.
        field_name: Attribute name to set (must be a float field ending in _ms).

    Yields:
        None.
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        setattr(trace, field_name, elapsed_ms)
```