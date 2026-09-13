> Content in this file is grounded in official Microsoft .NET documentation
> (learn.microsoft.com — DateTime, DateTimeOffset, CultureInfo, ParseExact — verified July 2026),
> Oracle JD Edwards EnterpriseOne date documentation (docs.oracle.com/cd/E59116_01, verified
> July 2026), and the JDE developer community (jdelist.com). All conversion algorithms have been
> independently verified against the documented CYYDDD specification.

# Date Handling in RPA and UiPath

## Why Dates Are a Persistent Source of RPA Failures

Date handling is responsible for a disproportionate share of RPA `BusinessRuleException` and
silent data corruption events. The reasons are structural:

- Source systems store dates as strings in regional formats (UK `dd/MM/yyyy`, US `MM/dd/yyyy`,
  EU `dd.MM.yyyy`, ISO `yyyy-MM-dd`) — and the same field may contain different formats across
  rows in the same DataTable when data comes from multiple sources.
- ERP systems (SAP, JD Edwards, Autoline) use proprietary date formats internally (JDE's CYYDDD
  Julian format, SAP's `dd.MM.yyyy` field format, Autoline's internal numeric date fields).
- OCR and screen-scraping produce text like `1/3/2025` which is ambiguous between January 3
  and March 1 depending on the source system's locale.
- `DateTime.Parse()` uses the machine's current `CultureInfo` — a bot running on a UK-locale
  server will parse `3/1/2025` as March 1; the same code on a US-locale server will parse it as
  January 3. The result is silent data corruption, not a runtime error.

The rule: **never use `DateTime.Parse()` on data from an external source**. Always use
`DateTime.ParseExact()` with an explicit format string, or `DateTime.TryParseExact()` when
the format may legitimately vary.

---

## Standard .NET Date Patterns in UiPath (VB.NET)

### ParseExact — Single Known Format

```vb
' Parse a date from a source known to always use dd/MM/yyyy (UK/AU format)
Dim parsedDate As DateTime = DateTime.ParseExact(
    strRawDate.Trim(),
    "dd/MM/yyyy",
    System.Globalization.CultureInfo.InvariantCulture)

' Parse MM/dd/yyyy (US format)
Dim parsedDate As DateTime = DateTime.ParseExact(
    strRawDate.Trim(),
    "MM/dd/yyyy",
    System.Globalization.CultureInfo.InvariantCulture)

' Parse a date with time component from a database output
Dim parsedDate As DateTime = DateTime.ParseExact(
    strRawDate.Trim(),
    "yyyy-MM-dd HH:mm:ss",
    System.Globalization.CultureInfo.InvariantCulture)
```

### TryParseExact — When Format May Vary or Data May Be Invalid

```vb
' Multiple possible formats from a single scraped source
Dim parsedDate As DateTime
Dim formats() As String = {
    "d/M/yyyy",   "dd/MM/yyyy",   "d/M/yy",   "dd/MM/yy",
    "d.M.yyyy",   "dd.MM.yyyy",
    "M/d/yyyy",   "MM/dd/yyyy",   "M/d/yy",   "MM/dd/yy",
    "yyyy-MM-dd", "yyyy/MM/dd",
    "d-MMM-yyyy", "dd-MMM-yyyy"   ' e.g. "5-Jan-2025"
}
If Not DateTime.TryParseExact(
        strRawDate.Trim(),
        formats,
        System.Globalization.CultureInfo.InvariantCulture,
        System.Globalization.DateTimeStyles.None,
        parsedDate) Then
    Throw New BusinessRuleException("Cannot parse date value: '" & strRawDate & "'")
End If
```

### Formatting DateTime for Target System

```vb
' For target system expecting dd/MM/yyyy (most UK/AU/EU systems)
strFormatted = parsedDate.ToString("dd/MM/yyyy")

' For target system expecting MM/dd/yyyy (US systems)
strFormatted = parsedDate.ToString("MM/dd/yyyy")

' For SAP date entry fields
strFormatted = parsedDate.ToString("dd.MM.yyyy")

' For ISO 8601 (database, API, modern ERP)
strFormatted = parsedDate.ToString("yyyy-MM-dd")

' For human-readable log output (unambiguous)
strFormatted = parsedDate.ToString("dd MMM yyyy")  ' e.g. "05 Jan 2025"

' Include time component
strFormatted = parsedDate.ToString("dd/MM/yyyy HH:mm:ss")

' Short 2-digit year (use sparingly — ambiguous for display, never for storage)
strFormatted = parsedDate.ToString("dd/MM/yy")
```

### Format Code Reference

