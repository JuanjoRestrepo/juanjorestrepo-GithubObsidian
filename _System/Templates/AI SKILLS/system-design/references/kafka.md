# Apache Kafka — Distributed Event Streaming

**Sources:** Apache Kafka official documentation (kafka.apache.org); Confluent documentation
(docs.confluent.io) — maintained by Kafka's original creators; Neha Narkhede, Gwen Shapira,
Todd Palino, *Kafka: The Definitive Guide* (O'Reilly, 2nd ed. 2021); Jay Kreps, Neha Narkhede,
Jun Rao, "Kafka: A Distributed Messaging System for Log Aggregation" (LinkedIn Engineering,
2011) — the original Kafka paper; Factor House, "Apache Kafka Architecture" (2026); Confluent
developer documentation on KRaft (Kafka 4.0 GA); Conduktor Kafka documentation (2026).

---

## 1. What Kafka Is (and Is Not)

**Kafka is a distributed, durable, replicated commit log.** It is not a message queue in the
traditional sense. The critical distinction:

| Traditional Message Queue (RabbitMQ, SQS) | Apache Kafka (Event Log) |
|---|---|
| Message deleted after consumption | Message retained for configurable period (default 7 days) |
| One consumer per message | Any number of independent consumer groups |
| No replay — consumed is consumed | Any consumer group can replay from any offset |
| Push-based delivery | Pull-based — consumers control their reading pace |
| Designed for task queues | Designed for event streaming and data pipelines |
| Lower throughput ceiling | Millions of messages/second throughput |
| Simpler to operate | Significant operational complexity |

Use Kafka when: you need fan-out (multiple systems consuming the same event stream), replay
capability (a new service needs historical data), high-throughput streaming (millions of
events/second), or event sourcing as the system of record.

Use a simpler queue (RabbitMQ, SQS, Azure Service Bus) when: a single consumer processes
each message, messages are transient tasks (not events), and the simpler operational model
is preferable.

---

## 2. Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Kafka Cluster                              │
│                                                                  │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │  Broker 1   │   │  Broker 2   │   │  Broker 3   │   ← brokers  │
│  └────────────┘   └────────────┘   └────────────┘              │
│        ↑                 ↑                 ↑                     │
│        └─────────────────┼─────────────────┘                    │
│                          │                                       │
│               ┌──────────────────┐                              │
│               │  KRaft Controller │  ← cluster metadata (Kafka 4.0) │
│               └──────────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
         ↑ produce                    ↓ consume
    Producers                    Consumer Groups
```

### Topics and Partitions

A **topic** is a named, ordered, durable stream of records. Every Kafka topic is divided into
one or more **partitions** — each partition is an ordered, immutable, append-only log stored
on disk.

```
Topic: "orders"
  Partition 0: [offset 0][offset 1][offset 2][offset 3] ← new records appended here
  Partition 1: [offset 0][offset 1][offset 2]
  Partition 2: [offset 0][offset 1][offset 2][offset 3][offset 4]
```

**Key properties of partitions:**
- **Ordering is guaranteed within a partition**, not across partitions. If you need all events
  for a given order to be processed in sequence, produce them to the same partition by setting
  the message key to the order ID (`hash(orderId) % numPartitions`).
- **Partitions are the unit of parallelism** — a topic with N partitions can be consumed by
  at most N consumers within a single consumer group simultaneously.
- **Partitions are replicated** for durability. Each partition has one **leader** (handles
  reads and writes) and zero or more **followers** (passive replicas). Replication factor 3
  is standard for production (tolerates 2 broker failures).
- **Kafka writes sequentially to disk** — disk I/O is sequential, not random. Sequential
  disk writes on modern SSDs are faster than random memory writes. This is how Kafka achieves
  high throughput despite persisting to disk.

### Offsets

An **offset** is a monotonically increasing integer assigned to each record within a
partition. Offsets are how Kafka tracks each consumer group's position:

```
Consumer group "analytics" has read up to offset 47 in partition 0.
Consumer group "notifications" has read up to offset 31 in partition 0.
Both are reading the same partition independently — neither affects the other.
```

Consumer lag = (log end offset) − (consumer committed offset). High lag means the consumer
is falling behind the producer. Monitor consumer lag as the primary operational metric for
consumer health.

### KRaft Mode — Kafka 4.0 (ZooKeeper Removed)

**Prior to Kafka 4.0**, Kafka required Apache ZooKeeper for cluster metadata management
(controller election, broker registration, topic configuration). ZooKeeper was a separate
operational dependency with its own quorum, monitoring, and failure modes.

**Kafka 4.0 (May 2026) made KRaft GA and removed ZooKeeper entirely.** KRaft
(Kafka Raft Metadata mode) is Kafka's own internal Raft consensus implementation for cluster
metadata. The controller role is now managed by a set of Kafka brokers designated as
controllers, using Raft for leader election.

Implications:
- Kafka 4.0+ clusters have no ZooKeeper dependency — simpler deployment and operation
- Controller failover is faster (seconds vs tens of seconds with ZooKeeper)
- New `consumer rebalance protocol` (GA in Kafka 4.0) eliminates the group leader —
  the broker-side coordinator handles assignments, reducing rebalance disruption

**If you're starting a new Kafka deployment in 2026, use Kafka 4.0+ in KRaft mode.**
For existing clusters, migration to KRaft is supported via a documented migration path.

---

## 3. Producers

A producer publishes records to Kafka topics. Key configuration decisions:

```python
# Python — confluent-kafka (the official Confluent Python client, maintained by Kafka's creators)
# uv add confluent-kafka

from confluent_kafka import Producer
import json

producer = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092,broker3:9092",

    # Durability vs latency trade-off:
    # acks=0: fire and forget — lowest latency, no durability guarantee
    # acks=1: leader confirms write — fast, but data loss if leader fails before replication
    # acks=all: all in-sync replicas confirm — highest durability, higher latency
    "acks": "all",

    # Retry configuration (applies only to retriable errors: network timeouts, leader election)
    "retries": 3,
    "retry.backoff.ms": 100,

    # Idempotent producer (Kafka 0.11+): prevents duplicate messages from retries
    # Requires acks=all and max.in.flight.requests.per.connection ≤ 5
    "enable.idempotence": True,

    # Batching: linger.ms delays sends to allow batching — increases throughput, adds latency
    "linger.ms": 5,
    "batch.size": 16384,       # bytes per batch
    "compression.type": "lz4", # compress batches — significant throughput improvement
})


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")


