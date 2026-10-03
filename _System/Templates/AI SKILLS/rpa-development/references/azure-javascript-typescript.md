> Content grounded in official Microsoft documentation: Azure SDK for JavaScript usage guide
> (learn.microsoft.com/azure/developer/javascript/how-to/common-javascript-tasks), Azure
> Identity JavaScript library README v4.13.3 (learn.microsoft.com/javascript/api/overview/
> azure/identity-readme), Azure Identity authentication best practices for JavaScript
> (learn.microsoft.com/azure/developer/javascript/sdk/authentication/best-practices),
> What is Azure for JavaScript development (learn.microsoft.com/azure/developer/javascript/
> what-is-azure-for-javascript-development) — all verified September 2026. Code examples
> are TypeScript-first; plain JavaScript equivalents remove type annotations.

# Azure JavaScript and TypeScript: SDK Development Reference

## 1. Scope and Positioning

This file covers **TypeScript/JavaScript development targeting Azure services** — authentication,
SDK client setup, service-specific patterns, and production practices. It does not cover
general TypeScript or JavaScript language practices; it covers Azure-specific usage only.

The Azure SDK for JavaScript is **written in TypeScript** and ships native type definitions
(`*.d.ts`) for every package. You do not need TypeScript to use the SDK, but TypeScript is
strongly recommended — the type definitions surface configuration errors at compile time
rather than at runtime.

**Runtime support:**
- Node.js LTS versions (22, 24 as of September 2026) — the primary supported runtime.
- Bun and Deno — experimental; Azure SDK support is not guaranteed. Do not use in production.
- Browser — many Azure SDK packages can be bundled for browser use, but connection string
  and managed identity patterns do not apply. Use SAS tokens or your own backend proxy for
  browser-to-Azure storage access.

---

## 2. Project Setup

### TypeScript Configuration

```json
// tsconfig.json — Azure TypeScript project baseline
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Package Structure

```bash
npm install @azure/identity                # DefaultAzureCredential — always install
npm install @azure/storage-blob           # Blob Storage
npm install @azure/storage-queue          # Queue Storage
npm install @azure/service-bus            # Service Bus
npm install @azure/keyvault-secrets       # Key Vault secrets
npm install @azure/cosmos                 # Cosmos DB NoSQL API
npm install @azure/app-configuration      # App Configuration (feature flags)
npm install @azure/monitor-opentelemetry  # Application Insights / Azure Monitor
npm install @azure/functions              # Azure Functions v4 TypeScript model
```

All Azure SDK packages follow the `@azure/` npm scope and are modular — install only what
you use.

---

## 3. Authentication: DefaultAzureCredential

The `DefaultAzureCredential` pattern in JavaScript/TypeScript is identical in intent to
Python and C#, but has an important production caveat documented in official Microsoft
guidance that Python and C# documentation does not emphasize as strongly.

```typescript
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();
// Pass to any @azure/* client as the second constructor argument
```

### Credential Chain (JavaScript)

`DefaultAzureCredential` tries credentials in this order:

1. `EnvironmentCredential` — `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`
2. `WorkloadIdentityCredential` — Azure Kubernetes Service with federated identity
3. `ManagedIdentityCredential` — Azure Functions, Container Apps, VMs
4. `SharedTokenCacheCredential` — shared token cache from VS/VS Code
5. `VisualStudioCodeCredential` — VS Code "Azure Account" extension sign-in
6. `AzureCliCredential` — `az login` (local development default)
7. `AzurePowerShellCredential` — `Connect-AzAccount`
8. `AzureDeveloperCliCredential` — `azd auth login`

### Production Caveat: Silent Fallthrough Risk

**This is the most important warning in this file, sourced from the official Microsoft
authentication best practices guide.**

`DefaultAzureCredential` silently skips failed credentials and tries the next one. In
production, this can cause a dangerous scenario:

A JavaScript app on an Azure VM successfully authenticates via managed identity
(`ManagedIdentityCredential`) for months. If managed identity is misconfigured during a
deployment (wrong identity attached, or identity removed), `DefaultAzureCredential` does not
throw immediately — it silently falls through to `AzureCliCredential`. If a developer's
`az login` credentials happen to be cached on the same VM (common in development VMs
reused as production), the app silently authenticates with the developer's personal
credentials instead of the managed identity. This is both a security issue (wrong identity)
and a reliability issue (developer token expires and breaks production at an unpredictable time).

**Mitigation — use `ManagedIdentityCredential` directly in production:**

```typescript
import {
    DefaultAzureCredential,
    ManagedIdentityCredential
} from "@azure/identity";

