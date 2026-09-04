---
name: system-design
description: 'Expert-level distributed systems and system design skill covering scalability, caching, databases and storage, messaging/streaming, networking protocols, load balancing, and system design interview frameworks. Trigger on ANY mention of: system design, scalability, distributed systems, caching strategy, cache-aside, write-through, load balancer, message queue, Kafka, RabbitMQ, SQS, SNS, EventBridge, Kinesis, database sharding, replication, consistency, CAP theorem, CDN, DNS, HTTP/2, HTTP/3, TCP vs UDP, TLS, reverse proxy, API gateway, design a system like X, how would you scale this, what happens when you type a URL, system design interview prep. Use even for partial mentions like how does Kafka work or when should I use Redis vs Postgres. For code structure inside a service use software-architecture. For API contracts use api-engineering. For CI/CD and containers use web-devops.'
---

# System Design & Distributed Systems

Source material curated and synthesized from _The Big Archive: System Design 2025_ (ByteByteGo)
plus standard distributed-systems engineering practice. This skill covers the **infrastructure
and distributed-systems layer**: how pieces of a large system communicate, store data, and stay
available under load — as opposed to how code is organized inside a service (`software-architecture`)
or how an API contract is designed and secured (`api-engineering`).

## How to Use This Skill

1. Identify which layer the problem is in using the Quick Decision Guide below.
2. Read the relevant reference file(s) — each is self-contained.
3. For a full system design answer (interview or real proposal), start from
   `references/case-studies.md` for the framework, then pull building blocks from the
   other reference files as needed.
4. Always surface the non-functional requirements before recommending a technology —
   the right answer is always requirements-dependent.

## Quick Decision Guide

| Question                                        | Where to look                            |
| ----------------------------------------------- | ---------------------------------------- |
| Which database type fits this workload?         | `references/databases-and-storage.md`    |
| How do I make reads/writes fast at scale?       | `references/scalability-and-caching.md`  |
| How do services communicate asynchronously?     | `references/messaging-and-streaming.md`  |
| What happens at the network/protocol level?     | `references/networking-and-protocols.md` |
| How do I structure a full system design answer? | `references/case-studies.md`             |

## Core Vocabulary

- **Vertical vs. horizontal scaling**: vertical = bigger machine (hard ceiling, single point
  of failure); horizontal = more machines (requires stateless app tier or consistent partitioning).
- **Latency vs. throughput**: latency = time for one request; throughput = requests per second.
  Batching raises throughput but adds latency — the right trade-off follows from the SLA.
- **CAP theorem**: under a network partition, a system must choose Consistency or Availability.
  Tune this per-operation (strong for payments, eventual for like counters).
- **Consistency models**: strong → causal → eventual. Always pick the weakest model the feature
  can tolerate — each step toward strong consistency costs latency and availability.

## Non-Functional Requirements Checklist

Before proposing any component, answer all five:

1. **Scale** — users, average QPS, peak QPS, data volume, growth rate.
2. **Read/write ratio** — read-heavy favors caching and read replicas; write-heavy favors sharding and async processing.
3. **Consistency** — strong (financial, inventory) or eventual (view counts, feeds)?
4. **Latency budget** — real-time (<50ms), near-real-time (<500ms), or batch (minutes/hours)?
5. **Availability target** — 99.9% (8.7 h/yr downtime) vs 99.99% (52 min/yr).

Jumping to "use Kafka and Redis" before answering these is the most common system design
mistake — technology choices must follow from requirements, never precede them.

## Reference Files

- `references/scalability-and-caching.md` — load balancing algorithms (round-robin, least
  connections, consistent hashing, L4 vs L7), caching layers and patterns (cache-aside,
  write-through, write-back), invalidation strategies, failure modes (stampede, penetration,
  avalanche, hot key), read replicas, connection pooling, rate limiting algorithms.
- `references/databases-and-storage.md` — relational vs NoSQL decision matrix, normal forms,
  indexing strategies (B-tree, hash, composite, covering), sharding strategies, replication
  topologies (leader-follower, multi-leader, leaderless/quorum), object storage, engine
  cheat sheet (Postgres, MongoDB, Redis, Cassandra, DynamoDB, Elasticsearch).
- `references/messaging-and-streaming.md` — queue vs pub/sub vs log-based streaming, AWS
  services decision guide (SQS vs SNS vs EventBridge vs Kinesis), Kafka vs RabbitMQ,
  delivery guarantees, consumer groups, dead-letter queues, batch vs stream processing.
- `references/networking-and-protocols.md` — full URL-in-browser walkthrough, DNS record
  types, TCP vs UDP, TLS handshake, HTTP/1.1 vs HTTP/2 vs HTTP/3, load balancer vs reverse
  proxy vs API gateway, forward vs reverse proxy, common ports reference.
- `references/case-studies.md` — 5-step repeatable framework (requirements, estimation,
  high-level design, deep dive, bottlenecks), worked designs for a social media feed,
  URL shortener, and rate limiter; architectural evolution from monolith to distributed.
