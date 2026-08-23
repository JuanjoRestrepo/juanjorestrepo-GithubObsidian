# Chunking Strategies Reference

Chunking is the single highest-leverage parameter in RAG quality. Poor chunking degrades
retrieval before the vector search or LLM ever runs. Select strategy based on document
structure and the granularity at which meaning is distributed.

---

## Strategy Selection Guide

| Strategy | Use When | Typical Chunk Size |
|---|---|---|
| **Fixed-size with overlap** | Unstructured text, PDFs with no heading hierarchy, bulk ingestion | 400-600 tokens, 10-20% overlap |
| **Sentence-aware** | Prose where sentence boundaries carry meaning (articles, policies, SOPs) | 3-8 sentences per chunk |
| **Markdown/structure-aware** | Documentation, wikis, READMEs with heading hierarchy | Section per heading |
| **Recursive** | Mixed documents; fallback for any of the above that exceeds size limits | Hierarchical split: paragraph → sentence → word |
| **Semantic** | High-quality corpora where topic shifts are important to preserve | Embedding-based boundary detection |
| **Document-level** | Short documents (< 512 tokens) where splitting loses context | Entire document = one chunk |

**Overlap rationale**: overlap ensures that context spanning a chunk boundary is captured.
If a key sentence sits at the end of chunk N, the overlap reproduces it at the start of
chunk N+1. Set overlap to 10-20% of chunk_size. As the BettaTech transcript confirms,
overlapping chunks allow a query to match chunk 2 while returning chunk 1-linked content,
preserving the full document context.

**Token counting**: use `tiktoken` (cl100k_base for OpenAI models) for exact token counts.
Approximation rule: 1 token ≈ 4 characters for English prose.

---

## Chunk Size Selection

| Embedding Model | Max Input Tokens | Recommended Chunk Size |
|---|---|---|
| `text-embedding-3-small` | 8192 | 400-600 tokens |
| `text-embedding-3-large` | 8192 | 400-600 tokens |
| `BAAI/bge-large-en-v1.5` | 512 | 256-400 tokens |
| `amazon.titan-embed-text-v2:0` | 8192 | 400-600 tokens |
| `intfloat/multilingual-e5-large` | 512 | 256-400 tokens |

Smaller chunks yield higher retrieval precision (less noise per chunk) but require more
top-k results to assemble a complete answer. Larger chunks yield better context per
result but lower precision. Start at 500 tokens; tune based on evaluation recall metrics.

---

## Implementations

### Fixed-Size with Overlap (Token-Aware)

```python
"""chunker_fixed.py — Token-aware fixed-size chunking with overlap."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import tiktoken

logger = logging.getLogger(__name__)

ENCODING = tiktoken.get_encoding("cl100k_base")


@dataclass
class Chunk:
    """Text chunk with source provenance.

    Attributes:
        text: Raw chunk text.
        doc_id: Source document identifier.
        chunk_index: Zero-based position within the source document.
        token_count: Exact token count via cl100k_base encoding.
    """

    text: str
    doc_id: str
    chunk_index: int
    token_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.token_count = len(ENCODING.encode(self.text))


class TokenAwareChunker:
    """Splits text into token-bounded chunks with configurable overlap.

    Args:
        chunk_tokens: Target chunk size in tokens.
        overlap_tokens: Overlap in tokens between adjacent chunks.
    """

    def __init__(
        self, chunk_tokens: int = 500, overlap_tokens: int = 80
    ) -> None:
        if overlap_tokens >= chunk_tokens:
            raise ValueError("overlap_tokens must be less than chunk_tokens")
        self._chunk_tokens = chunk_tokens
        self._overlap_tokens = overlap_tokens

    def chunk(self, text: str, doc_id: str) -> list[Chunk]:
        """Tokenize and split text into overlapping token-bounded chunks.

        Args:
            text: Raw document text.
            doc_id: Source document identifier.

        Returns:
            Ordered list of Chunk objects with exact token counts.
        """
        tokens = ENCODING.encode(text)
        step = self._chunk_tokens - self._overlap_tokens
        chunks: list[Chunk] = []
        idx = 0
        start = 0

        while start < len(tokens):
            end = min(start + self._chunk_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = ENCODING.decode(chunk_tokens).strip()
            if chunk_text:
                chunks.append(Chunk(text=chunk_text, doc_id=doc_id, chunk_index=idx))
                idx += 1
            start += step

        logger.debug(
            "TokenAwareChunker: doc='%s' -> %d chunks (avg %.0f tokens)",
            doc_id,
            len(chunks),
            sum(c.token_count for c in chunks) / max(1, len(chunks)),
        )
        return chunks
```

### Markdown/Structure-Aware Chunking

