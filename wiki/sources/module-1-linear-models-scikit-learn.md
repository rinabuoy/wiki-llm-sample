---
title: Module 1 - Linear Models Scikit-Learn
type: source
tags:
- applied-ai-mastery
- hands-on
- scikit-learn
aliases: []
sources: []
created: '2026-07-22'
updated: '2026-07-22'
---

## Summary

A runnable notebook (`raw/Module_1_LinearModels_ScikitLearn.ipynb`), part of the
*Applied AI Mastery Program* taught by [[Rina Buoy]]. It's the scikit-learn hands-on
companion to [[Module 1 - Linear Models]] — the same math (`Y = WXᵀ + w₀`, activation
functions, regularization, evaluation metrics) worked end-to-end on three real datasets:
California Housing (regression), Breast Cancer (binary classification), and Iris
(multiclass/softmax). Closes with a table mapping every sklearn concept to its PyTorch
equivalent.

## Key takeaways

- Confirms the linear-layer framing numerically: `Y = W @ X.T + w0` with explicit shape
  checks — see [[Linear Models as Neural Network Layers]].
- **Preprocessing** — nominal features get `OneHotEncoder` (dummy encoding drops one
  column to avoid multicollinearity), ordinal features get `OrdinalEncoder` with an
  explicit category order, numeric features get `StandardScaler`/`MinMaxScaler`, all
  composed via `ColumnTransformer`. See [[Data Preprocessing for Neural Networks]] and
  [[Scikit-learn Implementation of Linear Models]].
- **Regularization in practice** — Ridge (L2) shrinks coefficients continuously but never
  to zero; Lasso (L1) zeroes some out entirely (automatic feature selection, 3/12
  coefficients zeroed in the housing example); ElasticNet mixes both. Regularization
  paths plotted across `alpha` visually confirm this. See [[Regularization]].
- **Hyperparameter tuning** — `GridSearchCV` + `KFold`/`StratifiedKFold` search over
  `alpha` (regression) or `C` (classification, the *inverse* of regularization
  strength — smaller `C` means *stronger* regularization) using only the training set;
  the test set is touched once, at the end, for a final generalization estimate.
- **Evaluation** — regression compared via train/test R²/MSE/MAE and an "overfit gap";
  classification via confusion matrix, precision/recall/F1, and ROC-AUC, including how
  shifting the decision threshold trades recall for precision. See
  [[Model Evaluation Metrics]].
- Multiclass softmax regression gives each class its own weight vector, producing
  **linear** decision boundaries — demonstrated visually on Iris petal features.
- Closing equivalence table: `LinearRegression`→`nn.Linear`+`MSELoss`,
  `Ridge`→`weight_decay`, `LogisticRegression`→`nn.Linear`+`BCEWithLogitsLoss`,
  softmax `LogisticRegression`→`nn.Linear`+`CrossEntropyLoss` — see
  [[PyTorch Fundamentals]].

## Cited by

- [[Rina Buoy]]
- [[Scikit-learn Implementation of Linear Models]]
