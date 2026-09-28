# Prerequisite Bridge: ML Systems and Model Serving

Learner NOT STARTED. Before studying this laboratory, ensure the following concepts are understood:

## 1. Feature Representation and Normalization
- Raw features differ in units, scales, and variances.
- Standard z-score scaling centers features around zero with unit variance:
  $$z = \frac{x - \mu}{\sigma}$$
- The mean $\mu$ and standard deviation $\sigma$ must be computed exclusively from training data and applied identically during inference.

## 2. Gradient Descent and Logistic Regression
- Logistic regression models binary probability using the sigmoid function:
  $$\sigma(z) = \frac{1}{1 + e^{-z}}, \quad z = b + \sum_{j} w_j x_j$$
- Cross-entropy loss penalizes confident incorrect predictions:
  $$\mathcal{L} = - [y \ln(p) + (1-y) \ln(1-p)]$$
- Stochastic Gradient Descent (SGD) updates weights along the negative gradient:
  $$w_j \leftarrow w_j - \eta \left( (p - y) x_j + \lambda w_j \right)$$

## 3. Covariate Shift and Population Stability Index (PSI)
- In production, input feature distributions $P(X)$ often shift over time even if $P(Y|X)$ remains constant.
- PSI quantifies distribution divergence between a baseline $E$ (expected) and production sample $A$ (actual):
  $$PSI = \sum_{k=1}^K (A_k - E_k) \times \ln\left(\frac{A_k}{E_k}\right)$$
- Standard operational interpretation:
  - $PSI < 0.10$: Negligible shift; distribution stable.
  - $0.10 \le PSI \le 0.25$: Moderate shift; warranting investigation.
  - $PSI > 0.25$: Significant shift; model retraining or failover required.
