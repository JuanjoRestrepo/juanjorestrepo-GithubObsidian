> Content grounded in official Microsoft documentation: Azure Cosmos DB Python SDK best
> practices (learn.microsoft.com/azure/cosmos-db/best-practice-python), Python SDK README
> (learn.microsoft.com/python/api/overview/azure/cosmos-readme), Python SDK performance tips
> (learn.microsoft.com/azure/cosmos-db/nosql/performance-tips-python-sdk), .NET SDK v3
> (learn.microsoft.com/azure/cosmos-db/nosql/sdk-dotnet-v3), and the Azure Well-Architected
> Framework guide for Cosmos DB (learn.microsoft.com/azure/well-architected/service-guides/
> cosmos-db) — all verified September 2026. Data modelling guidance follows established
> NoSQL design principles from the official Cosmos DB documentation.

# Azure Cosmos DB: NoSQL API Reference

## 1. What Cosmos DB Is and When to Use It

Azure Cosmos DB is a fully managed, globally distributed NoSQL database service. It exposes
multiple API surfaces over the same underlying engine:

| API | Compatible with | Use when |
|---|---|---|
| **NoSQL (SQL API)** | Native Cosmos DB | New projects; JSON documents; rich SQL query syntax; best SDK support |
| **MongoDB** | MongoDB wire protocol | Migrating from MongoDB without changing application code |
| **Apache Cassandra** | Cassandra CQL | Migrating from Cassandra; wide-column workloads |
| **Apache Gremlin** | Gremlin graph traversal | Graph data (relationships, recommendations) |
| **Table** | Azure Table Storage API | Migrating from Table Storage with global distribution and higher throughput |
| **PostgreSQL** | PostgreSQL wire protocol | Distributed relational workloads via Citus extension |

This file covers the **NoSQL API** exclusively — it is the native API, has the best SDK
support for Python and C#, and is the right choice for all new projects.

In the RPA and data engineering context, Cosmos DB is the correct database choice when:
- Documents (invoices, transactions, bot run records) have variable schemas or nested structure
- Global distribution or multi-region writes are required
- Sub-10ms read latency at any scale is a requirement
- The access pattern is primarily point reads by document ID + partition key (not complex
  relational joins)

Use **Azure SQL Database** when: relational joins are central to the query pattern, the schema
is stable and normalized, or the team is deeply familiar with T-SQL and wants consistency
guarantees at row/table level. Use **Cosmos DB Analytical Store + Synapse/Databricks** for
large-scale aggregation queries over Cosmos DB data — the transactional store is not designed
for full-table scans.

---

## 2. Core Data Model

```
Cosmos DB Account
  └── Database (logical grouping, no billing at this level)
        └── Container (the unit of scale and partitioning)
              └── Items (JSON documents)
```

- **Account** — the top-level resource; has its endpoint URL and keys/managed identity config.
- **Database** — organizes containers; throughput can optionally be provisioned at database
  level (shared across containers in the database).
- **Container** — the unit of scale. Every container has a **partition key** and a throughput
  setting. This is the most important design decision (see Section 4).
- **Item** — a JSON document. Every item requires an `id` field (string; unique within its
  partition) and a field matching the container's partition key path. All other fields are
  schema-free.

```json
{
  "id": "INV-2025-001",
  "vendorId": "ACME-001",
  "invoiceDate": "2025-01-15",
  "totalAmount": 1250.00,
  "lineItems": [
    { "description": "Widget A", "qty": 10, "unitPrice": 125.00 }
  ],
  "status": "processed",
  "_rid": "...",
  "_ts": 1736942400,
  "_etag": "\"00000000-0000-0000-0000-...\""
}
```

System fields (`_rid`, `_ts`, `_etag`, `_self`) are added automatically. `_etag` is used for
optimistic concurrency; `_ts` is the last-modified Unix timestamp.

---

## 3. Throughput: Request Units and Provisioning Modes

All Cosmos DB operations (reads, writes, queries, deletes) consume **Request Units (RUs)**.
One RU equals the cost of reading a 1 KB item by its ID and partition key.

| Operation | Approximate RU cost |
|---|---|
| Point read (by id + partition key) | 1 RU per 1 KB |
| Insert / replace / upsert | ~5–10 RUs (varies with item size) |
| Delete | ~5 RUs |
| Query (index hit) | 1–10 RUs typical |
| Query (cross-partition) | Higher; proportional to partitions scanned |

