---
name: rag-systems
description: >
  Expert-level RAG engineering skill. Activate for: RAG, retrieval augmented generation,
  embeddings, vector search, vector database, semantic search, pgvector, Pinecone, Weaviate,
  Qdrant, Chroma, FAISS, text-to-SQL for LLM, chunking, embedding models, cosine similarity,
  LangChain retrieval, LlamaIndex, RAGAS, or building a chatbot over private or enterprise
  data. Also trigger for: chat with my data, query my database with AI, knowledge base,
  add context to my LLM, ground my AI responses, prevent hallucinations with retrieval,
  hybrid search, reranking, agentic RAG, or connecting an LLM to a database.
  Covers naive, advanced, hybrid, and agentic RAG; vector DB selection; chunking; distance
  metrics; indexing pipelines; evaluation (RAGAS, recall, MRR). Grounded in Databricks, AWS,
  Google Cloud, IBM, and Azure official standards plus academic research (Lewis 2020; Gao 2024).
  Stack-agnostic Python at production standard. RPA and data engineering integration included.
  When in doubt, use this skill.
---

# RAG Systems Engineering Skill

Expert-level Retrieval Augmented Generation skill covering architecture selection, embedding
pipeline engineering, vector database integration, chunking design, hybrid retrieval, evaluation
frameworks, and production deployment. Apply at senior ML/data engineering standard on every
relevant task.

---

## RAG Taxonomy and Selection Guide

Four canonical RAG architectures exist; select based on data characteristics and query semantics.

| Architecture | Use When | Core Mechanism |
|---|---|---|
| **Naive RAG** | Static documents, simple Q&A, single retrieval step | Embed doc → store → query → retrieve → generate |
| **Advanced RAG** | Low retrieval precision, long docs, quality matters | Adds pre/post-retrieval processing: query rewriting, reranking, summarization |
| **Hybrid RAG** | Mix of structured (SQL) and unstructured (semantic) queries | Routes query to vector search, SQL, or both based on intent classification |
| **Agentic RAG** | Multi-step reasoning, tool use, dynamic data sources | LLM as orchestrator: selects retrieval tools, chains calls, reflects on results |

**Decision rule**: start with Naive RAG as a baseline and add complexity only when evaluation
metrics justify it. Hybrid RAG is the production default for enterprise systems containing both
relational and document data (the primary use case in RPA and data engineering contexts).

---

## Approach Selection: Vector Search vs. Text-to-SQL

The most consequential architectural decision in enterprise RAG is the routing split between
semantic retrieval and SQL generation. Apply this framework before any implementation decision.

| Query Characteristic | Use Vector Search | Use Text-to-SQL |
|---|---|---|
| Conceptual / semantic ("something for back pain") | Yes | No |
| Requires exact values ("products under $100") | No | Yes |
| Involves aggregation (SUM, COUNT, AVG) | No | Yes |
| Data is static or append-only documents | Yes | No |
| Data updates frequently (inventory, transactions) | No | Yes |
| Query cannot be expressed as a SQL predicate | Yes | No |

Hybrid RAG implements both and uses an intent classifier (a small prompt or fine-tuned model)
to route each query. See `references/advanced_patterns.md` for the full routing implementation.

---

## Embedding Model Selection

The embedding model is a fixed dependency: all documents and all queries must use the same
model. Switching models requires re-indexing the entire corpus. Select once, document the
choice, and record the model name and dimension count alongside the vector store schema.

| Provider | Model | Dimensions | Best For |
|---|---|---|---|
| OpenAI | `text-embedding-3-large` | 3072 | General-purpose, high quality, English-dominant |
| OpenAI | `text-embedding-3-small` | 1536 | Cost-optimized, strong general performance |
| Cohere | `embed-multilingual-v3.0` | 1024 | Multilingual corpora (50+ languages) |
| Google | `text-embedding-004` | 768 | Vertex AI / GCP-native stacks |
| Amazon | `amazon.titan-embed-text-v2:0` | 1024 | AWS Bedrock-native, variable dimensions (256/512/1024) |
| Mistral | `mistral-embed` | 1024 | Self-hostable, strong on technical/code content |
| HuggingFace | `BAAI/bge-large-en-v1.5` | 1024 | Open-source, SOTA for English retrieval |
| HuggingFace | `intfloat/multilingual-e5-large` | 1024 | Open-source multilingual baseline |

