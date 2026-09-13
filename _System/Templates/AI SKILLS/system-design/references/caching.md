# Caching

**Sources:** Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017),
Ch. 5 (Replication) and Ch. 2 (Data Models); Alex Xu, *System Design Interview* Vol. 1,
Ch. 6 (Design a Key-Value Store) and Ch. 11 (Design a News Feed System); Redis documentation
(redis.io); Cloudflare Learning Center (CDN and cache documentation); Dan Kegel, "The C10K
Problem" (1999) — background on connection caching; Jeff Dean, "Latency Numbers Every
Programmer Should Know."

---

## 1. Why Cache

A database read at p50 takes ~1–10 ms. A Redis read at p50 takes ~0.1–1 ms. An in-memory
lookup takes ~100 ns. A CDN edge hit returns a response without touching your origin servers
at all. Caching trades staleness risk for latency and cost reduction — the correct cache
strategy depends entirely on how much staleness is acceptable for a given piece of data.

**The caching hierarchy:**

```
Fastest / Most expensive / Smallest:
  Browser cache (user's device)
         │
  CDN edge cache (geographically near user)
         │
  Load balancer / reverse proxy cache (NGINX, Varnish)
         │
  Application-layer cache (Redis, Memcached)
         │
  Database query cache (pgBouncer connection pool, PostgreSQL shared_buffers)
         │
Slowest / Cheapest / Largest:
  Disk (database primary storage)
```

Each layer serves different data with different staleness tolerances. Static assets (CSS, JS,
images) belong at the CDN. User session tokens belong in Redis. Dynamic, strongly-consistent
data (current account balance, inventory count) may not belong in a cache at all.

---

## 2. Content Delivery Networks (CDN)

A CDN is a geographically distributed network of edge servers that cache static (and
increasingly, dynamic) content close to end users, reducing round-trip time and origin server
load.

```
WITHOUT CDN:
  User in São Paulo → request → origin server in us-east-1 → ~180ms RTT

WITH CDN:
  User in São Paulo → CDN edge in GRU → cache hit → ~15ms RTT
```

**Two CDN models:**

**Pull CDN** (lazy caching — most common):
- Edge servers cache content on first request from a user
- Origin sets `Cache-Control: public, max-age=86400` (or similar)
- Subsequent requests for the same URL within the TTL are served from cache
- Cache miss → CDN fetches from origin → caches → serves to user
- Use for: images, videos, JS/CSS bundles, any static or slowly-changing content

**Push CDN** (eager caching):
- You proactively upload content to CDN edge servers before any user requests it
- Appropriate for: known-large assets (video files, software downloads), content you
  need available globally before the first request arrives
- Requires explicit invalidation when content changes

**Cache-Control headers for CDNs:**
```http
# Static assets with content hash in filename — cache forever, no revalidation
Cache-Control: public, max-age=31536000, immutable

# HTML pages — short TTL, CDN must revalidate before serving stale
Cache-Control: public, max-age=60, stale-while-revalidate=300

# Personalized or auth-required content — CDN must NOT cache
Cache-Control: private, no-store

# Dynamic but shared content (API responses) — CDN may cache briefly
Cache-Control: public, s-maxage=30, stale-while-revalidate=60
```

`s-maxage` overrides `max-age` for shared caches (CDN/proxy) while `max-age` applies to
the browser. `stale-while-revalidate` allows a CDN to serve stale content immediately while
revalidating asynchronously — eliminates the latency spike of a cache miss for revalidation.

---

## 3. Application Cache — Redis

Redis is an in-memory data structure store that functions as the standard application-layer
cache in most production systems. It supports strings, hashes, lists, sets, sorted sets,
and more — it's not just a key-value store.

### Cache Patterns — Four Models

**Cache-Aside (Lazy Loading) — the most common:**
```
Read:
  app → check Redis → HIT: return Redis value
                    → MISS: app reads DB → app writes to Redis → return DB value

Write:
  app writes to DB → app invalidates (deletes) Redis key
```

```typescript
async function getUser(userId: string): Promise<User> {
  const cached = await redis.get(`user:${userId}`);
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user) throw new NotFoundError("User");

  await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));  // 1h TTL
  return user;
}

async function updateUser(userId: string, data: UserUpdate): Promise<User> {
  const user = await db.user.update({ where: { id: userId }, data });
  await redis.del(`user:${userId}`);  // invalidate on write
  return user;
}
```

Pros: only caches data that's actually requested; resilient to Redis failure (falls back
to DB). Cons: first request after a miss (or after invalidation) hits the DB — "cold start."