// Production: explicit managed identity — fails fast if not configured correctly
const isProduction = process.env.NODE_ENV === "production";
const credential = isProduction
    ? new ManagedIdentityCredential(process.env.AZURE_CLIENT_ID)  // user-assigned identity
    : new DefaultAzureCredential();                                // local dev fallthrough ok
```

For local development, `DefaultAzureCredential` remains correct — the fallthrough to
`AzureCliCredential` is the intended behaviour. Only in deployed environments should you
switch to an explicit credential type.

---

## 4. Azure SDK Client Patterns

### Singleton Pattern

All Azure SDK clients are expensive to construct (connection pool setup, DNS resolution,
TLS handshakes). Instantiate once per application lifetime:

```typescript
// clients.ts — singleton module, imported by all other modules
import { DefaultAzureCredential, ManagedIdentityCredential } from "@azure/identity";
import { BlobServiceClient } from "@azure/storage-blob";
import { ServiceBusClient } from "@azure/service-bus";
import { SecretClient } from "@azure/keyvault-secrets";
import { CosmosClient } from "@azure/cosmos";

const credential = process.env.NODE_ENV === "production"
    ? new ManagedIdentityCredential(process.env.AZURE_CLIENT_ID!)
    : new DefaultAzureCredential();

export const blobServiceClient = new BlobServiceClient(
    `https://${process.env.STORAGE_ACCOUNT_NAME}.blob.core.windows.net`,
    credential
);

export const serviceBusClient = new ServiceBusClient(
    `${process.env.SERVICEBUS_NAMESPACE}.servicebus.windows.net`,
    credential
);

export const secretClient = new SecretClient(
    `https://${process.env.KEY_VAULT_NAME}.vault.azure.net`,
    credential
);

export const cosmosClient = new CosmosClient({
    endpoint: process.env.COSMOS_ENDPOINT!,
    aadCredentials: credential
});
```

### Paging with `for await...of`

Azure SDK operations that return multiple items implement the `PagedAsyncIterableIterator`
interface, which supports `for await...of` directly:

```typescript
import { BlobServiceClient } from "@azure/storage-blob";
import { blobServiceClient } from "./clients";

// Iterate all blobs — SDK handles pagination transparently
async function listInvoices(containerName: string): Promise<string[]> {
    const container = blobServiceClient.getContainerClient(containerName);
    const names: string[] = [];

    for await (const blob of container.listBlobsFlat({ prefix: "2025/jan/" })) {
        names.push(blob.name);
    }
    return names;
}

// Access pages explicitly when you need page-level metadata or continuation tokens
async function listByPage(containerName: string): Promise<void> {
    const container = blobServiceClient.getContainerClient(containerName);
    for await (const page of container.listBlobsFlat().byPage({ maxPageSize: 50 })) {
        for (const blob of page.segment.blobItems) {
            console.log(blob.name, blob.properties.contentLength);
        }
    }
}
```

### Long Running Operations (LRO)

Some Azure operations are asynchronous at the service level (container delete, blob copy,
database create). The SDK returns a **poller** — use `pollUntilDone()` to await completion:

```typescript
import { ContainerClient } from "@azure/storage-blob";

async function copyBlob(
    source: ContainerClient,
    dest: ContainerClient,
    blobName: string
): Promise<void> {
    const sourceBlob = source.getBlobClient(blobName);
    const destBlob = dest.getBlobClient(blobName);

    // Returns immediately with a poller; operation runs on the service side
    const copyPoller = await destBlob.beginCopyFromURL(sourceBlob.url);

    // Block until the copy completes (or throws if it fails)
    const result = await copyPoller.pollUntilDone();
    console.log(`Copy completed: ${result.copyStatus}`);
}
```

### Cancellation with AbortController

```typescript
import { blobServiceClient } from "./clients";

async function downloadWithTimeout(containerName: string, blobName: string): Promise<Buffer> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30_000); // 30s timeout

    try {
        const blob = blobServiceClient
            .getContainerClient(containerName)
            .getBlobClient(blobName);

        const response = await blob.download(0, undefined, {
            abortSignal: controller.signal
        });

        const chunks: Buffer[] = [];
        for await (const chunk of response.readableStreamBody!) {
            chunks.push(Buffer.from(chunk));
        }
        return Buffer.concat(chunks);
    } finally {
        clearTimeout(timeoutId);
    }
}
```

### Error Handling

```typescript
import { RestError } from "@azure/core-rest-pipeline";

