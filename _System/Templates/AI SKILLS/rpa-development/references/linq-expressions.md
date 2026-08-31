> Content in this file is grounded in official Microsoft .NET/LINQ documentation
> (learn.microsoft.com, docs.microsoft.com — verified July 2026), the UiPath Community Forum
> LINQ tutorial series (forum.uipath.com, May–June 2021, verified July 2026), and UiPath Studio
> expression-language documentation. All code examples are in VB.NET unless a C# alternative
> is explicitly shown; VB.NET is the recommended expression language for UiPath Studio Desktop
> and the only option for Studio Web (see `references/uipath-standards.md`).

# LINQ in RPA and UiPath

## Why LINQ Matters in RPA

RPA workflows routinely process tabular data loaded from Excel, CSV, databases, APIs, or
web-scraped sources — most often as a `DataTable`. The naive approach to querying or
transforming that data is a `For Each Row` loop with nested `If` activities. LINQ (Language-
Integrated Query) replaces these loops with concise, type-safe, declarative expressions that
execute inside a single `Assign` activity.

The benefits are concrete, not aesthetic:

| Dimension        | Loop approach                                  | LINQ approach                                                   |
| ---------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| Code location    | Multiple activities (For Each + If + Assign)   | Single `Assign` expression                                      |
| Readability      | Intent spread across multiple activities       | Intent visible in one expression                                |
| Performance      | O(n) with overhead per activity invocation     | O(n) with no activity-invocation overhead; JIT-compiled on .NET |
| DataTable result | Requires manual row-by-row `Add Row`           | `CopyToDataTable()` reconstructs in one call                    |
| Error surface    | Logic errors silent across multiple activities | Type errors surface at compile/validate time                    |

LINQ is not always the right tool: for operations that involve UI interaction per row, that
need side effects (logging, queue enqueue) per item, or that exceed 3-4 chained operators in
complexity, a `For Each Row` loop is more readable and debuggable. Use LINQ for data
transformation; use loops for data-driven action.

## Required Namespaces

LINQ in UiPath requires the following namespaces imported at the project level
(Project > Settings > Imports in Studio):

| Namespace                    | Required for                                                       |
| ---------------------------- | ------------------------------------------------------------------ |
| `System.Linq`                | All LINQ operators (`Where`, `Select`, `GroupBy`, `OrderBy`, etc.) |
| `System.Data`                | `DataTable`, `DataRow`, `DataColumn`, `DBNull`                     |
| `System.Collections.Generic` | `List(Of T)`, `IEnumerable(Of T)`, `Dictionary(Of K, V)`           |

`System.Data.DataSetExtensions` (which provides `AsEnumerable()` and `Field(Of T)()` on
DataTable and DataRow) is included automatically via `System.Data` in UiPath's Windows
compatibility mode. If using Windows-Legacy compatibility and `AsEnumerable()` throws a
compile error, add `System.Data.DataSetExtensions` explicitly.

## Syntax Variants: Query vs. Method (Lambda)

LINQ has two syntactically distinct but semantically equivalent forms. UiPath expressions
support both; the VB.NET query syntax is generally more readable for filtering DataTable rows,
while method syntax is more compact for chained collection operations.

**Query syntax (VB.NET):**

```vb
' From [alias] In [source] Where [condition] Select [projection]
(From row In dt.AsEnumerable()
 Where row("Status").ToString() = "Approved"
 Select row).CopyToDataTable()
```

**Method syntax (VB.NET lambda / fluent):**

```vb
' [source].Operator(Function([alias]) [expression])
dt.AsEnumerable() _
  .Where(Function(row) row("Status").ToString() = "Approved") _
  .CopyToDataTable()
```

Both produce identical results. Prefer query syntax when the operation reads naturally as a
sentence ("give me rows where Status = Approved"). Prefer method syntax when chaining many
operators or when the expression must fit on one line inside an `Assign` activity field.

**C# equivalents** (for Windows-compatibility projects set to C#):

```csharp
// Method syntax — C# uses lambda => not Function()
dt.AsEnumerable()
  .Where(row => row.Field<string>("Status") == "Approved")
  .CopyToDataTable()
```

