> Content in this file integrates official Microsoft Learn documentation
> (learn.microsoft.com/azure/azure-functions, verified July 2026), the Microsoft Build 2025
> Azure Functions announcements (May 2025), and course material provided directly by the user
> (Azure Functions Masterclass, ScholarHat). All architectural facts (plan limits, retirement
> dates, runtime versions) are sourced from official Microsoft documentation. Organization-
> specific Azure subscription IDs, resource group names, and connection strings are never
> stored here.

# Azure Functions: Complete Reference

## 1. What Azure Functions Is and Where It Fits

Azure Functions is a serverless Function-as-a-Service (FaaS) compute platform — developers
provide code and a trigger definition; Azure manages all infrastructure, scaling, and
patching. Billing is pure consumption: milliseconds of execution time multiplied by memory
allocated, with a monthly free grant of 1 million executions and 400,000 GB-seconds on the
Consumption plan.

In the RPA and automation context, Azure Functions occupies a specific position in the
integration hierarchy:

| Use case | Right tool |
|---|---|
| Lightweight event-driven integration (file uploaded → parse and store) | Azure Functions |
| Schedule-triggered Python bot replacement (run every night, process a file) | Azure Functions (Timer trigger) |
| Regex workaround for Power Automate Cloud (no native regex) | Azure Functions (HTTP trigger called from Power Automate) |
| Heavy batch ETL over millions of rows | Azure Databricks / Azure Data Factory |
| Long-running process (>10 minutes) | Azure Container Apps / Azure Batch |
| Stateful multi-step orchestration | Azure Durable Functions (extension of Functions) |
| Visual workflow with third-party connectors | Azure Logic Apps |

Azure Functions is not a replacement for UiPath Orchestrator or an RPA engine. It is the
right tool for the **stateless, event-driven, short-lived processing** that sits between
systems — data transformation, validation, notification dispatch, API delegation, and the
orchestration of lightweight tasks. For the RPA-to-Python migration context (see
`references/reframework-guide.md` and the main migration guidance), Azure Functions handles
the event-driven and API-integration tier.

---

## 2. Core Architecture: Triggers and Bindings

Every Azure Function is defined by exactly two components: a trigger and optionally one or
more bindings. Understanding this model is the prerequisite for everything else.

### Triggers

A trigger is the event that invokes the function. **Every function must have exactly one
trigger** — no function can exist without one, and no function can have two.

| Trigger type | Mechanism | Common use case | Key configuration |
|---|---|---|---|
| **HTTP** | REST API call or webhook | API endpoints, Power Automate webhooks, regex workarounds | `authLevel`: Anonymous / Function / Admin |
| **Timer** | Cron schedule | Nightly cleanup, scheduled reports, polling | 6-field CRON: `{sec} {min} {hr} {day} {month} {dow}` |
| **Blob Storage** | File created/modified in a container | Invoice processing, image analysis, ETL file ingestion | Storage path pattern: `samples/{name}` |
| **Queue Storage** | New message in a Storage Queue | Async work dispatch, decoupled processing | Queue name + connection string app setting |
| **Service Bus** | Message on a queue or topic | Enterprise-grade decoupled processing, RPA queue replacement | Queue/topic name + connection |
| **Event Grid** | Event published to an Event Grid topic | Fan-out routing (one upload → many functions) | Topic endpoint + event filter |
| **Event Hubs** | High-throughput event stream | IoT telemetry, streaming data ingestion | Event Hub name + consumer group |
| **Cosmos DB** | Document created/updated in a container | Change-feed processing, real-time data sync | Container name + lease container |

**Timer Trigger CRON format note:** Azure Functions uses a 6-field expression
(`{second} {minute} {hour} {day} {month} {day-of-week}`), which differs from the standard
Linux 5-field crontab. The second field is the addition. Example: `0 0 2 * * *` runs at
2:00:00 AM UTC daily.

### Bindings

Bindings declaratively connect the function to external resources without requiring you to
write connection, authentication, or SDK initialization code. They are optional — a function
can have zero, one, or many.

- **Input bindings:** Fetch data from an external source and pass it into the function as a
  parameter at invocation time.
- **Output bindings:** Accept data produced by the function and route it to a destination
  resource automatically.

**Complete bindings support matrix (source: official Microsoft docs, September 2026):**

| Azure service | Trigger | Input | Output | Notes |
|---|---|---|---|---|
| Blob Storage | Yes | Yes | Yes | |
| Azure Cosmos DB | Yes | Yes | Yes | |
| Azure Data Explorer | — | Yes | Yes | |
| Azure SQL | Yes | Yes | Yes | |
| Dapr | Yes | Yes | Yes | Kubernetes / IoT Edge / self-hosted only |
| Event Grid | Yes | — | Yes | |
| Event Hubs | Yes | — | Yes | |
| HTTP / webhooks | Yes | — | Yes | |
| IoT Hub | Yes | — | — | |
| Kafka | Yes | — | Yes | No Consumption plan trigger |
| Model Context Protocol | Yes | — | — | |
| Queue Storage | Yes | — | Yes | |
| Redis | Yes | Yes | Yes | |
| RabbitMQ | Yes | — | Yes | No Consumption plan trigger |
| SendGrid | — | — | Yes | |
| Service Bus | Yes | — | Yes | |
| Azure SignalR Service | Yes | Yes | Yes | |
| Table Storage | — | Yes | Yes | |
| Timer | Yes | — | — | |
| Twilio | — | — | Yes | |
| Managed connector | Yes | — | — | |

