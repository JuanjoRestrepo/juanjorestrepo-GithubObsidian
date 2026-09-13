---
name: system-design
description: >
  Expert-level distributed systems and system design skill. Use whenever the user is designing
  for scale, reliability, or performance at the infrastructure level — not code structure
  (use software-architecture) or API contracts (use api-engineering). Triggers: scalability,
  horizontal/vertical scaling, load balancing, caching (CDN, Redis, cache invalidation),
  database sharding, replication, CAP theorem, PACELC, consistent hashing, back-of-envelope
  estimation, latency vs throughput, SQL vs NoSQL trade-offs, Apache Kafka, event streaming,
  message queues, distributed systems, messaging patterns (SQS/SNS/Kafka/RabbitMQ), batch
  vs. stream processing, networking (TCP/UDP, HTTP versions, TLS, DNS, proxies, ports),
  design a system like Twitter/Netflix/Uber, how do I scale this, what happens when you type
  a URL, system design interview prep. For code structure use software-architecture; for API
  contracts use api-engineering; for CI/CD use web-devops.
---

# System Design & Distributed Systems Skill

Infrastructure-level design for scalable, reliable, high-performance distributed systems.
Grounded in the source literature and industry practice.

**Canonical sources:** Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly,
2017) — the definitive technical reference; Alex Xu, *System Design Interview* Vol. 1 (2020)
and Vol. 2 (2022) — practical large-scale design framework; Google SRE Book (Beyer et al.,
O'Reilly, free online) — reliability and availability at scale; Eric Brewer, "Towards Robust
Distributed Systems" (PODC 2000) — CAP theorem origin; Daniel Abadi, "Consistency Tradeoffs
in Modern Distributed Database System Design" (IEEE Computer, 2012) — PACELC theorem.

**Complements:** `software-architecture` (how to structure the code inside a service),
`api-engineering` (how services communicate at the contract level), `web-devops` (how to
build, containerize, and deploy those services).

---

## How to Use This Skill

1. **Clarify scale and constraints first** — "design a URL shortener" means different things
   at 1K RPS and 1M RPS. Always extract: DAU (daily active users), read/write ratio, latency
   SLO, consistency requirements, and data volume before proposing architecture.
2. **Back-of-envelope estimation before architecture** — rough capacity numbers prevent
   over/under-engineering. See `references/back-of-envelope.md` for the framework.
3. **State the trade-off, not just the choice** — every component here has a trade-off.
   Caching improves latency but introduces stale data risk. Sharding improves write throughput
   but loses cross-shard transactions. Never present a component as "free."
4. **Prefer proven building blocks** — at scale, originality is a liability. Consistent
   hashing, write-through cache, leader-follower replication — these have known failure modes
   that are documented and well-understood.
5. **Kafka specifically** — see `references/kafka.md` for architecture, use cases, consumer
   groups, offsets, KRaft mode, and when NOT to introduce Kafka.

---

## Quick Decision Guide

| Situation | Approach |
|---|---|
| Single server at capacity | Vertical scaling first; then horizontal if vertical ceiling hit |
| Multiple servers, traffic distribution | Load balancer (L7 for HTTP, L4 for TCP) |
| Same data read many times, DB overloaded | Cache layer (Redis/Memcached); choose eviction + invalidation strategy |
| Static assets, global low latency | CDN |
| Write throughput bottleneck on single DB | Read replicas first; horizontal sharding if writes still bottleneck |
| Need to choose between SQL and NoSQL | Start with SQL; switch only when a specific NoSQL property is required |
| Two services need async decoupling | Message queue (for point-to-point) or Kafka (for fan-out / replay / streaming) — see `references/messaging-and-streaming.md` |
| Need to choose between SQS, SNS, Kafka, RabbitMQ | See `references/messaging-and-streaming.md` §2–3 |
| "What happens when you type a URL?" / TCP vs. UDP / HTTP versions | See `references/networking-and-protocols.md` |
| Need to route to server for a specific key | Consistent hashing |
| Cross-service transaction without 2PC | Saga pattern (see `software-architecture/references/api-first-integration-nfrs.md`) |
| "How many servers do I need for X?" | Back-of-envelope estimation — see `references/back-of-envelope.md` |

---

## 0. System Design Framework — Start Here

Before diving into any specific component, establish the approach. A system design problem
without structured framing produces an answer that jumps to conclusions, ignores constraints,
and misses the most important trade-offs.

**Five steps for any design problem:**
1. Clarify requirements (functional and non-functional) — never assume
2. Capacity estimation (DAU → QPS → storage → bandwidth)
3. High-level design (draw the boxes and data flows)
4. Deep dive into 2–3 key components where trade-offs live
5. Identify bottlenecks and state trade-offs explicitly

→ See `references/system-design-framework.md` for the full methodology, SLO framing,
common system patterns (URL shortener, news feed, chat, rate limiter), distributed systems
fundamentals quick reference, and the most common mistakes to avoid.

---

## 1. Scalability & Load Balancing

**The first question in any scaling conversation:** is the bottleneck reads, writes, compute,
or network? The answer determines the scaling strategy.

**Vertical scaling (scale up):** add more CPU, RAM, or disk to the existing machine. Simple —
no application changes required. Hard ceiling: the largest available instance type. Single
point of failure unless paired with a standby. Use first — it's often sufficient and much
cheaper than the operational complexity of horizontal scaling.

**Horizontal scaling (scale out):** add more machines. No single ceiling. Requires the
application to be stateless (session state in Redis, not in-memory) so any instance can
handle any request. Introduces coordination complexity: load balancing, distributed state,
consistency challenges.

→ See `references/scalability-load-balancing.md` for L4 vs L7 load balancers, load balancing
algorithms (round robin, least connections, consistent hashing at the LB layer), health checks,
sticky sessions, stateless service design, and horizontal database scaling with read replicas.

---

## 2. Caching

**The single most impactful performance lever in most systems.** Cache frequently-read, rarely-
changed data at the layer closest to the consumer: CDN (static assets), application cache
(Redis), DB query cache.

**The fundamental challenge:** cache invalidation. Phil Karlton's famous observation — "there
are only two hard things in computer science: cache invalidation and naming things" — exists
because invalidating a cache entry at the right moment requires knowing when the underlying
data changed, which in a distributed system is non-trivial.

→ See `references/caching.md` for CDN, Redis patterns (cache-aside, write-through, write-behind,
read-through), cache invalidation strategies, eviction policies (LRU, LFU, TTL), cache
stampede / thundering herd prevention, and the trade-off between cache freshness and latency.

---

## 3. Database Design at Scale

**Default:** start with a single relational database (PostgreSQL). Add read replicas when
reads bottleneck. Consider sharding only when write throughput or data volume exceeds what
a single primary can handle — sharding introduces join complexity, cross-shard transaction
impossibility, and operational overhead that must be justified.

**The CAP theorem** (Brewer, 2000): in a distributed system experiencing a network partition,
you must choose between Consistency and Availability — you cannot have both. **PACELC**
(Abadi, 2012) extends this: even without a partition (during normal operation), there is
a trade-off between latency and consistency. CA is not a CAP "option" — partition tolerance
is non-negotiable in any real distributed system.

→ See `references/databases-at-scale.md` for CAP and PACELC with real database classifications,
SQL vs NoSQL selection criteria, sharding strategies (range, hash, directory), consistent
hashing, replication (leader-follower, multi-leader, leaderless), and the N+W+R quorum model.

---

## 4. Apache Kafka — Distributed Event Streaming

**Kafka is a distributed event log**, not a message queue. The distinction matters: a message
queue deletes a message once consumed; Kafka retains messages for a configurable period,
allowing any number of independent consumer groups to read the same data independently, at
their own pace, and replay from any point in history.

**When Kafka is the right choice** (and when it isn't):

| Kafka is appropriate | Use a simpler message queue instead |
|---|---|
| Multiple independent consumers of the same event stream | A single consumer per message |
| Event replay is a requirement (new service needs historical data) | Messages should be deleted after consumption |
| High throughput (millions of events/second) | Moderate throughput RabbitMQ/SQS handles fine |
| Event sourcing or audit log as the source of truth | Simple task/job queue |
| Stream processing (Kafka Streams, ksqlDB) | Request/response pattern (use REST/gRPC) |

→ See `references/kafka.md` for topics, partitions, brokers, producers, consumers, consumer
groups, offsets, KRaft mode (Kafka 4.0, ZooKeeper removed), at-least-once vs exactly-once
semantics, Kafka Streams, Python and TypeScript client implementations, and operational
concerns (consumer lag, rebalancing, retention).

---

## 5. Back-of-Envelope Estimation

Every system design starts with capacity estimation. Getting the order of magnitude wrong leads
to fundamentally incorrect architecture decisions — under-provisioning fails under load,
over-provisioning wastes budget and complexity.

→ See `references/back-of-envelope.md` for the latency numbers every engineer should know
(Kleppmann/Jeff Dean), storage/bandwidth estimation framework, DAU-to-QPS conversion, and
worked examples (design Twitter's storage, design a URL shortener).

---

## Cross-Cutting: The Over-Engineering Test

Apply before adding any component:
1. **What specific, measured problem does this solve?** "It might scale later" is not a problem.
2. **What is the operational cost?** Every distributed component is another thing to monitor,
   upgrade, debug, and on-call for.
3. **Is the simpler alternative actually insufficient?** A single PostgreSQL instance with
   proper indexes handles tens of thousands of requests per second for most applications.
   Adding Redis, Kafka, and sharding before hitting that ceiling adds complexity for problems
   that don't exist yet.

The most common system design mistake is not under-engineering — it's adding Kafka, sharding,
and multiple caching layers to a system that will never exceed 1000 DAU.

---

## Reference Files

- `references/system-design-framework.md` — five-step methodology, SLO/availability framing,
  high-level architecture template, common patterns (URL shortener, news feed, chat system,
  rate limiter), distributed systems quick reference, architectural evolution pattern
  (7-phase progression from monolith to multi-region), common mistakes
- `references/scalability-load-balancing.md` — vertical vs horizontal scaling, Scale Cube,
  L4/L7 load balancers, load balancing algorithms, health checks, stateless service design,
  read replicas
- `references/caching.md` — CDN (pull/push), Redis patterns (cache-aside, write-through,
  write-behind, read-through), invalidation strategies, eviction policies, cache failure modes
  (stampede, penetration + Bloom filter, avalanche, hot key), when NOT to cache
- `references/databases-at-scale.md` — CAP theorem, PACELC, SQL vs NoSQL trade-offs,
  sharding strategies, consistent hashing, replication models, quorum reads/writes, normal
  forms (1NF–BCNF), indexing strategies (B-tree, hash, composite, covering, partial,
  full-text), object storage pattern (pre-signed URLs), engine quick reference (PostgreSQL,
  MySQL, MongoDB, Redis, Cassandra, DynamoDB, Elasticsearch, Neo4j, TimescaleDB), query
  execution path and EXPLAIN ANALYZE guidance
- `references/kafka.md` — Kafka architecture (topics, partitions, brokers, KRaft 4.0),
  consumer groups, offsets, delivery semantics, Kafka Streams, Python/TypeScript
  implementations, operational concerns, when NOT to use Kafka, managed alternatives
- `references/messaging-and-streaming.md` — core messaging patterns (queue vs pub/sub vs
  log-based), AWS managed services decision guide (SQS, SNS, EventBridge, Kinesis),
  Kafka vs. RabbitMQ comparison, delivery guarantees, dead-letter queues, batch vs. stream
  processing, Lambda vs. Kappa architecture
- `references/networking-and-protocols.md` — full URL request lifecycle (DNS → TCP → TLS →
  HTTP → server → render), TCP vs. UDP, HTTP/1.1 vs. HTTP/2 vs. HTTP/3 (QUIC), load
  balancer vs. reverse proxy vs. API gateway, forward vs. reverse proxy, DNS record types,
  common ports reference
- `references/back-of-envelope.md` — latency numbers (Jeff Dean), storage estimation,
  DAU-to-QPS framework, worked examples (Twitter, URL shortener, chat application)
