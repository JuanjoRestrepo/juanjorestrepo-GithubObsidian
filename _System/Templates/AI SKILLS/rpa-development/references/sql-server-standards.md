# SQL Server Standards — Deep Reference

## Why Direct SQL Beats UI Automation

If a process reads or writes data that lives in (or can be staged in) SQL Server, direct database
access is almost always faster, more reliable, and easier to maintain than UI automation against a
database front-end or an app whose backend is that same database. Apply the integration priority
order (API → Database → UI → Citrix) before deciding to automate a UI at all.

## Query Standards

**Do:**
```sql
SELECT
    CustomerID,
    CustomerName,
    IsActive
FROM Customers
WHERE IsActive = 1
  AND CreatedDate >= @StartDate;
```

**Avoid:**
```sql
SELECT * FROM Customers WHERE IsActive = 1
```

- Name columns explicitly — never `SELECT *`. This documents intent, avoids pulling unnecessary
  (possibly sensitive) columns, and survives schema changes more gracefully.
- **Always parameterize** (`@StartDate`, `sp_executesql`, or the DB driver's native parameter
  binding) — never build SQL via string concatenation with bot-controlled or user-controlled
  values. This is the direct SQL-injection equivalent of "never hardcode credentials" — a hard
  security requirement, not a style choice.
- Filter/sort on indexed columns; avoid wrapping indexed columns in functions inside `WHERE`
  (`WHERE YEAR(CreatedDate) = 2026` prevents index seek — use
  `WHERE CreatedDate >= '2026-01-01' AND CreatedDate < '2027-01-01'` instead).

## Stored Procedures

- Use for any non-trivial or reused logic — keeps business rules versioned alongside the schema,
  testable independently of the bot, and reusable by other consumers (reporting, other bots).
- Every stored procedure: explicit parameter types (no implicit conversions relied upon), `SET
  NOCOUNT ON` to avoid unnecessary row-count messages over the wire, and a header comment (purpose,
  parameters, last-modified).
- Call from UiPath via `Execute Non Query`/`Execute Query` (Database activities) with parameters
  passed as typed arguments, never interpolated into the command text; from Python via
  `pyodbc`/`sqlalchemy` with bound parameters.

## Transactions

- Wrap any multi-statement write in an explicit transaction (`BEGIN TRAN` / `COMMIT` / `ROLLBACK`,
  or the driver's transaction context manager in Python/`SqlTransaction` in .NET).
- A bot that partially completes a multi-row write before crashing and leaves the database in an
  inconsistent state is a data-integrity incident, not just a bug — design for atomicity from the
  start, and make the retry-after-crash path idempotent (check "was this already written?" before
  re-writing).

## Indexing Awareness (developer-level, not DBA-level)

- Know which columns your bot's queries filter/join/sort on and confirm they're indexed —
  especially for high-volume or frequently-run bot queries; an unindexed query that's fine at 100
  rows can crater at 100,000.
- Prefer set-based operations (`UPDATE ... FROM ... JOIN`, `MERGE`) over row-by-row cursors when
  writing bulk updates from a bot — cursors in application code are almost always a performance
  anti-pattern.

## Connection Security

- Connection strings never hardcoded or committed — Orchestrator Asset / Key Vault / environment
  secret, same as any other credential in this skill.
- Use a dedicated service account scoped to only the schemas/tables/procedures the bot needs
  (least privilege) — never a shared `sa`/admin account.
- Prefer integrated/managed identity authentication where the infrastructure supports it over
  SQL-auth username/password pairs.

## SSMS Workflow

- Use **SQL Server Management Studio (SSMS)** for query development/testing against a
  non-production database first — validate execution plan (`Ctrl+M` actual execution plan) for any
  query expected to run against large tables before embedding it in a bot.
- Keep a `.sql` scripts folder in the same Git repo as the bot (versioned, reviewed via PR) —
  don't leave production-critical queries only inside a UiPath/PAD activity property or a
  developer's local SSMS session.
