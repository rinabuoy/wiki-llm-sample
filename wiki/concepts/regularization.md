---
title: Regularization
type: concept
tags:
- neural-networks
- training
aliases: []
sources:
- sources/module-1-linear-models.md
- sources/module-1-linear-models-pytorch.md
created: '2026-07-21'
updated: '2026-07-22'
---

## Definition

Regularization techniques discourage a model from overfitting the training data so it
generalizes better to unseen data.

## Discussion

- **Dropout**: during training, randomly zero out a fraction (typically 50%) of
  activations in a layer, forcing the network to not rely on any single node
  (`tf.keras.layers.Dropout(p=0.5)` / `torch.nn.Dropout(p=0.5)`).
- **Early stopping**: stop training once the *development/validation* loss starts to rise
  even as *training* loss keeps falling — that inflection point marks the transition from
  underfitting to overfitting.
- **L1 regularization** (Lasso): adds `λ Σ|Wᵢ|` to the loss. Coefficients shrink toward
  zero and get nullified (set exactly to 0) quickly as `λ` (the regularization factor,
  sometimes called `α`) increases — effectively performs feature selection. That *exact*
  zeroing relies on solving with **coordinate descent** (what sklearn's `Lasso` uses).
  Optimizing the same L1-penalized loss with plain **gradient descent** (as in a manual
  PyTorch training loop) only pushes weights toward *near*-zero, not exact zero — see
  [[PyTorch Fundamentals]].
- **L2 regularization** (Ridge): adds `λ Σ Wᵢ²` to the loss. Coefficients shrink smoothly
  as `λ` increases but are rarely nullified entirely.
- **Data splitting** also guards against overfitting to the test set itself:
  - *Train/Dev/Test split* (e.g. 80/10/10): train multiple candidate models on Train,
    select the best via Dev-set metrics (hyperparameter tuning + model selection), retrain
    the winner on Train+Dev, then report final generalization performance on the untouched
    Test set. Common for deep learning.
  - *K-fold cross-validation*: partition data into k folds; iterate k times, each time
    holding out one fold as the test set and training on the rest, then average
    performance across folds. Common for classical machine learning.

## Related

- [[Module 1 - Linear Models]]
- [[Module 1 - Linear Models PyTorch]]
- [[Gradient Descent and Optimization]]
- [[Loss Functions]]
- [[Model Evaluation Metrics]]
- [[PyTorch Fundamentals]]
