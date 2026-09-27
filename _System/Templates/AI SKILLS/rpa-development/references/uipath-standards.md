# UiPath Standards — Deep Reference

> Refreshed against official UiPath documentation (docs.uipath.com) and forum/product sources,
> July 2026. UiPath ships frequently — treat product-surface details (Studio family, Maestro, CLI)
> as accurate as of this date and verify against docs.uipath.com before relying on them for a
> version-sensitive decision (e.g., exact CLI flags, which Studio SKU a feature ships in).
>
> Sections marked **"Organization-Specific"** reflect this team's actual internal documentation
> (provided directly by the user), not independently-verified UiPath product documentation. They
> are followed as this team's binding standard where they exist; the rest of this file is
> general/official UiPath guidance used to fill gaps the internal documentation doesn't cover.
> Where the two overlap, the organization-specific version takes precedence.

## Organization-Specific Naming and Design Conventions

Per this team's internal UiPath Best Practices documentation:

- **Solution naming**: `<Market>_<Group>_<Process>` — short but descriptive, includes the market/
  region the automation serves. Example: `AU_ANX_Service_Order` for an Australia-market, Auto
  Nexus group, Service Order Report extraction. Add a solution description for further detail;
  optional but recommended.
- **Variables**: `thisIsCamelCase`; prefix with a **datatype abbreviation**, not a generic `var` —
  `str` (string), `int` (integer), `arr` (array), `dt` (DataTable), etc. Meaningful, distinct,
  not overly long.
- **Arguments**: `thisIsCamelCase` with a **direction prefix**: `In_CustomerName`,
  `Out_InvoiceTotal` — note this team's convention capitalizes the direction prefix
  (`In_`/`Out_`), which differs from the lowercase `in_`/`out_`/`io_` convention used elsewhere
  as a general default in this skill; follow the capitalized form for this team's projects.
- **Workflow files**: short, meaningful, verb-led name describing the task —
  `ExtractingCustomerInformation`, matching the same naming discipline as variables/arguments.
- **Activities and containers**: rename away from defaults (`Assign`, `If`) — a default-named
  activity is materially harder to trace when troubleshooting. Where keeping a default name is
  unavoidable, append a suffix describing the action: `Assign - Extract Customer Name`.
- **Assets and Queues** (Orchestrator): name to include the process they serve, and **always**
  add a description — an undescribed asset/queue is a recurring source of confusion for anyone
  other than its author.
- **Folder organization within the project**: group workflows by the application they interact
  with (a dedicated `SAP` folder for every workflow touching SAP, for example) or by function
  (`Data Processing` for data-manipulation workflows); keep REFramework's config under a `Config`
  folder. This is a structural extension of this skill's general "one `.xaml`, one responsibility"
  principle — folders make that discipline visible at the project level, not just the file level.

## Current Platform Landscape (Studio Family + Maestro)

UiPath's platform has split into distinct products that work together; picking the wrong one for
the task is a common avoidable mistake.

- **Studio Desktop** (Windows-installed) — the full-featured IDE for complex, deep UI automation:
  Citrix/mainframe, custom C# activities, REFramework, on-prem targets. This is what "Developer
  installation" means in practice, and it's still the right default for enterprise RPA developer
  work covered by this skill.
- **Studio Web** (browser-based, no install) — cross-platform (Windows/Mac/Linux), targets modern
  web/SaaS apps (Microsoft 365, Google Workspace, Salesforce), runs unattended by default on
  serverless cloud robots (can also target desktop machines when UI automation is needed). Projects
  are interchangeable with Studio Desktop — open a Studio Web project in Desktop and vice versa.
  Reach for it for citizen-developer-friendly or lightweight cloud-app automation; reach for Studio
  Desktop for anything Citrix/legacy/custom-activity-heavy. **Compatibility constraint (verified
  official)**: a project is only editable in Studio Web if it's a cross-platform "process" project
  using **VB** for expressions — any Windows project (regardless of language) and any
  cross-platform project using C# can be *saved* to the cloud but not opened/edited in Studio Web.
  **Flowchart workflows cannot be opened in Studio Web at all**, regardless of language. If Studio
  Web interoperability is a requirement, this constrains both the language and the workflow-type
  choice made in Studio Desktop up front — decide before starting the project, not after.
- **StudioX** — simplified, business-user-oriented desktop variant; not the target of this skill's
  senior-developer guidance but relevant if reviewing citizen-developer output.
