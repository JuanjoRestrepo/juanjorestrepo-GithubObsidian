# Databases & Storage

## 1. Decision Matrix

| Requirement               | Relational (Postgres, MySQL)                                            | Document (MongoDB)                                                           | Key-Value (Redis, DynamoDB)                         | Wide-Column (Cassandra)                      | Graph (Neo4j)                                          |
| ------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------ |
| Complex multi-table joins | Strong                                                                  | Weak — denormalize instead                                                   | None                                                | None                                         | Strong for graph traversal                             |
| Schema flexibility        | Rigid — migrations required                                             | Flexible per-document                                                        | Flexible (opaque value)                             | Flexible per-partition                       | Flexible                                               |
| Write throughput at scale | Moderate (vertical-first)                                               | Good                                                                         | Excellent                                           | Excellent                                    | Moderate                                               |
| ACID transactions         | Native                                                                  | Document-level only                                                          | Varies by engine                                    | Tunable; eventual by default                 | Native (most engines)                                  |
| Best fit                  | Financial records, relational data, anything needing joins/transactions | Semi-structured data with a natural document shape (user profiles, catalogs) | Session state, caching, feature flags, leaderboards | High-write time-series, logs, activity feeds | Social graphs, recommendation engines, fraud detection |

**Default**: start relational unless a specific access pattern justifies a specialized store.
Premature NoSQL adoption is a common and costly architecture mistake.

---

## 2. Normal Forms

| Form | Rule                                                        | Eliminates                     |
| ---- | ----------------------------------------------------------- | ------------------------------ |
| 1NF  | Each column holds atomic values; no repeating groups        | Multi-valued columns           |
| 2NF  | 1NF + every non-key column depends on the whole primary key | Partial dependency             |
| 3NF  | 2NF + no non-key column depends on another non-key column   | Transitive dependency          |
| BCNF | Every determinant is a candidate key                        | Edge-case anomalies 3NF misses |

Design to 3NF by default. Deliberately denormalize specific hot-read paths only after profiling
shows a join is a bottleneck — denormalization is an optimization applied after measuring, not
a starting design.

---

## 3. Indexing Strategies

| Index type               | Structure                                          | Best for                                           | Trade-off                                                                            |
| ------------------------ | -------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| B-tree (default)         | Balanced tree; O(log n) lookup; range-scan capable | Equality and range queries, ORDER BY               | Slower writes as index grows; standard default                                       |
| Hash                     | Hash table; O(1) average lookup                    | Pure equality lookups                              | No range query support                                                               |
| Composite (multi-column) | B-tree over concatenated columns                   | Queries filtering multiple columns together        | Column order matters — only left-prefix of indexed columns is used                   |
| Covering index           | Includes all columns the query needs               | Read-heavy queries — engine never reads base table | Larger size; more write overhead                                                     |
| Full-text                | Inverted index over tokenized text                 | Text search                                        | Requires a dedicated engine (Postgres GIN, Elasticsearch) for good relevance ranking |

**Discipline**: index columns in `WHERE`, `JOIN ON`, and `ORDER BY`. Every index speeds reads
but slows writes. Composite index: highest-selectivity/equality-filtered column first,
range-filtered column last.

---

## 4. Sharding & Partitioning

| Strategy           | How it works                                        | Trade-off                                                                          |
| ------------------ | --------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Range-based        | Partition by value range (user IDs 1–1M on shard A) | Simple; can create hot shards if data/traffic isn't uniform                        |
| Hash-based         | `hash(key) % N`                                     | Even distribution; resharding requires moving most data                            |
| Consistent hashing | Hash space as a ring; each node owns an arc         | Minimizes data movement when adding/removing nodes — standard for dynamic clusters |
| Directory-based    | Lookup service maps keys to shards explicitly       | Maximum flexibility; directory is a critical dependency and potential bottleneck   |

**Cross-shard query problem**: joins and aggregations across shards require application-level
fan-out and merge, or a separate analytical store. Choose a shard key that aligns with the
dominant query pattern to make cross-shard queries the rare case, not the common one.

---

## 5. Replication Topologies

| Topology                        | Consistency                                           | Use case                                                            |
| ------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------- |
| Leader–follower (single-leader) | Strong on leader; eventual on followers (async)       | Most common; simple failure model                                   |
| Multi-leader                    | Requires conflict resolution (last-write-wins, CRDTs) | Multi-region active-active write availability                       |
| Leaderless / quorum (W + R > N) | Tunable per-operation                                 | High availability, partition-tolerant systems (Cassandra, DynamoDB) |

**Sync vs. async replication**: sync = no data loss on leader failure but adds write latency
and reduces availability. Async = faster writes but may lose the most recent writes on
unplanned leader failure.

---

## 6. Object Storage

For unstructured binary data (images, video, documents, backups) — S3, GCS, Azure Blob.

- Store the binary in object storage; store metadata (owner, size, content type, key/URL) in
  the primary DB. Never store large binaries in a relational DB — it bloats backups, slows
  queries, and wastes buffer pool memory.
- Use pre-signed URLs: let clients upload/download directly to/from object storage, bypassing
  the application server for the data transfer itself. Critical for keeping application-tier
  bandwidth and compute costs down at scale.

---

## 7. Engine Cheat Sheet

| Engine        | Category                       | Sweet spot                                                                                                    |
| ------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| PostgreSQL    | Relational                     | General-purpose OLTP; strong JSONB support narrows the gap with document stores; PostGIS, pgvector extensions |
| MySQL         | Relational                     | General-purpose OLTP; very wide hosting/tooling support                                                       |
| MongoDB       | Document                       | Semi-structured data, rapid schema iteration, nested JSON-shaped domain objects                               |
| Redis         | In-memory key-value            | Caching, session store, leaderboards (sorted sets), rate limiting counters, lightweight pub/sub               |
| Memcached     | In-memory key-value            | Pure caching, simpler than Redis, no persistence or advanced data structures                                  |
| Cassandra     | Wide-column                    | Extremely high write throughput, multi-region active-active, time-series/event data                           |
| DynamoDB      | Key-value / document (managed) | Serverless-friendly, predictable low latency, tight AWS integration                                           |
| Elasticsearch | Search / inverted index        | Full-text search, log aggregation, complex filtering/faceting                                                 |

---

## 8. Query Execution Path (Relational)

1. **Parse** — SQL text → AST; syntax validated.
2. **Plan/optimize** — planner evaluates strategies (which index, join order, join algorithm)
   using table statistics; picks lowest estimated-cost plan.
3. **Execute** — index scans / table scans, joins, filters, aggregations; pages read from
   buffer pool (memory) or disk on cache miss.
4. **Return** — result rows stream back to the client.

Stale table statistics (after large bulk loads without `ANALYZE`) cause the planner to pick a
bad plan even when the right index exists. Always `ANALYZE` after large data changes and use
`EXPLAIN ANALYZE` to confirm index usage before assuming an index alone fixes a slow query.
