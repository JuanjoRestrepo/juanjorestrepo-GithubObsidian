> Content in this file is based on UiPath's publicly documented architecture as published in
> the Databricks Engineering Blog and official UiPath/Databricks documentation (verified July
> 2026). This is not organization-specific to this team's Inchcape deployment; it is a
> reference architecture and integration pattern document. Performance metrics, latency figures,
> and delivery-guarantee statements are drawn from the published source; verify against the
> live article if this is being used for architecture review.

# UiPath + Databricks: Real-Time ETL Pipeline and Agent Integration

This reference covers two distinct integration layers between UiPath and Databricks:

1. **Event ingestion pipeline** — how UiPath processes its own platform events (Robotlogs,
   Maestro events, Job/Queue/Machine events) using Spark Structured Streaming on Azure
   Databricks, producing a data warehouse that drives UiPath Insights and Maestro analytics.
   Understanding this architecture is directly relevant to the RPA-to-Data-Engineering
   transition (see `data-engineering-transition.md`) because it is the same pattern applied to
   any high-volume operational event stream.

2. **Databricks Agent connector for Maestro** — how a Maestro agentic process calls a
   Databricks AI agent (deployed via Mosaic AI Model Serving) as an external participant in
   an automation workflow. Understanding this integration is relevant for designing agentic
   processes that incorporate ML inference, information extraction, or classification via a
   Databricks-hosted model.

---

## Part 1 — Real-Time Event Ingestion Pipeline

### 1.1 Why Streaming Architecture Matters for UiPath Products

Maestro and UiPath Insights both require timely data:

- **Maestro** is the orchestration layer for UiPath's agentic automation platform. It
  coordinates AI agents, robots, and human-in-the-loop steps in response to real-time events.
  Every routing decision Maestro makes depends on fast, accurate signal processing; a pipeline
  with 30-minute latency cannot support real-time agentic decision-making.
- **UiPath Insights** surfaces monitoring and analytics across automations: trend detection,
  ROI calculations, issue detection. Near-real-time data is a prerequisite for actionable
  alerting rather than retrospective reporting.

### 1.2 Previous Architecture: The Problem Being Solved

The prior setup maintained two independent pipelines for Robotlog events and a third for
Job/Queue/Machine events:

**Pipeline 1 — High latency, complex infrastructure (Robotlogs historical path)**

```
Robotlog Source Events
  --> Azure Blob (Avro)
  --> Azure Function: Parsing
  --> Azure Blob (Parquet)
  --> Azure Data Factory (Merging & Mapping)
  --> Historical Robotlogs table
```

**Pipeline 2 — Low latency, high cost (Robotlogs + Jobs real-time path)**

```
Robotlog Source Events + Job/Queue/Machine Source Events
  --> Transformer Azure Function (Parsing & Enriching)
  --> Azure Event Hub
  --> Ingestor Azure Function
  --> Azure Blob (JSON)
  --> Realtime Robotlogs table + Realtime Jobs/Queues/Machines table
```

Problems this created:

| Problem                                                                     | Impact                                                                                                  |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Batching pipeline introduced up to 30 minutes of latency                    | Unusable for Maestro real-time decisions                                                                |
| Real-time pipeline delivered faster data but at higher cost                 | Not economically sustainable at scale                                                                   |
| Separate ingestion and storage paths for historical vs. real-time Robotlogs | Data duplication, two schemas to maintain, inconsistent query results                                   |
| Multiple Azure Function-based ingestion components                          | Operational complexity: separate deployment, monitoring, scaling, and failure domains for each function |
| No unified delivery guarantee model                                         | Maestro required at-least-once; the prior pipelines had inconsistent guarantees                         |

### 1.3 Why Spark Structured Streaming on Databricks

The core requirement was a framework that handles high-throughput batch workloads and low-
latency real-time data without the operational overhead of separate pipeline components.

