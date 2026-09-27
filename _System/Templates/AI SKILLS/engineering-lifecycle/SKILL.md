---
name: engineering-lifecycle
description: >-
  Comprehensive end-to-end engineering lifecycle framework for software development, data science,
  data engineering, machine learning, and RPA. Use when planning, designing, documenting, executing,
  testing, reviewing, or deploying high-quality production systems across any technical domain.
---

# End-to-End Engineering Lifecycle Standard

This skill establishes the universal quality standards, architectural methodologies, and procedural frameworks for executing any technical project across **Software Engineering (Full-Stack/Backend/APIs)**, **Data Science, Machine Learning & Data Engineering**, and **Robotic Process Automation (RPA)**.

---

## 1. Universal Engineering Lifecycle (7-Phase Framework)

Every technical artifact must advance through seven rigorous phases:

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           UNIVERSAL SDLC / EDLC                             │
  └─────────────────────────────────────────────────────────────────────────────┘
   [1. Discovery] ──> [2. Planning & ADR] ──> [3. System Design] ──> [4. Documentation]
           │                                                               │
           └─────────────────────────<─────────────────────────────────────┘
                                     │
                                     ▼
        [5. Execution & Clean Code] ──> [6. Testing Pyramid] ──> [7. Deploy & Observability]
```

---

### Phase 1: Problem Understanding & Discovery
*Goal: Clarify ambiguity, eliminate hidden assumptions, and define quantifiable success metrics.*

1. **Requirements Deconstruction:**
   - Classify requirements into Functional (FR) and Non-Functional (NFRs: Latency, Throughput, RTO/RPO, Security, Availability, Concurrency).
   - Identify Domain Invariants and Bounded Contexts (Domain-Driven Design).
2. **Feasibility & Constraints Matrix:**
   - Technical constraints (existing stack, compute limits, network bottlenecks).
   - Regulatory & compliance boundaries (GDPR, HIPAA, PCI-DSS, SOC2, Data Sovereignty).
3. **Clarification Protocol:**
   - When requirements are ambiguous or underspecified, formulate explicit clarifying questions and propose prompt/specification improvements before writing implementation code.

---

### Phase 2: Planning & Architectural Decision Making
*Goal: Evaluate trade-offs systematically and document architectural rationale with zero guesswork.*

1. **Architectural Decision Records (ADR):**
   Every significant architectural choice (framework, database engine, messaging protocol, orchestration engine) requires a structured ADR:
   - **Title & Context:** What problem is being solved and why now?
   - **Options Considered:** Minimum 2-3 viable alternatives with pros/cons matrix.
   - **Decision & Trade-offs:** The selected solution and the exact trade-offs accepted (e.g., consistency over availability under CAP, memory overhead vs. read latency).
   - **Consequences:** Positive, negative, and operational risks.
2. **System Constraints & Theorems:**
   - **Distributed Systems:** Explicit analysis of CAP Theorem / PACELC tradeoffs.
   - **Data Systems:** Batch vs. Stream processing evaluation; Lambda vs. Kappa vs. Lakehouse architecture.

---

### Phase 3: System & Interface Design
*Goal: Establish strict contracts, schema invariants, and component boundaries prior to coding.*

1. **Contracts-First Architecture:**
   - **APIs & Web:** OpenAPI 3.1 / JSON Schema for REST, Protocol Buffers for gRPC, AsyncAPI for event-driven systems.
   - **Data Engineering:** Schema enforcement at ingestion; Medallion Data Architecture (Bronze: Raw append-only, Silver: Cleaned/deduplicated/conformed, Gold: Business aggregations/marts).
   - **RPA:** Dispatcher-Performer pattern; segregated transactional queues; explicit contract between dispatcher payloads and performer consumers.
2. **Defensive Data Modeling:**
   - Relational schemas normalized to 3NF/BCNF with explicit indexing strategies (B-Tree, Hash, GIN/GiST).
   - Analytical schemas (Star/Snowflake schema, dimensional modeling with SCD Type 1/2/4).
   - Idempotency keys baked into write contracts.

---

### Phase 4: Documentation (Diátaxis Framework)
*Goal: Eliminate documentation drift and ensure clarity across all user and developer personas.*

Structure all technical documentation using the **Diátaxis Framework** (4 distinct quadrants):

| Quadrant | Purpose | Focus | Tone / Style |
| :--- | :--- | :--- | :--- |
| **Tutorials** | Learning-oriented | Guides a newcomer through a complete end-to-end example | Lesson-focused, step-by-step |
| **How-To Guides** | Problem-oriented | Solves a specific real-world problem or operational recipe | Task-focused, actionable |
| **Reference** | Information-oriented | Technical descriptions, APIs, schemas, configurations | Dry, complete, precise |
| **Explanation** | Understanding-oriented | Architectural context, rationale, design trade-offs | Conceptual, analytical |

#### Living Documentation Requirements:
- **Code Docstrings:** Google or NumPy docstring format on every function, class, and method containing:
  - Concise purpose summary.
  - Typed parameters with validation boundaries.
  - Return types and semantics.
  - Explicit list of raised exceptions.
- **Data Catalog & Dictionaries:** Column-level metadata, data types, business definitions, nullability, and lineage tracking (Unity Catalog / OpenLineage).
- **RPA Process Documentation:** Process Definition Document (PDD) with visual step maps + Solution Design Document (SDD) with exception handling tables.

---

### Phase 5: Execution & Implementation
*Goal: Write modular, secure, highly maintainable, and type-safe code.*

1. **Universal Coding Standards:**
   - **Type Safety:** 100% type hints / annotations (Python `typing`, TypeScript strict mode, Java/C# strong typing).
   - **Static Code Analysis (SCA):** Zero linting errors and zero type errors across Ruff, MyPy, ESLint, PMD, SonarQube.
   - **Modular OOP / Functional Design:** SOLID principles, Hexagonal Architecture (Ports and Adapters), Dependency Injection, high cohesion, low coupling.
   - **Error Handling & Observability:**
     - Explicit error handling; never swallow exceptions or use empty `except`/`catch`.
     - Structured JSON logging with contextual metadata (trace ID, user ID, tenant ID, execution time). **Never use raw `print()` statements in production code.**
   - **Security Invariants:**
     - Zero hardcoded credentials, tokens, or API keys. Always externalize via environment variables (`.env`, Secret Managers, Vault).
     - Strict server-side input validation and sanitization (Zod, Pydantic, Marshmallow).
     - Principle of Least Privilege (PoLP) across DB connections, IAM roles, and filesystem permissions.
2. **Database & Schema Evolution:**
   - Zero-Downtime migrations using the **Expand and Contract** pattern (Phase 1: Add new column; Phase 2: Dual write; Phase 3: Backfill; Phase 4: Switch read; Phase 5: Drop old column).

---

### Phase 6: Testing & Quality Assurance
*Goal: Ensure correctness, prevent regressions, and prove system reliability under stress.*

```
                       TESTING PYRAMID
                          /  E2E  \        (5-10% - Critical user paths)
                         /─────────\
                        /Integration\      (20-30% - Testcontainers, DB, Mocks)
                       /─────────────\
                      /   Contract    \    (10% - Pact, Schema validation)
                     /─────────────────\
                    /    Unit Tests     \  (≥80% Coverage - Pure functions, isolation)
                   └─────────────────────┘
