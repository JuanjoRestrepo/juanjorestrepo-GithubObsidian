---
name: rpa-development
description: >
  Expert-level RPA skill covering the full lifecycle from process discovery to hypercare, at
  senior/CoE-lead standard. Focus: UiPath (REFramework, Dispatcher/Performer, Orchestrator,
  selectors, custom C# activities), Power Automate Cloud and Desktop, Python (rpaframework/Robocorp,
  pywinauto), Citrix automation, SQL Server, Git, and the standard enterprise toolchain (VS Code,
  PyCharm, SSMS, Azure Storage Explorer, FileZilla, credential managers). Trigger on: RPA, bot,
  robot, UiPath, Power Automate Cloud/Desktop/PAD, Orchestrator, REFramework, Dispatcher/Performer,
  PDD/SDD, queues/transactions, selectors, Citrix, Robocorp, rpaframework, SQL Server queries,
  debugging a bot, environment setup, or automating a manual process. Also trigger on vague
  requests: "automate this process", "build a bot", "design a workflow", "review my automation",
  "why is my bot failing". Covers planning, design, docs, coding standards, testing, deployment,
  debugging, performance, and governance.
---

# RPA Development Skill

A senior RPA Developer / CoE-standard skill spanning process discovery, solution design, bot
development (UiPath + Power Automate Cloud/Desktop + Python + C# + SQL Server), Citrix automation,
testing, deployment, debugging, performance optimization, and governance.

---

## How to Use This Skill

1. **Identify the lifecycle stage** the user is at (discovery, design, build, test, deploy,
   hypercare/support) and jump to the matching section.
2. **Ask clarifying questions** when platform, exception scope, data sensitivity, or attended vs.
   unattended mode is unclear — never assume for anything touching credentials, PII, or financial
   transactions.
3. **Always apply** [Cross-Cutting Best Practices](#cross-cutting-best-practices) regardless of
   task type — these are non-negotiable at senior level.
4. **Produce artifacts in the right format**: workflows/code, PDD/SDD sections, test cases,
   exception matrices, or a combination — see [Output Format Guide](#output-format-guide).
5. **Justify design decisions** — especially state machine vs. sequence, queue vs. in-memory
   looping, and attended vs. unattended. Say _why_, not just _what_.

### Quick Platform Decision Guide

| Situation                                                                                        | Recommended approach                                                                                           |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Enterprise, Windows apps, legacy/mainframe (green-screen), citizen dev + CoE                     | **UiPath** (Studio + Orchestrator)                                                                             |
| Microsoft 365/Dynamics-connected system, event/API-driven process, approvals                     | **Power Automate Cloud** (default Power Automate choice — see note below)                                      |
| Desktop-only legacy app with no connector/API path                                               | **Power Automate Desktop** (PAD), typically invoked _from_ a Cloud flow                                        |
| Need custom logic UiPath can't express cleanly, reusable libraries, performance-critical parsing | **C# custom activities** inside UiPath, or invoke **Python** via `Invoke Python Method` / external process     |
| Full code-first automation, CI/CD-native, no per-bot licensing, data-heavy processing            | **Python** — `rpaframework` (Robocorp) + `pywinauto`/`Selenium`/`pyautogui`                                    |
| Bulk data read/write against a relational source, reporting, staging tables                      | **SQL Server** direct integration (parameterized queries/stored procs) — often replaces UI automation entirely |
| Target application is delivered via Citrix/virtual desktop                                       | Apply the **integration priority order** below — Citrix automation is the _last_ resort, not the default       |
| Process needs discovery/quantification before anything is built                                  | **Process/Task Mining** (UiPath Process Mining, Task Capture) first                                            |

**On Power Automate specifically**: default to **Cloud flows** — they call connectors/APIs
directly and sit at the top of the integration priority order below, the same position API access
occupies for every other platform in this skill. Reach for **Desktop flows** only for the specific
leg of a process that has no connector/API path (a legacy thick-client app, for example), and
prefer calling that Desktop flow _from_ a Cloud flow (`Run a flow built with Power Automate for
desktop`) over building a Desktop-only flow. See `references/power-automate-cloud.md` first for
any new Power Automate work; go to `references/power-automate-desktop.md` only for the UI-automation
leg.

**Integration priority order (applies to every platform, always check top-down before automating
the UI):** API → Database (SQL Server direct) → native UI automation → Citrix/virtualized
automation (Computer Vision/OCR/anchors as the last resort).

**Dispatcher/Performer model** (use for high-volume, decoupled, or multi-machine processing): a
**Dispatcher** process reads source data and populates an Orchestrator queue only — no processing
logic. One or more **Performer** processes (REFramework-based) consume the queue independently.
This decouples data acquisition from processing, enables horizontal scaling (more Performer
robots = more throughput), and lets the Dispatcher run on a different schedule than the Performers.
Default to this over a single monolithic Dispatcher+Performer workflow whenever volume is high or
multiple robots will process the same queue concurrently.

---

## Lifecycle Stage 1 — Process Discovery & Assessment

Never start building without this. A senior RPA developer qualifies the process first.

**Automatability checklist** (all should be true, or flag risk):

- Rule-based, deterministic — no subjective judgment calls
- Structured or semi-structured digital input (not handwriting, not ambiguous free text without an
  LLM/AI Center step)
- Stable process — hasn't changed in the last 6–12 months, no imminent system migration
- High volume and/or high frequency, or high error cost — ROI justifies build + maintenance cost
- Access to a **non-production/test environment** with representative test data

**Discovery outputs:**

- **Process Definition Document (PDD)** — business-level: as-is process, in/out scope, exception
  scenarios (business exceptions enumerated by the business, not guessed), volumes, SLAs,
  applications touched, credentials/access needed
- **Complexity scoring** (Low/Medium/High) — based on # applications, # decision points, # exception
  types, UI stability (thick client > web > Citrix/virtualized > mainframe/green-screen in
  ascending difficulty), need for OCR/AI

→ See `references/documentation-templates.md` for the full PDD/SDD/test case templates.

---

## Lifecycle Stage 2 — Solution Design

Produce a **Solution Design Document (SDD)** before writing any workflow. It must define:

- **Architecture**: attended vs. unattended vs. hybrid; framework (REFramework / linear / hybrid
  state machine); trigger (scheduled, queue-driven, event-driven via Orchestrator webhook/email)
- **Data flow diagram**: source system → bot → target system, with every credential/config touch
  point named
- **Exception taxonomy**: every failure mode classified as **Business Exception** (expected,
  bot continues to next item, logged, often emailed to business) vs. **System/Application
  Exception** (unexpected, bot retries per policy then escalates — never silently swallowed)
- **Reusability plan**: which pieces become shared libraries (login, common validations, logging
  wrapper) vs. process-specific
- **Non-functional requirements**: expected run time per item, concurrency (how many Orchestrator
  robots/sessions), peak volume handling, disaster recovery (what happens if the bot crashes
  mid-transaction — must be idempotent/resumable)

---

## Lifecycle Stage 3 — Build

### UiPath

- **Always use REFramework** (or a documented custom variant) for anything unattended/production —
  never a flat linear sequence for production bots. It gives you: Init → Get Transaction Data →
  Process → Set Transaction Status, with built-in retry-on-system-exception and config-driven
  behavior out of the box.
- **Config-driven, never hardcoded**: all URLs, paths, thresholds, retry counts, email recipients
  live in `Config.xlsx` (or Orchestrator Assets/Storage Buckets for shared values) — never in the
  workflow itself.
- **Credentials**: Orchestrator **Credential Store** (Asset of type Credential, backed by
  CyberArk/Azure Key Vault/Windows Credential Manager in enterprise setups) — never plaintext in
  Config, never `Get Password` from a config cell.
- **Naming conventions**: PascalCase for workflows (`GetInvoiceData.xaml`), camelCase for
  variables, `in_`/`out_`/`io_` prefixes for arguments by direction, one Sequence/Flowchart per
  `.xaml` doing one clearly named thing (Single Responsibility — 1 workflow file should fit on one
  screen without excessive scrolling).
- **Selectors**: prefer the **Object Repository** with reusable UI descriptors over ad-hoc
  selectors; avoid `idx` attributes (fragile, index-dependent); use dynamic selectors (`*`,
  wildcards) sparingly and only where the attribute is genuinely dynamic; always validate with
  **UI Explorer**, never hand-edit XML blind.
- **Workflow Analyzer**: run before every commit — zero errors, justify any suppressed warnings in
  a PR comment. Enforce via the `.editorconfig`/ruleset in CI (`uipath-cli` / `uipcli` in the
  pipeline).
- **Logging**: `Log Message` at every decision point and before/after every external system call,
  with structured fields (TransactionID, business key) via `Add Log Fields` — never bare strings.
  Route to Orchestrator via `Elastic Search`/robot logs, never local-only in production.
- **Testing**: UiPath **Test Manager** + Studio unit tests for individual workflows/reusable
  components; mock external dependencies where possible; a full E2E run against
  representative test data before every UAT handoff.

→ See `references/uipath-reframework.md` for the comprehensive, production-grade guide to REFramework theory, finite state machines, coding anatomy, tabular/queue architectures, multi-tier retries, circuit breakers, and enterprise best practices. See `references/uipath-standards.md` for Config.xlsx schema, Workflow Analyzer ruleset, queue/transaction design, selector/Object Repository best practices, and custom C# activity guidance.

### Power Automate Cloud (default Power Automate choice)

- Use as the default entry point for any Power Automate work: automated cloud flows for
  event-driven processes (new item, new email, record updated), instant cloud flows for
  user-initiated actions, scheduled cloud flows for batch/time-based jobs.
- **Error handling**: Scope-based Try/Catch/Finally via **Configure run after** — wrap main logic
  in a `Try` Scope, add a `Catch` Scope configured to run only when `Try` has failed, and
  optionally a `Finally` Scope for cleanup that always runs. Apply the same Business/System
  exception taxonomy used everywhere else in this skill inside the `Catch` branch.
- **Never call it a UI-automation problem before checking for a connector** — 700+ prebuilt
  connectors plus custom/HTTP connectors cover most modern SaaS/Microsoft 365/Dynamics/database
  targets; a Desktop flow is for the residual case only.
- **Approvals**: use the built-in Approvals connector (`Start and wait for an approval`) rather
  than hand-rolling email-based approval tracking.
- **Governance**: Data Loss Prevention (DLP) policies (connector classification/blocking), role-
  based access control over who can create/edit/run flows, and audit logs — configure before broad
  adoption, not after an incident. Un-owned flows are the Cloud-flow equivalent of shadow bots.
- **ALM**: same Solutions-based mechanism as Desktop flows — see the ALM section in
  `references/power-automate-desktop.md`, which applies identically to Cloud flow components.
- **Architecture and flow control**: layer a solution (trigger / orchestration / business logic /
  integration / data), pick the right control construct (Condition vs. Switch vs. Apply to each
  vs. Do Until) by naming the workflow pattern it implements rather than reaching for whichever
  action is familiar, and decompose logic into child flows once a flow's action count or branching
  obscures its overall shape — never let a flow grow past the point where its structure is
  readable at a glance.

→ See `references/power-automate-cloud.md` for the full trigger-type decision table, naming
conventions, the complete Scope/Configure-run-after error-handling pattern, batch/connector
efficiency guidance, licensing notes, and monitoring setup. See
`references/power-automate-architecture.md` for architectural layering, control-flow construct
selection (with verified concurrency limits and the Do Until silent-success trap), state
management under concurrency, child-flow decomposition mechanics, and orchestration patterns
(fan-out/fan-in, content-based routing, saga/compensating actions, idempotency).

### Power Automate Desktop (PAD) — the UI-automation companion to Cloud flows

- Use only for the specific leg of a process that has no connector/API path — a legacy thick-client
  app, a system with no exposed API, or an organization-specific desktop tool. Prefer calling this
  Desktop flow _from_ a Cloud flow (`Run a flow built with Power Automate for desktop`, targeting a
  machine group) over building a Desktop-only flow for an otherwise connector-reachable process.
- **Never build one gigantic monolithic flow.** Structure every automation the same way as a
  REFramework process conceptually: `Main Flow` orchestrates discrete, named subflows —
  `Login`, `ProcessData`, `Validation`, `Reporting`, `Logout` — each independently testable.
- Extract reusable logic into **subflows** called from multiple flows/projects rather than
  duplicating actions — PAD's flow-level reuse is weaker than UiPath's library model, so this
  discipline matters more, not less.
- Variables: `%CamelCaseWithPrefix%` conventions consistent across the team (e.g. `%inCustomerId%`)
  — PAD's default `%Variable1%` naming is never acceptable in production.
- Error handling: use **On Block Error** with explicit business/system exception branching, same
  taxonomy as UiPath — do not let a flow terminate on first error without a structured catch.

→ See `references/power-automate-desktop.md` for action priority order, credential handling
(`Get credential`), machine-group/timeout guidance for unattended runs, and Solutions-based ALM.

### Citrix / Virtualized-App Automation

Only reach for this after confirming API and direct database access are genuinely unavailable —
Citrix automation is the least reliable, highest-maintenance option and should be flagged as a
project risk in the SDD, not treated as routine.

- **Never rely on static screen coordinates** — they break on resolution/DPI change, window
  resize, or session reconnect.
- Preferred techniques, in order: native selectors (if the published app exposes an accessible UI
  tree through Citrix) → Computer Vision (CV Screen Scope + CV activities) → OCR (for text
  extraction where no UI tree exists) → anchor-based relative identification → keyboard-shortcut-
  driven navigation (most robust against visual drift, least flexible).
- Always add **image/OCR validation** after each action (assert expected screen state) before
  proceeding — Citrix's added latency and occasional render lag make blind sequential actions
  unreliable.
- Build in explicit `WaitForImage`/synchronization steps rather than fixed `Delay` — fixed delays
  are both slower than necessary on fast days and flaky on slow ones.

### SQL Server (direct integration)

Whenever the source or target is a relational database, prefer direct SQL access over UI
automation against a database front-end.

- Never `SELECT *` — name columns explicitly; only pull what the process needs (also limits PII
  exposure).
- Always use **parameterized queries** (never string-concatenated SQL) — this is a security
  requirement, not a style preference, identical to SQL-injection prevention in any other
  application.
- Wrap multi-statement writes in **transactions**; any partial-failure must roll back cleanly —
  a bot that writes 3 of 5 related rows before crashing is a data-integrity incident.
- Use stored procedures for non-trivial or frequently-reused logic — keeps business logic
  versioned in the database alongside (not scattered across) the bot's workflow.
- Respect indexes: filter/sort on indexed columns where possible; avoid functions wrapped around
  indexed columns in `WHERE` clauses (`WHERE YEAR(CreatedDate) = 2026` defeats an index — use a
  range predicate instead).
- Connection strings and credentials follow the same rule as everywhere else: Orchestrator Asset /
  Key Vault / environment secret — never embedded in the workflow or a config file in plaintext.

### Python (`rpaframework` / Robocorp, or bespoke)

- Use **`rpaframework`** (Robocorp) as the default library set — it wraps Selenium, pywinauto,
  Excel, email, PDF, cloud storage, and Outlook/Excel with a consistent, well-tested API; prefer it
  over hand-rolling raw `pyautogui`/`win32com` unless a library gap forces it.
- Structure as a proper Python package (not a script): `pyproject.toml` with `uv`, `src/` layout,
  `RobotFramework`-style `tasks.py` or a `Producer/Consumer/Process` pattern mirroring
  REFramework's shape (get work item → process → handle exception → report).
- **Work item / queue abstraction**: Robocorp Control Room work items, or a custom queue (DB table
  / Azure Queue) — never an in-memory list for anything that must survive a crash and resume.
- Type hints + docstrings + `mypy --strict` + `ruff` on all automation code — same standard as any
  other production Python (see cross-cutting practices below); RPA code is _not_ exempt because
  it's "just a script."
- **UI automation**: `pywinauto` (Win32/UIA backends) for desktop; `Selenium`/`Playwright` for web
  — prefer API/DB access over UI automation wherever the target system exposes one (UI automation
  is the _last resort_, not the default, even in an "RPA" project).
- **Page Object Model (POM)**: for any web/desktop UI automation with more than one screen or more
  than one script reusing a screen, structure the codebase around POM — one class per screen/UI
  region holding locators and actions, business logic never touches a raw selector directly. This
  is the single highest-leverage maintainability practice for Python UI automation: a UI change is
  fixed in one page class instead of hunted across every script that references it.
- Package and schedule via the same CI/CD discipline as any deployable: Docker image or Robocorp
  Robot artifact, deployed via **Azure Pipelines** or GitHub Actions, triggered by
  cron/Task Scheduler/Control Room.

→ See `references/python-rpa.md` for `rpaframework` module map, Producer/Consumer skeleton, and
pywinauto vs. Selenium decision guide. See `references/python-pom-pattern.md` for the full POM
project structure and base-page/page-object code pattern. See `references/azure-devops-cicd.md`
for the complete Azure Repos branching model, Azure Pipelines YAML, and deployment pipeline for a
Python + POM RPA project.

### C# (custom activities / invoked code)

- Reach for C# only when: (a) Studio's native activities can't express the logic cleanly, (b) you
  need to package reusable logic as a versioned NuGet activity for other developers, or (c)
  performance requires it (heavy string/regex parsing, complex object manipulation).
- Follow standard .NET conventions: PascalCase public members, `async`/`await` for I/O, proper
  `IDisposable` handling for COM/file handles (a leaked Excel/Word COM object is a classic RPA bot
  memory leak), XML doc comments on every public activity property (they surface as Studio
  tooltips).
- Package as a NuGet activity package with semantic versioning, published to a private feed
  (Orchestrator/Azure Artifacts) — never copy-pasted `.dll`s between projects.

---

## Lifecycle Stage 4 — Test

- **Unit level**: test each reusable workflow/component in isolation with known-good and
  known-bad inputs (Test Manager test cases in UiPath, PAD's native Testing module, `pytest` in
  Python).
- **Integration/E2E**: full run against a test environment with masked/synthetic data covering
  every exception path enumerated in the PDD — not just the happy path.
- **UAT**: business signs off against the PDD's acceptance criteria, not against "it ran once."
- **Regression**: re-run the full suite whenever a target application changes (version bump,
  UI update) — UI-dependent automations are uniquely fragile to upstream changes; track target
  app versions as a dependency.
- **CI-gated testing (Python)**: `pytest` + coverage threshold + `ruff`/`mypy --strict` run as
  required pipeline stages, not a manual pre-merge step — see `references/azure-devops-cicd.md`
  for the full Validation-stage breakdown (unit/UI/data/integration/regression test types and
  tool mapping).
- **Don't rely on brainstormed test cases alone**: derive coverage systematically — equivalence
  partitioning and boundary value analysis on every input, decision-table testing on every
  business-rule combination, state-transition testing on every process state, and an FMEA
  (Failure Mode and Effects Analysis, scored by Severity x Occurrence x Detection) performed
  during Solution Design to enumerate and prioritize failure modes before test cases are written,
  not after a gap surfaces in production. See `references/testing-quality-assurance.md` for the
  full methodology, resilience/chaos testing guidance, and platform-specific testing mechanics
  (including Power Automate Cloud's Flow Checker/Test Flow/static-result mocking and PAD's native
  Testing module).

---

## Lifecycle Stage 5 — Deploy & Operate

- **Environments**: Dev → Test/UAT → Production, each with its own Orchestrator tenant/folder (or
  Control Room workspace, or Azure DevOps Environment for Python deployments) and its own
  credentials/assets — never point a Dev bot at Production credentials "just to test."
- **Packaging**: versioned `.nupkg` (UiPath) or a wheel/sdist/Docker artifact (Python, via
  `python -m build`), published through a pipeline (Azure DevOps Pipelines/GitHub Actions +
  `uipcli`), never manual drag-and-drop publish to Production Orchestrator.
- **Scheduling & triggers**: queue-driven (new item → trigger) preferred over blind time-based
  polling where the source system supports it; time-based triggers must account for business
  calendar (holidays, month-end).
- **Monitoring**: Orchestrator dashboards/alerts on failed jobs and queue item age; Python bots
  emit structured logs + metrics to the same observability stack as any other service (Application
  Insights or equivalent).
- **Hypercare**: 2–4 weeks of active monitoring post-go-live with a defined escalation path and
  daily exception review before handing off to standard support/CoE operations.

→ For a Python + POM project specifically, see `references/azure-devops-cicd.md` for the full
Azure Repos → Azure Pipelines → Deploy pipeline, including a corrected, working
`azure-pipelines.yml` example.

---

## Cross-Cutting Best Practices

### Continuous Improvement and Pragmatic Innovation

- Improvement means measurably better, not newest/most expensive/most technically impressive —
  the simplest design that correctly and reliably solves the actual, present problem beats a more
  sophisticated one built for a hypothetical future requirement (KISS, YAGNI).
- **Eliminate and simplify a process before automating or re-automating it** — automating a
  broken or unnecessarily complex process makes bad output faster, not better. Check whether
  removing a step achieves the goal before adding automation around it.
- Run improvement as a disciplined loop, not an ad hoc impulse: identify a measured friction
  point, pilot a small change, measure the actual effect, then roll out through the same
  governance as any other change — or revert and record why. When several ideas compete for
  limited time, score them (impact/confidence/ease) rather than defaulting to whoever argued
  loudest.
- Calibrate review rigor to reversibility — a low-risk, easily-reversible change doesn't need the
  same ceremony as a change touching shared infrastructure, Production credentials, or many
  downstream processes.
- **Innovation never bypasses existing governance.** A simpler credential shortcut that skips the
  vault mechanism is a regression, not an improvement; every change still goes through code
  review, CI gates, DLP/connector governance, and ALM/change control regardless of how small or
  clever it is.

→ See `references/continuous-improvement-innovation.md` for the full framework (Lean waste
elimination mapped to RPA, the Plan-Do-Check-Act improvement cycle, ICE prioritization scoring,
the reversibility/"two-way door" calibration model, and a working pre-adoption checklist) and for
where team/company-specific standards belong once supplied.

### Exception Handling (the single most-checked thing in an RPA code review)

- Every process-level `Try Catch` distinguishes **Business Exception** (`BusinessRuleException` in
  UiPath / a custom `BusinessException` class in Python) from **System Exception** — never a bare
  `catch (Exception)` that swallows both the same way.
- System exceptions get a bounded retry policy (from Config, not hardcoded) before escalating;
  business exceptions never retry — they're expected outcomes, logged and reported to the business.
- **Never silently swallow an exception.** Every catch block logs (with stack trace for system
  exceptions) and updates the transaction/work-item status — a bot that "just continues" on
  unknown error states is a governance failure.
- Global exception handler (REFramework's `Set Transaction Status` / a top-level
  Producer/Consumer `except` in Python) as the last line of defense — never rely on every
  individual activity being wrapped.

### Security

- No hardcoded credentials, API keys, or connection strings — ever, in any language. Orchestrator
  Credential Store / Assets, Azure Key Vault, or environment-injected secrets in CI/CD only.
- Principle of least privilege for the bot's service account — scoped to exactly what the process
  needs, not a shared admin account reused across bots.
- Mask/redact PII and credentials in logs — log the transaction key, never the payload containing
  sensitive fields.
- Screen recording/screenshots on failure (common for debugging) must be reviewed for
  sensitive data exposure before being stored or emailed.

### Documentation & Governance

- Every bot has: PDD, SDD, a versioned README/runbook (what it does, how to restart it, who to
  contact), and an exception matrix mapping error message → cause → resolution.
- Change control: any workflow change goes through the same PR/code-review process as application
  code — no direct edits in Production Orchestrator/Studio against a live package.
- CoE governance: maintain a bot inventory (owner, business owner, criticality, last-tested date,
  dependencies) — untracked "shadow bots" are the most common cause of production incidents.

→ See `references/governance-security.md` for the CoE operating model, credential management
patterns, and full pre-go-live checklist.

### Code Quality (applies to both UiPath workflows and Python/C# code)

- Single Responsibility per workflow/function; no workflow/file that "does everything."
- Reusable components live in a shared library, versioned and consumed via package reference —
  never copy-pasted between projects.
- Static analysis in CI: Workflow Analyzer (UiPath, via `uipcli`) / Ruff + mypy --strict (Python) /
  Roslyn analyzers (C#) — zero warnings policy, same as any other production codebase.

### Git & Source Control

- **Everything** is source-controlled, including `.xaml` (Studio has native Git integration with
  XAML-aware diffing) and PAD flow exports — no automation artifact lives outside version control.
- **Branch strategy**: `main` (production-released) / `develop` (integration) /
  `feature/<short-description>` / `release/<version>` / `hotfix/<short-description>` — feature
  branches merge to `develop` via PR, `release/*` branches stabilize before merging to `main`, and
  `main` is what CI publishes to Production Orchestrator/Control Room.
- **Commit messages**: Conventional Commits, describing _what changed and why_ — `"Added invoice
validation workflow"`, `"Fixed queue retry logic"`, never `"changes"`, `"fix"`, `"update"`.
- PR review required before merge to any branch that triggers a Production or UAT publish — no
  direct commits to `main`.

### Debugging Methodology

A senior developer follows a fixed sequence, not guesswork:

1. **Reproduce** the issue reliably (same input, same environment) before touching anything.
2. **Analyze logs** — the structured logs from the Cross-Cutting Exception Handling standard are
   what make this possible; if logs are insufficient to diagnose, that itself is a defect to fix.
3. **Isolate the layer**: input data problem? Environment/config problem (Dev vs. Prod
   difference)? Target application problem (version change, UI update)? Bot code/logic problem?
   Infrastructure problem (network, robot machine resource exhaustion)?
4. **Determine root cause** — not just the symptom; a selector failure is a symptom, an
   application UI update is often the root cause.
5. **Implement a permanent fix**, not a workaround. A `Delay` added to "fix" a timing issue without
   understanding _why_ the timing changed is technical debt, not a fix — document the real cause
   even if the immediate patch is small.

### Performance Optimization Mindset

Before optimizing anything, ask in this order:

- Can this UI interaction be replaced by an API or direct database call? (Highest-impact change,
  almost always.)
- Can this loop be reduced or vectorized (e.g., bulk SQL operation instead of row-by-row UI entry)?
- Are selectors as specific/fast as possible (avoid overly broad selectors that force UiPath to
  scan large UI trees)?
- Can independent items be processed in **parallel** (multiple Performer robots via
  Dispatcher/Performer) rather than serially?
- Is queue-based processing used where applicable, so throughput scales with robot count instead
  of being capped by a single sequential run?

### Regular Expressions Across Platforms

Regular expressions are a cross-cutting tool throughout every platform in this skill — used for
input validation before `Type Into` and similar UI write activities, cleaning and extracting
values from `Get Text`/scraping/OCR output, normalizing data between systems, and processing
text in Python and Power Automate Desktop flows. Always validate and normalize scraped or typed
data with a pattern rather than assuming clean input; always raise a `BusinessException` (not a
silent continue) when a value doesn't match its expected format. See
`references/regex-in-rpa.md` for the full reference: syntax cheat sheet, platform-specific
mechanics (UiPath VB.NET, Python `re`, PAD native regex actions, Power Automate Cloud
limitations), the validate-normalize-type workflow for UI field interaction, OCR-specific
defensive patterns, debugging methodology, and performance guidance.

---

## Career Path — RPA to Data Engineering

RPA and data engineering share the same underlying discipline (move data reliably, at scale,
without a human watching it run) under different vocabulary — queues map to pipeline
runs/partitions, Config-driven design maps to pipeline parameters, business/system exception
classification maps to data-quality/infrastructure failure classification, and this skill's Git +
Azure Pipelines CI/CD discipline applies unchanged to pipeline code. When the user is transitioning
from RPA developer toward data engineering, or asks how their RPA experience applies to data work,
use `references/data-engineering-transition.md` — it maps exactly what transfers, what the real
gaps are (Airflow/ADF orchestration, polars/Spark at scale, dbt, dimensional modeling, data
quality tooling, CDC), a learning sequence ordered to reuse existing skills first, and a concrete
practice project that exercises every gap using tools already covered in this skill. See also
`references/uipath-databricks-integration.md` — UiPath's own production implementation of this
pattern (Spark Structured Streaming on Databricks for real-time event ingestion) and the
Databricks Agent connector that lets a Maestro agentic process call a Databricks AI model as
an external participant, bridging RPA orchestration with ML inference at the platform level.

---

## Output Format Guide

| Task                                      | Primary Output                                                                                                                                                        |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Process discovery                         | PDD sections: as-is process, exceptions, volumes, complexity score                                                                                                    |
| Solution design                           | SDD sections: architecture diagram (described), exception taxonomy, NFRs                                                                                              |
| UiPath workflow                           | `.xaml`-equivalent pseudocode/structure description + Config.xlsx schema                                                                                              |
| Python bot                                | Package skeleton (`pyproject.toml`, `src/` layout) + Producer/Consumer code                                                                                           |
| C# custom activity                        | `.cs` file with XML doc comments + NuGet packaging notes                                                                                                              |
| Power Automate Cloud flow                 | Trigger type + connector chain + Scope-based error handling design                                                                                                    |
| Power Automate architecture/design review | Layered structure + control-flow construct choice + named orchestration pattern (see `references/power-automate-architecture.md`)                                     |
| Power Automate Desktop flow               | Main flow + subflow breakdown, variable naming, error-branch design                                                                                                   |
| SQL Server integration                    | Parameterized query/stored proc + transaction boundaries                                                                                                              |
| Exception handling review                 | Exception matrix (error → business/system → handling → escalation)                                                                                                    |
| Test plan                                 | Test case table: scenario, input, expected outcome, exception path covered                                                                                            |
| Failure mode / coverage analysis          | FMEA table (failure mode, Severity/Occurrence/Detection, RPN) plus equivalence-class/boundary/decision-table coverage — see `references/testing-quality-assurance.md` |
| Debugging/RCA                             | 5-step root-cause writeup: symptom → layer isolated → root cause → permanent fix                                                                                      |
| Governance/CoE review                     | Checklist scored Pass/Fail + prioritized remediation                                                                                                                  |
| Python + POM structure                    | `references/python-pom-pattern.md` project layout + base-page/page-object code                                                                                        |
| Azure DevOps CI/CD pipeline               | `references/azure-devops-cicd.md` branching model + `azure-pipelines.yml`                                                                                             |
| Code review                               | `references/code-review-checklist.md` checklist scored against the diff                                                                                               |
| Environment/tooling setup                 | `references/tooling-environment-setup.md` install/config walkthrough                                                                                                  |

Always justify the architectural choice (framework, attended/unattended, queue vs. polling) — not
just deliver the artifact.

---

## Reference Files

- `references/continuous-improvement-innovation.md` — Lean/Kaizen waste elimination applied to
  RPA, eliminate-before-automate sequencing, the PDCA improvement loop, ICE prioritization
  scoring, reversibility-calibrated review rigor, a pre-adoption checklist, and a tracker for
  which team/company-specific standards have been supplied and integrated elsewhere vs. still
  genuinely open
- `references/uipath-reframework.md` — Comprehensive architectural theory, coding mechanics,
  and enterprise standards for the Robotic Enterprise Framework (REFramework): Finite State Machine
  (FSM) formalism, automata and ACID/idempotency guarantees, structural state anatomy (Init, Get
  Transaction Data, Process, End Process), component-level XAML walkthrough (Main, InitAllSettings,
  InitAllApplications, GetTransactionData, Process, SetTransactionStatus, RetryCurrentTransaction,
  TakeScreenshot, CloseAllApplications, KillAllProcesses), architectural applications (Queue-driven
  Dispatcher/Performer, Tabular/DataTable without queues, File/Directory batching, Long-Running Action
  Center), exception taxonomy, three-tier retry model (Activity vs Framework vs Queue auto-retry) and
  elimination of the double-retry anti-pattern, circuit breaker pattern (ConsecutiveSystemExceptions),
  session hygiene/memory leak prevention for 24/7 robots, structured logging/observability, Workflow
  Analyzer rules, and a 15-point production sign-off checklist
- `references/uipath-standards.md` — Config.xlsx schema, Workflow Analyzer
  ruleset, Orchestrator queues/transactions design, selector/Object Repository best practices,
  custom C# activity packaging, Test Manager workflow, VB vs. C# expression-language trade-offs
  (verified performance/completeness/Studio Web implications), workflow design/layout standards
  (Sequence vs. Flowchart vs. State Machine, file naming, annotations, decomposition), Windows vs.
  Windows-Legacy project compatibility, logging levels, and this team's Organization-Specific
  naming conventions and Azure DevOps ALM flow for UiPath
- `references/linq-expressions.md` — LINQ (Language-Integrated Query) in UiPath and RPA:
  why LINQ replaces For Each Row loops, required namespaces (System.Linq, System.Data,
  System.Data.DataSetExtensions), VB.NET query syntax vs. method/lambda syntax with side-by-
  side comparisons, C# equivalents, deferred vs. immediate execution (the most common source
  of subtle bugs in Studio expressions), and a 17-pattern DataTable cookbook covering: filter
  by value/multiple conditions/case-insensitive/date range, DBNull handling, remove empty
  rows, sort (single/multi-key), projection (extract columns as lists), distinct/deduplicate
  (DataRowComparer.Default), Count/Any/All, First/FirstOrDefault/Single, aggregate (Sum/Avg/
  Max/Min), GroupBy with aggregation, inner join and left outer join of two DataTables, set
  operations (Intersect/Except/Union/Concat), column enumeration by type, pagination
  (Take/Skip); LINQ on Lists/Arrays/Dictionaries; operator quick-reference table (deferred vs.
  immediate, Assign vs. Invoke Code); debugging guide (CopyToDataTable empty-result trap,
  namespace errors, DBNull object-reference errors, silent string-mismatch diagnosis);
  performance guidance and the threshold for switching to Python/Polars
- `references/python-rpa.md` — `rpaframework`/Robocorp module map, Producer/Consumer skeleton code,
  pywinauto vs. Selenium vs. Playwright decision guide, packaging and CI/CD for Python bots
- `references/documentation-templates.md` — full PDD, SDD, exception matrix, and test case
  document templates
- `references/testing-quality-assurance.md` — the cross-platform testing methodology: systematic
  test design techniques (equivalence partitioning, boundary value analysis, decision tables,
  state transition testing), FMEA-based failure mode enumeration, the full test type taxonomy,
  resilience/chaos testing, test data management, verified Power Automate testing mechanics
  (Flow Checker, Test Flow, static-result mocking, the native PAD Testing module), and this team's
  Organization-Specific four-phase RPA Testing Checklist
- `references/governance-security.md` — CoE operating model, bot inventory schema, credential
  management patterns (CyberArk/Key Vault/Orchestrator), pre-go-live checklist, hypercare plan,
  and this team's Organization-Specific Orchestrator access model, robot type governance, and
  asset handling rules
- `references/power-automate-cloud.md` — trigger-type decision table, org-specific naming
  conventions (action name format, variable initialization, comments/intent discipline,
  connection verification), trigger selection for development, concurrency control, Scope-based
  Try/Catch/Finally error handling, approvals, connector/batch efficiency, DLP governance,
  licensing, monitoring; the default starting point for Power Automate work
- `references/power-automate-architecture.md` — architectural layering, control-flow construct
  selection (Condition/Switch/Apply to each/Do Until mapped to Workflow Patterns), verified
  concurrency limits and the Do Until silent-success trap, state management under concurrency
  (Compose/select over shared variables), child-flow decomposition mechanics and security
  implications, orchestration patterns (fan-out/fan-in, content-based routing, saga/compensating
  actions, idempotency)
- `references/power-automate-desktop.md` — PAD project structure, subflow reuse, variable/error
  conventions, action priority order, credential handling, unattended-run machine-group guidance,
  Solutions-based ALM; use for the UI-automation leg of a process only
- `references/regex-in-rpa.md` — regular expressions across the full automation stack: syntax
  cheat sheet, UiPath VB.NET Matches/IsMatch/Replace/named-groups patterns, validate-normalize-
  type workflow for Type Into and UI field interaction, Get Text / OCR output cleaning, OCR
  engine selection guide (Tesseract, Microsoft OCR, Azure Computer Vision, Google Cloud Vision,
  UiPath Screen OCR, UiPath Document OCR — org-specific table plus decision criteria, pre-
  processing, confidence scoring, and ensemble pattern), selector wildcard vs. regex distinction,
  Python re module best practices, Power Automate Cloud limitations and workarounds, PAD native
  regex actions, common RPA patterns (dates, currencies, IDs, phone numbers), debugging workflow
  (false negative/positive/wrong-extraction diagnosis), and performance (compiled patterns,
  avoiding catastrophic backtracking)
- `references/sql-server-standards.md` — query/procedure standards, indexing, transactions,
  connection security, SSMS workflow
- `references/citrix-automation.md` — integration priority order, CV/OCR/anchor technique
  selection, synchronization patterns, risk framing for the SDD
- `references/code-review-checklist.md` — standalone reliability/maintainability/performance/
  security/deployment checklist for reviewing any RPA artifact (UiPath, PAD, Python, SQL)
- `references/tooling-environment-setup.md` — standard developer machine setup: UiPath (Developer
  install), Power Automate Desktop, Citrix Workspace, Forticlient VPN, PyCharm, VS Code, Visual
  Studio 2022, SQL Server 2022 + SSMS, Azure Storage Explorer, Git, FileZilla, Firefox, Sublime
  Text, Notepad++, 1Password
- `references/python-pom-pattern.md` — Page Object Model pattern for Python UI automation:
  `src/`-layout project structure, layer responsibilities, base-page/page-object code, Robot
  Framework/`rpaframework` relationship
- `references/azure-devops-cicd.md` — Azure Repos branching models (GitFlow-style vs. trunk-based),
  Azure Pipelines stages, a corrected working `azure-pipelines.yml`, validation/testing tool
  mapping, deployment targets, and the suggested Python RPA technology stack
- `references/data-engineering-transition.md` — RPA-to-data-engineering skill mapping, the real
  gaps to close (Airflow/ADF, polars/Spark, dbt, dimensional modeling, data quality tooling, CDC),
  an ordered learning sequence, and a practice project combining existing and new skills
- `references/uipath-databricks-integration.md` — four-part UiPath+Databricks integration
  reference: (1) Real-time event ingestion pipeline — the previous dual-pipeline problem
  (30-min latency, duplicated storage, high cost), unified Spark Structured Streaming
  architecture (filter/flatten/parse/enrich stages, Lakeflow Jobs, ~27s median latency,
  ~40K events/sec, at-least-once delivery, raw message preservation, DataFrame API, Spark
  execution model, monitoring, schema evolution, throughput tuning); (2) Databricks Agent
  connector for Maestro — Query Serving Endpoint and Manual variant, JSON payload, Maestro
  expression handling, prompt engineering for structured output, type handling, USE CATALOG
  permission; (3) Document intelligence — `ai_parse_document` full reference (syntax,
  output schema version 2.0, all 10 element types, bounding boxes, confidence scores),
  companion AI Functions (`ai_extract` v2.1 with citations, `ai_classify`, `ai_summarize`,
  `ai_prep_search`), full composable SQL pipeline (parse/classify/extract/prep_search in
  one query), Lakeflow Declarative Pipeline incremental pattern, UiPath-vs-Databricks OCR
  positioning table, operational considerations (error_status, confidence thresholds, page
  limits, schema pinning, data security); (4) RPA-to-DE concept mapping table
