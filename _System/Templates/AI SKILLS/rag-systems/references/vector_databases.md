# Vector Databases Reference

Full selection guide, configuration, and implementation patterns for every major vector store.

---

## Selection Guide

| Store | Deployment | Best For | Weakness |
|---|---|---|---|
| **pgvector** | Self-hosted / managed Postgres | Existing Postgres stacks, relational + vector in one DB, no infra overhead | Slower ANN at scale (>10M vectors) without tuning |
| **Qdrant** | Self-hosted / cloud | High throughput, rich payload filtering, Rust performance | Newer ecosystem, fewer integrations |
| **Pinecone** | Managed cloud only | Zero-ops, fast time-to-value, serverless | Vendor lock-in, cost at high volume |
| **Weaviate** | Self-hosted / cloud | Multi-modal (text + image + audio), GraphQL API, auto-vectorization | Complex setup for simple use cases |
| **Chroma** | Embedded / self-hosted | Local development, prototyping, notebooks | Not production-grade for large corpora |
| **FAISS** | Embedded (no server) | Maximum ANN performance, research, offline batch retrieval | No persistence layer, no filtering, CPU/GPU only |
| **Milvus** | Self-hosted / cloud | Enterprise scale (100M+ vectors), distributed architecture | Heavy infra requirement |

**Default recommendation**: pgvector for new projects already on PostgreSQL.
Qdrant for new projects requiring a dedicated vector store with filtering.
FAISS for offline batch retrieval or research pipelines.

---

## pgvector

### Setup and Schema

```sql
-- Enable extension (requires PostgreSQL 14+, pgvector 0.5+)
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table: chunks with metadata and embedding
-- Replace 1536 with the dimension count of your chosen embedding model.
CREATE TABLE document_chunks (
    id          BIGSERIAL PRIMARY KEY,
    doc_id      TEXT        NOT NULL,           -- source document identifier
    chunk_index INTEGER     NOT NULL,           -- position within source document
    text        TEXT        NOT NULL,           -- raw chunk text
    metadata    JSONB       DEFAULT '{}'::jsonb, -- arbitrary provenance metadata
    embedding   VECTOR(1536),                   -- matches text-embedding-3-small
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (doc_id, chunk_index)
);

-- Index: IVFFlat for cosine similarity (build after loading data)
-- lists = sqrt(row_count) is the standard starting point.
-- Requires at least (lists * 39) rows loaded before CREATE INDEX.
CREATE INDEX ON document_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Alternative: HNSW index (pgvector 0.5+) — better recall, slower build
-- m=16, ef_construction=64 are the default starting points.
CREATE INDEX ON document_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

### Index Type Selection

| Index | Recall | Build Time | Query Speed | RAM | Use When |
|---|---|---|---|---|---|
| None (exact) | 100% | N/A | Slow at scale | Low | < 100k vectors or exact recall required |
| IVFFlat | ~95% | Fast | Fast | Medium | 100k-10M vectors, balanced |
| HNSW | ~99% | Slow | Fastest | High | Query latency is critical; RAM available |

**HNSW tuning**: `m` controls the number of connections per node (higher = better recall,
more RAM); `ef_construction` controls build quality (higher = better recall, slower build).
At query time, set `SET hnsw.ef_search = 100;` to trade latency for recall.

**IVFFlat tuning**: set `SET ivfflat.probes = 10;` at query time (default: 1). Higher
probes = better recall at the cost of query latency. Target probes = lists / 10 as a
starting point.

### Distance Operators

```sql
-- Cosine distance (default for semantic similarity)
SELECT text, embedding <=> query_vec::vector AS distance
FROM document_chunks
ORDER BY distance ASC LIMIT 5;

-- L2 Euclidean distance
SELECT text, embedding <-> query_vec::vector AS distance
FROM document_chunks ORDER BY distance ASC LIMIT 5;

-- Negative inner product (for models trained with dot-product)
SELECT text, embedding <#> query_vec::vector AS distance
FROM document_chunks ORDER BY distance ASC LIMIT 5;
```

### Upsert Pattern (Idempotent)

```sql
INSERT INTO document_chunks (doc_id, chunk_index, text, metadata, embedding)
VALUES (%s, %s, %s, %s::jsonb, %s::vector)
ON CONFLICT (doc_id, chunk_index)
DO UPDATE SET
    text      = EXCLUDED.text,
    metadata  = EXCLUDED.metadata,
    embedding = EXCLUDED.embedding,
    created_at = NOW();
```

### Hybrid Filter Query (Metadata + Vector)

```sql
-- Retrieve nearest chunks within a metadata filter
-- (e.g., only chunks from a specific category)
SELECT doc_id, chunk_index, text, embedding <=> %s::vector AS distance
FROM document_chunks
WHERE metadata->>'category' = 'policy'
  AND embedding <=> %s::vector < 0.6
ORDER BY distance ASC
LIMIT %s;
```

---

## Qdrant

```python
"""qdrant_store.py — Qdrant vector store client."""

from __future__ import annotations

import logging
from uuid import uuid4

import numpy as np
from numpy.typing import NDArray
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest,
)

logger = logging.getLogger(__name__)

COLLECTION = "document_chunks"
DIMENSION = 1536  # Match your embedding model