Spark Structured Streaming on Databricks satisfies this by treating real-time data as an
unbounded table. The same DataFrame API operations used in batch processing apply unchanged
to streaming data — there is no separate API to learn, no separate execution path to
maintain. The engine handles micro-batch scheduling, fault-tolerant checkpointing, and
exactly-once semantics at the framework level.

The additional operational advantage: Databricks Lakeflow Jobs (formerly Databricks Workflows)
orchestrates the streaming jobs with the same tooling used for batch ETL, so the operational
model is unified across both modes.

### 1.4 New Architecture: Unified Streaming Pipeline

The new architecture consolidates previously separate components into a single unified pipeline:

**Event sources:**

| Source category                     | Examples                                                                            |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| **Robotlog Source Events**          | Bot execution logs, activity-level messages, custom `Log Message` output            |
| **Maestro Source Events**           | Orchestration flow events, trigger activations, cross-process coordination          |
| **Job/Queue/Machine Source Events** | Job started/completed/faulted, queue item lifecycle, machine heartbeat/availability |

**Processing: Spark Structured Streaming jobs** running on Azure Databricks, performing four
sequential transformation stages (executed by the optimizer as a single fused DAG):

| Stage                     | Purpose                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Filtering**             | Drop events not required for downstream storage (health-check noise, internal system events)                       |
| **Flattening**            | Normalize nested JSON payloads to flat columnar form                                                               |
| **Parsing**               | Extract typed values from raw string fields (timestamps, numeric IDs, enum codes)                                  |
| **Joining and Enriching** | Join with reference data (process definitions, machine metadata, user/role data) to produce self-contained records |

**Orchestration:** Databricks Lakeflow Jobs coordinates job scheduling, dependency management,
and retry behavior across all streaming jobs.

**Output: Data warehouse — three logical table groups:**

| Table group              | Source                         |
| ------------------------ | ------------------------------ |
| Single Robotlogs table   | Robotlog events                |
| Maestro tables           | Maestro events                 |
| Job/Queue/Machine tables | Job, queue, and machine events |

The output tables are separated by source-event semantics rather than collapsed into a single
generic events table. This makes downstream querying substantially simpler — analysts query
the table whose schema matches their question.

### 1.5 Measured Performance Characteristics

| Metric                    | Value                  |
| ------------------------- | ---------------------- |
| Median end-to-end latency | ~27 seconds            |
| 95th-percentile latency   | ~51 seconds            |
| 99th-percentile latency   | ~72 seconds            |
| Throughput (load test)    | ~40,000 events/second  |
| Throughput scaling        | Linear with core count |

Latency is measured end-to-end: event generation in the UiPath platform to event being
queryable in the data warehouse. The dominant contributors are ingestion queue dwell time,
Spark micro-batch trigger interval, and Delta write commit. Reducing the trigger interval
(at the cost of more frequent, smaller micro-batches) is the primary lever for reducing
median latency.

### 1.6 How Spark Distributes the Work

Understanding the execution model is necessary for sizing clusters and diagnosing throughput
problems.

**Partitions** are the unit of parallelism. The event source is divided into partitions (one
per upstream partition in the source — e.g., one per Kafka/Event Hub partition). Each
partition is processed independently.

**Stages** are groups of operations that can execute without network shuffle. Stage boundaries
occur at wide dependencies (joins, aggregations, sorts where data from multiple partitions
must be co-located). Within a stage, operations are pipelined and applied in a single pass.

**Tasks** are the atomic unit: one task processes one partition within one stage. A TaskSet
is all tasks for a given stage, executing in parallel — one task per available executor core.

**Executors** are JVM processes on Worker Nodes. Each executor has a fixed core count and
memory allocation; each core runs one task at a time.

```
Partition --> Task --> Executor Core
Stage N completes --> Shuffle (wide dependency) --> Stage N+1 --> Executor Cores
```

