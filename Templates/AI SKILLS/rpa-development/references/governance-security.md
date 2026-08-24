# RPA Governance & Security — Deep Reference

> The "Organization-Specific" section below reflects this team's internal UiPath Orchestrator
> Security Guidelines, provided directly by the user. It is followed as this team's binding
> standard, not independently verified against UiPath's own published documentation or trust
> materials — where this team's documentation states a certification, access model, or limit,
> that statement is taken as this organization's own assertion and reproduced faithfully, not
> re-verified against uipath.com by this file.

## CoE (Center of Excellence) Operating Model

- **Bot inventory** (mandatory, prevents "shadow bots"): one row per production bot —
  name, business owner, technical owner, criticality (P1/P2/P3), last-tested date, dependencies
  (target app versions), Orchestrator folder/Control Room workspace, package version currently in
  Production.
- **Intake & prioritization**: every candidate process goes through the discovery checklist
  (see main SKILL.md Stage 1) before being queued for build — CoEs that skip this drown in
  low-ROI, high-maintenance bots.
- **Standards enforcement**: shared component library (login helpers, logging wrapper, common
  validations) versioned centrally; every new project consumes it via package reference rather
  than reimplementing.
- **Roles**: RPA Developer (build), Solution Architect (design/SDD approval), Business Analyst
  (PDD/discovery), Infrastructure/Orchestrator Admin (environment, licensing, credential
  provisioning), CoE Lead (governance, prioritization, ROI tracking).
- **Change control board**: any change to a Production bot (workflow logic, config, target
  selectors) goes through the same PR review as new development — no live edits against a
  published Production package.

## Credential Management Patterns

| Pattern                                  | When                                                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| UiPath Orchestrator **Credential Asset** | Default for UiPath bots — Studio's `Get Credential`/`Get Secret` pulls at runtime, never stored in Config.xlsx                       |
| CyberArk / Azure Key Vault integration   | Enterprise setups — Orchestrator's credential store is itself backed by the vault; rotate secrets centrally without redeploying bots |
| Environment variables via CI/CD secrets  | Python bots — injected at deploy time (GitHub Actions secrets, Control Room vault), never committed                                  |
| Windows Credential Manager               | Local/attended automation fallback only — not for unattended production at scale                                                     |

**Never acceptable, in any language/platform:** credentials in Config.xlsx cell values, `.env`
files committed to Git, credentials in workflow XAML properties, credentials in plaintext log
output, a shared "generic bot admin" account reused across unrelated processes (violates least
privilege and breaks auditability of who/what did an action).

## Organization-Specific Orchestrator Governance

Per this team's internal UiPath Orchestrator Security Guidelines:

- **Access model**: Orchestrator access is restricted to the Enterprise Solutions team and
  developers assigned to a project's own Tenant. Login requires Microsoft 365 single sign-on with
  two-factor authentication; sessions are automatically logged out after 30 minutes of inactivity
  and require re-authentication. Developers are granted the minimum permissions their role
  requires, not broad default access.
- **Robot types and their governance implications**:
  - **Attended** — triggered by user events, runs alongside a human on the same workstation;
    managed through Orchestrator for centralized deployment and logging.
  - **Unattended** — runs in virtual environments, adds remote execution, scheduling, monitoring,
    and queue support on top of Attended capabilities.
  - **Studio/StudioX** — has Unattended-equivalent connectivity but is used only to connect a
    developer's Studio/StudioX to Orchestrator for development, not for production execution.
  - **NonProduction** — equivalent to Unattended but restricted to development/testing use only.
  - Debugging in Studio is supported against any of these robot types.
- **Scale (as documented internally)**: a single Orchestrator instance can run up to 1,000
  Unattended robots or up to 10,000 Attended robots simultaneously.
- **Service accounts**: the service account used on a VM to connect to Orchestrator must not carry
  administrative rights on that machine — the automation's execution identity is deliberately
  scoped below admin, independent of what the automated process itself needs to access.
