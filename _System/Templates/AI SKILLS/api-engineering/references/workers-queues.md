# Workers & Job Queues — Async Processing Outside the Request-Response Cycle

**Sources:** BullMQ official documentation (bullmq.io) and BullMQ 5.71 release notes
(March 2026) — OpenTelemetry support, FlowProducer DAG jobs; Celery official documentation
(docs.celeryq.dev), Celery 5.6.x (Python 3.9–3.13, PyPy 3.10+, dropped 3.8); Valentín
Torassa, "Workers & Queues en Backend" (UAI Facultad de Tecnología Informática, 2025);
DEV Community, "Background Job Processing in Node.js: BullMQ, Queues, and Worker Patterns"
(March 2026); OneUptime Engineering Blog, "How to Build a Job Queue in Python with Celery
and Redis" (January 2025); DEV Community, "Celery + Redis at Scale" (April 2026).

---

## 1. The Bottleneck Problem — Why You Need Workers

Any operation in your API that takes longer than ~200ms should not be executed synchronously
inside the request-response cycle. Common examples:

```
Sending an email via SMTP:    200ms–3s
Sending a transactional SMS:  300ms–2s
Resizing an uploaded image:   500ms–5s
Calling a third-party API:    100ms–2s (with network variance)
Generating a PDF report:      1s–30s
Processing a webhook payload: 50ms–500ms
Running ML inference:         100ms–10s
```

The naive implementation blocks the HTTP thread until the operation completes:

```typescript
// ❌ WRONG — blocks the request cycle; fails under load
app.post("/users/register", async (req, res) => {
  const user = await db.user.create({ data: req.body });
  await emailService.sendWelcomeEmail(user.email);  // can take 2–3s
  res.json({ userId: user.id });  // user waits for the email to send
});
```

Under load, slow operations cascade: if email sending takes 2s and you receive 100
requests/sec, your server needs 200 threads active simultaneously just for email — a single
saturated dependency takes down the entire API.

The correct pattern:

```typescript
// ✅ CORRECT — return 202 immediately, process asynchronously
app.post("/users/register", async (req, res) => {
  const user = await db.user.create({ data: req.body });
  await emailQueue.add("send-welcome", { userId: user.id, email: user.email });
  res.status(202).json({ userId: user.id });  // response in <10ms regardless of email speed
});

// Worker process (separate deployment unit):
const emailWorker = new Worker("email", async (job) => {
  await emailService.sendWelcomeEmail(job.data.email);
}, { connection });
```

**The 202 pattern** — HTTP 202 Accepted signals "the request was received and will be
processed" without implying completion. Include a way for the client to check status:

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
Location: /jobs/abc-123/status

{ "jobId": "abc-123", "status": "queued" }
```

---

## 2. Architecture — How Workers and Queues Fit Together

```
                        ┌────────────────────┐
Client ──▶ API Server ──▶│     Job Queue       │◀── (Redis as backing store)
                        │  (BullMQ / Celery)  │
                        └────────┬───────────┘
                                 │  distributes jobs
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Worker 1  │ │ Worker 2  │ │ Worker 3  │  (separate processes)
              └──────────┘ └──────────┘ └──────────┘
                    │            │            │
                    ▼            ▼            ▼
              Database / External APIs / Third-Party Services
```

**Key properties of this architecture:**

- **API stays fast** — the API process only enqueues a job (a Redis write: ~0.5ms) and
  returns. It is completely decoupled from the processing time.
- **Workers scale independently** — add more worker instances when queue depth grows; scale
  them down during quiet periods. Workers can run on cheaper compute than the API.
- **Failure isolation** — a crashed worker does not crash the API. The job remains in the
  queue and will be picked up by another worker after a configurable timeout.
- **Traffic spike absorption** — burst of 10,000 requests enqueues 10,000 jobs; workers
  process them at their own steady rate without overloading downstream services.

---

## 3. BullMQ — Node.js/TypeScript Job Queue (Production Standard, 2026)

BullMQ is the de-facto standard job queue for Node.js in 2026, the successor to Bull
(complete rewrite: TypeScript-first, improved concurrency control, more reliable job state
machine, FlowProducer for DAG-style job dependencies). <cite index="8-1">BullMQ 5.71 (March 2026)
added OpenTelemetry telemetry support, flow producers for DAG-style job dependencies,
rate limiting, priority queues, and dead letter queue patterns.</cite>

```bash
pnpm add bullmq ioredis
```

### Queue + Worker — Full Production Setup

```typescript
// src/queues/connection.ts — shared Redis connection
import { Redis } from "ioredis";

