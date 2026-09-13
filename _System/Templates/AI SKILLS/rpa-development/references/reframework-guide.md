> Content in this file is grounded in the official UiPath REFramework GitHub repository
> (github.com/UiPath/ReFrameWork, verified July 2026), UiPath official documentation
> (docs.uipath.com), the UiPath Marketplace REFramework for Tabular Data listing, and the
> UiPath Community Forum. All architectural descriptions match the canonical template.
> References to Maestro integration are based on the current UiPath platform documentation.

# REFramework — Robotic Enterprise Framework

## 1. What REFramework Is and Why It Exists

REFramework is a State Machine–based project template developed and maintained by UiPath. It
encodes the architectural decisions, exception-handling patterns, and retry mechanics that every
production-grade unattended automation requires — not as optional guidance but as implemented,
runnable code that developers extend rather than design from scratch.

Without REFramework (or equivalent), each project team makes its own decisions about retry
counts, exception categorization, application recovery, configuration management, and run
termination. These decisions are made inconsistently, are invisible at code review, and produce
automation that fails differently in every project. REFramework eliminates that surface area.

The framework is appropriate for any automation that processes a set of similar items
(transactions) where: the processing of item N is independent of item N-1, some items may fail
without stopping the entire run, and the process runs unattended (no human present to recover
from failures). It is not appropriate for linear single-run processes that have no transactional
structure — use the basic Transactional Business Process template for those.

---

## 2. Architecture: Four States and Their Transitions

REFramework's Main.xaml is a State Machine with exactly four states and seven transitions. Each
state is responsible for one phase of the automation lifecycle.

```
[Initial State]
      |
      v
[INIT] ──(System Exception)──────────────────────────────────► [END PROCESS]
  |
  |(Success)
  v
[GET TRANSACTION DATA] ──(No More Data)──────────────────────► [END PROCESS]
  |                  ▲
  |(Transaction      |
  | Retrieved)       |
  v                  |
[PROCESS TRANSACTION] ──(Success / BusinessException)──────────┘
  |
  |(System Exception, retries < max)
  └──────────────────────────────────► [INIT] (re-initialize, recover app)
  |
  |(System Exception, retries = max)
  └──────────────────────────────────► [END PROCESS]
```

### State 1: Init

**Responsibility:** Load configuration; authenticate; open and log in to all applications used
by the process. This state runs once at process start and again after a System Exception during
processing (to recover the application to a known-good state before retrying the transaction).

**Key workflows invoked:**
- `InitAllSettings.xaml` — reads `Config.xlsx` from the Data folder, then reads Orchestrator
  Assets for any keys defined in the Config. Final merged configuration is stored in the
  `Config` dictionary variable (`Dictionary(Of String, Object)`).
- `GetAppCredential.xaml` — retrieves credentials from Orchestrator Assets or the Windows
  Credential Manager using the key defined in Config.
- `InitAllApplications.xaml` — opens applications and logs in. Developer implements this.

**Exit conditions:**
- Success → transition to Get Transaction Data.
- System Exception → transition to End Process (no point retrying initialization failures,
  as they indicate an environment problem, not a transient failure).

**Developer responsibility:** Implement `InitAllApplications.xaml`. Add application URL /
path to Config.xlsx. Add credential asset key to Config.xlsx.

### State 2: Get Transaction Data

**Responsibility:** Retrieve the next transaction item to process. Signals the end of the
run when no more items exist.

**Key workflow invoked:**
- `GetTransactionData.xaml` — by default, calls `Get Transaction Item` activity to dequeue
  one item from the Orchestrator Queue. For non-queue variants, this workflow is replaced
  (see Section 5).

**Output:** Sets the `TransactionItem` variable:
- `QueueItem` for queue-based processes.
- `DataRow` for tabular-data variants.
- Any custom type for advanced customizations.

**Exit conditions:**
- `TransactionItem` is set (not Nothing) → transition to Process Transaction.
- `TransactionItem` is Nothing (queue empty / no more rows) → transition to End Process.