def produce_order_event(order_id: str, payload: dict) -> None:
    producer.produce(
        topic="orders",
        key=order_id.encode(),          # key determines partition — same order → same partition
        value=json.dumps(payload).encode(),
        callback=delivery_report,
    )
    producer.poll(0)  # trigger delivery callbacks — call frequently in production


producer.flush()  # wait for all outstanding messages to be delivered before exit
```

```typescript
// TypeScript — kafkajs (most popular Node.js Kafka client)
// pnpm add kafkajs

import { Kafka, CompressionTypes } from "kafkajs";

const kafka = new Kafka({
  clientId: "order-service",
  brokers: ["broker1:9092", "broker2:9092", "broker3:9092"],
  // SSL and SASL config for production:
  ssl: true,
  sasl: { mechanism: "plain", username: process.env.KAFKA_USER!, password: process.env.KAFKA_PASS! },
});

const producer = kafka.producer({
  idempotent: true,         // prevent duplicate messages from retries
  transactionalId: "order-service-producer",  // for exactly-once semantics
});

await producer.connect();

await producer.send({
  topic: "orders",
  compression: CompressionTypes.LZ4,
  messages: [
    {
      key: orderId,            // routes this message to a consistent partition
      value: JSON.stringify({ orderId, status: "created", amount }),
      headers: {
        "event-type": "order.created",
        "schema-version": "1",
        "source-service": "order-service",
      },
    },
  ],
});
```

---

## 4. Consumers and Consumer Groups

A **consumer group** is a set of consumers that cooperatively read from a topic. Kafka assigns
each partition to exactly one consumer within the group — enabling parallel processing without
duplicate processing within the group.

```
Topic: "orders" (3 partitions)     Consumer Group: "notifications-service"
  P0 ──────────────────────────────▶ Consumer Instance 1
  P1 ──────────────────────────────▶ Consumer Instance 2
  P2 ──────────────────────────────▶ Consumer Instance 3

