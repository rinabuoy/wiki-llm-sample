---
title: Linear Algebra Foundations
type: concept
tags:
- linear-algebra
- foundations
aliases: []
sources:
- sources/module-1-the-basics.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

The core data structures neural networks are built from, in increasing dimensionality:
**scalar** (0-D, a single number), **vector** (1-D array, magnitude + direction),
**matrix** (2-D grid of rows/columns), **tensor** (n-D array — scalars/vectors/matrices
are all technically tensors). Notation: scalars lowercase italic (`x`), vectors
lowercase bold (**x**), matrices uppercase bold (**W**).

## Discussion

**Examples:** a learning rate or loss value is a scalar; a dataset row is a vector; a
grayscale image (height × width) is a matrix; a batch of color images is a 4D tensor
`[batch_size, height, width, channels]`.

**Core operations**

- **Addition** — element-wise, requires identical shapes.
- **Dot product** — `a·b = Σ aᵢbᵢ = |a||b|cos(θ)`, collapses two equal-length vectors
  into one scalar measuring how much they "point" in the same direction. Used directly
  for similarity (e.g. cosine similarity between face embeddings).
- **Vector-matrix multiplication** — `y = Wx`: each output element is the dot product of
  a row of `W` with the input vector `x`. Shapes: `(m,n) × (n,) → (m,)`. This *is* a
  linear transformation — e.g. a 2D rotation matrix `[[cos θ, −sin θ],[sin θ, cos θ]]` or
  a scaling matrix `[[sₓ,0],[0,sᵧ]]`.
- **Matrix multiplication** — `y = ABx`; multiplying `A(m×n)` by `B(n×p)` gives an
  `(m×p)` matrix `C = AB` that is the *composition* of the two linear transformations
  (inner dimensions must match).
- **Norms** (vector "length", used for loss/distance) — `L¹` (Manhattan) `Σ|xᵢ|`, `L²`
  (Euclidean) `√(Σxᵢ²)`.

**Why it matters for ML:** a linear layer is literally `y = Wx + b` (vector-matrix
multiply + bias add) — see [[Linear Models as Neural Network Layers]]. Stacking these
with non-linear activations between them is what makes a deep neural network.

## Related

- [[Module 1 - The Basics]]
- [[Linear Models as Neural Network Layers]]
- [[Vector Calculus for Machine Learning]]
