---
title: Module 1 - The Basics
type: source
tags:
- applied-ai-mastery
- lecture-slides
aliases: []
sources: []
created: '2026-07-22'
updated: '2026-07-22'
---

## Summary

76-slide lecture deck, "Module 1 – The Basics from the Minimalist Perspective," part of
the *Applied AI Mastery Program* taught by [[Rina Buoy]]. Unlike the other two Module 1
decks (which build up linear models and CNNs/RNNs), this one covers the underlying math
toolkit: descriptive statistics and probability, linear algebra, and vector calculus —
the prerequisites needed to read the other lectures' formulas and derivations.

## Key takeaways

- Descriptive statistics (mean/median/mode, variance/std dev, percentiles, skewness,
  correlation) summarize a dataset's center, spread, and shape — see
  [[Descriptive Statistics]].
- Probability formalizes uncertainty: sample spaces, events, conditional probability,
  independence, random variables (discrete vs continuous, PMF/PDF/CDF), expected value,
  a handful of core distributions (Bernoulli, Binomial, Categorical, Gaussian), and
  Bayes' Rule for updating beliefs on new evidence — see [[Probability Fundamentals]].
- Linear algebra objects (scalars, vectors, matrices, tensors) and operations (dot
  product, matrix multiplication) are the data structures neural networks are built
  from; a linear layer is literally vector-matrix multiplication `y = Wx + b` — see
  [[Linear Algebra Foundations]] and [[Linear Models as Neural Network Layers]].
- Vector calculus — derivatives, partial derivatives, the gradient, and the chain rule —
  is "the engine of machine learning": it's what lets [[Gradient Descent and Optimization]]
  and backpropagation compute how to adjust millions of weights to reduce a
  [[Loss Functions|loss]]. Automatic differentiation (autograd) in PyTorch/TensorFlow/
  JAX/Keras handles this automatically via `.backward()`. See
  [[Vector Calculus for Machine Learning]].
- Real loss landscapes for deep networks are non-convex (many local minima, saddle
  points), unlike the single global minimum of a convex problem — this is why optimizers
  like Adam need momentum to escape shallow valleys.

## Cited by

- [[Rina Buoy]]
- [[Descriptive Statistics]]
- [[Probability Fundamentals]]
- [[Linear Algebra Foundations]]
- [[Vector Calculus for Machine Learning]]