- **Maestro** — a newer orchestration layer, distinct from Orchestrator's job/queue scheduling. It
  models end-to-end business processes (claims, loans, procurement) using BPMN (structured
  diagrams), Flow (developer-first sequential workflows), or Case Management (long-running,
  exception-heavy work), and coordinates RPA robots, AI agents, and human tasks within one process.
  **Maestro does not replace REFramework or Orchestrator queues** — the official guidance is
  explicit: use Orchestrator queues and REFramework/Performers for robust, queue-based UI-automation
  transaction processing; use Maestro to orchestrate the broader process around those
  transactions (start jobs, sequence steps across robots/agents/people, handle long-running state).
  A REFramework performer processing invoice line items and a Maestro process orchestrating the
  end-to-end invoice lifecycle (intake → performer robots → human approval → payment) are
  complementary, not competing, patterns. Treat Maestro as relevant once a process needs
  cross-actor orchestration (agents + robots + humans) rather than as a default for new work.

## Expression Language: VB vs. C# (project-level choice, verified official trade-offs)

Every Studio project sets an **expression language** at creation — VB or C# — governing every
`Assign`, `If`/`Switch` condition, and `Invoke Code` activity in the project. This is a distinct
decision from building external custom activities in C# (covered below); it governs the language
used *inside* ordinary workflow expressions throughout the project, and it cannot be changed
after the fact without rework.

- **Default recommendation for this skill: VB**, for three official, documented reasons — not
  inertia:
  1. **Performance**: UiPath's own documentation states design-time and runtime performance of
     C# projects is measurably lower than VB.NET, and explicitly recommends VB when runtime
     performance is essential.
  2. **Language completeness**: Studio's C# support compiles against C# version 5 — it does not
     support several conveniences taken for granted in modern C# (string interpolation, the
     null-conditional `?.` operator, the null-coalescing `??` operator, coalescing assignment
     `??=`, increment expressions, or the `nameof()` operator, which is explicitly rejected as
     invalid). A developer bringing modern C# habits into Studio will hit these limits quickly.
  3. **Studio Web and Flowchart compatibility**: as above — C#-language projects and any Flowchart
     workflow lose Studio Web editability.
- **When C# is still the right choice**: a team whose engineers are C#-native and where Studio Web
  interoperability and Flowchart workflows are both irrelevant to the project — familiarity and
  consistency with a team's broader .NET codebase can outweigh the performance/completeness
  trade-offs for that team, but this should be a deliberate, documented choice at project
  kickoff, not a default.
- **Do not mix languages across a library and its consumers casually**: default argument values
  defined in a library project using language-specific expressions are not accessible from a
  project in the *other* language once that library is installed — a VB library consumed by a C#
  project (or vice versa) can silently lose default argument behavior. Standardize on one
  language per shared-library ecosystem, and document the choice in the library's README.
