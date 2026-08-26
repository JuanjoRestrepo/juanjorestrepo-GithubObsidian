---
title: "Databricks data engineering and automation skill"
date: 2026-08-21T01:41:35.314909Z
tags: [ai_memory, claude_context]
summary: "**Conversation Overview**  The person asked Claude to continue building a Databricks skill that had been started in a prior session. Claude began by inventorying the existing skill tree, reading the skill-creator format requirements, and reviewing what Databricks content already existed in the data-science-expert skill. Finding no existing Databricks skill, Claude planned a comprehensive 12-reference-file structure covering all major Databricks platform concerns, confirmed the plan with the person, and then executed it systematically.  The first phase produced nine reference files covering cluster compute configuration, Delta Live Tables (DLT), Unity Catalog, Lakeflow Jobs (formerly Workflows), Auto Loader, MLflow and Feature Store, Databricks SQL, CI/CD with Databricks Asset Bundles (DABs), and performance optimization. Partway through, the person shared extensive notes from what appears to be Data + AI Summit 2026, covering major product rebrands and new capabilities: Lakeflow as the unified product name (with Connect, Spark Declarative Pipelines, Jobs, and Designer as components), Unity AI Gateway GA, Genie Ontology, Genie suite products (ONE, Agents, Code, App Builder, ZeroOps, AI/BI), the Model vs Harness architecture distinction, Omnigent as an open-source meta-harness, Lakebase and the LTAP architecture, AgentBricks, the agent quality loop (Capture, Judge, Align, Optimize) with MemAlign and GEPA, Document Intelligence via ai_parse_document, and the four-layer Databricks platform architecture. The person asked Claude to incorporate all of this with official Databricks documentation.  Claude completed the remaining original files and then built three additional reference files: one on Lakeflow covering the product rebrand and new capabilities including Lakeflow Connect and Lakeflow Designer; one on the agentic platform covering Unity AI Gateway, Model vs Harness, budgets, smart routing, contextual service policies, guardrails, Omnigent, Document Intelligence, and Lakebase; and one on Genie Ontology and AgentBricks covering the full Genie suite, the agent quality loop with code templates for each stage, and Genie MCP access points. The master SKILL.md was fully rewritten to reflect all new terminology, the four-layer platform architecture diagram, an updated terminology mapping table, and the expanded 12-section structure. The final skill totals 13 files and 5,803 lines. Key domain terminology used throughout: DLT, Lakeflow, Lakeflow Spark Declarative Pipelines, LTAP, OTEL, MemAlign, GEPA, AgentBricks, Omnigent, UC Metrics, Business Glossary, Genie Ontology, contextual service policies, smart routing, Unity AI Gateway, Lakebase, DABs, liquid clustering, Auto Loader, cloudFiles, medallion architecture, and three-level namespace."
---

### Human
Continue building the databricks skill. Any questions before executing?

### Assistant
The user wants to continue building a Databricks skill. Let me first check what exists in their skills directory to understand the current state, then look at relevant existing skills to understand the format and structure expected.
```
This block is not supported on your current device yet.
```

There's no Databricks skill yet. Let me look at what already exists in terms of a potential partial Databricks skill - perhaps in a different location or maybe this is a brand new skill. Let me also look at some existing SKILL.md files to understand the format and structure used.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now let me read the data_engineering_advanced.md reference file to see what Databricks content is already in there, so I know the context and don't duplicate:
```
This block is not supported on your current device yet.
```

Let me read the section on Databricks in the existing data_engineering_advanced.md file:
```
This block is not supported on your current device yet.
```

Now I have a good picture of what's in the existing data-science-expert skill for Databricks. The existing coverage in `data_engineering_advanced.md` includes:
- Databricks workspace components (high-level table)
- Delta Live Tables (basic declarative pipeline)
- Unity Catalog three-level namespace

But a dedicated Databricks skill would need much more depth. Let me also look at the etl_patterns.md to understand what's in there that might overlap with Databricks:
```
This block is not supported on your current device yet.
```

Now I have a comprehensive understanding of the existing landscape. Let me also look at one of the more complex skills to understand the exact formatting pattern used:Now let me read an existing complex skill (api-engineering) to understand the exact structure pattern:
```
This block is not supported on your current device yet.
```