### State 3: Process Transaction

**Responsibility:** Execute the business logic for the current transaction. Handle both
expected business failures (`BusinessRuleException`) and unexpected application failures
(`SystemException`) distinctly.

**Key workflows invoked:**
- `Process.xaml` — developer implements the full business logic here, invoking other
  sub-workflows as needed.
- `SetTransactionStatus.xaml` — marks the queue item as `Successful`, `BusinessException`,
  or `Failed` (with a System Exception) in Orchestrator. For non-queue variants, this writes
  the status to a status file or DataTable column.
- `TakeScreenshot.xaml` — called automatically on System Exception; screenshot stored in
  the Data/Temp folder and attached to the Orchestrator queue item.

**Exit conditions:**
- `Success` or `BusinessException` → transition back to Get Transaction Data (get next item).
- `System Exception` AND retry count < `Config("MaxRetryNumber")` → transition to Init
  (recover app, re-enqueue or re-attempt same transaction).
- `System Exception` AND retry count = max → transition to End Process.

### State 4: End Process

**Responsibility:** Graceful shutdown — log out, close applications, send summary notification
if configured.

**Key workflow invoked:**
- `CloseAllApplications.xaml` — developer implements logout and application close.

---

## 3. Config.xlsx Schema

`Config.xlsx` is the central configuration store. It has three sheets:

### Sheet 1: Settings
Defines all configuration key-value pairs loaded into the `Config` dictionary.

| Column | Purpose |
|---|---|
| Name | Key in the Config dictionary |
| Value | Default value used if no Orchestrator Asset exists for this key |
| Description | Free-text explanation for the team |

Standard keys (present in the default template):

| Key | Default value | Purpose |
|---|---|---|
| `logF_BusinessProcessName` | _(process name)_ | Prefix for all log messages |
| `MaxRetryNumber` | `3` | Max System Exception retries per transaction |
| `MaxConsecutiveSystemExceptions` | `3` | Aborts the run if N consecutive System Exceptions occur |
| `OrchestratorQueueName` | _(queue name)_ | Queue to dequeue transactions from |
| `OrchestratorQueueFolder` | _(folder path)_ | Orchestrator folder containing the queue |
| `RE_Framework_Version` | _(version)_ | Informational |

Add process-specific keys here: target application URLs, file paths, asset names for
credentials, thresholds, email addresses for notifications.

