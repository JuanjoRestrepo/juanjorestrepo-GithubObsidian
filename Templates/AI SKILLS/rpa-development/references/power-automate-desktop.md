# Power Automate Desktop (PAD) — Deep Reference

> Refreshed against official Microsoft Learn Power Automate guidance documentation
> (learn.microsoft.com/power-automate/guidance), July 2026.

## When to Choose PAD over UiPath

- Desktop-only automation with no need for enterprise Orchestrator-grade governance.
- Strong Microsoft 365 / Dynamics 365 / SharePoint / Teams integration surface.
- Organization already licenses Microsoft E3/E5 (PAD is included) and doesn't want separate RPA
  licensing.
- Legacy Windows applications where UiPath brings no material advantage over PAD's UI element
  recognition.

Not a good fit for: complex queue-based enterprise orchestration at scale, heavy Citrix/virtualized
work (weaker tooling than UiPath's CV stack), or teams needing REFramework-grade governance
maturity out of the box.

## Project Structure

Never build a single giant flow. Mirror the same separation-of-concerns discipline as REFramework:

```text
Main Flow
├── Login              (subflow)
├── Process Data        (subflow)
├── Validation           (subflow)
├── Reporting             (subflow)
└── Logout                 (subflow)
```

- Each subflow does one job, is independently testable (Run subflow in isolation from the
  Designer), and is named for what it does, not "Subflow1".
- Extract anything used by more than one flow into a shared subflow, and where the same logic is
  needed across _multiple projects_, promote it into a **UI flow/Action library** shared via a
  common location rather than copy-pasted.

## Variables & Naming (per official Microsoft Learn coding guidelines)

```text
%inCustomerId%      -- input, camelCase with in/out/io prefix, same discipline as UiPath arguments
%outInvoiceTotal%
%ioRetryCount%
```

Official guidance: use camelCase, PascalCase, or underscores consistently to separate words; add a
datatype prefix to variable names; for **input/output variables specifically**, prefix both the
internal variable name and the external (flow-facing) name to distinguish them from ordinary flow
variables — this is the official basis for the `in_`/`out_`/`io_` convention already used
throughout this skill, not a UiPath-only convention borrowed for consistency. Never leave PAD's
auto-generated `%Variable1%`, `%Variable2%` names in anything beyond a throwaway prototype.

**Comments and regions** (official readability guidance, distinct from naming): add a `Comment`
action at the start of the Main subflow describing the process, intended audience, and related
flows; add a comment at the start of every subflow describing its purpose; comment bug fixes
in place. Use **Region**/**End region** actions to group related actions within a subflow so they
can be collapsed/expanded — this is the official mechanism for taming a long subflow, use it
before splitting into a new subflow purely for length reasons.

## Action Priority Order (official — apply before choosing how to automate a step)

Microsoft's official guidance ranks action types from most to least preferable when more than one
could accomplish the same interaction:

1. **Cloud connector actions** (e.g., a SharePoint or Excel Online connector call) — no desktop UI
   dependency, most reliable.
2. **Application- or file-specific Power Automate for desktop actions** (dedicated Excel, PDF,
   file/folder actions) — structured, not raw UI automation.
3. **UI automation / Browser automation action groups** — last resort, used only when no
   connector or dedicated action covers the interaction.

This is the PAD-specific instance of this skill's general integration priority order (API/
connector → dedicated structured action → UI automation), and should govern action selection
inside a flow the same way it governs platform selection at the architecture level.

## Error Handling

- Use **On Block Error** around every action or action group that touches an external
  system (UI element, file, API, database).
- Classify exactly like every other platform in this skill: **Business Exception** (expected —
  log, continue/skip, notify) vs. **System Exception** (unexpected — retry per a configured count,
  then escalate). Do not let a flow simply stop on the first unhandled error in production.
- Centralize error notification (email/Teams webhook) in a single reusable subflow so every flow
  reports failures consistently.

## Credentials and Sensitive Data (official)

Use the **`Get credential`** action to retrieve sensitive values at runtime — this is the official
mechanism, not just a best practice: values retrieved this way are automatically marked as
sensitive and are excluded from flow run logs. Passing a secret as a plain input variable does not
get this protection and will leak the value into run history. This is PAD's equivalent of
UiPath's Orchestrator Credential Asset / `Get Credential` activity — the same "never a plaintext
config value" rule from this skill's cross-cutting security standards, with a PAD-specific
mechanism.

## Unattended Run Reliability (official machine/queue guidance)

- Desktop flows queue for up to **12 hours** waiting for an available machine before failing —
  design scheduling with this in mind, not on the assumption a trigger fires immediately on a
  target machine.
- Distribute workload with one of Microsoft's recommended strategies: spread triggers over time,
  or use **machine groups** (identically configured machines running flows in parallel) sized to
  the anticipated concurrent unattended volume — undersized machine groups cause flows to queue
  and compete for the same device.
- Adjust the **Timeout** setting on the `Run a flow built with Power Automate for desktop` cloud
  action for flows expected to run long (Microsoft calls out >24-hour flows explicitly) — the
  default timeout will fail a long-running flow that is otherwise working correctly.
- License headroom: machine/process license count should be planned against anticipated parallel
  unattended flow volume, not just total flow count — this is a common under-provisioning mistake
  at scale.

## Orchestration Beyond a Single Desktop Flow

- **Power Automate Cloud flow → Run Desktop flow** action gives you a lightweight trigger/queue
  layer: a Dataverse table, SharePoint list, or Outlook-triggered Cloud flow can enqueue work and
  invoke the Desktop flow per item — the closest PAD equivalent to an Orchestrator queue.
- For anything requiring true horizontal scaling across multiple machines, evaluate whether the
  process has outgrown PAD and would be better served by UiPath Orchestrator's queue/robot model —
  flag this as an architecture decision, not a default migration.

## Application Lifecycle Management (official — Solutions, not ad-hoc export)

The official ALM mechanism for Power Platform (and therefore for PAD flows tied to Cloud flows,
connections, and other components) is **Solutions**, not loose per-flow export/import:

- **Always put flows, connection references, and related components in a Solution** — this is the
  explicit official guidance ("always ensure that all your applications, cloud flows, and bots are
  in a solution"). A flow built outside a solution is difficult to move cleanly between
  environments and is a common source of broken ALM later.
- Two solution types: **unmanaged** (editable, used in Dev) and **managed** (locked, deployed to
  Test/Prod) — the standard pattern exports the unmanaged solution from Dev, builds/converts it to
  managed, and imports the managed solution downstream.
- **Microsoft Power Platform Build Tools** (Azure DevOps extension, also available as GitHub
  Actions for Power Platform) provide the official pipeline tasks for this: exporting/importing
  solutions, packing/unpacking solution metadata into source control, setting the solution version
  (typically bound to the pipeline's `BuildId` rather than hardcoded), and deploying to a target
  environment via a service principal (`PowerPlatformSPN`) connection — this is the direct
  Power-Platform analog of `references/azure-devops-cicd.md`'s Azure Pipelines approach for Python,
  and should be the default over hand-rolled export/import scripting.
- A typical pipeline shape: **Initiate → Export from Dev → Build (pack/set version) → Release
  (import to Test, then Prod)** — mirrors this skill's general CI/CD stage model
  (Trigger → Build → Test → Package → Deploy).
- Maintain separate Dev/Test/Prod **environments** (each with its own Dataverse database where
  applicable), distinct connection references/credentials per environment — same non-negotiable as
  every other platform in this skill.

## Governance and Code Review Tooling (official)

- **HEAT (Holistic Enterprise Automation Techniques)** and the Automation CoE whitepaper are
  Microsoft's official guidance for standing up a Power Automate Center of Excellence — covers
  admin/governance, and lifecycle management for RPA and hyperautomation at enterprise scale;
  consult this before designing CoE processes from scratch (parallels the CoE model in
  `references/governance-security.md`, Power-Automate-specific).
- **Power CAT Toolkit** — Microsoft's official toolkit for automated flow code review; it encodes
  many of the coding guidelines referenced in this file and flags non-conforming patterns
  automatically. Prefer this over a purely manual review checklist where available.
- **Manage Power Automate for desktop on Windows** (official whitepaper) — covers lifecycle
  management of the PAD client itself via Intune/SCCM/ring deployment, relevant when this skill's
  tooling/environment-setup guidance needs to scale beyond a single developer machine.

## Testing & Deployment

- **Use the native Testing module** (PAD 2.54+, premium license): Given/When/Then test cases per
  flow, the `Test a desktop flow`/`Test a subflow of a desktop flow` actions, and `Assert` for
  output validation — this is now the default way to test a PAD flow, not manual run-and-eyeball.
  See `references/testing-quality-assurance.md` for the full mechanics and how this fits the
  skill's broader testing methodology (equivalence partitioning, boundary value analysis, FMEA).
- Test each subflow independently with representative and edge-case inputs before wiring into
  Main Flow.
- Export flows and store `.txt`/package exports in Git alongside documentation, in addition to
  (not instead of) the Solution-based ALM above — PAD's native versioning is weaker than UiPath's,
  so this extra discipline still matters.
- Maintain separate Dev/Test/Prod environments (distinct connection references/credentials) inside
  the Power Platform environment structure — same non-negotiable as every other platform in this
  skill.

## Sources Consulted (official/primary, July 2026)

- learn.microsoft.com/power-automate/guidance — desktop flow coding guidelines (naming, comments,
  regions, optimize performance/action priority order, secure your data), cloud flow coding
  guidelines, best practices for running desktop flows (machine groups, timeouts, licensing),
  automation adoption/HEAT/CoE whitepapers
- learn.microsoft.com/power-platform/alm — Solutions, Power Platform Build Tools for Azure DevOps,
  GitHub Actions for Power Platform, using DevOps for automated ALM

Product-surface facts (specific action names, exact timeout defaults, CLI/task names) are current
as of this refresh; the underlying discipline (Solutions-based ALM, action priority order,
credential handling, naming) is durable guidance unlikely to be reversed even as UI details shift.
