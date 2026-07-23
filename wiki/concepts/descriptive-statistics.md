---
title: Descriptive Statistics
type: concept
tags:
- statistics
- foundations
aliases: []
sources:
- sources/module-1-the-basics.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

Descriptive statistics summarize a dataset's central tendency, variability, and
position, usually computed on a **sample** drawn from a larger **population** (sampling
+ inference lets you generalize sample stats back to the population).

## Discussion

**Central tendency**

- **Mean** — `μ = (1/N) Σ xᵢ` (population) or `x̄ = (1/n) Σ xᵢ` (sample). Sensitive to
  outliers.
- **Median** — the middle value once sorted; robust to outliers.
- **Mode** — the most frequent value; a dataset can be unimodal, multimodal, or have no
  mode.

**Variability**

- **Variance** — average squared deviation from the mean. Population: `σ² = (1/N) Σ (xᵢ
  − μ)²`. Sample: `s² = (1/(n−1)) Σ (xᵢ − x̄)²` (the `n−1` denominator, Bessel's
  correction, keeps the sample estimate unbiased).
- **Standard deviation** — `σ = √variance`, brings the units back to the original scale.

**Position**

- **Percentiles** — the value below which a given percentage of the data falls; rank of
  `x` is `(# values below x) / n × 100`.

**Shape**

- A **histogram** shows the frequency distribution of a dataset; fitting a smooth curve
  to it gives a model like the **normal (Gaussian) distribution** — see
  [[Probability Fundamentals]].
- **Skewness** measures asymmetry (Fisher-Pearson coefficient `g₁`). In a symmetric
  distribution mean = median = mode; in a positively-skewed one, mode < median < mean
  (long right tail), and vice versa for negative skew.

**Relationships between variables**

- Two variables are **independent** if one tells you nothing about the other;
  **dependent** if they do.
- **Correlation** `r` measures the strength and direction of a *linear* relationship:
  `r = Σ(xᵢ−x̄)(yᵢ−ȳ) / √(Σ(xᵢ−x̄)² Σ(yᵢ−ȳ)²)`, ranging from −1 (perfect negative) to +1
  (perfect positive); `r ≈ 0` doesn't rule out a non-linear relationship (e.g. a
  parabola can have `r = 0`).

## Related

- [[Module 1 - The Basics]]
- [[Probability Fundamentals]]
- [[Model Evaluation Metrics]]