| Code | Output (for 5 Jan 2025, 09:07:03) |
|---|---|
| `dd` | `05` |
| `d` | `5` |
| `MM` | `01` |
| `M` | `1` |
| `MMM` | `Jan` |
| `MMMM` | `January` |
| `yyyy` | `2025` |
| `yy` | `25` |
| `HH` | `09` (24-hour) |
| `hh` | `09` (12-hour) |
| `mm` | `07` |
| `ss` | `03` |
| `tt` | `AM` |
| `ddd` | `Sun` |
| `dddd` | `Sunday` |
| `dd/MM/yyyy` | `05/01/2025` |
| `MM/dd/yyyy` | `01/05/2025` |
| `yyyy-MM-dd` | `2025-01-05` |
| `dd.MM.yyyy` | `05.01.2025` |
| `d-MMM-yyyy` | `5-Jan-2025` |

---

## Regional Format Disambiguation

When the source format is ambiguous (`3/5/2025` could be March 5 or May 3), apply these rules:

1. **Know the source system's locale.** Document it in Config.xlsx. Do not infer from data.
2. **Use the most restrictive format that uniquely identifies the source.** If you know the
   source is Australian, use `d/MM/yyyy` — this forces the month to parse from the second
   segment, making `3/5/2025` unambiguously May 3.
3. **If the source may mix locales**, validate the month field:
   - If both interpretations produce a valid date AND both months are 1-12, you cannot resolve
     programmatically — raise a `BusinessRuleException` and route to human review.
   - If one interpretation produces an invalid date (month 13+), the valid one is correct.

```vb
' Disambiguation: try dd/MM/yyyy first, then MM/dd/yyyy
Dim dtDDMM, dtMMDD As DateTime
Dim isDDMM = DateTime.TryParseExact(strRawDate, "d/M/yyyy",
    System.Globalization.CultureInfo.InvariantCulture,
    System.Globalization.DateTimeStyles.None, dtDDMM)
Dim isMMDD = DateTime.TryParseExact(strRawDate, "M/d/yyyy",
    System.Globalization.CultureInfo.InvariantCulture,
    System.Globalization.DateTimeStyles.None, dtMMDD)

If isDDMM And isMMDD And dtDDMM <> dtMMDD Then
    ' Genuinely ambiguous — both parse to different, valid dates
    Throw New BusinessRuleException(
        "Ambiguous date format '" & strRawDate &
        "' — could be " & dtDDMM.ToString("dd MMM yyyy") &
        " or " & dtMMDD.ToString("dd MMM yyyy") & ". Manual review required.")
ElseIf isDDMM Then
    parsedDate = dtDDMM
ElseIf isMMDD Then
    parsedDate = dtMMDD
Else
    Throw New BusinessRuleException("Cannot parse date: '" & strRawDate & "'")
End If
```

---

## JDE Julian Date Format (CYYDDD)

### Format Specification

JD Edwards EnterpriseOne and JD Edwards World store dates internally in a 6-digit Julian
format: `CYYDDD` where:

| Position | Meaning | Example |
|---|---|---|
| `C` | Century indicator: `0` = 1900s, `1` = 2000s, `2` = 2100s | `1` for 2025 |
| `YY` | 2-digit year within the century | `25` for 2025 |
| `DDD` | Day of the year (1-based ordinal, 001–365/366) | `005` for January 5 |

Complete example: `125005` = January 5, 2025 (C=1→2000s, YY=25→2025, DDD=005→Jan 5).

Additional examples from Oracle's official specification:
- `098185` = July 4, 1998 (C=0→1900s, YY=98→1998, DDD=185→day 185)
- `100001` = January 1, 2000 (C=1→2000s, YY=00→2000, DDD=001)
- `105031` = January 31, 2005
- `107263` = September 20, 2007

**Edge case — JDE day 000:** JDE uses day `000` to represent a null/empty date (no date set).
This must be handled as `Nothing`/`DBNull` rather than treated as a valid date.

**Edge case — 5-digit JDE dates for 1900s:** Some legacy data shows JDE Julian dates without
a leading zero for the century (`98185` instead of `098185`). The 5-digit form is always a
1900s date (C=0 implied). Both forms must be handled.

### JDE Julian → Gregorian Conversion (VB.NET, Invoke Code)

