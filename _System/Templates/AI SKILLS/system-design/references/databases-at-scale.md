# Database Design at Scale

**Sources:** Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017) —
the primary reference throughout this file (Ch. 5 Replication, Ch. 6 Partitioning, Ch. 9
Consistency and Consensus); Eric Brewer, "Towards Robust Distributed Systems" (PODC Keynote,
2000) — CAP theorem origin; Seth Gilbert and Nancy Lynch, "Brewer's Conjecture and the
Feasibility of Consistent, Available, Partition-Tolerant Web Services" (ACM SIGACT News,
2002) — formal proof of CAP; Daniel Abadi, "Consistency Tradeoffs in Modern Distributed
Database System Design" (IEEE Computer, 2012) — PACELC theorem; Karger et al., "Consistent
Hashing and Random Trees" (ACM STOC, 1997) — consistent hashing origin.

---

## 1. Start Here — The Right Default

**PostgreSQL on a single machine handles tens of thousands of read/write requests per second
with proper indexing.** The scaling techniques in this file have significant operational cost.
Apply them in order:

```
1. Add proper indexes → often 10–100× query speedup, zero architecture change
2. Optimize expensive queries → EXPLAIN ANALYZE, slow query log
3. Add connection pooling (PgBouncer) → handle many more concurrent connections
4. Add read replicas → scale read throughput horizontally
5. Introduce application caching (Redis) → reduce DB load for repeated reads
6. Consider vertical scaling → before introducing distributed complexity
7. Only then: sharding → when write throughput or data volume genuinely exceeds single-primary ceiling
```

Most applications never need step 7. The ones that do — Stripe, GitHub, Shopify — spent
years at each previous step first.

---

## 2. CAP Theorem

Brewer (2000), formally proved by Gilbert and Lynch (2002): in the presence of a **network
partition** (communication failure between nodes), a distributed system must choose between:

**C — Consistency:** every read receives the most recent write (or an error).
**A — Availability:** every request receives a non-error response (not necessarily the most recent write).
**P — Partition Tolerance:** the system continues to operate despite arbitrary message loss or failure between nodes.

**Partition tolerance is not optional.** Networks fail — dropped packets, routing issues,
data center splits happen in any real distributed system. Therefore, the practical choice is
**CP vs AP**, not CA vs CP vs AP.

```
CP (Consistency + Partition Tolerance):
  Under partition: return an error rather than stale data.
  Examples: HBase, Zookeeper, etcd, Mongo (w: majority)
  Use when: financial transactions, inventory systems, anything where stale data is wrong.

AP (Availability + Partition Tolerance):
  Under partition: return stale data rather than an error.
  Examples: Cassandra, DynamoDB (default), CouchDB, DNS
  Use when: user profiles, social feeds, shopping carts — brief staleness is acceptable.
```

**What CAP does NOT cover:** normal operation (no partition). For that, see PACELC.

### Common Database Placements

| Database | CAP classification | Notes |
|---|---|---|
| PostgreSQL (single) | CA — partition is impossible (one node) | N/A — no partition |
| PostgreSQL (leader-follower) | CP | Async replica is AP until caught up |
| MongoDB (w: majority) | CP | Majority write waits for confirmation |
| Cassandra | AP | Tunable via consistency level; default is AP |
| DynamoDB | AP (default), CP (strong reads) | Strongly consistent reads opt-in |
| Zookeeper / etcd | CP | Won't serve reads during leader election |
| Redis Sentinel/Cluster | AP | Favors availability; brief inconsistency during failover |

---

## 3. PACELC Theorem

Abadi (2012) extends CAP to cover normal (non-partition) operation: **even when there is no
partition, there is a trade-off between Latency and Consistency.**

```
PACELC:
  PAC: During a Partition, choose between Availability and Consistency (= CAP)
  ELC: Else (no partition), choose between Latency and Consistency
```

| Database | PAC | ELC |
|---|---|---|
| DynamoDB | PA (Available) | EL (Low Latency) |
| Cassandra | PA | EL |
| MongoDB (strong) | PC (Consistent) | EC (Consistent) |
| CRDT systems | PA | EL |
| Spanner (Google) | PC | EC |

**Why PACELC matters in practice:** most of the time there is no partition. CAP only tells
you what happens in the exceptional case. PACELC tells you what happens every request —
the latency vs consistency trade-off is the one you tune daily, not just during failures.

---

