---
title: Data Preprocessing for Neural Networks
type: concept
tags:
- neural-networks
- data
aliases: []
sources:
- sources/module-1-linear-models.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

Raw data — structured (tables) or unstructured (images, audio, text) — must be converted
into a numeric feature matrix `X` (plus label vector `y`) before it can be fed into a
[[Linear Models as Neural Network Layers|linear layer]].

## Discussion

**Non-numerical (categorical) inputs:**
- *Nominal* (no order, e.g. color): **one-hot encoding** (one indicator column per
  category) or **dummy encoding** (one-hot with one column dropped to avoid redundancy).
- *Ordinal* (has order, e.g. Poor/Good/Very Good/Excellent): map directly to increasing
  integers (1,2,3,4).
- *Binary* (Yes/No): map to 0/1.

**Numeric inputs — rescaling:**
- **Standardization**: `z = (x − μ) / σ` — centers data to mean 0, std 1.
- **Min-max normalization**: `x_norm = (x − x_min) / (x_max − x_min)` — rescales to a
  fixed bounded range, usually [0,1].
- Choice of scaling affects **model convergence** during
  [[Gradient Descent and Optimization|gradient descent]].

**Unstructured data → feature extraction:**
- *Images*: flatten pixel grid `(h,w)` into a vector, then scale pixel values.
- *Audio*: Fourier analysis converts a waveform into a spectrogram image.
- *Text*: a text feature extractor converts text into a term-frequency vector (length =
  vocabulary size), which is then normalized.

## Related

- [[Module 1 - Linear Models]]
- [[Linear Models as Neural Network Layers]]
- [[Gradient Descent and Optimization]]
