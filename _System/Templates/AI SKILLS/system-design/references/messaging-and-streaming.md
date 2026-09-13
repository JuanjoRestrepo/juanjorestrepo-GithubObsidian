# Messaging & Streaming

**Sources:** AWS documentation — SQS, SNS, EventBridge, Kinesis; RabbitMQ documentation
(rabbitmq.com); Apache Kafka documentation (kafka.apache.org); Martin Kleppmann, *Designing
Data-Intensive Applications* (O'Reilly, 2017), Ch. 11 (Stream Processing); Jay Kreps, "The
Log: What every software engineer should know about real-time data's unifying abstraction"
(LinkedIn Engineering Blog, 2013); Nathan Marz, James Warren, *Big Data* (Manning, 2015) —
Lambda architecture; Stephan Ewen et al., "Apache Flink: Stream and Batch Processing in a
Single Engine" (IEEE Data Engineering Bulletin, 2015) — Kappa motivation.

**Kafka-specific content** (topics, partitions, consumer groups, offsets, delivery semantics,
KRaft, Python/TypeScript implementations, operational concerns) is covered in `references/kafka.md`.
This file covers the broader messaging and streaming landscape: when to use which system,
cross-platform patterns, and the batch vs. stream architecture decision.

---

## 1. Core Messaging Patterns

Three fundamental patterns underlie all messaging and streaming infrastructure. Every
concrete technology maps to one (or a combination) of these.

| Pattern | Description | Message fate | Example use case |
|---|---|---|---|
| **Point-to-point queue** | One producer; one consumer (or competing consumer pool) processes each message exactly once | Deleted once acknowledged | Order processing — any one worker picks up each order |
| **Pub/sub (fan-out)** | One producer; many independent subscribers each receive a copy of every message | Delivered to all subscribers | New order event fans out to email service, inventory service, and analytics simultaneously |
| **Log-based streaming** | Append-only, partitioned, replayable log; consumers track their own offset; message retention is time- or size-bounded, not consumption-bounded | Retained regardless of consumption; replayed at will | Event sourcing, real-time analytics, audit trails, feeding a new service with historical data |

**Queue vs. log — the critical distinction:** a traditional queue deletes a message once
a consumer acknowledges it; a log retains all messages for a configured retention period
regardless of how many consumers have read them, allowing multiple independent consumer
groups to replay from any offset. This is why Kafka serves as both a message bus and a
durable event store simultaneously.

---

## 2. AWS Managed Messaging Services

For cloud-native architectures on AWS, four managed services map to the three patterns above.

| Service | Model | Ordering | Retention | Best for |
|---|---|---|---|---|
| **SQS Standard** | Point-to-point queue | Best-effort (no guarantee) | Up to 14 days | Decoupling producer/consumer, work queues, buffering bursty writes in front of a slower service |
| **SQS FIFO** | Point-to-point queue | Strict FIFO (300 TPS limit) | Up to 14 days | Workflows requiring ordered, exactly-once processing at moderate throughput |
| **SNS** | Pub/sub fan-out | No ordering | Delivery only (no replay) | Broadcasting one event to multiple independent subscribers simultaneously |
| **EventBridge** | Event bus with content-based routing rules | No guarantee | Replay from archive (opt-in) | Complex routing across many producers/consumers, SaaS integrations, rule-based filtering |
| **Kinesis Data Streams** | Log-based streaming (Kafka-compatible model) | Strict per-shard | 1–365 days | Real-time analytics, clickstream, IoT, ordered per-shard processing with replay |

**SNS + SQS fan-out pattern — the standard AWS combination:**
SNS publishes one event; multiple SQS queues subscribe to that SNS topic, each feeding an
independent consumer service. Combines pub/sub fan-out with queue-level durability and
per-consumer retry/dead-letter handling.

```
            ┌─────────────────────────────────────────┐
            │               SNS Topic                  │
            │          "order-placed"                  │
            └───────┬──────────────┬──────────────────┘
                    │              │              │
           ┌────────▼────┐ ┌───────▼────┐ ┌─────▼────────┐
           │  SQS Queue   │ │  SQS Queue  │ │  SQS Queue   │
           │  (email svc) │ │  (inventory)│ │  (analytics) │
           └─────────────┘ └────────────┘ └──────────────┘
```

Each SQS queue maintains its own independent backlog, retry policy, and dead-letter queue.
If the inventory service is down, its queue accumulates — the email service is unaffected.

---

## 3. Kafka vs. RabbitMQ

The two most common self-hosted messaging systems serve fundamentally different purposes.

| Dimension | Apache Kafka | RabbitMQ |
|---|---|---|
| **Model** | Distributed commit log, partitioned, replayable | Traditional message broker (queues, exchanges, routing) |
| **Message fate** | Retained for configurable period regardless of consumption | Deleted once acknowledged by consumer |
| **Ordering** | Strict within a partition | Strict within a single queue |
| **Throughput ceiling** | Very high — millions of events/second per cluster | High, but lower than Kafka at extreme scale |
| **Routing** | Topic/partition; routing logic lives in consumer or stream processor | Rich built-in routing at the broker (direct, topic, fanout, headers exchanges) |
| **Replay** | Native — any consumer group can rewind to any retained offset | Not native — consumed and acknowledged messages are gone |
| **Protocol** | Custom Kafka protocol (TCP) | AMQP (and others: STOMP, MQTT) |
| **Operational complexity** | High — partition sizing, consumer group management, schema registry, retention tuning | Lower — simpler to deploy for teams without streaming expertise |
| **Best fit** | Event sourcing, log aggregation, multi-consumer fan-out, systems needing replay or audit trail, stream processing pipelines | Task queues, RPC-style request/reply, complex broker-side routing, teams where operational simplicity is a priority |

**Decision rule of thumb:** if you need multiple independent consumers reading the same
event stream, or if any consumer may need to replay historical events, Kafka is the correct
choice. If each message has exactly one consumer and replay is unnecessary, RabbitMQ (or
a managed queue such as SQS) is operationally simpler and entirely sufficient.

---

## 4. Delivery Guarantees

Delivery guarantees describe what a messaging system promises about whether a message will
be delivered and how many times. The guarantee applies end-to-end: broker delivery to
consumer is only part of the story — what the consumer does with the message determines the
actual semantic.

| Guarantee | Meaning | Risk | When to use |
|---|---|---|---|
| **At-most-once** | Delivered zero or one times — a message may be lost | Possible message loss; no duplicates | Non-critical telemetry, metrics aggregation where occasional loss is acceptable |
| **At-least-once** | Delivered one or more times — retries on failure may produce duplicates | Possible duplicate delivery | The correct default — design consumers to be idempotent |
| **Exactly-once** | Delivered and processed exactly once, end-to-end | Hardest guarantee — usually requires idempotent consumer + broker-level deduplication | Financial transactions, inventory deductions, any operation where both loss and duplication are unacceptable |

**Practical guidance:** design consumers to be idempotent (processing the same message twice
produces the same outcome as processing it once) and build systems around at-least-once
delivery. "Exactly-once" broker-level claims mean "effectively exactly-once given an
idempotent consumer" — they are not a literal guarantee against all failure modes at the
application level. See `references/kafka.md` §5 for Kafka's specific transactional API.

---

## 5. Dead-Letter Queues (DLQ)

A DLQ captures messages that fail processing after N retries, preventing them from blocking
the main queue indefinitely or being silently dropped.

**Configuration:**
- Set a **max receive count** (SQS) or **max retry count** (Kafka, RabbitMQ). After exceeding
  the threshold, route the message to the DLQ instead of retrying.
- Kafka equivalent: dead-letter topic. See `references/kafka.md` §7 for the implementation.

**Operational requirement:** a DLQ that nobody monitors is equivalent to silently dropping
messages — the safety net only functions if there is an alert (CloudWatch alarm, PagerDuty
trigger) and an operational process (inspect, diagnose, fix root cause, replay or discard).
A DLQ without monitoring is false comfort.

**Common root causes for DLQ routing:**
- Malformed message schema that the consumer cannot parse
- Permanently unavailable downstream dependency (DB is down)
- Poison-pill message that deterministically crashes the consumer on every attempt
- Deserialization failure from a schema version mismatch (missing schema registry)

**SQS DLQ configuration (AWS CDK — TypeScript):**
```typescript
import { Queue } from "aws-cdk-lib/aws-sqs";
import { Duration } from "aws-cdk-lib";

const dlq = new Queue(this, "OrdersDLQ", {
  retentionPeriod: Duration.days(14),  // keep failed messages for investigation
});

const mainQueue = new Queue(this, "OrdersQueue", {
  deadLetterQueue: {
    queue: dlq,
    maxReceiveCount: 3,  // move to DLQ after 3 failed delivery attempts
  },
  visibilityTimeout: Duration.seconds(30),
});
```

---

## 6. Batch vs. Stream Processing

The choice between batch and stream processing is a latency vs. simplicity trade-off.

| Dimension | Batch Processing | Stream Processing |
|---|---|---|
| **Latency** | Minutes to hours — data accumulates, then a job runs on the full batch | Milliseconds to seconds — events processed continuously as they arrive |
| **Throughput efficiency** | High — amortizes per-record overhead across large batches | Lower per-event, but continuous |
| **Failure model** | Simple — rerun the failed batch on the same bounded input | Harder — out-of-order events, event-time vs processing-time, watermarks, stateful aggregation |
| **Reprocessing** | Straightforward — rerun the job on historical data | Requires retained log (Kafka) and stateful recovery |
| **Typical tools** | Apache Spark (batch mode), Apache Airflow DAGs, dbt, SQL on S3 (Athena) | Apache Flink, Kafka Streams, Spark Structured Streaming, Google Dataflow |
| **Best fit** | Daily/hourly reporting, large historical reprocessing, ETL pipelines where real-time is not required | Fraud detection, real-time dashboards, alerting, monitoring, data whose value decays quickly with delay |

### Lambda Architecture vs. Kappa Architecture

Two approaches to building systems that must handle both historical reprocessing and
real-time processing.

**Lambda architecture** (Nathan Marz, 2011):
Runs both a batch layer and a speed (stream) layer in parallel. The batch layer computes
accurate results on the full historical dataset on a schedule; the speed layer computes
approximate or incremental results in real-time; a serving layer merges both.

```
Data source → [Batch layer  (Spark, dbt)]  → Batch views  ─┐
           → [Speed layer  (Flink, Kafka)]  → Real-time views → Serving layer → Query
```

Pros: the batch layer produces the ground truth; the speed layer covers the gap until the
next batch run. Cons: every pipeline must be written and maintained twice — once for batch
semantics and once for streaming semantics. Schema changes require updates in two places.

**Kappa architecture** (Jay Kreps, 2014):
Uses the stream as the single source of truth. Reprocessing is performed by replaying the
retained event log from the beginning. No separate batch layer.

```
Data source → Kafka (durable log) → Stream processor (Flink / Kafka Streams) → Serving layer
                 ↑ replay from offset 0 for reprocessing
```

Pros: one codebase, one pipeline. Simpler to maintain and evolve. Cons: requires the
streaming engine to be efficient at historical replay at scale (Kafka's configurable retention
makes this practical). Complex historical aggregations may be slower to reprocess than a
dedicated batch job.

**When to choose each:** Lambda when the batch and stream computations are inherently
different (e.g., ML training on full history vs. real-time inference). Kappa when the
same transformation applies to both historical and real-time data — it is almost always
the right default for greenfield systems.