Consumer Group: "analytics-service" (reads the SAME topic, independently)
  P0 ──────────────────────────────▶ Consumer Instance A
  P1 ──────────────────────────────▶ Consumer Instance B (reads own offset — not affected by notifications-service)
  P2 ──────────────────────────────▶ Consumer Instance C
```

**Scaling rule:** max parallelism = number of partitions. If you add a 4th consumer
instance to a group reading 3 partitions, one instance is idle. If you have 10 partitions,
10 consumer instances can read in parallel. **Size your topic partition count based on
your expected consumer parallelism.**

```python
from confluent_kafka import Consumer, KafkaError
import json

consumer = Consumer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "group.id": "notifications-service",

    # auto.offset.reset: what to do when the group has no committed offset
    # latest: start from the newest messages (skip historical)
    # earliest: start from the beginning of the log (replay all history)
    "auto.offset.reset": "earliest",

    # Disable auto-commit — commit manually after successful processing
    # Auto-commit can cause loss (committed before processing) or duplicates (committed but processing failed)
    "enable.auto.commit": False,
})

consumer.subscribe(["orders"])

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue  # end of partition — not an error, just caught up
            raise KafkaError(msg.error())

        event = json.loads(msg.value())
        try:
            process_order_event(event)
            # Only commit AFTER successful processing
            consumer.commit(message=msg, asynchronous=False)
        except Exception as e:
            # Do not commit — message will be redelivered after consumer restart
            # Implement dead-letter topic for poison messages that repeatedly fail
            handle_processing_failure(msg, e)

finally:
    consumer.close()  # always close cleanly — triggers graceful partition reassignment
```

```typescript
// TypeScript consumer
const consumer = kafka.consumer({ groupId: "notifications-service" });
await consumer.connect();
await consumer.subscribe({ topic: "orders", fromBeginning: true });

await consumer.run({
  // eachMessage is called once per message — auto-commits after return by default
  // For manual commit, set autoCommit: false and call consumer.commitOffsets()
  eachMessage: async ({ topic, partition, message }) => {
    const event = JSON.parse(message.value!.toString());
    await processOrderEvent(event);
    // kafkajs auto-commits after eachMessage resolves — ensure processing is truly complete
  },
});
```

### Rebalancing — The Operational Pain Point

When a consumer joins or leaves a group, Kafka triggers a **rebalance** — it reassigns
partitions among the remaining consumers. During a rebalance, all consumption in the group
stops. Long rebalances (caused by slow `max.poll.interval.ms` or large groups) are a common
production performance issue.

**Mitigations:**
- **Cooperative sticky rebalancing** (default since Kafka 2.4): only partitions that need
  to move are revoked, not all partitions. Minimizes pause duration.
- **Static membership** (`group.instance.id`): consumers with a static ID don't trigger a
  rebalance when they restart (within `session.timeout.ms`). Ideal for containerized
  environments where pod restarts are frequent.
- Tune `session.timeout.ms` (how long before a silent consumer is considered dead) and
  `max.poll.interval.ms` (how long processing a single batch can take) appropriately for
  your workload.

---

## 5. Delivery Semantics

Kafka supports three delivery semantics, configured via producer and consumer settings:

| Semantic | Configuration | Trade-off |
|---|---|---|
| **At-most-once** | `acks=0` or `enable.auto.commit=true` without processing guarantee | Messages may be lost; never duplicated |
| **At-least-once** | `acks=all` + manual commit after processing | No loss; duplicates possible on failure + retry |
| **Exactly-once** | Idempotent producer + transactional API (`transactional.id`) | No loss, no duplicates; significant complexity; Kafka-to-Kafka only natively |

**In practice:** at-least-once with idempotent consumers is the correct default. Make your
consumer logic idempotent (using a processed-event deduplication table or Redis SET NX, as
in `api-engineering/references/resilience-patterns.md`) rather than incurring the complexity
of Kafka's transactional API.

Exactly-once is only truly achievable end-to-end when both the source and destination are
Kafka topics. "Exactly-once" to an external system (database, REST API) requires application-
level idempotency — Kafka cannot guarantee what happens outside its own log.

---

## 6. Kafka Streams — Stream Processing in the Application Layer

Kafka Streams is a client library (not a separate cluster) for building stream processing
applications that read from and write to Kafka topics. No separate Flink or Spark cluster
required.

```java
// Java — Kafka Streams DSL (the primary language for Kafka Streams)
StreamsBuilder builder = new StreamsBuilder();

