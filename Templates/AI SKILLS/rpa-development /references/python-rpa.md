# Python RPA — Deep Reference

## Why / When Python instead of UiPath

- No per-bot licensing cost; CI/CD-native (same pipeline as any other Python service).
- Better fit when the process is data-heavy (transformation, parsing, joining across many files)
  rather than UI-heavy — Python's data stack (pandas/polars) outperforms low-code data
  manipulation.
- Worse fit for: thick-client/Citrix/mainframe UI automation where UiPath's selector/CV tooling is
  materially more mature; also worse fit where non-technical citizen developers must maintain the
  bot after handoff.

## `rpaframework` (Robocorp) Module Map

| Module                                           | Use for                                                                         |
| ------------------------------------------------ | ------------------------------------------------------------------------------- |
| `RPA.Excel.Application` / `RPA.Excel.Files`      | Excel via COM (Application) or openpyxl-backed (Files, no Excel install needed) |
| `RPA.Browser.Selenium`                           | Web automation — wraps Selenium with retry/logging built in                     |
| `RPA.Desktop`                                    | Windows desktop automation (wraps pywinauto-like control)                       |
| `RPA.Email.ImapSmtp` / `RPA.Outlook.Application` | Email read/send                                                                 |
| `RPA.PDF`                                        | PDF text/table extraction and generation                                        |
| `RPA.Cloud.AWS` / `.Azure` / `.Google`           | Cloud storage/service integration                                               |
| `RPA.Robocorp.WorkItems`                         | Control Room work item queue — the Python equivalent of Orchestrator queues     |
| `RPA.HTTP`                                       | REST calls — always prefer this over UI automation when an API exists           |

Install via `uv add rpaframework` (project-scoped), never a global install.

## Producer/Consumer Skeleton (REFramework-equivalent shape)

```python
"""Producer/Consumer automation entrypoint.

Mirrors UiPath REFramework's Init -> Get Transaction -> Process -> Set Status shape
so the same mental model transfers between platforms.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from RPA.Robocorp.WorkItems import WorkItems

logger = logging.getLogger(__name__)


class BusinessException(Exception):
    """Expected, business-rule failure. Do not retry. Log and continue."""


@dataclass
class Config:
    max_retry_count: int
    notification_recipients: list[str]


def init(config: Config) -> None:
    """Idempotent setup: open connections/applications. Safe to re-run on retry."""
    logger.info("init.start")
    # establish connections, launch apps
    logger.info("init.complete")


def process_item(payload: dict) -> None:
    """Business logic for a single work item.

    Raises:
        BusinessException: expected rule violation (e.g. missing required field).
        Exception: unexpected/system failure (network, app crash) -> triggers retry.
    """
    if "invoice_id" not in payload:
        raise BusinessException("Missing invoice_id — routed to business for correction.")
    # ... actual automation logic ...


def run() -> None:
    work_items = WorkItems()
    work_items.get_input_work_item()

    for item in work_items.iter_work_items():
        try:
            process_item(item.payload)
        except BusinessException as exc:
            logger.warning("business_exception", extra={"reason": str(exc)})
            item.fail(exception_type="BUSINESS", message=str(exc))
        except Exception:
            logger.exception("system_exception")
            item.fail(exception_type="APPLICATION", message="Unhandled error — see logs.")
        else:
            item.done()


if __name__ == "__main__":
    run()
```

Same standard applies as any other production Python code in this environment: type hints,
docstrings, `mypy --strict`, `ruff`, ≥80% test coverage on business logic, no hardcoded secrets
(use environment variables injected by Control Room/CI, or a secrets manager).

## pywinauto vs. Selenium vs. Playwright

| Target                               | Tool                                   | Notes                                                                                                               |
| ------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Windows desktop app (Win32)          | `pywinauto` (`win32` backend)          | Older MFC/legacy apps                                                                                               |
| Windows desktop app (modern/WPF/UWP) | `pywinauto` (`uia` backend)            | Slower but more reliable element identification                                                                     |
| Web application                      | `Playwright` (preferred) or `Selenium` | Playwright: better auto-waiting, network interception, faster; use Selenium only for legacy Grid infra requirements |
| Any target with an API/DB available  | Neither — call the API/DB directly     | UI automation is the fallback, not the default                                                                      |

## Packaging & CI/CD for Python Bots

- `pyproject.toml` (`uv`), `src/` layout, `.venv` via `uv` — same conventions as any other Python
  project in this workflow.
- Package as a Docker image (for server-triggered runs) or a Robocorp `robot.yaml`-defined Robot
  (for Control Room-managed unattended runs).
- CI (GitHub Actions): lint (`ruff`) → type-check (`mypy --strict`) → test (`pytest`, ≥80%
  coverage on business logic) → build artifact → deploy to Control Room/target scheduler.
- Trigger via Control Room schedule, cron, Windows Task Scheduler, or an upstream event
  (queue message, webhook) — same triggering philosophy as the UiPath side: event/queue-driven
  preferred over blind polling.
- Structured JSON logging (`structlog` or stdlib `logging` with a JSON formatter) shipped to the
  same observability stack as other services — an RPA bot is a service, not a one-off script, and
  should be monitored like one.
