> Content in this file is grounded in official Microsoft documentation
> (learn.microsoft.com/azure/container-apps, learn.microsoft.com/azure/aks,
> learn.microsoft.com/azure/container-instances — verified September 2026), Microsoft's
> own positioning statement ("when unsure, use Container Apps"), and architectural analysis
> from documented practitioner experience. Decision criteria are sourced from the official
> AKS comparison page. Organization-specific subscription IDs, ACR names, and resource group
> configurations are never stored here.

# Azure Containers: Decision Guide and Platform Reference

## 1. The Five Container Options on Azure

Azure offers five distinct services for running containers or containerized workloads. These
are not alternatives to each other — they solve different problems and are frequently combined
in a single architecture.

| Service | Positioning | Infrastructure management | When it is the right choice |
|---|---|---|---|
| **Azure Container Apps (ACA)** | Managed microservices and event-driven containers | Fully managed (Kubernetes underneath, abstracted away) | General containers, microservices, APIs, background workers, jobs — the default answer when unsure |
| **Azure Functions** | Serverless event-driven code | Fully managed (FaaS) | Short-lived, event-triggered code; no persistent process; see `references/azure-functions.md` |
| **Azure Container Instances (ACI)** | Lightweight one-off containers | Minimal management, no orchestration | Simple, short-lived, ad-hoc, or batch containers where you assemble your own scaling |
| **Azure App Service** | Web app and API hosting (supports containers) | Managed PaaS for web workloads | Traditional web apps and APIs, especially when migrating from IIS/ASP.NET |
| **Azure Kubernetes Service (AKS)** | Full managed Kubernetes | Managed control plane; you manage node pools and workloads | Complex enterprise applications requiring full Kubernetes API access, custom operators, service mesh, or very high scale |

**Microsoft's own positioning from official AKS documentation:** "Many teams prefer to start
building container microservices with Azure Container Apps." Container Apps is the default
answer for new containerized workloads unless a specific constraint requires AKS.

---

## 2. Decision Framework

Work through these filters in order:

**Step 1 — Is this an event-triggered, short-lived function?**
→ Yes: Azure Functions (see `references/azure-functions.md`). Stop here.

**Step 2 — Is this a traditional web app or API with no container-specific requirements?**
→ Yes: Azure App Service. Stop here. App Service is simpler for pure web workloads.

**Step 3 — Is this a simple, one-off, or batch container run with no orchestration needed?**
→ Yes: Azure Container Instances. Fast to deploy, pay-per-second, no overhead.

**Step 4 — Do you need direct access to the Kubernetes API, custom operators, node-level
configuration, Windows workloads, or a service mesh you control?**
→ Yes: Azure Kubernetes Service.

**Step 5 — Everything else (microservices, background workers, event-driven containers,
scheduled jobs, APIs that need autoscaling including scale-to-zero):**
→ Azure Container Apps. This is the default for new containerized workloads.

### Decision Matrix

| Factor | ACA | ACI | AKS |
|---|---|---|---|
| Startup complexity | Low — portal, CLI, or Bicep | Very low | High — cluster provisioning, node pools |
| Kubernetes API access | No (abstracted) | No | Yes (full) |
| Autoscaling | Yes (HTTP, CPU, custom KEDA scalers, scale-to-zero) | No native autoscale | Yes (HPA, KEDA, cluster autoscaler) |
| Scale-to-zero | Yes | N/A (containers stopped manually) | Yes with KEDA |
| Persistent state | Limited (volumes via Azure Files/NFS) | Limited (volumes) | Full (StatefulSets, persistent volumes) |
| Cost model | Consumption (pay per use) or Dedicated | Per-second per container | Per node-hour (always on) |
| Windows containers | No | Yes | Yes |
| Dapr built-in | Yes | No | Yes (self-managed) |
| Long-running processes | Yes | Yes | Yes |
| Scheduled jobs | Yes (Container Apps Jobs) | Yes (with logic app / ADF trigger) | Yes (Kubernetes CronJob) |
| VNet integration | Yes | Yes | Yes (more granular) |
| Managed identity | Yes (system + user assigned) | Yes | Yes |
| Team Kubernetes expertise required | No | No | Yes |
| Right for a team of 2–5 engineers | Yes | Yes | Usually not |

**ACI vs ACA in practice:** ACI has no built-in load balancer, no autoscaling, and no service
orchestration. If you need any of those, choose ACA. ACI is the right tool for: running a
container-based data processing job triggered by ADF or Logic Apps, a one-shot migration
script, or a development/test environment that needs a real container runtime without
infrastructure overhead.