try {
    const blob = containerClient.getBlobClient("missing.pdf");
    await blob.download();
} catch (error) {
    if (error instanceof RestError) {
        if (error.statusCode === 404) {
            // Resource not found — handle as expected case
            console.log("Blob not found");
        } else if (error.statusCode === 429) {
            // Rate limited — SDK retries automatically; if still thrown, retries exhausted
            throw error;
        } else if (error.statusCode === 403) {
            // Authorization failure — check RBAC role assignment and managed identity config
            throw new Error(`Auth failed: check RBAC on ${error.request?.url}`);
        } else {
            throw error;
        }
    } else {
        throw error;
    }
}
```

---

## 5. Azure Blob Storage (TypeScript)

```typescript
import {
    BlobServiceClient,
    BlockBlobUploadOptions,
    StorageSharedKeyCredential
} from "@azure/storage-blob";
import { blobServiceClient } from "./clients";

async function uploadBuffer(
    containerName: string,
    blobName: string,
    data: Buffer,
    contentType: string
): Promise<void> {
    const container = blobServiceClient.getContainerClient(containerName);
    const blob = container.getBlockBlobClient(blobName);

    const options: BlockBlobUploadOptions = {
        blobHTTPHeaders: { blobContentType: contentType },
        metadata: { uploadedBy: "rpa-bot", timestamp: new Date().toISOString() }
    };

    await blob.upload(data, data.length, options);
}

async function downloadToString(containerName: string, blobName: string): Promise<string> {
    const blob = blobServiceClient
        .getContainerClient(containerName)
        .getBlobClient(blobName);

    const response = await blob.download();
    const chunks: Buffer[] = [];
    for await (const chunk of response.readableStreamBody!) {
        chunks.push(Buffer.from(chunk));
    }
    return Buffer.concat(chunks).toString("utf-8");
}
```

---

## 6. Azure Service Bus (TypeScript)

```typescript
import { ServiceBusClient, ServiceBusMessage } from "@azure/service-bus";
import { serviceBusClient } from "./clients";

// Send a message
async function sendTransaction(queueName: string, payload: object): Promise<void> {
    const sender = serviceBusClient.createSender(queueName);
    try {
        await sender.sendMessages({
            body: JSON.stringify(payload),
            contentType: "application/json",
            messageId: crypto.randomUUID()     // idempotency key
        });
    } finally {
        await sender.close();
    }
}

// Process messages (pull-based, manual completion)
async function processQueue(queueName: string): Promise<void> {
    const receiver = serviceBusClient.createReceiver(queueName, {
        receiveMode: "peekLock"    // message invisible but not deleted until settled
    });

    try {
        const messages = await receiver.receiveMessages(10, { maxWaitTimeInMs: 5_000 });
        for (const message of messages) {
            try {
                await processMessage(message.body);
                await receiver.completeMessage(message);     // acknowledge success
            } catch (err) {
                // Business error: dead-letter the message (will not be retried)
                await receiver.deadLetterMessage(message, {
                    deadLetterReason: "BusinessRuleViolation",
                    deadLetterErrorDescription: String(err)
                });
            }
        }
    } finally {
        await receiver.close();
    }
}

// Subscribe (push-based — preferred for Azure Functions)
async function subscribe(queueName: string): Promise<void> {
    const receiver = serviceBusClient.createReceiver(queueName);
    receiver.subscribe({
        processMessage: async (message) => {
            await processMessage(message.body);
        },
        processError: async (error) => {
            console.error("Service Bus error:", error.error);
        }
    });
    // Keep alive until process exits; call receiver.close() to stop
}
```

---

## 7. Azure Key Vault Secrets (TypeScript)

```typescript
import { SecretClient } from "@azure/keyvault-secrets";
import { secretClient } from "./clients";

// Fetch a secret (call at application startup; cache in memory)
async function loadSecrets(): Promise<Record<string, string>> {
    const [dbPassword, apiKey] = await Promise.all([
        secretClient.getSecret("DatabasePassword"),
        secretClient.getSecret("ExternalApiKey")
    ]);
    return {
        dbPassword: dbPassword.value!,
        apiKey: apiKey.value!
    };
}

