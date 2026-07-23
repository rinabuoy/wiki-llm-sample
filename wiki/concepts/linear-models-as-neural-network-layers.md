---
title: Linear Models as Neural Network Layers
type: concept
tags:
- neural-networks
- linear-algebra
aliases: []
sources:
- sources/module-1-linear-models.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

A linear model computes `y = Wxᵀ + w0`, where `x` is a feature vector, `W` is a weight
matrix, and `w0` is a bias term (often folded into `W` via an augmented "bias feature"
column of 1s). Stacking several such linear transformations with a non-linear
**activation function** `g` in between produces a (deep) neural network:

```
Y = g_p( ... g_1( W_1 Xᵀ ) ... )
```

A single linear layer followed by one activation recovers several classic models as
special cases:

| Model | Output activation `g` | Task |
|---|---|---|
| Linear regression | identity | regression |
| Logistic regression | sigmoid | binary classification |
| Multiclass logistic regression / softmax classifier | softmax | multi-class classification |

## Discussion

- Without non-linear activations, stacking linear layers is pointless: a composition of
  linear functions is still linear (`f(x+y)=f(x)+f(y)`, `f(ax)=af(x)`), so an arbitrarily
  deep "linear" network has the same representational power as a single layer.
- Common activation functions: **sigmoid** `g(z)=1/(1+e⁻ᶻ)` (squashes to (0,1), used for
  binary probabilities), **tanh** (squashes to (-1,1)), **ReLU** `g(z)=max(0,z)` (cheap,
  avoids vanishing gradients, most common in hidden layers), and **softmax**
  `e^zᵢ / Σⱼ e^zⱼ` (turns a vector of scores into a probability distribution over classes;
  a "temperature" parameter T can sharpen or flatten that distribution).
- Output-layer activation is chosen by task: identity for regression, sigmoid for binary
  classification, softmax for multi-class classification.
- A worked example ("Lincoln Classifier"): given a small pixel image, a two-layer network
  with random weights `W1, W2 ~ N(0,1)` outputs `p(lincoln)`; training pushes that
  probability toward 1 for Lincoln images and 0 for others, which motivates why a loss
  function and gradient-based training are needed — see [[Loss Functions]] and
  [[Gradient Descent and Optimization]].

## Related

- [[Module 1 - Linear Models]]
- [[Loss Functions]]
- [[Gradient Descent and Optimization]]
- [[Data Preprocessing for Neural Networks]]