## 4. SQL vs NoSQL — Selection Criteria

The SQL vs NoSQL choice is not about modernity or scale — it is about which data model fits
your access patterns. NoSQL sacrifices relational integrity for a specific performance or
scale property; that sacrifice is only justified when you actually need that property.

| Criterion | SQL (PostgreSQL, MySQL) | NoSQL (varies by type) |
|---|---|---|
| **Data model** | Relational — joins, foreign keys, ACID transactions | Document, wide-column, key-value, graph |
| **Schema** | Enforced schema — consistency guaranteed | Flexible schema — useful for evolving data |
| **Joins** | Native, efficient | Absent or expensive (denormalize instead) |
| **Transactions** | Full ACID across tables | Limited (single document, or eventual consistency) |
| **Consistency** | Strong by default | Tunable; often eventual |
| **Scaling** | Vertical + read replicas (sharding is hard) | Designed for horizontal sharding |
| **Query flexibility** | Arbitrary SQL queries | Limited to indexed access patterns |
| **Use cases** | Financial systems, e-commerce, user data, most applications | Time-series, event logs, user sessions, social graphs, very-high write throughput |

### NoSQL Types and When to Choose Them

**Document (MongoDB, Firestore):**
Use when: data is naturally hierarchical (a user with their embedded addresses and preferences);
schema evolves frequently; joins are rare or non-existent.
Avoid when: data is highly relational; you need multi-document transactions.

**Key-Value (Redis, DynamoDB, Riak):**
Use when: single-key lookups at very high throughput; caching; session storage.
Avoid when: you need to query by anything other than the primary key.

**Wide-Column (Cassandra, HBase, Bigtable):**
Use when: write-heavy workloads at extreme scale (billions of writes/day); time-series data;
access patterns are known and fixed at design time.
Avoid when: query patterns are flexible or unknown; you need strong consistency.

**Graph (Neo4j, Amazon Neptune):**
Use when: the data is fundamentally graph-structured and the queries traverse relationships
(social network — "friends of friends who also like X"; fraud detection — shortest path
between two entities).
Avoid when: the graph topology is an afterthought — a relational DB with a recursive CTE
or a simple join table handles most "graph-like" problems.

**Time-Series (InfluxDB, TimescaleDB, VictoriaMetrics):**
Use when: the primary access pattern is "all values for key X between time T1 and T2";
metrics, IoT sensor data, financial tick data.
TimescaleDB is PostgreSQL with time-series optimizations — a good default that avoids
introducing another database.

---

## 5. Database Sharding (Horizontal Partitioning)

Sharding splits a dataset across multiple database nodes, each owning a subset of the data.
Each shard is an independent database — queries that span multiple shards require application-
or middleware-level aggregation because no single node has the full dataset.

**Cost of sharding:** cross-shard joins are impossible at the DB level; distributed
transactions across shards require the Saga pattern or 2PC; operational complexity multiplies;
schema migrations must be applied to every shard; re-sharding requires data migration.
**Do not shard unless you have measured that a single primary cannot keep up.**

### Sharding Strategies

**Range-based sharding:**
```
Shard 1: user_id 1 – 1,000,000
Shard 2: user_id 1,000,001 – 2,000,000
Shard 3: user_id 2,000,001 – 3,000,000

Pros: range queries (all users created in January) stay on one shard.
Cons: hotspots — if new users all get high IDs, Shard 3 gets all writes
     while Shard 1 is idle. Requires careful key design.
```

**Hash-based sharding:**
```
shard_id = hash(user_id) % number_of_shards

Pros: even distribution — no hotspots (assuming uniform hash).
Cons: range queries must scatter to all shards; adding/removing shards
     rehashes all assignments (use consistent hashing to mitigate).
```

**Directory-based sharding (lookup table):**
```
A routing service maintains a table: entity_id → shard_id.
Pros: maximum flexibility — any entity can be moved to any shard by updating the table.
Cons: the routing table is itself a single point of failure and a write bottleneck.
     Add read replicas for the directory, cache heavily.
```

---

## 6. Consistent Hashing

The fundamental problem with hash-based sharding: adding or removing a shard causes a full
rehash. If you have 3 shards and add a 4th, `hash(key) % 4 ≠ hash(key) % 3` for most keys
— nearly all data must move. In practice this means a migration event that reads/rewrites
the entire dataset.