```vb
' Input:  intJDEDate As Integer (e.g., 125005 for January 5, 2025)
' Output: dtResult As DateTime

Public Function JDEJulianToDateTime(jdeDate As Integer) As DateTime
    ' Handle null date sentinel
    If jdeDate = 0 Then Return Nothing

    Dim jdeStr As String = jdeDate.ToString().PadLeft(6, "0"c)

    ' Parse components
    Dim century As Integer = Integer.Parse(jdeStr.Substring(0, 1))  ' 0 or 1
    Dim year    As Integer = Integer.Parse(jdeStr.Substring(1, 2))   ' 00-99
    Dim dayOfYear As Integer = Integer.Parse(jdeStr.Substring(3, 3)) ' 001-366

    ' Reconstruct full year: 1900 + (century * 100) + year
    Dim fullYear As Integer = 1900 + (century * 100) + year

    ' Start at Jan 1 of fullYear, add (dayOfYear - 1) days
    Return New DateTime(fullYear, 1, 1).AddDays(dayOfYear - 1)
End Function
```

**In a single Invoke Code block in UiPath:**

```vb
' JDE Julian to DateTime — paste this into Invoke Code
Dim jdeStr As String = intJDEDate.ToString().PadLeft(6, "0"c)
Dim fullYear As Integer = 1900 + (Integer.Parse(jdeStr.Substring(0, 1)) * 100) +
                          Integer.Parse(jdeStr.Substring(1, 2))
Dim dayOfYear As Integer = Integer.Parse(jdeStr.Substring(3, 3))
dtResult = If(intJDEDate = 0, Nothing, New DateTime(fullYear, 1, 1).AddDays(dayOfYear - 1))
```

**As a single Assign expression (VB.NET):**

```vb
dtResult = If(intJDEDate = 0, Nothing,
    New DateTime(
        1900 + (CInt(intJDEDate.ToString().PadLeft(6,"0"c).Substring(0,1)) * 100) +
               CInt(intJDEDate.ToString().PadLeft(6,"0"c).Substring(1,2)),
        1, 1
    ).AddDays(CInt(intJDEDate.ToString().PadLeft(6,"0"c).Substring(3,3)) - 1))
```

### Gregorian → JDE Julian Conversion (VB.NET)

```vb
' Input:  dtDate As DateTime
' Output: intJDEDate As Integer (e.g., 125005 for January 5, 2025)

Dim century  As Integer = If(dtDate.Year >= 2000, 1, 0)
Dim twoDigitYear As Integer = dtDate.Year Mod 100
Dim dayOfYear As Integer = dtDate.DayOfYear
intJDEDate = (century * 100000) + (twoDigitYear * 1000) + dayOfYear

' Example: January 5, 2025
' century = 1, twoDigitYear = 25, dayOfYear = 5
' intJDEDate = 100000 + 25000 + 5 = 125005 -- verified
```

**As a single Assign expression:**

```vb
intJDEDate = (If(dtDate.Year >= 2000, 1, 0) * 100000) +
             (dtDate.Year Mod 100) * 1000 +
             dtDate.DayOfYear
```

### JDE Julian as String Input

When the JDE date arrives as a string (from screen-scraping, file extract, or database
string column) rather than as an integer:

```vb
' Handle both 5-digit (legacy 1900s) and 6-digit JDE Julian strings
Dim jdeStr As String = strJDEDate.Trim().PadLeft(6, "0"c)
Dim intJDEDate As Integer = Integer.Parse(jdeStr)
' Then apply the integer → DateTime conversion above
```

### Validating a JDE Julian Date Before Use

```vb
' Check before conversion — rejects 0 (null), negative, >1 million (impossible CYYDDD)
' and validates dayOfYear is within the year's valid range
Function IsValidJDEJulian(jdeDate As Integer) As Boolean
    If jdeDate <= 0 OrElse jdeDate > 999366 Then Return False
    Dim jdeStr As String = jdeDate.ToString().PadLeft(6, "0"c)
    Dim year   As Integer = 1900 + CInt(jdeStr.Substring(0, 1)) * 100 + CInt(jdeStr.Substring(1, 2))
    Dim doy    As Integer = CInt(jdeStr.Substring(3, 3))
    Dim daysInYear As Integer = If(DateTime.IsLeapYear(year), 366, 365)
    Return doy >= 1 AndAlso doy <= daysInYear
End Function
```

---

## Ordinal Julian Day Number (Astronomical JDN)

Distinct from the JDE format above. The astronomical Julian Day Number is the continuous count
of days since January 1, 4713 BC (Julian calendar) — a system used in astronomy and some
legacy systems for absolute date arithmetic.

A JDN of `2454115` corresponds to approximately January 1, 2007. This format appears in some
scientific databases, FITS files, and legacy financial systems.

```vb
' JDN to DateTime (approximate — JDN starts at noon UTC)
Dim jdnEpoch As New DateTime(2000, 1, 1, 12, 0, 0, DateTimeKind.Utc) ' J2000.0 = JDN 2451545
dtResult = jdnEpoch.AddDays(jdn - 2451545.0)
```