All binding extensions except HTTP and Timer require explicit registration via NuGet packages
(C#) or extension bundles (`host.json`). Extension bundles must be v4.0.0 or later for
Functions runtime v4.x. Kafka and RabbitMQ triggers require runtime-driven scaling and are
not supported on the Consumption plan.

---

## 3. Hosting Plans

The hosting plan determines scaling behavior, cold start characteristics, cost model, and
available limits. Choosing the wrong plan is a common source of production failures.

| Plan | Scaling | Cold start | Cost model | Best for | Key limits |
|---|---|---|---|---|---|
| **Consumption (Y1)** | Auto, scale-to-zero | Yes (mitigable) | Per execution + duration | Unpredictable/low traffic, prototyping | 5 min default timeout, 10 min max |
| **Flex Consumption** | Per-function scaling, always-ready instances configurable | Mitigated with always-ready | Execution + allocated memory | Enterprise serverless, private networking, consistent latency | VNet integration included |
| **Premium (EP1–EP3)** | Pre-warmed instances, no scale-to-zero | None (pre-warmed) | Minimum monthly per instance | High-throughput APIs, long-running tasks, VNet requirements | 60 min timeout (unlimited with Durable) |
| **App Service (Dedicated)** | Manual or auto-scale rules | None | Fixed hourly by SKU | Co-location with existing App Service, predictable cost | Timeout unlimited |

**Current recommendation (July 2026):** Flex Consumption is the preferred plan for new
production deployments. It combines the cost efficiency of the Consumption model with
per-function scaling, VNet integration, and configurable always-ready instances that
eliminate cold starts for critical functions. The standard Consumption plan on Linux is
being retired (see Section 4).

**Cold start mitigation options:**
- Flex Consumption or Premium: configure always-ready instances for latency-sensitive functions.
- Consumption: keep the package small; avoid heavy dependency chains at module load time.
- Python: use `FUNCTIONS_WORKER_PROCESS_COUNT` (up to 10) to pre-warm additional workers.
  Set in Application Settings, not in code.

---

## 4. Runtime Versions and Retirement Notices

### Runtime Host Version Status

Only **v4.x** of the Functions runtime is currently supported. All other versions are
retired or ending:

| Runtime version | Status | Notes |
|---|---|---|
| **v4.x** | GA — use this | Only supported version for new and existing apps |
| v3.x | Out of support (Dec 2022) | v3 on Linux Consumption **stops running Sep 30, 2026** |
| v2.x | Out of support (Dec 2022) | |
| v1.x | Out of support (Sep 14, 2026) | Migrate to v4 immediately |

**Platform retirement notices (official Microsoft, September 2026):**
- **v3 runtime on Linux Consumption:** Stops running September 30, 2026. Migrate to v4 now.
- **Linux Consumption plan (all runtimes):** Retiring September 30, 2028. Migrate to Flex
  Consumption before this date. No new language versions or features will be added to Linux
  Consumption after this announcement.
- Windows Consumption plan is not affected by the Linux retirement.

### Language Version Support Matrix (v4.x runtime, September 2026)

**Python** (use `FUNCTIONS_WORKER_RUNTIME: python`):

| Python version | Support level | End of support | Linux Consumption |
|---|---|---|---|
| 3.14 | GA | April 2029 | Not supported |
| 3.13 | GA | October 2029 | Not supported |
| 3.12 | GA | October 2028 | Supported (last version) |
| 3.11 | GA | October 2027 | Supported |
| 3.10 | GA | October 2026 | Supported |

Python 3.12 is the last Python version added to Linux Consumption. If you need Python 3.13+
on Linux, migrate to Flex Consumption.

**C# / .NET** (see Section 4a below for full C# guidance):

| .NET version | Isolated worker model | In-process model | Linux Consumption |
|---|---|---|---|
| .NET 10 | GA (Nov 2028) | Not supported | Not supported |
| .NET 9 | GA (Nov 2026) | Not supported | Supported (last version) |
| .NET 8 | GA (Nov 2026) | GA (last supported) | Supported |
| .NET Framework 4.8.1 | GA | Not supported | Not supported |

**Node.js** (TypeScript transpiles to JavaScript):

| Version | Support level | End of support | Linux Consumption |
|---|---|---|---|
| Node.js 24 | GA | April 2028 | Not supported |
| Node.js 22 | GA | April 2027 | Supported (last version) |

**Java:**

| Version | Support level | End of support | Linux Consumption |
|---|---|---|---|
| Java 25 | GA | May 2029 | Not supported |
| Java 21 | GA | September 2028 | Supported (last version) |
| Java 17/11/8 | GA | September 2027 | Supported |

**PowerShell:**

| Version | Support level | End of support | Linux Consumption |
|---|---|---|---|
| PowerShell 7.6 | GA | November 2028 | Not supported |
| PowerShell 7.4 | GA | November 2026 | Supported (last version) |

**Go:** Preview, Flex Consumption plan only, Go 1.24+. Not for production use.

### CLI Tooling

| Tool | Version | Status | Use when |
|---|---|---|---|
| Azure Functions Core Tools | v4 (GA) | Production standard | All development; full language support |
| Azure Functions CLI | v5 (Preview) | Preview | Lightweight workload-based experience; Java/PowerShell not yet supported |

Install Core Tools v4:
```bash
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

The `FUNCTIONS_EXTENSION_VERSION` application setting controls which runtime minor version
the deployed app uses. Do not change this arbitrarily — follow the official migration guides
when upgrading between major versions.

---

## 5. Local Development Workflow (Python, Core Tools v4)

### Project Initialization

```bash
# Install Core Tools v4
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Create project (use uv or venv — uv is recommended per this skill's tooling standard)
mkdir my-function-app && cd my-function-app
uv venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
func init --python                           # creates host.json, local.settings.json, requirements.txt

# Add a function from a template
func new --template "HTTP trigger" --name MyHttpTrigger
func new --template "Timer trigger" --name NightlyCleanup
func new --template "Azure Blob Storage trigger" --name ProcessInvoice

# Start the host locally (Azurite auto-managed in CLI v5; v4 needs manual Azurite)
func start
# Or with CLI v5 (preview):
func run  # auto-starts Azurite and the host
```

### Directory Structure (Python v2 Programming Model)

```
my-function-app/
├── function_app.py        # All function definitions in one file (v2 model)
├── host.json              # Runtime configuration (logging, extensions, timeouts)
├── local.settings.json    # Local environment variables — NEVER commit to source control
├── requirements.txt       # Python dependencies
└── .gitignore             # Must include local.settings.json and .venv/
```

The Python v2 programming model (introduced in Functions runtime v4) eliminates the
per-function `function.json` sidecar files. All trigger registrations are code-first,
directly in `function_app.py` using decorators.

### Python v2 Programming Model Examples

```python
# function_app.py
import azure.functions as func
import logging
import os

app = func.FunctionApp()

# HTTP Trigger — v2 decorator syntax (no function.json required)
@app.route(route="hello", methods=["GET", "POST"], auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger processed a request.")
    name = req.params.get("name") or (req.get_json().get("name")
                                       if req.headers.get("content-type") == "application/json"
                                       else None)
    if name:
        return func.HttpResponse(f"Hello, {name}.", status_code=200)
    return func.HttpResponse("Pass a name in the query string or body.", status_code=400)


# Timer Trigger — runs at 02:00:00 UTC daily
@app.timer_trigger(schedule="0 0 2 * * *", arg_name="timer", run_on_startup=False)
def nightly_cleanup(timer: func.TimerRequest) -> None:
    logging.info("Nightly cleanup triggered.")
    # Business logic here


# Blob Storage Trigger — fires when a file lands in the 'invoices' container
@app.blob_trigger(arg_name="blob", path="invoices/{name}", connection="AzureWebJobsStorage")
def process_invoice(blob: func.InputStream) -> None:
    logging.info(f"Processing blob: {blob.name}, size: {blob.length} bytes")
    content = blob.read().decode("utf-8")
    # Parse and validate content here


# Service Bus Queue Trigger — processes RPA queue messages from Service Bus
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name=os.getenv("SB_QUEUE_NAME", "rpa-tasks"),
    connection="AzureServiceBusConnection")
def process_queue_message(msg: func.ServiceBusMessage) -> None:
    body = msg.get_body().decode("utf-8")
    logging.info(f"Received message: {body}")
```

### `local.settings.json` — Full Schema (Never Commit to Source Control)

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "FUNCTIONS_WORKER_PROCESS_COUNT": "4",
    "AzureServiceBusConnection": "Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...",
    "SB_QUEUE_NAME": "rpa-tasks-dev",
    "AzureWebJobs.MyHttpTrigger.Disabled": "true"
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "*",
    "CORSCredentials": false
  },
  "ConnectionStrings": {
    "SQLConnectionString": "<sqlclient-connection-string>"
  }
}
```

**Key fields explained (from official Microsoft docs):**

| Field | Purpose |
|---|---|
| `IsEncrypted` | When `true`, all values are encrypted with the local machine key. Use `func settings encrypt` / `func settings decrypt` to manage. Default `false`. |
| `Values.AzureWebJobsStorage` | Required for all non-HTTP triggers. Use `"UseDevelopmentStorage=true"` to target Azurite locally. |
| `Values.FUNCTIONS_WORKER_RUNTIME` | Language runtime: `python`, `node`, `dotnet`, `dotnet-isolated`, `java`, `powershell`. |
| `Values.AzureWebJobs.<FunctionName>.Disabled` | Disables a specific function locally. Set to `"true"` to skip it during `func start`. |
| `Host.LocalHttpPort` | Local HTTP port (default 7071). Override with `--port` CLI flag. |
| `Host.CORS` | Allowed origins for CORS. `"*"` allows all during development. |
| `ConnectionStrings` | SQL connection strings for Entity Framework only — not for function bindings. Binding connections go in `Values`. |

`local.settings.json` is not published to Azure. Any setting the function needs in Azure
must be added separately to the Function App's Application Settings. VS Code and Core Tools
both support syncing settings between local and Azure (`func azure functionapp publish
--publish-local-settings`).

**Encrypt local settings containing secrets:**

```bash
func settings encrypt   # encrypts all Values with local machine key; sets IsEncrypted: true
func settings decrypt   # decrypts before editing; always re-encrypt before committing
```

### HTTP Test Tools for Local Development

Microsoft recommends using offline or local HTTP test tools to avoid exposing secrets to
cloud-synced services. Approved options:

- **VS Code REST Client extension** — `.http` files in VS Code; secrets stay local
- **Bruno** (usebruno.com) — offline-first API client; no cloud sync
- **curl** — built-in on macOS/Linux; `curl -X POST -H "x-functions-key: <key>" -d '{"name":"test"}' http://localhost:7071/api/MyFunction`
- **PowerShell `Invoke-RestMethod`** — built-in on Windows and cross-platform
- **Visual Studio `.http` files** — native support from VS 17.8+

Avoid tools that upload request history (including headers containing function keys) to
cloud accounts or telemetry services.

**Manually trigger a non-HTTP function during local development:**

```bash
# Trigger a Timer or Queue function via the admin endpoint (Core Tools must be running)
curl -X POST http://localhost:7071/admin/functions/NightlyCleanup \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Access Environment Variables in Python

```python
import os
queue_name = os.getenv("SB_QUEUE_NAME", "default-queue")  # with fallback default
conn_string = os.environ["AzureServiceBusConnection"]       # raises KeyError if missing
app_name    = os.environ.get("WEBSITE_SITE_NAME", "local") # None if missing (no error)
```

Both `os.getenv()` and `os.environ[]` work identically in local development (reading from
`local.settings.json` Values) and in Azure (reading from Application Settings). Do not use
`configparser` or `ConfigurationManager.AppSettings` — these are .NET patterns.

---

## 5a. C# Development Reference

### Execution Model: Isolated Worker vs. In-Process

C# in Azure Functions has two execution models. The choice is architectural and must be made
at project creation:

| Model | Status | .NET versions | Notes |
|---|---|---|---|
| **Isolated worker** | GA — use this | .NET 10, 9, 8, Framework 4.8.1 | Runs in a separate process from the Functions host. Supports all current .NET versions. Recommended for all new projects. |
| **In-process** | Retiring Nov 10, 2026 | .NET 8 only | Runs inside the Functions host process. Will lose support on November 10, 2026. Migrate existing apps to isolated worker now. |

The in-process model retirement is a hard deadline. Plan migration before November 10, 2026.
Migration guide: `learn.microsoft.com/azure/azure-functions/migrate-dotnet-to-isolated-model`

Note: .NET 10 cannot run on the Linux Consumption plan. Use Flex Consumption for .NET 10 on Linux.

### Project Structure and SDK

```xml
<!-- .csproj — isolated worker model (recommended) -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AzureFunctionsVersion>v4</AzureFunctionsVersion>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Azure.Functions.Worker" Version="2.*" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="2.*" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http" Version="3.*" />
  </ItemGroup>
</Project>

<!-- .csproj — in-process model (legacy, retiring Nov 10 2026) -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AzureFunctionsVersion>v4</AzureFunctionsVersion>
  </PropertyGroup>
  <ItemGroup>
    <!-- Minimum 4.5.0 required by Core Tools 4.0.6517+ -->
    <PackageReference Include="Microsoft.NET.Sdk.Functions" Version="4.5.0" />
  </ItemGroup>
</Project>
```

### C# Function Anatomy (In-Process Model — for reference / migration source)

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;

public static class InvoiceProcessor
{
    // FunctionName: unique, starts with letter, letters/numbers/-/_, max 127 chars
    [FunctionName("ProcessInvoiceQueue")]
    public static void Run(
        [QueueTrigger("invoices", Connection = "AzureWebJobsStorage")] string message,
        [Queue("processed-invoices")]  out string outputMessage,   // output binding via out param
        ILogger log,                                                // structured logging
        CancellationToken cancellationToken)                       // graceful shutdown support
    {
        if (cancellationToken.IsCancellationRequested)
        {
            log.LogWarning("Cancellation requested — stopping gracefully.");
            outputMessage = null;
            return;
        }
        log.LogInformation("Processing invoice: {Message}", message);
        outputMessage = $"Processed: {message}";
    }
}
```

**Multiple output values** — use `ICollector<T>` or `IAsyncCollector<T>` instead of `out`:

```csharp
[FunctionName("FanOutMessages")]
public static void Run(
    [QueueTrigger("source")]               string input,
    [Queue("destination")] ICollector<string> outputQueue,
    ILogger log)
{
    outputQueue.Add($"Copy 1: {input}");
    outputQueue.Add($"Copy 2: {input}");  // two messages to same queue
}
```

**Binding expressions** — read queue name or blob path from App Settings at runtime:

```csharp
// %queueappsetting% resolves the value of the "queueappsetting" App Setting
[QueueTrigger("%QueueName%", Connection = "StorageConnection")] string myQueueItem
```

**Async functions** — cannot use `out` parameters; use return value or `IAsyncCollector`:

```csharp
[FunctionName("BlobCopy")]
public static async Task RunAsync(
    [BlobTrigger("source/{blobName}")] Stream input,
    [Blob("dest/{blobName}", FileAccess.Write)] Stream output,
    CancellationToken token,
    ILogger log)
{
    await input.CopyToAsync(output, 4096, token);
}
```

### C# Logging: ILogger, Not Console.Write

Always use `ILogger` — `Console.Write` output is not captured by Application Insights:

```csharp
// CORRECT — structured logging; fields queryable in Application Insights KQL
log.LogInformation("Invoice {InvoiceId} processed with amount {Amount}.", invoiceId, amount);

// WRONG — not captured by Application Insights
Console.WriteLine($"Invoice {invoiceId} processed.");
```

In the isolated worker model, use `ILogger<T>` injected via dependency injection instead of
a method parameter. OpenTelemetry export is available in the isolated worker model
(`learn.microsoft.com/azure/azure-functions/opentelemetry-howto`); it is not supported in
the in-process model.

### ReadyToRun Compilation (Cold Start Reduction)

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <AzureFunctionsVersion>v4</AzureFunctionsVersion>
  <PublishReadyToRun>true</PublishReadyToRun>
  <RuntimeIdentifier>linux-x64</RuntimeIdentifier>  <!-- match deployment target OS/arch -->
</PropertyGroup>
```

ReadyToRun pre-compiles to native code at publish time, reducing JIT startup cost. Available
for .NET 6+ with Functions runtime v4. Most impactful for Consumption plan cold starts.

### Environment Variables in C#

```csharp
// Read from local.settings.json (locally) or Application Settings (Azure)
string queueName = System.Environment.GetEnvironmentVariable(
    "QueueName", EnvironmentVariableTarget.Process);
```

---

## 6. Configuration Management and Security

### Application Settings vs. Local Settings

| Setting location | Scope | Use case |
|---|---|---|
| `local.settings.json` | Local development only | Dev credentials, local emulator connection strings |
| Azure Portal → Function App → Configuration → Application Settings | Production | Non-secret config, feature flags |
| **Azure Key Vault** (via Key Vault reference) | Production | All secrets: API keys, connection strings, credentials |

**Key Vault reference pattern in Application Settings:**

```
MySecretKey = @Microsoft.KeyVault(SecretUri=https://my-vault.vault.azure.net/secrets/MySecret/)
```

The Function App's managed identity must be granted `Get` permission on the Key Vault.
This is the production-standard pattern — no secret ever touches Application Settings in
plaintext.

### Authorization Levels for HTTP Triggers

| Level | Key required | Access scope | Production use |
|---|---|---|---|
| `Anonymous` | None | Public | Protect behind APIM or Entra ID Easy Auth |
| `Function` | Function key or Host key | One function or all functions in app | Internal service-to-service |
| `Admin` | Master key `_master` | All functions + admin REST APIs | Automation/CI only; never expose |

**Key transmission:** Always pass function keys in the `x-functions-key` HTTP header, never
in the `?code=` query string parameter. The query string variant appears in gateway logs,
browser history, and Application Insights telemetry, exposing the secret.

```http
GET https://my-app.azurewebsites.net/api/MyFunction HTTP/1.1
x-functions-key: <function-key>
```

### Production Security Standards

Function keys provide shared-secret obfuscation, not true identity-based authorization.
For production APIs, use one of:

1. **Managed Identity + Azure AD (Entra ID Easy Auth):** Enable App Service Authentication
   on the Function App. Callers present a JWT bearer token from Entra ID. No shared secrets
   exist. Managed identity also eliminates connection string secrets for storage and Service
   Bus (`DefaultAzureCredential` in Python).

2. **Azure API Management (APIM):** Place APIM in front of all HTTP-triggered functions.
   APIM handles: subscription key management, OAuth2/JWT validation, rate limiting, CORS,
   request/response transformation. Functions run with `authLevel: Anonymous` (protected by
   network policy or APIM's own auth, not exposed to public internet directly).

3. **Managed Identity for Storage:** Since Build 2025, managed identity for the required
   `AzureWebJobsStorage` connection is configurable directly in the portal at Function App
   creation time. This eliminates the storage connection string from App Settings entirely.

---

## 7. Function App Grouping and Isolation

Functions within the same Function App share: hosting plan, runtime, deployment package,
environment variables, and scaling behavior. This determines how to group them.

**Group together** when functions share a business domain, have the same scaling
requirements, and are deployed in the same release cycle.

**Separate into different Function Apps** when:
- Functions require different runtime languages (one Python, one Node.js — polyglot requires
  separate apps; a single Function App cannot mix language workers).
- Functions have wildly different scaling requirements (a high-throughput event processor and
  a low-frequency nightly job would waste pre-warmed instances on the timer function).
- Functions need different security boundaries or network configurations.
- Testing isolation is required (never add test functions to a production Function App — they
  share resources including memory and storage transaction limits).

**One storage account per Function App** in production. Never share a storage account across
multiple Function Apps, especially with Durable Functions or Event Hubs triggers — these
generate high storage transaction volumes that interfere with each other.

---

## 8. Durable Functions: Stateful Serverless Orchestration

Standard Azure Functions are stateless and ephemeral. **Azure Durable Functions** is an
extension that adds stateful orchestration on top, enabling multi-step, long-running workflows
with automatic checkpointing and replay.

Durable Functions introduces three function types:

| Function type | Role |
|---|---|
| **Orchestrator** | Defines the workflow: calls activities, handles retries, manages state across steps |
| **Activity** | The actual unit of work: an atomic task (call an API, read a blob, write to a database) |
| **Client** | Starts an orchestration instance, queries its status, raises events to it |

### Pattern 1: Function Chaining (Sequential)

```python
import azure.durable_functions as df

@app.orchestration_trigger(context_name="context")
def invoice_processing_orchestrator(context: df.DurableOrchestrationContext):
    # Sequential: each step waits for the previous to complete
    extracted_data = yield context.call_activity("ExtractInvoiceData", context.get_input())
    validated_data = yield context.call_activity("ValidateInvoiceData", extracted_data)
    result        = yield context.call_activity("PostToERP", validated_data)
    return result

@app.activity_trigger(input_name="blob_path")
def ExtractInvoiceData(blob_path: str) -> dict:
    # Download blob, run ai_parse_document or Document Understanding extraction
    return {"invoice_id": "INV-001", "amount": 1250.00}

@app.activity_trigger(input_name="data")
def ValidateInvoiceData(data: dict) -> dict:
    if data["amount"] <= 0:
        raise ValueError("Invoice amount must be positive")
    return data

@app.activity_trigger(input_name="data")
def PostToERP(data: dict) -> str:
    # POST to SAP/ERP API
    return "ERP-CONFIRMATION-12345"
```

### Pattern 2: Fan-Out / Fan-In (Parallel then Aggregate)

```python
@app.orchestration_trigger(context_name="context")
def parallel_invoice_orchestrator(context: df.DurableOrchestrationContext):
    invoice_list = yield context.call_activity("GetPendingInvoices", None)

    # Fan-out: fire all activities in parallel
    tasks = [context.call_activity("ProcessSingleInvoice", inv) for inv in invoice_list]

    # Fan-in: wait for ALL to complete, then aggregate
    results = yield context.task_all(tasks)
    summary = {"processed": len(results), "total": sum(r["amount"] for r in results)}
    return summary
```

### Pattern 3: Async HTTP API (Long-Running Process with Status Poll)

```python
# Client function starts the orchestration and returns a 202 Accepted with status URLs
@app.route(route="start-process", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
@app.durable_client_input(client_name="client")
async def start_long_process(req: func.HttpRequest, client):
    payload = req.get_json()
    instance_id = await client.start_new("invoice_processing_orchestrator", client_input=payload)
    return client.create_check_status_response(req, instance_id)
# Returns: {"statusQueryGetUri": "...", "sendEventPostUri": "...", ...}
# Caller polls statusQueryGetUri until status = "Completed" or "Failed"
```

### Local Development with Durable Functions

```bash
# Start the Durable Task Scheduler emulator and Azurite (local storage)
docker run -d --name dtsemulator -p 8080:8080 -p 8082:8082 \
    mcr.microsoft.com/dts/dts-emulator:latest
docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 \
    mcr.microsoft.com/azure-storage/azurite

# Durable Task Scheduler dashboard (monitor orchestration instances)
# http://localhost:8082

func start  # start the Functions host
```

---

## 9. Real-World Integration Patterns

### Pattern A: Power Automate → Azure Functions (Regex Workaround)

Power Automate Cloud has no native regex function (see `references/regex-in-rpa.md`). The
correct workaround is an HTTP-triggered Azure Function:

```python
# function_app.py
import re
import json
import azure.functions as func

@app.route(route="regex", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def regex_handler(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    pattern = body.get("pattern", "")
    text    = body.get("text", "")
    flags   = re.IGNORECASE if body.get("ignoreCase") else 0
    try:
        match = re.search(pattern, text, flags)
        return func.HttpResponse(
            json.dumps({"matched": bool(match), "value": match.group(0) if match else None}),
            status_code=200,
            mimetype="application/json")
    except re.error as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}), status_code=400, mimetype="application/json")
```

In Power Automate: HTTP action → POST to the Function URL with `x-functions-key` header →
parse the JSON response.

### Pattern B: UiPath Bot → Service Bus → Azure Function (Async Processing)

```
UiPath Performer bot
  └─► Enqueues a Service Bus message for each completed transaction
        (payload: { "transaction_id": "...", "output": {...} })

Azure Function (Service Bus trigger)
  └─► Receives message, writes to Delta Lake / SQL / Blob for analytics
  └─► Sends confirmation email via SendGrid output binding
  └─► Updates a status table for the UiPath Insights dashboard
```

This pattern decouples the bot (which must process quickly per transaction) from the
post-processing work (which can run asynchronously).

### Pattern C: Serverless ETL — Blob Upload → Transform → Cosmos DB

```python
@app.blob_trigger(arg_name="blob", path="raw-data/{name}", connection="AzureWebJobsStorage")
@app.cosmos_db_output(arg_name="outputDoc",
                      database_name="ProcessedData",
                      container_name="Invoices",
                      connection="CosmosDBConnection",
                      create_if_not_exists=True)
def etl_blob_to_cosmos(blob: func.InputStream, outputDoc: func.Out[func.Document]) -> None:
    import json, xmltodict
    raw = blob.read()
    # Transform XML → dict → JSON document
    data = xmltodict.parse(raw)
    outputDoc.set(func.Document.from_dict(data))
```

**Anti-pattern — infinite loop:** Never write the output blob back to the same container
that triggered the function. Use a separate output container (`processed-data/`, not
`raw-data/`). Writing to the same container creates an infinite trigger loop that burns
through execution budget instantly.

---


### Pattern D: Event-Driven Image Analysis Pipeline (Blob → AI Vision → Cosmos DB)

This pattern implements the architecture from the provided course material: an image uploaded
to Blob Storage triggers a Function that calls Azure AI Vision, then writes the analysis
result to Cosmos DB via an output binding. It also demonstrates the critical production
corrections the course material identified.

**Architecture:**
```
Azure Blob Storage (image-input)
  --> [Blob Trigger / Event Grid Trigger]
        Azure Function
          --> Azure AI Vision REST API (HTTP POST, octet-stream)
          --> Cosmos DB Output Binding (structured JSON document)
```

#### Blob Trigger Timing: Standard vs. Event Grid

The course material identifies a critical production issue with standard `blobTrigger` on
the Consumption plan:

| Trigger type | Latency | Mechanism | When to use |
|---|---|---|---|
| Standard `blobTrigger` | Up to 10 minutes (low-traffic periods) | Log-polling on a schedule | Dev/test; small batch; latency-insensitive workloads |
| `eventGridBlobTrigger` | <100 ms | Event Grid push notification on blob creation | Production; any latency-sensitive pipeline |

The 10-minute delay occurs because the standard blob trigger polls the storage log on a
schedule. During low-traffic or cold-start periods, the polling interval extends
significantly. `eventGridBlobTrigger` receives a push notification from Event Grid
the moment blob creation completes — sub-100ms delivery is guaranteed.

To switch: change `blobTrigger` to `eventGridBlobTrigger` in the trigger type. The
path and connection settings are identical. Requires enabling the Event Grid extension
and creating a System Topic on the storage account in Azure Portal.

#### Managed Identity: Cosmos DB Bindings (the `__accountEndpoint` Format)

Connection strings for Cosmos DB bindings (`connection: 'CosmosDBConnection'`) can use
managed identity instead of a key-bearing connection string. The format uses a
double-underscore prefix convention — each individual setting shares the same prefix:

```
# App Settings (Azure Portal / local.settings.json Values)
CosmosDBConnection__accountEndpoint = https://<account>.documents.azure.com:443/
CosmosDBConnection__clientId        = <client-id>   # user-assigned identity only; omit for system-assigned
```

The same double-underscore pattern applies to all binding connections:

| Service | Managed identity setting | Value |
|---|---|---|
| Cosmos DB | `<PREFIX>__accountEndpoint` | `https://<account>.documents.azure.com:443/` |
| Blob Storage | `<PREFIX>__blobServiceUri` | `https://<account>.blob.core.windows.net` |
| Blob Storage (with trigger) | `<PREFIX>__queueServiceUri` also required | `https://<account>.queue.core.windows.net` |
| Service Bus | `<PREFIX>__fullyQualifiedNamespace` | `<namespace>.servicebus.windows.net` |

Required RBAC roles on the Function App's managed identity:
- Cosmos DB: `Cosmos DB Built-in Data Contributor` on the account
- Storage: `Storage Blob Data Reader` (trigger) + `Storage Blob Data Owner` or `Storage Queue Data Contributor` (trigger poison-blob queue)

#### Python Implementation (v2 model, Event Grid trigger, managed identity bindings)

```python
# function_app.py
import json
import os
import httpx
import azure.functions as func

app = func.FunctionApp()

@app.event_grid_blob_trigger(
    arg_name="blob",
    path="image-input/{name}",
    connection="AzureWebJobsStorage"    # AzureWebJobsStorage__blobServiceUri for managed identity
)
@app.cosmos_db_output(
    arg_name="output_doc",
    database_name="AnalysisDB",
    container_name="ImageAnalysis",
    connection="CosmosDBConnection",    # CosmosDBConnection__accountEndpoint for managed identity
    create_if_not_exists=False
)
def analyze_image(blob: func.InputStream, output_doc: func.Out[func.Document]) -> None:
    import logging
    log = logging.getLogger(__name__)
    log.info("Analyzing blob: %s (%d bytes)", blob.name, blob.length)

    endpoint = os.environ["VISION_API_ENDPOINT"]
    api_key  = os.environ["VISION_API_KEY"]
    url = f"{endpoint}/vision/v3.2/analyze?visualFeatures=Tags,Objects,Description"

    # POST binary stream directly to Azure AI Vision
    response = httpx.post(
        url,
        content=blob.read(),
        headers={
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": "application/octet-stream"
        },
        timeout=30.0
    )
    response.raise_for_status()
    analysis = response.json()

    # Cosmos DB requires "id" as a string; requestId from Vision API is a UUID string
    document = {
        "id":                 analysis["requestId"],
        "requestId":          analysis["requestId"],      # partition key
        "blobName":           blob.name.split("/")[-1],
        "processedTimestamp": func.utils.utcnow().isoformat(),
        "analysis":           analysis
    }

    output_doc.set(func.Document.from_dict(document))
    log.info("Stored analysis for requestId: %s", analysis["requestId"])
```

#### Node.js v4 Implementation (JavaScript, output binding return pattern)

```javascript
// src/functions/analyzeImage.js
const { app, output } = require('@azure/functions');

const cosmosOutput = output.cosmosDB({
    databaseName:    'AnalysisDB',
    containerName:   'ImageAnalysis',
    connection:      'CosmosDBConnection',   // CosmosDBConnection__accountEndpoint for managed identity
    createIfNotExists: false
});

app.storageBlob('analyzeImage', {
    path:       'image-input/{name}',
    connection: 'AzureWebJobsStorage',
    return:     cosmosOutput,               // return value maps to Cosmos DB output binding
    handler: async (blob, context) => {
        const { default: fetch } = await import('node-fetch');

        const url = `${process.env.VISION_API_ENDPOINT}/vision/v3.2/analyze` +
                    `?visualFeatures=Tags,Objects,Description`;

        const resp = await fetch(url, {
            method:  'POST',
            body:    blob,
            headers: {
                'Ocp-Apim-Subscription-Key': process.env.VISION_API_KEY,
                'Content-Type':              'application/octet-stream'
            }
        });
        if (!resp.ok) throw new Error(`Vision API error: ${resp.status}`);
        const analysis = await resp.json();

        context.log(`Analyzed ${context.triggerMetadata.name}: ${analysis.requestId}`);

        return {
            id:                 analysis.requestId,   // Cosmos DB primary key (must be string)
            requestId:          analysis.requestId,   // partition key field
            blobName:           context.triggerMetadata.name,
            processedTimestamp: new Date().toISOString(),
            analysis
        };
    }
});
```

**Production correction vs. the course material example:** Replace `axios` (raw HTTP,
no retry, no TypeScript types) with `node-fetch` or the native `fetch` (Node.js 18+) for
simple calls, and with `@azure-rest/ai-vision-image-analysis` for typed Vision SDK access
with built-in retry. The `@azure/cosmos` SDK should replace raw `CosmosDBConnection` string
handling where programmatic Cosmos DB access is needed alongside the output binding.

#### Azure AI Vision API Reference

The Azure AI Vision (formerly Computer Vision) REST API accepts images as binary or by URL:

| Parameter | Value |
|---|---|
| Endpoint format | `https://<resource>.cognitiveservices.azure.com/vision/v3.2/analyze` |
| Auth header | `Ocp-Apim-Subscription-Key: <key>` (key-based) or `Authorization: Bearer <token>` (Entra ID) |
| Binary content type | `application/octet-stream` |
| URL content type | `application/json` with body `{"url": "https://..."}` |
| `visualFeatures` param | Comma-separated: `Tags`, `Objects`, `Description`, `Categories`, `Color`, `Faces`, `Brands` |
| Key acquisition | Azure Portal → AI Services resource → Keys and Endpoint |

For production: use Entra ID authentication with `DefaultAzureCredential` and assign the
`Cognitive Services User` role to the Function's managed identity on the AI Services resource,
replacing the `Ocp-Apim-Subscription-Key` key-based pattern entirely.

---

## 10. Performance and Reliability Best Practices

All items below are sourced from `learn.microsoft.com/azure/azure-functions/functions-best-practices`
and `learn.microsoft.com/azure/azure-functions/performance-reliability` (July 2026).

**Storage account isolation:** Use a separate dedicated storage account per Function App in
production. This is mandatory for Event Hubs-triggered functions and Durable Functions, which
generate high storage transaction volumes. Do not use a storage account with Data Lake Storage
enabled for Event Hubs triggers.

**Async Python:** Use `async def` and `await` for I/O-bound operations. Never use
`.result()` or synchronous blocking inside an async function — this blocks the event loop and
degrades throughput.

**Worker process count:** For CPU-bound Python workloads, set
`FUNCTIONS_WORKER_PROCESS_COUNT` in Application Settings (not in code). Default is 1; maximum
is 10. The runtime distributes concurrent invocations across workers. For I/O-bound
workloads, async code is more effective than adding workers.

**Connection reuse:** Instantiate HTTP clients, database connections, and SDK clients once at
module level, not inside the function body. Module-level initialization is shared across
invocations on the same worker process, eliminating per-invocation connection overhead.

```python
# CORRECT — module-level client initialization (shared across warm invocations)
import httpx
_http_client = httpx.AsyncClient(timeout=30.0)

@app.route(route="process", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
async def process(req: func.HttpRequest) -> func.HttpResponse:
    response = await _http_client.get("https://api.example.com/data")
    ...

# WRONG — new client on every invocation
@app.route(route="process", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
async def process(req: func.HttpRequest) -> func.HttpResponse:
    async with httpx.AsyncClient() as client:  # creates and destroys a connection pool each time
        response = await client.get("https://api.example.com/data")
    ...
```

**Verbose logging:** Disable verbose/debug logging in production configuration. Excessive
logging has a measurable negative performance impact, particularly for high-throughput
functions.

**Package size:** Keep the deployment package small. Large packages increase cold start
times. Use a `requirements.txt` with only the packages the function actually uses — do not
share a monorepo requirements file across functions with different dependency sets.

**Run from package:** Deploy using Run From Package (`WEBSITE_RUN_FROM_PACKAGE = 1`). This
is faster than extracting files to the filesystem, improves cold-start performance for
JavaScript functions with large `node_modules`, and avoids file lock issues during deployment.

**Idempotency:** Queue, Service Bus, and Event Grid triggers guarantee at-least-once delivery.
A function invocation may occur twice for the same event. Design all functions to be
idempotent: processing the same message twice produces the same result without side effects
or data corruption. Use a unique event ID as an idempotency key in the output target.

---

## 11. CI/CD with Azure DevOps

The portal editor is for prototyping only. All production deployments go through a pipeline.

```yaml
# azure-pipelines.yml — Python Azure Function App deployment
trigger:
  branches:
    include: [main]

variables:
  pythonVersion: '3.13'
  functionAppName: 'my-function-app'

stages:
- stage: Build
  jobs:
  - job: BuildAndTest
    pool:
      vmImage: ubuntu-latest
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: $(pythonVersion)

    - script: |
        pip install uv
        uv pip install --system -r requirements.txt
        uv pip install --system ruff mypy pytest pytest-cov
      displayName: Install dependencies

    - script: ruff check .
      displayName: Lint (ruff)

    - script: mypy . --strict
      displayName: Type check (mypy)

    - script: pytest --cov=. --cov-report=xml --cov-fail-under=80
      displayName: Unit tests (coverage gate 80%)

    - task: ArchiveFiles@2
      inputs:
        rootFolderOrFile: $(System.DefaultWorkingDirectory)
        includeRootFolder: false
        archiveFile: $(Build.ArtifactStagingDirectory)/function-app.zip

    - task: PublishBuildArtifacts@1
      inputs:
        PathtoPublish: $(Build.ArtifactStagingDirectory)
        ArtifactName: function-package

- stage: Deploy
  dependsOn: Build
  jobs:
  - deployment: DeployFunction
    environment: production
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureFunctionApp@2
            inputs:
              connectedServiceNameARM: $(AzureServiceConnection)
              appType: functionAppLinux
              appName: $(functionAppName)
              package: $(Pipeline.Workspace)/function-package/function-app.zip
              deploymentMethod: zipDeploy
              runtimeStack: PYTHON|3.13
```

---

## 12. Monitoring with Application Insights

Always enable Application Insights when provisioning a Function App. It is the production
observability standard — portal log streaming is ephemeral, throttled under load, and
unsuitable for incident investigation.

**Key tables in Application Insights (query via KQL):**

| Table | Content |
|---|---|
| `traces` | `logging.info()`, `logging.warning()` output from function code |
| `exceptions` | Unhandled exceptions with stack traces |
| `requests` | HTTP-triggered function invocations (duration, status code, result) |
| `customEvents` | Custom telemetry emitted with `logging.info()` for structured events |
| `dependencies` | Outbound calls to external services (auto-tracked for HTTP and DB) |

**Structured logging for KQL queryability:**

```python
import logging
import json

# WRONG — flat string log (hard to query)
logging.info(f"Processed invoice {invoice_id} with amount {amount}")

# CORRECT — JSON-structured log (KQL can parse key-value pairs automatically)
logging.info(json.dumps({
    "event": "invoice.processed",
    "invoice_id": invoice_id,
    "amount": amount,
    "vendor": vendor_name
}))
```

**Useful KQL queries:**

```kql
// Function failure rate over 24 hours
requests
| where timestamp > ago(24h)
| summarize total=count(), failures=countif(success == false) by name
| project name, failure_rate=round(100.0 * failures / total, 2)
| order by failure_rate desc

// Exceptions by function, last 7 days
exceptions
| where timestamp > ago(7d)
| summarize count() by outerMessage, operation_Name
| order by count_ desc

// Average duration per function
requests
| where timestamp > ago(24h)
| summarize avg_ms=avg(duration) by name
| order by avg_ms desc
```

---

## 13. Anti-Patterns

| Anti-pattern | Consequence | Fix |
|---|---|---|
| Long-running function (>10 min) on Consumption plan | Hard timeout failure; state is lost | Use Durable Functions for orchestration; move compute to Azure Container Apps or Batch |
| Monolithic function (multiple responsibilities in one function) | Poor scaling isolation; cold start bloat | One function per responsibility; shared logic in modules imported by multiple functions |
| Creating clients/connections inside the function body | New connection pool per invocation; port exhaustion | Module-level client initialization (shared across warm invocations) |
| Blob trigger output to same container | Infinite trigger loop; billing exhaustion | Always use separate source and destination containers |
| Verbose logging in production | Measurable performance degradation | Set log level to `Warning` or `Error` in `host.json` for production |
| Function key in query string (`?code=...`) | Key exposed in logs, browser history, telemetry | Always use `x-functions-key` header |
| Shared storage account across multiple Function Apps | Storage transaction contention (critical for Durable Functions) | One dedicated storage account per Function App |
| Test functions in production Function App | Resource contention; unexpected billing | Separate Function Apps for test vs. production |
| Shared secrets in Application Settings plaintext | Secret exposed in portal and deployment logs | Key Vault references or managed identity for all secrets |

---

## 14. Official Resources

| Resource | URL |
|---|---|
| Azure Functions documentation | learn.microsoft.com/azure/azure-functions |
| Python developer guide | learn.microsoft.com/azure/azure-functions/functions-reference-python |
| Core Tools v4 local development | learn.microsoft.com/azure/azure-functions/functions-run-local |
| Best practices | learn.microsoft.com/azure/azure-functions/functions-best-practices |
| Performance and reliability | learn.microsoft.com/azure/azure-functions/performance-reliability |
| Durable Functions patterns | learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview |
| Durable Task Scheduler quickstart (Python) | learn.microsoft.com/azure/durable-task/durable-functions/quickstart-python-vscode |
| Triggers and bindings reference | learn.microsoft.com/azure/azure-functions/functions-triggers-bindings |
| Security concepts | learn.microsoft.com/azure/azure-functions/security-concepts |
| Build 2025 announcements | techcommunity.microsoft.com/blog/appsonazureblog/azure-functions-build-2025/4414655 |

---

## Sources Consulted

- User-provided course material: "Azure Functions Masterclass" (ScholarHat) — source for the
  serverless ecosystem categories, IaaS/PaaS/FaaS comparison table, trigger and bindings deep
  dive, authorization level matrix, key hierarchy diagram, in-portal testing workflow, and the
  Node.js v3 vs v4 programming model comparison; content adapted and corrected against official
  documentation where discrepancies were found.
- Microsoft Learn: Code and test Azure Functions locally
  (learn.microsoft.com/azure/azure-functions/functions-develop-local, fetched September 2026)
  — authoritative source for local.settings.json full schema (IsEncrypted, Values, Host,
  ConnectionStrings sections), AzureWebJobs.<FUNCTION_NAME>.Disabled per-function disable key,
  func settings encrypt/decrypt, HTTP test tool security guidance (Bruno, REST Client, curl,
  Invoke-RestMethod), Azurite integration, manual trigger via admin endpoint, and local
  development environment options (VS, VS Code, Maven, IntelliJ, Eclipse).
- Microsoft Learn: Develop legacy C# class library functions (in-process model)
  (learn.microsoft.com/azure/azure-functions/functions-dotnet-class-library, fetched Sep 2026)
  — source for in-process model retirement date (November 10, 2026), complete .NET version
  support table (isolated worker vs in-process), FunctionName attribute naming rules, ILogger
  structured logging (Console.Write not captured), CancellationToken graceful shutdown pattern,
  ICollector/IAsyncCollector for multiple outputs, binding expressions (%appsetting%), async
  function restrictions (no out params), ReadyToRun compilation, Microsoft.NET.Sdk.Functions
  minimum version 4.5.0, complete triggers and bindings table (21 services), and custom
  TelemetryClient patterns.
- Microsoft Learn: Compare Azure Functions runtime versions
  (learn.microsoft.com/azure/azure-functions/functions-versions, fetched September 2026) —
  authoritative source for complete language version support matrices with end-of-support dates
  (Python 3.10–3.14, Node.js 22/24, Java 8/11/17/21/25, PowerShell 7.4/7.6, Go preview),
  Linux Consumption last-supported versions per language, runtime v1.x end-of-support
  (September 14, 2026), v2.x/v3.x retirement (December 2022), extension bundle minimum
  version requirements (v4.0.0 for Functions 4.x), and FUNCTIONS_EXTENSION_VERSION guidance.
- Microsoft Learn: Azure Functions best practices
  (learn.microsoft.com/azure/azure-functions/functions-best-practices, July 2026) — storage
  account isolation, run-from-package recommendation, function grouping guidance.
- Microsoft Learn: Improve Azure Functions performance and reliability
  (learn.microsoft.com/azure/azure-functions/performance-reliability, July 2026) — source for
  FUNCTIONS_WORKER_PROCESS_COUNT, connection reuse pattern, verbose logging warning, async
  guidance.
- Microsoft Learn: Python developer guide for Azure Functions
  (learn.microsoft.com/azure/azure-functions/functions-reference-python, July 2026) — Python
  v4 programming model, environment variable access patterns.
- Microsoft Learn: Azure Functions Core Tools v4 reference
  (learn.microsoft.com/azure/azure-functions/functions-run-local, July 2026) — func init/new/
  start commands, Python virtual environment requirements.
- Microsoft Learn: Azure Functions CLI v5 (preview)
  (learn.microsoft.com/azure/azure-functions/functions-cli-develop-local, July 2026) — preview
  status and Java/PowerShell gap confirmed.
- Microsoft Learn: Durable Functions Python quickstart
  (learn.microsoft.com/azure/durable-task/durable-functions/quickstart-python-vscode, 2026)
  — Durable Task Scheduler emulator setup.
- Microsoft Learn: Azure Functions security concepts
  (learn.microsoft.com/azure/azure-functions/security-concepts, July 2026) — authorization
  levels, key hierarchy, managed identity at creation.
- Microsoft Build 2025: Azure Functions announcements (May 2025) — managed identity portal
  configuration, GitHub Copilot integration.

**Sections most likely to require re-verification before use:** language version support
tables (new versions added quarterly), Flex Consumption plan limits, CLI v5 feature parity
(Java/PowerShell support pending), in-process model migration deadline (November 10, 2026).
Always verify at learn.microsoft.com/azure/azure-functions before a new production project.
