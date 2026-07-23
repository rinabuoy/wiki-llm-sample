---
title: Model Evaluation Metrics
type: concept
tags:
- evaluation
- classification
- regression
aliases: []
sources:
- sources/module-1-linear-models.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

Metrics used to judge trained-model quality in human-readable terms, distinct from the
[[Loss Functions|loss]] used during training.

## Discussion

**Regression:**
- **R-squared (R²)**, range [0,1]: `1 − Σ(yᵢ−ŷᵢ)² / Σ(yᵢ−ȳ)²`. Baseline score for how well
  predictions fit observed data relative to just predicting the mean.

**Classification — confusion matrix and derived metrics:**
- A `k×k` **confusion matrix** cross-tabulates predicted vs true class (true
  positive/negative, false positive/negative).
- **Accuracy** = `(tp+tn)/(tp+tn+fp+fn)` — default metric, but misleading for imbalanced
  classes.
- **Precision** = `tp/(tp+fp)` — higher precision means fewer false positives.
- **Recall** = `tp/(tp+fn)` — higher recall means fewer false negatives.
- **F1-score** = `2·precision·recall/(precision+recall)` — harmonic mean, a good default
  overall metric when both false positives and false negatives matter.
- The classification **threshold** (default 0.5) trades precision against recall: raising
  it reduces false positives but raises false negatives, and vice versa (shown via
  contrasting confusion tables at threshold π=0.4 vs π=0.6).
- **ROC curve**: plots True Positive Rate vs False Positive Rate as the threshold sweeps
  across all values. An ideal curve hugs the top-left corner; the diagonal is a random
  classifier.
- **AUC** (Area Under the ROC Curve): single-number summary of classifier performance
  across all thresholds — higher is better, used to compare classifiers (logistic
  regression, k-NN, decision trees, etc.) independent of a specific threshold choice.

## Related

- [[Module 1 - Linear Models]]
- [[Loss Functions]]
- [[Regularization]]