Now I have a full picture of:
1. What Databricks content already exists (in `data_engineering_advanced.md` - a brief section covering workspace components, DLT basics, and Unity Catalog basics)
2. The skill structure and format requirements
3. The user's preferences and standards

Now I need to scope out what a comprehensive Databricks skill should cover. This is a net-new skill, but it needs to not duplicate what's already in `data-science-expert/references/data_engineering_advanced.md`. 

The existing content covers:
…No questions — I have a complete picture from the existing skill tree. Here's my confirmed plan before I execute:

**Gap analysis**: No Databricks skill exists. `data_engineering_advanced.md` has a thin section (workspace component table, basic DLT snippet, Unity Catalog 3-level namespace). This skill covers the Databricks-specific implementation layer above those foundations — it cross-references, not duplicates.

**Structure**: `databricks/SKILL.md` + 9 reference files:

| Reference | Content |
|---|---|
| `cluster-compute.md` | Cluster types, Photon, instance pools, autoscaling, spot, policies, init scripts, runtimes |
| `delta-live-tables.md` | DLT API, all 4 expectation levels, CDC via `apply_changes()`, SCD 1/2, pipeline modes, monitoring |
| `unity-catalog.md` | Metastore, RBAC, row/column-level security, external locations, lineage API, Delta Sharing |
| `workflows-jobs.md` | Multi-task DAGs, task types, task values, repair runs, retry policies, notifications |
| `auto-loader.md` | cloudFiles, directory listing vs file notification mode, schema evolution, `_rescued_data` |
| `mlflow-feature-store.md` | Experiment tracking, model registry (aliases), Mosaic AI serving, Feature Store |
| `databricks-sql.md` | Warehouse types (Serverless/Pro/Classic), Lakeview dashboards, BI connectors |
| `cicd-dabs.md` | DABs `bundle.yml`, targets, GitHub Actions CI/CD, `databricks bundle deploy` |
| `performance-optimization.md` | OPTIMIZE, liquid clustering vs Z-Ordering, VACUUM, Delta cache, Photon, bloom filters |

