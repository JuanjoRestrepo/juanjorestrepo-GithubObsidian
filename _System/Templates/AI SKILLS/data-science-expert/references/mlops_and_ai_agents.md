# MLOps, AI Agents, and Production AI Systems

> **References**: Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine Learning
> Operations (MLOps): Overview, Definition, and Architecture. *IEEE Access*, 11.
> Wang, L., et al. (2024). A Survey on Large Language Model based Autonomous Agents.
> *Frontiers of Computer Science*, 18(6). · Yao, S., et al. (2023). ReAct: Synergizing
> Reasoning and Acting in Language Models. *ICLR 2023*. arXiv:2210.03629. · Shinn, N.,
> et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. *NeurIPS
> 2023*. arXiv:2303.11366. · Wu, Q., et al. (2023). AutoGen: Enabling Next-Gen LLM
> Applications via Multi-Agent Conversation. arXiv:2308.08155. · Harness Developer Hub.
> https://developer.harness.io · MLflow Documentation. https://mlflow.org/docs/latest

## Table of Contents

1. [MLOps — Lifecycle and Architecture](#mlops)
2. [Experiment Tracking and Model Registry — MLflow](#mlflow)
3. [Harness AI — Platform Reference](#harness)
4. [AI Agents — Theory and Architecture](#agents-theory)
5. [ReAct — Reasoning and Acting](#react)
6. [Multi-Agent Systems — AutoGen, CrewAI, LangGraph](#multi-agent)
7. [Model Context Protocol (MCP)](#mcp)
8. [Model Deployment Patterns](#deployment)
9. [Model Monitoring and Drift Detection](#monitoring)
10. [Edge ML and IoT Deployment](#edge-iot)
11. [References](#references)

---

## 1. MLOps — Lifecycle and Architecture {#mlops}

> **Source**: Kreuzberger et al. (2023). Machine Learning Operations (MLOps):
> Overview, Definition, and Architecture. *IEEE Access*, 11, 31866–31879.
> Google (2020). *Practitioners Guide to MLOps*. https://cloud.google.com/resources/mlops-whitepaper

### What MLOps Is

MLOps (Machine Learning Operations) is the set of practices and infrastructure
that operationalizes the ML lifecycle — from data ingestion and model training to
deployment, serving, monitoring, and retraining. It applies DevOps principles
(automation, CI/CD, observability, version control) to the ML development process.

The core problem MLOps solves: ML models are not software artifacts that are built
once and deployed — they require continuous maintenance because the world changes.
Data distributions shift, model performance degrades, business requirements evolve.
MLOps treats model quality as an operational concern, not just a training-time concern.

### MLOps Maturity Levels (Google, 2020)

| Level | Description | Automation |
|---|---|---|
| **Level 0** | Manual process — Jupyter notebooks, ad hoc retraining | None — data scientist trains and deploys manually |
| **Level 1** | ML pipeline automation — automated training, CT (Continuous Training) | Automated data validation, model training, evaluation |
| **Level 2** | CI/CD pipeline automation — automated build, test, deploy of the full pipeline | Full CI/CD for pipelines; automated model deployment to serving |

### MLOps Full Lifecycle

```
Data Collection / Ingestion
      │
      ▼
Data Validation                     ← Great Expectations / Pandera
      │
      ▼
Feature Engineering / Feature Store ← Feast / Tecton / Databricks Feature Store
      │
      ▼
Model Training                      ← scikit-learn / XGBoost / PyTorch / TensorFlow
      │
      ▼
Experiment Tracking                 ← MLflow / Weights & Biases / Comet
      │
      ▼
Model Evaluation + Validation       ← Offline metrics: AUC, F1, RMSE
      │
      ▼
Model Registry                      ← MLflow Model Registry / Harness AI / SageMaker
      │
      ▼
CI/CD Pipeline (Harness / GitHub Actions / Jenkins)
      │
      ├── Unit tests on model code
      ├── Integration tests on serving endpoint
      ├── Shadow deployment / canary release
      └── A/B test against production model
      │
      ▼
Model Serving                       ← MLflow serving / FastAPI / TorchServe / Triton
      │
      ▼
Model Monitoring                    ← Evidently AI / WhyLogs / Arize / Fiddler
      │
      ├── Data drift detection
      ├── Model performance degradation
      ├── Prediction distribution shift
      └── Business KPI impact tracking
      │
      ▼
Trigger Retraining                  ← Airflow / Harness Pipelines / Vertex AI Pipelines
```

---

## 2. Experiment Tracking and Model Registry — MLflow {#mlflow}

> **Source**: MLflow Documentation. https://mlflow.org/docs/latest
> Chen, A., et al. (2020). Developments in MLflow: A System to Accelerate the Machine
> Learning Lifecycle. *DEEM Workshop at SIGMOD 2020*.

### MLflow Components

| Component | Purpose |
|---|---|
| **Tracking** | Log parameters, metrics, artifacts, and code version per experiment run |
| **Projects** | Packaging format for reproducible ML code (conda/docker environment) |
| **Models** | Standard model packaging format with `python_function` flavor — serves any framework |
| **Model Registry** | Lifecycle management: Staging → Production → Archived versioning with approval workflows |
| **Evaluate** | Automated evaluation of LLMs and classical ML models against test datasets |

### Experiment Tracking

```python
from __future__ import annotations

import mlflow
import mlflow.sklearn
import logging
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI: str = "http://localhost:5000"   # or Databricks / cloud URI
EXPERIMENT_NAME: str = "fraud_detection_gbm"


def train_and_log(
    X: pd.DataFrame,
    y: pd.Series,
    params: dict,
) -> str:
    """
    Train a GBM model and log all artifacts to MLflow.

    Returns:
        MLflow run_id for the logged experiment.
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        mlflow.log_param("feature_count", X.shape[1])

        # Train
        model = GradientBoostingClassifier(**params)
        model.fit(X_train, y_train)

        # Evaluate
        y_prob = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)
        auc   = roc_auc_score(y_test, y_prob)
        f1    = f1_score(y_test, y_pred)

        # Log metrics
        mlflow.log_metrics({"test_auc": auc, "test_f1": f1})

        # Log model with input example for schema inference
        input_example = X_train.iloc[:5]
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            input_example=input_example,
            registered_model_name="fraud_detection_gbm",   # auto-registers to Model Registry
        )

        logger.info("Run %s: AUC=%.4f, F1=%.4f", run.info.run_id, auc, f1)
        return run.info.run_id


def promote_to_production(model_name: str, version: int) -> None:
    """
    Promote a registered model version from Staging to Production.
    Previous Production version is automatically archived.
    """
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True,
    )
    logger.info("Model %s v%d promoted to Production", model_name, version)
```

---

## 3. Harness AI — Platform Reference {#harness}

> **Source**: Harness Developer Hub. https://developer.harness.io
> Harness (2025). *AI-Powered Software Delivery*. https://www.harness.io/platform
> Harness (2025). *Harness AI Documentation*. https://developer.harness.io/docs/platform/harness-ai

### What Harness AI Is

Harness is a unified AI software delivery platform that combines CI/CD, MLOps,
feature flags, security testing, chaos engineering, and cloud cost management
under one governance layer. The AI layer — Harness AI (formerly AIDA, AI
Development Assistant) — provides AI agents and automation across all platform
modules, helping engineering teams ship software faster with reduced risk.

From an MLOps perspective, Harness AI provides:
- **ML Pipeline CI/CD**: automated training pipelines triggered by data changes,
  code commits, or schedule — with the same pipeline governance applied to software
- **AI Agents for SDLC**: purpose-built AI agents that assist with writing pipelines,
  debugging failures, analyzing test results, and generating code
- **Governance**: unified access control, audit trails, and compliance across all
  pipelines — including ML training and deployment pipelines

### Core Platform Modules (MLOps-Relevant)

| Module | MLOps Application |
|---|---|
| **Harness CI** | Build and test ML code on every commit. Run training validation jobs. Trigger data validation gates. |
| **Harness CD** | Deploy models to serving infrastructure (Kubernetes, SageMaker, Vertex AI). Canary releases, blue-green deployments for model versions. |
| **Harness AI Agents** | AI-powered agents that assist in writing pipeline YAML, debugging failed runs, analyzing test coverage, and generating infrastructure-as-code |
| **Feature Flags** | Progressively roll out new model versions by feature flag — decouple deployment from release |
| **Cloud Cost** | Monitor compute costs for training runs and serving infrastructure |
| **Service Reliability** | Monitor ML endpoint latency, error rates, and SLOs post-deployment |

### Harness Pipeline for ML — YAML Specification

```yaml
# .harness/ml_training_pipeline.yaml
# Harness CI/CD Pipeline for ML model training and deployment
# Triggers: commit to main, scheduled daily, or manual dispatch

pipeline:
  name: fraud-detection-training-pipeline
  identifier: fraud_detection_training
  projectIdentifier: data_science
  orgIdentifier: engineering

  stages:
    - stage:
        name: Data Validation
        identifier: data_validation
        type: CI
        spec:
          execution:
            steps:
              - step:
                  name: Validate Data Contracts
                  identifier: validate_contracts
                  type: Run
                  spec:
                    connectorRef: dockerhub_connector
                    image: python:3.12-slim
                    command: |
                      pip install --quiet great_expectations pandera
                      python scripts/validate_data_contracts.py \
                        --contract contracts/orders_contract.yaml \
                        --data s3://datalake/silver/orders/latest/

              - step:
                  name: Data Quality Gate
                  identifier: data_quality_gate
                  type: Run
                  spec:
                    command: |
                      python scripts/check_data_freshness.py \
                        --max-age-hours 2 \
                        --exit-on-failure

    - stage:
        name: Model Training
        identifier: model_training
        type: CI
        spec:
          execution:
            steps:
              - step:
                  name: Train GBM Model
                  identifier: train_model
                  type: Run
                  spec:
                    image: python:3.12-slim
                    command: |
                      pip install --quiet xgboost lightgbm catboost mlflow scikit-learn
                      python scripts/train.py \
                        --mlflow-uri $MLFLOW_TRACKING_URI \
                        --experiment fraud_detection \
                        --output-model-path /tmp/model
                  envVariables:
                    MLFLOW_TRACKING_URI: <+secrets.getValue("mlflow_uri")>
                    AWS_ACCESS_KEY_ID: <+secrets.getValue("aws_access_key")>

              - step:
                  name: Model Evaluation Gate
                  identifier: eval_gate
                  type: Run
                  spec:
                    command: |
                      python scripts/evaluate.py \
                        --min-auc 0.85 \
                        --min-f1 0.70 \
                        --exit-on-failure

    - stage:
        name: Model Deployment
        identifier: model_deployment
        type: CD
        spec:
          execution:
            steps:
              - step:
                  name: Register Model in MLflow
                  identifier: register_model
                  type: Run
                  spec:
                    command: |
                      python scripts/register_model.py \
                        --model-name fraud_detection_gbm \
                        --stage Staging

              - step:
                  name: Deploy to Staging Endpoint
                  identifier: deploy_staging
                  type: K8sApply
                  spec:
                    filePaths:
                      - kubernetes/model-serving/staging-deployment.yaml

              - step:
                  name: Run Integration Tests
                  identifier: integration_tests
                  type: Run
                  spec:
                    command: |
                      pytest tests/integration/ \
                        --endpoint $STAGING_ENDPOINT \
                        --min-predictions-per-second 100

              - step:
                  name: Promote to Production
                  identifier: promote_production
                  type: Run
                  spec:
                    command: |
                      python scripts/promote_model.py \
                        --model fraud_detection_gbm \
                        --from-stage Staging \
                        --to-stage Production
```

### Harness AI Agents

Harness AI embeds AI agents directly into the SDLC workflow:

**AIDA (AI Development Assistant)**: generates pipeline YAML from natural language
descriptions, explains pipeline failures in plain English, suggests fixes for broken
stages, and writes remediation steps automatically.

**AI SRE Agent**: monitors deployed services and ML endpoints; detects anomalies in
latency, error rates, and prediction distributions; triggers rollbacks or alerts
without human intervention.

**AI Code Agent**: reviews pull requests, suggests improvements, flags security
issues in ML code (hardcoded secrets, unsafe deserialization of model artifacts).

---

## 4. AI Agents — Theory and Architecture {#agents-theory}

> **Source**: Wang, L., et al. (2024). A Survey on Large Language Model based Autonomous
> Agents. *Frontiers of Computer Science*, 18(6), 186345. arXiv:2308.11432.
> Xi, Z., et al. (2023). The Rise and Potential of Large Language Model Based Agents:
> A Survey. arXiv:2309.07864.

### What AI Agents Are

An AI agent is a system that perceives its environment, reasons about a goal, plans
a sequence of actions, executes those actions via tools, and iterates based on
feedback — all autonomously or with minimal human intervention. LLM-based agents use
a large language model as the reasoning and planning core.

The key distinction from a simple LLM call: an agent operates in a loop —
perceive → reason → act → observe → repeat — until the goal is achieved or a
stopping condition is met. The LLM acts as the "brain"; tools, APIs, databases,
and code executors act as the "hands."

### Agent Architecture

```
┌─────────────────────────────────────────────────────┐
│                    AI AGENT LOOP                    │
│                                                     │
│  Perception          Reasoning            Action    │
│  ──────────          ─────────            ──────    │
│  User goal     →    LLM Core        →    Tools      │
│  Observations  →    (Planning,      →    APIs       │
│  Tool outputs  →    Reflection,     →    Code exec  │
│  Memory        →    Chain-of-       →    File I/O   │
│                     Thought)        →    Web search │
│                         │                           │
│                         ▼                           │
│                    Memory Systems                   │
│                    ───────────────                  │
│                    Short-term (context window)      │
│                    Long-term (vector store / DB)    │
│                    Episodic (conversation history)  │
│                    Semantic (knowledge graph)       │
└─────────────────────────────────────────────────────┘
```

### Four Core Components (Wang et al., 2024)

**1. Profiling**: the agent's role, persona, and goal. Defined in the system prompt.
Determines how the LLM interprets tasks and communicates results.

**2. Memory**: what the agent knows and remembers across steps.
- In-context (short-term): the conversation history in the context window. Limited by
  context length. All current LLM reasoning operates here.
- External (long-term): vector databases (Chroma, Pinecone, Weaviate) storing embeddings
  of past interactions, documents, and intermediate results. Retrieved via semantic search.
- Episodic: structured records of past experiences (what worked, what failed) used for
  learning and self-improvement.

**3. Planning**: how the agent decomposes goals into steps.
- Chain-of-Thought (Wei et al., 2022): reason step-by-step before acting
- ReAct (Yao et al., 2023): interleave reasoning and action in a structured loop
- Reflexion (Shinn et al., 2023): reflect on past failures to improve future plans
- Tree-of-Thought (Yao et al., 2023): explore multiple reasoning paths simultaneously

**4. Action**: what the agent can do.
- Tool use: search, calculator, code execution, API calls, file read/write
- Memory operations: retrieve from vector store, write to long-term memory
- Agent interactions: call other agents (multi-agent systems)
- External world: browser automation, form filling, email sending

---

## 5. ReAct — Reasoning and Acting {#react}

> **Source**: Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in
> Language Models. *ICLR 2023*. arXiv:2210.03629.

### ReAct Pattern

ReAct interleaves **reasoning** (Thought) and **acting** (Action) in a structured
loop, with observation feedback after each action. This alternation grounds the
agent's reasoning in real tool outputs — preventing hallucination of results.

```
Thought_t   → What do I know? What should I do next?
Action_t    → tool_name(arguments)         ← calls an external tool
Observation_t → [tool output]              ← real result from the environment
Thought_{t+1} → What did I learn? What next?
Action_{t+1} → ...
...
Thought_N → I have enough information.
Answer → final response to the user
```

### ReAct Implementation (LangChain)

```python
from __future__ import annotations

import os
import logging
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain import hub

logger = logging.getLogger(__name__)


# --- Define tools the agent can use ---

@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query against the data warehouse and return results as a string.
    Use for any question that requires querying business data.

    Args:
        sql: Valid SQL SELECT query. Use snake_case table names.
    """
    import pandas as pd
    from sqlalchemy import create_engine, text
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as conn:
        result = pd.read_sql(text(sql), conn)
    return result.to_string(index=False)


@tool
def run_python(code: str) -> str:
    """
    Execute Python code and return stdout. Use for calculations,
    data transformations, and statistical computations.

    Args:
        code: Valid Python code string.
    """
    import io, contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(code, {})   # noqa: S102 — production: use a sandboxed executor
    return output.getvalue() or "Executed successfully (no output)"


@tool
def search_documentation(query: str) -> str:
    """
    Search internal documentation and data catalog for schema definitions,
    metric definitions, and business context.

    Args:
        query: Natural language search query.
    """
    # Replace with actual vector store retrieval in production
    return f"[Documentation search result for: {query}]"


def build_data_analyst_agent() -> AgentExecutor:
    """
    Build a ReAct agent that answers business questions by querying data,
    running Python computations, and searching documentation.
    """
    llm = ChatAnthropic(model="claude-opus-4-5", temperature=0)
    tools = [query_database, run_python, search_documentation]

    # ReAct prompt from LangChain Hub (or define a custom system prompt)
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,        # logs Thought/Action/Observation for debugging
        max_iterations=10,   # prevent infinite loops
        handle_parsing_errors=True,
    )


# Usage
agent_executor = build_data_analyst_agent()
result = agent_executor.invoke({
    "input": "What was the MoM revenue growth in APAC for Q1 2024? "
             "Show the calculation step by step."
})
print(result["output"])
```

### Reflexion — Self-Improvement via Verbal Reinforcement

Reflexion (Shinn et al., 2023) adds a self-evaluation loop: after each failed
attempt, the agent reflects on what went wrong and generates a verbal plan for
improvement, stored in its working memory.

```
Episode 1: Try → Fail → Reflect (store verbal feedback in memory)
Episode 2: Try (with reflection from memory) → Fail → Reflect
Episode 3: Try (with accumulated reflections) → Succeed
```

This enables an agent to improve over multiple attempts without gradient-based
training — verbal feedback replaces reward signals.

---

## 6. Multi-Agent Systems — AutoGen, CrewAI, LangGraph {#multi-agent}

> **Source**: Wu, Q., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications
> via Multi-Agent Conversation Framework. arXiv:2308.08155.
> Hong, S., et al. (2023). MetaGPT: Meta Programming for Multi-Agent Collaborative
> Framework. arXiv:2308.00352.

### Why Multi-Agent Systems

Single-agent systems have limitations: the context window bounds what one agent can
hold in memory; complex tasks require diverse specialization; sequential planning
is slow for tasks with independent subtasks. Multi-agent systems address these by:

1. **Specialization**: each agent has a defined role and tool set (data analyst,
   code reviewer, domain expert)
2. **Parallelism**: independent subtasks run concurrently across agents
3. **Error checking**: one agent's output is reviewed by another before acceptance
4. **Scale**: distribute context across agents; no single agent must hold everything

### AutoGen — Conversational Multi-Agent Framework

```python
from __future__ import annotations

import autogen
import os

# Configuration for Claude (Anthropic) as the LLM backend
config_list = [
    {
        "model": "claude-opus-4-5",
        "api_key": os.environ["ANTHROPIC_API_KEY"],
        "api_type": "anthropic",
    }
]

llm_config = {"config_list": config_list, "temperature": 0, "cache_seed": 42}

# Data Science AutoGen pattern: orchestrator + specialists
orchestrator = autogen.AssistantAgent(
    name="DataScienceOrchestrator",
    llm_config=llm_config,
    system_message="""You are a senior data science lead. Coordinate the team to
    solve analytical problems. Delegate to specialists, review their outputs,
    and synthesize a final answer. When all tasks are complete, say TERMINATE.""",
)

analyst = autogen.AssistantAgent(
    name="DataAnalyst",
    llm_config=llm_config,
    system_message="""You are a data analyst. Write SQL queries and Python code
    to explore data, compute metrics, and produce statistical summaries.
    Always validate your results before reporting.""",
)

ml_engineer = autogen.AssistantAgent(
    name="MLEngineer",
    llm_config=llm_config,
    system_message="""You are an ML engineer. Design and implement model training
    pipelines, select appropriate algorithms, tune hyperparameters, and evaluate
    model performance using appropriate metrics for the task.""",
)

# User proxy executes code locally
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",         # fully autonomous
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False,           # set True in production for isolation
    },
)

# Group chat: all agents communicate in a shared channel
group_chat = autogen.GroupChat(
    agents=[orchestrator, analyst, ml_engineer, user_proxy],
    messages=[],
    max_round=20,
    speaker_selection_method="auto",   # LLM decides who speaks next
)

manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# Start the multi-agent conversation
user_proxy.initiate_chat(
    manager,
    message="""Build a churn prediction model for the telecom dataset in
    /data/telecom_churn.csv. The analyst should explore the data first,
    the ML engineer should train and evaluate three models, and report
    which one generalizes best with a brief explanation.""",
)
```

### LangGraph — Stateful Agent Workflows

LangGraph models multi-agent workflows as directed graphs, enabling complex control
flow (loops, conditional branching, human-in-the-loop checkpoints) that is difficult
to express in linear chains.

```python
from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
import operator

llm = ChatAnthropic(model="claude-opus-4-5", temperature=0)


class AgentState(TypedDict):
    """Shared state passed between all nodes in the graph."""
    messages: Annotated[list, operator.add]
    data_profile: dict
    model_metrics: dict
    approved: bool


def data_exploration_node(state: AgentState) -> AgentState:
    """Node 1: Explore and profile the dataset."""
    response = llm.invoke([
        {"role": "user", "content": f"Profile this dataset and identify quality issues: {state['messages'][-1]}"}
    ])
    return {"messages": [response], "data_profile": {"status": "complete"}}


def model_training_node(state: AgentState) -> AgentState:
    """Node 2: Train models based on the data profile."""
    response = llm.invoke([
        {"role": "user", "content": f"Train GBM models given this profile: {state['data_profile']}"}
    ])
    return {"messages": [response], "model_metrics": {"auc": 0.92, "f1": 0.87}}


def review_node(state: AgentState) -> AgentState:
    """Node 3: Review model quality — conditional branching gate."""
    metrics = state["model_metrics"]
    approved = metrics.get("auc", 0) >= 0.85 and metrics.get("f1", 0) >= 0.70
    return {"approved": approved, "messages": [{"content": f"Review result: {'APPROVED' if approved else 'REJECTED'}"}]}


def should_deploy(state: AgentState) -> str:
    """Conditional edge: route to deployment or back to training."""
    return "deploy" if state["approved"] else "retrain"


def deployment_node(state: AgentState) -> AgentState:
    """Node 4a: Deploy approved model."""
    return {"messages": [{"content": "Model deployed to staging endpoint."}]}


def retraining_node(state: AgentState) -> AgentState:
    """Node 4b: Retrain with adjusted hyperparameters."""
    return {"messages": [{"content": "Retraining with adjusted parameters..."}]}


# Build the workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("explore",  data_exploration_node)
workflow.add_node("train",    model_training_node)
workflow.add_node("review",   review_node)
workflow.add_node("deploy",   deployment_node)
workflow.add_node("retrain",  retraining_node)

workflow.set_entry_point("explore")
workflow.add_edge("explore",  "train")
workflow.add_edge("train",    "review")
workflow.add_conditional_edges("review", should_deploy, {"deploy": "deploy", "retrain": "retrain"})
workflow.add_edge("retrain",  "train")   # loop back for retraining
workflow.add_edge("deploy",   END)

app = workflow.compile()
result = app.invoke({"messages": ["Train a fraud detection model on orders dataset."]})
```

---

## 7. Model Context Protocol (MCP) {#mcp}

> **Source**: Anthropic (2024). *Model Context Protocol Specification*.
> https://modelcontextprotocol.io · MCP GitHub. https://github.com/modelcontextprotocol

### What MCP Is

The Model Context Protocol (MCP) is an open standard introduced by Anthropic that
defines how AI models (LLMs) communicate with external data sources, tools, and
services. MCP provides a universal, vendor-neutral protocol for connecting AI
applications to any backend — replacing custom, one-off integrations with a
standardized interface.

MCP is to AI tool integration what REST/HTTP is to web APIs: a common protocol that
both sides implement, enabling any MCP-compatible AI client to connect to any
MCP-compatible server without custom integration code.

### MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Architecture                     │
│                                                         │
│  Host Application                                       │
│  (Claude Desktop, IDE, custom app)                      │
│         │                                               │
│         │  MCP Client (embedded in host)                │
│         │         │                                     │
│         │  ┌──────┴──────────────────────┐             │
│         │  │     MCP Transport Layer     │             │
│         │  │  stdio / HTTP+SSE / WebSocket│             │
│         │  └──────┬──────────────────────┘             │
│         │         │                                     │
│  MCP Servers (one per data source / tool):             │
│    ├── Database MCP Server (PostgreSQL queries)         │
│    ├── File System MCP Server (read/write files)        │
│    ├── GitHub MCP Server (repos, PRs, issues)           │
│    ├── Slack MCP Server (messages, channels)            │
│    └── Custom Data Science MCP Server                   │
│         (ML model inference, dataset access, EDA tools) │
└─────────────────────────────────────────────────────────┘
```

### MCP Core Primitives

| Primitive | Description | Example |
|---|---|---|
| **Tools** | Functions the LLM can call to perform actions or fetch data | `run_sql_query`, `train_model`, `get_dataset_schema` |
| **Resources** | Data sources the LLM can read (files, database records, API responses) | `dataset://orders/latest`, `model://fraud_detection/v2` |
| **Prompts** | Reusable prompt templates with defined arguments | A "data exploration" prompt template the user can invoke |
| **Sampling** | Server requests the client LLM to generate text | Server asks Claude to generate a SQL query given a schema |

### Building a Data Science MCP Server

```python
# mcp_server/data_science_server.py
# MCP server exposing data science tools to any MCP-compatible AI client
# Install: uv add mcp anthropic

from __future__ import annotations

import logging
import json
import pandas as pd
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, Resource
import mcp.server.stdio

logger = logging.getLogger(__name__)
app = Server("data-science-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Expose available data science tools to the MCP client."""
    return [
        Tool(
            name="run_eda",
            description=(
                "Run exploratory data analysis on a CSV or Parquet dataset. "
                "Returns statistical summary, missing value counts, data types, "
                "and correlation matrix."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the dataset file (CSV or Parquet).",
                    },
                    "target_column": {
                        "type": "string",
                        "description": "Optional target variable column name for supervised context.",
                    },
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="train_model",
            description=(
                "Train a GBM model (XGBoost, LightGBM, or CatBoost) on a dataset "
                "and return evaluation metrics. Model is saved to MLflow."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "target_column": {"type": "string"},
                    "algorithm": {
                        "type": "string",
                        "enum": ["xgboost", "lightgbm", "catboost"],
                    },
                    "task": {
                        "type": "string",
                        "enum": ["classification", "regression"],
                    },
                },
                "required": ["file_path", "target_column", "algorithm", "task"],
            },
        ),
        Tool(
            name="query_data_catalog",
            description="Search the data catalog for available datasets, their schemas, and owners.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query for the catalog.",
                    }
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from the MCP client (LLM)."""

    if name == "run_eda":
        path = arguments["file_path"]
        target = arguments.get("target_column")
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_parquet(path)

        summary = {
            "shape": list(df.shape),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "statistics": json.loads(df.describe().to_json()),
        }
        if target and target in df.columns:
            summary["target_distribution"] = df[target].value_counts().to_dict()

        return [TextContent(type="text", text=json.dumps(summary, indent=2))]

    elif name == "train_model":
        # Placeholder — in production: import and run the actual training pipeline
        return [TextContent(type="text", text=json.dumps({
            "status": "training_complete",
            "algorithm": arguments["algorithm"],
            "metrics": {"auc": 0.91, "f1": 0.85, "precision": 0.88, "recall": 0.82},
            "mlflow_run_id": "abc123-placeholder",
        }, indent=2))]

    elif name == "query_data_catalog":
        # Placeholder — in production: query Atlan, Unity Catalog, or OpenMetadata API
        return [TextContent(type="text", text=f"Found 3 datasets matching '{arguments['query']}'")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    """Run the MCP server over stdio transport."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="data-science-mcp-server",
                server_version="1.0.0",
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Client configuration** (Claude Desktop `config.json`):

```json
{
  "mcpServers": {
    "data-science": {
      "command": "uv",
      "args": ["run", "python", "/path/to/mcp_server/data_science_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host:5432/db",
        "MLFLOW_TRACKING_URI": "http://localhost:5000"
      }
    }
  }
}
```

---

## 8. Model Deployment Patterns {#deployment}

### Deployment Strategies

| Pattern | Description | When to Use |
|---|---|---|
| **Blue-Green** | Two identical environments; traffic switches instantly from Blue (old) to Green (new) | Zero-downtime deployments; easy rollback by switching back |
| **Canary Release** | Route a small % of traffic (1–5%) to the new model; monitor metrics; gradually increase | Detect regressions with minimal impact; A/B test model performance |
| **Shadow Mode** | New model receives all traffic but its predictions are not served — only logged for comparison | Validate a new model against production data without risk |
| **A/B Test** | Two models serve different user segments; measure business KPI impact | Statistical validation of model improvement on business metrics |
| **Champion-Challenger** | Production model (champion) vs. new model (challenger) on a subset of requests | Structured process for model replacement with governance |

### Model Serving — FastAPI + MLflow

```python
from __future__ import annotations

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time

logger = logging.getLogger(__name__)
app = FastAPI(title="ML Model Serving API", version="1.0.0")

MODEL_URI: str = "models:/fraud_detection_gbm/Production"
model = mlflow.pyfunc.load_model(MODEL_URI)


class PredictionRequest(BaseModel):
    features: dict[str, float | int | str]


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str
    latency_ms: float


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Serve predictions from the Production-stage MLflow model.
    Logs latency for monitoring.
    """
    start = time.perf_counter()
    try:
        df = pd.DataFrame([request.features])
        result = model.predict(df)
        latency_ms = (time.perf_counter() - start) * 1000

        logger.info("Prediction: %s | Latency: %.2fms", result, latency_ms)

        return PredictionResponse(
            prediction=int(result[0]),
            probability=float(result[0]),
            model_version=MODEL_URI,
            latency_ms=latency_ms,
        )
    except Exception as e:
        logger.error("Prediction error: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "model": MODEL_URI}
```

---

## 9. Model Monitoring and Drift Detection {#monitoring}

> **Source**: Gama, J., et al. (2014). A survey on concept drift adaptation. *ACM
> Computing Surveys*, 46(4). · Evidently AI Documentation. https://docs.evidentlyai.com

### Types of Drift

| Type | Definition | Impact |
|---|---|---|
| **Data drift** (covariate shift) | P(X) changes but P(y\|X) is stable — feature distributions shift | Model predictions may be based on unseen input patterns |
| **Concept drift** | P(y\|X) changes — the relationship between features and target changes | Model is fundamentally wrong even for familiar inputs |
| **Label drift** | P(y) changes — class distribution shifts | Decision threshold needs recalibration |
| **Prediction drift** | Distribution of ŷ shifts | Leading indicator of data or concept drift |

### Drift Detection with Evidently AI

```python
from __future__ import annotations

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.metrics import DatasetDriftMetric, ColumnDriftMetric
import logging

logger = logging.getLogger(__name__)


def run_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    output_path: str = "drift_report.html",
    drift_threshold: float = 0.05,
) -> dict:
    """
    Detect data drift between reference (training) and current (production) data.

    Uses the Kolmogorov-Smirnov test for numerical features and chi-squared
    for categorical features. Triggers a retraining alert if overall drift
    is detected above threshold.

    Args:
        reference_data: Training data distribution (baseline).
        current_data: Current production data to compare.
        drift_threshold: Proportion of drifted columns above which
                         retraining is recommended.

    Returns:
        Dictionary with drift status, drifted columns, and recommendation.
    """
    report = Report(metrics=[
        DatasetDriftMetric(drift_share_threshold=drift_threshold),
        DataDriftPreset(),
    ])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html(output_path)

    result = report.as_dict()
    drift_detected = result["metrics"][0]["result"]["dataset_drift"]
    share_drifted = result["metrics"][0]["result"]["share_of_drifted_columns"]

    recommendation = "RETRAIN" if drift_detected else "MONITOR"
    logger.warning(
        "Drift report: detected=%s, share_drifted=%.2f%%, recommendation=%s",
        drift_detected, share_drifted * 100, recommendation
    )

    return {
        "drift_detected": drift_detected,
        "share_drifted_columns": share_drifted,
        "recommendation": recommendation,
        "report_path": output_path,
    }
```

---

## 10. Edge ML and IoT Deployment {#edge-iot}

> **Reference**: Warden, P., & Situnayake, D. (2019). *TinyML: Machine Learning with
> TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*. O'Reilly.
> TensorFlow Lite Documentation. https://www.tensorflow.org/lite

### Edge ML Architecture

Edge ML deploys trained models directly on IoT devices, microcontrollers, or edge
servers — running inference locally without a round-trip to a cloud API. This
enables low-latency inference, offline operation, and privacy-preserving processing.

```
Cloud Training Pipeline                Edge Deployment
──────────────────────                 ──────────────────────────────
Data Lake                              Sensor → MCU / Edge Device
  → Model Training                       → Quantized TFLite model
  → Evaluation                           → Local inference
  → TFLite Conversion                    → Result (classification/detection)
  → Quantization (INT8)                  → Optional: send only anomalies to cloud
  → OTA Push to devices
```

### Practical Case — ESP32 + Claude via MCP

This case demonstrates the integration of IoT hardware (ESP32 microcontroller),
an ML backend, and an LLM (Claude) through MCP for natural language control.

**Architecture**:
```
User (natural language) → Claude (via MCP)
                               │
                         MCP Tool calls
                               │
                    Python Backend Server
                     ├── Command parser
                     ├── TCP/WiFi client
                     └── Protocol mapping
                               │
                         WiFi (TCP/UDP)
                               │
                         ESP32 Firmware
                     ├── Motor controller
                     ├── Camera (OV2640)
                     └── Sensor array
```

**Key engineering decisions in this pattern**:

1. **Firmware reprogramming**: flash custom firmware that connects the ESP32 to an
   existing WiFi network (instead of the device acting as an access point). This
   enables simultaneous internet access for the backend while communicating with
   the device locally.

2. **Static IP assignment**: assign a fixed IP to the ESP32 via DHCP reservation
   (MAC-to-IP binding in router settings). This enables consistent discovery without
   mDNS or dynamic lookup.

3. **Protocol reverse engineering**: inspect actual TCP/UDP packets using Wireshark
   when official documentation is incomplete or incorrect. Capture traffic between
   the official app and the device to discover the real command protocol.

4. **MCP server as the bridge**: the MCP server translates Claude's structured tool
   calls into the device-specific TCP/UDP byte sequences. Claude never directly
   touches the hardware protocol — the MCP server encapsulates all hardware-specific logic.

```python
# mcp_server/robot_controller_server.py
# MCP server bridging Claude ↔ ESP32 robot over WiFi

from __future__ import annotations

import asyncio
import socket
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from mcp.server.models import InitializationOptions

logger = logging.getLogger(__name__)
app = Server("robot-controller-mcp")

# Hardware configuration — externalize to environment variables in production
ROBOT_IP: str = "192.168.1.100"   # Static IP assigned to ESP32
ROBOT_PORT: int = 8889             # Discovered via protocol reverse engineering
COMMAND_TIMEOUT: float = 2.0


def send_robot_command(command_bytes: bytes) -> str:
    """Send a raw TCP command to the ESP32 and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(COMMAND_TIMEOUT)
        s.connect((ROBOT_IP, ROBOT_PORT))
        s.sendall(command_bytes)
        try:
            response = s.recv(1024)
            return response.decode("utf-8", errors="replace")
        except socket.timeout:
            return "OK (no response expected)"


# Protocol map — discovered via Wireshark packet capture
COMMAND_MAP: dict[str, bytes] = {
    "forward":    b"\x01\x00\x64\x00",
    "backward":   b"\x02\x00\x64\x00",
    "left":       b"\x03\x00\x64\x00",
    "right":      b"\x04\x00\x64\x00",
    "stop":       b"\x00\x00\x00\x00",
    "camera_on":  b"\x10\x01\x00\x00",
    "camera_off": b"\x10\x00\x00\x00",
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="control_robot",
            description=(
                "Control the ELEGOO Smart Robot Car. Send movement and camera commands. "
                "The robot is on the local WiFi network at a fixed IP address."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": list(COMMAND_MAP.keys()),
                        "description": "Robot command to execute.",
                    },
                    "duration_seconds": {
                        "type": "number",
                        "description": "How long to execute the command (default: 1.0s).",
                        "default": 1.0,
                    },
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="get_robot_status",
            description="Query the robot's current status: battery level, active sensors.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "control_robot":
        cmd = arguments["command"]
        duration = float(arguments.get("duration_seconds", 1.0))

        if cmd not in COMMAND_MAP:
            return [TextContent(type="text", text=f"Unknown command: {cmd}")]

        response = send_robot_command(COMMAND_MAP[cmd])
        await asyncio.sleep(duration)
        send_robot_command(COMMAND_MAP["stop"])

        return [TextContent(type="text", text=f"Executed '{cmd}' for {duration}s. Response: {response}")]

    elif name == "get_robot_status":
        status_cmd = b"\xFF\x00\x00\x00"   # status query byte sequence
        response = send_robot_command(status_cmd)
        return [TextContent(type="text", text=f"Robot status: {response}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream,
            InitializationOptions(
                server_name="robot-controller-mcp",
                server_version="1.0.0",
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 11. References {#references}

- Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine Learning Operations (MLOps). *IEEE Access*, 11, 31866–31879.
- Wang, L., et al. (2024). A Survey on Large Language Model based Autonomous Agents. *Frontiers of Computer Science*, 18(6). arXiv:2308.11432.
- Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. arXiv:2210.03629.
- Shinn, N., et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. *NeurIPS 2023*. arXiv:2303.11366.
- Wu, Q., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155.
- Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS 2022*. arXiv:2201.11903.
- Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *NeurIPS 2023*. arXiv:2305.10601.
- Gama, J., et al. (2014). A survey on concept drift adaptation. *ACM Computing Surveys*, 46(4).
- Warden, P., & Situnayake, D. (2019). *TinyML*. O'Reilly.
- Harness Developer Hub. https://developer.harness.io
- MLflow Documentation. https://mlflow.org/docs/latest
- Model Context Protocol Specification. https://modelcontextprotocol.io
- Evidently AI Documentation. https://docs.evidentlyai.com
- TensorFlow Lite. https://www.tensorflow.org/lite
- Google (2020). Practitioners Guide to MLOps. https://cloud.google.com/resources/mlops-whitepaper