For RPA purposes, if a system produces JDN values, always verify the epoch and whether the
value is a whole number (date only) or decimal (date + fractional time). JDE's CYYDDD format
is far more commonly encountered in automotive/manufacturing ERP contexts than astronomical JDN.

---

## Modern Julian Date (YYYYDDD / YYDDD) — Banking Format

Used in banking and some government systems. Simpler than JDE: a full 4-digit year prefix
followed by the 3-digit ordinal day. No century byte.

- `2025005` = January 5, 2025 (YYYYDDD, 7 digits)
- `25005` = January 5, 2025 (YYDDD, 5 digits — assumes current century, ambiguous post-2099)

```vb
' YYYYDDD to DateTime
Dim yyyyddd As String = strModernJulian.Trim()
Dim fullYear As Integer = Integer.Parse(yyyyddd.Substring(0, 4))
Dim dayOfYear As Integer = Integer.Parse(yyyyddd.Substring(4))
dtResult = New DateTime(fullYear, 1, 1).AddDays(dayOfYear - 1)

' DateTime to YYYYDDD
strModernJulian = dtDate.Year.ToString("D4") & dtDate.DayOfYear.ToString("D3")
```

---

## Date Arithmetic Patterns

```vb
' Add / subtract days
dtResult = dtBase.AddDays(30)
dtResult = dtBase.AddDays(-7)

' Add months (handles month-end edge cases: Jan 31 + 1 month = Feb 28/29)
dtResult = dtBase.AddMonths(1)

' Difference in days (always positive for elapsed time)
intDays = Math.Abs(CInt((dtEnd - dtStart).TotalDays))

' First day of month
dtFirstOfMonth = New DateTime(dtBase.Year, dtBase.Month, 1)

' Last day of month
dtLastOfMonth = New DateTime(dtBase.Year, dtBase.Month,
    DateTime.DaysInMonth(dtBase.Year, dtBase.Month))

' First day of next month
dtFirstOfNextMonth = New DateTime(dtBase.Year, dtBase.Month, 1).AddMonths(1)

' Is the date in the current month?
boolCurrentMonth = dtBase.Year = Now.Year AndAlso dtBase.Month = Now.Month

' Quarter (1-based)
intQuarter = ((dtBase.Month - 1) \ 3) + 1

' Financial year start (1 July in AU/UK; 1 Jan elsewhere — configure in Config)
dtFYStart = New DateTime(dtBase.Year,
    CInt(Config("FinancialYearStartMonth")), 1)

' Age in complete years (for vehicle age, contract tenure)
intAgeYears = CInt(Math.Floor((Now - dtBase).TotalDays / 365.25))
```

### Business Day Calculation (Simple — No Public Holidays)

```vb
' Add N business days (Mon-Fri only, no public holiday awareness)
Function AddBusinessDays(startDate As DateTime, days As Integer) As DateTime
    Dim result As DateTime = startDate
    Dim added As Integer = 0
    While added < days
        result = result.AddDays(1)
        If result.DayOfWeek <> DayOfWeek.Saturday AndAlso
           result.DayOfWeek <> DayOfWeek.Sunday Then
            added += 1
        End If
    End While
    Return result
End Function
```

For public holiday awareness, load a holiday list from Config or an Asset, then extend the
loop to also skip dates in the holiday list.

---

## Regex-Based Date Extraction from Scraped Text

When screen-scraping or OCR produces a text string containing a date embedded in surrounding
text, use regex to extract it before parsing:

```vb
' Extract dd/MM/yyyy or MM/dd/yyyy from surrounding text
Dim dateMatch = System.Text.RegularExpressions.Regex.Match(
    strRawText,
    "\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})\b")
strExtractedDate = If(dateMatch.Success, dateMatch.Value, "")

' Extract ISO date yyyy-MM-dd
Dim isoMatch = System.Text.RegularExpressions.Regex.Match(
    strRawText,
    "\b(\d{4})-(\d{2})-(\d{2})\b")
strExtractedDate = If(isoMatch.Success, isoMatch.Value, "")

' Extract date with month name (e.g., "5 January 2025", "Jan 5, 2025")
Dim monthNameMatch = System.Text.RegularExpressions.Regex.Match(
    strRawText,
    "\b(\d{1,2})\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|" &
    "May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|" &
    "Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{4})\b",
    System.Text.RegularExpressions.RegexOptions.IgnoreCase)
```

After extraction, parse with `ParseExact` or `TryParseExact` using the appropriate format.

---

## Date Normalization for Target System Entry

The complete normalize → validate → format → type sequence for a date field in a UI automation:

