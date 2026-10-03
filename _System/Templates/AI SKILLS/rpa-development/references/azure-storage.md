> Content in this file is grounded in official Microsoft documentation:
> Azure Blob Storage Python SDK reference (learn.microsoft.com/python/api/overview/azure/
> storage-blob-readme, version 12.30.2, September 2026), Azure Blob Storage developer guides
> (learn.microsoft.com/azure/storage/blobs, September 2026), and the Azure SDK for Python
> storage examples (learn.microsoft.com/azure/developer/python/sdk/examples/azure-sdk-
> example-storage-use, September 2026). All SDK method names and client hierarchy information
> are sourced from the official SDK README. Connection string patterns are shown for reference
> only — managed identity is the production standard.

# Azure Storage: Complete Reference

## 1. Azure Storage Services Overview

A single Azure Storage Account provides access to four distinct storage services. Each is
independent — a Storage Account can be used for one, several, or all simultaneously.

| Service | Use case | Access pattern | SDK client class (Python) |
|---|---|---|---|
| **Blob Storage** | Unstructured data — files, images, documents, backups, logs | Object storage via HTTP/SDK | `BlobServiceClient`, `ContainerClient`, `BlobClient` |
| **Queue Storage** | Async message passing between services | FIFO queue, message TTL, dequeue count | `QueueServiceClient`, `QueueClient` |
| **Table Storage** | Semi-structured NoSQL key-value data | Entity queries by PartitionKey/RowKey | `TableServiceClient`, `TableClient` |
| **File Storage** (Azure Files) | SMB/NFS file shares mountable on VMs | Shared file system via SMB 3.0 or NFS | `ShareServiceClient`, `ShareClient` |

**Azure Data Lake Storage Gen2 (ADLS Gen2)** is Blob Storage with a hierarchical namespace
enabled on the account. It adds directory-level operations, POSIX-compatible ACLs, and
Hadoop-compatible semantics. Use ADLS Gen2 for data engineering workloads (Databricks,
Synapse, ADF pipelines). Use standard Blob Storage for application storage, archival, and
file serving. Both use the same underlying storage account; enabling hierarchical namespace
is a one-way operation at account creation.

**Storage Account SKUs:**
- `Standard_LRS` — locally redundant (3 copies in one datacenter). Cheapest. Appropriate for
  dev/test and workloads that can tolerate datacenter-level failure.
- `Standard_ZRS` — zone-redundant (3 availability zones). Minimum for production in supported
  regions.
- `Standard_GRS` / `Standard_RAGRS` — geo-redundant (also replicates to a paired region).
  Use for disaster recovery requirements.
- `Premium_LRS` — SSD-backed for low-latency block blob workloads (does not support all blob
  tiers).

---

## 2. Authentication: DefaultAzureCredential — The Production Standard

**Never use storage account keys or SAS tokens in production application code.** Keys grant
unrestricted access to the entire storage account and cannot be scoped to a container or
specific operation. Use managed identity + RBAC for all production workloads.

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# DefaultAzureCredential tries credentials in this order:
# 1. EnvironmentCredential (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
# 2. WorkloadIdentityCredential (Azure Kubernetes Service)
# 3. ManagedIdentityCredential (Azure VM, Container Apps, Functions)
# 4. SharedTokenCacheCredential (VS / Visual Studio Code cached login)
# 5. VisualStudioCodeCredential
# 6. AzureCliCredential (az login — this is what developers use locally)
# 7. AzurePowerShellCredential
# 8. InteractiveBrowserCredential

