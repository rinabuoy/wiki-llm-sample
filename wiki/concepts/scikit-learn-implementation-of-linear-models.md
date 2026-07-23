---
title: Scikit-learn Implementation of Linear Models
type: concept
tags:
- scikit-learn
- implementation
- linear-models
aliases: []
sources:
- sources/module-1-linear-models-scikit-learn.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

The practical scikit-learn API for fitting and tuning linear models — the "batteries
included" counterpart to hand-rolling the same math in PyTorch (see
[[PyTorch Fundamentals]]).

## Discussion

**Preprocessing pipeline** — `ColumnTransformer` composes per-column transforms into one
fitted object: `OneHotEncoder` for nominal features (`drop='first'` for dummy encoding,
avoiding multicollinearity), `OrdinalEncoder` with an explicit `categories` ordering
for ordinal features, and `StandardScaler`/`MinMaxScaler` for numeric ones. Fit only on
the training split, then `.transform()` both train and test — never fit on test data.

**Regularized linear models** — `LinearRegression` (no penalty), `Ridge(alpha=λ)` (L2,
shrinks coefficients continuously, never to exactly zero), `Lasso(alpha=λ)` (L1, drives
some coefficients to exactly zero — automatic feature selection), `ElasticNet(alpha,
l1_ratio)` (mix of both). See [[Regularization]] for the underlying loss terms.

**Classification** — `LogisticRegression(penalty=...)` takes `C`, the *inverse* of
regularization strength (`C = 1/λ`): smaller `C` means *stronger* regularization, the
opposite of `alpha` in the regression classes. `penalty='l1'` requires
`solver='liblinear'`; `multi_class='multinomial'` + softmax link gives K-class softmax
regression, each class getting its own weight vector (linear decision boundaries).

**Hyperparameter tuning** — `GridSearchCV(estimator, param_grid, cv=KFold(...))` searches
a grid of hyperparameters using k-fold cross-validation purely on the training set;
`StratifiedKFold` preserves class balance per fold for classification. The held-out test
set is touched exactly once, after tuning, for the final generalization estimate.

**Evaluation** — regression: `r2_score`, `mean_squared_error`, `mean_absolute_error`,
compared train vs test to gauge an "overfit gap". Classification:
`confusion_matrix`/`ConfusionMatrixDisplay`, `precision_score`/`recall_score`/`f1_score`,
`classification_report`, `roc_curve`/`roc_auc_score` — shifting the decision threshold
trades recall for precision (lower threshold → higher recall, more false positives). See
[[Model Evaluation Metrics]].

## Related

- [[Module 1 - Linear Models Scikit-Learn]]
- [[Linear Models as Neural Network Layers]]
- [[Regularization]]
- [[Model Evaluation Metrics]]
- [[Data Preprocessing for Neural Networks]]
- [[PyTorch Fundamentals]]
