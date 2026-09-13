# Testing and Quality Assurance — Deep Reference

> The synthesis layer for testing across this entire skill. Platform-specific test mechanics
> already documented elsewhere (UiPath Test Manager in `references/uipath-standards.md`, pytest/
> CI gating in `references/azure-devops-cicd.md`, the PDD/SDD test case template in
> `references/documentation-templates.md`, the pre-go-live checklist in
> `references/governance-security.md`) are cross-referenced here, not duplicated. This file
> supplies what those don't: the underlying testing theory and systematic techniques that let you
> reason about test *coverage* — how do you know you've found every failure mode, not just the
> ones you happened to think of — plus the Power Automate testing mechanics this skill was
> previously missing, refreshed against official documentation, July 2026.

## Testing Philosophy: Why "Test Everything I Thought Of" Is Not Enough

The instinct to test "every possible failure" by brainstorming harder eventually runs out of
ideas — brainstorming finds the failures you can imagine, not the ones the *structure* of the
input space contains. The professional answer, grounded in established software testing theory
(ISTQB Foundation syllabus; Myers, *The Art of Software Testing*; ISO/IEC/IEEE 29119), is to
replace unstructured brainstorming with **systematic test design techniques** that generate cases
from the shape of the problem, plus a **systematic risk analysis technique** that generates
failure modes from the shape of the process. Used together, they produce a defensibly complete
test set rather than an anecdotal one:

1. **Test design techniques** (below) systematically derive test cases from what the process
   *processes* — every input variable's boundaries, every combination of business rules, every
   state the process can be in.
2. **FMEA** (below) systematically derives failure modes from what the process *does* — every
   step, every external dependency, every point where something could go wrong, ranked by how bad
   it would be and how likely it is.

Neither replaces judgment or domain knowledge — both are structured ways to apply that judgment so
coverage gaps are visible (an untested equivalence class, an unscored failure mode) rather than
invisible.

## Systematic Test Design Techniques

Apply these when designing test cases for any workflow, flow, script, or query in this skill —
not just for formal QA sign-off. They are the standard ISTQB/ISO 29119 black-box test design
techniques, adapted to RPA/automation:

### Equivalence Partitioning

Divide every input into classes where the system should behave the same way for any value in the
class, then test one representative value per class rather than exhaustively testing every value.
For an invoice amount field: {negative numbers}, {zero}, {valid positive amounts}, {non-numeric
input}, {empty/null} are five partitions — one test per partition, not one test per possible
number. This is the technique that turns "infinite possible inputs" into a finite, defensible test
set.

### Boundary Value Analysis

Failures cluster at the edges of a partition, not its middle — off-by-one errors, inclusive vs.
exclusive comparisons, overflow. For any bounded input (a quantity field capped at 9999, a date
range, a retry count capped at `MaxRetryCount`), explicitly test the boundary value, one below it,
and one above it (e.g., 9998, 9999, 10000 for a 9999 cap) rather than only mid-range values. Apply
this to every numeric config value already flagged as config-driven elsewhere in this skill
(`MaxRetryCount`, timeout thresholds, Do Until count/timeout limits) — these are exactly the
values most likely to have an off-by-one defect.

### Decision Table Testing

For business logic with multiple independent conditions combining to determine an outcome (a PDD's
enumerated business rules are exactly this), build a table with one column per condition and one
row per combination, and derive a test case per row. This is the systematic way to guarantee every
combination of business rules is tested, not just the ones that came to mind — a process with 4
binary business rules has 16 combinations; a decision table makes all 16 visible and lets you
consciously decide which are impossible (and why) rather than silently skipping them.

### State Transition Testing

For any process with distinct states (an invoice: Draft -> Submitted -> Approved -> Paid, or a
queue item: New -> InProgress -> Success/Failed/Retrying), model the state machine explicitly and
test: every valid transition, every invalid transition attempt (does the system correctly reject
or handle an attempt to pay a Draft invoice), and every state's boundary behavior. This is the
formal version of "test every business exception scenario" already required by this skill's PDD
process — state transition testing is how you verify the enumeration is actually complete.

