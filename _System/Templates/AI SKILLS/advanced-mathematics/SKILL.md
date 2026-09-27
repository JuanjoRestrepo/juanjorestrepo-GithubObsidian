---
name: advanced-mathematics
description: >
  Expert-level mathematics and cryptography: calculus (single/multivariable, vector),
  ODEs/PDEs, linear algebra, Fourier/Laplace/Z-transforms, wavelets and MRA, probability
  and stochastic processes, convex optimization, numerical methods, discrete mathematics,
  and cryptography/security — grounded in 40+ canonical references (Rosen, Stewart,
  Kreyszig, Mallat, Oppenheim, Boyd, Strang, Katz & Lindell, Ferguson & Schneier).
  Graduate level: derivations, proofs, Python (NumPy, SciPy, SymPy, cryptography).
  Trigger on: integral, derivative, ODE, PDE, Fourier, FFT, Z-transform, eigenvalue,
  SVD, wavelet, Kalman, LASSO, ADMM, graph theory, automata, RSA, AES, TLS, SHA-256,
  HMAC, ECC, Ed25519, Diffie-Hellman, post-quantum, Argon2, JWT, cipher, hash, prime,
  modular arithmetic, finite field, Boolean algebra, SAT, NP-complete. Also trigger on:
  "encrypt/decrypt", "digital signature", "key exchange", "password hashing", "secure
  token", "design a filter", "solve this ODE", "sparse recovery".
  When in doubt, use this skill.
---

# Advanced Mathematics Skill

