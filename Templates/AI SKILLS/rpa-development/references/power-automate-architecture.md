# Power Automate — Architecture, Flow Control, and Structural Design

> Refreshed against official Microsoft Learn documentation and cross-checked against current
> practitioner sources, July 2026. This file is the structural/architectural companion to
> `references/power-automate-cloud.md` (which covers triggers, naming, governance, and the
> Scope-based Try/Catch/Finally error-handling pattern) and `references/power-automate-desktop.md`.
> Read this file when the question is _how should this flow be shaped_, not just _which action do
> I use_ — architecture layering, control-flow construct selection, concurrency, and modular
> decomposition via child flows.

## Why Architecture Matters Even in a "Low-Code" Tool

A cloud flow is a program: it has control flow (sequence, branching, iteration), state (variables,
outputs), and integration boundaries (connectors). Treating it as a program subject to the same
software-architecture discipline as any other code — not as a series of drag-and-drop steps — is
what separates a flow that survives production traffic and six months of maintenance from one that
becomes unmaintainable at 40 actions. Two academic/industry bodies of work ground this discipline
concretely rather than by analogy:

- **Workflow Patterns** (van der Aalst et al., workflowpatterns.com) — the standard academic
  taxonomy of workflow control-flow structures: Sequence, Parallel Split, Synchronization,
  Exclusive Choice, Simple Merge, Multi-Choice, Structured Loop, and others. Every Power Automate
  control construct is an implementation of one of these patterns; naming the pattern you need
  _before_ picking the action prevents the common mistake of reaching for nested Conditions when
  the actual requirement is a Multi-Choice (Switch) or a Parallel Split (parallel branches).
- **Enterprise Integration Patterns** (Hohpe & Woolf) — the standard industry vocabulary for
  integration architecture: Content-Based Router, Splitter, Aggregator, Scatter-Gather. A cloud
  flow that calls multiple systems is an integration pipeline; naming which EIP pattern a segment
  of the flow implements clarifies intent for the next developer far better than "the flow that
  does the thing with the three branches."

## Architectural Layering for a Power Automate Solution

Adapt the same layered separation this skill already applies to RPA solution design (Process /
Business / Integration / Application) to a Power Automate solution:

| Layer                    | Power Automate implementation                                                                      | Responsibility                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Trigger layer**        | The trigger action, trigger conditions, trigger concurrency control                                | Decide _when_ the flow runs and how many instances run in parallel — nothing else                       |
| **Orchestration layer**  | The parent flow's top-level Scopes and Switch/Condition structure                                  | Sequence the process, dispatch to the right branch or child flow, own overall error handling            |
| **Business logic layer** | Child flows, or well-named Scopes within the parent for logic too small to warrant a separate flow | Encapsulate one discrete unit of business logic each — validation, calculation, decision                |
| **Integration layer**    | Connector actions (SharePoint, Dataverse, HTTP, SQL)                                               | Talk to external systems; nowhere else in the flow should reference a connector-specific shape directly |
| **Data/state layer**     | Variables, Compose actions, trigger/action outputs referenced via expressions                      | Hold state deliberately (see State Management below) — not implicitly through scattered variable writes |

A flow that mixes all five concerns into one undifferentiated action list is the Power Automate
equivalent of a single 2,000-line function — the fix is the same discipline this skill already
applies elsewhere: separate concerns into named, single-responsibility units (Scopes, child flows)
and give each layer a clear boundary.

## Control-Flow Constructs: What Each One Is For