**Write-Through:**
```
Write:
  app → write to Redis → write to DB atomically (or Redis pipeline then DB)

Read:
  app → always reads from Redis (always populated from writes)
```

Pros: cache is always populated — no cache misses on reads. Cons: every write goes through
Redis even for data that's never read; write latency is higher.
Use when: read-heavy data where you can tolerate write overhead (user profiles, config).

**Write-Behind (Write-Back):**
```
Write:
  app → write to Redis → Redis queues the write → async flush to DB (seconds/minutes later)

Read:
  app → reads from Redis
```

Pros: extremely low write latency (Redis is in-memory). Cons: data loss risk — if Redis
crashes before the async flush, writes are lost. Acceptable for: non-critical metrics,
analytics counters, rate-limit counters. Unacceptable for: financial transactions, orders.

**Read-Through:**
```
Read:
  app → always reads from Redis → Redis MISS: Redis itself fetches from DB → returns to app
```

The cache itself handles DB reads — the app only talks to Redis. Simplifies application code.
Less common in practice; more often seen as an embedded library than a Redis pattern.

### Eviction Policies (when Redis is full)

Redis offers 8 eviction policies, configured via `maxmemory-policy` in `redis.conf`:

| Policy | Behaviour | Use when |
|---|---|---|
| `noeviction` | Reject writes when full (return error) | You must never lose data |
| `allkeys-lru` | Evict the globally least-recently-used key | General-purpose cache — most common choice |
| `volatile-lru` | Evict LRU key among keys with a TTL set | Mix of persistent and cache data in same Redis |
| `allkeys-lfu` | Evict least-frequently-used key (Kafka-style access pattern awareness) | When recent ≠ important |
| `volatile-lfu` | LFU among TTL-set keys | |
| `allkeys-random` | Evict a random key | Uniform access pattern (rare) |
| `volatile-random` | Random among TTL-set keys | |
| `volatile-ttl` | Evict key closest to TTL expiry | Favour keeping longer-lived cache entries |

**`allkeys-lru` is the right default** for a pure cache. If Redis also stores persistent
data (session tokens, locks), use `volatile-lru` to protect data without TTLs from eviction.

### Cache Stampede / Thundering Herd

When a popular cache key expires, many requests arrive simultaneously, all miss the cache,
all read from the DB concurrently, and all try to write the result back to the cache. This
is a cache stampede — it can spike DB load beyond its capacity.

**Prevention strategies:**

```typescript
// Strategy 1 — Mutex lock: only one request rebuilds the cache
async function getUserWithLock(userId: string): Promise<User> {
  const cached = await redis.get(`user:${userId}`);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:user:${userId}`;
  const acquired = await redis.set(lockKey, "1", { NX: true, EX: 5 });  // 5s lock

  if (!acquired) {
    // Another request is rebuilding — wait briefly and retry
    await sleep(50);
    return getUserWithLock(userId);  // recursive retry
  }

  try {
    const user = await db.user.findUnique({ where: { id: userId } });
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
    return user!;
  } finally {
    await redis.del(lockKey);
  }
}

// Strategy 2 — Probabilistic early revalidation (XFetch algorithm):
// Recompute a cache entry before it actually expires, with probability proportional
// to how close to expiry it is. Eliminates the expiry cliff entirely.
async function getWithEarlyRevalidation(key: string, ttl: number, fetchFn: () => Promise<unknown>) {
  const [value, remainingTtl] = await Promise.all([redis.get(key), redis.pttl(key)]);
  const beta = 1.0;  // higher = more aggressive early revalidation

  if (value && remainingTtl > 0) {
    const recomputeTime = 100;  // estimated ms to recompute
    const shouldRecompute = -recomputeTime * beta * Math.log(Math.random()) > remainingTtl;
    if (!shouldRecompute) return JSON.parse(value);
  }

  const fresh = await fetchFn();
  await redis.setex(key, ttl, JSON.stringify(fresh));
  return fresh;
}
```

**Strategy 3 — Jitter on TTL:** Add random jitter (± 10–20% of TTL) so that related keys
don't all expire simultaneously:
```typescript
const baseTtl = 3600;
const jitter = Math.floor(Math.random() * 360);  // ±10%
await redis.setex(key, baseTtl + jitter, value);
```

---

## 4. Cache Invalidation Strategies

Cache invalidation is the hardest problem because it requires knowing when the underlying
data changed, in a system where multiple services may write to that data.

**TTL-based expiry** — simplest: set a short TTL and accept brief staleness.
Best for: user preferences, product catalog, config data where brief staleness is tolerable.

**Event-driven invalidation** — the writer publishes a "data changed" event; the cache
service subscribes and deletes the relevant key.
```typescript
// After any user update (from any service):
await eventBus.publish("user.updated", { userId });