### Sheet 2: Constants
Key-value pairs that are never overridden by Orchestrator Assets (used for truly static
values that don't vary by environment). Merged into the same `Config` dictionary, so
constants and settings are accessed identically at runtime.

### Sheet 3: Assets
Maps Config dictionary keys to Orchestrator Asset names. During `InitAllSettings`, the
framework reads this sheet and overwrites the local Config value with the Orchestrator Asset
value for every key listed. This is the mechanism for environment-specific configuration
without changing the Config.xlsx file between environments.

```
Assets sheet example:
Name                   Asset
OrchestratorQueueName  PROD_QueueName_Asset
CredentialAssetName    PROD_BotCredentials_Asset
```

---

## 4. Exception Hierarchy: BusinessRuleException vs. SystemException

This distinction is the most important design decision in any REFramework process, and it is
frequently made incorrectly.

| Category | Class | Meaning | Default REFramework response |
|---|---|---|---|
| **BusinessRuleException** | `UiPath.Core.BusinessRuleException` | The data in this transaction violates a business rule — the process cannot complete it regardless of retries. Examples: invoice total does not match sum of line items; required field missing; duplicate record detected. | Mark queue item `BusinessException`. Move to next transaction. Do NOT retry. |
| **SystemException** | Any other exception (selector timeout, web exception, NullReference, etc.) | The application or environment failed. A retry after recovery may succeed. Examples: target application not responding, selector changed, network timeout. | Mark queue item `Failed`. Increment retry counter. Re-initialize application. Retry up to `MaxRetryNumber`. |

**The decision rule:** would retrying this exact same transaction with the same data ever
succeed? If no → `BusinessRuleException`. If maybe → `SystemException`.

Throw `BusinessRuleException` explicitly in `Process.xaml`:

```vb
' VB.NET — in Process.xaml when business validation fails
Throw New BusinessRuleException("Invoice total " & invoiceTotal.ToString("C") &
    " does not match line item sum " & lineItemSum.ToString("C") &
    ". Transaction " & transactionID & " cannot be processed.")
```

The message is stored in the queue item's `SpecificContent` and is visible in Orchestrator's
queue monitoring UI — write messages that a support team member can act on without reading code.

---

## 5. Transaction Data Source Variants

### Variant A: Queue-Based (Default / Canonical)

The standard REFramework reads from an Orchestrator Queue. Each `QueueItem` carries:
- `SpecificContent` — a dictionary of named fields populated by the Dispatcher.
- `Output` — a dictionary of named fields written by the Performer when marking Successful.
- `Progress` — free-text status updated mid-processing (visible in Orchestrator UI).
- `Reference` — a string used for deduplication and search.
- `Priority` — High / Normal / Low (affects dequeue order).
- `DueDate` — items are not dequeued before this date.
- `DeferDate` — items dequeued after this date only.
- Retry count and last-exception detail — managed by Orchestrator, surfaced in queue monitoring.

```vb
' Access SpecificContent in Process.xaml
strInvoiceID = TransactionItem.SpecificContent("InvoiceID").ToString()
dblAmount    = CDbl(TransactionItem.SpecificContent("Amount"))
```

Queue-based is the correct choice when:
- Items are produced by a separate Dispatcher process (or an external system).
- Multiple Performer robots must share the same work pool.
- Per-item retry tracking with exponential backoff is required.
- Items may have different `DueDate` or priority values.
- Audit-trail of processing outcomes per item is required.

### Variant B: Tabular Data / DataRow (No Queue)

`TransactionItem` is typed as `DataRow` instead of `QueueItem`. The input DataTable is loaded
once in `InitAllSettings` (or a dedicated Load step in Init) and stored in the `TransactionData`
variable. `GetTransactionData` uses `TransactionNumber` to index into the DataTable:

```vb
' GetTransactionData.xaml — retrieve next DataRow
If TransactionNumber <= TransactionData.Rows.Count Then
    TransactionItem = TransactionData.Rows(TransactionNumber - 1)
Else
    TransactionItem = Nothing  ' signals end of data
End If
```

`SetTransactionStatus` writes the outcome to a status column in the DataTable (or a separate
status DataTable), which is written to an output file in End Process.

Tabular-data variant is the correct choice when:
- Input is a single Excel or CSV file submitted as a batch.
- The process runs attended or the submitter expects a single output file with status.
- Scale is low (hundreds of rows, single robot).
- Orchestrator queue overhead is not justified for the process volume.

**A status file** (separate Excel written by `SetTransactionStatus` after each row) is critical
for recoverability: if the bot crashes mid-batch, the status file shows which rows were
processed, enabling resume-from-checkpoint rather than re-processing the entire file.

### Variant C: Single Transaction (Linear Process with REFramework Structure)

For processes that have no transactional loop at all — a single long-running process with
exception handling and config management — the Get Transaction Data state is traversed once
(returns a sentinel item), Process Transaction executes the full process body, and the loop
terminates when Get Transaction Data returns Nothing on the second pass.

This variant preserves the Init/End Process lifecycle and the Config/credential management
without any looping. It is appropriate when:
- The process does not iterate over a data set.
- The REFramework is used for its Config, credential, and exception-handling infrastructure
  only (single-transaction process with retry logic).

---

## 6. Invoice Processing with REFramework

Invoice processing is the most common real-world application of REFramework, combining a
Dispatcher/Performer pattern with Document Understanding and DataTable manipulation.

### Dispatcher: Load Invoice Queue

```
Init:           Read invoice file/folder path from Config.
                Authenticate to invoice source (SharePoint, SFTP, email).
GetTransaction: Pick next unprocessed invoice file.
Process:        Read invoice metadata (filename, date, source).
                Add Queue Item with InvoiceFileName, SourcePath, ReceivedDate.
                Move invoice to "In Progress" folder.
SetStatus:      Mark Successful.
End:            Log total items queued.
```

### Performer: Process Invoice Queue Items

```
Init:           Open target application (ERP, accounting system).
                Login using Config credential.
GetTransaction: Dequeue next QueueItem.
Process:
  1. Download invoice file from SourcePath (SharePoint, SFTP).
  2. Run Document Understanding extraction (or ai_parse_document → ai_extract).
  3. Validate extracted fields:
     - Invoice number: regex [A-Z]{2,3}-\d{6,10}
     - Total: must be > 0, must equal sum of line items (BusinessRuleException if not)
     - Date: must be parseable and within acceptable range (see date-handling.md)
     - Vendor name: must match vendor master lookup
  4. Navigate to invoice entry screen in target application.
  5. Type extracted fields. Verify each field after typing (re-read and compare).
  6. Submit. Capture confirmation number. Update QueueItem Output["ConfirmationNumber"].
SetStatus:
  - Success with ConfirmationNumber.
  - BusinessException for data validation failures.
  - SystemException for application failures.
End:            Log out. Send summary email (total processed, total BusinessExceptions,
                total SystemExceptions).
```

### Key LINQ Patterns in Invoice REFramework

```vb
' In GetTransactionData — filter pending invoices from a DataTable status tracker
Dim pendingRows = (From row In dtInvoiceStatus.AsEnumerable()
                   Where row("Status").ToString() = "Pending"
                   Order By DateTime.Parse(row("ReceivedDate").ToString()) Ascending
                   Select row).ToList()

' In Process — validate line items sum against header total
Dim lineItemSum As Double = dtLineItems.AsEnumerable() _
    .Sum(Function(row) CDbl(row("UnitPrice").ToString()) *
                       CDbl(row("Quantity").ToString()))

If Math.Abs(lineItemSum - dblInvoiceTotal) > 0.01 Then
    Throw New BusinessRuleException(
        "Line item sum " & lineItemSum.ToString("F2") &
        " does not match invoice total " & dblInvoiceTotal.ToString("F2"))
End If

' Find duplicate invoices already processed (prevent double-entry)
Dim existingItem = dtProcessedInvoices.AsEnumerable() _
    .FirstOrDefault(Function(row) row("InvoiceID").ToString() = strInvoiceID)
If existingItem IsNot Nothing Then
    Throw New BusinessRuleException(
        "Invoice " & strInvoiceID & " already processed on " &
        existingItem("ProcessedDate").ToString())
End If
```

### Key Regex Patterns in Invoice REFramework

```vb
' Validate invoice number format before typing into ERP
Dim invoicePattern As New System.Text.RegularExpressions.Regex(
    "^[A-Z]{2,3}-\d{6,10}$", System.Text.RegularExpressions.RegexOptions.IgnoreCase)
If Not invoicePattern.IsMatch(strInvoiceNumber.Trim()) Then
    Throw New BusinessRuleException("Invalid invoice number format: " & strInvoiceNumber)
End If

' Extract invoice number from OCR output (permissive extraction)
Dim match = System.Text.RegularExpressions.Regex.Match(
    strRawOCROutput,
    "(?:Invoice\s*(?:No|Number|#)[:\s]*)([\w\-]+)",
    System.Text.RegularExpressions.RegexOptions.IgnoreCase)
strInvoiceNumber = If(match.Success, match.Groups(1).Value.Trim(), "")

' Normalize and extract currency amount from scraped text
Dim amountMatch = System.Text.RegularExpressions.Regex.Match(
    strAmountText.Replace(",", ""), "[\d]+(?:\.\d{1,2})?")
dblAmount = If(amountMatch.Success, CDbl(amountMatch.Value), 0)
```

---

## 7. REFramework System Exception Retry Mechanics

Understanding exactly how the retry loop works prevents common misconfigurations:

1. A System Exception is thrown in `Process.xaml`.
2. `SetTransactionStatus` marks the queue item `Failed` and stores the exception details.
   Orchestrator increments the item's retry count and sets its status to `Retried` (if max
   retries not yet reached) or `Failed` permanently (if max reached).
