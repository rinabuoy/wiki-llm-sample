---
title: PyTorch Fundamentals
type: concept
tags:
- pytorch
- deep-learning
- implementation
aliases: []
sources:
- sources/pytorch-in-one-hour.md
- sources/module-1-linear-models-pytorch.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

PyTorch is an open-source, Python-based deep learning library, structured as three parts:
a **tensor library** (array programming with seamless CPU↔GPU execution), an **automatic
differentiation engine** (autograd), and a **deep learning toolkit** (layers, losses,
optimizers, data utilities).

## Discussion

**Tensors** — `torch.tensor(...)` generalizes scalars/vectors/matrices to any rank (0D,
1D, 2D, 3D+), mirroring [[Linear Algebra Foundations]]. Python ints default to
`torch.int64`, floats to `torch.float32` (the deep-learning workhorse: enough precision,
less memory than float64, GPU-optimized). Core ops: `.shape`, `.reshape`/`.view`, `.T`,
`.matmul`/`@`.

**Computation graphs & autograd** — every operation on a tensor with `requires_grad=True`
is recorded into a directed graph. Calling `.backward()` on a final loss walks that graph
right-to-left, applying the **chain rule** at each node to accumulate `.grad` on every
leaf tensor — this is backpropagation, made concrete. See
[[Vector Calculus for Machine Learning]] and [[Gradient Descent and Optimization]]. In
practice you almost never call the low-level `grad(...)` form by hand.

**Building models** — subclass `torch.nn.Module`: define layers in `__init__` (often
wrapped in `nn.Sequential`), describe the forward data flow in `forward`. Autograd
derives `backward` automatically. Networks return raw **logits**; PyTorch's
classification losses (e.g. `cross_entropy`) fold softmax in internally for numerical
stability, so you apply `softmax`/`argmax` explicitly only when you want probabilities
or a prediction. Random weight initialization breaks symmetry so neurons learn different
things; seed with `torch.manual_seed` for reproducibility.

**Data pipelines** — a `Dataset` implements `__getitem__`/`__len__` for one example; a
`DataLoader` wraps it to handle batching, shuffling, and (optionally, via `num_workers`)
parallel loading. `drop_last=True` drops an undersized final batch that could
destabilize training.

**Training loop** — always the same five steps: forward pass → compute loss (see
[[Loss Functions]]) → `optimizer.zero_grad()` (gradients accumulate by default, so reset
them) → `loss.backward()` → `optimizer.step()`. `model.train()`/`model.eval()` toggle
layers like dropout/batch norm that behave differently at train vs inference time.

**Persistence** — save/load the **`state_dict`** (a dict of learned weights/biases), not
the whole Python object; recreate the same architecture, then load the dict into it.

**Regularization in PyTorch** — there's no `Ridge`/`Lasso` class; regularization is
assembled by hand. L2 (Ridge-equivalent) comes for free via the optimizer's
`weight_decay` argument (e.g. `optim.Adam(model.parameters(), weight_decay=λ)`). L1
(Lasso-equivalent) has no built-in flag — add `loss = loss + l1_lam * sum(w.abs().sum()
for w in model.parameters())` manually. Because plain gradient descent (unlike sklearn's
Lasso, which uses coordinate descent) never drives a weight to *exactly* zero, this only
gives *near*-zero coefficients — see [[Regularization]]. Likewise there's no
`GridSearchCV`: hyperparameter search over `weight_decay`/`l1_lam` means writing the
K-Fold (or `StratifiedKFold`) loop yourself, training a fresh model per fold/value
combination and averaging validation metrics.

**Devices & scaling** — a tensor's **device** (`cpu`, `cuda`, `mps`) determines where it
lives and computes; all tensors in one operation must share a device. Single-GPU training
needs only `model.to(device)` + moving each batch to `device`. Multi-GPU scaling uses
**`DistributedDataParallel` (DDP)**: one process per GPU, each with a model copy fed a
different data slice via `DistributedSampler`, with gradients averaged/synced across
copies — this requires launching via `torchrun` and cannot run inside a notebook.

## Related

- [[PyTorch in One Hour]]
- [[Module 1 - Linear Models PyTorch]]
- [[Linear Algebra Foundations]]
- [[Vector Calculus for Machine Learning]]
- [[Gradient Descent and Optimization]]
- [[Loss Functions]]
- [[Regularization]]
- [[Scikit-learn Implementation of Linear Models]]