Expert-level mathematics from calculus foundations through graduate applied analysis,
covering theory, derivations, and direct engineering/industry implementations. All
responses are anchored to canonical sources (see [Source Library](#source-library)).

---

## How to Use This Skill

1. **Identify the mathematical domain** using the [Domain Selector](#domain-selector) table
   and read the matching reference file before responding.
2. **Establish the context**: pure theory, applied derivation, numerical implementation,
   or engineering application — and match the depth to the request.
3. **Always ground claims** in the source library. State the theorem name, provide the
   key steps of the derivation or proof, and surface assumptions explicitly.
4. **Surface failure modes**: convergence conditions, domain restrictions, numerical
   stability hazards, and physical validity windows before delivering a solution.
5. **Provide Python implementations** (NumPy / SciPy / SymPy) for every numerical or
   computational result unless the request is purely theoretical.
6. **Link theory to industry**: every major result should be connected to at least one
   real-world application domain (signal processing, control systems, structural mechanics,
   thermodynamics, data science, communications).

---

## Domain Selector

| Topic cluster | Reference file | Key triggers |
|---|---|---|
| Single/multivariable calculus, vector calculus, complex analysis | `references/calculus-multivariable.md` | integral, derivative, gradient, curl, divergence, Stokes, Green, Gauss, series, Taylor, complex, residue, conformal, Cauchy |
| Ordinary & partial differential equations | `references/differential-equations.md` | ODE, PDE, heat equation, wave equation, Laplace equation, separation of variables, Runge-Kutta, Bessel, Legendre, bifurcation, Lyapunov |
| Fourier, Laplace, Z-transforms | `references/transforms.md` | Fourier series, Fourier transform, FFT, DFT, DTFT, Laplace, Z-transform, transfer function, convolution, frequency response, impulse response, sampling theorem, Nyquist, aliasing, Hilbert transform |
| Linear algebra — applied and computational | `references/linear-algebra-applied.md` | matrix, eigenvalue, eigenvector, SVD, PCA, LU, QR, Cholesky, projection, least squares, pseudoinverse, condition number, Gram-Schmidt |
| Numerical methods | `references/numerical-methods.md` | root finding, Newton-Raphson, numerical integration, finite difference, finite element, Runge-Kutta, condition number, interpolation, spline, quadrature, CFL, stiffness, conjugate gradient |
| Wavelets & multi-resolution analysis | `references/wavelets-multiresolution.md` | wavelet, DWT, CWT, filter bank, Daubechies, Haar, Morlet, multiresolution, subband, JPEG2000, wavelet denoising, scalogram, mother wavelet, vanishing moments |
| Probability, random processes & stochastic methods | `references/probability-stochastic.md` | probability, random variable, distribution, Gaussian, covariance, stochastic process, PSD, autocorrelation, Wiener-Khinchin, Kalman filter, SDE, Brownian motion, Itô, spectral estimation, Bayesian |
| Convex optimization | `references/convex-optimization.md` | convex, optimization, KKT, Lagrangian, duality, LP, QP, SOCP, SDP, LASSO, gradient descent, ADMM, proximal, interior-point, MPC, FISTA, Nesterov, Adam |
| Discrete mathematics | `references/discrete-mathematics.md` | logic, proof, sets, relations, functions, graphs, trees, counting, permutations, combinations, Pigeonhole, recurrence, Catalan, Boolean algebra, automata, DFA, NFA, regular expression, Turing machine, NP-complete, SAT, group, ring, field, lattice, Markov chain |
| Information theory & coding | `references/information-theory-coding.md` | entropy, mutual information, KL divergence, cross-entropy, Huffman, arithmetic coding, LZ77, rate-distortion, Shannon capacity, AWGN, MIMO, BSC, Hamming code, Reed-Solomon, BCH, CRC, LDPC, turbo codes, polar codes, Blahut-Arimoto, AEP, Kolmogorov complexity |
| Mathematical statistics | `references/mathematical-statistics.md` | MLE, Fisher information, Cramér-Rao, sufficient statistic, exponential family, Bayesian inference, MAP, conjugate prior, MCMC, HMC, NUTS, confidence interval, hypothesis testing, p-value, t-test, ANOVA, power analysis, OLS, Ridge, LASSO, elastic net, GLM, logistic regression, KDE, bootstrap, permutation test |
| Formal methods & logic | `references/formal-methods-logic.md` | Hoare logic, program verification, weakest precondition, loop invariant, temporal logic, LTL, CTL, model checking, SPIN, BDD, bounded model checking, SAT, CDCL, SMT, Z3, type theory, lambda calculus, Hindley-Milner, dependent types, Curry-Howard, abstract interpretation, Galois connection, operational semantics |
| Cryptography & security | `references/cryptography-security.md` | cipher, RSA, AES, DES, TLS, HTTPS, hash, SHA-256, MD5, HMAC, MAC, digital signature, certificate, PKI, ECC, Ed25519, X25519, Diffie-Hellman, ECDH, key exchange, password hashing, Argon2, bcrypt, JWT, OAuth, post-quantum, Kyber, Dilithium, homomorphic encryption, zero-knowledge proof, secret sharing, OWASP, encrypt, decrypt, PRNG, nonce, IV, padding, GCM, CBC |
| Engineering applications survey | `references/engineering-applications.md` | control systems, signal processing, structural mechanics, heat transfer, fluid dynamics, communications, power systems, FEA, vibration, bearing fault |

**When a question spans multiple files**, read all relevant references and synthesize.
Examples:
- "Design a digital filter using the Z-transform" → `transforms.md` + `engineering-applications.md`
- "Compressed sensing for sparse signal recovery" → `wavelets-multiresolution.md` + `convex-optimization.md`
- "Kalman smoother for noisy ODE trajectory" → `probability-stochastic.md` + `differential-equations.md`
- "Control system with LQR and noise" → `engineering-applications.md` + `probability-stochastic.md` + `linear-algebra-applied.md`

---

## Core Response Protocol

### Theory Requests
- State the formal definition with full mathematical notation.
- Identify all **assumptions and domain restrictions** explicitly.
- Provide the **key proof steps** or derivation — not just the result.
- State the theorem in its **most general form**, then specialize to the applied case.
- Cite the canonical source (author, edition, chapter/section).

### Computational / Numerical Requests
- Provide **analytical solution first** (SymPy where applicable).
- Then provide **numerical implementation** in Python with full type hints, docstrings,
  and error handling per the user's PEP8/mypy/Ruff standards.
- State **convergence conditions and numerical stability** caveats explicitly.
- Include **validation** against a known closed-form result when possible.

### Engineering Application Requests
- Frame the mathematical object (transform, operator, decomposition) in the physical context.
- Derive or reference the **governing equation** first.
- Connect to system properties (stability, frequency response, energy, convergence).
- Provide a **Python simulation or computation** with representative parameters.
- Identify where the model breaks down (linearity assumption, small-angle, etc.).

---

## Source Library

All mathematical content in this skill is grounded in these canonical references.
Cite by [SRC-XX] tag when needed.

### Calculus & Analysis
| Tag | Reference |
|---|---|
| [SRC-01] | Stewart, J. *Calculus: Early Transcendentals*, 9th ed. Cengage, 2020. |
| [SRC-02] | Apostol, T. M. *Calculus*, Vols. 1 & 2, 2nd ed. Wiley, 1967. (Rigorous treatment, proofs) |
| [SRC-03] | Spivak, M. *Calculus*, 4th ed. Publish or Perish, 2008. (Proof-level rigor) |
| [SRC-04] | Rudin, W. *Principles of Mathematical Analysis*, 3rd ed. McGraw-Hill, 1976. ("Baby Rudin") |
| [SRC-05] | Marsden, J. E. & Tromba, A. J. *Vector Calculus*, 6th ed. W. H. Freeman, 2011. |
| [SRC-06] | Ahlfors, L. V. *Complex Analysis*, 3rd ed. McGraw-Hill, 1979. |
| [SRC-07] | Churchill, R. V. & Brown, J. W. *Complex Variables and Applications*, 9th ed. McGraw-Hill, 2013. |

### Differential Equations
| Tag | Reference |
|---|---|
| [SRC-08] | Boyce, W. E., DiPrima, R. C. & Meade, D. B. *Elementary Differential Equations*, 11th ed. Wiley, 2017. |
| [SRC-09] | Strauss, W. A. *Partial Differential Equations: An Introduction*, 2nd ed. Wiley, 2008. |
| [SRC-10] | Evans, L. C. *Partial Differential Equations*, 2nd ed. AMS Graduate Studies, 2010. (Graduate-level) |
| [SRC-11] | Haberman, R. *Applied Partial Differential Equations*, 5th ed. Pearson, 2012. |
| [SRC-12] | Strogatz, S. H. *Nonlinear Dynamics and Chaos*, 2nd ed. CRC Press, 2018. |

### Transforms & Signal Processing
| Tag | Reference |
|---|---|
| [SRC-13] | Oppenheim, A. V. & Schafer, R. W. *Discrete-Time Signal Processing*, 3rd ed. Pearson, 2010. |
| [SRC-14] | Bracewell, R. N. *The Fourier Transform and Its Applications*, 3rd ed. McGraw-Hill, 2000. |
| [SRC-15] | Körner, T. W. *Fourier Analysis*. Cambridge University Press, 1988. |
| [SRC-16] | Proakis, J. G. & Manolakis, D. K. *Digital Signal Processing*, 4th ed. Pearson, 2006. |
| [SRC-17] | Doetsch, G. *Introduction to the Theory and Application of the Laplace Transformation*. Springer, 1974. |
| [SRC-18] | Papoulis, A. *The Fourier Integral and Its Applications*. McGraw-Hill, 1962. |

### Linear Algebra
| Tag | Reference |
|---|---|
| [SRC-19] | Strang, G. *Linear Algebra and Its Applications*, 4th ed. Cengage, 2005. |
| [SRC-20] | Strang, G. *Introduction to Linear Algebra*, 5th ed. Wellesley-Cambridge, 2016. |
| [SRC-21] | Horn, R. A. & Johnson, C. R. *Matrix Analysis*, 2nd ed. Cambridge, 2012. |
| [SRC-22] | Golub, G. H. & Van Loan, C. F. *Matrix Computations*, 4th ed. Johns Hopkins, 2013. |
| [SRC-23] | Trefethen, L. N. & Bau, D. *Numerical Linear Algebra*. SIAM, 1997. |

### Numerical Methods
| Tag | Reference |
|---|---|
| [SRC-24] | Burden, R. L., Faires, J. D. & Burden, A. M. *Numerical Analysis*, 10th ed. Cengage, 2016. |
| [SRC-25] | Press, W. H. et al. *Numerical Recipes: The Art of Scientific Computing*, 3rd ed. Cambridge, 2007. |
| [SRC-26] | Quarteroni, A., Sacco, R. & Saleri, F. *Numerical Mathematics*, 2nd ed. Springer, 2007. |
| [SRC-27] | LeVeque, R. J. *Finite Difference Methods for Ordinary and Partial Differential Equations*. SIAM, 2007. |

### Engineering & Applied Mathematics
| Tag | Reference |
|---|---|
| [SRC-28] | Kreyszig, E. *Advanced Engineering Mathematics*, 10th ed. Wiley, 2011. |
| [SRC-29] | Arfken, G. B., Weber, H. J. & Harris, F. E. *Mathematical Methods for Physicists*, 7th ed. Academic Press, 2012. |
| [SRC-30] | Ogata, K. *Modern Control Engineering*, 5th ed. Pearson, 2010. |
| [SRC-31] | Haykin, S. *Communication Systems*, 4th ed. Wiley, 2001. |
| [SRC-32] | Incropera, F. P. et al. *Fundamentals of Heat and Mass Transfer*, 7th ed. Wiley, 2011. |

### Wavelets & Multi-Resolution Analysis
| Tag | Reference |
|---|---|
| [SRC-W1] | Mallat, S. *A Wavelet Tour of Signal Processing*, 3rd ed. Academic Press, 2009. |
| [SRC-W2] | Daubechies, I. *Ten Lectures on Wavelets*. SIAM, 1992. |
| [SRC-W3] | Strang, G. & Nguyen, T. *Wavelets and Filter Banks*, rev. ed. Wellesley-Cambridge, 1996. |
| [SRC-W4] | Vetterli, M. & Kovačević, J. *Wavelets and Subband Coding*. Prentice Hall, 1995. |

### Probability, Stochastic Processes & Estimation
| Tag | Reference |
|---|---|
| [SRC-P1] | Papoulis, A. & Pillai, S. U. *Probability, Random Variables and Stochastic Processes*, 4th ed. McGraw-Hill, 2002. |
| [SRC-P2] | Kay, S. M. *Fundamentals of Statistical Signal Processing*, Vols. I & II. Prentice Hall, 1993/1998. |
| [SRC-P3] | Øksendal, B. *Stochastic Differential Equations*, 6th ed. Springer, 2003. |
| [SRC-P4] | Anderson, B. D. O. & Moore, J. B. *Optimal Filtering*. Dover, 2012. |

### Convex Optimization
| Tag | Reference |
|---|---|
| [SRC-O1] | Boyd, S. & Vandenberghe, L. *Convex Optimization*. Cambridge University Press, 2004. (Free: web.stanford.edu/~boyd/cvxbook) |
| [SRC-O2] | Nocedal, J. & Wright, S. J. *Numerical Optimization*, 2nd ed. Springer, 2006. |
| [SRC-O3] | Bertsekas, D. P. *Nonlinear Programming*, 3rd ed. Athena Scientific, 2016. |
| [SRC-O4] | Rockafellar, R. T. *Convex Analysis*. Princeton University Press, 1970. |
| [SRC-O5] | Nesterov, Y. *Lectures on Convex Optimization*, 2nd ed. Springer, 2018. |

### Discrete Mathematics
| Tag | Reference |
|---|---|
| [SRC-D1] | Rosen, K. H. *Discrete Mathematics and Its Applications*, 8th ed. McGraw-Hill, 2019. *(Primary — §4.5 hashing, §4.6 cryptography verified against uploaded text.)* |
| [SRC-D2] | Knuth, D. E., Graham, R. L. & Patashnik, O. *Concrete Mathematics*, 2nd ed. Addison-Wesley, 1994. |
| [SRC-D3] | Sipser, M. *Introduction to the Theory of Computation*, 3rd ed. Cengage, 2012. |
| [SRC-D4] | Cormen, T. H. et al. *Introduction to Algorithms (CLRS)*, 4th ed. MIT Press, 2022. |
| [SRC-D5] | Diestel, R. *Graph Theory*, 5th ed. Springer, 2017. (Free: diestel-graph-theory.com) |
| [SRC-D6] | Matousek, J. & Nesetril, J. *Invitation to Discrete Mathematics*, 2nd ed. Oxford, 2008. |
| [SRC-D7] | Grimaldi, R. P. *Discrete and Combinatorial Mathematics*, 5th ed. Pearson, 2004. |
| [SRC-D8] | Mitzenmacher, M. & Upfal, E. *Probability and Computing*, 2nd ed. Cambridge, 2017. |
| [SRC-D9] | Knuth, D. E. *The Art of Computer Programming*, Vols. 1–4. Addison-Wesley. |

### Information Theory & Coding
| Tag | Reference |
|---|---|
| [SRC-I1] | Shannon, C. E. & Weaver, W. *The Mathematical Theory of Communication*. Univ. of Illinois Press, 1949. |
| [SRC-I2] | Cover, T. M. & Thomas, J. A. *Elements of Information Theory*, 2nd ed. Wiley, 2006. |
| [SRC-I3] | MacKay, D. J. C. *Information Theory, Inference, and Learning Algorithms*. Cambridge, 2003. (Free: inference.org.uk) |
| [SRC-I4] | Lin, S. & Costello, D. J. *Error Control Coding*, 2nd ed. Pearson, 2004. |
| [SRC-I5] | Richardson, T. & Urbanke, R. *Modern Coding Theory*. Cambridge, 2008. |

### Mathematical Statistics
| Tag | Reference |
|---|---|
| [SRC-S1] | Casella, G. & Berger, R. L. *Statistical Inference*, 2nd ed. Cengage, 2002. |
| [SRC-S2] | Hogg, R. V., McKean, J. W. & Craig, A. T. *Introduction to Mathematical Statistics*, 8th ed. Pearson, 2018. |
| [SRC-S3] | Gelman, A. et al. *Bayesian Data Analysis*, 3rd ed. CRC Press, 2013. |
| [SRC-S4] | Hastie, T., Tibshirani, R. & Friedman, J. *The Elements of Statistical Learning*, 2nd ed. Springer, 2009. (Free: stanford.edu) |
| [SRC-S5] | Bishop, C. M. *Pattern Recognition and Machine Learning*. Springer, 2006. |

### Formal Methods & Logic
| Tag | Reference |
|---|---|
| [SRC-F1] | Huth, M. & Ryan, M. *Logic in Computer Science*, 2nd ed. Cambridge, 2004. |
| [SRC-F2] | Pierce, B. C. *Types and Programming Languages*. MIT Press, 2002. |
| [SRC-F3] | Baier, C. & Katoen, J. P. *Principles of Model Checking*. MIT Press, 2008. |
| [SRC-F4] | Winskel, G. *The Formal Semantics of Programming Languages*. MIT Press, 1993. |
| [SRC-F5] | Nipkow, T., Paulson, L. C. & Wenzel, M. *Isabelle/HOL*. Springer, 2002. |
| [SRC-F6] | de Moura, L. & Bjørner, N. Z3: An Efficient SMT Solver. TACAS 2008. |

### Cryptography & Security
| Tag | Reference |
|---|---|
| [SRC-C1] | Stinson, D. R. *Cryptography: Theory and Practice*, 4th ed. CRC Press, 2019. |
| [SRC-C2] | Boneh, D. & Shoup, V. *A Graduate Course in Applied Cryptography*. (Free: crypto.stanford.edu/~dabo/cryptobook) |
| [SRC-C3] | Katz, J. & Lindell, Y. *Introduction to Modern Cryptography*, 3rd ed. CRC Press, 2020. |
| [SRC-C4] | Ferguson, N., Schneier, B. & Kohno, T. *Cryptography Engineering*. Wiley, 2010. |
| [SRC-C5] | NIST SP 800-57 (Key Management), SP 800-175B (Cryptographic Standards Guidance). |
| [SRC-C6] | RFC 8446 (TLS 1.3), RFC 8017 (PKCS#1 v2.2 / RSA-OAEP), RFC 8032 (EdDSA / Ed25519). |

---

## Mathematical Notation Standards

Use these conventions consistently across all responses:

```
Scalars:           a, b, x, t  (lowercase italic)
Vectors:           𝐯, 𝐮, 𝐱     (bold lowercase)
Matrices:          𝐀, 𝐁, 𝐌     (bold uppercase)
Sets/spaces:       ℝ, ℂ, ℕ, ℤ  (blackboard bold)
Operators:         ∇ (gradient/nabla), Δ (Laplacian), ∂ (partial), 𝒟 (differential operator)
Transforms:        ℒ{·} (Laplace), ℱ{·} (Fourier), 𝒵{·} (Z-transform)
Inner product:     ⟨f, g⟩
Norm:              ‖·‖₂, ‖·‖_F (Frobenius)
Convolution:       f * g
Composition:       f ∘ g
```

---

## Quick Reference: Fundamental Theorems

These theorems appear across all domains — memorize their scope and conditions.

| Theorem | Statement summary | Domain |
|---|---|---|
| **Fundamental Theorem of Calculus** | ∫ₐᵇ f′(x)dx = f(b) − f(a); connects differentiation and integration | Calculus |
| **Green's Theorem** | ∮_C (P dx + Q dy) = ∬_D (∂Q/∂x − ∂P/∂y) dA | Vector calc, 2D |
| **Stokes' Theorem** | ∮_C 𝐅·d𝐫 = ∬_S (∇×𝐅)·d𝐒 | Vector calc, 3D |
| **Divergence Theorem** | ∯_S 𝐅·d𝐒 = ∭_V (∇·𝐅) dV | Vector calc, 3D |
| **Cauchy's Integral Formula** | f⁽ⁿ⁾(a) = n!/(2πi) ∮_C f(z)/(z−a)ⁿ⁺¹ dz | Complex analysis |
| **Residue Theorem** | ∮_C f(z) dz = 2πi Σ Res(f, aₖ) | Complex analysis |
| **Fourier Inversion** | f(x) = ∫ F(ω) eⁱωˣ dω/(2π) | Fourier analysis |
| **Parseval's Theorem** | ∫|f|² dx = ∫|F̂|² dω/(2π) | Signal processing |
| **Convolution Theorem** | ℱ{f*g} = ℱ{f}·ℱ{g} | Transforms |
| **Final Value Theorem** | lim_{t→∞} f(t) = lim_{s→0} sF(s) | Laplace / Z |
| **Spectral Theorem** | 𝐀 = 𝐐Λ𝐐ᵀ for symmetric 𝐀 | Linear algebra |
| **Existence & Uniqueness (Picard)** | Lipschitz condition guarantees unique ODE solution | ODE theory |

---

## Engineering Domain Map

Maps mathematical tools to the industrial problem they directly solve.

```
Signal Processing
  ├── Fourier Transform         → frequency-domain analysis, filter design
  ├── DFT / FFT                 → spectral analysis, fast convolution
  ├── Z-Transform               → discrete-time system analysis, digital filter design
  ├── Laplace Transform         → continuous-time system analysis
  └── Convolution               → LTI system response, matched filtering

Control Systems
  ├── Laplace / Transfer Function → stability analysis (poles/zeros), Bode, Nyquist
  ├── Z-Transform               → digital controller design
  ├── State-Space (Linear Alg.) → controllability, observability, LQR
  └── Eigenvalue Analysis       → system stability, modal decomposition

Structural Mechanics / FEA
  ├── PDEs (elasticity tensor)  → stress/strain fields
  ├── Finite Element Method     → discretized PDE solutions
  ├── Eigenvalue problems       → natural frequencies, buckling loads
  └── Linear systems (𝐊𝐮 = 𝐟) → stiffness matrix solution

Heat Transfer / Fluid Dynamics
  ├── Heat equation (PDE)       → transient/steady-state thermal analysis
  ├── Navier-Stokes (PDE)       → fluid flow modeling
  ├── Fourier series / modes    → analytical solutions on bounded domains
  └── Numerical PDE methods     → CFD, FDM, FVM

Communications / RF
  ├── Fourier Transform         → bandwidth, spectral efficiency
  ├── Convolution / correlation → matched filter, signal detection
  ├── Hilbert Transform         → analytic signal, envelope, instantaneous freq.
  └── Sampling theorem          → Nyquist rate, aliasing avoidance

Data Science / ML
  ├── SVD / PCA                 → dimensionality reduction, latent features
  ├── Least squares             → regression, normal equations
  ├── Eigendecomposition        → graph Laplacian, spectral clustering
  ├── Gradient calculus         → backpropagation, optimization
  └── Fourier features          → kernel approximation, periodic feature encoding

Wavelets & Time-Frequency
  ├── CWT / Scalogram           → non-stationary signal analysis, ridge extraction
  ├── DWT / Filter banks        → compression (JPEG2000), denoising, feature extraction
  ├── Wavelet packets           → best basis selection, EEG band decomposition
  └── Wavelet thresholding      → adaptive denoising, edge-preserving smoothing

Probability & Stochastic Methods
  ├── Gaussian / Bayesian       → MMSE estimation, probabilistic inference, sensor fusion
  ├── Kalman / EKF / UKF        → state estimation, SLAM, target tracking
  ├── PSD / Wiener-Khinchin     → noise characterization, system identification
  ├── ARMA models               → time-series prediction, spectral estimation
  └── Itô calculus / SDE        → financial modeling, stochastic control, diffusion

Convex Optimization
  ├── LP / QP                   → resource allocation, regression, scheduling
  ├── SOCP / SDP                → beamforming, robust control (LMI), geometry
  ├── LASSO / compressed sensing → sparse recovery, feature selection, CS imaging
  ├── ADMM                      → distributed optimization, federated learning
  └── MPC (receding-horizon QP) → real-time constrained control
```

---

## Python Toolchain

| Need | Library | Key functions |
|---|---|---|
| Symbolic math (exact) | `sympy` | `integrate`, `diff`, `dsolve`, `laplace_transform`, `fourier_transform`, `series`, `residue` |
| Numerical arrays | `numpy` | `linalg.*`, `fft.*`, `gradient`, `trapz`, `cumsum` |
| Scientific computing | `scipy` | `integrate.odeint`, `fft.fft`, `signal.*`, `linalg.*`, `optimize.*` |
| Visualization | `matplotlib`, `plotly` | time/frequency domain plots, phase portraits, 3D surfaces |
| Solving PDEs numerically | `scipy.integrate`, `fipy`, `fenics` | FDM grids, FEM meshes |

Always structure implementations as typed, documented classes or functions:

```python
from typing import Callable
import numpy as np
from scipy import signal


def compute_frequency_response(
    b: np.ndarray,
    a: np.ndarray,
    n_points: int = 1024,
    fs: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the frequency response of a digital filter.

    Args:
        b: Numerator (FIR / MA) coefficients of the filter.
        a: Denominator (IIR / AR) coefficients of the filter.
        n_points: Number of frequency points to evaluate.
        fs: Sampling frequency in Hz. Defaults to normalized (1.0).

    Returns:
        Tuple of (frequencies_hz, complex_response).

    References:
        [SRC-13] Oppenheim & Schafer, Ch. 6.
    """
    frequencies, response = signal.freqz(b, a, worN=n_points, fs=fs)
    return frequencies, response
```

---

## Reference Files Index

| File | Topics covered | Read when... |
|---|---|---|
| `references/calculus-multivariable.md` | Limits, derivatives, integrals, partial derivatives, gradient, curl, divergence, Green/Stokes/Gauss theorems, complex analysis, power series | Single/multi-variable calc, vector fields, complex integrals |
| `references/differential-equations.md` | 1st/2nd order ODEs, systems of ODEs, series solutions, Bessel/Legendre functions, heat/wave/Laplace PDEs, separation of variables, characteristics | Modeling dynamic systems, solving ODEs/PDEs analytically or numerically |
| `references/transforms.md` | Fourier series, CTFT, DTFT, DFT, FFT algorithms, Laplace transform, Z-transform, inverse transforms, convolution, ROC, frequency response | Any transform-domain problem, digital/analog filter design, spectral analysis |
| `references/linear-algebra-applied.md` | Matrix ops, eigendecomposition, SVD, PCA, LU/QR/Cholesky, least squares, matrix calculus, tensor basics | Linear systems, optimization geometry, ML mathematics |
| `references/numerical-methods.md` | Root finding, quadrature, ODE integrators, linear system solvers, interpolation, condition number, stability analysis | Computational implementations, numerical error analysis |
| `references/wavelets-multiresolution.md` | CWT, DWT, MRA theory, filter banks, Daubechies/Morlet/biorthogonal families, 2D wavelets, denoising, compression, wavelet packets | Time-frequency analysis, non-stationary signals, image processing, fault detection |
| `references/probability-stochastic.md` | Probability axioms, distributions, moments, joint Gaussian, CLT, random processes, PSD, Wiener-Khinchin, Kalman filter, SDEs, Itô calculus | Noise analysis, state estimation, stochastic modeling, spectral estimation |
| `references/convex-optimization.md` | Convex sets/functions, KKT conditions, Lagrangian duality, LP/QP/SOCP/SDP, gradient/proximal/ADMM algorithms, LASSO, compressed sensing, MPC | Constrained optimization, sparse recovery, control synthesis, ML training |
| `references/discrete-mathematics.md` | Logic & proofs, sets/relations/functions, algorithm complexity (P/NP, Master theorem), number theory, counting/combinatorics (Catalan, inclusion-exclusion, generating functions), discrete probability and Markov chains, graph theory (BFS/DFS/SCC/MST/matching), trees (B-tree, Union-Find), Boolean algebra, automata/CFG/Turing machines, algebraic structures (groups, rings, fields, lattices) | Theory of computation, algorithm design, database theory, compiler construction, network analysis, formal verification |
| `references/information-theory-coding.md` | Entropy, joint/conditional/mutual information, KL divergence, cross-entropy, AEP, source coding theorem, Huffman, arithmetic coding, LZ77/LZ78, rate-distortion, channel models (BSC, AWGN, MIMO), Shannon capacity, Shannon-Hartley, noisy channel theorem, Fano's inequality, Hamming codes, BCH, Reed-Solomon (MDS, RAID-6, QR codes), turbo codes, LDPC (belief propagation), polar codes, information theory in cryptography (perfect secrecy, unicity distance), Kolmogorov complexity | Digital communications (5G, Wi-Fi), data storage (RAID, SSD), compression (ZIP, JPEG, H.265), quantum-safe error correction, security entropy analysis |
| `references/mathematical-statistics.md` | Sufficient statistics, exponential family, MLE (Fisher information, Cramér-Rao, asymptotic normality), Bayesian estimation (conjugate priors, MAP, MCMC, HMC/NUTS), bias-variance-MSE, Rao-Blackwell/UMVUE, confidence intervals (z/t/χ²/bootstrap/BCa), hypothesis testing (Neyman-Pearson, common tests, p-value, Bonferroni/BH correction, power analysis, sample size), OLS/Ridge/LASSO/elastic net regression, GLMs (logistic, Poisson), KDE, permutation tests, rank tests | Data science inference, A/B testing, model selection, regression analysis, clinical trials, survey design |
| `references/formal-methods-logic.md` | Natural deduction, sequent calculus, resolution refutation, FOL decidability, Hoare logic (triples, proof rules, weakest precondition/wp calculus, loop invariants), LTL (X/F/G/U operators, specification patterns), CTL (path quantifiers, fixed-point operators), model checking (explicit SPIN, symbolic BDD/NuSMV, bounded SAT-based/CBMC), DPLL + CDCL SAT, SMT theories (LIA/LRA/BV/Arrays, Z3), type theory (STLC, System F, HM type inference, dependent types), Curry-Howard correspondence, operational/denotational semantics, abstract interpretation (Galois connections, widening/narrowing), Astrée/Frama-C | Program verification (Dafny, SPARK), compiler type checkers, hardware verification, security analysis (KLEE, symbolic execution, SMT-backed tools) |
| `references/cryptography-security.md` | Classical ciphers (shift, affine, Vigenère, OTP), formal cryptosystem definition, hashing and check digits (UPC/ISBN/LUHN/CRC), RSA full derivation (Rosen §4.6 verified), OAEP/RSA-PSS padding, Diffie-Hellman (discrete log), digital signatures (DSA/ECDSA/EdDSA), AES block modes (GCM/CBC/CTR), cryptographic hash functions (SHA-256/SHA-3/BLAKE3), HMAC, AEAD, KDF/PBKDF2/HKDF, password hashing (Argon2id/bcrypt), ECC/X25519/Ed25519, post-quantum (ML-KEM Kyber, ML-DSA Dilithium), TLS 1.3, JWT/OAuth 2.0, homomorphic encryption, ZKP, Shamir secret sharing, OWASP security patterns | Secure application development, authentication, API security, protocol design, key management |
| `references/engineering-applications.md` | Control systems, DSP, FEA, heat transfer, fluid dynamics, communications, power systems — connecting math to physical systems | Industry problem framing, applied derivations, system design |
