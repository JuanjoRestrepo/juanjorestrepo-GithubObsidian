# Power Automate Cloud — Deep Reference

> Refreshed against official Microsoft Learn Power Automate guidance, July 2026. In this project's
> context, Cloud flows are the primary automation surface (approximately 90% of usage per current
> guidance); Desktop flows (`references/power-automate-desktop.md`) are reserved for the specific
> subset of a process that has no connector/API path. Read this file first when starting new
> Power Automate work; go to the Desktop reference only for the UI-automation leg of a process.

## Why Cloud-First Is the Correct Default (Not Just a Preference)

This mirrors the integration priority order already established elsewhere in this skill (API →
Database → UI automation → Citrix as last resort), applied at the Power Automate product level.
Microsoft's own official action-priority guidance ranks **cloud connector actions** above
app/file-specific actions, which rank above **UI automation actions** — the same ordering, not a
coincidence. Cloud flows call connectors (700+ prebuilt, plus custom/HTTP connectors) directly
against an API; Desktop flows exist specifically for the residual case where no API is exposed.
As more target systems ship real APIs/SaaS connectors, the UI-automation share of a portfolio
should shrink, not grow — a rising Desktop-flow percentage over time is usually a signal that new
automation candidates aren't being API-vetted first, not that the process genuinely requires it.

The common production hybrid pattern, and the one to default to when a process spans both a
connected system and a legacy/UI-only system: a **scheduled or triggered cloud flow orchestrates
the process end-to-end**, and calls out to an **unattended desktop flow** (via the `Run a flow
built with Power Automate for desktop` action, targeting a machine group) only for the specific
leg that requires UI automation — then resumes cloud-connector actions for everything downstream
(writing to Dataverse/SQL, sending notifications, routing approvals). Do not build a Desktop-only
flow when the same process could be a Cloud flow with one Desktop-flow call embedded in it.

## Flow Types — Choosing the Right One

| Trigger style | Flow type | Use for |
|---|---|---|
| An event happens in a connected system (new item, new email, record updated) | **Automated cloud flow** | The majority of business-process automation — event-driven, no manual start |
| A person starts it on demand (button, Power Apps, Teams) | **Instant cloud flow** | User-initiated actions — approval requests, manual data pushes, ad hoc reports |
| Time-based (daily, hourly, cron-like recurrence) | **Scheduled cloud flow** | Batch jobs, nightly syncs, report generation, orchestrating a Desktop-flow leg overnight |
| Long-running, milestone-driven business process | **Business process flow** | Guiding data-readiness through stages (e.g., a sales methodology) rather than pure integration |

Prefer Automated over Scheduled when a real trigger exists — polling on a schedule for something
that has an event-based trigger available wastes API calls and adds latency versus an
event-driven design.

## Naming, Structure, and Readability (official guidance)

- **Flows**: descriptive, purpose-revealing names (`SalesOrderApprovalFlow`, not `Flow 1`).
- **Triggers**: a clear prefix convention (e.g., `Trg_WhenItemCreated`) so the trigger's role is
  obvious when a flow is reviewed months later.
- **Variables**: same discipline as the rest of this skill — descriptive names, a consistent
  casing convention, `in`/`out` distinction where the value crosses a flow boundary.
- **Scope actions** double as both a Try/Catch/Finally mechanism (see Error Handling below) and a
  readability tool — group related actions under a named Scope (`GetInvoiceData`,
  `NotifyApprover`) the same way `references/power-automate-desktop.md`'s Region/End region
  guidance groups desktop-flow actions; a flat, ungrouped chain of 40 actions is exactly as bad a
  smell in a cloud flow as an unstructured desktop flow.
- Use **environment variables** (not hardcoded values) for anything that differs by
  Dev/Test/Prod — site URLs, connection references, thresholds — consistent with this skill's
  universal config-driven design rule.

## Organization-Specific Naming and Documentation Conventions

Per this team's internal Power Automate Cloud Best Practices documentation:

- **Action names**: every action name must **start with the action's original description** —
  this is what lets a developer see which action type was used without expanding it — then a
  colon, then additional context describing what the action does within this flow. Use proper
  case throughout. Example: `Initialize Variable: Customer ID`, not the bare default name
  (which hides intent) and not just `Customer ID` (which hides the action type).
- **Variables**: Power Automate Cloud does not force single-word names — use this flexibility
  for clear, readable names. Prefer clarity over brevity.
- **Initialize variables at the top**: immediately (or almost immediately) after the trigger,
  group all variable initializations in one place so the flow's state is declared up front and
  visible at a glance. Use a variable when its value is updated at multiple points during the
  run, or to store the result of a calculation. **Do not create a variable for a constant** — a
  value that's supplied once at initialization and never changes belongs as a direct expression
  reference, not a named variable. Similarly, do not introduce a variable where a direct
  reference to a prior action's output would serve the same purpose without the indirection.