**Selection rules**: (1) If the LLM provider is OpenAI, default to `text-embedding-3-small`
unless precision benchmarks justify the cost of `large`. (2) For multilingual corpora, Cohere
`embed-multilingual-v3.0` outperforms OpenAI models. (3) For on-premise or air-gapped
environments, use `BAAI/bge-large-en-v1.5` via `sentence-transformers`. (4) Record model
name and dimension count in both the DB schema (column comment) and config — they are
non-negotiable for future compatibility.

---

## Distance Metrics

Choice of distance metric affects retrieval quality independently of the embedding model.
Most embedding models are trained with cosine similarity as the objective; use it as default.

| Metric | pgvector Op | Formula Characteristic | Use When |
|---|---|---|---|
| **Cosine similarity** | `<=>` | Angle between vectors; magnitude-invariant | Default. Semantic similarity, variable-length docs |
| **Inner product (dot product)** | `<#>` | Magnitude-sensitive cosine | Models explicitly trained with dot-product (some OpenAI models) |
| **L2 Euclidean** | `<->` | Absolute spatial distance | When magnitude carries semantic meaning |
| **L1 Manhattan** | `<+>` | Sum of absolute differences | Sparse vectors, some NLP tasks |
| **Hamming** | `<~>` | Bit-difference count | Binary embeddings only |
| **Jaccard** | `<%>` | Set intersection / union | Binary/sparse embeddings |

**Practical guidance**: cosine similarity is correct for >95% of use cases with modern
embedding models. Switch to inner product only when the model card explicitly states it.
See `references/vector_databases.md` for pgvector operator syntax and index type selection.

---

## Core Code Templates

### Embedding Pipeline

```python
"""embedding_pipeline.py — Stack-agnostic embedding generation pipeline."""

from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Protocol defining the embedding provider interface."""

    def embed(self, texts: list[str]) -> list[NDArray[np.float32]]:
        """Embed a batch of texts.

        Args:
            texts: List of raw text strings to embed.

        Returns:
            List of float32 embedding vectors, one per input text.
        """
        ...


class OpenAIEmbeddingProvider:
    """OpenAI embedding provider using the Embeddings API.

    Args:
        model: Model identifier, e.g. 'text-embedding-3-small'.
        client: Pre-initialized openai.OpenAI client instance.
        batch_size: Number of texts per API call (max 2048 for OpenAI).
    """

    def __init__(
        self,
        model: str,
        client: object,  # openai.OpenAI — avoid hard dependency at import
        batch_size: int = 512,
    ) -> None:
        self._model = model
        self._client = client
        self._batch_size = batch_size

    def embed(self, texts: list[str]) -> list[NDArray[np.float32]]:
        """Embed texts in batches.

        Args:
            texts: List of raw text strings.

        Returns:
            List of float32 embedding vectors.

        Raises:
            RuntimeError: On API failure after retry exhaustion.
        """
        vectors: list[NDArray[np.float32]] = []
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i : i + self._batch_size]
            try:
                response = self._client.embeddings.create(
                    model=self._model, input=batch
                )
                for item in response.data:
                    vectors.append(np.array(item.embedding, dtype=np.float32))
            except Exception as exc:
                logger.error("Embedding API call failed for batch %d: %s", i, exc)
                raise RuntimeError(f"Embedding failed at batch {i}") from exc
        return vectors
```

### Chunking (Fixed-Size with Overlap)

