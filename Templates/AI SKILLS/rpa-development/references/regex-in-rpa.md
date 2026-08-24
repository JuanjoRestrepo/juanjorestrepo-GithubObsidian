# Regular Expressions in RPA and Automation — Deep Reference

> This file covers regular expressions (regex) as used throughout the automation stack in this
> skill: UiPath (VB.NET's `System.Text.RegularExpressions`), Python (`re` / `regex` module),
> Power Automate Cloud expressions (`uriComponent`, `replace`, `split` and their limits), and
> the specific RPA context of UI automation (selectors, field validation, text extraction from
> UI output). The regex syntax described is standard PCRE/NFA-based regex, the model used by
> .NET (`System.Text.RegularExpressions`), Python `re`, and JavaScript — these differ in minor
> ways noted where relevant.

## Why Regex Matters in RPA Specifically

UI automation surfaces text — from scraped screen output, OCR results, PDF extractions, web
scrapes, and typed-input validation — in a form that is rarely perfectly clean and that varies
between runs in predictable ways (an amount field might be `$1,234.56` one run and `1234.56`
the next; a date might be `2026-08-09` or `09/08/2026` depending on user locale). Ad hoc string
manipulation (repeated `Replace`/`Split`/`Substring` chains) is the most common source of
fragile, hard-to-maintain data-handling code in RPA projects. Regex replaces a five-activity
string-chasing sequence with a single, explicit, testable pattern — applied well, it's both
simpler and more reliable than the alternative.

The two main RPA uses:

1. **Extraction**: pull a specific piece of text out of a larger string (an invoice number from
   a scraped page, an amount from an email body, a reference code from a status message).
2. **Validation**: confirm that a field's content matches an expected format before typing it
   into or reading it from a UI target (this is the `Type Into`-adjacent use the request
   specifically mentions).

## Regex Fundamentals: Cheat Sheet for RPA Work

| Construct          | Meaning                                                      | Example                            |
| ------------------ | ------------------------------------------------------------ | ---------------------------------- |
| `.`                | Any single character (except newline)                        | `A.C` matches `ABC`, `A1C`         |
| `\d`               | Digit `[0-9]`                                                | `\d{4}` matches `2026`             |
| `\D`               | Non-digit                                                    |                                    |
| `\w`               | Word character `[A-Za-z0-9_]`                                |                                    |
| `\W`               | Non-word character                                           |                                    |
| `\s`               | Whitespace (space, tab, newline)                             |                                    |
| `\S`               | Non-whitespace                                               |                                    |
| `^`                | Start of string (or line in multiline mode)                  |                                    |
| `$`                | End of string (or line in multiline mode)                    |                                    |
| `[abc]`            | Character class — any of a, b, c                             |                                    |
| `[^abc]`           | Negated class — anything except a, b, c                      |                                    |
| `[a-z]`            | Range                                                        | `[A-Za-z]` matches any letter      |
| `{n}`              | Exactly n repetitions                                        | `\d{4}`                            |
| `{n,m}`            | Between n and m repetitions                                  | `\d{2,4}`                          |
| `*`                | 0 or more (greedy)                                           |                                    |
| `+`                | 1 or more (greedy)                                           |                                    |
| `?`                | 0 or 1 (also makes quantifier lazy when appended to another) |                                    |
| `*?` `+?` `{n,m}?` | Lazy (non-greedy) — match as little as possible              |                                    |
| `(...)`            | Capturing group — value accessible by index                  |                                    |
| `(?:...)`          | Non-capturing group — grouping without capture overhead      |                                    |
| `(?<name>...)`     | Named capturing group — value accessible by name             |                                    |
| `\|`               | Alternation (OR)                                             | `cat\|dog`                         |
| `(?=...)`          | Lookahead — match if followed by                             | `\d+(?= USD)`                      |
| `(?!...)`          | Negative lookahead                                           |                                    |
| `(?<=...)`         | Lookbehind — match if preceded by                            | `(?<=Invoice #)\d+`                |
| `(?<!...)`         | Negative lookbehind                                          |                                    |
| `\b`               | Word boundary                                                | `\bTotal\b` won't match `SubTotal` |

**Greedy vs. lazy** is the single most common source of regex bugs in RPA text extraction:
a greedy `.*` expands as far as possible, often consuming more than intended. Use `.*?` (lazy)
whenever extracting content between two delimiters, and anchor both ends as tightly as possible
rather than relying on the engine to stop in the right place.

## UiPath: `System.Text.RegularExpressions` in Practice

UiPath Studio (VB project) exposes the full .NET `System.Text.RegularExpressions` namespace.
The three activities/methods used most often:

### Matches (extract all occurrences)

```vb
' Activity: Matches
' Input: strSourceText, "\d{1,3}(?:,\d{3})*(?:\.\d{2})?" (finds currency amounts)
' Output: IEnumerable(Of Match) → assign to colMatches
'
' Then iterate colMatches:
' For Each match In colMatches
'     strAmount = match.Value   ' e.g. "1,234.56"
' Next
```

Use when you need every occurrence of a pattern in the source text. The output is an enumerable
of `Match` objects — access `.Value` for the matched string, `.Groups` for captured groups.

### IsMatch (validate a field before acting on it)

```vb
' Returns Boolean — use in an If condition or Assign:
boolIsValid = System.Text.RegularExpressions.Regex.IsMatch(
    strFieldValue,
    "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
)
' Pattern: ISO date YYYY-MM-DD
```

This is the `Type Into`-adjacent use: before typing a value into a UI field (or before
processing output read from one), validate it matches the expected format rather than letting
an invalid value flow through silently. An `IsMatch` check that raises a `BusinessException`
on failure is materially better than discovering the downstream system rejected the value two
steps later with an opaque error message.

### Replace (clean and normalize extracted text)

```vb
' Strip everything that isn't a digit, dot, or hyphen from a scraped amount:
strClean = System.Text.RegularExpressions.Regex.Replace(
    strRaw, "[^\d.\-]", ""
)
' "$ 1,234.56" → "1234.56" (after also removing comma with a second pass, or a combined pattern)
```

Prefer `Regex.Replace` over chained `String.Replace` calls when the characters to remove follow
a pattern rather than being a fixed list — one regex replaces three or four individual `Replace`
activities, and the intent is explicit in the pattern string rather than implicit in the chain.

### Named groups: the right way to extract multiple fields in one pass

```vb
Dim pattern As String = "INV-(?<InvoiceNo>\d{5,8}).*?(?<Amount>\d{1,3}(?:,\d{3})*\.\d{2})"
Dim m As Match = Regex.Match(strSourceText, pattern, RegexOptions.Singleline)
If m.Success Then
    strInvoiceNo = m.Groups("InvoiceNo").Value   ' e.g. "00123"
    strAmount    = m.Groups("Amount").Value      ' e.g. "1,234.56"
End If
```

Named groups (`(?<Name>...)`) produce self-documenting code — `m.Groups("InvoiceNo")` is
unambiguous; `m.Groups(1)` requires counting parentheses to understand. Use named groups for
any regex that extracts more than one piece of data.

### `RegexOptions` flags worth knowing

| Flag             | VB constant               | Use for                                                                                   |
| ---------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| Case-insensitive | `RegexOptions.IgnoreCase` | User-facing text where case varies (`Total` vs `TOTAL`)                                   |
| Multiline        | `RegexOptions.Multiline`  | `^`/`$` match start/end of each line, not just the whole string                           |
| Singleline       | `RegexOptions.Singleline` | `.` matches newline — required when extracted text spans multiple lines                   |
| Compiled         | `RegexOptions.Compiled`   | Pre-compiles the pattern; worth it when the same pattern runs hundreds of times in a loop |

### UiPath Selector Context: Regex-Like Wildcards

UiPath selectors use a simplified wildcard syntax (`*` for any sequence of characters, `?` for
any single character) that is **not** full regex — it's a distinct, simpler pattern language.
When a dynamic attribute value follows a predictable format but varies across runs (an auto-
incremented ID, a timestamp embedded in a `aaname`), use:

- `*` to replace the variable segment: `aaname="Invoice 2026-*"` matches any date suffix.
- `?` sparingly for single-character variation.
- For cases where wildcards aren't expressive enough, switch to the attribute's **pattern
  selector variant** (available in UI Explorer for some attributes) which accepts proper regex,
  or use a **dynamic selector** built with a VB `String.Format` / string interpolation expression
  rather than embedding a hardcoded value.

Never put a raw UiPath wildcard selector string into `Regex.IsMatch` — they use different
syntaxes and a `*` in a wildcard means something different from `*` in regex (`{0 or more of
the preceding}` in regex, `{any sequence}` in selector wildcards).

## Python: `re` Module Best Practices

```python
import re

# Always compile patterns used more than once — avoids recompiling on every call
DATE_PATTERN = re.compile(
    r"(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])-(?P<day>0[1-9]|[12]\d|3[01])"
)

# Extraction — re.search finds the first match anywhere in the string
m = DATE_PATTERN.search(text)
if m:
    year  = m.group("year")
    month = m.group("month")

# Validation — re.fullmatch requires the entire string to match (preferred over re.match
# which only anchors the start, not the end — a common source of accepting invalid input)
def is_valid_invoice_id(value: str) -> bool:
    return bool(re.fullmatch(r"INV-\d{5,8}", value))

# Extraction of all occurrences — re.findall with groups returns list of tuples
amounts = re.findall(r"(\d{1,3}(?:,\d{3})*\.\d{2})", text)

# Clean/normalize — re.sub
clean = re.sub(r"[^\d.]", "", raw_amount)  # keep only digits and decimal point
```

Use **raw strings** (`r"..."`) for every regex pattern — without the `r` prefix, backslash
sequences like `\d` and `\b` require double-escaping (`\\d`, `\\b`), which makes patterns
harder to read and compare against documentation.

Use `re.fullmatch` over `re.match` for validation — `re.match` only anchors the start of the
string, so `re.match(r"\d{4}", "2026abc")` succeeds (matches the first 4 characters). Only
`re.fullmatch` (or explicitly anchoring with `^` and `$`) confirms the whole string is valid.

## Power Automate Cloud: Regex Limitations and Workarounds

Power Automate Cloud **does not expose a native regex function** in its expression language as of
this writing — there is no `regexMatch()` or `regexExtract()` built-in. Available text functions
(`replace()`, `split()`, `substring()`, `indexOf()`, `startsWith()`, `endsWith()`, `contains()`)
cover simple cases but cannot express pattern-based matching or extraction.

**Practical approaches when regex is genuinely required in a Cloud flow:**

1. **Delegate to a child flow or HTTP action that calls Python/Azure Function**: a Python Azure
   Function that accepts a string and a pattern, and returns match/no-match plus extracted groups,
   is the cleanest way to bring regex into a Power Automate Cloud flow — it stays in the
   integration layer (an HTTP connector action calling the function) and keeps the regex
   maintainable in Python code rather than buried in an expression.
2. **Power Automate Desktop as the text-processing leg**: when a process already uses a Desktop
   flow for another step, place the regex logic there (PAD exposes `RegEx` actions natively) and
   return the extracted/validated value as a Desktop flow output variable to the parent Cloud flow.
3. **Reformulate as a combination of built-in functions**: for predictable, structured inputs
   (a fixed-width field, a delimiter-separated format), `split()`/`substring()`/`indexOf()` can
   extract reliably without regex — prefer this when it handles the real input variation correctly,
   because it's more readable to a non-technical reviewer than a regex pattern would be.

Do not reach for a workaround that produces a regex-shaped expression out of nested `replace()`
and `substring()` calls — if the logic is complex enough to need that, it's complex enough to
justify delegating to a code-capable layer (Python/Azure Function/Desktop flow).

## Patterns for Common RPA Scenarios

```text
Invoice/reference numbers (alphanumeric with prefix):
  (?i)INV-\d{5,8}|REF-[A-Z0-9]{6,12}

Currency amounts (US format, optional leading sign):
  -?\d{1,3}(?:,\d{3})*(?:\.\d{2})?

Dates — ISO 8601 (YYYY-MM-DD):
  \d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])

Dates — slash-separated (DD/MM/YYYY or MM/DD/YYYY):
  (0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/\d{4}

Email address (RFC 5322 simplified, suitable for validation not parsing):
  [a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}

Australian phone number (mobile: 04xx, landline: 02/03/07/08):
  (?:0[234578]\d{8}|\+614\d{8})

UK postcode:
  [A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}

Extract value between two known delimiters (lazy):
  (?<=StartDelimiter).*?(?=EndDelimiter)

Leading/trailing whitespace (for normalization):
  ^\s+|\s+$

Non-printable/control characters (for sanitizing OCR output):
  [^\x20-\x7E]
```

These are starting points — test every pattern against the actual input variation from the
target system, not just a clean example. OCR output in particular introduces character
substitutions (`0` vs `O`, `1` vs `l`/`I`, `,` vs `.`) that a pattern that works perfectly
against a clean string may fail on.

## Regex in UI Automation: Type Into, Get Text, and Field Interaction

This is the most directly RPA-specific use of regex, and the most commonly under-applied. Every
UI interaction that reads from or writes to a field has an implicit data contract — the field
expects a certain format, and the source data may or may not conform to it. Making that contract
explicit with regex is what separates a robust flow from one that fails silently when input
varies.

### Before `Type Into` — Input Validation

The `Type Into` activity sends keystrokes to a UI element. If the value being typed is invalid
for the target field (wrong format, unexpected characters, wrong length), the application either
silently truncates it, raises a validation error mid-transaction, or accepts it and fails
downstream when it reaches a database or API layer — all three are harder to diagnose than a
`BusinessException` raised one step earlier with a clear message.

The pattern to apply before any `Type Into` that handles formatted data:

```vb
' Step 1: validate input before typing
Dim pattern As String = "^\d{1,3}(?:,\d{3})*(?:\.\d{2})$"   ' e.g. "1,234.56"
If Not Regex.IsMatch(strAmountToType, pattern) Then
    Throw New BusinessRuleException(
        $"Amount '{strAmountToType}' does not match expected format. " &
        "Expected: 1-7 digit integer or decimal with exactly 2 decimal places."
    )
End If

' Step 2: normalize before typing (some fields reject commas)
Dim strNormalized As String = Regex.Replace(strAmountToType, ",", "")
' → "1234.56"

' Step 3: type the normalized value
' [Type Into activity] → strNormalized
```

This applies to: date fields (validate ISO or locale format, then reformat if the target expects
a different separator), reference/ID fields (validate prefix and digit count), phone number
fields (strip non-numeric before typing), and any field where source data originates from a
scraped page, email body, or OCR output rather than a clean structured source.

**Normalize, then validate, then type** — in that order. Normalization removes characters the
field won't accept (thousands separators, currency symbols, whitespace); validation confirms the
normalized form is still structurally correct; `Type Into` sends the result. Doing validation
before normalization produces false negatives on valid data that just has extra formatting.

### After `Get Text` / UI Scraping — Output Extraction and Cleaning

`Get Text`, `Get Full Text`, Data Scraping, and OCR activities return raw strings. These strings
frequently contain:

- Leading/trailing whitespace and non-breaking spaces (`\u00A0`) that `.Trim()` alone doesn't
  remove
- Currency symbols, commas, and locale-specific formatting characters
- Newlines and extra spaces from HTML/table rendering artifacts
- OCR substitutions (the characters look right on screen but the underlying text isn't)

A standard cleaning sequence for a scraped numeric value in VB:

```vb
' Raw scraped text: "  $  1,234.56 \r\n"
Dim strRaw As String = strScrapedValue

' 1. Strip non-breaking spaces and control characters, normalize whitespace
strRaw = Regex.Replace(strRaw, "[\u00A0\u200B\uFEFF]", " ")   ' special whitespace to regular space
strRaw = Regex.Replace(strRaw, "\s+", " ").Trim()               ' collapse multiple spaces, trim ends

' 2. Extract the numeric portion
Dim m As Match = Regex.Match(strRaw, "-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?")
If Not m.Success Then
    Throw New BusinessRuleException($"Could not extract numeric value from: '{strScrapedValue}'")
End If

' 3. Remove thousands separator for downstream processing
Dim strClean As String = m.Value.Replace(",", "")   ' → "1234.56"
Dim dblAmount As Double = Double.Parse(strClean)
```

For multi-field scraping (a table row or a form summary), extract all fields in a single `Regex.
Match` with named groups rather than running a separate `Get Text` / extraction per field — one
pattern with named groups extracts five fields from one scraped string with one activity call,
which is faster and less fragile than five separate UI interactions:

```vb
Dim pattern As String =
    "Invoice:\s*(?<InvoiceNo>INV-\d{5,8})" &
    "[\s\S]*?" &
    "Date:\s*(?<Date>\d{2}/\d{2}/\d{4})" &
    "[\s\S]*?" &
    "Amount:\s*\$(?<Amount>[\d,]+\.\d{2})"

Dim m As Match = Regex.Match(strScrapedPage, pattern, RegexOptions.Singleline)
If m.Success Then
    strInvoiceNo = m.Groups("InvoiceNo").Value
    strDate      = m.Groups("Date").Value
    strAmount    = m.Groups("Amount").Value.Replace(",", "")
Else
    Throw New BusinessRuleException("Required fields not found in scraped output")
End If
```

### OCR-Specific Patterns

OCR output introduces character substitution errors that a pattern designed for clean text will
reject even though the underlying data is valid. Design OCR-targeting patterns defensively:

| Common OCR substitution  | Defensive pattern                                    |
| ------------------------ | ---------------------------------------------------- |
| `0` read as `O` or `D`   | `[0O]` for expected digit zero; `[0-9O]` if mixed    |
| `1` read as `l` or `I`   | `[1lI]` where a `1` is expected                      |
| `,` read as `.`          | `[\.,]` for decimal/thousands separator              |
| `5` read as `S`          | `[5S]` in numeric contexts                           |
| Spaces inserted mid-word | `\s*` between every character in short fixed strings |

For critical reference numbers read by OCR, consider a two-step approach: extract a candidate
with a permissive pattern, then validate it against an exact known list (Orchestrator Asset,
database lookup, or an in-memory list from a config) rather than relying on the pattern alone
to reject bad reads.

## Choosing the Right OCR Engine

OCR engine selection is a decision that belongs in the Solution Design Document — the wrong
engine for a context produces low-confidence output that defensive regex patterns can only
partially compensate for. A better engine that matches the content type eliminates the root
cause rather than patching around it.

### Engine Reference Table (Organization-Specific)

The following table reflects this team's internal documentation, with extended guidance added.

| OCR Engine                              | Cost                          | Primary use case                                                       | API key source                                   | Endpoint                                     |
| --------------------------------------- | ----------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------- |
| **Tesseract OCR**                       | Free                          | Practice and learning; offline baseline testing                        | N/A                                              | N/A                                          |
| **Microsoft OCR**                       | Free                          | Practice and learning; simple, clean screen text                       | N/A                                              | N/A                                          |
| **Microsoft Azure Computer Vision OCR** | Paid                          | Scraping full bodies of text from documents or images                  | Azure portal → Computer Vision resource          | Resource-specific endpoint from Azure portal |
| **Google Cloud Vision OCR**             | Paid                          | Scraping portions of text; handwriting; multi-language content         | Google Cloud Console → Cloud Vision API          | N/A (regional endpoint auto-selected)        |
| **UiPath Screen OCR**                   | Paid (Document Understanding) | Optimized for on-screen content (UI elements, web pages, desktop apps) | UiPath Automation Cloud — Document Understanding | `https://ocr.uipath.com/`                    |
| **UiPath Document OCR**                 | Paid (Document Understanding) | Optimized for scanned documents and PDFs                               | UiPath Automation Cloud — Document Understanding | See docs.uipath.com/document-understanding   |

### Decision Guide: Which Engine for Which Context

**Free engines (Tesseract, Microsoft OCR)** — acceptable for development, testing, and any
process where OCR is a secondary step on high-quality, clean, machine-rendered text (e.g.,
reading a well-formatted label on a modern web UI). Not appropriate as the sole engine for
production processes where OCR accuracy drives downstream financial, compliance, or
transactional decisions. Tesseract requires the image to be pre-processed (correctly scaled,
binarized, deskewed) to produce useful output — it is a tool for understanding the problem
space, not a default production choice.

**Azure Computer Vision OCR** — strong choice when the input is a full page or multi-paragraph
body of text (an invoice image, a scanned letter, a document photograph) where layout and
reading-order reconstruction matter in addition to raw character recognition. The `Read` API
(asynchronous, handles multi-page documents) vs. the `OCR` endpoint (synchronous, single image,
faster but layout-limited) is a real architectural choice: use `Read` for anything longer than
one page or where line/paragraph structure in the output is needed.

**Google Cloud Vision OCR** — competitive on partial text extraction from complex scenes
(photographs, mixed-content images, non-document screenshots), handwritten text, and multi-
language documents. Its label/logo/entity detection features are adjacent capabilities worth
noting for processes that need more than raw text. For pure document OCR in an Azure-standardized
environment, Azure Computer Vision is usually the more natural fit given existing Azure
infrastructure.

**UiPath Screen OCR** — the correct default for any UiPath automation that needs to read text
from the screen itself (a virtualized/Citrix app, a legacy thick-client application, a terminal
emulator) rather than from a document file. Its model is trained on screen-rendered fonts and
UI layouts, not on document page layouts — using a document OCR engine on screen content
(or vice versa) degrades accuracy materially. Requires a Document Understanding API key from
UiPath Automation Cloud.

**UiPath Document OCR** — the correct default for processing uploaded files, scanned PDFs, or
document images within a Document Understanding pipeline (alongside the Document Understanding
framework's ML extractor and classifier). Use this rather than Screen OCR when the input is a
file, not a live screen. The two UiPath engines are complementary, not interchangeable.

### Pre-processing: The Most Impactful Accuracy Lever

Regardless of engine, OCR accuracy is dominated by input image quality. A suboptimal engine on
a well-prepared image frequently outperforms a premium engine on a degraded one. Apply these
steps before invoking any OCR activity when the input is an image file (not live screen content):

- **Scale to at least 300 DPI** — the minimum recommended for most engines; 300 DPI on a
  standard A4/letter document renders text at roughly 35 pixels per character height, which is
  the threshold below which most engines begin to degrade significantly.
- **Binarize (convert to black-and-white)** using an adaptive threshold rather than a fixed one
  — adaptive thresholding handles uneven lighting and scanning artifacts that a fixed global
  threshold will either wash out or darken into blobs.
- **Deskew** — even a 1–2 degree tilt reduces character segmentation accuracy noticeably; most
  document imaging libraries (OpenCV in Python, `ImageMagick`) provide auto-deskew. UiPath's
  Document Understanding pipeline includes pre-processing steps for this.
- **Remove borders, stamps, and watermarks** where they overlap text — these are among the
  most common sources of character substitution errors, particularly for scanned forms.
- In Python: use `opencv-python` + `Pillow` for pre-processing before passing to a Cloud OCR
  API, or `pytesseract` for Tesseract with an explicit `--psm` (page segmentation mode) flag
  appropriate for the document type (`--psm 6` for a uniform block of text; `--psm 11` for
  sparse text with no particular layout order).

### Confidence Scores: When to Trust the Output

Every production-grade engine returns a confidence score per character, word, or line. Treat
this score as a first-class output, not an afterthought:

- Define a confidence threshold in `Config.xlsx` / Orchestrator Asset (not hardcoded) — values
  below the threshold route the item to a human-review queue rather than proceeding automatically.
  A typical starting threshold for financial document processing is 85–90%; the right value is
  process-specific and should be tuned against real samples during UAT.
- Log the minimum and average confidence per document at `Info` level — a sustained drop in
  average confidence across a batch of documents is a leading indicator of a source-quality
  problem (scanner degraded, document format changed) before individual failures start appearing.
- In UiPath Document Understanding, confidence scores are exposed per field by the ML extractor;
  in the `Read` API (Azure) and Cloud Vision, they are returned per word. Aggregate them to the
  field level before applying the threshold, not per character — a single low-confidence
  character in an otherwise well-read field may not warrant human review if the surrounding
  context makes the value unambiguous.

### Combining Engines (Voting / Ensemble)

For critical fields in high-accuracy requirements contexts (financial amounts, legal reference
numbers, compliance document IDs), run two engines independently and compare results:

- If both agree → high confidence, proceed.
- If they disagree → route to human review, log both candidates.

This is not a default recommendation for every OCR step — it doubles the API cost and latency.
It is appropriate when a single character misread has a material financial or compliance
consequence and the volume is manageable. In UiPath, implement as two separate OCR activities
on the same image region, two `Get Text` extractions, followed by an equality check that raises
a `BusinessException` (review queue) on mismatch.

### Databricks `ai_parse_document`: Beyond OCR

For document processing workloads at corpus scale — bulk ingestion of invoice archives,
processing thousands of scanned PDFs, or building a RAG knowledge base from document
repositories — the traditional OCR-engine selection decision (Tesseract, Azure CV, Google
Vision, UiPath Screen/Document OCR) is the wrong frame. At that scale, **Databricks
`ai_parse_document`** is the appropriate tool: a single SQL function that parses PDFs,
Word documents, PowerPoint files, and images into structured elements (text paragraphs,
tables in HTML, figures with AI-generated captions, bounding boxes, confidence scores)
and returns the result as a `VARIANT`-typed Delta table row.

The key distinction from traditional OCR:

- Traditional OCR engines extract a raw text string with layout information partially or
  entirely lost. Tables become flat text; figures are skipped or returned as pixels.
- `ai_parse_document` understands document structure. Every table is returned as HTML with
  merged cells preserved. Every figure gets an AI-generated natural-language description.
  Every element carries its type, bounding box, confidence score, and page reference —
  individually accessible in SQL without any regex post-processing.

This does not replace the OCR engine selection decision for bot-time, per-document
extraction within a UiPath workflow (where UiPath Document OCR or Screen OCR is still
the correct tool). It adds a complementary capability at the data-platform layer: the
same documents captured by a bot can be landed in a Unity Catalog Volume and processed
at scale by `ai_parse_document` for analytics, search, and AI agent consumption.

Full reference — syntax, arguments, output schema, element types, code examples
(SQL, PySpark, Lakeflow Pipeline pattern), integration with `ai_extract`/`ai_classify`/
AI Search, and the architecture pattern combining UiPath capture with Databricks corpus-
scale parsing — is in `references/uipath-databricks-integration.md`, Part 3.

### Invoke Code / Custom VB for Complex Regex Logic

When a regex operation requires logic beyond a single `Matches`/`IsMatch`/`Replace` activity
(iterating groups, conditional replacement based on match content, building a result dictionary
from named groups), place it in an `Invoke Code` activity or a custom C# activity rather than
chaining multiple regex activities. This is faster (one compiled regex pass vs. multiple
separate passes over the same string), more readable (the logic is in one place), and easier
to unit-test (a custom C# method can be tested outside UiPath entirely).

```vb
' Invoke Code example — extract all table rows matching a pattern into a DataTable
Dim dtResults As New DataTable
dtResults.Columns.Add("InvoiceNo")
dtResults.Columns.Add("Amount")

For Each m As Match In Regex.Matches(strScrapedTable,
    "INV-(?<InvoiceNo>\d{5,8})\s+\$(?<Amount>[\d,]+\.\d{2})",
    RegexOptions.Multiline)
    dtResults.Rows.Add(m.Groups("InvoiceNo").Value,
                       m.Groups("Amount").Value.Replace(",", ""))
Next
' Output argument: out_InvoiceTable = dtResults
```

## Power Automate Desktop: Native Regex Actions

PAD exposes regex as dedicated actions in the `Text` action group — a significant advantage over
Cloud flows for regex-heavy text processing:

| PAD Action                                              | Purpose                                                                  |
| ------------------------------------------------------- | ------------------------------------------------------------------------ |
| `Parse text with regular expression`                    | Extracts the first match (and all named/numbered groups) from input text |
| `Parse text with regular expression` (Find All Matches) | Returns a list of all matches                                            |

Both actions accept a pattern string and a `%TextToSearch%` variable. The match result is stored
in a variable; named groups are accessible via the Groups collection. The pattern syntax is .NET
(`System.Text.RegularExpressions`), consistent with UiPath's syntax.

Best practices specific to PAD:

- Store complex patterns in an **Orchestrator Asset** or a config file rather than directly in
  the action field — this makes a pattern change a config update, not a flow edit requiring
  redeploy.
- Test the pattern string against representative samples (including edge cases — empty field,
  extra whitespace, OCR-substituted characters) in a dedicated standalone test flow before
  embedding it in the production flow. PAD has no REPL; a test flow with a hardcoded sample
  input and a `Display message` showing the match result is the practical equivalent.
- Use PAD's regex actions when the text-processing leg is already in a Desktop flow — do not
  route a string out of a Desktop flow into a Cloud flow solely to process it with an expression
  function, then back. Keep the data in the layer where it was acquired.

## Debugging Regex in the RPA Context

Regex patterns fail in three distinct ways in practice:

1. **False negative** (pattern doesn't match input that should match) — almost always caused by
   an unexpected character in the input (a non-breaking space, a currency symbol, an OCR
   substitution, a locale-specific decimal separator) or an insufficiently general quantifier.
   Debug by logging the raw input string's character codes (`Asc(char)` per character in VB,
   `ord(c)` in Python) to find the unexpected character, then widen the pattern to accommodate
   it.
2. **False positive** (pattern matches input that shouldn't match) — almost always caused by an
   overly permissive pattern (`\d+` matching a single digit when you expected at least 5) or
   missing anchors. Debug by constructing adversarial inputs that should not match and running
   them through the same `IsMatch` call.
3. **Wrong extraction** (matches, but captures the wrong text) — almost always caused by greedy
   quantifiers consuming more than intended. Switch to lazy (`.*?`) and tighten the leading and
   trailing anchors.

**Recommended debugging workflow for any new RPA pattern:**

1. Write the pattern in a dedicated tool (regex101.com targets .NET or Python flavors and shows
   match logic step-by-step; or a Python `re` REPL for Python-targeted patterns) against at
   least five real samples from the target system, including one OCR/scraped sample with its
   actual character encoding rather than a manually typed clean version.
2. Add at least one adversarial input that is close to valid but should fail — confirm the
   pattern correctly rejects it.
3. Capture the character codes of any unexpected non-match before assuming the pattern is wrong —
   the input is the more common source of the problem than the pattern in OCR and scraping
   contexts.
4. Log the raw input at `Trace` level in production for the first several runs after deploying
   a new regex-dependent step, so any unexpected input variation is visible in the logs before
   it causes a production failure.

## Performance Considerations

- **Compile patterns used in loops** (UiPath: construct the `Regex` object once with
  `New Regex(pattern, RegexOptions.Compiled)` before the loop; Python: call `re.compile()`
  once and reuse the object). Compiling once and reusing is materially faster than passing a
  pattern string to `Regex.IsMatch`/`re.match` on every iteration.
- **Avoid catastrophic backtracking** (the most serious regex performance failure): patterns
  with nested quantifiers like `(.+)+` can enter exponential runtime on certain inputs —
  specifically on strings that _almost_ match but don't. For any pattern that runs against
  untrusted or variable-length input, review for nested quantifiers and prefer atomic groups or
  possessive quantifiers (available in the `regex` Python module but not in the standard `re`
  module) where backtracking performance is a concern.
- **Prefer specific character classes over `.`** when you know the shape of the data: `\d+`
  is faster and more precise than `.+` restricted to digits by context. Specificity reduces the
  search space the engine must explore.
- **Anchor patterns where the match position is known**: `^INV-\d+` with an anchor fails
  immediately on non-matching strings rather than scanning the whole string for a match starting
  anywhere.

## Sources Consulted

- This team's internal OCR engine selection table, provided directly by the user — the source
  for the "Engine Reference Table" above; the extended decision criteria, pre-processing
  guidance, confidence scoring, and ensemble pattern are general best-practice additions.
- Friedl, _Mastering Regular Expressions_ (3rd ed., O'Reilly) — the standard comprehensive
  reference for regex theory, NFA/DFA engine behavior, greedy/lazy quantifiers, backtracking.
- Python documentation: `re` module (docs.python.org/3/library/re.html).
- Microsoft documentation: `System.Text.RegularExpressions` namespace, `RegexOptions` enum
  (docs.microsoft.com); Azure Computer Vision `Read` API and `OCR` endpoint documentation.
- docs.uipath.com — Matches, IsMatch, Replace activities; selector wildcard vs. pattern syntax;
  Document Understanding framework, UiPath Screen OCR and Document OCR endpoint references.
- learn.microsoft.com/power-automate — expression functions reference (no native regex function
  confirmed as of July 2026).
- Google Cloud Vision API documentation (cloud.google.com/vision).
- Smith, R., "An Overview of the Tesseract OCR Engine" (ICDAR 2007) — Tesseract accuracy
  characteristics and DPI/pre-processing requirements.
- OpenCV documentation (opencv.org) — adaptive thresholding, deskew, image pre-processing.

Core regex behavior (pattern syntax, engine behavior, named groups, lazy quantifiers) and OCR
theory are stable. The specific UiPath Document Understanding endpoint URLs, Azure/Google API
key acquisition paths, and the Power Automate Cloud expression function list are the parts of
this file most likely to change — verify against vendor documentation for any new project.