// List all secrets in the vault (useful for bulk loading)
async function listSecretNames(): Promise<string[]> {
    const names: string[] = [];
    for await (const secret of secretClient.listPropertiesOfSecrets()) {
        if (secret.enabled) names.push(secret.name);
    }
    return names;
}
```

---

## 8. Cosmos DB (TypeScript)

```typescript
import { CosmosClient, PartitionKey } from "@azure/cosmos";
import { cosmosClient } from "./clients";

const db = cosmosClient.database("InvoiceDB");
const container = db.container("Invoices");

// Point read (cheapest: 1 RU per 1 KB)
async function getInvoice(id: string, vendorId: string) {
    const { resource } = await container.item(id, vendorId).read();
    return resource;   // undefined if not found (no exception thrown)
}

// Upsert
async function saveInvoice(invoice: Invoice): Promise<void> {
    await container.items.upsert(invoice);
}

// Query with paging
async function* queryPending(vendorId: string): AsyncGenerator<Invoice> {
    const { resources } = await container.items.query<Invoice>(
        {
            query: "SELECT * FROM c WHERE c.vendorId = @v AND c.status = 'pending'",
            parameters: [{ name: "@v", value: vendorId }]
        },
        { partitionKey: vendorId }
    ).fetchAll();

    for (const item of resources) yield item;
}
```

---

## 9. Azure Functions v4 TypeScript Model

See `references/azure-functions.md` Section 5 for the full v4 TypeScript model. Quick
reference for the most common pattern:

```typescript
// function_app.ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { DefaultAzureCredential, ManagedIdentityCredential } from "@azure/identity";
import { BlobServiceClient } from "@azure/storage-blob";

// Singleton clients at module level (shared across warm invocations)
const credential = process.env.NODE_ENV === "production"
    ? new ManagedIdentityCredential(process.env.AZURE_CLIENT_ID!)
    : new DefaultAzureCredential();

const blobClient = new BlobServiceClient(
    `https://${process.env.STORAGE_ACCOUNT_NAME}.blob.core.windows.net`,
    credential
);

// HTTP trigger
export async function processInvoice(
    request: HttpRequest,
    context: InvocationContext
): Promise<HttpResponseInit> {
    context.log(`Processing: ${request.url}`);
    const body = await request.json() as { invoiceId: string; vendorId: string };

    // ... business logic using blobClient ...

    return { status: 200, jsonBody: { result: "processed" } };
}

app.http("ProcessInvoice", {
    methods: ["POST"],
    authLevel: "function",
    handler: processInvoice
});

// Service Bus trigger
export async function processQueue(
    message: unknown,
    context: InvocationContext
): Promise<void> {
    context.log("Service Bus message received:", message);
    // ... process message ...
}

app.serviceBusQueue("ProcessQueue", {
    queueName: process.env.SB_QUEUE_NAME!,
    connection: "AzureServiceBusConnection",
    handler: processQueue
});
```

---

## 10. Testing Azure SDK Code (TypeScript)

### Unit Tests: Mocking with Jest/Vitest

```typescript
// tests/invoice.test.ts
import { vi, describe, it, expect, beforeEach } from "vitest";
import { BlobServiceClient, ContainerClient, BlobClient } from "@azure/storage-blob";

// Mock the Azure SDK module entirely
vi.mock("@azure/storage-blob");

describe("InvoiceService", () => {
    let mockContainer: Partial<ContainerClient>;
    let mockBlob: Partial<BlobClient>;

    beforeEach(() => {
        mockBlob = {
            download: vi.fn().mockResolvedValue({
                readableStreamBody: (async function* () { yield Buffer.from("invoice data"); })()
            }),
            exists: vi.fn().mockResolvedValue(true)
        };

        mockContainer = {
            getBlobClient: vi.fn().mockReturnValue(mockBlob)
        };

        vi.mocked(BlobServiceClient).mockImplementation(() => ({
            getContainerClient: vi.fn().mockReturnValue(mockContainer)
        } as unknown as BlobServiceClient));
    });

    it("downloads invoice content", async () => {
        const service = new InvoiceService(new BlobServiceClient("https://fake.blob.core.windows.net"));
        const content = await service.getInvoice("invoices", "INV-001");
        expect(content).toBe("invoice data");
        expect(mockContainer.getBlobClient).toHaveBeenCalledWith("INV-001");
    });

    it("returns null when invoice not found", async () => {
        (mockBlob.exists as ReturnType<typeof vi.fn>).mockResolvedValue(false);
        const service = new InvoiceService(new BlobServiceClient("https://fake.blob.core.windows.net"));
        const content = await service.getInvoice("invoices", "MISSING");
        expect(content).toBeNull();
    });
});
```

### Integration Tests

```typescript
// tests/integration/blob.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { BlobServiceClient, ContainerClient } from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity";