**ACA vs AKS migration path:** Start in ACA. Move to AKS only when a concrete constraint
requires it — typically: custom Kubernetes operators, Windows workload, sustained average
CPU/memory utilization above 40% (where AKS reserved instances become cheaper than ACA
consumption billing), or a requirement for service mesh control (Istio, Linkerd).

---

## 3. Azure Container Apps — Deep Reference

### Core Concepts

**Environment:** The isolation boundary for a group of Container Apps. Apps in the same
environment share a VNet, log analytics workspace, and internal service discovery. Apps in
different environments are fully isolated. Use separate environments for: production vs.
staging, customer tenants requiring full resource isolation, different VNet configurations.

**Container App:** The deployable unit. Each app has one or more containers (typically one
per microservice — running multiple containers in one app is the sidecar pattern, not a
general practice). Each app has an ingress configuration, scaling rules, secrets, and
environment variables.

**Revision:** A versioned snapshot of a Container App configuration. New revisions are
created when container image, environment variables, scaling rules, or resource limits change.
Traffic can be split between revisions (for blue/green or canary deployments). Use
`--revision-suffix` on `az containerapp update` to name revisions.

**Job:** A Container App that runs to completion (not continuously). Supports three trigger
types: Manual, Scheduled (cron), Event-driven (KEDA-based, e.g., trigger on queue depth).
Use Jobs for: ETL runs, report generation, data export — anything that starts, processes, and
stops. Jobs replace the need for ACI + ADF trigger for many scenarios.

### Scaling

Container Apps uses **KEDA** (Kubernetes Event-Driven Autoscaling) for all scaling decisions.
Scaling rules can target:

- **HTTP concurrency** — number of concurrent requests per instance
- **CPU and memory** utilization percentages
- **Azure Queue / Service Bus** — scale based on message count (directly relevant for RPA bot
  output processing)
- **Custom KEDA scalers** — Kafka, Redis, Prometheus, and many others
- **Scale to zero** — supported for both HTTP and event-driven triggers (not for CPU/memory
  triggers, which require a minimum of 1 replica)

```yaml
# Container App scaling rule — scale on Service Bus queue depth
scale:
  minReplicas: 0
  maxReplicas: 10
  rules:
    - name: service-bus-queue-rule
      custom:
        type: azure-servicebus
        metadata:
          queueName: rpa-output-queue
          namespace: my-servicebus-namespace
          messageCount: "5"   # scale up one replica per 5 messages
        auth:
          - secretRef: sb-connection-string
            triggerParameter: connection
```

### Container Registry Integration

Always use **Azure Container Registry (ACR)** for production images. Never use Docker Hub
for production — rate limits and reliability SLAs are unsuitable for production workloads.

```bash
# Create ACR and build + push an image
az acr create --name myregistry --resource-group myRG --sku Basic
az acr build --registry myregistry --image myapp:latest .

# Deploy Container App pulling from ACR using managed identity (no credentials)
az containerapp create \
  --name my-app \
  --resource-group myRG \
  --environment my-env \
  --image myregistry.azurecr.io/myapp:1.2.3 \
  --registry-server myregistry.azurecr.io \
  --registry-identity system
```

**Never use `latest` or other mutable tags in production.** Use semantic versions or Git
commit SHAs (e.g., `myapp:1.2.3` or `myapp:abc1234`). Mutable tags make rollbacks
unreliable and break deployment reproducibility.

### Secrets and Configuration

```bash
# Store a secret in the Container App (encrypted at rest; never in image or env directly)
az containerapp secret set \
  --name my-app \
  --resource-group myRG \
  --secrets "db-password=<value>"

# Reference the secret in an environment variable
az containerapp update \
  --name my-app \
  --resource-group myRG \
  --set-env-vars "DB_PASSWORD=secretref:db-password"
```

For production, prefer **Key Vault references** over storing secrets directly in Container
Apps. The Container App's managed identity needs `Key Vault Secrets User` role on the vault.

```bash
# Reference a Key Vault secret directly
az containerapp secret set \
  --name my-app \
  --resource-group myRG \
  --secrets "db-password=keyvaultref:https://myvault.vault.azure.net/secrets/db-password,identityref:system"
```

### Ingress

```bash
# External ingress (public HTTPS endpoint)
az containerapp ingress enable \
  --name my-app \
  --resource-group myRG \
  --type external \
  --target-port 8000 \
  --transport http

# Internal ingress (accessible only within the environment)
az containerapp ingress enable \
  --name my-app \
  --resource-group myRG \
  --type internal \
  --target-port 8000
```

