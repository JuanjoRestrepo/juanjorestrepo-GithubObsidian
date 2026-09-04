# Messaging & Streaming

## 1. Core Patterns

| Pattern              | Description                                                                         | Example                                                               |
| -------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Point-to-point queue | One producer; one consumer (or competing consumer pool) processes each message once | Order processing — any one worker picks up each order                 |
| Pub/sub (fan-out)    | One producer; many independent subscribers each receive a copy                      | New order event fans out to email, inventory, and analytics consumers |
| Log-based streaming  | Append-only, partitioned, replayable log; consumers track their own offset          | Event sourcing, real-time analytics, audit trails                     |

**Queue vs. log**: a queue deletes a message once consumed; a log retains messages for a
configured retention period regardless of consumption, allowing multiple independent consumers
to replay from any offset. This is why Kafka is used for both messaging and as a durable event
store.

---

## 2. AWS Messaging Services Decision Guide

| Service         | Model                                      | Best for                                                                                         |
| --------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **SQS**         | Point-to-point queue (standard or FIFO)    | Decoupling producer/consumer, work queues, buffering bursty traffic in front of a slower service |
| **SNS**         | Pub/sub fan-out                            | Broadcasting one event to multiple independent subscribers simultaneously                        |
| **EventBridge** | Event bus with content-based routing rules | Complex event routing across many producers/consumers, SaaS integrations, rule-based filtering   |
| **Kinesis**     | Managed log-based streaming (Kafka-like)   | Real-time analytics, clickstream, ordered per-shard processing with replay                       |

**SNS + SQS fan-out pattern**: SNS publishes once; multiple SQS queues subscribe — each feeds
an independent consumer. Combines pub/sub fan-out with queue-like durability and per-consumer
retry/backoff. Standard AWS pattern when a pub/sub event needs queue-level reliability.

---

## 3. Kafka vs. RabbitMQ

| Dimension           | Kafka                                                                           | RabbitMQ                                                                            |
| ------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Model               | Distributed commit log, partitioned, replayable                                 | Traditional message broker (queues, exchanges, routing)                             |
| Message retention   | Configurable; retained regardless of consumption                                | Deleted once acknowledged                                                           |
| Ordering            | Strict within a partition                                                       | Strict within a single queue                                                        |
| Throughput ceiling  | Very high (firehose-scale event streams)                                        | High, but lower than Kafka at extreme scale                                         |
| Routing flexibility | Topic/partition; routing logic lives in consumer or stream processor            | Rich built-in routing (direct, topic, fanout, headers exchanges) at the broker      |
| Replay              | Native — rewind to any retained offset                                          | Not native — consumed+acked messages are gone                                       |
| Best fit            | Event sourcing, log aggregation, stream pipelines, systems needing replay/audit | Task queues, RPC-style request/reply, complex routing, lower operational complexity |

---

## 4. Delivery Guarantees

| Guarantee     | Meaning                              | Risk                                                                                       |
| ------------- | ------------------------------------ | ------------------------------------------------------------------------------------------ |
| At-most-once  | Delivered zero or one times          | Possible message loss — acceptable for non-critical telemetry                              |
| At-least-once | Delivered one or more times          | Possible duplicate delivery — consumer must be idempotent                                  |
| Exactly-once  | Delivered and processed exactly once | Hardest to guarantee end-to-end; usually achieved via idempotent consumers + deduplication |

**Practical default**: design consumers to be idempotent and build systems around at-least-once
delivery. "Exactly-once" broker claims mean "effectively exactly-once given an idempotent
consumer" — not a literal guarantee against all failure modes.

---

## 5. Consumer Groups & Ordering

- **Consumer group (Kafka)**: multiple instances share the work of reading a topic; each
  partition assigned to exactly one consumer within the group — parallelism across partitions,
  ordering preserved within each.
- **Ordering trade-off**: strict global ordering requires a single partition, capping throughput
  to what one consumer can process. Most systems accept ordering only within a partition
  (e.g., partition by `user_id` so all events per user are ordered, but users interleave).
- **Rebalancing**: when a consumer joins or leaves, partitions are reassigned — brief processing
  pause; consumers must commit offsets before losing a partition.

---

## 6. Dead-Letter Queues (DLQ)

A DLQ captures messages that fail processing after N retries, preventing them from blocking the
main queue or being silently dropped.

- Configure a **max receive count**; after that threshold, route to the DLQ instead of
  retrying indefinitely.
- A DLQ nobody monitors is equivalent to silently dropping messages — the safety net is only
  real if there is an alert and an operational process (inspect, fix, replay or discard).
- Common root causes: malformed message schema, permanently unavailable downstream dependency,
  or a poison-pill message that deterministically crashes the consumer on every attempt.

---

## 7. Batch vs. Stream Processing

| Dimension             | Batch                                                                                          | Stream                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Latency               | Minutes to hours (scheduled, on accumulated data)                                              | Milliseconds to seconds (continuous, per-event)                                             |
| Throughput efficiency | High — amortizes overhead across large batches                                                 | Lower per-event, but continuous                                                             |
| Failure model         | Simpler — rerun the batch                                                                      | Harder — out-of-order events, watermarks, exactly-once state                                |
| Typical tools         | Spark batch, Airflow ETL, dbt                                                                  | Kafka Streams, Flink, Spark Structured Streaming                                            |
| Best fit              | Daily/hourly reporting, large historical reprocessing, anything where real-time isn't required | Fraud detection, real-time dashboards, alerting, data whose value decays quickly with delay |

**Lambda vs. Kappa architecture**: Lambda runs both a batch and a stream path in parallel
(stream for speed, batch for correctness/reprocessing) — powerful but doubles pipeline logic.
Kappa uses the stream as the single source of truth and replays the log for reprocessing —
simpler when the streaming engine supports efficient replay (Kafka's retention makes this
practical).
