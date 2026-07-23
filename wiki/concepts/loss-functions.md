---
title: Loss Functions
type: concept
tags:
- neural-networks
- training
aliases: []
sources:
- sources/module-1-linear-models.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

A loss (cost) function `L(f(x), y)` measures how wrong a model's prediction is for a
single example; training is framed as minimizing the average loss over all training
examples:

```
W* = argmin_W  (1/n) Σᵢ L(f(x⁽ⁱ⁾; W), y⁽ⁱ⁾)  =  argmin_W J(W)
```

## Discussion

Common losses covered, matched to task type:

- **Mean-Squared Error (MSE)** — `(1/n) Σ (yᵢ − f(xᵢ))²` — regression.
- **Mean-Absolute Error (MAE)** — `(1/n) Σ |yᵢ − f(xᵢ)|` — regression, more robust to
  outliers than MSE.
- **Binary Cross-Entropy** — `(1/n) Σ yᵢ log(pᵢ) + (1−yᵢ) log(1−pᵢ)` — binary
  classification, paired with a sigmoid output.
- **Cross-Entropy** — `(1/n) Σ yᵢ log(pᵢ)` — multi-class classification, paired with a
  softmax output; `yᵢ` is 1 for the true class of sample i and `pᵢ` is the predicted
  probability for that class.

Losses are a *proxy* for human-readable performance, not the end goal itself — that's why
separate [[Model Evaluation Metrics]] (accuracy, F1, R², AUC, etc.) exist alongside the
loss used for training.

Because `J(W)` is generally a **non-convex** surface with many local minima, there is
usually no closed-form way to jump straight to the minimum (except for linear
regression under MSE, which has one — see [[Gradient Descent and Optimization]]).
Training instead walks downhill iteratively.

## Related

- [[Module 1 - Linear Models]]
- [[Linear Models as Neural Network Layers]]
- [[Gradient Descent and Optimization]]
- [[Model Evaluation Metrics]]
