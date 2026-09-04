# System Design Method & Case Studies

## 1. The 5-Step Framework

Use this structure for any open-ended system design prompt — interview or real proposal.
Spending 40–50% of total time on steps 1–2 before jumping to components is appropriate.

### Step 1 — Clarify Requirements

**Functional**: what must the system actually do? List the 3–5 core user actions explicitly.
For a social feed: post content, follow users, view personalized feed, like/comment. Confirm
what is explicitly out of scope.

**Non-functional**: scale (users, QPS, data volume), read/write ratio, consistency requirement,
latency target, availability target. Use the checklist in the main SKILL.md.

### Step 2 — Back-of-Envelope Estimation

Numbers that drive every downstream decision:

- **Traffic**: daily active users × actions per user / seconds per day = average QPS; × peak
  factor (2–5x) = peak QPS.
- **Storage**: avg object size × objects/day × retention days × replication factor.
- **Bandwidth**: QPS × avg payload size (separately for read and write paths).

These numbers determine whether a single DB can handle the load (often much longer than
intuition suggests) or whether sharding/caching/CDN is justified from day one.

### Step 3 — High-Level Design

Sketch major components and data flow: client → CDN/gateway → load balancer → app services →
cache → DB → async workers/queues. Keep it at the box-and-arrow level; resist diving into any
one component's internals until the overall shape is agreed.

### Step 4 — Deep Dive on 1–2 Components

Pick the component(s) most central to the problem's hard part. Go deep: exact data model,
specific technology choice with justification, how it handles the estimated scale from Step 2.

### Step 5 — Identify Bottlenecks & Trade-offs

Name the single points of failure, the component most likely to be the first bottleneck at
10x scale, and what would change in the design at that point. A strong answer acknowledges
trade-offs explicitly rather than presenting the design as flawless — every design decision
costs something in exchange for what it buys.

---

## 2. Worked Design: Social Media Feed (Instagram-style)

**Core actions**: upload post (image/video + caption), follow user, view personalized feed,
like/comment.

**High-level flow**:

1. Client uploads media → API gateway → app server generates a **pre-signed URL** for direct
   upload to object storage (S3). The binary never routes through the application tier.
2. Post metadata (caption, media URL, author, timestamp) written to a relational DB (structured,
   needs integrity) or document store if schema varies significantly by post type.
3. High-write-throughput data — likes, view counts, activity logs — written to a write-optimized
   store (Cassandra) or buffered through cache and flushed asynchronously; these tolerate
   eventual consistency.
4. **Feed generation strategy** — the central design decision:
   - _Fan-out on write (push)_: when a user posts, the post is immediately pushed to every
     follower's precomputed feed. Fast reads; expensive writes for high-follower-count accounts
     (a celebrity's post fans out to millions of feeds).
   - _Fan-out on read (pull)_: feed assembled at read time by querying posts from all followed
     accounts. Cheap writes; expensive reads, especially for users following many accounts.
   - _Hybrid (real systems)_: fan-out on write for typical users; fan-out on read (or a merge
     step at feed-view time) for high-follower-count accounts. Avoids the celebrity write
     cost while keeping normal-user reads fast. Every major platform uses this approach.
5. Notifications (new follower, new like) dispatched **asynchronously via queue** so the
   triggering write path isn't blocked on notification delivery.

**Core bottleneck**: the fan-out strategy is a direct trade-off between write cost and read
cost; the right choice depends on the follower-count distribution, which is why the hybrid
approach exists in practice.

---

## 3. Worked Design: URL Shortener

**Core actions**: submit a long URL → receive a short code; visiting the short URL redirects.

**ID generation options**:

| Approach                        | How it works                                                            | Trade-off                                                                                                                        |
| ------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Random string + collision check | Generate random 6–8 char string; check DB for collision; retry if taken | Simple; collision probability rises as keyspace fills                                                                            |
| Base62 of auto-incrementing ID  | Centralized (or coordinated) counter → encode to base62                 | No collisions; single counter can become a write bottleneck at extreme scale — mitigated with pre-allocated ID ranges per server |
| Truncated hash of URL           | `MD5/SHA(url)`, first N chars                                           | Same URL always maps to same code; truncated hashes still collide; need fallback                                                 |

**Read path**: redirect lookup is the overwhelmingly dominant operation (many more reads than
writes). Textbook cache-aside candidate — cache `short_code → long_url` aggressively, since a
short URL's target essentially never changes after creation.

**Data model**: `short_code (PK), long_url, created_at, expires_at, click_count`.
Click count is write-heavy — use async-incremented counter (queue + batch update, or separate
write-optimized store) rather than a synchronous update on every redirect.

---

## 4. Worked Design: Rate Limiter

**Core requirement**: reject requests beyond a threshold per client/key within a time window,
with minimal added latency to allowed requests.

**Where it lives**: API gateway (centralized, consistent across all backend instances) or
in-application (simpler; each instance enforces its own limit unless backed by a shared store).
A distributed rate limiter needs a shared, low-latency store — Redis using atomic `INCR` with
TTL for fixed-window, or a sorted set for sliding window log.

**Algorithm**: see `scalability-and-caching.md` §7 for the full comparison — token bucket is
the most common production choice (controlled bursts, steady-state rate limit).

**Distributed correctness**: naive `GET` + check + `SET` against Redis has a race condition
(two concurrent requests read the same count before either writes the increment). Use Redis's
atomic `INCR` or a Lua script for multi-step logic — never separate read-then-write calls.

---

## 5. Architectural Evolution Pattern

The consistent pattern across platforms that scaled from a single-server MVP to global scale:

1. **Monolith + single relational DB** — the correct starting point; premature distributed
   complexity is the most common early-stage mistake.
2. **Vertical scaling of the DB** until it is clearly the bottleneck (often much later than
   teams expect).
3. **Read replicas + application-layer cache (Redis)** for the hottest read paths.
4. **Functional decomposition** — splitting the monolith into services around clear domain
   boundaries once team size and deployment coupling (not raw traffic) make the monolith
   painful to ship.
5. **Sharding** once a single primary can no longer hold the write volume; shard key aligned
   with the dominant access pattern.
6. **Async processing via queues/streams** for anything not on the critical response path —
   notifications, analytics, search-index updates, media transcoding.
7. **Multi-region deployment** once latency-to-user or data residency requirements demand it;
   the point at which multi-leader replication and conflict resolution become unavoidable.

**The recurring lesson**: the architecture a system needs is a function of its current scale
and team size — not a fixed "best practice" applied from day one. Introducing sharding or
multi-region replication before the corresponding bottleneck actually exists adds operational
cost without benefit. The skill in system design is recognizing which problem is actually
present, not defaulting to the most sophisticated available solution.