export const redisConnection = new Redis(process.env.REDIS_URL!, {
  maxRetriesPerRequest: null,  // required by BullMQ — disables ioredis auto-retry interference
  enableReadyCheck: false,
});

// src/queues/email.queue.ts — queue definition (used by API to enqueue jobs)
import { Queue } from "bullmq";
import { redisConnection } from "./connection";

export const emailQueue = new Queue("email", {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 5,                        // retry up to 5 times on failure
    backoff: { type: "exponential", delay: 2000 }, // 2s, 4s, 8s, 16s, 32s
    removeOnComplete: { count: 1000 },  // keep last 1000 completed jobs for inspection
    removeOnFail: { count: 5000 },      // keep last 5000 failed jobs for debugging
  },
});

// API route — enqueue without blocking
app.post("/users/register", async (req, res) => {
  const user = await db.user.create({ data: req.body });

  const job = await emailQueue.add(
    "send-welcome",
    { userId: user.id, email: user.email, name: user.name },
    {
      // Override per-job if needed:
      priority: 1,           // lower number = higher priority
      delay: 0,              // process immediately
      jobId: `welcome-${user.id}`,  // deduplicate — same jobId won't be added twice
    },
  );

  res.status(202).json({ userId: user.id, jobId: job.id });
});
```

```typescript
// src/workers/email.worker.ts — SEPARATE PROCESS from the API
import { Worker, Job } from "bullmq";
import { redisConnection } from "../queues/connection";

interface WelcomeEmailPayload {
  userId: string;
  email: string;
  name: string;
}

const worker = new Worker<WelcomeEmailPayload>(
  "email",
  async (job: Job<WelcomeEmailPayload>) => {
    // Idempotency check — if this job ran before (retry), don't double-send
    const alreadySent = await db.emailLog.findUnique({
      where: { jobId: job.id },
    });
    if (alreadySent) {
      console.log(`Job ${job.id} already processed — skipping`);
      return;
    }

    await emailService.sendWelcome(job.data.email, job.data.name);

    await db.emailLog.create({ data: { jobId: job.id!, userId: job.data.userId } });
  },
  {
    connection: redisConnection,
    concurrency: 10,    // process up to 10 jobs simultaneously in this worker process
    limiter: {
      max: 100,         // max 100 jobs per duration per worker instance
      duration: 60000,  // per minute — respects external service rate limits
    },
  },
);

worker.on("completed", (job) => console.log(`Job ${job.id} completed`));
worker.on("failed", (job, err) => console.error(`Job ${job?.id} failed:`, err));
```

### Job Types — Delayed, Scheduled, Priority, Flow

```typescript
// Delayed job — process after a delay
await emailQueue.add(
  "trial-expiry-reminder",
  { userId },
  { delay: 7 * 24 * 60 * 60 * 1000 },  // 7 days from now
);

// Recurring cron job (scheduler — replaces deprecated repeat option)
await emailQueue.upsertJobScheduler(
  "daily-digest",        // scheduler name (unique key)
  { pattern: "0 9 * * *" },  // cron: every day at 9 AM UTC
  { name: "daily-digest", data: {} },
);

// Priority queue — lower number = higher priority
await emailQueue.add("password-reset", { email }, { priority: 1 });  // urgent
await emailQueue.add("newsletter",     { email }, { priority: 10 }); // bulk

// FlowProducer — DAG of dependent jobs (child jobs run in parallel, parent waits for all)
import { FlowProducer } from "bullmq";
const flow = new FlowProducer({ connection: redisConnection });

