# Mathematical Foundations for Machine Learning

> **References**: Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*.
> Springer. · Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*.
> MIT Press. · Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of
> Statistical Learning* (2nd ed.). Springer. · Murphy, K. P. (2022). *Probabilistic
> Machine Learning: An Introduction*. MIT Press. · Friedman, J. H. (2001). Greedy
> Function Approximation: A Gradient Boosting Machine. *Annals of Statistics*, 29(5).

## Table of Contents

1. [Regression — Linear and Logistic](#regression)
2. [Loss Functions](#loss-functions)
3. [Optimization — Gradient Descent and Variants](#optimization)
4. [Regularization — L1, L2, Elastic Net](#regularization)
5. [Activation Functions](#activations)
6. [Neural Network Fundamentals — Backpropagation](#backprop)
7. [Attention Mechanism — Transformer Core](#attention)
8. [Information Theory — Entropy and KL Divergence](#information-theory)
9. [Distance and Similarity Metrics](#distance)
10. [Estimation — MLE and MAP](#estimation)
11. [PCA — Variance Maximization](#pca)
12. [Quick Reference — All Formulas](#quick-ref)
13. [Python Implementations](#python)

---

## 1. Regression — Linear and Logistic {#regression}

### Linear Regression

Models the expected value of a continuous target as a linear combination of features.

```
ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₚxₚ
  = β₀ + X β       (matrix form: X ∈ R^(n×p), β ∈ R^p)
```

**OLS closed-form solution** (minimizes MSE exactly, no iteration required):
```
β̂ = (XᵀX)⁻¹ Xᵀy
```
Exists when XᵀX is invertible — fails under perfect multicollinearity. Use Ridge
regression or SVD decomposition when XᵀX is ill-conditioned.

**Geometric interpretation**: β̂ is the projection of y onto the column space of X.
The residuals ε = y − Xβ̂ are orthogonal to every column of X: Xᵀε = 0.

### Logistic Regression — Sigmoid Function

Models the probability of binary class membership as a logistic function of a linear
predictor z = β₀ + Xβ.

```
P(y=1|x) = σ(z) = 1 / (1 + e^(−z))
```

Properties of σ(z):
- σ(z) ∈ (0, 1) for all z ∈ R
- σ(0) = 0.5 (decision boundary)
- σ'(z) = σ(z)(1 − σ(z)) (derivative in terms of itself — essential for backprop)
- Symmetric: σ(−z) = 1 − σ(z)

No closed-form OLS solution — parameters are estimated by maximizing the
log-likelihood via gradient descent or Newton-Raphson.

### Softmax — Multiclass Extension

Extends logistic regression to K classes, producing a probability distribution:

```
P(y=k|x) = e^(z_k) / Σⱼ₌₁ᴷ e^(z_j)

Properties:
  Σₖ P(y=k|x) = 1    (valid probability distribution)
  P(y=k|x) > 0       for all k and z
```

**Numerical stability**: in practice, subtract the maximum before exponentiation to
prevent overflow: P(y=k|x) = e^(z_k − max_j z_j) / Σⱼ e^(z_j − max_j z_j)

---

## 2. Loss Functions {#loss-functions}

### Mean Squared Error (MSE)

```
MSE = (1/n) Σᵢ₌₁ⁿ (yᵢ − ŷᵢ)²
RMSE = √MSE    (returns to original unit of y)
MAE  = (1/n) Σᵢ |yᵢ − ŷᵢ|    (more robust to outliers — linear penalty)
```

MSE squares the residuals — outliers are penalized quadratically. Use MAE when
large errors should not be disproportionately penalized.

**MSE gradient** (needed for gradient descent):
```
∂MSE/∂ŷᵢ = −2(yᵢ − ŷᵢ)/n
```

### Binary Cross-Entropy Loss

The negative log-likelihood under a Bernoulli model — the standard loss for binary
classification and logistic regression:

```
L_BCE = −(1/n) Σᵢ [yᵢ log(ŷᵢ) + (1−yᵢ) log(1−ŷᵢ)]
```

When yᵢ ∈ {0,1}: only the term matching the true label contributes.
Perfect prediction → L = 0. Random prediction → L ≈ log(2) ≈ 0.693.

### Categorical Cross-Entropy Loss

Multiclass generalization — standard loss for softmax output layers:

```
L_CCE = −(1/n) Σᵢ Σₖ yᵢₖ log(ŷᵢₖ)
```

where yᵢₖ ∈ {0,1} is the one-hot encoded true label and ŷᵢₖ = P(y=k|xᵢ).

**Key property**: minimizing categorical cross-entropy is equivalent to maximizing
the log-likelihood of the multinomial distribution — it is the correct loss for
any model whose output is interpreted as a probability distribution over classes.

### Hinge Loss (SVM)

```
L_hinge = (1/n) Σᵢ max(0, 1 − yᵢ ŷᵢ)    where yᵢ ∈ {−1, +1}
```

Zero loss when the prediction is correct with margin ≥ 1. Positive loss when the
margin is violated. Not differentiable at yᵢŷᵢ = 1 — use subgradients.

---

## 3. Optimization — Gradient Descent and Variants {#optimization}

### Gradient Descent (Batch)

Updates all parameters using the gradient of the loss over the full training set:

```
θ ← θ − α ∇_θ J(θ)

where:
  θ ∈ R^p   : parameter vector
  α > 0     : learning rate
  J(θ)      : loss function (averaged over the training set)
  ∇_θ J(θ) : gradient of J with respect to θ
```

**The gradient points uphill** — subtracting it moves parameters in the direction
of steepest descent on the loss surface. Convergence to a local minimum is
guaranteed for convex J and sufficiently small α.

### Stochastic Gradient Descent (SGD)

Uses one randomly sampled example per update — noisy but fast:
```
θ ← θ − α ∇_θ J(θ; xᵢ, yᵢ)    (single-example gradient)
```

### Mini-Batch Gradient Descent (Standard in Practice)

Uses a batch of B examples — balances the variance of SGD with the stability of
full-batch gradient descent:
```
θ ← θ − α (1/B) Σᵢ∈B ∇_θ J(θ; xᵢ, yᵢ)
```
Typical batch sizes: 32, 64, 128, 256.

### Adam Optimizer (Adaptive Moment Estimation)

The standard optimizer for deep learning. Maintains per-parameter first and second
moment estimates to adaptively scale learning rates:

```
m_t = β₁ m_{t−1} + (1−β₁) g_t          (first moment — mean of gradients)
v_t = β₂ v_{t−1} + (1−β₂) g_t²         (second moment — uncentered variance)

m̂_t = m_t / (1−β₁ᵗ)                    (bias correction for initialization)
v̂_t = v_t / (1−β₂ᵗ)

θ_t ← θ_{t−1} − α m̂_t / (√v̂_t + ε)

Defaults: β₁=0.9, β₂=0.999, ε=1e-8, α=0.001
```

Adam adapts the effective learning rate per parameter: parameters with large
consistent gradients get smaller effective rates; sparse parameters get larger
effective rates. Combines momentum (m_t) with RMSprop-style scaling (v_t).

### Learning Rate and Convergence

Too large α → oscillates or diverges. Too small α → slow convergence or gets
stuck in flat regions. Standard strategies:
- Learning rate scheduling: reduce α by factor 0.1 when validation loss plateaus
- Warmup: start from α=0, linearly increase to α_max over N steps (standard in Transformers)
- Cosine annealing: α(t) = α_min + 0.5(α_max − α_min)(1 + cos(πt/T))

---

## 4. Regularization — L1, L2, Elastic Net {#regularization}

Regularization adds a penalty term to the loss function that penalizes model complexity,
preventing overfitting by shrinking coefficients toward zero.

### L2 Regularization — Ridge

```
J(β) = L(β) + λ Σⱼ βⱼ²     = L(β) + λ ‖β‖₂²
```

Effect: shrinks all coefficients proportionally toward zero — never exactly to zero.
Closed-form solution for OLS + L2: β̂ = (XᵀX + λI)⁻¹ Xᵀy.
The λI addition makes the problem always invertible regardless of multicollinearity.

**Bayesian interpretation**: L2 regularization corresponds to a Gaussian prior N(0, 1/λ)
on each coefficient. MAP estimation under this prior yields the Ridge solution.

### L1 Regularization — Lasso

```
J(β) = L(β) + λ Σⱼ |βⱼ|    = L(β) + λ ‖β‖₁
```

Effect: shrinks coefficients toward zero AND sets some exactly to zero — performs
implicit variable selection. No closed-form solution (non-differentiable at βⱼ=0);
solved via coordinate descent or subgradient methods.

**Geometric interpretation**: L1 penalty defines a diamond-shaped constraint region
in parameter space. The loss function's contours most often touch the diamond at
a corner — where some coordinates are exactly zero. This sparsity is geometric,
not a coincidence.

**Bayesian interpretation**: L1 regularization corresponds to a Laplace (double
exponential) prior on each coefficient.

### Elastic Net — Combined L1 + L2

```
J(β) = L(β) + λ₁ ‖β‖₁ + λ₂ ‖β‖₂²
     = L(β) + λ [α ‖β‖₁ + (1−α) ‖β‖₂²]    (mixing parameter α ∈ [0,1])
```

Use when: L1 is too aggressive (too many coefficients zeroed) but L2 cannot
select variables. Especially useful with correlated features — Elastic Net tends
to include or exclude correlated features together (Lasso arbitrarily selects one).

---

## 5. Activation Functions {#activations}

Activation functions introduce non-linearity. Without them, a multi-layer network
collapses to a single linear transformation regardless of depth.

### ReLU — Rectified Linear Unit

```
f(x) = max(0, x)
f'(x) = 1 if x > 0, else 0
```

The default activation for hidden layers in deep networks. Advantages: sparse
activation (inactive neurons consume no compute), no vanishing gradient for positive
inputs, computationally trivial. Problem: dying ReLU (neurons stuck at 0 for
negative inputs never recover during training).

### Leaky ReLU and Variants

```
Leaky ReLU:  f(x) = max(αx, x)           α = 0.01 (small slope for x < 0)
ELU:         f(x) = x if x > 0, else α(e^x − 1)
GELU:        f(x) = x Φ(x)               (Φ = Gaussian CDF; used in Transformers)
SiLU/Swish:  f(x) = x σ(x)              (smooth, non-monotonic; used in modern LLMs)
```

GELU is the default activation in BERT, GPT, and most Transformer architectures.
It approximates ReLU while being smooth and having non-zero gradient everywhere.

### Sigmoid and Tanh

```
Sigmoid: σ(x) = 1 / (1 + e^(−x))    range (0,1)
Tanh:    tanh(x) = (e^x − e^(-x)) / (e^x + e^(-x))    range (−1,1)
```

Both suffer from vanishing gradients for large |x| (derivatives ≈ 0). Avoid in
hidden layers of deep networks. Sigmoid used in output layer for binary classification;
tanh used in LSTM gates (zero-centered unlike sigmoid, which helps gradient flow).

---

## 6. Neural Network Fundamentals — Backpropagation {#backprop}

### Forward Pass

For a network with L layers, weight matrices W^(l), biases b^(l), activation φ^(l):

```
z^(l) = W^(l) a^(l−1) + b^(l)        (pre-activation: linear combination)
a^(l) = φ^(l)(z^(l))                  (post-activation: apply activation function)
```

The final layer output a^(L) is the prediction ŷ.

### Backpropagation — Chain Rule

Backpropagation computes ∂L/∂W^(l) and ∂L/∂b^(l) for every layer via the chain rule.
Define the error signal δ^(l) = ∂L/∂z^(l):

```
Output layer:    δ^(L) = ∂L/∂a^(L) ⊙ φ'^(L)(z^(L))
Hidden layer:    δ^(l) = (W^(l+1))ᵀ δ^(l+1) ⊙ φ'^(l)(z^(l))

Gradients:
  ∂L/∂W^(l) = δ^(l) (a^(l−1))ᵀ
  ∂L/∂b^(l) = δ^(l)
```

⊙ denotes element-wise multiplication. The error signal propagates backward through
the network layer by layer — hence "backpropagation."

**Vanishing gradient problem**: if |φ'(z)| < 1 for most z (as with sigmoid/tanh),
then δ^(l) → 0 exponentially as we move to earlier layers. ReLU, residual connections
(skip connections), and batch normalization are the standard mitigations.

**Residual connection** (He et al., 2016 — ResNet):
```
a^(l) = φ(z^(l)) + a^(l−2)    (skip connection bypasses two layers)
```
Gradient of the residual path is 1.0 — guarantees gradient flow even through many layers.

---

## 7. Attention Mechanism — Transformer Core {#attention}

> **Reference**: Vaswani, A., et al. (2017). Attention Is All You Need. *NeurIPS*.
> arXiv:1706.03762.

### Scaled Dot-Product Attention

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) V

where:
  Q ∈ R^(n×d_k)  : Query matrix (what the current token is looking for)
  K ∈ R^(m×d_k)  : Key matrix   (what each token offers as a key)
  V ∈ R^(m×d_v)  : Value matrix (what each token contributes to the output)
  d_k             : key dimension (dividing by √d_k prevents vanishing gradients in softmax)
```

**Intuition**: each query q_i computes a dot product with every key k_j, producing
raw scores. Softmax normalizes these to attention weights α_ij = P(token j is
relevant to token i). The output is a weighted sum of values: o_i = Σⱼ α_ij v_j.

The quadratic cost O(n²d_k) in sequence length n is the bottleneck for long sequences.

### Multi-Head Attention

```
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)    (h independent heads)
MultiHead(Q,K,V) = Concat(head_1,...,head_h) W^O
```

Different heads learn to attend to different aspects of the sequence simultaneously —
syntactic structure, semantic relationships, positional proximity.

---

## 8. Information Theory — Entropy and KL Divergence {#information-theory}

### Shannon Entropy

```
H(p) = −Σₓ p(x) log₂ p(x)    (in bits; use ln for nats)
```

Measures the expected information content (uncertainty) of a probability distribution.
H=0 for deterministic distributions; H=log₂(n) maximum for uniform over n outcomes.

**Cross-entropy**: expected log-probability of true label under the model's distribution:
```
H(p, q) = −Σₓ p(x) log q(x)
```
Minimizing cross-entropy H(y, ŷ) is equivalent to maximizing log-likelihood — they
are the same optimization problem under different names.

### KL Divergence — How Different Are Two Distributions?

```
D_KL(p ‖ q) = Σₓ p(x) log [p(x) / q(x)]
            = H(p, q) − H(p)    (cross-entropy minus entropy)
```

D_KL(p‖q) ≥ 0 always; equals 0 iff p = q everywhere. Not symmetric: D_KL(p‖q) ≠ D_KL(q‖p).

**In ML**: minimizing D_KL(y ‖ ŷ) from the true label distribution to the model
distribution is equivalent to minimizing cross-entropy loss (since H(y) is constant
with respect to model parameters).

---

## 9. Distance and Similarity Metrics {#distance}

### Euclidean Distance (L2 Norm)

```
d_E(x, y) = √(Σᵢ (xᵢ − yᵢ)²) = ‖x − y‖₂
```

Used in: K-Means, KNN, SVM (RBF kernel), PCA. Scale-sensitive — requires
feature scaling before application. Sensitive to irrelevant dimensions in high-
dimensional spaces (curse of dimensionality).

### Manhattan Distance (L1 Norm)

```
d_M(x, y) = Σᵢ |xᵢ − yᵢ| = ‖x − y‖₁
```

More robust to outliers than Euclidean. Useful when features represent independent
additive contributions (e.g., city-block distances, sparse features).

### Cosine Similarity

```
cos(x, y) = (x · y) / (‖x‖₂ ‖y‖₂)    ∈ [−1, 1]
```

Measures the angle between two vectors — invariant to magnitude. The standard
similarity metric for text embeddings, NLP (TF-IDF, word vectors, sentence
embeddings), and recommendation systems. cos(x,y) = 1 → identical direction;
cos(x,y) = 0 → orthogonal; cos(x,y) = −1 → opposite.

### Mahalanobis Distance

```
d_M(x, μ) = √((x − μ)ᵀ Σ⁻¹ (x − μ))

where Σ is the covariance matrix of the feature distribution.
```

Accounts for feature correlations and scale differences — equivalent to Euclidean
distance in the standardized, decorrelated (whitened) feature space. Used in:
anomaly detection (multivariate outlier scoring), Linear Discriminant Analysis (LDA),
Gaussian Mixture Models.

---

## 10. Estimation — MLE and MAP {#estimation}

### Maximum Likelihood Estimation (MLE)

```
θ̂_MLE = argmax_θ L(θ) = argmax_θ Σᵢ log p(xᵢ | θ)
```

Find the parameters that make the observed data most probable. Maximizing the
log-likelihood is equivalent to minimizing negative log-likelihood (NLL) — the
standard form in practice (NLL = cross-entropy for classification).

**MLE properties** (under regularity conditions):
- Consistent: θ̂_MLE → θ* as n → ∞
- Asymptotically normal: √n(θ̂_MLE − θ*) → N(0, I(θ*)⁻¹)
- Asymptotically efficient: achieves the Cramér-Rao lower bound

### Maximum A Posteriori (MAP) Estimation

```
θ̂_MAP = argmax_θ [Σᵢ log p(xᵢ | θ) + log p(θ)]
       = argmax_θ [log-likelihood + log-prior]
```

MAP incorporates prior knowledge p(θ). When p(θ) = N(0, 1/λ) (Gaussian prior),
MAP is equivalent to L2-regularized MLE. When p(θ) = Laplace(0, 1/λ), MAP is
equivalent to L1-regularized MLE. This is the precise mathematical connection
between regularization and Bayesian priors.

---

## 11. PCA — Variance Maximization {#pca}

Principal Component Analysis finds the directions of maximum variance in the data.

**Formulation**: find unit vectors w₁, w₂, ..., w_k that sequentially maximize the
variance of the projected data, subject to orthogonality:

```
w₁ = argmax_{‖w‖=1} Var(Xw) = argmax_{‖w‖=1} wᵀ S w

where S = (1/n) Xᵀ X is the sample covariance matrix (centered X).
```

**Solution**: the principal components are the eigenvectors of S, ordered by
decreasing eigenvalue. The k-th eigenvalue λₖ equals the variance explained by
the k-th component.

```
Eigendecomposition:  S = V Λ Vᵀ
PCA projection:      Z = X V_k        (X projected onto first k eigenvectors)
Variance explained:  R²_k = Σᵢ₌₁ᵏ λᵢ / Σᵢ₌₁ⁿ λᵢ
```

For large datasets, use SVD directly: X = U Σ Vᵀ, where the right singular vectors
V are the principal components and the singular values satisfy λᵢ = σᵢ²/n.

**PCA and feature scaling**: PCA maximizes variance — features with larger scales
will dominate. Always standardize (Z-score) before applying PCA. This is the
precise reason feature scaling is required before PCA.

---

## 12. Quick Reference — All Formulas {#quick-ref}

| Equation | Formula | Notes |
|---|---|---|
| Linear Regression | ŷ = Xβ, β̂ = (XᵀX)⁻¹Xᵀy | OLS closed form |
| Sigmoid | σ(z) = 1/(1+e^(−z)) | σ'(z) = σ(z)(1−σ(z)) |
| Softmax | P(k|x) = e^(z_k)/Σⱼe^(z_j) | Subtract max for stability |
| MSE | (1/n)Σ(y−ŷ)² | Gradient: −2(y−ŷ)/n |
| MAE | (1/n)Σ|y−ŷ| | Robust to outliers |
| Binary Cross-Entropy | −Σ[y log ŷ + (1−y)log(1−ŷ)] / n | = NLL under Bernoulli |
| Gradient Descent | θ ← θ − α∇J(θ) | α = learning rate |
| Adam | θ ← θ − α m̂/(√v̂+ε) | β₁=0.9, β₂=0.999 |
| L1 (Lasso) | J = L + λΣ|βⱼ| | Induces sparsity |
| L2 (Ridge) | J = L + λΣβⱼ² | Shrinks all coefficients |
| ReLU | max(0,x) | f'(x)=1 if x>0, else 0 |
| GELU | xΦ(x) | Default in Transformers |
| Attention | softmax(QKᵀ/√d_k)V | O(n²) in sequence length |
| Entropy | −Σp(x)log p(x) | Bits (log₂) or nats (ln) |
| KL Divergence | Σp(x)log[p(x)/q(x)] | ≥ 0; = 0 iff p=q |
| Euclidean | √Σ(xᵢ−yᵢ)² | Scale-sensitive |
| Cosine Similarity | (x·y)/(‖x‖‖y‖) | Scale-invariant; range [−1,1] |
| MLE | argmax Σlog p(xᵢ|θ) | = minimize NLL |
| MAP | argmax [log-likelihood + log-prior] | MLE + regularization |
| PCA | S = VΛVᵀ, Z = XV_k | Standardize X first |
| Bias-Variance | E[(y−ŷ)²] = Bias² + Var + ε | See statistics_reference.md §8 |
| Bayes' Theorem | P(A|B) = P(B|A)P(A)/P(B) | See statistics_reference.md §9 |

---

## 13. Python Implementations {#python}

```python
from __future__ import annotations

import numpy as np
from scipy.special import softmax as scipy_softmax


# ── Activation functions ─────────────────────────────────────────────────────

def sigmoid(z: np.ndarray) -> np.ndarray:
    """σ(z) = 1 / (1 + e^(−z)). Numerically stable via clip."""
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def relu(z: np.ndarray) -> np.ndarray:
    """f(z) = max(0, z). Element-wise."""
    return np.maximum(0.0, z)


def leaky_relu(z: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """f(z) = z if z > 0 else alpha*z."""
    return np.where(z > 0, z, alpha * z)


def gelu(z: np.ndarray) -> np.ndarray:
    """GELU ≈ z * Φ(z). Used in BERT, GPT, modern LLMs."""
    from scipy.stats import norm
    return z * norm.cdf(z)


def softmax(z: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax: subtract max before exponentiation."""
    z_shift = z - np.max(z, axis=axis, keepdims=True)
    exp_z = np.exp(z_shift)
    return exp_z / np.sum(exp_z, axis=axis, keepdims=True)


# ── Loss functions ────────────────────────────────────────────────────────────

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Squared Error."""
    return float(np.mean((y_true - y_pred) ** 2))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error — robust to outliers."""
    return float(np.mean(np.abs(y_true - y_pred)))


def binary_cross_entropy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    eps: float = 1e-12,
) -> float:
    """
    Binary cross-entropy loss: −mean[y log(ŷ) + (1−y) log(1−ŷ)].
    Clips ŷ to (eps, 1−eps) to prevent log(0).
    """
    y_pred = np.clip(y_pred, eps, 1.0 - eps)
    return float(-np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)))


def categorical_cross_entropy(
    y_true: np.ndarray,   # one-hot encoded, shape (n, K)
    y_pred: np.ndarray,   # softmax probabilities, shape (n, K)
    eps: float = 1e-12,
) -> float:
    """Categorical cross-entropy: −mean[Σₖ yₖ log ŷₖ]."""
    y_pred = np.clip(y_pred, eps, 1.0)
    return float(-np.mean(np.sum(y_true * np.log(y_pred), axis=1)))


# ── Gradient descent ──────────────────────────────────────────────────────────

def gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_iter: int = 1000,
    l2_lambda: float = 0.0,
) -> tuple[np.ndarray, list[float]]:
    """
    Linear regression via mini-batch gradient descent with optional L2 regularization.

    Returns:
        Tuple of (learned weights, loss history).
    """
    n, p = X.shape
    theta = np.zeros(p)
    history: list[float] = []

    for _ in range(n_iter):
        y_pred = X @ theta
        residuals = y_pred - y
        grad = (X.T @ residuals) / n + l2_lambda * theta  # gradient + L2 penalty
        theta -= learning_rate * grad
        history.append(mse(y, y_pred))

    return theta, history


# ── Distance metrics ──────────────────────────────────────────────────────────

def euclidean_distance(x: np.ndarray, y: np.ndarray) -> float:
    """L2 norm distance between two vectors."""
    return float(np.sqrt(np.sum((x - y) ** 2)))


def cosine_similarity(x: np.ndarray, y: np.ndarray) -> float:
    """
    Cosine similarity ∈ [−1, 1]. Scale-invariant.
    Use for text embeddings and recommendation systems.
    """
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    if norm_x == 0 or norm_y == 0:
        return 0.0
    return float(np.dot(x, y) / (norm_x * norm_y))


def mahalanobis_distance(x: np.ndarray, mu: np.ndarray, cov: np.ndarray) -> float:
    """
    Mahalanobis distance: √((x−μ)ᵀ Σ⁻¹ (x−μ)).
    Accounts for feature correlations and scale.
    Use for anomaly detection and multivariate outlier scoring.
    """
    diff = x - mu
    cov_inv = np.linalg.inv(cov)
    return float(np.sqrt(diff.T @ cov_inv @ diff))


# ── Information theory ────────────────────────────────────────────────────────

def entropy(p: np.ndarray, base: float = 2.0) -> float:
    """Shannon entropy H(p) in bits (base=2) or nats (base=e)."""
    p = p[p > 0]   # 0 * log(0) = 0 by convention
    return float(-np.sum(p * np.log(p) / np.log(base)))


def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """
    KL divergence D_KL(p‖q) = Σ p log(p/q) ≥ 0.
    Not symmetric. Equals 0 iff p = q.
    """
    q = np.clip(q, eps, 1.0)
    mask = p > 0
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))


# ── PCA from scratch ──────────────────────────────────────────────────────────

def pca_from_scratch(
    X: np.ndarray,
    n_components: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    PCA via eigendecomposition of the sample covariance matrix.
    Always standardize X before calling.

    Returns:
        Tuple of (projected data Z, principal components V, explained variance ratio).
    """
    # Center X (standardization must be done before calling)
    X_centered = X - X.mean(axis=0)

    # Sample covariance matrix
    S = (X_centered.T @ X_centered) / (len(X) - 1)

    # Eigendecomposition — eigenvalues in ascending order; reverse for descending
    eigenvalues, eigenvectors = np.linalg.eigh(S)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Select top k components
    V_k = eigenvectors[:, :n_components]
    Z = X_centered @ V_k

    explained_variance_ratio = eigenvalues[:n_components] / eigenvalues.sum()

    return Z, V_k, explained_variance_ratio
```
