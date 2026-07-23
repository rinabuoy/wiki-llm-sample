---
title: Module 1 - Linear Models
type: source
tags:
- applied-ai-mastery
- lecture-slides
aliases: []
sources: []
created: '2026-07-21'
updated: '2026-07-21'
---

## Summary

71-slide lecture deck, "Module 1 – From Linear Models to Deep Learning", part of the
*Applied AI Mastery Program* taught by [[Rina Buoy]]. It builds up from basic linear
algebra to deep neural networks by showing that linear regression, logistic regression,
and the softmax classifier are all special cases of a single linear layer `Y = g(WXᵀ + w0)`
with a particular choice of activation `g`. It then covers how such models are trained
(loss functions, gradient descent, backpropagation), the practical difficulties of
training (hyperparameters, over/underfitting), regularization techniques, data
preprocessing, and standard evaluation metrics.

## Key takeaways

- A linear model is `y = Wxᵀ + w0`; stacking layers with non-linear activations between
  them turns it into a (deep) neural network — see [[Linear Models as Neural Network Layers]].
- Linear regression (identity activation), logistic regression (sigmoid), and softmax
  classification (softmax activation) are all the *same* linear layer, differing only in
  the output activation and loss function.
- Non-linear activation functions (sigmoid, tanh, ReLU) are what let a network approximate
  arbitrarily complex, non-linear decision boundaries — a purely linear stack of layers
  collapses back into one linear function no matter how deep.
- Training = minimizing a loss function over the weights, `W* = argmin_W J(W)`. See
  [[Loss Functions]] and [[Gradient Descent and Optimization]].
- Linear regression has a closed-form solution (`W = (XᵀX)⁻¹Xᵀy`); most other losses are
  non-convex and require iterative gradient descent.
- Training neural networks is hard because of three families of hyperparameters:
  optimizer-related (learning rate, epochs), model-related (depth, width, loss choice),
  and preprocessing-related (standardization, min-max scaling).
- Overfitting is controlled via [[Regularization]] (dropout, early stopping, L1/L2 —
  Ridge vs Lasso) and via proper data splitting (train/dev/test, k-fold cross-validation).
- Model quality is judged with task-appropriate metrics — see [[Model Evaluation Metrics]]
  (R² for regression; confusion matrix, precision/recall/F1, ROC/AUC for classification).
- Raw data (categorical, numeric, image, audio, text) must be converted into numeric
  feature vectors before it reaches a linear layer — see
  [[Data Preprocessing for Neural Networks]].

## Cited by

- [[Rina Buoy]]
- [[Linear Models as Neural Network Layers]]
- [[Loss Functions]]
- [[Gradient Descent and Optimization]]
- [[Regularization]]
- [[Model Evaluation Metrics]]
- [[Data Preprocessing for Neural Networks]]