3. `ConsecutiveSystemExceptions` counter increments.
4. If `ConsecutiveSystemExceptions >= MaxConsecutiveSystemExceptions`, the process transitions
   to End Process immediately, regardless of remaining queue items. This prevents a broken
   environment from burning through all queue items, marking each as Failed in turn.
5. Otherwise, transition to Init — re-initialize the application (close and reopen if needed).
6. On the next pass through Get Transaction Data, Orchestrator re-delivers the `Retried` item
   (it is treated as a new dequeue attempt). The retry count embedded in the item is visible
   via `TransactionItem.RetryNumber`.
7. If `Process.xaml` succeeds on retry, `ConsecutiveSystemExceptions` resets to 0.

**Configuration guidance:**
- `MaxRetryNumber = 3` is the default. For UI-heavy automations with flaky selectors, 1-2
  retries is often sufficient (third failure is usually the same failure as the first).
- `MaxConsecutiveSystemExceptions = 3` is the default. For processes running on a single
  machine with a known-stable environment, 1-2 is appropriate — fail fast rather than
  corrupting multiple transactions.
- For queue items, Orchestrator's queue-level max retry count (set in Orchestrator → Queues
  → Edit) is separate from the REFramework's `MaxRetryNumber`. Both limits apply: the item is
  abandoned if either limit is reached. The Orchestrator queue-level setting takes precedence.