- **Comments**: write comments that describe **intent** (the goal of a section) not a restatement
  of what the action name already says — this is what lets a reviewer spot a mismatch between
  intended goal and actual behavior. Keep comments updated when the goal changes; a stale comment
  is worse than none. Don't over-comment — comments create their own maintenance debt. Write in
  full sentences and plain language; no abbreviations, acronyms, or slang. **Paste the actual
  Power Automate expression text into the comment** for any non-trivial expression — the designer
  doesn't show an expression's full text without hovering or opening the code editor, so a
  pasted-in copy makes the flow browsable at a glance. Update the pasted copy whenever the
  expression changes.

## Choosing the Right Trigger (organization-specific guidance)

A cloud flow cannot be saved without a trigger, so development is blocked until one is chosen.
When the production trigger is undecided or has external prerequisites that aren't available yet
(a specific mailbox, a specific SharePoint library), per this team's practice: use **Recurrence**
as a development-time placeholder trigger — it has no external dependency and the flow can be
run almost immediately. Swap in the real production trigger once the flow logic is stable. Avoid
triggers like "When a file is created" or "When an email is received" for early-stage testing,
since they require the external event to actually occur before you can run a test.

## Connections to Third-Party Resources (organization-specific)

Many actions depend on a connection to an external account — `Send an email` needs an Outlook
connection, `Create blob` needs an Azure Storage connection, and so on.

- **Always verify the connection an action is actually using is the correct one** for the target
  environment before treating a flow as ready. A flow silently using a developer's personal
  connection instead of a shared service account is a common defect that only surfaces after that
  developer leaves or their token expires.
- **Connection reference naming** (when built inside a Solution): starts with a noun describing
  the connected account, followed by the connection type, the solution name, and a unique
  identifier — Power Automate generates this automatically for connections made inside a solution,
  which is one more reason to build inside a solution from the start rather than adding one later.
- Use the **Connections tab** in the Power Automate dashboard to audit every connection across
  every flow — this shows which flows use which connections, making it straightforward to identify
  unused/orphaned connections and to understand the blast radius before changing a shared one.

## Concurrency Control (organization-specific + official)

Two independent concurrency settings govern how much parallelism a flow allows — already
documented in detail in `references/power-automate-architecture.md`'s "Concurrency — Apply to
Each and Trigger Level" section. The team-specific framing here:

- **Trigger-level concurrency**: when a process uses a shared resource that can only handle one
  run at a time (a Virtual Machine, a single-instance licensed application, a resource with an
  exclusive lock), enable trigger-level concurrency and set the degree to 1 to serialize runs —
  without this, two near-simultaneous trigger fires will execute in parallel and race on that
  shared resource. Set this deliberately at project design time, not reactively after a production
  incident involving a collision.
- **Apply to Each concurrency**: loops run sequentially by default (item 1 then 2 then 3…). Enable
  concurrency control in the `Apply to Each` settings to process up to 50 items simultaneously
  when iterations are genuinely independent — this can turn a long sequential loop into a
  materially faster parallel one. Only safe when iterations share no mutable state (see
  `references/power-automate-architecture.md`'s State Management section on the correct
  Compose-then-aggregate pattern for concurrent loops).

## Error Handling: Scope-Based Try/Catch/Finally (official pattern)

Cloud flows have no native `try`/`catch` keyword, but the **Scope** action combined with
**Configure run after** produces the equivalent, and is the standard production pattern:

1. Wrap the main logic in a Scope named `Try`.
2. Add a second Scope named `Catch`, and set its **Configure run after** to trigger only when the
   `Try` scope **has failed** (uncheck "is successful") — this is the mechanism, found under the
   action's `...` menu, that makes it behave like an exception handler rather than running
   unconditionally.
3. Optionally add a `Finally` scope configured to run after `Try` regardless of outcome
   (successful, failed, skipped, and timed out all checked) for cleanup/logging that must always
   execute.
4. Inside `Catch`, log the failure (to Dataverse, Application Insights, or a SIEM — see
   Monitoring below) and send a clear failure notification — never let a Catch scope be empty.

**Important limitation to design around**: `Configure run after` only inspects the *immediately
preceding* action/scope, not the whole upstream chain — this is precisely why the main logic must
be grouped inside one `Try` Scope rather than left as a flat sequence of individual actions each
with their own run-after configuration; grouping is what lets a single `Catch` scope cover
failures from any action inside `Try`.

Apply the same Business Exception vs. System Exception classification used everywhere else in
this skill inside the `Catch` scope's branching logic — a validation failure on the triggering
record is not the same handling path as a downstream connector timeout.

## Approvals

