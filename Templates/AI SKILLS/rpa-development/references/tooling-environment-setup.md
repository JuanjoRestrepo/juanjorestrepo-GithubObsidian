# Standard RPA Developer Toolchain & Environment Setup

Reference machine setup for a senior enterprise RPA developer. Install order roughly follows this
list; VPN/network access tools generally need to be installed and connected before anything that
depends on corporate network resources (Orchestrator, SQL Server, internal Git remotes).

## Connectivity & Access

| Tool                 | Purpose                                                                                                                        | Notes                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Forticlient**      | VPN client for corporate network access                                                                                        | Install and validate connectivity first — most other enterprise tools (Orchestrator, internal SQL Server, internal Git) are unreachable without it           |
| **Citrix Workspace** | Access to Citrix-published/virtualized applications                                                                            | Required only if the role involves Citrix automation targets                                                                                                 |
| **1Password**        | Enterprise credential/secrets manager for the developer's _own_ access credentials (VPN, Git, Orchestrator login, DB accounts) | This is for the developer's personal credential hygiene — never a substitute for Orchestrator Assets/Key Vault, which secure the _bot's_ runtime credentials |

## RPA Platforms

| Tool                                 | Purpose                                                                   | Notes                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **UiPath Studio**                    | Primary RPA IDE                                                           | Install via the **Developer installation** track (not the End User/Robot-only install) — this gives Studio, Studio Web connectivity, and local debugging/packaging tools a Robot-only machine lacks. Confirm the version matches (or is compatible with) the target Orchestrator's LTS/version policy before building.                                       |
| **Power Automate** (Cloud + Desktop) | Primary/Microsoft-ecosystem automation platform in this project's context | Power Automate Cloud is browser-based at make.powerautomate.com, no install required — this is the default surface for most work. Power Automate Desktop is bundled with Windows 11 or installed standalone, needed only for the UI-automation leg of a process; sign in to both with the org's Power Platform environment, not a personal Microsoft account |

## Code Editors & IDEs

| Tool                             | Purpose                                                              | Notes                                                                                                                                                |
| -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Visual Studio Code**           | Primary editor for Python automation code, config, Markdown docs     | Recommended extensions: Python, Pylance, Ruff, GitLens, mssql (for inline SQL work)                                                                  |
| **PyCharm**                      | Full Python IDE for larger Python automation packages                | Preferred over VS Code when working in a large, multi-module Python RPA package with heavy refactoring/debugging needs                               |
| **Visual Studio 2022**           | .NET IDE for custom UiPath C# activities and NuGet activity packages | Required for anything beyond trivial C# — Studio's inline VB editor is not a substitute for building/testing a proper class library                  |
| **Sublime Text** / **Notepad++** | Lightweight text editors                                             | Quick config edits, log inspection, XML/XAML diff review — not for writing production code, but genuinely useful for fast, no-project-overhead edits |

## Data & Database Tools

| Tool                                    | Purpose                                                           | Notes                                                                                                                          |
| --------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **SQL Server 2022**                     | Target/source database engine                                     | Local Developer Edition install for local testing against a representative schema before touching Test/Prod                    |
| **SQL Server Management Studio (SSMS)** | Query development, execution plan analysis, schema inspection     | Validate every non-trivial query's execution plan here before embedding it in a bot — see `references/sql-server-standards.md` |
| **Azure Storage Explorer**              | Browse/manage Azure Blob/Queue/Table Storage and Storage Accounts | Used when a process integrates with Azure Storage for file staging, queue-based triggers, or archival                          |

## File Transfer & Browser

| Tool          | Purpose                                      | Notes                                                                                                                                                                                                                    |
| ------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **FileZilla** | FTP/SFTP client                              | For processes that exchange files with external parties via (S)FTP — always use SFTP over plain FTP when the target supports it                                                                                          |
| **Firefox**   | Secondary browser for web automation testing | Useful for cross-browser selector validation when the target process must run reliably regardless of the end user's default browser, and for isolating browser-specific automation issues from Chrome/Edge-specific ones |

## Source Control

| Tool    | Purpose                                                                                      | Notes                                                                                                                                                                                     |
| ------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Git** | Version control for everything — `.xaml`, PAD exports, Python packages, `.sql` scripts, docs | Configure Studio's native Git integration for UiPath projects; see `references/documentation-templates.md` and the Git & Source Control section of `SKILL.md` for branch/commit standards |

## Setup Order (Recommended)

1. Forticlient (VPN) → confirm corporate network access
2. Git + credential setup (SSH keys or PAT, stored in 1Password)
3. UiPath Studio (**Developer install**) + Power Automate Desktop
4. VS Code / PyCharm + `uv` for Python tooling; Visual Studio 2022 if building custom activities
5. SQL Server 2022 (local Developer Edition) + SSMS
6. Citrix Workspace (only if the role involves Citrix targets) + Azure Storage Explorer (only if
   the role involves Azure Storage integrations)
7. FileZilla, Firefox, Sublime Text/Notepad++ as needed per project

Document the exact version of each tool actually used on a project (especially UiPath Studio/
Orchestrator compatibility and .NET/Python versions) in the project's README — version drift
between developer machines and Production robot machines is a common, avoidable source of
"works on my machine" incidents.