**Consistent hashing** (Karger et al., 1997, introduced to web systems by Amazon's Dynamo
paper, 2007): maps both servers and keys to positions on a conceptual "hash ring" (modular
arithmetic, typically mod 2³²). A key is owned by the first server clockwise from it on
the ring.

```
Hash ring (0 to 2³² - 1, wraps around):

              0
           /     \
      S1         S2
      |             |
  2³² ─────────────
      |             |
      S4         S3
           \     /
           2³²/2

Key K maps to position hash(K) on the ring.
Key K is owned by the next server clockwise.
```

**Adding/removing a server:** only keys between the new server and its predecessor on the
ring need to move. On average, only K/N keys move (K = total keys, N = server count).

**Virtual nodes (vnodes):** each physical server has multiple positions (100–200) on the ring.
This smooths out uneven distribution and makes failure/addition impact even more incremental.
Used by Cassandra, Amazon Dynamo, and Redis Cluster.

Used in: Cassandra, Redis Cluster, Amazon Dynamo, Memcached (via client-side consistent
hashing), CDN routing.

---

## 7. Replication

Replication maintains copies of data on multiple nodes for fault tolerance and read scaling.

### Leader-Follower (Primary-Replica, Master-Slave)

```
         ┌──────────────┐
Writes ──▶│  Leader       │
         └──────┬───────┘
                │ replication log
       ┌────────┴──────────┐
       ▼                   ▼
┌────────────┐      ┌────────────┐
│ Follower 1  │      │ Follower 2  │
│ (read only) │      │ (read only) │
└────────────┘      └────────────┘
       ▲ Reads               ▲ Reads
```

**Synchronous vs asynchronous replication:**
- **Synchronous:** leader waits for follower to confirm write before acknowledging to client.
  Durability guarantee: no data loss on leader failure. Cost: write latency increases with
  replica distance. Postgres `synchronous_commit = on`.
- **Asynchronous:** leader acknowledges write immediately; replica catches up in background.
  Latency: minimal. Risk: brief data loss if leader fails before replica receives the write.
  Postgres `synchronous_commit = off` (the default).
- **Semi-synchronous (MySQL default):** at least one replica must confirm before commit.
  Balance between durability and latency.

**Replication lag:** asynchronous replicas always lag behind the leader by some amount
(typically milliseconds to seconds). "Read-your-writes consistency" requires reading from
the leader (or waiting for replica to catch up) after any write you depend on being visible.

### Multi-Leader Replication

Multiple nodes accept writes. Useful for: multi-datacenter deployments (leader in each
region accepts local writes); offline-capable applications (each device is a "leader").

**The write conflict problem:** if Leader A and Leader B both modify the same record
concurrently, there is a conflict. Resolution strategies:
- Last-write-wins (LWW) — risk of data loss
- Merge (CRDTs — Conflict-free Replicated Data Types) — automatic, mathematically sound
- Application-level conflict resolution — highest fidelity, highest complexity

Kleppmann dedicates significant attention to CRDTs as the technically correct solution for
multi-leader conflict resolution; they underpin collaborative editing (Google Docs) and
distributed counters.

### Leaderless Replication (Dynamo-style)

Any node accepts writes. Reads and writes are quorum-based:
```
W + R > N  →  at least one node in every R set has seen every write in every W set

W = write quorum (number of nodes that must confirm a write)
R = read quorum (number of nodes that must respond to a read)
N = number of replica nodes

Common configuration:
  N = 3, W = 2, R = 2  →  W + R = 4 > 3  →  quorum achieved
  Trade-off: 2/3 writes must succeed (tolerates 1 failure),
             2/3 reads must agree (read is compared, latest wins)
```

Used by: Amazon Dynamo (original, not DynamoDB), Cassandra, Riak.
Pros: no single point of failure, high availability, tunable consistency.
Cons: "sloppy quorum" (Dynamo) can violate the quorum guarantee during partitions;
      read repair adds background load; versioning conflicts require application handling.

---

## 8. Normal Forms — Relational Schema Design

Normal forms reduce data redundancy and enforce referential integrity. Apply sequentially;
each form builds on the previous.

**First Normal Form (1NF):**
- Every column holds only atomic (indivisible) values — no comma-separated lists, no arrays
  stored as strings
- No repeating column groups (`phone1`, `phone2`, `phone3`)
- Each row uniquely identified by a primary key