```python
"""chunker.py — Production chunking with overlap and token-awareness."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """A single text chunk with provenance metadata.

    Attributes:
        text: The chunk text content.
        doc_id: Identifier of the source document.
        chunk_index: Zero-based position within the source document.
        token_count: Estimated token count (cl100k_base approximation).
    """

    text: str
    doc_id: str
    chunk_index: int
    token_count: int = field(init=False)

    def __post_init__(self) -> None:
        # Approximate: 1 token ≈ 4 characters (cl100k_base for English)
        self.token_count = max(1, len(self.text) // 4)


class FixedSizeChunker:
    """Splits text into fixed-size overlapping chunks by character count.

    The overlap ensures that context spanning a chunk boundary is not lost.
    Both videos confirm: ~500-token chunks (≈2000 chars) with 10-20% overlap
    are the empirically validated starting point for most corpora.

    Args:
        chunk_size: Target chunk size in characters (default: 2000 ≈ 500 tokens).
        overlap: Overlap in characters between adjacent chunks (default: 200).
    """

    def __init__(self, chunk_size: int = 2000, overlap: int = 200) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk(self, text: str, doc_id: str) -> list[Chunk]:
        """Split text into overlapping chunks.

        Args:
            text: Raw document text.
            doc_id: Source document identifier for provenance tracking.

        Returns:
            Ordered list of Chunk objects.
        """
        chunks: list[Chunk] = []
        step = self._chunk_size - self._overlap
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + self._chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(text=chunk_text, doc_id=doc_id, chunk_index=idx))
                idx += 1
            start += step
        logger.debug("Chunked doc '%s' into %d chunks", doc_id, len(chunks))
        return chunks
```

### Retrieval Function (pgvector)

```python
"""retriever.py — Vector similarity retrieval against pgvector."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import psycopg2
from numpy.typing import NDArray
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """A retrieved chunk with its similarity score.

    Attributes:
        doc_id: Source document identifier.
        chunk_index: Position within source document.
        text: Chunk text content.
        score: Cosine distance (lower = more similar; 0 = identical).
    """

    doc_id: str
    chunk_index: int
    text: str
    score: float


class PgVectorRetriever:
    """Retrieves semantically similar chunks from a pgvector-backed store.

    Args:
        conn: Active psycopg2 connection.
        table: Target table name (must have 'embedding vector(N)' column).
        top_k: Maximum number of results to return.
        distance_threshold: Maximum cosine distance to include (0.0-2.0; lower = stricter).
    """

    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        table: str,
        top_k: int = 4,
        distance_threshold: float = 0.6,
    ) -> None:
        self._conn = conn
        self._table = table
        self._top_k = top_k
        self._distance_threshold = distance_threshold

    def retrieve(self, query_vector: NDArray[np.float32]) -> list[RetrievedChunk]:
        """Find the top-k chunks nearest to the query vector.

        Args:
            query_vector: Embedded query as a float32 numpy array.

        Returns:
            List of RetrievedChunk ordered by ascending cosine distance.

        Raises:
            RuntimeError: On database query failure.
        """
        vec_str = "[" + ",".join(str(float(v)) for v in query_vector) + "]"
        sql = f"""
            SELECT doc_id, chunk_index, text,
                   embedding <=> %s::vector AS distance
            FROM {self._table}
            WHERE embedding <=> %s::vector < %s
            ORDER BY distance ASC
            LIMIT %s;
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    sql,
                    (vec_str, vec_str, self._distance_threshold, self._top_k),
                )
                rows = cur.fetchall()
        except Exception as exc:
            logger.error("Retrieval query failed: %s", exc)
            raise RuntimeError("Vector retrieval failed") from exc

        return [
            RetrievedChunk(
                doc_id=row[0],
                chunk_index=row[1],
                text=row[2],
                score=float(row[3]),
            )
            for row in rows
        ]
```

---

## Indexing Pipeline Design

Every production RAG system requires an automated, incremental indexing pipeline. Batch-loading
documents once and forgetting the pipeline is a maintenance failure — new or modified documents
must be indexed without full re-indexing.

**Required components:**
- Source connector: reads raw documents from the origin (filesystem, DB, object store)
- Change detector: hash-based or timestamp-based, identifies new/modified/deleted documents
- Chunker: splits documents into retrieval units
- Embedder: calls the embedding model API in batches
- Vector writer: upserts vectors and metadata into the vector store
- Index state tracker: persists indexing status per document and model

**Design rules:**
1. Track index state per document AND per embedding model. When evaluating a new model,
   you need parallel indexes without touching the live one.
