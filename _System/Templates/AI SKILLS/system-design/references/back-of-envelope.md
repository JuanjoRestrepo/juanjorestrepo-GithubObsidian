# Back-of-Envelope Estimation

**Sources:** Jeff Dean and Sanjay Ghemawat, "Numbers Every Engineer Should Know" (Google
Engineering, widely cited since ~2010); Martin Kleppmann, *Designing Data-Intensive
Applications* (O'Reilly, 2017), Ch. 1 (Reliability, Scalability, Maintainability); Alex Xu,
*System Design Interview* Vol. 1 (2020), Ch. 2 (Back-of-the-Envelope Estimation); Peter
Norvig, "Teach Yourself Programming in Ten Years" (norvig.com) — latency numbers context.

---

## 1. Why Estimation Matters

A system design discussion without capacity estimation produces architectures that are either
dramatically over-engineered (sharding a system that will never exceed 10 RPS) or structurally
incapable of handling the stated load (a single database primary for a system expecting 1M
DAU with heavy writes). Two minutes of estimation prevents both failure modes.

The goal is **order-of-magnitude accuracy** — within 10× is sufficient to make correct
architectural decisions. You are not computing a billing number; you are determining whether
you need 1 server or 100, one database or a sharded cluster, a CDN or not.

---

## 2. Latency Numbers Every Engineer Should Know

These numbers, originally from Jeff Dean (Google), are approximate orders of magnitude.
Exact values shift with hardware generation; the ratios and ordering are stable and are what
matter for architectural reasoning.

```
Operation                              Approximate Latency   Relative to L1 cache
─────────────────────────────────────────────────────────────────────────────────
L1 cache reference                     0.5 ns                1×
Branch misprediction                   5 ns                  10×
L2 cache reference                     7 ns                  14×
Mutex lock/unlock                      25 ns                 50×
Main memory reference                  100 ns                200×
Compress 1K bytes (Snappy)             3,000 ns  = 3 μs      6,000×
Send 1KB over 1 Gbps network           10,000 ns = 10 μs     20,000×
Read 4KB from SSD (random)             150,000 ns = 0.15 ms  300,000×
Read 1MB sequentially from memory      250,000 ns = 0.25 ms  500,000×
Round trip within same datacenter      500,000 ns = 0.5 ms   1,000,000×
Read 1MB sequentially from SSD         1,000,000 ns = 1 ms   2,000,000×
Disk seek (HDD)                        10,000,000 ns = 10 ms 20,000,000×
Read 1MB sequentially from disk (HDD)  20,000,000 ns = 20 ms 40,000,000×
Send packet: California → Netherlands  150,000,000 ns = 150ms 300,000,000×
```

**Key architectural conclusions from these numbers:**

1. **Memory is 200× faster than disk (random)** — design your hot path to be memory-resident.
   This is why Redis cache hit = ~0.5ms vs PostgreSQL uncached read = ~10–50ms.

2. **Same-datacenter round trip ≈ 0.5ms** — microservice call overhead is real. A request
   fan-out to 10 internal services adds ~5ms in network overhead alone, before any processing.
   This is one argument for modular monoliths (in-process calls, ~100ns) over microservices.

3. **SSD random reads ≈ 0.15ms** — fast, but 300× slower than memory. The gap justifies
   in-memory caches for frequently-accessed, hot data.

4. **Cross-continent latency ≈ 150ms** — fundamental physics. A CDN edge server serves users
   from ~15ms; origin servers from a different continent serve at 150ms+. At 150ms, a user
   can perceive the latency as "slow" — CDNs exist to close this gap.

---

## 3. Storage and Throughput Units

```
Power of 2:
  1 KB  = 10³ bytes  ≈ 10^3
  1 MB  = 10^6 bytes
  1 GB  = 10^9 bytes
  1 TB  = 10^12 bytes
  1 PB  = 10^15 bytes

Time conversions:
  1 day   = 86,400 seconds ≈ 10^5 seconds (close enough for estimation)
  1 month = 2.5 × 10^6 seconds
  1 year  = 3.15 × 10^7 seconds ≈ 10^7.5

Throughput rules of thumb:
  A single PostgreSQL primary: ~10,000 simple reads/sec, ~2,000–5,000 writes/sec
  A Redis node: ~100,000 ops/sec (reads and writes)
  A well-optimized Node.js/FastAPI server: ~10,000–50,000 req/sec (simple endpoints)
  A Kafka broker partition: ~1,000–50,000 messages/sec (depends on message size)
  CDN bandwidth: effectively unlimited (100s of Gbps per PoP)
```

---

## 4. The Estimation Framework

Use this sequence for any system design estimation problem:

```
1. DAU (Daily Active Users)
   └─▶ 2. Requests Per Second (QPS)
         └─▶ 3. Storage Per Day / Per Year
               └─▶ 4. Bandwidth
                     └─▶ 5. Server / Cache / DB count
```

### Step 1 → Step 2: DAU to QPS

```
QPS (average) = DAU × requests_per_user_per_day / 86,400 seconds

Peak QPS ≈ 2–3× average QPS
  (traffic is not uniform — most traffic arrives in a few peak hours)
```

### Step 3: Storage

```
Storage per day = QPS × seconds_per_day × bytes_per_record
               = QPS × 86,400 × record_size

Storage per year = Storage per day × 365
```

### Step 4: Bandwidth

```
Inbound bandwidth  = write QPS × average_request_size
Outbound bandwidth = read QPS × average_response_size
```

### Step 5: Server Count

```
Servers = Peak QPS / QPS_per_server

Where QPS_per_server depends on operation type:
  CPU-bound (encryption, compression, complex logic): ~2,000–5,000 req/sec per core
  I/O-bound (database calls, external APIs): ~10,000–50,000 req/sec (async)
```

---

## 5. Worked Examples

### Example A — Design Twitter's Storage

**Given:** 300M DAU, average user posts 1 tweet/day, reads 100 tweets/day,
tweet size ≈ 280 chars ≈ 280 bytes text + 500 bytes metadata = ~800 bytes.
Images: 10% of tweets include a 500KB image.

**Step 1: Write QPS (tweets):**
```
Write QPS = 300M × 1 tweet/day / 86,400 ≈ 3,500 tweets/sec
Peak write QPS ≈ 10,000/sec
```

**Step 2: Read QPS:**
```
Read QPS = 300M × 100 reads/day / 86,400 ≈ 350,000 reads/sec
Read:write ratio ≈ 100:1 (extremely read-heavy — Redis cache is essential)
```

**Step 3: Storage:**
```
Tweet text per day:     3,500 tweets/sec × 86,400 × 800 bytes ≈ 240 GB/day
Images per day:         3,500 × 0.10 × 86,400 × 500 KB ≈ 15 TB/day
Total per day:          ~15 TB/day
Per year:               ~5.5 PB/year
5-year storage:         ~27 PB (for media — text is negligible by comparison)
```

**Step 4: Architectural conclusions:**
- 350K read QPS → cannot serve from DB alone → Redis cache is mandatory
- Read replicas needed to handle even cache-miss reads
- 15 TB/day of media → object storage (S3/GCS), not database storage
- Serving global users at 150ms+ without CDN is not viable → CDN mandatory
- Timeline generation: 350K reads × 100 tweet fan-out = 35M DB rows/sec for naive approach
  → write-time fan-out (pre-computed timelines in Redis) for normal users;
  read-time for celebrities with 30M+ followers (same conclusion Twitter documented in 2012)

---

### Example B — Design a URL Shortener

**Given:** 100M DAU, 10% create short URLs (10M/day), 90% click existing links (90M/day).
Short URL ≈ 7 chars (e.g., bit.ly/abc1234) → 100B possible URLs. URL record ≈ 500 bytes.

**Step 1: Write QPS (new URLs):**
```
Write QPS = 10M / 86,400 ≈ 115 writes/sec (very low — DB handles easily)
```

**Step 2: Read QPS (redirects):**
```
Read QPS = 90M / 86,400 ≈ 1,040 reads/sec
Peak read QPS ≈ 3,000/sec
```

**Step 3: Storage:**
```
Per day: 10M records × 500 bytes = 5 GB/day
Per year: 5 GB × 365 = 1.8 TB/year
10-year storage: 18 TB — a single database handles this comfortably
```

**Step 4: Architectural conclusions:**
- 1,040 read QPS with 500-byte records → single PostgreSQL primary handles this with ease
- Add Redis cache: most short URLs are accessed in bursts shortly after creation.
  Cache hit rate likely 80–90% → DB sees only ~200 reads/sec
- No sharding needed — data volume and QPS are both manageable by a single DB
- 7-character base62 short code: 62^7 ≈ 3.5 trillion unique URLs — more than sufficient
- ID generation: auto-increment + base62 encoding, or distributed ID (Snowflake if multi-region)

---

### Example C — Design a Chat Application (Back-End Capacity)

**Given:** 50M DAU, average user sends 40 messages/day, message = 100 bytes.
Messages stored 5 years. 10% of messages include a 100KB image.

**Write QPS:**
```
50M × 40 / 86,400 ≈ 23,000 messages/sec
```

**Storage:**
```
Text per day: 23,000 × 86,400 × 100 bytes ≈ 200 GB/day
Images per day: 23,000 × 0.10 × 86,400 × 100 KB ≈ 2 TB/day
Per year: 73 TB text + 730 TB images ≈ 800 TB/year
5-year: 4 PB — requires distributed storage
```

**Architectural conclusions:**
- 23,000 writes/sec → exceeds single-DB write capacity → sharding by user_id required,
  OR Cassandra (designed for write-heavy time-series workloads at this scale)
- Messages are naturally partitioned by conversation/user_id — good shard key
- 4 PB media → object storage (S3), not DB
- WebSocket connections: 50M DAU × peak concurrency factor (~10%) = 5M concurrent WebSocket
  connections → horizontal scaling with Redis Pub/Sub required (see websockets.md in api-engineering)

---

## 6. Common Mistakes in Estimation

```
❌ Forgetting peak vs average — peak is 2–3× average for typical diurnal patterns;
   global apps with users across time zones may be more uniform

❌ Ignoring read:write ratio — a read-heavy app (Twitter, Reddit) needs read replicas and
   caching; a write-heavy app (logging, IoT) needs write throughput optimization

❌ Confusing MB and GB (or GB and TB) — one order of magnitude changes the entire architecture

❌ Assuming all storage is equal — 10 TB of object storage (cheap, ~$0.02/GB/month) is very
   different from 10 TB of RDS database storage (~$0.10/GB/month) or NVMe SSD ($1+/GB/month)

❌ Not considering replication factor — if you need 3× replication (standard production),
   your actual storage is 3× the raw data size

❌ Treating "active users" as "concurrent users" — 100M DAU does not mean 100M concurrent
   connections. Concurrent sessions at peak are typically 1–5% of DAU
```