```

1. **Testing Standards by Discipline:**
   - **Software & APIs:**
     - Unit tests with ≥80% branch and line coverage (PyTest, Jest, Vitest, JUnit).
     - Strict mock isolation (unit tests must never make real network/disk I/O).
     - Integration tests utilizing ephemeral dependencies (Testcontainers, in-memory databases).
     - Property-Based Testing (Hypothesis / Fast-Check) for mathematical algorithms, parsers, and serialization routines.
   - **Data Science & ML:**
     - Data quality checks: Schema validation, null rate limits, distribution drift, range assertions (Great Expectations, Soda, Pandera).
     - Pipeline idempotency tests: Multiple runs with same input yield exact same output without duplicate side-effects.
     - Model evaluation: Slice-based evaluation across sub-populations, fairness/bias checks, confusion matrix, ROC-AUC, PR-AUC, calibration curves.
   - **Robotic Process Automation (RPA):**
     - REFramework state transitions validation.
     - Selector resilience tests (dynamic fuzzy selectors, anchor-based matching).
     - Segregated exception testing: Business Rule Exceptions (BRE) vs. Application Exceptions (SysEx) with automated retries.

---

### Phase 7: Deployment, Release & Observability
*Goal: Deliver changes reliably, verify in production safely, and monitor health continuously.*

1. **CI/CD Pipeline Invariants:**
   - Automated steps: `Lint -> Typecheck -> Unit Tests -> Build -> Security Scan (SAST/DAST/Trivy) -> Integration Tests -> Artifact Registry -> Deploy`.
   - Immutable build artifacts (Docker images with pinned SHA digests, versioned wheels/jars).
2. **Deployment Strategies:**
   - Zero-downtime releases: Blue-Green, Canary (1% -> 10% -> 50% -> 100%), or Feature Flags (LaunchDarkly, Unleash).
   - Automated rollback triggers upon error rate spikes or latency degradation.
3. **Observability Stack (The Three Pillars):**
   - **Metrics:** RED method for services (Rate, Errors, Duration); USE method for resources (Utilization, Saturation, Errors).
   - **Logs:** Structured JSON logs correlated with distributed trace IDs.
   - **Traces:** OpenTelemetry instrumentation across service boundaries, database queries, and async queues.
4. **SLO / SLA / SLI Framework:**
   - Define Service Level Indicators (e.g., P99 latency < 200ms, HTTP 5xx rate < 0.01%).
   - Establish error budgets and automated alerting through PagerDuty / OpsGenie.
5. **Post-Release & Hypercare:**
   - Hypercare monitoring window for newly deployed systems (active triage).
   - Blameless Post-Mortem culture with root-cause analysis (5 Whys) and actionable prevention backlog.

---

## 2. Domain-Specific Deep Dives

### A. Data Science & Machine Learning Standards
- **Jupyter Notebook Structure:**
  1. `Setup & Imports` (pinned dependencies, seed definition).
  2. `Data Ingestion & Schema Assertion`.
  3. `Data Cleaning & Validation`.
  4. `Exploratory Data Analysis (EDA)` (Seaborn for distribution analysis, Plotly for interactive exploration).
  5. `Feature Engineering & Preprocessing` (encapsulated in scikit-learn Pipelines or ColumnTransformers to avoid data leakage).
  6. `Model Training & Cross-Validation` (stratified K-fold, temporal splits for time-series).
  7. `Model Evaluation & Diagnostics`.
  8. `Export Production Pipeline` (clean modular `.py` modules, MLflow model logging).
- **MLOps Requirements:**
  - Feature store integration (Feast / Databricks Feature Store).
  - Model registry versioning with lineage from dataset hash to evaluation metrics.
  - Drift monitoring (Data Drift with Kolmogorov-Smirnov / PSI; Concept Drift with metric degradation alerts).

### B. Full-Stack & Backend Engineering Standards
- **Framework Selection:**
  - Full-Stack: TypeScript T3 Stack (Next.js, tRPC, Prisma, NextAuth, Tailwind) for end-to-end type safety.
  - High-Performance APIs: FastAPI (async Python, Pydantic v2) or Go / Django Rest Framework per scalability needs.
- **Security Headers & Middleware:**
  - CSP (Content Security Policy), HSTS, CORS configuration, Rate Limiting (Token Bucket / Leaky Bucket via Redis), CSRF protection.

### C. RPA (Robotic Process Automation) Standards
- **Architecture:** REFramework (UiPath / Python-Robocorp) with Dispatcher / Performer separation.
- **Queue Management:** Idempotent transaction processing, retry policies (exponential backoff for transient system failures, immediate dead-lettering for business rule exceptions).
- **Selector Resilience:** Avoid strict index-based selectors; use semantic fuzzy attributes, UI Automation trees, and fallback visual OCR anchors.
- **Governance:** Credential injection via CyberArk / Orchestrator Assets; zero local credential persistence.

---

## 3. Pre-Commit / Pre-Delivery Quality Checklist

Before completing any task or delivering code, verify:

- [ ] **Architecture:** Is the solution modular, decoupled, and compliant with the system's design patterns?
- [ ] **Type Safety:** Are all type annotations complete with zero type checker warnings?
- [ ] **Docstrings:** Are Google/NumPy docstrings present with typed inputs, returns, and raised exceptions?
- [ ] **Error Handling:** Are exceptions explicitly caught, handled, and logged with structured logs?
- [ ] **Testing:** Are unit tests written with ≥80% coverage, isolated from I/O, and passing?
- [ ] **Security:** Are all secrets externalized, inputs validated server-side, and least-privilege applied?
- [ ] **Idempotency:** Are mutations, data pipelines, and transactional workflows safe for concurrent / repeated execution?
- [ ] **Documentation:** Are user guides, API specs, or ADRs updated without drift?