2. Use a content hash (SHA-256 of the raw text) as the change signal — timestamps are
   unreliable across systems.
3. Process in batches of 20-100 documents per invocation; never unbounded.
4. Idempotent by design: re-indexing a document that has not changed must be a no-op.
5. Emit structured logs (JSON) with doc_id, model, chunk_count, latency_ms for observability.

See `references/advanced_patterns.md` for the full indexing pipeline implementation.

---

## SQL Injection Prevention in Text-to-SQL

When the LLM generates SQL from natural language, the generated query must be validated
before execution. Never execute raw LLM output against a production database.

**Mandatory safeguards:**
- Whitelist-only validation: reject any query containing `INSERT`, `UPDATE`, `DELETE`,
  `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `GRANT`, `REVOKE`, `EXEC`, or `EXECUTE`
- Parse with `sqlparse` and verify the statement type is `SELECT` only
- Enforce row limit: append `LIMIT N` if absent
- Run under a read-only database role with no write privileges
- Log every generated query before execution

See `references/advanced_patterns.md` for the full `TextToSQLHandler` implementation.

---

## RPA and Data Engineering Integration Notes

**RPA context**: RAG is most useful in attended/unattended bots that need to answer
natural-language questions over a business knowledge base (product catalogs, policies,
SOPs) or query structured transaction data (invoices, orders, inventory). The Text-to-SQL
pattern maps directly to existing SQL query patterns in REFramework Performer bots.
Embed the retrieval call as a custom activity or `Invoke Python Method` step.

**Data engineering context**: RAG pipelines fit naturally into Medallion Architecture.
Bronze layer ingests raw documents; Silver transforms and chunks; Gold stores the vector
embeddings alongside clean structured data. The indexing pipeline is an Airflow DAG
(or dbt post-hook for column-level embedding triggers). pgvector on PostgreSQL is the
simplest integration if the warehouse is already PostgreSQL-based; for Snowflake/BigQuery,
use Cortex Search or BigQuery Vector Search respectively.

---

## Reference Files

Load the relevant reference file when the task falls into that subdomain.

| File | Load When |
|---|---|
| `references/theory_and_industry.md` | RAG theory (Lewis 2020; Gao et al. 2024 survey); taxonomy (Naive/Advanced/Modular/Self-RAG/GraphRAG); RAG vs fine-tuning decision matrix; Databricks, AWS, Google, IBM, Azure architecture standards; RAGAS evaluation standard; evidence-based chunking guidance; security considerations; emerging patterns (HyDE, contextual retrieval, multimodal RAG) |
| `references/databricks_rag_deepdive.md` | Databricks-specific: full LLM customization decision matrix (prompt engineering vs RAG vs fine-tuning vs pretraining); Databricks 3-step evaluation pipeline; LLM-as-judge best practices (Leng et al. 2023); grading rubric with validated examples (0-3 scale); Python LLM judge + MLflow logging templates; Experian Latte case study full architecture; Databricks service reference table (AI Search, Vector Search, Model Gateway, Agent Evaluation, AI Functions, DBRX) |
| `references/vector_databases.md` | Selecting or implementing a vector store; pgvector setup with HNSW/IVFFlat; FAISS, Qdrant, Pinecone, Weaviate, Chroma, Milvus configuration and code templates |
| `references/chunking_strategies.md` | Chunking design: fixed-size token-aware, sentence-aware, markdown-aware, recursive; overlap rationale; NVIDIA 2024 benchmark findings; NAACL 2025 evidence on semantic chunking |
| `references/evaluation_framework.md` | Evaluating retrieval quality: RAGAS metrics, recall/precision/MRR/NDCG, evaluation dataset design (JSONL format), automated Python harness, two-layer evaluation model (retrieval then generation), Databricks LLM-as-judge standard, continuous evaluation loop |
| `references/advanced_patterns.md` | Hybrid RAG intent routing, Text-to-SQL with SQL injection prevention, Agentic RAG, dense+sparse BM25 hybrid (RRF fusion), cross-encoder reranking, semantic caching, structured observability traces, full incremental indexing pipeline |