- **Asset types**: Orchestrator Assets are Text, Bool, Integer, or Credential. Credential assets
  are write-only from a developer's perspective once saved — the stored password cannot be viewed
  again, even by re-opening the asset for editing. Assets are scoped per folder; a user without
  access to a given folder cannot create, view, edit, or delete assets within it.
- **Package deployment**: every package deployment must go through the DevOps CI/CD process (see
  `references/uipath-standards.md`'s "Organization-Specific Azure DevOps ALM for UiPath" section)
  — this is a security control as much as a release-process one, since it guarantees a secured
  backup and an audit trail that a direct Studio-to-Orchestrator publish would not have.
- **Certifications and attestations referenced internally**: ISO/IEC 27001, SOC 2 Type 1 and
  Type 2, the UK NHS Data Security & Protection Toolkit self-assessment, Cyber Essentials Plus,
  Veracode Verified Continuous, and the Paris Call for Trust and Security in Cyberspace. Treat
  this list as this organization's documented understanding of UiPath's compliance posture; verify
  directly against UiPath's Trust Portal before citing it externally (e.g., in a customer-facing
  document) rather than relying on this file as the source of record.
- **Baseline security guidelines** (this team's internal summary, consistent with the credential/
  access controls above): secure access via strong authentication and MFA; role-based access
  granted on a need-to-know basis; encrypted communication (HTTPS/TLS) throughout; secure,
  isolated development environments separate from production; deployment restricted to authorized
  personnel via access control lists; continuous monitoring and logging of workflow activity;
  regular software updates/patching; secure, regular backups; and periodic security assessments to
  catch control gaps before an incident does.

## Pre-Go-Live Checklist

- [ ] PDD signed off by business owner; SDD signed off by technical/architecture reviewer
- [ ] Every PDD exception scenario has a corresponding test case and passes
- [ ] Workflow Analyzer / Ruff+mypy CI checks pass with zero unsuppressed warnings
- [ ] No hardcoded credentials/secrets (verified by grep/secret-scanning in CI, not just manual
      review)
- [ ] Logging in place at every decision point and external call, PII redacted from logs
- [ ] Idempotency verified — safe to re-run Init/retry mid-process without duplicate side effects
      (e.g., double-submitted payments, duplicate emails)
- [ ] Dev/Test/Prod environments fully separated — distinct credentials, distinct queue/folder
      names, no cross-environment references left over from testing
- [ ] Runbook/README complete: restart procedure, log location, known limitations, contact owners
- [ ] Rollback plan documented and tested (revert to manual process or previous package version)
- [ ] Bot registered in the CoE inventory with criticality and ownership assigned
- [ ] Monitoring/alerting configured (failed job alerts, queue age alerts) before go-live, not
      added reactively after the first incident

## Hypercare Plan

- 2–4 weeks of active daily monitoring post-go-live (exception review, volume vs. expected,
  runtime vs. expected).
- Defined escalation path with response-time SLA per severity (P1 = bot down/blocking business
  operation, P2 = degraded/high exception rate, P3 = cosmetic/non-blocking).
- Formal handoff to standard support only after: exception rate stabilizes at expected baseline,
  no P1/P2 incidents in the final week of hypercare, and the runbook has been validated by someone
  other than the original developer (a documentation smell-test — if only the author can operate
  it, the runbook isn't done).
- Post-hypercare retro: capture any process/PDD gaps discovered in production for the CoE's
  discovery-checklist improvement backlog.

## Sources Consulted

- This team's internal UiPath Orchestrator Security Guidelines, provided directly by the user —
  the source for the "Organization-Specific Orchestrator Governance" section above.
- General CoE operating model, credential management patterns, and go-live/hypercare structure
  reflect established RPA governance practice cross-referenced throughout this skill (not
  vendor-specific documentation with a single canonical source to cite).