**Provisioned throughput:** Set a fixed RU/s limit on the container. Billed hourly for the
provisioned capacity regardless of usage. Appropriate for predictable, sustained workloads.
Auto-scale provisioned throughput adjusts between 10% and 100% of the configured maximum
automatically.

**Serverless:** Billed per RU consumed, no provisioned capacity. No commitment, no idle cost.
Appropriate for: dev/test, intermittent workloads, Azure Functions output binding targets.
Serverless has limits: max 250 GB storage per container, no global distribution (single
region only), no analytical store.

**Rule:** start with serverless for development and low-volume production; switch to
provisioned (with auto-scale) when the workload is predictable or crosses 1,000 RU/s average.

---

## 4. Partition Key Design (Most Important Decision)

The partition key determines how data is distributed across physical partitions. A poor
partition key choice causes hot partitions (one partition receives most traffic, throttled
at its per-partition limit) or uneven data distribution. Both degrade performance and
increase cost.

**Partition key selection criteria (from official documentation):**
- High cardinality — many distinct values to distribute data evenly.
- Even read and write distribution across values — avoid keys where one value (e.g., `status:
  "pending"`) receives 90% of writes.
- Queries should include the partition key in their filter — cross-partition queries are more
  expensive and slower.
- Items in the same partition key are co-located — this enables efficient in-partition queries
  and transactional batches.

**Common patterns:**

| Use case | Good partition key | Anti-pattern |
|---|---|---|
| Invoice documents | `/vendorId` (many vendors, even distribution) | `/status` (few values, hot partition) |
| Bot run logs | `/botName` (multiple bots) or `/date` | `/region` if only one region active |
| User records | `/userId` | `/country` if most users in one country |
| IoT telemetry | `/deviceId` | `/sensorType` (few types, hot) |

For large containers (hundreds of GB), consider **synthetic partition keys** that combine
multiple fields: `"/partitionKey"` with value `"vendorId_month"` (e.g., `"ACME-001_2025-01"`)
to achieve both high cardinality and bounded partition size.

---

### Hierarchical Partition Keys (HPK)

Hierarchical partition keys allow up to **three levels** of nesting. They solve two specific
problems that a single partition key cannot:

1. **The 20 GB logical partition limit.** Each logical partition in Cosmos DB has a hard limit
   of 20 GB. A single partition key value (e.g., `/tenantId = "Contoso"`) that accumulates
   more than 20 GB of data stops accepting new writes. Hierarchical partition keys break each
   logical partition into sub-partitions — the logical partition is now the full concatenation
   of all levels (e.g., `Contoso_Alice`), so each sub-partition has its own 20 GB limit.

2. **Fan-out query reduction in read-heavy workloads.** A query that specifies only the first
   level of the hierarchy is routed to a single physical partition containing all data for that
   tenant, rather than fanning out across all physical partitions.

**Requirements:** NoSQL API only; new containers only (cannot be added to existing containers
without data migration); SDK minimum versions: .NET SDK v3 >= 3.33.0, JavaScript SDK >= 4.0.0,
Python SDK >= 4.x.

**When to use HPK vs. a synthetic partition key:**

| Scenario | Recommendation |
|---|---|
| First-level key has HIGH cardinality AND data per key exceeds 20 GB | Hierarchical partition key |
| First-level key has LOW cardinality | Synthetic partition key (HPK will just create uneven first-level distribution) |
| Existing container approaching 20 GB per partition key value | New container with HPK + data migration |
| Multi-tenant app: partitioning by `/tenantId` hitting 20 GB per tenant | HPK: `/tenantId → /userId` or `/tenantId → /id` |

