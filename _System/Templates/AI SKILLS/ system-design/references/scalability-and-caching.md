# Scalability & Caching

## 1. Scaling Strategies

**Vertical scaling**: add CPU/RAM to one machine. Simple, no distributed complexity, but has a
hard ceiling (largest available instance type) and is a single point of failure. Right for
early-stage or inherently single-writer components (e.g., primary DB before sharding is needed).

**Horizontal scaling**: more machines behind a load balancer. Near-unlimited ceiling, but requires
the application tier to be stateless (session state externalized to Redis/DB) or requests routed
consistently to the node holding relevant state (sticky sessions, consistent hashing).

### Load Balancing Algorithms

| Algorithm                    | Behavior                                     | Best for                                    |
| ---------------------------- | -------------------------------------------- | ------------------------------------------- |
| Round robin                  | Requests distributed sequentially            | Uniform request cost, homogeneous servers   |
| Weighted round robin         | Round robin with per-server capacity weights | Heterogeneous server capacity               |
| Least connections            | Routes to fewest active connections          | Long-lived or variable-duration connections |
| IP hash / consistent hashing | Same client/key always routes to same server | Session affinity, cache locality            |
| Least response time          | Routes to lowest-latency server currently    | Latency-sensitive, variable server load     |

### Layer 4 vs. Layer 7 Load Balancing

- **L4 (transport)**: routes on IP/port only; no payload inspection. Faster, protocol-agnostic,
  but cannot route on URL path or headers.
- **L7 (application)**: inspects HTTP headers/path/cookies for content-based routing (e.g.,
  `/api/*` to one service, `/static/*` to a CDN origin). More CPU cost; enables SSL termination,
  request-level observability, and host-based routing.

---

## 2. Caching Layers (closest to furthest from user)

1. **Client cache** — browser/mobile local storage; zero network RTT; controlled via
   `Cache-Control` / `ETag` headers; eviction outside application control.
2. **CDN (edge cache)** — caches static assets and cacheable API responses near the user;
   reduces origin load and geographic latency; invalidation is the hard problem (see §4).
3. **Reverse-proxy cache** — caches whole HTTP responses in front of the app tier
   (Varnish, nginx, gateway built-in cache).
4. **Application-layer cache** — in-memory or distributed cache (Redis, Memcached) that the
   application code explicitly reads/writes; used for expensive computations or hot DB rows.
5. **Database buffer pool** — engine's own page cache; benefits from queries that repeatedly
   touch the same working set; keep hot data small enough to fit in memory.

## 3. Caching Patterns

**Cache-aside (lazy loading)** — app checks cache first; on miss, reads from DB and populates
the cache. Only requested data is cached (efficient memory use); cache failure degrades to
normal DB reads. Risk: first request after miss pays full DB latency; stale data if the DB
row changes without an explicit invalidation. Default choice for most workloads.

**Write-through** — app writes to cache and the cache synchronously writes to DB. Cache and DB
never diverge. Cost: every write pays cache + DB latency; cache holds write-only data that
may never be read, wasting memory.

**Write-back (write-behind)** — app writes to cache only; cache flushes to DB asynchronously
on a delay or batch. Lowest write latency; batched DB writes reduce load. Risk: data loss if
the cache node fails before the flush — only acceptable when the data is non-critical or
recoverable.

**Read-through** — like cache-aside, but the cache itself loads from DB on a miss (requires
the caching library to support a loader function). Simplifies application code.

---

## 4. Cache Invalidation Strategies

- **TTL expiration** — simplest; accept a staleness window in exchange for zero invalidation
  logic. Default when eventual consistency is acceptable.
- **Explicit invalidation on write** — write path deletes/updates the cache key. Every write
  path that mutates data must also touch the cache, or staleness bugs accumulate.
- **Event-driven invalidation** — CDC stream (e.g., Debezium tailing the WAL) triggers cache
  invalidation asynchronously; decouples write path from cache maintenance.
- **Versioned/namespaced keys** — change the key itself on write (include a version or
  timestamp); old entries expire unused. Avoids race conditions between invalidation and
  re-population.

---

## 5. Cache Failure Modes

| Failure                        | What happens                                                                                | Mitigation                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Stampede / thundering herd** | A hot key expires; many concurrent requests miss simultaneously and hammer the DB           | Request coalescing, staggered/jittered TTLs, background refresh before expiry      |
| **Cache penetration**          | Requests for keys that don't exist in the DB (e.g., probing attack) bypass cache every time | Cache the "not found" result with short TTL; Bloom filter to reject invalid keys   |
| **Cache avalanche**            | Many keys expire at the same moment (same TTL set at startup)                               | Add random jitter to TTLs to spread expirations                                    |
| **Hot key**                    | One key receives disproportionate traffic and overwhelms its cache shard                    | Replicate the hot key across multiple nodes; local in-process cache layer in front |

---

## 6. Database Read Scaling

**Read replicas** — async copies of the primary that serve reads. Introduces replication lag —
a read immediately after a write may not see that write on a replica (solve by routing
read-after-write to the primary, or using session-consistent reads).

**Connection pooling** — reuse DB connections across requests instead of opening a new TCP +
auth handshake per request. Pool size must be tuned to the DB's max connection limit divided
across application instances — setting it arbitrarily high starves the database.

---

## 7. Rate Limiting Algorithms

| Algorithm              | Behavior                                                                            | Trade-off                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Fixed window           | Count requests in a fixed window; reset at boundary                                 | Simple; allows 2x burst at window boundaries                              |
| Sliding window log     | Timestamp per request; count in trailing window                                     | Accurate; memory scales with request volume                               |
| Sliding window counter | Weighted average of current and previous fixed windows                              | Good approximation of sliding log with fixed memory                       |
| Token bucket           | Tokens refill at fixed rate; each request consumes one; reject when bucket is empty | Allows controlled bursts up to bucket size; most common production choice |
| Leaky bucket           | Requests queue and are processed at a fixed output rate                             | Smooths bursts into constant rate; adds latency for bursty traffic        |