### Exploratory and Negative Testing

Systematic techniques generate the test set; exploratory testing (unscripted, simultaneous
learning and testing by someone who understands the process) catches what the model of the system
didn't anticipate — a genuinely unexpected UI state, an undocumented data quirk. Budget explicit
time for this; it is not a lesser substitute for scripted testing, it is a complementary technique
that catches a different class of defect. Explicitly include **negative testing** — deliberately
feeding invalid, malformed, or hostile input (wrong data types, missing required fields, injected
special characters, oversized payloads) to confirm the system fails safely rather than crashing,
corrupting data, or silently succeeding with wrong results — as a first-class test category, not
an afterthought after positive-path testing is done.

## FMEA: Systematic Failure Mode Enumeration

**Failure Mode and Effects Analysis** (originating in reliability engineering — aerospace and
automotive — and widely adopted in software/process risk analysis) is the systematic technique for
answering "have we covered every possible failure" directly, rather than by exhaustive testing
alone. Apply it during Solution Design (Stage 2), before test cases are written:

1. **List every step** of the process (every workflow/action/query in the SDD's component
   breakdown).
2. For each step, enumerate every **failure mode** — every way that step could fail (a connector
   timeout, a selector not found, a validation rule violated, a downstream system returning an
   unexpected schema, a credential expiring, a duplicate record).
3. For each failure mode, score:
   - **Severity** (1-10): how bad is the impact if it happens (data corruption/financial loss = 10,
     cosmetic delay = 1)?
   - **Occurrence** (1-10): how likely is it to happen (a flaky third-party API = high, a
     well-tested internal system = low)?
   - **Detection** (1-10): how likely is the *current* design to catch it before it causes harm
     (no monitoring = 10/undetectable, a validation check + alert = 1/highly detectable)?
4. **Risk Priority Number (RPN)** = Severity x Occurrence x Detection. Sort by RPN descending —
   this is your test-effort and error-handling-design priority order, not a gut-feel guess. A
   failure mode with high severity, high occurrence, and poor detection is where design and test
   effort goes first; a low-severity, low-occurrence, well-detected failure mode is legitimately
   lower priority, and FMEA lets you say so with a number instead of an argument.
5. **Feed the output directly into the exception matrix** (`references/documentation-templates.md`)
   and the SDD's exception taxonomy — every high-RPN failure mode becomes a named Business or
   System exception with explicit handling, not a gap discovered in production.

This is the concrete, defensible answer to "how do I know I've covered every possible case of
failure": FMEA doesn't guarantee omniscience, but it replaces an unstructured guess with a
structured, reviewable artifact that a second person can audit for gaps.

## Test Types Taxonomy (what to run, and when)

| Test type | Question it answers | Applies to |
|---|---|---|
| **Unit** | Does this one function/workflow/page-object method work in isolation? | Every reusable component (UiPath sub-workflow, Python function, PAD subflow) |
| **Integration** | Do two components work correctly together (bot + queue, flow + connector, Python module + database)? | Every boundary between components |
| **System / End-to-End** | Does the full process work against a representative environment, covering every exception path in the PDD, not just the happy path? | Every full process before UAT |
| **User Acceptance (UAT)** | Does the business agree this meets the PDD's acceptance criteria? | Business sign-off gate, not a developer self-check |
| **Regression** | Did a change break something that previously worked? | Every change, automated in CI where possible |
| **Performance/Load** | Does the process meet its expected runtime/throughput at expected (and peak) volume? | Any process with a volume/SLA requirement in the PDD |
| **Security** | Can the process be made to leak credentials/data, or be abused (injection, privilege escalation)? | Every process touching credentials, PII, or external input |
| **Resilience / Chaos** | Does the process fail safely when a dependency is unavailable or slow? | Any process with an external dependency (see Resilience Testing below) |
| **Data Quality** | Is the data the process reads/writes correct, complete, and consistent? | Every process reading/writing a shared data store |
| **Disaster Recovery** | Can the process recover cleanly from a mid-run crash without duplicating or losing work? | Every unattended/production process (this is the idempotency requirement, verified by test rather than assumed) |