// Cache service listener:
eventBus.on("user.updated", ({ userId }) => redis.del(`user:${userId}`));
```
Best for: shared data written by multiple services where cache-aside alone can't catch all
writes. Requires an event bus (Kafka, Redis Pub/Sub, SNS).

**Write-through invalidation** — the same code path that writes to the DB also invalidates
(or repopulates) the cache atomically. Simplest when one service owns all writes to a resource.

**Cache versioning** — embed a version or generation number in the cache key:
```
user:v2:123  → changes to user schema increment version → old keys naturally expire
```
Useful for schema migrations — invalidate an entire cache namespace by bumping the version.

---

## 5. Cache Failure Modes

Beyond cache stampede (covered with code examples in §3), three additional failure patterns
have distinct characteristics and mitigations.

| Failure | What happens | Mitigation |
|---|---|---|
| **Cache stampede / thundering herd** | A hot key expires; concurrent requests all miss simultaneously and hammer the DB | Mutex lock, probabilistic early revalidation (XFetch), jittered TTL — see §3 for full implementation |
| **Cache penetration** | Requests for keys that *do not exist in the DB* (invalid IDs, probing attacks) bypass the cache on every request — a missing key is never cached, so every request hits the DB | Cache the "not found" result with a short TTL; use a Bloom filter to reject provably invalid keys before hitting either cache or DB |
| **Cache avalanche** | Many keys expire simultaneously (same TTL set at startup or during a cold fill) — mass concurrent misses spike DB load just like stampede, but across many different keys | Add random jitter to all TTLs so expirations spread over time; pre-warm the cache gradually on startup rather than filling all keys at once; Redis cluster + persistence reduces cold-start risk |
| **Hot key** | One key receives disproportionate read traffic and overwhelms its cache shard — a single Redis node becomes a bottleneck regardless of how large the cluster is | Replicate the hot key across multiple cache nodes (read from a random replica); add an in-process (L1) memory cache (e.g., `functools.lru_cache`, or a small `Map` in Node.js) in front of Redis for the highest-traffic keys |

**Cache penetration — Bloom filter pattern:**

A Bloom filter answers "definitely not in the set" with zero false negatives (no key it has
seen is ever reported absent). Route all lookups through it at the application layer: if the
filter returns "absent," skip cache and DB entirely and return a not-found response. Refresh
the filter periodically as new records are added.

```python
# uv add bloom-filter2
from bloom_filter2 import BloomFilter
import json

# Populate at startup from the DB, refresh on a schedule
valid_ids: BloomFilter = BloomFilter(max_elements=10_000_000, error_rate=0.01)

def get_user(user_id: str) -> dict | None:
    if user_id not in valid_ids:
        return None  # Definitely invalid — skip cache and DB entirely

    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    result = db.query_user(user_id)
    if result is None:
        redis.setex(f"user:{user_id}", 60, "NULL")  # cache the miss with short TTL
        return None

    redis.setex(f"user:{user_id}", 3600, json.dumps(result))
    return result
```

**Cache avalanche — jitter implementation:**

```python
import random

BASE_TTL = 3600  # 1 hour

def set_with_jitter(key: str, value: str, base_ttl: int = BASE_TTL) -> None:
    """Spread expirations by ±15% of base TTL to prevent avalanche."""
    jitter = random.randint(-int(base_ttl * 0.15), int(base_ttl * 0.15))
    redis.setex(key, base_ttl + jitter, value)
```

---

## 6. When NOT to Cache

- **Strongly-consistent reads** — if the application absolutely cannot tolerate reading stale
  data (inventory count at checkout, account balance at transfer), cache introduces an
  unacceptable correctness risk unless paired with extremely short TTLs or event-driven
  invalidation with near-zero lag
- **Write-heavy, rarely-read data** — a cache that misses on every read and writes on every
  request adds latency to writes and provides no read benefit
- **Highly unique query patterns** — if every request queries different data, the cache hit
  rate approaches zero; you're paying the write overhead with no read benefit
- **Data with complex dependency graphs** — if invalidating one cache key requires
  invalidating 50 related keys (due to denormalization), the invalidation logic becomes a
  source of bugs and subtle inconsistencies that outweigh the performance benefit