---

## 8. REFramework with LINQ — Practical Patterns

LINQ is used in three distinct places within a REFramework process:

**In GetTransactionData (non-queue):** filter and sort the next transaction from a DataTable.
See `references/linq-expressions.md` — Patterns 1, 7, 11.

**In Process.xaml:** transform and validate data extracted from source applications or
documents before writing to the target application. This is the most common use: filtering
a scraped DataTable to find the matching row, aggregating line items, detecting duplicates.

**In SetTransactionStatus (non-queue):** update the status column of the transaction DataRow
and propagate to a summary DataTable for the output file.

```vb
' GetTransactionData — filter unprocessed rows, ordered by priority then date
TransactionItem = (From row In TransactionData.AsEnumerable()
                   Where row("Status").ToString() = "Pending"
                     And Not IsDBNull(row("DueDate"))
                   Order By row("Priority").ToString() Ascending,
                             DateTime.Parse(row("DueDate").ToString()) Ascending
                   Select row).FirstOrDefault()
' Returns Nothing when no more Pending rows → transitions to End Process
```

---

## 9. REFramework with Regex — Input Validation Before Writing

The REFramework's exception model makes regex validation natural: validate in
`Process.xaml` before writing to the target application, and throw `BusinessRuleException`
on format mismatch. This ensures the queue item is marked `BusinessException` (not retried)
rather than `SystemException` (retried up to max), which would waste retries on fundamentally
bad data. See `references/regex-in-rpa.md` — the validate-normalize-type workflow.

```vb
' Normalize extracted date string, then validate, then format for target system
Dim rawDate As String = row("InvoiceDate").ToString().Trim()
' Normalize separators
rawDate = System.Text.RegularExpressions.Regex.Replace(rawDate, "[./]", "-")
Dim parsedDate As DateTime
If Not DateTime.TryParseExact(rawDate,
        {"d-M-yyyy","dd-MM-yyyy","M-d-yyyy","MM-dd-yyyy","d-M-yy","dd-MM-yy"},
        System.Globalization.CultureInfo.InvariantCulture,
        System.Globalization.DateTimeStyles.None,
        parsedDate) Then
    Throw New BusinessRuleException("Cannot parse date: " & row("InvoiceDate").ToString())
End If
' Format for target system (SAP: dd.MM.yyyy; ERP field: MM/dd/yyyy)
strFormattedDate = parsedDate.ToString("dd.MM.yyyy")
```

