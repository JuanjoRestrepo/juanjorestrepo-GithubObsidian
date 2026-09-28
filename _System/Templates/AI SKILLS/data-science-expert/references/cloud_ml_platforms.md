# Cloud ML Platforms — Azure, AWS, and GCP

> **References**: Microsoft Azure Machine Learning Documentation.
> https://learn.microsoft.com/en-us/azure/machine-learning · AWS SageMaker Developer
> Guide. https://docs.aws.amazon.com/sagemaker · Google Vertex AI Documentation.
> https://cloud.google.com/vertex-ai/docs · Kleppmann, M. (2017). *Designing Data-
> Intensive Applications*. O'Reilly. · Google (2020). *Practitioners Guide to MLOps*.
> https://cloud.google.com/resources/mlops-whitepaper · Microsoft (2024). *Azure ML
> Best Practices*. https://learn.microsoft.com/en-us/azure/machine-learning/best-practices-overview

## Table of Contents

1. [Cloud ML Platform Comparison](#comparison)
2. [Azure Machine Learning — Full Reference](#azure-ml)
3. [AWS SageMaker — Full Reference](#sagemaker)
4. [Google Vertex AI — Full Reference](#vertex-ai)
5. [Cloud Storage for ML — ADLS, S3, GCS](#cloud-storage)
6. [Cloud ML Security — Identity and Access](#security)
7. [Cloud ML Cost Management](#cost)
8. [Multi-Cloud ML Architecture Patterns](#patterns)
9. [References](#references)

---

## 1. Cloud ML Platform Comparison {#comparison}

```
CLOUD ML PLATFORM DECISION MAP
────────────────────────────────────────────────────────────────────────────────

Primary cloud is Azure / Microsoft stack?
  YES → Azure Machine Learning (AML)
        Deep integration with Azure DevOps, Azure Data Factory, Synapse,
        Power BI, and Microsoft Entra ID. Native MLOps via AML Pipelines.

Primary cloud is AWS?
  YES → AWS SageMaker
        Tightest integration with S3, Glue, Redshift, Lambda, Step Functions.
        Most mature managed training infrastructure (SageMaker Training Jobs).

Primary cloud is GCP / heavy BigQuery usage?
  YES → Google Vertex AI
        Native BigQuery ML integration. Best-in-class AutoML.
        TPU access for large-scale deep learning.

Using Databricks (any cloud)?
  → Databricks MLflow (managed) + Unity Catalog
    See data_engineering_advanced.md §4 for Databricks reference.
    Databricks runs on Azure, AWS, or GCP — cloud-agnostic ML layer.

Multi-cloud or vendor-neutral requirement?
  → MLflow (open source) + Kubeflow Pipelines (Kubernetes-native)
    Portable across all clouds; higher operational overhead.
```

### Feature Comparison Matrix

| Dimension | Azure ML | AWS SageMaker | Google Vertex AI |
|---|---|---|---|
| **Experiment tracking** | AML Jobs + MLflow integration | SageMaker Experiments | Vertex Experiments |
| **Model registry** | AML Model Registry | SageMaker Model Registry | Vertex Model Registry |
| **Pipeline orchestration** | AML Pipelines (Python SDK v2) | SageMaker Pipelines | Vertex AI Pipelines (Kubeflow) |
| **Managed training** | Compute Clusters (CPU/GPU) | Training Jobs (managed fleet) | Custom Training Jobs |
| **Managed endpoints** | Online Endpoints (real-time) + Batch Endpoints | Real-time / Async / Batch Endpoints | Online Prediction + Batch Prediction |
| **AutoML** | Azure AutoML | SageMaker Autopilot | Vertex AutoML |
| **Feature store** | AML Feature Store | SageMaker Feature Store | Vertex Feature Store |
| **Monitoring** | AML Data Monitor | SageMaker Model Monitor | Vertex Model Monitoring |
| **DevOps integration** | Azure DevOps / GitHub Actions native | CodePipeline / CodeBuild | Cloud Build / Cloud Deploy |
| **Notebook environment** | AML Compute Instance | SageMaker Studio | Vertex Workbench |
| **IAM model** | Microsoft Entra ID + RBAC | AWS IAM Roles | GCP IAM + Service Accounts |
| **Data lake integration** | ADLS Gen2 + Azure Synapse | S3 + Glue + Redshift | GCS + BigQuery |
| **LLM / Foundation models** | Azure OpenAI + Model Catalog | SageMaker JumpStart | Model Garden (Gemini, Llama) |
| **Pricing model** | Pay-per-compute-minute | Pay-per-compute-minute | Pay-per-compute-minute |

---

## 2. Azure Machine Learning — Full Reference {#azure-ml}

> **Source**: Microsoft Azure ML Documentation.
> https://learn.microsoft.com/en-us/azure/machine-learning
> Azure ML Python SDK v2: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme

### Core Architecture

```
AZURE ML WORKSPACE — RESOURCE HIERARCHY
────────────────────────────────────────────────────────────────────────────

Azure Subscription
  └── Resource Group
        └── Azure ML Workspace  ←  central governance unit
              │
              ├── Compute
              │     ├── Compute Clusters   (scalable CPU/GPU for training)
              │     ├── Compute Instances  (single-node dev notebooks)
              │     └── Serverless Compute (pay-per-job, no provisioning)
              │
              ├── Data
              │     ├── Datastores         (connections to ADLS, Blob, SQL)
              │     └── Data Assets        (versioned references to datasets)
              │
              ├── Assets
              │     ├── Environments       (Docker images + conda/pip deps)
              │     ├── Models             (versioned model registry)
              │     └── Components         (reusable pipeline steps)
              │
              ├── Jobs
              │     ├── Command Jobs       (single training run)
              │     └── Pipeline Jobs      (multi-step ML workflows)
              │
              └── Endpoints
                    ├── Online Endpoints   (real-time inference, REST API)
                    └── Batch Endpoints    (async large-scale scoring)

Connected Azure Services (automatically provisioned with workspace):
  ├── Azure Storage Account (default datastore — Blob + ADLS Gen2)
  ├── Azure Container Registry (stores training environment images)
  ├── Azure Key Vault (secrets: connection strings, API keys)
  └── Azure Application Insights (logs, metrics, endpoint monitoring)
```

### Environment Setup

```bash
# Install Azure ML SDK v2
uv add azure-ai-ml azure-identity

# Authenticate — use DefaultAzureCredential (chains through:
# environment variables → managed identity → Azure CLI → browser)
# In CI/CD: use Service Principal via env vars or managed identity
```

### Workspace Connection and Configuration

```python
from __future__ import annotations

import logging
import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

logger = logging.getLogger(__name__)

# --- Constants — externalize to environment variables or Azure Key Vault ---
SUBSCRIPTION_ID: str = os.environ["AZURE_SUBSCRIPTION_ID"]
RESOURCE_GROUP:  str = os.environ["AZURE_RESOURCE_GROUP"]
WORKSPACE_NAME:  str = os.environ["AZURE_ML_WORKSPACE"]


def get_ml_client() -> MLClient:
    """
    Authenticate and return an Azure ML client.

    Uses DefaultAzureCredential — works locally (Azure CLI),
    in CI/CD (Service Principal via env vars), and on Azure
    compute (Managed Identity). No credentials in code.
    """
    credential = DefaultAzureCredential()
    client = MLClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME,
    )
    logger.info("Connected to workspace: %s", WORKSPACE_NAME)
    return client
```

### Registering Data Assets

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes


def register_data_asset(
    client: MLClient,
    name: str,
    path: str,
    version: str = "1",
    description: str = "",
) -> Data:
    """
    Register a versioned data asset in the AML workspace.

    The path can point to:
    - ADLS Gen2:  azureml://datastores/<name>/paths/<folder>/
    - Blob:       azureml://datastores/<name>/paths/<blob>
    - Local path: automatically uploaded to the default datastore

    Args:
        path: Cloud path or local path to the data.
        version: Semantic version string — increment on every schema change.
    """
    data_asset = Data(
        name=name,
        version=version,
        description=description,
        path=path,
        type=AssetTypes.URI_FOLDER,   # URI_FOLDER for directories, URI_FILE for single files
    )
    registered = client.data.create_or_update(data_asset)
    logger.info("Registered data asset: %s v%s", registered.name, registered.version)
    return registered
```

### Defining Training Environments

```python
from azure.ai.ml.entities import Environment, BuildContext


def create_training_environment(client: MLClient) -> Environment:
    """
    Create a versioned AML environment from a conda specification.
    Environments are cached as Docker images in Azure Container Registry.
    Reuse across jobs to avoid image rebuilds on every run.
    """
    env = Environment(
        name="data-science-training-env",
        description="Python 3.12 environment for ML training: XGBoost, LightGBM, CatBoost, MLflow",
        conda_file="environments/training_conda.yaml",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest",
        version="2.0",
    )
    registered_env = client.environments.create_or_update(env)
    logger.info("Environment registered: %s v%s", registered_env.name, registered_env.version)
    return registered_env
```

```yaml
# environments/training_conda.yaml
name: training-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - pip:
    - xgboost>=2.0
    - lightgbm>=4.0
    - catboost>=1.2
    - scikit-learn>=1.4
    - pandas>=2.0
    - mlflow>=2.12
    - azure-ai-ml
    - azureml-mlflow
    - pandera
    - great-expectations
```

### Running a Training Job

```python
from azure.ai.ml import command, Input, Output
from azure.ai.ml.constants import AssetTypes, InputOutputModes


def submit_training_job(client: MLClient) -> str:
    """
    Submit a managed training job to an Azure ML compute cluster.
    Returns the job name for tracking.

    Job isolation: each job runs in its own container with its own
    environment, compute, and output storage. No shared state.
    """
    job = command(
        display_name="fraud-detection-gbm-training",
        description="Train XGBoost/LightGBM/CatBoost benchmark on fraud dataset",
        experiment_name="fraud-detection",

        # Script and arguments
        code="./src",                        # local folder uploaded to AML
        command="python train.py \
                 --data-path ${{inputs.training_data}} \
                 --output-path ${{outputs.model_output}} \
                 --n-estimators 500 \
                 --learning-rate 0.05",

        # Data inputs — point to registered data assets
        inputs={
            "training_data": Input(
                type=AssetTypes.URI_FOLDER,
                path="azureml:orders_silver_features:3",  # name:version
                mode=InputOutputModes.RO_MOUNT,           # read-only mount — no copy
            )
        },

        # Outputs — written to default datastore automatically
        outputs={
            "model_output": Output(
                type=AssetTypes.URI_FOLDER,
                mode=InputOutputModes.RW_MOUNT,
            )
        },

        # Environment and compute
        environment="data-science-training-env:2.0",
        compute="gpu-cluster",              # name of the AML compute cluster
        instance_count=1,                   # increase for distributed training

        # Environment variables — reference Key Vault secrets
        environment_variables={
            "MLFLOW_TRACKING_URI": "azureml://",   # logs to AML workspace automatically
        },
    )

    submitted = client.jobs.create_or_update(job)
    logger.info("Job submitted: %s | Studio URL: %s", submitted.name, submitted.studio_url)
    return submitted.name
```

### AML Pipelines — Multi-Step ML Workflow

```python
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import load_component


# Load reusable components (YAML-defined, versioned, shareable across pipelines)
data_validation_component = load_component(source="components/data_validation/spec.yaml")
training_component         = load_component(source="components/training/spec.yaml")
evaluation_component       = load_component(source="components/evaluation/spec.yaml")
registration_component     = load_component(source="components/model_registration/spec.yaml")


@pipeline(
    display_name="end-to-end-fraud-detection-pipeline",
    description="Full ML pipeline: validate → train → evaluate → register",
    default_compute="cpu-cluster",
)
def fraud_detection_pipeline(raw_data_path: str, min_auc: float = 0.85):
    """
    End-to-end AML pipeline. Each step runs in isolation on managed compute.
    Outputs of one step automatically become inputs to the next.
    """
    validation_step = data_validation_component(
        data_path=raw_data_path,
        contract_path="contracts/orders_contract.yaml",
    )

    training_step = training_component(
        training_data=validation_step.outputs.validated_data,
        n_estimators=500,
        learning_rate=0.05,
    )

    evaluation_step = evaluation_component(
        model_path=training_step.outputs.model,
        test_data=validation_step.outputs.test_data,
        min_auc=min_auc,
    )

    # Registration only runs if evaluation passes the AUC gate
    registration_step = registration_component(
        model_path=training_step.outputs.model,
        metrics=evaluation_step.outputs.metrics,
        model_name="fraud-detection-gbm",
    )

    return {"registered_model": registration_step.outputs.registered_model}


def run_pipeline(client: MLClient) -> str:
    pipeline_job = fraud_detection_pipeline(
        raw_data_path="azureml:orders_silver_features:latest",
        min_auc=0.85,
    )
    submitted = client.jobs.create_or_update(pipeline_job)
    logger.info("Pipeline submitted: %s", submitted.studio_url)
    return submitted.name
```

### Online Endpoints — Managed Real-Time Inference

```python
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    CodeConfiguration,
)
from azure.ai.ml.constants import AssetTypes


def deploy_online_endpoint(client: MLClient, model_name: str, model_version: str) -> str:
    """
    Deploy a registered model to a managed online endpoint.
    AML handles load balancing, scaling, health checks, and TLS.

    Deployment pattern: create endpoint first, then deployment.
    Traffic is controlled per-deployment — enables blue-green and canary.
    """
    endpoint_name = "fraud-detection-endpoint"

    # Create endpoint (DNS name and auth configuration)
    endpoint = ManagedOnlineEndpoint(
        name=endpoint_name,
        description="Real-time fraud scoring endpoint",
        auth_mode="key",       # 'key' or 'aml_token' (Entra ID)
        tags={"team": "data-science", "model": model_name},
    )
    client.online_endpoints.begin_create_or_update(endpoint).result()

    # Create deployment (compute SKU, model, scoring script, environment)
    deployment = ManagedOnlineDeployment(
        name="blue",           # deployment name — traffic routes here
        endpoint_name=endpoint_name,
        model=f"azureml:{model_name}:{model_version}",
        code_configuration=CodeConfiguration(
            code="./src/scoring",
            scoring_script="score.py",   # must define init() and run()
        ),
        environment="data-science-training-env:2.0",
        instance_type="Standard_DS3_v2",
        instance_count=2,      # minimum for production HA
    )
    client.online_deployments.begin_create_or_update(deployment).result()

    # Route 100% of traffic to this deployment
    endpoint.traffic = {"blue": 100}
    client.online_endpoints.begin_create_or_update(endpoint).result()

    endpoint_uri = client.online_endpoints.get(endpoint_name).scoring_uri
    logger.info("Endpoint live: %s", endpoint_uri)
    return endpoint_uri
```

```python
# src/scoring/score.py — scoring script for AML online endpoint
import mlflow
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)
model = None

def init():
    """Called once when the container starts — load the model."""
    import os
    global model
    model_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], "model")
    model = mlflow.pyfunc.load_model(model_path)
    logger.info("Model loaded from %s", model_path)

def run(raw_data: str) -> str:
    """Called on every inference request."""
    data = json.loads(raw_data)
    df = pd.DataFrame(data["data"], columns=data["columns"])
    predictions = model.predict(df)
    return json.dumps({"predictions": predictions.tolist()})
```

### AML + Azure DevOps CI/CD Integration

```yaml
# azure-pipelines.yml — Azure DevOps pipeline for ML CI/CD
trigger:
  branches:
    include: [main]
  paths:
    include: [src/, components/, environments/]

pool:
  vmImage: ubuntu-latest

variables:
  - group: azure-ml-credentials   # variable group with AZURE_* env vars

stages:
  - stage: CodeQuality
    jobs:
      - job: Lint
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "3.12"
          - script: |
              pip install --quiet uv
              uv sync --dev
              uv run ruff check .
              uv run ruff format --check .
              uv run mypy src/ --strict
            displayName: Ruff + mypy

          - script: uv run pytest tests/ -v --tb=short
            displayName: Unit tests

  - stage: TrainAndEvaluate
    dependsOn: CodeQuality
    jobs:
      - job: SubmitAMLPipeline
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "3.12"
          - script: |
              pip install --quiet azure-ai-ml azure-identity
              python scripts/submit_pipeline.py \
                --workspace $AZURE_ML_WORKSPACE \
                --subscription $AZURE_SUBSCRIPTION_ID \
                --resource-group $AZURE_RESOURCE_GROUP \
                --min-auc 0.85
            env:
              AZURE_SUBSCRIPTION_ID: $(AZURE_SUBSCRIPTION_ID)
              AZURE_RESOURCE_GROUP: $(AZURE_RESOURCE_GROUP)
              AZURE_ML_WORKSPACE: $(AZURE_ML_WORKSPACE)
              AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
              AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
              AZURE_TENANT_ID: $(AZURE_TENANT_ID)
            displayName: Submit AML training pipeline

  - stage: Deploy
    dependsOn: TrainAndEvaluate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployEndpoint
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - script: |
                    python scripts/deploy_endpoint.py \
                      --model-name fraud-detection-gbm \
                      --model-version latest \
                      --endpoint fraud-detection-endpoint
                  displayName: Deploy to AML Online Endpoint
```

---

## 3. AWS SageMaker — Full Reference {#sagemaker}

> **Source**: AWS SageMaker Developer Guide.
> https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html

### Core Architecture

```
AWS SAGEMAKER RESOURCE HIERARCHY
────────────────────────────────────────────────────────────────────────────

AWS Account → Region
  └── SageMaker Domain  ←  central workspace (IAM + VPC + S3 configured here)
        │
        ├── Studio       (web IDE — notebooks, pipelines, experiments)
        ├── Experiments  (run tracking — equivalent to MLflow experiments)
        ├── Model Registry (versioned model catalog with approval workflow)
        │
        ├── Training Jobs  (managed compute fleet — spot instances supported)
        ├── Processing Jobs (data preprocessing at scale)
        ├── Pipelines       (multi-step ML workflow DAG)
        │
        └── Endpoints
              ├── Real-Time Endpoints   (synchronous, low-latency)
              ├── Async Endpoints       (queued, large payloads)
              └── Batch Transform Jobs  (offline scoring, no endpoint needed)

Underlying AWS Services (managed transparently by SageMaker):
  ├── S3          (model artifacts, training data, output storage)
  ├── ECR         (Docker images for training and inference containers)
  ├── CloudWatch  (logs, metrics, alarms)
  └── IAM         (execution role — grants SageMaker access to S3, ECR, etc.)
```

### Training Job

```python
from __future__ import annotations

import boto3
import sagemaker
from sagemaker.sklearn import SKLearn
from sagemaker.xgboost import XGBoost
import logging
import os

logger = logging.getLogger(__name__)

ROLE_ARN:   str = os.environ["SAGEMAKER_EXECUTION_ROLE_ARN"]
S3_BUCKET:  str = os.environ["S3_BUCKET"]
REGION:     str = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

session = sagemaker.Session(boto_session=boto3.Session(region_name=REGION))


def run_training_job(
    train_s3_path: str,
    job_name: str,
    n_estimators: int = 500,
    learning_rate: float = 0.05,
    use_spot: bool = True,
) -> str:
    """
    Submit a managed SageMaker training job using the built-in XGBoost container.
    Spot instances reduce cost by up to 70% — enable for non-critical training runs.

    Args:
        train_s3_path: S3 URI to training data (CSV or LibSVM format).
        use_spot: Enable managed spot training with checkpointing.

    Returns:
        SageMaker training job name.
    """
    estimator = XGBoost(
        entry_point="train.py",
        source_dir="./src",
        role=ROLE_ARN,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        framework_version="1.7-1",
        py_version="py3",

        hyperparameters={
            "n-estimators":  n_estimators,
            "learning-rate": learning_rate,
            "objective":     "binary:logistic",
        },

        # Spot instance configuration (70% cost reduction, requires checkpointing)
        use_spot_instances=use_spot,
        max_wait=7200,                         # max seconds including spot wait
        max_run=3600,                          # max training seconds
        checkpoint_s3_uri=f"s3://{S3_BUCKET}/checkpoints/{job_name}/" if use_spot else None,

        # Output
        output_path=f"s3://{S3_BUCKET}/models/",
        sagemaker_session=session,
    )

    estimator.fit(
        inputs={"train": train_s3_path},
        job_name=job_name,
        wait=False,    # async — poll or use EventBridge to trigger next step
    )
    logger.info("Training job submitted: %s", job_name)
    return job_name


def deploy_real_time_endpoint(
    model_name: str,
    endpoint_name: str,
    instance_type: str = "ml.m5.large",
) -> str:
    """
    Deploy a registered model to a SageMaker real-time endpoint.
    Returns the endpoint URL for inference calls.
    """
    sm_client = boto3.client("sagemaker", region_name=REGION)

    sm_client.create_endpoint_config(
        EndpointConfigName=f"{endpoint_name}-config",
        ProductionVariants=[{
            "VariantName": "primary",
            "ModelName": model_name,
            "InstanceType": instance_type,
            "InitialInstanceCount": 2,
            "InitialVariantWeight": 1.0,
        }],
    )

    sm_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=f"{endpoint_name}-config",
    )

    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=endpoint_name)
    logger.info("Endpoint %s is in service", endpoint_name)
    return endpoint_name


def invoke_endpoint(endpoint_name: str, payload: str) -> dict:
    """Call a SageMaker real-time endpoint for inference."""
    runtime = boto3.client("sagemaker-runtime", region_name=REGION)
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=payload,
    )
    return {"prediction": response["Body"].read().decode("utf-8")}
```

### SageMaker Model Monitor — Drift Detection

```python
from sagemaker.model_monitor import DefaultModelMonitor, CronExpressionGenerator
from sagemaker.model_monitor.dataset_format import DatasetFormat


def setup_model_monitor(
    endpoint_name: str,
    baseline_s3_path: str,
    monitor_s3_output: str,
) -> None:
    """
    Configure SageMaker Model Monitor to detect data drift on a live endpoint.
    Monitor runs on a schedule; violations are published to CloudWatch.

    Baseline: collected from training data statistics.
    Monitor: compares live traffic distributions to baseline.
    """
    monitor = DefaultModelMonitor(
        role=ROLE_ARN,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        volume_size_in_gb=20,
        max_runtime_in_seconds=3600,
        sagemaker_session=session,
    )

    # Suggest baseline statistics from training data
    monitor.suggest_baseline(
        baseline_dataset=baseline_s3_path,
        dataset_format=DatasetFormat.csv(header=True),
        output_s3_uri=f"{monitor_s3_output}/baseline/",
        wait=True,
    )

    # Schedule monitoring — runs hourly, compares to baseline
    monitor.create_monitoring_schedule(
        monitor_schedule_name=f"{endpoint_name}-monitor",
        endpoint_input=endpoint_name,
        output_s3_uri=f"{monitor_s3_output}/reports/",
        statistics=monitor.baseline_statistics(),
        constraints=monitor.suggested_constraints(),
        schedule_cron_expression=CronExpressionGenerator.hourly(),
    )
    logger.info("Model monitor scheduled for endpoint: %s", endpoint_name)
```

---

## 4. Google Vertex AI — Full Reference {#vertex-ai}

> **Source**: Google Vertex AI Documentation.
> https://cloud.google.com/vertex-ai/docs

### Core Architecture

```
GOOGLE VERTEX AI RESOURCE HIERARCHY
────────────────────────────────────────────────────────────────────────────

GCP Project → Region
  └── Vertex AI
        │
        ├── Workbench       (managed Jupyter notebooks — JupyterLab)
        ├── Experiments     (run tracking — compatible with MLflow)
        ├── Model Registry  (versioned models with metadata)
        │
        ├── Custom Training Jobs  (single-node or distributed)
        ├── Vertex AI Pipelines   (Kubeflow Pipelines v2 on managed infra)
        ├── AutoML              (no-code model training for tabular/vision/NLP)
        │
        └── Endpoints
              ├── Online Prediction  (synchronous REST)
              └── Batch Prediction   (async, large-scale)

Native GCP Integrations:
  ├── BigQuery     (BigQuery ML — SQL-native model training)
  ├── GCS          (Cloud Storage for data and artifacts)
  ├── Dataflow     (Apache Beam — feature engineering at scale)
  ├── Pub/Sub      (streaming data sources)
  └── Cloud Build  (CI/CD for ML pipelines)
```

### Custom Training Job

```python
from __future__ import annotations

from google.cloud import aiplatform
import logging
import os

logger = logging.getLogger(__name__)

PROJECT_ID:  str = os.environ["GCP_PROJECT_ID"]
REGION:      str = os.environ.get("GCP_REGION", "us-central1")
GCS_BUCKET:  str = os.environ["GCS_BUCKET"]

aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=f"gs://{GCS_BUCKET}")


def submit_custom_training_job(
    job_display_name: str,
    training_script: str = "train.py",
    machine_type: str = "n1-standard-4",
    accelerator_type: str | None = None,
    accelerator_count: int = 0,
) -> aiplatform.CustomTrainingJob:
    """
    Submit a Vertex AI custom training job.
    Uses a pre-built Python container — no Docker image required.
    """
    job = aiplatform.CustomTrainingJob(
        display_name=job_display_name,
        script_path=training_script,
        container_uri="us-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.1-0:latest",
        requirements=["xgboost>=2.0", "lightgbm>=4.0", "catboost>=1.2", "mlflow"],
        model_serving_container_image_uri=(
            "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
        ),
    )

    model = job.run(
        model_display_name="fraud-detection-gbm",
        args=[
            "--training-data-uri", f"gs://{GCS_BUCKET}/silver/orders/",
            "--output-uri",        f"gs://{GCS_BUCKET}/models/",
            "--n-estimators",      "500",
        ],
        replica_count=1,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        sync=False,   # non-blocking
    )

    logger.info("Training job submitted: %s", job.display_name)
    return job


def deploy_vertex_endpoint(model_display_name: str) -> aiplatform.Endpoint:
    """Deploy a registered Vertex AI model to a managed online endpoint."""
    models = aiplatform.Model.list(filter=f"display_name={model_display_name}")
    if not models:
        raise ValueError(f"No model found with display_name: {model_display_name}")

    model = models[0]
    endpoint = model.deploy(
        machine_type="n1-standard-4",
        min_replica_count=1,
        max_replica_count=5,        # auto-scales to 5 replicas under load
        traffic_split={"0": 100},   # 100% to this deployment
        sync=True,
    )
    logger.info("Endpoint deployed: %s", endpoint.resource_name)
    return endpoint
```

### BigQuery ML — SQL-Native Model Training

```sql
-- Train a logistic regression model directly in BigQuery
-- No Python, no compute cluster — runs on BigQuery's distributed engine
CREATE OR REPLACE MODEL `project.dataset.fraud_model`
OPTIONS (
    model_type       = 'LOGISTIC_REG',
    input_label_cols = ['is_fraud'],
    l1_reg           = 0.01,
    l2_reg           = 0.01,
    max_iterations   = 50,
    data_split_method = 'AUTO_SPLIT'    -- automatic train/eval split
)
AS
SELECT
    amount,
    days_since_last_transaction,
    merchant_category,
    is_foreign_transaction,
    hour_of_day_sin,
    hour_of_day_cos,
    is_fraud
FROM `project.dataset.gold_transactions`
WHERE partition_date BETWEEN '2023-01-01' AND '2024-12-31';

-- Evaluate
SELECT * FROM ML.EVALUATE(MODEL `project.dataset.fraud_model`);

-- Predict on new data
SELECT
    transaction_id,
    predicted_is_fraud,
    predicted_is_fraud_probs
FROM ML.PREDICT(
    MODEL `project.dataset.fraud_model`,
    (SELECT * FROM `project.dataset.gold_transactions_new`)
);
```

---

## 5. Cloud Storage for ML — ADLS, S3, GCS {#cloud-storage}

### Storage Patterns for ML Workflows

```
CLOUD STORAGE USAGE BY ML PHASE
────────────────────────────────────────────────────────────────────────────

TRAINING DATA:
  Store as Parquet or Delta Lake in the cloud data lake.
  Partition by date for efficient incremental reads.
  Never store training data as CSV in cloud storage for large datasets.

  Azure:  ADLS Gen2 (abfss://container@account.dfs.core.windows.net/path/)
  AWS:    S3         (s3://bucket/silver/orders/year=2024/month=01/)
  GCP:    GCS        (gs://bucket/silver/orders/year=2024/month=01/)

MODEL ARTIFACTS:
  Store model files (pickle, ONNX, MLflow artifacts) in object storage.
  Each training run writes to a unique, versioned path.
  Register in the platform model registry pointing to this path.

  Azure:  azureml://datastores/workspaceblobstore/paths/models/{run_id}/
  AWS:    s3://bucket/models/{job_name}/output/model.tar.gz
  GCP:    gs://bucket/models/{job_name}/

LOGS AND METRICS:
  Platform-managed: AML → Application Insights, SageMaker → CloudWatch,
  Vertex → Cloud Logging. Use MLflow for cross-platform portability.

INFERENCE OUTPUTS (batch):
  Write batch prediction results to partitioned Parquet in the data lake.
  Apply the same data contract standards as any Gold-layer output.
```

### Efficient Cloud Data Loading

```python
from __future__ import annotations

import pandas as pd
import polars as pl
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_training_data_azure(
    adls_path: str,
    columns: list[str] | None = None,
    filters: list | None = None,
) -> pl.DataFrame:
    """
    Read partitioned Parquet from ADLS Gen2 using Polars with column pruning.
    Requires: AZURE_STORAGE_ACCOUNT_KEY or DefaultAzureCredential configured.

    Args:
        adls_path: ADLS Gen2 path, e.g.
                   'abfss://silver@account.dfs.core.windows.net/orders/'
        columns: Subset of columns to read (column pruning reduces I/O).
        filters: Partition filter list for predicate pushdown, e.g.
                 [('year', '=', '2024'), ('month', '>=', '06')]
    """
    df = pl.scan_parquet(
        adls_path,
        hive_partitioning=True,     # reads year=2024/month=01/ as columns
    )
    if filters:
        for col, op, val in filters:
            if op == '=':
                df = df.filter(pl.col(col) == val)
            elif op == '>=':
                df = df.filter(pl.col(col) >= val)
    if columns:
        df = df.select(columns)

    result = df.collect()
    logger.info("Loaded %d rows, %d cols from ADLS", result.height, result.width)
    return result


def read_training_data_s3(
    s3_path: str,
    columns: list[str] | None = None,
) -> pl.DataFrame:
    """
    Read partitioned Parquet from S3 using Polars.
    Requires: AWS credentials via environment variables or IAM role.
    """
    import s3fs
    fs = s3fs.S3FileSystem(anon=False)
    files = fs.glob(f"{s3_path}/**/*.parquet")

    df = pl.scan_parquet(
        [f"s3://{f}" for f in files],
        storage_options={"anon": False},
    )
    if columns:
        df = df.select(columns)

    result = df.collect()
    logger.info("Loaded %d rows from S3: %s", result.height, s3_path)
    return result
```

---

## 6. Cloud ML Security — Identity and Access {#security}

### Authentication Patterns by Platform

```
AUTHENTICATION DECISION — CLOUD ML
────────────────────────────────────────────────────────────────────────────

AZURE (Microsoft Entra ID):
  Local development:  Azure CLI  (az login)   → DefaultAzureCredential
  CI/CD pipelines:    Service Principal        → client_id + client_secret + tenant_id
                      (stored in Azure DevOps variable groups or Key Vault)
  Azure compute:      Managed Identity         → no credentials, automatic
                      (assigned to AML Compute Cluster or Compute Instance)

  Rule: NEVER use Service Principal credentials in code or source control.
        Use DefaultAzureCredential — it chains automatically through all methods.

AWS:
  Local development:  AWS CLI profile           → boto3 picks up automatically
  CI/CD pipelines:    IAM Role via OIDC         → GitHub Actions / Azure DevOps
                      (preferred over long-lived access keys)
  AWS compute:        EC2/SageMaker IAM Role     → no credentials, automatic

  Rule: NEVER use AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY in code.
        Attach IAM roles to compute resources.

GCP:
  Local development:  gcloud auth application-default login
  CI/CD pipelines:    Workload Identity Federation (OIDC — keyless auth)
                      or Service Account key (legacy — avoid)
  GCP compute:        Attached Service Account   → automatic credentials
```

### Key Vault Integration — Secrets for ML Pipelines

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os


def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret from Azure Key Vault.
    Use for database passwords, API keys, and connection strings —
    never hardcode these in training scripts or pipeline YAML.

    The Key Vault URI is the only config needed in code;
    access is granted via Managed Identity or Service Principal.
    """
    vault_uri = os.environ["AZURE_KEY_VAULT_URI"]
    client = SecretClient(vault_url=vault_uri, credential=DefaultAzureCredential())
    return client.get_secret(secret_name).value


# Usage in training scripts:
# db_password = get_secret("sql-db-password")
# mlflow_token = get_secret("mlflow-tracking-token")
```

### RBAC for Azure ML

```python
# Minimum required roles for Azure ML operations (principle of least privilege)

# READ ROLES (analysts / ML engineers — read access to workspace)
# "AzureML Data Scientist": submit jobs, read experiments, download models
# "Reader": list resources only

# WRITE ROLES (MLOps engineers — production operations)
# "AzureML Compute Operator": start/stop compute
# "Contributor": create and manage all workspace resources

# ADMIN ROLES (workspace owners only)
# "Owner": full control including role assignments

# SERVICE PRINCIPAL (CI/CD pipeline) — minimum required:
# "AzureML Data Scientist" on the workspace
# "Storage Blob Data Contributor" on the ADLS Gen2 account
# "AcrPull" on the Container Registry (to pull training images)
```

---

## 7. Cloud ML Cost Management {#cost}

### Cost Drivers by Phase

```
ML COST BREAKDOWN BY CLOUD PHASE
────────────────────────────────────────────────────────────────────────────

TRAINING (largest variable cost):
  ├── Compute hours × instance price per hour
  ├── GPU instances cost 10–100× CPU instances
  └── Optimization strategies:
        - Spot/preemptible instances: 60–80% discount (requires checkpointing)
        - Rightsizing: don't use GPU for tabular GBM (CPU is sufficient)
        - Early stopping: stop training when validation metric plateaus
        - Use managed containers (SageMaker built-in, AML curated) to avoid
          image build time charges

SERVING (largest sustained cost):
  ├── Endpoint instances × hours online × instance price
  ├── Real-time endpoints run 24/7 even with zero requests
  └── Optimization strategies:
        - Use batch endpoints for non-real-time use cases (much cheaper)
        - Scale to zero: AML serverless endpoints, Vertex AI autoscaling to 0
        - Right-size: start with smallest instance that meets latency SLA
        - Multi-model endpoints: serve multiple models on one instance

STORAGE (usually <5% of total):
  ├── Object storage is cheap ($0.02–0.023/GB/month)
  ├── Cost grows if model artifacts accumulate without lifecycle policies
  └── Optimization: lifecycle policies to archive/delete old model versions
```

### Cost Guardrails — Azure ML

```python
from azure.ai.ml.entities import ComputeInstance, AmlCompute


def create_auto_shutdown_compute(client: MLClient) -> None:
    """
    Create an AML compute cluster with cost guardrails:
    - scale-to-zero when idle (min_instances=0)
    - auto-shutdown for compute instances
    - spot instances for training jobs
    """
    # Compute cluster — scales to zero, uses spot instances
    cluster = AmlCompute(
        name="cpu-spot-cluster",
        type="amlcompute",
        size="Standard_DS3_v2",
        min_instances=0,       # CRITICAL: scales to zero when idle — no idle cost
        max_instances=4,
        tier="Dedicated",      # or "LowPriority" (spot) — 60-80% cheaper
        idle_time_before_scale_down=120,   # seconds of idle before scale-down
    )
    client.compute.begin_create_or_update(cluster).result()

    # Compute instance — auto-shutdown to prevent idle waste
    instance = ComputeInstance(
        name="dev-instance",
        type="computeinstance",
        size="Standard_DS3_v2",
        idle_time_before_shutdown_minutes=30,   # shut down after 30 min idle
        enable_node_public_ip=False,            # security: private network only
    )
    client.compute.begin_create_or_update(instance).result()
```

---

## 8. Multi-Cloud ML Architecture Patterns {#patterns}

### The MLflow Bridge — Cross-Cloud Portability

MLflow provides a common experiment tracking and model serving interface that is
platform-agnostic. This enables training on one cloud and serving on another, or
migrating between cloud providers without rewriting ML code.

```python
import mlflow
import os

# Configure MLflow tracking URI — works on any cloud or local server
# Azure:    mlflow.set_tracking_uri("azureml://...")   or  AML auto-configures
# AWS:      mlflow.set_tracking_uri("http://sagemaker-mlflow-server:5000")
# GCP:      mlflow.set_tracking_uri("http://vertex-mlflow:5000")
# Local:    mlflow.set_tracking_uri("http://localhost:5000")
# Databricks: mlflow.set_tracking_uri("databricks")  (auto-configured)

# The experiment code is identical regardless of cloud:
with mlflow.start_run():
    mlflow.log_params({"n_estimators": 500, "learning_rate": 0.05})
    # ... train model ...
    mlflow.log_metrics({"test_auc": 0.92, "test_f1": 0.87})
    mlflow.sklearn.log_model(model, "model")
```

### Cloud Comparison — When to Use What

| Scenario | Recommended Platform | Reason |
|---|---|---|
| Microsoft-stack org (Azure DevOps, Power BI, Teams) | Azure ML | Native integration with existing Microsoft services; Entra ID governance |
| Data-warehouse-centric org on AWS | SageMaker | Tightest S3 + Redshift + Glue integration; managed spot training |
| BigQuery-heavy analytics org | Vertex AI + BigQuery ML | SQL-native training in BigQuery; Gemini integration for LLM workflows |
| Databricks on any cloud | Databricks ML + MLflow | Platform-agnostic; best-in-class data+ML unified layer |
| Regulated industry (finance, healthcare) | Azure ML or AWS (both have FedRAMP/HIPAA) | Compliance certifications; data residency controls |
| Multi-cloud / vendor lock-in concern | MLflow + Kubeflow on Kubernetes | Portable; runs on any cloud; higher operational burden |

---

## 9. References {#references}

- Microsoft Azure Machine Learning Documentation. https://learn.microsoft.com/en-us/azure/machine-learning
- Azure ML Python SDK v2 Reference. https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme
- Azure ML Best Practices. https://learn.microsoft.com/en-us/azure/machine-learning/best-practices-overview
- AWS SageMaker Developer Guide. https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html
- AWS SageMaker Model Monitor. https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
- Google Vertex AI Documentation. https://cloud.google.com/vertex-ai/docs
- Google BigQuery ML. https://cloud.google.com/bigquery/docs/bqml-introduction
- Google (2020). Practitioners Guide to MLOps. https://cloud.google.com/resources/mlops-whitepaper
- MLflow Documentation. https://mlflow.org/docs/latest
- Microsoft (2024). Azure ML + Azure DevOps Integration. https://learn.microsoft.com/en-us/azure/machine-learning/how-to-devops-machine-learning
