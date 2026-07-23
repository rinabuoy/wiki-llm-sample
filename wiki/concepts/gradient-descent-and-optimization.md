---
title: Gradient Descent and Optimization
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

Gradient descent minimizes a [[Loss Functions|loss]] surface `J(W)` by iteratively moving
weights opposite the gradient:

```
1. Initialize weights randomly, W ~ N(0, σ²)
2. Loop until convergence:
   3. Compute gradient ∂J(W)/∂W   (via backpropagation)
   4. Update weights: W ← W − η · ∂J(W)/∂W     (η = learning rate)
5. Return weights
```

## Discussion

- **Backpropagation** computes `∂J(W)/∂W` layer by layer via the chain rule, e.g. for a
  two-weight chain `x → z1 → ŷ → J`: `∂J/∂w1 = ∂J/∂ŷ · ∂ŷ/∂z1 · ∂z1/∂w1`.
- **Closed-form vs iterative**: linear regression under MSE has a closed-form solution,
  `W = (XᵀX)⁻¹Xᵀy` (solving `∂J/∂W = 0` directly), analogous to solving `2x+3=7`
  algebraically. Most other loss surfaces have no such algebraic solution (analogous to
  `x = cos(x)`) and require gradient descent's iterative approximation instead.
- **Loss surfaces are typically non-convex**, with multiple local minima — random weight
  initialization plus iterative descent is used to search for a good one, not
  necessarily the global optimum.
- **Batch size variants**:
  - *Vanilla/batch gradient descent*: gradient computed over all `n` samples each step —
    `O(n)` per step, accurate but expensive at scale (e.g. 1M samples).
  - *Stochastic gradient descent (SGD)*: gradient computed from a single random sample
    per step — cheap but noisy.
  - *Mini-batch gradient descent*: gradient averaged over a batch of `B` samples,
    `∂J/∂W = (1/B) Σₖ ∂Jₖ/∂W` — the common middle ground, fast and a good gradient
    estimate.
- **Learning rate (η)** is critical: too high causes oscillation/divergence around the
  minimum, too low makes convergence very slow; **adaptive learning rate** optimizers
  (SGD, Adam, Adadelta, Adagrad, RMSProp — available as `tf.keras.optimizers.*` /
  `torch.optim.*`) adjust step size automatically during training.
- Training difficulty comes from three families of hyperparameters: optimizer-related
  (learning rate, epochs → training *stability*), model-related (depth, width, loss
  choice → model *generalization*, see [[Regularization]]), and preprocessing-related
  (standardization, min-max → model *convergence*, see
  [[Data Preprocessing for Neural Networks]]).

## Related

- [[Module 1 - Linear Models]]
- [[Loss Functions]]
- [[Linear Models as Neural Network Layers]]
- [[Regularization]]