## Resilience Testing (a deliberately underused category worth calling out)

Most RPA/automation testing verifies the happy path plus a handful of anticipated exceptions, and
stops there. Resilience testing deliberately induces failure in dependencies to verify the process
degrades safely — the automation-scale application of chaos engineering principles (Netflix's
Chaos Monkey lineage): what happens if the target application is unreachable mid-run, if a
connector call times out, if the database connection drops between two statements in a
transaction, if a queue item is malformed. If this hasn't been deliberately tested, it hasn't been
verified — it's been assumed, and "the bot never crashes because the target system has never been
down during testing" is not evidence the bot handles that case correctly. Practical ways to induce
this without a chaos-engineering platform: point a test run at a deliberately unreachable endpoint,
kill a database connection mid-transaction in a test environment, feed a malformed/oversized
payload, or (for UiPath/PAD) temporarily rename a UI element the selector depends on.

## Platform-Specific Testing Mechanics

### Power Automate Cloud (previously undocumented in this skill — official mechanics)

- **Flow Checker**: static analysis run automatically in the designer, flags logic/action/
  connector errors and performance issues before a flow ever runs — the direct Cloud-flow analog
  of UiPath's Workflow Analyzer. Always resolve every Flow Checker warning before considering a
  flow ready for testing, not just before publishing.
- **Test Flow pane**: manual test (trigger the flow for real) or automatic test (replay a recent
  trigger payload or a previous run) directly in the designer. A flow must be tested manually at
  least once before the automatic-replay option becomes available.
- **Static result / mock data testing**: capture a real action's output once (via "Show raw
  outputs" in run history), then configure that action to always return the captured static
  result on subsequent test runs — this mocks the action (skipping real execution, e.g., skipping
  an actual approval request or a real record write) so you can test everything downstream of it
  repeatably and quickly. This is the practical mocking mechanism this skill's Python testing
  guidance gets for free from `pytest`/`unittest.mock`, but Power Automate requires explicitly
  configuring it per action.
- **Official testing-strategy guidance** (learn.microsoft.com/power-automate/guidance/planning/
  testing-strategy) makes two points worth stating explicitly: test **every** pattern/outcome
  combination, not just failure paths — a flow that runs without erroring but produces the wrong
  result is a silent failure, arguably worse than a visible one; and record actual results in a
  tracked table (expected vs. actual per scenario) so coverage is auditable rather than "I tried a
  few things and it seemed fine." When no separate test environment exists for a target system,
  Microsoft's documented workarounds are: use a static value to mock a lookup, or pair a
  create-record test step with an immediate delete-record step to avoid polluting live data.
- No native unit-testing framework exists for cloud flows as of this refresh — the closest
  approaches are the static-result mocking above (isolates a segment of one flow) or a third-party/
  community flow-runner library for true unit testing outside the designer; know this is a real
  platform gap rather than assuming an equivalent to `pytest` exists.

→ See `references/power-automate-cloud.md` and `references/power-automate-architecture.md` for
the flows this testing approach applies to.

### Power Automate Desktop (native Testing module — confirm current state against docs.microsoft.com,
this shipped recently and is still evolving)

Power Automate for desktop now has a dedicated **Testing** module (requires PAD 2.54+ and a
premium license) distinct from the Cloud-flow testing tools above:

- Create a **test case** (Tests > + New > Test case) tied to one desktop flow, structured as
  **Given/When/Then** (behavior-driven-development style, the same structure this skill's Python
  testing already implicitly follows via `pytest` naming conventions).
- The **`Test a desktop flow`** action runs the target flow (or, via **`Test a subflow of a
  desktop flow`**, a specific local subflow — global subflows aren't supported for subflow-level
  testing) and exposes its output variables for validation; the test run blocks until the flow
  under test completes.
- The **`Assert`** action validates actual output against expected output within the test case.
- Test cases run and are debuggable directly in the PAD console, with results recorded there, and
  can be integrated into automated pipelines — this is the practical way to give PAD flows the
  same CI-gated testing discipline `references/azure-devops-cicd.md` already applies to Python.