Note: UiPath recommends VB.NET over C# for Studio expressions; C# in the studio expression
language compiles against an older spec (C#5) that lacks string interpolation and null-
conditional operators. See `references/uipath-standards.md` — Expression Language section.

## Deferred vs. Immediate Execution

This is the most common source of subtle bugs in UiPath LINQ usage:

- **Deferred execution**: Most LINQ operators (`Where`, `Select`, `OrderBy`, `GroupBy`, `Take`,
  `Skip`) return an `IEnumerable` that has not yet executed. The query runs only when the
  result is enumerated — i.e., when you call `CopyToDataTable()`, `ToList()`, `ToArray()`,
  `Count()`, `First()`, or iterate in a `For Each`.
- **Immediate execution**: Operators that produce a scalar or concrete collection execute
  immediately: `Count()`, `Sum()`, `Any()`, `All()`, `First()`, `FirstOrDefault()`,
  `ToList()`, `ToArray()`, `CopyToDataTable()`.

**Why it matters in UiPath:** If you store a LINQ query result in a variable typed as
`IEnumerable(Of DataRow)` and then modify the source DataTable before enumerating the result,
the query will execute against the modified table. Always materialize to a `DataTable`,
`List(Of T)`, or `Array` immediately if the source may change.

```vb
' RISK: deferred — query hasn't run yet, result reflects source at iteration time
Dim filteredRows As IEnumerable(Of DataRow) = dt.AsEnumerable().Where(...)

' SAFE: materialized immediately — result is a snapshot of the current source state
Dim filteredTable As DataTable = dt.AsEnumerable().Where(...).CopyToDataTable()
Dim filteredList  As List(Of DataRow) = dt.AsEnumerable().Where(...).ToList()
```

---

## LINQ to DataTable: Core Patterns

These are the patterns used in the large majority of RPA data transformation workflows.
All examples assume `dt` is a `DataTable` variable with data loaded and `System.Linq`/
`System.Data` imported.

### DataTable Entry Point: `AsEnumerable()` and `Field(Of T)()`

`dt.AsEnumerable()` converts the DataTable's `Rows` collection to an `IEnumerable(Of DataRow)`,
enabling LINQ operators. It is the required entry point for all DataTable LINQ queries.

`row.Field(Of T)("ColumnName")` is the type-safe accessor for a DataRow field. It handles
`DBNull` correctly (returns `Nothing` for nullable reference types rather than throwing):

```vb
' Untyped access — returns Object, requires .ToString() for string operations
row("ColumnName").ToString()

' Typed access — returns the declared type; DBNull becomes Nothing (nullable types)
row.Field(Of String)("ColumnName")          ' returns Nothing if DBNull
row.Field(Of Integer)("Amount")             ' returns Integer
row.Field(Of Date)("InvoiceDate")           ' returns Date
row.Field(Of Nullable(Of Double))("Price")  ' returns Nothing if DBNull
```

In UiPath expressions within the `Assign` field, both forms work. The untyped `row("Col").ToString()`
is the most common in practice and safe when the column is known to contain strings. Use
`Field(Of T)` when type precision matters (numeric comparisons, date comparisons, null
detection).

### Pattern 1: Filter Rows by Column Value

```vb
' Query syntax
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Status").ToString().Trim() = "Approved"
              Select row).CopyToDataTable()

' Method syntax
dtFiltered = dt.AsEnumerable() _
               .Where(Function(row) row("Status").ToString().Trim() = "Approved") _
               .CopyToDataTable()
```

### Pattern 2: Multiple Conditions (AND / OR)

```vb
' AND condition
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Status").ToString() = "Approved"
                And row("Region").ToString() = "APAC"
              Select row).CopyToDataTable()

' OR condition
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Status").ToString() = "Approved"
                 Or row("Status").ToString() = "Pending"
              Select row).CopyToDataTable()

' NOT condition — negate the whole predicate
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Status").ToString() <> "Cancelled"
              Select row).CopyToDataTable()
```

### Pattern 3: Case-Insensitive String Comparison

```vb
dtFiltered = (From row In dt.AsEnumerable()
              Where String.Equals(
                  row("Status").ToString(),
                  "approved",
                  StringComparison.OrdinalIgnoreCase)
              Select row).CopyToDataTable()
```

### Pattern 4: Null and DBNull Handling

```vb
' Check for DBNull explicitly
dtFiltered = (From row In dt.AsEnumerable()
              Where Not IsDBNull(row("InvoiceDate"))
              Select row).CopyToDataTable()

' Using Field(Of T) — DBNull returns Nothing; compare with Is Nothing
dtFiltered = (From row In dt.AsEnumerable()
              Where row.Field(Of String)("VendorName") IsNot Nothing
                And row.Field(Of String)("VendorName").Trim() <> ""
              Select row).CopyToDataTable()

' Remove rows where any field is DBNull or empty string
dtFiltered = dt.Rows.Cast(Of DataRow)() _
               .Where(Function(row)
                   Not row.ItemArray.All(Function(f)
                       f Is DBNull.Value OrElse f.Equals(""))) _
               .CopyToDataTable()
```

### Pattern 5: Numeric and Date Comparisons

```vb
' Numeric comparison (parse string column to numeric)
dtFiltered = (From row In dt.AsEnumerable()
              Where Double.Parse(row("Amount").ToString()) > 1000
              Select row).CopyToDataTable()

' Safer numeric comparison with TryParse to avoid exceptions on bad data
dtFiltered = (From row In dt.AsEnumerable()
              Let amount = 0.0
              Where Double.TryParse(row("Amount").ToString(), amount) AndAlso amount > 1000
              Select row).CopyToDataTable()

' Date range filter
dtFiltered = (From row In dt.AsEnumerable()
              Where DateTime.Parse(row("InvoiceDate").ToString()) >= New DateTime(2025, 1, 1)
                And DateTime.Parse(row("InvoiceDate").ToString()) < New DateTime(2026, 1, 1)
              Select row).CopyToDataTable()

' Using Field(Of Date) for typed date access
dtFiltered = (From row In dt.AsEnumerable()
              Where Not IsDBNull(row("InvoiceDate"))
                And row.Field(Of Date)("InvoiceDate") >= #1/1/2025#
              Select row).CopyToDataTable()
```

### Pattern 6: Substring / Contains / StartsWith / EndsWith

```vb
' Contains (case-sensitive by default in String methods)
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Description").ToString().Contains("invoice")
              Select row).CopyToDataTable()

' Case-insensitive Contains
dtFiltered = (From row In dt.AsEnumerable()
              Where row("Description").ToString().IndexOf(
                  "invoice", StringComparison.OrdinalIgnoreCase) >= 0
              Select row).CopyToDataTable()

' StartsWith
dtFiltered = (From row In dt.AsEnumerable()
              Where row("OrderID").ToString().StartsWith("AU-")
              Select row).CopyToDataTable()
```

### Pattern 7: Sort / Order

```vb
' Sort ascending by a string column
dtSorted = (From row In dt.AsEnumerable()
            Order By row("Surname").ToString() Ascending
            Select row).CopyToDataTable()

' Sort descending by a numeric column
dtSorted = (From row In dt.AsEnumerable()
            Order By Convert.ToDouble(row("Amount").ToString()) Descending
            Select row).CopyToDataTable()

' Multi-key sort — primary descending, secondary ascending
dtSorted = (From row In dt.AsEnumerable()
            Order By row("Region").ToString() Ascending,
                     Convert.ToDouble(row("Amount").ToString()) Descending
            Select row).CopyToDataTable()
```

### Pattern 8: Select (Projection) — Extract a Subset of Columns

The `Select` clause in query syntax projects each row into a new form. Combined with
anonymous types or explicit column selection, it is useful for extracting one or more
columns as a typed collection.

```vb
' Extract a single column as List(Of String)
listVendors = (From row In dt.AsEnumerable()
               Select row("VendorName").ToString()).ToList()

' Extract a single column, trim and deduplicate, sorted
listRegions = (From row In dt.AsEnumerable()
               Select row("Region").ToString().Trim()
               Distinct
               Order By It Ascending).ToList()

' Extract two columns as a list of tuples (anonymous type — Invoke Code only, not Assign)
' For Assign activity, extract to two separate lists instead:
listIDs    = (From row In dt.AsEnumerable() Select row("ID").ToString()).ToList()
listAmounts = (From row In dt.AsEnumerable() Select CDbl(row("Amount").ToString())).ToList()
```

Note: Anonymous types (VB.NET `New With { .ID = ..., .Name = ... }`) in query `Select`
clauses work in `Invoke Code` activities but cannot be used as a typed variable in the
`Assign` activity because Studio requires an explicit declared type for every variable.
For multi-column extraction in an `Assign`, build a new DataTable or extract to parallel lists.

### Pattern 9: Distinct / Deduplicate

```vb
' Distinct values from one column as a list
listDistinct = (From row In dt.AsEnumerable()
                Select row("Category").ToString()
                Distinct).ToList()

' Distinct rows across all columns (DataRowComparer.Default is required for DataRow equality)
dtDistinct = dt.AsEnumerable() _
               .Distinct(DataRowComparer.Default) _
               .CopyToDataTable()
```

`DataRowComparer.Default` compares all field values in the row. Without it, `.Distinct()`
compares object references (all DataRow references are unique), so duplicates would not be
removed.

### Pattern 10: Count, Any, All

```vb
' Count rows matching a condition (returns Integer)
intCount = (From row In dt.AsEnumerable()
            Where row("Status").ToString() = "Approved").Count()

' Method syntax equivalent
intCount = dt.AsEnumerable().Count(Function(row) row("Status").ToString() = "Approved")

' Does any row match? (returns Boolean)
boolExists = dt.AsEnumerable().Any(Function(row) row("Status").ToString() = "Error")

' Do all rows match? (returns Boolean)
boolAllApproved = dt.AsEnumerable().All(Function(row) row("Status").ToString() = "Approved")
```

### Pattern 11: First, FirstOrDefault, Single

```vb
' First matching row — throws InvalidOperationException if no match
rowFirst = (From row In dt.AsEnumerable()
            Where row("OrderID").ToString() = strTargetID
            Select row).First()

' FirstOrDefault — returns Nothing if no match (check before accessing fields)
rowFirst = dt.AsEnumerable() _
             .FirstOrDefault(Function(row) row("OrderID").ToString() = strTargetID)
If rowFirst IsNot Nothing Then
    strValue = rowFirst("Amount").ToString()
End If

' Single — throws if zero or more than one row matches (use when exactly one is expected)
rowUnique = dt.AsEnumerable() _
              .Single(Function(row) row("InvoiceID").ToString() = strInvoiceID)
```

In UiPath `Assign` activities, the entire block is one expression — the `If rowFirst IsNot
Nothing` guard must go into a subsequent `If` activity after the `Assign`. For
`FirstOrDefault`, always store the result first, then check for `Nothing` in a separate `If`.

### Pattern 12: Aggregate — Sum, Average, Max, Min

```vb
' Sum a numeric column
dblTotal = dt.AsEnumerable() _
             .Sum(Function(row) Convert.ToDouble(row("Amount").ToString()))

' Average — wrapped in CDbl for explicit conversion
dblAvg = dt.AsEnumerable() _
           .Average(Function(row) CDbl(row("Amount").ToString()))

' Max and Min
dblMax = dt.AsEnumerable().Max(Function(row) CDbl(row("Amount").ToString()))
dblMin = dt.AsEnumerable().Min(Function(row) CDbl(row("Amount").ToString()))

' Conditional aggregate — sum only Approved rows
dblApprovedTotal = dt.AsEnumerable() _
                     .Where(Function(row) row("Status").ToString() = "Approved") _
                     .Sum(Function(row) CDbl(row("Amount").ToString()))
```

### Pattern 13: Group By and Aggregate per Group

Group By is one of the most powerful DataTable LINQ patterns — it replaces a loop that
maintains a running dictionary, which is a common source of subtle off-by-one errors.

```vb
' Group rows by Region, count per group — result as List(Of String) summary lines
listSummary = (From row In dt.AsEnumerable()
               Group row By Key = row("Region").ToString() Into grp = Group
               Select Key & ": " & grp.Count().ToString()).ToList()

' Group by Region, sum Amount per group — build a new summary DataTable in Invoke Code
' (multi-step construction requires Invoke Code rather than a single Assign expression)

' Equivalent in Invoke Code (C# project or VB Invoke Code):
' var summary = dt.AsEnumerable()
'     .GroupBy(row => row["Region"].ToString())
'     .Select(g => new { Region = g.Key, Total = g.Sum(r => (double)r["Amount"]) });
```

For multi-step GroupBy that produces a new DataTable, use an `Invoke Code` activity:

```vb
' Invoke Code VB — builds a summary DataTable from grouping
Dim dtSummary As New DataTable()
dtSummary.Columns.Add("Region", GetType(String))
dtSummary.Columns.Add("TotalAmount", GetType(Double))
dtSummary.Columns.Add("Count", GetType(Integer))

Dim groups = From row In dt.AsEnumerable()
             Group row By Key = row("Region").ToString() Into grp = Group
             Select New With {
                 .Region = Key,
                 .Total  = grp.Sum(Function(r) CDbl(r("Amount").ToString())),
                 .Count  = grp.Count()
             }

For Each g In groups
    dtSummary.Rows.Add(g.Region, g.Total, g.Count)
Next
```

### Pattern 14: Join Two DataTables

LINQ joins are the declarative replacement for the manual nested-loop join, which is
extremely slow for large tables (O(n\*m)) because UiPath activity invocation per row
adds overhead that compounds with table size.

```vb
' LINQ join — method syntax in Invoke Code (cleaner for multi-line joins)
' Inner join: dt1 LEFT.OrderID = dt2 RIGHT.OrderID, select matching rows from dt1
Dim dtJoined As DataTable = dt1.Clone() ' preserve dt1 schema

Dim joined = dt1.AsEnumerable() _
               .Join(
                   dt2.AsEnumerable(),
                   Function(left)  left("OrderID").ToString(),
                   Function(right) right("OrderID").ToString(),
                   Function(left, right)
                       Dim row As DataRow = dtJoined.NewRow()
                       row.ItemArray = left.ItemArray.Clone()
                       Return row
                   End Function)

For Each r In joined
    dtJoined.Rows.Add(r)
Next

' Query syntax inner join
Dim dtMatched As DataTable = dt1.Clone()
Dim matchedRows =
    From left  In dt1.AsEnumerable()
    Join right In dt2.AsEnumerable()
      On left("OrderID").ToString() Equals right("OrderID").ToString()
    Select left

For Each r In matchedRows
    dtMatched.Rows.Add(r.ItemArray)
Next
```

For a **left outer join** (keep all left rows, match where available):

```vb
Dim dtLeft As DataTable = dt1.Clone()

Dim leftJoin =
    From left In dt1.AsEnumerable()
    Group Join right In dt2.AsEnumerable()
      On left("OrderID").ToString() Equals right("OrderID").ToString()
    Into matches = Group
    From match In matches.DefaultIfEmpty()
    Select New With {
        .LeftRow  = left,
        .RightRow = match  ' Nothing if no match
    }

For Each item In leftJoin
    Dim row As DataRow = dtLeft.NewRow()
    row.ItemArray = item.LeftRow.ItemArray.Clone()
    ' item.RightRow Is Nothing for unmatched left rows
    dtLeft.Rows.Add(row)
Next
```

### Pattern 15: Set Operations — Intersect, Except, Union

```vb
' Rows in dt1 that also appear in dt2 (DataRowComparer.Default compares all field values)
dtIntersect = dt1.AsEnumerable() _
                 .Intersect(dt2.AsEnumerable(), DataRowComparer.Default) _
                 .CopyToDataTable()

' Rows in dt1 that are NOT in dt2 (difference / anti-join)
dtExcept = dt1.AsEnumerable() _
              .Except(dt2.AsEnumerable(), DataRowComparer.Default) _
              .CopyToDataTable()

' All rows from both tables combined (with deduplication)
dtUnion = dt1.AsEnumerable() _
             .Union(dt2.AsEnumerable(), DataRowComparer.Default) _
             .CopyToDataTable()

' All rows from both tables (with duplicates preserved)
dtConcat = dt1.AsEnumerable() _
              .Concat(dt2.AsEnumerable()) _
              .CopyToDataTable()
```

`Intersect`/`Except`/`Union` with `DataRowComparer.Default` compare ALL fields in the row.
For key-based set operations (rows whose primary key appears in both tables, regardless of
other field values), use a `Join` or `Where ... Any(...)` pattern instead.

### Pattern 16: Get Column Names by Type

```vb
' Get names of all DateTime columns as a String array
arrDateColumns = (From dc In dt.Columns.Cast(Of DataColumn)()
                  Where dc.DataType = GetType(DateTime)
                  Select dc.ColumnName).ToArray()

' Get names of all columns whose DataType is a numeric type
arrNumericColumns = (From dc In dt.Columns.Cast(Of DataColumn)()
                     Where dc.DataType = GetType(Integer) _
                        Or dc.DataType = GetType(Double) _
                        Or dc.DataType = GetType(Decimal)
                     Select dc.ColumnName).ToArray()
```

### Pattern 17: Pagination — Take and Skip

```vb
' Get the first 100 rows (e.g., for testing or batching)
dtPage = dt.AsEnumerable().Take(100).CopyToDataTable()

' Skip the first 100 rows and take the next 100 (page 2)
dtPage2 = dt.AsEnumerable().Skip(100).Take(100).CopyToDataTable()

' Combined filter + skip + take (common for batch processing)
dtBatch = dt.AsEnumerable() _
            .Where(Function(row) row("Processed").ToString() = "N") _
            .Skip(intOffset) _
            .Take(intBatchSize) _
            .CopyToDataTable()
```

---

## LINQ to Collections: Lists, Arrays, Dictionaries

These patterns operate on non-DataTable collections — common when working with queue item
payloads, API response objects, file path lists, or configuration arrays.

```vb
' Filter a List(Of String)
listFiltered = listItems.Where(Function(s) s.StartsWith("AU-")).ToList()

' Filter and transform
listUpper = listItems.Where(Function(s) s.Length > 5) _
                     .Select(Function(s) s.ToUpper().Trim()) _
                     .Distinct() _
                     .OrderBy(Function(s) s) _
                     .ToList()

' Check if any item in a list matches
boolFound = listItems.Any(Function(s) s.Contains("ERROR"))

' Find first matching item (or Nothing if not found)
strFound = listItems.FirstOrDefault(Function(s) s.StartsWith("INV-"))

' Count items matching a condition
intErrors = listItems.Count(Function(s) s.StartsWith("ERROR"))

' Get distinct values
listUnique = listItems.Distinct().ToList()

' Sort a list (does not modify original)
listSorted = listItems.OrderBy(Function(s) s).ToList()

' Convert List(Of String) to array
arrItems = listItems.ToArray()

' Flatten a nested list (List(Of List(Of String)) to List(Of String))
listFlat = listNested.SelectMany(Function(inner) inner).ToList()

' Get keys from Dictionary where value meets condition
listKeys = dictData.Where(Function(kv) kv.Value > 100) _
                   .Select(Function(kv) kv.Key) _
                   .ToList()
```

---

## LINQ in UiPath Activities

### Assign Activity (Single Expression)

The Assign activity accepts a single VB.NET or C# expression. All single-statement LINQ
patterns above work directly. Wrap multi-line query syntax in parentheses when the result
needs `.CopyToDataTable()` or `.ToList()` chained at the end.

```
Variable: dtFiltered
Value:    (From row In dt.AsEnumerable()
           Where row("Status").ToString() = "Approved"
           Order By row("Date").ToString() Descending
           Select row).CopyToDataTable()
```

**Important:** The `Assign` activity field does not support multi-statement code — only a
single expression. For patterns that require variable declarations (let, intermediate results,
for-each over groups), use `Invoke Code`.

### Invoke Code Activity (Multi-Statement, Complex Logic)

Use `Invoke Code` when:

- The LINQ result requires further manipulation before the final assignment
- You need intermediate variables (e.g., building a summary DataTable from GroupBy results)
- You are constructing anonymous types (`New With { ... }`) that cannot be declared as
  typed Studio variables
- The expression is long enough that debugging inside the Assign field is impractical

Example arguments: `In` parameter `dtInput As DataTable`, `Out/In-Out` parameter
`dtResult As DataTable`.

```vb
' Invoke Code body — VB.NET
Dim groups = From row In dtInput.AsEnumerable()
             Group row By Region = row("Region").ToString() Into grp = Group

dtResult = New DataTable()
dtResult.Columns.Add("Region", GetType(String))
dtResult.Columns.Add("Total",  GetType(Double))
dtResult.Columns.Add("Count",  GetType(Integer))

For Each g In groups
    dtResult.Rows.Add(
        g.Region,
        g.grp.Sum(Function(r) CDbl(r("Amount").ToString())),
        g.grp.Count())
Next
```

---

## Operator Quick-Reference Table

| Operator                          | Category    | Returns                     | UiPath Assign? | Notes                                               |
| --------------------------------- | ----------- | --------------------------- | -------------- | --------------------------------------------------- |
| `Where`                           | Filtering   | `IEnumerable`               | Yes (deferred) | Most common filter                                  |
| `Select`                          | Projection  | `IEnumerable`               | Yes (deferred) | Column extraction, transformation                   |
| `OrderBy` / `ThenBy`              | Sorting     | `IEnumerable`               | Yes (deferred) | Always chain with `CopyToDataTable()` or `ToList()` |
| `GroupBy`                         | Grouping    | `IEnumerable(Of IGrouping)` | Invoke Code    | Use in Assign only for simple string projections    |
| `Join`                            | Joining     | `IEnumerable`               | Invoke Code    | Multi-line; use Invoke Code                         |
| `Distinct`                        | Set         | `IEnumerable`               | Yes            | Requires `DataRowComparer.Default` for DataRows     |
| `Union` / `Intersect` / `Except`  | Set         | `IEnumerable`               | Yes            | Require `DataRowComparer.Default` for DataRows      |
| `Concat`                          | Combining   | `IEnumerable`               | Yes            | No deduplication                                    |
| `Take` / `Skip`                   | Pagination  | `IEnumerable`               | Yes            | Always chain with terminal operator                 |
| `First`                           | Element     | Single item                 | Yes            | Throws if empty                                     |
| `FirstOrDefault`                  | Element     | Single item or Nothing      | Yes            | Returns Nothing if empty                            |
| `Single`                          | Element     | Single item                 | Yes            | Throws if zero or >1 match                          |
| `Any`                             | Quantifier  | Boolean                     | Yes            | Immediate                                           |
| `All`                             | Quantifier  | Boolean                     | Yes            | Immediate                                           |
| `Count`                           | Aggregation | Integer                     | Yes            | Immediate                                           |
| `Sum` / `Average` / `Max` / `Min` | Aggregation | Numeric                     | Yes            | Immediate                                           |
| `ToList`                          | Terminal    | `List(Of T)`                | Yes            | Materializes                                        |
| `ToArray`                         | Terminal    | `T()`                       | Yes            | Materializes                                        |
| `CopyToDataTable`                 | Terminal    | `DataTable`                 | Yes            | DataRow sequences only                              |
| `AsEnumerable`                    | Entry point | `IEnumerable(Of DataRow)`   | Yes            | Required for DataTable                              |
| `Cast(Of T)`                      | Conversion  | `IEnumerable(Of T)`         | Yes            | For non-generic collections                         |
| `SelectMany`                      | Flattening  | `IEnumerable`               | Yes            | Flatten nested collections                          |

---

## Debugging LINQ in UiPath

### Common Errors and Fixes

**`CopyToDataTable()` throws `InvalidOperationException: The source contains no DataRows`**

Cause: The LINQ query returned zero rows; `CopyToDataTable()` requires at least one row.

Fix: Check row count first, or use a null-guard:

```vb
' Check before calling CopyToDataTable
Dim rows = dt.AsEnumerable().Where(Function(row) row("Status").ToString() = "Approved")
If rows.Any() Then
    dtFiltered = rows.CopyToDataTable()
Else
    dtFiltered = dt.Clone() ' empty table with same schema
End If
```

**`Value of type 'IEnumerable(Of DataRow)' cannot be converted to 'DataTable'`**

Cause: Missing `.CopyToDataTable()` at the end of the expression.

Fix: Chain `.CopyToDataTable()` as the terminal operator.

**`'row' is not declared` in the Assign activity field**

Cause: The query is written across multiple lines in the Assign field, but the VB.NET parser
cannot see the continuation. The line-continuation character `_` is required for multi-line
expressions in Assign, OR the whole expression must be wrapped in parentheses.

Fix:

```vb
' Wrap in parentheses — the parser treats the content as one expression
(From row In dt.AsEnumerable()
 Where row("Status").ToString() = "Approved"
 Select row).CopyToDataTable()
```

**`System.Data.DataSetExtensions` namespace not found / `AsEnumerable()` not available**

Cause: Missing namespace import. In Windows-Legacy projects, `DataSetExtensions` is not
auto-imported.

Fix: Add `System.Data.DataSetExtensions` to Project > Settings > Imports.

**`Object reference not set to an instance of an object` inside a LINQ predicate**

Cause: A row field contains `DBNull` and `.ToString()` is called on `DBNull.Value` after
another operation strips the safety net. This often happens with intermediate `.Select()`
projections that call `.ToString()` before filtering for nulls.

Fix: Filter out nulls/DBNulls before transforming:

```vb
' Filter nulls first, then transform
(From row In dt.AsEnumerable()
 Where Not IsDBNull(row("VendorName")) AndAlso row("VendorName").ToString().Trim() <> ""
 Select row).CopyToDataTable()
```

**Expression runs but produces wrong results — silent mismatch**

Cause: String comparison with leading/trailing spaces, mixed casing, or the wrong column name
(UiPath DataRow column access by name is case-sensitive by default).

Fix:

- Always `.Trim()` scraped or user-input strings before comparison.
- Use `StringComparison.OrdinalIgnoreCase` for case-insensitive matching.
- Verify column names exactly as they appear in the DataTable (check with `dt.Columns(0).ColumnName` in a Log Message during development).

---

## Performance Notes

- LINQ is generally faster than a `For Each Row` + `If` + `Add Row` sequence for DataTable
  filtering because it eliminates per-activity invocation overhead and the JIT-compiled lambda
  executes natively. For tables with more than a few thousand rows, the difference is
  measurable.
- For very large tables (>100,000 rows), consider switching to Polars or pandas in a Python
  `Invoke Python` script. See `data-engineering-transition.md` — the >1M-row threshold for
  Polars applies to data engineering pipelines; for in-bot processing, the practical threshold
  for switching to Python is typically 50,000-100,000 rows depending on the complexity of the
  transformation.
- Avoid chaining deferred operators over a source DataTable that is being modified concurrently
  by another branch of the workflow (rare but possible in parallel activities). Always
  materialize first.
- For repeated queries against the same DataTable with different parameters, prefer
  `.AsEnumerable()` once and store the `IEnumerable(Of DataRow)` — re-calling `AsEnumerable()`
  on every query is fine (it is O(1) and doesn't re-read the table), but it is cleaner to
  assign to an `IEnumerable` variable when the same source is queried many times.

---

## Sources Consulted

- Microsoft official documentation: LINQ (Language-Integrated Query) overview
  (learn.microsoft.com/dotnet/csharp/linq, verified July 2026) — LINQ architecture, deferred
  vs. immediate execution, standard query operators.
- Microsoft official documentation: LINQ to DataSet / ADO.NET
  (learn.microsoft.com/dotnet/framework/data/adonet/linq-to-dataset, verified July 2026) —
  `AsEnumerable()`, `CopyToDataTable()`, `Field(Of T)()`, set operations, `DataRowComparer`.
- Microsoft official documentation: `System.Linq` namespace, `Enumerable` class
  (learn.microsoft.com/dotnet/api/system.linq.enumerable, verified July 2026) — authoritative
  source for all operator signatures, behavior, and exception conditions.
- UiPath Community Forum: "[HowTo] — First Start with LINQ (VB.Net)"
  (forum.uipath.com/t/howto-first-start-with-linq-vb-net/318964, May 2021) and
  "[HowTo] — Exploring the LINQ Universe (VB.Net)"
  (forum.uipath.com/t/howto-exploring-the-linq-universe-vb-net/325667, June 2021) — UiPath
  Community tutorial series covering LINQ in the Studio expression context.
- UiPath Community Forum: Multiple DataTable filtering and CopyToDataTable threads (2021–2025)
  — source for common error patterns, namespace requirements, and the empty-result
  `CopyToDataTable` gotcha.
- Eric Alvarado, "RPA/UiPath — LINQ/Lambda Expressions and Shortcuts" (Medium, October 2024)
  — source for the column-type enumeration pattern and the uncommon-rows-between-two-tables
  pattern using `Except`.

LINQ operators and VB.NET lambda syntax are part of the stable .NET standard; they do not
change across UiPath Studio versions. The `System.Data.DataSetExtensions` namespace
requirement in Windows-Legacy projects is the one version-sensitive detail — verify if
moving a project between compatibility modes.