await flow.add({
  name: "publish-video",
  queueName: "video",
  data: { videoId },
  children: [
    { name: "extract-audio",       queueName: "audio",    data: { videoId } },
    { name: "generate-thumbnails", queueName: "images",   data: { videoId } },
    // Both children run in parallel; parent runs only after both complete
  ],
});
```

### Dead-Letter Queue Pattern

<cite index="8-1">BullMQ doesn't have a built-in dead letter queue — implement one with the `failed` event.</cite>

```typescript
const dlqQueue = new Queue("dead-letter", { connection: redisConnection });

worker.on("failed", async (job, err) => {
  if (job && job.attemptsMade >= job.opts.attempts!) {
    // Job exhausted all retries — move to DLQ for manual inspection
    await dlqQueue.add("failed-job", {
      originalQueue: "email",
      jobId: job.id,
      jobData: job.data,
      failureReason: err.message,
      failedAt: new Date().toISOString(),
    });
    // Alert your team:
    await alertService.send(`Job ${job.id} in queue 'email' permanently failed: ${err.message}`);
  }
});
```

### Critical Production Mistakes

```
❌ Running workers inside the API process
   Worker crashes take down your API. Always separate processes/containers.

❌ No removeOnComplete TTL
   Every completed job stays in Redis forever. At 10K jobs/day → gigabytes within weeks.
   Always set: removeOnComplete: { count: 1000 } or { age: 86400 }

❌ Non-idempotent job processors
   If a job runs twice (retry after timeout), it must not send two emails or charge twice.
   Use a deduplication check (jobId lookup in DB) at the start of every processor.

❌ Missing dead-letter handling
   When a job exhausts all retries, log it, alert on it, move it to a DLQ.
   Jobs silently disappearing into the failed set is a data loss event.
```

---

## 4. Celery — Python Distributed Task Queue (Production Standard)

<cite index="12-1">Celery is the de facto standard for distributed task processing in Python, handling millions of tasks per day at companies like Instagram, Mozilla, and Robinhood.</cite> <cite index="15-1">Celery 5.6.x supports Python 3.9 through 3.13 and PyPy 3.10+. Support for Python 3.8 was dropped as it reached end-of-life in October 2024.</cite>

```bash
uv add "celery[redis]>=5.6" redis
```

**Broker vs Result Backend** — two distinct responsibilities:
- **Broker** (Redis/RabbitMQ): transports task messages from producers (your API) to workers
- **Result backend** (Redis/PostgreSQL): stores task return values so callers can retrieve them

```
FastAPI → Redis (Broker) → Celery Worker → Redis (Result Backend) → FastAPI (optional result fetch)
```

### Full Production Setup

```python
# app/celery.py — Celery application factory
import os
from celery import Celery

celery_app = Celery("myapp")