KStream<String, Order> orders = builder.stream("orders");

// Filter, transform, aggregate — all expressed as a DSL
KStream<String, Notification> notifications = orders
    .filter((key, order) -> order.getStatus().equals("SHIPPED"))
    .mapValues(order -> new Notification(order.getCustomerId(), "Your order shipped!"));

notifications.to("notifications");

KafkaStreams streams = new KafkaStreams(builder.build(), config);
streams.start();
```

For Python/TypeScript use cases, Flink (with Python DataStream API) or simple consumer loops
with Redis for state are more practical than the Java-native Kafka Streams.

---

## 7. Operational Concerns

**Consumer lag monitoring** — the most important Kafka operational metric:
```bash
# Check lag for all consumer groups
kafka-consumer-groups.sh --bootstrap-server broker:9092 \
  --describe --group notifications-service

# Output shows: TOPIC, PARTITION, CURRENT-OFFSET, LOG-END-OFFSET, LAG
# LAG = LOG-END-OFFSET - CURRENT-OFFSET
# Growing lag = consumer can't keep up with producer
```

**Retention configuration:**
```properties
# Topic-level retention (override cluster default)
kafka-configs.sh --bootstrap-server broker:9092 --entity-type topics \
  --entity-name orders --alter \
  --add-config retention.ms=604800000   # 7 days in ms
               retention.bytes=10737418240  # 10 GB (whichever limit hit first)
```

**Replication factor and min.insync.replicas:**
```properties
# Cluster default (broker configuration)
default.replication.factor=3        # 3 replicas per partition
min.insync.replicas=2               # with acks=all, at least 2 replicas must confirm
                                    # this tolerates 1 broker failure without blocking writes
```

**Dead-letter topic pattern** — messages that repeatedly fail processing should be sent to a
dedicated dead-letter topic rather than blocking the consumer indefinitely:
```python
MAX_RETRIES = 3

async def process_with_dlq(msg, consumer, dlq_producer):
    attempts = int(msg.headers().get("retry-count", 0))
    try:
        await process(msg)
        consumer.commit(message=msg, asynchronous=False)
    except Exception:
        if attempts >= MAX_RETRIES:
            dlq_producer.produce("orders-dlq", key=msg.key(), value=msg.value(),
                headers={"original-topic": msg.topic(), "failure-reason": str(e)})
        else:
            dlq_producer.produce(msg.topic(), key=msg.key(), value=msg.value(),
                headers={"retry-count": str(attempts + 1)})
```

---

## 8. When NOT to Use Kafka

Kafka has significant operational complexity — a Kafka cluster requires planning around
broker count, partition sizing, replication factor, consumer group management, schema
registry, and monitoring. Justify it explicitly before adopting it.

- **A single consumer processes each message** — use SQS, RabbitMQ, or Azure Service Bus;
  no replay needed = no reason to pay Kafka's overhead
- **Low message volume** (< 10K messages/day) — SQS is operationally trivial; Kafka is not
- **Simple request/response** — use REST or gRPC; Kafka is not a request/response transport
- **You need a fully managed, zero-ops message queue** — AWS SQS/SNS, Google Pub/Sub, and
  Azure Service Bus are dramatically simpler to operate for teams without Kafka expertise
- **The team has no prior Kafka experience** — the learning curve is steep; consumer group
  rebalancing, partition sizing, offset management, and schema evolution all have sharp edges;
  consider Confluent Cloud (managed Kafka) to reduce operational burden if you need the
  streaming capability

**Managed alternatives to self-hosted Kafka:**
- **Confluent Cloud** — managed Kafka by Kafka's creators; closest to self-hosted feature set
- **Amazon MSK** — managed Kafka on AWS; good for AWS-native architectures
- **Redpanda** — Kafka-compatible protocol, written in C++, dramatically lower latency and
  simpler to operate; no JVM, no ZooKeeper, no KRaft required
- **WarpStream** — Kafka-compatible, built on object storage (S3); near-zero operational cost