- **Where this is configured**: per-project at creation, or as a Studio-wide default via *Use C#
  Language* in Studio Settings (Studio Pro profile only — Studio and StudioX profiles always use
  VB, which is itself a signal of where UiPath's own defaults sit).

**LINQ in expressions:** VB.NET expression syntax is the default language for all LINQ queries
used inside `Assign` activities, `For Each` conditions, and `Invoke Code` bodies. LINQ is the
primary mechanism for filtering DataTables, transforming collections, joining tables, and
aggregating data without using `For Each Row` loops. See `references/linq-expressions.md` for
the full reference: VB.NET vs. C# syntax, required namespaces, deferred vs. immediate
execution, and a cookbook covering the 17 most common DataTable and collection patterns used
in UiPath RPA workflows.

## Workflow Design and Layout Best Practices

Beyond variable/argument naming conventions (below), the shape and structure of the workflows
themselves is a frequent, avoidable source of unmaintainable projects:

- **Sequence vs. Flowchart vs. State Machine — choose deliberately, not by habit**:
  - **Sequence**: linear, top-to-bottom logic with no complex branching — the default for most
    invoked sub-workflows (a single business function: validate this, extract that).
  - **Flowchart**: multiple branching paths, especially where the branching logic itself is the
    point (decision-heavy routing) — more visually reviewable than a deeply nested `If`/`Switch`
    chain inside a Sequence, at the cost of losing Studio Web editability (see above).
  - **State Machine**: the process has genuinely distinct states with defined transitions between
    them (REFramework itself is a State Machine: Init, Get Transaction Data, Process, End
    Process) — reach for this when the process is naturally state-based, not as a default project
    skeleton for simple linear work.
- **One `.xaml`, one clearly named responsibility**: a workflow file should be reviewable without
  extensive scrolling; if a Sequence grows past roughly one screen of activities, extract the
  excess into an invoked child workflow via `Invoke Workflow File` rather than letting one file
  keep growing — the same Single Responsibility discipline this skill applies to Python
  functions and Power Automate child flows, applied at the `.xaml` level.
- **File naming**: PascalCase, verb-noun pattern describing what the workflow does —
  `GetInvoiceData.xaml`, `ValidateCustomerRecord.xaml` — never `Process1.xaml` or a name that only
  makes sense with tribal knowledge of the project's history.
- **Annotations**: use Studio's native annotation feature (right-click an activity or workflow →
  Add Annotation, or the docked-annotation Studio setting) to document *why* a non-obvious design
  choice was made directly on the workflow — this travels with the `.xaml` in source control,
  unlike an external design doc that drifts out of sync with the implementation. **Every workflow
  file should carry a top-level annotation covering, at minimum**: a description of what the
  workflow does, its input/output arguments and their expected data types, and its pre-conditions
  and post-conditions (the state the target application/data must be in before the workflow runs,
  and the state it's left in afterward) — this is what lets another developer safely invoke the
  workflow without opening it first. Annotate variables and arguments individually too, via the
  Variables/Arguments panels, describing their purpose.
- **Comments**: use the `Comment` activity inline to explain non-obvious logic at the point it
  occurs, distinct from the top-level workflow annotation described above.
- **Decompose into subprocesses deliberately**: break a process into subtask/subprocess workflow
  files invoked from a central control workflow via `Invoke Workflow File` — there's no universal
  rule for exactly where to split, but separating business logic from UI-automation/integration
  components is the guiding principle, consistent with this skill's general architectural
  layering (see `references/power-automate-architecture.md`'s layering model, applied identically
  in spirit to UiPath).
- **Layout discipline**: keep activity flow visually top-to-bottom (Sequence) or
  left-to-right/top-to-bottom without crossing connector lines (Flowchart) — a workflow that's
  visually tangled is a maintenance cost independent of whether the logic is correct, and is a
  legitimate Workflow Analyzer / code-review finding on its own.
- **Avoid deeply nested `If`/`Switch` activities**: past two or three levels of nesting, either
  restructure as a Flowchart (branching is the point) or extract the nested logic into an invoked
  child workflow — the UiPath-workflow equivalent of the same anti-pattern this skill flags for
  Power Automate (`references/power-automate-architecture.md`'s Condition-vs-Switch guidance) and
  for deeply nested code in general. Avoid nested Flowcharts specifically as well — a Flowchart
  invoking another Flowchart is harder to trace visually than extracting the inner one as an
  invoked Sequence-based subprocess.

## Project Compatibility: Windows vs. Windows-Legacy

Distinct from the VB/C# expression-language choice above, every project also has a **compatibility**
setting — Windows, Windows-Legacy, or cross-platform — governing which runtime/activity set it
targets. **Windows is the current default for new projects**; Windows-Legacy remains supported but
is increasingly feature-frozen: recent Studio releases have shipped capabilities (global
variables/constants in the Data Manager, the newer design experience, customizable activity layouts
from libraries, among others) that are simply unavailable in Windows-Legacy projects. Treat an
existing Windows-Legacy project as a migration candidate, not a permanent steady state.

**Converting an existing project to Windows compatibility:**
- If the **"Convert to Windows"** link is visible in Studio: enable "Create a new project" (do not
  convert in place), give the new project a name distinct from the Windows-Legacy original, choose
  the target location, convert, then open and fully test the Main workflow before publishing the
  migrated version to Orchestrator.
- If the link isn't shown: confirm the Studio version is 2021.10.0 or later (update via the
  installer distributed through Orchestrator if not), then retry.
- **Known post-conversion failure mode**: selector errors appearing only after conversion, not
  resolved by updating packages, have been traced (by this team) to a specific UiPath Studio
  setting changed as a side effect of conversion — if this occurs, check recent Studio settings
  changes around selector/UI-automation behavior before assuming the selectors themselves are
  broken; this is a settings regression, not necessarily a selector redesign problem.

## Organization-Specific Azure DevOps ALM for UiPath

Per this team's internal Azure DevOps integration documentation — this is the binding process for
this team's UiPath projects specifically, distinct from the general Python/Azure Pipelines content
in `references/azure-devops-cicd.md`:

- **Publishing directly from UiPath Studio to Orchestrator is disabled.** All publishing happens
  through the Azure DevOps pipeline — there is no sanctioned manual-publish path.
- **Pipeline creation is restricted to the team's UiPath subject-matter expert (SME) role** — an
  individual developer does not create or modify the deployment pipeline itself, only uses it.
- **Branching flow**: `feature-<Feature Name>` branches (e.g. `feature-initialProjectSolution`) →
  pull request into `dev` → approve and complete the PR to merge → pull request from `dev` into
  `main` → approve and complete the PR to merge → merging to `main` automatically triggers the
  deployment pipeline. **Never commit directly to `main`.**
- **Repository naming convention**: `UiPath_<Tenant Name>_<Region>_<Market>_<Project Name>` —
  e.g. `UiPath_COE_APAC_SG_TestProject`.
- **New project setup** (first-time Git integration for a UiPath project): create the Azure DevOps
  repo (following the naming convention above) → create the `dev` branch → create the initial
  feature branch → clone the repo locally via VS Code → create a new UiPath project in Studio
  named to match the repo → copy the new project's files into the cloned repo's working directory
  (**never delete the hidden `.git` folder** in the process) → reopen the project from that
  location in Studio, confirm Git is detected as initialized, and confirm the feature branch (not
  `main`) is selected before any development begins.
- **Committing changes**: from Studio's Project panel, right-click the project → `Commit` → enter
  commit notes → `Commit and Push`. (VS Code's clone/checkout tooling is an equally valid
  alternative path for the same operation.)

## REFramework Anatomy

REFramework (Robotic Enterprise Framework) is the default state-machine skeleton for any
unattended/production process. Its states:

1. **Init** — reads `Config.xlsx`, opens applications, establishes connections. Runs once, and
   again on `SystemException` retry (so it must be idempotent: safe to re-run without duplicating
   side effects).
2. **Get Transaction Data** — pulls the next work item from the queue (Orchestrator Queue,
   database row, email, Excel row). Returns `Nothing`/`null` when queue is empty → transitions to
   End Process.
3. **Process** — the actual business logic. Wrapped in a `Try Catch`:
   - `catch (BusinessRuleException)` → log, `Set Transaction Status = Failed (Business)`, continue
     to next item.
   - `catch (Exception)` → log with full detail, `Set Transaction Status = Failed (Application)`,
     framework decides retry vs. escalate based on `Config("MaxRetryCount")`.
4. **Set Transaction Status** — writes back to the queue (Success/Business Exception/System
   Exception), increments retry counters.
5. **End Process** — closes applications, sends summary email/report, releases resources.

**Key config-driven values (never hardcoded):**
| Config key | Purpose |
|---|---|
| `OrchestratorQueueName` | Which queue to pull from |
| `MaxRetryCount` | System exception retry ceiling |
| `EmailNotification.To/CC` | Escalation recipients |
| `Timeout.*` | Per-application wait timeouts |
| Asset references | Credential asset names, not the credentials themselves |

## Logging Standards

Log Message activities are the primary source of truth for diagnosing a run, in Studio during
development and in Orchestrator/Elasticsearch in production. UiPath's Log Message activity
supports five levels — use them by their actual defined purpose, not interchangeably:

| Level | Purpose |
|---|---|
| **Trace** | Development/debugging detail — verbose enough that it would clutter production logs; strip or leave disabled once a workflow reaches production. |
| **Info** | Normal progress information — entering/exiting a workflow, a value being processed, a transaction starting. The default level for routine "the bot is working" visibility. |
| **Warn** | Data that needs to stand out from routine Info noise without being an outright failure — an unusual-but-handled condition worth a human noticing on review. |
| **Error** | An error occurred and the robot is attempting to recover and continue with the next item — this is the level for handled System Exceptions in the REFramework sense. |
| **Fatal** | The robot cannot or should not recover — something has gone critically wrong and the workflow must stop. Reserve this for genuinely unrecoverable states, not routine business exceptions. |

**Log at two structural points, at minimum, on every subtask/subprocess ("checkpoints")**: once
on entry and once on exit — this is what makes it possible to tell, from the logs alone, whether a
given subprocess completed successfully without having to reproduce the run. Log at every decision
point (`If`/`Switch` branch taken) as well — this is what lets you reconstruct *which path* a
specific run took after the fact, not just that it finished.

## Exception Handling (UiPath-specific mechanics)

Beyond the Business/System Exception taxonomy already established as a cross-cutting standard in
this skill:

- Wrap workflows where issues commonly occur in `Try Catch`, and structure the `Catch`/`Finally`
  blocks to actively restore the workflow to a known state (close a stuck dialog, reset an
  application) rather than just logging and stopping.
- Use **Retry Scope** for fragile, narrowly-defined steps (a flaky selector, an intermittent
  connection) where a bounded, localized retry is more appropriate than failing the entire
  transaction and relying on REFramework's transaction-level retry.
- **Orchestrator Queues auto-retry** transactions that fail with an Application/System Exception,
  up to the queue's configured retry count — if a process isn't queue-based, it must implement
  equivalent auto-retry logic explicitly (do not assume "it'll just work" without a queue backing
  it).
- Build a **Global Exception Handler** (Project panel → Manage Project Dependencies/Settings, or
  the Global Handler workflow generated via the Project panel) as the last line of defense to
  catch and retry/report failures escaping every individual `Try Catch` — never rely solely on
  per-activity error handling being complete.

## Config.xlsx Schema (standard sheets)

- **Settings** — key/value pairs, everything above
- **Constants** — paths, file extensions, static thresholds
- **Assets** — Orchestrator Asset names the bot will fetch at runtime (never store the asset
  *value* here — only the *name*)
- **Queues** — queue names per environment (Dev/Test/Prod use different queue names to avoid
  cross-environment contamination)

## Workflow Analyzer Ruleset (run before every commit)

Workflow Analyzer is UiPath's built-in static analyzer (Design ribbon → Analyze File/Analyze
Project), checking for inconsistencies without executing the project — distinct from runtime
validation. Per official documentation:

- **Rule ID structure**: `<origin>-<category>-<number>`, e.g. `ST-NMG-001` (Variables Naming
  Convention). Origin prefixes: `ST` = built into Studio, `UI` = UIAutomation.Activities rules,
  `TA` = Application/Test Automation rules (multi-stakeholder project stability).
- **Severity/action per rule**: Error, Warning, or Message (Trace) — configurable per rule; the
  Error List panel filters by these. A rule set to Error blocks execution/publish/source-control
  push when `Enforce Analyzer before Publish` is enabled in Studio settings.
- **Governance at scale**: `Automation Ops` lets a CoE centrally define, configure, and deploy
  Workflow Analyzer rule policies across teams/projects rather than relying on every developer's
  local Studio settings — the correct mechanism for enforcing a CoE-wide ruleset, not just local
  `.editorconfig`-style project settings.
- **Custom rules**: buildable with the `UiPath.Activities.Api` SDK package when built-in rules
  don't cover an org-specific standard (e.g., a mandatory logging pattern); loaded from a custom
  rules location configured in Studio settings.

Non-negotiable rules to keep enabled regardless of ruleset customization:
- No hardcoded credentials/secrets in any activity property
- No `Message Box` in unattended workflows (blocks execution indefinitely)
- No empty `Catch` blocks
- Variable/argument naming convention compliance (camelCase vars, `in_`/`out_`/`io_` args)
- No unused variables/arguments
- Workflow file complexity threshold (flag `.xaml` files exceeding a cyclomatic-complexity-like
  activity count — split into invoked sub-workflows)