- This is a genuine capability gap-filler versus the historical PAD testing story (manual run +
  eyeball the result) — treat it as the default for any PAD subflow expected to be reused or
  maintained beyond a single build, not an optional extra.

→ See `references/power-automate-desktop.md` for the subflows this testing approach applies to.

### UiPath, Python, SQL Server

Already documented in depth elsewhere in this skill — cross-references, not repeated here:

- UiPath Test Manager, Test Data Queues, and mocked external dependencies:
  `references/uipath-standards.md`, "Test Manager Workflow" section.
- Python `pytest`/`ruff`/`mypy --strict`/coverage-gated CI: `references/azure-devops-cicd.md`,
  "Validation / Testing Layer" section, and `references/python-pom-pattern.md` for testing
  page-object-based automation specifically.
- SQL: validate query correctness and execution plans in SSMS against non-production data before
  embedding in a bot (`references/sql-server-standards.md`); apply Equivalence Partitioning and
  Boundary Value Analysis (above) to every parameterized query's inputs, not just to UI-facing
  fields.

## Organization-Specific Testing Procedure (RPA Testing Checklist)

Per this team's internal RPA Testing Checklist — this is the binding operational testing
procedure for this team, structured in four phases. It's a concrete, disciplined instance of the
theory above (its "Before Testing" phase is largely test-design and FMEA preparation by another
name; "Special Cases" is a stricter, compliance-driven version of the resilience-testing caution
about production-only failure modes), and takes precedence over generic practice where the two
overlap.

### Before Testing
- Develop detailed test plans covering scenarios the bot might encounter in production, including
  exception-handling scenarios specifically.
- Communicate the testing schedule and potential impact to stakeholders, share the test plan, and
  secure their approval before proceeding.
- Ensure the production environment is isolated from the test environment (separate VMs for
  test/development vs. production); verify all required software (UiPath, and target
  line-of-business applications such as Autoline, SAP, etc.) is installed and current.
- Catalog every asset the bot uses (credentials, config files, database connections); verify
  development and production assets are kept separate, correctly configured per environment, and
  contain no hardcoded values or cross-environment references.
- Prepare test data that closely mimics production data — **do not use live production data
  unless absolutely necessary**, and secure explicit stakeholder confirmation for whatever data is
  used; anonymize or securely handle anything sensitive.
- Grant the bot only the minimum access/permissions required for the process; use
  environment-specific credentials only (production credentials never used in test/dev, and vice
  versa).
- Secure peer/lead review and approval of process maps, documentation, and scripts before testing
  begins.
- Confirm backup and recovery plans exist where feasible, and document recovery procedures.

### During Testing
- **Do not run the full process end-to-end blindly.** Step through the workflow in UiPath Studio
  activity by activity, verifying each step as you go.
- Eliminate or skip steps that would write, update, or delete data/objects unless that action is
  specifically what's under test.
- Run tests in a virtual machine connected to the organization's privileged access management
  tooling (PAM360) to generate video logs of the session wherever possible, and execute all test
  runs through UiPath Studio (not a direct Orchestrator-triggered run) during this phase.
- Log all activities and errors for later analysis; assess the bot's efficiency, accuracy, and
  exception handling as you go; collect stakeholder feedback where applicable; track every issue
  or bug found for later resolution, rather than fixing silently mid-test without a record.

### After Testing
- Review asset usage logs to confirm only appropriate test-environment assets were actually used;
  remove or correct anything that isn't suitable for its environment.
- Revoke the tester's and the bot's access/permissions from the test environment once testing
  concludes — access is not left open by default after the test window closes.
- Assess whether the bot met its objectives; secure the PAM360 video logs as a record of the
  testing activity.
- Fix identified issues, then produce a detailed test report (performance metrics, issues found,
  resolutions), document lessons learned for future deployments, debrief stakeholders on the
  outcome, and update process documentation to reflect anything that changed during testing.

### Special Cases: Testing in the Production Environment