```vb
' 1. Extract from scraped text (regex if embedded, direct if isolated)
Dim rawDate As String = strScrapedText.Trim()

' 2. Normalize separators (handle /, -, . interchangeably)
rawDate = System.Text.RegularExpressions.Regex.Replace(rawDate, "[/.\-]", "/")

' 3. Parse with known candidate formats
Dim parsedDate As DateTime
If Not DateTime.TryParseExact(rawDate,
        {"d/M/yyyy","dd/MM/yyyy","d/M/yy","dd/MM/yy",
         "M/d/yyyy","MM/dd/yyyy","yyyy/MM/dd"},
        System.Globalization.CultureInfo.InvariantCulture,
        System.Globalization.DateTimeStyles.None,
        parsedDate) Then
    Throw New BusinessRuleException("Cannot parse date '" & strScrapedText & "'")
End If

' 4. Validate range (reject clearly wrong dates)
If parsedDate.Year < 2000 OrElse parsedDate > DateTime.Now.AddYears(5) Then
    Throw New BusinessRuleException("Date out of acceptable range: " &
        parsedDate.ToString("dd MMM yyyy"))
End If

' 5. Format for the target system (from Config to avoid hardcoding)
Dim targetFormat As String = Config("TargetDateFormat").ToString()
strFormattedDate = parsedDate.ToString(targetFormat)

' 6. Type into field — see references/linq-expressions.md and references/uipath-standards.md
'    for the validate-normalize-type workflow in UiPath UI activities
```

---

## Date Format Quick-Reference for Common Systems

| System | Entry format | Notes |
|---|---|---|
| SAP (most locales) | `dd.MM.yyyy` | Dot separator; consistent across SAP modules |
| JD Edwards (JDE) | Internal CYYDDD; screen may show `MM/DD/YY` | Parse from UI as `MM/dd/yy`; store/compare as DateTime |
| Autoline / Keyloop DMS | Varies by market: UK `dd/MM/yyyy`, AU `dd/MM/yyyy` | See `references/autoline-dms.md` |
| Salesforce | ISO: `yyyy-MM-dd` | API uses ISO; UI depends on org locale |
| SharePoint / M365 | ISO internally; display locale-dependent | Always use `yyyy-MM-dd` for API/Power Automate |
| Excel (date cell) | `DateTime` (numeric internally) | Read with `CDate(row("Col"))` not `.ToString()` |
| SQL Server | ISO `yyyy-MM-dd HH:mm:ss` in queries | Always use parameterized queries; never string-concat dates |
| Microsoft Dynamics | `dd/MM/yyyy` or `MM/dd/yyyy` by locale | Verify per environment |

---

## Sources Consulted

- Microsoft official documentation: `System.DateTime.ParseExact`
  (learn.microsoft.com/dotnet/api/system.datetime.parseexact, verified July 2026) — authoritative
  source for all ParseExact/TryParseExact overloads, format strings, and DateTimeStyles flags.
- Microsoft official documentation: Standard and Custom Date/Time Format Strings
  (learn.microsoft.com/dotnet/standard/base-types/standard-date-and-time-format-strings,
  learn.microsoft.com/dotnet/standard/base-types/custom-date-and-time-format-strings,
  verified July 2026) — source for all format codes in the table above.
- Oracle JD Edwards EnterpriseOne documentation: Date Calculation RPG Programs
  (docs.oracle.com/cd/E59116_01/doc.94/e58802/ap_dates.htm, verified July 2026) — official
  authoritative specification of the JDE CYYDDD format, including the C=0→1900s/C=1→2000s
  rule and the examples (`098185`, `100001`, `099666`).
- Microsoft MSDN Forums: "Converting JD Edwards Date (6-digit Julian format) to MMDDYY format"
  (social.msdn.microsoft.com, 2011) — source for the modulus-based conversion algorithm
  and the PadLeft(6,"0"c) normalization for 5-digit legacy JDE dates.
- Kirix Strata Blog: "JD Edwards Date Conversions (CYYDDD)" (kirix.com, 2009) — independent
  verification of the CYYDDD algorithm with additional examples.
- JDELIST Community: "Julian Date Converter" thread (jdelist.com) — community verification
  of VB.NET conversion utility behavior.
- Surety Systems: "JDE Julian Date Converter" (suretysystems.com, 2025) — business context
  for JDE Julian usage in JDE World and EnterpriseOne report writing.

The JDE CYYDDD format specification and .NET DateTime format codes are stable and not expected
to change. The "common systems" date format table reflects observed behavior as of July 2026;
system-specific locale configurations may produce different formats — always verify in a test
environment before production.