```
❌ Violation: customer(id, name, phones="555-1234,555-5678")
✅ Fix:       customer(id, name) + customer_phone(customer_id, phone)
```

**Second Normal Form (2NF):** requires 1NF
- Every non-key attribute depends on the *entire* primary key (eliminates partial dependencies)
- Violation only possible when the primary key is composite

```
❌ Violation: order_item(order_id, product_id, product_name, quantity)
             product_name depends only on product_id, not the full (order_id, product_id) key
✅ Fix:       order_item(order_id, product_id, quantity)
             product(product_id, product_name)
```

**Third Normal Form (3NF):** requires 2NF
- Every non-key attribute depends *directly* on the primary key (eliminates transitive
  dependencies: non-key → non-key → key)

```
❌ Violation: employee(id, department_id, department_name)
             department_name depends on department_id, not directly on employee id
✅ Fix:       employee(id, department_id)
             department(department_id, department_name)
```

**Boyce-Codd Normal Form (BCNF):** stronger than 3NF
- For every functional dependency `X → Y`, X must be a superkey
- Most tables in 3NF also satisfy BCNF; the edge case arises only with overlapping candidate
  keys. Satisfying BCNF eliminates all redundancy that stems from functional dependencies.

**When to intentionally denormalize:**
- After profiling confirms joins are a measured performance bottleneck — not speculation
- Read-heavy reporting schemas (star schema, OLAP fact tables) where joins across many tables
  degrade analytical query performance
- Cached/materialized views updated by a reliable event-driven invalidation pipeline
- Cassandra data models — wide-column stores require denormalization by design (no joins)

---

## 9. Indexing Strategies

An index is a separate data structure that the database maintains alongside the table to
accelerate specific query patterns. Every index speeds reads at the cost of write overhead
and storage. Index only what you query; over-indexing degrades write throughput.

**B-tree indexes (default in PostgreSQL and MySQL):**
- Balanced tree; keeps data sorted; supports equality (`=`), range (`>`, `<`, `BETWEEN`),
  `ORDER BY`, and `LIKE 'prefix%'` queries
- Standard choice for almost every indexed column
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
```

**Hash indexes:**
- Hash table structure; only supports equality (`=`) — no ranges, no sorting
- PostgreSQL supports explicit hash indexes; MySQL uses B-tree even for hash-styled lookups
- Rarely worth choosing over B-tree; faster for pure equality only on very large tables

**Composite (multi-column) indexes:**
- Covers multiple columns in a single index structure
- **Leftmost prefix rule:** an index on `(user_id, created_at)` can satisfy queries on
  `user_id` alone OR `user_id + created_at` together, but NOT `created_at` alone
- Column order matters: equality columns first, then range columns
```sql
-- Supports: WHERE user_id = ? AND created_at > ?  (both columns)
--           WHERE user_id = ?                       (leftmost prefix)
-- Does NOT: WHERE created_at > ?                   (not leftmost)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

**Covering indexes:**
- Index includes all columns a query needs, eliminating the table (heap) lookup entirely
- PostgreSQL `INCLUDE` clause adds non-key columns to the index leaf pages without affecting
  the sort order; MySQL achieves this by adding columns to the index definition
```sql
-- Query: SELECT status, total FROM orders WHERE user_id = ?
-- Covering index — no table access required:
CREATE INDEX idx_orders_cover ON orders(user_id) INCLUDE (status, total_amount);
```

**Partial indexes:**
- Index only a subset of rows matching a `WHERE` predicate — smaller, faster, targeted
```sql
-- Index only active users — queries for inactive users skip the index entirely
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Index only unprocessed queue entries — keeps index small as processed rows accumulate
CREATE INDEX idx_pending_jobs ON jobs(created_at) WHERE status = 'pending';
```

**Full-text indexes:**
- Purpose-built for natural language search: tokenization, stemming, stopwords, relevance ranking
- PostgreSQL GIN index on `tsvector`; Elasticsearch for production search workloads
```sql
-- PostgreSQL full-text index
CREATE INDEX idx_articles_fts ON articles USING gin(to_tsvector('english', content));

-- Query
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', 'distributed systems');
```

**When indexes hurt:**
- High-volume `INSERT`/`UPDATE`/`DELETE` tables — every write updates all indexes on the table
- Low-cardinality columns (`boolean`, a `status` enum with 2 values) — the planner
  prefers a sequential scan over an index when selectivity is low