This repeats on every micro-batch trigger. Throughput scales linearly with cores because
adding cores adds parallel tasks without changing any individual partition's processing logic.

**Note on the enrichment join:** the reference data being joined (process definitions, machine
metadata) is typically small enough for a broadcast join — Spark distributes a copy to every
executor rather than shuffling the event stream, eliminating the wide dependency entirely.

### 1.7 Key Engineering Principles

**Delivery guarantees: the path to exactly-once**

Spark Structured Streaming provides the mechanisms for exactly-once:

- Write-ahead logging (WAL) records each micro-batch's input offsets before processing,
  enabling recovery to a consistent point on failure.
- Checkpointing persists query state and progress to a durable store (ADLS, DBFS) so a
  restarted job resumes from the last committed offset.
- Idempotent sinks (keyed MERGE on a unique event ID into Delta tables) are the application-
  level requirement to close at-least-once to exactly-once.

UiPath's current implementation operates at **at-least-once** — events are not lost, but
a failure during a micro-batch write can cause some events to be reprocessed and written
twice. The stated roadmap is to implement idempotent sinks to achieve exactly-once. For
audit-trail or financial reconciliation use cases, implement idempotent sinks before going
to production; for dashboarding and trend analysis, deduplicate at query time
(`DISTINCT` or `QUALIFY ROW_NUMBER() = 1`).

**Raw data preservation**

Every output table persists a `rawMessage` column containing the complete raw event payload
as a string alongside all parsed, typed columns. Benefits:

- When a parsing bug, schema change, or unexpected value causes a downstream quality
  problem, the raw payload is available for re-parsing without re-ingesting from the source.
- Critical in streaming where re-reading historical source data may be unavailable (Event Hub
  retention limits, for example).
- Storage cost is low — columnar compression on a repeated-schema JSON string is efficient.

Apply this pattern to any RPA-driven data pipeline: store the raw extracted text or file
content in a `_raw` column alongside structured output. The storage cost is negligible;
the debugging cost savings are significant.

**DataFrame API over RDD**

| Dimension      | RDD API                                  | DataFrame API                                                               |
| -------------- | ---------------------------------------- | --------------------------------------------------------------------------- |
| Abstraction    | Specify how to compute, task by task     | Specify what to compute; Spark determines how                               |
| Optimizer      | None                                     | Catalyst optimizer + Tungsten execution engine                              |
| Schema         | Schema-free; errors surface at runtime   | Schema-enforced; errors surface at plan time                                |
| Expressiveness | Manual map/flatMap/reduceByKey chains    | SQL-equivalent: `select`, `filter`, `groupBy`, `join`                       |
| Debugging      | Trace individual transformation closures | `df.explain()` shows full physical plan                                     |
| Performance    | Manual partitioning and join strategy    | Adaptive Query Execution handles partition sizing, join strategy at runtime |

Use the DataFrame API for all new Spark development. RDD-level code is warranted only for
custom stateful operations the structured API cannot express — rare in event processing.

### 1.8 Operational Considerations

**Monitoring a Structured Streaming job**

| Metric                   | Healthy signal                      | Alert condition                                                   |
| ------------------------ | ----------------------------------- | ----------------------------------------------------------------- |
| `processedRowsPerSecond` | Stable, matches expected throughput | Sharp drop: source backlog or executor loss                       |
| `inputRowsPerSecond`     | Tracks source event rate            | Spike with flat processedRows: backpressure                       |
| Micro-batch duration     | Below trigger interval              | Consistently exceeds trigger interval: under-provisioned          |
| `numInputRows` per batch | Non-zero during active hours        | Extended zero: source connectivity issue                          |
| Failed/retried tasks     | Near zero                           | Sustained failures: OOM, executor eviction, or source read errors |

