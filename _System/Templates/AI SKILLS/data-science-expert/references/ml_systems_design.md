# ML Systems Design — Production-Ready Applications

> **Primary reference**: Huyen, C. (2022). *Designing Machine Learning Systems: An
> Iterative Process for Production-Ready Applications*. O'Reilly.
> Additional references: Sculley, D., et al. (2015). Hidden Technical Debt in Machine
> Learning Systems. *NeurIPS 2015*. · Breck, E., et al. (2017). The ML Test Score.
> *IEEE Big Data 2017*. · Kleppmann, M. (2017). *Designing Data-Intensive Applications*.
> O'Reilly. · Google (2020). *Practitioners Guide to MLOps*.
> https://cloud.google.com/resources/mlops-whitepaper

## Table of Contents

1. [The Iterative ML System Design Framework](#framework)
2. [Framing ML Problems from Business Objectives](#framing)
3. [Training Data — Sampling Strategies](#sampling)
4. [Training Data — Labeling and Weak Supervision](#labeling)
5. [Class Imbalance — Strategies and Tradeoffs](#class-imbalance)
6. [Feature Engineering from a Systems Perspective](#feature-engineering)
7. [Model Development — Baselines and Iterative Improvement](#model-development)
8. [Batch vs. Online vs. Streaming Prediction](#prediction-serving)
9. [Data Distribution Shifts — Rigorous Taxonomy](#distribution-shifts)
10. [Continual Learning](#continual-learning)
11. [Test in Production](#test-in-production)
12. [Slice-Based Evaluation and Fairness](#fairness)
13. [ML Systems Design Checklist](#checklist)
14. [References](#references)

---

## 1. The Iterative ML System Design Framework {#framework}

> Huyen (2022), Ch. 1–2: "ML in production is fundamentally different from ML in
> research. In research, you optimize for a single metric. In production, you optimize
> for multiple metrics that often conflict, under constraints that keep changing."

The central thesis of Huyen (2022): ML systems are not static artifacts — they are
living systems that degrade as the world changes. Designing for production requires
an iterative loop that continuously revisits every component.

```
                    THE ITERATIVE ML SYSTEM DESIGN LOOP
                    ─────────────────────────────────────

          ┌─────────────────────────────────────────────┐
          │           BUSINESS REQUIREMENTS             │
          │  What problem? What metric? What constraint? │
          └───────────────────┬─────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────────┐
          │              DATA ENGINEERING               │
          │  Collection · Storage · Processing · Pipelines│
          └───────────────────┬─────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────────┐
          │            FEATURE ENGINEERING              │
          │  Feature selection · Creation · Validation  │
          └───────────────────┬─────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────────┐
          │            MODEL DEVELOPMENT                │
          │  Algorithm · Training · Evaluation · Debug  │
          └───────────────────┬─────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────────┐
          │          DEPLOYMENT & SERVING               │
          │  Batch · Online · Streaming · Edge          │
          └───────────────────┬─────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────────┐
          │         MONITORING & OBSERVABILITY          │
          │  Data drift · Model drift · Business KPIs  │
          └───────────────────┬─────────────────────────┘
                              │
               ───────────────┘  (continuous feedback)
               │
               ▼  ITERATE — any layer may trigger changes upstream
```

**Why every layer feeds back to every other**: a drift detected in monitoring may
require new training data (data engineering), new features (feature engineering),
a retrained model (model development), or a changed serving pattern (deployment).
The system is never "done."

### Key Properties of Production ML Systems (Huyen, 2022)

| Property | Definition | Why it conflicts with research ML |
|---|---|---|
| **Reliability** | System performs correctly even under adversarial inputs, edge cases, and infrastructure failures | Research accepts clean, curated inputs |
| **Scalability** | System handles growth in data volume, request volume, and model complexity | Research benchmarks on fixed datasets |
| **Maintainability** | Different teams (DS, DE, MLOps, product) can work on and understand the system | Research is typically single-person |
| **Adaptability** | System can be updated to new data distributions without major refactoring | Research models are trained once |

---

## 2. Framing ML Problems from Business Objectives {#framing}

> Huyen (2022), Ch. 2: "Before you can design an ML system, you must understand what
> problem you're solving. This sounds obvious but is where most ML projects fail."

### Business Metric → ML Metric Mapping

ML objectives and business objectives are rarely the same. Every ML system must map
its optimization target to the business metric it is intended to improve.

```
BUSINESS OBJECTIVE          ML OBJECTIVE (PROXY)           RISK OF MISMATCH
─────────────────────────────────────────────────────────────────────────────
Maximize revenue         →  Maximize CTR (click-through)   High CTR ≠ high revenue
                                                            if low-value items are clicked

Reduce fraud losses      →  Maximize recall of fraud       High recall at precision=0.01
                                                            → 99% of flagged txns legitimate
                                                            → customer experience destroyed

Improve user retention   →  Maximize engagement time       Addictive content maximizes
                                                            engagement but destroys retention

Reduce customer churn    →  Minimize churn prediction MSE  RMSE improvement ≠ fewer churned
                                                            customers if decision threshold
                                                            is wrong

Clinical decision support → Maximize AUC                   AUC ignores calibration —
                                                            P(disease) = 0.6 vs. 0.9 both
                                                            "positive" but clinically differ
```

**Practical rule**: always define both the ML metric *and* the business KPI it is
supposed to move, with an explicit hypothesis linking them. Monitor both in production.
If the ML metric improves but the business KPI does not, the hypothesis was wrong.

### Requirements Classification

Before framing the ML problem, answer these four questions explicitly:

**1. Is ML the right tool?** ML requires sufficient labeled training data, acceptable
latency for model inference, and a pattern that generalizes. Problems with deterministic
rules, tiny datasets, or strict regulatory requirements for explicit logic may be better
served by rule engines, optimization solvers, or expert systems.

**2. What are the latency requirements?**
```
< 1 ms      → Rules or lookup tables only; ML inference is infeasible
1–10 ms     → Pre-computed batch predictions (offline) or highly optimized edge models
10–100 ms   → Online prediction with model caching; careful infrastructure design
100–500 ms  → Standard online ML serving; most recommendation and classification tasks
> 500 ms    → Batch prediction or document processing; user-facing async patterns
```

**3. What is the interpretability requirement?** High-stakes decisions (credit,
healthcare, legal) require explainable predictions. Tree-based models + SHAP are
the standard. Neural networks require LIME, integrated gradients, or attention visualization.

**4. What does the feedback loop look like?** (See Section 3 on natural labels)

---

## 3. Training Data — Sampling Strategies {#sampling}

> Huyen (2022), Ch. 4: "Sampling is one of the most underappreciated aspects of ML.
> Wrong sampling can introduce systematic biases that are invisible during training
> and only surface in production."

### Sampling Methods

```
SAMPLING METHODS FOR ML TRAINING DATA
──────────────────────────────────────────────────────────────────

Non-probability sampling (selection bias risk — cannot support statistical
inference; use only when probability sampling is operationally impossible):
  ├── Convenience sampling: use whatever data is easiest to collect
  │     Risk: systematic exclusion of hard-to-reach subpopulations
  ├── Quota sampling: establish fixed counts per group (e.g., 50%/50% split)
  │     then fill each quota by convenience — enforces distribution control
  │     but within-quota selection is non-random
  ├── Snowball / chain-referral: existing samples recruit similar samples
  │     Use: when the target population is hard to locate (rare conditions,
  │     niche user groups, fraud rings in graph data)
  └── Voluntary response: individuals self-select into the sample
        Example: open internet surveys — severe self-selection bias;
        over-represents people with strong opinions

Probability sampling (each sample has a known, non-zero selection probability):
  ├── Simple random sampling
  │     Every record has equal probability of selection (1/N)
  │     Problem: rare classes may be severely underrepresented
  │
  ├── Systematic sampling
  │     Sort the population; select every k-th record (k = N/n)
  │     Fast and deterministic; preserves ordering
  │     Risk: if data has a periodic pattern with period = k,
  │     systematic sampling will capture only one phase of the cycle
  │     Example: select every 10th transaction record
  │
  ├── Stratified sampling
  │     Partition the population into mutually exclusive strata
  │     (e.g., class label, region, age group, fraud vs. legitimate)
  │     Sample independently within each stratum — proportional or equal
  │     Proportional: stratum sample ∝ stratum size (maintains distribution)
  │     Equal: equal n per stratum (boosts rare class representation)
  │     Use for classification with imbalanced classes
  │
  ├── Cluster / conglomerate sampling
  │     Divide the population into naturally occurring groups (clusters):
  │     schools, hospitals, geographic regions, time windows
  │     Select entire clusters randomly — survey all members within them
  │     Advantage: logistically efficient when population spans locations
  │     Risk: within-cluster homogeneity inflates effective sample variance
  │     (members of the same school are more similar than random individuals)
  │     Use in ML: sample entire time windows, entire stores, or entire
  │     user cohorts rather than individual records
  │
  ├── Weighted / importance sampling
  │     Assign non-uniform probabilities to records
  │     Use to: oversample rare classes, undersample majorities,
  │     or re-weight historical data to match current production distribution
  │
  └── Reservoir sampling
        Sample k records uniformly from a stream of unknown length n
        Algorithm: fill reservoir with first k records;
                   for record i > k: with probability k/i, replace a
                   random reservoir element with the current record
        Use: sample from large files or streams without loading into memory
        See implementation below (Vitter 1985 Algorithm R)

Resampling (operates on an existing sample, not the original population):
  └── Bootstrap
        Draw n samples WITH REPLACEMENT from the original dataset of size n
        The non-selected records (~36.8% per bootstrap draw) form the
        out-of-bag (OOB) set — used as a validation set without a formal split
        Use: estimate uncertainty of any statistic, construct confidence
        intervals, power ensemble methods (bagging), assess model stability
        See Bootstrap section below
```

### Pre-Sampling Checklist

Before selecting a sampling strategy, answer these questions to avoid
introducing systematic bias that will be invisible at training time:

- What is the full population? Is the sampling frame (the list from which
  you actually sample) representative of it?
- How are the data distributed? Are rare classes, regions, or time periods
  at risk of underrepresentation?
- Are there data quality problems (missing values, duplicates, stale records)
  that should be resolved before sampling, not after?
- Which variables are correlated with the outcome variable AND with the
  probability of a record being in the dataset? These are confounders
  that require stratified or weighted sampling.
- What patterns or trends exist that a systematic or time-ordered sample
  might inadvertently capture or miss?
- What hypothesis is the sample intended to support? Does the sampling
  strategy provide the statistical power to test it?

### Reservoir Sampling — Implementation

```python
from __future__ import annotations

import random
from typing import Iterator


def reservoir_sample(stream: Iterator, k: int, seed: int = 42) -> list:
    """
    Sample k items uniformly from a stream of unknown length.
    Uses O(k) memory regardless of stream size.

    Vitter (1985) Algorithm R: each item in the stream has exactly k/n
    probability of appearing in the final sample, where n is the
    stream length.

    Args:
        stream: Any iterable — file lines, database cursor, Kafka consumer.
        k: Number of items to retain in the reservoir.

    Returns:
        List of k uniformly sampled items.
    """
    rng = random.Random(seed)
    reservoir: list = []

    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            # Replace a random element with probability k/(i+1)
            j = rng.randint(0, i)
            if j < k:
                reservoir[j] = item

    return reservoir
```

### Bootstrap Resampling — Theory and Implementation

Bootstrap is a resampling technique that estimates the sampling distribution of
any statistic by drawing repeated samples with replacement from the original dataset.
It is not a sampling method for the original data collection — it operates on data
you already have to quantify uncertainty.

**Mathematical foundation**: given n observations, each bootstrap sample draws n
records with replacement. On average, each bootstrap sample contains approximately
63.2% unique records (1 − 1/e ≈ 0.632). The remaining ~36.8% never selected form
the **out-of-bag (OOB)** set, which serves as a natural validation set.

```
BOOTSTRAP PROCESS
────────────────────────────────────────────────────────────────────────

Original dataset: [x₁, x₂, x₃, x₄, x₅, x₆, x₇, x₈, x₉, x₁₀]  (n = 10)

Bootstrap sample 1: [x₃, x₁, x₇, x₃, x₂, x₉, x₁, x₄, x₃, x₆]  (with replacement)
Bootstrap sample 2: [x₁, x₅, x₂, x₈, x₅, x₃, x₉, x₁, x₅, x₄]
Bootstrap sample 3: [x₂, x₇, x₁, x₁, x₆, x₄, x₈, x₂, x₇, x₃]
...
Bootstrap sample B: [...]

For each bootstrap sample b:
  Train model on sample b → evaluate on OOB set → record metric θ̂_b

Bootstrap distribution: {θ̂₁, θ̂₂, ..., θ̂_B}

95% confidence interval: [percentile(θ̂, 2.5), percentile(θ̂, 97.5)]
Bootstrap standard error: std({θ̂₁, ..., θ̂_B})
```

**Applications in data science**:
- **Confidence intervals for any metric**: AUC, F1, RMSE — without parametric assumptions
- **Ensemble learning — Bagging**: Random Forest trains each tree on a bootstrap sample; the OOB set provides unbiased accuracy estimates without a separate validation split
- **Model stability assessment**: high variance across bootstrap samples signals model instability or insufficient data
- **Feature importance uncertainty**: bootstrap distributions of feature importances reveal which features are consistently important vs. spuriously ranked

```python
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import roc_auc_score
from typing import Callable


def bootstrap_metric(
    y_true: np.ndarray,
    y_score: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> dict:
    """
    Compute bootstrap confidence interval for any binary classification metric.

    Draws n_bootstraps samples with replacement from (y_true, y_score),
    computes the metric on each, and returns the empirical confidence interval.
    Does not assume normality — valid for AUC, F1, precision, recall, and any
    other metric where the sampling distribution may be non-Gaussian.

    Args:
        y_true:    Ground-truth binary labels.
        y_score:   Predicted probabilities or scores.
        metric_fn: Any callable (y_true, y_score) -> float.
        n_bootstraps: Number of bootstrap draws (1000 standard; 5000 for publication).
        confidence_level: Confidence level for the interval (0.95 = 95% CI).

    Returns:
        Dictionary with point estimate, CI lower/upper, and bootstrap std error.
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)
    bootstrap_scores: list[float] = []

    for _ in range(n_bootstraps):
        idx = rng.integers(0, n, size=n)          # sample with replacement
        y_true_b  = y_true[idx]
        y_score_b = y_score[idx]

        # Skip degenerate samples (only one class — metric undefined)
        if len(np.unique(y_true_b)) < 2:
            continue

        bootstrap_scores.append(metric_fn(y_true_b, y_score_b))

    scores = np.array(bootstrap_scores)
    alpha = 1.0 - confidence_level
    lower = float(np.percentile(scores, 100 * alpha / 2))
    upper = float(np.percentile(scores, 100 * (1 - alpha / 2)))

    return {
        "point_estimate":   float(metric_fn(y_true, y_score)),
        "ci_lower":         lower,
        "ci_upper":         upper,
        "ci_width":         round(upper - lower, 4),
        "bootstrap_std_err": round(float(scores.std()), 4),
        "n_valid_bootstraps": len(bootstrap_scores),
    }


def bootstrap_model_stability(
    model: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    n_bootstraps: int = 200,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Assess model stability by training on bootstrap samples and evaluating OOB.

    High variance in OOB AUC across bootstrap samples → model is unstable:
    either insufficient data, excessive model complexity, or noisy features.

    Args:
        model: Any scikit-learn compatible estimator with predict_proba.
        n_bootstraps: Number of bootstrap training runs (200 is sufficient for stability).

    Returns:
        DataFrame with per-bootstrap OOB AUC, plus summary statistics.
    """
    rng = np.random.default_rng(seed)
    n = len(X)
    results = []

    for b in range(n_bootstraps):
        idx_in  = rng.integers(0, n, size=n)               # bootstrap sample
        idx_oob = np.setdiff1d(np.arange(n), idx_in)       # out-of-bag

        if len(np.unique(y.iloc[idx_oob])) < 2:
            continue   # skip if OOB has only one class

        model.fit(X.iloc[idx_in], y.iloc[idx_in])
        y_prob_oob = model.predict_proba(X.iloc[idx_oob])[:, 1]
        oob_auc = roc_auc_score(y.iloc[idx_oob], y_prob_oob)
        results.append({"bootstrap": b, "oob_auc": oob_auc})

    df = pd.DataFrame(results)
    df.attrs["mean_oob_auc"] = df["oob_auc"].mean()
    df.attrs["std_oob_auc"]  = df["oob_auc"].std()
    return df
```

---

## 4. Training Data — Labeling and Weak Supervision {#labeling}

> Huyen (2022), Ch. 4: "Getting good labels is often the biggest bottleneck in
> production ML, not modeling."

### Label Acquisition Spectrum

```
COST                                                            SCALE
HIGH ←────────────────────────────────────────────────────────→ HIGH

Hand labeling     Semi-supervision    Weak supervision    Natural labels
(gold standard)   (label propagation) (Snorkel / LFs)    (user behavior)

Expensive         Moderate            Low                 Free
Slow              Moderate            Fast                Real-time
Small scale       Medium scale        Large scale         Massive scale
High quality      Medium quality      Moderate quality    Noisy
```

### Natural Labels and Feedback Loops

**Natural labels** are labels generated automatically by the system's own feedback
— no human annotation required. They are the cheapest and most scalable labels.

```
NATURAL LABEL EXAMPLES:
  Click-through prediction  → whether the user clicked (feedback: seconds)
  Fraud detection           → chargeback filed (feedback: days to weeks)
  Recommendation system     → whether item was purchased (feedback: hours)
  Loan default prediction   → whether borrower defaulted (feedback: months)

FEEDBACK LOOP LENGTH:
  Short (< 1 hour)  → model can be updated daily or more frequently
  Medium (1 day–1 week) → weekly retraining cadence typical
  Long (> 1 month)  → proxy labels needed (e.g., partial engagement signals)
                        before true labels arrive
```

**The label delay problem**: when feedback arrives much later than the prediction,
you must decide how long to wait before treating an unlabeled prediction as a
negative. Too short → false negatives in training. Too long → stale training data.

### Weak Supervision — Programmatic Labeling

Weak supervision (Ratner et al., 2017 — Snorkel) uses labeling functions (LFs) —
heuristic rules, regex patterns, third-party models, or knowledge bases — to
generate noisy labels at scale, then aggregates them using a generative model.

```python
from __future__ import annotations

import numpy as np
from typing import Callable

# Define labeling functions — each returns a label {-1 (abstain), 0 (negative), 1 (positive)}
LabelingFunction = Callable[[dict], int]

def lf_keyword_fraud(record: dict) -> int:
    """Flag transactions with suspicious keywords."""
    suspicious = {"test", "xxx", "aaa", "123"}
    return 1 if any(w in str(record.get("description", "")).lower() for w in suspicious) else -1

def lf_large_amount(record: dict) -> int:
    """Flag unusually large transactions."""
    return 1 if record.get("amount", 0) > 10_000 else -1

def lf_foreign_country(record: dict) -> int:
    """Flag transactions from unexpected countries."""
    home_country = record.get("home_country", "US")
    txn_country  = record.get("txn_country", "US")
    return 1 if txn_country != home_country else -1

def lf_new_merchant(record: dict) -> int:
    """Transactions at merchants seen < 3 times in user history are suspicious."""
    return 1 if record.get("merchant_visit_count", 999) < 3 else -1


def majority_vote(
    records: list[dict],
    labeling_functions: list[LabelingFunction],
) -> np.ndarray:
    """
    Apply labeling functions and aggregate via majority vote.
    Returns -1 where no LF votes (all abstain).
    For production: replace with Snorkel's generative label model,
    which weights LFs by estimated accuracy and correlation.
    """
    n = len(records)
    L = np.full((n, len(labeling_functions)), -1, dtype=int)   # label matrix

    for j, lf in enumerate(labeling_functions):
        for i, record in enumerate(records):
            L[i, j] = lf(record)

    # Majority vote over non-abstaining LFs per record
    labels = np.full(n, -1, dtype=int)
    for i in range(n):
        votes = L[i][L[i] != -1]
        if len(votes) > 0:
            labels[i] = int(np.sign(votes.sum()))   # +1 if more positives, -1 if more negatives

    return labels
```

---

## 5. Class Imbalance — Strategies and Tradeoffs {#class-imbalance}

> Huyen (2022), Ch. 4: "Class imbalance is the norm, not the exception, in production
> ML. Fraud, medical diagnosis, anomaly detection — real positive rates of 0.1%–1%
> are common. Treating this as a symmetric classification problem produces models that
> always predict the majority class."

### The Imbalance Problem

Standard cross-entropy minimization with imbalanced data drives the model to predict
the majority class. A model that always predicts "not fraud" achieves 99.9% accuracy
on a dataset with 0.1% fraud — while being useless.

Accuracy is the wrong metric. For imbalanced data: use **precision, recall, F1,
AUROC, or AUPRC** (area under precision-recall curve — more informative than AUROC
when the positive class is rare).

### Strategy Comparison

```
STRATEGIES FOR CLASS IMBALANCE
────────────────────────────────────────────────────────────────────────────

1. RESAMPLING
   ├── Oversampling minority: duplicate minority samples (naïve) or
   │   synthesize new ones via SMOTE — interpolation in feature space
   │   Risk: memorization / overfit if naïve duplication
   │
   └── Undersampling majority: randomly drop majority samples
       Risk: discards information; use Tomek Links or NearMiss for informed removal

2. ALGORITHM-LEVEL
   ├── Class weights: scale loss by 1/class_frequency
   │   sklearn: class_weight='balanced'
   │   XGBoost: scale_pos_weight = neg_count / pos_count
   │
   └── Focal loss (Lin et al., 2017 — RetinaNet):
       FL(p_t) = −(1 − p_t)^γ log(p_t)    γ ∈ [0, 5]
       Down-weights easy examples (large p_t) → forces model to focus
       on hard, misclassified minority examples
       Standard in object detection; applies to any classification task

3. THRESHOLD TUNING
   Train with balanced loss; adjust decision threshold at inference.
   Default threshold = 0.5 is wrong for imbalanced data.
   Tune threshold on a held-out validation set to meet business requirements
   (e.g., minimum recall of 0.95 for fraud; then maximize precision at that recall)

4. ENSEMBLE METHODS
   ├── BalancedBaggingClassifier: each bag is balanced
   └── EasyEnsemble: ensemble of AdaBoost on balanced subsets
```

```python
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_recall_curve
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline


def handle_imbalance(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    strategy: str = "class_weight",
    target_recall: float = 0.90,
) -> dict:
    """
    Train a classifier with imbalance handling and tune decision threshold.

    Args:
        strategy: 'class_weight', 'smote', or 'threshold_only'
        target_recall: Minimum recall required on positive class.
                       Threshold is set to achieve this recall on validation set.

    Returns:
        Dictionary with model, optimal threshold, and validation metrics.
    """
    if strategy == "smote":
        pipeline = ImbPipeline([
            ("smote", SMOTE(random_state=42, k_neighbors=5)),
            ("model", LogisticRegression(max_iter=1000, random_state=42)),
        ])
        pipeline.fit(X_train, y_train)
        model = pipeline
    else:
        weight = "balanced" if strategy == "class_weight" else None
        model = LogisticRegression(class_weight=weight, max_iter=1000, random_state=42)
        model.fit(X_train, y_train)

    # Threshold tuning: find lowest threshold that meets recall requirement
    y_prob = model.predict_proba(X_val)[:, 1]
    precision_vals, recall_vals, thresholds = precision_recall_curve(y_val, y_prob)

    # Find thresholds where recall >= target
    valid_idx = np.where(recall_vals[:-1] >= target_recall)[0]
    if len(valid_idx) == 0:
        optimal_threshold = 0.5
    else:
        # Among valid thresholds, pick the one with highest precision
        best = valid_idx[np.argmax(precision_vals[valid_idx])]
        optimal_threshold = float(thresholds[best])

    y_pred = (y_prob >= optimal_threshold).astype(int)

    return {
        "model": model,
        "optimal_threshold": optimal_threshold,
        "classification_report": classification_report(y_val, y_pred, output_dict=True),
        "strategy_used": strategy,
    }
```

---

## 6. Feature Engineering from a Systems Perspective {#feature-engineering}

> Huyen (2022), Ch. 5: "Features are not just what you extract from data — they are
> the interface between your data and your model. Bad features make good models bad."

### Feature Leakage — The Silent Killer

Feature leakage occurs when a feature contains information about the label that would
not be available at inference time. Models with leaked features achieve near-perfect
training metrics and fail catastrophically in production.

```
LEAKAGE TAXONOMY
────────────────────────────────────────────────────────────────────────

TARGET LEAKAGE (most common):
  A feature that is derived from or highly correlated with the target
  AFTER the target is determined, but included as if it were available before.

  Example: predicting hospital readmission.
    Leaked feature: "discharge_medication_count" — derived after discharge decision.
    Why it leaks: the discharge decision IS the outcome proxy.

TRAIN-TEST CONTAMINATION:
  Information from the test set leaks into training via preprocessing.
  Example: StandardScaler fit on full dataset before train/test split.
  Prevention: ALWAYS fit preprocessing on train set only (see ml_evaluation.md §1)

TEMPORAL LEAKAGE:
  Using data from the future to predict events in the past.
  Example: using 2024 Q4 customer behavior to predict 2024 Q1 churn.
  Prevention: always sort by time before splitting; use walk-forward validation.

DETECTION:
  1. Unusually high accuracy on a simple model → suspect leakage
  2. A feature with correlation > 0.95 with the target → investigate provenance
  3. Permutation importance: if removing one feature drops performance 30%+ → investigate
  4. Check feature generation timestamp vs. label timestamp for every feature
```

### Feature Types and Engineering Patterns

```
FEATURE TYPE           ENGINEERING PATTERN                    TOOL
──────────────────────────────────────────────────────────────────────
Numeric                Log transform (right-skewed)            numpy
                       Box-Cox / Yeo-Johnson (general)        sklearn.PowerTransformer
                       Binning (capture non-linear effects)   pandas.cut / qcut
                       Interactions (x₁ × x₂)                PolynomialFeatures

Categorical (low card.) One-hot encoding                      pandas.get_dummies
                        Ordinal encoding (ordered categories)  sklearn.OrdinalEncoder

Categorical (high card.) Target encoding (mean of target)     category_encoders
                          Hashing trick (sparse features)      sklearn.FeatureHasher
                          Embedding (deep learning)            torch.nn.Embedding

Text                   TF-IDF                                 sklearn.TfidfVectorizer
                       Sentence embeddings                    sentence-transformers
                       Count vectorizer + SVD (LSA)           sklearn

Time series            Lag features: x(t-1), x(t-2)          pandas.shift
                       Rolling statistics: mean, std, min/max  pandas.rolling
                       Calendar: hour, day-of-week, month     pandas.dt
                       Cyclical encoding: sin/cos transforms
                         hour_sin = sin(2π × hour / 24)
                         hour_cos = cos(2π × hour / 24)

Geographic             Distance to landmark                    geopy
                       Cluster assignment (neighborhood)       KMeans on coords
                       H3 hexagonal grid index                 h3-py
```

### Cyclical Feature Encoding

```python
import numpy as np
import pandas as pd

def encode_cyclical(series: pd.Series, period: float) -> pd.DataFrame:
    """
    Encode a cyclical feature (hour, day of week, month) as sine/cosine pair.
    Preserves the circular nature: hour 23 is close to hour 0.

    Args:
        series: Numeric series representing position in cycle (e.g., hour 0-23).
        period: The full cycle length (24 for hours, 7 for days, 12 for months).

    Returns:
        DataFrame with _sin and _cos columns.
    """
    name = series.name or "feature"
    radians = 2 * np.pi * series / period
    return pd.DataFrame({
        f"{name}_sin": np.sin(radians),
        f"{name}_cos": np.cos(radians),
    }, index=series.index)
```

---

## 7. Model Development — Baselines and Iterative Improvement {#model-development}

> Huyen (2022), Ch. 6: "Always start with the simplest baseline that could possibly
> work. You can only know if a sophisticated model adds value if you know what a
> naive baseline achieves."

### Baseline Hierarchy

```
BASELINE PROGRESSION — start at the top, only move down when justified
──────────────────────────────────────────────────────────────────────

Level 0: Random / majority class
  Performance floor — anything below this is broken

Level 1: Simple heuristic rule
  Example (churn): "flag customer if no login in 30 days"
  Often surprisingly competitive; defines the "value of ML" threshold

Level 2: Simple statistical model
  Logistic regression, decision tree (max_depth=3)
  Fast, interpretable, establishes the linear signal baseline

Level 3: Gradient boosting (XGBoost / LightGBM / CatBoost)
  State-of-the-art for tabular data (see ml_evaluation.md §3)
  If GBM ≈ simple model → features lack signal, not model complexity

Level 4: Ensemble / neural / complex model
  Only justified if Level 3 is insufficient AND additional complexity
  is operationally sustainable (serving latency, retraining cost)
```

**Rule**: if adding model complexity does not improve the business metric by a
meaningful threshold (defined before training begins), do not accept the complex model.
Complexity is a liability: harder to debug, more expensive to serve, faster to drift.

### Debugging ML Models — A Systematic Framework

```
POOR MODEL PERFORMANCE DIAGNOSIS TREE
──────────────────────────────────────────────────────────────────

Start: Is performance below baseline?
  YES →
    Is training loss decreasing?
      NO → Implementation bug (gradient, loss function, data loading)
      YES →
        Is validation loss also decreasing?
          NO → Overfitting
               Fixes: more data, dropout, L1/L2, reduce model size, early stopping
          YES → Is validation loss below baseline?
                  NO → Underfitting
                       Fixes: more features, more model capacity, longer training
                  YES → Deployment / distribution shift problem
                        Fixes: check serving pipeline, monitor input distributions
```

---

## 8. Batch vs. Online vs. Streaming Prediction {#prediction-serving}

> Huyen (2022), Ch. 7: "The choice of prediction serving pattern is one of the most
> consequential infrastructure decisions in ML systems design."

```
PREDICTION SERVING PATTERNS — COMPARISON
─────────────────────────────────────────────────────────────────────────────

                BATCH              ONLINE (REQUEST-TIME)    STREAMING
                ──────────         ─────────────────────    ─────────────────
When           Pre-compute         At request time          Near-real-time
               (hourly/daily)      (per API call)           (as events arrive)

Latency        Minutes–hours       Milliseconds             Milliseconds–seconds

Freshness      Stale by design     Always fresh             Near-fresh

Throughput     Very high           Moderate                 High

Infrastructure Simple (batch job)  Inference server         Kafka + stream processor

Feature        Only batch          Batch + real-time        Batch + real-time
availability   features            features                 features (joins required)

Use cases      Recommendations,    Search ranking,          Fraud detection,
               reports, marketing  content scoring,         IoT anomaly detection,
               campaigns,          Q&A, chatbots            real-time personalization
               offline analytics

When to use    Predictions needed  Low-latency required;    Sub-second latency + high
               ahead of time;      result depends on        throughput required;
               batch jobs OK;      live user context        continuous data streams
               high throughput

Example        Pre-rank all items  LLM inference            Transaction fraud score
               for each user       at request time          at card swipe
               nightly
```

### Feature Stores — Bridging Batch and Online Features

A feature store maintains two pipelines:
- **Offline store** (batch): historical feature values in Parquet/Delta for training
- **Online store** (low-latency): latest feature values in Redis/DynamoDB for serving

```python
# Conceptual feature store access pattern (Feast / Tecton / Databricks Feature Store)
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Training: retrieve historical features from offline store
training_df = store.get_historical_features(
    entity_df=training_entities,
    features=["customer_features:days_since_last_login",
               "customer_features:total_spend_30d",
               "transaction_features:amount_vs_avg_ratio"],
).to_df()

# Serving: retrieve latest features from online store (< 10ms)
online_features = store.get_online_features(
    features=["customer_features:days_since_last_login",
               "customer_features:total_spend_30d"],
    entity_rows=[{"customer_id": "CUST-001"}],
).to_dict()
```

---

## 9. Data Distribution Shifts — Rigorous Taxonomy {#distribution-shifts}

> Huyen (2022), Ch. 8: "ML models are making predictions about a world that is
> constantly changing. All models become wrong eventually — the question is when
> and by how much."

### Mathematical Definitions

Let X be the input features and y be the label. At training time, data is drawn
from P_train(X, y). At serving time, data is drawn from P_serve(X, y).
Drift occurs when P_train ≠ P_serve.

```
DISTRIBUTION SHIFT TAXONOMY
────────────────────────────────────────────────────────────────────────────────

COVARIATE SHIFT (most common):
  P_train(X) ≠ P_serve(X)   but   P(y|X) is stable
  The input feature distribution changes; the relationship is unchanged.

  Example: a fraud model trained on 2022 transaction patterns deployed in 2024
           — payment methods changed (crypto, BNPL) but fraud indicators per
           payment type remain the same.
  Detection: monitor feature distributions (mean, std, quantiles, KL divergence)
  Fix: importance weighting, retrain on recent data

LABEL SHIFT (prior probability shift):
  P_train(y) ≠ P_serve(y)   but   P(X|y) is stable
  The class frequency changes; the appearance of each class is unchanged.

  Example: seasonal fraud surge — fraud rate increases 3× in December.
           A fraudster's behavior looks the same; there are just more of them.
  Detection: monitor prediction distribution and incoming label rate (if available)
  Fix: re-weight training examples, recalibrate decision threshold

CONCEPT DRIFT:
  P_train(y|X) ≠ P_serve(y|X)
  The fundamental relationship between features and labels changes.
  Most severe — retraining on historical data does not fix it.

  Example: fraud patterns change as fraudsters adapt to the model.
           Features that predicted fraud in 2023 no longer predict it in 2024.
  Detection: monitor model accuracy directly (requires labels); hard without labels
  Fix: continual learning on fresh data; feature evolution

SCHEMA DRIFT:
  Features are added, removed, renamed, or their type changes in the data pipeline.
  Not a statistical shift — a structural change in the input.
  Detection: schema validation at inference time (Pandera / Great Expectations)
  Fix: data contracts (see data_engineering_advanced.md §8)
```

```
DRIFT DETECTION METHODS BY TYPE

Method              Detects             Requires labels?  Latency
─────────────────────────────────────────────────────────────────
Statistical tests:
  KS test           Covariate           No                Moderate
  Chi-squared       Covariate (cat.)    No                Moderate
  PSI (Population   Covariate           No                Fast
  Stability Index)

Model-based:
  Drift classifier  Covariate           No                Slow
  (train model to
  discriminate
  train vs. serve)

Performance:
  Accuracy monitor  All types           YES               Depends on
  AUC / F1 monitor                                        label delay
  Residual monitor

Prediction:
  Output distribution All (proxy)       No                Fast
  monitoring
```

### Population Stability Index (PSI)

PSI quantifies how much a feature distribution has shifted between reference and
current. Standard thresholds (industry convention, insurance/banking origins):

```
PSI = Σᵢ (Actual_pct_i − Expected_pct_i) × ln(Actual_pct_i / Expected_pct_i)

PSI < 0.10  →  No significant shift
PSI < 0.20  →  Moderate shift — investigate
PSI ≥ 0.20  →  Significant shift — retraining likely required
```

```python
import numpy as np
import pandas as pd


def compute_psi(
    reference: pd.Series,
    current: pd.Series,
    n_bins: int = 10,
    eps: float = 1e-6,
) -> float:
    """
    Compute Population Stability Index (PSI) between reference and current distributions.
    Standard drift detection metric in financial services.

    PSI < 0.10: stable  |  0.10–0.20: moderate shift  |  > 0.20: significant shift

    Args:
        reference: Feature values from training / reference period.
        current: Feature values from current production period.
        n_bins: Number of quantile bins for discretization.

    Returns:
        PSI scalar value.
    """
    breakpoints = np.unique(
        np.percentile(reference.dropna(), np.linspace(0, 100, n_bins + 1))
    )
    breakpoints[0], breakpoints[-1] = -np.inf, np.inf

    ref_counts  = np.histogram(reference, bins=breakpoints)[0]
    curr_counts = np.histogram(current,   bins=breakpoints)[0]

    ref_pct  = ref_counts  / (ref_counts.sum()  + eps) + eps
    curr_pct = curr_counts / (curr_counts.sum() + eps) + eps

    psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
    return float(psi)
```

---

## 10. Continual Learning {#continual-learning}

> Huyen (2022), Ch. 9: "Continual learning is not about training forever — it is
> about having the infrastructure to update models quickly when the world changes."

### Stateless vs. Stateful Retraining

```
RETRAINING PARADIGMS
────────────────────────────────────────────────────────────────────────────

STATELESS RETRAINING (train from scratch):
  Model is retrained on a fresh dataset from scratch every cycle.
  The previous model's weights are discarded.

  Pros:  Simple; no catastrophic forgetting; reproducible
  Cons:  Computationally expensive; discards learned signal from historical data
  When:  Data is abundant; retraining is fast; weekly/monthly cadence

STATEFUL RETRAINING (fine-tuning / continual learning):
  Model is initialized from the previous checkpoint and updated on new data.
  The previous model's weights are the starting point.

  Pros:  Faster training; preserves accumulated knowledge; handles data scarcity
  Cons:  Catastrophic forgetting (new data overwrites old learning);
         requires careful data mixing to prevent distribution collapse
  When:  Large models (LLMs, deep neural nets); high-frequency retraining;
         data is scarce relative to model size

CATASTROPHIC FORGETTING MITIGATION:
  ├── Experience replay: mix old data into every new training batch
  ├── Elastic Weight Consolidation (EWC): penalize changes to weights
  │   important for previous tasks
  └── Learning rate scheduling: very small LR for fine-tuning to prevent
      large weight updates that destroy prior knowledge
```

### Retraining Triggers

```
WHEN TO RETRAIN — TRIGGER HIERARCHY

Time-based:          Retrain on a fixed schedule (daily, weekly, monthly)
                     Simple but ignores actual drift state

Performance-based:   Retrain when a monitored metric drops below a threshold
                     Best practice — triggered by real evidence of degradation
                     Requires labeled data to monitor performance

Data-based:          Retrain when PSI > 0.20 on a critical feature
                     Leading indicator — fires before performance degrades
                     No labels required

Volume-based:        Retrain when N new labeled samples accumulate
                     Use for tasks with slow, manual label acquisition
```

---

## 11. Test in Production {#test-in-production}

> Huyen (2022), Ch. 9: "Offline evaluation is necessary but not sufficient. Models
> that perform well offline fail in production for reasons that are invisible offline:
> feedback loops, distribution mismatches, latency constraints, A/B interaction effects."

```
PRODUCTION TESTING PATTERNS — COMPARISON
──────────────────────────────────────────────────────────────────────────

SHADOW MODE:
  New model receives live traffic and generates predictions,
  but predictions are NOT served — only logged for comparison.
  Champion model serves all users.
  Use: validate new model on production data before any user impact
  Risk: zero
  Limitation: cannot measure true business impact (no user interaction)

CANARY RELEASE:
  1–5% of traffic → new model; 95–99% → champion
  Monitor for errors, latency violations, and metric degradation
  Gradually increase new model traffic if healthy
  Use: detect infrastructure issues and gross performance regressions
  Risk: low (small user impact)

A/B TEST:
  Traffic randomly split between champion and challenger
  Measure business KPI impact with statistical significance
  Use: validate that model improvement translates to business improvement
  Duration: long enough for statistical power (weeks)
  Risk: moderate (challenger serves real users)

MULTI-ARMED BANDIT:
  Dynamically allocate more traffic to the better-performing model
  as evidence accumulates — no fixed traffic split
  Use: when fast adaptation is required; reduces regret vs. A/B
  Limitation: requires real-time reward signal; statistical interpretation harder
  Variants: epsilon-greedy, UCB (Upper Confidence Bound), Thompson Sampling
```

---

## 12. Slice-Based Evaluation and Fairness {#fairness}

> Huyen (2022), Ch. 6: "Aggregate metrics hide failures on specific subgroups.
> A model with 95% overall accuracy may have 40% accuracy on a minority group."

### Why Aggregate Metrics Are Insufficient

```
AGGREGATE METRIC MASKING EXAMPLE:

Dataset:  1000 samples — 900 majority group, 100 minority group
Model:    95% accuracy overall

Reality:
  Majority group accuracy:  97% (970/1000 × 0.9 = 873/900 correct)
  Minority group accuracy:  68% (68/100 correct)

Aggregate accuracy = (873 + 68) / 1000 = 94.1% ← masks 68% minority performance

Without slice evaluation, this failure is completely invisible in standard reports.
```

### Slice-Based Evaluation

```python
from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score


def slice_evaluation(
    df: pd.DataFrame,
    y_true_col: str,
    y_pred_col: str,
    y_prob_col: str,
    slice_columns: list[str],
    min_slice_size: int = 30,
) -> pd.DataFrame:
    """
    Evaluate model performance across all slices of specified columns.
    Surfaces performance disparities invisible in aggregate metrics.

    Args:
        df: DataFrame with true labels, predictions, and probabilities.
        slice_columns: Categorical columns to slice by (e.g., region, gender, age_group).
        min_slice_size: Minimum samples required to report a slice (< 30 is statistically unreliable).

    Returns:
        DataFrame with per-slice metrics, sorted by F1 ascending (worst slices first).
    """
    results = []

    # Overall metrics baseline
    overall_f1  = f1_score(df[y_true_col], df[y_pred_col])
    overall_auc = roc_auc_score(df[y_true_col], df[y_prob_col])

    results.append({
        "slice": "OVERALL",
        "n_samples": len(df),
        "f1": overall_f1,
        "auc": overall_auc,
        "precision": precision_score(df[y_true_col], df[y_pred_col]),
        "recall": recall_score(df[y_true_col], df[y_pred_col]),
        "f1_vs_overall": 0.0,
    })

    for col in slice_columns:
        for value, group in df.groupby(col):
            if len(group) < min_slice_size:
                continue
            f1  = f1_score(group[y_true_col], group[y_pred_col], zero_division=0)
            auc = roc_auc_score(group[y_true_col], group[y_prob_col]) if group[y_true_col].nunique() > 1 else np.nan
            results.append({
                "slice": f"{col}={value}",
                "n_samples": len(group),
                "f1": round(f1, 4),
                "auc": round(auc, 4) if not np.isnan(auc) else None,
                "precision": round(precision_score(group[y_true_col], group[y_pred_col], zero_division=0), 4),
                "recall": round(recall_score(group[y_true_col], group[y_pred_col], zero_division=0), 4),
                "f1_vs_overall": round(f1 - overall_f1, 4),
            })

    result_df = pd.DataFrame(results).sort_values("f1_vs_overall")
    return result_df


### Fairness Metrics

```

| Metric | Definition | When Required |
|---|---|---|
| **Demographic Parity** | P(ŷ=1 \| group A) = P(ŷ=1 \| group B) | Equal positive prediction rate across groups |
| **Equal Opportunity** | P(ŷ=1 \| y=1, A) = P(ŷ=1 \| y=1, B) | Equal true positive rate (recall) across groups |
| **Equalized Odds** | Both TPR and FPR equal across groups | Strongest fairness constraint; often impossible with accuracy |
| **Calibration** | P(y=1 \| ŷ=p, A) = P(y=1 \| ŷ=p, B) = p | Predicted probabilities are equally accurate across groups |

**The impossibility theorem** (Chouldechova, 2017): when base rates differ between
groups, calibration, equal opportunity, and demographic parity cannot all hold
simultaneously. Fairness criteria must be chosen based on the specific harm model —
there is no universally correct fairness metric.

---

## 13. ML Systems Design Checklist {#checklist}

> Breck, E., et al. (2017). The ML Test Score: A Rubric for ML Production Readiness
> and Technical Debt Reduction. *IEEE Big Data 2017*.

Apply before any model goes to production:

**Data**
- [ ] Feature generation timestamps verified to be before label timestamps (no leakage)
- [ ] Train/validation/test splits are non-overlapping and time-ordered for temporal data
- [ ] Class distribution documented; imbalance strategy selected and justified
- [ ] Data contract defined and validated for all input features
- [ ] Baseline PSI computed between training and holdout/production data

**Modeling**
- [ ] Baseline (heuristic / logistic regression) performance documented
- [ ] Model complexity justified by meaningful improvement over baseline
- [ ] Slice evaluation completed on all protected and business-critical subgroups
- [ ] Calibration checked: predicted probabilities reflect true probabilities
- [ ] SHAP values computed for feature importance and spot-check explanation

**Deployment**
- [ ] Serving pipeline tested with production-scale load
- [ ] Latency P50 / P95 / P99 verified against requirements
- [ ] Schema validation enforced on serving inputs
- [ ] Fallback strategy defined (what happens if model fails or is slow?)
- [ ] Prediction logging enabled with schema matching training features

**Monitoring**
- [ ] PSI monitoring on all critical features (threshold: 0.20)
- [ ] Prediction distribution monitoring configured
- [ ] Business KPI linked to model output and monitored independently
- [ ] Retraining trigger defined (time-based, drift-based, or performance-based)
- [ ] Alerting configured with on-call escalation path

**Fairness**
- [ ] Protected attributes identified (age, gender, geography, etc.)
- [ ] Slice evaluation on all protected attributes documented
- [ ] Fairness metric selected and justified relative to the harm model
- [ ] Fairness constraints encoded in model objective or post-processing threshold

---

## 14. References {#references}

- Huyen, C. (2022). *Designing Machine Learning Systems*. O'Reilly.
- Sculley, D., et al. (2015). Hidden Technical Debt in Machine Learning Systems. *NeurIPS 2015*.
- Breck, E., et al. (2017). The ML Test Score. *IEEE Big Data 2017*.
- Ratner, A., et al. (2017). Snorkel: Rapid Training Data Creation with Weak Supervision. *VLDB 2017*.
- Lin, T. Y., et al. (2017). Focal Loss for Dense Object Detection. *ICCV 2017*. arXiv:1708.02002.
- Vitter, J. S. (1985). Random sampling with a reservoir. *ACM TOMS*, 11(1), 37–57.
- Chouldechova, A. (2017). Fair prediction with disparate impact. *Big Data*, 5(2), 153–163.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly.
- Google (2020). *Practitioners Guide to MLOps*. https://cloud.google.com/resources/mlops-whitepaper