- Columns never referenced in `WHERE`, `JOIN ON`, or `ORDER BY` — they add write overhead
  and storage with no read benefit

---

## 10. Object Storage Pattern

Object storage (AWS S3, Google Cloud Storage, Azure Blob Storage) is the correct destination
for all binary assets — user uploads, images, videos, PDFs, generated reports, database
backups. Storing binary data in a relational database is an antipattern: it bloats the DB,
cannot be CDN-cached, and makes the DB a data-transfer bottleneck.

**Pre-signed URL pattern — the standard architecture:**

```
1. Client → POST /api/upload-url → App Server
2. App Server → AWS S3: generate_presigned_url(PUT, key, expiry=15min) → returns URL
3. App Server → Client: { uploadUrl, objectKey }
4. Client → PUT {uploadUrl} (direct to S3, bypassing App Server)
5. Client → POST /api/confirm-upload { objectKey } → App Server persists metadata to DB
```

The app server is never in the data path for large file transfers — it only generates the
URL and stores the object key (path) in the database.

```python
import boto3
from botocore.config import Config

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))

def generate_upload_url(bucket: str, key: str, content_type: str,
                         expiry_seconds: int = 900) -> str:
    """Generate a pre-signed PUT URL for direct client-to-S3 upload."""
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key, "ContentType": content_type},
        ExpiresIn=expiry_seconds,
    )

def generate_download_url(bucket: str, key: str, expiry_seconds: int = 3600) -> str:
    """Generate a pre-signed GET URL for authenticated access to a private object."""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiry_seconds,
    )
```

**Key design decisions:**
- Store only the S3 **key** (path) in the database — not the full pre-signed URL, which
  contains an expiry and changes on every generation
- CDN (CloudFront) in front of S3 for frequently-accessed public objects — cache at the
  edge; significantly reduces S3 request costs and latency for global users
- Enable S3 versioning for objects subject to overwrite (profile pictures, config files);
  provides rollback without a separate backup strategy
- S3 Lifecycle policies: transition cold objects to Glacier after 90 days, expire after
  the retention requirement; eliminates manual cleanup
- Access control: bucket is private by default; expose via pre-signed URLs (private assets)
  or CloudFront signed URLs (streaming media, time-limited download links)

---

## 11. Database Engine Quick Reference

