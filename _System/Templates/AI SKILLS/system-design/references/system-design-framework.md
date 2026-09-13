# System Design Framework — Approaching Any Design Problem

**Sources:** Alex Xu, *System Design Interview* Vol. 1 (2020), Ch. 1 (A Step-By-Step
Framework); Alex Xu, *System Design Interview* Vol. 2 (2022), Ch. 1; Martin Kleppmann,
*Designing Data-Intensive Applications* (O'Reilly, 2017), Ch. 1; Donne Martin,
*System Design Primer* (github.com/donnemartin/system-design-primer, 50k+ stars —
the most-starred system design reference on GitHub); Google SRE Book, Ch. 3 (Embracing
Risk — SLO framing); ByteByteGo (Alex Xu's newsletter, newsletter.bytebytego.com).

---

## 1. The Framework — Five Steps for Any System Design Problem

A reusable methodology that applies to any system design question — whether it's "design
Twitter," "design a URL shortener," or "design a distributed cache." The goal is to
demonstrate structured thinking, not to produce a perfect answer. An interviewer evaluates
your reasoning process more than the final diagram.

```
Step 1 (5 min): Clarify Requirements
Step 2 (3 min): Capacity Estimation
Step 3 (10 min): High-Level Design
Step 4 (15 min): Deep Dive (2–3 components)
Step 5 (5 min): Bottlenecks, Trade-offs, Follow-ups
Total: ~38 min (leave time for questions and discussion)
```

### Step 1 — Clarify Requirements

Never assume. Ask before drawing. The question is deliberately ambiguous.

**Functional requirements (what the system does):**
```
"Design Twitter"
→ What features are in scope?
  - Tweeting (text only, or media?)
  - Timeline (home, user profile, trending?)
  - Following / followers?
  - Search?
  - Notifications?
→ Decide together: "Let's focus on posting tweets, following users,
  and rendering a home timeline. Not search or notifications."
```

**Non-functional requirements (quality attributes — these drive the architecture):**
```
Scale:
  - How many Daily Active Users (DAU)?
  - Read-heavy, write-heavy, or balanced? (Twitter: ~100:1 read/write)
  - Global or regional?

Performance:
  - Latency SLO? ("Timeline must load in <200ms at p95")
  - Consistency requirement? (strong, eventual, or doesn't matter?)
  - Availability requirement? ("99.99% = 52 min downtime/year")

Constraints:
  - Mobile-first or desktop-primary?
  - Any regulatory/data residency requirements?
  - Existing infrastructure or greenfield?
```

**The SLO framing (Google SRE Book, Ch. 3):**
```
Availability SLOs and their meaning:
  99%      = 3.65 days downtime/year  (unacceptable for most products)
  99.9%    = 8.7 hours/year           (acceptable for internal tools)
  99.99%   = 52 minutes/year          (consumer internet products)
  99.999%  = 5.2 minutes/year         (financial/critical systems)
```

### Step 2 — Capacity Estimation

Back-of-envelope numbers to determine scale class — see `references/back-of-envelope.md`
for the full framework. Key questions:

```
DAU:         How many? (10K, 1M, 100M, 1B?)
QPS:         DAU × requests/day / 86,400 → peak is 2–3× average
Storage:     QPS × record_size × seconds × retention_period
Bandwidth:   read QPS × response_size + write QPS × request_size
Cache:       What % of reads hit cache? (hot data rule: 20% of data = 80% of traffic)
```

This informs: do I need sharding? multiple database nodes? CDN? multiple regions?

### Step 3 — High-Level Design

Draw the architecture with boxes and arrows. Show the happy path for the 2–3 most
important use cases. **Start broad, then narrow.** Five canonical components appear in
almost every system:

```
┌─────────────────────────────────────────────────────────┐
│                     Client (Mobile/Web)                   │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                  API Gateway / Load Balancer              │
│           (auth, rate limiting, routing, SSL termination) │
└──────┬──────────────────────────────────────┬───────────┘
       │                                      │
┌──────▼──────────┐                 ┌─────────▼──────────┐
│   Web Servers    │                 │   Web Servers       │
│ (stateless app)  │                 │ (stateless app)     │
└──────┬──────────┘                 └─────────┬───────────┘
       │                                      │
┌──────▼──────────────────────────────────────▼───────────┐
│              Cache Layer (Redis / Memcached)              │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│            Primary Database + Read Replicas               │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│         Object Storage (S3/GCS) + CDN for static assets   │
└─────────────────────────────────────────────────────────┘
```

Present the data flow for each core use case:
- **Write path:** user posts tweet → API → app server → write to DB → publish event
- **Read path:** user opens timeline → API → cache hit? return; miss → DB → cache → return

### Step 4 — Deep Dive into Key Components

Pick 2–3 components where interesting trade-off decisions live and go deep. Good candidates:
- The database schema and choice
- The caching strategy and invalidation
- The feed generation mechanism (write-time vs read-time fan-out)
- The message queue / event streaming design
- The storage layer for media

**Example deep dive: Twitter home timeline**
```
Naive approach (read-time fan-out):
  → On timeline load: query all users you follow, fetch their tweets, merge, sort
  → Problem: if you follow 1000 users, that's 1000 DB reads per timeline load
  → At 350,000 timeline reads/sec (see back-of-envelope example): 350M DB reads/sec

Write-time fan-out (Twitter's actual approach for most users):
  → When a user tweets: write to all followers' timeline caches (Redis sorted set)
  → Timeline read: single Redis lookup per user — O(1)
  → Trade-off: if @user has 30M followers, writing to 30M Redis entries per tweet
    takes too long (blocking the tweet for minutes)

Hybrid (what Twitter actually does):
  → Regular users (< ~10K followers): write-time fan-out
  → Celebrities (30M followers): read-time fan-out, merged at read time
  → Lazy evaluation: inactive followers not precomputed
```

### Step 5 — Bottlenecks, Trade-offs, Follow-ups

Proactively identify what would break first and how you'd handle it:

```
Bottleneck:          Solution:
Single DB primary    → Read replicas, then sharding
Hot cache keys       → Consistent hashing, replica reads
High write volume    → CQRS, async writes via message queue
Media storage cost   → CDN tiering, lifecycle policies, compression
Cross-region latency → Geographic load balancing, data replication
Single point of failure → Redundancy at every layer, multi-AZ
```

---

## 2. Common System Design Patterns Reference

### URL Shortener (bit.ly)

**Requirements:** generate short aliases for long URLs, redirect on click, 100M DAU.
**Key insight:** read-heavy (100:1 read/write). The short → long mapping is the hot data.

```
Write path: POST /shorten → generate 7-char base62 ID → store (shortId, longUrl) in DB
Read path:  GET /{shortId} → Redis cache check (hot) → DB fallback → 301 redirect

Short code generation:
  Option A: auto-increment ID + base62 encoding
    ID 1 → "0000001", ID 100 → "0000028" (predictable — crawlable)
  Option B: MD5(long URL) → take first 7 chars (collision risk, must check)
  Option C: Snowflake ID → unique, time-ordered, no coordination needed (preferred at scale)

Database: single PostgreSQL table, indexed on short_code column
Cache: Redis (shortCode → longUrl), LRU eviction, 1-day TTL
CDN: 301 (permanent) vs 302 (temporary) redirects — 302 preserves click analytics
```

### News Feed / Social Timeline

**Core tension:** at-rest data (posts) vs materialized views (per-user timelines).

```
Option A — Pull model (compute on read):
  SELECT posts FROM followed_users WHERE created_at > last_seen ORDER BY created_at DESC
  → Simple but doesn't scale (N followees = N DB reads per page load)

Option B — Push model (pre-compute on write):
  On post: for each follower, insert post reference into their timeline cache (Redis sorted set)
  → Fast reads, expensive writes for high-follower accounts
  → Store as sorted set: ZADD timeline:{userId} {timestamp} {postId}

Option C — Hybrid (Instagram/Twitter approach):
  Push for regular users, pull for celebrities at read time, merge

Edge cases:
  → Deleted posts: filter at render time or propagate deletion events
  → Edited posts: event-driven invalidation to fan-out consumers
  → Rate of following/unfollowing: can shift a user's fan-out category
```

### Chat System (WhatsApp-style)

**Core tension:** real-time delivery vs offline queue vs read receipt reliability.

```
Message flow:
  Sender → WebSocket → Chat Server → Message DB + delivery to recipient's server

Online recipient: WebSocket push (immediate)
Offline recipient: message queued, push notification sent

Data model (Apache Cassandra is ideal — write-heavy, time-ordered queries):
  CREATE TABLE messages (
    channel_id   UUID,
    message_id   TIMEUUID,    -- time-ordered UUID for sorting
    sender_id    UUID,
    content      TEXT,
    created_at   TIMESTAMP,
    PRIMARY KEY ((channel_id), message_id)  -- partition by channel, sort by time
  );

Message ID generation: Snowflake or ULID (lexicographically sortable UUID)
Read receipts: maintain last_read_message_id per (user, channel) in a separate table
Group chats: fan-out to each member's inbox, or store once + per-member read state
```

### Rate Limiter Design

**Algorithms (each with different trade-offs):**
```
Token Bucket (Stripe's approach):
  → Bucket holds N tokens, refills at R tokens/second
  → Each request consumes 1 token; reject if empty
  → Allows bursting (bucket pre-fills during quiet periods)
  → Redis implementation: INCRBY + EXPIRE per user key

Sliding Window Log:
  → Store timestamp of each request in a sorted set
  → Count requests in the last 60 seconds
  → Most accurate — no edge-of-window bursts
  → Memory-heavy: O(requests) storage per user

Fixed Window Counter:
  → Increment counter each request, reset every minute
  → Simple: INCR + EXPIRE in Redis
  → Allows 2× burst at window boundary (last second of old + first second of new)

Sliding Window Counter (Google's approach):
  → Approximation: current_window_count + (previous_window_count × overlap_ratio)
  → Low memory, no edge burst, good accuracy
  → Redis: 2 keys per user (current and previous window count)
```

---

## 3. Distributed Systems Fundamentals Quick Reference

### CAP and Consistency Models

*(Full treatment in `references/databases-at-scale.md`)*

```
Consistency levels (weak → strong):
  Eventual: reads may return stale data; converges eventually
  Monotonic read: once you've seen a value, you won't see an older one
  Read-your-writes: after writing, your own reads reflect your write
  Bounded staleness: reads are at most X time behind the primary
  Strong (linearizable): every read reflects the most recent write globally
```

### Fault Tolerance Patterns

```
Retry with backoff: exponential delay between retries (see api-engineering)
Circuit breaker: fail fast when a dependency is unhealthy (see api-engineering)
Bulkhead: isolate failure domains — DB pool for critical vs non-critical paths
Timeout: every network call must have a timeout; default is catastrophic
Fallback: serve degraded (cached, empty, default) response when dependency fails
Graceful degradation: show the timeline without recommendations if ML service fails
```

### Idempotency at the Infrastructure Level

```
Idempotency key: client generates UUID per logical operation, includes in every attempt
Server: check Redis/DB for key before processing — return cached result on duplicate
Guaranteed delivery = at-least-once → client idempotency = effectively exactly-once
```

### Leader Election

Used when only one node in a cluster should perform an action (cron job, primary DB writes):
```
ZooKeeper / etcd: watch for lock node; first to create wins; heartbeat to hold it
Redis: SET key value NX PX 30000 (set if not exists, with 30s TTL auto-expiry)
Raft (Kafka KRaft, etcd): formal consensus protocol — fault-tolerant leader election
```

---

## 4. The Most Common Mistakes in System Design

```
❌ Jumping to solutions without clarifying requirements
   → The question is ambiguous on purpose. Ask before drawing.

❌ Designing for 1B users immediately when the requirement is 1M
   → Over-engineering: sharding, multi-region, Kafka for 1K DAU adds complexity
     for problems you don't have. State the scale threshold at which you'd add each layer.

❌ Single points of failure left unaddressed
   → Every component should have a stated redundancy strategy.
     "We'd add a standby replica" or "deploy across 2 AZs" counts.

❌ Ignoring the data model
   → Database schema and indexing strategy are often the most important design decision.
     Sketch the schema for your 2–3 most critical entities.

❌ Ignoring the failure case of the happy path
   → "What happens if Redis is unavailable?" "What if the DB is under heavy write load?"
     Show that you've thought about degradation, not just the sunny path.

❌ Proposing a technology without explaining why
   → "I'd use Kafka" is incomplete. "I'd use Kafka because we need fan-out to multiple
     independent consumers and replay capability" demonstrates understanding.

❌ Not discussing trade-offs
   → Every architectural choice trades something. Consistency vs availability.
     Write-time fan-out vs read-time. Normalization vs denormalization.
     Stating the trade-off is what separates a senior answer from a junior one.

---

## 5. Architectural Evolution Pattern — From Monolith to Multi-Region

Real systems don't start distributed — they evolve into it as traffic, data volume, and
availability requirements grow. Understanding this progression is essential for proposing the
right architecture at the right scale, and for recognizing which problems at each phase
actually justify the complexity of the next.

```
Phase 1 ─────────────────────────────────────────────────────────────── Single Server
Phase 2 ───────────────────────────────────────────── Separate Database Server
Phase 3 ──────────────────────────────── Load Balancer + Horizontal Web Tier
Phase 4 ─────────────────────── Database Read Replicas
Phase 5 ─────────────────── Cache Layer (Redis)
Phase 6 ──────────── CDN + Object Storage
Phase 7 ──────── Multi-Region / Geographic Distribution
```

---

### Phase 1 — Single Server

Everything runs on one machine: web server, application logic, and database.

```
┌──────────────────────────────────┐
│           Single Server           │
│  Web Server + App + Database      │
└──────────────────────────────────┘
```

**Capacity:** handles hundreds to low thousands of requests per day. Suitable for early-stage
products, internal tools, and proof-of-concepts. **SPOF:** the server going down takes
everything with it. **Next trigger:** CPU or memory saturation; the team can't afford the
downtime risk.

---

### Phase 2 — Separate Database Server

Move the database to its own machine. Web/app tier and DB tier scale independently.

```
┌──────────────────┐       ┌──────────────────┐
│  Web / App Server │ ────▶ │  Database Server  │
│  (stateless app)  │       │  (PostgreSQL)     │
└──────────────────┘       └──────────────────┘
```

**Benefits:** DB can be given more RAM and disk independently of the app; DB credentials are
not collocated with the web process; failure domains are separated. **Next trigger:** web
tier CPU saturation under load; a single app instance cannot handle the traffic volume.

---

### Phase 3 — Load Balancer + Horizontal Web Tier

Add a load balancer and clone the stateless web/app servers. Any instance handles any request.

```
                    ┌──────────────────┐
                    │   Load Balancer   │
                    │  (AWS ALB, NGINX) │
                    └──────┬───────────┘
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ App Srv 1 │ │ App Srv 2 │ │ App Srv 3 │
        └──────────┘ └──────────┘ └──────────┘
                           │
                    ┌──────▼───────┐
                    │   Database    │
                    └──────────────┘
```

**Prerequisites:** the application must be stateless — session state externalized to Redis,
file uploads directed to object storage (S3), configuration from environment variables.
**Benefits:** horizontal scalability; instance failure is transparent to users. **Next
trigger:** database read throughput saturation; the single primary DB becomes the bottleneck.

---

### Phase 4 — Database Read Replicas

Add read replicas. Route reads to replicas; route writes to the primary.

```
                    ┌──────────────┐
  Writes ──────────▶│    Primary    │
                    └──────┬───────┘
                           │  async replication
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Replica 1 │ │ Replica 2 │ │ Replica 3 │
        └──────────┘ └──────────┘ └──────────┘
              ▲            ▲            ▲
                        Reads
```

**Consistency caveat:** asynchronous replicas lag the primary by milliseconds to seconds.
Do not read from a replica immediately after a write you depend on being reflected — route
that read to the primary (read-your-writes). **Next trigger:** repetitive reads of the same
hot data hammering the DB even with replicas; read response time degrades as traffic grows.

---

### Phase 5 — Cache Layer (Redis)

Introduce a distributed cache. Serve hot reads from memory; the database handles only cache
misses and writes.

```
  App Servers
       │
       ▼
┌─────────────────┐     HIT: return cached value (< 1 ms)
│  Redis Cluster   │ ◀────── app checks cache first
└────────┬────────┘
         │ MISS
         ▼
┌─────────────────┐
│  DB Primary +   │
│    Replicas     │
└─────────────────┘
```

**Cache strategy:** cache-aside (lazy loading) for most use cases. Write-through for data
that is written and immediately read. TTL + jitter to prevent avalanche. **Impact:** a
20/80 hot-data distribution means 80% of reads can be served from cache — the DB sees 80%
less read traffic on popular data. **Next trigger:** media/asset delivery becomes a
bandwidth bottleneck; global users experience high latency to the origin region.

---

### Phase 6 — CDN + Object Storage

Offload static and media assets to a CDN (CloudFront, Cloudflare) backed by object storage
(S3). Move all binary assets out of the database.

```
User (São Paulo)
      │
      ▼
┌──────────────────────┐
│  CDN Edge (GRU)       │  ← ~15 ms RTT from São Paulo
│  Cache hit: image     │
└──────────────────────┘
      │ cache miss
      ▼
┌──────────────────────┐
│  S3 (us-east-1)       │  ← only on first request to this PoP
└──────────────────────┘
```

**Benefits:** origin server bandwidth drops dramatically; static asset latency falls from
150–200 ms (cross-continent) to 10–30 ms (nearest CDN PoP); S3 is effectively infinitely
scalable for object storage at low cost. **Next trigger:** core API/DB layer is the global
bottleneck; users in distant regions experience unacceptably high latency on dynamic content.

---

### Phase 7 — Multi-Region / Geographic Distribution

Deploy the full stack (app tier + DB) to multiple geographic regions. Route users to the
nearest region. Replicate data globally.

```
          ┌──────── Global DNS / GeoDNS ────────┐
          │                                       │
    us-east-1                              ap-southeast-1
  ┌──────────────┐                       ┌──────────────┐
  │ LB + App Tier │                       │ LB + App Tier │
  │ Redis Cache   │                       │ Redis Cache   │
  │ DB Primary    │◀── async replication ▶│ DB Primary   │
  └──────────────┘                       └──────────────┘
```

**Consistency challenge:** multi-region write conflicts require multi-leader replication
(last-write-wins, CRDTs) or active-passive (one primary region, replicas elsewhere for
read locality only). Active-active with strong consistency across regions is extremely
complex and should be reserved for systems with hard global consistency requirements.
**Cost:** 3–5× infrastructure cost, 10× operational complexity. Reserve for systems with
global DAU distribution and strict latency SLOs that cannot be met from a single region.

**When each phase is justified:**

| Phase | Traffic signal | Operational cost |
|---|---|---|
| 1 → 2 | DB contending with app for CPU/RAM | Low — one more server |
| 2 → 3 | App CPU saturation; can't handle peak QPS | Low — add instances + LB |
| 3 → 4 | DB read throughput > 80% at peak | Medium — replica lag management |
| 4 → 5 | Repetitive reads still hammering DB replicas | Medium — cache invalidation strategy |
| 5 → 6 | Static asset bandwidth and global asset latency | Low — managed service |
| 6 → 7 | p95 API latency > SLO from distant regions | Very high — data residency, consistency |
```