| Construct             | Workflow pattern                        | Use for                                                                                                                                                                                                       | Avoid for                                                                                                                                                          |
| --------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Condition**         | Exclusive Choice (binary)               | A single yes/no branch                                                                                                                                                                                        | More than one mutually exclusive branch — nesting Conditions for a 3+-way decision is the single most common Power Automate structural anti-pattern                |
| **Switch**            | Multi-Choice / Exclusive Choice (n-ary) | Any decision with 3+ mutually exclusive branches (status codes, record types, routing keys)                                                                                                                   | Binary decisions — a Condition is clearer for a true/false split                                                                                                   |
| **Apply to each**     | Structured Loop                         | Iterating a known array to act on every item                                                                                                                                                                  | Iterating just to search for one item (use `filter array` or `first()` instead) or to transform data (use `select`/data operations instead — see State Management) |
| **Do Until**          | Structured Loop (post-test)             | Polling for an external condition to become true (a job completing, a status changing)                                                                                                                        | A fixed number of iterations over known data — that's an Apply to each over a generated range, not a Do Until                                                      |
| **Scope**             | Sequence + grouping                     | Grouping related actions for shared error handling (`references/power-automate-cloud.md`'s Try/Catch/Finally pattern) and for readability                                                                     | —                                                                                                                                                                  |
| **Parallel branches** | Parallel Split + Synchronization        | Genuinely independent work that can run concurrently and must all complete before continuing (Scatter-Gather)                                                                                                 | Work with a dependency between branches — that's Sequence, not Parallel Split                                                                                      |
| **Terminate**         | Explicit termination                    | Force a specific run status (Succeeded/Failed/Cancelled) with a custom message, e.g. after a Catch scope handles a failure and you want the run to be flagged Failed in run history rather than showing green | Using it as a routine "exit early" inside normal logic — prefer restructuring branches so Terminate is the exception path, not a substitute for correct branching  |

### Concurrency — Apply to Each and Trigger Level (official limits, verified July 2026)

Two independent concurrency settings exist; know which one you're touching:

- **Apply to each concurrency control**: off by default (strictly sequential). When enabled,
  default degree of parallelism is **20**, range **1–50**. Enabling it can turn a 100-minute
  serial loop over 2,000 items into a 2–5 minute parallel one — but it **does not preserve
  iteration order**, and it **breaks any logic that shares state across iterations** (see State
  Management below for the correct pattern). Use it only when iterations are genuinely
  independent (send an email per recipient, update unrelated records); leave it off when
  ordering or a shared running total matters, or restructure to remove the dependency first.
  Check the target connector's rate limits before maximizing parallelism — 50 concurrent calls
  against a connector with a 100-calls-per-minute limit throttles the flow rather than speeding
  it up.
- **Trigger concurrency control**: off by default (unlimited parallel flow _runs_). When enabled,
  default degree of parallelism is **25**, range **1–100**, plus a configurable "maximum waiting
  runs" queue depth. Set to 1 to serialize an entire flow (only one run executes at a time,
  others queue) — the correct fix when multiple near-simultaneous triggers could race on the same
  shared resource (two runs updating the same record). **This setting cannot be disabled once
  saved** — decide deliberately, don't toggle it experimentally on a production flow.

### The Do Until "Silent Success" Trap (a genuine reliability gotcha, not a style note)

Do Until's condition is evaluated at the **end** of each iteration (post-test), so the loop body
always runs at least once even if the condition was already true. More importantly: by default,
if a Do Until reaches its **Count** limit (default 60, max 5000) or **Timeout** (default `PT1H`,
max `P30D`, ISO 8601 format) without the condition ever becoming true, the action is still marked
**Succeeded** — the flow continues as if the wait condition was actually met. This silently masks
a real failure (a job that never finished, a status that never changed) unless you explicitly
check the loop's exit reason (e.g., compare the final value against the expected condition in a
subsequent Condition action) or set the `operationOptions: FailWhenLimitsReached` parameter in the
action's underlying JSON definition. Treat every Do Until in a production flow as needing an
explicit post-loop check — do not assume "the flow succeeded" means "the condition was met."

## State Management: Compose/Select Over Loop-Scoped Variables

The single most common performance and correctness mistake once concurrency enters the picture:
using `Increment variable`/`Append to array variable` **inside** a concurrent Apply to each. Shared
mutable variables written from parallel iterations race — the final value is not reliably the sum
of all iterations, and results can silently vary between runs. The correct pattern (an application
of the Aggregator EIP pattern):

- Inside the loop, use a **Compose** action per iteration to capture that iteration's result —
  Compose has no shared state, so it's safe under concurrency.