---

## 10. REFramework in 2026: Modernization Considerations

The Community Forum discussion (March 2026) on REFramework's current relevance surfaces
several legitimate architectural tensions:

**Still best practice:**
- State machine with four states is the correct model for transactional unattended automation.
- Exception categorization (Business vs. System) is a permanent pattern, not a legacy one.
- Config.xlsx + Orchestrator Asset override pattern works well for multi-environment deployment.
- Per-item retry with recovery initialization is the right default for unattended bots.

**Where modernization is warranted:**
- The global `Config As Dictionary(Of String, Object)` is untyped. For new projects, consider
  wrapping Config in a typed class (via `Invoke Code`) to surface key-misname errors at
  development time rather than runtime.
- `Config.xlsx` as the configuration source may be superseded by Orchestrator's bucket-based
  storage or structured Assets as UiPath's platform matures.
- For processes built around Maestro (the agentic orchestration layer), REFramework's
  sequential transaction loop may be replaced by Maestro's event-driven task distribution.
  REFramework remains relevant for robot-executed steps within a Maestro workflow.
- The `MaxConsecutiveSystemExceptions` circuit breaker should be reduced from the default
  `3` in production environments — fail the run fast, alert operations, rather than burning
  through multiple transactions in a broken environment.

---

## 11. Official Resources

| Resource | Location | Notes |
|---|---|---|
| Official REFramework GitHub | github.com/UiPath/ReFrameWork | Canonical VB.NET template; pull this rather than the Studio template if you need the latest version |
| REFramework for Tabular Data | marketplace.uipath.com/listings/reframework-for-tabular-data | Official non-queue variant; `TransactionItem` typed as `DataRow` |
| REFramework without Queue | marketplace.uipath.com/listings/re-framework-without-queue | Community variant; status file pattern; good reference for the output-file approach |
| UiPath Academy: Advanced RPA Developer | academy.uipath.com | Contains the full REFramework training module with exercises |
| Document Understanding Process Template | docs.uipath.com/document-understanding | Based on REFramework; adds a Document Understanding extraction phase |

---

## Sources Consulted

- UiPath official GitHub: github.com/UiPath/ReFrameWork (verified July 2026) — canonical
  template source; all workflow names, state names, and default Config keys are from this
  repository.
- UiPath Marketplace: REFramework for Tabular Data
  (marketplace.uipath.com/listings/reframework-for-tabular-data, verified July 2026) — source
  for the DataRow variant mechanics (`TransactionData` in Init, `TransactionNumber` index
  pattern, status file approach).
- UiPath Marketplace: REFramework without Queue (marketplace.uipath.com/listings/re-framework-
  without-queue, verified July 2026) — source for the no-retry-on-tabular rationale and
  receipt/email-on-completion pattern.
- UiPath Community Forum: "REFramework in 2026: Still Best Practice or Due for
  Modernization?" (forum.uipath.com, March 2026) — source for the modernization considerations
  in Section 10.
- UiPath Community Forum: "ReFramework official" (forum.uipath.com, January 2018) — confirms
  the GitHub repository as the official canonical source.
- UiPath Documentation: Document Understanding Process Template, based on REFramework
  (docs.uipath.com/document-understanding, verified July 2026).

The REFramework state machine architecture, exception model, and Config.xlsx pattern are
stable and have not changed materially since 2019. The Maestro integration considerations
and the `MaxConsecutiveSystemExceptions` guidance are the parts of this file most likely
to evolve as the UiPath platform matures.
