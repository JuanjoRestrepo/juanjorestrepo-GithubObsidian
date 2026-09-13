# RPA Documentation Templates

## Process Definition Document (PDD) — Skeleton

1. **Process Overview** — name, business owner, department, requester, priority
2. **As-Is Process** — numbered step-by-step of the current manual process, screenshots/system
   names per step
3. **In Scope / Out of Scope** — explicit bullet lists; anything ambiguous goes in Out of Scope
   with a note to revisit
4. **Applications & Access** — every system touched, access type needed (read/write), owner to
   request credentials from
5. **Business Rules** — every decision point as an explicit if/then rule, sourced from the business
   SME, not inferred
6. **Exception Scenarios** (critical — enumerate exhaustively with the business):
   | # | Scenario | Type (Business/System) | Current manual handling | Bot should... |
   |---|---|---|---|---|
7. **Volumes & SLAs** — items/day, peak periods (month-end, quarter-end), current SLA, target SLA
8. **Data Sensitivity** — PII/PCI/PHI involved? Data retention requirements?
9. **Complexity Score** — Low/Medium/High with justification (# apps, # decision points, # exception
   types, UI stability)
10. **Sign-off** — business owner + process owner signatures/approval date

## Solution Design Document (SDD) — Skeleton

1. **Architecture Summary** — attended/unattended/hybrid; REFramework/Python Producer-Consumer/
   linear (with justification for anything other than the state-machine default)
2. **High-Level Diagram** (described in text/ASCII if no diagramming tool): source system → queue
   → bot → target system, credential/config touch points labeled
3. **Trigger & Scheduling** — queue-driven / scheduled / event-driven, frequency, business calendar
   exceptions (holidays, month-end blackout windows)
4. **Component Breakdown** — one row per reusable workflow/module: name, responsibility, inputs,
   outputs, owner
5. **Exception Taxonomy** — every PDD exception scenario mapped to Business/System classification
   and the specific handling (retry count, escalation contact, email template)
6. **Data Flow & Security** — what data is stored where, encryption at rest/in transit, PII masking
   in logs, credential storage mechanism (Orchestrator Asset / Key Vault name — not the secret)
7. **Non-Functional Requirements** — expected runtime per item, concurrency/robot count, disaster
   recovery (idempotency/resumability plan if the bot crashes mid-item)
8. **Environments** — Dev/Test/Prod folder or workspace names, environment-specific config deltas
9. **Rollback Plan** — how to revert to manual process or a previous package version if go-live
   fails
10. **Sign-off** — technical lead + architecture review approval

## Exception Matrix Template

| Error message / symptom | Classification | Root cause | Bot behavior | Escalation |
|---|---|---|---|---|
| e.g. "Invoice ID not found" | Business | Source data incomplete | Log, skip item, flag in report | Daily digest to AP team |
| e.g. "Login timeout" | System | Target app slow/down | Retry x3 (Config-driven), then escalate | Immediate email/Teams to CoE on-call |

## Test Case Document Template

| Test ID | Scenario (linked to PDD exception #) | Input | Expected Outcome | Exception path covered? | Pass/Fail |
|---|---|---|---|---|---|

Cover, at minimum: happy path, every enumerated business exception, at least one simulated system
exception (target app unavailable / network timeout), empty queue, and a malformed/edge-case input
row.

## Bot README/Runbook Template (lives with the package)

- **What it does** (1–2 sentences, business language)
- **Owner** (technical + business)
- **How to restart** if stuck (kill process, requeue item, re-trigger schedule)
- **Where logs live** and how to read them
- **Known limitations** (e.g., "does not handle multi-page PDF invoices over 20 pages")
- **Dependencies** (target app versions, upstream file formats — anything that breaks this bot if
  changed upstream without notice)