credential = DefaultAzureCredential()
account_url = "https://<storage-account-name>.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
```

**Required RBAC roles for storage access:**

| Role | Scope | Grants |
|---|---|---|
| `Storage Blob Data Contributor` | Account or container | Read, write, delete blobs |
| `Storage Blob Data Reader` | Account or container | Read-only blob access |
| `Storage Blob Data Owner` | Account or container | Full control including POSIX ACLs (ADLS) |
| `Storage Queue Data Contributor` | Account or queue | Read, write, delete queue messages |
| `Storage Queue Data Message Processor` | Account or queue | Peek, dequeue, delete messages |
| `Storage Table Data Contributor` | Account | Read, write, delete table entities |

Assign roles at the container level (not account level) where possible — least-privilege
principle. A bot that only reads from one container should have `Storage Blob Data Reader` on
that container, not on the whole account.

**Local development authentication:** `DefaultAzureCredential` falls through to `AzureCliCredential`
locally if `az login` has been run. No separate credentials file or environment variable
configuration is needed for developers.

```bash
az login                                          # authenticate locally
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee <developer-email-or-service-principal-id> \
  --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default/containers/<container>"
```

---

## 3. Blob Storage: Python SDK Reference

### Client Hierarchy

The Azure Blob Storage Python SDK (`azure-storage-blob`) exposes three client classes:

```
BlobServiceClient          → Entire storage account
  └── ContainerClient      → One blob container
        └── BlobClient     → One individual blob
```

Each client can be instantiated directly from a URL or derived from a parent:

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

credential = DefaultAzureCredential()
account_url = "https://mystorageaccount.blob.core.windows.net"

# BlobServiceClient — account level
service_client = BlobServiceClient(account_url=account_url, credential=credential)

# ContainerClient — from service client or directly
container_client = service_client.get_container_client("invoices")
# OR directly:
container_url = f"{account_url}/invoices"
container_client = ContainerClient(container_url, credential=credential)

# BlobClient — from container client or directly
blob_client = container_client.get_blob_client("2025/jan/inv-001.pdf")
# OR directly:
blob_url = f"{account_url}/invoices/2025/jan/inv-001.pdf"
blob_client = BlobClient(blob_url, credential=credential)
```