const SKIP = !process.env.AZURE_STORAGE_ACCOUNT_NAME;

describe.skipIf(SKIP)("Blob Storage integration", () => {
    let container: ContainerClient;

    beforeAll(async () => {
        const client = new BlobServiceClient(
            `https://${process.env.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net`,
            new DefaultAzureCredential()
        );
        container = client.getContainerClient("test-integration");
        await container.createIfNotExists();
    });

    afterAll(async () => {
        await container.delete();
    });

    it("uploads and downloads a blob", async () => {
        const blob = container.getBlockBlobClient("test.txt");
        await blob.upload(Buffer.from("hello azure"), 11);
        const response = await blob.download();
        const chunks: Buffer[] = [];
        for await (const chunk of response.readableStreamBody!) {
            chunks.push(Buffer.from(chunk));
        }
        expect(Buffer.concat(chunks).toString()).toBe("hello azure");
    });
});
```

---

## 11. Configuration Pattern

```typescript
// src/config.ts
import { z } from "zod";   // npm install zod — schema validation at startup

const envSchema = z.object({
    NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
    STORAGE_ACCOUNT_NAME: z.string().min(3),
    SERVICEBUS_NAMESPACE: z.string(),
    KEY_VAULT_NAME: z.string().optional(),
    COSMOS_ENDPOINT: z.string().url(),
    AZURE_CLIENT_ID: z.string().uuid().optional(),   // user-assigned managed identity
    SB_QUEUE_NAME: z.string().default("rpa-tasks"),
    PROCESSING_BATCH_SIZE: z.coerce.number().int().min(1).default(50),
});

export const config = envSchema.parse(process.env);
// Throws at startup if any required variable is missing — no silent undefined access
```

---

## Sources Consulted

- Microsoft Learn: Use Azure SDK for JavaScript and TypeScript
  (learn.microsoft.com/azure/developer/javascript/how-to/common-javascript-tasks,
  September 2026) — paging with `for await...of`, LRO poller pattern, AbortController,
  `@azure/` npm scope overview, SDK package index reference.
- Microsoft Learn: Azure Identity library for JavaScript README v4.13.3
  (learn.microsoft.com/javascript/api/overview/azure/identity-readme, September 2026) —
  `DefaultAzureCredential` chain order, VS Code credential, Broker authentication,
  `useIdentityPlugin` pattern, code examples for all credential types.
- Microsoft Learn: Authentication best practices with Azure Identity for JavaScript
  (learn.microsoft.com/azure/developer/javascript/sdk/authentication/best-practices,
  September 2026) — the silent fallthrough production risk of `DefaultAzureCredential` on
  VMs; the recommendation to use `ManagedIdentityCredential` explicitly in production
  deployments; Express.js example illustrating the risk scenario.
- Microsoft Learn: What is Azure for JavaScript development
  (learn.microsoft.com/azure/developer/javascript/what-is-azure-for-javascript-development,
  September 2026) — supported frameworks, Deno/Bun experimental status, TypeScript-first
  SDK design, Node.js LTS version policy.
- Microsoft Learn: Use Azure client libraries for JavaScript and TypeScript
  (learn.microsoft.com/azure/developer/javascript/sdk/use-azure-sdk, September 2026) —
  client construction pattern, `ResourceManagementClient` example with `DefaultAzureCredential`.
- Official `@azure/storage-blob`, `@azure/service-bus`, `@azure/cosmos`, `@azure/keyvault-secrets`
  npm package READMEs (npmjs.com, September 2026) — TypeScript method signatures, options
  types, and async iterator patterns.

The `DefaultAzureCredential` silent-fallthrough production risk (Section 3) and the Node.js
v4 Functions model (cross-referenced to azure-functions.md) are the sections most likely to
require re-verification. The Zod configuration pattern is a practitioner recommendation, not
an official Microsoft standard; verify alignment with your team's tooling choices.
