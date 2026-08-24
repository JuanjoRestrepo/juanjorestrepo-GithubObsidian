# Azure DevOps CI/CD for Python RPA

Applies the standard Code -> Repos -> Pipeline -> Validation -> Deployment lifecycle to a
Python + POM RPA project. Complements `references/python-pom-pattern.md` (code structure) and the
main SKILL.md's Debugging/Performance/Governance sections, which apply unchanged here.

> For **UiPath** projects specifically, this team has its own binding Azure DevOps branching and
> deployment flow (feature branch -> `dev` -> `main`, repo naming convention, SME-owned pipelines,
> Studio publish disabled) — see `references/uipath-standards.md`'s "Organization-Specific Azure
> DevOps ALM for UiPath" section rather than applying the generic model below to UiPath work.

## Azure Repos — Source Control

- One repository per RPA project (or a shared monorepo with clear `src/` package boundaries for a
  CoE-wide component library) — never uncontrolled code on a developer's machine or a network
  share.
- **Branching model** — two valid options, pick one and document it in the README:
  - **GitFlow-style** (`main` / `develop` / `feature/*` / `release/*` / `hotfix/*`): appropriate
    for scheduled, batched releases (e.g., monthly RPA release windows aligned to a change-control
    board).
  - **Trunk-based / GitHub-Flow-style** (`main` + short-lived `feature/*` branches merged directly
    via PR, deploys triggered per merge): appropriate for teams deploying frequently with strong
    automated test coverage; Microsoft's own DevOps guidance favors short-lived branches and
    frequent integration for teams with mature CI/CD, since long-lived `develop`/`release` branches
    increase merge conflict risk and slow feedback.
  - Do not default to GitFlow purely out of habit — choose based on release cadence and test
    coverage maturity.
- Repository layout: keep `.azure-pipelines/azure-pipelines.yml` (or `azure-pipelines.yml` at
  root) in the same repo as the code it builds — pipeline-as-code, versioned alongside the
  automation.
- Branch policies on `main` (Azure Repos "Branch policies"): require a minimum number of
  reviewers, require the build/test pipeline to pass, and require linked work items — configured
  in Repos settings, not just a team convention.
- Commit messages: Conventional Commits, matching the standard already defined in the main
  SKILL.md's Git & Source Control section — no platform-specific exception for Python projects.

## Azure Pipelines — CI/CD Stages

```text
Trigger -> Build -> Test -> Package -> Deploy
```

| Stage   | What happens                                                                                                                                                                                 |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Trigger | Pipeline runs on push/PR to a configured branch                                                                                                                                              |
| Build   | Install the target Python version and dependencies (`uv sync`, not raw `pip install -r requirements.txt`, to match project convention)                                                       |
| Test    | `pytest` runs the full suite (unit + POM-driven UI tests), `ruff` and `mypy --strict` run as separate lint/type-check jobs, results published as JUnit XML for visibility in the pipeline UI |
| Package | Build a versioned artifact (`python -m build`, the official PyPA build front-end, producing a wheel/sdist) or a Docker image, depending on the deployment target                             |
| Deploy  | Copy/publish the artifact to the target server/VM/container registry and (re)start the scheduled task/service                                                                                |

### Example `azure-pipelines.yml`

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage:
    'ubuntu-latest' # use 'windows-latest' only if the bot needs a Windows-only
    # dependency (e.g. pywinauto); prefer Linux agents otherwise —
    # faster to provision and cheaper on Microsoft-hosted pools

variables:
  pythonVersion: '3.12'

stages:
  - stage: Build
    jobs:
      - job: Install
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: $(pythonVersion)
          - script: |
              pip install uv
              uv sync --frozen
            displayName: 'Install dependencies (uv)'

  - stage: Test
    dependsOn: Build
    jobs:
      - job: RunTests
        steps:
          - script: uv run ruff check .
            displayName: 'Lint (ruff)'
          - script: uv run mypy --strict src/
            displayName: 'Type check (mypy)'
          - script: uv run pytest tests/ --junitxml=report.xml --cov=src --cov-fail-under=80
            displayName: 'Unit + POM tests (pytest, coverage gate)'
          - task: PublishTestResults@2
            condition: succeededOrFailed()
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: 'report.xml'

  - stage: Package
    dependsOn: Test
    jobs:
      - job: BuildArtifact
        steps:
          - script: uv run python -m build
            displayName: 'Build wheel/sdist'
          - task: PublishBuildArtifacts@1
            inputs:
              PathtoPublish: 'dist'
              ArtifactName: 'rpa-package'

  - stage: Deploy
    dependsOn: Package
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployToServer
        environment: 'rpa-production' # Azure DevOps Environment — enables approvals/gates
        strategy:
          runOnce:
            deploy:
              steps:
                - task: DownloadBuildArtifacts@0
                  inputs:
                    artifactName: 'rpa-package'
                # The SSH task requires installing the "SSH" Marketplace extension
                # (not a default built-in task) — confirm it's enabled in the
                # organization before relying on it.
                - task: SSH@0
                  inputs:
                    sshEndpoint: 'RPA-Server'
                    runOptions: 'commands'
                    commands: 'systemctl restart rpa-bot.service'
                  displayName: 'Restart bot service on target server'
