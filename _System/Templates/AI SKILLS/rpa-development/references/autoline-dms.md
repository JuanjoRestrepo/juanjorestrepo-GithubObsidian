> Content in this file is grounded in publicly available Keyloop developer documentation
> (developer.keyloop.io, verified July 2026), CDK Global product documentation
> (cdkglobal.co.uk/products-dms, July 2026), industry analysis of DMS automation complexity
> (minicor.com/blog, July 2026), and general UiPath UI automation best practices from
> docs.uipath.com. Organization-specific Autoline workflows, screen layouts, and business
> rules are NOT documented here; those belong in the process-specific SDD and must be
> provided by the team. This file covers the platform architecture, integration patterns,
> and UiPath automation techniques applicable to any Autoline deployment.

# Autoline DMS: Automation Reference

## 1. What Autoline Is

Autoline (now branded as **Keyloop Autoline**, formerly CDK Autoline) is a Dealer Management
System (DMS) — an enterprise application suite that manages the full lifecycle of an automotive
dealership: vehicle sales, aftersales service (repair orders, workshop scheduling), parts
inventory, customer relationship management, and dealer accounting.

**Publisher:** Keyloop (formerly CDK Global's international DMS division, rebranded ~2021).
**Deployment model:** Client-server Windows desktop application with a server-side database.
Market-specific variants exist: Autoline Drive (newer, more modern UI), Autoline Rev8 (legacy,
character-based / hybrid UI), and regional variants (Aswin, Windrakkar, EVA, Automaster share
the same Keyloop platform and API surface).

**Why DMS automation is harder than standard enterprise UI automation:**

- <cite index="29-1">DMS interfaces are complex: multi-step forms with conditional fields, nested tabs, and
  validation rules that vary by dealership configuration. A single workflow might involve ten
  screens, each with multiple fields and branching logic.</cite>
- Selector-based automation breaks when Keyloop pushes DMS updates.
- The application renders with legacy Windows controls (legacy versions) or hybrid
  web/desktop controls (Drive variant), requiring different selector strategies per variant.
- Business logic is encoded in the DMS itself: field values that are valid in one context
  are rejected in another based on the current state of the record.

---

## 2. Integration Priority Order for Autoline

Before building UI automation, always check the Keyloop API first. The priority order is
identical to this skill's general integration priority (see SKILL.md main file):

```
1. Keyloop API (developer.keyloop.io)     — preferred: structured, version-stable
2. Direct database query (SQL Server)     — for read-only reporting/extraction
3. UI automation (UiPath + selectors)     — for operations with no API equivalent
4. Computer Vision / OCR                  — only when UI automation selectors fail
```

---

## 3. Keyloop API: What Is Available

Keyloop publishes a REST API platform at `developer.keyloop.io`. API access requires
enrolment in the Keyloop Partner Programme. Coverage as of July 2026:

| Product | Availability (DMS variants) | Key endpoints |
|---|---|---|
| **Find Vehicle Service History** | Autoline, Autoline Drive, Autoline Rev8, Windrakkar, Automaster, DRACAR+, EVA | `GET /service-history`, `GET /service-history/{serviceHistoryId}` |
| **Inspect Vehicle — Basic** | Autoline, Autoline Drive, Automaster, DRACAR+, EVA, Aswin, Windrakkar | `GET /repair-orders`, `GET /repair-orders/{id}`, add/remove/get jobs |
| **Inspect Vehicle — Advanced** | Autoline, Autoline Drive, Automaster, DRACAR+, EVA, Aswin, Windrakkar | Full repair order lifecycle: create, check-in, check-out, add jobs/parts/labor/menus/discounts/notes |
| **Book a Service Appointment** | Multiple variants | Online service booking endpoints |
| **Order Parts** | Autoline, Aswin, DRACAR+, Drive, EVA, Windrakkar, Automaster | Parts pricing, availability, order placement, order status |
| **Parts Catalogue** | Multiple variants | Parts lookup by code, supersession, pricing, supplier catalogue updates |

**Repair Order endpoints (Inspect Vehicle — Advanced) — full list:**

```
GET  /repair-orders
POST /repair-orders
GET  /repair-orders/{repairOrderId}
POST /repair-orders/{repairOrderId}/check-in
POST /repair-orders/{repairOrderId}/check-out
PATCH /repair-orders/{repairOrderId}/appointment
PATCH /repair-orders/{repairOrderId}/details
POST /repair-orders/{repairOrderId}/jobs
POST /repair-orders/{repairOrderId}/multipleJobs
GET  /repair-orders/{repairOrderId}/jobs/{jobId}
DELETE /repair-orders/{repairOrderId}/jobs/{jobId}
POST /repair-orders/{repairOrderId}/jobs/{jobId}/fees
POST /repair-orders/{repairOrderId}/jobs/{jobId}/items
POST /repair-orders/{repairOrderId}/jobs/{jobId}/discount
POST /repair-orders/{repairOrderId}/jobs/{jobId}/labor
POST /repair-orders/{repairOrderId}/jobs/{jobId}/menus
POST /repair-orders/{repairOrderId}/jobs/{jobId}/notes
POST /repair-orders/{repairOrderId}/jobs/{jobId}/parts
PATCH /repair-orders/{repairOrderId}/planning
```

**Integration with UiPath via API:** use UiPath's `HTTP Request` activity (or custom
C# activities wrapping `HttpClient`) with the Keyloop OAuth token stored in Orchestrator
as a Credential asset. Keyloop uses OAuth 2.0; token refresh must be managed within the
bot (refresh before expiry, store the refreshed token in a workflow variable).

---

## 4. When UI Automation Is Required

API coverage is expanding but not complete. UI automation is required for:

- Operations not yet exposed in the Keyloop API (accounting entries, certain report generation,
  complex multi-step data entry workflows with DMS-enforced business logic).
- Processes running on Autoline deployments where API access has not been arranged (Partner
  Programme enrolment takes time; some markets/markets/franchise configs are not enrolled).
- Processes that integrate Autoline with other non-API-accessible systems where a single
  bot must operate multiple UIs in sequence.

---

## 5. Autoline UI Automation: Window and Application Management

### Application Structure

Autoline typically presents as a Windows desktop application with:
- A **main navigation frame** (menu bar, function key shortcuts, module navigation tree).
- **Work area** — one or more document windows within the main frame (MDI — Multiple Document
  Interface in legacy versions; tabbed or floating panels in Drive).
- **Popup dialogs** — confirmation dialogs, lookup/search popups, error messages.

Autoline uses a mix of Win32 controls (TextBox, ComboBox, DataGrid) in legacy versions and
WPF or hybrid controls in Drive. The selector strategy must match the control technology.

### Window Management

```vb
' Attach to Autoline main window (adjust selector to match your DMS version/title)
' Use Attach Window or Application/Browser activities to scope all subsequent UI activities

' Recommended selector pattern for main window (adjust title as needed)
<wnd app='autoline.exe' title='Autoline*' />

' Wait for application to be ready before interacting
' Use "Wait App State" or a deliberate "Element Exists" check before the first interaction:
<wnd app='autoline.exe' title='*Autoline*' />

' For MDI child windows — target the inner document window, not the main frame
<wnd app='autoline.exe' cls='MDIClient' /><wnd title='*Service Order*' />
```

### Focus and Activation

Legacy Autoline can lose focus during long operations. Always:
- Use `Activate` or `Click` on a neutral area of the target window before starting a
  keystroke-heavy sequence.
- Wrap each logical screen transition in a `Wait for Element` / `Element Exists` check
  rather than assuming the navigation completed.

---

## 6. Selectors: Targets and Anchors in Autoline

### Selector Strategy Priority (Autoline-Specific)

1. **Stable attribute selectors** (by `name`, `automationId`, `className` + `idx`) — prefer
   when controls have stable IDs. In Drive (web-based panels), use `aaname`, `tag`, `type`.
2. **Anchored selectors** — when a field's own attributes are unstable but a nearby label
   or static element is stable. Use `UiPath.Core.Activities.AnchorBase` with the label as
   anchor and the input field as the target.
3. **Computer Vision** (see Section 7) — for Citrix-hosted Autoline or when UI controls
   are rendered images without accessible attributes.
4. **Send Hotkeys / function key navigation** — Autoline relies heavily on function keys
   (F1–F12) for navigation between screens and confirmation. These are often more stable
   than click-based selectors for navigation steps.

### Common Selector Patterns

```xml
<!-- Field identified by its label — use Anchor Base -->
<!-- Anchor: label control with text "Registration No" -->
<ctrl name='Registration No' role='text' />
<!-- Target: input field adjacent to that label -->
<ctrl role='editable text' />

<!-- Field by tab order position (fragile — avoid where possible) -->
<wnd cls='Edit' idx='3' />

<!-- Function key confirmation (more stable than clicking OK button) -->
<!-- Use "Send Hotkey" activity with F8, F10, Escape, etc. -->

<!-- Popup dialog — always use title to scope -->
<wnd title='Confirm' />
<ctrl name='Yes' role='push button' />
```

### Anchor Base Pattern for Autoline Fields

When a field does not have a unique `name` or `automationId` attribute, use Anchor Base:

1. Set the Anchor to the **label** immediately left of or above the field. Labels in Autoline
   are typically `Static` controls or `text` role elements with stable text content.
2. Set the Target to the **input field** immediately right of or below the anchor.
3. Set the Anchor position to `Left`, `Top`, `Right`, or `Bottom` matching the label's
   position relative to the input.

If the label itself is not unique (multiple fields labelled "Date" on the same screen), scope
the entire interaction to the panel or group box that contains the target field first.

---

## 7. Computer Vision in Autoline

Use Computer Vision (CV) activities when:
- Autoline is accessed via Citrix (the application window is an image, not a native Win32
  process) — see `references/citrix-automation.md` for the Citrix automation technique
  hierarchy.
- A control does not expose accessible attributes (rendered as a graphic element, not a
  Win32 or WPF control).

CV activities in UiPath use the AI-based `CV Click`, `CV Type`, `CV Get Text`, `CV Check`,
and `CV Select` activities. They operate on a screenshot of the application window and locate
elements by visual appearance rather than by UI control attributes.

**Autoline-specific CV guidance:**

- **Train the CV model** on representative screenshots of each screen used in the process.
  CV accuracy degrades if DMS screen resolution, theme, or zoom level changes between training
  and production — standardize these at the machine configuration level.
- Always use **anchors in CV activities** (a stable nearby visual element — a label, icon, or
  static graphic) to constrain the search region. CV without an anchor searches the entire screen,
  which is slow and produces false positives on screens with repeated visual elements.
- **CV Get Text** accuracy depends on the screen rendering and text antialiasing settings of
  the Autoline host machine. See `references/regex-in-rpa.md` — OCR Engine Selection section
  for guidance on when to supplement CV with an explicit OCR engine.

---

## 8. Error Handling and Recovery in Autoline Automation

Autoline produces several categories of errors that require distinct recovery strategies:

| Error category | Symptom | Recovery approach |
|---|---|---|
| **Field validation error** | DMS shows an inline error message or popup after typing a value | Read the error message text (Get Text / CV Get Text on the error region). Map to BusinessRuleException or retry with corrected value depending on whether the error is data-driven or app-driven. |
| **Record locked** | DMS shows "Record in use" / "Locked by user X" popup | If expected (another user has the record open), raise BusinessRuleException. If unexpected (stale lock from a previous failed bot run), alert operations — do not attempt to force-unlock programmatically. |
| **DMS session timeout / auto-logout** | Main window disappears or login screen appears | Detect in Global Exception Handler. Re-login via InitAllApplications. REFramework will recover if SystemException is thrown. |
| **DMS popup dialog blocks navigation** | Unexpected dialog appears, next activity fails because expected element is not present | Use "Element Exists" before each navigation step. If unexpected dialog detected, attempt to dismiss with Escape, log the dialog text, raise SystemException. |
| **Slow screen load** | Activity timeout before the next screen loads | Do not use fixed delays. Use "Wait Element Vanish" on the loading indicator or "Element Exists" on a stable element of the target screen. See Section 9. |
| **Wrong screen/navigation state** | Bot navigates to the wrong menu path due to a previous partial action | At the start of each major navigation sequence, use a "Get Active Window" or title check to assert the expected screen is open before proceeding. |

### Global Exception Handler Pattern for Autoline

In `Main.xaml` (State Machine body), use a Global Exception Handler to:
1. Take a screenshot of the current application state.
2. Log the exception with the active window title as context.
3. Attempt to close popup dialogs (Escape) and return to the main navigation menu.
4. Re-throw as `SystemException` to trigger REFramework's recovery path.

---

## 9. Delays and Timing Optimization

### Guiding Principle: Never Use Static Delays

Fixed `Delay` activities are the primary cause of slow bots. Replace every `Delay` with a
dynamic wait:

| Static delay use case | Dynamic replacement |
|---|---|
| Wait for screen to load after navigation | `Element Exists` on first stable element of target screen (loop with short interval + counter) |
| Wait for loading spinner to disappear | `Wait Element Vanish` on the spinner/progress element |
| Wait for DMS to process a transaction | `Wait Element Appear` on the confirmation message or status change |
| Wait for popup to appear | `Wait Element Appear` on the popup's title or content |
| Wait for field to become enabled | `Element Exists` with `enabled=true` attribute in selector |

### Dynamic Wait Pattern (Autoline)

```vb
' Wait up to maxWait seconds for target element to appear (in Invoke Workflow)
Dim waited As Integer = 0
Dim maxWait As Integer = CInt(Config("ElementWaitTimeout")) ' from Config.xlsx
Dim bElementFound As Boolean = False
Do While Not bElementFound AndAlso waited < maxWait
    bElementFound = uiElement.Exists(TimeSpan.FromSeconds(1))
    If Not bElementFound Then
        waited += 1
        ' Optional: check for error dialogs here during the wait
    End If
Loop
If Not bElementFound Then
    Throw New Exception("Element not found after " & maxWait & " seconds: " & selectorDescription)
End If
```

### DMS-Specific Timing Considerations

- **Server round-trips:** Autoline operations that write to the database (save, commit, post)
  take longer than read operations. Wait for the DMS's own "saved" or "posted" confirmation
  before reading back the result.
- **Batch operations:** Operations that trigger DMS background jobs (batch posting, overnight
  runs) should not be polled from a bot. Design these as fire-and-check processes: trigger the
  batch, exit the bot, schedule a second bot run to verify completion.
- **Multi-user contention:** In a shared DMS environment with many concurrent users, operations
  that lock records (editing a repair order, posting a parts transaction) may experience
  intermittent lock failures. Include a `RetryScope` around lock-sensitive operations.

---

## 10. Data Handling in Autoline Automation

### Date Fields

Autoline date fields typically accept `dd/MM/yyyy` format in UK and AU markets. Always use
`ParseExact` when reading dates from Autoline screens, and always format dates explicitly
before typing. See `references/date-handling.md` for the full normalize → validate → format
→ type workflow.

Autoline internally may store or expose dates in formats other than what the screen shows —
database-level reads via SQL Server will see dates in SQL `datetime` format; API responses
from Keyloop use ISO 8601.

### Part Numbers and VINs

```vb
' VIN validation — 17-character ISO 3779 standard (no I, O, Q)
Dim vinPattern As New System.Text.RegularExpressions.Regex(
    "^[A-HJ-NPR-Z0-9]{17}$",
    System.Text.RegularExpressions.RegexOptions.IgnoreCase)
If Not vinPattern.IsMatch(strVIN.Trim()) Then
    Throw New BusinessRuleException("Invalid VIN format: " & strVIN)
End If

' Clean part number — strip spaces, normalize case
strPartNumber = System.Text.RegularExpressions.Regex.Replace(
    strPartNumber.Trim().ToUpper(), "\s+", "")

' Service Order / Repair Order number — typical format varies by market
' AU example: numeric 6-8 digits; UK example: alphanumeric prefix-number
Dim roPattern As New System.Text.RegularExpressions.Regex("^\d{6,8}$")
If Not roPattern.IsMatch(strRONumber.Trim()) Then
    Throw New BusinessRuleException("Invalid RO number: " & strRONumber)
End If
```

### Amount and Currency Fields

```vb
' Clean scraped currency values from Autoline screen
' Input examples: "$1,234.56", "1,234.56", "1234.56", "-$500.00"
Dim amountStr As String = strScrapedAmount.Trim()
' Remove currency symbol and thousand separators
amountStr = System.Text.RegularExpressions.Regex.Replace(amountStr, "[$£€,]", "")
Dim dblAmount As Double
If Not Double.TryParse(amountStr,
        System.Globalization.NumberStyles.Any,
        System.Globalization.CultureInfo.InvariantCulture,
        dblAmount) Then
    Throw New BusinessRuleException("Cannot parse amount: " & strScrapedAmount)
End If
```

### Typing Activities: Simulation vs. Hardware Events

Autoline fields frequently respond only to **hardware-emulated keystrokes** (SimulateType =
False, SendWindowMessages = False). The DMS uses keyboard event listeners that do not fire on
simulated input:

- Default `Type Into` mode (hardware events) is the correct starting point.
- `SimulateType = True` is faster but bypasses the DMS's field validation triggers — fields
  may accept the value visually but not commit it to the database.
- `SendWindowMessages = True` is a middle ground — slower than simulate but more compatible
  than hardware with some controls.
- For fields that require Tab to move to the next field and trigger validation (common in
  Autoline), always send a Tab keystroke (`Send Hotkey: Tab`) after each field entry rather
  than clicking the next field.

**Type Into sequence for Autoline fields:**

```
1. Click field (to focus — do NOT use SimulateType for the click)
2. Send Hotkey: Ctrl + A  (select all existing content)
3. Type Into: [value]     (hardware events, not simulated)
4. Send Hotkey: Tab       (trigger field validation and move to next field)
5. Verify (optional): Get Text from field, compare to typed value
```

### Worksheet / DataTable Handling

When Autoline data is exported to Excel (via the DMS's own export function, or via screen-
scraping a grid):

```vb
' Read Autoline export file — use Read Range with PreserveFormat = False
' so numeric-looking strings (part numbers like "001234") are not auto-converted to numbers

' Clean up Autoline date columns (often exported as strings)
For Each row As DataRow In dtAutolineExport.AsEnumerable()
    If Not IsDBNull(row("InvoiceDate")) AndAlso row("InvoiceDate").ToString().Trim() <> "" Then
        Dim parsedDate As DateTime
        If DateTime.TryParseExact(row("InvoiceDate").ToString().Trim(),
                {"dd/MM/yyyy","d/MM/yyyy","dd/M/yyyy"},
                System.Globalization.CultureInfo.InvariantCulture,
                System.Globalization.DateTimeStyles.None, parsedDate) Then
            row("InvoiceDate") = parsedDate.ToString("yyyy-MM-dd")  ' normalize to ISO
        Else
            row("InvoiceDate") = DBNull.Value  ' invalid date — mark as null
        End If
    End If
Next

' Filter to current month's invoices using LINQ
Dim currentMonthInvoices = (From row In dtAutolineExport.AsEnumerable()
    Where Not IsDBNull(row("InvoiceDate"))
      And DateTime.Parse(row("InvoiceDate").ToString()).Year = Now.Year
      And DateTime.Parse(row("InvoiceDate").ToString()).Month = Now.Month
    Select row).CopyToDataTable()

' De-duplicate by RO number (keep most recent)
Dim deduped = (From row In dtAutolineExport.AsEnumerable()
    Group row By Key = row("RONumber").ToString() Into grp = Group
    Select grp.OrderByDescending(Function(r) r("InvoiceDate").ToString()).First()
    ).CopyToDataTable()
```

---

## 11. Common Automation Scenarios

| Scenario | API available? | Approach |
|---|---|---|
| Service history lookup by VIN | Yes | Keyloop API `GET /service-history` |
| Repair order search and read | Yes | Keyloop API `GET /repair-orders` with filter params |
| Create new repair order | Yes (Advanced) | Keyloop API `POST /repair-orders` |
| Add jobs/parts to existing RO | Yes (Advanced) | Keyloop API endpoints above |
| Parts pricing and availability check | Yes | Keyloop API `GET /parts` |
| Place parts order | Yes | Keyloop API Order Parts product |
| Invoice extraction for accounting | Not yet (as of July 2026) | UI automation: navigate to invoice screen, scrape fields, validate, write to target |
| Warranty claims submission | Not yet | UI automation: multi-screen workflow |
| Vehicle registration update | Not yet | UI automation: CRM/vehicle admin module |
| Labour posting / technician time | Not yet | UI automation: aftersales posting screen |
| DMS report generation and export | Not yet | UI automation: run report, export, process file |
| Balance/account inquiry | Not yet | UI automation or direct SQL read |

---

## 12. API Integration via UiPath (Keyloop REST)

```vb
' OAuth token retrieval — store client_id and client_secret in Orchestrator Credential Asset
Dim strClientID     As String = Config("KeyloopClientID").ToString()
Dim strClientSecret As String = Config("KeyloopClientSecret").ToString()
Dim strTokenURL     As String = Config("KeyloopTokenURL").ToString()

' Use HTTP Request activity (POST) to obtain access token
' Body: grant_type=client_credentials&client_id=...&client_secret=...
' Response: {"access_token":"...","expires_in":3600,...}

' Store token + expiry in workflow variables; refresh before each API call if within 60s of expiry

' Search repair orders by VIN
' GET /repair-orders?vin={vin}&status=OPEN
' Headers: Authorization: Bearer {access_token}
'           Accept: application/json
'           Content-Type: application/json
```

Use `Deserialize JSON` activity to parse the response. Access nested fields with
`jObject("data")("repairOrders")(0)("repairOrderId").ToString()`.

---

## Sources Consulted

- Keyloop Developer Portal: developer.keyloop.io — Products listing (July 2026), Inspect
  Vehicle Basic and Advanced endpoint lists, Order Parts, Find Vehicle Service History, Parts
  Catalogue. All endpoint URLs and DMS availability claims are from this source.
- CDK Global UK: cdkglobal.co.uk/products-dms/autoline.asp — product description, Autoline
  Drive branding and features.
- Information Systems Ltd (Malta): isl.com.mt/products/autoline-dms — Autoline module
  structure (CRM, Vehicle Sales, Aftersales Service, Parts, Accounting).
- Minicor Blog: "How to Automate CDK Global and Dealer Management Systems"
  (minicor.com/blog, July 2026) — industry analysis of DMS automation complexity, selector
  fragility, and the computer-use agent approach as a complement to traditional RPA.
- UiPath official documentation: UI Automation activities, Anchor Base, Computer Vision,
  Global Exception Handler (docs.uipath.com, July 2026).
- Keyloop Partner Programme page (keyloop.com/keyloop-partner-programme) — partner integration
  examples confirming API availability for parts ordering and VHC workflows.

Organization-specific Autoline screen layouts, field validation rules, module configurations,
and business processes are NOT in this file. They must be documented in the process-specific
PDD/SDD from direct observation of the live system. The Keyloop API endpoint availability
table is current as of July 2026 — verify at developer.keyloop.io before scoping a new
process, as the partner API is actively expanding.