In Databricks, the Spark UI (accessible from the cluster's running jobs panel) provides all
of these plus shuffle read/write bytes, GC time, and per-stage timeline views. Databricks
Lakeflow Jobs surfaces job-level run history, retry counts, and duration trends.

**Schema evolution**

UiPath platform events change across product versions. Design the processing layer
defensively:

- Use `schema_of_json` + `from_json` with `PERMISSIVE` mode when parsing raw JSON payloads;
  unknown fields are silently dropped rather than causing a job failure.
- Use Delta Lake schema evolution (`mergeSchema = true`) to allow new columns to be added
  to output tables without DDL migrations — existing rows retain `null` for new columns.
- Never `SELECT *` from the raw stream in a production job; always select named columns
  explicitly so that source additions do not implicitly widen the output table schema.

**Throughput tuning**

If `processedRowsPerSecond` cannot keep pace with `inputRowsPerSecond` over a sustained period:

1. Increase cluster core count — throughput scales linearly.
2. Check `maxOffsetsPerTrigger` (Event Hub / Kafka source) — cap per-trigger input to
   prevent a burst from overwhelming a fixed-size cluster.
3. Check shuffle partitions (`spark.sql.shuffle.partitions`) — the default (200) is too high
   for small streaming micro-batches; tune to 2x the number of cores for streaming jobs.
4. Profile per-stage durations in the Spark UI — if the enrichment join stage dominates,
   check whether the broadcast join threshold (`spark.sql.autoBroadcastJoinThreshold`) needs
   tuning for the reference dataset size.

---

## Part 2 — Databricks Agent Connector for UiPath Maestro

### 2.1 Overview

The Databricks Agent connector is a UiPath Integration Service connector that enables a
Maestro agentic process to call a Databricks AI agent as an external participant. The agent
must be deployed via a Mosaic AI Model Serving endpoint in the Databricks workspace.

**Scope and availability:**

- Cloud only: supported on Databricks deployed to AWS, Google Cloud Platform, and Azure.
- Maestro exclusive: this integration is only available in workflows created in UiPath
  Maestro, using the **Start and Wait for External Agent** action type on a Service Task.
  It cannot be used in Studio REFramework or Power Automate workflows.
- The connector does not support events (no trigger/inbound webhook capability).

**Authentication:** OAuth or personal access token to the Databricks workspace. Full
step-by-step instructions at:
`docs.uipath.com/integration-service/automation-cloud/latest/user-guide/databricks-agent-authentication`

### 2.2 What "Agent" Means in this Context

A Databricks agent is any model or application deployed to a Mosaic AI Model Serving
endpoint that exposes a compatible API surface. This includes:

- LLM-based chat agents (LangChain, LlamaIndex, or any framework deployed via MLflow)
- Information extraction agents (document parsing, entity recognition)
- Classification agents (routing/categorization tasks)
- Custom Python applications deployed behind a serving endpoint

The requirement for Maestro integration: the agent must render its output in a structured
JSON schema that Maestro can parse and assign to process variables. Any agent can be prompted
to respond in a well-defined schema; information extraction agents in Databricks are a natural
fit because their output is already structured.

### 2.3 Activities

The connector exposes two activities:

**Query Serving Endpoint** (schema-assisted)

The activity retrieves the input and output schema from the selected serving endpoint,
auto-generating the request form in Maestro's Properties panel. Use this activity when:

- The serving endpoint is a standard Databricks-supported model type.
- You want Maestro to guide the request structure via the UI.

**Query Serving Endpoint (Manual)** (full JSON control)

The activity accepts the complete JSON payload manually and does not retrieve the endpoint
schema. Use this when:

- The auto-generated schema approach is unavailable for your model type.
- You need full control over the JSON payload (non-standard request shapes, extra headers).
- You are integrating with a custom or non-standard serving endpoint.

For manual invocation, the payload structure depends entirely on the serving endpoint.
For a chat-based model:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your prompt here"
    }
  ]
}
```

Test the payload directly in the Databricks workspace before integrating into a Maestro
process; the activity cannot surface schema errors at design time.

### 2.4 Maestro Integration Workflow

The full integration flow in Maestro:

1. Add a **Service Task** element to the Maestro process canvas.
2. In the Properties panel, set **Action** to `Start and wait for external agent`.
3. Select the **Databricks Agent** connector.
4. Select or create a connection (see authentication docs above).
5. Select the **Activity**: `Query serving endpoint` or `Query serving endpoint (Manual)`.
6. Select the **Serving Endpoint** from the list of endpoints in the connected workspace.
7. Compose the **Messages** input as an ARRAY of OBJECTs, each with `role` (string: `"user"`)
   and `content` (string: the prompt).
8. Assign the agent's output to a **process variable** for use in subsequent tasks or routing
   decisions.

**Example response structure** (from `Query serving endpoint`):

```json
{
  "id": "bf185700-c100-41be-9d4b-6a8aee2d8444",
  "databricks_output": {
    "databricks_request_id": "bf185700-c100-41be-9d4b-6a8aee2d8444"
  },
  "messages": [
    {
      "role": "assistant",
      "id": "run--38ced1fa-f810-49c2-87fc-e831e5ffb1d0-0",
      "content": "..."
    }
  ]
}
```

Access the agent's reply in the Maestro Expression editor:

```javascript
result.response.messages[0].content;
```

If the content is a JSON-encoded string (the agent was prompted to return structured JSON),
parse it explicitly:

```javascript
js: JSON.parse(result.response.messages[0].content);
```

Then assign individual fields from the parsed object to typed process variables.

### 2.5 Prompt Engineering for Maestro-Driven Agents

The agent's behavior at inference time is determined by two prompt layers:

| Layer             | Location                                                       | Responsibility                                                                         |
| ----------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **System prompt** | Defined in the Databricks agent configuration, not in Maestro  | Detailed instructions, output schema definition, domain knowledge, few-shot examples   |
| **User prompt**   | Composed in Maestro at runtime, passed via the `content` field | Brief and specific; provides the runtime variables the agent needs to perform the task |

Keep the user prompt minimal: its role is to supply the runtime values, not to re-explain
the task. Example (using C# string concatenation in Studio expressions to interpolate a
process variable):

```csharp
"What is the inventory quantity for Order ID " + vars.orderId_1 +
"? Respond only with a JSON object: {\"Order_Quantity\": <integer>}. No explanation."
```

Expected response:

```json
{ "Order_Quantity": 100 }
```

**Type handling.** Pay strict attention to types: a response that looks like JSON may be a
string of type `String` in Maestro, not a JSON object. Always use
`js:JSON.parse(result.response.messages[0].content)` when the agent returns a JSON-encoded
string, and assign the result to a variable of type **JSON** in Maestro before extracting
fields.

### 2.6 Connection Requirements

The Databricks Agent connector requires the following permission on the Databricks workspace
for the Query Serving Endpoint activity:

```
USE CATALOG permission for Catalog <catalog_name>
```

Grant this at the Unity Catalog level on the catalog containing the model's registered
assets. Without this permission, the activity cannot enumerate serving endpoints or retrieve
the endpoint schema (for the schema-assisted activity variant).

### 2.7 Designing the Agent for Maestro Consumption

The most reliable pattern for Maestro integration is **structured output from the agent's
system prompt**, not ad-hoc prompting in the Maestro user prompt. Design the agent to:

1. Always return a fixed JSON schema (no extra prose, no markdown fences, no "here is your
   answer:" preambles).
2. Version the schema explicitly if the agent's output contract may change — Maestro process
   variables are typed and will fail silently if the schema drifts.
3. For classification tasks (routing decisions in Maestro), return an enum value from a
   defined list rather than free text — free text requires a `Switch` with fuzzy matching,
   which is fragile.
4. For extraction tasks, return all extracted fields even when not found (return `null`
   rather than omitting the key) so the Maestro expression always resolves.

Output intended for human display (escalation reason text, a summary for a human-in-the-loop
step) can be natural language. Output consumed by subsequent automated tasks or robot
activities must be strictly typed.

---

## Part 3 — Relevance to the RPA-to-Data-Engineering Transition

The event ingestion pipeline (Part 1) is the real-world embodiment of the skills bridge
in `data-engineering-transition.md`:

| RPA concept                                    | Equivalent in the Databricks pipeline                                              |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| Queue item (Orchestrator)                      | Event Hub / Kafka message consumed by the Structured Streaming job                 |
| Transaction processing (REFramework Performer) | Micro-batch trigger processing a bounded set of events                             |
| BusinessException → item marked as failed      | Downstream routing: failed parse → `_raw` preserved, item flagged for reprocessing |
| Config.xlsx / Orchestrator Asset               | Spark job configuration parameters, `maxOffsetsPerTrigger`, cluster policy         |
| Dispatcher/Performer separation                | Producer (event source) / Consumer (Streaming job) separation                      |
| Retry mechanism (queue auto-retry)             | Kafka/Event Hub offset commitment strategy + WAL-based replay                      |
| Workflow Analyzer rule                         | Schema enforcement at parse time (`from_json` with PERMISSIVE mode)                |

**Practical next step for DE transition exposure:**

Instrument an existing UiPath process to emit structured log messages to an Azure Event Hub
(or a Kafka-compatible endpoint), build a minimal Spark Structured Streaming job on
Databricks to consume those messages and write them to a Delta table, and query the results
with Databricks SQL. This is the same end-to-end pattern as UiPath's production
implementation at manageable scale — it exercises Structured Streaming, Delta Lake writes,
Unity Catalog, and Lakeflow Jobs simultaneously.

---

## Sources Consulted

- Databricks Engineering Blog: "How UiPath Built a Scalable Real-Time ETL Pipeline on
  Databricks" (databricks.com/blog/how-uipath-built-scalable-real-time-etl-pipeline-databricks,
  verified July 2026) — primary source for the previous architecture diagram, new
  architecture description, performance metrics (latency, throughput), and delivery
  guarantee statement; all attributed figures are drawn from this published source.
- UiPath official documentation: Databricks Agent connector
  (docs.uipath.com/integration-service/automation-cloud/latest/user-guide, verified July 2026)
  — source for connector scope, authentication requirements, activity descriptions (Query
  Serving Endpoint and Query Serving Endpoint Manual), response structure examples, and
  prompt engineering guidance.
- UiPath official documentation: Databricks Agent activities
  (docs.uipath.com/activities/other/latest/integration-service/uipath-databricks-databricks-about,
  verified July 2026).
- UiPath official documentation: Introduction to Maestro
  (docs.uipath.com/maestro/automation-cloud/latest/user-guide/introduction-to-maestro).
- Apache Spark documentation: Structured Streaming Programming Guide
  (spark.apache.org/docs/latest/structured-streaming-programming-guide.html).
- Apache Spark documentation: SQL, DataFrames, and Datasets Guide
  (spark.apache.org/docs/latest/sql-programming-guide.html).
- Databricks documentation: Lakeflow Jobs (formerly Databricks Workflows); Mosaic AI Model
  Serving; Unity Catalog permissions (docs.databricks.com, verified July 2026).
- Delta Lake documentation: MERGE semantics, schema evolution, idempotent writes
  (delta.io/docs).
- Armbrust et al., "Spark SQL: Relational Data Processing in Spark" (SIGMOD 2015) — Catalyst
  optimizer and DataFrame API foundations.

The Databricks Agent connector feature set, Mosaic AI Model Serving endpoint requirements,
and Unity Catalog permission model are the sections of this file most likely to change across
product versions — verify against official docs.uipath.com and docs.databricks.com for any
new implementation.
