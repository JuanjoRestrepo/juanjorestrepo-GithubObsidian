# RPA Developer to Data Engineer — Transition Bridge

For an RPA developer planning a transition into data engineering. Maps what already transfers
directly, identifies the real gaps, and gives a concrete learning sequence. Complements a
dedicated data-engineering/data-science skill for deep technical depth on any single topic below —
this file focuses on the bridge itself: how the two disciplines overlap, and how to close the gap
efficiently rather than starting from zero.

## Why This Transition Is Natural, Not a Restart

RPA and data engineering are both, structurally, "move data reliably from A to B, at scale,
without a human watching it run." The mental models transfer directly even though the tools
differ:

| RPA concept                                                   | Data engineering equivalent                                                                    |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Queue + Transaction (Orchestrator, Dispatcher/Performer)      | Pipeline task/DAG run + partition/batch                                                        |
| REFramework Init -> Get Transaction -> Process -> Set Status  | Extract -> Transform -> Load (ETL) / Extract -> Load -> Transform (ELT) stage sequence         |
| Config.xlsx / Orchestrator Assets (never hardcoded)           | Pipeline parameters, environment variables, Airflow Variables/Connections                      |
| Business Exception vs. System Exception                       | Data quality failure (bad row, schema drift) vs. infrastructure failure (source down, network) |
| Idempotency (safe to re-run a transaction after crash)        | Idempotent pipeline runs (safe to re-run a DAG/task without duplicating rows)                  |
| Selector fragility when the target UI changes                 | Schema drift when an upstream source changes its structure                                     |
| Orchestrator dashboards / queue item age monitoring           | Pipeline observability: DAG run status, data freshness/SLA monitoring                          |
| Git + Azure Pipelines CI/CD for bot code                      | Git + CI/CD for pipeline code (dbt, Airflow DAGs, Python transforms) — identical discipline    |
| SQL Server direct integration (already a core RPA skill here) | The relational/warehouse layer data engineers write against constantly                         |

The exception-handling discipline, the "never hardcode config/credentials" discipline, the
idempotency discipline, and the CI/CD discipline in this skill's Cross-Cutting Best Practices
section are not RPA-specific — they are data-engineering best practices under different names.
That is the strongest part of the transition story, and it is true, not just a resume framing
trick.

## What Transfers Directly (No New Learning Required)

- **SQL** — `references/sql-server-standards.md` (parameterized queries, indexing awareness,
  transactions, stored procedures) is directly applicable; data engineering adds warehouse-specific
  SQL dialects (T-SQL vs. Snowflake SQL vs. BigQuery SQL) but the fundamentals don't change.