Container Apps automatically provisions TLS/HTTPS for external ingress using a managed
certificate. Custom domains are supported with `az containerapp hostname add`.

### Container Apps Jobs (Scheduled and Event-Driven)

```bash
# Scheduled job (cron — 6-field Azure format matching Functions)
az containerapp job create \
  --name nightly-report \
  --resource-group myRG \
  --environment my-env \
  --trigger-type Schedule \
  --cron-expression "0 0 2 * * *" \
  --image myregistry.azurecr.io/report-generator:1.0.0 \
  --cpu 1 --memory 2Gi

# Event-driven job (triggers when Service Bus queue depth >= 10)
az containerapp job create \
  --name process-queue \
  --resource-group myRG \
  --environment my-env \
  --trigger-type Event \
  --image myregistry.azurecr.io/queue-processor:1.0.0 \
  --min-executions 0 \
  --max-executions 20 \
  --scale-rule-name sb-rule \
  --scale-rule-type azure-servicebus \
  --scale-rule-metadata "queueName=my-queue" "namespace=my-namespace" "messageCount=10"
```

### Dapr Integration

Container Apps has built-in Dapr support. Enabling Dapr on a Container App injects a Dapr
sidecar that provides: service invocation (service-to-service HTTP/gRPC with retries),
pub/sub messaging (abstracted over Service Bus, Event Hubs, Redis), state management, secrets,
and distributed tracing.

```bash
az containerapp dapr enable \
  --name my-app \
  --resource-group myRG \
  --dapr-app-id my-app \
  --dapr-app-port 8000
```

Dapr is useful for RPA-to-microservice integration: a bot can publish a message to a Dapr
pub/sub topic, and multiple subscriber Container Apps receive it independently, without the
bot knowing about any of them.

### Health Probes

Always configure health probes for production Container Apps. Without them, traffic is routed
to containers that have not finished starting up (liveness failures are silent).

```yaml
probes:
  - type: liveness
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 10
    periodSeconds: 30
  - type: readiness
    httpGet:
      path: /ready
      port: 8000
    initialDelaySeconds: 5
    periodSeconds: 10
  - type: startup
    httpGet:
      path: /started
      port: 8000
    failureThreshold: 30
    periodSeconds: 10
```

---

## 4. Azure Container Instances — Reference

ACI is the lowest-overhead way to run a container in Azure. No cluster, no environment, no
orchestration. A container group starts within seconds and bills per second per resource unit.

```bash
# Run a one-off container (e.g., a database migration, a data export script)
az container create \
  --resource-group myRG \
  --name migration-job \
  --image myregistry.azurecr.io/migrator:1.0.0 \
  --registry-login-server myregistry.azurecr.io \
  --registry-username $(az acr credential show -n myregistry --query username -o tsv) \
  --registry-password $(az acr credential show -n myregistry --query passwords[0].value -o tsv) \
  --restart-policy Never \
  --environment-variables "DB_HOST=mydb.database.windows.net" \
  --secure-environment-variables "DB_PASSWORD=mysecret" \
  --cpu 1 --memory 1.5

# Check output and status
az container logs --resource-group myRG --name migration-job
az container show --resource-group myRG --name migration-job --query instanceView.state
```

**ACI limitations to know before choosing it:**
- IP address is not static — changes if the container group is recreated. Use Application
  Gateway or a DNS name if a stable address is needed.
- No built-in autoscaling or load balancing. If you need either, use ACA or AKS.
- Maximum of 4 CPU cores and 16 GiB RAM per container group.
- No Windows Server 2022 — Windows containers support is limited to specific versions.

---

## 5. Azure Kubernetes Service — When You Actually Need It

AKS is the right choice when a specific, concrete requirement cannot be met by ACA:

- **Full Kubernetes API access** — custom operators (CRDs), custom admission webhooks,
  cluster-level RBAC policies, custom schedulers.
- **Windows container workloads** that ACA does not support.
- **Sustained high utilization** (>40% average CPU/memory) where AKS node pool reserved
  instances become materially cheaper than ACA consumption pricing.
- **Existing Kubernetes tooling** (Helm charts, Kustomize, Flux/ArgoCD GitOps) that the team
  already manages and wants to reuse.
- **Complex networking** — custom CNI plugins, specific network policy implementations, BGP
  peering.

If none of these apply, the operational overhead of AKS (node pool management, upgrades,
security patching, monitoring complexity) is not justified. The official Microsoft documentation
explicitly states: "If you require access to the Kubernetes APIs and control plane, you should
use AKS. However, if you would like to build Kubernetes-style applications and don't require
direct access to all the native Kubernetes APIs and cluster management, Container Apps provides
a fully managed experience based on best-practices."