| Engine | Type | Best for | Avoid when |
|---|---|---|---|
| **PostgreSQL** | Relational (ACID) | Default choice. Complex queries, transactions, JSONB, full-text search, TimescaleDB extension for time-series | When horizontal write scaling is the primary constraint — sharding requires external tooling (Citus) |
| **MySQL / MariaDB** | Relational (ACID) | Existing MySQL workloads, read-heavy web apps, LAMP stack | Complex analytical queries (PostgreSQL's planner and window functions are superior) |
| **MongoDB** | Document (BSON/JSON), eventual | Flexible/evolving schema, hierarchical data, rapid prototyping | Complex multi-document transactions at scale; highly relational data requiring joins |
| **Redis** | Key-value, in-memory | Caching, sessions, rate limiting, pub/sub, leaderboards (sorted sets), distributed locks | Primary durable datastore — risk of data loss without AOF persistence + proper backup |
| **Cassandra** | Wide-column, AP (leaderless) | Write-heavy at extreme scale, time-series, globally distributed; access patterns fixed at design time | Ad-hoc analytical queries, strong consistency requirements, unknown access patterns |
| **DynamoDB** | Key-value / document, AP | Serverless AWS workloads, predictable single-table access, effectively unlimited scale | Relational queries, highly varied access patterns, cost-sensitive workloads with unpredictable traffic |
| **Elasticsearch** | Inverted index, distributed | Full-text search, log aggregation (ELK stack), analytics on text and semi-structured data | ACID transactions; use as a search index alongside a primary DB, not as the system of record |
| **Neo4j** | Graph | Highly connected data: social graphs, fraud detection, recommendation engines, knowledge graphs | Non-graph data — the graph overhead provides no benefit; a relational DB + recursive CTE handles most "graph-like" problems |
| **TimescaleDB** | Time-series (PostgreSQL extension) | Metrics, IoT sensor data, financial tick data — while keeping full SQL and PostgreSQL tooling | When a dedicated time-series DB (InfluxDB, VictoriaMetrics) is preferred or PostgreSQL constraints are unacceptable |

**Decision heuristic:** start with PostgreSQL. Move to a specialized engine only when a
specific property you actually need (extreme write throughput → Cassandra, full-text ranking
→ Elasticsearch, graph traversal → Neo4j) cannot be achieved with PostgreSQL and proper
indexing.

---

## 12. Query Execution Path & EXPLAIN ANALYZE

Understanding how a database executes a query is the most direct path to diagnosing slow
queries and validating index usage.

**PostgreSQL query execution path (four stages):**
1. **Parser** — transforms the SQL text into a parse tree; validates syntax
2. **Analyzer / Rewriter** — resolves table and column names, checks permissions, applies
   view rewrites and rule substitutions
3. **Planner / Optimizer** — generates candidate execution plans using cost estimates derived
   from table statistics (row counts, column cardinality, value distributions); selects the
   lowest-cost plan. Statistics are maintained by `ANALYZE` and updated automatically by
   `autovacuum`
4. **Executor** — runs the chosen plan and streams rows to the client

**Reading EXPLAIN ANALYZE:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```

Example output (nodes execute bottom-up — innermost first):
```
Sort  (cost=1234.56..1245.67 rows=4444 width=40)
      (actual time=12.345..12.456 rows=1000 loops=1)
  Sort Key: (count(o.id)) DESC
  -> HashAggregate (cost=... rows=4444 width=...)
       (actual time=9.876..10.012 rows=1000 loops=1)
       Group Key: u.id
       -> Hash Join (cost=... rows=... width=...)
              Hash Cond: (o.user_id = u.id)
              -> Seq Scan on orders o (cost=... rows=50000)
                   (actual time=0.012..3.456 rows=50000 loops=1)
                   Buffers: hit=1234 read=567
              -> Hash (cost=... rows=4444 width=...)
                   Buckets: 8192  Batches: 1
                   -> Index Scan using idx_users_created_at on users u
                        Index Cond: (created_at > '2024-01-01')
```

**Key numbers to interpret:**
- `cost=X..Y` — planner estimate (X: startup cost to first row; Y: total cost). Units are
  arbitrary but comparable within the same query plan
- `actual time=X..Y` — measured milliseconds (X: first row; Y: last row)
- `rows=N` (planner) vs `actual rows=N` (measured) — a large divergence (10×+) means
  stale statistics; run `ANALYZE table_name` to refresh
- `Buffers: hit=N read=M` — `hit` = served from shared_buffers (memory); `read` = disk I/O.
  High `read` on a hot table signals the working set doesn't fit in memory

**Scan types — ordered by cost:**
```
Index Scan      → uses an index to find matching rows, then fetches from heap
                   Efficient when selectivity is high (few rows match)
Index Only Scan → uses a covering index; no heap fetch at all
                   Most efficient; requires all projected columns in the index
Bitmap Index Scan → batches index lookups, then fetches heap pages in bulk
                   Efficient for moderate result sets; reduces random I/O
Sequential Scan → reads the entire table; efficient when most rows match
                   Fast for bulk scans; slow when misapplied to selective queries
```

**Common performance antipatterns:**
```sql
-- N+1 queries: loop in app code that executes one query per row
-- Fix: JOIN or IN clause to fetch all rows in one query

-- Function on indexed column prevents index use:
❌ WHERE LOWER(email) = 'user@example.com'
✅ CREATE INDEX idx_email_lower ON users(LOWER(email));
   WHERE LOWER(email) = 'user@example.com'  -- now uses the functional index

-- Offset-based pagination scans discarded rows:
❌ SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 100000;  -- scans 100,020 rows
✅ SELECT * FROM posts WHERE id > :last_seen_id ORDER BY id LIMIT 20;  -- keyset pagination

-- SELECT * prevents covering index use and transfers unnecessary data:
❌ SELECT * FROM orders WHERE user_id = ?
✅ SELECT id, status, total FROM orders WHERE user_id = ?
```

**Autovacuum tuning — when statistics go stale:**
```sql
-- Check table statistics freshness
SELECT relname, last_analyze, last_autoanalyze, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Force statistics refresh on a specific table
ANALYZE orders;

-- Per-table autovacuum tuning for high-write tables
ALTER TABLE orders SET (
  autovacuum_analyze_scale_factor = 0.01,  -- analyze after 1% of rows change (default: 0.2)
  autovacuum_vacuum_scale_factor  = 0.02   -- vacuum after 2% of rows change (default: 0.2)
);