- **Python fundamentals** — type hints, docstrings, `mypy --strict`, `ruff`, `pytest`, `uv`/
  `pyproject.toml` discipline (already this project's standard) carries over unchanged; data
  engineering just adds new libraries (see gaps below), not a new coding standard.
- **Git + CI/CD** — `references/azure-devops-cicd.md`'s branching model and pipeline structure
  applies to pipeline code exactly as it applies to bot code.
- **Exception/error taxonomy thinking** — classifying failures (expected/data-quality vs.
  unexpected/infrastructure) and designing bounded retries is the same skill, applied to a
  different failure surface.
- **Process discovery mindset** (Stage 1 of this skill: is this automatable, what's the volume,
  what are the exception scenarios) — directly reusable as "is this pipeline-able, what's the data
  volume, what are the data quality failure modes."
- **Config-driven design, credential management (Key Vault), least privilege** — identical
  requirement in data engineering; a pipeline with a hardcoded connection string is exactly as
  wrong as a bot with one.

## The Real Gaps to Close

| Gap                                  | What it is                                                                                                                                                                                              | Why RPA doesn't cover it                                                                                                                                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Orchestration at scale**           | Apache Airflow (DAGs, operators, sensors, scheduling, backfills) or Azure Data Factory (pipelines, triggers, Integration Runtimes)                                                                      | Orchestrator/Control Room orchestrate _bots_; Airflow/ADF orchestrate _arbitrary data tasks_ across many more source/sink types, with dependency graphs and backfill semantics that queue-based RPA doesn't need |
| **Bulk/distributed data processing** | `pandas` for small-to-medium data; **polars** or **Apache Spark** once data exceeds roughly 1M rows or single-machine memory                                                                            | RPA processes one transaction at a time; data engineering processes millions of rows per run and needs vectorized/distributed compute, not per-row loops                                                         |
| **Transformation-layer tooling**     | **dbt** (data build tool) — SQL-based, version-controlled, testable transformation layer that runs inside the warehouse                                                                                 | RPA has no equivalent; this is the modern standard way transformation logic is written, tested, and documented in a warehouse                                                                                    |
| **Data modeling**                    | Dimensional modeling (star schema, fact/dimension tables — the Kimball approach) and the **medallion architecture** (bronze/raw -> silver/cleaned -> gold/aggregated layers, popularized by Databricks) | RPA doesn't require thinking about how data is _shaped_ for downstream analytics consumption; this is a new design skill, not a new tool                                                                         |
| **Data quality frameworks**          | **Great Expectations** or **Pandera** — schema/statistical validation of dataframes as an explicit pipeline step                                                                                        | RPA's "business exception" concept is close, but formalized, declarative data quality assertions are a distinct skill worth deliberate practice                                                                  |
| **Change Data Capture (CDC)**        | Detecting and propagating only _changed_ rows from a source (SQL Server 2022 natively supports CDC and Change Tracking) instead of full reloads                                                         | RPA typically processes discrete transactions/items, not incremental table deltas — CDC is a genuinely new concept                                                                                               |
| **Cloud data platforms**             | Azure Synapse Analytics, Databricks, Snowflake, or BigQuery — the actual compute/storage layer data runs on                                                                                             | RPA's infrastructure knowledge (Orchestrator, robot machines) doesn't transfer to warehouse/lakehouse platform administration                                                                                    |
| **Batch vs. streaming**              | Recognizing when a problem needs streaming (Kafka, Event Hubs, Spark Structured Streaming) vs. scheduled batch                                                                                          | RPA is essentially always batch/event-triggered at the transaction level; large-scale streaming is a new mental model                                                                                            |

## Learning Sequence (Building on This Project's Existing Stack)

Ordered to maximize reuse of what's already known (Python, SQL Server, Azure DevOps, `uv`) before
introducing genuinely new tools.

1. **SQL depth** — window functions, CTEs, query plan analysis (already have SSMS from
   `references/tooling-environment-setup.md`); this is the highest-leverage, lowest-new-tool step.
2. **pandas -> polars** — same DataFrame mental model as pandas, but the default for anything
   exceeding ~1M rows; low switching cost, immediate practical payoff.
3. **dbt fundamentals** — models, tests, `ref()`/`source()` macros, documentation generation; SQL
   skill (already strong) is the main prerequisite, so this has a short ramp.
4. **Airflow fundamentals** — DAGs, operators, task dependencies, sensors, scheduling; conceptually
   close to REFramework's process orchestration, so the mental model transfers even though the
   syntax is new. Azure Data Factory is a reasonable alternative/complement given this project's
   existing Azure DevOps investment.
5. **Data modeling** — star schema, dimensional modeling, medallion architecture; a design skill,
   practice by modeling a familiar RPA-adjacent dataset (e.g., invoice/transaction data the bots
   already process).
6. **Data quality tooling** — Great Expectations or Pandera, formalizing the business-exception
   instinct already built from RPA exception handling.
7. **A cloud data platform** — pick one based on the target job market (Databricks and Snowflake
   are both strong choices; Azure Synapse is the most natural fit given existing Azure DevOps/Key
   Vault/Storage Explorer familiarity from this project's toolchain).
8. **CDC and incremental loading patterns** — once the above is solid; this is an optimization
   concept best learned after full-reload pipelines are already comfortable.

Optional but recognized in the market: **Microsoft Certified: Azure Data Engineer Associate
(DP-203)** — directly leverages existing Azure DevOps/Azure Storage Explorer/Azure Key Vault
familiarity from this project's toolchain, and signals the transition credibly to employers.

## Where RPA Itself Fits Inside a Data Engineering Platform

This is a genuinely useful, recognized pattern — not just a resume-framing exercise: RPA is a
legitimate **ingestion mechanism** for data engineering when a source system has no API and no
direct database access (the exact "last resort" scenario already covered by the integration
priority order in this skill's main file and in `references/citrix-automation.md`). A bot that
extracts data from a legacy/Citrix-only system and lands it as structured files (CSV/Parquet) in
Blob Storage is functionally the **Extract** step of an ELT pipeline — Airflow or ADF can then
pick up from that landing zone exactly as it would from any other source connector.

UiPath itself is a concrete, production-scale example of this pattern: their Maestro and
Insights products ingest platform events (Robotlogs, Maestro events, Job/Queue/Machine events)
via Spark Structured Streaming on Azure Databricks, processing ~40,000 events/second with
a median end-to-end latency of ~27 seconds. The full architecture — the problem the previous
dual-pipeline setup created, how SSS on Databricks solved it, the Spark execution model,
delivery guarantees, and operational considerations — is documented in
`references/uipath-databricks-integration.md`. That file also covers the Databricks Agent
connector for Maestro: how a Maestro agentic process calls a Databricks AI model (deployed
via Mosaic AI Model Serving) as a structured external participant in an automation workflow.

This means real production experience already exists to draw on for interviews and practice
projects: reframe an existing or hypothetical bot as "the extraction layer for a pipeline with no
native API," not as a standalone automation — that framing is both accurate and exactly how
experienced data engineers describe RPA-as-ingestion when they encounter it.

## Practice Project (Combines Existing + New Skills Directly)

1. Build (or reuse) a bot that extracts transaction/invoice data from a UI-only or legacy source
   using this skill's existing UiPath/Python standards — this is the **Extract** step.
2. Land the output as Parquet files in Azure Blob Storage (already familiar via Azure Storage
   Explorer) instead of writing directly to a destination table — this creates a proper raw/bronze
   layer.
3. Orchestrate a scheduled Airflow DAG (or ADF pipeline) that picks up new files, validates them
   with Great Expectations/Pandera (formalizing the business-exception instinct), and loads them
   into a staging table in SQL Server or a cloud warehouse — this is **Load** plus data quality.
4. Write dbt models that transform staging data into a small star schema (a `fact_transactions`
   table plus 2-3 dimension tables) — this is the **Transform** and data-modeling step.
5. Version everything in Azure Repos with the same branching/PR discipline as
   `references/azure-devops-cicd.md`, and build an Azure Pipelines CI/CD flow that tests the dbt
   models (`dbt test`) and the Python extraction/validation code (`pytest`) before deploying.

This single project exercises every gap in the table above while reusing every skill already
built in this project — it is deliberately the fastest path from "RPA developer" to a portfolio
piece that reads as genuine data engineering work.