```

Notes on accuracy vs. common copy-pasted examples: `SSH@0` is a real, Microsoft-documented task
but ships via the Marketplace "SSH" extension rather than the default built-in task set — verify
it's installed for the organization before depending on it in a pipeline. Prefer an **Azure DevOps
Environment** with approval gates (as shown) over an unconditional deploy job for any Production
target — this is the supported way to require manual sign-off before a Production deploy.

## Validation / Testing Layer

| Test type         | Purpose                                                               | Typical tool                                                                   |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Unit tests        | Validate individual functions/page-object methods in isolation        | `pytest` (preferred) or stdlib `unittest`                                      |
| UI/POM tests      | Validate interaction with the target application through page objects | `pytest` + Selenium/Playwright, or `Robot Framework` + `rpaframework` keywords |
| Data validation   | Verify input/intermediate/output data correctness                     | `pytest` with `pandas`/`Pandera`/`Great Expectations` assertions               |
| Integration tests | Validate communication between modules/services/systems               | `pytest` against a Test-environment target, not mocks alone                    |
| Regression tests  | Confirm a change didn't break existing behavior                       | Full `pytest` suite re-run in CI on every PR                                   |

- Write tests alongside development, not after — CI enforces this indirectly by gating merges on
  a passing suite and a coverage threshold (`--cov-fail-under=80`, matching the ≥80% coverage
  standard used across this project's Python work).
- Use **Allure** (`allure-pytest` plugin) for readable, stakeholder-shareable test reports beyond
  raw JUnit XML, when a richer report is valuable for business sign-off during UAT.
- Never merge past a failing or flaky test by disabling it silently — a skipped test without a
  tracked reason is a regression waiting to happen; use `pytest.mark.xfail(reason=..., strict=True)`
  with a linked ticket, not a bare skip.

## Deployment

| Target            | When to choose it                                                                                                                   |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| On-premise server | Data sensitivity/compliance requires on-prem; existing internal infra already hosts other bots                                      |
| Azure VM          | Need managed scaling/availability without full containerization; simplest lift for a team already in Azure                          |
| Docker container  | Need environment consistency across Dev/Test/Prod, or the target orchestrator (Kubernetes, Azure Container Apps) expects containers |

- Artifact contents: application code (wheel/sdist or container image), pinned dependencies (from
  `uv.lock`, not a hand-edited `requirements.txt`), configuration (environment-specific, injected
  at deploy time — never baked into the artifact), and the scheduled-task/service definition.
- Secrets: **Azure Key Vault**, referenced via a Key Vault-backed Azure DevOps variable group or
  fetched at runtime by the deployed service's managed identity — never embedded in the artifact
  or committed to the pipeline YAML.
- Scheduling: `systemd` timer/cron (Linux) or Windows Task Scheduler, invoked by the deploy step,
  or a persistent service if the bot is queue/event-triggered rather than time-triggered — prefer
  event/queue-driven triggers over blind polling, consistent with the rest of this skill.
- Monitoring: **Application Insights** (or the org's existing observability stack) for run metrics,
  exceptions, and custom events emitted from the bot's structured logging — the deployed bot is a
  service and should be monitored like one, per the main SKILL.md's Stage 5 guidance.

## Suggested Technology Stack Summary

| Layer                 | Choice                                                           | Rationale                                                          |
| --------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------ |
| Language              | Python 3.12                                                      | Consistent with this project's broader Python standard             |
| Dependency management | `uv` + `pyproject.toml`                                          | Fast, reproducible, single source of truth — no `requirements.txt` |
| Web automation        | Playwright (default) / Selenium (legacy/Grid-standardized teams) | See `references/python-rpa.md` decision table                      |
| Desktop automation    | `pywinauto`                                                      | Windows UI Automation/Win32 backends                               |
| Testing               | `pytest` + `ruff` + `mypy --strict`                              | Matches the project-wide code-quality bar                          |
| Reporting             | Allure (optional, for stakeholder-facing UAT reports)            | Readable beyond raw CI logs                                        |
| Source control        | Azure Repos (Git)                                                | Centralized, policy-enforced, integrated with Pipelines            |
| CI/CD                 | Azure Pipelines                                                  | Native integration with Azure Repos/Environments/Key Vault         |
| Secrets               | Azure Key Vault                                                  | Centralized rotation, no secrets in code or pipeline YAML          |
| Monitoring            | Application Insights                                             | Native Azure telemetry integration                                 |
| Deployment target     | On-prem server / Azure VM / Docker                               | Selected per the table above, not by default                       |