Use the built-in **Approvals** connector (`Start and wait for an approval`) rather than
hand-rolling an approval mechanism with email + manual tracking — it provides a governed request/
response record, four approval types (first-to-respond, everyone-must-approve, custom), and
surfaces pending approvals in the Teams/Outlook Approvals hub for the approver. Approval flows are
saved in Dataverse, so a Dataverse database and an appropriate Power Automate/Office 365/
Dynamics 365 license are prerequisites the first time an environment uses approvals.

## Connectors and Data Efficiency

- Prefer **batch operations** over row-by-row looped actions when a connector supports them
  (SharePoint, Dataverse, and many services expose batch/bulk endpoints) — this is the Cloud-flow
  equivalent of this skill's SQL Server guidance to prefer set-based operations over row-by-row
  processing.
- Filter at the trigger/query level (e.g., a SharePoint trigger scoped to a specific view) rather
  than pulling everything and filtering in a downstream Condition — reduces unnecessary API calls
  and keeps the flow within connector throttling limits.
- Be deliberate about **premium connectors** and **per-flow (process) licensing** — many
  enterprise-grade connectors (SQL Server, HTTP with Azure AD, on-premises data gateway
  connectors) require premium licensing distinct from a standard Microsoft 365 seat; confirm
  licensing before designing a flow around a premium connector, not after building it.

## Governance and Security

- **Data Loss Prevention (DLP) policies**: defined in the Power Platform admin center, DLP
  policies classify connectors as Business or Non-Business (or block them outright) and prevent
  a flow from combining data across that boundary in ways that violate policy — this is the
  Power-Platform-specific instance of this skill's data-security standards, and should be
  configured by an admin before broad Cloud-flow adoption, not discovered after an incident.
  Design flows to use DLP-approved connector combinations by default.
- **Role-based access control** over who can create/edit/run flows, and **audit logs** for
  compliance tracking of changes and access — part of the same CoE governance model this skill
  already applies to RPA bots (`references/governance-security.md`), applied to Cloud flows.
  Un-owned, ungoverned "shadow flows" are the Cloud-flow equivalent of shadow bots.
- Same ALM mechanism as Desktop flows: **Solutions**, exported unmanaged from Dev and imported
  managed to Test/Prod via **Power Platform Build Tools** — see
  `references/power-automate-desktop.md`'s ALM section, which applies identically here since Cloud
  flows are Power Platform components like any other.

## Testing

Cloud flows have no native unit-testing framework — the practical toolkit is **Flow Checker**
(automatic static analysis in the designer, resolve every warning before considering a flow test-
ready), the **Test Flow** pane (manual trigger or automatic replay of a previous run), and
**static result/mock data testing** (capture a real action's output once, then force that action
to return it on subsequent test runs to isolate and speed up testing of everything downstream).
Official Microsoft guidance is explicit that a flow should be tested against **every** pattern/
outcome combination, not just failure paths — a flow that completes without erroring but produces
the wrong result is a silent failure. See `references/testing-quality-assurance.md` for the full
methodology (systematic test design techniques, FMEA-based failure mode enumeration, resilience
testing) this mechanics-level toolkit should be applied through, rather than testing ad hoc.

## Monitoring

- Use Power Automate's built-in **analytics** to track run history, performance, and failure
  trends per flow — check this before assuming a flow is healthy just because no one has
  complained.
- Set up **alerts** for failures/anomalies rather than relying on manual review of run history.
- For anything feeding this skill's broader observability standard, push flow outcomes to
  **Dataverse, Application Insights, or a SIEM** — the same "the bot/flow is a service and should
  be monitored like one" principle already applied to RPA bots and Python automation in this
  skill.

## Sources Consulted (official/primary, July 2026)

- This team's internal Power Automate Cloud Best Practices documentation (authored by @Czar
  Bragas), provided directly by the user — the source for every section marked
  "Organization-Specific" above. Followed as this team's binding standard.
- learn.microsoft.com/power-automate — triggers introduction, approvals (get started, custom
  connector approvals, wait-for-approval tutorial), cloud flow coding guidelines, DLP policies,
  Power Platform admin center guidance
- Industry implementation guides (Withum, 2toLead, PowerTech365, Automiq) cross-checked against
  the above for the Scope/Configure-run-after error-handling pattern and the Cloud-orchestrates/
  Desktop-executes hybrid pattern, since Microsoft's own docs describe the mechanism but the
  named "Try/Catch/Finally via Scope" pattern is an established community convention built on top
  of it, not itself a distinct Microsoft feature name.

Product-surface facts (specific connector names, licensing boundaries, exact DLP UI) are current
as of this refresh; the underlying discipline (Cloud-first, Scope-based error handling, DLP-aware
design, Solutions-based ALM) is durable guidance.
