> Content in this file is grounded in official Microsoft documentation: Azure SDK for Python
> guidelines (azure.github.io/azure-sdk/python_implementation.html), Azure SDK for .NET
> guidelines, DefaultAzureCredential documentation (learn.microsoft.com/python/api/azure-
> identity/azure.identity.defaultazurecredential), Azure Key Vault Python reference, and
> Application Insights SDK documentation (all verified September 2026). Python tooling
> recommendations (uv, Ruff, mypy) align with this skill's established tooling standards
> in `references/azure-devops-cicd.md`.

# Azure Development Practices: Python and C#

## 1. The Shared Authentication Foundation: DefaultAzureCredential

Every Azure SDK client requires a credential. `DefaultAzureCredential` is the one credential
class to use in both Python and C#, in all environments, in all code. It tries authentication
methods in a defined order, automatically resolving to the right credential for each context:

| Environment | Credential used automatically |
|---|---|
| Local development (`az login`) | `AzureCliCredential` (no code change needed) |
| Local development (VS Code signed in) | `VisualStudioCodeCredential` |
| Azure Functions / Container Apps / ACI | `ManagedIdentityCredential` |
| Azure VM with managed identity | `ManagedIdentityCredential` |
| GitHub Actions / Azure DevOps | `EnvironmentCredential` (via AZURE_CLIENT_ID etc.) |
| Azure Kubernetes Service (Workload Identity) | `WorkloadIdentityCredential` |

The same code runs locally and in production without modification. The pattern eliminates
credential-in-code entirely.

```python
# Python — import once, reuse everywhere
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

# Pass to any Azure SDK client
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient
from azure.servicebus import ServiceBusClient

blob_client  = BlobServiceClient("https://account.blob.core.windows.net", credential)
kv_client    = SecretClient("https://myvault.vault.azure.net", credential)
sb_client    = ServiceBusClient("mynamespace.servicebus.windows.net", credential)
```

```csharp
// C# — same pattern
using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Security.KeyVault.Secrets;

var credential = new DefaultAzureCredential();
var blobClient = new BlobServiceClient(new Uri("https://account.blob.core.windows.net"), credential);
var kvClient   = new SecretClient(new Uri("https://myvault.vault.azure.net"), credential);
```

**Do not catch `CredentialUnavailableException` and fall back to a connection string.** If
the credential is unavailable, the deployment environment is not configured correctly — fix
the configuration, do not work around it in code.

---

## 2. Python: Project Setup for Azure Development

### Package Installation

```bash
# Core identity and common utilities — always install these
uv add azure-identity                # DefaultAzureCredential and all auth strategies
uv add azure-core                    # Shared SDK infrastructure (retry, pipeline, errors)

# Add SDK packages per service used
uv add azure-storage-blob            # Blob Storage
uv add azure-storage-queue          # Queue Storage
uv add azure-storage-file-datalake  # ADLS Gen2
uv add azure-data-tables            # Table Storage
uv add azure-keyvault-secrets       # Key Vault secrets
uv add azure-servicebus             # Service Bus
uv add azure-appconfiguration       # App Configuration
uv add azure-monitor-opentelemetry  # Application Insights / Azure Monitor
```

### pyproject.toml (Azure Python project)

```toml
[project]
name = "my-azure-bot"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "azure-identity>=1.17",
    "azure-storage-blob>=12.22",
    "azure-keyvault-secrets>=4.8",
    "azure-servicebus>=7.12",
    "azure-monitor-opentelemetry>=1.4",
    "pydantic-settings>=2.4",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.2",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "mypy>=1.10",
    "ruff>=0.5",
]

[tool.mypy]
strict = true
python_version = "3.12"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "ANN"]
```

### Configuration with pydantic-settings

```python
# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Storage
    storage_account_url: str                    # https://<account>.blob.core.windows.net
    invoice_container: str = "invoices"

    # Service Bus
    servicebus_namespace: str                   # <namespace>.servicebus.windows.net
    queue_name: str = "rpa-transactions"

    # Key Vault
    key_vault_url: str                          # https://<vault>.vault.azure.net

    # Application Insights
    applicationinsights_connection_string: str

    # Processing
    max_retry_count: int = 3
    processing_batch_size: int = 50

# Singleton instance — import from here in all modules
settings = Settings()
```

```bash
# .env (local development — never commit; add to .gitignore)
STORAGE_ACCOUNT_URL=https://mystorageaccount.blob.core.windows.net
SERVICEBUS_NAMESPACE=mynamespace.servicebus.windows.net
QUEUE_NAME=rpa-transactions-dev
KEY_VAULT_URL=https://myvault.vault.azure.net
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
MAX_RETRY_COUNT=3
PROCESSING_BATCH_SIZE=10
```

### Key Vault Integration