**Best practice — unique last level:** Use `/id` (the item's primary key) as the final HPK
level to guarantee that each individual logical partition never exceeds 20 GB. This makes
the partition key unbounded in practice. If you need stored procedures or transactional
batches at a level above `/id`, do not use `/id` as the last level — those operations are
scoped to a full logical partition key value (all levels).

```python
# Python SDK — create container with hierarchical partition keys
from azure.cosmos import PartitionKey

container = db.create_container_if_not_exists(
    id="InvoicesByTenant",
    partition_key=PartitionKey(
        path=["/tenantId", "/vendorId", "/id"],  # 3-level HPK
        kind="MultiHash"
    )
)

# Query specifying only first level — routed to single physical partition
# (efficient: no fan-out)
items = list(container.query_items(
    query="SELECT * FROM c WHERE c.tenantId = @t",
    parameters=[{"name": "@t", "value": "Inchcape"}],
    partition_key="Inchcape"     # first-level prefix routing
))

# Point read — must supply all levels as a tuple/list
item = container.read_item(
    item="INV-001",
    partition_key=("Inchcape", "ACME", "INV-001")  # (tenantId, vendorId, id)
)
```

```csharp
// C# SDK — create container with HPK
var containerProperties = new ContainerProperties
{
    Id = "InvoicesByTenant",
    PartitionKeyPaths = new List<string> { "/tenantId", "/vendorId", "/id" },
    PartitionKeyDefinitionVersion = PartitionKeyDefinitionVersion.V2
};
await db.CreateContainerIfNotExistsAsync(containerProperties, throughput: 400);

// Point read with HPK — PartitionKey takes multiple values
var response = await container.ReadItemAsync<Invoice>(
    id: "INV-001",
    partitionKey: new PartitionKeyBuilder()
        .Add("Inchcape")
        .Add("ACME")
        .Add("INV-001")
        .Build());
```

### Physical Partition Limits

Understanding physical partitions is necessary for capacity planning:

| Resource | Limit per physical partition |
|---|---|
| Storage | 50 GB |
| Throughput | 10,000 RU/s |
| Logical partition size | 20 GB per logical partition key value |

Cosmos DB automatically splits physical partitions when either limit is approached. You
cannot directly control the number of physical partitions — they are managed by the service.
With HPK and `/id` as the last level, each logical partition is a single item, so storage per
logical partition is always bounded by the item size limit (2 MB per item).

---

## 4a. Change Feed

The change feed is a log of all insert and update operations on a container, in the order
they occur per partition. It is the mechanism for building event-driven architectures on top
of Cosmos DB — any write to the container triggers downstream processing without polling.

**What the change feed includes:** All inserts and updates (upserts), ordered within each
partition by modification time. Deletes are not included by default (enable "all versions and
deletes" mode for delete events — requires containers created with this mode explicitly).

**Common uses in RPA and data engineering:**
- Materialize a secondary index or read model (write invoices to one container; change feed
  builds a summary view in another container for reporting)
- Trigger downstream processing when a bot writes a transaction result
- Sync Cosmos DB data to ADLS Gen2 or Event Hubs for Databricks analytics
- Invalidate a cache when data changes

**Change feed processor (Python):**

```python
# The change feed processor pattern — preferred for production
# (handles lease management, distributed processing, checkpointing automatically)
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import asyncio

credential = DefaultAzureCredential()
client = CosmosClient(os.environ["COSMOS_ENDPOINT"], credential)
container = client.get_database_client("InvoiceDB").get_container_client("Invoices")
lease_container = client.get_database_client("InvoiceDB").get_container_client("leases")

# Read the change feed from a specific point in time
start_time = datetime(2025, 1, 1, tzinfo=timezone.utc)
for page in container.query_items_change_feed(
    start_time=start_time,
    is_start_from_beginning=False
).by_page():
    for item in page:
        print(f"Changed: {item['id']}")
```

**Change feed as an Azure Functions trigger** (see `references/azure-functions.md`
bindings table and Pattern D section) is the production pattern for event-driven change
feed consumption. The Functions runtime manages the lease container automatically.

```python
# Azure Functions Cosmos DB trigger — fires on every change feed event
@app.cosmos_db_trigger(
    arg_name="documents",
    database_name="InvoiceDB",
    container_name="Invoices",
    lease_container_name="leases",
    connection="CosmosDBConnection",        # CosmosDBConnection__accountEndpoint for managed identity
    create_lease_container_if_not_exists=True
)
def process_invoice_changes(documents: func.DocumentList) -> None:
    for doc in documents:
        logging.info("Invoice changed: %s vendor=%s status=%s",
                     doc["id"], doc.get("vendorId"), doc.get("status"))
        # Write to ADLS, update secondary index, trigger notification, etc.
```

---

## 11. Python SDK Reference

### Installation and Client Setup

```bash
uv add azure-cosmos azure-identity
```

```python
# src/cosmos_client.py — singleton pattern (mandatory; one client per application lifetime)
import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient
from azure.identity import DefaultAzureCredential

# Synchronous client — for scripts, batch jobs, Azure Functions (sync)
_credential = DefaultAzureCredential()
cosmos_client = CosmosClient(
    url=os.environ["COSMOS_ENDPOINT"],          # https://<account>.documents.azure.com:443/
    credential=_credential                       # managed identity; never use account keys
)

# Asynchronous client — for FastAPI, async Azure Functions, any async framework
async_cosmos_client = AsyncCosmosClient(
    url=os.environ["COSMOS_ENDPOINT"],
    credential=_credential
)
```

**The singleton pattern is mandatory.** Each `CosmosClient` instance manages its own
connection pool and address routing cache. Recreating the client on every request throws
away these resources and causes a severe performance degradation. Instantiate once at module
level or via dependency injection.

**Use `azure.cosmos.aio.CosmosClient`** (async) for: FastAPI, Quart, async Azure Functions,
any framework running an async event loop. Use `azure.cosmos.CosmosClient` (sync) for:
scripts, REFramework bots via `Invoke Python`, simple Azure Functions (sync).

**Never use account keys in production code.** `DefaultAzureCredential` with RBAC roles is
the production standard. Required role: `Cosmos DB Built-in Data Contributor` on the account
or database.

### Database and Container Operations

```python
# Get references (no network call — these are lightweight client objects)
db = cosmos_client.get_database_client("InvoiceDB")
container = db.get_container_client("Invoices")

# Create database and container (idempotent)
db = cosmos_client.create_database_if_not_exists("InvoiceDB")
container = db.create_container_if_not_exists(
    id="Invoices",
    partition_key=PartitionKey(path="/vendorId"),
    offer_throughput=400       # RU/s; omit for serverless account
)
```

### Item CRUD

```python
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosHttpResponseError

# Create (fails if id + partition key already exists)
invoice = {"id": "INV-001", "vendorId": "ACME", "amount": 1250.00, "status": "pending"}
container.create_item(body=invoice)

# Upsert — create or replace; preferred for idempotent writes
container.upsert_item(body=invoice)

# Read by id + partition key (cheapest operation — 1 RU per 1 KB)
item = container.read_item(item="INV-001", partition_key="ACME")

# Update (replace entire document)
item["status"] = "processed"
container.replace_item(item="INV-001", body=item)

# Partial update with patch (modify specific fields without reading first)
from azure.cosmos import operations as patch_ops
container.patch_item(
    item="INV-001",
    partition_key="ACME",
    patch_operations=[
        patch_ops.set("/status", "processed"),
        patch_ops.set("/processedAt", "2025-01-15T09:00:00Z"),
        patch_ops.incr("/retryCount", 1)
    ]
)

# Delete
container.delete_item(item="INV-001", partition_key="ACME")

# Error handling
try:
    item = container.read_item(item="INV-MISSING", partition_key="ACME")
except CosmosResourceNotFoundError:
    # Document does not exist — handle as expected case
    item = None
except CosmosHttpResponseError as exc:
    if exc.status_code == 429:
        # Rate limited (RU/s exceeded) — SDK retries automatically for reads/queries
        # but NOT for writes (writes are not idempotent by default)
        raise
```

### Query

Cosmos DB for NoSQL uses a SQL-like query syntax. All queries return JSON documents.

```python
# In-partition query (include partition key in WHERE — always prefer this)
query = "SELECT * FROM c WHERE c.vendorId = @vendorId AND c.status = @status"
params = [
    {"name": "@vendorId", "value": "ACME"},
    {"name": "@status",   "value": "pending"}
]
items = list(container.query_items(
    query=query,
    parameters=params,
    partition_key="ACME"          # enables in-partition routing
))

# Cross-partition query (more expensive — avoid for high-frequency operations)
all_pending = list(container.query_items(
    query="SELECT * FROM c WHERE c.status = 'pending'",
    enable_cross_partition_query=True
))

# Projection — only fetch required fields (reduces RU cost and network payload)
vendors = list(container.query_items(
    query="SELECT c.id, c.vendorId, c.amount FROM c WHERE c.status = 'processed'",
    partition_key="ACME"
))

# Aggregation (requires index support or cross-partition scan)
result = list(container.query_items(
    query="SELECT VALUE SUM(c.amount) FROM c WHERE c.vendorId = @vendorId",
    parameters=[{"name": "@vendorId", "value": "ACME"}],
    partition_key="ACME"
))
total = result[0] if result else 0.0

# Pagination — query_items returns an iterator; process in pages
pager = container.query_items(
    query="SELECT * FROM c WHERE c.vendorId = @vendorId",
    parameters=[{"name": "@vendorId", "value": "ACME"}],
    partition_key="ACME",
    max_item_count=50             # items per page
)
for page in pager.by_page():
    for item in page:
        process(item)
```

### Transactional Batch

All items in a batch must share the same partition key. The batch succeeds or fails
atomically — no partial commits.

```python
# All items must have the same partition key value
batch = container.create_transactional_batch(partition_key="ACME")
batch.upsert_item({"id": "INV-001", "vendorId": "ACME", "status": "processed"})
batch.upsert_item({"id": "INV-002", "vendorId": "ACME", "status": "processed"})
batch.patch_item("INV-003", [patch_ops.set("/status", "failed")])

results = container.execute_transactional_batch(batch)
# results is a list of per-operation results; all succeed or all fail
```

### Async Pattern

```python
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential

async def get_invoice(invoice_id: str, vendor_id: str) -> dict | None:
    async with AsyncDefaultAzureCredential() as credential:
        async with AsyncCosmosClient(os.environ["COSMOS_ENDPOINT"], credential) as client:
            container = client.get_database_client("InvoiceDB").get_container_client("Invoices")
            try:
                return await container.read_item(item=invoice_id, partition_key=vendor_id)
            except CosmosResourceNotFoundError:
                return None

# For singleton async client (module level — preferred for Functions/FastAPI)
_async_credential = AsyncDefaultAzureCredential()
_async_client = AsyncCosmosClient(os.environ["COSMOS_ENDPOINT"], _async_credential)

async def upsert_invoice(invoice: dict) -> None:
    container = _async_client.get_database_client("InvoiceDB").get_container_client("Invoices")
    await container.upsert_item(body=invoice)
```

---

## 6. C# SDK Reference (.NET SDK v3)

### Installation

```xml
<PackageReference Include="Microsoft.Azure.Cosmos" Version="3.*" />
<PackageReference Include="Azure.Identity" Version="1.*" />
```

### Client Setup (DI Singleton)

```csharp
// Program.cs — register CosmosClient as singleton
using Azure.Identity;
using Microsoft.Azure.Cosmos;

builder.Services.AddSingleton(_ => new CosmosClient(
    accountEndpoint: builder.Configuration["CosmosEndpoint"],
    tokenCredential: new DefaultAzureCredential(),
    clientOptions: new CosmosClientOptions
    {
        // Direct mode: bypasses the gateway for data plane ops — lowest latency
        ConnectionMode = ConnectionMode.Direct,
        // Preferred regions for reads (list in priority order)
        ApplicationPreferredRegions = new[] { "Australia East", "Southeast Asia" },
        // Enable content response on write: false reduces payload (no full document returned)
        EnableContentResponseOnWrite = false,
        SerializerOptions = new CosmosSerializationOptions
        {
            PropertyNamingPolicy = CosmosPropertyNamingPolicy.CamelCase
        }
    }));
```

**`ConnectionMode.Direct`** is the production standard for .NET. It bypasses the Azure
Cosmos DB gateway for data plane operations (reads, writes, queries), routing directly to
the partition replica, which reduces latency by 1–5 ms per operation. Use
`ConnectionMode.Gateway` only when Direct mode is blocked by network policy (strict firewall
that permits only HTTPS/443 outbound).

### Item CRUD

```csharp
// Inject via DI
public class InvoiceRepository
{
    private readonly Container _container;

    public InvoiceRepository(CosmosClient client)
    {
        _container = client.GetContainer("InvoiceDB", "Invoices");
    }

    // Point read — cheapest operation; requires both id and partition key
    public async Task<Invoice?> GetAsync(string id, string vendorId, CancellationToken ct = default)
    {
        try
        {
            var response = await _container.ReadItemAsync<Invoice>(
                id: id,
                partitionKey: new PartitionKey(vendorId),
                cancellationToken: ct);
            return response.Resource;
        }
        catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return null;
        }
    }

    // Upsert — create or replace (preferred for idempotent writes)
    public async Task<Invoice> UpsertAsync(Invoice invoice, CancellationToken ct = default)
    {
        var response = await _container.UpsertItemAsync(
            item: invoice,
            partitionKey: new PartitionKey(invoice.VendorId),
            cancellationToken: ct);
        return response.Resource;
    }

    // Delete
    public async Task DeleteAsync(string id, string vendorId, CancellationToken ct = default)
    {
        await _container.DeleteItemAsync<Invoice>(
            id: id,
            partitionKey: new PartitionKey(vendorId),
            cancellationToken: ct);
    }
}
```

### Query with FeedIterator

```csharp
// Always prefer FeedIterator for queries — enables pagination and streaming
public async IAsyncEnumerable<Invoice> GetByVendorAsync(
    string vendorId,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    var query = new QueryDefinition(
        "SELECT * FROM c WHERE c.vendorId = @vendorId AND c.status = @status")
        .WithParameter("@vendorId", vendorId)
        .WithParameter("@status", "pending");

    using FeedIterator<Invoice> iterator = _container.GetItemQueryIterator<Invoice>(
        queryDefinition: query,
        requestOptions: new QueryRequestOptions
        {
            PartitionKey = new PartitionKey(vendorId),   // in-partition routing
            MaxItemCount = 50
        });

    while (iterator.HasMoreResults)
    {
        FeedResponse<Invoice> page = await iterator.ReadNextAsync(ct);
        foreach (var item in page)
            yield return item;
    }
}
```

### Patch (Partial Update)

```csharp
// Modify specific fields without reading the full document first
var patchOperations = new List<PatchOperation>
{
    PatchOperation.Set("/status", "processed"),
    PatchOperation.Set("/processedAt", DateTime.UtcNow),
    PatchOperation.Increment("/retryCount", 1)
};

await _container.PatchItemAsync<Invoice>(
    id: "INV-001",
    partitionKey: new PartitionKey("ACME"),
    patchOperations: patchOperations);
```

---

## 7. Indexing Policy

By default, Cosmos DB indexes all fields in all documents. This simplifies querying but
increases write cost (every write must update the index). Optimize for write-heavy workloads
by excluding paths that are never queried.

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/vendorId/?"},
    { "path": "/status/?"},
    { "path": "/invoiceDate/?"},
    { "path": "/amount/?"}
  ],
  "excludedPaths": [
    { "path": "/rawPayload/*"},
    { "path": "/lineItems/*/description/?"},
    { "path": "/_etag/?"}
  ]
}
```

Set the indexing policy when creating the container (`container_properties` in Python,
`ContainerProperties` in C#). Changing the policy on an existing container triggers an
asynchronous re-index operation that runs in the background.

---

## 8. Consistency Levels

Cosmos DB offers five consistency levels, from strongest to weakest:

| Level | Guarantee | RU cost | Latency | When to use |
|---|---|---|---|---|
| **Strong** | Linearizability — reads always return latest committed write | Highest (2x reads) | Highest | Financial data requiring strict consistency; single region only |
| **Bounded Staleness** | Reads lag behind writes by at most N operations or T seconds | High | Low-medium | Multi-region with bounded consistency window |
| **Session** | Consistent for a client session — your own writes are readable | Medium (default) | Low | Most applications; default and correct for most RPA/automation scenarios |
| **Consistent Prefix** | No out-of-order reads; eventual but ordered | Low | Low | Order-sensitive data where slight staleness is acceptable |
| **Eventual** | No ordering guarantee — lowest latency and cost | Lowest | Lowest | High-throughput read workloads where eventual consistency is acceptable |

**Session consistency is the default and the correct choice for most automation and bot
workloads.** It guarantees that a bot's own writes are immediately visible to the same bot's
subsequent reads within the same client session (i.e., same `CosmosClient` instance), which
is the behaviour most automation logic assumes.

---

## 9. Local Development: Cosmos DB Emulator

```bash
# Run the Cosmos DB emulator locally (Docker)
docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest
docker run -d \
  --name cosmosdb-emulator \
  -p 8081:8081 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254 \
  -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=3 \
  -e AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=false \
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

