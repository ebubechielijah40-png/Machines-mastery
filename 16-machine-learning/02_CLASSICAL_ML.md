# 02 — Classical machine learning

Classical ML is where the discipline becomes concrete: representation, objective, inductive bias, generalization, and evaluation can be studied without the scale of modern deep networks.

## Supervised learning

We observe pairs `(x, y)` and choose a parameterized function `f_theta(x)`. Training minimizes empirical loss on a sample. The real target, however, is expected performance on future data from the deployment distribution. The gap between training performance and deployment performance is where overfitting, leakage, shift, and poor measurement enter.

### Linear regression

`y_hat = w^T x + b` and mean squared error form a simple system whose geometry can be inspected directly. Linear regression assumes the relationship is adequately represented by a linear combination at the chosen feature level. Nonlinearity can sometimes be introduced by changing the features rather than the learner.

### Logistic regression

Logistic regression models log-odds linearly and maps the score through a sigmoid. Its decision boundary is linear in feature space. It can be an excellent baseline because it is cheap, interpretable, and difficult to hide behind.

### Trees and ensembles

A decision tree recursively partitions feature space. Deep trees can memorize training examples. Random forests reduce variance by averaging diverse trees. Gradient boosting builds a sequence of weak learners that correct residual error. These models reveal a general principle: strong systems can arise from composition, not only from one complex component.

## Leakage example

Suppose a hospital model predicts whether a patient will be admitted, and a feature contains a code written only after the admission decision. Random train/test splitting may show spectacular performance because the future leaked into the input. No optimizer can repair a bad causal timeline.

## Experiment: capacity versus generalization

Generate noisy points from `y = 2x + epsilon`. Fit models of increasing polynomial degree. Measure training and held-out error. Plot both. The expected pattern is underfitting at too little capacity, a useful region, then variance/overfit as capacity becomes excessive relative to data and regularization.

## Production questions

- What happens if the training data are from Lagos but deployment shifts to another population?
- What metric matters if false negatives cost 100× false positives?
- What does a 95% validation score conceal when one subgroup has 60%?
- Can the target itself be measured reliably?

## Mastery tasks

Implement linear regression from scratch, logistic regression with gradient descent, a tiny decision tree split finder, and a leakage demonstration. For each, write tests, report assumptions, and compare against a library implementation only after your version works.