```python
# src/secrets.py — load secrets from Key Vault at startup
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from src.config import settings

def load_secrets() -> dict[str, str]:
    """Fetch secrets from Key Vault. Call once at application startup."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=settings.key_vault_url, credential=credential)
    return {
        "db_password":    client.get_secret("DatabasePassword").value,
        "api_key":        client.get_secret("ExternalApiKey").value,
        "smtp_password":  client.get_secret("SmtpPassword").value,
    }

# Load at module level (once per process start)
# secrets = load_secrets()  # call in main() after config is loaded
```

For Azure Functions or Container Apps, prefer Key Vault references in Application Settings
(`@Microsoft.KeyVault(SecretUri=...)`) over fetching secrets in code — they are resolved by
the platform without any SDK code and are rotated automatically when the vault secret rotates.

---

## 3. Application Insights: Observability for Azure Python Applications

Azure Monitor OpenTelemetry is the current standard for Python application observability.
It replaces the older `opencensus-ext-azure` and classic Application Insights SDK.

```python
# src/telemetry.py
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import Tracer
import logging

def configure_telemetry() -> None:
    """Call once at application startup before any other code runs."""
    configure_azure_monitor(
        connection_string=settings.applicationinsights_connection_string,
        logger_name="my-azure-bot",    # structured logs from this logger go to App Insights
        enable_live_metrics=True
    )

# Get a tracer for custom spans
tracer: Tracer = trace.get_tracer("my-azure-bot")

# Use standard Python logging — automatically shipped to Application Insights
import logging
log = logging.getLogger("my-azure-bot")
log.setLevel(logging.INFO)

# In your business logic
def process_invoice(invoice_id: str) -> None:
    with tracer.start_as_current_span("process_invoice") as span:
        span.set_attribute("invoice.id", invoice_id)
        log.info("Processing invoice", extra={"invoice_id": invoice_id, "step": "start"})
        # ... processing ...
        log.info("Invoice processed", extra={"invoice_id": invoice_id, "step": "complete"})
```

**Structured logging — always use `extra` for queryable fields:**

```python
# CORRECT — key-value pairs queryable in Application Insights KQL
log.info("Transaction completed", extra={
    "event": "transaction.complete",
    "transaction_id": txn_id,
    "duration_ms": elapsed_ms,
    "bot_name": "AU_ANX_InvoiceBot"
})

# WRONG — flat string, no queryable fields
log.info(f"Transaction {txn_id} completed in {elapsed_ms}ms")
```

---

## 4. C# Azure Development Practices

### SDK Package References (.csproj)

```xml
<ItemGroup>
  <!-- Identity — always include -->
  <PackageReference Include="Azure.Identity" Version="1.*" />

  <!-- Storage -->
  <PackageReference Include="Azure.Storage.Blobs" Version="12.*" />
  <PackageReference Include="Azure.Storage.Queues" Version="12.*" />

  <!-- Key Vault -->
  <PackageReference Include="Azure.Security.KeyVault.Secrets" Version="4.*" />

  <!-- Service Bus -->
  <PackageReference Include="Azure.Messaging.ServiceBus" Version="7.*" />

  <!-- App Insights — isolated worker model (current standard) -->
  <PackageReference Include="Microsoft.ApplicationInsights.WorkerService" Version="2.*" />
  <!-- OR OpenTelemetry approach (recommended for new projects) -->
  <PackageReference Include="Azure.Monitor.OpenTelemetry.AspNetCore" Version="1.*" />
</ItemGroup>
```

### Dependency Injection Pattern (ASP.NET Core / Isolated Azure Functions)

```csharp
// Program.cs — configure all Azure clients once at startup
using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Security.KeyVault.Secrets;
using Azure.Messaging.ServiceBus;

var builder = Host.CreateApplicationBuilder(args);
var credential = new DefaultAzureCredential();

// Register Azure SDK clients as singletons
builder.Services.AddSingleton(_ =>
    new BlobServiceClient(
        new Uri(builder.Configuration["StorageAccountUrl"]),
        credential));

builder.Services.AddSingleton(_ =>
    new SecretClient(
        new Uri(builder.Configuration["KeyVaultUrl"]),
        credential));

builder.Services.AddSingleton(_ =>
    new ServiceBusClient(
        builder.Configuration["ServiceBusNamespace"],
        credential));

// Application Insights (OpenTelemetry approach)
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor(options =>
        options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"]);
```

### Configuration (appsettings.json + User Secrets)

```json
// appsettings.json (safe to commit — no secrets)
{
  "StorageAccountUrl": "https://mystorageaccount.blob.core.windows.net",
  "KeyVaultUrl": "https://myvault.vault.azure.net",
  "ServiceBusNamespace": "mynamespace.servicebus.windows.net",
  "InvoiceContainer": "invoices",
  "QueueName": "rpa-transactions"
}
```