- Log Message coverage at decision points (custom rule many CoEs add via the SDK)

**CLI tooling for CI/CD — two generations, know which one a pipeline is using:**
- **Legacy `uipcli`** (`uipcli.exe` / `dotnet uipcli.dll`, .NET-based): `uipcli package analyze
  <project.json>` runs Workflow Analyzer against a governance file and fails the build on
  Error/Warning violations (`--treatWarningsAsErrors`, `--stopOnRuleViolation`,
  `--ignoredRules`); `uipcli package pack`/`deploy` handle packaging and Orchestrator deployment;
  `uipcli test run` executes Test Manager test sets. This remains fully supported for existing
  pipelines and is what most current production CI/CD setups use.
- **New `uip` CLI** (TypeScript-based, broader platform surface, introduced 2025/2026): `uip rpa
  analyze` (with governance policies), `uip rpa pack`, `uip solution pack`, plus commands for the
  newer platform surface (`uip agent pack`, `uip flow init`, `uip maestro init`). This is the
  direction UiPath is consolidating tooling toward — for a new pipeline being built today, check
  docs.uipath.com/uipath-cli for whether `uip` is the currently recommended entry point before
  defaulting to legacy `uipcli`.

Treat any new Workflow Analyzer warning as a build failure, with exceptions requiring an explicit
suppression comment (`--ignoredRules`) + PR justification.