```python
"""chunker_markdown.py — Heading-aware chunking for structured documents."""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)


@dataclass
class Chunk:
    """Structured chunk with heading context.

    Attributes:
        text: Chunk text including its heading.
        doc_id: Source document identifier.
        chunk_index: Zero-based position within source.
        heading: The section heading that introduces this chunk.
        level: Heading level (1, 2, or 3).
    """

    text: str
    doc_id: str
    chunk_index: int
    heading: str
    level: int


class MarkdownChunker:
    """Splits markdown documents at heading boundaries.

    Each chunk contains the heading and all content until the next heading
    of equal or higher level. Chunks exceeding max_tokens are further split
    by paragraph to stay within the embedding model's input window.

    Args:
        max_tokens: Maximum token count per chunk before paragraph-level split.
    """

    def __init__(self, max_tokens: int = 600) -> None:
        self._max_tokens = max_tokens

    def chunk(self, text: str, doc_id: str) -> list[Chunk]:
        """Split a markdown document by heading structure.

        Args:
            text: Raw markdown text.
            doc_id: Source document identifier.

        Returns:
            Ordered list of Chunk objects with heading metadata.
        """
        sections = _HEADING_RE.split(text)
        chunks: list[Chunk] = []
        idx = 0

        # split() on a multi-group pattern returns: [pre, lvl, heading, body, ...]
        # Walk in triplets after the preamble.
        pre = sections[0].strip()
        if pre:
            chunks.append(
                Chunk(
                    text=pre,
                    doc_id=doc_id,
                    chunk_index=idx,
                    heading="(preamble)",
                    level=0,
                )
            )
            idx += 1

        i = 1
        while i + 2 < len(sections):
            hashes, heading, body = sections[i], sections[i + 1], sections[i + 2]
            level = len(hashes)
            content = f"{'#' * level} {heading}\n\n{body.strip()}"
            # Approximate token count; sub-split on paragraphs if oversized.
            approx_tokens = len(content) // 4
            if approx_tokens > self._max_tokens:
                for para in body.strip().split("\n\n"):
                    if para.strip():
                        para_text = f"{'#' * level} {heading}\n\n{para.strip()}"
                        chunks.append(
                            Chunk(
                                text=para_text,
                                doc_id=doc_id,
                                chunk_index=idx,
                                heading=heading,
                                level=level,
                            )
                        )
                        idx += 1
            else:
                chunks.append(
                    Chunk(
                        text=content,
                        doc_id=doc_id,
                        chunk_index=idx,
                        heading=heading,
                        level=level,
                    )
                )
                idx += 1
            i += 3

        logger.debug(
            "MarkdownChunker: doc='%s' -> %d chunks", doc_id, len(chunks)
        )
        return chunks
```

### Recursive Chunker (Fallback / Mixed Docs)

```python
"""chunker_recursive.py — Recursive splitting: paragraph -> sentence -> word."""

from __future__ import annotations

import re
import logging

logger = logging.getLogger(__name__)

_PARAGRAPH_SEP = re.compile(r"\n{2,}")
_SENTENCE_SEP = re.compile(r"(?<=[.!?])\s+")


def recursive_chunk(
    text: str,
    doc_id: str,
    max_tokens: int = 500,
    overlap_chars: int = 200,
) -> list[dict]:
    """Split text recursively: paragraph -> sentence -> word boundary.

    Falls back to finer granularity only when a segment exceeds max_tokens.
    Overlap is applied at the character level between segments.

    Args:
        text: Raw document text.
        doc_id: Source document identifier.
        max_tokens: Maximum tokens per chunk (approximated at 4 chars/token).
        overlap_chars: Character overlap between adjacent chunks.

    Returns:
        List of dicts with 'text', 'doc_id', 'chunk_index' keys.
    """
    max_chars = max_tokens * 4
    chunks: list[str] = []

    def _split(segment: str, separators: list[str]) -> None:
        if len(segment) <= max_chars:
            chunks.append(segment.strip())
            return
        sep = separators[0]
        remaining_seps = separators[1:]
        parts = re.split(sep, segment)
        current = ""
        for part in parts:
            if len(current) + len(part) + 1 <= max_chars:
                current = (current + " " + part).strip()
            else:
                if current:
                    if remaining_seps:
                        _split(current, remaining_seps)
                    else:
                        chunks.append(current.strip())
                current = part.strip()
        if current:
            chunks.append(current.strip())

    seps = [_PARAGRAPH_SEP.pattern, _SENTENCE_SEP.pattern, r"\s+"]
    _split(text, seps)

    # Apply overlap by prepending the tail of the previous chunk
    result: list[dict] = []
    for i, chunk_text in enumerate(chunks):
        if i > 0 and overlap_chars > 0:
            prev_tail = chunks[i - 1][-overlap_chars:]
            chunk_text = prev_tail + " " + chunk_text
        result.append({"text": chunk_text.strip(), "doc_id": doc_id, "chunk_index": i})

    logger.debug(
        "RecursiveChunker: doc='%s' -> %d chunks", doc_id, len(result)
    )
    return result
```

---

## Chunking Parameters Reference

| Parameter | Conservative (precision) | Balanced (default) | Aggressive (recall) |
|---|---|---|---|
| chunk_tokens | 256 | 500 | 800 |
| overlap_tokens | 40 | 80 | 150 |
| Typical top_k | 6-8 | 3-5 | 2-3 |
| Context length passed to LLM | Moderate | Moderate | Large |

Start at balanced defaults. Run the evaluation harness (see `evaluation_framework.md`)
to measure recall before adjusting. Increasing top_k compensates for smaller chunks
but increases LLM context token cost.