Production-environment testing is permitted **only** for two scenarios, and only under strict
controls in both cases:

1. **Verifying that elements captured in the test environment are also present in production**
   (e.g., confirming a selector resolves correctly against the real production UI).
2. **No test environment is available at all** for the system in question.

In either case: secure explicit stakeholder approval both for production-environment access and
for the specific testing activity; complete every "Before Testing" step first; **comment out any
activity that would write, update, or delete data or objects** (unless that action is
unavoidably part of what must be verified); **never run the full process end-to-end in
production** — test only the specific activities in question, directly, rather than stepping
through the entire process; then complete the "During Testing" and "After Testing" procedures as
normal. Production testing is an exception path with its own approval gate, not a convenience for
skipping test-environment setup.

## Test Data Management

- Use **synthetic or masked data** in every non-production test environment — production PII
  never belongs in Dev/Test, consistent with this skill's universal security standards.
  Masking/synthesis should preserve the statistical/structural shape of real data (correct field
  lengths, realistic value distributions) so boundary and equivalence-class tests remain valid.
- Maintain a **versioned test data set** covering every equivalence class and boundary identified
  above, checked into source control alongside the automation it tests — an untracked, ad hoc test
  spreadsheet that only one developer has is not reusable and not auditable.
- Explicitly include known **historically problematic records** (a prior production incident's
  actual input, anonymized) in the regression data set — this is the single highest-value entry in
  a test data set, since it's a confirmed real failure mode, not a hypothetical one.

## Production Readiness: Tying It Together

The pre-go-live checklist in `references/governance-security.md` already enumerates the gate
conditions. This section states the testing-specific standard those conditions imply: before any
process reaches Production, confirm that (1) every equivalence class and boundary for every input
has at least one test, (2) every business rule combination relevant to the process has been
covered by decision-table analysis, (3) every state transition (valid and invalid) has been
tested, (4) an FMEA has been performed and every high-RPN failure mode has a named, tested
handling path, (5) at least one resilience test has been run against every external dependency,
and (6) actual results are recorded against expected results in an auditable table, not asserted
from memory. A process that can show all six is defensibly tested; a process that can only show
"I ran it a few times and it worked" is not, regardless of how many times "a few" was.

Testing does not end at go-live: production monitoring (Orchestrator dashboards, Power Automate
analytics/alerts, Application Insights — already covered in this skill's Stage 5 and platform
reference files) is the continuation of testing into the environment that actually matters,
catching the failure modes that only manifest at real volume, real data, and real dependency
behavior no test environment fully replicates.

## Sources Consulted (official/primary, July 2026)

- This team's internal RPA Testing Checklist, provided directly by the user — the source for the
  entire "Organization-Specific Testing Procedure" section above. Followed as this team's binding
  testing procedure, not independently verified against an external standard.
- learn.microsoft.com/power-automate/guidance/planning/testing-strategy — official Power Automate
  testing strategy guidance
- learn.microsoft.com/power-automate/guidance/coding-guidelines/test-cloud-flows — Flow Checker,
  Test Flow pane, static result/mock data testing
- learn.microsoft.com/power-automate/desktop-flows/test-desktop-flows and
  power-platform/release-plan (2025 wave 1) — native PAD Testing module, Assert/Test actions,
  Given/When/Then test case structure, subflow test support
- ISTQB Foundation Level syllabus; Myers, *The Art of Software Testing*; ISO/IEC/IEEE 29119 —
  equivalence partitioning, boundary value analysis, decision table testing, state transition
  testing (standard, stable body of knowledge, not expected to change)
- FMEA methodology (SAE J1739 / AIAG-VDA FMEA handbook lineage, adapted to software/process risk) —
  stable methodology, not expected to change

Power Automate testing tooling (Flow Checker specifics, the PAD Testing module) is the part of
this file most likely to evolve — the PAD Testing module in particular shipped recently and is
still being extended (subflow test suites, for example, per the 2026 release-wave notes). Test
design theory (equivalence partitioning, FMEA, the test pyramid) is durable and framework-
independent.
