---
title: Module 1 - Linear Models PyTorch
type: source
tags:
- applied-ai-mastery
- hands-on
- pytorch
aliases: []
sources: []
created: '2026-07-22'
updated: '2026-07-22'
---

## Summary

A runnable notebook (`raw/Module_1_Linear_Models_Pytorch.ipynb`), part of the *Applied AI
Mastery Program* taught by [[Rina Buoy]]. It's the PyTorch counterpart to
[[Module 1 - Linear Models Scikit-Learn]] — the exact same lecture content (`Y = WXᵀ +
w₀`, regularized regression, logistic/softmax classification) on the same three
datasets (California Housing, Breast Cancer, Iris), but implemented with `nn.Linear` +
manual training loops instead of sklearn estimators. Its value is making concrete
*exactly* how each sklearn abstraction maps onto raw PyTorch mechanics.

## Key takeaways

- **Ridge (L2)** has a direct PyTorch equivalent: `optim.Adam(params, weight_decay=λ)`.
- **Lasso (L1)** has no built-in flag — it's a manual `loss += λ·Σ|w|` penalty term.
  Because plain gradient descent (unlike sklearn's coordinate-descent solver) never
  drives a weight to *exactly* zero, PyTorch Lasso only achieves *near*-zero
  coefficients, not sklearn's exact sparsity — a genuinely new insight over the sklearn
  notebook. See [[Regularization]] and [[PyTorch Fundamentals]].
- **ElasticNet** = `weight_decay` (L2 half) + manual L1 penalty (L1 half), combined.
- **`GridSearchCV` has no PyTorch equivalent** — hyperparameter tuning means writing the
  K-Fold/`StratifiedKFold` loop by hand: train a fresh model per fold × candidate value,
  average validation RMSE/AUC, pick the best.
- **Logistic regression** = `nn.Linear(n,1)` + `BCEWithLogitsLoss` (sigmoid folded into
  the loss for numerical stability); **softmax/multiclass** = `nn.Linear(n,K)` +
  `CrossEntropyLoss` (softmax folded in likewise).
- Confirms the closing equivalence table from [[Module 1 - Linear Models Scikit-Learn]]
  by actually running both sides: sklearn class ↔ `nn.Linear` + specific loss +
  specific optimizer configuration.

## Cited by

- [[Rina Buoy]]
- [[PyTorch Fundamentals]]
- [[Regularization]]
