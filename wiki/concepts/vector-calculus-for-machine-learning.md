---
title: Vector Calculus for Machine Learning
type: concept
tags:
- calculus
- foundations
- optimization
aliases: []
sources:
- sources/module-1-the-basics.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

The calculus machinery — derivatives, gradients, the chain rule — that lets a model find
weights minimizing its [[Loss Functions|loss]]: plotting every weight combination against
the resulting error creates a landscape of hills and valleys, and training means finding
the lowest point in that landscape.

## Discussion

- **Derivative** `f'(x) = df/dx` — the instantaneous slope of a function at a point.
  Standing on the "loss hill," it tells you how steep the ground is and whether a step
  forward goes up (positive slope) or down (negative slope).
- **Partial derivative** `∂f/∂xᵢ` — how the loss changes if you tweak *one* weight while
  freezing all the others (real models have millions of weights, not one).
- **Gradient** `∇f` — the vector packaging all partial derivatives together. Crucial
  property: it always points in the direction of **steepest ascent**, so gradient
  *descent* moves in `−∇f`. See [[Gradient Descent and Optimization]].
- **Chain rule** — `dy/dx = (dy/du)·(du/dx)` for a composed function `y=g(u(x))`. This is
  the engine of **backpropagation**: a neural network is a deeply nested function (e.g.
  `F(x) = w₃ᵀσ(W₂ᵀσ(W₁ᵀx+b₁)+b₂)+b₃`), and the chain rule lets you compute the gradient
  of the loss with respect to every weight by propagating derivatives backward through
  the layers.
- **Automatic differentiation (autograd)** — PyTorch, TensorFlow, Keras, and JAX compute
  all of the above automatically (`.backward()`); you never hand-derive the chain rule
  for a real network.
- **Convex vs non-convex** — a convex loss surface is a single bowl with one global
  minimum, and gradient descent is mathematically guaranteed to find it (e.g. linear
  regression under MSE). Deep network loss landscapes are non-convex — rugged, with local
  minima (shallow valleys) and saddle points (flat, zero-slope regions that aren't
  minima) — which is why optimizers like Adam carry momentum to avoid getting stuck.

## Related

- [[Module 1 - The Basics]]
- [[Gradient Descent and Optimization]]
- [[Loss Functions]]
- [[Linear Algebra Foundations]]