def init_collection(client: QdrantClient, dimension: int = DIMENSION) -> None:
    """Create the collection if it does not exist.

    Args:
        client: Authenticated QdrantClient instance.
        dimension: Embedding vector dimension for your chosen model.
    """
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=dimension, distance=Distance.COSINE
            ),
        )
        logger.info("Created Qdrant collection '%s'", COLLECTION)


def upsert_chunks(
    client: QdrantClient,
    texts: list[str],
    embeddings: list[NDArray[np.float32]],
    doc_ids: list[str],
    chunk_indices: list[int],
) -> None:
    """Upsert chunks into the Qdrant collection.

    Args:
        client: Authenticated QdrantClient instance.
        texts: Raw chunk texts.
        embeddings: Corresponding embedding vectors.
        doc_ids: Source document identifiers.
        chunk_indices: Zero-based chunk positions within source documents.
    """
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=emb.tolist(),
            payload={
                "text": text,
                "doc_id": doc_id,
                "chunk_index": chunk_idx,
            },
        )
        for text, emb, doc_id, chunk_idx in zip(
            texts, embeddings, doc_ids, chunk_indices
        )
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    logger.debug("Upserted %d chunks to Qdrant", len(points))


def retrieve(
    client: QdrantClient,
    query_vector: NDArray[np.float32],
    top_k: int = 4,
    filter_doc_id: str | None = None,
) -> list[dict]:
    """Retrieve the top-k similar chunks from Qdrant.

    Args:
        client: Authenticated QdrantClient instance.
        query_vector: Embedded query as a float32 numpy array.
        top_k: Maximum number of results.
        filter_doc_id: Optional doc_id to restrict retrieval scope.

    Returns:
        List of payload dicts with 'text', 'doc_id', 'chunk_index', and 'score'.
    """
    query_filter: Filter | None = None
    if filter_doc_id:
        query_filter = Filter(
            must=[FieldCondition(key="doc_id", match=MatchValue(value=filter_doc_id))]
        )
    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_vector.tolist(),
        limit=top_k,
        query_filter=query_filter,
        with_payload=True,
    )
    return [
        {**r.payload, "score": r.score}
        for r in results
    ]
```

---

## Chroma (Local / Prototyping)

```python
"""chroma_store.py — Chroma embedded vector store for local development."""

from __future__ import annotations

import chromadb
from chromadb.config import Settings

# Persistent local storage; replace with HttpClient for a deployed instance.
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False),
)
collection = client.get_or_create_collection(
    name="document_chunks",
    metadata={"hnsw:space": "cosine"},  # cosine distance
)


def upsert(
    ids: list[str],
    embeddings: list[list[float]],
    texts: list[str],
    metadatas: list[dict],
) -> None:
    """Upsert chunks. IDs must be unique per chunk."""
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )


def query(query_embedding: list[float], n_results: int = 4) -> list[dict]:
    """Return nearest chunks. Chroma returns distances (lower = closer)."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": doc,
            "metadata": meta,
            "score": dist,
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
```

---

## FAISS (Offline / Batch Retrieval)

```python
"""faiss_store.py — In-memory FAISS index for batch or offline retrieval."""

from __future__ import annotations

import logging
from pathlib import Path

import faiss
import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


class FaissStore:
    """Flat L2 FAISS index with an external text store.

    FAISS stores only vectors; text and metadata must be managed separately,
    keyed by the integer index position.

    Args:
        dimension: Embedding vector dimension.
    """

    def __init__(self, dimension: int) -> None:
        # IndexFlatIP = inner product (use normalized vectors for cosine)
        # IndexFlatL2 = L2 Euclidean
        self._index = faiss.IndexFlatIP(dimension)
        self._texts: list[str] = []
        self._doc_ids: list[str] = []

    def add(
        self,
        embeddings: NDArray[np.float32],
        texts: list[str],
        doc_ids: list[str],
    ) -> None:
        """Add vectors. Normalize first for cosine similarity via inner product.

        Args:
            embeddings: (N, D) float32 array of embedding vectors.
            texts: Corresponding chunk texts.
            doc_ids: Corresponding source document identifiers.
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = embeddings / np.maximum(norms, 1e-10)
        self._index.add(normalized.astype(np.float32))
        self._texts.extend(texts)
        self._doc_ids.extend(doc_ids)
        logger.debug("FAISS index size: %d", self._index.ntotal)

    def search(
        self, query: NDArray[np.float32], top_k: int = 4
    ) -> list[dict]:
        """Search the index for the top-k nearest vectors.

        Args:
            query: 1-D float32 query vector.
            top_k: Number of results to return.

        Returns:
            List of dicts with 'text', 'doc_id', and 'score' (cosine similarity).
        """
        norm = np.linalg.norm(query)
        normalized = (query / max(norm, 1e-10)).reshape(1, -1).astype(np.float32)
        scores, indices = self._index.search(normalized, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(
                {
                    "text": self._texts[idx],
                    "doc_id": self._doc_ids[idx],
                    "score": float(score),
                }
            )
        return results

    def save(self, path: Path) -> None:
        """Persist the FAISS index to disk."""
        faiss.write_index(self._index, str(path))

    @classmethod
    def load(cls, path: Path, dimension: int) -> "FaissStore":
        """Load a persisted FAISS index from disk."""
        store = cls(dimension=dimension)
        store._index = faiss.read_index(str(path))
        return store
```