```bash
# User secrets for local development (never committed)
dotnet user-secrets set "ApplicationInsights:ConnectionString" "InstrumentationKey=..."
dotnet user-secrets set "DatabasePassword" "localdevpassword"
```

### ILogger in C# (Application Insights Integration)

```csharp
// Inject ILogger<T> — messages automatically route to Application Insights
public class InvoiceProcessor
{
    private readonly ILogger<InvoiceProcessor> _log;

    public InvoiceProcessor(ILogger<InvoiceProcessor> logger) => _log = logger;

    public async Task ProcessAsync(string invoiceId)
    {
        // Structured logging — properties are queryable in KQL
        _log.LogInformation("Processing invoice {InvoiceId}", invoiceId);
        // NOT: _log.LogInformation($"Processing invoice {invoiceId}");
        // Message template strings enable semantic logging in Application Insights

        // Exception logging with full context
        try { /* ... */ }
        catch (Exception ex)
        {
            _log.LogError(ex, "Failed to process invoice {InvoiceId}", invoiceId);
            throw;
        }
    }
}
```

---

## 5. Testing Azure-Dependent Code

The strategy for testing code that calls Azure services: unit-test business logic with mocked
clients; integration-test the integration boundary against a real Azure environment.

### Python: Mocking Azure SDK Clients

```python
# tests/test_invoice_processor.py
from unittest.mock import MagicMock, AsyncMock, patch
import pytest
from src.invoice_processor import InvoiceProcessor

def test_process_invoice_success():
    # Arrange: mock the blob client — no actual Azure call
    mock_blob_client = MagicMock()
    mock_blob_client.download_blob.return_value.readall.return_value = b'{"id": "INV-001"}'
    mock_blob_client.exists.return_value = True

    processor = InvoiceProcessor(blob_client=mock_blob_client)

    # Act
    result = processor.process("INV-001")

    # Assert
    assert result["status"] == "success"
    mock_blob_client.download_blob.assert_called_once()

def test_process_invoice_not_found():
    mock_blob_client = MagicMock()
    mock_blob_client.exists.return_value = False

    processor = InvoiceProcessor(blob_client=mock_blob_client)

    with pytest.raises(FileNotFoundError):
        processor.process("INV-MISSING")

@pytest.mark.asyncio
async def test_async_upload():
    mock_blob_client = AsyncMock()
    mock_blob_client.upload_blob.return_value = None

    # Test async upload path
    await mock_blob_client.upload_blob(b"data", overwrite=True)
    mock_blob_client.upload_blob.assert_awaited_once()
```

### Python: Integration Tests against Azure

```python
# tests/integration/test_blob_storage.py
import pytest
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Skip integration tests if no Azure credentials are available
pytestmark = pytest.mark.skipif(
    os.getenv("AZURE_STORAGE_ACCOUNT_URL") is None,
    reason="Azure integration test environment not configured"
)

@pytest.fixture(scope="module")
def blob_service():
    return BlobServiceClient(
        account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
        credential=DefaultAzureCredential()
    )

@pytest.fixture(autouse=True)
def test_container(blob_service):
    """Create a test container before each test; delete after."""
    container = blob_service.get_container_client("test-integration")
    container.create_container(exist_ok=True)
    yield container
    container.delete_container()

def test_upload_and_download(test_container):
    blob = test_container.get_blob_client("test-blob.txt")
    blob.upload_blob(b"integration test data", overwrite=True)
    downloaded = blob.download_blob().readall()
    assert downloaded == b"integration test data"
```

### C#: Mocking Azure SDK Clients

```csharp
// Tests/InvoiceProcessorTests.cs
using Moq;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;

public class InvoiceProcessorTests
{
    [Fact]
    public async Task ProcessAsync_BlobExists_ReturnsSuccess()
    {
        // Arrange
        var mockBlobClient = new Mock<BlobClient>();
        var mockDownload = BinaryData.FromString("{\"id\": \"INV-001\"}");

        mockBlobClient
            .Setup(x => x.ExistsAsync(default))
            .ReturnsAsync(Response.FromValue(true, Mock.Of<Response>()));

        mockBlobClient
            .Setup(x => x.DownloadContentAsync(default))
            .ReturnsAsync(Response.FromValue(
                BlobsModelFactory.BlobDownloadResult(mockDownload),
                Mock.Of<Response>()));

        var processor = new InvoiceProcessor(mockBlobClient.Object);

        // Act
        var result = await processor.ProcessAsync("INV-001");

        // Assert
        Assert.Equal("success", result.Status);
        mockBlobClient.Verify(x => x.DownloadContentAsync(default), Times.Once);
    }
}
```

---

## 6. Local Development Setup Checklist

For both Python and C# Azure development, the following must be in place before writing code:

```bash
# 1. Authenticate with Azure CLI (used by DefaultAzureCredential locally)
az login
az account set --subscription "<subscription-id>"

# 2. Verify you have the correct role on the target resource
az role assignment list --assignee $(az ad signed-in-user show --query id -o tsv) \
  --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>"

# 3. Test credential works before writing application code
python3 -c "
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
cred = DefaultAzureCredential()
client = BlobServiceClient('https://mystorageaccount.blob.core.windows.net', credential=cred)
print([c['name'] for c in client.list_containers()])
"

# 4. Install Azure VS Code extension (includes Storage Explorer, Functions, Container Apps tools)
# Extension: ms-azuretools.vscode-azurefunctions
# Extension: ms-azuretools.vscode-azurecontainerapps
# Extension: ms-azuretools.vscode-azurestorage
# Extension: ms-azuretools.vscode-docker

# 5. Install Azurite for local Storage emulation (required for Functions development)
npm install -g azurite
azurite --silent --location /tmp/azurite --debug /tmp/azurite-debug.log &
```

---

## 7. Retry and Error Handling

All Azure SDK clients have built-in retry policies with exponential backoff for transient
failures. Do not implement your own retry loop around Azure SDK calls for transient errors —
the SDK handles these correctly.

```python
from azure.core.exceptions import (
    ResourceNotFoundError,      # 404 — blob/queue/secret does not exist
    ResourceExistsError,        # 409 — trying to create something that already exists
    HttpResponseError,          # Other HTTP errors (4xx/5xx)
    ServiceRequestError,        # Network/transport error (SDK will retry)
    ClientAuthenticationError,  # Auth failure — check credential and RBAC assignment
)

try:
    data = blob_client.download_blob().readall()
except ResourceNotFoundError:
    # Blob does not exist — handle as expected business case
    raise FileNotFoundError(f"Blob {blob_name} not found in {container_name}")
except ClientAuthenticationError as exc:
    # Permanent auth error — do not retry; fix the managed identity or role assignment
    log.error("Authentication failed — check managed identity RBAC assignment", exc_info=exc)
    raise
except HttpResponseError as exc:
    # Unexpected HTTP error after SDK retries exhausted
    log.error("Azure Storage error after retries", extra={"status": exc.status_code}, exc_info=exc)
    raise
```

---

## 8. Key Patterns Summary

| Pattern | Python | C# |
|---|---|---|
| Authentication | `DefaultAzureCredential()` | `new DefaultAzureCredential()` |
| SDK clients | Module-level singleton | DI container singleton |
| Config management | `pydantic-settings` + `.env` | `appsettings.json` + User Secrets |
| Secrets | Key Vault `SecretClient` or KV reference in App Settings | Key Vault `SecretClient` or KV reference |
| Logging | `logging` module + `azure-monitor-opentelemetry` | `ILogger<T>` + `Azure.Monitor.OpenTelemetry` |
| Retry | SDK built-in (do not wrap in your own retry) | SDK built-in |
| Testing (unit) | `unittest.mock` + `MagicMock`/`AsyncMock` | Moq |
| Testing (integration) | `pytest` + skip marker + real credentials | xUnit + real credentials |
| Linting | `ruff` + `mypy --strict` | `dotnet-format` + Roslyn analyzers |

---

## Sources Consulted

- Microsoft Learn: DefaultAzureCredential Python reference
  (learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential,
  September 2026) — credential chain order, environment variable names for service principal,
  workload identity support.
- Microsoft Learn: Azure SDK for Python — use Azure Storage example
  (learn.microsoft.com/azure/developer/python/sdk/examples/azure-sdk-example-storage-use,
  September 2026) — DefaultAzureCredential with BlobClient, RBAC assignment via CLI.
- Microsoft Learn: Azure SDK for Python — configuration and credential best practices
  (azure.github.io/azure-sdk/python_implementation.html, September 2026) — singleton client
  pattern, pydantic-settings alignment.
- Microsoft Learn: Azure Monitor OpenTelemetry for Python
  (learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable, September 2026) —
  configure_azure_monitor(), structured logging with extra kwargs.
- Microsoft Learn: Azure SDK for .NET — dependency injection
  (learn.microsoft.com/dotnet/azure/sdk/dependency-injection, September 2026) —
  AddAzureClients(), singleton registration patterns.
- Microsoft Learn: Azure Key Vault Secrets Python quickstart
  (learn.microsoft.com/azure/key-vault/secrets/quick-create-python, September 2026) —
  SecretClient pattern, get_secret() usage.
- Official azure-identity SDK: azure.github.io/azure-sdk-for-python — source for the
  CredentialUnavailableException guidance.

The DefaultAzureCredential chain order and the OpenTelemetry exporter API are the most likely
to change. The RBAC role names, SDK method signatures, and singleton pattern are stable.
Always verify the current SDK minor version against pypi.org/project/azure-identity before
starting a new project.