# Emulator endpoint: https://localhost:8081/
# Emulator key: C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
# Explorer UI: https://localhost:8081/_explorer/index.html

# Python connection to emulator (disable TLS verification for local only)
import os
os.environ["AZURE_COSMOS_DISABLE_SERVER_CERTIFICATE_VALIDATION"] = "true"
client = CosmosClient(
    url="https://localhost:8081/",
    credential="C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
)
```

The emulator key shown above is the well-known public emulator key published in all official
Microsoft documentation — it is not a secret.

---

## 10. Best Practices

| Category | Practice | Reason |
|---|---|---|
| Client | Singleton `CosmosClient` for application lifetime | Connection pool and routing cache reuse; recreating per request causes severe degradation |
| Client | Use `azure.cosmos.aio` for async frameworks | Avoids blocking the event loop in FastAPI, async Azure Functions |
| Client | .NET: use `ConnectionMode.Direct` | Bypasses gateway for data plane ops; 1-5ms latency reduction |
| Auth | `DefaultAzureCredential` + `Cosmos DB Built-in Data Contributor` RBAC | Never use account keys in application code |
| Region | Co-locate app and Cosmos DB account in same Azure region | 1-2ms in-region vs 50ms+ cross-region |
| Partition key | High cardinality, even distribution, matches query filter | Avoids hot partitions and cross-partition queries |
| Reads | Use point reads (`read_item` / `ReadItemAsync`) over queries wherever possible | Point reads cost 1 RU/KB; queries cost more |
| Writes | Use `upsert_item` / `UpsertItemAsync` for idempotent writes | Safe for retry without duplicate inserts |
| Writes | Use patch operations for partial updates | Avoids read-then-write pattern; lower RU cost |
| Indexing | Exclude fields never used in queries | Reduces write RU cost and storage |
| Queries | Always include partition key in query filter | Eliminates cross-partition fan-out |
| Throughput | Start with serverless; move to provisioned auto-scale when sustained traffic is known | Avoids over-provisioning during development |
| Emulator | Use Docker emulator for local development and CI | No Cosmos DB account cost during development |

---

## Sources Consulted

- Microsoft Learn: Best practices for Python SDK in Azure Cosmos DB for NoSQL
  (learn.microsoft.com/azure/cosmos-db/best-practice-python, September 2026) — singleton
  client rule, async vs sync client selection, region colocation, indexing guidance.
- Microsoft Learn: Azure Cosmos DB Python SDK README v4.15.0
  (learn.microsoft.com/python/api/overview/azure/cosmos-readme, September 2026) — SDK
  installation, CosmosClient construction, CRUD examples, bulk/transactional batch support
  status, id must be string constraint.
- Microsoft Learn: Performance tips for Azure Cosmos DB Python SDK
  (learn.microsoft.com/azure/cosmos-db/nosql/performance-tips-python-sdk, September 2026)
  — singleton client justification, preferred regions, indexing path performance impact.
- Microsoft Learn: Azure Cosmos DB .NET SDK v3 release notes
  (learn.microsoft.com/azure/cosmos-db/nosql/sdk-dotnet-v3, September 2026) — .NET SDK v3
  package name, Direct mode recommendation, minimum supported framework (.NET Standard 2.0).
- Microsoft Learn: Architecture best practices for Azure Cosmos DB for NoSQL
  (learn.microsoft.com/azure/well-architected/service-guides/cosmos-db, September 2026) —
  availability zone configuration, SDK usage mandate, transactional batch, analytical store,
  minimum recommended SDK version enforcement.
- Microsoft Learn: Quickstart — Azure Cosmos DB for NoSQL with Python
  (learn.microsoft.com/azure/cosmos-db/quickstart-python, September 2026) — end-to-end
  quickstart patterns for database/container/item operations.

Partition key design and consistency level selection are stable architectural guidance.
The RU cost estimates are approximate and workload-dependent — use the Azure Cosmos DB
Capacity Calculator for production sizing. The emulator version tag and port mappings
should be verified against the current Docker Hub image tags before use.