- Outside the loop, aggregate the per-iteration Compose outputs (referenced as an array via
  `outputs('Compose')` in the loop's result) using **`select`**, **`filter array`**, or a
  **`join`** expression rather than a second loop.
- Prefer this array-oriented, expression-based style generally, even outside concurrent loops — a
  `select` or `filter array` action that transforms a whole array in one step is both faster and
  more reviewable than an Apply to each that appends to a variable, and it composes naturally with
  Scope-based error handling instead of threading a variable through nested branches.

## Modular Decomposition: Child Flows

Child flows are the primary mechanism for keeping a flow's action count and cyclomatic complexity
bounded — the Power Automate analog of extracting a function, and directly addresses this skill's
general Single Responsibility principle at the flow level.

- **Mechanics** (verify against docs.microsoft.com/power-automate for any version-sensitive
  detail): a child flow is a cloud flow built with a manual/Instant trigger and a `Respond to a
PowerApp or flow` (or premium `Response`) action returning outputs; the parent calls it via the
  `Run a Child Flow` action, passing inputs and receiving outputs synchronously — the parent waits
  for the child to complete. For fire-and-forget (parent doesn't wait), trigger the child via an
  HTTP request trigger instead.
- **Hard requirement**: parent and child must both be part of a **Solution** (the same ALM
  mechanism covered in `references/power-automate-desktop.md`) — a child flow outside a solution
  will not appear in the parent's `Run a Child Flow` picker. This is the most common cause of
  "child flow not found" and should be checked first when it happens.
- **Security implication, not just a technical detail**: a child flow runs under **its owner's**
  connections, not the caller's. This is a deliberate and useful pattern — e.g., a button-triggered
  parent flow usable by any employee can call a child flow owned by an account with elevated
  SharePoint/Dataverse access, so the calling user gets the result without needing that access
  directly. It is also a governance point: know and document who owns every child flow's
  connections, since that ownership determines what the flow can actually access in production —
  an orphaned child flow (owner leaves the organization) silently breaks every parent that calls
  it.
- **When to extract a child flow**: logic reused across more than one parent flow (shared
  validation, shared error notification, a common approval routine); a Switch branch's logic that
  is substantial enough to obscure the parent's overall shape if inlined (official guidance
  explicitly recommends calling child flows from Switch branches rather than expanding each branch
  in place); or a unit of logic that needs different connection/permission scope than the parent.
  Do not extract a child flow for a two-action sequence with no reuse case — that adds an
  indirection without a corresponding benefit.

## Orchestration Patterns (naming the shape you're building)

- **Fan-out / fan-in (Scatter-Gather)**: parallel branches dispatch independent work (e.g., query
  three systems simultaneously), then a downstream action synchronizes on all branches completing
  before aggregating results. Power Automate's parallel-branch construct implements this natively;
  the Aggregator pattern above (Compose per branch, combine after) is how you gather the results
  correctly.
- **Content-based routing**: a Switch (or a chain of Conditions, for 2 branches) inspecting a
  field and dispatching to the branch/child flow that handles that case — the standard shape for
  "process this record differently depending on its type/status."
- **Saga / compensating actions**: for a multi-step process where a later step can fail after
  earlier steps have already committed (e.g., a payment charged before a shipment record fails to
  create), design an explicit compensating action for each committed step, invoked from the
  relevant `Catch` Scope — cloud flows have no native distributed-transaction rollback, so
  compensation must be modeled explicitly, the same discipline this skill's SQL Server standards
  already apply via explicit transactions where the target is a single database.
- **Idempotency**: design triggers and downstream writes so a re-run (manual retry, or a duplicate
  trigger fire) doesn't duplicate side effects — check for an existing record before creating one,
  use upsert semantics where the connector supports them, and prefer a natural business key over a
  flow-generated one when checking for duplicates. This is the same idempotency requirement this
  skill applies to RPA transaction processing, restated at the Cloud-flow level.

## Sources Consulted (official/primary, July 2026)

- learn.microsoft.com/power-automate/guidance — coding guidelines: implement parallel execution
  (Apply to each concurrency, calling child flows from Switch branches), cloud flow coding
  guidelines
- Community/practitioner sources cross-checked against the above for specific numeric limits
  (Apply to each degree of parallelism 1–50 default 20; trigger concurrency 1–100 default 25;
  Do Until count default 60/max 5000, timeout default PT1H/max P30D) and the Do Until
  `FailWhenLimitsReached` behavior, since Microsoft's own docs describe the mechanism without
  always stating every default/limit value in one place
- workflowpatterns.com (van der Aalst et al.) — Workflow Patterns taxonomy
- Hohpe & Woolf, _Enterprise Integration Patterns_ — Content-Based Router, Aggregator,
  Scatter-Gather pattern vocabulary

Numeric limits and action-level mechanics are current as of this refresh and the part most likely
to drift; the architectural reasoning (layering, pattern naming, idempotency, modular
decomposition) is durable and framework-independent.