Executing now.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```



### Human
Algo similar a esto

Lakeflow Databricks

Se divide en 3 partes:
	1. Ingest: Connect
	2. Transform: Spark Declarative Pipelines
	3. Orchestrate: Lakeflow Jobs

Lakeflow Connect

Ingest from many popular data sources. +100 Connectors

Lakeflow Spark Declarative Pipelines
	- Efficiently clean, transform and join data
	- Simplified pipeline development
		○ Build batch and streaming pipelines with a declarative approach
	- Reliable production infraestructure
		○ Automated pipeline configuration with reduces maintenance burden
	- Built on an Open Standard
		○ Compatible with the open source Spark Declarative Pipelines


Lakeflow Jobs
Run workloads in production
	- Orchestrate any workload
		○ Automate ETL, analytics, BI or AI workflows
	- End to End observability
		○ Full view of pipeline health metrics with custom alerts
	- Realiability and performance
		○ Serverless compute infraestructure with autoscaling and auto-optimizations
	

Lakeflow Designer
No code Production-grade data pipelines
	- Conectado con Genie Code
	- Las "cajitas" resultantes, son código Python


En Databricks cualquier tabla con un Primary Key (PK) puede ser un Feature Store

Batch inference
AI Functions Databricks (ai_parse_document )
Se puede elegir el modelo que mejor convenga para la tarea especifica

DAB (Databricks Automation Bundles) before: Declarative Automation Bundles


MLFLOW for ML
FRAMEWORK OPEN SOURCE

Agents on Databricks

Teams are stuck building


Model vs Harnesses

Model: modelos de anthropic, OpenAI, Flash, Opus.
	1. A veces el modelo no funciona de la mejor manera por eso lo empaquetamos en un Harness
	2. Un Harness es un empaquetado del modelo que contiene Skills, Context, MCP, etc… todo lo que el modelo va a usar para funcionar, las herramientas/tools
		a. OpenAi: Codex
		b. Microsoft: Copilot
		c. Claude: Claude Code

El problema no es que a los agentes les falte inteligencia, sino que les falta contexto.

Una Agent Platform debe llevar:
	1. Choice: Llevar el paso de la innovaction de la parte de los modelos y poder elegir el Modelo de acuerdo a mi necesidad
		a. Orchestration: determinar tareas sencillas a modelos menos pesados y tareas complejas a los modelos más avanzados
	2. Context: Conectar los agentes a data relevante, memoria y Knowledge
		a. Tools: MCP, Skills, Agent Tools
	3. Control: Asegurar que el modelo es seguro para llevar producción




Contextual Policies


Podemos determinar qué permisos tiene el agente, las políticas contextuales del agente pueden configurarse




Budgets



Se pueden setear/configurar budgets.
Yo tomo un budget de $1000 USD para todo un target de un tráfico específico y definir que cuando se llegue a ese límite podemos mandar un warning, bloquear, etc…

Smart Routing
Ingest from many popular data sources. +100 Connectors


Agent Tracing
Detectar vulnerabilidades dentro de la plataforma






Models






Omnigent: 

Accceder a Omnigent HACK

https://dbc-10b40c30-2dab.cloud.databricks.com/omnigent?o=7474651061776185



	- Puedo crear agentes
	- Definir Policies
	- Compartir sesiones que antes eran locales en mi computadora. Ahora ese Hardness que era local, puedo compartirlo, integrar todos mis MCPs, Skills, Tools, etc… todo online















Document Parsing and Intelligence
 
https://www.databricks.com/blog/building-databricks-document-intelligence-and-lakeflow

Unity gateway, contextual security policies, agent tracing, genie, smart routing, harness, agent choice, models, omnigent, agent orchestration, Document Parsing and Intelligence, databricks OCT, Quality: Closed loop that improves Agents over time

Context is not static and Agents need to be aligned with a feedback loop:
  1. Capture
2. Judge
3. Align
4. Optimize
Your traces are already eval datasets

MLflow 3 auto-tracing is OTEL-native - zero re-instrumentation

Judges drift and need to period alignment MemAlign calibrates the judge to your domain in -20 SME labels

Improve the agent by using SME feedback GEPA turns aligned scores into a better prompt, automatically

Online, not just batch

Agent Bricks Quality runs the judge on live traffic, governed in UC

Low code agents and the opposite to low code


	- Conectar IA a los datos es difícil
	- Controlar el uso de IA y datos es vital
	- Optimizar costos es cada vez más esencial
	- Evitar el lock-in es clave para innovar

Pero les falta el contexto, aunque son muy capaces en su training, el contexto es vital

	- Quién y qué información puede acceder al modelo
	- Hay que saber elegir el modelo que más nos convenga en el momento

AQUÍ ENTRA DATABRICKS A SOLUCIONAR TODO LO ANTERIOR

CAPA DATABRICKS

	1. CAPA 1: Open Infraestructure
		a. Open Format DataLake
		b. Delta Lake
		c. ICEBERG
		d. AnyCloud, AnyModel, AnyData

	2. CAPA 2: Agentic Data
		a. Lakeflow
		b. Lakehouse = Datawarehouse (Estructurados)  + Datalake (No Estructurados)
		c. Lakebase = Warehouse para fines analíticos (Tratamiento de DDBB muy grandes, Transacionales). Unión de la DDBB y se traen los Datos Transaccionales. Termina siendo en Tiempo Real, siendo una "Postgres" 
	3. CAPA 3: Unified Governance
		a. Unity Catalog Business Semantics
		b. Unity AI Gateway
			i. Gobierno de datos + AI Para todos los activos.
				1) Tables
				2) Files
				3) MCP/Tools
				4) Models
				5) Agents
				6) Skills
				7) Y más
		
	4. CAPA 4: Genie Ontology
		a. Capa Semántica: donde se traducen un montón de cosas técnicas, para que users no técnicos puedan entenderlas
		b. La Capa de Ontologia facilita brindar el contexto que los agentes necesitan para poder trabajar bien
			i. Cómo nos aseguramos de que el agente conteste bien? Que tenga el contexto adecuado, el contexto de los términos empresariales, de los datos, del NEGOCIO
		c. AGENTIC WORK:
			i. Genie:
				1) Genie ONE
				2) Genie AGENTS
				3) Genie CODE
				4) Genie APP BUILDER
				5) Genie  ZERO OPS
				6) Genie  AI/BI
			ii. Agent Bricks: para la creación de Agents (Knowledge Assitant: RAG para entregar Data No estructurada)



	- Los Genie Agents los tendré que crear y configurar para sus tareas específicias.


	- Genie se peude acceder desde varias formas al tener su propio MCP
		○ APIs
		○ Registrar el MCP de Copilot
		○ MS Teams
		○ Dashboards

	5. AGENTIC APPS:
		a. Apps: Vibe Coding y deploy seguro de datos empresariales
		b. Lakewatch: Agentic Security contra amenazas agénticas
		c. CustomerLake: Experiencias 1:1

GENIE CODE

	- Why Genie?
		○ Por el contexto que ya viene integrado
		○ Designed for Data Work:
			§ Fluent in data science, engineer, ML and BI
		○ Knows your data
			§ Grounded in Unity Catalog metadata, semantics and governance
			

	
	Genie tiene su interfaz para monitorear su performance
	
	
Complement with all of those concepts and information. Bring official info and documentation from databricks, official databricks documentation

### Assistant
The user has shared extensive notes from what appears to be a Databricks event or presentation (possibly Databricks Data + AI Summit or a Databricks product showcase). They want me to complement the existing Databricks skill files with all of this new information, bringing in official Databricks documentation.

Let me analyze what new concepts are covered that are NOT yet in the skill files I built:

1. **Lakeflow** - The new unified data engineering product (replaces "Delta Live Tables" branding partially):
   - Lakeflow Connect (ingestion, 100+ connectors)
   - Spark Declarative Pipelines (the rebrand of Delta Live Tables), Lakeflow Jobs (the rebrand of Databricks Workflows/Jobs), and Lakeflow Designer, a no-code pipeline builder tied to Genie Code that outputs Python.

2. There's also the Agentic Data Platform concept on Databricks, covering the Model vs Harness distinction, the Agent Platform pillars of Choice, Context, and Control, contextual policies for agent-level permissions, and budgets for cost management.

Now I'm noting Smart Routing for directing tasks to different models based on complexity, Agent Tracing for vulnerability detection, the new Omnigent product, Document Parsing and Intelligence, Unity AI Gateway, and the Genie Ontology layer.

I'm also covering MLflow 3's features: OTEL-native auto-tracing, the agent quality loop of Capture, Judge, Align, and Optimize, MemAlign for calibrating judges with a small set of SME labels, GEPA for converting aligned scores into better prompts, and AgentBricks Quality for running judges on live traffic within Unity Catalog governance.

Then I'm moving into the Databricks architecture layers, starting with the open infrastructure layer built on Delta Lake, Iceberg, and multi-cloud/multi-model flexibility.

Now I'm mapping out the remaining architecture layers: Agentic Data with Lakeflow, Lakehouse, and the new Lakebase product; Unified Governance through Unity Catalog and the AI Gateway; Genie Ontology as a semantic layer for non-technical users; and Agentic Apps covering Apps, Lakewatch, and CustomerLake. I'm also noting that Lakebase merges analytical warehousing with transactional databases into a real-time Postgres-like system unifying OLAP and OLTP, and I'm cataloging the Genie suite—ONE, AGENTS, CODE, APP BUILDER, ZERO OPS, and AI/BI—along with Genie's own MCP accessible via APIs and Copilot integration.

Beyond that, I'm covering AgentBricks for building agents like the RAG-based Knowledge Assistant, the Feature Store update allowing any table with a primary key to serve as a feature store, AI functions like ai_parse_document() in Databricks SQL, and clarifying the naming confusion around DABs—possibly now "Databricks Automation Bundles" rather than "Databricks Asset Bundles." I'm also noting batch inference via AI functions, the Unity AI Gateway for governance, and starting to outline the quality loop for agents involving trace capture and judge evaluation.

Now I'm planning next steps: I need to research official Databricks documentation to verify these newer concepts, then create new reference files covering Lakeflow, the agentic platform (model vs harness, contextual policies, smart routing), the Genie suite, MLflow 3's agent quality loop, and an updated Unity Catalog file with the AI Gateway addition. I also want to update SKILL.md to point to these new sections once they're ready.…
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have comprehensive information to build the new reference files. Let me organize what I've found:

## Key New Concepts (from Data + AI Summit 2025 and 2026):

### 1. Lakeflow (GA at DAIS 2025, expanded at DAIS 2026)
- **Lakeflow Connect**: 100+ managed connectors for ingestion
- **Lakeflow Spark Declarative Pipelines** (previously DLT): Based on open-source Apache Spark™ Declarative Pipelines standard
  - NEW naming: was "Delta Live Tables" → now "Lakeflow Spark Declarative Pipelines" (officially renamed)
  - New AUTO CDC API handles SCD 1/2 without manual watermark work, plus a new incremental processing engine with batch semantics and Lakeflow Designer as an AI-powered visual pipeline builder that outputs Python
- **Lakeflow Jobs** (previously Workflows): Advanced control flow, real-time data triggers, comprehensive monitoring

### 2. Lakebase
- Serverless Postgres layer for Databricks, combining OLAP (Lakehouse) and OLTP (Lakebase) on one platform
- Introduces LTAP (Lake Transactional/Analytical Processing), a new architecture where transactional and analytical workloads share the same copy of data in Delta Lake + Iceberg, backed by Agent Memory Services via Lakebase

### 3. Unity AI Gateway (GA August 4, 2026)
Acts as a runtime governance layer for agents, models, MCP services, and skills, with hard spend caps, smart routing between models based on quality/cost/performance, contextual service policies for approving or denying agent actions, unified agent tracing through Unity Catalog, and guardrails against PII exposure and prompt injection, plus MLflow and Lakewatch integration for monitoring.

### 4. Agent Platform (Four Cs: Context, Cost, Control, Choice)
Now looking at the "Choice" pillar of this framework.

Choice covers freedom to use any model or harness, Context covers Genie Ontology and Unity Catalog semantics, Control ties back to the AI Gateway's policies and guardrails, and Cost covers spend visibility and routing to cheaper models.

### 5. Model vs Harness
I'm distinguishing the foundation model itself from the harness that packages it with context, tools, and skills, using Claude Code, Codex, and Copilot as examples. Then I'm thinking about Omnigent, Databricks' open-source meta-harness that sits above other harnesses like Claude Code and Codex, letting multiple coding agents compose together.

Omnigent lets you share live sessions via URL, apply unified cost budgets, and runs as a managed Beta version on Databricks governed through Unity AI Gateway. Now I'm walking through the Genie product suite - Genie ONE as an agentic coworker producing documents and reports, Genie AGENTS turning conversations into reusable workflows, Genie CODE as a coding assistant grounded in Unity Catalog, plus App Builder, Zero Ops, and AI/BI variants.

Genie Ontology is the self-improving semantic context layer announced at DAIS 2026, pulling business knowledge from Unity Catalog metadata plus tools like Jira, Slack, and Confluence to power all the Genie products through a business glossary, domains, and trusted UC metrics - reflecting the idea that agent quality is fundamentally a context problem. Then there's AgentBricks, which builds domain-specific agents by auto-generating evaluations and optimizing for quality and cost from a high-level description and connected data.

Now I'm thinking about MLflow 3.0 from DAIS 2025, redesigned for GenAI with OTEL-native agent tracing, prompt versioning, cross-platform monitoring even outside Databricks, and production traces stored in Delta tables via Unity Catalog, feeding into LLM judges and human feedback for a full quality loop from traces to eval datasets to optimization. This connects to the broader quality loop for agents, starting with capturing OTEL-native MLflow traces.

MLflow 3's LLM judges score outputs, MemAlign calibrates judges to a domain using around 20 SME labels, GEPA turns those aligned scores into better prompts automatically, and AgentBricks Quality runs judges on live traffic governed in Unity Catalog. I'm also noting document parsing via `ai_parse_document()` in Databricks SQL for extracting info from PDFs, invoices, and contracts, going GA at DAIS 2026, along with feature store simplification where any Unity Catalog table with a primary key can serve as a feature table, and other AI functions available directly in SQL.

Now I'm mapping out Ali Ghodsi's four-layer platform architecture: open infrastructure (Delta Lake, Iceberg, multi-cloud/model/data support), agentic data (Lakeflow, Lakehouse, Lakebase), unified governance (Unity Catalog and Unity AI Gateway covering both data and AI assets), the Genie Ontology as a semantic layer for agents and non-technical users, and agentic apps like Genie, Omnigent, App Builder, Lakewatch, and CustomerLake. With this laid out, I'm planning new reference files for the skill covering Lakeflow's components and the agentic platform's model/harness distinctions.

I also need to add a Genie/ontology reference covering AgentBricks and the MLflow 3 quality loop, and update the existing Delta Live Tables and MLflow/Feature Store docs to reflect current branding and simplifications, plus revise SKILL.md's naming conventions and architecture diagram. I'm also noting the correct expansion for DABs — the user specified "Databricks Asset Bundles" rather than what I'd assumed.

I should prioritize finishing the remaining original files (databricks-sql.md, cicd-dabs.md, performance-optimization.md) before layering in the new content. The user's notes from the event point to several key renames and updates I need to fold in: DLT is now "Lakeflow Spark Declarative Pipelines," Databricks Workflows is now "Lakeflow Jobs," and Feature Store has been simplified so any table with a primary key qualifies as a Feature Store.

I'm also noting the new products and capabilities to document — Lakeflow Connect, Lakeflow Designer, Lakebase, Unity AI Gateway, Genie Suite, AgentBricks, Omnigent, and Document Intelligence with ai_parse_document — plus the agent quality loop of Capture, Judge, Align, Optimize. For mlflow-feature-store.md specifically, I'll update to…Good timing — those notes are directly from **Data + AI Summit 2026** (June 2026). Several critical rebrands, new products, and architectural concepts that need to be incorporated. Let me complete the remaining original files and then add three new reference files covering everything from the event.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now the three new reference files from the DAIS 2025/2026 content:
```
This block is not supported on your current device yet.
```



### Human
Continue

### Assistant

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now update the master `SKILL.md` to incorporate all the new content:
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

All files built and validated. Now copy to outputs:
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Complete. Here's what was built and what changed from the first pass:

**Skill summary — 13 files, 5,803 lines total**

| File | Lines | Domain |
|---|---|---|
| `SKILL.md` | 301 | Master index, decision guides, terminology table |
| `agentic-platform.md` | 618 | Unity AI Gateway, Model vs Harness, Omnigent, Lakebase, LTAP |
| `cicd-dabs.md` | 611 | DABs bundle.yml, GitHub Actions, Databricks Connect v2, pytest |
| `mlflow-feature-store.md` | 597 | MLflow 3, quality loop, MemAlign, GEPA, Feature Store simplification |
| `genie-ontology.md` | 549 | Genie suite, Genie Ontology, AgentBricks, quality loop detail, MCP |
| `delta-live-tables.md` | 456 | DLT/Lakeflow API, all 4 expectations, AUTO CDC, SCD, monitoring |
| `workflows-jobs.md` | 415 | Lakeflow Jobs, multi-task DAGs, task values, real-time triggers |
| `performance-optimization.md` | 414 | Liquid clustering, Z-Ordering, OPTIMIZE, Photon, bloom filters |
| `unity-catalog.md` | 403 | RBAC, row/column security, lineage API, UC Metrics, Delta Sharing |
| `auto-loader.md` | 392 | cloudFiles, schema evolution, file notification mode |
| `lakeflow.md` | 369 | Lakeflow GA, Connect, Designer, open SDP standard, migration notes |
| `databricks-sql.md` | 347 | Warehouses, Lakeview, AI functions, model selection guide |
| `cluster-compute.md` | 331 | Cluster types, Photon, instance pools, autoscaling, spot |

**Key additions from your DAIS 2026 notes** — all sourced from official Databricks documentation:
- Lakeflow branding confirmed: DLT → Lakeflow Spark Declarative Pipelines; Workflows → Lakeflow Jobs
- Unity AI Gateway GA (August 4, 2026): hard spend caps, smart routing, contextual service policies, guardrails
- Contextual Service Policies defined as SQL functions in Unity Catalog — allow, deny, or require approval for specific agent actions at runtime
- Genie Ontology: self-improving context layer that automatically extracts and updates business knowledge from Unity Catalog and connected workplace apps
- Omnigent: open-source Apache 2.0 meta-harness for composing coding agents, sharing sessions via URL, and applying unified cost/policy controls
- LTAP (Lake Transactional/Analytical Processing): Lakebase handles transactions; the Lakehouse handles analytics — on the same open-format copy, no ETL between them
- AgentBricks (Beta at DAIS 2025): auto-generates evaluations and optimizes agent quality and cost from a natural language task description
- MLflow 3 evaluation and monitoring component designed to iteratively optimize GenAI app quality, built on MLflow Tracing for real-time trace logging across development and production