**AKS Automatic** (GA as of 2025): A managed AKS mode where Microsoft manages node pool
upgrades, security patching, and scaling configurations. Reduces operational overhead
significantly while retaining full Kubernetes API access. Appropriate for teams that need
AKS capabilities but lack a dedicated platform engineering team.

---

## 6. Security Best Practices (All Container Services)

**Managed identity over credentials everywhere.** ACR pull, Key Vault access, Storage
access, Service Bus access — all should use managed identity, not connection strings or
service principal credentials stored in environment variables or secrets.

**Never use mutable image tags in production.** `latest`, `stable`, `main` are mutable —
they can point to a different image after a push. Use semantic versions or commit SHAs.

**System-assigned vs. user-assigned managed identity:**
- System-assigned: tied to the resource lifecycle; deleted with the container app. Use for
  resources with a single identity requirement.
- User-assigned: independent lifecycle; shared across multiple resources. Use when multiple
  container apps access the same Key Vault or storage account.

**Network isolation:** For production, deploy Container Apps environments with VNet injection
(`--infrastructure-subnet-resource-id`) to prevent public internet exposure of the environment
itself. Use internal ingress for services that only need to be called by other services in the
same environment.

**Image scanning:** Enable **Microsoft Defender for Containers** on ACR to scan images for
vulnerabilities at push time. Block deployment of images with critical CVEs via ACR policies.

---

## 7. CI/CD with Azure DevOps

```yaml
# azure-pipelines.yml — build, push to ACR, deploy to Container Apps
trigger:
  branches:
    include: [main]

variables:
  acrName: myregistry
  imageTag: $(Build.BuildId)

stages:
- stage: BuildAndPush
  jobs:
  - job: Docker
    pool:
      vmImage: ubuntu-latest
    steps:
    - task: AzureCLI@2
      inputs:
        azureSubscription: $(AzureServiceConnection)
        scriptType: bash
        script: |
          az acr login --name $(acrName)
          docker build -t $(acrName).azurecr.io/myapp:$(imageTag) .
          docker push $(acrName).azurecr.io/myapp:$(imageTag)

- stage: Deploy
  dependsOn: BuildAndPush
  jobs:
  - deployment: ContainerApp
    environment: production
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: $(AzureServiceConnection)
              scriptType: bash
              script: |
                az containerapp update \
                  --name my-app \
                  --resource-group myRG \
                  --image $(acrName).azurecr.io/myapp:$(imageTag)
```

---

## Sources Consulted

- Microsoft Learn: Comparing AKS with other Azure container options
  (learn.microsoft.com/azure/aks/compare-container-options-with-aks, September 2026) —
  official Microsoft positioning of ACA vs AKS vs ACI; source for "many teams prefer to start
  with Container Apps" and the Kubernetes API access decision criterion.
- Microsoft Learn: Containers in Azure Container Apps
  (learn.microsoft.com/azure/container-apps/containers, September 2026) — sidecar vs separate
  app pattern, container configuration schema, health probe fields, mutable tag warning.
- Microsoft Learn: Security overview for Azure Container Apps
  (learn.microsoft.com/azure/container-apps/security, September 2026) — managed identity
  selection (system vs user assigned), Key Vault integration, secrets management best practices.
- Microsoft Learn: Azure Container Instances best practices
  (learn.microsoft.com/azure/container-instances/container-instances-best-practices-and-
  considerations, September 2026) — IP address instability, static IP with Application Gateway,
  multi-region guidance.
- Microsoft Learn: Container architecture design guidance
  (learn.microsoft.com/azure/architecture/containers/container-get-started, September 2026)
  — autoscaling best practices, Container Apps operations, monitoring guidance.
- Practitioner analysis: ACA vs AKS decision framework (developersvoice.com, 2026) — the
  40% utilization threshold for AKS reserved instance cost comparison, engineering team size
  heuristic, AKS Automatic positioning. This is practitioner analysis, not official Microsoft
  documentation; use as directional guidance and verify cost calculations with the Azure
  Pricing Calculator for your specific workload.
- Official AKS comparison (tomodahinata.com/blog, June 2026) — five-option decision flow
  incorporating official Microsoft positioning statements.

The Container Apps features table (Dapr, Jobs, scaling rules) and AKS Automatic GA status
are the sections most likely to change. Verify current feature availability at
learn.microsoft.com/azure/container-apps before production project scoping.