celery_app.conf.update(
    # Broker and backend — Redis for both in most setups
    broker_url=os.environ["REDIS_URL"],
    result_backend=os.environ["REDIS_URL"],

    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Reliability — these three settings together make Celery safe for critical tasks
    task_acks_late=True,           # acknowledge AFTER processing, not before
    task_reject_on_worker_lost=True,  # re-queue if worker dies mid-task
    worker_prefetch_multiplier=1,  # take one task at a time — prevents worker hoarding

    # Concurrency
    worker_concurrency=int(os.getenv("CELERY_CONCURRENCY", "8")),

    # Memory management — prevent workers from leaking memory indefinitely
    worker_max_tasks_per_child=1000,     # restart worker process after 1000 tasks
    worker_max_memory_per_child=200_000, # restart if worker exceeds 200 MB

    # Timeouts
    task_soft_time_limit=300,  # raises SoftTimeLimitExceeded after 5 min — handle gracefully
    task_time_limit=600,       # hard kill after 10 min

    # Result expiry
    result_expires=86400,      # clean up results after 24 hours

    # Priority queues
    task_queues={
        "high":    {"exchange": "high",    "routing_key": "high"},
        "default": {"exchange": "default", "routing_key": "default"},
        "low":     {"exchange": "low",     "routing_key": "low"},
    },
    task_default_queue="default",
)
```

```python
# app/tasks/email_tasks.py — task definitions
from app.celery import celery_app
from app.services.email import EmailService
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task(
    name="tasks.send_welcome_email",
    bind=True,
    max_retries=5,
    queue="high",            # route to high-priority workers
    acks_late=True,
)
def send_welcome_email(self, user_id: str, email: str, name: str) -> dict:
    """Send welcome email — idempotent: safe to retry."""
    try:
        # Idempotency check
        from app.models import EmailLog
        if EmailLog.objects.filter(task_id=self.request.id).exists():
            logger.info(f"Task {self.request.id} already processed — skipping")
            return {"status": "skipped", "reason": "already_sent"}

        EmailService().send_welcome(email, name)

        EmailLog.objects.create(task_id=self.request.id, user_id=user_id)
        return {"status": "sent", "email": email}

    except Exception as exc:
        logger.error(f"Failed to send welcome email to {email}: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)  # exponential backoff
```

```python
# FastAPI route — enqueue without blocking
from fastapi import APIRouter
from app.tasks.email_tasks import send_welcome_email

router = APIRouter()

@router.post("/users/register", status_code=202)
async def register(payload: RegisterPayload, db: DBSession) -> dict:
    user = await user_service.create(db, payload)

    # .delay() enqueues and returns immediately — does NOT wait for execution
    task = send_welcome_email.delay(
        user_id=str(user.id),
        email=user.email,
        name=user.name,
    )

    return {"userId": str(user.id), "taskId": task.id}


# Optional: status endpoint so clients can poll for completion
@router.get("/tasks/{task_id}/status")
async def task_status(task_id: str) -> dict:
    from celery.result import AsyncResult
    result = AsyncResult(task_id, app=celery_app)
    return {
        "taskId": task_id,
        "status": result.status,          # PENDING, STARTED, SUCCESS, FAILURE, RETRY
        "result": result.result if result.ready() else None,
    }
```

**Starting workers:**
```bash
# Development — single worker
celery -A app.celery worker --loglevel=info

# Production — separate workers per priority, tuned concurrency
celery -A app.celery worker -Q high    --concurrency=4  --loglevel=warning
celery -A app.celery worker -Q default --concurrency=8  --loglevel=warning
celery -A app.celery worker -Q low     --concurrency=2  --loglevel=warning

# I/O-bound tasks (HTTP calls, email) — gevent for high concurrency without threads
celery -A app.celery worker --pool=gevent --concurrency=100

# CPU-bound tasks (image processing, ML) — use process pool, match CPU count
celery -A app.celery worker --pool=prefork --concurrency=4
```

**Flower — Celery monitoring dashboard:**
```bash
uv add flower
celery -A app.celery flower --port=5555
# → http://localhost:5555 — live worker status, queue depth, task history
```

---

## 5. Scaling Workers

Workers scale independently from the API — this is the key operational advantage of the
decoupled architecture.

**Horizontal scaling (most common):**
```yaml
# docker-compose.yml — scale workers without touching API
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    replicas: 3

  worker-high:
    build: .
    command: celery -A app.celery worker -Q high --concurrency=4
    replicas: 2    # scale independently

  worker-default:
    build: .
    command: celery -A app.celery worker -Q default --concurrency=8
    replicas: 4    # more workers for the default queue
```

**Autoscaling on queue depth (Kubernetes HPA):**

<cite index="2-1">Kubernetes HPA can scale workers based on BullMQ queue depth, configured via an External metric targeting average queue depth — e.g., scale when more than 50 jobs are waiting.</cite>

```yaml
# Scale workers when more than 50 jobs are waiting in the queue
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: email-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: email-worker
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: bullmq_queue_waiting   # exposed via Prometheus + KEDA
          selector:
            matchLabels:
              queue: email
        target:
          type: AverageValue
          averageValue: "50"
```

---

## 6. Concurrency — Choosing the Right Model

| Workload type | Characteristics | Recommended model |
|---|---|---|
| **I/O-bound** (email, HTTP calls, DB writes) | Spends time waiting for external responses | Async workers / gevent (Celery) / high BullMQ concurrency |
| **CPU-bound** (image processing, ML, PDF) | Spends time on computation | Process pool / Node.js worker_threads |
| **Mixed** | Some I/O, some CPU | Separate queues per type with appropriate worker pools |

```typescript
// BullMQ + Node.js worker_threads for CPU-bound jobs
import { Worker as BullWorker } from "bullmq";
import { Worker as NodeWorker } from "worker_threads";

const imageWorker = new BullWorker("image-processing", async (job) => {
  return new Promise((resolve, reject) => {
    // Spawn a worker thread — does not block the Node.js event loop
    const thread = new NodeWorker("./image-processor.worker.js", { workerData: job.data });
    thread.on("message", resolve);
    thread.on("error", reject);
  });
}, { connection, concurrency: 2 }); // 2 concurrent threads per worker process
```

---

## 7. Monitoring and Observability

**Key metrics to track (alert on these):**

| Metric | What it signals |
|---|---|
| Queue depth (waiting jobs) | Workers can't keep up — scale up or a downstream service is slow |
| Consumer lag (BullMQ) | Same as queue depth — growing lag = trouble |
| Job failure rate | External service down, code bug, or bad data |
| Job processing time (p95) | Upstream slowdown or resource contention |
| Worker memory (RSS) | Memory leak in job processor — tune `worker_max_memory_per_child` |

**BullMQ with OpenTelemetry (BullMQ 5.71+):**
```typescript
// Distributed tracing — trace from HTTP request through to job completion
import { trace } from "@opentelemetry/api";
import { BullMQInstrumentation } from "@opentelemetry/instrumentation-bullmq";
// Automatically traces: job.add, job.process, job.complete, job.fail
```

**Celery with Flower + Prometheus:**
```python
# Celery signals — emit metrics on task events
from celery.signals import task_success, task_failure
from prometheus_client import Counter, Histogram

TASKS_COMPLETED = Counter("celery_tasks_completed", "...", ["task_name"])
TASK_DURATION   = Histogram("celery_task_duration_seconds", "...", ["task_name"])

@task_success.connect
def on_success(sender=None, **kwargs):
    TASKS_COMPLETED.labels(task_name=sender.name).inc()
```

---

## 8. Orchestration vs Choreography at the Worker Level

*(Full architectural treatment in `software-architecture/references/microservices-monolith.md`
— Sam Newman section. This covers the practical worker-level implementation.)*

**Orchestration (central controller enqueues all steps):**
```typescript
// Order processing orchestrator — enqueues steps sequentially
async function processOrder(orderId: string) {
  await inventoryQueue.add("reserve",  { orderId });  // step 1
  await paymentQueue.add("charge",     { orderId });  // step 2 (after step 1)
  await shippingQueue.add("schedule",  { orderId });  // step 3 (after step 2)
}
// Visibility: the orchestrator sees all steps. Single point of control.
// Risk: orchestrator failure blocks all steps.
```

**Choreography (each worker publishes events for the next):**
```typescript
// Inventory worker — publishes event, Payment worker subscribes
const inventoryWorker = new Worker("inventory", async (job) => {
  await reserveStock(job.data.orderId);
  await paymentQueue.add("charge", { orderId: job.data.orderId });  // triggers next step
});

const paymentWorker = new Worker("payment", async (job) => {
  await chargePayment(job.data.orderId);
  await shippingQueue.add("schedule", { orderId: job.data.orderId });
});
// No central controller. More resilient. Harder to trace end-to-end.
```

**For complex, long-running workflows** (multi-day approval chains, saga with compensations):
use a dedicated workflow engine — **Temporal** (open-source, TypeScript and Python SDKs) or
**AWS Step Functions** (managed, no infrastructure). These provide durable execution,
built-in retry, timeout, and saga compensation — far more robust than hand-rolled queue
chains for workflows with many steps or long lifetimes.

---

## 9. When NOT to Use Workers

- **The operation is fast** (<200ms, simple DB write, synchronous computation) — the queue
  overhead and async complexity is not justified
- **The caller needs the result immediately** — if the user must wait for the response anyway
  (e.g., calculating a total at checkout), async processing provides no benefit; keep it
  synchronous
- **You have no Redis infrastructure** — simple AWS Lambda + SQS, or a database-backed queue
  (PostgreSQL `SKIP LOCKED` pattern), may be operationally simpler for low volume
- **The operation must complete in the same transaction** — database operations that must
  be atomic with the triggering write should stay synchronous within the transaction, not
  be dequeued (use the Transactional Outbox pattern from `api-engineering/gateway-integration.md`
  when you need to bridge a transaction boundary)
