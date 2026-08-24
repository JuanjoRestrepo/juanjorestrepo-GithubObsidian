# RPA Code Review Checklist

Standalone scoring checklist for reviewing any RPA artifact — UiPath workflow, PAD flow, Python
bot, C# activity, or SQL integration — before merge/promotion. Score each item Pass/Fail and
require a justification comment for any Fail that's being accepted rather than fixed.

## Reliability

- [ ] All external calls (UI, API, DB, file) are wrapped with appropriate exception handling
- [ ] Business exceptions and system exceptions are classified separately, never caught together
- [ ] Retry strategy exists for system exceptions and is config-driven (not hardcoded counts)
- [ ] No empty `Catch` blocks / silent `except: pass` anywhere
- [ ] Idempotency verified — safe to re-run after a crash mid-transaction without duplicate side
      effects (double payments, duplicate emails, duplicate DB rows)
- [ ] Logging present at process start/end, transaction start/end, every retry, and every
      exception — with structured fields (transaction key), not bare strings like `"Processing..."`

## Maintainability

- [ ] Naming conventions followed (PascalCase workflows / camelCase variables / `in_`/`out_`/`io_`
      argument prefixes in UiPath; `%inX%`/`%outX%` in PAD; PEP8 + type hints in Python)
- [ ] Single Responsibility respected — no workflow/function/flow that "does everything"
- [ ] Reusable components extracted to a shared library/subflow, not copy-pasted across the project
- [ ] No duplicated business logic between workflows/scripts
- [ ] Every public component (workflow argument, C# activity property, Python function) is
      documented (Studio tooltip / XML doc comment / docstring)

## Performance

- [ ] UI interaction is used only where API/DB access genuinely isn't available (priority order
      respected: API → DB → UI → Citrix)
- [ ] Selectors are as specific and minimal as possible (no unnecessarily broad UI-tree scans)
- [ ] No cursor-based row-by-row SQL processing where a set-based operation would work
- [ ] Loops minimized / batched where possible; parallel/queue-based processing considered for
      high-volume work
- [ ] No fixed `Delay`/`Wait` used to paper over a synchronization problem — explicit
      wait-for-condition used instead

## Security

- [ ] No hardcoded credentials, API keys, connection strings, or secrets anywhere in the artifact
- [ ] Credentials sourced from Orchestrator Assets / Key Vault / Credential Manager / environment
      secret — never from a config spreadsheet cell or committed file
- [ ] SQL queries are parameterized — no string-concatenated SQL built from bot- or
      user-controlled values
- [ ] Logs and error screenshots don't expose PII or credentials
- [ ] Least privilege respected for the automation's service account (scoped to what this process
      needs, not a shared admin account)

## Deployment

- [ ] Source-controlled in Git, including `.xaml`/PAD exports/`.sql` scripts — nothing lives only
      on a developer's machine
- [ ] Conventional Commit messages used; PR reviewed before merge to a publish-triggering branch
- [ ] Versioned package/artifact (`.nupkg`, Docker image, Robot artifact) — not a manual drag-and-
      drop publish
- [ ] Release notes / changelog entry created for the change
- [ ] Rollback plan exists and is documented (previous version, or fallback to manual process)
- [ ] Dev/Test/Prod environment separation confirmed — no leftover Dev credentials, queue names,
      or connection strings pointing at the wrong environment