## Selectors & Object Repository

- Prefer the **Object Repository**: reusable, versioned UI descriptors shared across workflows —
  a UI change is fixed once, not in N places.
- Selector fragility ranking (most → least robust): `aaname`/`automationid` > `name` + `role` >
  `text` (locale-dependent, avoid for multi-language deployments) > `idx` (index — breaks the
  moment the UI reorders elements, avoid).
- Use **Anchor Base** / relative-to-anchor activities for UI regions where absolute selectors are
  unstable (dynamically positioned elements).
- For Citrix/virtualized/mainframe: prefer native (if published) app selectors over Computer
  Vision; fall back to CV activities or OCR only when no accessible UI tree exists at all.
- Validate every selector in **UI Explorer** before committing — never hand-edit the underlying
  XML from memory.

## Orchestrator Queues & Transactions

- One queue per process (not shared across unrelated processes); queue item `Reference` = a
  human-readable business key (invoice #, ticket ID) for traceability, not a GUID.
- Set `Priority` meaningfully if SLA differs by item type; use `Postpone` (`Defer Date`) for items
  that must not process before a certain time rather than looping/sleeping in the workflow.
- Queue item `SpecificContent` holds only what Process needs — don't dump entire source records if
  most fields are unused; this also limits PII exposure in the queue.
- Retries: Orchestrator's built-in queue retry (`Max # of retries` on the queue) is separate from
  REFramework's in-transaction retry — decide which layer owns retry logic and document it (usually
  Orchestrator queue retry for System Exceptions, no retry for Business Exceptions).

## Custom C# Activities

- Build as a class library targeting the same .NET version as the Studio project; implement
  `CodeActivity` (synchronous) or `AsyncCodeActivity`/`NativeActivity` for long-running/async work
  so the Orchestrator thread isn't blocked.
- Every public `InArgument<T>`/`OutArgument<T>` property gets an XML doc comment — it becomes the
  tooltip in Studio's Properties panel.
- Dispose COM interop objects explicitly (`Marshal.ReleaseComObject`) when wrapping Excel/Word/
  Outlook interop — this is the #1 cause of orphaned `EXCEL.EXE`/`WINWORD.EXE` processes on
  unattended robot machines.
- Package as NuGet (`.nupkg`), semantic-versioned, published to a private feed (Orchestrator
  activities feed or Azure Artifacts) — consumed via Studio's Manage Packages, never a manually
  copied `.dll` in the project folder.

## Test Manager Workflow

- Link Test Manager test cases to PDD acceptance criteria — every enumerated exception scenario
  gets at least one test case.
- Use **Test Data Queues** or parameterized test cases to run the same test workflow against
  multiple input rows without duplicating test case definitions.
- Mock external systems where a live test environment isn't available (`Test Activities` with
  stubbed responses) so unit-level tests don't depend on flaky third-party uptime.
- Gate Production package promotion on a passing Test Manager run in CI, not a manual "looks fine."

## Sources Consulted (official/primary, July 2026)

- This team's internal UiPath Best Practices, Azure DevOps Integration/Branching, and Legacy-to-
  Windows Conversion documentation, provided directly by the user — the source for every section
  marked "Organization-Specific" above. Followed as this team's binding standard, not
  independently verified against docs.uipath.com.
- docs.uipath.com — Studio, Studio Web, Workflow Analyzer, SDK (custom rules), Automation Ops,
  UiPath CLI (`uip`) and CI/CD integrations (legacy `uipcli`), Maestro overview and
  Maestro/REFramework FAQ, "About Automation Projects" (VB/C# expression language limitations and
  Studio Web compatibility requirements), "Configuring Studio Settings" (Use C# Language setting)
- github.com/UiPath/ReFrameWork — official REFramework template and documentation PDF
- github.com/UiPath/uipathcli — official CLI reference examples
- uipath.com product pages — Maestro, Studio family positioning

Product-surface facts (Studio family lineup, Maestro's role, CLI generations, VB/C# language
limitations) are current as of this refresh; architecture and coding-standard guidance
(REFramework shape, exception taxonomy, naming, selectors, workflow design principles) is durable
and not expected to go stale at the same rate.