**Best practice: treat clients as singletons.** Instantiate once at module level (or at
dependency injection container level in C#) and reuse across calls. Client construction
includes connection setup — recreating on every call wastes resources and can cause port
exhaustion in high-throughput scenarios.

```python
# MODULE LEVEL — created once, reused across all function invocations
_credential = DefaultAzureCredential()
_blob_service = BlobServiceClient(
    account_url=os.environ["STORAGE_ACCOUNT_URL"],
    credential=_credential
)

def get_container(name: str) -> ContainerClient:
    return _blob_service.get_container_client(name)
```

### Container Operations

```python
from azure.storage.blob import ContainerClient, PublicAccess

# Create a container (idempotent with exist_ok=True)
container_client.create_container()                     # raises if exists
container_client.create_container(exist_ok=True)        # idempotent

# List containers in the account
for container in service_client.list_containers():
    print(container["name"], container["last_modified"])

# Delete a container
container_client.delete_container()
```

### Upload: All Patterns

```python
from azure.storage.blob import BlobClient, StandardBlobTier
import io

blob_client = container_client.get_blob_client("reports/q3-2025.xlsx")

# From a local file path
with open("./q3-2025.xlsx", "rb") as f:
    blob_client.upload_blob(f, overwrite=True)

# From bytes
data: bytes = b"Hello, Azure Storage."
blob_client.upload_blob(data, overwrite=True)

# From a string
text: str = "Invoice data here"
blob_client.upload_blob(text.encode("utf-8"), overwrite=True)

# From an in-memory stream
stream = io.BytesIO(b"stream data here")
blob_client.upload_blob(stream, overwrite=True)

# Upload to Cool tier directly (cost optimization for infrequently accessed data)
blob_client.upload_blob(data, overwrite=True, standard_blob_tier=StandardBlobTier.COOL)

# Large file upload with configurable block size (default 4 MiB; max 4000 MiB)
from azure.storage.blob import BlobBlock
blob_client.upload_blob(
    data=large_data,
    overwrite=True,
    max_concurrency=4,       # parallel upload threads
    blob_type="BlockBlob"
)
```

### Download: All Patterns

```python
# Download to a local file
with open("./downloaded.xlsx", "wb") as f:
    f.write(blob_client.download_blob().readall())

# Download to bytes (in-memory — only for small blobs)
data: bytes = blob_client.download_blob().readall()

# Download to string
text: str = blob_client.download_blob().readall().decode("utf-8")

# Download in chunks (memory-efficient for large blobs)
stream = blob_client.download_blob()
chunk_list = []
for chunk in stream.chunks():
    chunk_list.append(chunk)  # each chunk is bytes; process here

# Async download (for Azure Functions or async applications)
from azure.storage.blob.aio import BlobServiceClient as AsyncBlobServiceClient
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential

async def download_async(container: str, blob_name: str) -> bytes:
    async with AsyncDefaultAzureCredential() as credential:
        async with AsyncBlobServiceClient(account_url, credential=credential) as client:
            blob = client.get_container_client(container).get_blob_client(blob_name)
            return await (await blob.download_blob()).readall()
```

### List Blobs

```python
# List all blobs in a container (flat listing)
for blob in container_client.list_blobs():
    print(blob.name, blob.size, blob.last_modified)

# List with prefix filter (virtual directory simulation)
for blob in container_client.list_blobs(name_starts_with="2025/jan/"):
    print(blob.name)

# List by hierarchy (simulate folder structure)
for item in container_client.walk_blobs(name_starts_with="2025/"):
    if hasattr(item, "prefix"):
        print(f"[DIR]  {item.name}")   # BlobPrefix — virtual directory
    else:
        print(f"[FILE] {item.name}")   # BlobItem
```

### Delete and Lifecycle

```python
# Delete a single blob
blob_client.delete_blob()                              # raises if not found
blob_client.delete_blob(delete_snapshots="include")   # delete blob + all snapshots

# Check existence before operating
if blob_client.exists():
    data = blob_client.download_blob().readall()

# Soft delete — blob is retained for the configured retention period before permanent deletion
# Enable at account level; blob is marked deleted but recoverable
blob_client.delete_blob()           # soft-deletes if enabled on account
blob_client.undelete_blob()         # restores a soft-deleted blob within retention window
```

### Blob Access Tiers

```python
from azure.storage.blob import StandardBlobTier

# Move blob to Cool tier (infrequently accessed, cheaper storage, higher access cost)
blob_client.set_standard_blob_tier(StandardBlobTier.COOL)

# Move blob to Archive tier (rarely accessed; rehydration takes hours)
blob_client.set_standard_blob_tier(StandardBlobTier.ARCHIVE)

# Rehydrate from Archive (ONLINE required before the blob is readable again)
# This operation is asynchronous and can take 1-15 hours depending on priority
blob_client.set_standard_blob_tier(StandardBlobTier.HOT)  # triggers rehydration

# Check current tier
props = blob_client.get_blob_properties()
print(props.blob_tier, props.archive_status)
```

**Blob tier cost model:**
- **Hot** — highest storage cost, lowest access cost. Active data.
- **Cool** — ~50% lower storage cost vs Hot, higher per-operation cost. Data accessed < once/month.
- **Cold** — lower than Cool storage, higher access. Data accessed < once/90 days.
- **Archive** — lowest storage cost, highest access cost, hours to rehydrate. Long-term retention.

### Metadata and Properties

```python
# Set metadata (arbitrary key-value pairs, stored with the blob)
blob_client.set_blob_metadata({
    "invoiceid": "INV-2025-001",
    "vendor": "AcmeCorp",
    "processedat": "2025-01-15T09:00:00Z"
})

# Read metadata and properties
props = blob_client.get_blob_properties()
print(props.metadata)          # dict of metadata
print(props.content_type)      # MIME type
print(props.size)              # size in bytes
print(props.last_modified)     # datetime
print(props.blob_tier)         # Hot / Cool / Archive
```

### SAS Tokens (Delegated Access — Not for Application Code)

SAS tokens are appropriate for: generating time-limited download links for end-users,
enabling external systems to upload directly to blob storage without going through your
application. They are not appropriate for application-to-application authentication — use
managed identity for that.

```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timezone, timedelta

sas_token = generate_blob_sas(
    account_name="mystorageaccount",
    container_name="invoices",
    blob_name="inv-001.pdf",
    account_key=os.environ["STORAGE_ACCOUNT_KEY"],   # OK here: only used to sign the SAS
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1)
)
download_url = f"https://mystorageaccount.blob.core.windows.net/invoices/inv-001.pdf?{sas_token}"
```

---

## 4. Queue Storage: Python SDK Reference

Queue Storage is the standard lightweight message queue for Azure workloads. It is simpler
and cheaper than Service Bus. Use it when: message ordering guarantees beyond FIFO are not
needed, message size is under 64 KiB, dead-lettering is not required, and topic/subscription
fan-out is not needed.

```python
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient

credential = DefaultAzureCredential()
service_client = QueueServiceClient(
    account_url="https://mystorageaccount.queue.core.windows.net",
    credential=credential
)

queue_client = service_client.get_queue_client("rpa-output")

# Send a message (max 64 KiB; max TTL 7 days by default, max 7 days)
import json
queue_client.send_message(json.dumps({"transaction_id": "T-001", "status": "success"}))

# Receive and process messages (messages become invisible for 30s after dequeue)
messages = queue_client.receive_messages(messages_per_page=10, visibility_timeout=60)
for message in messages:
    payload = json.loads(message.content)
    # process...
    queue_client.delete_message(message)  # delete after successful processing

# Peek without dequeuing (non-destructive inspection)
for message in queue_client.peek_messages(max_messages=5):
    print(message.content)

# Get queue depth (approximate message count)
props = queue_client.get_queue_properties()
print(props.approximate_message_count)
```

**Visibility timeout and dequeue count:** When a message is dequeued, it becomes invisible
for the `visibility_timeout` duration. If processing fails and the message is not deleted
within that window, it becomes visible again and can be dequeued by another consumer. After
a configurable number of dequeues (`max_dequeue_count`, default 5), the message is moved to
the poison message queue (`<queue-name>-poison`). Check this queue for systematic processing
failures.

---

## 5. Table Storage: Python SDK Reference

Table Storage is a NoSQL key-value store with a flat schema — rows are entities with a
`PartitionKey`, `RowKey`, and arbitrary properties. It is cheap and fast for point reads by
PartitionKey + RowKey, but has limited query capability (no joins, no aggregations, no full-
text search). Use it for: configuration tables, lookup tables, audit logs, and status tracking.
For complex query patterns, use Cosmos DB instead.

```python
from azure.data.tables import TableServiceClient, TableClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
table_client = TableServiceClient(
    endpoint="https://mystorageaccount.table.core.windows.net",
    credential=credential
).get_table_client("BotStatus")

# Upsert an entity (create or replace)
entity = {
    "PartitionKey": "AU_ANX_InvoiceBot",   # partition = bot name
    "RowKey": "2025-01-15",                 # row = date
    "Status": "Completed",
    "ProcessedCount": 142,
    "FailedCount": 3
}
table_client.upsert_entity(entity)

# Get a single entity by partition + row key (fastest operation)
entity = table_client.get_entity(
    partition_key="AU_ANX_InvoiceBot",
    row_key="2025-01-15"
)

# Query entities in a partition (table scan within partition)
from azure.data.tables import TableEntity
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'AU_ANX_InvoiceBot' and Status eq 'Failed'"
)
for e in entities:
    print(e["RowKey"], e["FailedCount"])

# Delete an entity
table_client.delete_entity(partition_key="AU_ANX_InvoiceBot", row_key="2025-01-15")
```

---

## 6. Data Lake Storage Gen2 (ADLS Gen2)

ADLS Gen2 is standard Blob Storage with `isHierarchicalNamespaceEnabled: true` on the
account. It adds:
- **Directory-level operations** (rename, move at directory level without copying all files)
- **POSIX-compatible ACLs** at file and directory level (not just RBAC)
- **Hadoop-compatible endpoint** for Spark/Databricks access via `abfss://` protocol

Use ADLS Gen2 for: Databricks Lakehouse storage, ADF pipeline staging, Synapse Analytics,
any workload where Spark or Hadoop tooling needs to access the data.

```python
# ADLS Gen2 uses the DataLake SDK, not the Blob SDK
# pip install azure-storage-file-datalake
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
service_client = DataLakeServiceClient(
    account_url="https://mystorageaccount.dfs.core.windows.net",
    credential=credential
)

# Create a file system (equivalent to blob container)
fs_client = service_client.get_file_system_client("bronze")
fs_client.create_file_system()

# Create a directory
dir_client = fs_client.get_directory_client("invoices/2025/jan")
dir_client.create_directory()

# Upload a file
file_client = dir_client.create_file("inv-001.json")
with open("inv-001.json", "rb") as f:
    data = f.read()
    file_client.append_data(data, offset=0, length=len(data))
    file_client.flush_data(len(data))

# Read a file
download = file_client.download_file()
content = download.readall()
```

**ACL management** (ADLS Gen2 specific — not available on standard Blob Storage):

```python
# Grant a service principal read access to a specific directory
from azure.storage.filedatalake import DataLakeFileSystemClient, DataLakeDirectoryClient

acl_props = dir_client.get_access_control()
# Modify acl_props["acl"] and call set_access_control
dir_client.set_access_control(
    acl="user::rwx,group::r-x,other::r-x,user:<sp-object-id>:r-x"
)
```

---

## 7. C# SDK Reference (Azure.Storage.Blobs)

```csharp
using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;

// Module-level singleton (DI container pattern in ASP.NET Core / Azure Functions)
// Never instantiate per-request
var credential = new DefaultAzureCredential();
var serviceClient = new BlobServiceClient(
    new Uri("https://mystorageaccount.blob.core.windows.net"),
    credential);

// Get container and blob clients
var containerClient = serviceClient.GetBlobContainerClient("invoices");
var blobClient = containerClient.GetBlobClient("2025/jan/inv-001.pdf");

// Upload
await using (var stream = File.OpenRead("inv-001.pdf"))
{
    await blobClient.UploadAsync(stream, overwrite: true);
}

// Upload with options (access tier)
var uploadOptions = new BlobUploadOptions
{
    AccessTier = AccessTier.Cool
};
await blobClient.UploadAsync(BinaryData.FromString("Hello!"), uploadOptions);

// Download to stream
var response = await blobClient.DownloadStreamingAsync();
await using (var fileStream = File.OpenWrite("./downloaded.pdf"))
{
    await response.Value.Content.CopyToAsync(fileStream);
}

// Download to string
var download = await blobClient.DownloadContentAsync();
string text = download.Value.Content.ToString();

// List blobs
await foreach (var blobItem in containerClient.GetBlobsAsync(prefix: "2025/jan/"))
{
    Console.WriteLine($"{blobItem.Name} ({blobItem.Properties.ContentLength} bytes)");
}

// Set metadata
var metadata = new Dictionary<string, string>
{
    { "invoiceid", "INV-001" },
    { "vendor", "AcmeCorp" }
};
await blobClient.SetMetadataAsync(metadata);
```

**Dependency injection in ASP.NET Core or isolated Azure Functions:**

```csharp
// Program.cs
builder.Services.AddSingleton(_ =>
    new BlobServiceClient(
        new Uri(builder.Configuration["StorageAccountUrl"]),
        new DefaultAzureCredential()));
```

---

## 8. Best Practices

**Performance — upload/download:**
- For files larger than 8 MiB, the SDK automatically uses block (chunked) upload. Control
  `max_concurrency` (Python) or `MaximumConcurrency` (C#) to tune parallel block upload
  throughput against available bandwidth.
- For reads, download in chunks when the blob may be large (>100 MiB) to avoid loading the
  entire file into memory. Use `stream.chunks()` in Python or `DownloadStreamingAsync()` in C#.

**Performance — listing:**
- List with a `prefix` filter wherever possible. Blob listing without a prefix is a full
  container scan. For virtual folder structures, use `walk_blobs()` (Python) or
  `GetBlobsByHierarchyAsync()` (C#).

**Cost — blob tiers:**
- Set the access tier at upload time for data that is immediately archivable (audit logs,
  processed invoice PDFs). Changing tier after upload costs a tier-change operation fee.
- Use lifecycle management policies to automatically move blobs from Hot → Cool → Archive
  based on last-modified date. Define policies in the Azure Portal or via Bicep/ARM.

**Security:**
- Never store storage account keys in application code, configuration files, or environment
  variables. Use `DefaultAzureCredential` and RBAC role assignments.
- Disable storage account key access entirely (set `allowSharedKeyAccess: false` on the
  account) in environments where all access goes through managed identity. This prevents
  accidental key-based access that bypasses RBAC auditing.
- Enable **soft delete** for blobs (minimum 7-day retention) and **versioning** for critical
  data containers to protect against accidental or malicious deletion.
- Enable **diagnostic logging** (`StorageBlobLogs`) to Log Analytics for audit trails.

**Naming:**
- Container names: lowercase, 3–63 characters, letters/numbers/hyphens only.
- Blob names: up to 1,024 characters, any Unicode character. Use `/` as a virtual directory
  delimiter (e.g., `2025/jan/invoices/inv-001.pdf`).

---

## Sources Consulted

- Microsoft Learn: Azure Blob Storage Python SDK README
  (learn.microsoft.com/python/api/overview/azure/storage-blob-readme, version 12.30.2,
  September 2026) — client hierarchy (BlobServiceClient/ContainerClient/BlobClient),
  SDK method signatures, async client patterns, code examples for upload/download.
- Microsoft Learn: Create and manage client objects
  (learn.microsoft.com/azure/storage/blobs/storage-blob-client-management, September 2026)
  — singleton best practice, DefaultAzureCredential with storage, ContainerClient and
  BlobClient construction from URL.
- Microsoft Learn: Upload a block blob with Python
  (learn.microsoft.com/azure/storage/blobs/storage-blob-upload-python, September 2026) —
  upload_blob() all overloads, BlobUploadOptions, max_concurrency, staging blocks.
- Microsoft Learn: Download a blob with Python
  (learn.microsoft.com/azure/storage/blobs/storage-blob-download-python, September 2026) —
  download_blob() all patterns, chunked download, async download pattern.
- Microsoft Learn: Azure Blob Storage quickstart for Python
  (learn.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python, September 2026)
  — end-to-end quickstart: container creation, upload, list, download, delete.
- Microsoft Learn: Use Azure Storage with Python SDK
  (learn.microsoft.com/azure/developer/python/sdk/examples/azure-sdk-example-storage-use,
  September 2026) — DefaultAzureCredential with BlobClient, RBAC role assignment via CLI.
- Microsoft Learn: Azure Storage queues overview and Queue Python SDK reference
  (learn.microsoft.com/azure/storage/queues, September 2026) — visibility timeout, dequeue
  count, poison message queue pattern.
- Official Azure SDK for Python: azure-data-tables, azure-storage-file-datalake
  (pypi.org/project/azure-data-tables, azure-storage-file-datalake, September 2026) —
  TableClient upsert/query/delete patterns, DataLakeServiceClient operations, ACL management.

SDK method signatures (upload_blob, download_blob, list_blobs, queue operations) are stable
across minor versions. The RBAC role names and DefaultAzureCredential credential chain are
stable. The ADLS Gen2 ACL management API and the Table Storage query filter syntax are the
sections most likely to require verification against the current SDK README before use.
